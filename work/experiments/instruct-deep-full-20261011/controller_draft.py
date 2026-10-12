"""Reviewed source draft: main8 teacher drain -> final data -> actual smoke -> full deep SFT.

Not launched while teacher owns GPUs. No allocation, stopping teacher, or Cloud mutations.
"""
from pathlib import Path
import json,hashlib,os,subprocess,time,sys,math
P=Path.cwd();B=P/'work/experiments/instruct-deep-full-20261011'
cfg=json.loads((B/'plan.json').read_text());PY=cfg['interpreter']
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
def write(p,r):
 p=Path(p);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(r,indent=2)+'\n');tmp.replace(p)
def source_gate():
 seal=B/'source-seal.json';r=read(B/'root-source-approved.json')
 assert r['approved'] and r['source_seal_sha256']==sha(seal)
 review=B/'independent-source-review.json';assert read(review)['passed'] and r['independent_source_review_sha256']==sha(review)
 assert read(review)['source_seal_sha256']==sha(seal)
 assert all(Path(k).resolve().is_relative_to(P) and sha(k)==v for k,v in read(seal)['sha256'].items())
def prepare_gate():
 assert all(Path(k).resolve().is_relative_to(P) and sha(k)==v for k,v in read(B/'prepare-proof.json')['manifest'].items())
def free_main8():
 # A recorded main hostname prevents accidental Cloud lane use.
 assert os.uname().nodename==cfg['main_hostname']
 drain=read(cfg['teacher_drained']);assert drain['passed'] and drain['teacher_processes_drained']
 if drain.get('teacher_pid'):
  assert not (Path('/proc')/str(drain['teacher_pid'])).exists()
 inventory=subprocess.check_output(['nvidia-smi','--query-gpu=index,name','--format=csv,noheader'],text=True).strip().splitlines()
 assert len(inventory)==8 and all('A100' in r for r in inventory)
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
def run(argv):subprocess.run(argv,cwd=P,check=True)
assert cfg['state']=='CPU_source_draft_not_GPU_released'
fd=os.open(B/'controller.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
while True:
 source_gate()
 required=[cfg[k] for k in ['train_jsonl','val_jsonl','data_manifest','data_admission','teacher_drained']]
 if all(Path(p).exists() for p in required):break
 write(B/'controller-status.json',dict(state='waiting_final_admitted_data_and_teacher_drain',pid=os.getpid(),updated=time.time()))
 time.sleep(30)
free_main8();write(B/'controller-status.json',dict(state='CPU_prepare',pid=os.getpid()))
run([PY,str(B/'prepare.py')]);source_gate()
prepare_gate();free_main8();write(B/'controller-status.json',dict(state='actual8GPU_smoke',pid=os.getpid()))
run(['bash',str(B/'run_train.sh'),'smoke']);run([PY,str(B/'audit_export.py')]);free_main8()
source_gate();prepare_gate();run(['bash',str(B/'run_train.sh'),'isolation']);free_main8()
smoke=read(B/'smoke-export-proof.json');isolation=read(B/'runs/isolation/isolation-proof.json')
assert smoke['passed'] and smoke['changed_tensor_count']>0 and any('layers.' in k for k in smoke['changed_tensors'])
init=read(B/'runs/smoke/initialization-proof.json');assert init['total_parameters']==4022468096 and init['trainable_parameters']==4022468096
assert isolation['passed'] and isolation['actual_full_fsdp_model'] and isolation['sibling_logits_max_abs_diff']<=1e-5 and isolation['merged_suffix_max_abs_diff']>0
assert all(sha(k)==v for k,v in read(B/'prepare-proof.json')['manifest'].items())
write(B/'actual-engineering-admission.json',dict(passed=True,source_seal_sha256=sha(B/'source-seal.json'),prepare_proof_sha256=sha(B/'prepare-proof.json'),smoke_export_sha256=sha(B/'smoke-export-proof.json'),isolation_proof_sha256=sha(B/'runs/isolation/isolation-proof.json'),init_proof_sha256=sha(B/'runs/smoke/initialization-proof.json'),autonomous_static_reviewed_gate=True))
source_gate();prepare_gate();free_main8();write(B/'controller-status.json',dict(state='production_fullSFT_running',pid=os.getpid(),actual_engineering_admission_sha256=sha(B/'actual-engineering-admission.json')))
run(['bash',str(B/'run_train.sh'),'production'])
terminal=read(B/'runs/production/result.json');assert terminal['state']=='complete' and terminal['steps']==126 and terminal['full_model'] and terminal['think_wrapped']
run([PY,str(B/'audit_production.py')]);assert read(B/'production-export-proof.json')['passed']
observations=[json.loads(x) for x in (B/'runs/production/epoch-validation.jsonl').read_text().splitlines()]
assert {r['step'] for r in observations}=={42,84}
observations.append(dict(epoch=3,step=126,clean_validation_ce=terminal['val_loss']))
assert all(math.isfinite(r['clean_validation_ce']) for r in observations)
best=min(observations,key=lambda r:r['clean_validation_ce'])
write(B/'clean-validation-selection.json',dict(passed=True,selection_source='teacher-holdout300-fullresponseCE ONLY',observations=observations,selected_step=best['step'],selected_checkpoint=str(B/'runs/production'/('global_step_'+str(best['step']))),benchmark_selection=False))
write(B/'controller-status.json',dict(state='completed',pid=os.getpid(),steps=126,epochs=3,clean_validation_ce=terminal['val_loss'],production_result_sha256=sha(B/'runs/production/result.json'),production_export_proof_sha256=sha(B/'production-export-proof.json'),clean_validation_selection_sha256=sha(B/'clean-validation-selection.json')))
