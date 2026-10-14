"""One platform MPI parent/rank, eight production children; NO fresh GPU smoke."""
from pathlib import Path
import hashlib,json,os,socket,subprocess,time,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R);P=Path('${PROJECT_ROOT}/work/experiments/rl-r4-dapo2k-sft-16gpu-20261013');C=P/'control';C.mkdir(exist_ok=True)
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def save(path,d):
 t=path.with_name(path.name+'.tmp-'+str(os.getpid()));t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,path)
def wait(path,timeout=86400):
 start=time.monotonic()
 while not path.exists():
  if list(C.glob('failure-rank-*.json')):raise RuntimeError('Peer failure; preserve evidence')
  if time.monotonic()-start>timeout:raise TimeoutError(str(path))
  time.sleep(2)
 return json.loads(path.read_text())
def ident(pid):
 raw=Path(f'/proc/{pid}/stat').read_text();f=raw[raw.rfind(')')+2:].split();return dict(pid=pid,start_ticks=f[19])
rank=int(os.environ.get('RANK',os.environ.get('OMPI_COMM_WORLD_RANK','-1')));local=int(os.environ.get('LOCAL_RANK',os.environ.get('OMPI_COMM_WORLD_LOCAL_RANK','-1')));world=int(os.environ.get('WORLD_SIZE',os.environ.get('OMPI_COMM_WORLD_SIZE','0')))
try:
 assert world==16 and 0<=rank<16 and local==rank%8,(rank,local,world)
 # Exclusive bootstrap prevents platform retry from duplicating already-launched training.
 with (C/f'entry-claim-rank-{rank}.json').open('x') as f:json.dump(dict(rank=rank,host=socket.gethostname(),**ident(os.getpid()),time=time.time()),f)
 ready=json.loads((P/'LAUNCH-READY.json').read_text());assert ready['passed'] and ready['world_size']==16
 for path,digest in ready['sha256'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
 if local==0:assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 save(C/f'ready-rank-{rank}.json',dict(rank=rank,local_rank=local,host=socket.gethostname(),time=time.time()))
 if rank==0:
  records=[wait(C/f'ready-rank-{r}.json',600) for r in range(16)];assert len({r['host'] for r in records})==2
  assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
  s=socket.socket();s.bind(('',0));port=s.getsockname()[1];s.close();save(C/'master.json',dict(address=socket.gethostbyname(socket.gethostname()),port=port,world_size=16))
 master=wait(C/'master.json',600)
 env=dict(os.environ,RANK=str(rank),WORLD_SIZE='16',LOCAL_RANK=str(local),LOCAL_WORLD_SIZE='8',MASTER_ADDR=master['address'],MASTER_PORT=str(master['port']),TORCHELASTIC_USE_AGENT_STORE='False',PYTHONPATH=str(P/'src'),PYTHONNOUSERSITE='1',STRUCTURED_GPU_AUTHORIZED='1',VLLM_USE_V1='0',VLLM_WORKER_MULTIPROC_METHOD='spawn',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',NCCL_DEBUG='WARN')
 site=R/'.venv/lib/python3.12/site-packages';env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'/usr/local/nvidia/lib','/usr/local/nvidia/lib64'])
 for var,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('VLLM_CACHE_ROOT','vllm')]:
  cache=P/'cache'/leaf;cache.mkdir(parents=True,exist_ok=True);env[var]=str(cache)
 cmd=[str(PY),'-u',str(P/'src/train.py'),'--config',str(P/'production-config.json'),'--receipt',str(C/'production-approved.json')]
 with (P/f'production-rank-{rank}.log').open('ab',buffering=0) as log:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);save(C/f'production-child-rank-{rank}.json',dict(rank=rank,command=cmd,host=socket.gethostname(),**ident(child.pid),time=time.time()));code=child.wait()
 save(C/f'production-exit-rank-{rank}.json',dict(rank=rank,returncode=code,time=time.time()));assert code==0,'Production child failed; no blind restart'
 for r in range(16):assert wait(C/f'production-exit-rank-{r}.json',14*86400)['returncode']==0
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 save(C/f'gpu-empty-rank-{rank}.json',dict(passed=True,rank=rank,time=time.time()))
 if rank==0:
  for r in range(16):assert wait(C/f'gpu-empty-rank-{r}.json')['passed']
  result=json.loads((P/'production/result.json').read_text());assert result['completed'] and result['steps']==150
  save(C/'completed.json',dict(passed=True,initial_step=0,target_step=150,new_iterations=150,all16exit0=True,all_gpu_empty=True,time=time.time()))
 wait(C/'completed.json',600)
except BaseException as error:
 save(C/f'failure-rank-{rank}.json',dict(rank=rank,error=repr(error),traceback=traceback.format_exc(),time=time.time()));raise
