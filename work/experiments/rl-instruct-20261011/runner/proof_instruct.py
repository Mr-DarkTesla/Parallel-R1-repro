"""Tiny actual Qwen CPU proof for guarded generation and identical replay."""
import copy,json,hashlib
from pathlib import Path
import torch
from transformers import Qwen3Config,Qwen3ForCausalLM
import structured_replay as replay
from audit_semantics import make_case
from microbatch_decoder import MicrobatchedHFDecoder

torch.set_num_threads(2);torch.manual_seed(131)
cfg=Qwen3Config(vocab_size=128,hidden_size=64,intermediate_size=128,num_hidden_layers=3,num_attention_heads=4,num_key_value_heads=2,head_dim=16,attention_dropout=0.,pad_token_id=0)
cfg._attn_implementation='sdpa';model=Qwen3ForCausalLM(cfg).eval();records=[]
for width in [2,3,4,6,8]:
 calls=copy.deepcopy([c for c in make_case(width)['calls'] if c['phase']=='path'][-width:])
 for i,c in enumerate(calls):c.update(seed=53+i,temperature=1.,blocked_token_ids=[120,121]);c['prompt_ids'] += [20]*(i%3)
 decoder=MicrobatchedHFDecoder(model,replay,'cpu',max_paths=2);results=decoder.decode_many(calls,7,[13,16])
 for c,(ids,logps,_) in zip(calls,results):
  assert not set(ids)&set(c['blocked_token_ids']);c['generated_ids']=ids
  values,entropy=replay.score_call(model,c,calculate_entropy=True);assert torch.isfinite(entropy).all();delta=max(abs(a-b) for a,b in zip(values.detach().tolist(),logps));assert delta<1e-5
  values.sum().backward();assert any(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters());model.zero_grad(set_to_none=True)
  records.append(dict(width=width,max_delta=delta,sampled_actions=len(ids),blocked_token_ids=c['blocked_token_ids']))
# Post-think final stage: all six actual tiny control IDs blocked.
for width in [2,3,4,6,8]:
 c=copy.deepcopy(make_case(width)['calls'][-1]);c['prompt_ids'] += [120]
 c.update(seed=100+width,temperature=1.,blocked_token_ids=list(range(10,16)))
 ids,old,_=MicrobatchedHFDecoder(model,replay,'cpu').decode_many([c],9,[127])[0]
 assert not set(ids)&set(c['blocked_token_ids']);c['generated_ids']=ids
 values,entropy=replay.score_call(model,c,calculate_entropy=True);assert torch.isfinite(entropy).all()
 delta=max(abs(a-b) for a,b in zip(values.detach().tolist(),old));assert delta<1e-5
 records.append(dict(width=width,phase='postthink_final',all_six_tags_blocked=True,max_delta=delta,sampled_actions=len(ids)))
# A deliberately forbidden target must fail rather than silently score -inf.
bad=dict(c,generated_ids=[c["blocked_token_ids"][0]]);failed=False
try:replay.score_call(model,bad)
except ValueError:failed=True
assert failed
out=dict(passed=True,actual_model='tiny random Qwen3 CPU; not 4B GPU readiness',cases=records,max_logp_delta=max(x['max_delta'] for x in records),forbidden_target_rejected=True,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
(Path(__file__).parent/'cpu-instruct-guard-proof.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=True,cases=len(records),max_logp_delta=out['max_logp_delta'])))
