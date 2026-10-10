"""Exact sampler of the parallel-thinking contract for an SFT'd checkpoint (evaluation).

Protocol per sample, on token ids only (contract.py is the source of truth):

    prompt -> MAIN until <Parallel> | EOS | budget
    <Parallel> -> insert branches= ; COUNT samples one of contract.COUNTS ; insert <Plan>
               -> PLAN until </Plan> (contract.plan_status; anything but valid ends the trajectory)
               -> per branch i: insert <Path> i: ; PATH until </Path> (EOS is written as </Path>,
                  a cut gets an inserted </Path>)
               -> insert </Parallel><Summary> ; SUMMARY until </Summary> (same closing rules)
               -> MAIN continues (MAIN_OPEN while blocks remain, else MAIN_CLOSED)

Every node applies the contract suppression (logit_bias SUPPRESS_BIAS on suppressed_tokens(node); COUNT via
allowed ids). Graph semantics are exact: the branches of a block are causal continuations of the shared prefix
through </Plan> (so they run in any causal backend, e.g. vLLM, at positions base+offset), and every stage whose
context holds a finished block (summary, the main text after it, a second block) runs in HFBackend with the
contract mask (graph_attention_mask) and positions (graph_positions).

Budget semantics follow the RL loop (parallel_thinking_loop_v3._plan_block): every call gets at most the
sampled-token room left (`budget - T`); all branches of a block get the same room (they run in parallel, so T can
exceed the budget by the branches of the last block); the plan is capped by plan_cap and each branch by
branch_cap. A summary or main call with no room left ends the trajectory as trajectory_budget.
"""
import math
from dataclasses import dataclass, field
from typing import Callable, Optional

import torch

from common import contract

EOS_TOKENS = ('<|im_end|>', '<|endoftext|>')
COMPLETE, TRAJECTORY_BUDGET = 'complete', 'trajectory_budget'
DEFAULT_TEMPLATE = '{problem}\n\nPlease reason step by step, and put your final answer within \\boxed{{}}.'


@dataclass
class Sampling:
    """Qwen3 thinking-mode defaults. temperature <= 0 is greedy."""
    temperature: float = 0.6
    top_p: float = 0.95
    top_k: int = 20


@dataclass
class Request:
    """One generation call: continue `context` (full sequence ids, prompt included)."""
    context: list
    node: int
    stop: tuple            # token ids that end the call (kept as the last token)
    max_tokens: int
    seed: int
    constraint: dict       # contract.sampling_constraint: {'logit_bias': {...}} or {'allowed_token_ids': [...]}
    spans: tuple = ()      # contract.Span of finished branches in context; non-empty needs a graph backend


@dataclass
class Result:
    tokens: list
    logits: Optional[torch.Tensor] = None  # (len(tokens), vocab) raw logits that produced each token (record mode)


# ---------------------------------------------------------------------------------------------------- sampling

def constraint_bias(constraint, vocab, device):
    """(vocab,) additive float32 bias of one request: logit_bias entries, or HARD_MASK outside allowed ids."""
    bias = torch.zeros(vocab, dtype=torch.float32, device=device)
    allowed = constraint.get('allowed_token_ids')
    if allowed is not None:
        bias.fill_(contract.HARD_MASK)
        bias[torch.tensor(list(allowed), device=device)] = 0.0
    for token, value in (constraint.get('logit_bias') or {}).items():
        bias[int(token)] += value
    return bias


def sample_rows(logits, sampling, generators):
    """One token per row of float32 logits (bias already applied), vLLM order: temperature, top-k, top-p."""
    if sampling.temperature <= 0:
        return logits.argmax(-1).tolist()
    logits = logits / sampling.temperature
    if sampling.top_k and 0 < sampling.top_k < logits.size(-1):
        kth = logits.topk(sampling.top_k, dim=-1).values[:, -1:]
        logits = logits.masked_fill(logits < kth, -math.inf)
    if sampling.top_p < 1.0:
        ordered, index = logits.sort(dim=-1)  # ascending, as vLLM's apply_top_k_top_p
        cumulative = ordered.softmax(-1).cumsum(-1)
        drop = cumulative <= 1 - sampling.top_p
        drop[:, -1] = False
        logits = logits.scatter(-1, index, ordered.masked_fill(drop, -math.inf))
    probs = logits.softmax(-1)
    return [int(torch.multinomial(probs[row], 1, generator=generators[row])) for row in range(probs.size(0))]


