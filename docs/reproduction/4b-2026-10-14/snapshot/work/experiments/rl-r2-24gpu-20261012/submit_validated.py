from pathlib import Path
import hashlib,json,os,requests,shutil,time
R=Path('${PROJECT_ROOT}');os.chdir(R);B=R/'work/experiments/rl-r2-24gpu-20261012'
os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
import client_lib as cloud
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old_id='HISTORICAL_JOB'
prior=json.loads((B/'cloud-submission.json').read_text())
assert prior['job_id'] is None and prior['reply']=="Error 400: 'max_retry': value must be between 3 and 100"
archive=B/'attempts/09-rejected-max-retry';archive.mkdir(exist_ok=False)
(B/'cloud-submission.json').rename(archive/'cloud-submission.json')
job=cloud.Job(script=str(B/'node_entry_v4.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=3,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
intent=dict(state='submitting',job_desc='larin | tmp',gpus=24,nodes=3,processes_per_node=8,type='pytorch2',pytorch_use_env=True,script=str(B/'node_entry_v4.py'),script_sha256=sha(B/'node_entry_v4.py'),config_sha256=sha(B/'production-config-v2.json'),data_manifest_sha256=sha(B/'data/manifest.json'),runtime_manifest_sha256=sha(B/'runtime-build-v2.json'),supersedes_failed=old_id,time=time.time())
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2))
reply=job.submit();intent.update(reply=str(reply),job_id=job.job_name,state='submitted' if job.job_name else 'unknown_or_rejected')
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2));print(json.dumps(intent),flush=True)
assert job.job_name,'Do not duplicate uncertain submission'
