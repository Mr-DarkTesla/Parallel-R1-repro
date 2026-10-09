"""GPU check of graph rollout (agent.graph_rollout; verl/verl/parallel_thinking_generation_v3/vllm_graph.py).

Runs trajectories through the agent loop's graph-rollout requests against vLLM 0.8.5 started with vllm_graph's
scheduler and worker, then scores every sampled token with HF transformers (float32) under the contract's graph
mask and positions, which is what the actor scores with (logprob_context=tree). vLLM V1 reports log-probs of the
raw logits (before logit_bias, allowed_token_ids and temperature), so every forward uses raw log_softmax too.
Graph rollout is right when vLLM matches the graph forward up to bf16 noise for every kind of token, notably
the second and later branches, summaries and text after a block, which only see merged KV at graph positions.
Two contrasts show what an error would look like: the graph mask at physical positions (RoPE offsets not
applied) and a plain causal forward (flat context, no branch isolation).

  forced (default)  each trajectory has a fixed structure, two blocks of 2 and 3 branches with a written
                    plan; vLLM samples the text of every main, branch and summary segment freely. Needs only
                    single-token tags (check_checkpoint.py --plan), so a smoke model works.
  --loop            the real agent loop (protocol=plan) on a few questions; informative only if the model
                    writes valid plans (the thinking SFT checkpoint), otherwise it never forks.

--blocks N shrinks vLLM's KV cache to N blocks (of 16 tokens) so that held branch KV fills it: requests are
preempted, trajectories evicted and rebuilt (graph_kv.py), and the log-probs must still match.

  VLLM_USE_V1=1 python experiments/qwen06/check_graph_rollout.py MODEL_DIR [--trajectories 16] [--blocks 160]
  VLLM_USE_V1=1 python experiments/qwen06/check_graph_rollout.py MODEL_DIR --loop [--response-length 4096]

Prints a table per segment (mean and max |vLLM - forward| in nats), writes --out (JSON), exits 1 on failure.
"""
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'verl'))

import torch  # noqa: E402

from verl.parallel_thinking_generation_v3 import contract, graph_kv  # noqa: E402

QUESTIONS = [
    'A bakery sells muffins for $3 each and cookies for $2 each. Mia buys 4 muffins and some cookies and pays $22. '
    'How many cookies did she buy?',
    'Find all real x with x^2 - 5x + 6 = 0.',
    'What is the remainder when 2^20 is divided by 7?',
    'A rectangle has perimeter 30 and area 56. What are its side lengths?',
    'How many positive divisors does 360 have?',
    'Evaluate the polynomial p(x) = x^3 - 2x + 1 at x = -1, 0, 1 and 2.',
    'Tom is twice as old as Ann. In 6 years he will be 1.5 times as old as she will be. How old is Ann?',
    'Is 221 a prime number?',
]

FORWARDS = ('graph', 'graph_mask_physical_positions', 'causal')  # the actor's context, then two wrong ones
FORCED_BLOCKS = [('cases', ['n is even', 'n is odd']),
                 ('candidates', ['try x = 1', 'try x = 2', 'try x = 3'])]


def agent_config(prompt_length, response_length, path_length):
    agent = SimpleNamespace(add_diverse_prefix=False, max_iterations_for_parallel_thinking=2, num_paths=2,
                            max_path_response_length=path_length, logprob_context='tree', rollout_logprobs=True,
                            protocol='plan', max_plan_tokens=256, allow_parallel=True, graph_rollout=True,
                            enable_thinking=True)
    return SimpleNamespace(actor_rollout_ref=SimpleNamespace(rollout=SimpleNamespace(
        prompt_length=prompt_length, response_length=response_length, agent=agent)))


