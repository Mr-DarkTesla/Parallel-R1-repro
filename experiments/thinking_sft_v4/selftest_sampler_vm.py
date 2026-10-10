"""VM self-test of graph_sampler.py on the real checkpoint (run before eval_graph.py).

  python selftest_sampler_vm.py --model CKPT            # HF exactness + vLLM API checks
  python selftest_sampler_vm.py --model CKPT --no-vllm  # HF only

1. tokenizer: tags are single ids (Qwen3: 151669..151676 in contract.TAGS order), EOS ids, count/branches ids.
2. HF exactness (float32, TF32 off): a forced fork on 3 prompts, greedy; every sampled token's logits (branches,
   summary, main after the block) equal a full-sequence forward of the final ids with the contract graph mask and
   positions. Fails above --atol.
3. vLLM 0.8.5 API (the parts graph_sampler relies on): allowed_token_ids restricts COUNT, logit_bias is applied,
   the stop token is the last output id, a per-request seed reproduces, the node suppression holds in samples;
   greedy agreement with HF bf16 is reported (informational: kernels differ).
4. End to end: a few trajectories with vLLM (causal stages) + HF (graph stages).
Prints one JSON line per check and exits non-zero on a failure.
"""
import argparse
import json
import sys
from collections import Counter

import torch

import graph_sampler as gs
from common import contract

PROMPTS = ['What is 17 * 23?', 'How many positive divisors does 360 have?',
           'Find the remainder when 2^100 is divided by 7.']
FAILED = []


def check(name, ok, **info):
    print(json.dumps(dict(check=name, ok=bool(ok), **info), default=str), flush=True)
    if not ok:
        FAILED.append(name)


class Recording:
    graph = True

    def __init__(self, backend):
        self.backend, self.log = backend, []

    def generate(self, requests, sampling):
        results = self.backend.generate(requests, sampling)
        self.log.extend(zip(requests, results))
        return results


def forced(tokenizer):
    enc = lambda text: tokenizer.encode(text, add_special_tokens=False)  # noqa: E731
    table = {('main', 1): '<think>\nLet me split this into two parts.\n\n<Parallel>', ('count', 1): '2',
             ('plan', 1): 'decompose\n1: compute directly\n2: check another way\n</Plan>'}
    return lambda index, stage, block, path: enc(table[stage, block]) if (stage, block) in table else None


def full_logits(model, ids, spans):
    device = next(model.parameters()).device
    allowed = contract.graph_attention_mask(len(ids), spans, device=device)
    mask = torch.zeros(1, 1, len(ids), len(ids), device=device).masked_fill(~allowed, torch.finfo(torch.float32).min)
    positions = torch.tensor([contract.graph_positions(len(ids), spans)], device=device)
    with torch.no_grad():
        return model(input_ids=torch.tensor([ids], device=device), attention_mask=mask,
                     position_ids=positions).logits[0].float().cpu()


def call_position(ids, request, tokens, path_open):
    """Index in the serialized ids of a call's first sampled token (branches: after their own <Path> i:)."""
    if request.node == contract.PATH:
        cut = len(request.context) - 1 - request.context[::-1].index(path_open)
        prefix, own = request.context[:cut], request.context[cut:]
        if ids[:len(prefix)] != prefix:
            return None
        for index in range(len(prefix), len(ids) - len(own) + 1):
            body = index + len(own)
            if ids[index:body] == own and ids[body:body + len(tokens) - 1] == tokens[:-1]:
                return body
        return None
    start = len(request.context)
    if ids[:start] != request.context or ids[start:start + len(tokens) - 1] != tokens[:-1]:
        return None
    return start


def exactness(args, tokenizer):
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    from transformers import AutoModelForCausalLM
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float32,
                                                 attn_implementation='sdpa').to(device).eval()
    backend = Recording(gs.HFBackend(model, record_logits=True))
    sampler = gs.GraphSampler(tokenizer, backend, sampling=gs.Sampling(temperature=0.0), max_blocks=1, budget=400,
                              branch_cap=96, force=forced(tokenizer))
    reports = sampler.generate(PROMPTS)
    path_open = contract.token_ids(tokenizer)['<Path>']
    serialized = [(r['prompt_ids'] + r['token_ids'], gs.serialized_spans(r)) for r in reports]
    logits = [full_logits(model, ids, spans) for ids, spans in serialized]
    worst, counted = 0.0, Counter()
    for request, result in backend.log:
        for (ids, _), full in zip(serialized, logits):
            position = call_position(ids, request, result.tokens, path_open)
            if position is None:
                continue
            want = full[position - 1:position - 1 + len(result.tokens)]
            worst = max(worst, (result.logits - want).abs().max().item())
            counted['graph' if request.spans else 'causal'] += 1
            break
        else:
            check('exactness_locate', False, node=request.node)
    check('hf_graph_exactness', worst <= args.atol and counted['graph'] >= 3, max_abs_diff=worst, calls=dict(counted),
          statuses=[r['status'] for r in reports], blocks=[r['blocks'] for r in reports])
    del model
    torch.cuda.empty_cache() if torch.cuda.is_available() else None


