from pathlib import Path
import ast,json,hashlib,shutil,time,os
R=Path('${PROJECT_ROOT}');os.chdir(R)
B=R/'work/experiments/rl-r4-dapo2k-paired-20261013';S=B/'from-sft';P=R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
if P.exists():
 assert not (P/'LAUNCH-READY.json').exists() and not (P/'cloud-submission.json').exists(),'Never overwrite sealed or submitted sources'
 shutil.rmtree(P)
P.mkdir();shutil.copytree(S/'src',P/'src');shutil.copy(S/'reward.py',P/'reward.py')
entry=(S/'node_entry.py').read_text().replace(str(S),str(P))
entry=entry.replace('world==8 and 0<=rank<8 and local==rank','world==16 and 0<=rank<16 and local==rank%8')
entry=entry.replace('range(8)','range(16)').replace("ready['world_size']==8","ready['world_size']==16").replace("WORLD_SIZE='8'","WORLD_SIZE='16'")
entry=entry.replace("LOCAL_WORLD_SIZE='16'","LOCAL_WORLD_SIZE='8'")
entry=entry.replace("len({r['host'] for r in records})==1","len({r['host'] for r in records})==2")
entry=entry.replace('world_size=8','world_size=16').replace('all8exit0=True','all16exit0=True')
entry=entry.replace("save(C/f'ready-rank-{rank}.json'","if local==0:assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()\n save(C/f'ready-rank-{rank}.json'")
(P/'node_entry.py').write_text(entry)
c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)))
c.update(world_size=16,expected_world_size=16,group=4,checkpoint_steps=[50,100,150],lane='DAPO2000 SFT fresh150 iterations on16GPU batch64',initial_step=0,initial_checkpoint=None,steps=150,new_training_iterations=150,total_training_iterations=150,processes_per_node=8)
save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
# Source-level assignment review, not a new GPU smoke/test run.
assert "LOCAL_WORLD_SIZE='8'" in entry and "WORLD_SIZE='16'" in entry and 'local==rank%8' in entry
assert c['global_batch']==dict(prompts_per_step=16,rollouts_per_prompt=4,responses_per_step=64)
assert c['resume'] is None and c['optimizer_reset'] and c['model'].endswith('instruct-full-20261011/runs/epoch1/final')
sources=[P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]
save(P/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(f):sha(f) for f in sources},fresh_GPU_smoke=False,user_authorization='One16GPU run from SFT weights,150iterations,direct production',initial_step=0,target_step=150,new_iterations=150,weights_only_newAdam=True,time=time.time()))
(P/'control').mkdir();proof=Path(c['gpu_audit'])
save(P/'control/production-approved.json',dict(approved=True,config_sha256=sha(P/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='User direct production/no fresh GPU smoke; existing8GPU engine proof cited,16GPU newproduction notyetverified',time=time.time()))
save(P/'planning-receipt.json',dict(model=c['model'],initial_step=0,target_step=150,iterations=150,global_batch=64,world_size=16,nodes=2,caps=dict(response=32000,path=4000,context=40960),train_manifest=str(B/'data/manifest.json'),new_Adam=True,optimizer_states_loaded=False,RNG_states_loaded=False,loss_denominator=32000,user_authorization='Start16GPU fromSFT, cancel bothpaired8GPU plans',time=time.time()))
save(P/'source-current.json',json.loads((B/'source-current.json').read_text()))
print(json.dumps(dict(prepared=str(P),world_size=16,target=150,config_sha256=sha(P/'production-config.json'))),flush=True)
