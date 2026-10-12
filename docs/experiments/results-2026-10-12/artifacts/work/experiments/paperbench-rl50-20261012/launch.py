from pathlib import Path
import json,os,subprocess,time,socket,hashlib,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R);B=R/'work/experiments/paperbench-rl50-20261012'
python=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def save(state,**kw):(B/'status.json').write_text(json.dumps(dict(state=state,pid=os.getpid(),host=socket.gethostname(),time=time.time(),**kw),indent=2)+'\n')
try:
 assert not (B/'result.json').exists();manifest=json.loads((B/'manifest.json').read_text());assert manifest['passed'] and manifest['samples_per_question']==1
 for p,d in manifest['sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==d,p
 for path in manifest['jobs']:
  job=json.loads(Path(path).read_text());name=Path(path).name
  occupied=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True);assert not occupied.strip(),occupied
  save('evaluating',job=name);children=[];logs=[]
  for rank in range(8):
   env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(rank),OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',PYTHONNOUSERSITE='1');env.pop('PYTHONPATH',None)
   site=R/'.venv/lib/python3.12/site-packages';env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'${NVIDIA_ROOT}/lib','${NVIDIA_ROOT}/lib64'])
   cache=B/'cache'/str(rank);cache.mkdir(parents=True,exist_ok=True)
   for variable,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton')]:
    p=cache/leaf;p.mkdir(exist_ok=True);env[variable]=str(p)
   log=(B/(name+f'-rank-{rank}.log')).open('ab',buffering=0);logs.append(log)
   children.append(subprocess.Popen([str(python),str(B/'worker.py'),'--job',path,'--rank',str(rank)],env=env,cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True))
  (B/(name+'-launch.json')).write_text(json.dumps(dict(pids=[p.pid for p in children],job=path,hostname=socket.gethostname(),time=time.time()),indent=2)+'\n')
  codes=[p.wait() for p in children]
  for log in logs:log.close()
  (B/(name+'-exits.json')).write_text(json.dumps(dict(returncodes=codes,time=time.time()),indent=2)+'\n');assert codes==[0]*8,codes
  subprocess.run([str(python),str(B/'finalize.py'),path],cwd=R,check=True)
 save('completed');(B/'result.json').write_text(json.dumps(dict(completed=True,checkpoint=50,samples_per_question=1,jobs=manifest['jobs'],time=time.time()),indent=2)+'\n')
except BaseException as error:save('failed',error=repr(error),traceback=traceback.format_exc());raise
