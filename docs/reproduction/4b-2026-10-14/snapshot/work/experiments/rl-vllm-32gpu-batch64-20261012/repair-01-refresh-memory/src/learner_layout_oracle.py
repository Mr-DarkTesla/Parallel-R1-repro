"""Independent unchanged HF FP32 cached/full canonical layout oracle, not q."""
import torch
from decoder import BatchedHFDecoder

def fp32_layout_oracle(model,replay,trajectories):
 was=model.training;model.eval();decoder=BatchedHFDecoder(model,replay);calls=trajectories[0]['policy_calls'];groups=[];i=0
 while i<len(calls):
  group=[calls[i]];i+=1
  if group[0]['phase']=='path':
   while i<len(calls) and calls[i]['phase']=='path':group.append(calls[i]);i+=1
  if not groups or group[0]['phase']=='path':groups.append(group)
  if any(g[0]['phase']=='path' for g in groups):break
 errors=[]
 with torch.inference_mode(),torch.autocast('cuda',enabled=False):
  for group in groups:
   targets=[c['generated_ids'][:8] for c in group]
   values=decoder.decode_many(group,[len(t) for t in targets],[],target_sequences=targets)
   for call,target,(ids,lp,F) in zip(group,targets,values):
    if not target:continue
    full,_=replay.score_call(model,dict(call,generated_ids=target));errors.append((full-torch.tensor(lp,device=full.device)).abs().cpu())
 model.train(was);values=torch.cat(errors);assert torch.isfinite(values).all();return dict(max=float(values.max()),mean=float(values.mean()),p95=float(values.quantile(.95)),actions=len(values),policy='HF_FP32_layout_oracle_NOT_behavior_q')
