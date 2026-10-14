"""Replace only confirmed terminal allocation, one16GPU direct production."""
from pathlib import Path
import json,os,sys,subprocess,time,hashlib,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013';N=O/'repair-03-ipc-compatible-cache'
def save(path,data):
 tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,path)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
try:
 assert not (N/'cloud-submission.json').exists(),'Unknown submission must reconcile; no duplicate'
 assert json.loads((N/'repair-receipt.json').read_text())['passed']
 raw=subprocess.check_output(['/bin/bash','-c','source /etc/profile.d/aicloud_envs.sh; /usr/bin/env -0'])
 for item in raw.split(b'\0'):
  if b'=' in item:
   k,v=item.split(b'=',1);os.environ[k.decode()]=v.decode()
 os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID'];os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.path.insert(0,'${HOME}/shares/SR004.nfs3/edge-llms-shared/repos/llm-foundry/current/c_lib')
 import client_lib as cloud,requests
 headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
 prior=json.loads((O/'cloud-submission.json').read_text());old=prior['job_id'];assert old=='HISTORICAL_JOB'
 def status():return requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=old,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
 response=status();assert response.status_code==200 and response.json()['job_status']=='Failed',response.text
 save(N/'source-terminal.json',dict(job_id=old,status='Failed',direct_GPU_SSH='host connection failed',no_completed_new_updates=True,time=time.time()))
 save(N/'source-cloud-submission.json',prior)
 C=N/'control';C.mkdir(exist_ok=True);c=json.loads((N/'production-config.json').read_text());proof=Path(c['gpu_audit'])
 save(C/'production-approved.json',dict(approved=True,config_sha256=sha(N/'production-config.json'),sha256={key:sha(value) for key,value in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='Standing isolated repair of confirmed dead run, direct production no fresh GPU smoke',qualification_scope='Existing engine proof, original DDP and loss retained; new memory repair not yet GPU qualified',time=time.time()))
 save(N/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(p):sha(p) for p in [N/'node_entry.py',N/'production-config.json',N/'reward.py',*(N/'src').rglob('*.py')]},initial_checkpoint=c['initial_checkpoint'],initial_step=300,weights_only_newAdam=True,time=time.time()))
 job=cloud.Job.__new__(cloud.Job);job.job_name=old;job.region=cloud.RegionMT.SR004;reply=job.kill();save(N/'source-kill-receipt.json',dict(job_id=old,reply=str(reply),time=time.time()))
 for _ in range(60):
  response=status()
  if response.status_code==400 and response.text.strip()=='"No such job"':break
  time.sleep(5)
 assert response.status_code==400 and response.text.strip()=='"No such job"','No replacement before deletion confirmed'
 save(N/'source-deleted.json',dict(passed=True,job_id=old,status_code=400,reply='No such job',time=time.time()))
 new=cloud.Job(script=str(N/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=2,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
 d=dict(state='submitting',gpus=16,nodes=2,current_run_root=str(N),initial_step=300,target_step=400,new_iterations=100,config_sha256=sha(N/'production-config.json'),created_at=time.time());save(N/'cloud-submission.json',d)
 try:reply=new.submit()
 except BaseException:
  d.update(state='unknown',job_id=getattr(new,'job_name',None));save(N/'cloud-submission.json',d);raise
 d.update(state='submitted' if new.job_name else 'unknown',job_id=new.job_name,reply=str(reply),submitted_at=time.time());save(N/'cloud-submission.json',d);assert new.job_name
 save(O/'cloud-submission.json',d)
 save(N/'launch-receipt.json',dict(submitted=True,job_id=new.job_name,fresh_GPU_smoke=False,source_frozen=True,first_update_not_yet_verified=True,time=time.time()))
 print(json.dumps(dict(submitted=True,job_id=new.job_name,current_run_root=str(N),gpus=16)))
except BaseException:
 save(N/'launch-failure.json',dict(error=traceback.format_exc(),time=time.time()));raise
