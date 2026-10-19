"""Standalone counted-fork executor; exact raw actions and serial cost accounting.

Native Instruct Think boundaries are preserved during structured execution. Forced path headers and
bridges are excluded from the policy loss; sampled closing actions retain their
original IDs even if the visible assembly replaces a stop with a closing tag.
"""
import json
import re
import copy
from pathlib import Path


TAGS = ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']


def execute(tokenizer, prompt_ids, decoder, eos_ids, response_budget=4096,
            path_budget=768, max_context=16384, seed=0):
    encoded = [tokenizer.encode(x, add_special_tokens=False) for x in TAGS]
    if any(len(x) != 1 for x in encoded):
        raise ValueError('Each control tag must have exactly one token')
    po, pc, bo, bc, so, sc = tags = [x[0] for x in encoded]
    newline = tokenizer.encode('\n', add_special_tokens=False)
    if len(newline) != 1 or len(set(tags)) != 6:
        raise ValueError('Distinct tags and single-token newline required')
    close = tokenizer.encode("</think>", add_special_tokens=False)
    if len(close) != 1:
        raise ValueError("Single native think close token required")
    tc = close[0]
    thinking = True
    ids = list(prompt_ids)
    start = len(ids)
    if not ids or start >= max_context:
        raise ValueError('Empty or oversized prompt')
    mask, calls, widths, path_lengths = [], [], [], []
    depth = 0
    invalid = False
    physical_forwards = 0
    prefill_forwards = 0
    fork_batch_ledger = []

    def left():
        return min(response_budget - len(mask), max_context - len(ids))

    def inject(tokens):
        ids.extend(tokens)
        mask.extend([0] * len(tokens))

    def sampled(tokens, call):
        if len(tokens) != len(call['generated_ids']):
            raise ValueError('Replacement changed sampled action span')
        call['response_start'] = len(mask)
        ids.extend(tokens)
        mask.extend([1] * len(tokens))
        calls.append(call)

    def generate(phase, prefix, budget, stops, call_seed_offset=0):
        nonlocal physical_forwards, prefill_forwards
        call = dict(phase=phase, prompt_ids=list(prefix), structure_start=start,
                    structure_tags=tags[:4], pad_id=tokenizer.pad_token_id,
                    blocked_token_ids=list(tags) if not thinking else ([tc] if phase != 'main' else []),
                    temperature=1., seed=seed + (len(calls)+call_seed_offset) * 1009)
        raw, logps, forwards = decoder(call, min(budget, max_context-len(prefix)), stops)
        if len(raw) != len(logps) or len(raw) > budget:
            raise ValueError('Decoder action/logp count mismatch')
        call.update(generated_ids=list(raw), old_logprobs=list(logps),
                    actual_model_forward_calls=int(forwards))
        physical_forwards += int(forwards)
        prefill_forwards += int(bool(raw))
        return list(raw), call

    while left() > 0:
        raw, call = generate('main', ids, left(), [po, tc, *eos_ids] if thinking else eos_ids)
        sampled(raw, call)
        depth += len(raw)
        if raw and raw[-1] == tc and thinking:
            thinking = False
            continue
        if not raw or raw[-1] != po or left() <= 0:
            break
        raw, call = generate('width', ids, min(4, left()), [newline[0], *eos_ids, *tags])
        sampled(raw, call)
        depth += len(raw)
        header = tokenizer.decode(raw, skip_special_tokens=False)
        if re.fullmatch(r'[2-8]\n', header) is None:
            invalid = True
            break
        width = int(header)
        prefixes = [[bo] + tokenizer.encode(str(i)+'\n', add_special_tokens=False)
                    for i in range(1, width+1)]
        suffix = [pc] + newline + [so]
        overhead = sum(len(p)+1 for p in prefixes) + len(suffix) + 1
        budget = min(path_budget, (left()-overhead)//width)
        if budget <= 0:
            break
        shared = list(ids)
        lengths = []
        stop_ids = [bc, *eos_ids, bo, po, pc, so, sc]
        if hasattr(decoder,'decode_many'):
            path_calls = [dict(phase='path',prompt_ids=shared+prefix,structure_start=start,
                              structure_tags=tags[:4],pad_id=tokenizer.pad_token_id,temperature=1.,blocked_token_ids=[tc],
                              seed=seed+(len(calls)+i)*1009) for i,prefix in enumerate(prefixes)]
            budgets = [min(budget,max_context-len(c['prompt_ids'])) for c in path_calls]
            outputs = decoder.decode_many(path_calls,budgets,stop_ids)
            if len(outputs)!=width:
                raise ValueError('Batched decoder returned wrong number of siblings')
            batch_stats = copy.deepcopy(decoder.last_batch_stats)
            if not 0 < batch_stats['physical_forward_calls'] <= sum(len(x[0]) for x in outputs):
                raise ValueError('Invalid instrumented physical fork batch cost')
            physical_forwards += int(batch_stats['physical_forward_calls'])
            prefill_forwards += int(batch_stats['prefill_forward_calls'])
            fork_batch_ledger.append(batch_stats)
            results=[]
            for call,(raw,logps,row_forwards) in zip(path_calls,outputs):
                if len(raw)!=len(logps) or len(raw)>budget or row_forwards!=len(raw):
                    raise ValueError('Batched sampled action/logp/work count mismatch')
                call.update(generated_ids=list(raw),old_logprobs=list(logps),
                            serial_equivalent_forward_calls=int(row_forwards),
                            physical_forward_accounting='Shared cost charged once in fork_batch_ledger')
                results.append((list(raw),call))
        else:
            results=[generate('path',shared+prefix,budget,stop_ids,call_seed_offset=i) for i,prefix in enumerate(prefixes)]
        for prefix,(raw,call) in zip(prefixes,results):
            inject(prefix)
            visible = list(raw)
            if visible and visible[-1] in [*eos_ids, bo, po, pc, so, sc]:
                visible[-1] = bc
            sampled(visible, call)
            if not visible or visible[-1] != bc:
                inject([bc])
            lengths.append(len(raw))
        widths.append(width)
        path_lengths.extend(lengths)
        depth += max(lengths, default=0)
        inject(suffix)
        if left() > 1:
            raw, call = generate('summary', ids, left()-1, [sc, *eos_ids, po, pc, bo, bc, so])
            visible = list(raw)
            if visible and visible[-1] in [*eos_ids, po, pc, bo, bc, so]:
                visible[-1] = sc
            sampled(visible, call)
            depth += len(raw)
            if not visible or visible[-1] != sc:
                inject([sc])
        else:
            inject([sc])
    response = ids[start:]
    if len(response) != len(mask) or len(response) > response_budget:
        raise ValueError('Response mask/budget mismatch')
    return dict(prompt_ids=prompt_ids, response_ids=response, response_mask=mask,
                output=tokenizer.decode(response, skip_special_tokens=False),
                policy_calls=calls, widths=widths, path_lengths=path_lengths,
                fork_batch_ledger=fork_batch_ledger,
                stats=dict(forks=len(widths), critical_depth=depth,
                           sampled_tokens=sum(mask), forced_tokens=len(mask)-sum(mask),
                           generation_calls=len(calls), invalid_width=invalid,
                           actual_model_forward_calls=physical_forwards,
                           actual_prefill_forward_calls=prefill_forwards,
                           actual_decode_forward_calls=physical_forwards-prefill_forwards,
                           serial_equivalent_forward_calls=sum(len(c['generated_ids']) for c in calls),
                           truncated=len(response) >= response_budget))


class HFDecoder:
    def __init__(self, model, replay, device='cuda'):
        self.model, self.replay, self.device = model, replay, device

    def __call__(self, call, budget, stops):
        import torch
        if budget <= 0:
            return [], [], 0
        sampled, logps = [], []
        gen = torch.Generator(device=self.device).manual_seed(call['seed'])
        initial = dict(call, generated_ids=[0])
        with torch.inference_mode():
            ids, pos, mask = self.replay.call_inputs(initial, self.device, next(self.model.parameters()).dtype)
            out = self.model(input_ids=ids, position_ids=pos, attention_mask=mask,
                             use_cache=True, logits_to_keep=1)
            position = int(pos[0, -1])
            for i in range(budget):
                logits = out.logits[0, -1].float()
                logits = self.replay.mask_logits(logits, call)
                target = int(torch.multinomial(logits.softmax(-1), 1, generator=gen))
                sampled.append(target)
                logps.append(float(logits[target]-logits.logsumexp(-1)))
                if target in stops or i+1 == budget:
                    break
                position += 1
                mask = torch.zeros((1, 1, 1, len(call['prompt_ids'])+len(sampled)),
                                   dtype=next(self.model.parameters()).dtype, device=self.device)
                out = self.model(input_ids=torch.tensor([[target]], device=self.device),
                                 position_ids=torch.tensor([[position]], device=self.device),
                                 attention_mask=mask, past_key_values=out.past_key_values,
                                 use_cache=True, logits_to_keep=1)
        return sampled, logps, len(sampled)


def native_eos_ids(model, tokenizer):
    values = [tokenizer.eos_token_id]
    for name in ('generation_config.json', 'config.json'):
        p = Path(model)/name
        if p.exists():
            value = json.loads(p.read_text()).get('eos_token_id')
            values.extend(value if isinstance(value, list) else [value])
    return sorted(set(x for x in values if isinstance(x, int)))
