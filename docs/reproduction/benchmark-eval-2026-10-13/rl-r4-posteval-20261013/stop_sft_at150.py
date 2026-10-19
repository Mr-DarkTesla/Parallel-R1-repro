"""Cancel only the waiting CPU extension; keep live SFT training untouched."""
from pathlib import Path
import hashlib,json,os,signal,subprocess,time,shutil
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013';U=O/'continuation-150-to-200'
B=R/'work/experiments/rl-r4-posteval-20261013';Q=B/'sft'
assert not (U/'cloud-submission.json').exists(),'Continuation already submitted; reconcile before touching'
assert not (Q/'cloud-submission.json').exists(),'Eval already submitted; reconcile before touching'
def save(p,d):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
def info(pid):
 a=Path('/proc')/str(pid)
 try:
  s=(a/'stat').read_text();v=s[s.rfind(')')+2:].split();return dict(pid=pid,state=v[0],ticks=v[19],cmd=(a/'cmdline').read_bytes().replace(b'\0',b' ').decode())
 except FileNotFoundError:return None
def stop(launch,expected):
 d=json.loads(launch.read_text());a=info(d['pid']);assert a and a['ticks']==str(d['start_ticks']) and any(Path(arg).resolve()==expected.resolve() for arg in a['cmd'].split())
 os.kill(d['pid'],signal.SIGTERM)
 for _ in range(30):
  a=info(d['pid'])
  if not a or a['state']=='Z':break
  time.sleep(.1)
 a=info(d['pid'])
 if a and a['state']!='Z' and a['ticks']==str(d['start_ticks']):os.kill(d['pid'],signal.SIGKILL)
 return d
backup=Q/'maintenance'/('target150-'+str(int(time.time())));backup.mkdir(parents=True)
for f in [Q/'config.json',Q/'waiter-launch.json',Q/'waiter-claim.json',Q/'waiter-status.json',B/'source-seal.json',O/'extension-request.json']:
 if f.exists():shutil.copy(f,backup/f.name)
extension=json.loads((U/'CANCELLED-BY-USER.json').read_text())['old_controller'] if (U/'CANCELLED-BY-USER.json').exists() else stop(U/'controller-launch.json',U/'handoff.py')
save(U/'CANCELLED-BY-USER.json',dict(cancelled=True,user_request='Wait for checkpoint150 and stop SFT; no150to200 continuation',old_controller=extension,live_GPU_training_untouched=True,time=time.time()))
request=json.loads((O/'extension-request.json').read_text());request.update(cancelled=True,status='cancelled_by_user',target_step=150,updated_at=time.time());save(O/'extension-request.json',request)
save(O/'stop-at-150-request.json',dict(authorized=True,target_step=150,wait_for_weights_and_validation=True,existing_frozen150trainer_unchanged=True,continuation_cancelled=True,posteval_checkpoints=[50,100,150],time=time.time()))
oldwaiter=stop(Q/'waiter-launch.json',B/'wait_and_submit.py')
c=json.loads((Q/'config.json').read_text());c.update(training_target=150,checkpoints=[50,100,150],updated_at=time.time());save(Q/'config.json',c)
seal=json.loads((B/'source-seal.json').read_text())
if str(Q/'config.json') in seal['sha256']:seal['sha256'][str(Q/'config.json')]=hashlib.sha256((Q/'config.json').read_bytes()).hexdigest();save(B/'source-seal.json',seal)
for f in ['waiter-claim.json','waiter-status.json','waiter-launch.json']:
 p=Q/f
 if p.exists():p.unlink()
with (Q/'waiter.log').open('ab',buffering=0) as log:
 p=subprocess.Popen([str(R/'.venv/bin/python'),'-u',str(B/'wait_and_submit.py'),'--lane','sft'],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
a=info(p.pid);save(Q/'waiter-launch.json',dict(pid=p.pid,start_ticks=a['ticks'],server='8a100_jupyter',detached=True,lane='sft',wait_for_training=True,training_target=150,time=time.time()))
receipt=dict(passed=True,SFT_GPU_training_untouched=True,extension_CPU_cancelled=True,old_waiter=oldwaiter,new_waiter_pid=p.pid,target_step=150,eval_checkpoints=[50,100,150],other_RL300_lane_untouched=True,time=time.time());save(Q/'stop150-receipt.json',receipt);print(json.dumps(receipt))
