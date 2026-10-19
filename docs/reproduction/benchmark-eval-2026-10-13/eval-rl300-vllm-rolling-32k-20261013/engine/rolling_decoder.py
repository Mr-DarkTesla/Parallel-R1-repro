"""Rolling episode admission; one GPU owner, indivisible width<=8 requests."""
import copy,queue,threading,time
from concurrent.futures import ThreadPoolExecutor
from cohort_decoder import Client
class RollingClient(Client):
 def decode_many(self,calls,budget,stops,*,target_sequences=None):
  if self.owner.failed is not None:raise self.owner.failed
  if not 1<=len(calls)<=8:raise ValueError('Never split sibling groups')
  budgets=[budget]*len(calls) if isinstance(budget,int) else list(budget)
  if len(budgets)!=len(calls) or any(b<0 for b in budgets):raise ValueError('Budgets')
  request=dict(calls=calls,budgets=budgets,stops=tuple(sorted(set(stops))),targets=target_sequences,episode=self.episode,ready=threading.Event())
  self.owner.pending.put(request)
  while not request['ready'].wait(.1):
   if self.owner.failed is not None:raise self.owner.failed
  if 'error' in request:raise request['error']
  outputs=request['result'];lengths=[len(v[0]) for v in outputs];physical=max(lengths,default=0)
  stats=dict(physical_forward_calls=physical,prefill_forward_calls=int(physical>0),decode_forward_calls=max(0,physical-1),active_row_forward_work=sum(lengths),call_indices=list(range(len(calls))))
  self.last_batch_stats=dict(**stats,requested_rows=len(calls),microbatch_max_paths=8,sequential_subgroup_count=1,sequential_subgroups=[dict(stats)],episode_cost_is_actual_backend_participation=True,cross_episode_server_cost_not_used_for_reward=True)
  return outputs
class RollingDecoder:
 def __init__(self,core,max_active=4,max_rows=16,context_reservation=40960,slot_margin=8192):
  self.core=core;self.max_active=max_active;self.max_rows=max_rows;self.context_reservation=context_reservation;self.slot_margin=slot_margin
  self.pending=queue.Queue();self.failed=None;self.server_batches=[];self.admissions=[]
 def run(self,next_job):
  pool=ThreadPoolExecutor(max_workers=self.max_active);active={};deferred=[];sequence=0;exhausted=False
  try:
   while active or not exhausted:
    # Completed episodes are removed immediately, even while others still run.
    finished=[ep for ep,f in active.items() if f.done()]
    completed=[]
    for ep in finished:
     completed.append(active.pop(ep).result());self.core.release_episode(str(ep))
    # Reserve full context for every active episode: no budget shortening/OOM gamble.
    while not exhausted and len(active)<self.max_active and (len(active)+1)*self.context_reservation+self.slot_margin<=self.core.backend.allocator.capacity:
     job=next_job()
     if job is None:exhausted=True;break
     ep=sequence;sequence+=1;client=RollingClient(self,ep);active[ep]=pool.submit(job,client)
     self.admissions.append(dict(episode=ep,active=len(active),time=time.time(),slots_live=len(self.core.backend.allocator.allocated)))
    # Caller grades on MAIN thread, after replacements have already been admitted.
    for value in completed:yield value
    if not active:continue
    try:request=deferred.pop(0) if deferred else self.pending.get(timeout=.01)
    except queue.Empty:continue
    cohort=[request];rows=len(request['calls']);deadline=time.monotonic()+.003
    while rows<self.max_rows:
     try:other=self.pending.get(timeout=max(0.,deadline-time.monotonic()))
     except queue.Empty:break
     if rows+len(other['calls'])>self.max_rows or other['stops']!=request['stops'] or (other['targets'] is None)!=(request['targets'] is None):deferred.append(other);continue
     cohort.append(other);rows+=len(other['calls'])
    calls=[dict(c,episode_id=str(r['episode'])) for r in cohort for c in r['calls']]
    budgets=[b for r in cohort for b in r['budgets']]
    targets=None if request['targets'] is None else [t for r in cohort for t in r['targets']]
    options={} if targets is None else dict(target_sequences=targets)
    values=self.core.decode_many(calls,budgets,request['stops'],**options)
    stats=copy.deepcopy(self.core.last_batch_stats)
    self.server_batches.append(dict(episode_ids=[r['episode'] for r in cohort],episode_row_counts=[len(r['calls']) for r in cohort],**stats))
    offset=0
    for r in cohort:r['result']=values[offset:offset+len(r['calls'])];offset+=len(r['calls']);r['ready'].set()
  except BaseException as error:
   self.failed=error
   for r in deferred:r['error']=error;r['ready'].set()
   while True:
    try:r=self.pending.get_nowait();r['error']=error;r['ready'].set()
    except queue.Empty:break
   raise
  finally:pool.shutdown(wait=True,cancel_futures=True)
