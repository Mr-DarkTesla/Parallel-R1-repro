from pathlib import Path
import os,sys,json,time,hashlib,subprocess,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
P=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
def save(p,d):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
try:
 with (P/'schedule-controller-claim.json').open('x') as f:json.dump(dict(pid=os.getpid(),time=time.time()),f)
 schedule=json.loads((P/'schedule.json').read_text());deadline=schedule['deadline_timestamp']
 save(P/'schedule-status.json',dict(state='waiting',deadline=deadline,scheduled_at_moscow=schedule['scheduled_at_moscow'],pid=os.getpid(),time=time.time()))
 while time.time()<deadline:time.sleep(min(30,deadline-time.time()))
 schedule=json.loads((P/'schedule.json').read_text())
 assert not (P/'cloud-submission.json').exists(),'Existing/unknown submission must reconcile; no duplicate'
 ready=json.loads((P/'LAUNCH-READY.json').read_text());assert ready['passed'] and ready['world_size']==16
 for path,digest in ready['sha256'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
 raw=subprocess.check_output(['/bin/bash','-c','source /etc/profile.d/aicloud_envs.sh; /usr/bin/env -0'])
 for item in raw.split(b'\0'):
  if b'=' in item:
   k,v=item.split(b'=',1);os.environ[k.decode()]=v.decode()
 os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID'];os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.path.insert(0,'${HOME}/shares/SR004.nfs3/edge-llms-shared/repos/llm-foundry/current/c_lib')
 import client_lib as cloud
 job=cloud.Job(script=str(P/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=2,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
 d=dict(state='submitting',gpus=16,nodes=2,current_run_root=str(P),initial_step=300,target_step=schedule['target_step'],new_iterations=schedule['new_iterations'],scheduled_at_moscow=schedule['scheduled_at_moscow'],config_sha256=schedule['config_sha256'],created_at=time.time())
 save(P/'cloud-submission.json',d);save(P/'schedule-status.json',dict(state='submitting',pid=os.getpid(),time=time.time()))
 try:reply=job.submit()
 except BaseException:
  d.update(state='unknown',job_id=getattr(job,'job_name',None));save(P/'cloud-submission.json',d);raise
 d.update(state='submitted' if job.job_name else 'unknown',job_id=job.job_name,reply=str(reply),submitted_at=time.time());save(P/'cloud-submission.json',d);assert job.job_name
 save(P/'schedule-status.json',dict(state='submitted',job_id=job.job_name,scheduled_at_moscow=schedule['scheduled_at_moscow'],submitted_at=time.time(),independent_sft_job_untouched=True))
 save(P/'launch-receipt.json',dict(submitted=True,job_id=job.job_name,gpus=16,initial_step=300,target_step=schedule['target_step'],new_iterations=schedule['new_iterations'],new_Adam=True,optimizer_or_rng_loaded=False,no_fresh_smoke=True,first_update_not_yet_verified=True,time=time.time()))
 print(json.dumps(dict(submitted=True,job_id=job.job_name,gpus=16)),flush=True)
except BaseException:
 save(P/'schedule-failure.json',dict(error=traceback.format_exc(),time=time.time()));raise
