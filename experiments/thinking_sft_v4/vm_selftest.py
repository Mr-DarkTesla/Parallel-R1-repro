"""GPU-VM self-test of the SFT data path and graph forward on the REAL model (default Qwen/Qwen3-4B at the pinned
revision, common.BASE_MODEL / BASE_REVISION). Exit code 1 on any failure.

    python vm_selftest.py [--data train.jsonl] [--rows 200] [--show 3]
    python vm_selftest.py --model Qwen/Qwen3-0.6B            # the 0.6B snapshot (its pinned revision is used)
    python vm_selftest.py --model /path/to/ckpt --revision ''  # a local directory

Checks: ensure_tags adds the eight tags as consecutive ids right after the base vocabulary, in contract.TAGS
order (tags.py: add_special_tokens appends at len(tokenizer)); for the Qwen3 vocabulary (len 151669, which the 4B
and 0.6B tokenizers share) that is 151669..151676 inside the padded 151936 embedding rows without a resize, and
the Qwen3 constants (<think> 151667, </think> 151668, <|im_end|> 151645) are checked too. Another tokenizer gets
its actual ids reported ([INFO]) instead of failing on those constants. Then: <think>, </think>, <|im_end|> and
the counts 2-4 are single tokens; the chat template ends with '<|im_start|>assistant\\n' for enable_thinking=True;
the transformers 4D-mask semantics; the first --rows JSONL rows tokenize (drop reasons printed, a few samples
rendered with no-loss tokens in [[...]]); the graph forward equals the independent references (exactness.py) in
fp32 (atol 1e-3) on the built-in row and on up to --exact-rows real parallel rows clipped to --max-exact-tokens
(exactness.clip_sample: first block + continuation; bounded so the fp32 4B references fit), and reports bf16 /
autocast deviations; one gradient-checkpointed bf16-autocast training step with the chunked loss is finite. All
forwards use the trainer's SDPA kernel choice (--sdpa-backend efficient: memory-efficient kernel only).
Memory: fp32 4B weights 16 GB + grads 16 GB (no optimizer); the long-row fit is sft_train.py --memory-report.
"""
import argparse
import json
import sys
import traceback
from itertools import islice
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exactness  # noqa: E402
import sft_data as D  # noqa: E402
import sft_train  # noqa: E402
from common import BASE_MODEL, contract, default_revision  # noqa: E402
from tags import ensure_tags  # noqa: E402

# Qwen3 vocabulary (shared by the 0.6B and 4B tokenizers): base length, padded embedding rows, control ids.
FIRST_TAG_ID = 151669
QWEN3_ROWS = 151936
QWEN3_IDS = {'<think>': 151667, '</think>': 151668, '<|im_end|>': 151645}
BUILTIN = (
    '<think>\nOkay, we need all real x with x^2 - 5x + 6 = 0 and then the sum of the roots.\n\n'
    '<Parallel>branches=3<Plan>methods\n1: factor the quadratic\n2: use the quadratic formula\n'
    '3: use Vieta directly\n</Plan><Path>1: x^2 - 5x + 6 = (x - 2)(x - 3), so x = 2 or x = 3 and the sum is 5.</Path>'
    '<Path>2: The discriminant is 25 - 24 = 1, so x = (5 +- 1)/2, giving 3 and 2; the sum is 5.</Path>'
    '<Path>3: By Vieta the sum of the roots is 5.</Path></Parallel><Summary> All three methods give a sum of 5.'
    '</Summary>\nLet me double check the product too.\n\n<Parallel>branches=2<Plan>verify\n1: product by Vieta\n'
    '2: product from the roots\n</Plan><Path>1: The product is 6.</Path><Path>2: 2 * 3 = 6, consistent.</Path>'
    '</Parallel><Summary> Both agree.</Summary>\n</think>\n\nThe sum of the roots is $\\boxed{5}$.<|im_end|>')
BUILTIN_PROMPT = 'Find the sum of all real solutions of x^2 - 5x + 6 = 0.'


