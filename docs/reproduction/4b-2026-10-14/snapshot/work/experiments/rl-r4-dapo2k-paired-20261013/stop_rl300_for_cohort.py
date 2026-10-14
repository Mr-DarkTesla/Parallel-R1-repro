"""User-authorized stop of only the current RL300 lane, on this host."""
from pathlib import Path
import json,os,signal,socket,subprocess,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
d=json.loads((O/'cloud-submission.json').read_text());N=Path(d['current_run_root']);P=O/'candidate-cohort4-separated-actor'
assert N.name=='repair-03-ipc-compatible-cache' and d['job_id']=='HISTORICAL_JOB'
host=socket.gethostname();C=N/'control'
def info(pid):
 try:
  a=Path('/proc')/str(pid);s=(a/'stat').read_text();v=s[s.rfind(')')+2:].split()
  return dict(pid=int(pid),state=v[0],ppid=int(v[1]),start_ticks=v[19],cmd=(a/'cmdline').read_bytes().replace(b'\0',b' ').decode())
 except (FileNotFoundError,ProcessLookupError):return None
parents=[x for f in C.glob('entry-claim-rank-*.json') if (x:=json.loads(f.read_text()))['host']==host]
trainers=[x for f in C.glob('production-child-rank-*.json') if (x:=json.loads(f.read_text()))['host']==host]
assert len(parents)==len(trainers)==8
for r in parents+trainers:
 x=info(r['pid']);assert x and x['start_ticks']==str(r['start_ticks']) and str(N) in x['cmd'],r
processes=[x for f in Path('/proc').iterdir() if f.name.isdigit() and (x:=info(int(f.name)))]
owned={x['pid'] for x in trainers}
while True:
 more={x['pid'] for x in processes if x['ppid'] in owned}
 if more<=owned:break
 owned|=more
identities={x['pid']:x for x in processes if x['pid'] in owned};assert all(x>1 for x in owned)
rows=(N/'production/metrics.jsonl').read_text().splitlines();step=json.loads(rows[-1])['step']
receipt=dict(authorization='Direct user: restart only RL300 after fixing; SFT left running',job_id=d['job_id'],source=str(N),host=host,latest_global_step_before_stop=step,last_saved_step=300,parents=parents,children=list(identities.values()),time=time.time())
out=P/'stop-receipts';out.mkdir(exist_ok=True);path=out/f'{host}.json';path.write_text(json.dumps(receipt,indent=2))
for r in parents:os.kill(r['pid'],signal.SIGSTOP)
for pid,x in identities.items():
 if (a:=info(pid)) and a['start_ticks']==x['start_ticks']:os.kill(pid,signal.SIGTERM)
deadline=time.monotonic()+20
while time.monotonic()<deadline:
 if all(not (x:=info(pid)) or x['state']=='Z' for pid in owned):break
 time.sleep(1)
for pid,x in identities.items():
 if (a:=info(pid)) and a['state']!='Z' and a['start_ticks']==x['start_ticks']:os.kill(pid,signal.SIGKILL)
time.sleep(2)
gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip();assert not gpu,gpu
receipt.update(passed=True,all_gpu_empty=True,parents_held_to_prevent_retry=True,stopped_at=time.time());path.write_text(json.dumps(receipt,indent=2))
print(json.dumps(dict(passed=True,host=host,latest_step=step,gpu_empty=True)))
