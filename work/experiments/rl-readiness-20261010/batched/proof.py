"""Actual Qwen SDPA CPU/GPU parity and physical-forward proof for batch paths."""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent/'rl-campaign-20261010'/'runner'))
import structured_replay as replay
from audit_semantics import make_case
from rollout import HFDecoder
from decoder import BatchedHFDecoder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model')
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--output', default=str(HERE/'cpu-proof.json'))
    args = parser.parse_args()
    torch.set_num_threads(2)
    torch.manual_seed(103)
    torch.set_float32_matmul_precision('highest')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    tokenizer = None
    if args.model:
        tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(args.model, local_files_only=True,
                 torch_dtype=torch.float32, attn_implementation='sdpa').to(args.device).eval()
    else:
        config = Qwen3Config(vocab_size=128, hidden_size=64, intermediate_size=128,
                            num_hidden_layers=3, num_attention_heads=4, num_key_value_heads=2,
                            head_dim=16, attention_dropout=0., pad_token_id=0)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).eval()
    batch = BatchedHFDecoder(model, replay, args.device)
    serial = HFDecoder(model, replay, args.device)
    original_forward = model.forward
    forward_records = []

    def counted_forward(*a, **kw):
        forward_records.append(list(kw['input_ids'].shape))
        return original_forward(*a, **kw)

    model.forward = counted_forward
    records, deltas, serial_deltas = [], [], []
    for width in [2, 3, 4, 6, 8]:
        case = make_case(width, tokenizer)
        paths = [c for c in case['calls'] if c['phase'] == 'path']
        for round_index in range(4):
            calls = copy.deepcopy(paths[round_index*width:(round_index+1)*width])
            for row, call in enumerate(calls):
                # Unequal valid prefix lengths exercise fully masked left pads;
                # every prefix still ends inside its own unfinished Path.
                call['prompt_ids'] += [20] * (row % 4)
                call['temperature'], call['seed'] = 1., 211+row
            bc = case['tags'][3]
            stop2 = 16 if tokenizer is None else int(tokenizer.eos_token_id)
            targets = [[21+(row % 9)] * (1+row%5) + [bc if row%2 else stop2]
                       for row in range(width)]
            forward_records.clear()
            outputs = batch.decode_many(calls, 16, [bc, stop2], target_sequences=targets)
            physical_shapes = list(forward_records)
            stats = copy.deepcopy(batch.last_batch_stats)
            assert len(physical_shapes) == stats['physical_forward_calls'] == max(map(len, targets))
            assert physical_shapes[0][0] == width and all(shape == [width, 1] for shape in physical_shapes[1:])
            assert stats['active_row_forward_work'] == sum(map(len, targets))
            for call, target, (raw, old, forwards) in zip(calls, targets, outputs):
                assert raw == target and forwards == len(target)
                scored = dict(call, generated_ids=raw)
                full, _ = replay.score_call(model, scored)
                cached, _ = replay.decoder_logprobs(model, scored)
                difference = (full.cpu()-torch.tensor(old)).abs()
                cached_difference = (torch.tensor(cached)-torch.tensor(old)).abs()
                deltas.extend(difference.tolist())
                serial_deltas.extend(cached_difference.tolist())
            # A row's outputs cannot depend on another row's prompt contents.
            changed = copy.deepcopy(calls)
            changed[0]['prompt_ids'][-1] = 27
            perturbed = batch.decode_many(changed, 16, [bc, stop2], target_sequences=targets)
            sibling_delta = max(abs(a-b) for original, new in zip(outputs[1:], perturbed[1:])
                                for a,b in zip(original[1], new[1]))
            assert sibling_delta == 0., sibling_delta
            # Changing only the value of masked left-pad embeddings cannot
            # change any live row's likelihood.
            if tokenizer is None:
                changed = copy.deepcopy(calls)
                for call in changed:
                    call['pad_id'] = 127
                other_pad = batch.decode_many(changed, 16, [bc, stop2], target_sequences=targets)
                pad_delta = max(abs(a-b) for original, new in zip(outputs, other_pad)
                                for a,b in zip(original[1], new[1]))
                assert pad_delta < 1e-6, pad_delta
            else:
                pad_delta = None
            records.append(dict(width=width, round=round_index+1,
                                real_prefix_lengths=[len(c['prompt_ids']) for c in calls],
                                physical_input_shapes=physical_shapes,
                                actual_forward_count_verified=True,
                                sibling_perturbation_delta=sibling_delta,
                                masked_padding_value_delta=pad_delta, **stats))
        if not args.model:
            # Independent RNG streams preserve sampled actions versus serial
            # decoding, including unequal lengths and per-row stop transitions.
            sampled = batch.decode_many(calls, [2+row%5 for row in range(width)], [bc, stop2])
            for call, n, batched_output in zip(calls, [2+row%5 for row in range(width)], sampled):
                one = serial(call, n, [bc, stop2])
                assert one[0] == batched_output[0], (width, one[0], batched_output[0])
                serial_deltas.extend(abs(a-b) for a,b in zip(one[1], batched_output[1]))
    values = torch.tensor(deltas)
    metrics = dict(maximum_abs_logp_delta=float(values.max()), mean_abs_logp_delta=float(values.mean()),
                   p95_abs_logp_delta=float(values.quantile(.95)),
                   max_batched_vs_serial_cache_delta=max(serial_deltas))
    limits = dict(maximum=.01, mean=.002, p95=.005) if args.model else dict(maximum=1e-5, mean=1e-5, p95=1e-5)
    passed = metrics['maximum_abs_logp_delta'] <= limits['maximum'] and metrics['mean_abs_logp_delta'] <= limits['mean'] and metrics['p95_abs_logp_delta'] <= limits['p95']
    report = dict(passed=passed, model=args.model or 'tiny actual Qwen3 SDPA', device=args.device,
                  dtype='FP32', tf32=False, logits_target_count=len(deltas), **metrics,
                  tolerance=limits, cases=records, raw_stops_preserved=True,
                  physical_vs_serial=dict(physical_total=sum(r['physical_forward_calls'] for r in records),
                                          serial_total=sum(r['active_row_forward_work'] for r in records),
                                          prefill_total=sum(r['prefill_forward_calls'] for r in records),
                                          decode_total=sum(r['decode_forward_calls'] for r in records)),
                  finished_row_dummy_cost_included=True, generation_gpu_launch_ready=False,
                  remaining='Actual 4B FP32 GPU parity and performance proof before integration' if not args.model else 'Production integration independent review and live throughput benchmark',
                  source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [HERE/'decoder.py', Path(__file__), HERE.parent/'structured_replay.py']})
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['passed', 'maximum_abs_logp_delta', 'mean_abs_logp_delta',
                                          'p95_abs_logp_delta', 'max_batched_vs_serial_cache_delta',
                                          'physical_vs_serial']}))
    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
