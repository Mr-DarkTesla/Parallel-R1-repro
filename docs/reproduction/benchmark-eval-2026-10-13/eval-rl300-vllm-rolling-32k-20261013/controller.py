"""Eight owned eval children on each host; no RL startup and no extra allocation."""
from pathlib import Path
import argparse,fcntl,json,os,socket,subprocess,time,traceback,hashlib
R=Path('${PROJECT_ROOT}');os.chdir(R)
E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013';C=E/'control';C.mkdir(parents=True,exist_ok=True)
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def save(path,d):
 temp=path.with_name(path.name+'.tmp-'+str(os.getpid()));temp.write_text(json.dumps(d,indent=2)+'\n');os.replace(temp,path)
def empty():return not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
def wait(path):
 while not path.exists():
  if list(C.glob('failure-node-*.json')):raise RuntimeError('Eval peer failed; preserve healthy children and traces')
  time.sleep(5)
 return json.loads(path.read_text())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--node',required=True,type=int);a=parser.parse_args();node=a.node
 roles=['mpimaster-0','mpiworker-0','mpiworker-1','mpiworker-2'];assert 0<=node<4 and socket.gethostname().endswith(roles[node])
 lock=(C/f'node-{node}.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 seal=json.loads((E/'source-seal.json').read_text())
 for path,digest in seal['sha256'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
 assert empty(),'Never launch over a live GPU process'
 save(C/f'ready-node-{node}.json',dict(passed=True,node=node,gpu_empty=True,time=time.time()))
 for n in range(4):assert wait(C/f'ready-node-{n}.json')['passed']
 procs={};exits={}
 for local in range(8):
  rank=node*8+local;env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(local),OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
  for key in ['RANK','LOCAL_RANK','WORLD_SIZE','LOCAL_WORLD_SIZE','MASTER_ADDR','MASTER_PORT','PYTHONPATH']:env.pop(key,None)
  site=R/'.venv/lib/python3.12/site-packages';env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'/usr/local/nvidia/lib','/usr/local/nvidia/lib64'])
  for key,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda')]:
   cache=E/'cache'/str(node)/leaf;cache.mkdir(parents=True,exist_ok=True);env[key]=str(cache)
  log=(E/f'rank-{rank}.log').open('ab',buffering=0);cmd=[str(PY),'-u',str(E/'worker.py'),'--job',str(E/'job.json'),'--rank',str(rank)]
  child=subprocess.Popen(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  raw=Path(f'/proc/{child.pid}/stat').read_text();fields=raw[raw.rfind(')')+2:].split()
  save(C/f'child-rank-{rank}.json',dict(pid=child.pid,start_ticks=fields[19],rank=rank,node=node,command=cmd,host=socket.gethostname(),time=time.time()));procs[rank]=(child,log)
 while procs:
  for rank,(child,log) in list(procs.items()):
   code=child.poll()
   if code is None:continue
   log.close();exits[str(rank)]=code;del procs[rank];save(C/f'exit-rank-{rank}.json',dict(rank=rank,returncode=code,time=time.time()))
  save(C/f'status-node-{node}.json',dict(state='evaluation',node=node,active={str(r):p.pid for r,(p,_) in procs.items()},exits=exits,time=time.time()));time.sleep(3)
 assert len(exits)==8 and all(v==0 for v in exits.values()),'Eval worker failed; preserve traces'
 assert empty(),'Eval children exited but GPU remains occupied'
 save(C/f'exits-node-{node}.json',dict(passed=True,node=node,exits=exits,gpu_empty=True,time=time.time()))
 for n in range(4):assert wait(C/f'exits-node-{n}.json')['passed']
 if node==0:
  subprocess.run([str(PY),str(E/'finalize.py')],cwd=R,check=True)
  save(C/'completed.json',dict(passed=True,checkpoint=300,all32exit0=True,all_gpu_empty=True,result=str(E/'result.json'),time=time.time()))
 wait(C/'completed.json');save(C/f'status-node-{node}.json',dict(state='completed',node=node,time=time.time()))
if __name__=='__main__':
 try:main()
 except BaseException as error:
  node=next((int(os.sys.argv[i+1]) for i,x in enumerate(os.sys.argv) if x=='--node'),-1);save(C/f'failure-node-{node}.json',dict(node=node,error=repr(error),traceback=traceback.format_exc(),time=time.time()));raise
