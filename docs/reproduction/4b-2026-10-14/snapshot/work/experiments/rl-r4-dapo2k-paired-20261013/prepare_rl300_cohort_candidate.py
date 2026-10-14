"""Prepare only. No submission, signals, or edits to the live RL300 source."""
from pathlib import Path
import ast,hashlib,json,os,shutil,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
S=Path(json.loads((O/'cloud-submission.json').read_text())['current_run_root'])
P=O/'candidate-cohort4-separated-actor'
assert not P.exists(),'Do not overwrite a prepared candidate'
P.mkdir();shutil.copytree(S/'src',P/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(S/'reward.py',P/'reward.py')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
f=P/'src/train.py';s=f.read_text()
old='    decoder=ActorBuddy(model,cfg,rank,local_rank)'
assert s.count(old)==1
s=s.replace(old,'    gc.collect();torch.cuda.empty_cache()\n'+old)
old="        memory_stages.append(memory_snapshot('after_rollout'))"
assert s.count(old)==1
s=s.replace(old,old+"\n        # Preserve immutable behavior q/receipt, drain IPC, then release the\n        # entire actor process and KV pool before full-context learner work.\n        last_actor_rollout=decoder.last_rollout\n        with profiler.phase('actor_release_before_learner',cuda=True):\n            decoder.close()\n            del decoder\n            gc.collect();torch.cuda.empty_cache()\n        memory_stages.append(memory_snapshot('actor_released'))")
assert s.count("q_fixture=decoder.last_rollout['guard']")==1
s=s.replace("q_fixture=decoder.last_rollout['guard']","q_fixture=last_actor_rollout['guard']")
old='                decoder.refresh_actor(optimizer_update_id)'
assert s.count(old)==1
s=s.replace(old,"        # New actor receives the current full FP32 masters by exact CUDA IPC.\n        # Its bootstrap version is the committed learner version, including skips.\n        with profiler.phase('actor_rebuild_current_master',cuda=True):\n            gc.collect();torch.cuda.empty_cache()\n            decoder=ActorBuddy(model,dict(cfg,initial_step=optimizer_update_id),rank,local_rank)\n            decoder.last_rollout=last_actor_rollout")
assert 'ddp = DDP(model' in s and 'else ddp.no_sync()' in s
f.write_text(s)
entry=(S/'node_entry.py').read_text().replace(str(S),str(P));(P/'node_entry.py').write_text(entry)
c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)))
c['actor_episodes_per_wave']=4;c['slot_capacity']=196608
c['actor_lifecycle']='release_after_rollout_rebuild_from_current_master_after_learner'
save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
assert c['expected_world_size']==16 and c['global_batch']['responses_per_step']==64
assert c['response_budget']==32000 and c['path_budget']==4000 and c['max_context']==40960
assert sha(P/'reward.py')==sha(S/'reward.py')
save(P/'PREPARED-NOT-AUTHORIZED-TO-LAUNCH.json',dict(prepared=True,source_AST_pass=True,source=str(S),no_live_source_changes=True,no_process_signals=True,no_submit=True,no_GPU_test=True,no_measured_speedup=True,requires_explicit_user_switch_authorization=True,checkpoint_source_unchanged=True,unsaved_progress_would_be_lost_if_restarted_now=True,changes=['4 complete episodes per actor wave','KV capacity196608 slots','actor process/KV released before learner and rebuilt from actual current masters'],unchanged=['batch64','reward/data/caps','DDP/no_sync/loss','FP32masterAdam','immutableq/TIS/guards','fullwidth8'],estimated_KV_bytes=196608*36*8*128*2*2,memory_estimate_not_GPU_proof=True,sha256={str(f):sha(f) for f in [P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]},time=time.time()))
print(json.dumps(dict(prepared=True,root=str(P),not_launched=True,config_sha256=sha(P/'production-config.json'))))
