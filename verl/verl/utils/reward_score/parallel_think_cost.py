"""Rewards for thinking-mode parallel RL (V0/V1/V2 agreed in the reward debate, 2026-10-08).

c = 1 only for a correct final answer after the closing </think>, outside every branch, in a trajectory
the rollout did not end early (protocol=plan_v1: an invalid, unfinished or over-budget plan gives c = 0).
V0 = 2c - 1
V1 = 2c - 1 - c * (alpha * D / 16384 + beta * T / 16384)   (low: .10/.05, high: .50/.25)
V2 = 2c - 1 - c * (alpha * g(D / s_D) + beta * g(T / s_T)),  g(x) = x / (1 + x), alpha=.10, beta=.05
D is the critical depth and T the total count of sampled tokens; tags the runtime inserted
count in neither. s_D, s_T are frozen per task or task bucket from the SFT checkpoint's correct
answers on train calibration questions (experiments/qwen06/calibrate_cost_scales.py).
"""
import json
import re
from functools import lru_cache

from .math_dapo import last_boxed_only_string, normalize_final_answer, remove_boxed

LENGTH_SCALE = 16384
WEIGHTS = {'think_v0': None, 'think_v1_low': (0.10, 0.05), 'think_v1_high': (0.50, 0.25), 'think_v2': (0.10, 0.05)}
THINK_CLOSE = '</think>'
SPECIAL = re.compile(r'<\|[^|]*\|>')
BLOCK = re.compile(r'<Parallel>.*?(</Parallel>|$)', re.S)


def answer_region(text):
    """Text after the last </think> with branches removed; None if thinking never closed in the main chain."""
    end = text.rfind(THINK_CLOSE)
    if end < 0:
        return None
    before = text[:end]
    if before.count('<Parallel>') != before.count('</Parallel>'):
        return None  # </think> was written inside a branch
    return BLOCK.sub('', SPECIAL.sub('', text[end + len(THINK_CLOSE):]))


def extract_answer(region):
    boxed = last_boxed_only_string(region)
    if boxed is not None:
        return remove_boxed(boxed)
    match = re.findall(r'(?i)Final Answer\s*:\s*([^\n]+)', region)
    return match[-1] if match else None


@lru_cache(maxsize=4)
def load_scales(path):
    with open(path) as f:
        return json.load(f)


def cost_scales(path, bucket, task):
    """s_D, s_T for a task: its own median when calibration had enough correct answers, else its bucket's."""
    scales = load_scales(path)
    entry = scales.get('tasks', {}).get(task) or scales.get('buckets', {}).get(bucket) or scales.get('default')
    if entry is None:
        raise KeyError(f'No cost scale for task {task!r} or bucket {bucket!r} in {path}')
    return entry['D'], entry['T']


def compute_score(text, ground_truth, data_source, extra_info):
    method = extra_info['reward_method']
    if method not in WEIGHTS:
        raise ValueError(f'Unknown reward_method {method!r}; use one of {sorted(WEIGHTS)}')
    region = answer_region(text)
    pred = extract_answer(region) if region is not None else None
    ended = extra_info.get('trajectory_status', 'ok') != 'ok'
    correct = (not ended and pred is not None
               and normalize_final_answer(pred) == normalize_final_answer(str(ground_truth)))
    depth, tokens = extra_info.get('critical_depth'), extra_info.get('sampled_tokens')
    cost = 0.0
    if WEIGHTS[method] is not None:
        if depth is None or tokens is None:
            raise ValueError(f'{method} needs critical_depth and sampled_tokens from the rollout')
        alpha, beta = WEIGHTS[method]
        if method == 'think_v2':
            scale_d, scale_t = cost_scales(extra_info['cost_scales'], data_source, str(extra_info.get('index', '')))
            depth_term, token_term = depth / scale_d, tokens / scale_t
            cost = alpha * depth_term / (1 + depth_term) + beta * token_term / (1 + token_term)
        else:
            cost = alpha * depth / LENGTH_SCALE + beta * tokens / LENGTH_SCALE
    c = float(correct)
    return dict(score=2 * c - 1 - c * cost, acc=c, cost=cost, formatted=float(region is not None),
                plan_failed=float(ended),
                critical_depth=-1 if depth is None else int(depth), sampled_tokens=-1 if tokens is None else int(tokens),
                pred='' if pred is None else pred, bucket=str(data_source), task=str(extra_info.get('index', '')))
