"""BF16 vLLM DAG eval; four independent n1 questions/GPU, full raw traces."""
from pathlib import Path
import argparse,fcntl,hashlib,json,os,socket,sys,time,threading
ap=argparse.ArgumentParser();ap.add_argument('--job',required=True);ap.add_argument('--rank',required=True,type=int);a=ap.parse_args()
job=json.loads(Path(a.job).read_text());E=Path(job['root']);sys.path.insert(0,job['runtime'])
from train import instruct_prefix,format_flags,load_module
sys.path.insert(0,job['engine_runtime'])
os.environ.update(STRUCTURED_GPU_AUTHORIZED='1',VLLM_USE_V1='0',TORCHELASTIC_USE_AGENT_STORE='False')
import torch
from transformers import AutoTokenizer
from engine_patch import load_patched_worker
from structured_adapter import Ledger
from slot_decoder import VLLMSlotDecoder
from rolling_decoder import RollingDecoder
from rollout import execute,native_eos_ids
assert 0<=a.rank<32 and job['samples_per_question']==1
assert job['response_budget']==32768 and job['max_context']==40960
torch.set_num_threads(1);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
ledger=Ledger();worker,backend=load_patched_worker(job['model'],ledger,'bfloat16',40960,job['slot_capacity'],29700+a.rank)
tok=AutoTokenizer.from_pretrained(job['model'],local_files_only=True);eos=native_eos_ids(job['model'],tok)
decoder=VLLMSlotDecoder(backend,'eval/'+job['model_sha256']);system=Path(job['system']).read_text();scorer=load_module('frozen_math_scorer',job['scorer'])
rows=[json.loads(l) for l in Path(job['questions']).read_text().splitlines() if l.strip()];assert all(r['response_budget']==32768 and r['max_context']==40960 for r in rows)
control=E/'control';jobsha=hashlib.sha256(Path(a.job).read_bytes()).hexdigest();rawlock=threading.Lock()
def save(path,d):
 temp=path.with_name(path.name+'.tmp-'+str(os.getpid()));temp.write_text(json.dumps(d,indent=2)+'\n');os.replace(temp,path)
def claim():
 with (control/'queue.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);s=json.loads((control/'queue.json').read_text())
  while s['next']<len(rows):
   index=s['next'];s['next']+=1
   if str(index) in s['leases'] and s['leases'][str(index)]['state']=='done':continue
   row=rows[index];s['leases'][str(index)]=dict(rank=a.rank,pid=os.getpid(),host=socket.gethostname(),dataset=row['dataset'],id=row['id'],state='running',time=time.time());save(control/'queue.json',s);return index,row
  save(control/'queue.json',s);return None
def done(index,unknown):
 with (control/'queue.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);s=json.loads((control/'queue.json').read_text());s['leases'][str(index)].update(state='unknown' if unknown else 'done',finished_at=time.time());save(control/'queue.json',s)
def next_job():
 assigned=claim()
 if assigned is None:return None
 index,row=assigned
 prefix=instruct_prefix(tok,[dict(role='system',content=system),dict(role='user',content=row['problem'])])
 def generate(client):
  started=time.time();trace=execute(tok,prefix,client,eos,32768,768,40960,row['seed']);actual=trace['stats']['actual_model_forward_calls']
  assert all(x['microbatch_max_paths']==8 and x['sequential_subgroup_count']==1 and 1<=x['requested_rows']<=8 for x in trace['fork_batch_ledger'])
  trace.update(id=row['id'],dataset=row['dataset'],problem=row['problem'],reference_answer=str(row['answer']),index=row['original_index'],task_index=index,rank=a.rank,prompt_ids=prefix,instrumented_forward_calls=actual,model_identity=dict(path=job['model'],sha256=job['model_sha256'],checkpoint=job['checkpoint']),evaluation_job_sha256=jobsha,seed=row['seed'],response_budget=32768,path_budget=768,max_context=40960,samples_per_question=1,precision='BF16',backend='vllm-dag-rolling',selection_allowed=False,benchmark=True,seconds=time.time()-started)
  out=E/'runs'/row['dataset'];out.mkdir(parents=True,exist_ok=True)
  with rawlock,(out/f'raw-rank-{a.rank}.jsonl').open('a') as f:f.write(json.dumps(trace,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
  return trace
 return generate
server=RollingDecoder(decoder,max_active=job['questions_per_gpu'],max_rows=job['aggregate_rows'],context_reservation=40960)
before=backend.actual_model_forwards;batch_cursor=0;admit_cursor=0
for trace in server.run(next_job):
 # Generator/model owner and grader both run on MAIN; raw writer never grades.
 batches=server.server_batches[batch_cursor:];admissions=server.admissions[admit_cursor:];batch_cursor=len(server.server_batches);admit_cursor=len(server.admissions)
 assert backend.actual_model_forwards-before==sum(b['physical_forward_calls'] for b in server.server_batches)
 assert int(backend.device_forward_counter.item())==backend.actual_model_forwards==ledger.global_forwards
 with (E/f'backend-rank-{a.rank}.jsonl').open('a') as f:f.write(json.dumps(dict(task_index=trace['task_index'],global_backend_F=sum(b['physical_forward_calls'] for b in batches),admissions=admissions,batches=batches,slots_live=len(backend.allocator.allocated),time=time.time()))+'\n');f.flush();os.fsync(f.fileno())
 valid,parallel=format_flags(trace['output'],trace['stats']);grade=scorer.grade('<think>\n'+trace['output'],trace['reference_answer']);unknown=bool(grade.get('error'))
 trace.update(grade=grade,technical_unknown=unknown,format_valid=valid,parallel_valid=parallel,finished_at=time.time())
 with (E/'runs'/trace['dataset']/f"rank-{a.rank}.jsonl").open('a') as f:f.write(json.dumps(trace,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
 done(trace['task_index'],unknown)
 save(control/f'progress-rank-{a.rank}.json',dict(state='generating',rank=a.rank,pid=os.getpid(),last_completed=trace['task_index'],scheduler='rolling',active_episodes=len(decoder.episode_signatures),slots_live=len(backend.allocator.allocated),time=time.time()))
assert not decoder.episode_signatures and not decoder.bank and not backend.allocator.refs
decoder.clear();backend.close()
import torch.distributed as dist
if dist.is_initialized():dist.destroy_process_group()
save(control/f'progress-rank-{a.rank}.json',dict(state='completed',rank=a.rank,time=time.time()))
