"""Durable checkpoint-bound handoff. Never stop the source before verified weights."""
from pathlib import Path
import os,json,time,hashlib,fcntl,traceback,sys
R=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1');os.chdir(R)
M=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
B=R/'work/experiments/rl-r2-24gpu-20261012'
N=B/'recovery-20261012-global-parity'
OLD='lm-mpi-job-cac6899b-a660-40d1-b4d6-2ab0e2b64c88'
ANCHORS=[50,100,200,300,400,500]
class SourceAdvanced(Exception):pass

def save(p,x):
    p=Path(p);temporary=p.with_name(p.name+'.tmp-'+str(os.getpid()))
    temporary.write_text(json.dumps(x,indent=2)+'\n');os.replace(temporary,p)
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for data in iter(lambda:f.read(8*1024*1024),b''):h.update(data)
    return h.hexdigest()
def load(p):return json.loads(Path(p).read_text())
def status(state,**kw):
    save(M/'handoff-status.json',dict(state=state,pid=os.getpid(),time=time.time(),old_job=OLD,**kw))

def verify_source():
    proof=load(M/'cpu-reward-group-proof.json');assert proof['passed'] and proof['actual_gloo_ranks']==8
    seal=load(M/'source-seal.json')
    for path,digest in seal['sha256'].items():assert sha(path)==digest,path
    assert load(N/'distributed-smoke-proof.json')['passed']
    return seal

def checkpoint_proof(cp):
    import torch
    from safetensors import safe_open
    complete=load(cp/'complete.json');step=complete['step']
    assert step in ANCHORS and complete['world_size']==24 and complete['unsharded'] and complete['model']
    assert complete['optimizer'] is False and complete['rng'] is False
    hf=cp/'hf';assert (hf/'model.safetensors').is_file() and not list(hf.glob('model-*.safetensors'))
    assert not (hf/'model.safetensors.index.json').exists()
    config=load(hf/'config.json');assert config['hidden_size']==2560 and config['num_hidden_layers']==36
    expected=list((Path(load(N/'production-config-v2.json')['model'])).glob('*token*'))
    assert (hf/'tokenizer_config.json').is_file() and (hf/'tokenizer.json').is_file()
    torch.set_num_threads(2)
    tensor_count=0;count=0
    with safe_open(hf/'model.safetensors',framework='pt',device='cpu') as model:
        for name in model.keys():
            tensor=model.get_tensor(name)
            assert torch.isfinite(tensor).all().item(),name
            count+=tensor.numel();tensor_count+=1;del tensor
    assert tensor_count==398 and count>=4_000_000_000,(tensor_count,count)
    model_sha=sha(hf/'model.safetensors')
    summary=load(N/'production'/f'validation-{step:04}'/'summary.json');assert summary['step']==step and summary['completed']==32
    latest=load_metrics()
    assert latest['step']>=step and len(latest['ranks'])==24
    proof=dict(passed=True,step=step,checkpoint=str(cp),model_sha256=model_sha,
               tensors=tensor_count,parameters=count,finite=True,unsharded=True,optimizer_reset=True,
               exact_optimizer_resume=False,source_validation_summary=summary,time=time.time())
    save(M/f'checkpoint-{step:04}-handoff-proof.json',proof)
    return proof

def load_metrics():
    lines=(N/'production/metrics.jsonl').read_text().splitlines()
    return json.loads(lines[-1]) if lines else dict(step=0,ranks=[])

def prepare_configs(cp,proof):
    original=load(N/'production-config-v2.json')
    cfg=dict(original)
    cfg.update(model=str(cp/'hf'),initial_checkpoint=str(cp),initial_step=proof['step'],
               prompt_exposure_offset=proof['step']*24,group=1,reward_group=4,
               expected_world_size=32,world_size=32,
               global_batch=dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32),
               replay=str(M/'runner/structured_replay.py'),batch_decoder=str(M/'runner/microbatch_decoder.py'),
               gpu_audit=str(M/'distributed-smoke-proof.json'),output=str(M/'production'),
               lane='one_cloud_job_4x8_one_response_per_gpu',
               validation_protocol='Matched clean val32 fixed seed; fullwidth8; weights-only continuation',
               data_reuse=dict(prior_prompts=proof['step']*24,remaining_prompts=(500-proof['step'])*8),
               optimizer_reset=True,exact_optimizer_resume=False,total_training_iterations=500)
    sealed={k:p for k,p in original['sealed_inputs'].items() if '/runner/' not in p}
    for path in sorted((M/'runner').rglob('*.py')):sealed[str(path.relative_to(R))]=str(path)
    sealed['cpu-reward-group-proof']=str(M/'cpu-reward-group-proof.json')
    sealed['weights-only-handoff-proof']=str(M/f"checkpoint-{proof['step']:04}-handoff-proof.json")
    cfg['sealed_inputs']=sealed
    smoke=dict(cfg,steps=proof['step']+2,output=str(M/'smoke'),skip_validation=True,skip_exports=True,
               resident_fixture_step=proof['step']+2)
    save(M/'production-config-v2.json',cfg);save(M/'smoke-config-v2.json',smoke)
    manifest=dict(passed=True,world_size=32,group_size=4,global_batch=cfg['global_batch'],
                  sha256={p:sha(p) for p in [*sealed.values(),str(M/'node_entry.py'),str(M/'production-config-v2.json'),str(M/'smoke-config-v2.json')]},
                  initial_step=proof['step'],optimizer_reset=True,model_sha256=proof['model_sha256'])
    save(M/'runtime-build-v2.json',manifest)
    return cfg

