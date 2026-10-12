"""Bounded actual Base FP32 batch parity, physical-count and latency audit.

Frozen real trace branches benchmark production shapes; synthetic four-round
contexts additionally cover width8 and uneven prefixes/long path termination.
No optimizer, no training writes, no source mutation.
"""
import argparse
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'frozen'))
import structured_replay as replay
from audit_semantics import make_case
from decoder import BatchedHFDecoder
from rollout import HFDecoder


@torch.inference_mode()
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--device', default='cuda')
    p.add_argument('--cases', default=str(HERE/'frozen-trace-cases.json'))
    p.add_argument('--output', default=str(HERE/'gpu-proof.json'))
    args = p.parse_args()
    torch.set_num_threads(2)
    torch.set_float32_matmul_precision('highest')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.manual_seed(103)
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, local_files_only=True,
            torch_dtype=torch.float32, attn_implementation='sdpa').to(args.device).eval()
    decoder = BatchedHFDecoder(model, replay, args.device)
    serial = HFDecoder(model, replay, args.device)
    frozen = json.loads(Path(args.cases).read_text())
    cases = list(frozen['cases'])
    tag_ids = [tokenizer.encode(s, add_special_tokens=False)[0]
               for s in ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']]
    stop_ids = [*tag_ids, int(tokenizer.eos_token_id)]
    ordinary = tokenizer.encode('result ', add_special_tokens=False)[0]
    for width in [2, 4, 8]:
        trace = make_case(width, tokenizer)
        paths = [c for c in trace['calls'] if c['phase']=='path']
        for round_index in range(4):
            calls = copy.deepcopy(paths[round_index*width:(round_index+1)*width])
            lengths = [16, 24, 32, 48, 64, 96, 112, 128][:width]
            for row, call in enumerate(calls):
                call['prompt_ids'] += [ordinary]*(row%4)
                call['temperature'], call['seed'] = 1., 17+row
                call['generated_ids'] = [ordinary]*(lengths[row]-1) + [tag_ids[3]]
            cases.append(dict(kind='synthetic_four_round_long_unequal', width=width,
                              round=round_index+1, calls=calls))
    # Tiny real workload warmup, excluded from reported latency counts.
    first = cases[0]['calls'][0]
    decoder.decode_many([first], 2, stop_ids,
                        target_sequences=[first['generated_ids'][:2]])
    torch.cuda.synchronize()
    records, all_deltas, cache_deltas, prefix_deltas = [], [], [], []
    original_forward = model.forward
    physical_shapes = []

    def tracked(*a, **kw):
        physical_shapes.append(list(kw['input_ids'].shape))
        return original_forward(*a, **kw)

    model.forward = tracked
    for index, case in enumerate(cases):
        calls = copy.deepcopy(case['calls'])
        targets = [list(c['generated_ids']) for c in calls]
        width = len(calls)
        for call in calls:
            call['temperature'] = 1.
        physical_shapes.clear()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        started = time.perf_counter()
        outputs = decoder.decode_many(calls, max(map(len, targets)), stop_ids,
                                      target_sequences=targets)
        torch.cuda.synchronize()
        batch_seconds = time.perf_counter()-started
        batch_peak = torch.cuda.max_memory_allocated()
        stats = copy.deepcopy(decoder.last_batch_stats)
        actual_shapes = list(physical_shapes)
        assert len(actual_shapes) == stats['physical_forward_calls'] == max(map(len, targets))
        assert all(r[0] == t for r,t in zip(outputs, targets))
        physical_shapes.clear()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
        started = time.perf_counter()
        references = [replay.decoder_logprobs(model, dict(c, generated_ids=t))[0]
                      for c,t in zip(calls, targets)]
        torch.cuda.synchronize()
        serial_seconds = time.perf_counter()-started
        serial_peak = torch.cuda.max_memory_allocated()
        serial_physical = len(physical_shapes)
        assert serial_physical == sum(map(len, targets))
        case_delta, case_cache_delta = [], []
        for call, target, (_, old, _), reference in zip(calls, targets, outputs, references):
            full, _ = replay.score_call(model, dict(call, generated_ids=target))
            dif = (full.cpu()-torch.tensor(old)).abs().tolist()
            cached = (torch.tensor(reference)-torch.tensor(old)).abs().tolist()
            case_delta.extend(dif)
            case_cache_delta.extend(cached)
            all_deltas.extend(dif)
            cache_deltas.extend(cached)
            prefix_deltas.append(dif[0])
        row = {k:v for k,v in case.items() if k!='calls'}
        row.update(batch_seconds=batch_seconds, serial_seconds=serial_seconds,
                   serial_over_batch_wall_ratio=serial_seconds/batch_seconds,
                   batch_peak_allocated_bytes=batch_peak, serial_peak_allocated_bytes=serial_peak,
                   physical_model_forward_calls=stats['physical_forward_calls'],
                   serial_physical_model_forward_calls=serial_physical,
                   real_prefix_lengths=[len(c['prompt_ids']) for c in calls],
                   target_lengths=list(map(len, targets)),
                   maximum_abs_logp_delta=max(case_delta),
                   max_batch_vs_serial_cache_logp_delta=max(case_cache_delta),
                   actual_forward_shapes=actual_shapes, **stats)
        records.append(row)
        print(json.dumps({k:row[k] for k in ['kind', 'width', 'batch_seconds', 'serial_seconds',
                  'maximum_abs_logp_delta', 'physical_forward_calls', 'serial_physical_model_forward_calls']}), flush=True)
    # Production sampling parity, same seeded RNG streams and stopping controls.
    sample_proof = []
    for width in [2, 4, 8]:
        calls = copy.deepcopy(next(c['calls'] for c in cases if len(c['calls'])==width))
        for i, call in enumerate(calls):
            call['seed'], call['temperature'] = 900+i, 1.
        budgets = [4+i%4 for i in range(width)]
        many = decoder.decode_many(calls, budgets, stop_ids)
        ones = [serial(c,n,stop_ids) for c,n in zip(calls,budgets)]
        same = all(a[0]==b[0] for a,b in zip(many,ones))
        delta = max(abs(x-y) for a,b in zip(many,ones) for x,y in zip(a[1],b[1]))
        sample_proof.append(dict(width=width, same_raw_actions=same, max_abs_logp_delta=delta))
        assert same, sample_proof[-1]
    tensor = torch.tensor(all_deltas)
    metrics = dict(maximum_abs_logp_delta=float(tensor.max()), mean_abs_logp_delta=float(tensor.mean()),
                   p95_abs_logp_delta=float(tensor.quantile(.95)),
                   maximum_batched_vs_serial_cache_logp_delta=max(cache_deltas),
                   maximum_first_action_logp_delta=max(prefix_deltas))
    passed = metrics['maximum_abs_logp_delta']<=.01 and metrics['mean_abs_logp_delta']<=.002 and metrics['p95_abs_logp_delta']<=.005
    source = [HERE/'decoder.py', Path(__file__), Path(args.cases), *(HERE/'frozen').rglob('*.py')]
    report = dict(passed=passed, model=args.model, device=args.device, dtype='FP32',
                  tf32=False, frozen_trace_source_sha256=frozen['source_sha256'],
                  target_count=len(all_deltas), **metrics, cases=records, sampling_proof=sample_proof,
                  numeric_gate=dict(max=.01, mean=.002, p95=.005),
                  total_batch_seconds=sum(r['batch_seconds'] for r in records),
                  total_serial_seconds=sum(r['serial_seconds'] for r in records),
                  physical_total=sum(r['physical_forward_calls'] for r in records),
                  serial_physical_total=sum(r['serial_physical_model_forward_calls'] for r in records),
                  prefill_total=sum(r['prefill_forward_calls'] for r in records),
                  peak_batch_allocated_bytes=max(r['batch_peak_allocated_bytes'] for r in records),
                  inactive_dummy_compute_included=True, warmup_excluded=True,
                  latency_is_single_gpu_decode_only=True, production_integration_review_required=True,
                  source_sha256={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source})
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['passed', 'target_count', 'maximum_abs_logp_delta',
        'mean_abs_logp_delta', 'p95_abs_logp_delta', 'total_batch_seconds', 'total_serial_seconds',
        'physical_total', 'serial_physical_total', 'peak_batch_allocated_bytes']}), flush=True)
    if not passed:
        raise SystemExit(2)


if __name__=='__main__':
    main()
