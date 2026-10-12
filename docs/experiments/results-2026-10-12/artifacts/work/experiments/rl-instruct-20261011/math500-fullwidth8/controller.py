from pathlib import Path
import os,json,hashlib,subprocess,time,sys,traceback
R=Path.cwd();B=R/'work/experiments/rl-instruct-20261011/math500-fullwidth8'
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(p,x):
 p=Path(p);t=p.with_suffix('.tmp');t.write_text(json.dumps(x,indent=2)+'\n');t.replace(p)
plan=read(B/'plan.json');fd=os.open(B/'controller.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
def status(state,**kw):write(B/'status.json',dict(state=state,pid=os.getpid(),updated=time.time(),**kw))
def gate():
 assert os.uname().nodename==plan['hostname']
 assert all(sha(k)==v for k,v in read(B/'seal.json')['sha256'].items())
 s=read(plan['sft_status'])
 if s['state']!='completed':return False
 if Path('/proc',str(s['pid'])).exists():return False
 return not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
while True:
 try:
  pending=[j for j in plan['jobs'] if not (B/'results'/f"{j['id']}.json").exists()]
  if not pending:status('completed');break
  if not gate():status('waiting_mainSFT_terminal_and_empty8');time.sleep(30);continue
  job=next((j for j in pending if Path(j['model'],'model.safetensors.index.json').exists() and (not j.get('complete') or Path(j['complete']).exists())),None)
  if job is None:status('waiting_standalone_checkpoints');time.sleep(30);continue
  
  if job.get('audit'):
   assert sha(job['audit'])==job['audit_sha256'];audit=read(job['audit']);assert audit['passed'] and audit['checkpoint']==job['model'];assert all(sha(k)==v for k,v in audit['manifest'].items())
  model=Path(job['model']);index=read(model/'model.safetensors.index.json');assert set(index['weight_map'])==set(read(Path(plan['baseline'],'model.safetensors.index.json'))['weight_map'])
  if job.get('complete'):assert read(job['complete'])['model']
  manifest={str(p):sha(p) for p in model.iterdir() if p.is_file()};job=dict(job,questions=plan['questions'],system=plan['system'],scorer=plan['scorer'],output=str(B/'runs'/job['id']))
  release=B/'releases'/f"{job['id']}.json";release.parent.mkdir(exist_ok=True);write(release,dict(job,model_manifest=manifest,selection_allowed=False,protocol=plan['protocol']))
  logs=B/'logs';logs.mkdir(exist_ok=True);children=[];handles=[];status('evaluating',job=job['id'])
  for rank in range(8):
   env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(rank),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',NVIDIA_TF32_OVERRIDE='0');h=(logs/f"{job['id']}-rank{rank}.log").open('a');handles.append(h);children.append(subprocess.Popen([sys.executable,str(B/'worker.py'),'--job',str(release),'--rank',str(rank)],cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=h,stderr=subprocess.STDOUT))
  while any(c.poll() is None for c in children):status('evaluating',job=job['id'],worker_pids=[c.pid for c in children]);time.sleep(30)
  codes=[c.wait() for c in children]
  for h in handles:h.close()
  assert codes==[0]*8,codes
  rows=[json.loads(l) for p in Path(job['output']).glob('rank-*.jsonl') for l in p.read_text().splitlines()];questions=[json.loads(l) for l in Path(plan['questions']).read_text().splitlines()]
  assert len(rows)==500 and len({r['id'] for r in rows})==500 and {r['id'] for r in rows}=={r['id'] for r in questions}
  assert all(sha(k)==v for k,v in manifest.items())
  stats=[r['stats'] for r in rows];grades=[r['grade'] for r in rows];assert all(not g.get('error') for g in grades); correct=[bool(g.get('correct',g.get('is_correct',False))) if isinstance(g,dict) else bool(g) for g in grades]
  summary=dict(passed=True,job=job['id'],completed=500,missing=0,correct=sum(correct),accuracy=sum(correct)/500,format_valid=sum(r['format_valid'] for r in rows),parallel_valid=sum(r['parallel_valid'] for r in rows),correct_parallel=sum(c and r['parallel_valid'] for c,r in zip(correct,rows)),fork_samples=sum(s['forks']>0 for s in stats),rounds=sum(s['forks'] for s in stats),widths=[w for row in rows for w in row['widths']],stats_totals={k:sum(s.get(k,0) for s in stats) for k in ['critical_depth','sampled_tokens','forced_tokens','actual_model_forward_calls']},question_wall_seconds=sum(r['seconds'] for r in rows),exit_codes=codes,model_manifest=manifest,protocol=plan['protocol'],selection_allowed=False)
  (B/'results').mkdir(exist_ok=True);write(B/'results'/f"{job['id']}.json",summary)
 except Exception as e:
  status('failed',error=repr(e),traceback=traceback.format_exc());raise
