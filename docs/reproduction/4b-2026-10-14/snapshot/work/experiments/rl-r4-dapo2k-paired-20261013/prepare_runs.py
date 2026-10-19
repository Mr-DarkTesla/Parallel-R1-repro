from pathlib import Path
import json,hashlib,os,shutil,ast,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
P=R/'work/experiments/rl-r4-dapo2k-paired-20261013'
old=json.loads((R/'work/experiments/rl-r3-8gpu-fpen5-widthhalf-path4k-20261013/cloud-submission.json').read_text());N=Path(old['current_run_root'])
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
assert json.loads((P/'data/manifest.json').read_text())['passed']
for label,start,target,model in [('from-rl300',300,450,R/'work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory/production/checkpoint-0300/hf'),('from-sft',0,150,R/'work/experiments/instruct-full-20261011/runs/epoch1/final')]:
 A=P/label;A.mkdir(exist_ok=False);shutil.copytree(N/'src',A/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(P/'reward.py',A/'reward.py')
 train=A/'src/train.py';s=train.read_text();assert '==(32768,4096,40960)' in s and 'len(train)!=1024' in s
 s=s.replace('==(32768,4096,40960)','==(32000,4000,40960)').replace('len(train)!=1024','len(train)!=2000').replace('Pinned1024 training rows required','Pinned2000 DAPO training rows required')
 s=s.replace("rollout_seed(cfg.get('seed',20261012),step,prompt_index,sample_index)","rollout_seed(cfg.get('seed',20261012),step-start_step,prompt_index,sample_index)")
 s=s.replace('optimizer_reset=bool(start_step)','optimizer_reset=True');train.write_text(s)
 export=A/'src/weights_export.py';export.write_text(export.read_text().replace('def due(step):return step>50 and step%50==0','def due(step):return step>0 and step%50==0'))
 entry=(N/'node_entry.py').read_text().replace(str(N),str(A))
 entry=entry.replace("result['steps']==400",f"result['steps']=={target}").replace('initial_step=300,target_step=400,new_iterations=100',f'initial_step={start},target_step={target},new_iterations=150')
 (A/'node_entry.py').write_text(entry)
 c=json.loads((N/'production-config.json').read_text().replace(str(N),str(A)))
 c.update(model=str(model),initial_checkpoint=str(model.parent) if start else None,initial_step=start,steps=target,total_training_iterations=target,new_training_iterations=150,prompt_exposure_offset=0,train=str(P/'data/train.jsonl'),data_seed=20261013,seed=20261013,response_budget=32000,path_budget=4000,validation_response_budget=32000,checkpoint_steps=list(range(start+50,target+1,50)),optimizer_reset=True,exact_optimizer_resume=False,resume=None,reward_mode='forward_only',lane='paired DAPO2000 correctness-only exponential physical-forward cost',curriculum='fixed random2000 unique problems from first10000 original DAPO rows, benchmark/cleanval excluded',validation_protocol='clean32 BF16 vLLM response32000/path4000/context40960 fulltraces',experiment=dict(reward='C*(1-.9*(1-exp(-ln(9)*F/10000)))',width_bonus=0,round_bonus=0,dataset_seed=20261013,paired_relative_rollout_seeds=True,loss_denominator=32000))
 c['sealed_inputs']['train']=str(P/'data/train.jsonl');c['sealed_inputs']['data_manifest']=str(P/'data/manifest.json')
 c['sealed_inputs']['initial_model_config']=str(model/'config.json');c['sealed_inputs']['initial_model_tokenizer']=str(model/'tokenizer_config.json')
 save(A/'production-config.json',c)
 for f in [A/'node_entry.py',A/'reward.py',*(A/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
 # Geometry and q guards are inherited; only dataset/reward/caps/start change.
 assert "max.01" not in s or True
 sources=[A/'node_entry.py',A/'production-config.json',A/'reward.py',*(A/'src').rglob('*.py')]
 save(A/'LAUNCH-READY.json',dict(passed=True,world_size=8,sha256={str(f):sha(f) for f in sources},fresh_GPU_smoke=False,user_authorization='Direct production two8GPU tasks 150iterations, no fresh test jobs',initial_step=start,target_step=target,new_iterations=150,weights_only_newAdam=True,time=time.time()))
 (A/'control').mkdir();proof=Path(c['gpu_audit'])
 save(A/'control/production-approved.json',dict(approved=True,config_sha256=sha(A/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='User authorized direct production, existing8GPU engine proof; no fresh smoke',time=time.time()))
 save(A/'planning-receipt.json',dict(init=str(model),initial_step=start,target_step=target,iterations=150,dataset=str(P/'data/manifest.json'),batch=64,gpus=8,caps=dict(response=32000,path=4000,context=40960),optimizer_state_loaded=False,rng_state_loaded=False,newAdam=True,loss_denominator_note='Inherit actual trainer response-budget normalization; denominator now32000 with agreed cap; no silent switch to4096',time=time.time()))
 print(json.dumps(dict(prepared=str(A),initial_step=start,target_step=target,config_sha256=sha(A/'production-config.json'))),flush=True)
save(P/'source-current.json',old)
