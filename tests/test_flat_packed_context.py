"""The flat_packed actor must score each sampled token exactly as the vLLM call that produced it.

A fake server answers the real rollout loop with scripted tokens and reports their
log-probs under a tiny Qwen3 in each call's own causal context, as vLLM does. The
real actor forward must reproduce those log-probs (and their gradients) for every
sampled token, across two parallel blocks, three paths, left padding, a path that
ends with EOS and a path cut at its length budget. The upstream tree objective is
checked to match only before the first summary.

python -m unittest tests.test_flat_packed_context
"""
import ast
import asyncio
import contextlib
import copy
import importlib.util
from pathlib import Path
import random
from types import SimpleNamespace
from typing import Any
import unittest
from unittest.mock import patch
from uuid import uuid4

import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'verl/verl/parallel_thinking_generation_v3'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trace = load(SOURCE / 'repro_trace.py', 'repro_trace')
gap = load(SOURCE / 'logprob_gap.py', 'logprob_gap')
replay = load(ROOT / 'verl/verl/workers/actor/replay_context.py', 'replay_context')
TOKENS = trace.TOKENS
PARALLEL, END_PARALLEL, PATH, END_PATH, SUMMARY, END_SUMMARY = range(10, 16)
EOS, NEWLINE = 0, 1


def compiled(path, class_name, method=None):
    tree = ast.parse(path.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)
    if method:
        node = next(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == method)
    else:
        node.decorator_list = []
        for item in node.body:
            if isinstance(item, ast.AsyncFunctionDef):
                item.decorator_list = []
    return compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec')


ns = dict(torch=torch, asyncio=asyncio, copy=copy, random=random, Any=Any, uuid4=uuid4, AgentLoopBase=object,
          AgentLoopOutput=lambda **kw: SimpleNamespace(**kw), Trace=trace.Trace, TOKENS=TOKENS,
          **{name: getattr(gap, name) for name in ('MAIN_BEFORE', 'MAIN_AFTER', 'PATH_FIRST', 'PATH_LATER',
                                                   'SUMMARY_FIRST', 'SUMMARY_LATER')})
exec(compiled(SOURCE / 'parallel_thinking_loop_v3.py', 'ParallelThinkingAgentLoopV3'), ns)
Loop = ns['ParallelThinkingAgentLoopV3']


def logprobs_from_logits(logits, labels, inplace_backward=True):
    return logits.log_softmax(-1).gather(-1, labels[..., None]).squeeze(-1)


actor_ns = dict(torch=torch, logprobs_from_logits=logprobs_from_logits,
                append_replay_segments=replay.append_replay_segments,
                verl_F=SimpleNamespace(entropy_from_logits=lambda x: -(x.softmax(-1) * x.log_softmax(-1)).sum(-1)))
exec(compiled(ROOT / 'verl/verl/workers/actor/dp_actor.py', 'DataParallelPPOActor', '_forward_micro_batch'), actor_ns)
forward_micro_batch = actor_ns['_forward_micro_batch']


class Tokenizer:
    eos_token_id = EOS
    def __init__(self, prompt):
        self.prompt = prompt
    def encode(self, text, **kwargs):
        return [10 + TOKENS.index(text)] if text in TOKENS else [NEWLINE]
    def apply_chat_template(self, *args, **kwargs):
        return list(self.prompt)
    def decode(self, ids, **kwargs):
        return ' '.join(map(str, ids))


class Server:
    """Scripted tokens; log-probs from the model in each call's causal context (like vLLM)."""
    def __init__(self, model, script):
        self.model, self.script, self.calls = model, script, []

    async def generate(self, request_id, prompt_ids, sampling_params, routing_key=None, return_logprobs=False):
        kind = {PARALLEL: 'main', END_PATH: 'path', END_SUMMARY: 'summary'}[sampling_params['stop_token_ids'][0]]
        ids = self.script[kind].pop(0)[:sampling_params['max_tokens']]
        self.calls.append(dict(kind=kind, routing_key=routing_key, prompt=list(prompt_ids), ids=list(ids)))
        with torch.no_grad():
            logits = self.model(torch.tensor([prompt_ids + ids])).logits[0, len(prompt_ids) - 1:-1]
        log_probs = logprobs_from_logits(logits, torch.tensor(ids)).tolist()
        return dict(token_ids=list(ids), logprobs=log_probs) if return_logprobs else list(ids)


