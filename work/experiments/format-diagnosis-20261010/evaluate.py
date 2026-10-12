"""Eight-GPU same-24-question evaluation; full production traces and isolated scorer."""
from pathlib import Path
from native_eos import native_eos_ids
import argparse,os,sys,json,time,subprocess,datetime as dt,math,re,importlib.util
R=Path(__file__).resolve().parent;P=R.parents[3]
def validate_model(model):
 model=Path(model).resolve()
 if not model.is_dir():raise ValueError('Model directory missing')
 if (model/'model.safetensors').exists():return model
 index=model/'model.safetensors.index.json'
 if not index.exists():raise ValueError('HF safetensors model/index missing')
 shards=set(json.loads(index.read_text())['weight_map'].values())
 if not shards:raise ValueError('Empty shard index')
 for name in shards:
  if Path(name).name!=name or not (model/name).is_file():raise ValueError('Invalid/missing model shard')
 return model

def validate_output(a,worker=False):
 if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,100}',a.name):raise ValueError('Flat unique output name required')
 out=R/a.name
 if out.resolve().parent!=R.resolve():raise ValueError('Output must remain inside isolated evaluations')
 if not Path(a.system_file).is_file():raise ValueError('Explicit system file required')
 if worker:
  m=json.loads((out/'manifest.json').read_text())
  if any(m[k]!=v for k,v in {'model':a.model,'mode':a.mode,'system_file':a.system_file,'suite':a.suite}.items()):raise ValueError('Worker manifest identity mismatch')
 elif out.exists():raise FileExistsError(out)
 return out

def provenance(a):
 import hashlib
 digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
 return {'evaluator_sha256':digest(__file__),'system_sha256':digest(a.system_file),
  'questions_sha256':digest(R/f'questions-{a.suite}.jsonl'),
  'generation_config_sha256':digest(Path(a.model)/'generation_config.json'),
  'runtime_sha256':{str(p.relative_to(R)):digest(p) for p in [R/'native_eos.py',R/'summary_metrics.py',R/'runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py',R/'runtime/verl/workers/rollout/vllm_rollout/structured_worker.py',R/'runtime/verl/utils/parallel_structure.py']}}