class Server:
    """AsyncvLLMServer.generate / release (verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py) on a
    local AsyncLLM; one server, so routing keys are ignored."""

    def __init__(self, engine, max_model_len):
        self.engine, self.max_model_len, self.graph = engine, max_model_len, graph_kv.Registry()
        self.evicted = 0

    async def generate(self, request_id, *, prompt_ids, sampling_params, routing_key=None, return_logprobs=False,
                       graph=None):
        from vllm import SamplingParams
        from vllm.inputs import TokensPrompt
        params = dict(sampling_params)
        max_tokens = min(params.pop('max_tokens', self.max_model_len), self.max_model_len - len(prompt_ids))
        if max_tokens <= 0:
            return dict(token_ids=[], logprobs=[]) if return_logprobs else []
        if return_logprobs:
            params['logprobs'] = 0
        if graph is not None:
            self.graph.validate(graph, len(prompt_ids))
            params['extra_args'] = {graph_kv.GRAPH_KEY: graph}
        final = None
        async for output in self.engine.generate(prompt=TokensPrompt(prompt_token_ids=list(prompt_ids)),
                                                 sampling_params=SamplingParams(max_tokens=max_tokens, **params),
                                                 request_id=request_id):
            final = output
        completion = final.outputs[0]
        result = dict(token_ids=list(completion.token_ids))
        if return_logprobs:
            result['logprobs'] = [step[token].logprob for step, token in zip(completion.logprobs, completion.token_ids)]
        if graph is None:
            return result if return_logprobs else result['token_ids']
        if completion.stop_reason == graph_kv.GRAPH_TOO_LARGE:
            raise RuntimeError('graph rollout: a trajectory needs more KV than the cache has')
        result['graph_evicted'] = completion.stop_reason == graph_kv.GRAPH_EVICTED
        self.evicted += result['graph_evicted']
        if not result['graph_evicted']:
            self.graph.finished(request_id, graph, len(prompt_ids), len(completion.token_ids))
        return result

    async def release(self, request_ids, routing_key=None):
        held = self.graph.release(request_ids)
        if held:
            await self.engine.engine_core.abort_requests_async(held)


def bare_loop(loop_class, server, name):
    """A loop instance whose graph-rollout helpers (_generate, _seal, _release) can be called directly."""
    from verl.parallel_thinking_generation_v3.repro_trace import Trace
    loop = loop_class.__new__(loop_class)
    loop.server_manager, loop.loop = server, asyncio.get_running_loop()
    loop.held, loop.routing_key = {}, uuid4().hex
    loop.graph_key = graph_kv.trajectory_key(time.time(), name)
    loop.trace = Trace(dict(check=name), 0)
    return loop