def vllm_checks(args, tokenizer):
    ids, counts = contract.token_ids(tokenizer), contract.count_ids(tokenizer)
    backend = gs.VLLMBackend(args.model, gpu_memory_utilization=args.gpu_memory_utilization,
                             max_model_len=args.max_model_len)
    hot = gs.Sampling(temperature=1.0, top_p=1.0, top_k=0)
    context = gs.chat_prompt_ids(tokenizer, PROMPTS[0])
    fork = context + tokenizer.encode('<think>\nok\n<Parallel>branches=', add_special_tokens=False)
    count = [gs.Request(fork, contract.COUNT, (), 1, s, contract.sampling_constraint(contract.COUNT, ids, counts))
             for s in range(64)]
    got = [r.tokens for r in backend.generate(count, hot)]
    check('vllm_allowed_token_ids', all(len(t) == 1 and t[0] in counts for t in got),
          histogram=dict(Counter(t[0] for t in got if t)))
    target = tokenizer.encode(' banana', add_special_tokens=False)[0]
    push = gs.Request(context, contract.MAIN_CLOSED, (), 3, 0, dict(logit_bias={target: 100.0}))
    check('vllm_logit_bias', backend.generate([push], hot)[0].tokens == [target] * 3)
    stop = gs.Request(context, contract.MAIN_CLOSED, (target,), 5, 0, dict(logit_bias={target: 100.0}))
    check('vllm_stop_token_kept', backend.generate([stop], hot)[0].tokens == [target])
    seeded = [gs.Request(context, contract.MAIN_OPEN, tuple(gs.eos_ids(tokenizer)), 48, 1234,
                         contract.sampling_constraint(contract.MAIN_OPEN, ids, counts)) for _ in range(2)]
    a, b = backend.generate(seeded, gs.Sampling())
    check('vllm_seed_reproducible', a.tokens == b.tokens)
    suppressed = {}
    for node, tail in ((contract.PLAN, '<Plan>'), (contract.PATH, '<Path>1:'), (contract.SUMMARY, '<Summary>')):
        ctx = context + tokenizer.encode('<think>\nok\n<Parallel>branches=2' + tail, add_special_tokens=False)
        requests = [gs.Request(ctx, node, (), 64, s, contract.sampling_constraint(node, ids, counts)) for s in range(8)]
        banned = {ids[t] for t in contract.suppressed_tokens(node)}
        suppressed[node] = sum(t in banned for r in backend.generate(requests, hot) for t in r.tokens)
    check('vllm_node_suppression', not any(suppressed.values()), hits=suppressed)

    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16,
                                                 attn_implementation='sdpa').to('cuda').eval()
    hf = gs.HFBackend(model)
    greedy = gs.Sampling(temperature=0.0)
    requests = [gs.Request(gs.chat_prompt_ids(tokenizer, p), contract.MAIN_OPEN, tuple(gs.eos_ids(tokenizer)), 64, 0,
                           contract.sampling_constraint(contract.MAIN_OPEN, ids, counts)) for p in PROMPTS]
    agree = []
    for x, y in zip(backend.generate([gs.Request(**vars(r)) for r in requests], greedy),
                    hf.generate(requests, greedy)):
        agree.append(next((i for i, (u, v) in enumerate(zip(x.tokens, y.tokens)) if u != v),
                          min(len(x.tokens), len(y.tokens))))
    check('vllm_hf_greedy_agreement_info', True, first_divergence=agree)

    sampler = gs.GraphSampler(tokenizer, backend, hf, sampling=gs.Sampling(), max_blocks=1, budget=args.budget)
    reports = sampler.generate(PROMPTS * 2, seeds=range(6))
    check('end_to_end', all(r['status'] for r in reports), statuses=[r['status'] for r in reports],
          forked=[r['forked'] for r in reports], T=[r['T'] for r in reports], D=[r['D'] for r in reports])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--no-vllm', action='store_true')
    parser.add_argument('--atol', type=float, default=2e-3)
    parser.add_argument('--budget', type=int, default=2048)
    parser.add_argument('--gpu-memory-utilization', type=float, default=0.35)
    parser.add_argument('--max-model-len', type=int, default=8192)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    ids = contract.token_ids(tokenizer)
    tags = [ids[t] for t in contract.TAGS]
    qwen = tokenizer.convert_tokens_to_ids('<think>') == 151667
    check('tokenizer_tags', not qwen or tags == list(range(151669, 151677)), tags=tags, qwen=qwen,
          eos=gs.eos_ids(tokenizer), counts=contract.count_ids(tokenizer), branches=contract.branches_ids(tokenizer),
          contract_sha256=contract.SHA256)
    exactness(args, tokenizer)
    if not args.no_vllm:
        vllm_checks(args, tokenizer)
    print(json.dumps(dict(failed=FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == '__main__':
    main()
