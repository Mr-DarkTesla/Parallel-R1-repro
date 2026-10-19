"""Evaluation-only recovery after a verified complete warmup; never starts training."""
from pathlib import Path
import fcntl,hashlib,json,os,subprocess,time,traceback
from production_controller import D,P,PY,save,now,run,check_eval_sources

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 lock=(D/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert not Path('/proc/1249140').exists(),'Prior production controller alive'
 assert not (D/'posttrain-controller-started.json').exists(),'No duplicate evaluation queue'
 approval=json.loads((D/'posttrain-approved.json').read_text());assert approval['passed']
 for filename,expected in approval['hashes'].items():assert sha(D/filename)==expected,('Approval pin changed',filename)
 for record in ['controller-started.json','production-controller-started.json']:
  for filename,expected in json.loads((D/record).read_text())['hashes'].items():assert sha(D/filename)==expected,('Original startup source changed',filename)
 result=json.loads((D/'runs/production/result.json').read_text())
 assert result['state']=='complete' and result['steps']==129 and result['epochs']==3 and result['only_six_rows_updated'] and result['all_other_parameters_frozen_version_checks_passed']
 proof=json.loads((D/'export-byte-proof.json').read_text())
 assert proof['passed'] and proof['audit_source_version']==2 and proof['only_six_rows_changed'] and proof['new_rows_exact_committed_checkpoint'] and proof['old_embedding_rows_bitwise_identical']
 assert len(proof['all_other_tensors_bitwise_identical'])==398 and all(proof['all_other_tensors_bitwise_identical'].values())
 assert json.loads((D/'independent-export-v2-review.json').read_text())['passed']
 check_eval_sources()
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU occupied'
 (P/'t/warm4beval').mkdir(parents=True,exist_ok=True)
 save(D/'posttrain-controller-started.json',{'pid':os.getpid(),'at':now(),'source_sha256':sha(__file__),'evaluation_only':True,'no_training_or_weight_edits':True,'prior_failure':'native inline template vs expected standalone file; byte checks subsequently PASS v2'})
 launcher=D/'evaluations/run_eval.sh';native=P/'work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model';trained=D/'runs/production/final'
 smokes=[('native-runtime-smoke24',native,'native','math-system.txt'),('structured-runtime-smoke24',trained,'structured','system.txt')]
 for name,model,mode,system in smokes:
  check_eval_sources()
  run(['bash',launcher,'--model',model,'--name',name,'--suite','24','--mode',mode,'--system-file',D/system],name,3600)
  folder=D/'evaluations'/name;summary=json.loads((folder/'summary.json').read_text())
  assert summary['completed']==24 and summary['missing']==0
  assert json.loads((folder/'worker-exits.json').read_text())==[0]*8
 gate={'passed':True,'at':now(),'actual_gpus':8,'native_samples':24,'structured_samples':24,'trained_format_quality_is_an_outcome_not_an_admission_threshold':True,'hashes':{str(f.relative_to(D)):sha(f) for name,_,_,_ in smokes for f in [D/'evaluations'/name/'summary.json',D/'evaluations'/name/'scores.jsonl']}}
 save(D/'inference-smoke-gate.json',gate)
 save(D/'status.json',{'state':'awaiting_root_inference_smoke_review','at':now(),'controller_pid':os.getpid(),'smoke_gate':'inference-smoke-gate.json','training_complete129':True})
 deadline=time.monotonic()+3600
 while not (D/'root-inference-smoke-approved.json').exists():
  if time.monotonic()>deadline:raise TimeoutError('Root actual inference smoke review pending')
  time.sleep(5)
 admission=json.loads((D/'root-inference-smoke-approved.json').read_text())
 assert admission['passed'] and admission['smoke_gate_sha256']==sha(D/'inference-smoke-gate.json')
 for f,expected in gate['hashes'].items():assert sha(D/f)==expected
 evaluations=[('original-native-128',native,'native','math-system.txt'),('trained-native-128',trained,'native','math-system.txt'),('initial-structured-128',D/'init-model','structured','system.txt'),('trained-structured-128',trained,'structured','system.txt')]
 for name,model,mode,system in evaluations:
  check_eval_sources()
  run(['bash',launcher,'--model',model,'--name',name,'--suite','128','--mode',mode,'--system-file',D/system],name,7200)
  folder=D/'evaluations'/name;summary=json.loads((folder/'summary.json').read_text())
  assert summary['completed']==128 and summary['missing']==0 and json.loads((folder/'worker-exits.json').read_text())==[0]*8
 save(D/'status.json',{'state':'complete','finished_at':now(),'controller_pid':os.getpid(),'training':result,'evaluations':[x[0] for x in evaluations],'only_six_embedding_rows_trained':True,'no_RL_or_LoRA_or_backbone_updates':True})
if __name__=='__main__':
 try:main()
 except BlockingIOError:
  raise SystemExit('An existing controller owns the lock; status untouched')
 except BaseException as error:
  save(D/'status.json',{'state':'failed','at':now(),'controller_pid':os.getpid(),'error':repr(error),'evaluation_only':True,'training_complete129':True});traceback.print_exc();raise