async def forced_trajectory(loop, prompt, lengths, blocks=FORCED_BLOCKS):
    """One trajectory with the structure `blocks`, made of the requests the agent loop makes in graph rollout:
    main text; per block a held request for the shared prefix through </Plan> (what the count and plan requests
    leave), each branch from it, a seal per branch, the summary on the merged branch KV; main text after it.
    vLLM samples every segment freely (tags suppressed, EOS ignored); the structure is written here.

    Returns the tokens, the branch spans and, per sampled token, (index, token, vLLM log-prob, segment), where
    index is the token's place in the tokens (branch n follows branches 1..n-1 there; its own request had only
    the shared prefix before it)."""
    ids, tokenizer = loop.tag_ids, loop.tokenizer
    free = dict(temperature=1.0, top_p=1.0, n=1, ignore_eos=True, stop_token_ids=[],
                logit_bias=contract.logit_bias(contract.MAIN_CLOSED, ids))
    tokens, spans, sampled = list(prompt), [], []
    chain, offset = None, 0

    async def sample(segment, prompt_ids, max_tokens, parent, offset):
        return await loop._generate(segment, uuid4().hex, list(prompt_ids), {**free, 'max_tokens': max_tokens},
                                    parent, offset)

    def record(start, segment, out, log_probs):
        sampled.extend((start + k, token, log_prob, segment) for k, (token, log_prob) in enumerate(zip(out, log_probs)))

    for block, (kind, items) in enumerate(blocks):
        segment = 'main_before_fork' if block == 0 else 'main_after_fork'
        out, log_probs, handle = await sample(segment, tokens, lengths['main'], chain, offset)
        record(len(tokens), segment, out, log_probs)
        tokens += out
        await loop._release(chain)
        chain = handle
        plan = f'{kind}\n' + ''.join(f'{number}: {item}\n' for number, item in enumerate(items, 1))
        base = tokens + [ids['<Parallel>'], *loop.branches_ids, loop.count_ids[len(items) - contract.MIN_PATHS],
                         ids['<Plan>'], *tokenizer.encode(plan, add_special_tokens=False), ids['</Plan>']]
        shared = await loop._seal(base, chain, offset)

        async def branch(number):
            prefix = [ids['<Path>']] + contract.path_prefix_ids(tokenizer, number)
            out, log_probs, handle = await sample('path', base + prefix, lengths['path'], shared, offset)
            seal = await loop._seal(base + prefix + out + [ids['</Path>']], handle, offset)
            await loop._release(handle)
            return prefix, out, log_probs, seal

        branches = await asyncio.gather(*[branch(number) for number in range(1, len(items) + 1)])
        tokens, lengths_in_block = list(base), []
        for number, (prefix, out, log_probs, _) in enumerate(branches, 1):
            record(len(tokens) + len(prefix), f"path{'1' if number == 1 else '2+'}_block{block + 1}", out, log_probs)
            written = prefix + out + [ids['</Path>']]
            spans.append(contract.Span(len(tokens), len(tokens) + len(written), block, number))
            lengths_in_block.append(len(written))
            tokens += written
        seals = [seal for *_, seal in branches]
        offset = graph_kv.merged_offset(offset, lengths_in_block)
        tokens += [ids['</Parallel>'], ids['<Summary>']]
        out, log_probs, handle = await sample('summary', tokens, lengths['summary'], graph_kv.merge(seals, len(base)),
                                              offset)
        record(len(tokens), f'summary_block{block + 1}', out, log_probs)
        tokens += out + [ids['</Summary>']]
        await loop._release(seals + [shared, chain])
        chain = handle
    out, log_probs, handle = await sample('main_after_fork', tokens, lengths['main'], chain, offset)
    record(len(tokens), 'main_after_fork', out, log_probs)
    tokens += out
    await loop._release([chain, handle])
    assert not loop.held, loop.held
    return tokens, spans, sampled


def branch_spans(tokens, parallel, path, end_path):
    """contract.Span of every branch (<Path> through </Path>) as the agent loop records them: a branch cut by the
    response limit ends at len(tokens)."""
    spans, block, number, start = [], -1, 0, None
    for index, token in enumerate(tokens):
        if token == parallel:
            block, number = block + 1, 0
        elif token == path:
            start, number = index, number + 1
        elif token == end_path and start is not None:
            spans.append(contract.Span(start, index + 1, block, number))
            start = None
    if start is not None:
        spans.append(contract.Span(start, len(tokens), block, number))
    return spans


async def loop_trajectory(loop_class, server, tokenizer, config, question, name):
    """The real agent loop (AgentLoopBase.__init__ and run) on one question: tokens, branch spans, sampled tokens
    (as in forced_trajectory; a sampled EOS the loop wrote as a closing tag is scored as EOS) and the status."""
    from verl.parallel_thinking_generation_v3.logprob_gap import SEGMENTS
    loop = loop_class(SimpleNamespace(config=config), server, tokenizer)
    loop.trajectory = dict(check=name)
    result = await loop.run([{'role': 'user', 'content': question}], dict(temperature=1.0, top_p=1.0))
    prompt, response = list(result.prompt_ids), list(result.response_ids)
    tokens = prompt + response
    labels = dict(result.label_overrides)
    sampled = [(len(prompt) + j, labels.get(j, token), log_prob, SEGMENTS[segment])
               for j, (token, keep, log_prob, segment) in enumerate(zip(response, result.response_mask,
                                                                         result.rollout_log_probs,
                                                                         result.rollout_segments))
               if keep and segment >= 0]
    tags = loop.tag_ids
    spans = branch_spans(tokens, tags['<Parallel>'], tags['<Path>'], tags['</Path>'])
    pad = config.actor_rollout_ref.rollout.prompt_length - len(prompt)
    positions = result.multiverse_pos_ids[pad:pad + len(tokens)]
    assert positions.tolist() == contract.graph_positions(len(tokens), spans), 'loop positions differ from the contract'
    return tokens, spans, sampled, result.repro_stats['trajectory_status']


