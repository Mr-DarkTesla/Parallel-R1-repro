"""Existing rollout/CohortDecoder API over the patched vLLM paged KV runner.
Prefix KV is addressed by actor-bound canonical visibility signatures; partial
sibling prefixes and merged full contexts therefore reuse identical shared KV.
All alive rows execute one model forward. Raw last targets never become KV.
"""
import hashlib,struct
import torch
from structured_adapter import Plan,Lease
from source.parallel_structure import layout


def prefix_signatures(ids,call,actor_version):
 positions,blocks=layout(torch.tensor(ids),call['structure_start'],call['structure_tags'],call['pad_id'],allow_partial=True)
 starts={begin:(end,spans[0][0]) for spans in blocks for begin,end in spans[1:]}
 schema=[int(call['structure_start']),*map(int,call['structure_tags']),int(call['pad_id'])]
 flat=hashlib.sha256(struct.pack('<'+'q'*len(schema),*schema)+actor_version).digest();prefix=[flat];branch=None;result=[]
 for i,(token,pos) in enumerate(zip(ids,positions.tolist())):
  if i in starts:branch=[starts[i][0],prefix[starts[i][1]]]
  parent=branch[1] if branch is not None and i<branch[0] else flat
  value=hashlib.sha256(struct.pack('<qq',token,pos)+parent).digest();result.append(value);flat=hashlib.sha256(flat+value).digest();prefix.append(flat)
  if branch is not None and i<branch[0]:branch[1]=hashlib.sha256(branch[1]+value).digest()
  else:branch=None
 return result,positions.tolist(),blocks,flat

