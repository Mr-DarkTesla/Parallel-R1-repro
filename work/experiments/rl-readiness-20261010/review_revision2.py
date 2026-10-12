"""Independent artifact/counter/mask/prefix/reward review of actual two-step smoke."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REWARD_SHA = '4c7ceb7f0fe50b2cdfb69308ae2a26459ea9bbd67dee351a14ead4c5f1db5eac'


def read(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lines(p):
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def close(a,b):
    assert abs(float(a)-float(b))<1e-8, (a,b)


def check_trajectory(t,cfg,tok,problems,system):
    assert t['id'] in problems
    expected = tok.apply_chat_template([dict(role='system',content=system),
                      dict(role='user',content=problems[t['id']]['problem'])],
                      tokenize=True,add_generation_prompt=True)
    assert t['prompt_ids']==expected, 'Base plain training/inference prefix mismatch'
    calls=t['policy_calls'];mask=t['response_mask'];response=t['response_ids'];stats=t['stats']
    assert len(mask)==len(response) and all(x in [0,1] for x in mask)
    coverage=[0]*len(mask);replacements=0
    for c in calls:
        s=c['response_start'];e=s+len(c['generated_ids'])
        assert 0<=s<=e<=len(mask) and not any(coverage[s:e])
        coverage[s:e]=[1]*(e-s)
        assert len(c['generated_ids'])==len(c['old_logprobs'])
        assert all(math.isfinite(x) for x in c['old_logprobs'])
        assert c['structure_start']==len(expected) and c['temperature']==1.
        if c['phase']!='path':
            assert c['prompt_ids']==expected+response[:s]
        replacements+=sum(a!=b for a,b in zip(c['generated_ids'],response[s:e]))
    assert coverage==mask, 'Forced/injected tokens or sampled labels have incorrect loss mask'
    assert sum(mask)==sum(len(c['generated_ids']) for c in calls)==stats['sampled_tokens']
    assert len(mask)-sum(mask)==stats['forced_tokens']
    path_groups=[];group=[]
    for c in calls:
        if c['phase']=='path':group.append(c)
        elif group:path_groups.append(group);group=[]
    if group:path_groups.append(group)
    assert [len(g) for g in path_groups]==t['widths']
    assert len(path_groups)==stats['forks']==len(t['fork_batch_ledger'])
    branch_open=tok.encode('<Path>',add_special_tokens=False)
    branch_close=tok.encode('</Path>',add_special_tokens=False)[0]
    for group in path_groups:
        first_header=branch_open+tok.encode('1\n',add_special_tokens=False)
        common=group[0]['prompt_ids'][:-len(first_header)]
        for index,c in enumerate(group,1):
            header=branch_open+tok.encode(str(index)+'\n',add_special_tokens=False)
            assert c['prompt_ids']==common+header, 'Sibling leak into rollout prefix'
            s=c['response_start'];assert response[s-len(header):s]==header
            visible=response[s:s+len(c['generated_ids'])];raw=c['generated_ids']
            assert visible==raw or visible==raw[:-1]+[branch_close], 'Unexpected policy relabeling'
    ledger=t['fork_batch_ledger']
    physical=sum(len(c['generated_ids']) for c in calls if c['phase']!='path')
    prefill=sum(bool(c['generated_ids']) for c in calls if c['phase']!='path')
    for width,batch in zip(t['widths'],ledger):
        assert batch['microbatch_max_paths']==cfg['max_batched_paths']==2
        assert batch['requested_rows']==width
        assert batch['physical_forward_calls']==sum(g['physical_forward_calls'] for g in batch['sequential_subgroups'])
        assert batch['prefill_forward_calls']==sum(g['prefill_forward_calls'] for g in batch['sequential_subgroups'])
        for g in batch['sequential_subgroups']:
            assert len(g['call_indices'])<=2
            assert g['physical_forward_calls']==max(g['generated_lengths'],default=0)
            assert g['active_row_forward_work']==sum(g['generated_lengths'])
        physical+=batch['physical_forward_calls'];prefill+=batch['prefill_forward_calls']
    assert physical==stats['actual_model_forward_calls'], 'Physical forward double count or missing subgroup'
    assert prefill==stats['actual_prefill_forward_calls']
    assert physical-prefill==stats['actual_decode_forward_calls']
    assert sum(mask)==stats['serial_equivalent_forward_calls']
    assert 0<physical<=sum(mask)
    # Independent direct formula, without calling the reward implementation.
    correct=bool(t['grade']['correct']);valid=bool(t['format_valid']);step=t['step']-1
    penalty=min(.4,.02*(physical//200))
    scale=max(0.,min(1.,(64-step)/32)) if cfg['reward_mode']=='strong_width' else 0.
    width=sum(min(w-1,3)/3 for w in t['widths'])/len(t['widths']) if valid and t['widths'] else 0.
    bonus=scale*(.3*width+.05*min(4,len(t['widths']))) if valid else 0.
    reward=t['reward'];close(reward['score'],float(correct)*(1-penalty+bonus))
    close(reward['forward_penalty'],float(correct)*penalty)
    close(reward['fork_bonus'],float(correct)*bonus)
    assert reward['actual_generation_forward_calls']==physical
    close(reward['depth_penalty'],0);close(reward['token_penalty'],0)
    return dict(replacements=replacements,physical=physical,sampled=sum(mask),
                forks=stats['forks'],widths=t['widths'],correct=correct,valid=valid)


def main():
    from transformers import AutoTokenizer
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();cfg=read(a.config);run=Path(cfg['output'])
    assert cfg['steps']==2 and cfg['world_size']==8 and cfg['response_budget']==4096
    assert cfg['max_batched_paths']==2 and cfg['std_normalization'] is False
    assert cfg['actor_dtype']=='fp32' and cfg['tf32'] is False
    assert sha(cfg['reward'])==REWARD_SHA
    result=read(run/'result.json');status=read(run/'status.json');smoke=read(run/'smoke-proof.json')
    assert result['completed'] and result['steps']==2 and result['world_size']==8
    assert status['state']=='completed' and smoke['passed']
    assert smoke['config_sha256']==sha(a.config)
    assert read(run/'checkpoint-0002/complete.json')['step']==2
    assert (run/'checkpoint-0002/optimizer.pt').stat().st_size>30_000_000_000
    assert len(list((run/'checkpoint-0002').glob('rng-*.pt')))==8
    ready=read(Path(a.config).parents[1]/'ready.json')
    sealed=cfg.get('sealed_inputs') or read(Path(a.config).parent/'forward_only.json')['sealed_inputs']
    for name,path in sealed.items():assert sha(path)==ready['sealed_sha256'][name],name
    gpu=read(cfg['gpu_audit']);batch_gpu=read(cfg['batch_gpu_audit'])
    assert gpu['passed'] and batch_gpu['passed'] and gpu['model']==batch_gpu['model']==cfg['model']
    token=AutoTokenizer.from_pretrained(cfg['model'],local_files_only=True)
    source=lines(cfg['train']);problems={r['id']:r for r in source};system=Path(cfg['system']).read_text()
    traces=[];metrics=[]
    for rank in range(8):
        local=lines(run/f'metrics-rank-{rank}.jsonl')
        assert [x['step'] for x in local]==[1,2]
        for m in local:
            assert m['rank']==rank and m['trainable']>=4_000_000_000 and m['optimizer_step']
            assert math.isfinite(m['loss']) and math.isfinite(m['grad_norm']) and m['grad_norm']>0
            assert m['backbone_update_l2']>0
            assert m['max_replay_logp_drift']<=.01 and m['mean_replay_logp_drift']<=.002 and m['p95_replay_logp_drift']<=.005
            mean=sum(r['score'] for r in m['rewards'])/len(m['rewards'])
            for adv,r in zip(m['advantages'],m['rewards']):close(adv,r['score']-mean)
            metrics.append(m)
        local_traces=lines(run/f'traces-rank-{rank}.jsonl')
        assert len(local_traces)==cfg['group']*2
        assert {(t['step'],t['sample']) for t in local_traces}=={(s,i) for s in [1,2] for i in range(cfg['group'])}
        traces.extend(check_trajectory(t,cfg,token,problems,system) for t in local_traces)
    report=dict(passed=True,independent=True,reviewed_config=str(Path(a.config).resolve()),
                config_sha256=sha(a.config),actual_steps_per_rank=2,ranks=8,optimizer_updates_per_rank=2,
                resident_Adam_iteration2_observed=True,smoke_proof_sha256=sha(run/'smoke-proof.json'),
                source_sha256={name:sha(path) for name,path in sealed.items()},
                trace_count=len(traces),raw_replacements=sum(t['replacements'] for t in traces),
                actual_physical_forwards=sum(t['physical'] for t in traces),sampled_tokens=sum(t['sampled'] for t in traces),
                max_gpu_bytes=max(m['peak_gpu_bytes'] for m in metrics),
                max_logp_drift=max(m['max_replay_logp_drift'] for m in metrics),
                zero_advantage_groups=sum(m['zero_advantage_group'] for m in metrics),
                prefix_mask_rawtargets_physicalcost_reward_all_checked=True,
                limitations='Two-step smoke is engineering evidence, not evidence of reward quality or benchmark improvement')
    out=Path(a.output);assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,report=str(out),sha256=sha(out),max_gpu_bytes=report['max_gpu_bytes'])))


if __name__=='__main__':main()
