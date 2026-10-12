"""Computational width/depth and actual decoder/replay parity audit; CPU or GPU."""
import argparse
import hashlib
import json
import os
from contextlib import nullcontext
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3Config, Qwen3ForCausalLM
from structured_replay import score_call, score_trajectory, decoder_logprobs
from source.parallel_structure import attention, layout

HERE = Path(__file__).resolve().parent


def make_case(width, tokenizer=None, prompt_extra=0):
    if tokenizer:
        enc = lambda s: tokenizer.encode(s, add_special_tokens=False)
        tags = [enc(s)[0] for s in ['<Parallel>', '</Parallel>', '<Path>', '</Path>']]
        summary_open, summary_close = enc('<Summary>')[0], enc('</Summary>')[0]
        pad = tokenizer.pad_token_id
        prefix = enc('Instruction: Solve carefully with independent counted paths.\n\nProblem: Compute 2+3.\n\nSolution:\n')
        prefix += enc('Context. ' * prompt_extra)
    else:
        enc = lambda s: [30 + ord(s[i]) % 60 for i in range(0, len(s), 8)]
        tags = [10, 11, 12, 13]
        summary_open, summary_close, pad = 14, 15, 0
        prefix = [1, 2, 3] + [4] * prompt_extra
    ids = list(prefix)
    origin = len(prefix)
    calls, action_mask, phase_cost, groups = [], [], [], []
    def add(phase, target, prompt=None):
        calls.append(dict(prompt_ids=list(ids if prompt is None else prompt), generated_ids=list(target),
                          phase=phase, temperature=.8, structure_start=origin, structure_tags=tags,
                          pad_id=pad, response_start=len(action_mask)))
        ids.extend(target); action_mask.extend([1] * len(target))
    def inject(tokens):
        ids.extend(tokens); action_mask.extend([0] * len(tokens))
    for round_index in range(4):
        main = enc('Plan: Calculate independent pieces.\n') + [tags[0]]
        add('main', main); phase_cost.append(len(main))
        header = enc(str(width) + '\n')
        add('width', header); phase_cost.append(len(header))
        shared = list(ids); spans, costs = [], []
        for i in range(width):
            opening = [tags[2]] + enc(str(i + 1) + '\n')
            path = enc('Result = 5. ' * (1 if i < width-1 else 3)) + [tags[3]]
            s = len(ids); inject(opening)
            add('path', path, shared + opening)
            spans.append((s, len(ids))); costs.append(len(path))
        groups.append(spans); phase_cost.append(max(costs))
        inject([tags[1], summary_open])
        summary = enc('Combine results = 5.\n') + [summary_close]
        add('summary', summary); phase_cost.append(len(summary))
    add('main', enc('Final Answer: 5.'))
    phase_cost.append(len(calls[-1]['generated_ids']))
    return dict(ids=ids, calls=calls, mask=action_mask, origin=origin, tags=tags,
                pad=pad, groups=groups, F=sum(phase_cost), T=sum(action_mask))


