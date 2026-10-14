"""Exact likelihood of sampled actions in a counted, isolated fork rollout.

Prefixes are the actual per-call prefixes, not slices of the assembled response.
Only raw sampled IDs are policy targets; injected bridges never are.
"""
import math
import torch
import lane_profile
from source.parallel_structure import attention, layout


def mask_logits(logits, call):
    blocked = call.get('blocked_token_ids', [])
    if blocked:
        logits = logits.clone()
        logits[..., blocked] = -torch.inf
    return logits


def call_inputs(call, device, dtype):
    prompt = list(call['prompt_ids'])
    targets = list(call['generated_ids'])
    if not prompt or not targets:
        raise ValueError('A scored call needs a nonempty prefix and sampled actions')
    ids = torch.tensor(prompt + targets[:-1], dtype=torch.long)
    start = int(call['structure_start'])
    tags = call['structure_tags']
    pad = call['pad_id']
    positions, _ = layout(ids, start, tags, pad, allow_partial=True)
    allowed = attention(ids, start, tags, pad, allow_partial=True)
    additive = torch.zeros_like(allowed, dtype=dtype).masked_fill_(~allowed, -torch.inf)
    return ids[None].to(device), positions[None].to(device), additive[None, None].to(device)


def score_call(model, call, temperature=None, calculate_entropy=False):
    sampled = call['generated_ids']
    if not sampled:
        empty = next(model.parameters()).new_empty((0,), dtype=torch.float32)
        return empty, empty if calculate_entropy else None
    value = float(call.get('temperature', 1.) if temperature is None else temperature)
    if not math.isfinite(value) or value <= 0:
        raise ValueError('PPO requires a finite positive sampling temperature')
    parameter = next(model.parameters())
    ids, positions, mask = call_inputs(call, parameter.device, parameter.dtype)
    lane_profile.category("replay")
    output = model(input_ids=ids, position_ids=positions, attention_mask=mask,
                   use_cache=False, logits_to_keep=len(sampled))
    logits = output.logits[0].float() / value
    if logits.shape[0] != len(sampled):
        raise ValueError('Model did not retain exactly the requested target logits')
    logits = mask_logits(logits, call)
    if any(x in call.get("blocked_token_ids", []) for x in sampled):
        raise ValueError("Raw sampled action violates recorded guard")
    target = torch.tensor(sampled, device=logits.device, dtype=torch.long)
    normalizer = logits.logsumexp(-1)
    logp = logits.gather(-1, target[:, None]).squeeze(-1) - normalizer
    entropy = normalizer - (logits.softmax(-1) * logits.masked_fill(~torch.isfinite(logits), 0)).sum(-1) if calculate_entropy else None
    return logp, entropy


def score_trajectory(model, calls, response_mask, temperature=None, calculate_entropy=False):
    parameter = next(model.parameters())
    mask = torch.as_tensor(response_mask, device=parameter.device, dtype=torch.bool)
    logp = parameter.new_zeros(mask.shape, dtype=torch.float32)
    entropy = parameter.new_zeros(mask.shape, dtype=torch.float32) if calculate_entropy else None
    occupied = torch.zeros_like(mask)
    for call in calls:
        n = len(call['generated_ids'])
        if not n:
            continue
        start = int(call['response_start'])
        end = start + n
        if start < 0 or end > len(mask) or occupied[start:end].any() or not mask[start:end].all():
            raise ValueError('Sampled-action span is outside or overlaps the loss mask')
        values, ent = score_call(model, call, temperature, calculate_entropy)
        logp[start:end] = values
        if calculate_entropy:
            entropy[start:end] = ent
        occupied[start:end] = True
    if not torch.equal(occupied, mask):
        raise ValueError('Policy calls must cover every sampled token and no forced/pad token')
    return logp, entropy


@torch.no_grad()
def decoder_logprobs(model, call, temperature=None):
    """Reference: prefill once, then actual per-token KV-cache decode forwards."""
    sampled = call['generated_ids']
    if not sampled:
        return [], 0
    prompt = list(call['prompt_ids'])
    initial = dict(call, generated_ids=[sampled[0]])
    parameter = next(model.parameters())
    ids, positions, mask = call_inputs(initial, parameter.device, parameter.dtype)
    output = model(input_ids=ids, position_ids=positions, attention_mask=mask,
                   use_cache=True, logits_to_keep=1)
    pos = int(positions[0, -1])
    temp = float(call.get('temperature', 1.) if temperature is None else temperature)
    values = []
    for i, target in enumerate(sampled):
        logits = output.logits[0, -1].float() / temp
        logits = mask_logits(logits, call)
        values.append(float(logits[target] - logits.logsumexp(-1)))
        if i + 1 == len(sampled):
            break
        pos += 1
        decode_mask = torch.zeros((1, 1, 1, len(prompt) + i + 1),
                                  device=parameter.device, dtype=parameter.dtype)
        output = model(input_ids=torch.tensor([[target]], device=parameter.device),
                       position_ids=torch.tensor([[pos]], device=parameter.device),
                       attention_mask=decode_mask, past_key_values=output.past_key_values,
                       use_cache=True, logits_to_keep=1)
    return values, len(sampled)
