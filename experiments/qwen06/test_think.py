"""Thinking-mode RL: rewards V0/V1/V2, D/T accounting, sequential baseline, scale calibration."""
import asyncio
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch
from omegaconf import OmegaConf

from test_repro import Loop, Server, Tokenizer
from verl import DataProto
from verl.utils.reward_score import default_compute_score
from verl.workers.reward_manager.naive import NaiveRewardManager

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('calibrate_cost_scales', HERE / 'calibrate_cost_scales.py')
calibrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calibrate)


def score(text, method='think_v0', truth='34', **info):
    return default_compute_score('math_dapo', '', text, truth, dict(reward_method=method, **info))


@pytest.mark.parametrize('text, correct', [
    ('<think>a\nb</think>\n\nSo \\boxed{34}.<|im_end|>', True),
    ('<think>a</think>\n\nFinal Answer: 34<|im_end|>', True),
    ('<think>a</think>\n\n\\boxed{35}<|im_end|>', False),
    ('<think>a\\boxed{34}', False),  # thinking never closed (truncated)
    ('<think>a<Parallel><Path>b</think>\\boxed{34}</Path></Parallel>', False),  # </think> inside a branch
    ('<think>a</think><Parallel><Path>\\boxed{34}</Path></Parallel><|im_end|>', False),  # answer only in a branch
    ('<think>a<Parallel><Path>\\boxed{1}</Path><Path>c</Path></Parallel><Summary>s</Summary></think>\\boxed{34}', True),
])
def test_correctness_reads_only_the_final_answer_outside_branches(text, correct):
    result = score(text)
    assert result['acc'] == float(correct)
    assert result['score'] == (1.0 if correct else -1.0)


def test_v1_costs_scale_with_depth_and_tokens_for_correct_answers_only():
    right, wrong = '<think>a</think>\\boxed{34}', '<think>a</think>\\boxed{1}'
    low = score(right, 'think_v1_low', critical_depth=8192, sampled_tokens=16384)
    high = score(right, 'think_v1_high', critical_depth=8192, sampled_tokens=16384)
    assert low['score'] == pytest.approx(1 - (0.10 * 0.5 + 0.05 * 1.0))
    assert high['score'] == pytest.approx(1 - (0.50 * 0.5 + 0.25 * 1.0))
    assert score(wrong, 'think_v1_high', critical_depth=8192, sampled_tokens=16384)['score'] == -1.0
    with pytest.raises(ValueError):
        score(right, 'think_v1_low')  # no D/T from the rollout
    with pytest.raises(ValueError):
        score(right, 'think_v3', critical_depth=1, sampled_tokens=1)


def test_v2_uses_task_scale_then_bucket_scale(tmp_path):
    path = tmp_path / 'scales.json'
    path.write_text(json.dumps(dict(tasks={'q1': dict(D=100, T=400)}, buckets={'math_dapo': dict(D=200, T=200)})))
    right = '<think>a</think>\\boxed{34}'
    task = score(right, 'think_v2', critical_depth=100, sampled_tokens=400, cost_scales=str(path), index='q1')
    bucket = score(right, 'think_v2', critical_depth=600, sampled_tokens=200, cost_scales=str(path), index='q2')
    assert task['cost'] == pytest.approx(0.10 * 0.5 + 0.05 * 0.5)
    assert bucket['cost'] == pytest.approx(0.10 * 0.75 + 0.05 * 0.5)


def run_loop(server, **agent):
    Loop._class_initialized = False
    config = OmegaConf.create({'actor_rollout_ref': {'rollout': {
        'prompt_length': 8, 'response_length': 64, 'agent': {'add_diverse_prefix': False,
        'max_iterations_for_parallel_thinking': 2, 'num_paths': 2, 'max_path_response_length': 16, **agent}}}})
    tokenizer = Tokenizer()
    templates = []
    tokenizer.apply_chat_template = lambda *args, **kwargs: templates.append(kwargs) or [1, 2, 3]

    async def run():
        loop = Loop(SimpleNamespace(config=config), server, tokenizer)
        loop.trajectory = {'step': 1, 'sample_index': 0, 'rollout_n': 0, 'validate': False}
        return await loop.run([], {})
    return asyncio.run(run()), templates


