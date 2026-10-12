"""Owned worker2 only: CPU→one GPU probability + FP32 geometry→all8 cases."""
import os,json,time,subprocess,socket,hashlib,fcntl,traceback,shutil
from pathlib import Path
R=Path('${PROJECT_ROOT}');os.chdir(R);ROOT=Path(__file__).resolve().parent;A=ROOT/'attempt1';PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(name,data):
 p=A/name;p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,p)
def status(state,**kw):write('status.json',dict(state=state,pid=os.getpid(),host=socket.gethostname(),time=time.time(),**kw))
def identity(pid):
 try:
  p=Path('/proc')/str(pid);raw=(p/'stat').read_text();fields=raw[raw.rfind(')')+2:].split();return dict(state=fields[0],start_ticks=fields[19],cmdline=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode())
 except FileNotFoundError:return None
def free(gpu=None):
 rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid,memory.used,utilization.gpu','--format=csv,noheader'],text=True)
 data=[line.split(',') for line in rows.splitlines()];mapping={int(r[0]):r[1].strip() for r in data}
 apps=subprocess.check_output(['nvidia-smi','--query-compute-apps=gpu_uuid,pid','--format=csv,noheader'],text=True)
 targets=list(mapping) if gpu is None else [gpu]
 return not any(any(line.split(',')[0].strip()==mapping[g] for line in apps.splitlines()) for g in targets) and all(int(r[2].split()[0])==0 and int(r[3].strip().split()[0])==0 for r in data if int(r[0]) in targets)
def env(gpu=None):
 e=dict(os.environ,CUDA_VISIBLE_DEVICES='' if gpu is None else str(gpu),VLLM_USE_V1='0',VLLM_WORKER_MULTIPROC_METHOD='spawn',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='1',PYTHONPATH=str(A/'src'))
 if gpu is None:e.pop('STRUCTURED_GPU_AUTHORIZED',None)
 else:e['STRUCTURED_GPU_AUTHORIZED']='1'
 for k in ['RANK','WORLD_SIZE','LOCAL_RANK','LOCAL_WORLD_SIZE','GROUP_RANK','MASTER_ADDR','MASTER_PORT','TORCHELASTIC_RUN_ID']:e.pop(k,None)
 e['TORCHELASTIC_USE_AGENT_STORE']='False';site=R/'.venv/lib/python3.12/site-packages';e['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'${NVIDIA_ROOT}/lib','${NVIDIA_ROOT}/lib64'])
 for k,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('VLLM_CACHE_ROOT','vllm')]:
  p=A/'cache'/str(gpu)/leaf;p.mkdir(parents=True,exist_ok=True);e[k]=str(p)
 return e
def launch(gpu,width,problem,mode,label,cfg,receipt):
 assert free(gpu),f'AssignedGPU{gpu} occupied; no overlap'
 c=dict(cfg,width=width,problem_index=problem,mode=mode,output=str(A/label),port=30971+gpu,input_receipt=receipt)
 if label.startswith('rank-7-'):c['natural_source']=str(R/'work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/traces-rank-7.jsonl')
 write(label+'-job.json',c);log=(A/(label+'.log')).open('ab',buffering=0)
 p=subprocess.Popen([str(PY),'-u',str(A/'src/gpu_contract.py'),'--job',str(A/(label+'-job.json'))],cwd=R,env=env(gpu),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 write(label+'-launch.json',dict(pid=p.pid,gpu=gpu,width=width,mode=mode,identity=identity(p.pid),config_sha256=sha(A/(label+'-job.json')),time=time.time()));return p,log

def main():
 A.mkdir(parents=True,exist_ok=True);lock=(A/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert socket.gethostname()=='RUN_5482aee87e-mpiworker-2'
 status('fresh_empty_gpu_check');assert free();write('GPU-EMPTY-RECEIPT.json',dict(host=socket.gethostname(),all8_empty=True,time=time.time()))
 assert not (A/'src').exists(),'Never overwrite an active/sealed proof snapshot';shutil.copytree(ROOT/'src',A/'src',ignore=shutil.ignore_patterns('__pycache__','._*'))
 cfg=json.loads((ROOT/'base-job.json').read_text());status('input_and_source_hash_guard')
 assert sha(A/'src/source/parallel_structure.py')=='f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f'
 receipt=dict(model_sha256=sha(Path(cfg['model'])/'model.safetensors'),train_sha256=sha(cfg['train']),system_sha256=sha(cfg['system']),source_sha256={str(p.relative_to(A)):sha(p) for p in (A/'src').rglob('*.py')})
 assert receipt['model_sha256']==cfg['expected_model_sha256'] and receipt['train_sha256']==cfg['expected_train_sha256'];write('INPUT-AND-SOURCE-SEAL.json',receipt)
 status('CPU_contract_gate')
 for script,name in [('proof_contract_cpu.py','CPU-TIS-PROOF.json'),('proof_rollout_cpu.py','CPU-MASK-PROOF.json')]:
  with (A/(name+'.log')).open('wb') as log:subprocess.run([str(PY),str(A/'src'/script),'--output',str(A/name)],cwd=R,env=env(),stdout=log,stderr=subprocess.STDOUT,check=True)
  assert json.loads((A/name).read_text())['passed']
 assert free();initial={0:launch(0,4,0,'probability','pilot-probability',cfg,receipt),1:launch(1,4,1,'geometry','pilot-FP32-geometry',cfg,receipt)};status('parallel_oneGPU_initial_proofs',pids={str(g):p.pid for g,(p,_) in initial.items()});exits={}
 while initial:
  for g,(p,log) in list(initial.items()):
   code=p.poll()
   if code is None:continue
   log.close();exits[str(g)]=code;del initial[g];write('pilot-exits.json',exits)
  time.sleep(2)
 assert all(c==0 for c in exits.values()),'Initial bounded proof failed; preserve logs, no expansion'
 assert json.loads((A/'pilot-probability/proof.json').read_text())['passed'] and json.loads((A/'pilot-FP32-geometry/proof.json').read_text())['passed'];assert free()
 widths=[2,3,4,6,8,2,6,8];procs={g:launch(g,w,g,'probability',f'rank-{g}-width{w}',cfg,receipt) for g,w in enumerate(widths)};exits={};status('all8_different_problem_contracts',pids={str(g):p.pid for g,(p,_) in procs.items()})
 while procs:
  for g,(p,log) in list(procs.items()):
   code=p.poll()
   if code is None:continue
   log.close();exits[str(g)]=code;del procs[g];write('all8-exits.json',exits)
  status('all8_different_problem_contracts',active={str(g):p.pid for g,(p,_) in procs.items()},exits=exits);time.sleep(3)
 assert all(c==0 for c in exits.values());assert free();proofs=[json.loads((A/f'rank-{g}-width{w}/proof.json').read_text()) for g,w in enumerate(widths)]
 assert len({p['problem_id'] for p in proofs})==8 and all(p['passed'] for p in proofs)
 write('RESULT.json',dict(passed=True,all8_exit0=True,all8_GPU_empty=True,proofs=proofs,pilot_geometry=json.loads((A/'pilot-FP32-geometry/proof.json').read_text()),scope='n1 actor→BF16 teacher math/mask/probability proof; not Adam/IPC/full32/speed'))
 status('completed',all8_exit0=True,all8_GPU_empty=True)
if __name__=='__main__':
 try:main()
 except BaseException as error:status('failed',error=repr(error),traceback=traceback.format_exc());raise
