"""CPU-only terminal process audit; never launches or modifies an experiment."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import psutil

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'exps').is_dir())
lane=ROOT/'work/experiments/night-20261010/cloud-continued/tmp3'
ready=json.loads((lane/'ready.json').read_text())
assert os.uname().nodename==ready['hostname']
worker=psutil.Process(ready['pid'])
assert worker.is_running()
old=psutil.Process(ready['old_pid'])
assert old.status()==psutil.STATUS_STOPPED
result=json.loads((lane/'results/211-distributed-rl-batched-smoke.json').read_text())
assert result['returncode']==1
owned=[]
for process in psutil.process_iter(['pid','cmdline']):
    argv=process.info['cmdline'] or []
    if str(HERE/'train.py') in argv or str(HERE/'run_job.py') in argv:
        owned.append(dict(pid=process.pid,argv=argv))
gpu=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],
                   capture_output=True,text=True,timeout=30,check=True)
receipt=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             state='terminal_no_restart',terminal_result=result,owned_training_processes=owned,
             gpu_processes=gpu.stdout.strip().splitlines(),worker_pid=worker.pid,
             worker_alive=True,old_parent_stopped=True,allocations_unchanged=True,
             terminal_cause='NCCL shutdown cuda out of memory; launcher returncode1',
             log_sha256=hashlib.sha256((lane/'211-distributed-rl-batched-smoke.log').read_bytes()).hexdigest(),
             passed=not owned and not gpu.stdout.strip())
path=HERE/'base-stop-receipt.json'
assert not path.exists()
path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
if not receipt['passed']:
    raise SystemExit(1)