def main():
    verify_source()
    assert not (M/'cloud-submission.json').exists(),'Existing or unknown submit: reconcile; never duplicate'
    assert load(B/'cloud-submission.json')['job_id']==OLD
    status('waiting_verified_checkpoint',batch_target='8prompts x4responses =32')
    while True:
        assert load(B/'cloud-submission.json')['job_id']==OLD,'Current allocation changed; refuse duplicate'
        latest=load_metrics();step=latest['step']
        failures=list((N/'control').glob('failure-rank-*.json'))
        if failures:raise RuntimeError('Source job failed before handoff: '+str(failures))
        candidates=[a for a in ANCHORS if a<500 and a>=step and (N/'production'/f'checkpoint-{a:04}'/'complete.json').exists()]
        if not candidates:
            if step>=500:status('source_completed_no_migration_needed',step=step);return
            status('waiting_verified_checkpoint',current_step=step,next_anchor=next(a for a in ANCHORS if a>=step))
            time.sleep(10);continue
        anchor=min(candidates);cp=N/'production'/f'checkpoint-{anchor:04}'
        status('verifying_checkpoint',step=anchor)
        proof=checkpoint_proof(cp)
        if load_metrics()['step']>anchor:
            status('next_anchor_required',checkpoint_step=anchor,current_step=load_metrics()['step'])
            time.sleep(10);continue
        verify_source();cfg=prepare_configs(cp,proof)
        if load_metrics()['step']>anchor:continue
        break
    # CPU-side Cloud calls only after all immutable source and complete weights passed.
    os.environ['NB_PREFIX']='/notebook/'+os.environ['NAMESPACE']+'/'+os.environ['WORKSPACE_ID']
    import client_lib as cloud
    import requests
    headers={'X-Api-Key':cloud.environment.GW_API_KEY,'X-Namespace':cloud.environment.NAMESPACE}
    url='http://'+cloud.environment.GW_API_ADDR+'/job_status'
    def query(ident):return requests.get(url,params=dict(job=ident,region=cloud.RegionMT.SR004),headers=headers,timeout=20)
    old=cloud.Job.__new__(cloud.Job);old.job_name=OLD;old.region=cloud.RegionMT.SR004
    assert old.status()=='Job status=Running'
    # Construct/validate the replacement before stopping source allocation.
    job=cloud.Job(script=str(M/'node_entry.py'),base_image='cr.ai.cloud.ru/aicloud-base-images/py3.11-torch2.6.0:0.0.41',
                  instance_type='a100.8gpu',region=cloud.RegionMT.SR004,type=cloud.Job.Type.pytorch2,pytorch_use_env=True,
                  job_desc='larin | tmp',n_workers=4,processes_per_worker=8,queue_name='edge',
                  priority_class=cloud.PriorityClass.medium,detached=True,max_retry=3,
                  env_variables={'PYTHONDONTWRITEBYTECODE':'1'})
    if load_metrics()['step']!=anchor:raise SourceAdvanced('Preserve newer updates; wait next exported anchor')
    save(M/'before-stop.json',dict(checkpoint_proof=proof,source_latest_metrics=load_metrics(),old_submission=load(B/'cloud-submission.json')))
    status('stopping_verified_source',step=anchor)
    reply=old.kill();assert 'deleted' in reply
    for _ in range(180):
        response=query(OLD)
        if response.status_code==400 and response.text.strip()=='"No such job"':break
        time.sleep(5)
    else:raise RuntimeError('Deletion unconfirmed: replacement not submitted')
    save(M/'source-deleted.json',dict(job_id=OLD,reply=reply,confirmed=True,time=time.time()))
    # Allow platform teardown; absence must remain confirmed before submit.
    time.sleep(20)
    response=query(OLD);assert response.status_code==400 and response.text.strip()=='"No such job"'
    final=load_metrics();assert final['step']==anchor,'Unexpected completed source step after snapshot; investigate before replacement'
    save(M/'source-training-preserved.json',dict(passed=True,completed_source_step=anchor,restored_weight_step=anchor,
                                               all_completed_updates_preserved=True,inflight_batch_discarded=True,
                                               optimizer_reset=True,source_run=str(N),time=time.time()))
    intent=dict(state='submitting',job_desc='larin | tmp',gpus=32,nodes=4,processes_per_node=8,
                current_run_root=str(M),supersedes=OLD,initial_step=anchor,steps=500,
                global_batch=cfg['global_batch'],optimizer_reset=True,exact_optimizer_resume=False,
                script=str(M/'node_entry.py'),script_sha256=sha(M/'node_entry.py'),config_sha256=sha(M/'production-config-v2.json'),
                runtime_manifest_sha256=sha(M/'runtime-build-v2.json'),time=time.time())
    save(M/'cloud-submission.json',intent)
    response=job.submit();intent.update(reply=str(response),job_id=job.job_name,state='submitted' if job.job_name else 'unknown')
    save(M/'cloud-submission.json',intent)
    assert job.job_name,'Unknown submission: reconcile, never blindly resubmit'
    save(B/'cloud-submission.json',intent)
    status('submitted32_waiting_actual_smoke',job_id=job.job_name,initial_step=anchor,optimizer_reset=True)

if __name__=='__main__':
    lock=(M/'handoff.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    try:
        while True:
            try:
                main();break
            except SourceAdvanced:
                status('source_advanced_wait_next_anchor');time.sleep(10)
    except BaseException as error:
        status('failed',error=repr(error),traceback=traceback.format_exc())
        raise
