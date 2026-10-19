"""Preserve the failed pre-generation attempt and restart after scorer repair."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
import verl.trainer.ppo.reward
import reward_bridge

first=reward_bridge.compute_score('test','','Final Answer: 0.5','0.5',{'index':7})
second=reward_bridge.compute_score('test','','Final Answer: 2','3',{'index':8})
assert first['acc']==1 and second['acc']==0 and first['sample_index']==7
assert first['scorer_error']==0 and second['scorer_error']==0
(ROOT/'bridge-check.json').write_text(json.dumps(dict(passed=True,correct_test=first,incorrect_test=second),indent=2)+'\n')
state=json.loads((ROOT/'status.json').read_text())
assert state['state']=='failed' and state['jobs'][0]['completed_runtime_records']==0
assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
archive=ROOT/'attempts/startup-import-01'
archive.mkdir(parents=True,exist_ok=False)
for name in ('runs','status.json','queue.log','controller.pid'):
    path=ROOT/name
    if path.exists():path.rename(archive/name)
manifest=json.loads((ROOT/'manifest.json').read_text())
manifest['scorer_isolation']='Persistent clean Python subprocess via reward_bridge.py to avoid verl ANTLR version conflict'
manifest['evaluation_files_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
signal.signal(signal.SIGHUP,signal.SIG_IGN)
with (ROOT/'queue.log').open('w') as log:
    child=subprocess.Popen([sys.executable,'-u',str(ROOT/'run_queue.py')],cwd=ROOT,
        stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
(ROOT/'controller.pid').write_text(str(child.pid)+'\n')
print(json.dumps(dict(bridge_tests='passed',controller_pid=child.pid,archived_attempt=str(archive))),flush=True)
