# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import json
import logging
import os
import time
from typing import Any
from uuid import uuid4
import random
from verl.parallel_thinking_generation_v3.agent_loop import AgentLoopBase, AgentLoopOutput, register
from verl.utils.rollout_trace import rollout_trace_op
import copy
from contextlib import contextmanager
from typing import Dict, Optional, Type
from codetiming import Timer
import torch
from verl.parallel_thinking_generation_v3.repro_trace import Trace, TOKENS
from verl.parallel_thinking_generation_v3.logprob_gap import (MAIN_AFTER, MAIN_BEFORE, PATH_FIRST, PATH_LATER,
                                                              PLAN_FIRST, PLAN_LATER, SUMMARY_FIRST, SUMMARY_LATER)
from verl.parallel_thinking_generation_v3 import contract, graph_kv
logger = logging.getLogger(__file__)
logger.setLevel(os.getenv("VERL_LOGGING_LEVEL", "WARN"))


@contextmanager
def _timer(name: str, timing_raw: Dict[str, float]):
    """Context manager for timing code execution.

    This utility function measures the execution time of code within its context
    and accumulates the timing information in the provided dictionary.

    Args:
        name (str): The name/identifier for this timing measurement.
        timing_raw (Dict[str, float]): Dictionary to store timing information.

    Yields:
        None: This is a context manager that yields control back to the code block.
    """
    with Timer(name=name, logger=None) as timer:
        yield
    if name not in timing_raw:
        timing_raw[name] = 0
    timing_raw[name] += timer.last

def test_mask(mask: torch.Tensor, position_ids: torch.Tensor, start: int, end: int) -> bool:
    """Test if the mask is valid for the given position range."""
    if start < 0 or end > mask.size(0):
        return False
    return mask[start:end, start:end].all().item()