def structural_check(case):
    ids = torch.tensor(case['ids'])
    positions, spans = layout(ids, case['origin'], case['tags'], case['pad'])
    allowed = attention(ids, case['origin'], case['tags'], case['pad'])
    assert len(spans) == 4
    assert allowed.diagonal().all(), 'self visibility'
    assert not allowed.triu(1).any(), 'future leakage'
    for round_index, paths in enumerate(spans):
        for i, (s, e) in enumerate(paths):
            assert allowed[s:e, :paths[0][0]].all(), 'common context missing'
            assert allowed[s:e, s:e].equal(torch.ones(e-s, e-s, dtype=torch.bool).tril())
            assert positions[s] == positions[paths[0][0]]
            for j, (t, u) in enumerate(paths):
                if i != j:
                    assert not allowed[s:e, t:u].any(), 'sibling leakage'
        closing = paths[-1][1]
        assert int(positions[closing]) == max(int(positions[e-1]) for s,e in paths) + 1
        assert allowed[closing:, paths[0][0]:closing].all(dim=1)[0], 'summary cannot read all paths'
        if round_index:
            previous_end = spans[round_index-1][-1][1]
            assert allowed[paths[0][0], :previous_end].all(), 'next round cannot read prior round'
    total = sum(len(c['generated_ids']) for c in case['calls'])
    assert total == case['T'] and case['F'] < total
    padded_mask = case['mask'] + [0] * 19
    coverage = [0] * len(padded_mask)
    for call in case['calls']:
        s = call['response_start']; n = len(call['generated_ids'])
        coverage[s:s+n] = [1] * n
    assert coverage == padded_mask, 'forced/pad sampled-mask policy'
    return dict(tokens=len(ids), sampled=total, forced=len(case['mask'])-total,
                rounds=4, width=len(spans[0]), F=case['F'], T=total)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model'); p.add_argument('--device', default='cpu')
    p.add_argument('--output', default=str(HERE/'cpu-proof.json'))
    p.add_argument('--dtype', choices=['fp32', 'bf16'], default='fp32')
    p.add_argument('--autocast-bf16', action='store_true')
    a = p.parse_args()
    torch.set_num_threads(2)
    torch.manual_seed(20261010)
    tokenizer = None
    if a.model:
        tokenizer = AutoTokenizer.from_pretrained(a.model, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(a.model, local_files_only=True,
                  torch_dtype=torch.float32 if a.dtype=='fp32' else torch.bfloat16,
                  attn_implementation='sdpa').to(a.device).eval()
    else:
        config = Qwen3Config(vocab_size=128, hidden_size=64, intermediate_size=128,
                     num_hidden_layers=3, num_attention_heads=4, num_key_value_heads=2,
                     head_dim=16, attention_dropout=0., pad_token_id=0)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).eval()
    results = []
    structural_results = []
    toler = .06 if a.dtype=='bf16' or a.autocast_bf16 else 3e-4 if a.model else 2e-5
    for width in [2, 3, 4, 6, 8]:
        case = make_case(width, tokenizer)
        structural_results.append(structural_check(case))
        # GPU: sample key boundaries in every width and all four rounds.
        selected = case['calls']
        if a.model:
            selected = [c for j,c in enumerate(selected) if c['phase'] in ['summary', 'width'] or
                        c['phase']=='main' or c['phase']=='path' and c['prompt_ids'][-2:] == case['calls'][2]['prompt_ids'][-2:]]
        for call in selected:
            # Limit targets for expensive live checkpoint proof, keeping real prefix.
            actual = dict(call, generated_ids=call['generated_ids'][:8]) if a.model else call
            autocast = torch.autocast(device_type='cuda', dtype=torch.bfloat16) if a.autocast_bf16 else nullcontext()
            with torch.no_grad(), autocast:
                recomputed, _ = score_call(model, actual)
                reference, forwards = decoder_logprobs(model, actual)
            difference = (recomputed.cpu()-torch.tensor(reference)).abs()
            delta = float(difference.max()) if len(difference) else 0.
            results.append(dict(width=width, phase=call['phase'], target_count=len(actual['generated_ids']),
                                maximum_abs_logp_delta=delta, decoder_forwards=forwards))
            assert delta < toler, (width, call['phase'], delta, toler)
        if not a.model:
            logp, entropy = score_trajectory(model, case['calls'], case['mask']+[0]*19,
                                            calculate_entropy=True)
            mask = torch.tensor(case['mask']+[0]*19, dtype=torch.bool)
            assert (logp[~mask]==0).all() and (entropy[~mask]==0).all()
            (-logp[mask].mean()).backward()
            assert all(torch.isfinite(x.grad).all() for x in model.parameters() if x.grad is not None)
            assert model.model.embed_tokens.weight.grad.abs().sum()>0
            model.zero_grad(set_to_none=True)
    report = dict(passed=True, model=a.model or 'synthetic tiny Qwen3 SDPA FP32',
                   dtype=a.dtype, autocast_bf16=a.autocast_bf16, device=a.device, structural_cases=structural_results,
                   call_parity=results, maximum_abs_logp_delta=max(r['maximum_abs_logp_delta'] for r in results),
                   tolerance=toler, total_calls=len(results),
                   actual_decoder_forward_proof=True, training_launch_ready=False,
                   remaining='Distributed actor and weight synchronization smoke still required',
                   source_sha256={str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()
                       for f in [HERE/'structured_replay.py', HERE/'source/parallel_structure.py', Path(__file__)]})
    Path(a.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['passed','maximum_abs_logp_delta','total_calls','training_launch_ready']}))


if __name__=='__main__':
    main()
