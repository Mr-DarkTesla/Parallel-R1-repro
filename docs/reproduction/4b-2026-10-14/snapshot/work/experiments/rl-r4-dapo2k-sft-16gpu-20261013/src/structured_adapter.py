"""Executable token-slot fork/seal/merge adapter. No engine imports on import.
HFSlotBackend is the CPU differential oracle. SGLangSlotBackend lives separately;
its runner requires the pinned generic-self-mask patch and GPU qualification.
"""
from dataclasses import dataclass, field
import torch

@dataclass(frozen=True)
class Lease:
    actor_version: str
    episode: str

@dataclass
class Handle:
    uid: int
    lease: Lease
    ids: tuple
    positions: tuple
    slots: tuple
    logits: torch.Tensor
    root_uid: int = 0
    shared_length: int = 0
    pending: tuple = ()
    raw_ids: tuple = ()
    raw_logprobs: tuple = ()
    released: bool = False

@dataclass
class Plan:
    lease: Lease
    read_slots: tuple
    query_ids: tuple
    query_positions: tuple
    allowed: torch.Tensor
    phase: str

class Ledger:
    def __init__(self): self.events=[]; self.episode={}
    def record(self, plans):
        episodes=tuple(sorted({p.lease.episode for p in plans}))
        self.events.append(dict(episodes=episodes,phases=[p.phase for p in plans],rows=len(plans),query_tokens=sum(len(p.query_ids) for p in plans)))
        for e in episodes:self.episode[e]=self.episode.get(e,0)+1
    @property
    def global_forwards(self):return len(self.events)

class HFSlotBackend:
    """Private token-slot pool; physical cache indices do not equal RoPE positions.
    Retains autograd in proof mode. Production actor should call under no_grad.
    """
    def __init__(self, model, ledger):
        self.model=model;self.ledger=ledger;self.pool={};self.refs={};self.next_slot=1
    def retain(self,slots):
        for s in slots:self.refs[s]=self.refs.get(s,0)+1
    def release(self,slots):
        for s in slots:
            self.refs[s]-=1
            if not self.refs[s]:self.refs.pop(s);self.pool.pop(s)
    def forward(self,plans):
        from transformers.cache_utils import DynamicCache
        if not plans:return []
        parameter=next(self.model.parameters());device=parameter.device;dtype=parameter.dtype
        qmax=max(len(p.query_ids) for p in plans);kmax=max(len(p.read_slots) for p in plans);bs=len(plans)
        ids=torch.zeros(bs,qmax,device=device,dtype=torch.long);pos=torch.zeros_like(ids)
        mask=torch.full((bs,1,qmax,kmax+qmax),-torch.inf,dtype=dtype,device=device)
        cache=None
        if kmax:
            example=next(iter(self.pool.values()));layers=[]
            for layer in range(len(example)):
                pairs=[]
                for which in range(2):
                    h,d=example[layer][which].shape
                    rows=[]
                    for p in plans:
                        values=[self.pool[s][layer][which] for s in p.read_slots]
                        real=torch.stack(values,dim=1) if values else parameter.new_zeros(h,0,d)
                        rows.append(torch.cat([parameter.new_zeros(h,kmax-len(values),d),real],dim=1))
                    pairs.append(torch.stack(rows))
                layers.append(tuple(pairs))
            cache=DynamicCache.from_legacy_cache(tuple(layers))
        for r,p in enumerate(plans):
            n,q=len(p.read_slots),len(p.query_ids);off=qmax-q
            if q==0:raise ValueError('No zero-query forward; do not fabricate free F')
            if p.allowed.shape!=(q,n+q):raise ValueError('Mask shape mismatch')
            ids[r,off:]=torch.tensor(p.query_ids,device=device);pos[r,off:]=torch.tensor(p.query_positions,device=device)
            cols=list(range(kmax-n,kmax))+list(range(kmax+off,kmax+qmax))
            mask[r,0,torch.arange(off,qmax,device=device)[:,None],torch.tensor(cols,device=device)[None,:]]=torch.zeros_like(p.allowed,dtype=dtype,device=device).masked_fill(~p.allowed.to(device),-torch.inf)
            for i in range(off):mask[r,0,i,kmax+i]=0
        output=self.model(input_ids=ids,position_ids=pos,attention_mask=mask,past_key_values=cache,
                          cache_position=torch.arange(kmax,kmax+qmax,device=device),use_cache=True)
        self.ledger.record(plans)
        legacy=output.past_key_values.to_legacy_cache();result=[]
        for r,p in enumerate(plans):
            q=len(p.query_ids);off=qmax-q;slots=[]
            for j in range(q):
                s=self.next_slot;self.next_slot+=1
                self.pool[s]=tuple(tuple(value[r,:,kmax+off+j,:] for value in pair) for pair in legacy)
                self.refs[s]=0;slots.append(s)
            result.append((tuple(slots),output.logits[r,off:]))
        return result

