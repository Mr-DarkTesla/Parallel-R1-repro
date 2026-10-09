"""Graph rollout inside vLLM 0.8.5 V1: branch KV kept after a request ends, merged by copying, RoPE offsets.

Enabled with AsyncEngineArgs(scheduler_cls=SCHEDULER, worker_cls=WORKER); vLLM imports this module by those
names in its engine-core process and in every worker, so nothing else has to be patched. Requests without
extra_args['graph'] behave exactly as in vLLM. See graph_kv.py for the request format.

Scheduler (engine core): a graph request with KV segments asks for its prefix-cache hit as usual; the rest of
prompt[0:kv_end) is reported as externally computed through vLLM's KV-connector hooks (the scheduler calls
get_num_new_matched_tokens / update_state_after_alloc / build_connector_meta on self.connector, which is this
scheduler), so vLLM allocates blocks for it without computing it. build_connector_meta turns that range into
slot-to-slot copies from the held sources' blocks and sends them to the workers in
SchedulerOutput.kv_connector_metadata. Prefix-cache hits are reused as they are: in graph rollout a token
sequence fixes its own graph (tags mark the branches), so equal tokens have equal KV. A server must therefore
not mix graph and flat rollout of the same contract.

Memory: held KV cannot be preempted (only the trajectory can recompute a merged context), so requests are
ordered by trajectory age (waiting: oldest first; running: the youngest is preempted first), and when nothing
can be scheduled because held KV fills the cache, the youngest trajectory that holds KV is evicted: its held
requests are freed and its waiting requests that copy from them are failed back to the client (finish reason
abort, stop reason GRAPH_EVICTED), which recomputes the KV and resubmits (parallel_thinking_loop_v3._generate).

Worker: before the forward pass the model runner applies the copies to every layer's KV cache, and after the
inputs are prepared it subtracts each graph request's offset from its RoPE positions.
"""
from collections import deque
from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch
from vllm.logger import init_logger
from vllm.v1.core.sched.scheduler import Scheduler
from vllm.v1.engine import EngineCoreOutput, FinishReason
from vllm.v1.request import RequestStatus
from vllm.v1.worker.gpu_model_runner import GPUModelRunner
from vllm.v1.worker.gpu_worker import Worker

from verl.parallel_thinking_generation_v3.graph_kv import GRAPH_EVICTED, GRAPH_KEY, GRAPH_TOO_LARGE, kv_end

logger = init_logger(__name__)

SCHEDULER = 'verl.parallel_thinking_generation_v3.vllm_graph.GraphScheduler'
WORKER = 'verl.parallel_thinking_generation_v3.vllm_graph.GraphWorker'


def graph_spec(request) -> Optional[dict]:
    extra = request.sampling_params.extra_args
    return extra.get(GRAPH_KEY) if extra else None


def trajectory(request) -> str:
    spec = graph_spec(request)
    return spec.get('trajectory', '') if spec else ''


@dataclass
class GraphKVCopies:
    """Slot copies for one step: kv_cache[slot dst[i]] = kv_cache[slot src[i]] in every layer."""
    src: np.ndarray
    dst: np.ndarray


