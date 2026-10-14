from pathlib import Path
import os,json,time,signal,subprocess
R=Path('${PROJECT_ROOT}');os.chdir(R)
P=R/'work/experiments/rl-r4-dapo2k-paired-20261013'
s=json.loads((P/'source-current.json').read_text());N=Path(s['current_run_root']);C=N/'control'
def info(pid):
 try:
  x=Path(f'/proc/{pid}/stat').read_text();v=x[x.rfind(')')+2:].split()
  return dict(pid=int(pid),state=v[0],ppid=int(v[1]),start_ticks=v[19],cmd=Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ').decode())
 except (FileNotFoundError,ProcessLookupError):return None
parents=[json.loads(p.read_text()) for p in C.glob('entry-claim-rank-*.json')]
trainers=[json.loads(p.read_text()) for p in C.glob('production-child-rank-*.json')]
assert len(parents)==len(trainers)==8
for r in parents+trainers:
 x=info(r['pid']);assert x and str(x['start_ticks'])==str(r['start_ticks']) and str(N) in x['cmd'],r
allproc=[x for p in Path('/proc').iterdir() if p.name.isdigit() and (x:=info(int(p.name)))]
owned={r['pid'] for r in trainers}
while True:
 more={x['pid'] for x in allproc if x['ppid'] in owned}
 if more<=owned:break
 owned|=more
identities={x['pid']:x for x in allproc if x['pid'] in owned};assert all(p>1 for p in owned)
metrics=N/'production/metrics.jsonl';rows=[json.loads(l) for l in metrics.read_text().splitlines()] if metrics.exists() else []
receipt=dict(user_authorization='Stop previous R3; launch paired8GPU DAPO runs from RL300/SFT',job_id=s['job_id'],current_run_root=str(N),latest_completed_step=rows[-1]['step'] if rows else 300,last_saved_initial_anchor=300,unsaved_updates_not_transferred=(rows[-1]['step']-300 if rows else 0),parents=parents,owned_children=list(identities.values()),time=time.time())
(P/'stop-request.json').write_text(json.dumps(receipt,indent=2)+'\n')
for r in parents:os.kill(r['pid'],signal.SIGSTOP)
for pid,x in identities.items():
 if (now:=info(pid)) and now['start_ticks']==x['start_ticks']:os.kill(pid,signal.SIGTERM)
deadline=time.monotonic()+20
while time.monotonic()<deadline:
 if all(not (z:=info(pid)) or z['state']=='Z' for pid in owned):break
 time.sleep(1)
for pid,x in identities.items():
 if (now:=info(pid)) and now['state']!='Z' and now['start_ticks']==x['start_ticks']:os.kill(pid,signal.SIGKILL)
time.sleep(3)
gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip();assert not gpu,gpu
receipt.update(passed=True,all_gpu_empty=True,platform_parents_intentionally_held=True,stopped_at=time.time())
(P/'source-ready-to-delete.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(passed=True,latest_completed_step=receipt['latest_completed_step'],unsaved_updates_not_transferred=receipt['unsaved_updates_not_transferred'],all_gpu_empty=True)),flush=True)
