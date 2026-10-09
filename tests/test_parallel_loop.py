"""CPU checks of the real loop with a fake generation server (no Ray/vLLM).

python -m unittest discover -s tests -p test_parallel_loop.py
"""
import ast
import asyncio
import copy
import importlib.util
import json
import os
from pathlib import Path
import random
import tempfile
from types import SimpleNamespace
from typing import Any
import unittest
from unittest.mock import patch
from uuid import uuid4

import torch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'verl/verl/parallel_thinking_generation_v3'
spec = importlib.util.spec_from_file_location('repro_trace', SOURCE / 'repro_trace.py')
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)
TOKENS = trace.TOKENS
spec = importlib.util.spec_from_file_location('logprob_gap', SOURCE / 'logprob_gap.py')
gap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gap)

# Load the unchanged class body; replace only infrastructure decorators/base/output.
tree = ast.parse((SOURCE / 'parallel_thinking_loop_v3.py').read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'ParallelThinkingAgentLoopV3')
cls.decorator_list = []
for node in cls.body:
    if isinstance(node, ast.AsyncFunctionDef):
        node.decorator_list = []
ns = dict(torch=torch, asyncio=asyncio, copy=copy, random=random, Any=Any, uuid4=uuid4,
          AgentLoopBase=object, AgentLoopOutput=lambda **kw: SimpleNamespace(**kw), Trace=trace.Trace, TOKENS=TOKENS,
          **{name: getattr(gap, name) for name in ('MAIN_BEFORE', 'MAIN_AFTER', 'PATH_FIRST', 'PATH_LATER',
                                                   'SUMMARY_FIRST', 'SUMMARY_LATER')})
exec(compile(ast.Module(body=[cls], type_ignores=[]), str(SOURCE), 'exec'), ns)
Loop = ns['ParallelThinkingAgentLoopV3']


class Tokenizer:
    eos_token_id = 0
    def encode(self, text, **kwargs):
        return [10 + TOKENS.index(text)] if text in TOKENS else [1]
    def apply_chat_template(self, *args, **kwargs):
        return [1, 2, 3]
    def decode(self, ids, **kwargs):
        return ''.join(TOKENS[i - 10] if 10 <= i < 16 else str(i) for i in ids)


class Server:
    def __init__(self, mode):
        self.mode, self.calls, self.main = mode, [], 0
    async def generate(self, **kw):
        self.calls.append(kw)
        params = kw['sampling_params']
        budget = params['max_tokens']
        assert budget >= 0
        if budget == 0 or self.mode == 'empty':
            return []
        stop = params['stop_token_ids'][0]
        if stop == 10:
            self.main += 1
            return [10] if self.main == 1 else [0]
        if self.mode == 'long':
            return [42] * budget
        return [stop]


class LoopTests(unittest.TestCase):
    def test_budgets_and_real_fork_telemetry(self):
        async def run(limit, paths, mode):
            config = SimpleNamespace(actor_rollout_ref=SimpleNamespace(rollout=SimpleNamespace(
                prompt_length=8, response_length=limit, agent=SimpleNamespace(
                    add_diverse_prefix=False, max_iterations_for_parallel_thinking=4,
                    num_paths=paths, max_path_response_length=4096))))
            Loop._class_initialized = False
            Loop.init_class(config, Tokenizer())
            loop = Loop()
            loop.loop = asyncio.get_running_loop()
            loop.server_manager = Server(mode)
            result = await loop.run([], {})
            self.assertLessEqual(len(result.response_ids), limit)
            self.assertEqual(len(result.response_ids), len(result.response_mask))
            self.assertEqual(len(result.multiverse_pos_ids), 8 + limit)
            expected_forks = int(mode != 'empty' and limit - 1 >= 2 * paths + 4)
            self.assertEqual(result.repro_stats['forks'], expected_forks)
            self.assertEqual(result.repro_stats['generation_calls'], len(loop.server_manager.calls))
            self.assertFalse(result.repro_stats['truncated'])
            if expected_forks:
                self.assertIn(15, result.response_ids)  # Summary always closes.
                self.assertEqual(len(result.position_required_mask), paths * (paths - 1))
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'PARALLEL_R1_TRACE_DIR': tmp}):
            for limit in (1, 7, 8, 9, 20, 100, 3000):
                for paths in (1, 2, 3):
                    for mode in ('empty', 'normal', 'long'):
                        with self.subTest(limit=limit, paths=paths, mode=mode):
                            asyncio.run(run(limit, paths, mode))
            records = [json.loads(line) for p in Path(tmp).glob('traces-*.jsonl') for line in p.read_text().splitlines()]
            self.assertEqual(len(records), 63)


if __name__ == '__main__':
    unittest.main()
