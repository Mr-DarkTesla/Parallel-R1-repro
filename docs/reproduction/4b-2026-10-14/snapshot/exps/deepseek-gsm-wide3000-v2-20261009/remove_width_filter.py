"""Drain the old controller, restore valid deferred rows, resume without width filter."""
import json,os,subprocess,time,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'production';PYTHON=ROOT.parent.parent/'.venv/bin/python'
OLD_CONTROLLER=1010072;OLD_SUPERVISOR=1010071
state={'state':'draining','requested_at':time.time(),'width_filter_enabled':False,'old_controller_pid':OLD_CONTROLLER,'pid':os.getpid()}
def save():
 t=ROOT/'remove-width-filter-status.tmp';t.write_text(json.dumps(state,indent=2)+'\n');t.replace(ROOT/'remove-width-filter-status.json')
def running(pid,name):
 try:command=Path(f'/proc/{pid}/cmdline').read_bytes()
 except FileNotFoundError:return False
 return str(ROOT/name).encode() in command
try:
 assert 'new_width_sum=' not in (ROOT/'produce.py').read_text()
 (OUT/'STOP').write_text('User removed width threshold; drain requests, restore correct deferred examples, resume.\n')
 save()
 while running(OLD_CONTROLLER,'produce.py') or running(OLD_SUPERVISOR,'run_pipeline.py'):
  state['updated_at']=time.time();save();time.sleep(5)
 records=[json.loads(l) for l in (OUT/'journal.jsonl').read_text().splitlines()]
 snapshot=OUT/'journal.before-remove-width.jsonl';assert not snapshot.exists();shutil.copy2(OUT/'journal.jsonl',snapshot)
 p=OUT/'valid-narrow-deferred.jsonl';deferred={r['row']['id']:r['row'] for r in map(json.loads,p.read_text().splitlines())} if p.exists() else {}
 accepted=sum(r['decision']=='accepted' for r in records);restored=[]
 for r in records:
  if r.get('error')=='width_distribution_deferred' and accepted<3000:
   row=deferred[r['id']];assert row['verification']['structure'] and row['verification']['semantic_judge']['accept']
   r.update(decision='accepted',row=row,previous_decision='rejected',previous_error=r.pop('error'),width_filter_restored_at=time.time());accepted+=1;restored.append(r['id'])
 assert accepted<=3000
 tmp=OUT/'journal.restored.tmp';tmp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records));tmp.replace(OUT/'journal.jsonl')
 for filename,key in [('pilot-review.json','mean_width_selection_target'),('pool-manifest.json','mean_width_acceptance_target')]:
  p=ROOT/filename;d=json.loads(p.read_text());d[key]=None;d['width_filter_enabled']=False;p.write_text(json.dumps(d,indent=2)+'\n')
 (OUT/'STOP').unlink(missing_ok=True)
 log=(ROOT/'pipeline-after-width-removal.log').open('a')
 child=subprocess.Popen([str(PYTHON),str(ROOT/'run_pipeline.py')],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 (ROOT/'pipeline.pid').write_text(str(child.pid)+'\n')
 state.update(state='resumed',resumed_at=time.time(),new_pipeline_pid=child.pid,accepted_at_resume=accepted,restored_count=len(restored),restored_ids=restored,previous_journal_sha256=hashlib.sha256(snapshot.read_bytes()).hexdigest());save()
except BaseException as e:
 state.update(state='failed',error=repr(e),at=time.time());save();raise