def args():
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--mode',choices=['native','structured'],default='structured');p.add_argument('--name',default='new-sft-gate4096');p.add_argument('--suite',choices=['24','128'],default='24');p.add_argument('--system-file',required=True);p.add_argument('--worker',type=int);return p.parse_args()
def worker(a):
 out=validate_output(a, worker=True);os.environ.update(VLLM_USE_V1='1',VLLM_ENABLE_V1_MULTIPROCESSING='0',PARALLEL_R1_TRACE_DIR=str(out/'repro'));sys.path.insert(0,str(R/'runtime'))
 import torch,asyncio,random
 from transformers import AutoTokenizer
 from omegaconf import OmegaConf
 from vllm import LLM,SamplingParams
 from types import SimpleNamespace
 from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3
 from native_eos import native_eos_ids
 eos_ids=native_eos_ids(a.model, AutoTokenizer.from_pretrained(a.model,local_files_only=True).eos_token_id)
 torch.set_num_threads(1);assert torch.cuda.mem_get_info()[0]>60*1024**3,'occupiedGPU';tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True);tags=[tok.convert_tokens_to_ids(t) for t in ['<Parallel>','</Parallel>','<Path>','</Path>']]
 llm=LLM(model=a.model,dtype='bfloat16',tensor_parallel_size=1,gpu_memory_utilization=.35,max_model_len=16384,max_num_seqs=1,max_num_batched_tokens=16384,enforce_eager=True,enable_prefix_caching=False,enable_chunked_prefill=False,worker_extension_cls='verl.workers.rollout.vllm_rollout.structured_worker.StructuredWorkerExtension',compilation_config={'level':0},disable_log_stats=True,seed=42)
 class Server:
  async def generate(self,request_id,prompt_ids,sampling_params):
   sp=dict(sampling_params);b=sp.pop('_structure_start');sp['_evaluation_only']=True;sp['max_tokens']=min(sp['max_tokens'],16384-len(prompt_ids));return llm.llm_engine.collective_rpc('structured_generate',args=(prompt_ids,sp,b,tags,tok.pad_token_id))[0] if sp['max_tokens']>0 else []
 cfg=OmegaConf.create({'actor_rollout_ref':{'rollout':{'prompt_length':4096,'response_length':4096,'structured_unseen':True,'agent':{'max_path_response_length':2048,'max_iterations_for_parallel_thinking':0,'min_paths':2,'max_paths':8,'force_think_prefix':True}}}})
 questions=[json.loads(l) for l in (R/f'questions-{a.suite}.jsonl').read_text().splitlines()][a.worker::8]
 async def run():
  with (out/f'traces-{a.worker}.jsonl').open('w',buffering=1) as f:
   for q in questions:
    seed=42+q['sample_index'];random.seed(seed);torch.manual_seed(seed);system=(P/'exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt').read_text() if a.mode=='structured' else 'Solve the math problem carefully. End with Final Answer: followed by the exact result.';system=Path(a.system_file).read_text() if a.system_file else system;messages=[{'role':'system','content':system},{'role':'user','content':q['problem']}];prefix=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);start=time.time();trace={}
    if a.mode=='native':
     think=tok.encode('<think>\n',add_special_tokens=False)
     if prefix[-len(think):]!=think:
      prefix+=think[1:] if prefix[-1:]==think[:1] else think
     x=llm.generate(prompt_token_ids=[prefix],sampling_params=SamplingParams(temperature=.6,top_p=.95,top_k=20,max_tokens=4096-len(think),seed=seed,stop_token_ids=eos_ids),use_tqdm=False)[0];ids=think+list(x.outputs[0].token_ids);text=tok.decode(ids,skip_special_tokens=False);stats={'critical_depth':len(x.outputs[0].token_ids),'sampled_tokens':len(x.outputs[0].token_ids),'forced_tokens':len(think),'generated_tokens':len(x.outputs[0].token_ids),'generation_calls':1,'forks':0,'truncated':len(ids)>=4096,'invalid_width':False}
    else:
     ParallelThinkingAgentLoopV3._class_initialized=False;agent=ParallelThinkingAgentLoopV3(SimpleNamespace(config=cfg),Server(),tok);agent.trajectory={'sample_index':q['sample_index'],'unique_id':q['id']};x=await agent.run(messages,{'temperature':.6,'top_p':.95,'top_k':20,'repetition_penalty':1.,'seed':seed});ids=list(x.response_ids);text=tok.decode(ids,skip_special_tokens=False);stats=x.repro_stats;trace=agent.trace.record
    f.write(json.dumps(dict(q,output=text,prompt_ids=prefix,response_ids=ids,response_tokens=len(ids),stats=stats,trace=trace,seed=seed,seconds=time.time()-start,mode=a.mode,worker=a.worker),ensure_ascii=False)+'\n')
 asyncio.run(run())
def strict_format(t,stats):
 valid=t.count('<think>')==t.count('</think>')==1 and all(t.count(a)==t.count(b) for a,b in [('<Parallel>','</Parallel>'),('<Path>','</Path>'),('<Summary>','</Summary>')]) and len(re.findall(r'^Final Answer:',t.split('</think>',1)[-1],re.M))==1 and not stats.get('invalid_width',False)
 blocks=list(re.finditer(r'<Parallel>(.*?)</Parallel>',t,re.S))
 for block in blocks:
  body=block.group(1);paths=re.findall(r'<Path>(.*?)</Path>',body,re.S);header=re.sub(r'<Path>.*?</Path>','',body,flags=re.S).strip()
  valid=valid and header in list('2345678') and len(paths)==int(header) if header in list('2345678') else False
  if header in list('2345678'):
   ids=[re.match(r'\s*(\d+)',x) for x in paths];valid=valid and all(ids) and [int(x.group(1)) for x in ids if x]==list(range(1,int(header)+1))
  valid=valid and bool(re.match(r'\s*<Summary>.*?</Summary>',t[block.end():],re.S))
 return bool(valid),bool(valid and blocks and stats.get('forks',0)>0)
