from pathlib import Path
import argparse,json,os,time,sys,subprocess,hashlib,shutil,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
ap=argparse.ArgumentParser();ap.add_argument('--lane',choices=['sft','rl300'],required=True);a=ap.parse_args()
B=R/'work/experiments/rl-r4-posteval-20261013';Q=B/a.lane;cfg=json.loads((Q/'config.json').read_text());O=Path(cfg['training_outer'])
def save(p,d):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
try:
 with (Q/'waiter-claim.json').open('x') as f:json.dump(dict(pid=os.getpid(),time=time.time()),f)
 save(Q/'waiter-status.json',dict(state='waiting_for_RL_completion',training_target=cfg['training_target'],pid=os.getpid(),time=time.time()))
 while True:
  f=O/'cloud-submission.json'
  if f.exists():
   source=json.loads(f.read_text());S=Path(source['current_run_root']);done=S/'control/completed.json';result=S/'production/result.json'
   if done.exists() and result.exists():
    d=json.loads(done.read_text());r=json.loads(result.read_text())
    if d['passed'] and r['completed'] and r['steps']==cfg['training_target']:
     assert all(json.loads((S/f'control/production-exit-rank-{i}.json').read_text())['returncode']==0 for i in range(16))
     assert all(json.loads((S/f'control/gpu-empty-rank-{i}.json').read_text())['passed'] for i in range(16))
     break
  time.sleep(30)
 seal=json.loads((B/'source-seal.json').read_text())
 for path,h in seal['sha256'].items():assert sha(path)==h,path
 template=json.loads((B/'job-template.json').read_text());models=[]
 for step in cfg['checkpoints']:
  candidates=[S/f'production/checkpoint-{step:04}',O/f'production/checkpoint-{step:04}',*[p/f'production/checkpoint-{step:04}' for p in O.iterdir() if p.is_dir()]]
  checkpoint=next((p for p in candidates if (p/'complete.json').exists()),None);assert checkpoint,step
  complete=json.loads((checkpoint/'complete.json').read_text());assert complete['step']==step and complete['unsharded'] and complete['weights_only'] and complete['all_master_finite']
  for relative,file in complete['files'].items():assert sha(checkpoint/relative)==file['sha256'],relative
  modelsha=complete['files']['hf/model.safetensors']['sha256']
  E=Q/f'checkpoint-{step:04}';E.mkdir();C=E/'control';C.mkdir()
  for name in ['worker.py','controller.py','finalize.py']:shutil.copy(B/name,E/name)
  job=dict(template,root=str(E),checkpoint=step,model=str(checkpoint/'hf'),model_sha256=modelsha,checkpoint_complete_sha256=sha(checkpoint/'complete.json'),questions=str(B/'questions.jsonl'),created_at=time.time(),precision='BF16',job_id='actual host/job identity recorded by launch receipts')
  save(E/'job.json',job);save(C/'queue.json',dict(next=0,leases={},completed=0))
  hashes=dict(seal['sha256']);hashes.update({str(f):sha(f) for f in [E/'worker.py',E/'controller.py',E/'finalize.py',E/'job.json']})
  save(E/'source-seal.json',dict(passed=True,sha256=hashes));models.append(dict(step=step,checkpoint=str(checkpoint),model_sha256=modelsha))
 save(Q/'training-completed-proof.json',dict(passed=True,job_id=source['job_id'],source_root=str(S),completed_step=cfg['training_target'],all16exit0=True,both_GPU_empty=True,checkpoint_hashes_verified=models,time=time.time()))
 raw=subprocess.check_output(['/bin/bash','-c','source /etc/profile.d/aicloud_envs.sh; /usr/bin/env -0'])
 for item in raw.split(b'\0'):
  if b'=' in item:
   k,v=item.split(b'=',1);os.environ[k.decode()]=v.decode()
 os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID'];os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.path.insert(0,'${HOME}/shares/SR004.nfs3/edge-llms-shared/repos/llm-foundry/current/c_lib')
 import client_lib as cloud,requests
 old=source['job_id'];headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
 def status():return requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=old,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
 r=status()
 if not (r.status_code==400 and r.text.strip()=='"No such job"'):
  oldjob=cloud.Job.__new__(cloud.Job);oldjob.job_name=old;oldjob.region=cloud.RegionMT.SR004;reply=oldjob.kill();save(Q/'source-kill-receipt.json',dict(job_id=old,reply=str(reply),after_training_complete=True,time=time.time()))
 for _ in range(60):
  r=status()
  if r.status_code==400 and r.text.strip()=='"No such job"':break
  time.sleep(5)
 assert r.status_code==400 and r.text.strip()=='"No such job"'
 save(Q/'source-deleted.json',dict(passed=True,job_id=old,code=400,reply='No such job',time=time.time()))
 assert not (Q/'cloud-submission.json').exists(),'Reconcile unknown submission; no duplicate'
 job=cloud.Job(script=str(B/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=2,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1','PARALLEL_POSTEVAL_ROOT':str(Q)})
 d=dict(state='submitting',gpus=16,nodes=2,current_run_root=str(Q),checkpoints=cfg['checkpoints'],after_RL_completed=True,created_at=time.time());save(Q/'cloud-submission.json',d)
 try:reply=job.submit()
 except BaseException:
  d.update(state='unknown',job_id=getattr(job,'job_name',None));save(Q/'cloud-submission.json',d);raise
 d.update(state='submitted' if job.job_name else 'unknown',job_id=job.job_name,reply=str(reply),submitted_at=time.time());save(Q/'cloud-submission.json',d);assert job.job_name
 save(Q/'waiter-status.json',dict(state='eval_submitted',job_id=job.job_name,checkpoints=cfg['checkpoints'],other_lane_untouched=True,time=time.time()))
 print(json.dumps(dict(submitted=True,lane=a.lane,job_id=job.job_name)),flush=True)
except BaseException:
 save(Q/'waiter-failure.json',dict(error=traceback.format_exc(),time=time.time()));raise
