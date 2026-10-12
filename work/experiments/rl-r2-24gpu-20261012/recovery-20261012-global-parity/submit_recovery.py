from pathlib import Path
import os,json,time,hashlib,requests
R=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1');os.chdir(R);B=R/'work/experiments/rl-r2-24gpu-20261012';N=B/'recovery-20261012-global-parity'
os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
import client_lib as cloud
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior=json.loads((B/'cloud-submission.json').read_text());assert prior['job_id']=='lm-mpi-job-faf91a66-4547-44e8-b127-4151858e8c88'
h={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
r=requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=prior['job_id'],region=cloud.RegionMT.SR004),headers=h,timeout=20)
assert r.status_code==400 and r.text.strip()=='"No such job"','Do not overlap or duplicate allocation'
assert json.loads((N/'guard-collective-proof.json').read_text())['passed']
assert json.loads((N/'repair-proof.json').read_text())['passed']
assert not (N/'cloud-submission.json').exists()
job=cloud.Job(script=str(N/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=3,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
x=dict(state='submitting',job_desc='larin | tmp',gpus=24,nodes=3,processes_per_node=8,type='pytorch2',pytorch_use_env=True,script=str(N/'node_entry.py'),current_run_root=str(N),script_sha256=sha(N/'node_entry.py'),config_sha256=sha(N/'production-config-v2.json'),runtime_manifest_sha256=sha(N/'runtime-build-v2.json'),data_manifest_sha256=sha(B/'data/manifest.json'),supersedes_failed=prior['job_id'],lost_unexported_prior_updates=36,fresh500=True,time=time.time())
for p in [B/'cloud-submission.json',N/'cloud-submission.json']:p.write_text(json.dumps(x,indent=2))
reply=job.submit();x.update(reply=str(reply),job_id=job.job_name,state='submitted' if job.job_name else 'unknown_or_rejected')
for p in [B/'cloud-submission.json',N/'cloud-submission.json']:p.write_text(json.dumps(x,indent=2))
print(json.dumps(x),flush=True);assert job.job_name,'Reconcile unknown outcome; never blind duplicate'
