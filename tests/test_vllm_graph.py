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
            loops = []
            for index in range(trajectories):
                loop = base.Loop()
                loop.server_manager, loop.loop = engine, asyncio.get_running_loop()
                loop.trajectory = dict(index=index)  # trace metadata, set by the agent loop worker
                loops.append(loop)
            results = await asyncio.gather(*[loop.run([], dict(temperature=1.0, top_p=1.0)) for loop in loops])
            runner.cancel()
            for index, loop in enumerate(loops):
                self.assertEqual(loop.trace.record['trajectory'], dict(index=index))
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

    def test_evicted_trajectories_rebuild_their_kv(self):
        # A trajectory alone needs 30 blocks here: with 32, held KV keeps filling the cache, younger
        # trajectories are evicted, rebuild their KV branch by branch and continue after their sampled tokens.
        engine = SimEngine(make_scheduler(num_blocks=32, max_batched=32), scripts(6, seed=3))
        results = self.rollout(engine, 6)
        self.assertGreater(engine.evicted, 0)
        self.check(engine, results)

    def test_trajectory_larger_than_the_cache_fails(self):
        engine = SimEngine(make_scheduler(num_blocks=24, max_batched=32), scripts(1))
        with self.assertRaisesRegex(RuntimeError, 'more KV than the cache has'):
            self.rollout(engine, 1)

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

    def test_eviction_follows_trajectory_age(self):
        scheduler = make_scheduler(num_blocks=17)  # 16 usable blocks of 4 tokens
        engine = SimEngine(scheduler)
        engine.samplers = dict(a=lambda k: 30, b=lambda k: 31, c=lambda k: 32)
        self.add(scheduler, 'a', list(range(1, 41)), 2, dict(kv=[], offset=0, hold=True, trajectory='t1'))
        while engine.step():
            pass
        self.add(scheduler, 'b', [50] * 30, 1, dict(kv=[], offset=0, hold=False, trajectory='t2'))
        for _ in range(3):  # does not fit next to a's 11 held blocks
            self.assertFalse(engine.step())
        # t1 is older and between requests: its next request would come first, so it is not evicted.
        self.assertIn('a', scheduler.graph_held)
        self.assertEqual([request.request_id for request in scheduler.waiting], ['b'])
        self.add(scheduler, 'c', [51] * 30, 1, dict(kv=[], offset=0, hold=False, trajectory='t0'))
        engine.step()  # c belongs to an older trajectory than t1: t1 is evicted
        self.assertEqual(scheduler.graph_held, {})
        self.assertEqual(scheduler.graph_evicted, {'a'})
        while engine.step():
            pass
        self.assertEqual((engine.outputs['b'], engine.outputs['c']), ([31], [32]))
        scheduler.finish_requests(['a'], RequestStatus.FINISHED_ABORTED)  # the client's release
        self.assertEqual(scheduler.graph_evicted, set())

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


class ClientTest(unittest.TestCase):
    """vLLM's client side (OutputProcessor, as in AsyncLLM) on requests the scheduler failed after an eviction."""

    def outputs(self, log_stats):
        from vllm.v1.engine import EngineCoreOutput, EngineCoreRequest
        from vllm.v1.engine.output_processor import OutputProcessor
        from vllm.v1.metrics.stats import IterationStats
        processor = OutputProcessor(SimpleNamespace(get_lora_tokenizer=lambda lora: None), log_stats=log_stats)
        for request_id in 'ab':
            processor.add_request(EngineCoreRequest(request_id, [1, 2, 3], None, None, None,
                                                    SamplingParams(max_tokens=8, logprobs=0), EOS, time.time(), None),
                                  None)
        stats = IterationStats() if log_stats else None
        processor.process_outputs([EngineCoreOutput('a', [7, 8])], time.time(), stats)  # a, then preempted
        scheduler = make_scheduler()
        scheduler._graph_fail(SimpleNamespace(request_id='a'))
        scheduler._graph_fail(SimpleNamespace(request_id='b'))  # never got its first token
        return {output.request_id: output.outputs[0] for output in
                processor.process_outputs(scheduler.graph_failed, time.time(), stats).request_outputs}

    def test_failed_requests_end_with_their_sampled_tokens(self):
        outputs = self.outputs(log_stats=False)  # as the server runs vLLM in graph rollout
        self.assertEqual(outputs['a'].token_ids, [7, 8])
        self.assertEqual(outputs['b'].token_ids, [])
        for output in outputs.values():
            self.assertEqual((output.finish_reason, output.stop_reason), ('abort', graph_kv.GRAPH_EVICTED))

    def test_request_stats_reject_a_failure_before_the_first_token(self):
        with self.assertRaises(AssertionError):  # hence disable_log_stats in graph rollout
            self.outputs(log_stats=True)


