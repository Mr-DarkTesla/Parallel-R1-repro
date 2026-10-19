"""Selected SAME actor/query/KV/operator/shape reexecution, separate physical F.
Never compare q to learner p0; generation and technical GPU counters distinct.
"""
import torch,types
from structured_adapter import Ledger

def enable_same_actor_audit(backend):
 original=backend.forward;backend.audit_errors=[];backend.audit_remaining=8
 def reset(self):self.audit_errors=[];self.audit_remaining=8
 def stats(self):
  values=torch.cat(self.audit_errors) if self.audit_errors else torch.zeros(0)
  return dict(max=float(values.max()) if len(values) else 0.,mean=float(values.mean()) if len(values) else 0.,p95=float(values.quantile(.95)) if len(values) else 0.,actions=len(values),same_actor_weights=True,same_query_cache_mask_positions_shape=True,behavior_not_overwritten=True)
 @torch.inference_mode()
 def forward(plans):
  values=original(plans)
  if backend.audit_remaining>0:
   backend.audit_remaining-=1;ledger=backend.ledger;backend.technical_mode=True;backend.ledger=Ledger()
   try:
    replay=original(plans)
    for (slots,q),(temporary,p) in zip(values,replay):
     # Normalize all vocab identically; tests selection probability, not just logits.
     a=q.float()-q.float().logsumexp(-1,keepdim=True);z=p.float()-p.float().logsumexp(-1,keepdim=True)
     backend.audit_errors.append((a-z).abs().flatten().cpu());backend.allocator.discard(temporary)
   finally:backend.technical_mode=False;backend.ledger=ledger
  return values
 backend.forward=forward;backend.reset_audit=types.MethodType(reset,backend);backend.audit_stats=types.MethodType(stats,backend)