@register("parallel_thinking_agent_v3")
class ParallelThinkingAgentLoopV3(AgentLoopBase):
    graph_attempts = 10000  # graph rollout: a request evicted this often in a row is a bug, not memory pressure

    @staticmethod
    def eos_ids(tokenizer):
        """Every id vLLM ends a request on as EOS: the tokenizer's eos_token_id and the eos_token_id of the
        model's generation_config.json, which vLLM adds as stops (Qwen3-0.6B: <|im_end|> and <|endoftext|>)."""
        ids = [tokenizer.eos_token_id]
        path = getattr(tokenizer, 'name_or_path', None)
        if path:
            from transformers import GenerationConfig
            try:
                extra = GenerationConfig.from_pretrained(path, local_files_only=True).eos_token_id
            except OSError:  # no generation_config.json next to the tokenizer
                extra = None
            ids += list(extra) if isinstance(extra, (list, tuple)) else [extra]
        return tuple(dict.fromkeys(i for i in ids if i is not None))

    @classmethod
    def init_class(cls, config, tokenizer, **kwargs):
        if cls._class_initialized:
            return
        cls._class_initialized = True
        print("Performing class-level ParallelThinkingV3AgentLoop initialization")

        # Initialize tools from config file
        cls.tokenizer = tokenizer
        encoded = [tokenizer.encode(t, add_special_tokens=False) for t in TOKENS]
        if any(len(ids) != 1 for ids in encoded) or len({ids[0] for ids in encoded}) != 6:
            raise ValueError('SFT tokenizer must contain all six distinct single-token Parallel-R1 tags')
        cls.add_diverse_prefix = config.actor_rollout_ref.rollout.agent.add_diverse_prefix
        cls.max_iterations_for_parallel_thinking = config.actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking
        cls.num_paths = config.actor_rollout_ref.rollout.agent.num_paths
        cls.max_path_response_length = config.actor_rollout_ref.rollout.agent.max_path_response_length
        # tree: upstream objective (Unseen mask + multiverse positions), which differs from the
        # contexts vLLM samples summaries and later blocks in. flat_packed: the actor scores every
        # sampled token in the causal context and positions of the vLLM call that produced it.
        cls.logprob_context = getattr(config.actor_rollout_ref.rollout.agent, 'logprob_context', 'tree')
        if cls.logprob_context not in ('tree', 'flat_packed'):
            raise ValueError(f'Unknown logprob_context {cls.logprob_context!r}; use tree or flat_packed')
        cls.rollout_logprobs = bool(getattr(config.actor_rollout_ref.rollout.agent, 'rollout_logprobs', False))
        # None keeps the chat template's default; Qwen3 thinks unless enable_thinking is false.
        cls.enable_thinking = getattr(config.actor_rollout_ref.rollout.agent, 'enable_thinking', None)
        # false: sequential baseline, <Parallel> is never sampled.
        cls.allow_parallel = bool(getattr(config.actor_rollout_ref.rollout.agent, 'allow_parallel', True))
        # legacy: upstream blocks of num_paths branches. plan: the shared contract (contract.py), where the
        # model samples branches=N after <Parallel> and then a plan of N lines, and every node suppresses
        # the tags it may not sample.
        cls.protocol = getattr(config.actor_rollout_ref.rollout.agent, 'protocol', 'legacy')
        if cls.protocol not in ('legacy', 'plan'):
            raise ValueError(f'Unknown protocol {cls.protocol!r}; use legacy or plan')
        cls.max_plan_tokens = int(getattr(config.actor_rollout_ref.rollout.agent, 'max_plan_tokens', 256))
        # graph_rollout (protocol=plan): vLLM samples every token in its contract graph context (sibling branches
        # isolated, graph positions) by keeping branch KV and merging it (vllm_graph.py), so the actor scores
        # with the same graph positions and mask (logprob_context=tree).
        cls.graph_rollout = bool(getattr(config.actor_rollout_ref.rollout.agent, 'graph_rollout', False))
        if cls.graph_rollout and (cls.protocol != 'plan' or cls.logprob_context != 'tree'):
            raise ValueError('graph_rollout needs protocol=plan and logprob_context=tree')
        if cls.protocol == 'plan':
            cls.tag_ids = contract.token_ids(tokenizer)  # the tags and the control tokens nodes suppress
            cls.count_ids = contract.count_ids(tokenizer)
            cls.branches_ids = contract.branches_ids(tokenizer)
            cls.graph_tags = tuple(cls.tag_ids[tag] for tag in ('<Parallel>', '</Parallel>', '<Path>', '</Path>'))

        cls.eos_token_id = cls.tokenizer.eos_token_id
        # protocol=plan: a node that samples any of these ends on EOS (plan incomplete, closing tag written).
        cls.eos_token_ids = cls.eos_ids(cls.tokenizer)
        cls.start_parallel_token = cls.tokenizer.encode('<Parallel>')[0]
        cls.end_parallel_token = cls.tokenizer.encode('</Parallel>')[0]
        cls.start_path_token = cls.tokenizer.encode('<Path>')[0]
        cls.end_path_token = cls.tokenizer.encode('</Path>')[0]
        cls.start_summary_token = cls.tokenizer.encode('<Summary>')[0]
        cls.end_summary_token = cls.tokenizer.encode('</Summary>')[0]
        cls.new_line_token = cls.tokenizer.encode('\n')

        cls.prompt_length = config.actor_rollout_ref.rollout.prompt_length
        cls.response_length = config.actor_rollout_ref.rollout.response_length
        cls.system_prompt = []

    @rollout_trace_op
    async def run(
        self,
        messages: list[dict[str, Any]],
        sampling_params: dict[str, Any],
    ) -> AgentLoopOutput:
        self.held = {}  # graph rollout: request id -> Handle kept on the server until released
        # graph rollout: orders this trajectory by age on the server (self.trajectory is the trace's metadata)
        self.graph_key = graph_kv.trajectory_key(time.time(), uuid4().hex)
        try:
            return await self._run(messages, sampling_params)
        finally:
            if self.held:
                await self._release(list(self.held.values()))

    async def _run(self, messages, sampling_params):

        
        prompt_ids = await self.loop.run_in_executor(
            None,
            lambda: self.tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=True,
                **({} if self.enable_thinking is None else {'enable_thinking': self.enable_thinking}),
            ),
        )
        init_len      = len(prompt_ids)
        if init_len > self.prompt_length:
            raise ValueError(f'Prompt has {init_len} tokens; limit is {self.prompt_length}. Filter data before rollout.')
        self.trace = Trace(getattr(self, 'trajectory', {}), init_len)
        self.trace.record['messages'] = messages
        self.trace.record['prompt_ids'] = list(prompt_ids)
        position_ids  = torch.arange(init_len, dtype=torch.long)
        # Every call of this trajectory goes to one server, which holds its prefix cache.
        self.routing_key = uuid4().hex

        response_mask = []                                     
        # Per response token: rollout segment (-1 for injected tags) and vLLM log-prob.
        rollout_segments, rollout_log_probs = [], []
        forced, label_overrides, replay_segments = [], [], []
        # Sampled tokens on the longest chain (main + longest path + summary per block) and in total;
        # tags the runtime inserted count in neither.
        critical_depth = sampled_tokens = 0
        iterations    = 0
        request_id    = uuid4().hex

        left_pad_len = self.prompt_length - init_len
        if left_pad_len < 0:
            print(f"Warning: prompt length {self.prompt_length} is less than initial prompt length {init_len}, truncating prompt.")
            left_pad_len = 0

        position_required_masks = []

        
        parallel_stack: list[dict] = []

        
        def append_tokens(new_ids: list[int],
                        is_parallel: bool = False,
                        path_spans: list[tuple[int, int]] | None = None, manual_mask_positions= None):
            
            nonlocal prompt_ids, position_ids, parallel_stack, position_required_masks, left_pad_len

            start = len(prompt_ids) # correct
            prompt_ids.extend(new_ids) # correct -> merge new_ids into prompt_ids
            response_mask.extend([1] * len(new_ids)) # correct -> extend response_mask with 1s for new_ids
            # masks = [1] * len(new_ids)
            # if manual_mask_positions:
            #     for idx in manual_mask_positions:
            #         if 0 <= idx < len(masks):
            #             masks[idx] = 0
            # response_mask.extend(masks)
            # first generate position_ids with same length as new_ids if not is_parallel just append or we will process it later
            incr = torch.arange(1, len(new_ids) + 1, dtype=torch.long) + position_ids[-1] # -> correct
            position_ids = torch.cat([position_ids, incr]) # correct -> extend position_ids with new_ids' positions

            if not is_parallel:
                return

            blk     = parallel_stack.pop()
            base_p  = blk["base"]
            longest = blk["longest"]
            

            # a) 校正 Path 内位置 ＆ b) 写跨 Path 掩码
            for i, (s_rel, e_rel) in enumerate(path_spans):
                
                # assert new_ids[s_rel] == self.start_path_token, \
                #     f"append_tokens(is_parallel=True) 期望新 token {new_ids[s_rel]} 是 {self.start_path_token}，但实际是 {new_ids[s_rel]}"
                # assert new_ids[e_rel-1] == self.end_path_token, \
                #     f"append_tokens(is_parallel=True) 期望新 token {new_ids[e_rel-1]} 是 {self.end_path_token}，但实际是 {new_ids[e_rel]}"
                s_abs, e_abs = start + s_rel, start + e_rel
                # the first path we do not need to shift
                shift = position_ids[s_abs] - (base_p)
                # print("shift", shift.item())
                if shift.item():
                    position_ids[s_abs:e_abs] -= shift
                # assert position_ids[s_abs] == base_p, \
                #     f"append_tokens(is_parallel=True) 期望 position_ids[s_abs] {position_ids[s_abs]} 是 {base_p}，但实际是 {position_ids[s_abs]}"
                # # print("prompt_ids[s_abs] == self.start_path_token", prompt_ids[s_abs], self.start_path_token)
                # assert prompt_ids[s_abs] == self.start_path_token, \
                #     f"append_tokens(is_parallel=True) 期望 prompt_ids[s_abs] {prompt_ids[s_abs]} 是 {self.start_path_token}，但实际是 {prompt_ids[s_abs]}"
                # # print("prompt_ids[e_abs - 1] == self.end_path_token", prompt_ids[e_abs - 1], self.end_path_token)
                # assert prompt_ids[e_abs - 1] == self.end_path_token, \
                #     f"append_tokens(is_parallel=True) 期望 prompt_ids[e_abs - 1] {prompt_ids[e_abs - 1]} 是 {self.end_path_token}，但实际是 {prompt_ids[e_abs - 1]}"
                path_max_pos = position_ids[e_abs - 1]  
                longest = max(longest, (path_max_pos - base_p).item())
                # longest = max(longest, e_rel - 1)
                for j, (sj_rel, ej_rel) in enumerate(path_spans):
                    if j == i: continue
                    sj_abs, ej_abs = left_pad_len + start + sj_rel, left_pad_len + start + ej_rel
                    
                    if e_abs + left_pad_len > ej_abs:
                        if ej_abs < self.prompt_length + self.response_length:
                            position_required_masks.append((left_pad_len, s_abs + left_pad_len, e_abs + left_pad_len, sj_abs, ej_abs))
                            print(f"mask {s_abs+left_pad_len}:{e_abs+left_pad_len} 与 {sj_abs}:{ej_abs} attention")
                    elif e_abs + left_pad_len < ej_abs:
                        if sj_abs < self.prompt_length + self.response_length:
                            position_required_masks.append((left_pad_len, s_abs + left_pad_len, e_abs + left_pad_len, sj_abs, ej_abs))
                            print(f"mask {s_abs+left_pad_len}:{e_abs+left_pad_len} 与 {sj_abs}:{ej_abs} attention")
                    

            # try:
            #     p_rel = new_ids.index(self.end_parallel_token)   # first find relative pos of </Parallel> in  new_ids 
            # except ValueError:
            #     raise RuntimeError("append_tokens(is_parallel=True) 找不到 </Parallel> 标记")
            s2, e2 = path_spans[-1]  # the last path ends right before </Parallel>

            p_end_abs   = start + e2
            
            desired_end = base_p + longest + 1
            shift2      = position_ids[p_end_abs] - desired_end
            if shift2.item():
                position_ids[p_end_abs:] -= shift2
            # print("prompt_ids[p_end_abs], self.end_parallel_token", prompt_ids[p_end_abs], self.end_parallel_token)
            # print("position_ids[p_end_abs], desired_end", position_ids[p_end_abs], desired_end)
            # print(position_ids[p_end_abs], position_ids[p_end_abs-1])
            # assert prompt_ids[p_end_abs] == self.end_parallel_token, \
            #     f"append_tokens(is_parallel=True) 期望 prompt_ids[p_end_abs] {prompt_ids[p_end_abs]} 是 {self.end_parallel_token}，但实际是 {prompt_ids[p_end_abs]}"
            # # print(position_ids)
            # print("prompt_ids",prompt_ids)
            # assert torch.all(position_ids[1:] >= position_ids[:-1]), "position_ids 非递增"
            # check if position_ids is strictly increasing
            # s1, e1 = path_spans[0]
            # s2, e2 = path_spans[1]
            # assert position_ids[start+s1] == base_p, \
            #     f"append_tokens(is_parallel=True) 期望 position_ids[start+s1] {position_ids[start+s1]} 是 {base_p}，但实际是 {position_ids[start+s1]}"
            # assert position_ids[start+s2] == base_p, \
            #     f"append_tokens(is_parallel=True) 期望 position_ids[start+s2] {position_ids[start+s2]} 是 {base_p}，但实际是 {position_ids[start+s2]}"
            
            # print("position_ids[start+s1:start+e1]", position_ids[start+s1:start+e1])
            # print("position_ids[start+s2:start+e2]", position_ids[start+s2:start+e2])
            # print("position_ids[start+e1-1]", position_ids[start+e1-1])
            # print("position_ids[start+e1-1+1]", position_ids[start+e1-1+1])
            # print("position_ids[start+e2-1]", position_ids[start+e2-1])
            # print("position_ids[start+e2-1+1]", position_ids[start+e2-1+1])
            
            # print(position_ids[start+s1:start+e1])
            # print(position_ids[start+s2:start+e2])
            # print(position_ids[start+e1-1])
            # print(position_ids[start+e1-1+1])
            # print(position_ids[start+e2-1])
            # print(position_ids[start+e2-1+1])
            # print(position_ids[start+e2] - position_ids[start+e2-1])
            # if position_ids[start+e2-1] > position_ids[start+e1-1]:
            #     if start+e2-1 > start+e1-1:
            #         assert (position_ids[start+e2] - position_ids[start+e2-1]).item() ==  1, \
            #             f"append_tokens(is_parallel=True) 期望 position_ids[start+e2] - position_ids[start+e2-1] {position_ids[start+e2] - position_ids[start+e2-1]} 是 1，但实际是 {position_ids[start+e2] - position_ids[start+e2-1]}, {position_ids[start+s1:start+e1]}, {position_ids[start+s2:start+e2]}, {self.tokenizer.decode(prompt_ids[start+s1:start+e1], skip_special_tokens=False)}, {self.tokenizer.decode(prompt_ids[start+s2:start+e2], skip_special_tokens=False)},{base_p}, {position_ids}"
            #     elif position_ids[start+e1-1] > position_ids[start+e2-1]:
            #         assert position_ids[start+e1] - position_ids[start+e1-1] == 1, \
            #             f"append_tokens(is_parallel=True) 期望 position_ids[start+e1] - position_ids[start+e1-1] {position_ids[start+e1] - position_ids[start+e1-1]} 是 1，但实际是 {position_ids[start+e1] - position_ids[start+e1-1]}"
            # elif position_ids[start+e1-1] > position_ids[start+e2-1]:
            #     if start+e1-1 > start+e2-1:
            #         assert position_ids[start+e1] - position_ids[start+e1-1] ==  1, \
            #             f"append_tokens(is_parallel=True) 期望 position_ids[start+e1] - position_ids[start+e1-1] {position_ids[start+e1] - position_ids[start+e1-1]} 是 1，但实际是 {position_ids[start+e1] - position_ids[start+e1-1]}"
            #     elif position_ids[start+e2-1] > position_ids[start+e1-1]:
            #         assert position_ids[start+e2] - position_ids[start+e2-1] ==  1, \
            #             f"append_tokens(is_parallel=True) 期望 position_ids[start+e2] - position_ids[start+e2-1] {position_ids[start+e2] - position_ids[start+e2-1]} 是 1，但实际是 {position_ids[start+e2] - position_ids[start+e2-1]}"
           
        def should_stop() -> bool:
            gen_len = len(position_ids) - init_len
            if gen_len >= self.response_length:
                return True
            if (
                self.max_iterations_for_parallel_thinking
                and iterations >= self.max_iterations_for_parallel_thinking
            ):
                return True
            return False

        plan_protocol = self.protocol == 'plan'
        max_blocks = self.max_iterations_for_parallel_thinking or contract.MAX_BLOCKS
        # plan: generation calls (for D/T), branch spans, per-token node codes, block counters.
        calls, spans, node_codes = [], [], []
        status = 'ok'
        counters = dict(parallel_triggers=0, valid_plan_blocks=0, fork_dispatches=0, path_jobs=0)
        # graph rollout: the held request whose KV covers a prefix of prompt_ids, and the RoPE offset
        # (physical index - graph position) of the tokens appended next.
        chain, offset = None, 0

        while True:
            request_id = uuid4().hex
            if plan_protocol:
                # Up to max_blocks the main chain may sample <Parallel>; after that every tag is suppressed.
                node = contract.main_node(iterations, max_blocks, self.allow_parallel)
                stops = [self.start_parallel_token] if node == contract.MAIN_OPEN else []
                sp_main = {**sampling_params, 'stop_token_ids': stops + list(self.eos_token_ids),
                           'logit_bias': contract.logit_bias(node, self.tag_ids)}
            else:
                sp_main = {**sampling_params, "stop_token_ids": [self.start_parallel_token, self.eos_token_id]}
                if not self.allow_parallel:
                    sp_main.update(stop_token_ids=[self.eos_token_id], logit_bias={self.start_parallel_token: -100.0})
            remaining = self.response_length - (len(prompt_ids) - init_len)
            sp_main['max_tokens'] = remaining
            ids, log_probs, handle = await self._generate('main', request_id, prompt_ids, sp_main, chain, offset)
            if handle is not None:
                await self._release(chain)
                chain = handle
            critical_depth += len(ids)
            sampled_tokens += len(ids)
            rollout_segments.extend([MAIN_BEFORE if iterations == 0 else MAIN_AFTER] * len(ids))
            rollout_log_probs.extend(log_probs)
            append_tokens(ids)
            if plan_protocol:
                calls.append(dict(node=node, block=None, sampled=len(ids)))
                node_codes.extend([node] * len(ids))
                if (len(response_mask) >= self.response_length or node != contract.MAIN_OPEN
                        or not await self.check_parallel(ids)):
                    break
                counters['parallel_triggers'] += 1
                block_start = len(response_mask)
                block = await self._plan_block(prompt_ids, sampling_params, iterations,
                                               self.response_length - block_start, chain, offset)
                chain, offset = block['chain'], block['offset']
                codes = dict(plan=PLAN_FIRST if iterations == 0 else PLAN_LATER,
                             path=PATH_FIRST if iterations == 0 else PATH_LATER,
                             summary=SUMMARY_FIRST if iterations == 0 else SUMMARY_LATER, forced=-1)
                rollout_segments.extend(codes[kind] for kind in block['kinds'])
                rollout_log_probs.extend(block['log_probs'])
                forced.extend(block_start + i for i, kind in enumerate(block['kinds']) if kind == 'forced')
                label_overrides.extend((block_start + i, token) for i, token in block['overrides'])
                node_codes.extend(block['nodes'])
                calls.extend(block['calls'])
                if block['path_spans']:
                    # Every branch was sampled after prompt + response through </Plan> (+ its <Path>i:).
                    context_end = block_start + block['path_spans'][0][0]
                    replay_segments.extend((block_start + s, block_start + e, context_end)
                                           for s, e in block['path_spans'][1:])
                spans.extend(contract.Span(block_start + s, block_start + e, iterations, number)
                             for number, (s, e) in enumerate(block['path_spans'], 1))
                append_tokens(block['ids'])
                if block['status'] != contract.VALID:
                    status = block['status']  # no repair, no empty block: the trajectory ends here
                    break
                jobs = sum(call['node'] == contract.PATH for call in block['calls'])
                counters['valid_plan_blocks'] += 1
                counters['fork_dispatches'] += bool(jobs)
                counters['path_jobs'] += jobs
                self.trace.fork(block_start - 1)
                iterations += 1
                if len(response_mask) >= self.response_length:
                    break
                continue
            if should_stop() or not self.allow_parallel or not await self.check_parallel(ids):
                break

            assert ids[-1] != self.eos_token_id
            self.trace.fork(len(response_mask) - 1)

            # elict parallel thinking 
            base_pos = position_ids[-1].item() + 1 # the position of the <Path> token
            parallel_stack.append({"base": base_pos, "longest": 0})

            block_start = len(prompt_ids) - init_len
            parallel_ids, path_spans, manual_mask_positions, tokens = await self._call_parallel_thinking(
                prompt_ids, sampling_params
            )
            codes = dict(path=PATH_FIRST if iterations == 0 else PATH_LATER,
                         summary=SUMMARY_FIRST if iterations == 0 else SUMMARY_LATER, forced=-1)
            rollout_segments.extend(codes[kind] for kind in tokens['kinds'])
            rollout_log_probs.extend(tokens['log_probs'])
            forced.extend(block_start + i for i, kind in enumerate(tokens['kinds']) if kind == 'forced')
            label_overrides.extend((block_start + i, token) for i, token in tokens['overrides'])
            # vLLM generated path k from prompt + response[:block_start] + <Path>, without the
            # earlier sibling paths that precede it in the response (path 1 needs no replay).
            replay_segments.extend((block_start + s, block_start + e, block_start) for s, e in path_spans[1:])
            path_tokens = [sum(kind == 'path' for kind in tokens['kinds'][s:e]) for s, e in path_spans]
            summary_tokens = sum(kind == 'summary' for kind in tokens['kinds'])
            critical_depth += max(path_tokens) + summary_tokens
            sampled_tokens += sum(path_tokens) + summary_tokens
            append_tokens(parallel_ids, is_parallel=True, path_spans=path_spans, manual_mask_positions=manual_mask_positions)

            iterations += 1
            if should_stop():
                break

        untruncated_length = len(response_mask)
        response_ids = prompt_ids[init_len:]
        prompt_ids = prompt_ids[: len(prompt_ids) - len(response_mask)]
        assert init_len == (len(prompt_ids))
        flat_packed = self.logprob_context == 'flat_packed'
        if plan_protocol:
            critical_depth, sampled_tokens = contract.depth_and_tokens(calls)
        if flat_packed:
            # vLLM positions are physical indices; sibling paths are separated by replay, not masks.
            position_ids = torch.arange(len(position_ids), dtype=torch.long)
            position_required_masks = []
        elif plan_protocol:
            # Graph positions and sibling isolation from the contract, in padded sequence columns.
            kept = min(untruncated_length, self.response_length)
            position_ids = torch.cat([torch.arange(init_len, dtype=torch.long), torch.tensor(
                contract.graph_positions(untruncated_length, spans, first=init_len), dtype=torch.long)])
            column = left_pad_len + init_len
            kept_spans = [span for span in spans if span.start < kept]
            position_required_masks = [
                (left_pad_len, column + a.start, column + min(a.end, kept), column + b.start, column + min(b.end, kept))
                for a, b in contract.isolation_pairs(kept_spans) if a.path < b.path]
        if flat_packed or plan_protocol:
            for index in forced:  # injected tags were never sampled
                response_mask[index] = 0
        
        if left_pad_len > 0:
            position_ids = torch.cat([
                torch.zeros(left_pad_len, dtype=torch.long),
                position_ids
            ])
        if len(response_ids) < self.response_length:
            right_pad_len = self.response_length - len(response_ids)
            position_ids = torch.cat([
                position_ids,
                torch.zeros(right_pad_len, dtype=torch.long)])
            # bool_mask[:, -right_pad_len:] = False
        else:
            position_ids = position_ids[:self.prompt_length + self.response_length]
            response_ids = response_ids[: self.response_length]
            response_mask = response_mask[: self.response_length]

        self.trace.finish(self.tokenizer, response_ids, response_mask, position_ids, position_required_masks, untruncated_length)
        kept = len(response_ids)
        extra = {}
        if flat_packed:
            # A replay needs at least one sampled token after <Path> inside the kept response.
            extra['replay_segments'] = [(s, min(e, kept), c) for s, e, c in replay_segments if min(e, kept) - s >= 2]
        if flat_packed or plan_protocol:
            extra['label_overrides'] = [(i, token) for i, token in label_overrides if i < kept]
        if plan_protocol:
            assert len(node_codes) == untruncated_length
            extra['node_codes'] = node_codes[:kept]
            extra['node_suppression'] = contract.suppression_table(self.tag_ids, self.count_ids).tolist()
        if self.rollout_logprobs:
            assert len(rollout_segments) == len(rollout_log_probs) == untruncated_length
            extra['rollout_segments'] = rollout_segments[:kept]
            extra['rollout_log_probs'] = [lp if seg >= 0 else 0.0 for lp, seg in
                                          zip(rollout_log_probs[:kept], rollout_segments[:kept])]
        return AgentLoopOutput(
            prompt_ids          = prompt_ids,
            response_ids        = response_ids,
            response_mask       = response_mask,
            position_required_mask       = position_required_masks,
            multiverse_pos_ids  = position_ids.cpu(),        # 1-D
            num_turns           = iterations + 1,
            metrics             = {},
            repro_stats         = {
                'forks': self.trace.record['executed_fork_count'],
                'positions': self.trace.record['parallel_relative_positions'],
                'generation_calls': self.trace.record['generation_calls'],
                'generated_tokens': self.trace.record['generated_tokens_total'],
                'truncated': self.trace.record['truncated'],
                'critical_depth': critical_depth,
                'sampled_tokens': sampled_tokens,
                'trajectory_status': status,
                **(counters if plan_protocol else {}),
            },
            **extra,
        )

    async def _generate(self, phase, request_id, prompt_ids, sampling_params, parent=None, offset=0, traced=True):
        """Token ids, their vLLM log-probs (zeros unless rollout_logprobs is on) and, in graph rollout, the
        finished request now held on the server (a Handle; None if nothing was sampled).

        Graph rollout: parent is the Handle whose tokens the prompt continues, or ready KV segments; offset is
        the RoPE offset of the tokens the request computes. If the engine evicts this trajectory's held KV
        (memory pressure, see graph_kv.py), the KV is rebuilt from the tokens and sampling continues after the
        tokens sampled so far, in a new request.
        """
        extra = dict(return_logprobs=True) if self.rollout_logprobs else {}
        call = self.trace.generate if traced else self._untraced
        if not self.graph_rollout:
            output = await call(self.server_manager, phase, request_id=request_id, prompt_ids=prompt_ids,
                                sampling_params=sampling_params, routing_key=self.routing_key, **extra)
            return (*self._tokens(output), None)
        kv = parent if isinstance(parent, list) else graph_kv.continuation(parent, prompt_ids)
        ids, log_probs, replays = [], [], []
        for _ in range(self.graph_attempts):
            graph = graph_kv.GraphSpec(kv=kv, offset=offset, trajectory=self.graph_key).as_dict()
            output = await call(self.server_manager, phase, request_id=request_id, prompt_ids=prompt_ids + ids,
                                sampling_params={**sampling_params, 'max_tokens': sampling_params['max_tokens'] - len(ids)},
                                routing_key=self.routing_key, graph=graph, **extra)
            await self._release(replays)
            new_ids, new_log_probs = self._tokens(output)
            ids, log_probs = ids + new_ids, log_probs + new_log_probs
            if not (isinstance(output, dict) and output.get('graph_evicted')):
                return ids, log_probs, self._hold(request_id, prompt_ids, ids, offset)
            kv, rebuilt, replays = await self._rebuild(prompt_ids + ids)
            assert rebuilt == offset, f'rebuilt offset {rebuilt} != {offset}'
            request_id = uuid4().hex
        raise RuntimeError(f'graph rollout: KV evicted {self.graph_attempts} times in a row')

    async def _untraced(self, manager, phase, **kwargs):
        return await manager.generate(**kwargs)

    @staticmethod
    def _tokens(output):
        if isinstance(output, dict):
            ids = list(output['token_ids'])
            return ids, list(output['logprobs']) if 'logprobs' in output else [0.0] * len(ids)
        return list(output), [0.0] * len(output)

    def _hold(self, request_id, prompt_ids, ids, offset):
        """Record a finished graph request as held. No ids: the server had no room to run it, nothing is held."""
        if not ids:
            return None
        handle = graph_kv.Handle(request_id, list(prompt_ids) + list(ids), len(prompt_ids) + len(ids) - 1, offset)
        self.held[request_id] = handle
        return handle

    async def _release(self, handles):
        handles = [handles] if isinstance(handles, graph_kv.Handle) else [h for h in handles or () if h is not None]
        if handles:
            for handle in handles:
                self.held.pop(handle.request_id, None)
            await self.server_manager.release([h.request_id for h in handles], routing_key=self.routing_key)

    async def _seal(self, prompt_ids, parent, offset):
        """graph_rollout: hold the KV of prompt_ids (e.g. a branch through its closing tag, which the request
        that sampled </Path> has none for) computed from parent. One discarded sampled token; not a generation
        call for D/T or traces."""
        _, _, handle = await self._generate('seal', uuid4().hex, prompt_ids, dict(n=1, max_tokens=1, temperature=1.0),
                                            parent, offset, traced=False)
        return handle

    async def _rebuild(self, tokens):
        """graph_rollout, after an eviction: recompute the KV of tokens' closed blocks as it was sampled (each
        branch in its own context after the shared prefix, then merged), with one-token requests. Returns the KV
        segments and offset for a request whose prompt extends tokens, and the held requests they come from."""
        kv, offset, held = [], 0, []
        for paths in graph_kv.closed_blocks(tokens, *self.graph_tags):
            base = list(tokens[:paths[0][0]])
            first = await self._seal(base + list(tokens[slice(*paths[0])]), kv, offset)
            rest = await asyncio.gather(*[self._seal(base + list(tokens[start:end]), first, offset)
                                          for start, end in paths[1:]])
            await self._release(held)
            held = [first, *rest]
            assert None not in held, 'no room to rebuild a branch that was sampled'
            kv = graph_kv.merge(held, len(base))
            offset = graph_kv.merged_offset(offset, [end - start for start, end in paths])
        return kv, offset, held

    async def _node_call(self, phase, node, close, prompt_ids, sampling_params, max_tokens, parent=None, offset=0):
        """plan: sample one node until its closing tag, EOS or max_tokens, with the node's tags suppressed.

        COUNT (close None) samples one token from contract.COUNTS. Returns ids, log-probs, stop ('close',
        'eos' or 'budget'), whether a call was made and, in graph rollout, the held request (a Handle).
        """
        if max_tokens < 1:
            return [], [], 'budget', False, None
        params = {**sampling_params, 'n': 1, 'max_tokens': max_tokens,
                  'stop_token_ids': [] if close is None else [close, *self.eos_token_ids],
                  **contract.sampling_constraint(node, self.tag_ids, self.count_ids)}
        ids, log_probs, handle = await self._generate(phase, uuid4().hex, prompt_ids, params, parent, offset)
        if close is None:
            return ids, log_probs, 'close' if ids else 'budget', True, handle
        stop = 'close' if ids and ids[-1] == close else 'eos' if ids and ids[-1] in self.eos_token_ids else 'budget'
        return ids, log_probs, stop, True, handle

    def _written(self, ids, stop, close):
        """A segment as it is written into the sequence: a sampled EOS becomes the closing tag, a cut gets one."""
        ids = list(ids)
        if stop == 'eos':
            ids[-1] = close
        return ids + [close] if stop == 'budget' else ids

    async def _plan_block(self, context, sampling_params, block, room, chain=None, offset=0):
        """plan block after a sampled <Parallel>: branches=N, <Plan>, the plan, its N branches,
        </Parallel><Summary>, summary.

        context: prompt + response through <Parallel>; room: response tokens left. Returns the block's ids
        and, per token, kind (plan/path/summary when sampled, forced when inserted), node code and vLLM
        log-prob; EOS overrides; block-relative branch spans (<Path> through </Path>); the generation calls
        made (for D/T); and the plan status. After an invalid plan the block ends with the plan tokens.
        Graph rollout: chain is the held request ending in <Parallel>, offset its RoPE offset; the result's
        chain and offset are those of the summary request.
        """
        ids_of = self.tag_ids
        out = dict(ids=[], kinds=[], nodes=[], log_probs=[], overrides=[], calls=[], path_spans=[],
                   chain=chain, offset=offset)

        def add(ids, kind, node=contract.INSERTED, log_probs=None):
            out['ids'].extend(ids)
            out['kinds'].extend([kind] * len(ids))
            out['nodes'].extend([node] * len(ids))
            out['log_probs'].extend([0.0] * len(ids) if log_probs is None else log_probs)

        def close_segment(ids, log_probs, stop, kind, node, close):
            # As in legacy blocks: a sampled EOS is written as the closing tag but scored as the EOS it was;
            # a segment cut by its budget gets an inserted closing tag.
            if stop == 'eos':
                out['overrides'].append((len(out['ids']) + len(ids) - 1, ids[-1]))
            written = self._written(ids, stop, close)
            add(written[:len(ids)], kind, node, log_probs)
            add(written[len(ids):], 'forced')

        async def advance(handle):
            # The new held request continues the chain; the previous one is no longer needed.
            if handle is not None:
                await self._release(out['chain'])
                out['chain'] = handle

        # branches=N: the model samples N (one of contract.COUNTS); the plan must then have N lines.
        add(self.branches_ids, 'forced')
        ids, log_probs, stop, called, handle = await self._node_call(
            'count', contract.COUNT, None, context + out['ids'], sampling_params,
            min(1, room - len(out['ids'])), out['chain'], offset)
        await advance(handle)
        if called:
            out['calls'].append(dict(node=contract.COUNT, block=block, sampled=len(ids)))
        add(ids, 'plan', contract.COUNT, log_probs)
        if stop != 'close':
            out['status'] = contract.PLAN_BUDGET_EXHAUSTED
            return out
        branches = contract.MIN_PATHS + self.count_ids.index(ids[0])

        add([ids_of[tag] for tag in contract.PLAN_OPEN], 'forced')
        ids, log_probs, stop, called, handle = await self._node_call(
            'plan', contract.PLAN, ids_of['</Plan>'], context + out['ids'], sampling_params,
            min(self.max_plan_tokens, room - len(out['ids'])), out['chain'], offset)
        await advance(handle)
        if called:
            out['calls'].append(dict(node=contract.PLAN, block=block, sampled=len(ids)))
        text = self.tokenizer.decode(ids[:-1] if stop == 'close' else ids, skip_special_tokens=False)
        out['status'] = contract.plan_status(text, stop, branches)
        add(ids, 'plan', contract.PLAN, log_probs)
        if out['status'] != contract.VALID:
            return out

        items = contract.parse_plan(text, branches).items
        prefixes = [[ids_of['<Path>']] + contract.path_prefix_ids(self.tokenizer, number)
                    for number in range(1, len(items) + 1)]
        base, left = context + out['ids'], room - len(out['ids'])
        plan = out['chain']

        async def branch(prefix):
            result = await self._node_call('path', contract.PATH, ids_of['</Path>'], base + prefix, sampling_params,
                                           min(self.max_path_response_length, left - len(prefix) - 1), plan, offset)
            if not self.graph_rollout:
                return result, None
            ids, _, stop, _, handle = result
            seal = await self._seal(base + prefix + self._written(ids, stop, ids_of['</Path>']), handle or plan, offset)
            await self._release(handle)
            return result, seal

        results = await asyncio.gather(*[branch(prefix) for prefix in prefixes])
        for prefix, ((ids, log_probs, stop, called, _), _) in zip(prefixes, results):
            if called:
                out['calls'].append(dict(node=contract.PATH, block=block, sampled=len(ids)))
            start = len(out['ids'])
            add(prefix, 'forced')
            close_segment(ids, log_probs, stop, 'path', contract.PATH, ids_of['</Path>'])
            out['path_spans'].append((start, len(out['ids'])))

        add([ids_of[tag] for tag in contract.BLOCK_CLOSE], 'forced')
        parent, seals = out['chain'], [seal for _, seal in results]
        if self.graph_rollout and None in seals:  # a branch reached the length limit: no room for a summary
            assert room - len(out['ids']) < 1, 'a branch could not be sealed although the summary has room'
        elif self.graph_rollout:
            # The summary sees every branch, each with the KV it got in its own context, at graph positions.
            parent = graph_kv.merge(seals, len(base))
            out['offset'] = graph_kv.merged_offset(offset, [end - start for start, end in out['path_spans']])
        ids, log_probs, stop, called, handle = await self._node_call(
            'summary', contract.SUMMARY, ids_of['</Summary>'], context + out['ids'], sampling_params,
            room - len(out['ids']), parent, out['offset'])
        await self._release(seals)
        await advance(handle)
        if called:
            out['calls'].append(dict(node=contract.SUMMARY, block=block, sampled=len(ids)))
            close_segment(ids, log_probs, stop, 'summary', contract.SUMMARY, ids_of['</Summary>'])
        assert len(out['ids']) == len(out['kinds']) == len(out['nodes']) == len(out['log_probs'])
        return out

    async def check_parallel(self, response_ids):
        """
        check whether need to conduct parallel thinking
        """
        if response_ids and response_ids[-1] == self.start_parallel_token:
            return True
        else:
            return False

    async def _call_parallel_thinking(
        self,
        prompt_ids: list[int],
        sampling_params: dict[str, Any],
    ):
        print("Conducting parallel thinking...")
        num_paths = self.num_paths
        max_len   = self.max_path_response_length
        PATH_OPEN, PATH_CLOSE = self.start_path_token, self.end_path_token
        manual_mask_positions = []

        
        async def _gen_single_path(seed_i: int, prompt_i: list[int]):
            sp = copy.deepcopy(sampling_params)
            sp.update({"seed": seed_i, "n": 1, "stop_token_ids": [PATH_CLOSE, self.eos_token_id],
                    "temperature": 1.0})
            # sp.update({"n": 1, "stop_token_ids": [PATH_CLOSE, self.eos_token_id],
            #         "temperature": 1.0})
            manual_append = False
            sp['max_tokens'] = min(max_len, self.prompt_length + self.response_length - len(prompt_i) - 1)
            ids, log_probs, _ = await self._generate('path', uuid4().hex, prompt_i + [PATH_OPEN], sp)
            if max_len and len(ids) > max_len:
                ids, log_probs = ids[:max_len], log_probs[:max_len]
            close = 'sampled'
            if not ids:
                ids = [PATH_CLOSE]
                log_probs = [0.0]
                close = 'appended'
                manual_append = True
            elif ids[-1] != PATH_CLOSE:
                if ids[-1] == self.eos_token_id:
                    ids[-1] = PATH_CLOSE
                    close = 'replaced'
                else:
                    ids.append(PATH_CLOSE)
                    log_probs.append(0.0)
                    close = 'appended'
                manual_append = True
            return [PATH_OPEN] + ids, manual_append, log_probs, close

        tasks = []
        for i in range(num_paths):
            # prompt_i **不再含 PATH_OPEN**，防止 tag 重复
            prompt_i = prompt_ids
            tasks.append(
                asyncio.create_task(
                    _gen_single_path(random.randint(0, 2**31 - 1), prompt_i)
                )
            )

        path_token_lists = await asyncio.gather(*tasks)     

        parallel_ids = []             
        path_spans   = []
        cursor       = 0              
        # Per token of parallel_ids: path/summary (sampled) or forced (injected), and its vLLM log-prob;
        # overrides keep the sampled EOS where the runtime wrote a closing tag instead.
        tokens = dict(kinds=[], log_probs=[], overrides=[])

        def track(kind, sampled_ids, log_probs, close):
            tokens['kinds'].extend([kind] * len(sampled_ids))
            tokens['log_probs'].extend(log_probs)
            if close == 'appended':
                tokens['kinds'][-1] = 'forced'
            elif close == 'replaced':
                tokens['overrides'].append((len(tokens['kinds']) - 1, self.eos_token_id))

        def force(count):
            tokens['kinds'].extend(['forced'] * count)
            tokens['log_probs'].extend([0.0] * count)

        #### <Path> </Path><Path> </Path> -> path_spans (0, len(path_1)) (len(path_1), len(path_1) + len(path_2))
        for (ids, manual_append_flag, path_log_probs, close) in path_token_lists:
            force(1)  # <Path>
            track('path', ids[1:], path_log_probs, close)
            assert ids[0] == PATH_OPEN and ids[-1] == PATH_CLOSE, \
                f"Path tokens must start with {PATH_OPEN} and end with {PATH_CLOSE}, got {ids}"
            span_start = cursor 
            parallel_ids.extend(ids)
            cursor     += len(ids)
            span_end   = cursor
            path_spans.append((span_start, span_end))
            manual_mask_positions.append(span_start)
            if manual_append_flag:
                manual_mask_positions.append(span_end-1)

        # ---------- 3) add </Parallel><Summary> ----------
        parallel_ids.append(self.end_parallel_token)           # </Parallel>
        manual_mask_positions.append(cursor)
        assert parallel_ids[cursor] == self.end_parallel_token
        cursor += 1
        parallel_ids.extend(self.new_line_token)          # \n
        manual_mask_positions.append(cursor)
        cursor += len(self.new_line_token)
        parallel_ids.append(self.start_summary_token)          # <Summary>
        manual_mask_positions.append(cursor)
        assert parallel_ids[cursor] == self.start_summary_token
        cursor += 1
        force(len(parallel_ids) - len(tokens['kinds']))  # </Parallel>, newline, <Summary>
        
        # if exploration stage alos superass the max length, we will not generate summary
        if len(prompt_ids) + 2 + len(parallel_ids) + 1 < self.prompt_length + self.response_length:
            print("Conducting Summary...")
            manual_append_summary = False
            sp_sum = copy.deepcopy(sampling_params)
            sp_sum.update({"n": 1, "stop_token_ids": [self.end_summary_token, self.eos_token_id]})
            sp_sum['max_tokens'] = self.prompt_length + self.response_length - len(prompt_ids) - len(parallel_ids)
            summary_ids, summary_log_probs, _ = await self._generate(
                'summary', uuid4().hex, prompt_ids + parallel_ids, sp_sum)   # 现在的完整 prompt
            close = 'sampled'
            if not summary_ids:
                summary_ids = [self.end_summary_token]
                summary_log_probs = [0.0]
                close = 'appended'
                manual_append_summary = True
            elif summary_ids[-1] != self.end_summary_token:
                if summary_ids[-1] == self.eos_token_id:
                    summary_ids[-1] = self.end_summary_token
                    close = 'replaced'
                else:
                    summary_ids.append(self.end_summary_token)
                    summary_log_probs.append(0.0)
                    close = 'appended'
                manual_append_summary = True
            track('summary', summary_ids, summary_log_probs, close)
            parallel_ids.extend(summary_ids)
            cursor += len(summary_ids)
            if manual_append_summary:
                manual_mask_positions.append(cursor-1)
            # print("asadas", parallel_ids[cursor-1])
            assert parallel_ids[cursor-1] == self.end_summary_token
            assert parallel_ids[-1] == self.end_summary_token, \
                f"Parallel thinking did not end with {self.end_summary_token}, got {parallel_ids[-1]}"
        # print(self.tokenizer.decode(parallel_ids, skip_special_tokens=False))
        assert len(tokens['kinds']) == len(tokens['log_probs']) == len(parallel_ids)
        return parallel_ids, path_spans, manual_mask_positions, tokens        # path_spans 已是相对 parallel_ids       
        

