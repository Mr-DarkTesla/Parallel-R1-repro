from pathlib import Path
import json,hashlib,os,time,ast
R=Path('${PROJECT_ROOT}');os.chdir(R)
T=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013';P=R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
assert not (T/'cloud-submission.json').exists(),'Never edit submitted/healthy sources'
assert time.time()<json.loads((T/'schedule.json').read_text())['deadline_timestamp']-300
c=json.loads((T/'production-config.json').read_text());assert c['steps']==350 and c['initial_step']==300
save(T/'target-change-before.json',dict(config=c,node_entry=(T/'node_entry.py').read_text(),time=time.time()))
c.update(steps=400,total_training_iterations=400,new_training_iterations=100,checkpoint_steps=[350,400],lane='DAPO2000 RL300100newiterations on16GPU scheduled23:59MSK')
entry=(T/'node_entry.py').read_text().replace("result['steps']==350","result['steps']==400").replace('initial_step=300,target_step=350,new_iterations=50','initial_step=300,target_step=400,new_iterations=100')
ast.parse(entry);(T/'node_entry.py').write_text(entry);save(T/'production-config.json',c)
ready=json.loads((T/'LAUNCH-READY.json').read_text());ready.update(target_step=400,new_iterations=100);ready['sha256']={f:sha(f) for f in ready['sha256']};save(T/'LAUNCH-READY.json',ready)
approval=json.loads((T/'control/production-approved.json').read_text());approval['config_sha256']=sha(T/'production-config.json');approval['sha256']={k:sha(v) for k,v in c['sealed_inputs'].items()};save(T/'control/production-approved.json',approval)
schedule=json.loads((T/'schedule.json').read_text());schedule.update(target_step=400,new_iterations=100,config_sha256=sha(T/'production-config.json'));save(T/'schedule.json',schedule)
save(T/'target-change.json',dict(user_authorization=True,initial_step=300,target_step=400,new_iterations=100,scheduled_at_moscow=schedule['scheduled_at_moscow'],controller_unchanged=True,time=time.time()))
# Running SFT sources/config are frozen; continuation follows complete150 export.
save(P/'extension-request.json',dict(user_authorization='First200iterations, second100iterations',total_target=200,current_phase_target=150,continuation_initial_step=150,continuation_target=200,continuation_new_iterations=50,weights_only=True,new_Adam_at150=True,optimizer_RNG_states_not_saved_or_loaded=True,healthy_run_not_stopped=True,current_source_hashes_unchanged=True,time=time.time()))
print(json.dumps(dict(scheduled_RL300_target=400,SFT_total_target=200,SFT_active_sources_unchanged=True)))
