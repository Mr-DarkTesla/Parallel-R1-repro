"""Graph rollout bookkeeping shared by the agent loop, the vLLM server and vllm_graph (no vLLM import).

A graph request is an ordinary vLLM request with sampling_params.extra_args['graph'] = GraphSpec:

    kv      [[source request id, source start, source end, destination start], ...]: the request's KV for
            prompt[0:kv_end) is copied from finished, held requests instead of being computed; segments are
            contiguous from 0, kv_end < len(prompt), so at least one prompt token is computed.
    offset  RoPE position = physical index - offset for every token this request computes.
    hold    keep the request's KV blocks after it finishes, until released, so later requests can copy them.
    trajectory  a key fixed for the whole trajectory; keys order trajectories by age (oldest first).

A held request has KV for its prompt and every sampled token but the last: kv_length = prompt + output - 1.
Releasing a request that a running request still copies from is deferred until that request finishes,
since a preempted request copies again when it resumes.

Held KV cannot be preempted the way vLLM preempts a running request (by recomputing it later): only the
trajectory knows how to recompute a merged context. So when held KV leaves no room for any waiting request,
the scheduler evicts the held requests of the youngest trajectory that has any and fails its requests that
copy from them (finish reason abort, stop reason GRAPH_EVICTED, with the tokens sampled so far). The
trajectory then recomputes its KV branch by branch from its tokens (closed_blocks) and continues. The oldest
trajectory is never evicted while another holds KV, so rollout always progresses, provided one trajectory fits
in the KV cache on its own (it needs up to about twice its length: branches are also copied when merged);
one that does not is failed with GRAPH_TOO_LARGE.
"""
from dataclasses import dataclass, field

GRAPH_KEY = 'graph'
GRAPH_EVICTED = 'graph_evicted'  # stop reason of a request failed because its trajectory's held KV was evicted
GRAPH_TOO_LARGE = 'graph_too_large'  # stop reason of a request whose trajectory cannot fit in the KV cache alone


@dataclass
class Handle:
    """A finished, held graph request: its full token list, how many tokens have KV, and its offset."""
    request_id: str
    tokens: list
    kv_length: int
    offset: int


@dataclass
class GraphSpec:
    kv: list = field(default_factory=list)
    offset: int = 0
    hold: bool = True
    trajectory: str = ''

    def as_dict(self):
        return dict(kv=[list(segment) for segment in self.kv], offset=int(self.offset), hold=bool(self.hold),
                    trajectory=str(self.trajectory))


def trajectory_key(started, name):
    """A trajectory's key: start time first, so keys sort by age."""
    return f'{started:020.6f}-{name}'


def kv_end(kv):
    return sum(end - start for _, start, end, _ in kv)


def common_prefix(a, b, limit):
    n = 0
    for x, y in zip(a[:limit], b[:limit]):
        if x != y:
            break
        n += 1
    return n


def continuation(handle, prompt):
    """KV segments for a prompt that extends handle's tokens (its last token may differ, e.g. EOS written as a tag)."""
    if handle is None:
        return []
    length = common_prefix(handle.tokens, prompt, min(handle.kv_length, len(prompt) - 1))
    return [[handle.request_id, 0, length, 0]] if length else []


def closed_blocks(tokens, parallel, end_parallel, path, end_path):
    """Branch spans [(start, end), ...] (<Path> through </Path>) of each block closed by </Parallel>, in order.
    Branches see only the shared prefix and themselves; everything after </Parallel> is causal."""
    blocks, pending = [], []
    for index, token in enumerate(tokens):
        if token == parallel:
            pending = []
        elif token == path:
            pending.append([index, None])
        elif token == end_path and pending:
            pending[-1][1] = index + 1
        elif token == end_parallel:
            assert pending and all(end is not None for _, end in pending), f'block closed at {index} has open branches'
            blocks.append([tuple(span) for span in pending])
            pending = []
    return blocks


def merge(handles, shared):
    """KV segments for the merged block: handles[0] covers prompt[0:end of branch 1]; branch i > 1 comes from
    handles[i][shared:] (its copy of the shared prefix is skipped), placed after the branches before it."""
    kv = [[handles[0].request_id, 0, handles[0].kv_length, 0]]
    position = handles[0].kv_length
    for handle in handles[1:]:
        kv.append([handle.request_id, shared, handle.kv_length, position])
        position += handle.kv_length - shared
    return kv


def merged_offset(offset, lengths):
    """Offset after a block whose branches (<Path> through </Path>) have these lengths: siblings share
    positions, </Parallel> follows the longest branch (contract.graph_positions)."""
    return offset + sum(lengths) - max(lengths)


class Registry:
    """Server-side record of held requests: validates specs before they reach the engine."""

    def __init__(self):
        self.held = {}  # request id -> kv_length

    def validate(self, spec, prompt_length):
        position = 0
        for source, start, end, destination in spec['kv']:
            if source not in self.held:
                raise ValueError(f'graph source {source} is not a finished, held request')
            if not 0 <= start < end <= self.held[source]:
                raise ValueError(f'graph source {source} has KV for {self.held[source]} tokens, not [{start}, {end})')
            if destination != position:
                raise ValueError(f'graph segments must be contiguous from 0: {spec["kv"]}')
            position += end - start
        if position >= prompt_length:
            raise ValueError(f'graph KV covers {position} of {prompt_length} prompt tokens; one must be computed')
        if spec['offset'] < 0 or spec['offset'] > prompt_length:
            raise ValueError(f'bad graph offset {spec["offset"]}')

    def finished(self, request_id, spec, prompt_length, output_length):
        if spec['hold']:
            self.held[request_id] = prompt_length + output_length - 1

    def release(self, request_ids):
        return [request_id for request_id in request_ids if self.held.pop(request_id, None) is not None]
