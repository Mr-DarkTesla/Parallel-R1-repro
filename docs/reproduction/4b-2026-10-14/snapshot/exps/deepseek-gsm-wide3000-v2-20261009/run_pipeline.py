"""Own controller lifecycle; expand GSM reserve if needed; export after completion."""
import json,subprocess,time,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'production';PYTHON=sys.executable
assert json.loads((ROOT/'pilot-review.json').read_text())['production_ready']
state={'pid':os.getpid(),'state':'running','started_at':time.time(),'target':3000,'mean_width_target':None,'concurrency':256,'source':'GSM_Infinite'}
def save():
 (ROOT/'pipeline-status.json').write_text(json.dumps(state,indent=2)+'\n')
def execute(name,args=()):
 state.update(stage=name,updated_at=time.time());save()
 with (ROOT/(name.replace('.py','')+'.log')).open('a') as log:
  child=subprocess.Popen([PYTHON,str(ROOT/name),*args],stdout=log,stderr=subprocess.STDOUT)
  state.update(child_pid=child.pid);save();code=child.wait()
 assert code==0,(name,code)
try:
 for attempt in range(2):
  execute('produce.py')
  s=json.loads((OUT/'status.json').read_text())
  if s['state']=='complete':break
  assert s['state']=='pool_exhausted',s['state']
  assert attempt==0,'Expanded GSM reserve exhausted'
  # Same family and decontamination rules; every source revision is pinned.
  execute('expand_pool_fallback.py');execute('combine_expanded_pool.py')
 else:raise RuntimeError('Failed to reach target')
 execute('serialize_think.py')
 assert (OUT/'sft-think/READY').exists()
 state.update(state='complete',finished_at=time.time(),output=str(OUT/'sft-think'));save()
except BaseException as e:
 state.update(state='failed',error=repr(e),finished_at=time.time());save();raise
