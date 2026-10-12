"""Correctness-gated relative parallel efficiency pilot.

R = I[correct] * (1 + 0.2 * (1 - critical_depth/generated_tokens)).
Bonus requires a valid parallel format. Wrong responses always receive zero.
This measures structural efficiency, not physical GPU throughput. The legacy
depth_lambda argument is unused and retained only for launcher compatibility.

Depth counts sampled tokens, including sampled stop tokens, along the longest
dependency chain. Injected tags cost no model call. Prompt-prefill FLOPs and
physical GPU batch forwards are different quantities and are not this reward.
"""
import math
from verl.utils.reward_score.math_dapo import compute_score as accuracy_score
from verl.utils.reward_score.math_dapo_acc_parallel_interved import compute_score as s2_score
from verl.utils.reward_score.gsm8k_add_special_token_reward import check_parallel_thinking_format


def critical_depth(calls):
    depth=0
    paths=[]
    for call in calls:
        n=call['generated_tokens']
        assert isinstance(n,int) and n>=0
        if call['phase']=='path':
            paths.append(n)
        else:
            assert call['phase'] in ('main','summary'),call['phase']
            if paths:
                depth+=max(paths)
                paths=[]
            depth+=n
    return depth+(max(paths) if paths else 0)


def compute_score(data_source,solution_str,solution_str_with_special_tokens,ground_truth,
                  extra_info=None,mode='s2',depth_lambda=0.0001):
    info=extra_info or {}
    stats=info['parallel_stats']
    depth=stats['critical_depth']
    assert isinstance(depth,(int,float)) and math.isfinite(depth) and 0<=depth<=3000,depth
    base=accuracy_score(solution_str,ground_truth)
    acc=bool(base['acc'])
    total=stats['generated_tokens']
    assert isinstance(total,(int,float)) and math.isfinite(total) and total>=depth
    valid=not check_parallel_thinking_format(solution_str_with_special_tokens)
    gain=(1.-depth/total) if total>0 and valid and stats['forks']>0 else 0.
    if info.get('validate',False):
        reward=float(acc)
    elif mode=='s2':
        reward=s2_score(solution_str,solution_str_with_special_tokens,ground_truth,info['global_steps'])['score']
    else:
        assert mode=='depth'
        assert depth_lambda==0.0001
        reward=float(acc)*(1.+.2*gain)
    return dict(score=reward,acc=acc,pred=base['pred'],critical_depth=float(depth),
                depth_penalty=0.,parallel_efficiency=gain,generated_tokens=float(total),
                forks=float(stats['forks']),parallel=float(stats['forks']>0),
                format_ok=float(not check_parallel_thinking_format(solution_str_with_special_tokens)),
                question_id=str(info.get('index','unknown')),data_source=data_source)
