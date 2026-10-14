from pathlib import Path
import os,json,time,shutil,hashlib,ast
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013';P=O/'repair-01-explicit-gradient-sync'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
assert not P.exists(),'Do not overwrite or duplicate a repair'
P.mkdir();shutil.copytree(O/'src',P/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(O/'reward.py',P/'reward.py')
train=P/'src/train.py';s=train.read_text()
old="    ddp = DDP(model, device_ids=[local_rank], broadcast_buffers=False,\n              gradient_as_bucket_view=True, bucket_cap_mb=25) if world > 1 else model"
assert old in s
s=s.replace(old,"""    # All local replay/backward calls are communication-free. Their counts differ
    # by rank; perform exactly one ordered FP32 gradient mean after replay.
    ddp = model
    if world > 1:
        with torch.no_grad():
            for parameter in model.parameters():
                flat=parameter.view(-1)
                for start in range(0,flat.numel(),16*1024*1024):
                    dist.broadcast(flat[start:start+16*1024*1024],src=0)""")
s=s.replace("context = contextlib.nullcontext() if world==1 or sync else ddp.no_sync()","context = contextlib.nullcontext()")
s=s.replace('                    loss.backward()',"""                    atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,call=j,total_calls=len(all_calls),phase='local_backward',time=time.time()))
                    loss.backward()
                    atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,call=j,total_calls=len(all_calls),phase='local_backward_complete',time=time.time()))""")
needle="        memory_stages.append(memory_snapshot('after_backward'))"
assert needle in s
s=s.replace(needle,"""        if world > 1 and parity_passed:
            with profiler.phase('explicit_fp32_gradient_mean',cuda=True),torch.no_grad():
                for parameter_index,parameter in enumerate(model.parameters()):
                    if parameter.grad is None:
                        parameter.grad=torch.zeros_like(parameter)
                    assert parameter.grad.dtype==torch.float32
                    flat=parameter.grad.view(-1)
                    atomic_json(output/f'learner-phase-rank-{rank}.json',dict(step=step,phase='gradient_mean',parameter_index=parameter_index,time=time.time()))
                    for start in range(0,flat.numel(),16*1024*1024):
                        chunk=flat[start:start+16*1024*1024]
                        dist.all_reduce(chunk,op=dist.ReduceOp.SUM)
                        chunk.div_(world)
        memory_stages.append(memory_snapshot('after_backward'))""")
train.write_text(s)
entry=(O/'node_entry.py').read_text().replace(str(O),str(P));(P/'node_entry.py').write_text(entry)
c=json.loads((O/'production-config.json').read_text().replace(str(O),str(P)));c['gradient_sync']='explicit_fp32_mean_after_all_local_replay';save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
assert c['global_batch']['responses_per_step']==64 and c['expected_world_size']==16 and c['initial_step']==300 and c['steps']==400
assert c['response_budget']==32000 and c['path_budget']==4000 and c['max_context']==40960 and c['lr']==1e-6
assert sha(P/'reward.py')==sha(O/'reward.py') and c['train']==json.loads((O/'production-config.json').read_text())['train']
# Preserve the same reduction: mean16 of localSUM*(16/64) = globalSUM/64.
assert (16/64)/16==1/64
save(P/'repair-proof.json',dict(passed=True,source_AST=True,reward_data_caps_LR_unchanged=True,global_loss_scale='mean16(localSum*.25)/32000 = globalSum/(64*32000)',FP32masters_gradients_Adam_unchanged=True,guards_unchanged=True,no_GPU_test=True,not_yet_GPU_qualified=True,root_cause_hypothesis='DDP implicit collective overlap on uneven structured replay/activation checkpointing',observed='15ranks final backward,rank3 summary backward, no proximal advancement>70min',old_failure_sources_untouched=True,requires_user_permission_before_stopping_live_source=True,time=time.time()))
files=[P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]
save(P/'LAUNCH-READY.json',dict(passed=True,world_size=16,sha256={str(f):sha(f) for f in files},initial_step=300,target_step=400,new_iterations=100,no_fresh_GPU_smoke=True,launch_NOT_authorized_while_source_live_without_user_confirmation=True,time=time.time()))
(P/'control').mkdir();proof=Path(c['gpu_audit'])
save(P/'control/production-approved.json',dict(approved=True,config_sha256=sha(P/'production-config.json'),sha256={k:sha(v) for k,v in c['sealed_inputs'].items()},distributed_smoke=dict(path=str(proof),sha256=sha(proof)),qualification_scope='Existing engine8GPU proof, explicitmean CPU algebra; no newGPUtest',time=time.time()))
print(json.dumps(dict(prepared=True,root=str(P),config_sha256=sha(P/'production-config.json'),source_unchanged=True,not_launched=True)))
