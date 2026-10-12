"""Durable full500 orchestrator; no future agent/human message needed after source approval."""
import subprocess,sys,time,os
from common import *
lock=HERE/'controller.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
status=HERE/'status.json';result307=ROOT/'work/experiments/night-20261010/cloud-continued/tmp2/results/307-instruct-rl-bs32-technical-step-resume.json'
while True:
 try:
  s,r=source_gate()
  if not result307.exists():write(status,dict(state='waiting_actual307',pid=os.getpid(),updated=time.time()));time.sleep(30);continue
  bs32=False;review=BASE/'long-run/independent-batch32-runtime-review.json';reason='307 technical failure: explicit verified8prompt fallback'
  if read(result307)['returncode']==0:
   completed=subprocess.run([sys.executable,str(ROOT/'work/experiments/instruct-full-20261011/audit_batch32_runtime.py'),'--result',str(result307),'--output',str(review)],cwd=ROOT)
   bs32=completed.returncode==0 and read(review).get('passed',False);reason='actual32prompt proof and independent executable runtime review PASS' if bs32 else '307 runtime audit failed: explicit verified8prompt fallback'
  data=BASE/'data/revision2';choice='admitted_revision2_fallback128train32val';public=BASE/'data/revision4-public'
  if all((public/f).exists() for f in ['manifest.json','independent-admission-review.json','actual4b-difficulty-review.json']):
   m=read(public/'manifest.json');ad=read(public/'independent-admission-review.json');difficulty=read(public/'actual4b-difficulty-review.json')
   if m.get('passed') and all(m.get(k) for k in ['group_disjoint','independent_actual_answer_review','reference_parser_compatible','math_all_train_test_excluded','reserved_aime_excluded','long_run_admitted']) and ad.get('passed') and difficulty.get('passed') and ad.get('manifest_sha256')==sha(public/'manifest.json') and difficulty.get('manifest_sha256')==sha(public/'manifest.json'):
    data=public;choice='independently_admitted_public_revision4_with_actual_difficulty'
  m=read(data/'manifest.json');assert m['passed'] and m['train_sha256']==sha(data/'train.jsonl') and m['val_sha256']==sha(data/'val.jsonl')
  decision=dict(target_steps=500,initial16_immutable=True,additional_updates=484,batch32_passed=bs32,prompts_per_rank=4 if bs32 else 1,global_prompts=32 if bs32 else 8,rollouts_per_prompt=4,historical_responses=256,reason=reason,data=str(data),data_choice=choice,train=str(data/'train.jsonl'),val=str(data/'val.jsonl'),manifest=str(data/'manifest.json'),manifest_sha256=sha(data/'manifest.json'),train_sha256=sha(data/'train.jsonl'),val_sha256=sha(data/'val.jsonl'),train_count=len((data/'train.jsonl').read_text().splitlines()),val_count=len((data/'val.jsonl').read_text().splitlines()),result307_sha256=sha(result307),runtime_review_sha256=sha(review) if review.exists() else None,created=time.time())
  if data==public:
   decision.update(admission_review=str(public/'independent-admission-review.json'),admission_review_sha256=sha(public/'independent-admission-review.json'),difficulty_review=str(public/'actual4b-difficulty-review.json'),difficulty_review_sha256=sha(public/'actual4b-difficulty-review.json'))
  assert not (HERE/'decision.json').exists();write(HERE/'decision.json',decision)
  for mode,lane,num in [('strong_width','tmp2',308),('forward_only','tmp3',233)]:
   prior=ROOT/'work/experiments/night-20261010/cloud-continued'/lane/'results'/('306-instruct-rl-strong-width-stage16.json' if lane=='tmp2' else '232-instruct-rl-forward-only-stage16.json')
   q=ROOT/'work/experiments/night-20261010/cloud-continued'/lane/'queue'/f'{num}-instruct-rl-{mode}-full500.json';assert not q.exists()
   write(q,dict(argv=['bash',str(HERE/'arm.sh'),mode],cwd=str(ROOT),timeout_seconds=1209600,wait_for=[str(prior),str(HERE/'decision.json'),str(HERE/'source-root-approved.json')],production=True,lane=lane,total_steps=500))
  write(status,dict(state='full500_queued',pid=os.getpid(),decision_sha256=sha(HERE/'decision.json'),updated=time.time()));break
 except BaseException as e:write(status,dict(state='failed',error=repr(e),pid=os.getpid(),updated=time.time()));raise

while True:
 arms=[]
 for mode in ['strong_width','forward_only']:
  run=HERE/'runs'/(mode+'-full500');m=run/'metrics.jsonl';rows=[readline for readline in m.read_text().splitlines() if readline.strip()] if m.exists() else [];metrics=[__import__('json').loads(l) for l in rows]
  arms.append(dict(mode=mode,state=read(run/'status.json') if (run/'status.json').exists() else 'queued',completed=(run/'result.json').exists(),training_iterations=metrics[-1]['step'] if metrics else 16,actual_optimizer_updates=sum(any(r['optimizer_step'] for r in z['ranks']) for z in metrics),initial_stage16_updates_not_in_counter=True))
 write(status,dict(state='completed' if all(z['completed'] for z in arms) else 'full500_queued_or_running',pid=os.getpid(),arms=arms,target_total_training_iterations=500,updated=time.time()))
 if all(z['completed'] for z in arms):break
 time.sleep(30)
