from pathlib import Path
import json
M=Path(__file__).parent
N=M.parent/'rl-r2-24gpu-20261012/recovery-20261012-global-parity'
R=Path('${PROJECT_ROOT}'); remote=R/M
(M/'runner').mkdir(exist_ok=True)
helper='''"""One response/rank, four ranks/prompt; exact prompt-local mean centering."""
import math

def partition(rank, world, group=4):
    if world % group or not 0 <= rank < world:
        raise ValueError('Invalid response partition')
    return rank//group, rank%group

def grouped_advantages(records, group=4):
    if len(records)%group: raise ValueError('Incomplete prompt groups')
    result=[]
    for start in range(0,len(records),group):
        chunk=records[start:start+group]
        if any(r['rank']!=start+i or r['prompt_index']!=start//group or r['sample_index']!=i for i,r in enumerate(chunk)):
            raise ValueError('Duplicate or misordered response assignments')
        if len({r['id'] for r in chunk})!=1: raise ValueError('Mixed prompts in reward group')
        rewards=[r['reward'] for r in chunk]
        if not all(math.isfinite(x) for x in rewards): raise ValueError('Nonfinite rewards')
        mean=sum(rewards)/group
        result.extend(x-mean for x in rewards)
    return result
'''
(M/'runner/rollout_partition.py').write_text(helper)
s=(N/'runner/train.py').read_text()
s=s.replace('Expected exactly 24 distributed training ranks','Expected exactly 32 distributed training ranks').replace("cfg.get('expected_world_size', 24)","cfg.get('expected_world_size', 32)")
s=s.replace("    group = int(cfg.get('group', 4))", "    group = int(cfg['group'])\n    from rollout_partition import partition, grouped_advantages\n    assert world == 32 and group == 1 and cfg['reward_group'] == 4\n    assert cfg['global_batch'] == dict(prompts_per_step=8, rollouts_per_prompt=4, responses_per_step=32)\n    prompt_index, sample_index = partition(rank, world)")
a=s.index('    start_step = 0\n'); b=s.index('    def memory_snapshot',a)
s=s[:a]+'''    start_step = int(cfg.get('initial_step', 0))
    assert 0 < start_step < steps
    checkpoint = Path(cfg['initial_checkpoint'])
    complete = json.loads((checkpoint/'complete.json').read_text())
    assert complete['step'] == start_step and complete['optimizer'] is False and complete['unsharded']
    assert Path(cfg['model']).resolve() == (checkpoint/'hf').resolve()
    resume_proof = dict(checkpoint=str(checkpoint), initial_step=start_step,
                        weights_only_continuation=True, optimizer_reset=True, exact_optimizer_resume=False)
''' + s[b:]
s=s.replace('        position = (step-1)*world + rank',"        position = int(cfg['prompt_exposure_offset']) + (step-start_step-1)*8 + prompt_index")
s=s.replace("cfg.get('seed',20261010)+step*100000+rank*1000+sample*100", "cfg.get('seed',20261010)+step*100000+prompt_index*1000+sample_index*100")
s=s.replace('step=step, rank=rank, sample=sample)', 'step=step, rank=rank, sample=sample_index, prompt_index=prompt_index)')
s=s.replace("        advantages = centered([float(t['reward']['score']) for t in trajectories])",'''        reward_record = dict(rank=rank, prompt_index=prompt_index, sample_index=sample_index,
                             id=row['id'], reward=float(trajectories[0]['reward']['score']))
        reward_records = [None]*world
        dist.all_gather_object(reward_records, reward_record)
        advantages = [grouped_advantages(reward_records)[rank]]''')
s=s.replace('(step >= 20 and parity_skips/step > .10)', '((step-start_step) >= 20 and parity_skips/(step-start_step) > .10)')
s=s.replace('group=group, rewards=', 'group=group, reward_group=4, prompt_index=prompt_index, sample_index=sample_index,\n                      phase_iteration=step-start_step, global_responses_per_step=32, rewards=')
s=s.replace("final=str(output/f'checkpoint-{steps:04}'/'hf')))","final=str(output/f'checkpoint-{steps:04}'/'hf'), initial_step=start_step, optimizer_reset=True))")
(M/'runner/train.py').write_text(s)
s=(N/'node_entry.py').read_text().replace('real 24-rank','real 32-rank').replace('durable fresh 500-step','weights-only continuation to global step500')
s=s.replace("B=R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity'", "B=R/'work/experiments/rl-r2-32gpu-batch32-20261012'")
s=s.replace('world==24','world==32').replace('rank<24','rank<32').replace('range(24)','range(32)').replace("WORLD_SIZE='24'","WORLD_SIZE='32'").replace('world_size=24','world_size=32').replace("})==3","})==4").replace('nodes=3','nodes=4')
s=s.replace("assert [x['step'] for x in rows]==[1,2]", "initial=json.loads((B/'production-config-v2.json').read_text())['initial_step']\n                    assert [x['step'] for x in rows]==[initial+1,initial+2]")
s=s.replace("x['max_replay_logp_drift']<=.01 for x in rows", "x['max_replay_logp_drift']<=.01 and x['replay_guard_passed'] and x['group']==1 and x['reward_group']==4 for x in rows")
s=s.replace("authorization='User requested full500 R2 on24GPU; autonomous actual engineering review'", "authorization='User authorized careful migration32GPU, batch8prompts x4responses, preserve weights and continue global500'")
s=s.replace("                assert production['reward_mode']", "                assert production['global_batch']==dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32)\n                assert production['expected_world_size']==32\n                assert production['reward_mode']")
(M/'node_entry.py').write_text(s)
