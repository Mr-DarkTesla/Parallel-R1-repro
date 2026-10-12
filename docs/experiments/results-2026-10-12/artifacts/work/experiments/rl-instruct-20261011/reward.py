"""Paired Instruct RL rewards: physical forward cost and a constant bonus.

All counts come from executed trajectories. No bonus annealing is performed.
"""
import math


def _count(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be a nonnegative integer')
    if not math.isfinite(value) or value < 0 or int(value) != value:
        raise ValueError(f'{name} must be a nonnegative integer')
    return int(value)


def score(correct, valid, depth, total, widths, step=0, mode='strong_width', *, forward_calls=None):
    if type(correct) is not bool or type(valid) is not bool:
        raise ValueError('Correctness and format verdicts must be explicit booleans')
    if mode not in ('forward_only', 'strong_width'):
        raise ValueError(f'Unknown reward mode: {mode}')
    depth, total = _count('depth', depth), _count('total', total)
    step = _count('step', step)
    forwards = _count('forward_calls', forward_calls)
    if not 0 < depth <= total or not 0 < forwards <= total:
        raise ValueError('Require positive depth and actual generation forwards <= sampled tokens')
    widths = [_count('width', w) for w in widths]
    if any(not 2 <= w <= 8 for w in widths):
        raise ValueError('Executed fork widths must be in [2,8]')
    cost = min(.4, .02 * (forwards // 200))
    width_units = sum(min(w - 1, 3) / 3 for w in widths) / len(widths) if widths else 0.
    round_units = min(len(widths), 4)
    scale = float(mode == 'strong_width' and valid)
    width_bonus = scale * .3 * width_units
    round_bonus = scale * .05 * round_units
    accuracy = float(correct)
    auxiliary = accuracy * (-cost + width_bonus + round_bonus)
    return dict(score=accuracy + auxiliary, accuracy_reward=accuracy, aux_reward=auxiliary,
                forward_penalty=accuracy * cost, token_penalty=0., depth_penalty=0.,
                width_bonus=accuracy * width_bonus, round_bonus=accuracy * round_bonus,
                fork_bonus=accuracy * (width_bonus + round_bonus), bonus_scale=scale,
                bonus_schedule='constant_no_annealing', width_bonus_units=width_units,
                round_bonus_units=round_units, actual_generation_forward_calls=forwards,
                generated_tokens=total, critical_depth=depth, actual_rounds=len(widths),
                widths=widths, format_valid=valid, mode=mode, step=step)


def centered_advantages(rewards):
    """Within-prompt mean centering, without std division or whitening."""
    if not rewards or not all(math.isfinite(x) for x in rewards):
        raise ValueError('Require a nonempty group of finite rewards')
    mean = sum(rewards) / len(rewards)
    return [x - mean for x in rewards]
