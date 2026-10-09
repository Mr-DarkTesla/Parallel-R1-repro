import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from omegaconf import OmegaConf

from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3 as Loop
from verl.parallel_thinking_generation_v3.repro_trace import TOKENS
from verl.utils.reward_score import math_dapo_acc_parallel_interved as reward


class Tokenizer:
    eos_token_id = 0
    def encode(self, text, **kwargs):
        return [TOKENS.index(text) + 10] if text in TOKENS else [1]
    def apply_chat_template(self, *args, **kwargs):
        return [1, 2, 3]
    def decode(self, ids, **kwargs):
        return ''.join(TOKENS[i-10] if 10 <= i < 16 else str(i) for i in ids)


class Server:
    def __init__(self, empty=False): self.main = 0; self.empty = empty
    async def generate(self, request_id, prompt_ids, sampling_params, **kwargs):
        stop = sampling_params['stop_token_ids'][0]
        if stop == 10:
            self.main += 1
            return [5, 10] if self.main == 1 else [6, 0]
        if stop == 13:
            return [] if self.empty else [7, 8, 13]
        return [] if self.empty else [9, 15]


@pytest.mark.parametrize('empty', [False, True])
def test_fork_merge_masks_and_trace(tmp_path, monkeypatch, empty):
    monkeypatch.setenv('PARALLEL_R1_TRACE_DIR', str(tmp_path))
    Loop._class_initialized = False
    config = OmegaConf.create({'actor_rollout_ref': {'rollout': {
        'prompt_length': 8, 'response_length': 64, 'agent': {'add_diverse_prefix': False,
        'max_iterations_for_parallel_thinking': 4, 'num_paths': 2, 'max_path_response_length': 16}}}})
    async def run():
        loop = Loop(SimpleNamespace(config=config), Server(empty), Tokenizer())
        loop.trajectory = {'step': 9, 'sample_index': 1, 'rollout_n': 0, 'validate': False}
        return await loop.run([], {})
    result = asyncio.run(run())
    assert result.response_ids[-1] == 0
    assert len(result.multiverse_pos_ids) == 72
    assert len(result.position_required_mask) == 2
    _, start1, end1, start2, end2 = result.position_required_mask[0]
    assert result.multiverse_pos_ids[start1] == result.multiverse_pos_ids[start2]
    assert end1 <= start2
    trace = json.loads(next(tmp_path.glob('traces-*.jsonl')).read_text())
    assert trace['executed_fork_count'] == 1
    assert trace['generation_calls'] == 5
    assert trace['parallel_relative_positions'] == [1 / len(result.response_ids)]
    assert sorted(call['phase'] for call in trace['calls']) == ['main', 'main', 'path', 'path', 'summary']


def test_reward_schedule():
    valid = '<Parallel><Path>A</Path><Path>B</Path></Parallel><Summary>C</Summary>Final Answer: 2'
    seq = 'Final Answer: 2'
    for step in range(1, 21):
        par = reward.compute_score(seq, valid, '2', step)
        expected = 1.2 if (step-1) % 10 >= 8 else 1.0
        assert par['score'] == expected
        assert reward.compute_score(seq, seq, '2', step)['score'] == 1.0
        assert reward.compute_score('Final Answer: 3', valid, '2', step)['score'] == -1.0
