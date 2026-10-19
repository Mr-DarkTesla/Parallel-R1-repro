"""Isolate the confirmed replay OOM repair; retain original DDP and loss math."""
from pathlib import Path
import ast, hashlib, json, os, shutil, time
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
P=O/'repair-02-replay-memory'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
assert not P.exists(),'Do not overwrite a repair or duplicate a submission'
P.mkdir();shutil.copytree(O/'src',P/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(O/'reward.py',P/'reward.py')
f=P/'src/train.py';s=f.read_text()
needle='        for j, (i, call) in enumerate(all_calls):\n'
assert s.count(needle)==1
s=s.replace(needle,needle+"            gc.collect();torch.cuda.empty_cache()\n            atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,call=j,total_calls=len(all_calls),phase='replay_forward',time=time.time()))\n")
needle='                with profiler.phase("backward"):\n                    loss.backward()'
assert s.count(needle)==1
s=s.replace(needle,"                # Only unoccupied allocator blocks; live autograd and gradients stay.\n                torch.cuda.empty_cache()\n                atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,call=j,total_calls=len(all_calls),phase='backward',time=time.time()))\n"+needle+"\n                atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,call=j,total_calls=len(all_calls),phase='backward_complete',time=time.time()))")
needle='                del logp, old, p0, rho, drift, loss_tokens, ratio, loss'
assert s.count(needle)==1
s=s.replace(needle,needle+', _\n                gc.collect();torch.cuda.empty_cache()')
assert 'ddp = DDP(model, device_ids=[local_rank]' in s and 'else ddp.no_sync()' in s
f.write_text(s)
s=(O/'node_entry.py').read_text().replace(str(O),str(P))
assert "NCCL_DEBUG='WARN')" in s
s=s.replace("NCCL_DEBUG='WARN')","NCCL_DEBUG='WARN',PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True')")
(P/'node_entry.py').write_text(s)
c=json.loads((O/'production-config.json').read_text().replace(str(O),str(P)));save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
old=json.loads((O/'production-config.json').read_text())
assert c['global_batch']['responses_per_step']==64 and c['expected_world_size']==16 and c['initial_step']==300 and c['steps']==400
assert c['response_budget']==32000 and c['path_budget']==4000 and c['max_context']==40960 and c['lr']==1e-6
assert c['train']==old['train'] and sha(P/'reward.py')==sha(O/'reward.py')
save(P/'repair-receipt.json',dict(passed=True,source_AST=True,confirmed_root_cause='rank3 CUDA OOM loss.backward: requested1.45GiB/free1.32GiB/reserved_unused9GiB/actor17.06GiB',old_job='HISTORICAL_JOB',secondary='Peer NCCL timeout and platform retry bootstrap FileExistsError',changes=['expandable_segments:True','release unused CUDA allocator cache before replay/backward and after deleting per-call tensors','per-rank replay/backward phase timestamps'],DDP_and_no_sync_unchanged=True,loss_reward_data_caps_batch_guards_unchanged=True,no_new_GPU_test=True,actual_GPU_memory_result_not_yet_verified=True,old_sources_logs_raw_preserved=True,no_completed_new_updates_lost=True,time=time.time()))
files=[P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]
save(P/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(f):sha(f) for f in files},initial_step=300,target_step=400,new_iterations=100,no_fresh_GPU_smoke=True,time=time.time()))
(P/'control').mkdir();proof=Path(c['gpu_audit'])
save(P/'control/production-approved.json',dict(approved=True,config_sha256=sha(P/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),authorization='Standing isolated terminal-run repair; no fresh GPU test',qualification_scope='Existing engine proof, original DDP/math retained; memory repair has no new GPU qualification',time=time.time()))
N1=O/'repair-01-explicit-gradient-sync'
if N1.exists():save(N1/'SUPERSEDED.json',dict(reason='Confirmed rank3 CUDA OOM; speculative DDP root cause not established. Do not launch.',replacement=str(P),time=time.time()))
print(json.dumps(dict(prepared=True,root=str(P),config_sha256=sha(P/'production-config.json'),not_launched=True)))