@torch.no_grad()
def score(model, tokens, spans, rows_labels):
    """Raw log-probs of each (row, label) under three forwards: graph mask and positions, graph mask at physical
    positions, plain causal."""
    device = next(model.parameters()).device
    length = len(tokens)
    input_ids = torch.tensor([tokens], device=device)
    physical = torch.arange(length, device=device)[None]
    graph = torch.tensor([contract.graph_positions(length, spans)], device=device)
    graph_mask = contract.graph_attention_mask(length, spans, device=device)
    causal = torch.ones(length, length, dtype=torch.bool, device=device).tril()
    rows = torch.tensor([row for row, _ in rows_labels], device=device)
    labels = torch.tensor([label for _, label in rows_labels], device=device)
    out = {}
    for name, mask, positions in zip(FORWARDS, [graph_mask, graph_mask, causal], [graph, physical, physical]):
        additive = torch.zeros(length, length, dtype=model.dtype, device=device).masked_fill(
            ~mask, torch.finfo(model.dtype).min)  # HF's convention for an inverted 4D mask
        hidden = model.model(input_ids=input_ids, attention_mask=additive[None, None], position_ids=positions,
                             use_cache=False).last_hidden_state[0]
        log_probs = model.lm_head(hidden[rows]).float().log_softmax(-1)
        out[name] = log_probs.gather(-1, labels[:, None])[:, 0].tolist()
    return out


def report(rows, tolerance):
    """Per segment (in order of appearance) and overall: tokens, mean and max |vLLM - forward| for each forward;
    a segment is ok if the graph forward is within tolerance on average."""
    table, ok = {}, True
    for segment in list(dict.fromkeys(row['segment'] for row in rows)) + ['all']:
        group = [row for row in rows if segment in ('all', row['segment'])]
        entry = dict(tokens=len(group))
        for name in FORWARDS:
            errors = [abs(row['vllm'] - row[name]) for row in group]
            entry[name] = dict(mean=sum(errors) / len(errors), max=max(errors))
        entry['ok'] = entry['graph']['mean'] <= tolerance
        ok &= entry['ok']
        table[segment] = entry
    return table, ok


