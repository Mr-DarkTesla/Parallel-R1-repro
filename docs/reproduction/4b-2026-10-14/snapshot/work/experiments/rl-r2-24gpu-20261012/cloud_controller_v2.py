"""Stable control notebook replaces exactly three authorized old allocations once data is ready."""
from pathlib import Path
import hashlib,json,os,time,traceback

R=Path('${PROJECT_ROOT}');os.chdir(R)
B=R/'work/experiments/rl-r2-24gpu-20261012'
os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
import client_lib as cloud
import requests
original_post=requests.post
def bounded_post(*a,**k):
    k.setdefault('timeout',(10,120));return original_post(*a,**k)
requests.post=bounded_post
original_get=requests.get
def bounded_get(*a,**k):
    k.setdefault('timeout',(10,30));return original_get(*a,**k)
requests.get=bounded_get
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):
    t=p.with_suffix('.tmp');t.write_text(json.dumps(x,indent=2));os.replace(t,p)
def status(state,**x):save(B/'cloud-controller-status.json',dict(state=state,time=time.time(),**x))
old_ids=['HISTORICAL_JOB','HISTORICAL_JOB','HISTORICAL_JOB']
ledger=B/'cloud-submission.json'
assert not ledger.exists(),'Never duplicate a possibly submitted allocation'
try:
    status('waiting_for_verified_data_and_teacher_drain',old_jobs=old_ids)
    while not (B/'data/manifest.json').exists() or not (B/'teacher-drained.json').exists():time.sleep(10)
    data=json.loads((B/'data/manifest.json').read_text());assert data['passed'] and data['train']==1024 and data['previous128_preserved']
    assert data['train_sha256']==sha(B/'data/train.jsonl') and data['val_sha256']==sha(B/'data/val.jsonl')
    assert json.loads((B/'teacher-drained.json').read_text())['passed']
    cfg=json.loads((B/'production-config.json').read_text())
    assert cfg['expected_world_size']==24 and cfg['steps']==500 and cfg['reward_mode']=='strong_width' and cfg['max_batched_paths']==8
    assert cfg['checkpoint_steps']==[50,100,200,300,400,500] and cfg['resume'] is None
    assert json.loads((B/'runtime-build.json').read_text())['passed']
    status('deleting_three_old_jobs',old_jobs=old_ids)
    prior=B/'old-jobs-deleted.json'
    if prior.exists():
        deletion=json.loads(prior.read_text())['requests']
        assert {r['job_id'] for r in deletion}==set(old_ids)
        assert all('deleted' in r['reply'].lower() for r in deletion)
    else:
        raise RuntimeError('This repair requires confirmed prior deletion receipts')
    # Wait until deletion is confirmed, so replacement never overlaps the 24-GPU budget.
    deadline=time.monotonic()+900
    while True:
        statuses=[]
        for ident in old_ids:
            response=requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=ident,region=cloud.RegionMT.SR004),
                                  headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE})
            if response.status_code==404 or (response.status_code==400 and response.text.strip()=='\"No such job\"'):state='NotFound'
            else:
                response.raise_for_status();state=response.json().get('job_status')
            statuses.append(dict(job_id=ident,status=state,http_status=response.status_code))
        save(B/'old-jobs-terminal.json',dict(statuses=statuses,time=time.time()))
        if all(x['status'] in [None,'Deleted','Killed','Stopped','Failed','Succeeded','Completed','Terminated','NotFound','Not Found'] for x in statuses):break
        if time.monotonic()>deadline:raise TimeoutError('Old allocations still running')
        time.sleep(10)
    job=cloud.Job(script=str(B/'node_entry.py'),base_image='jupyter-mosaicml-llm-foundry:python3.10.12-cuda-124-torch24',
                  instance_type='a100plus.8gpu.80vG.96C.1456G',region=cloud.RegionMT.SR004,type=cloud.Job.Type.horovod,
                  job_desc='larin | tmp',n_workers=3,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,
                  detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
    intent=dict(state='submitting',time=time.time(),job_desc='larin | tmp',gpus=24,nodes=3,processes_per_node=8,
                script=str(B/'node_entry.py'),script_sha256=sha(B/'node_entry.py'),node_entry_sha256=sha(B/'node_entry.py'),
                config_sha256=sha(B/'production-config.json'),data_manifest_sha256=sha(B/'data/manifest.json'),
                allocation_restart_resume_supported=False)
    save(ledger,intent);status('submitting_one_24gpu_job')
    reply=job.submit()
    if not job.job_name:
        intent.update(state='unknown_or_rejected',reply=str(reply));save(ledger,intent)
        raise RuntimeError('Submission did not return a job id; do not submit again without reconciliation: '+str(reply))
    intent.update(state='submitted',job_id=job.job_name,reply=str(reply));save(ledger,intent)
    status('submitted',job_id=job.job_name,job_status=job.status())
    print(json.dumps(intent),flush=True)
except BaseException as error:
    status('failed',error=repr(error),traceback=traceback.format_exc())
    raise
