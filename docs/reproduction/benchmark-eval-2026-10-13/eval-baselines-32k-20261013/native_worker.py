"""Original Instruct native thinking, dynamic global queue, continuous batch8."""
from pathlib import Path
import argparse,fcntl,hashlib,importlib.util,json,os,time
p=argparse.ArgumentParser();p.add_argument('--job',required=True);p.add_argument('--rank',required=True,type=int);a=p.parse_args()
job=json.loads(Path(a.job).read_text());E=Path(job['root']);C=E/'control';os.environ.update(VLLM_USE_V1='0',VLLM_WORKER_MULTIPROC_METHOD='spawn')
from transformers import AutoTokenizer
from vllm import LLM,SamplingParams
assert job['response_budget']==32768 and job['max_context']==40960 and job['samples_per_question']==1
tok=AutoTokenizer.from_pretrained(job['model'],local_files_only=True)
spec=importlib.util.spec_from_file_location('frozen_scorer',job['scorer']);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
rows=[json.loads(l) for l in Path(job['questions']).read_text().splitlines() if l.strip()]
llm=LLM(model=job['model'],tokenizer=job['model'],dtype='bfloat16',tensor_parallel_size=1,max_model_len=40960,max_num_seqs=8,gpu_memory_utilization=.80,enable_prefix_caching=False,enable_chunked_prefill=False,num_scheduler_steps=1,worker_cls='counting_worker.CountingWorker',enforce_eager=False)
engine=llm.llm_engine;rpc=engine.model_executor.collective_rpc;rpc('reset_physical_counter');pending={};exhausted=False
jobsha=hashlib.sha256(Path(a.job).read_bytes()).hexdigest()
def save(path,data):
 tmp=path.with_name(path.name+'.tmp-'+str(os.getpid()));tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,path)
def claim():
 with (C/'queue.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);state=json.loads((C/'queue.json').read_text())
  if state['next']>=len(rows):return None
  i=state['next'];state['next']+=1;row=rows[i];state['leases'][str(i)]=dict(state='running',rank=a.rank,pid=os.getpid(),id=row['id'],dataset=row['dataset'],time=time.time());save(C/'queue.json',state);return i,row
def done(i,unknown):
 with (C/'queue.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);state=json.loads((C/'queue.json').read_text());state['leases'][str(i)].update(state='unknown' if unknown else 'done',finished_at=time.time());save(C/'queue.json',state)
started=time.time()
while pending or not exhausted:
 while len(pending)<8 and not exhausted:
  item=claim()
  if item is None:exhausted=True;break
  i,row=item;ids=tok.apply_chat_template([dict(role='system',content=job['native_system']),dict(role='user',content=row['problem'])],tokenize=True,add_generation_prompt=True,enable_thinking=True)
  text=tok.decode(ids,skip_special_tokens=False)
  if text.endswith('<think>'):ids+=tok.encode('\n',add_special_tokens=False)
  elif not text.endswith('<think>\n'):ids+=tok.encode('<think>\n',add_special_tokens=False)
  assert len(ids)+32768<=40960
  request=f'{a.rank}/{i}';params=SamplingParams(n=1,temperature=1,top_p=1,top_k=-1,max_tokens=32768,seed=row['seed'],logprobs=0)
  engine.add_request(request,dict(prompt_token_ids=ids),params);pending[request]=(i,row,ids,time.time())
  save(C/f'progress-rank-{a.rank}.json',dict(state='generating',rank=a.rank,pid=os.getpid(),pending_tasks=[v[0] for v in pending.values()],time=time.time()))
 if not pending:continue
 outputs=engine.step();finished=[result for result in outputs if result.finished]
 if not finished:continue
 counters=rpc('read_physical_counter')[0];assert counters['actual_global_model_forwards']==len(counters['events'])
 for result in finished:
  i,row,ids,t0=pending.pop(result.request_id);generated=result.outputs[0];text=generated.text
  events=[index for index,event in enumerate(counters['events']) if result.request_id in event['request_ids']]
  trace=dict(id=row['id'],dataset=row['dataset'],problem=row['problem'],reference_answer=str(row['answer']),index=row['original_index'],task_index=i,rank=a.rank,seed=row['seed'],output=text,prompt_ids=ids,response_ids=list(generated.token_ids),response_mask=[1]*len(generated.token_ids),sampled_logprobs=[v[t].logprob for t,v in zip(generated.token_ids,generated.logprobs)],native_think_opener_in_prompt=True,widths=[],path_lengths=[],fork_batch_ledger=[],stats=dict(forks=0,sampled_tokens=len(generated.token_ids),truncated=generated.finish_reason=='length',actual_model_forward_calls=len(events)),instrumented_forward_calls=len(events),physical_forward_indices=events,forward_metric_kind='request participation in actual CUDAgraph-counted physical model forwards',request_id=result.request_id,finish_reason=generated.finish_reason,stop_reason=generated.stop_reason,backend='native-vllm-continuous8',precision='BF16',model_identity=dict(path=job['model'],sha256=job['model_sha256'],label=job['model_label'],revision=job['native_source_proof']['revision']),evaluation_job_sha256=jobsha,response_budget=32768,max_context=40960,path_budget=768,samples_per_question=1,seconds=time.time()-t0,selection_allowed=False,benchmark=True)
  out=E/'runs'/row['dataset'];out.mkdir(parents=True,exist_ok=True)
  with (out/f'raw-rank-{a.rank}.jsonl').open('a') as f:f.write(json.dumps(trace,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
  grade=scorer.grade('<think>\n'+text,str(row['answer']));unknown=bool(grade.get('error'));valid='</think>' in text and text.count('</think>')==1 and not trace['stats']['truncated'] and bool(grade.get('valid'))
  trace.update(grade=grade,technical_unknown=unknown,format_valid=valid,parallel_valid=False,finished_at=time.time())
  with (out/f'rank-{a.rank}.jsonl').open('a') as f:f.write(json.dumps(trace,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
  done(i,unknown)
counters=rpc('read_physical_counter')[0];assert counters['actual_global_model_forwards']==len(counters['events'])
(E/f'backend-rank-{a.rank}.json').write_text(json.dumps(dict(rank=a.rank,wall=time.time()-started,**counters))+'\n')
save(C/f'progress-rank-{a.rank}.json',dict(state='completed',rank=a.rank,time=time.time()))
