from pathlib import Path
import os,json,time,hashlib,subprocess,socket,traceback,importlib.util,concurrent.futures
from repair_io import recover,read_rows
R=Path('${PROJECT_ROOT}');os.chdir(R);B=Path(__file__).resolve().parent;Q=B.parent
PYTHON=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def write(name,value):
 p=B/name;t=p.with_suffix('.tmp');t.write_text(json.dumps(value,indent=2)+'\n');os.replace(t,p)
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(8<<20),b''):h.update(block)
 return h.hexdigest()
def proc(pid):
 p=Path('/proc')/str(pid)
 try:
  raw=(p/'stat').read_text();fields=raw[raw.rfind(')')+2:].split();cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode()
  return dict(pid=pid,state=fields[0],start_ticks=fields[19],exit_code=int(fields[49]),cmdline=cmd)
 except FileNotFoundError:return None
def free_gpu(rank):
 uuids=subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid','--format=csv,noheader'],text=True)
 uuid=dict((int(line.split(',')[0]),line.split(',')[1].strip()) for line in uuids.splitlines())[rank]
 apps=subprocess.check_output(['nvidia-smi','--query-compute-apps=gpu_uuid,pid','--format=csv,noheader'],text=True)
 return not any(line.split(',')[0].strip()==uuid for line in apps.splitlines())
