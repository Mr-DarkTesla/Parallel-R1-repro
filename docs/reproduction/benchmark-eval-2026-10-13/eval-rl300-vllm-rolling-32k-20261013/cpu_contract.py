"""CPU-only scheduler and shared-KV lifetime regression, no GPU/model launch."""
import sys,json,threading,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'engine'))
from rolling_decoder import RollingDecoder
from slot_decoder import VLLMSlotDecoder
class Allocator:
 capacity=196608
 allocated=set()
class Backend:
 allocator=Allocator()
 def __init__(self):self.released=[]
 def release(self,slots):self.released.extend(slots)
b=Backend();d=VLLMSlotDecoder(b,'v');d.bank={b'shared':1,b'private0':2,b'private1':3}
d.own('0',[b'shared',b'private0']);d.own('1',[b'shared',b'private1'])
d.release_episode('0');assert d.bank=={b'shared':1,b'private1':3} and b.released==[2]
d.release_episode('1');assert not d.bank and sorted(b.released)==[1,2,3] and not d.signature_owners
class Core:
 backend=Backend()
 def __init__(self):self.released=[];self.forwards=0;self.last_batch_stats={}
 def release_episode(self,ep):self.released.append(ep)
 def decode_many(self,calls,budgets,stops,**kw):
  self.forwards+=1;self.last_batch_stats=dict(physical_forward_calls=1)
  return [([int(c['token'])],[-.1],1) for c in calls]
core=Core();scheduler=RollingDecoder(core,max_active=4);submitted=[];finished=[];counts={}
def make(index):
 def job(client):
  count=1 if index in [0,4] else 4;answer=[]
  for step in range(count):
   if index in [1,2,3]:time.sleep(.02)
   width=[2,3,4,6,8][index]
   calls=[dict(token=index*100+step) for _ in range(width)]
   values=client.decode_many(calls,1,{9999});answer.extend(v[0][0] for v in values)
  return dict(index=index,answer=answer)
 return job
def next_job():
 i=len(submitted)
 if i>=5:return None
 submitted.append(dict(index=i,completed=list(finished)))
 return make(i)
for result in scheduler.run(next_job):finished.append(result['index']);counts[result['index']]=result['answer']
assert sorted(finished)==list(range(5))
assert submitted[4]['completed']==[],submitted # replacement is admitted BEFORE yielding first completed result
assert '0' in core.released and len(core.released)==5
assert core.forwards==sum(b['physical_forward_calls'] for b in scheduler.server_batches)
assert max(sum(b['episode_row_counts']) for b in scheduler.server_batches)<=16
for i in range(5):
 width=[2,3,4,6,8][i];count=1 if i in [0,4] else 4
 assert counts[i]==[i*100+s for s in range(count) for _ in range(width)]
print(json.dumps(dict(passed=True,replacement_before_slow_peer_completion=True,shared_KV_retained_until_last_owner=True,widths=[2,3,4,6,8],whole_group_max16=True,physical_ledger_reconciled=True,no_GPU_launch=True)))