# ---------------------------------------------------------------------------------------------------- backends

class HFBackend:
    """Batched HF generation with left padding, explicit position ids and a 4D additive mask per row.

    Handles plain causal requests and graph requests (spans) alike: one prefill over the padded contexts with
    the contract mask/positions, then cached decoding where each new token sees every non-pad key and continues
    from its row's last graph position. transformers 4.51.3 Qwen3 passes a 4D mask through unchanged
    (_prepare_4d_causal_attention_mask_with_cache_position), shape (B, 1, q_len, kv_len) with 0 = attend and
    finfo.min = masked, during prefill and during decode with a DynamicCache. Needs attn_implementation sdpa or
    eager (flash_attention_2 ignores 4D masks).
    """
    graph = True

    def __init__(self, model, batch_tokens=200_000, max_batch=64, record_logits=False):
        self.model = model.eval()
        self.batch_tokens, self.max_batch, self.record_logits = batch_tokens, max_batch, record_logits
        impl = getattr(model.config, '_attn_implementation', None)
        if impl not in (None, 'sdpa', 'eager'):
            raise ValueError(f'HFBackend needs sdpa or eager attention for 4D graph masks, got {impl}')

    def batches(self, requests):
        order = sorted(range(len(requests)), key=lambda i: len(requests[i].context))
        batch, width = [], 0
        for index in order:
            request = requests[index]
            need = len(request.context) + request.max_tokens
            if batch and ((len(batch) + 1) * max(width, need) > self.batch_tokens or len(batch) >= self.max_batch):
                yield batch
                batch, width = [], 0
            batch.append(index)
            width = max(width, need)
        if batch:
            yield batch

    def generate(self, requests, sampling):
        results = [None] * len(requests)
        live = []
        for index, request in enumerate(requests):
            if request.max_tokens < 1:
                results[index] = Result([], None)
            else:
                live.append(index)
        for batch in self.batches([requests[i] for i in live]):
            for index, result in zip(batch, self._run([requests[live[i]] for i in batch], sampling)):
                results[live[index]] = result
        return results

    @torch.no_grad()
    def _run(self, requests, sampling):
        from transformers import DynamicCache
        model = self.model
        device = next(model.parameters()).device
        dtype = next(model.parameters()).dtype
        floor = torch.finfo(dtype).min
        rows = len(requests)
        lengths = [len(r.context) for r in requests]
        width = max(lengths)
        input_ids = torch.zeros(rows, width, dtype=torch.long, device=device)
        position_ids = torch.zeros(rows, width, dtype=torch.long, device=device)
        mask = torch.full((rows, 1, width, width), floor, dtype=dtype, device=device)
        keys = torch.full((rows, width), floor, dtype=dtype, device=device)  # decode mask over the prefill keys
        next_position = []
        for row, request in enumerate(requests):
            length, pad = lengths[row], width - lengths[row]
            input_ids[row, pad:] = torch.tensor(request.context, device=device)
            positions = contract.graph_positions(length, list(request.spans))
            position_ids[row, pad:] = torch.tensor(positions, device=device)
            allowed = contract.graph_attention_mask(length, list(request.spans), device=device)
            mask[row, 0, pad:, pad:].masked_fill_(allowed, 0.0)
            idle = torch.arange(pad, device=device)
            mask[row, 0, idle, idle] = 0.0  # pad queries see themselves: no fully masked row
            keys[row, pad:] = 0.0
            next_position.append(positions[-1] + 1)
        cache = DynamicCache()
        out = model(input_ids=input_ids, attention_mask=mask, position_ids=position_ids, past_key_values=cache,
                    use_cache=True, logits_to_keep=1)
        del mask
        vocab = out.logits.size(-1)
        bias = torch.stack([constraint_bias(r.constraint, vocab, device) for r in requests])
        generators = [torch.Generator(device=device).manual_seed(int(r.seed) % (2 ** 63)) for r in requests]
        next_position = torch.tensor(next_position, dtype=torch.long, device=device)
        tokens = [[] for _ in requests]
        recorded = [[] for _ in requests] if self.record_logits else None
        active = list(range(rows))  # request index of each live row
        logits = out.logits[:, -1].float()
        while True:
            chosen = sample_rows(logits + bias, sampling, generators)
            keep = []
            for row, request_index in enumerate(active):
                request, token = requests[request_index], chosen[row]
                tokens[request_index].append(token)
                if recorded is not None:
                    recorded[request_index].append(logits[row].cpu())
                if token not in request.stop and len(tokens[request_index]) < request.max_tokens:
                    keep.append(row)
            if not keep:
                break
            if len(keep) < len(active):
                select = torch.tensor(keep, device=device)
                cache.batch_select_indices(select)
                bias, keys, next_position = bias[select], keys[select], next_position[select]
                generators = [generators[row] for row in keep]
                chosen = [chosen[row] for row in keep]
                active = [active[row] for row in keep]
            keys = torch.cat([keys, torch.zeros(len(active), 1, dtype=dtype, device=device)], dim=1)
            out = model(input_ids=torch.tensor(chosen, device=device)[:, None], attention_mask=keys[:, None, None, :],
                        position_ids=next_position[:, None], past_key_values=cache, use_cache=True)
            next_position = next_position + 1
            logits = out.logits[:, -1].float()
        return [Result(tokens[i], torch.stack(recorded[i]) if recorded is not None else None)
                for i in range(rows)]