@pytest.mark.parametrize('empty, depth, tokens', [(False, 2 + 3 + 2 + 2, 2 + 6 + 2 + 2), (True, 2 + 2, 2 + 2)])
def test_depth_and_tokens_count_sampled_tokens_only(tmp_path, monkeypatch, empty, depth, tokens):
    # main "5 <Parallel>", two paths "7 8 </Path>", summary "9 </Summary>", main "6 EOS";
    # <Path>, </Parallel>, newline and <Summary> (and empty generations' closing tags) are inserted.
    monkeypatch.setenv('PARALLEL_R1_TRACE_DIR', str(tmp_path))
    result, templates = run_loop(Server(empty), enable_thinking=True)
    assert result.repro_stats['critical_depth'] == depth
    assert result.repro_stats['sampled_tokens'] == tokens
    assert templates[0]['enable_thinking'] is True


class SequentialServer:
    def __init__(self):
        self.params = []

    async def generate(self, request_id, prompt_ids, sampling_params, **kwargs):
        self.params.append(sampling_params)
        return [5, 10] if len(self.params) == 1 else [6, 0]  # <Parallel> could only end a call at max_tokens


def test_sequential_baseline_never_forks(tmp_path, monkeypatch):
    monkeypatch.setenv('PARALLEL_R1_TRACE_DIR', str(tmp_path))
    server = SequentialServer()
    result, templates = run_loop(server, allow_parallel=False)
    assert len(server.params) == 1
    assert server.params[0]['stop_token_ids'] == [0] and server.params[0]['logit_bias'] == {10: -100.0}
    assert result.repro_stats['forks'] == 0 and result.repro_stats['critical_depth'] == 2
    assert 'enable_thinking' not in templates[0]


def test_reward_manager_passes_rollout_depth_and_configured_method():
    class Decoder:
        def decode(self, ids, skip_special_tokens=True):
            return '<think>a</think>\\boxed{34}<|im_end|>'
    data = DataProto.from_dict(
        tensors=dict(prompts=torch.ones(2, 3, dtype=torch.long), responses=torch.ones(2, 4, dtype=torch.long),
                     attention_mask=torch.ones(2, 7, dtype=torch.long)),
        non_tensors=dict(data_source=np.array(['math_dapo'] * 2, dtype=object),
                         reward_model=np.array([{'ground_truth': '34'}] * 2, dtype=object),
                         extra_info=np.array([{'reward_method': 'accuracy_reward'}] * 2, dtype=object),
                         parallel_stats=np.array([{'critical_depth': 8192, 'sampled_tokens': 16384},
                                                  {'critical_depth': 0, 'sampled_tokens': 0}], dtype=object)),
        meta_info=dict(global_steps=1))
    manager = NaiveRewardManager(Decoder(), 0, reward_method='think_v1_low')
    result = manager(data, return_dict=True)
    assert result['reward_tensor'][:, -1].tolist() == pytest.approx([0.9, 1.0])
    assert result['reward_extra_info']['critical_depth'] == [8192, 0]
    assert data.non_tensor_batch['extra_info'][0] == {'reward_method': 'accuracy_reward'}  # rows untouched


def test_calibration_takes_medians_of_correct_answers():
    rows = [dict(acc=1, critical_depth=d, sampled_tokens=2 * d, bucket='gsm', task='a') for d in (10, 20, 30)]
    rows += [dict(acc=1, critical_depth=100, sampled_tokens=100, bucket='math', task='b'),
             dict(acc=0, critical_depth=999, sampled_tokens=999, bucket='math', task='b')]
    result = calibrate.scales(rows, min_correct=3)
    assert result['buckets']['gsm'] == dict(D=20, T=40, correct=3)
    assert result['buckets']['math'] == dict(D=100, T=100, correct=1)
    assert set(result['tasks']) == {'a'}
    assert result['correct'] == 4
