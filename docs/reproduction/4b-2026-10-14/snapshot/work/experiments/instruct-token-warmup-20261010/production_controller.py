"""Own Sirius8GPU queue: audited CPU ->2step smoke ->3epoch rows-only warmup ->fixed validation."""
from pathlib import Path
import datetime as dt,fcntl,hashlib,json,os,signal,subprocess,sys,time,traceback
D=Path(__file__).resolve().parent;P=D.parents[2];PY=P/'.venv/bin/python'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def save(path,value):
 path=Path(path);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def run(command,name,timeout):
 log=D/(name+'.log');state={'state':'running','stage':name,'controller_pid':os.getpid(),'started_at':now(),'command':list(map(str,command)),'log':str(log)}
 env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(P/'t/warm4beval'),XDG_CACHE_HOME=str(D/'cache'),HF_HOME=str(D/'cache/huggingface'),CUDA_CACHE_PATH=str(D/'cache/cuda'),TORCHINDUCTOR_CACHE_DIR=str(D/'cache/torchinductor'),WANDB_MODE='disabled')
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

def check_eval_sources():
 ready=json.loads((D/'evaluations/ready.json').read_text())
 assert ready['cpu_passed']
 for filename,expected in ready['sha256'].items():assert hashlib.sha256(Path(filename).read_bytes()).hexdigest()==expected,('Eval source pin',filename)

def main():
 lock=(D/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert not (D/'production-controller-started.json').exists(),'No duplicate production'
 handoff=json.loads((D/'production-handoff.json').read_text())
 assert handoff['prior_state']=='awaiting_root_smoke_review' and handoff['prior_controller_pid']==1248043
 assert not Path('/proc') .joinpath(str(handoff['prior_controller_pid'])).exists(),'Prior controller still alive'
 old_start=json.loads((D/'controller-started.json').read_text())
 for name,expected in old_start['hashes'].items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==expected,('Prior source changed',name)
 independent=json.loads((D/'independent-smoke-review.json').read_text())
 assert independent['passed'] and independent['actual8GPU2step_completed']
 assert independent['smoke_gate_sha256']==hashlib.sha256((D/'smoke-gate.json').read_bytes()).hexdigest()
 for name,expected in handoff['reviewed_hashes'].items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==expected,('Handoff pin changed',name)
 (P/'t/warm4beval').mkdir(parents=True,exist_ok=True)
 check_eval_sources()
 assert json.loads((D/'data-audit.json').read_text())['passed']
 assert json.loads((D/'independent-train-review.json').read_text())['passed']
 assert json.loads((D/'initialization-proof.json').read_text())['passed']
 assert json.loads((D/'evaluations/cpu-proof.json').read_text())['passed']
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU occupied: do not touch another process'
 hashes={str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [D/'train.py',D/'data.py',D/'controller.py',D/'system.txt',D/'math-system.txt',D/'tokenizer-proof.json',D/'production_controller.py',D/'audit_export.py',D/'evaluations/ready.json',D/'evaluations/run_eval.sh']}
 review=json.loads((D/'independent-train-review.json').read_text())
 for key,field in [('train.py','train_source_sha256'),('data.py','data_source_sha256')]:assert review[field]==hashes[key],('Independent review stale',key)
 save(D/'production-controller-started.json',{'pid':os.getpid(),'at':now(),'hashes':hashes,'gpus':list(range(8)),'authorized_new_experiment_outside_old_night':True})
 launch=[PY,'-m','torch.distributed.run','--standalone','--nnodes=1','--nproc_per_node=8',D/'train.py']
 # Reuse independently reviewed completed two-step smoke; never reuse its optimizer or rows.
 result=json.loads((D/'runs/smoke/result.json').read_text());init=json.loads((D/'runs/smoke/initialization-proof.json').read_text())
 assert result['steps']==2 and result['only_six_rows_updated'] and result['trainable_parameters']==15360 and init['rank0_gpu_isolation']['passed'] and init['ddp_frozen_bytes_equal']
 metrics=[json.loads(x) for x in (D/'runs/smoke/metrics.jsonl').read_text().splitlines()];assert len(metrics)==2 and all(m['frozen_parameter_versions_unchanged'] for m in metrics) and metrics[-1]['row_update_l2']>0
 for key in ['train.py','data.py']:assert hashlib.sha256((D/key).read_bytes()).hexdigest()==hashes[key]
 assert json.loads((D/'smoke-gate.json').read_text())['passed']
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
 run([PY,D/'audit_export.py'],'export-audit',1800)
 assert json.loads((D/'export-byte-proof.json').read_text())['passed']
 # Fixed before/after evaluations. Both initial and final weights are immutable during evaluation.
 check_eval_sources()
 evalfile=D/'evaluations/run_eval.sh';native=P/'work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model'
 # Actual runtime smoke; model format quality is an outcome, not an admission requirement for this token warmup.
 for name,model,mode,system in [('native-runtime-smoke24',native,'native','math-system.txt'),('structured-runtime-smoke24',D/'runs/production/final','structured','system.txt')]:
  run(['bash',evalfile,'--model',model,'--name',name,'--suite','24','--mode',mode,'--system-file',D/system],name,3600)
  summary=json.loads((D/'evaluations'/name/'summary.json').read_text())
  assert summary['completed']==24 and summary['missing']==0
  assert json.loads((D/'evaluations'/name/'worker-exits.json').read_text())==[0]*8
 check_eval_sources()
 evaluations=[('original-native-128',native,'native','math-system.txt'),('trained-native-128',D/'runs/production/final','native','math-system.txt'),('initial-structured-128',D/'init-model','structured','system.txt'),('trained-structured-128',D/'runs/production/final','structured','system.txt')]
 for name,model,mode,system in evaluations:
  run(['bash',evalfile,'--model',model,'--name',name,'--suite','128','--mode',mode,'--system-file',D/system],name,7200)
 save(D/'status.json',{'state':'complete','finished_at':now(),'controller_pid':os.getpid(),'training':result,'evaluations':[x[0] for x in evaluations],'only_six_embedding_rows_trained':True,'no_RL_or_LoRA_or_backbone_updates':True})
if __name__=='__main__':
 try:main()
 except BaseException as error:
  save(D/'status.json',{'state':'failed','at':now(),'controller_pid':os.getpid(),'error':repr(error)});traceback.print_exc();raise
