"""vLLM0.8.5 Attention.impl patch: paged slots and canonical DAG masks.
CPU-runnable attention math; the real ModelRunner binding is in engine_patch.py.
No monkeypatch of installed files, stock scheduler or global attention selector.
"""
from dataclasses import dataclass
import threading
import torch
from torch.nn import functional as F

@dataclass
class DAGRow:
 read_slots: tuple
 write_slots: tuple
 allowed: torch.Tensor
 query_begin: int
 query_end: int

@dataclass
class DAGMetadata:
 rows: tuple
 num_prefill_tokens: int
 num_decode_tokens: int = 0
 enable_kv_scales_calculation: bool = False
 write_indices: object = None
 query_destinations: object = None
 physical_indices: object = None
 allowed_mask: object = None
 qmax: int = 0

 def prepare(self,device):
  self.qmax=max(row.query_end-row.query_begin for row in self.rows);kmax=max(len(row.read_slots) for row in self.rows)
  physical=torch.zeros(len(self.rows),kmax+self.qmax,dtype=torch.long,device=device)
  mask=torch.zeros(len(self.rows),1,self.qmax,kmax+self.qmax,dtype=torch.bool,device=device)
  writes=[];destinations=[]
  for i,row in enumerate(self.rows):
   n=len(row.read_slots);count=row.query_end-row.query_begin;off=self.qmax-count
   if row.allowed.shape!=(count,n+count) or count!=len(row.write_slots):raise ValueError("DAG row shape mismatch")
   if n:physical[i,kmax-n:kmax]=torch.tensor(row.read_slots,dtype=torch.long,device=device)
   physical[i,kmax+off:]=torch.tensor(row.write_slots,dtype=torch.long,device=device)
   cols=torch.tensor(list(range(kmax-n,kmax))+list(range(kmax+off,kmax+self.qmax)),device=device)
   mask[i,0,torch.arange(off,self.qmax,device=device)[:,None],cols[None,:]]=row.allowed.to(device)
   if off:mask[i,0,torch.arange(off,device=device),kmax+torch.arange(off,device=device)]=True
   writes.extend(row.write_slots);destinations.extend(range(i*self.qmax+off,(i+1)*self.qmax))
  if len(writes)!=len(set(writes)) or 0 in writes:raise ValueError("Duplicate/reserved physical writes")
  self.write_indices=torch.tensor(writes,dtype=torch.long,device=device)
  self.query_destinations=torch.tensor(destinations,dtype=torch.long,device=device)
  self.physical_indices=physical;self.allowed_mask=mask
  return self

class SlotAllocator:
 def __init__(self,capacity):
  if capacity<2:raise ValueError('Capacity includes reserved padding slot0')
  self.capacity=capacity;self.free=list(range(capacity-1,0,-1));self.refs={};self.allocated=set();self.peak_live=0
 def allocate(self,n):
  if n>len(self.free):raise MemoryError('Structured KV slot capacity exhausted; no budget truncation')
  result=tuple(self.free.pop() for _ in range(n));self.allocated.update(result)
  self.peak_live=max(self.peak_live,len(self.allocated));return result
 def retain(self,slots):
  for slot in slots:
   if slot not in self.allocated:raise ValueError('Retain unallocated/foreign slot')
   self.refs[slot]=self.refs.get(slot,0)+1
 def release(self,slots):
  for slot in slots:
   if self.refs.get(slot,0)<=0:raise ValueError('Release unleased slot')
   self.refs[slot]-=1
   if not self.refs[slot]:self.refs.pop(slot);self.allocated.remove(slot);self.free.append(slot)
 def discard(self,slots):
  for slot in slots:
   if self.refs.get(slot,0):raise ValueError('Discard live leased slot')
   self.allocated.remove(slot);self.free.append(slot)

class DAGSDPAImpl:
 """One SDPA call for all live rows in one real model layer forward.
 Writes new K/V in real [2,blocks,block_size,kv_heads,head_size] tensors.
 Slot IDs select storage only; Q/K have already received semantic-position RoPE.
 """
 def __init__(self,num_heads,head_size,scale,num_kv_heads):
  self.num_heads=num_heads;self.head_size=head_size;self.scale=scale;self.num_kv_heads=num_kv_heads;self.calls=0
 def forward(self,layer,query,key,value,kv_cache,attn_metadata,output=None):
  if not isinstance(attn_metadata,DAGMetadata):raise TypeError('Canonical DAG metadata required; stock causal metadata rejected')
  if kv_cache.ndim!=5 or kv_cache.shape[0]!=2:raise ValueError('Expected paged physical KV tensor')
  rows=attn_metadata.rows
  if not rows:raise ValueError('Empty structured forward')
  q=query.reshape(-1,self.num_heads,self.head_size);k=key.reshape(-1,self.num_kv_heads,self.head_size);v=value.reshape_as(k)
  if q.shape[0]!=attn_metadata.num_prefill_tokens:raise ValueError('Query cardinality mismatch')
  metadata=attn_metadata
  if metadata.write_indices is None:metadata.prepare(q.device)
  store=kv_cache.reshape(2,-1,self.num_kv_heads,self.head_size)
  store[0].index_copy_(0,metadata.write_indices,k);store[1].index_copy_(0,metadata.write_indices,v)
  batch=len(rows);qmax=metadata.qmax
  qpad=q.new_zeros(batch*qmax,self.num_heads,self.head_size)
  qpad.index_copy_(0,metadata.query_destinations,q)
  qpad=qpad.reshape(batch,qmax,self.num_heads,self.head_size)
  # One metadata build per model forward, reused across all attention layers.
  keys=store[0][metadata.physical_indices].transpose(1,2)
  values=store[1][metadata.physical_indices].transpose(1,2)
  attended=F.scaled_dot_product_attention(qpad.transpose(1,2),keys,values,attn_mask=metadata.allowed_mask,dropout_p=0.,is_causal=False,scale=self.scale,enable_gqa=self.num_heads!=self.num_kv_heads).transpose(1,2)
  result=attended.reshape(batch*qmax,self.num_heads,self.head_size).index_select(0,metadata.query_destinations)
  self.calls+=1
  if output is not None:output.copy_(result.reshape_as(output));return output
  return result.reshape(query.shape)