def summarize(out):
 planned=json.loads((out/'manifest.json').read_text())['planned']
 spec=importlib.util.spec_from_file_location('gate_score',P/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);rows=[]
 for p in out.glob('traces-*.jsonl'):
  for line in p.read_text().splitlines():
   if not line.strip():continue
   r=json.loads(line);r['historical_grade']=s.grade(r['output'],str(r['answer']));r['grade']=s.grade(re.sub(r'</?think>','',r['output']),str(r['answer']));t=r['output'];valid,parallel=strict_format(t,r['stats']);r['format_valid']=valid;r['parallel_protocol_valid']=parallel;rows.append(r)
 n=len(rows);fmt=sum(r['format_valid'] for r in rows);protocol=sum(r['parallel_protocol_valid'] for r in rows);correct=sum(r['grade']['correct'] for r in rows);summary={'planned':planned,'completed':n,'missing':planned-n,'correct':correct,'pass_at_1_completed_only':correct/n if n else None,'format_valid':fmt,'format_fraction_completed_only':fmt/n if n else None,'executed_fork_samples':sum(r['stats'].get('forks',0)>0 for r in rows),'unfinished_thinking':sum('</think>' not in r['output'] for r in rows),'gate_format_threshold':.8,'parallel_protocol_valid':protocol,'parallel_protocol_fraction_completed_only':protocol/n if n else None,'gate_passed':n==planned and protocol/n>=.8,'response_cap':4096,'path_cap':2048,'accuracy_gate':'at least one correct; no stronger accuracy threshold','model':json.loads((out/'manifest.json').read_text())['model']}
 sys.path.insert(0,str(R))
 from summary_metrics import enrich_summary
 manifest=json.loads((out/'manifest.json').read_text());planned_rows=[json.loads(l) for l in Path(manifest['fixed_questions']).read_text().splitlines()]
 summary=enrich_summary(summary,rows,planned_rows)
 summary['system_file']=manifest.get('system_file')
 summary['provenance']={k:manifest.get(k) for k in ['evaluator_sha256','system_sha256','questions_sha256','generation_config_sha256','runtime_sha256']}
 if manifest.get('system_file'):
  import hashlib
  summary['system_sha256']=hashlib.sha256(Path(manifest['system_file']).read_bytes()).hexdigest();summary['matching_protocol']['prompt_policy']='Custom system-file supplied verbatim before native chat-template rendering; see system_file and hash'
 summary['suite']=manifest.get('suite');summary['curriculum_selection_allowed']=manifest.get('suite') in ('64','128')
 summary.update(diagnostic_only=True,checkpoint_selection_allowed=False,selection_allowed=False,curriculum_selection_allowed=False,native_eos_ids=json.loads((out/'manifest.json').read_text())['native_eos_ids'])
 (out/'scores.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
def main():
 a=args()
 if a.worker is not None:return worker(a)
 validate_model(a.model);out=validate_output(a);out.mkdir(exist_ok=False);assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPUoccupied';(out/'manifest.json').write_text(json.dumps({'model':a.model,'mode':a.mode,'system_file':a.system_file,'fixed_questions':str(R/f'questions-{a.suite}.jsonl'),'response_cap':4096,'path_cap':2048,'planned':len((R/f'questions-{a.suite}.jsonl').read_text().splitlines()),'suite':a.suite,'native_eos_ids':native_eos_ids(a.model),'diagnostic_only':True,'checkpoint_selection_allowed':False,**provenance(a)},indent=2)+'\n');procs=[]
 for rank in range(8):
  env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(rank),PYTHONPATH=str(R/'runtime'),OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1');log=(out/f'worker-{rank}.log').open('w');p=subprocess.Popen([os.environ.get('PARALLEL_R1_PYTHON',sys.executable),str(Path(__file__).resolve()),'--worker',str(rank),'--model',a.model,'--mode',a.mode,*(['--system-file',a.system_file] if a.system_file else []),'--name',a.name,'--suite',a.suite],cwd=P,env=env,stdout=log,stderr=subprocess.STDOUT);procs.append(p)
 rcs=[p.wait() for p in procs];(out/'worker-exits.json').write_text(json.dumps(rcs)+'\n');summarize(out)
 if any(rcs):raise SystemExit(1)
if __name__=='__main__':main()
