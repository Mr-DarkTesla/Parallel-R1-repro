"""Tiny Qwen3 CPU behavior/logp/replay/row-isolation and cost equivalence."""
import copy
import json
import sys
from pathlib import Path
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT/'work/experiments/rl-readiness-20261010'))
sys.path.insert(0, str(HERE.parent/'production-runner'))
import structured_replay as replay
from audit_semantics import make_case
from decoder import BatchedHFDecoder
from microbatch_decoder import MicrobatchedHFDecoder
from cohort_decoder import CohortDecoder


def main():
    torch.set_num_threads(2)
    torch.manual_seed(103)
    cfg = Qwen3Config(vocab_size=128, hidden_size=64, intermediate_size=128,
                      num_hidden_layers=3, num_attention_heads=4, num_key_value_heads=2,
                      head_dim=16, attention_dropout=0., pad_token_id=0)
    cfg._attn_implementation = 'sdpa'
    model = Qwen3ForCausalLM(cfg).eval()
    core = BatchedHFDecoder(model, replay)
    serial = MicrobatchedHFDecoder(model, replay, max_paths=2)
    cohort = CohortDecoder(core, max_rows=8, max_paths=2, gather_seconds=.02)
    case = make_case(4, None)
    paths = [c for c in case['calls'] if c['phase'] == 'path'][:4]
    bc = case['tags'][3]
    stops = [*case['tags'], 16]
    calls = []
    for episode in range(4):
        part = copy.deepcopy(paths)
        for row, call in enumerate(part):
            call['prompt_ids'] += [20+episode] * ((row+episode)%4)
            call.update(temperature=1., seed=211+row+episode*100)
        calls.append(part)
    budgets = [2, 3, 4, 6]
    def evaluate(collection, forced):
        jobs = []
        baselines = []
        baseline_stats = []
        for episode, part in enumerate(collection):
            targets = [[21+i]*(budgets[i]-1)+[bc] for i in range(4)] if forced else None
            options = {} if targets is None else dict(target_sequences=targets)
            baselines.append(serial.decode_many(part, budgets, stops, **options))
            baseline_stats.append(copy.deepcopy(serial.last_batch_stats))
            def job(client, part=part, options=options):
                result = client.decode_many(part, budgets, stops, **options)
                return result, copy.deepcopy(client.last_batch_stats)
            jobs.append(job)
        outputs = cohort.run(jobs)
        deltas = []
        replay_deltas = []
        for part, expected, (observed, stats), original_stats in zip(collection, baselines, outputs, baseline_stats):
            assert stats['physical_forward_calls'] == original_stats['physical_forward_calls']
            for call, before, after in zip(part, expected, observed):
                assert before[0] == after[0] and before[2] == after[2]
                deltas.extend(abs(a-b) for a,b in zip(before[1],after[1]))
                scored = dict(call, generated_ids=after[0])
                full, _ = replay.score_call(model, scored)
                replay_deltas.extend((full.detach().cpu()-torch.tensor(after[1])).abs().tolist())
        assert max(deltas) < 1e-5 and max(replay_deltas) < 1e-5
        return dict(forced=forced, max_logp_delta=max(deltas), max_replay_delta=max(replay_deltas),
                    baseline_episode_calls=[s['physical_forward_calls'] for s in baseline_stats],
                    episode_calls=[s['physical_forward_calls'] for _,s in outputs],
                    server_calls=sum(s['physical_forward_calls'] for s in cohort.server_batches),
                    server_rows=[s['kernel_batch_rows'] for s in cohort.server_batches]), outputs
    forced, original = evaluate(calls, True)
    sampled, _ = evaluate(calls, False)
    changed = copy.deepcopy(calls)
    changed[0][0]['prompt_ids'][-1] = 29
    _, altered = evaluate(changed, True)
    sibling_delta = max(abs(a-b) for before,after in zip(original[1:],altered[1:])
                        for x,y in zip(before[0],after[0]) for a,b in zip(x[1],y[1]))
    # Scheduling may change batch shapes, giving normal FP32 kernel rounding.
    assert sibling_delta < 1e-5, sibling_delta
    result = dict(passed=True, model='tiny-random-Qwen3-CPU-FP32', forced=forced, sampled=sampled,
                  cross_episode_perturbation_delta=sibling_delta,
                  gpu4b_parity_and_memory_not_proven=True, full_rollout_trace_integration_not_proven=True)
    (HERE/'cpu-cohort-proof.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
