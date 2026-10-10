"""GPU-VM self-test of the SFT data path and graph forward on the REAL Qwen3-0.6B. Exit code 1 on any failure.

    python vm_selftest.py [--data sft_train.jsonl] [--rows 200] [--show 3] [--model Qwen/Qwen3-0.6B]

Checks: ensure_tags gives the eight tags ids 151669..151676 in contract.TAGS order without a resize; <think>,
</think>, <|im_end|>, the counts 2-4 are single tokens; the chat template ends with '<|im_start|>assistant\\n'
for enable_thinking=True; the transformers 4D-mask semantics; the first --rows JSONL rows tokenize (drop reasons
printed, a few samples rendered with no-loss tokens in [[...]]); the graph forward equals the independent
references (exactness.py) in fp32 (atol 1e-3) and reports bf16 / autocast deviations; one gradient-checkpointed
bf16-autocast training step is finite.
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
from common import contract  # noqa: E402
from tags import ensure_tags  # noqa: E402

REVISION = 'c1899de289a04d12100db370d81485cdf75e47ca'
FIRST_TAG_ID = 151669
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
    parser.add_argument('--model', default='Qwen/Qwen3-0.6B')
    parser.add_argument('--revision', default=REVISION, help="'' for a local --model path")
    parser.add_argument('--data', type=Path, default=None)
    parser.add_argument('--rows', type=int, default=200)
    parser.add_argument('--show', type=int, default=3)
    parser.add_argument('--max-len', type=int, default=8192)
    parser.add_argument('--attn', default='sdpa', choices=('sdpa', 'eager'))
    parser.add_argument('--atol', type=float, default=1e-3)
    parser.add_argument('--max-exact-tokens', type=int, default=2048, help='skip longer data rows in the exactness test')
    args = parser.parse_args()
    check = Checks()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    check(device.type == 'cuda', 'cuda available')
    try:
        check(True, 'transformers 4D-mask semantics', sft_train.check_transformers())
    except AssertionError as error:
        check(False, 'transformers 4D-mask semantics', str(error))

    revision = args.revision or None
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=revision, torch_dtype=torch.float32,
                                                 attn_implementation=args.attn)
    check(len(tokenizer) == FIRST_TAG_ID, 'base tokenizer length', len(tokenizer))
    report = ensure_tags(tokenizer, model)
    print(json.dumps({k: v for k, v in report.items() if k != 'token_ids'}, indent=1))
    ids = [report['tag_ids'][tag] for tag in contract.TAGS]
    check(ids == list(range(FIRST_TAG_ID, FIRST_TAG_ID + 8)), 'tag ids 151669..151676 in TAGS order', ids)
    check(report['status'] == 'initialized' and not report['resized'] and report['rows'] == 151936,
          'tags fit the padded rows', f'{report["status"]} rows={report["rows"]}')
    check(report['tied'], 'tied embeddings')
    check(report['max_offdiag_cos'] < 0.99, 'tag rows distinct', f'max cos {report["max_offdiag_cos"]:.3f}')
    tokens = contract.token_ids(tokenizer)
    check(tokens['<think>'] == 151667 and tokens['</think>'] == 151668, '<think>/</think> ids',
          (tokens['<think>'], tokens['</think>']))
    check(tokenizer.encode('<|im_end|>', add_special_tokens=False) == [151645], '<|im_end|> single token')
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
        parallel = [s for s in data if s['mode'] == 'parallel' and s['length'] <= args.max_exact_tokens]
        samples += parallel[:2]

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
        losses, _ = sft_train.token_losses(model, batch)
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
