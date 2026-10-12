"""Own Sirius8GPU queue: audited CPU ->2step smoke ->3epoch rows-only warmup ->fixed validation."""
from pathlib import Path
import datetime as dt,fcntl,hashlib,json,os,signal,subprocess,sys,time,traceback
D=Path(__file__).resolve().parent;P=D.parents[2];PY=P/'.venv/bin/python'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def save(path,value):
 path=Path(path);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def run(command,name,timeout):
 log=D/(name+'.log');state={'state':'running','stage':name,'controller_pid':os.getpid(),'started_at':now(),'command':list(map(str,command)),'log':str(log)}
 env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(D/'tmp'),XDG_CACHE_HOME=str(D/'cache'),HF_HOME=str(D/'cache/huggingface'),CUDA_CACHE_PATH=str(D/'cache/cuda'),TORCHINDUCTOR_CACHE_DIR=str(D/'cache/torchinductor'),WANDB_MODE='disabled')
 with log.open('x') as f:
  proc=subprocess.Popen(list(map(str,command)),cwd=P,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  state.update(pid=proc.pid,owned_process_group=proc.pid);save(D/'status.json',state)
  began=time.monotonic()
  while proc.poll() is None:
   if time.monotonic()-began>timeout:
    os.killpg(proc.pid,signal.SIGTERM)
    try:proc.wait(timeout=60)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
    raise TimeoutError(name+' own process exceeded timeout')
   state['heartbeat_at']=now()
   progress=D/'runs'/name/'status.json'
   if progress.exists():state['training_progress']=json.loads(progress.read_text())
   save(D/'status.json',state);time.sleep(10)
  state.update(returncode=proc.returncode,finished_at=now());save(D/(name+'-process-result.json'),state)
  assert proc.returncode==0,(name,proc.returncode)
 return state

def main():
 lock=(D/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert not (D/'controller-started.json').exists(),'No duplicate/restart'
 assert json.loads((D/'data-audit.json').read_text())['passed']
 assert json.loads((D/'independent-train-review.json').read_text())['passed']
 assert json.loads((D/'initialization-proof.json').read_text())['passed']
 assert json.loads((D/'evaluations/cpu-proof.json').read_text())['passed']
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU occupied: do not touch another process'
 hashes={str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [D/'train.py',D/'data.py',D/'controller.py',D/'system.txt',D/'math-system.txt',D/'tokenizer-proof.json']}
 review=json.loads((D/'independent-train-review.json').read_text())
 for key,field in [('train.py','train_source_sha256'),('data.py','data_source_sha256')]:assert review[field]==hashes[key],('Independent review stale',key)
 save(D/'controller-started.json',{'pid':os.getpid(),'at':now(),'hashes':hashes,'gpus':list(range(8)),'authorized_new_experiment_outside_old_night':True})
 launch=[PY,'-m','torch.distributed.run','--standalone','--nnodes=1','--nproc_per_node=8',D/'train.py']
 run(launch+['--stage','smoke'],'smoke',2400)
 result=json.loads((D/'runs/smoke/result.json').read_text());init=json.loads((D/'runs/smoke/initialization-proof.json').read_text())
 assert result['steps']==2 and result['only_six_rows_updated'] and result['trainable_parameters']==15360 and init['rank0_gpu_isolation']['passed']
 metrics=[json.loads(x) for x in (D/'runs/smoke/metrics.jsonl').read_text().splitlines()];assert len(metrics)==2 and all(m['frozen_parameter_versions_unchanged'] for m in metrics) and metrics[-1]['row_update_l2']>0
 for key in ['train.py','data.py']:assert hashlib.sha256((D/key).read_bytes()).hexdigest()==hashes[key]
 save(D/'smoke-gate.json',{'passed':True,'at':now(),'actual_gpus':8,'actual_optimizer_steps':2,'only15360_parameters_trainable':True,'actual_nonzero_row_update':metrics[-1]['row_update_l2'],'GPU_sibling_isolation':init['rank0_gpu_isolation'],'CPU_data_audit':'data-audit.json','frozen_base_versions_unchanged':True,'smoke_updates_not_used_for_production':True})
 # Root reads actual2step proof before admitting production; no auto-admission from CPU tests.
 approval_deadline=time.monotonic()+1800
 save(D/'status.json',{'state':'awaiting_root_smoke_review','at':now(),'controller_pid':os.getpid(),'smoke_gate':'smoke-gate.json'})
 while not (D/'root-smoke-approved.json').exists():
  if time.monotonic()>approval_deadline:raise TimeoutError('Root smoke review not received')
  time.sleep(5)
 approval=json.loads((D/'root-smoke-approved.json').read_text())
 assert approval['passed'] and approval['smoke_gate_sha256']==hashlib.sha256((D/'smoke-gate.json').read_bytes()).hexdigest()
 run(launch+['--stage','production'],'production',18000)
 result=json.loads((D/'runs/production/result.json').read_text());assert result['state']=='complete' and result['epochs']==3 and result['only_six_rows_updated']
 # Fixed before/after evaluations. Both initial and final weights are immutable during evaluation.
 evalfile=D/'evaluations/evaluate.py';native=P/'work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model'
 evaluations=[('original-native-128',native,'native','math-system.txt'),('trained-native-128',D/'runs/production/final','native','math-system.txt'),('initial-structured-128',D/'init-model','structured','system.txt'),('trained-structured-128',D/'runs/production/final','structured','system.txt')]
 for name,model,mode,system in evaluations:
  run([PY,evalfile,'--model',model,'--name',name,'--suite','128','--mode',mode,'--system-file',D/system],name,7200)
 save(D/'status.json',{'state':'complete','finished_at':now(),'controller_pid':os.getpid(),'training':result,'evaluations':[x[0] for x in evaluations],'only_six_embedding_rows_trained':True,'no_RL_or_LoRA_or_backbone_updates':True})
if __name__=='__main__':
 try:main()
 except BaseException as error:
  save(D/'status.json',{'state':'failed','at':now(),'controller_pid':os.getpid(),'error':repr(error)});traceback.print_exc();raise