class VLLMBackend:
    """Causal requests only, through vLLM 0.8.5 offline LLM.generate with token-id prompts.

    Constraints use SamplingParams.logit_bias (dict id -> bias) and SamplingParams.allowed_token_ids, the same
    fields the RL loop passes to vLLM 0.8.5 V1 (parallel_thinking_loop_v3._node_call). The stop token is the last
    output id (vLLM keeps stop_token_ids and EOS in CompletionOutput.token_ids); normalize() guards against a
    build that drops it.
    """
    graph = False

    def __init__(self, model, gpu_memory_utilization=0.45, max_model_len=32768, dtype='bfloat16', seed=0,
                 enforce_eager=False, **kwargs):
        from vllm import LLM
        self.llm = LLM(model=model, dtype=dtype, gpu_memory_utilization=gpu_memory_utilization,
                       max_model_len=max_model_len, seed=seed, enforce_eager=enforce_eager,
                       enable_prefix_caching=True, **kwargs)
        self.max_model_len = max_model_len

    def params(self, request, sampling):
        from vllm import SamplingParams
        args = dict(n=1, max_tokens=request.max_tokens, seed=int(request.seed) % (2 ** 31),
                    stop_token_ids=list(request.stop), detokenize=False, skip_special_tokens=False)
        if sampling.temperature <= 0:
            args.update(temperature=0.0)
        else:
            args.update(temperature=sampling.temperature, top_p=sampling.top_p,
                        top_k=sampling.top_k if sampling.top_k and sampling.top_k > 0 else -1)
        if request.constraint.get('allowed_token_ids') is not None:
            args['allowed_token_ids'] = list(request.constraint['allowed_token_ids'])
        if request.constraint.get('logit_bias'):
            args['logit_bias'] = {int(k): float(v) for k, v in request.constraint['logit_bias'].items()}
        return SamplingParams(**args)

    @staticmethod
    def normalize(completion, stop):
        tokens = list(completion.token_ids)
        reason = getattr(completion, 'stop_reason', None)
        if (getattr(completion, 'finish_reason', None) == 'stop' and isinstance(reason, int) and reason in stop
                and (not tokens or tokens[-1] != reason)):
            tokens.append(reason)
        return tokens

    def generate(self, requests, sampling):
        from vllm.inputs import TokensPrompt
        results = [None] * len(requests)
        live = []
        for index, request in enumerate(requests):
            assert not request.spans, 'VLLMBackend runs causal requests only'
            max_tokens = min(request.max_tokens, self.max_model_len - len(request.context))
            if max_tokens < 1:
                results[index] = Result([])
            else:
                request.max_tokens = max_tokens
                live.append(index)
        if live:
            outputs = self.llm.generate([TokensPrompt(prompt_token_ids=list(requests[i].context)) for i in live],
                                        sampling_params=[self.params(requests[i], sampling) for i in live],
                                        use_tqdm=False)
            for index, output in zip(live, outputs):
                results[index] = Result(self.normalize(output.outputs[0], set(requests[index].stop)))
        return results


