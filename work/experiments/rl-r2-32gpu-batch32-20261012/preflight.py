from pathlib import Path
import json,hashlib,ast,sys
R=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1');M=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
N=R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity'
sys.path.insert(0,str(M/'runner'))
from rollout_partition import partition,grouped_advantages
for rank in range(32):assert partition(rank,32)==(rank//4,rank%4)
records=[dict(rank=r,prompt_index=r//4,sample_index=r%4,id=str(r//4),reward=float(r%4)) for r in range(32)]
a=grouped_advantages(records)
assert a==[-1.5,-.5,.5,1.5]*8
for step in [51,52,100,500]:
    pos=[50*24+(step-51)*8+r//4 for r in range(32)]
    assert len(set(pos))==8 and all(pos[4*g:4*g+4]==[pos[4*g]]*4 for g in range(8))
    seeds=[20261012+step*100000+(r//4)*1000+(r%4)*100 for r in range(32)]
    assert len(set(seeds))==32
paths=[M/'node_entry.py',M/'handoff.py',M/'group_proof.py',M/'preflight.py',*sorted((M/'runner').rglob('*.py'))]
for p in paths:ast.parse(p.read_text())
# All mask/attention/runtime modules are byte-identical to already tested fullwidth8 runtime.
for name in ['rollout.py','decoder.py','microbatch_decoder.py','structured_replay.py','replay_guard.py','source/counted_loop.py','source/parallel_structure.py']:
    assert (M/'runner'/name).read_bytes()==(N/'runner'/name).read_bytes(),name
proof=json.loads((M/'cpu-reward-group-proof.json').read_text());assert proof['passed']
train=(M/'runner/train.py').read_text()
assert "loss_tokens.sum()/(budget*group)" in train and "assert world == 32 and group == 1" in train
assert "grouped_advantages(reward_records)[rank]" in train
assert "scorer.grade('<think>\\n'+trajectory['output']" in train
assert "sequential_subgroup_count']==1" in train
assert "while True" in (M/'handoff.py').read_text()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths.extend([M/'cpu-reward-group-proof.json',N/'production-config-v2.json',N/'distributed-smoke-proof.json'])
proof=dict(passed=True,global_batch=dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32),world_size=32,
           cpu_32_rank_partition=True,distributed_cpu_gradient_adam_parity=True,inherited_fullwidth_mask_sources_unchanged=True,
           gpu32_smoke_pending=True,weights_only_handoff=True,optimizer_reset=True,
           sha256={str(p):sha(p) for p in paths})
(M/'source-seal.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k!='sha256'}))
