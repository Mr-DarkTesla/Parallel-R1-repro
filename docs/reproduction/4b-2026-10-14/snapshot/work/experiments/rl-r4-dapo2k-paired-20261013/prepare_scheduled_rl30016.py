from pathlib import Path
import os,json,hashlib,shutil,ast,time,datetime
from zoneinfo import ZoneInfo
R=Path('${PROJECT_ROOT}');os.chdir(R)
S=R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013';P=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
assert not P.exists(),'Reconcile scheduled namespace before any retry'
P.mkdir();shutil.copytree(S/'src',P/'src');shutil.copy(S/'reward.py',P/'reward.py')
entry=(S/'node_entry.py').read_text().replace(str(S),str(P)).replace("result['steps']==150","result['steps']==350").replace('initial_step=0,target_step=150,new_iterations=150','initial_step=300,target_step=350,new_iterations=50')
(P/'node_entry.py').write_text(entry)
c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)))
checkpoint=R/'work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory/production/checkpoint-0300';complete=json.loads((checkpoint/'complete.json').read_text());assert complete['step']==300 and complete['unsharded'] and complete['weights_only']
c.update(model=str(checkpoint/'hf'),initial_checkpoint=str(checkpoint),initial_step=300,steps=350,total_training_iterations=350,new_training_iterations=50,checkpoint_steps=[350],lane='DAPO2000 RL30050newiterations on16GPU scheduled23:59MSK')
c['sealed_inputs']['initial_model_config']=str(checkpoint/'hf/config.json');c['sealed_inputs']['initial_model_tokenizer']=str(checkpoint/'hf/tokenizer_config.json');c['sealed_inputs']['initial_weights_complete']=str(checkpoint/'complete.json')
save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
sources=[P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]
save(P/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(f):sha(f) for f in sources},fresh_GPU_smoke=False,user_authorization='Second16GPU job fromRL300 for50iterations scheduled23:59MSK server-side',initial_step=300,target_step=350,new_iterations=50,weights_only_newAdam=True,time=time.time()))
(P/'control').mkdir();proof=Path(c['gpu_audit'])
save(P/'control/production-approved.json',dict(approved=True,config_sha256=sha(P/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='User direct production, second16GPU allocation, no fresh GPU smoke',time=time.time()))
deadline=datetime.datetime(2026,10,13,23,59,tzinfo=ZoneInfo('Europe/Moscow'))
assert deadline.timestamp()>time.time(),'Scheduled time already passed; do not silently launch late'
save(P/'schedule.json',dict(status='scheduled',scheduled_at_moscow=deadline.isoformat(),scheduled_at_utc=deadline.astimezone(datetime.timezone.utc).isoformat(),deadline_timestamp=deadline.timestamp(),server_side=True,mac_network_not_required=True,gpus=16,nodes=2,initial_step=300,target_step=350,new_iterations=50,separate_allocation=True,must_not_stop_sft_job=True,model=c['model'],config_sha256=sha(P/'production-config.json'),time=time.time()))
print(json.dumps(dict(prepared=str(P),scheduled=deadline.isoformat(),gpus=16,steps='301..350')))