# ---------------------------------------------------------------------------------------------------- sampler

def chat_prompt_ids(tokenizer, prompt, enable_thinking=True):
    text = tokenizer.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=False,
                                         add_generation_prompt=True, enable_thinking=enable_thinking)
    return tokenizer.encode(text, add_special_tokens=False)


def eos_ids(tokenizer):
    ids = set()
    for token in EOS_TOKENS:
        encoded = tokenizer.encode(token, add_special_tokens=False)
        if len(encoded) == 1 and tokenizer.convert_ids_to_tokens(encoded[0]) == token:
            ids.add(encoded[0])
    if tokenizer.eos_token_id is not None:
        ids.add(tokenizer.eos_token_id)
    if not ids:
        raise ValueError('tokenizer has no EOS token')
    return tuple(sorted(ids))


@dataclass
class Trajectory:
    index: int
    seed: int
    ids: list
    prompt_len: int
    allow_parallel: bool
    stage: str = 'main'
    status: Optional[str] = None
    spans: list = field(default_factory=list)
    calls: list = field(default_factory=list)
    blocks: list = field(default_factory=list)
    blocks_done: int = 0
    sampled: int = 0
    requests_made: int = 0
    branches: int = 0
    prefix_end: int = 0    # len(ids) after </Plan> of the open block