def env(rank):
 e=dict(os.environ,CUDA_VISIBLE_DEVICES=str(rank),OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',PYTHONNOUSERSITE='1',VLLM_USE_V1='0',VLLM_WORKER_MULTIPROC_METHOD='spawn')
 for key in ['RANK','WORLD_SIZE','LOCAL_RANK','LOCAL_WORLD_SIZE','GROUP_RANK','MASTER_ADDR','MASTER_PORT','TORCHELASTIC_RUN_ID','TORCHELASTIC_USE_AGENT_STORE']:e.pop(key,None)
 e['PYTHONPATH']=str(B);site=R/'.venv/lib/python3.12/site-packages';e['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'${NVIDIA_ROOT}/lib','${NVIDIA_ROOT}/lib64'])
 for key,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('VLLM_CACHE_ROOT','vllm')]:
  p=B/'cache'/str(rank)/leaf;p.mkdir(parents=True,exist_ok=True);e[key]=str(p)
 return e
def launch(rank,stage):
 log=(B/f'{stage}-rank-{rank}.log').open('ab',buffering=0)
 child=subprocess.Popen([str(PYTHON),str(B/f'{stage}_worker.py'),'--job',str(B/f'{stage}-job.json'),'--rank',str(rank)],cwd=R,env=env(rank),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 write(f'{stage}-rank-{rank}-launch.json',dict(pid=child.pid,rank=rank,stage=stage,time=time.time(),identity=proc(child.pid),source_sha256=sha(B/f'{stage}_worker.py'),config_sha256=sha(B/f'{stage}-job.json')))
 return child,log
def native_proof():
 cfg=json.loads((B/'native-job.json').read_text());checks={}
 for name,digest in cfg['native_source_proof']['files'].items():
  actual=sha(Path(cfg['model'])/name);assert actual==digest,name;checks[name]=actual
 write('native-original-hashes-proof.json',dict(passed=True,revision=cfg['native_source_proof']['revision'],sha256=checks,time=time.time()))
 return True
def main():
 hold=json.loads((Q/'ROOT-REPAIR-HOLD.json').read_text());assert hold['gpu_children_untouched'] and hold['action'] in ['already_exited','SIGTERM','terminated','stopped']
 oldcontroller=proc(hold['controller_pid']);assert oldcontroller is None or oldcontroller['state']=='Z',oldcontroller
 proof=json.loads((B/'CPU-PROOF.json').read_text());assert proof['passed']
 for name,digest in proof['sha256'].items():assert sha(B/name)==digest,name
 manifest=json.loads((Q/'manifest.json').read_text());assert manifest['passed']
 for path,digest in manifest['sha256'].items():assert sha(path)==digest,path
 seal={str(p):sha(p) for p in B.glob('*.py')};write('SOURCE-SEAL.json',dict(passed=True,sha256=seal,original_manifest_sha256=sha(Q/'manifest.json'),hold_sha256=sha(Q/'ROOT-REPAIR-HOLD.json')))
 for stage in ['rl','native']:
  cfg=json.loads((Q/f'{stage}-job.json').read_text());cfg['output']=str(B/'runs'/('rl50-retries' if stage=='rl' else 'native-instruct'));write(f'{stage}-job.json',cfg)
 cfg=json.loads((B/'rl-job.json').read_text());spec=importlib.util.spec_from_file_location('frozen_scorer',cfg['scorer']);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
 owned={};states={str(r):'await_old_rl' for r in range(8)};active={};exits={str(r):{} for r in range(8)};errors={};evidence={}
 for rank in range(8):
  receipt=hold['children'][f'rl-rank-{rank}-launch.json'];observed=proc(receipt['pid'])
  if observed and observed['state']!='Z':assert str(Q/'rl_worker.py') in observed['cmdline'] and f'--rank {rank}' in observed['cmdline'],observed
  owned[rank]=dict(receipt=receipt,initial=observed)
 write('OLD-OWNERSHIP.json',owned)
 pool=concurrent.futures.ThreadPoolExecutor(1);native_future=pool.submit(native_proof)
 while any(state not in ['completed','failed'] for state in states.values()):
  for rank in range(8):
   key=str(rank);state=states[key]
   try:
    if state=='await_old_rl':
     owner=owned[rank];now=proc(owner['receipt']['pid']);initial=owner['initial']
     if now and initial:assert now['start_ticks']==initial['start_ticks'],'PID reuse detected'
     if now and now['state']!='Z':
      assert str(Q/'rl_worker.py') in now['cmdline'] and f'--rank {rank}' in now['cmdline'],'old PID identity mismatch';continue
     if not free_gpu(rank):continue
     log=Q/f'rl-rank-{rank}.log';text=log.read_text(errors='replace') if log.exists() else ''
     evidence[key]=dict(terminal=now or 'proc_absent',initial=initial,old_log_sha256=sha(log) if log.exists() else None,known_thread_error='threaded environment' in text or 'signal only works' in text,old_recorded_exits=json.loads((Q/'exits.json').read_text()).get(key,{}) if (Q/'exits.json').exists() else {})
     write('OLD-TERMINAL-EVIDENCE.json',evidence)
     recovered=recover(Q/'runs/rl50-retries',B/'runs/rl50-retries',rank,scorer);write(f'recovered-rank-{rank}.json',dict(ids=recovered,resampled_saved_answers=False))
     active[rank]=('rl',*launch(rank,'rl'));states[key]='rl'
    elif state in ['rl','native']:
     stage,child,log=active[rank];code=child.poll()
     if code is None:continue
     log.close();exits[key][stage]=code;write('exits.json',exits);del active[rank]
     if code!=0:raise RuntimeError(f'{stage} rank {rank} exited {code}; healthy ranks continue')
     states[key]='await_native' if stage=='rl' else 'completed'
    elif state=='await_native':
     if not native_future.done():continue
     assert native_future.result();oldreceipt=Q/f'native-rank-{rank}-launch.json'
     if oldreceipt.exists():
      receipt=json.loads(oldreceipt.read_text());now=proc(receipt['pid'])
      if now and now['state']!='Z':
       assert str(Q/'native_worker.py') in now['cmdline'] and f'--rank {rank}' in now['cmdline'],'native identity mismatch';continue
     if not free_gpu(rank):continue
     recover(Q/'runs/native-instruct',B/'runs/native-instruct',rank,scorer)
     active[rank]=('native',*launch(rank,'native'));states[key]='native'
   except Exception as error:
    states[key]='failed';errors[key]=dict(error=repr(error),traceback=traceback.format_exc());write('errors.json',errors)
  write('status.json',dict(state='running',pid=os.getpid(),host=socket.gethostname(),time=time.time(),ranks=states,exits=exits,errors=errors,native_hash_proof_ready=native_future.done(),no_gpu_worker_signals=True))
  time.sleep(3)
 pool.shutdown()
 if errors:raise RuntimeError(errors)
 subprocess.run([str(PYTHON),str(B/'finalize.py')],check=True,cwd=R)
 write('status.json',dict(state='completed',pid=os.getpid(),time=time.time(),ranks=states,exits=exits))
if __name__=='__main__':
 try:main()
 except BaseException as error:write('controller-failure.json',dict(error=repr(error),traceback=traceback.format_exc(),pid=os.getpid()));raise