def slots(blocks, start, end, block_size):
    """Physical slot ids of token indices [start, end) of a request whose block ids are `blocks`."""
    index = np.arange(start, end)
    return np.asarray(blocks, dtype=np.int64)[index // block_size] * block_size + index % block_size


class GraphScheduler(Scheduler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.connector is not None:
            raise ValueError('graph rollout cannot be combined with a KV connector')
        self.connector = self  # vLLM's external-KV hooks, see the module docstring
        self.graph_held = {}  # request id -> (request, kv_length): finished requests whose blocks are kept
        self.graph_users = {}  # source id -> ids of unfinished requests that copy from it
        self.graph_release_pending = set()
        self.graph_copies = []  # (request, start, end) allocated this step
        self.graph_evicted = set()  # evicted held ids, until the client releases them
        self.graph_failed = []  # outputs of requests failed by an eviction, sent with the next step's outputs
        if not self.cache_config.enable_prefix_caching:
            # Without it a continuation copies its whole prefix instead of sharing the held blocks.
            raise ValueError('graph rollout needs prefix caching')
        manager = self.kv_cache_manager
        common_prefix = manager.get_num_common_prefix_blocks

        def num_common_prefix_blocks(request, num_running_requests):
            # Cascade attention counts blocks whose ref_cnt equals the number of running requests;
            # held blocks carry extra references, so the count is not trustworthy while any are held.
            return 0 if self.graph_held else common_prefix(request, num_running_requests)
        manager.get_num_common_prefix_blocks = num_common_prefix_blocks

    # ---- requests -------------------------------------------------------------------------------------
    def add_request(self, request):
        spec = graph_spec(request)
        if spec:
            sources = [source for source, *_ in spec['kv']]
            if any(source in self.graph_evicted for source in sources):
                return self._graph_fail(request)
            for source, start, end, _ in spec['kv']:
                held = self.graph_held.get(source)
                # The server validates specs against its own record of held requests; a mismatch is a bug.
                assert held is not None and end <= held[1], (
                    f'{request.request_id}: graph source {source} not held or too short ({held and held[1]} < {end})')
            for source in sources:
                self.graph_users.setdefault(source, set()).add(request.request_id)
        super().add_request(request)

    def _free_request(self, request):
        spec = graph_spec(request)
        if spec:
            for source, *_ in spec['kv']:
                users = self.graph_users.get(source)
                if users is not None:
                    users.discard(request.request_id)
                    if not users:
                        del self.graph_users[source]
                        if source in self.graph_release_pending:
                            self._graph_free(source)
        if not spec or not spec['hold'] or request.status == RequestStatus.FINISHED_ABORTED:
            return super()._free_request(request)
        # As Scheduler._free_request, but the KV blocks stay allocated until graph_release.
        self.graph_held[request.request_id] = (request, request.num_computed_tokens)
        self.kv_cache_manager.free_block_hashes(request)
        self.encoder_cache_manager.free(request)
        self._cached_reqs_data.pop(request.request_id, None)
        del self.requests[request.request_id]
        self.finished_req_ids.add(request.request_id)

    def graph_release(self, request_ids):
        """Free held requests; one that a running request still copies from is freed when that one finishes."""
        for request_id in request_ids:
            if request_id not in self.graph_held:
                continue
            if self.graph_users.get(request_id):
                self.graph_release_pending.add(request_id)
            else:
                self._graph_free(request_id)

    def _graph_free(self, request_id):
        self.graph_release_pending.discard(request_id)
        request, _ = self.graph_held.pop(request_id)
        self.kv_cache_manager.free(request)

    def finish_requests(self, request_ids, finished_status):
        # Aborting a held request id (the client's release call) frees its blocks.
        request_ids = (request_ids, ) if isinstance(request_ids, str) else set(request_ids)
        self.graph_evicted.difference_update(request_ids)
        self.graph_release([request_id for request_id in request_ids if request_id in self.graph_held])
        super().finish_requests([request_id for request_id in request_ids if request_id not in self.graph_held],
                                finished_status)

    def reset_prefix_cache(self):
        self.graph_release(list(self.graph_held))
        self.graph_evicted.clear()
        return super().reset_prefix_cache()

    # ---- memory: trajectory order and eviction ----------------------------------------------------------
    def schedule(self):
        if self.graph_held or any(graph_spec(request) for request in self.waiting):
            # Oldest trajectory first; vLLM preempts the last running request, i.e. the youngest trajectory's.
            self.running.sort(key=trajectory)
            self.waiting = deque(sorted(self.waiting, key=trajectory))
        output = super().schedule()
        if not output.total_num_scheduled_tokens and self.waiting and not self.running and self.graph_held:
            self._graph_evict()
        return output

    def _graph_evict(self):
        """Nothing could be scheduled and held KV fills the cache. The waiting head belongs to the oldest
        trajectory with a waiting request; evict the youngest trajectory younger than it that holds KV.

        If only older trajectories hold KV, they are between requests (none of theirs is waiting or running), and
        their next requests will be scheduled before this one: wait, so the oldest trajectory always progresses.
        If only the head's own trajectory holds KV, everything else is free and it still does not fit: it can
        never finish, so its requests fail with GRAPH_TOO_LARGE instead of being evicted forever.
        """
        head = trajectory(self.waiting[0])
        holders = {trajectory(request) for request, _ in self.graph_held.values()}
        younger = [key for key in holders if key > head]
        if not younger and holders != {head}:
            return
        victim = max(younger) if younger else head
        evicted = {request_id for request_id, (request, _) in self.graph_held.items() if trajectory(request) == victim}
        if younger:
            reason = GRAPH_EVICTED
            failed = [request for request in self.waiting
                      if any(source in evicted for source, *_ in (graph_spec(request) or {}).get('kv', ()))]
            logger.warning('graph rollout: KV cache full, evicting trajectory %s (%d held, %d waiting requests failed)',
                           victim, len(evicted), len(failed))
        else:
            reason = GRAPH_TOO_LARGE
            failed = [request for request in self.waiting if trajectory(request) == victim]
            logger.error('graph rollout: trajectory %s does not fit in the KV cache (%d blocks)', victim,
                         self.kv_cache_manager.block_pool.num_gpu_blocks)
        for request in failed:
            self.waiting.remove(request)
            request.status = RequestStatus.FINISHED_ABORTED
            self._free_request(request)
            self._graph_fail(request, reason)
        for request_id in evicted:
            assert not self.graph_users.get(request_id), f'evicted {request_id} still has users'
            if request_id in self.graph_held:  # not already freed as a pending release
                self._graph_free(request_id)
        self.graph_evicted |= evicted

    def _graph_fail(self, request, reason=GRAPH_EVICTED):
        self.graph_failed.append(EngineCoreOutput(request_id=request.request_id, new_token_ids=[],
                                                  finish_reason=FinishReason.ABORT, stop_reason=reason))

    def has_requests(self):
        return super().has_requests() or bool(self.graph_failed)

    def update_from_output(self, scheduler_output, model_runner_output):
        outputs = super().update_from_output(scheduler_output, model_runner_output)
        if self.graph_failed:
            outputs.outputs.extend(self.graph_failed)
            self.graph_failed = []
        return outputs

    # ---- KV-connector hooks called by Scheduler.schedule ----------------------------------------------
    def get_num_new_matched_tokens(self, request, num_computed_tokens):
        spec = graph_spec(request)
        return max(0, kv_end(spec['kv']) - num_computed_tokens) if spec else 0

    def update_state_after_alloc(self, request, num_external_tokens):
        if num_external_tokens:
            end = kv_end(graph_spec(request)['kv'])
            self.graph_copies.append((request, end - num_external_tokens, end))

    def build_connector_meta(self, scheduler_output):
        if not self.graph_copies:
            return None
        block_size = self.kv_cache_manager.block_size
        blocks = self.kv_cache_manager.req_to_blocks
        src, dst = [], []
        for request, start, end in self.graph_copies:
            target = [block.block_id for block in blocks[request.request_id]]
            for source, source_start, source_end, destination in graph_spec(request)['kv']:
                lo, hi = max(start, destination), min(end, destination + source_end - source_start)
                if lo >= hi:
                    continue
                shift = source_start - destination
                assert source in self.graph_held, f'{request.request_id}: graph source {source} was released'
                source_blocks = [block.block_id for block in blocks[source]]
                src.append(slots(source_blocks, lo + shift, hi + shift, block_size))
                dst.append(slots(target, lo, hi, block_size))
        self.graph_copies = []
        return GraphKVCopies(np.concatenate(src), np.concatenate(dst))


# ---- worker side ---------------------------------------------------------------------------------------
def apply_kv_copies(kv_caches, copies):
    """kv_caches: per-layer tensors shaped (2, num_blocks, block_size, ...) (FlashAttention V1 layout)."""
    if copies is None or not len(copies.src):
        return
    device = kv_caches[0].device
    src = torch.from_numpy(copies.src).to(device, non_blocking=True)
    dst = torch.from_numpy(copies.dst).to(device, non_blocking=True)
    for cache in kv_caches:
        assert cache.dim() >= 4 and cache.size(0) == 2, f'unexpected KV cache layout {tuple(cache.shape)}'
        flat = cache.view(2, cache.size(1) * cache.size(2), *cache.shape[3:])
        flat[:, dst] = flat[:, src]


def position_offsets(req_ids, num_scheduled_tokens, offsets):
    """Per scheduled token, the offset of its request (None if no scheduled request has one)."""
    per_request = [offsets.get(req_id, 0) for req_id in req_ids]
    if not any(per_request):
        return None
    counts = [num_scheduled_tokens[req_id] for req_id in req_ids]
    return np.repeat(np.asarray(per_request, dtype=np.int64), counts)


class GraphModelRunner(GPUModelRunner):
    """GPUModelRunner plus KV copies before the forward pass and per-request RoPE offsets.

    Installed by GraphWorker on an existing GPUModelRunner (class swap), so it adds no state in __init__.
    """

    @property
    def graph_offsets(self):
        return self.__dict__.setdefault('_graph_offsets', {})

    def _update_states(self, scheduler_output):
        for req_id in scheduler_output.finished_req_ids:
            self.graph_offsets.pop(req_id, None)
        for new in scheduler_output.scheduled_new_reqs:
            extra = new.sampling_params.extra_args
            spec = extra.get(GRAPH_KEY) if extra else None
            if spec and spec['offset']:
                self.graph_offsets[new.req_id] = int(spec['offset'])
        return super()._update_states(scheduler_output)

    def _prepare_inputs(self, scheduler_output):
        result = super()._prepare_inputs(scheduler_output)
        if self.graph_offsets:
            num_reqs = self.input_batch.num_reqs
            offsets = position_offsets(self.input_batch.req_ids[:num_reqs], scheduler_output.num_scheduled_tokens,
                                       self.graph_offsets)
            if offsets is not None:
                assert not self.uses_mrope, 'graph rollout needs 1-D RoPE positions'
                total = scheduler_output.total_num_scheduled_tokens
                self.positions_np[:total] -= offsets
                self.positions[:total].copy_(self.positions_cpu[:total], non_blocking=True)
        return result

    def execute_model(self, scheduler_output, intermediate_tensors=None):
        if isinstance(scheduler_output.kv_connector_metadata, GraphKVCopies):
            apply_kv_copies(self.kv_caches, scheduler_output.kv_connector_metadata)
        return super().execute_model(scheduler_output, intermediate_tensors)


class GraphWorker(Worker):

    def init_device(self):
        super().init_device()
        self.model_runner.__class__ = GraphModelRunner