def load_check():
    spec = importlib.util.spec_from_file_location('check_graph_rollout', ROOT / 'experiments/qwen06/check_graph_rollout.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FingerprintEngine(SimEngine):
    """Reports each sampled token's query fingerprint as its log-prob, so a driver's bookkeeping can be checked."""

    async def generate(self, *args, **kwargs):
        result = await super().generate(*args, **kwargs)
        if result['token_ids']:
            result['logprobs'] = self.views[-1]['queries']  # this request's view: nothing ran in between
        return result


def merged_cache_log_probs(model, tokens, spans):
    """Log-softmax at every token computed as graph rollout does in vLLM, with HF caches: each branch from its own
    copy of the KV before it, the branches' KV concatenated after the block, RoPE positions continuing after the
    longest branch."""
    from transformers import DynamicCache

    def run(ids, start, cache):
        past = cache.get_seq_length()
        out = model(torch.tensor([ids]), position_ids=torch.arange(start, start + len(ids))[None],
                    past_key_values=cache, cache_position=torch.arange(past, past + len(ids)), use_cache=True)
        return out.logits[0], out.past_key_values

    blocks = {}
    for span in spans:
        blocks.setdefault(span.block, []).append(span)
    logits, cache, index, position = [], DynamicCache(), 0, 0
    for block in sorted(blocks.values(), key=lambda block: block[0].start):
        out, cache = run(tokens[index:block[0].start], position, cache)
        logits.append(out)
        position += block[0].start - index
        layers, tails = cache.to_legacy_cache(), []
        for span in block:
            size = span.end - span.start
            copy = DynamicCache.from_legacy_cache(tuple((k.clone(), v.clone()) for k, v in layers))
            out, copy = run(tokens[span.start:span.end], position, copy)
            logits.append(out)
            tails.append([(k[:, :, -size:], v[:, :, -size:]) for k, v in copy.to_legacy_cache()])
        cache = DynamicCache.from_legacy_cache(tuple(
            (torch.cat([layers[layer][0]] + [tail[layer][0] for tail in tails], 2),
             torch.cat([layers[layer][1]] + [tail[layer][1] for tail in tails], 2)) for layer in range(len(layers))))
        position += max(span.end - span.start for span in block)
        index = block[-1].end
    out, cache = run(tokens[index:], position, cache)
    logits.append(out)
    return torch.cat(logits).log_softmax(-1)


class CheckScriptTest(unittest.TestCase):
    """experiments/qwen06/check_graph_rollout.py: its forced-structure driver and its HF scorer."""

    def test_forced_driver_records_each_token_in_its_graph_context(self):
        check = load_check()
        config = check.agent_config(prompt_length=8, response_length=200, path_length=8)
        base.Loop._class_initialized = False
        base.Loop.init_class(config, base.PlanTokenizer([3, 4, 5, 6, 7]))
        lengths = dict(main=6, path=5, summary=4)
        for blocks, expect_evictions in [(None, False), (32, True)]:  # 32: one fits, four evict each other
            rng = torch.Generator().manual_seed(blocks or 0)
            engine = FingerprintEngine(make_scheduler(**{'num_blocks': blocks} if blocks else {}, max_batched=32),
                                       [dict(main=[torch.randint(30, 40, (6,), generator=rng).tolist()
                                                   for _ in range(10)]) for _ in range(4)])

            async def main():
                runner = asyncio.create_task(engine.run())
                results = await asyncio.gather(*[
                    check.forced_trajectory(check.bare_loop(base.Loop, engine, f't{number}'), [3, 4, 5, 6, 7 + number],
                                            lengths) for number in range(4)])
                runner.cancel()
                return results

            results = asyncio.run(main())
            self.assertEqual(engine.evicted > 0, expect_evictions)
            for tokens, spans, sampled in results:
                self.assertEqual([(s.start, s.end, s.block, s.path) for s in spans],
                                 [(s.start, s.end, s.block, s.path) for s in spans_of(tokens)])
                self.assertEqual([len([s for s in spans if s.block == b]) for b in (0, 1)], [2, 3])
                reference = graph_fingerprints(tokens)
                for index, token, query, segment in sampled:
                    self.assertEqual(tokens[index], token)
                    self.assertEqual(query, reference[index - 1], (segment, index))
                counts = {segment: sum(row[3] == segment for row in sampled) for segment in dict.fromkeys(
                    row[3] for row in sampled)}
                self.assertEqual(counts, {'main_before_fork': 6, 'path1_block1': 5, 'path2+_block1': 5,
                                          'summary_block1': 4, 'main_after_fork': 12, 'path1_block2': 5,
                                          'path2+_block2': 10, 'summary_block2': 4})
            self.assertEqual(engine.scheduler.graph_held, {})
            self.assertEqual(engine.registry.held, {})

    def test_scores_are_those_of_merged_branch_caches(self):
        check = load_check()
        from transformers import Qwen3Config, Qwen3ForCausalLM
        torch.manual_seed(0)
        config = Qwen3Config(vocab_size=64, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                             num_attention_heads=4, num_key_value_heads=2, head_dim=16)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).double().eval()
        rng = torch.Generator().manual_seed(1)
        text = lambda n: torch.randint(30, 64, (n,), generator=rng).tolist()
        tokens, spans = text(6), []
        for block, sizes in enumerate([(5, 8), (6, 3, 4)]):
            tokens += [PARALLEL, WORDS['branches='], WORDS[str(len(sizes))], 16] + text(3) + [17]  # ...<Plan>..</Plan>
            for number, size in enumerate(sizes, 1):
                start = len(tokens)
                tokens += [PATH, WORDS[str(number)], WORDS[':']] + text(size) + [END_PATH]
                spans.append(check.contract.Span(start, len(tokens), block, number))
            tokens += [END_PARALLEL, base.SUMMARY] + text(4) + [base.END_SUMMARY] + text(3)
        rows = [(index - 1, tokens[index]) for index in range(1, len(tokens))]
        scores = {name: torch.tensor(values, dtype=torch.float64) for name, values in
                  check.score(model, tokens, spans, rows).items()}
        with torch.no_grad():
            reference = merged_cache_log_probs(model, tokens, spans)
        reference = reference[torch.arange(len(rows)), torch.tensor(tokens[1:])]
        torch.testing.assert_close(scores['graph'], reference, atol=1e-5, rtol=0)
        before = spans[0].start  # up to the first branch everything is causal: the three forwards agree
        for name in check.FORWARDS:
            torch.testing.assert_close(scores[name][:before], reference[:before], atol=1e-5, rtol=0)
        later = [index - 1 for span in spans if span.path > 1 for index in range(span.start + 1, span.end)]
        after = list(range(spans[1].end - 1, len(rows)))  # </Parallel> onwards
        for name in ('graph_mask_physical_positions', 'causal'):  # the contrasts are not vacuous
            self.assertGreater((scores[name][later] - reference[later]).abs().max().item(), 1e-3, name)
            self.assertGreater((scores[name][after] - reference[after]).abs().max().item(), 1e-3, name)


if __name__ == '__main__':
    unittest.main()
