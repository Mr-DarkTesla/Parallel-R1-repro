"""CPU BF16 numerical screening only; no GPU speed or 4B parity claim."""
import copy
import json
import torch
from proof_cohort import HERE, replay, make_case, BatchedHFDecoder, Qwen3Config, Qwen3ForCausalLM


def main():
    torch.set_num_threads(2)
    torch.manual_seed(103)
    cfg=Qwen3Config(vocab_size=128,hidden_size=64,intermediate_size=128,num_hidden_layers=3,
                    num_attention_heads=4,num_key_value_heads=2,head_dim=16,attention_dropout=0.,pad_token_id=0)
    cfg._attn_implementation='sdpa'
    fp32=Qwen3ForCausalLM(cfg).eval()
    bf16=copy.deepcopy(fp32).to(torch.bfloat16).eval()
    case=make_case(4,None)
    calls=copy.deepcopy([c for c in case['calls'] if c['phase']=='path'][:4])
    for i,c in enumerate(calls): c.update(temperature=1.,seed=211+i)
    stops=[*case['tags'],16]
    targets=[[21+i]*8+[case['tags'][3]] for i in range(4)]
    reference=BatchedHFDecoder(fp32,replay).decode_many(calls,16,stops,target_sequences=targets)
    reduced=BatchedHFDecoder(bf16,replay).decode_many(calls,16,stops,target_sequences=targets)
    drift=torch.tensor([abs(x-y) for a,b in zip(reference,reduced) for x,y in zip(a[1],b[1])])
    sampled_fp32=BatchedHFDecoder(fp32,replay).decode_many(calls,16,stops)
    sampled_bf16=BatchedHFDecoder(bf16,replay).decode_many(calls,16,stops)
    result=dict(cpu_only_numerical_screen=True,model='tiny-random-Qwen3',
                max_fp32_vs_bf16_logp_delta=float(drift.max()),mean_logp_delta=float(drift.mean()),
                p95_logp_delta=float(drift.quantile(.95)),bitwise_likelihood_parity=bool((drift==0).all()),
                sampled_ids_same_this_small_case=[a[0]==b[0] for a,b in zip(sampled_fp32,sampled_bf16)],
                strict_fp32_1e5_gate_passed=bool(drift.max()<1e-5),
                tf32_cpu_test_possible=False,gpu4b_parity_not_proven=True,speedup_not_measured=True,
                rollout_dtype_change_not_enabled=True)
    (HERE/'cpu-precision-screen.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__': main()