async def run(args):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.v1.engine.async_llm import AsyncLLM
    from verl.parallel_thinking_generation_v3 import vllm_graph
    from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3 as Loop

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    prompt_length = 1024
    response_length = args.response_length if args.loop else 1024
    path_length = args.path_length or (1024 if args.loop else 40)
    config = agent_config(prompt_length, response_length, path_length)
    Loop.init_class(config, tokenizer)  # checks the eight tags and the branch counts are single tokens
    max_model_len = prompt_length + response_length + 64
    engine = AsyncLLM.from_engine_args(AsyncEngineArgs(
        model=str(args.model), dtype='bfloat16', max_model_len=max_model_len, seed=args.seed,
        gpu_memory_utilization=args.gpu_memory_utilization, num_gpu_blocks_override=args.blocks,
        enable_prefix_caching=True, enable_chunked_prefill=True, enforce_eager=not args.cuda_graphs,
        disable_log_stats=True, scheduler_cls=vllm_graph.SCHEDULER, worker_cls=vllm_graph.WORKER))
    server = Server(engine, max_model_len)
    started = time.time()
    try:
        if args.loop:
            questions = (QUESTIONS * args.trajectories)[:args.trajectories]
            results = await asyncio.gather(*[loop_trajectory(Loop, server, tokenizer, config, question, f'q{index}')
                                             for index, question in enumerate(questions)])
            statuses = [status for *_, status in results]
            trajectories = [result[:3] for result in results]
        else:
            lengths = dict(main=args.main_length, path=path_length, summary=args.summary_length)

            async def one(index):
                question = QUESTIONS[index % len(QUESTIONS)]
                prompt = tokenizer.apply_chat_template([{'role': 'user', 'content': question}],
                                                       add_generation_prompt=True, tokenize=True, enable_thinking=True)
                return await forced_trajectory(bare_loop(Loop, server, f'forced{index}'), prompt, lengths)
            trajectories = await asyncio.gather(*[one(index) for index in range(args.trajectories)])
            statuses = ['ok'] * len(trajectories)
        rollout_seconds = time.time() - started
        leaked = dict(server.graph.held)
    finally:
        engine.shutdown()

    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float32,
                                                 attn_implementation='sdpa').to('cuda').eval()
    rows = []
    for tokens, spans, sampled in trajectories:
        forwards = score(model, tokens, spans, [(index - 1, token) for index, token, _, _ in sampled])
        for k, (index, token, log_prob, segment) in enumerate(sampled):
            rows.append(dict(segment=segment, vllm=log_prob, **{name: values[k] for name, values in forwards.items()}))
    table, ok = report(rows, args.tolerance)
    forks = sum(len({span.block for span in spans}) for _, spans, _ in trajectories)
    checks = dict(no_held_kv_left=not leaked, forked=forks > 0)
    ok &= all(checks.values())
    summary = dict(ok=ok, mode='loop' if args.loop else 'forced', trajectories=len(trajectories), blocks=forks,
                   statuses={status: statuses.count(status) for status in set(statuses)}, evicted_requests=server.evicted,
                   kv_blocks=args.blocks, rollout_seconds=round(rollout_seconds, 1), tolerance=args.tolerance,
                   checks=checks, segments=table)
    print(f"{'segment':<20}{'tokens':>8}  {'graph':>15}  {'graph@physical':>15}  {'causal':>15}   mean / max |vLLM - HF|")
    for segment, entry in table.items():
        cells = '  '.join(f"{entry[name]['mean']:7.4f}/{entry[name]['max']:7.3f}" for name in FORWARDS)
        print(f"{segment:<20}{entry['tokens']:>8}  {cells}   {'ok' if entry['ok'] else 'FAIL'}")
    print(json.dumps({key: value for key, value in summary.items() if key != 'segments'}, indent=1))
    if args.out:
        args.out.write_text(json.dumps(summary, indent=1))
    return ok


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('model', type=Path, help='HF model directory with the contract tags (check_checkpoint --plan)')
    parser.add_argument('--loop', action='store_true', help='run the real agent loop instead of forced blocks')
    parser.add_argument('--trajectories', type=int, default=16)
    parser.add_argument('--blocks', type=int, default=None, help='KV cache size in blocks of 16 tokens (stress)')
    parser.add_argument('--main-length', type=int, default=48)
    parser.add_argument('--path-length', type=int, help='branch length: forced 40, --loop max_path_response_length 1024')
    parser.add_argument('--summary-length', type=int, default=24)
    parser.add_argument('--response-length', type=int, default=4096, help='--loop only')
    parser.add_argument('--gpu-memory-utilization', type=float, default=0.4)
    parser.add_argument('--cuda-graphs', action='store_true', help='vLLM with CUDA graphs (run_rl.sh uses eager)')
    parser.add_argument('--tolerance', type=float, default=0.05, help='max mean |vLLM - graph forward| per segment')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    # vLLM imports the scheduler and worker classes by name in its engine-core and worker processes.
    os.environ['PYTHONPATH'] = os.pathsep.join(filter(None, [str(ROOT / 'verl'), os.environ.get('PYTHONPATH')]))
    os.environ.setdefault('VLLM_USE_V1', '1')
    # A forked engine core fails here with "Cannot re-initialize CUDA in forked subprocess" (H100 VM,
    # 2026-10-09); verl's servers run in Ray actors, where vLLM spawns it anyway.
    os.environ.setdefault('VLLM_WORKER_MULTIPROC_METHOD', 'spawn')
    sys.exit(0 if asyncio.run(run(args)) else 1)


if __name__ == '__main__':
    main()