class GraphSampler:
    """Runs many trajectories stage by stage; each round batches every pending call of every live sample.

    causal_backend: any backend (VLLMBackend or HFBackend) for calls whose context has no finished block;
    graph_backend: an HFBackend for calls that need the graph mask. force: test hook
    force(sample_index, stage, block, path) -> token list (used instead of sampling) or None.
    """

    def __init__(self, tokenizer, causal_backend, graph_backend=None, sampling=None, max_blocks=1, budget=16384,
                 branch_cap=4096, plan_cap=256, force: Optional[Callable] = None):
        if not 0 <= max_blocks <= contract.MAX_BLOCKS:
            raise ValueError(f'max_blocks must be in 0..{contract.MAX_BLOCKS}')
        self.tokenizer = tokenizer
        self.causal = causal_backend
        self.graph = graph_backend if graph_backend is not None else causal_backend
        if not getattr(self.graph, 'graph', False):
            raise ValueError('graph_backend must support graph masks (HFBackend)')
        self.sampling = sampling or Sampling()
        self.max_blocks, self.budget, self.branch_cap, self.plan_cap = max_blocks, budget, branch_cap, plan_cap
        self.force = force
        self.ids = contract.token_ids(tokenizer)
        self.counts = contract.count_ids(tokenizer)
        self.branches_ids = contract.branches_ids(tokenizer)
        self.eos = eos_ids(tokenizer)
        self.tag = {tag: self.ids[tag] for tag in contract.TAGS}

    # -- public

    def generate(self, prompts, seeds=None, allow_parallel=True, prompt_ids=None):
        """prompts: user messages (chat template applied here) or, with prompt_ids, ready token lists."""
        if prompt_ids is None:
            prompt_ids = [chat_prompt_ids(self.tokenizer, prompt) for prompt in prompts]
        seeds = list(range(len(prompt_ids))) if seeds is None else list(seeds)
        trajectories = [Trajectory(i, seeds[i], list(ids), len(ids), allow_parallel)
                        for i, ids in enumerate(prompt_ids)]
        while True:
            pending = []
            for trajectory in trajectories:
                if trajectory.status is None:
                    pending.append((trajectory, self.requests(trajectory)))
            if not pending:
                break
            self.run(pending)
        return [self.report(t) for t in trajectories]

    # -- stages

    def node_of_main(self, t):
        return contract.main_node(t.blocks_done, self.max_blocks, t.allow_parallel)

    def room(self, t):
        return self.budget - t.sampled

    def request(self, t, context, node, stop, max_tokens):
        t.requests_made += 1
        seed = (t.seed * 1_000_003 + t.requests_made * 7919) % (2 ** 31)
        return Request(list(context), node, tuple(stop), max_tokens, seed,
                       contract.sampling_constraint(node, self.ids, self.counts), tuple(t.spans))

    def requests(self, t):
        """[(stage, block, path, Request)] for the trajectory's current stage."""
        block = t.blocks_done + 1
        if t.stage == 'main':
            node = self.node_of_main(t)
            stop = ([self.tag['<Parallel>']] if node == contract.MAIN_OPEN else []) + list(self.eos)
            return [('main', block, None, self.request(t, t.ids, node, stop, self.room(t)))]
        if t.stage == 'count':
            return [('count', block, None, self.request(t, t.ids, contract.COUNT, (), min(1, self.room(t))))]
        if t.stage == 'plan':
            stop = [self.tag['</Plan>'], *self.eos]
            return [('plan', block, None,
                     self.request(t, t.ids, contract.PLAN, stop, min(self.plan_cap, self.room(t))))]
        if t.stage == 'paths':
            stop = [self.tag['</Path>'], *self.eos]
            cap = min(self.branch_cap, self.room(t))
            prefix = t.ids[:t.prefix_end]
            return [('path', block, i, self.request(
                t, prefix + [self.tag['<Path>']] + contract.path_prefix_ids(self.tokenizer, i), contract.PATH, stop,
                cap)) for i in range(1, t.branches + 1)]
        if t.stage == 'summary':
            stop = [self.tag['</Summary>'], *self.eos]
            return [('summary', block, None, self.request(t, t.ids, contract.SUMMARY, stop, self.room(t)))]
        raise AssertionError(t.stage)

    def run(self, pending):
        causal, graph, results = [], [], {}
        for trajectory, calls in pending:
            for k, (stage, block, path, request) in enumerate(calls):
                forced = self.force(trajectory.index, stage, block, path) if self.force else None
                if forced is not None:
                    results[trajectory.index, k] = Result(list(forced)[:max(request.max_tokens, 0)])
                elif request.spans:
                    graph.append(((trajectory.index, k), request))
                else:
                    causal.append(((trajectory.index, k), request))
        for backend, group in ((self.causal, causal), (self.graph, graph)):
            if group:
                for (key, _), result in zip(group, backend.generate([r for _, r in group], self.sampling)):
                    results[key] = result
        for trajectory, calls in pending:
            self.advance(trajectory, [(c, results[trajectory.index, k]) for k, c in enumerate(calls)])

    def stop_of(self, tokens, close, max_tokens):
        if tokens and close is not None and tokens[-1] == close:
            return 'close'
        if tokens and tokens[-1] in self.eos:
            return 'eos'
        return 'budget'

    def written(self, tokens, stop, close):
        """As the RL loop writes a segment: a sampled EOS becomes the closing tag, a cut gets an inserted one."""
        tokens = list(tokens)
        if stop == 'eos':
            tokens[-1] = close
        return tokens + [close] if stop == 'budget' else tokens

    def advance(self, t, outcomes):
        (stage, block, _, request), result = outcomes[0]
        tokens = result.tokens
        if stage == 'main':
            if request.max_tokens < 1:
                t.status = TRAJECTORY_BUDGET
                return
            t.calls.append(dict(node=request.node, block=None, sampled=len(tokens)))
            t.sampled += len(tokens)
            t.ids += tokens
            if tokens and tokens[-1] in self.eos:
                t.status = COMPLETE
            elif tokens and tokens[-1] == self.tag['<Parallel>'] and request.node == contract.MAIN_OPEN:
                t.blocks.append(dict(block=block, start=len(t.ids) - 1, N=None, kind=None, items=None,
                                     plan_status=None, plan_tokens=0, branches=[], summary_tokens=None,
                                     summary_stop=None))
                t.ids += self.branches_ids
                t.stage = 'count'
            else:
                t.status = TRAJECTORY_BUDGET
            return
        record = t.blocks[-1]
        if stage == 'count':
            if request.max_tokens < 1:
                t.status = record['plan_status'] = contract.PLAN_BUDGET_EXHAUSTED
                return
            t.calls.append(dict(node=contract.COUNT, block=block, sampled=len(tokens)))
            t.sampled += len(tokens)
            t.ids += tokens
            if len(tokens) != 1 or tokens[0] not in self.counts:
                raise RuntimeError(f'COUNT sampled {tokens}, outside {self.counts}')
            t.branches = record['N'] = contract.MIN_PATHS + self.counts.index(tokens[0])
            t.ids += [self.tag[tag] for tag in contract.PLAN_OPEN]
            t.stage = 'plan'
            return
        if stage == 'plan':
            if request.max_tokens < 1:
                t.status = record['plan_status'] = contract.PLAN_BUDGET_EXHAUSTED
                return
            close = self.tag['</Plan>']
            stop = self.stop_of(tokens, close, request.max_tokens)
            t.calls.append(dict(node=contract.PLAN, block=block, sampled=len(tokens)))
            t.sampled += len(tokens)
            t.ids += tokens
            text = self.tokenizer.decode(tokens[:-1] if stop == 'close' else tokens, skip_special_tokens=False)
            status = contract.plan_status(text, stop, t.branches)
            record.update(plan_status=status, plan_tokens=len(tokens), plan_text=text)
            if status != contract.VALID:
                t.status = status
                return
            plan = contract.parse_plan(text, t.branches)
            record.update(kind=plan.kind, items=list(plan.items))
            t.prefix_end = len(t.ids)
            t.stage = 'paths'
            return
        if stage == 'path':
            close = self.tag['</Path>']
            spans = []
            for (_, _, path, request), result in outcomes:
                tokens = result.tokens
                stop = self.stop_of(tokens, close, request.max_tokens)
                reason = stop
                if stop == 'budget':
                    reason = 'cap' if request.max_tokens >= 1 and request.max_tokens == self.branch_cap else 'budget'
                if request.max_tokens >= 1:
                    t.calls.append(dict(node=contract.PATH, block=block, sampled=len(tokens)))
                t.sampled += len(tokens)
                start = len(t.ids)
                t.ids += [self.tag['<Path>']] + contract.path_prefix_ids(self.tokenizer, path)
                t.ids += self.written(tokens, stop, close)
                spans.append(contract.Span(start, len(t.ids), block, path))
                record['branches'].append(dict(path=path, sampled=len(tokens), stop=reason))
            t.spans += spans
            t.ids += [self.tag[tag] for tag in contract.BLOCK_CLOSE]
            t.stage = 'summary'
            return
        if stage == 'summary':
            t.blocks_done += 1
            if request.max_tokens < 1:
                t.status = TRAJECTORY_BUDGET
                return
            close = self.tag['</Summary>']
            stop = self.stop_of(tokens, close, request.max_tokens)
            t.calls.append(dict(node=contract.SUMMARY, block=block, sampled=len(tokens)))
            t.sampled += len(tokens)
            t.ids += self.written(tokens, stop, close)
            record.update(summary_tokens=len(tokens), summary_stop=stop)
            if stop == 'budget':
                t.status = TRAJECTORY_BUDGET
                return
            t.stage = 'main'
            return
        raise AssertionError(stage)

    # -- output

    def report(self, t):
        tokenizer = self.tokenizer
        response = t.ids[t.prompt_len:]
        text = tokenizer.decode(response, skip_special_tokens=False)
        depth, tokens = contract.depth_and_tokens(t.calls)
        return dict(index=t.index, seed=t.seed, status=t.status, mode='graph' if t.allow_parallel else 'sequential',
                    prompt_len=t.prompt_len, prompt_ids=t.ids[:t.prompt_len], token_ids=response, text=text, answer=final_answer(text),
                    blocks=[{k: v for k, v in b.items() if k != 'start'} for b in t.blocks],
                    spans=[[s.start - t.prompt_len, s.end - t.prompt_len, s.block, s.path] for s in t.spans],
                    calls=t.calls, D=depth, T=tokens, forked=bool(t.blocks),
                    truncated=t.status == TRAJECTORY_BUDGET)


def final_answer(text):
    """Text after the last </think>, without chat control tokens; None if thinking never closed."""
    end = text.rfind('</think>')
    if end < 0:
        return None
    answer = text[end + len('</think>'):]
    for token in EOS_TOKENS + ('<|im_start|>',):
        answer = answer.replace(token, '')
    return answer.strip()


def serialized_spans(report):
    """contract.Span list of a report in full-sequence coordinates (prompt included)."""
    offset = report['prompt_len']
    return [contract.Span(s + offset, e + offset, b, p) for s, e, b, p in report['spans']]