class VLLMSlotDecoder:
 def __init__(self,backend,actor_version):
  self.backend=backend;self.actor_version=str(actor_version);self.version=self.actor_version.encode();self.bank={};self.last_batch_stats={};self.call_index=0
 def clear(self):
  if self.bank:self.backend.release(tuple(self.bank.values()))
  self.bank.clear()
 def change_actor(self,version):
  if self.bank:raise ValueError('Drain whole-episode actor leases and clear KV before actor update')
  self.actor_version=str(version);self.version=self.actor_version.encode()
 def _store(self,sigs,slots):
  for signature,slot in zip(sigs,slots):
   if signature not in self.bank:self.bank[signature]=slot;self.backend.retain((slot,))
   else:self.backend.allocator.discard((slot,))
 def __call__(self,call,budget,stops):return self.decode_many([call],[budget],stops)[0]
 @torch.inference_mode()
 def decode_many(self,calls,budget,stops,*,target_sequences=None):
  budgets=[budget]*len(calls) if isinstance(budget,int) else list(budget)
  if len(budgets)!=len(calls):raise ValueError('Budget cardinality')
  if target_sequences is not None:
   if len(target_sequences)!=len(calls):raise ValueError('Target cardinality')
   if any(len(t)>b for t,b in zip(target_sequences,budgets)):raise ValueError('Target budget exceeds frozen cap')
   budgets=list(map(len,target_sequences))
  outputs=[([],[],0) for _ in calls];live=[i for i,b in enumerate(budgets) if b>0]
  if not live:self.last_batch_stats=dict(physical_forward_calls=0,prefill_forward_calls=0,decode_forward_calls=0,active_row_forward_work=0,generated_lengths=[0]*len(calls));return outputs
  device=self.backend.device;states={};generators=[torch.Generator(device=device).manual_seed(int(c.get('seed',0))) for c in calls]
  plans=[];fresh_rows=[]
  for i in live:
   call=calls[i];ids=list(call['prompt_ids']);sigs,positions,blocks,flat=prefix_signatures(ids,call,self.version)
   if not ids:raise ValueError('Nonempty prompt required')
   cached=[j for j,sig in enumerate(sigs) if sig in self.bank];fresh=[j for j,sig in enumerate(sigs) if sig not in self.bank]
   # Every call first-action logits come from an actual model forward. Replaying
   # an already-cached prefix recomputes its last row with the same mask.
   if not fresh:fresh=[len(ids)-1];cached.remove(fresh[0])
   queries=torch.tensor(fresh)[:,None];keys=torch.tensor(cached+fresh)[None,:];allowed=queries>=keys
   for spans in blocks:
    first=spans[0][0]
    for begin,end in spans[1:]:allowed &= ~((queries>=begin)&(queries<end)&(keys>=first)&(keys<begin))
   lease=Lease(self.actor_version,str(call.get('episode_id',i)))
   plans.append(Plan(lease,tuple(self.bank[sigs[j]] for j in cached),tuple(ids[j] for j in fresh),tuple(positions[j] for j in fresh),allowed,call.get('phase','prefill')))
   fresh_rows.append([sigs[j] for j in fresh]);states[i]=dict(sigs=sigs,positions=positions,flat=flat,lease=lease)
  first=self.backend.actual_model_forwards
  values=self.backend.forward(plans)
  for i,sigs,(slots,logits) in zip(live,fresh_rows,values):
   self._store(sigs,slots);states[i]['logits']=logits[-1];states[i]['slots']=[self.bank[sig] for sig in states[i]['sigs']]
  while live:
   tokens=[];logps=[]
   for i in live:
    call=calls[i];temperature=float(call.get('temperature',1.));assert temperature>0
    logits=states[i]['logits'].float()/temperature;blocked=call.get('blocked_token_ids',[])
    if blocked:logits=logits.clone();logits[blocked]=-torch.inf
    token=torch.tensor(target_sequences[i][len(outputs[i][0])],device=device,dtype=torch.long) if target_sequences is not None else torch.multinomial(logits.softmax(-1),1,generator=generators[i])[0]
    tokens.append(token);logps.append(logits[token]-logits.logsumexp(-1))
   # One group transfer for actions and one for q; no per-row .item sync.
   sampled=torch.stack(tokens).tolist();values=torch.stack(logps).tolist();continuing=[];next_plans=[];new_signatures=[]
   for i,token,logp in zip(live,sampled,values):
    if token in calls[i].get('blocked_token_ids',[]):raise ValueError('Raw action violates native Think guard')
    raw,old,_=outputs[i];raw.append(token);old.append(logp);outputs[i]=(raw,old,len(raw))
    if token in stops or len(raw)>=budgets[i]:continue
    state=states[i];pos=state['positions'][-1]+1
    signature=hashlib.sha256(struct.pack('<qq',token,pos)+state['flat']).digest();state['flat']=hashlib.sha256(state['flat']+signature).digest()
    read=tuple(state['slots']);state['sigs'].append(signature);state['positions'].append(pos)
    next_plans.append(Plan(state['lease'],read,(token,),(pos,),torch.ones(1,len(read)+1,dtype=torch.bool),'decode'))
    new_signatures.append([signature]);continuing.append(i)
   if not continuing:break
   values=self.backend.forward(next_plans)
   for i,sigs,(slots,logits) in zip(continuing,new_signatures,values):
    self._store(sigs,slots);states[i]['slots'].append(self.bank[sigs[0]]);states[i]['logits']=logits[-1]
   live=continuing
  lengths=[len(row[0]) for row in outputs];physical=self.backend.actual_model_forwards-first
  assert physical==max(lengths),'All alive branches must share each physical forward'
  self.last_batch_stats=dict(physical_forward_calls=physical,prefill_forward_calls=1,decode_forward_calls=physical-1,active_row_forward_work=sum(lengths),generated_lengths=lengths,requested_rows=len(calls),microbatch_max_paths=8,sequential_subgroup_count=1,sequential_subgroups=[dict(physical_forward_calls=physical,active_row_forward_work=sum(lengths))],semantic_slots=len(self.bank),model_version=self.actor_version)
  return outputs
