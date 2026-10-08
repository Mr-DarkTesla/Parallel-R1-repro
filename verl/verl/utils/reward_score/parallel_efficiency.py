"""Correctness-gated decode-depth cost and relative parallel-efficiency bonus.

Use with algorithm.split_accuracy_aux=true so group standardization does not
cancel the auxiliary coefficient. Validation reports accuracy alone.
"""

import math
import re

from verl.utils.reward_score.math_dapo import compute_score as accuracy_score


def valid_structure(text):
    """Require complete, unnested blocks with >=2 paths and a following summary."""
    stack = []
    paths = 0
    waiting_summary = False
    for token in re.findall(r'</?(?:Parallel|Path|Summary)>', text):
        if token == '<Parallel>':
            if stack or waiting_summary:
                return False
            stack.append('Parallel')
            paths = 0
        elif token == '<Path>':
            if stack != ['Parallel']:
                return False
            stack.append('Path')
            paths += 1
        elif token == '</Path>':
            if stack != ['Parallel', 'Path']:
                return False
            stack.pop()
        elif token == '</Parallel>':
            if stack != ['Parallel'] or paths < 2:
                return False
            stack.pop()
            waiting_summary = True
        elif token == '<Summary>':
            if stack or not waiting_summary:
                return False
            stack.append('Summary')
        elif token == '</Summary>':
            if stack != ['Summary']:
                return False
            stack.pop()
            waiting_summary = False
    return not stack and not waiting_summary


def compute_score(data_source, solution_str, solution_str_with_special_tokens,
                  ground_truth, extra_info=None, mode='gated_depth',
                  depth_lambda=0.0001, bonus_alpha=0.2):
    """Return accuracy and auxiliary components separately for split GRPO.

    D counts sequential generated tokens plus the longest path in each fork;
    T counts all generated tokens. Neither includes injected tags or prefill.
    Reward coefficients must be finite and nonnegative. Keep lambda*max(D)<1
    if a correct response must always score above an incorrect response.
    """
    if mode not in ('gated_depth', 'parallel_gain'):
        raise ValueError(f'Unknown efficiency reward mode: {mode}')
    for name, value in [('depth_lambda', depth_lambda), ('bonus_alpha', bonus_alpha)]:
        if not math.isfinite(value) or value < 0:
            raise ValueError(f'{name} must be finite and nonnegative')
    info = extra_info or {}
    stats = info.get('parallel_stats')
    if stats is None:
        raise ValueError('Efficiency rewards require parallel rollout statistics')
    depth, total, forks = (stats[key] for key in ('critical_depth', 'generated_tokens', 'forks'))
    if not all(math.isfinite(value) for value in (depth, total, forks)):
        raise ValueError('Parallel statistics must be finite')
    if not 0 <= depth <= total or forks < 0:
        raise ValueError('Expected 0 <= critical_depth <= generated_tokens and forks >= 0')

    base = accuracy_score(solution_str, ground_truth)
    acc = bool(base['acc'])
    valid = valid_structure(solution_str_with_special_tokens)
    efficiency = 1.0 - depth / total if total > 0 else 0.0
    if mode == 'gated_depth':
        auxiliary = -depth_lambda * depth * acc
    else:
        auxiliary = bonus_alpha * acc * efficiency * int(valid and forks > 0)
    if info.get('validate', False):
        auxiliary = 0.0
    return dict(
        score=float(acc) + auxiliary, acc=acc, pred=base['pred'],
        accuracy_reward=float(acc), aux_reward=auxiliary,
        critical_depth=float(depth), generated_tokens=float(total),
        parallel_efficiency=efficiency,
        depth_penalty=-auxiliary if mode == 'gated_depth' else 0.0,
        parallel_bonus=auxiliary if mode == 'parallel_gain' else 0.0,
        forks=float(forks), parallel=float(forks > 0), format_ok=float(valid),
        question_id=str(info.get('index', 'unknown')), data_source=data_source,
    )
