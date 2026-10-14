from pathlib import Path
import json,os,sys,subprocess,time,hashlib,shutil,ast,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013';P=O/'continuation-150-to-200'
P.mkdir(exist_ok=True)
def save(p,d):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
try:
 with (P/'controller-claim.json').open('x') as f:json.dump(dict(pid=os.getpid(),time=time.time()),f)
 assert json.loads((O/'extension-request.json').read_text())['total_target']==200
 save(P/'handoff-status.json',dict(state='waiting_for_completed150',pid=os.getpid(),new_Adam=True,no_live_stop=True,time=time.time()))
 while True:
  current=json.loads((O/'cloud-submission.json').read_text());S=Path(current['current_run_root'])
  checkpoint=S/'production/checkpoint-0150';f=S/'control/completed.json'
  if f.exists() and checkpoint.joinpath('complete.json').exists():
   done=json.loads(f.read_text());result=json.loads((S/'production/result.json').read_text())
   if done['passed'] and result['completed'] and result['steps']==150:
    exits=[json.loads((S/f'control/production-exit-rank-{r}.json').read_text()) for r in range(16)]
    empty=[json.loads((S/f'control/gpu-empty-rank-{r}.json').read_text()) for r in range(16)]
    assert all(x['returncode']==0 for x in exits) and all(x['passed'] for x in empty)
    break
  time.sleep(30)
 complete=json.loads((checkpoint/'complete.json').read_text());assert complete['step']==150 and complete['unsharded'] and complete['weights_only']
 for relative,digest in complete['files'].items():
  assert sha(checkpoint/relative)==digest['sha256'],relative
 save(P/'source-preserved.json',dict(passed=True,source=str(S),checkpoint=str(checkpoint),completed_step=150,all16exit0=True,all_gpu_empty=True,manifest_verified=True,optimizer_RNG_states=False,time=time.time()))
 shutil.copytree(S/'src',P/'src');shutil.copy(S/'reward.py',P/'reward.py')
 entry=(S/'node_entry.py').read_text().replace(str(S),str(P)).replace("result['steps']==150","result['steps']==200").replace('initial_step=0,target_step=150,new_iterations=150','initial_step=150,target_step=200,new_iterations=50');(P/'node_entry.py').write_text(entry)
 train=P/'src/train.py';code=train.read_text();needle="step-start_step,prompt_index,sample_index";assert needle in code
 code=code.replace(needle,"step-start_step+int(cfg.get('rollout_iteration_offset',0)),prompt_index,sample_index");train.write_text(code)
 c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)))
 c.update(model=str(checkpoint/'hf'),initial_checkpoint=str(checkpoint),initial_step=150,steps=200,total_training_iterations=200,new_training_iterations=50,checkpoint_steps=[200],prompt_exposure_offset=2400,rollout_iteration_offset=150,lane='SFT DAPO extension150to200 weights-only freshAdam')
 c['sealed_inputs']['initial_model_config']=str(checkpoint/'hf/config.json');c['sealed_inputs']['initial_model_tokenizer']=str(checkpoint/'hf/tokenizer_config.json');c['sealed_inputs']['initial_weights_complete']=str(checkpoint/'complete.json')
 save(P/'production-config.json',c)
 files=[P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]
 for f in files:
  if f.suffix=='.py':ast.parse(f.read_text(),filename=str(f))
 save(P/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(f):sha(f) for f in files},fresh_GPU_smoke=False,user_authorization='Extend firstSFT200total, do not stophealthyfirst150',initial_step=150,target_step=200,new_iterations=50,new_Adam=True,time=time.time()))
 (P/'control').mkdir();proof=Path(c['gpu_audit'])
 save(P/'control/production-approved.json',dict(approved=True,config_sha256=sha(P/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='User200total, weights-only continuation, no newGPUtests',time=time.time()))
 raw=subprocess.check_output(['/bin/bash','-c','source /etc/profile.d/aicloud_envs.sh; /usr/bin/env -0'])
 for item in raw.split(b'\0'):
  if b'=' in item:
   k,v=item.split(b'=',1);os.environ[k.decode()]=v.decode()
 os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID'];os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.path.insert(0,'${HOME}/shares/SR004.nfs3/edge-llms-shared/repos/llm-foundry/current/c_lib')
 import client_lib as cloud,requests
 old=current['job_id'];headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
 def status():return requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=old,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
 r=status()
 if not (r.status_code==400 and r.text.strip()=='"No such job"'):
  job=cloud.Job.__new__(cloud.Job);job.job_name=old;job.region=cloud.RegionMT.SR004;reply=job.kill();save(P/'source-kill-receipt.json',dict(job_id=old,reply=str(reply),after_completed150_all16exit0=True,time=time.time()))
 for _ in range(60):
  r=status()
  if r.status_code==400 and r.text.strip()=='"No such job"':break
  time.sleep(5)
 assert r.status_code==400 and r.text.strip()=='"No such job"'
 save(P/'source-deleted.json',dict(passed=True,job_id=old,code=400,reply='No such job',time=time.time()))
 assert not (P/'cloud-submission.json').exists(),'Unknown submission must reconcile, no duplicate'
 new=cloud.Job(script=str(P/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=2,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
 d=dict(state='submitting',gpus=16,nodes=2,current_run_root=str(P),initial_step=150,target_step=200,new_iterations=50,total_campaign_iterations=200,config_sha256=sha(P/'production-config.json'),created_at=time.time());save(P/'cloud-submission.json',d)
 try:reply=new.submit()
 except BaseException:
  d.update(state='unknown',job_id=getattr(new,'job_name',None));save(P/'cloud-submission.json',d);raise
 d.update(state='submitted' if new.job_name else 'unknown',job_id=new.job_name,reply=str(reply),submitted_at=time.time());save(P/'cloud-submission.json',d);assert new.job_name
 save(O/'cloud-submission.json',d);save(P/'handoff-status.json',dict(state='submitted',job_id=new.job_name,target_step=200,new_Adam=True,old150weights_preserved=True,time=time.time()))
 print(json.dumps(dict(submitted=True,job_id=new.job_name,target_step=200)),flush=True)
except BaseException:
 save(P/'handoff-failure.json',dict(error=traceback.format_exc(),time=time.time()));raise
