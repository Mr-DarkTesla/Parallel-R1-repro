"""Bounded, correctness-gated rewards for the isolated Base RL campaign.

All counts must come from executed policy calls, never textual tag counts.
Depth and tokens are recorded. Cost uses instrumented generation forwards.
"""
import math


def _count(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be a nonnegative integer count')
    if not math.isfinite(value) or value < 0 or int(value) != value:
        raise ValueError(f'{name} must be a nonnegative integer count')
    return int(value)


def bonus_coefficient(step, warmup=32, anneal_end=64):
    """Keep the exploratory bonus for 32 updates, then remove it by update 64."""
    step = _count('step', step)
    if not 0 <= warmup < anneal_end:
        raise ValueError('Require 0 <= warmup < anneal_end')
    return max(0., min(1., (anneal_end - step) / (anneal_end - warmup)))


def score(correct, valid, depth, total, widths, step=0, mode='strong_width', *, forward_calls=None):
    """Wrong answers have zero reward; correct ones always score at least .6.

Width credit saturates at four paths and round credit at four completed
rounds. Independent recomputation is allowed. No depth penalty is applied.
"""
    if type(correct) is not bool or type(valid) is not bool:
        raise ValueError('correct and valid must be explicit booleans')
    if mode not in ('token_only', 'forward_only', 'strong_width', 'bucketed_width'):
        raise ValueError(f'Unknown reward mode: {mode}')
    depth = _count('depth', depth)
    total = _count('total', total)
    step = _count('step', step)
    if not 0 < depth <= total:
        raise ValueError('Require 0 < logical depth <= total sampled tokens')
    widths = [_count('width', value) for value in widths]
    if any(not 2 <= value <= 8 for value in widths):
        raise ValueError('Executed fork widths must be in [2, 8]')
    forward_penalty = 0.
    token_penalty = 0.
    if mode in ('forward_only', 'strong_width'):
        if forward_calls is None:
            raise ValueError('Instrumented generation forward_calls required')
        forward_calls = _count('forward_calls', forward_calls)
        if not 0 < forward_calls <= total:
            raise ValueError('Require 0 < generation forwards <= sampled tokens')
        forward_penalty = min(.4, .02 * (forward_calls // 200))
    else:
        token_penalty = min(.4, .025 * (total // 250)) if mode == 'bucketed_width' else min(.4, 1e-4 * total)
    width_units = sum(min(width - 1, 3) / 3 for width in widths) / len(widths) if valid and widths else 0.
    round_units = min(4, len(widths)) if valid else 0
    scale = bonus_coefficient(step) if mode not in ('token_only', 'forward_only') else 0.
    width_bonus = scale * .3 * width_units
    round_bonus = scale * .05 * round_units
    bonus = width_bonus + round_bonus
    accuracy = float(correct)
    auxiliary = accuracy * (-token_penalty - forward_penalty + bonus)
    return dict(score=accuracy + auxiliary, accuracy_reward=accuracy,
                aux_reward=auxiliary, depth_penalty=0.,
                token_penalty=accuracy * token_penalty, fork_bonus=accuracy * bonus,
                forward_penalty=accuracy * forward_penalty,
                actual_generation_forward_calls=forward_calls,
                width_bonus=accuracy * width_bonus, round_bonus=accuracy * round_bonus,
                bonus_scale=scale, width_bonus_units=width_units,
                round_bonus_units=round_units,
                critical_depth=depth, generated_tokens=total, actual_rounds=len(widths),
                widths=widths, format_valid=valid, mode=mode)


def centered_advantages(rewards):
    """One prompt group; no standard-deviation or subsequent whitening."""
    if not rewards or not all(math.isfinite(value) for value in rewards):
        raise ValueError('Require a nonempty group of finite rewards')
    mean = sum(rewards) / len(rewards)
    return [value - mean for value in rewards]
