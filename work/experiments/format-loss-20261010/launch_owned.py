import os,json,signal,time,hashlib,subprocess,datetime
from pathlib import Path
P=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1'); C=P/'work/experiments/format-loss-20261010';D=P/'work/experiments/instruct-token-warmup-20261010'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def proc(pid):
 q=Path('/proc')/str(pid); s=(q/'stat').read_text().rsplit(')',1)[1].split();return dict(pid=pid,state=s[0],ppid=int(s[1]),pgid=int(s[2]),start=s[19],uid=q.stat().st_uid,cwd=os.readlink(q/'cwd'),cmd=(q/'cmdline').read_bytes().replace(b'\0',b' ').decode())
def same(x):
 try:return proc(x['pid'])['start']==x['start']
 except FileNotFoundError:return False
st=read(D/'status.json');assert st['stage']=='trained-structured-128'
control=proc(st['controller_pid']);leader=proc(st['pid']);assert control['uid']==leader['uid']==os.getuid() and control['cwd']==leader['cwd']==str(P)
assert str(D/'posttrain_controller.py') in control['cmd'] and str(D/'evaluations/evaluate.py') in leader['cmd'] and 'trained-structured-128' in leader['cmd']
assert leader['pgid']==leader['pid']==st['owned_process_group']
os.kill(control['pid'],signal.SIGSTOP)
try:
 assert same(control) and same(leader)
 members=[]
 for p in Path('/proc').iterdir():
  if p.name.isdigit():
   try:
    x=proc(int(p.name))
    if x['pgid']==leader['pgid']:members.append(x)
   except (FileNotFoundError,ProcessLookupError,PermissionError):pass
 assert members and all(x['uid']==os.getuid() and x['cwd']==str(P) for x in members)
 ids={x['pid'] for x in members}
 for x in members:
  if x['pid']!=leader['pid']:assert x['ppid'] in ids
 gpu={int(x) for x in subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).split()}; assert gpu<=ids
 receipt=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_status=st,controller=control,eval_members=members,reason='User prioritizes weighted SFT and new guarded evaluation',preserved_results=True)
 (C/'owned-eval-handoff.json').write_text(json.dumps(receipt,indent=2)+'\n')
 os.kill(control['pid'],signal.SIGTERM);os.kill(control['pid'],signal.SIGCONT);os.killpg(leader['pgid'],signal.SIGTERM)
 time.sleep(3)
 for x in [control]+members:
  if same(x):os.kill(x['pid'],signal.SIGKILL)
 for i in range(20):
  occupied=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
  if not occupied:break
  time.sleep(1)
 assert not occupied,occupied
 st.update(state='interrupted_for_weighted_sft',interrupted_at=receipt['at'],handoff_receipt=str(C/'owned-eval-handoff.json'))
 (D/'status.json').write_text(json.dumps(st,indent=2)+'\n')
except BaseException:
 if same(control):os.kill(control['pid'],signal.SIGCONT)
 raise
review=read(C/'independent-sft-controller-review.json'); assert review['passed']
pins=review['verified_source_sha256']
for p,h in pins.items():assert sha(Path(p))==h,p
for p in [C/'independent-sft-controller-review.json',C/'cpu-data-proof.json',C/'guard-worker-cpu-proof.json',D/'runs/smoke/initialization-proof.json']:
 pins[str(p)]=sha(p)
ready=dict(passed=True,trainable_parameters=15360,sha256={str(Path(p).relative_to(P)):h for p,h in pins.items()},owned_handoff_receipt=str(C/'owned-eval-handoff.json'))
assert not (C/'sft-launch-ready.json').exists()
(C/'sft-launch-ready.json').write_text(json.dumps(ready,indent=2)+'\n')
with (C/'sft-controller.log').open('x') as log:
 child=subprocess.Popen([str(P/'.venv/bin/python'),'-B',str(C/'sft_controller.py')],cwd=P,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True)
print('LAUNCHED',child.pid,'GPU empty confirmed, sources pinned',len(pins),flush=True)
time.sleep(3)
print((C/'sft-status.json').read_text() if (C/'sft-status.json').exists() else (C/'sft-controller.log').read_text())
