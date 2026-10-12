"""Actual CPU Qwen proof of cost accounting and seeded-output microbatch parity."""
import copy
import json
import sys
from pathlib import Path
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'frozen'))
import structured_replay as replay
from audit_semantics import make_case
from decoder import BatchedHFDecoder
from microbatch_decoder import MicrobatchedHFDecoder


def main():
    torch.set_num_threads(2)
    torch.manual_seed(131)
    config = Qwen3Config(vocab_size=128,hidden_size=64,intermediate_size=128,num_hidden_layers=3,
                        num_attention_heads=4,num_key_value_heads=2,head_dim=16,attention_dropout=0.,pad_token_id=0)
    config._attn_implementation='sdpa'
    model=Qwen3ForCausalLM(config).eval()
    full=BatchedHFDecoder(model,replay,'cpu')
    records=[]
    for cap in [1,2,4]:
        decoder=MicrobatchedHFDecoder(model,replay,'cpu',max_paths=cap)
        for width in [2,3,4,6,8]:
            case=make_case(width)
            calls=copy.deepcopy([c for c in case['calls'] if c['phase']=='path'][-width:])
            for i,c in enumerate(calls):
                c['seed'],c['temperature']=53+i,1.
                c['prompt_ids'] += [20]*(i%3)
            lengths=[2+i%5 for i in range(width)]
            targets=[[21+i]*n for i,n in enumerate(lengths)]
            one=full.decode_many(calls,lengths,[13,16],target_sequences=targets)
            many=decoder.decode_many(calls,lengths,[13,16],target_sequences=targets)
            expected=sum(max(lengths[i:i+cap]) for i in range(0,width,cap))
            assert decoder.last_batch_stats['physical_forward_calls']==expected
            assert decoder.last_batch_stats['prefill_forward_calls']==(width+cap-1)//cap
            delta=max(abs(a-b) for x,y in zip(one,many) for a,b in zip(x[1],y[1]))
            assert delta<1e-5
            sampled_one=full.decode_many(calls,lengths,[13,16])
            sampled_many=decoder.decode_many(calls,lengths,[13,16])
            assert [r[0] for r in sampled_one]==[r[0] for r in sampled_many]
            records.append(dict(cap=cap,width=width,physical=expected,serial=sum(lengths),
                                max_delta=delta,seeded_actions_same=True))
    report=dict(passed=True,cases=records,max_logp_delta=max(r['max_delta'] for r in records),
                optimizer_memory_proof_still_required=True)
    (HERE/'cpu-microbatch-proof.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,max_logp_delta=report['max_logp_delta'],case_count=len(records))))


if __name__=='__main__':
    main()
