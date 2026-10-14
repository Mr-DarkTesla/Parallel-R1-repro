from pathlib import Path
import hashlib,json,os,requests,shutil,time
R=Path('${PROJECT_ROOT}');os.chdir(R);B=R/'work/experiments/rl-r2-24gpu-20261012'
os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
import client_lib as cloud
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old_id='HISTORICAL_JOB'
old=cloud.Job.__new__(cloud.Job);old.job_name=old_id;old.region=cloud.RegionMT.SR004
state=old.status();assert state in ['Job status=Running','Job status=Failed']
assert not (B/'production').exists()
assert not any(p.read_text().strip() for p in (B/'smoke').glob('metrics*.jsonl'))
assert 'FileNotFoundError' in (B/'smoke-rank-8.log').read_text()
archive=B/'attempts/08-nfs-visibility';archive.mkdir(parents=True,exist_ok=False)
r=json.loads((B/'cloud-submission.json').read_text());assert r['job_id']==old_id
(B/'cloud-submission.json').rename(archive/'cloud-submission.json')
(archive/'failure-proof.json').write_text(json.dumps(dict(job_id=old_id,status=state,actual_optimizer_steps=0,model_loaded=True,root_cause='Cross-node NFS directory visibility: workers8/16 could not open metrics path after rank0 mkdir and DDP barrier',repair='Each rank mkdir existing shared output/validation directories, forcing NFS parent refresh'),indent=2))
reply=old.kill();assert 'deleted' in reply
(archive/'deleted.json').write_text(json.dumps(dict(job_id=old_id,reply=reply)))
headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
for _ in range(90):
    q=requests.get('http://'+cloud.environment.GW_API_ADDR+'/job_status',params=dict(job=old_id,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
    if q.status_code==400 and q.text.strip()=='"No such job"':break
    time.sleep(5)
else:raise RuntimeError('Deletion not confirmed; do not allocate duplicate')
for name in ['control','bootstrap-pytorch','smoke']:
    if (B/name).exists():(B/name).rename(archive/name)
for p in B.glob('smoke-rank-*.log'):p.rename(archive/p.name)
runner=B/'runner-v2';shutil.copytree(B/'runner',runner)
p=runner/'train.py';s=p.read_text()
a="    if world > 1:\n        dist.barrier()\n    train ="
b="    if world > 1:\n        dist.barrier()\n    # DDP barriers do not invalidate per-node NFS negative directory caches.\n    # mkdir from each client refreshes the parent before creating rank-local files.\n    output.mkdir(parents=True, exist_ok=True)\n    train ="
assert s.count(a)==1;s=s.replace(a,b)
a="        if world>1:\n            dist.barrier()\n        model.eval()\n        records = []"
b="        if world>1:\n            dist.barrier()\n        directory.mkdir(parents=True, exist_ok=True)\n        model.eval()\n        records = []"
assert s.count(a)==1;s=s.replace(a,b);compile(s,str(p),'exec');p.write_text(s)
manifest=json.loads((B/'runtime-build.json').read_text());manifest['sources']={k.replace('/runner/','/runner-v2/'):sha(R/k.replace('/runner/','/runner-v2/')) for k in manifest['sources']}
manifest['nfs_visibility_repair']=True;(B/'runtime-build-v2.json').write_text(json.dumps(manifest,indent=2))
for stage in ['smoke','production']:
    c=json.loads((B/(stage+'-config.json')).read_text())
    for k,v in c.items():
        if isinstance(v,str):c[k]=v.replace('/runner/','/runner-v2/')
    c['sealed_inputs']={k.replace('/runner/','/runner-v2/'):v.replace('/runner/','/runner-v2/') for k,v in c['sealed_inputs'].items()}
    (B/(stage+'-config-v2.json')).write_text(json.dumps(c,indent=2))
s=(B/'node_entry_v3.py').read_text().replace("cfg=B/(stage+'-config.json')","cfg=B/(stage+'-config-v2.json')").replace("B/'runner/train.py'","B/'runner-v2/train.py'").replace("smoke-config.json","smoke-config-v2.json").replace("production-config.json","production-config-v2.json").replace("runtime-build.json","runtime-build-v2.json")
compile(s,'node_entry_v4.py','exec');(B/'node_entry_v4.py').write_text(s)
job=cloud.Job(script=str(B/'node_entry_v4.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,job_desc='larin | tmp',n_workers=3,processes_per_worker=8,queue_name='edge',priority_class=cloud.PriorityClass.medium,detached=True,max_retry=0,env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
intent=dict(state='submitting',job_desc='larin | tmp',gpus=24,nodes=3,processes_per_node=8,type='pytorch2',pytorch_use_env=True,script=str(B/'node_entry_v4.py'),script_sha256=sha(B/'node_entry_v4.py'),config_sha256=sha(B/'production-config-v2.json'),data_manifest_sha256=sha(B/'data/manifest.json'),runtime_manifest_sha256=sha(B/'runtime-build-v2.json'),supersedes_failed=old_id,time=time.time())
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2))
reply=job.submit();intent.update(reply=str(reply),job_id=job.job_name,state='submitted' if job.job_name else 'unknown_or_rejected')
(B/'cloud-submission.json').write_text(json.dumps(intent,indent=2));print(json.dumps(intent),flush=True)
assert job.job_name,'Do not duplicate uncertain submission'