class PagedSlotBackend:
 """Adapter backend binding the real vLLM model and patched Attention layers."""
 def __init__(self,model,vllm_config,layers,ledger,capacity=65536,block_size=16,runner=None):
  self.actor_version=None;self.runner=runner;self.model=model;self.config=vllm_config;self.layers=layers;self.ledger=ledger;self.allocator=SlotAllocator(capacity);self.block_size=block_size;self.lock=threading.RLock()
  parameter=next(model.parameters());self.device=parameter.device;self.dtype=parameter.dtype
  blocks=(capacity+block_size-1)//block_size
  for layer in layers:
   layer.impl=DAGSDPAImpl(layer.num_heads,layer.head_size,layer.impl.scale,layer.num_kv_heads)
   layer.use_direct_call=True;layer.use_output=True;layer.calculate_kv_scales=False
   cache=torch.empty((2,blocks,block_size,layer.num_kv_heads,layer.head_size),dtype=self.dtype,device=self.device)
   cache[:,0,0].zero_();layer.kv_cache=[cache]
  self.actual_model_forwards=0;self.total_model_forwards=0;self.technical_mode=False
  self.device_total_counter=torch.zeros((),dtype=torch.int64,device=self.device)
  self.device_forward_counter=torch.zeros((),dtype=torch.int64,device=self.device)
  def tick(module,args):
   self.total_model_forwards+=1;self.device_total_counter.add_(1)
   if not self.technical_mode:
    self.actual_model_forwards+=1;self.device_forward_counter.add_(1)
  self.hook=model.register_forward_pre_hook(tick)
 def retain(self,slots):self.allocator.retain(slots)
 def release(self,slots):self.allocator.release(slots)
 @torch.inference_mode()
 def forward(self,plans):
  from vllm.forward_context import set_forward_context
  if not plans:return []
  version=plans[0].lease.actor_version
  if self.actor_version is None:self.actor_version=version
  if version!=self.actor_version or any(p.lease.actor_version!=version for p in plans):raise ValueError('Mixed/changed actor versions require drained weight-update barrier')
  with self.lock:
   rows=[];written=[];ids=[];positions=[];begin=0
   try:
    for plan in plans:
     if not plan.query_ids:raise ValueError('No fabricated zero-query F')
     slots=self.allocator.allocate(len(plan.query_ids));written.extend(slots)
     rows.append(DAGRow(plan.read_slots,slots,plan.allowed,begin,begin+len(slots)));begin+=len(slots)
     ids.extend(plan.query_ids);positions.extend(plan.query_positions)
    metadata=DAGMetadata(tuple(rows),begin).prepare(self.device);before=self.total_model_forwards
    # Prune LM-head queries exactly as serving does: forced headers/prefix tokens
    # need KV but only the final query supplies next-action logits. Explicit
    # dense-reference plans request additional logit rows for parity proofs.
    selections=[];spans=[];cursor=0
    for plan,row in zip(plans,rows):
     local=getattr(plan,'logit_indices',None)
     if local is None:local=range(row.query_end-row.query_begin) if plan.phase=='dense_reference' else [row.query_end-row.query_begin-1]
     local=list(local)
     if not local or any(i<0 or i>=row.query_end-row.query_begin for i in local):raise ValueError('Invalid requested LM-head query')
     selections.extend(row.query_begin+i for i in local);spans.append((cursor,cursor+len(local)));cursor+=len(local)
    indices=torch.tensor(selections,dtype=torch.long,device=self.device)
    input_tokens=torch.tensor(ids,dtype=torch.long,device=self.device)
    semantic_positions=torch.tensor(positions,dtype=torch.long,device=self.device)
    if self.runner is not None:
     logits=self.runner.execute_structured(input_tokens,semantic_positions,metadata,indices)
    else:
     with set_forward_context(metadata,self.config):hidden=self.model(input_ids=input_tokens,positions=semantic_positions)
     logits=self.model.compute_logits(hidden.index_select(0,indices),None).float()
    assert self.total_model_forwards-before==1,'Backend must execute exactly one real model forward'
    self.ledger.record(plans)
    return [(row.write_slots,logits[begin:end]) for row,(begin,end) in zip(rows,spans)]
   except BaseException:
    if written:self.allocator.discard(written)
    raise
 def close(self):
  if self.allocator.refs:raise ValueError('Live version leases must drain before cache close')
  self.hook.remove()