class Checks:
    def __init__(self):
        self.failures = []

    def __call__(self, condition, name, detail=''):
        print(f'[{"PASS" if condition else "FAIL"}] {name}' + (f': {detail}' if detail else ''))
        if not condition:
            self.failures.append(name)
        return condition


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=BASE_MODEL)
    parser.add_argument('--revision', default=None,
                        help="HF revision (default: the pinned one for a known model id); '' for a local path")
    parser.add_argument('--data', type=Path, default=None)
    parser.add_argument('--rows', type=int, default=200)
    parser.add_argument('--show', type=int, default=3)
    parser.add_argument('--max-len', type=int, default=16384)
    parser.add_argument('--attn', default='sdpa', choices=('sdpa', 'eager'))
    parser.add_argument('--atol', type=float, default=1e-3)
    parser.add_argument('--max-exact-tokens', type=int, default=3072,
                        help='real rows are clipped to this many tokens for the fp32 exactness test')
    parser.add_argument('--exact-rows', type=int, default=2, help='real parallel rows in the exactness test')
    parser.add_argument('--sdpa-backend', choices=('efficient', 'auto'), default='efficient',
                        help='as sft_train: efficient = only the memory-efficient SDPA kernel on CUDA')
    args = parser.parse_args()
    check = Checks()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    check(device.type == 'cuda', 'cuda available')
    print(f'[INFO] sdpa backends: {sft_train.configure_sdpa(args.sdpa_backend, device.type == "cuda")}')
    try:
        check(True, 'transformers 4D-mask semantics', sft_train.check_transformers())
    except AssertionError as error:
        check(False, 'transformers 4D-mask semantics', str(error))

    revision = default_revision(args.model) if args.revision is None else (args.revision or None)
    print(f'model {args.model} revision {revision}')
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=revision, torch_dtype=torch.float32,
                                                 attn_implementation=args.attn)
    base_len = len(tokenizer)
    qwen3 = base_len == FIRST_TAG_ID
    kind = 'Qwen3 vocabulary' if qwen3 else 'NOT the Qwen3 vocabulary: ids are reported, Qwen3 constants not enforced'
    print(f'[INFO] base tokenizer length {base_len} ({kind}), embedding rows '
          f'{model.get_input_embeddings().weight.size(0)}')
    report = ensure_tags(tokenizer, model)
    print(json.dumps({k: v for k, v in report.items() if k != 'token_ids'}, indent=1))
    ids = [report['tag_ids'][tag] for tag in contract.TAGS]
    check(ids == list(range(base_len, base_len + 8)), f'tag ids {base_len}..{base_len + 7} (after the base vocab) '
          f'in TAGS order', ids)
    print(f'[INFO] tag ids {dict(zip(contract.TAGS, ids))}; Qwen3 expectation 151669..151676: '
          f'{"match" if ids == list(range(FIRST_TAG_ID, FIRST_TAG_ID + 8)) else "DIFFERENT"}')
    check(report['status'] == 'initialized', 'tags added and initialized', report['status'])
    if qwen3:
        check(not report['resized'] and report['rows'] == QWEN3_ROWS, 'tags fit the padded rows (151936)',
              f'resized={report["resized"]} rows={report["rows"]}')
    else:
        print(f'[INFO] rows {report["rows_before"]} -> {report["rows"]} (resized={report["resized"]})')
    # computed from the model: ensure_tags reports 'tied' only when it initialized the rows
    output = model.get_output_embeddings()
    tied = output is None or output.weight.data_ptr() == model.get_input_embeddings().weight.data_ptr()
    check(tied, 'tied embeddings')
    check(report['max_offdiag_cos'] < 0.99, 'tag rows distinct', f'max cos {report["max_offdiag_cos"]:.3f}')
    tokens = contract.token_ids(tokenizer)
    im_end = tokenizer.encode('<|im_end|>', add_special_tokens=False)
    check(len(im_end) == 1, '<|im_end|> single token', im_end)
    actual = {'<think>': tokens['<think>'], '</think>': tokens['</think>'], '<|im_end|>': im_end[0]}
    if qwen3:
        check(actual == QWEN3_IDS, 'Qwen3 control ids <think>/</think>/<|im_end|>', actual)
    else:
        print(f'[INFO] control ids {actual} (Qwen3: {QWEN3_IDS})')
    counts = contract.count_ids(tokenizer)
    check(len(counts) == 3, 'counts 2-4 single tokens', counts)
    print('branches= ->', contract.branches_ids(tokenizer), [tokenizer.decode([i]) for i in contract.branches_ids(tokenizer)])
    for k in range(1, 5):
        prefix = contract.path_prefix_ids(tokenizer, k)
        check(tokenizer.decode(prefix) == f'{k}:', f'path prefix {k}', prefix)
    for tag in contract.TAGS:
        check(tokenizer.decode([report['tag_ids'][tag]]) == tag, f'decode {tag}')
    joint = tokenizer.encode('<Parallel>branches=2<Plan>', add_special_tokens=False)
    check(joint[0] == report['tag_ids']['<Parallel>'] and joint[-1] == report['tag_ids']['<Plan>'],
          'tags split out of running text', joint)
    prompt = D.prompt_text(tokenizer, BUILTIN_PROMPT)
    check(prompt.endswith(D.ASSISTANT_PREFIX) and '<think>' not in prompt, 'chat template (enable_thinking=True)',
          repr(prompt[-60:]))
    off = tokenizer.apply_chat_template([{'role': 'user', 'content': 'q'}], tokenize=False, add_generation_prompt=True,
                                        enable_thinking=False)
    check(off.endswith('<think>\n\n</think>\n\n'), 'chat template is Qwen3 (enable_thinking=False prefills)')

    vocab = D.Vocab(tokenizer)
    samples = [D.tokenize_row(D.make_row('builtin', 'builtin', BUILTIN_PROMPT, BUILTIN), vocab)]
    print(D.render(samples[0], tokenizer))
    if args.data:
        rows = list(islice(D.read_jsonl(args.data), args.rows))
        data, stats = D.build_dataset(rows, vocab, args.max_len)
        print(json.dumps({k: v for k, v in stats.items()}, indent=1))
        check(stats['invalid'] == 0, f'first {len(rows)} data rows valid', stats['dropped'])
        for s in data[:args.show]:
            text = D.render(s, tokenizer)
            print(f'--- {s["id"]} ({s["mode"]}, {s["length"]} tokens, {s["n_loss"]} in loss)\n'
                  f'{text if len(text) < 6000 else text[:3000] + " ..... " + text[-2500:]}')
        clipped = [exactness.clip_sample(s, args.max_exact_tokens) for s in data if s['mode'] == 'parallel']
        clipped = [s for s in clipped if s is not None]
        print(f'[INFO] {len(clipped)} real parallel rows have their first block within {args.max_exact_tokens} '
              f'tokens; {min(len(clipped), args.exact_rows)} used for exactness')
        samples += clipped[:args.exact_rows]

    model.to(device).eval()
    pad = vocab.pad_id
    for s in samples:
        try:
            result = exactness.check_sample(model, s, pad)
            ok = all(result[key] < args.atol for key in ('path', 'kv', 'eager')) and result['causal_control'] > 1e-2
            check(ok, f'fp32 exactness {s["id"]} ({s["length"]} tokens)', json.dumps(result))
        except Exception:
            traceback.print_exc()
            check(False, f'fp32 exactness {s["id"]}')
    s = samples[0]
    fp32_logits = exactness.graph_logits(model, s, pad)
    with torch.no_grad():
        batch = D.collate([s], pad, dtype=torch.bfloat16, device=device)
        with torch.autocast(device_type=device.type, dtype=torch.bfloat16):
            autocast_logits = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                                    position_ids=batch['position_ids'], use_cache=False).logits[0].float()
    diff = (autocast_logits - fp32_logits).abs().max().item()
    check(torch.isfinite(autocast_logits).all().item() and diff < 1.0, 'bf16 autocast graph forward',
          f'max |diff| vs fp32 {diff:.4f}')

    # one gradient-checkpointed autocast training step on fp32 weights (as sft_train runs)
    model.train()
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    batch = D.collate(samples[:2] if len(samples) > 1 else samples, pad, dtype=torch.bfloat16, device=device)
    with torch.autocast(device_type=device.type, dtype=torch.bfloat16):
        losses, _ = sft_train.token_losses(model, batch, chunk=512)
    losses.mean().backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1e9).item()
    check(torch.isfinite(losses).all().item() and 0 < norm < float('inf'), 'autocast + grad-ckpt train step',
          f'loss {losses.mean().item():.4f} grad norm {norm:.3f}')
    model.zero_grad(set_to_none=True)
    model.gradient_checkpointing_disable()

    model.to(torch.bfloat16).eval()
    for s in samples[:1]:
        result = exactness.check_sample(model, s, pad, brute_force=False)
        print(f'[INFO] pure bf16 deviations {s["id"]}: {json.dumps(result)}')
    if check.failures:
        print(f'{len(check.failures)} FAILED: {check.failures}')
        sys.exit(1)
    print('ALL PASSED')


if __name__ == '__main__':
    main()
