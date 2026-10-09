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
                                                              SUMMARY_FIRST, SUMMARY_LATER)
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

        cls.eos_token_id = cls.tokenizer.eos_token_id
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

        
        prompt_ids = await self.loop.run_in_executor(
            None,
            lambda: self.tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=True
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
            s2, e2 = path_spans[-1]

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

        
        while True:
            request_id = uuid4().hex
            remaining = self.response_length - (len(prompt_ids) - init_len)
            sp_main = {**sampling_params, "max_tokens": remaining,
                       "stop_token_ids": [self.start_parallel_token, self.eos_token_id]}
            ids, log_probs = await self._generate('main', request_id, prompt_ids, sp_main)
            rollout_segments.extend([MAIN_BEFORE if iterations == 0 else MAIN_AFTER] * len(ids))
            rollout_log_probs.extend(log_probs)
            append_tokens(ids)
            if should_stop() or not await self.check_parallel(ids):
                break

            assert ids[-1] != self.eos_token_id

            remaining = self.response_length - (len(prompt_ids) - init_len)
            # Reserve the injected path/parallel/summary tags and newline.
            if remaining < 2 * self.num_paths + 3 + len(self.new_line_token):
                break

            self.trace.fork(len(response_mask) - 1)

            # elict parallel thinking 
            base_pos = position_ids[-1].item() + 1 # the position of the <Path> token
            parallel_stack.append({"base": base_pos, "longest": 0})

            block_start = len(prompt_ids) - init_len
            parallel_ids, path_spans, manual_mask_positions, tokens = await self._call_parallel_thinking(
                prompt_ids, sampling_params, remaining
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
            append_tokens(parallel_ids, is_parallel=True, path_spans=path_spans, manual_mask_positions=manual_mask_positions)

            iterations += 1
            if should_stop():
                break

        untruncated_length = len(response_mask)
        response_ids = prompt_ids[init_len:]
        prompt_ids = prompt_ids[:init_len]
        assert init_len == (len(prompt_ids))
        flat_packed = self.logprob_context == 'flat_packed'
        if flat_packed:
            # vLLM positions are physical indices; sibling paths are separated by replay, not masks.
            position_ids = torch.arange(len(position_ids), dtype=torch.long)
            position_required_masks = []
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
            extra['label_overrides'] = [(i, token) for i, token in label_overrides if i < kept]
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
                'critical_depth': self.trace.record['critical_depth'],
                'truncated': self.trace.record['truncated'],
            },
            **extra,
        )

    async def _generate(self, phase, request_id, prompt_ids, sampling_params):
        """Token ids and their vLLM log-probs (zeros unless rollout_logprobs is on)."""
        extra = dict(return_logprobs=True) if self.rollout_logprobs else {}
        output = await self.trace.generate(self.server_manager, phase, request_id=request_id, prompt_ids=prompt_ids,
                                           sampling_params=sampling_params, routing_key=self.routing_key, **extra)
        if isinstance(output, dict):
            return list(output['token_ids']), list(output['logprobs'])
        return list(output), [0.0] * len(output)



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
        remaining: int,
    ):
        print("Conducting parallel thinking...")
        num_paths = self.num_paths
        overhead = 2 * num_paths + 3 + len(self.new_line_token)
        path_budget = (remaining - overhead) // num_paths
        max_len = min(self.max_path_response_length or path_budget, path_budget)
        PATH_OPEN, PATH_CLOSE = self.start_path_token, self.end_path_token
        manual_mask_positions = []

        
        async def _gen_single_path(seed_i: int, prompt_i: list[int]):
            sp = copy.deepcopy(sampling_params)
            sp.update({"seed": seed_i, "n": 1, "stop_token_ids": [PATH_CLOSE, self.eos_token_id],
                    "temperature": 1.0, "max_tokens": max_len})
            # sp.update({"n": 1, "stop_token_ids": [PATH_CLOSE, self.eos_token_id],
            #         "temperature": 1.0})
            manual_append = False
            ids, log_probs = await self._generate('path', uuid4().hex, prompt_i + [PATH_OPEN], sp)
            if max_len and len(ids) > max_len:
                ids, log_probs = ids[:max_len], log_probs[:max_len]
            close = 'sampled'
            if not ids or ids[-1] != PATH_CLOSE:
                if ids and ids[-1] == self.eos_token_id:
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
        if len(parallel_ids) < remaining:
            print("Conducting Summary...")
            manual_append_summary = False
            sp_sum = copy.deepcopy(sampling_params)
            sp_sum.update({"n": 1, "max_tokens": remaining - len(parallel_ids) - 1,
                           "stop_token_ids": [self.end_summary_token, self.eos_token_id]})
            summary_ids, summary_log_probs = await self._generate(
                'summary', uuid4().hex, prompt_ids + parallel_ids, sp_sum)   # 现在的完整 prompt
            close = 'sampled'
            if not summary_ids or summary_ids[-1] != self.end_summary_token:
                if summary_ids and summary_ids[-1] == self.eos_token_id:
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
