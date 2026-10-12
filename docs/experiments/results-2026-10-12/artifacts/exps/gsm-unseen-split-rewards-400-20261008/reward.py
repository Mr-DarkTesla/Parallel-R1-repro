"""Correctness-gated depth cost or parallel efficiency bonus.

Accuracy and auxiliary reward are normalized separately by split_grpo.py.
Depth is critical generated-token depth, not prefill or batched GPU FLOPs.
"""
import math
import re
from verl.utils.reward_score.math_dapo import compute_score as accuracy_score

def critical_depth(calls):
    depth=0;paths=[]
    for call in calls:
        n=call['generated_tokens']
        assert isinstance(n,int) and n>=0
        if call['phase']=='path':paths.append(n)
        else:
            assert call['phase'] in ('main','summary')
            if paths:depth+=max(paths);paths=[]
            depth+=n
    return depth+(max(paths) if paths else 0)

def valid_structure(text):
    """Validate complete, unnested Parallel/Path/Summary tag structure."""
    stack=[];paths=0;blocks=0;summaries=0;waiting_summary=False
    for token in re.findall(r'</?(?:Parallel|Path|Summary)>',text):
        if token=='<Parallel>':
            if stack or waiting_summary:return False
            stack.append('Parallel');paths=0;blocks+=1
        elif token=='<Path>':
            if stack!=['Parallel']:return False
            stack.append('Path');paths+=1
        elif token=='</Path>':
            if stack!=['Parallel','Path']:return False
            stack.pop()
        elif token=='</Parallel>':
            if stack!=['Parallel'] or paths<2:return False
            stack.pop();waiting_summary=True
        elif token=='<Summary>':
            if stack or not waiting_summary:return False
            stack.append('Summary');summaries+=1
        elif token=='</Summary>':
            if stack!=['Summary']:return False
            stack.pop();waiting_summary=False
    return not stack and not waiting_summary and blocks==summaries

def compute_score(data_source,solution_str,solution_str_with_special_tokens,ground_truth,
                  extra_info=None,mode='gated_depth',depth_lambda=0.0001,bonus_alpha=0.2):
    info=extra_info or {};stats=info['parallel_stats']
    depth=stats['critical_depth'];total=stats['generated_tokens'];forks=stats['forks']
    assert isinstance(depth,(int,float)) and math.isfinite(depth) and 0<=depth<=3000
    assert isinstance(total,(int,float)) and math.isfinite(total) and total>=depth
    assert depth_lambda==0.0001 and bonus_alpha==0.2
    base=accuracy_score(solution_str,ground_truth);acc=bool(base['acc'])
    valid=valid_structure(solution_str_with_special_tokens)
    efficiency=1.-depth/total if total>0 else 0.
    if mode=='gated_depth':aux=-depth_lambda*depth*acc
    else:
        assert mode=='parallel_gain'
        aux=bonus_alpha*acc*efficiency*int(valid and forks>0)
    if info.get('validate',False):aux=0.
    return dict(score=float(acc)+aux,acc=acc,pred=base['pred'],accuracy_reward=float(acc),aux_reward=aux,
        critical_depth=float(depth),generated_tokens=float(total),parallel_efficiency=efficiency,
        depth_penalty=-aux if mode=='gated_depth' else 0.,parallel_bonus=aux if mode=='parallel_gain' else 0.,
        forks=float(forks),parallel=float(forks>0),format_ok=float(valid),
        question_id=str(info.get('index','unknown')),data_source=data_source)
