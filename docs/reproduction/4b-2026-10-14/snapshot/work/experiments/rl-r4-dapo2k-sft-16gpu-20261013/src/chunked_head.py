"""Exact sampled-token likelihood, bounded vocabulary projection tiles.

No context/token/action truncation. FP32 normalization, existing autocast
projection dtype, original shared master weights. Checkpoint only the LM-head
chunks; geometry and transformer replay remain untouched.
"""
import torch
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

def projected_logprobs(hidden,weight,bias,targets,blocked,temperature,entropy=False,chunk=128):
 if hidden.ndim!=3 or hidden.shape[0]!=1 or hidden.shape[1]!=len(targets):raise ValueError('Exact target projection shape')
 if any(int(t) in blocked for t in targets):raise ValueError('Raw action violates recorded guard')
 outputs=[]
 def tile(h,w,b,t):
  logits=F.linear(h,w,b).float()
  if temperature!=1.:logits=logits/temperature
  if blocked:logits=logits.clone();logits[...,blocked]=-torch.inf
  normalizer=logits.logsumexp(-1)
  lp=logits.gather(-1,t[:,None]).squeeze(-1)-normalizer
  if not entropy:return lp[:,None]
  ent=normalizer-(logits.softmax(-1)*logits.masked_fill(~torch.isfinite(logits),0)).sum(-1)
  return torch.stack([lp,ent],-1)
 for start in range(0,len(targets),chunk):
  h=hidden[0,start:start+chunk];t=targets[start:start+chunk]
  args=(h,weight,bias,t)
  result=checkpoint(tile,*args,use_reentrant=False,preserve_rng_state=False) if torch.is_grad_enabled() else tile(*args)
  outputs.append(result)
 return torch.cat(outputs,dim=0)[None]