def script(rng):
    text = lambda n: torch.randint(20, 40, (n,), generator=rng).tolist()
    return dict(
        # Block 1: path 2 ends with EOS (runtime writes </Path>), path 3 hits its budget.
        main=[text(4) + [PARALLEL], text(3) + [PARALLEL], text(5) + [EOS]],
        path=[text(3) + [END_PATH], text(5) + [EOS], text(30),
              text(2) + [END_PATH], text(4) + [END_PATH], text(3) + [END_PATH]],
        summary=[text(3) + [END_SUMMARY], text(2) + [EOS]])


class FlatPackedContextTest(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        torch.manual_seed(3)
        config = Qwen3Config(vocab_size=40, hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                             num_attention_heads=4, num_key_value_heads=2, head_dim=8)
        config._attn_implementation = 'sdpa'
        self.model = Qwen3ForCausalLM(config).eval()
        # The actor builds a bf16 mask under autocast; this test runs in float32.
        self.model.register_forward_pre_hook(
            lambda module, args, kwargs: (args, {**kwargs, 'attention_mask': kwargs['attention_mask'].float()})
            if kwargs.get('attention_mask') is not None else None,
            with_kwargs=True)

    def rollout(self, context, prompt, seed):
        prompt_length, response_length = 8, 96
        config = SimpleNamespace(actor_rollout_ref=SimpleNamespace(rollout=SimpleNamespace(
            prompt_length=prompt_length, response_length=response_length, agent=SimpleNamespace(
                add_diverse_prefix=False, max_iterations_for_parallel_thinking=4, num_paths=3,
                max_path_response_length=8, logprob_context=context, rollout_logprobs=True))))
        Loop._class_initialized = False
        Loop.init_class(config, Tokenizer(prompt))
        loop = Loop()
        loop.server_manager = Server(self.model, script(torch.Generator().manual_seed(seed)))

        async def run():
            loop.loop = asyncio.get_running_loop()
            return await loop.run([], dict(temperature=1.0, top_p=1.0))
        result = asyncio.run(run())
        self.assertEqual({call['routing_key'] for call in loop.server_manager.calls}, {loop.routing_key})
        calls = loop.server_manager.calls
        self.assertEqual([call['kind'] for call in calls],
                         ['main'] + ['path'] * 3 + ['summary', 'main'] + ['path'] * 3 + ['summary', 'main'])
        # Response index of each call's first generated token. Paths 2-3 of a block follow their
        # siblings in the response; flat_packed's replay segments record where (<Path> at start).
        later_paths = iter(start + 1 for start, _, _ in (getattr(result, 'replay_segments', None) or []))
        previous = None
        for call in calls:
            first_path = call['kind'] == 'path' and previous != 'path'
            if call['kind'] != 'path' or first_path:
                call['start'] = len(call['prompt']) - len(prompt)
            elif context == 'flat_packed':
                call['start'] = next(later_paths)
            previous = call['kind']
        result.calls = calls
        return result, prompt_length, response_length

    def batch(self, context):
        """Two trajectories assembled like AgentLoopWorker._postprocess (left/right padding)."""
        outputs = [self.rollout(context, [3, 4, 5], 0), self.rollout(context, [3, 4, 5, 6, 7, 8], 1)]
        prompt_length, response_length = outputs[0][1:]
        rows = []
        for result, *_ in outputs:
            left = prompt_length - len(result.prompt_ids)
            ids = [EOS] * left + result.prompt_ids + result.response_ids
            ids += [EOS] * (prompt_length + response_length - len(ids))
            mask = [0] * left + [1] * (len(result.prompt_ids) + len(result.response_ids))
            mask += [0] * (prompt_length + response_length - len(mask))
            pad = response_length - len(result.response_ids)
            rows.append(dict(ids=ids, mask=mask, left=left, result=result,
                             response_mask=result.response_mask + [0] * pad,
                             segments=result.rollout_segments + [-1] * pad,
                             rollout=result.rollout_log_probs + [0.0] * pad))
        ids = torch.tensor([row['ids'] for row in rows])
        batch = dict(input_ids=ids, responses=ids[:, prompt_length:], attention_mask=torch.tensor([r['mask'] for r in rows]),
                     position_ids=torch.stack([r['result'].multiverse_pos_ids for r in rows]),
                     left_pad_lens=[r['left'] for r in rows],
                     position_required_masks=[[list(m) for m in r['result'].position_required_mask] for r in rows])
        if context == 'flat_packed':
            batch['replay_segments'] = [r['result'].replay_segments for r in rows]
            batch['label_overrides'] = [r['result'].label_overrides for r in rows]
        info = dict(response_mask=torch.tensor([r['response_mask'] for r in rows]),
                    segments=torch.tensor([r['segments'] for r in rows]),
                    rollout=torch.tensor([r['rollout'] for r in rows]), calls=[r['result'].calls for r in rows])
        return batch, info

    def actor_log_probs(self, batch, trim):
        actor = SimpleNamespace(config=SimpleNamespace(entropy_checkpointing=False, get=lambda key, default=None: trim),
                                actor_module=self.model, device_name='cpu', use_remove_padding=False,
                                use_fused_kernels=False)
        with patch.object(torch, 'autocast', lambda **kw: contextlib.nullcontext()):
            entropy, log_probs = forward_micro_batch(actor, batch, 1.0, True)
        self.assertTrue(torch.isfinite(entropy).all())
        return log_probs

    def test_flat_packed_matches_every_rollout_call(self):
        batch, info = self.batch('flat_packed')
        sampled = info['segments'] >= 0
        # Injected tags (and only they) are out of the loss.
        torch.testing.assert_close(info['response_mask'].bool(), sampled)
        self.assertEqual([len(x) for x in batch['label_overrides']], [2, 2])  # EOS in a path and in a summary
        self.assertEqual([len(x) for x in batch['replay_segments']], [4, 4])  # paths 2-3 of both blocks
        for trim in (False, True):
            with self.subTest(trim=trim):
                actual = self.actor_log_probs(batch, trim)
                torch.testing.assert_close(actual[sampled], info['rollout'][sampled], atol=2e-6, rtol=1e-5)
        metrics = gap.gap_metrics(info['rollout'], actual.detach(), info['segments'])
        self.assertLess(metrics['rollout_gap/all_abs_max'], 2e-6)
        self.assertEqual(metrics['rollout_gap/path_later_tokens'], 2 * (3 + 5 + 4))

    def test_flat_packed_gradients_match_independent_calls(self):
        batch, info = self.batch('flat_packed')
        sampled = info['segments'] >= 0
        weights = torch.randn(sampled.shape)
        self.model.zero_grad(set_to_none=True)
        actual = self.actor_log_probs(batch, True)
        (actual * weights)[sampled].sum().backward()
        packed = torch.cat([p.grad.flatten() for p in self.model.parameters()])

        # Reference: one causal forward per recorded call, as in the reverted call replay (2ae4b8b).
        self.model.zero_grad(set_to_none=True)
        loss = 0
        for row, calls in enumerate(info['calls']):
            for call in calls:
                logits = self.model(torch.tensor([call['prompt'] + call['ids']])).logits[0, len(call['prompt']) - 1:-1]
                scores = logprobs_from_logits(logits, torch.tensor(call['ids']))
                slots = torch.arange(call['start'], call['start'] + len(call['ids']))
                keep = sampled[row, slots]
                loss = loss + (scores * weights[row, slots])[keep].sum()
        loss.backward()
        reference = torch.cat([p.grad.flatten() for p in self.model.parameters()])
        torch.testing.assert_close(packed, reference, atol=1e-6, rtol=1e-4)

    def test_tree_objective_differs_after_the_first_summary(self):
        batch, info = self.batch('tree')
        actual = self.actor_log_probs(batch, True).detach()
        # Where the runtime replaced a sampled EOS by a closing tag, tree scores the tag, not the
        # sampled action: a real mismatch even inside block-1 paths. Same script -> same slots.
        segments = info['segments'].clone()
        for row, overrides in enumerate(self.batch('flat_packed')[0]['label_overrides']):
            for index, token in overrides:
                self.assertGreater((actual[row, index] - info['rollout'][row, index]).abs().item(), 1e-3)
                segments[row, index] = -1
        metrics = gap.gap_metrics(info['rollout'], actual, segments)
        for name in ('main_before_fork', 'path_block1'):
            self.assertLess(metrics[f'rollout_gap/{name}_abs_max'], 2e-6, name)
        for name in ('summary_block1', 'path_later', 'summary_later', 'main_after_fork'):
            self.assertGreater(metrics[f'rollout_gap/{name}_abs_max'], 1e-3, name)


if __name__ == '__main__':
    unittest.main()
