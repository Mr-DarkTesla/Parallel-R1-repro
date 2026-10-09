"""Graph rollout on vLLM 0.8.5's own V1 scheduler (vllm_graph.GraphScheduler) with a simulated model.

The simulated model writes into each KV slot a fingerprint of (token, RoPE position, fingerprints of every slot the
token attends to), so a fingerprint pins down the whole context a token was computed in. Each sampled token records
the fingerprint of the query that produced it. The real agent loop runs in graph mode against this engine, several
trajectories at once, with prefix caching, chunked prefill and (in one test) preemption. For every request, each
sampled token's query fingerprint must equal the one computed from the contract's graph positions and mask over
that request's tokens: vLLM sampled every token in its graph context. The worker side here mirrors
GraphModelRunner (copies before the forward pass, offsets via position_offsets); the CUDA model runner itself is
checked by experiments/qwen06/check_graph_rollout.py on a GPU.

Needs vLLM 0.8.5 importable (skipped otherwise): python -m pytest tests/test_vllm_graph.py
"""
import asyncio
import importlib.util
import itertools
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch

try:
    from vllm.platforms import current_platform
    current_platform.is_async_output_supported = lambda *args, **kwargs: False  # CPU-only test machine
    from vllm.config import CacheConfig, ModelConfig, SchedulerConfig, VllmConfig
    from vllm.sampling_params import SamplingParams
    from vllm.v1.kv_cache_interface import FullAttentionSpec, KVCacheConfig, KVCacheGroupSpec
    from vllm.v1.outputs import ModelRunnerOutput
    from vllm.v1.request import Request, RequestStatus
    from vllm.v1.structured_output import StructuredOutputManager
    try:
        import vllm.v1.worker.gpu_worker  # noqa: F401
    except ImportError:  # no CUDA driver: GraphWorker is only defined here, never run
        sys.modules['vllm.v1.worker.gpu_worker'] = SimpleNamespace(Worker=object)
    from verl.parallel_thinking_generation_v3 import vllm_graph
except ImportError as error:  # pragma: no cover
    raise unittest.SkipTest(f'vLLM not importable: {error}')

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
import test_flat_packed_context as base  # noqa: E402  (the real loop, its plan tokenizer and scripts)

contract, graph_kv = base.contract, base.graph_kv
PARALLEL, END_PARALLEL, PATH, END_PATH = base.PARALLEL, base.END_PARALLEL, base.PATH, base.END_PATH
EOS, WORDS = base.EOS, base.WORDS
JUNK = 39


def make_scheduler(num_blocks=400, block_size=4, max_batched=64, max_model_len=512):
    directory = tempfile.mkdtemp()
    from transformers import Qwen3Config
    Qwen3Config(vocab_size=64, hidden_size=32, intermediate_size=64, num_hidden_layers=2, num_attention_heads=4,
                num_key_value_heads=2, head_dim=8, max_position_embeddings=max_model_len,
                architectures=['Qwen3ForCausalLM']).save_pretrained(directory)
    model = ModelConfig(model=directory, task='generate', tokenizer=directory, tokenizer_mode='auto',
                        trust_remote_code=False, dtype='float32', seed=0, skip_tokenizer_init=True)
    scheduler = SchedulerConfig(max_num_seqs=32, max_num_batched_tokens=max_batched, max_model_len=max_model_len,
                                enable_chunked_prefill=True)
    cache = CacheConfig(block_size=block_size, gpu_memory_utilization=0.9, swap_space=0, cache_dtype='auto',
                        enable_prefix_caching=True)
    config = VllmConfig(scheduler_config=scheduler, model_config=model, cache_config=cache)
    cache.num_gpu_blocks = num_blocks
    kv = KVCacheConfig(num_blocks=num_blocks, tensors={}, kv_cache_groups=[
        KVCacheGroupSpec(['layer'], FullAttentionSpec(block_size, 1, 1, torch.float32, False))])
    return vllm_graph.GraphScheduler(vllm_config=config, kv_cache_config=kv, log_stats=False,
                                     structured_output_manager=StructuredOutputManager(config))


def fingerprint(token, position, visible):
    return hash((token, position, tuple(visible)))


