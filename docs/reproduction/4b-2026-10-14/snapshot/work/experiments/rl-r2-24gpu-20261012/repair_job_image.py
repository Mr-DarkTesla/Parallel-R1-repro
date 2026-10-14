from pathlib import Path
import hashlib,json,os,requests,time
R=Path('${PROJECT_ROOT}');os.chdir(R);B=R/'work/experiments/rl-r2-24gpu-20261012'
os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
import client_lib as cloud
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old_id='HISTORICAL_JOB'
old=cloud.Job.__new__(cloud.Job);old.job_name=old_id;old.region=cloud.RegionMT.SR004
assert old.status() in ['Job status=Pending','Job status=Inqueue','Job status=Failed']
assert not (B/'smoke').exists() and not (B/'production').exists()
assert not list((B/'control').glob('node-rank-*.json'))
assert not list((B/'bootstrap-pytorch').glob('*.json'))
archive=B/'attempts/06-replaced-jupyter-image';archive.mkdir(parents=True,exist_ok=False)
receipt=json.loads((B/'cloud-submission.json').read_text());assert receipt['job_id']==old_id
(B/'cloud-submission.json').rename(archive/'cloud-submission.json')
(archive/'failure-proof.json').write_text(json.dumps(dict(job_id=old_id,status='Pending_before_replacement',actual_training_steps=0,rank_artifacts=0,
    platform_log_api='429 daily namespace rate limit; no log bypass',root_cause_verified=False,official_image_requirement='https://cloud.ru/docs/aicloud/mlspace/concepts/troubleshooting/troubleshooting__jobs/troubleshooting__premis-denied',
    repair='Use official training-job base image instead of incompatible Jupyter image; native PyTorch launcher unchanged'),indent=2))
reply=old.kill();assert 'deleted' in reply
(archive/'deleted.json').write_text(json.dumps(dict(job_id=old_id,reply=reply)))
headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
for _ in range(90):
    response=requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=old_id,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
    if response.status_code==400 and response.text.strip()=='"No such job"':break
    time.sleep(5)
else:raise RuntimeError('Failed allocation deletion not confirmed')
job=cloud.Job(script=str(B/'node_entry_v2.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',
    instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,
    job_desc='larin | tmp',n_workers=3,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,
    detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
intent=dict(state='submitting',job_desc='larin | tmp',gpus=24,nodes=3,processes_per_node=8,type='pytorch2',pytorch_use_env=True,
    script=str(B/'node_entry_v2.py'),script_sha256=sha(B/'node_entry_v2.py'),config_sha256=sha(B/'production-config.json'),
    data_manifest_sha256=sha(B/'data/manifest.json'),supersedes_failed=old_id,time=time.time())
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2))
reply=job.submit();intent.update(reply=str(reply),job_id=job.job_name,state='submitted' if job.job_name else 'unknown_or_rejected')
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2));print(json.dumps(intent),flush=True)
assert job.job_name,'Do not duplicate uncertain submission'