class StructuredAdapter:
    def __init__(self, backend, canonical, actor_version, tags, pad_id=0, structure_start=3):
        self.backend=backend;self.canonical=canonical;self.actor_version=str(actor_version)
        self.tags=tuple(tags);self.pad_id=pad_id;self.start=structure_start;self.handles={};self.next_uid=1
    def _check(self,h):
        if h.released or self.handles.get(h.uid) is not h:raise ValueError('Released/foreign handle')
        if h.lease.actor_version!=self.actor_version:raise ValueError('Actor version mismatch')
    def _layout(self,ids):return self.canonical.layout(torch.tensor(ids),self.start,self.tags,self.pad_id,allow_partial=True)[0].tolist()
    def _plan(self,lease,ids,slotmap,phase):
        positions,blocks=self.canonical.layout(torch.tensor(ids),self.start,self.tags,self.pad_id,allow_partial=True);positions=positions.tolist()
        cached=[i for i,s in enumerate(slotmap) if s is not None];fresh=[i for i,s in enumerate(slotmap) if s is None]
        queries=torch.tensor(fresh)[:,None];keys=torch.tensor(cached+fresh)[None,:]
        # Exact rows of canonical.attention without allocating its full N×N matrix.
        allowed=queries>=keys
        for spans in blocks:
            first=spans[0][0]
            for begin,end in spans[1:]:allowed &= ~((queries>=begin)&(queries<end)&(keys>=first)&(keys<begin))
        return Plan(lease,tuple(slotmap[i] for i in cached),tuple(ids[i] for i in fresh),tuple(positions[i] for i in fresh),allowed,phase),fresh,positions
    def _new(self,lease,ids,positions,slots,logits,**kwargs):
        h=Handle(self.next_uid,lease,tuple(ids),tuple(positions),tuple(slots),logits,**kwargs);self.next_uid+=1
        self.backend.retain(h.slots);self.handles[h.uid]=h;return h
    def prefill_many(self,prompts,episodes):
        if len(prompts)!=len(episodes) or not prompts:raise ValueError('Nonempty prompt/episode cardinality required')
        items=[]
        for ids,e in zip(prompts,episodes):
            lease=Lease(self.actor_version,e);plan,fresh,pos=self._plan(lease,list(ids),[None]*len(ids),'root_prefill');items.append((ids,lease,plan,pos))
        results=self.backend.forward([x[2] for x in items])
        return [self._new(lease,ids,pos,slots,logits[-1]) for (ids,lease,plan,pos),(slots,logits) in zip(items,results)]
    def append_many(self,handles,tokens,phase='continuation'):
        if len(handles)!=len(tokens) or not handles:raise ValueError('Nonempty handle/token cardinality required')
        items=[]
        for h,t in zip(handles,tokens):
            self._check(h)
            if h.pending:raise ValueError('Seal/merge pending canonical tokens first')
            ids=list(h.ids)+list(t);mapping=list(h.slots)+[None]*len(t)
            plan,fresh,pos=self._plan(h.lease,ids,mapping,phase);items.append((h,ids,mapping,plan,fresh,pos))
        outputs=self.backend.forward([x[3] for x in items]);new=[]
        for (h,ids,mapping,plan,fresh,pos),(slots,logits) in zip(items,outputs):
            for i,s in zip(fresh,slots):mapping[i]=s
            new.append(self._new(h.lease,ids,pos,mapping,logits[-1],root_uid=h.root_uid,shared_length=h.shared_length))
        return new
    def fork(self,shared,headers):
        self._check(shared)
        if not 2<=len(headers)<=8:raise ValueError('Intact fork width must be 2..8')
        branches=self.append_many([shared]*len(headers),headers,'fork_headers')
        for b in branches:b.root_uid=shared.uid;b.shared_length=len(shared.ids)
        return branches
    def decode_group(self,branches,budgets,stops,targets=None,seeds=None,blocked=(),temperature=1.):
        if not 1<=len(branches)<=8:raise ValueError('Full-width group ≤8 required')
        if temperature<=0:raise ValueError('Positive temperature')
        if len(budgets)!=len(branches):raise ValueError('Budget cardinality')
        if targets is not None:
            if len(targets)!=len(branches) or any(len(t)>b for t,b in zip(targets,budgets)):raise ValueError('Target budget mismatch')
            budgets=[len(t) for t in targets]
        if any(b<=0 for b in budgets):raise ValueError('No zero-action path requests')
        live=list(range(len(branches)));raw=[[] for _ in branches];logps=[[] for _ in branches];current=list(branches)
        gens=[torch.Generator(device=branches[i].logits.device).manual_seed((seeds or list(range(len(branches))))[i]) for i in range(len(branches))]
        while live:
            continuing=[];feed=[]
            for i in live:
                self._check(current[i]);logits=current[i].logits/temperature
                if blocked:logits=logits.clone();logits[list(blocked)]=-torch.inf
                target=int(targets[i][len(raw[i])]) if targets is not None else int(torch.multinomial(logits.softmax(-1),1,generator=gens[i]))
                if target in blocked:raise ValueError('Raw action violates native guard')
                raw[i].append(target);logps[i].append(torch.log_softmax(logits,-1)[target])
                if target not in stops and len(raw[i])<budgets[i]:continuing.append(i);feed.append([target])
            if not continuing:break
            new=self.append_many([current[i] for i in continuing],feed,'branch_decode')
            for i,h in zip(continuing,new):
                old=current[i];current[i]=h;self.release(old)
            live=continuing
        for i,h in enumerate(current):h.raw_ids=tuple(raw[i]);h.raw_logprobs=tuple(logps[i])
        return current
    def seal(self,h,closure,stops):
        self._check(h)
        if not h.raw_ids:raise ValueError('Seal requires sampled actions')
        if h.pending:raise ValueError('Already sealed')
        last=h.raw_ids[-1]
        h.pending=(closure,) if last in stops else (last,closure)
        return h
    def merge(self,shared,branches,bridge):
        self._check(shared)
        ids=list(shared.ids);mapping=list(shared.slots)
        for b in branches:
            self._check(b)
            if b.lease!=shared.lease or b.root_uid!=shared.uid:raise ValueError('Cross-episode/root merge')
            if not b.pending:raise ValueError('Unsealed branch')
            if b.ids[:b.shared_length]!=shared.ids:raise ValueError('Shared ancestry changed')
            ids.extend(b.ids[b.shared_length:]);mapping.extend(b.slots[b.shared_length:])
            ids.extend(b.pending);mapping.extend([None]*len(b.pending))
        ids.extend(bridge);mapping.extend([None]*len(bridge))
        plan,fresh,pos=self._plan(shared.lease,ids,mapping,'merge_closures_bridge')
        slots,logits=self.backend.forward([plan])[0]
        for i,s in zip(fresh,slots):mapping[i]=s
        # All raw last actions stay targets, while pending canonical writes are counted once.
        return self._new(shared.lease,ids,pos,mapping,logits[-1])
    def release(self,h):
        self._check(h);h.released=True;self.handles.pop(h.uid);self.backend.release(h.slots)
    def clear(self):
        for h in list(self.handles.values()):self.release(h)
    def change_actor(self,version):
        if self.handles:raise ValueError('Cannot hot-swap actor under live leases/KV handles')
        self.actor_version=str(version)