class SimEngine:
    """EngineCore.step with the simulated model; generate/release as in AsyncvLLMServer (graph_kv.Registry)."""

    def __init__(self, scheduler, scripts=()):
        self.scheduler, self.registry = scheduler, graph_kv.Registry()
        self.kv, self.offsets, self.queries, self.outputs, self.done = {}, {}, {}, {}, {}
        self.scripts, self.script_of, self.views, self.preempted = list(scripts), {}, [], 0
        self.samplers, self.stop_reasons, self.resume, self.evicted = {}, {}, {}, 0

    def step(self):
        scheduler = self.scheduler
        if not scheduler.has_requests():  # EngineCore.step
            return False
        self.preempted += sum(request.status == RequestStatus.PREEMPTED for request in scheduler.waiting)
        out = scheduler.schedule()
        # Worker: GraphModelRunner._update_states, execute_model (copies), _prepare_inputs (offsets).
        for req_id in out.finished_req_ids:
            self.offsets.pop(req_id, None)
        for new in out.scheduled_new_reqs:
            spec = (new.sampling_params.extra_args or {}).get(graph_kv.GRAPH_KEY)
            if spec and spec['offset']:
                self.offsets[new.req_id] = spec['offset']
        copies = out.kv_connector_metadata
        if isinstance(copies, vllm_graph.GraphKVCopies):
            values = [self.kv[int(source)] for source in copies.src]
            for target, value in zip(copies.dst, values):
                self.kv[int(target)] = value
        req_ids = list(out.num_scheduled_tokens)
        offsets = vllm_graph.position_offsets(req_ids, out.num_scheduled_tokens, self.offsets)
        size = scheduler.kv_cache_manager.block_size
        sampled, cursor = [], 0
        for req_id in req_ids:
            request, count = scheduler.requests[req_id], out.num_scheduled_tokens[req_id]
            blocks = [block.block_id for block in scheduler.kv_cache_manager.req_to_blocks[req_id]]
            slot = lambda index: blocks[index // size] * size + index % size
            start = request.num_computed_tokens - count
            for index in range(start, start + count):
                position = index - (0 if offsets is None else int(offsets[cursor + index - start]))
                visible = [self.kv[slot(j)] for j in range(index)]
                self.kv[slot(index)] = fingerprint(request.all_token_ids[index], position, visible)
            cursor += count
            if start + count == request.num_tokens:  # prefill finished or decoding: sample
                self.queries.setdefault(req_id, []).append(self.kv[slot(start + count - 1)])
                sampled.append([self.samplers[req_id](len(request.output_token_ids))])
            else:
                sampled.append([])
        result = ModelRunnerOutput(req_ids=req_ids, req_id_to_index={r: i for i, r in enumerate(req_ids)},
                                   sampled_token_ids=sampled, spec_token_ids=None, logprobs=None,
                                   prompt_logprobs_dict={})
        outputs = scheduler.update_from_output(out, result).outputs
        for output in outputs:
            self.outputs.setdefault(output.request_id, []).extend(output.new_token_ids)
            if output.finish_reason is not None and output.request_id in self.done:
                self.stop_reasons[output.request_id] = output.stop_reason
                self.done.pop(output.request_id).set_result(None)
        return bool(out.total_num_scheduled_tokens or outputs)

    async def run(self):
        idle = 0
        while True:
            try:
                idle = 0 if self.step() else idle + 1
                assert idle < 10000 or not self.done, f'requests {list(self.done)} are never scheduled'
            except BaseException as error:  # fail the waiting rollouts instead of hanging them
                for future in self.done.values():
                    future.set_exception(error)
                raise
            await asyncio.sleep(0)

    def kind(self, params):
        stops = params.get('stop_token_ids') or []
        if stops:
            return base.PlanServer.KINDS[stops[0]]
        return 'count' if params.get('allowed_token_ids') else 'seal' if params['max_tokens'] == 1 else 'main'

    async def generate(self, request_id, prompt_ids, sampling_params, routing_key=None, return_logprobs=False,
                       graph=None):
        params = dict(sampling_params)
        kind = self.kind(params)
        max_tokens = min(params.pop('max_tokens'), self.scheduler.max_model_len - len(prompt_ids))
        if max_tokens <= 0:
            return dict(token_ids=[], logprobs=[]) if return_logprobs else []
        if routing_key not in self.script_of:
            self.script_of[routing_key] = self.scripts.pop(0)
        script = self.script_of[routing_key]
        # A request that continues an evicted one samples the rest of its tokens.
        tokens = self.resume.pop(tuple(prompt_ids), None)
        if tokens is None:
            tokens = [JUNK] if kind == 'seal' else script[kind].pop(0)
        self.samplers[request_id] = lambda k: tokens[k] if k < len(tokens) else 30 + k % 9
        if graph is not None:
            self.registry.validate(graph, len(prompt_ids))
            params['extra_args'] = {graph_kv.GRAPH_KEY: graph}
        params = {k: v for k, v in params.items() if k in ('stop_token_ids', 'logit_bias', 'allowed_token_ids',
                                                            'extra_args', 'n', 'temperature', 'top_p')}
        request = Request(request_id, list(prompt_ids), None, None, None, SamplingParams(max_tokens=max_tokens, **params),
                          EOS, time.time())
        self.done[request_id] = asyncio.get_running_loop().create_future()
        self.scheduler.add_request(request)
        await self.done[request_id]
        ids = self.outputs.pop(request_id, [])
        reason = self.stop_reasons.pop(request_id)
        if reason == graph_kv.GRAPH_TOO_LARGE:
            raise RuntimeError('graph rollout: a trajectory needs more KV than the cache has')
        evicted = reason == graph_kv.GRAPH_EVICTED
        if evicted:
            self.evicted += 1
            self.resume[tuple(prompt_ids) + tuple(ids)] = tokens[len(ids):]
        elif graph is not None:
            self.registry.finished(request_id, graph, len(prompt_ids), len(ids))
        self.views.append(dict(kind=kind, prompt=list(prompt_ids), ids=list(ids),
                               queries=self.queries.pop(request_id, [])))
        result = dict(token_ids=ids, logprobs=[0.0] * len(ids))
        return {**result, 'graph_evicted': evicted} if graph is not None else result if return_logprobs else ids

    async def release(self, request_ids, routing_key=None):
        held = self.registry.release(request_ids)
        if held:
            self.scheduler.finish_requests(held, RequestStatus.FINISHED_ABORTED)  # EngineCore.abort_requests


def spans_of(tokens):
    """Branch spans of the closed blocks in a token sequence (an open block is plain causal)."""
    spans, pending, block = [], [], 0
    for index, token in enumerate(tokens):
        if token == PARALLEL:
            pending = []
        elif token == PATH:
            pending.append([index, None])
        elif token == END_PATH and pending:
            pending[-1][1] = index + 1
        elif token == END_PARALLEL:
            spans += [contract.Span(s, e, block, number) for number, (s, e) in enumerate(pending, 1)]
            pending, block = [], block + 1
    return spans


def graph_fingerprints(tokens):
    spans = spans_of(tokens)
    positions = contract.graph_positions(len(tokens), spans)
    mask = contract.graph_attention_mask(len(tokens), spans)
    out = []
    for index, token in enumerate(tokens):
        out.append(fingerprint(token, positions[index], [out[j] for j in range(index) if mask[index, j]]))
    return out


def scripts(count, seed=0):
    out = []
    for number in range(count):
        script = base.plan_script(torch.Generator().manual_seed(seed + number))
        script['main'][0] = [30 + number % 3] + script['main'][0]  # a few distinct prompts' worth of prefixes
        out.append(script)
    return out


class GraphRolloutTest(unittest.TestCase):

    def rollout(self, engine, trajectories, prompt=(3, 4, 5, 6, 7)):
        config = SimpleNamespace(actor_rollout_ref=SimpleNamespace(rollout=SimpleNamespace(
            prompt_length=8, response_length=200, agent=SimpleNamespace(
                add_diverse_prefix=False, max_iterations_for_parallel_thinking=2, num_paths=2,
                max_path_response_length=8, logprob_context='tree', rollout_logprobs=False, protocol='plan',
                max_plan_tokens=32, allow_parallel=True, graph_rollout=True))))
        base.Loop._class_initialized = False
        base.Loop.init_class(config, base.PlanTokenizer(list(prompt)))

        async def main():
            runner = asyncio.create_task(engine.run())
            results = []
            for _ in range(trajectories):
                loop = base.Loop()
                loop.server_manager, loop.loop = engine, asyncio.get_running_loop()
                results.append(loop.run([], dict(temperature=1.0, top_p=1.0)))
            results = await asyncio.gather(*results)
            runner.cancel()
            return results
        return asyncio.run(main())

    def check(self, engine, results):
        kinds = [view['kind'] for view in engine.views]
        if not engine.evicted:  # rebuilding evicted KV adds one-token requests
            self.assertEqual(kinds.count('seal'), kinds.count('path'))
        self.assertGreater(kinds.count('summary'), 0)
        for view in engine.views:  # every sampled token in its graph context
            tokens = view['prompt'] + view['ids']
            reference = graph_fingerprints(tokens)
            expected = reference[len(view['prompt']) - 1:len(tokens) - 1]
            self.assertEqual(view['queries'], expected, view['kind'])
        for result in results:
            self.assertEqual(result.repro_stats['trajectory_status'], 'ok')
        scheduler = engine.scheduler
        self.assertEqual(scheduler.graph_held, {})
        self.assertEqual(scheduler.graph_users, {})
        self.assertEqual(scheduler.graph_evicted, set())
        self.assertEqual(engine.registry.held, {})
        self.assertFalse(any(scheduler.kv_cache_manager.req_to_blocks.values()))
        pool = scheduler.kv_cache_manager.block_pool
        self.assertEqual(pool.get_num_free_blocks(), pool.num_gpu_blocks - 1)  # all but the null block

    def test_every_token_is_sampled_in_its_graph_context(self):
        engine = SimEngine(make_scheduler(), scripts(6))
        results = self.rollout(engine, 6)
        self.check(engine, results)
        # The summary request computed only </Parallel><Summary>: the branches' KV was copied.
        summaries = [view for view in engine.views if view['kind'] == 'summary']
        self.assertTrue(all(view['prompt'][-2:] == [END_PARALLEL, base.SUMMARY] for view in summaries))

    def test_preempted_graph_requests_copy_again(self):
        engine = SimEngine(make_scheduler(num_blocks=48, max_batched=32), scripts(6, seed=7))
        results = self.rollout(engine, 6)
        self.assertGreater(engine.preempted, 0)
        self.check(engine, results)

    def test_graph_positions_match_the_actor(self):
        engine = SimEngine(make_scheduler(), scripts(1))
        result = self.rollout(engine, 1)[0]
        tokens = result.prompt_ids + result.response_ids
        positions = result.multiverse_pos_ids[8 - len(result.prompt_ids):][:len(tokens)]
        self.assertEqual(positions.tolist(), contract.graph_positions(len(tokens), spans_of(tokens)))


class SchedulerTest(unittest.TestCase):
    """Held blocks and deferred release on the real scheduler."""

    def add(self, scheduler, request_id, prompt, max_tokens, graph=None):
        extra = {graph_kv.GRAPH_KEY: graph} if graph else None
        scheduler.add_request(Request(request_id, prompt, None, None, None,
                                      SamplingParams(max_tokens=max_tokens, extra_args=extra), EOS, time.time()))

    def test_release_waits_for_requests_that_copy(self):
        scheduler = make_scheduler(num_blocks=64)
        engine = SimEngine(scheduler)
        engine.samplers = dict(a=lambda k: 30 + k, b=lambda k: 40 + k)
        self.add(scheduler, 'a', list(range(1, 11)), 3, dict(kv=[], offset=0, hold=True))
        while engine.step():
            pass
        self.assertEqual(set(scheduler.graph_held), {'a'})
        self.assertEqual(scheduler.graph_held['a'][1], 12)  # 10 prompt + 3 sampled - 1
        free = scheduler.kv_cache_manager.block_pool.get_num_free_blocks()
        self.add(scheduler, 'b', list(range(1, 11)) + [30, 31, 32, 33], 5,
                 dict(kv=[['a', 0, 12, 0]], offset=2, hold=False))
        engine.step()
        scheduler.graph_release(['a'])  # b is still running: deferred
        self.assertEqual(scheduler.graph_release_pending, {'a'})
        while engine.step():
            pass
        self.assertEqual(scheduler.graph_held, {})
        self.assertEqual(scheduler.kv_cache_manager.block_pool.get_num_free_blocks(),
                         scheduler.kv_cache_manager.block_pool.num_gpu_blocks - 1)
        self.assertLess(free, scheduler.kv_cache_manager.block_pool.num_gpu_blocks - 1)

    def test_abort_and_reset_free_held_blocks(self):
        scheduler = make_scheduler(num_blocks=64)
        engine = SimEngine(scheduler)
        engine.samplers = dict(a=lambda k: 30 + k, c=lambda k: 30 + k)
        self.add(scheduler, 'a', list(range(1, 9)), 2, dict(kv=[], offset=0, hold=True))
        self.add(scheduler, 'c', list(range(20, 29)), 2, dict(kv=[], offset=0, hold=True))
        while engine.step():
            pass
        scheduler.finish_requests(['a'], RequestStatus.FINISHED_ABORTED)
        self.assertEqual(set(scheduler.graph_held), {'c'})
        self.assertTrue(scheduler.reset_prefix_cache())
        self.assertEqual(scheduler.graph_held, {})


if __name__ == '__main__':
    unittest.main()
