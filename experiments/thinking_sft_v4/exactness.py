"""Independent references for the graph (4D mask + graph positions) training forward of one sample.

    path_reference     branch k of a block == causal forward of [everything before the block's first <Path>,
                       branch k] with ordinary positions 0..n-1 (what the runtime samples branch k from)
    kv_reference       the whole sample decoded as the runtime does: shared prefix in a KV cache, each branch on
                       its own copy, the branch caches concatenated, later tokens continuing from the longest
                       branch's last position + 1 (positions computed here, not by contract.graph_positions)
    eager_reference    a from-scratch fp32 Qwen3 forward with an explicit visibility matrix (brute force)
    causal_control     plain causal forward: must DIFFER on later branches (shows the test is sensitive)

Used by tests/test_sft.py (tiny model) and vm_selftest.py (real Qwen3-0.6B).
"""
import copy

import torch
from transformers import DynamicCache

from sft_data import collate


def _dtype(model):
    return next(model.parameters()).dtype


def _device(model):
    return next(model.parameters()).device


@torch.no_grad()
def forward_logits(model, input_ids, position_ids=None, attention_mask=None, past_key_values=None):
    device = _device(model)
    ids = torch.as_tensor(input_ids, device=device).view(1, -1)
    kwargs = dict(use_cache=past_key_values is not None, past_key_values=past_key_values)
    if position_ids is not None:
        kwargs['position_ids'] = torch.as_tensor(position_ids, device=device).view(1, -1)
    if attention_mask is not None:
        kwargs['attention_mask'] = attention_mask
    return model(input_ids=ids, **kwargs).logits[0].float()


@torch.no_grad()
def graph_logits(model, sample, pad_id=0):
    batch = collate([sample], pad_id, dtype=_dtype(model), device=_device(model))
    out = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                position_ids=batch['position_ids'], use_cache=False)
    return out.logits[0].float()


def _blocks(sample):
    blocks = {}
    for span in sample['spans']:
        blocks.setdefault(span.block, []).append(span)
    return [sorted(spans) for _, spans in sorted(blocks.items())]


def path_reference(model, sample, logits):
    """Max |diff| over every branch token of the FIRST block vs. the causal forward of [pre-block tokens, branch]
    with ordinary positions (later blocks have no ordinary-position equivalent: kv/eager references cover them)."""
    ids, worst = sample['input_ids'], 0.0
    blocks = _blocks(sample)
    if not blocks:
        return 0.0
    first = blocks[0][0].start
    for span in blocks[0]:
        sequence = ids[:first] + ids[span.start:span.end]
        reference = forward_logits(model, sequence, list(range(len(sequence))))
        worst = max(worst, (logits[span.start:span.end] - reference[first:]).abs().max().item())
    return worst


@torch.no_grad()
def kv_reference(model, sample, logits):
    """Max |diff| over all tokens vs. a runtime-style KV-cache decode with branch caches concatenated."""
    ids, length = sample['input_ids'], sample['length']
    reference = torch.zeros_like(logits)
    cache = DynamicCache()
    cursor, next_position = 0, 0

    def run(begin, end, start_position, kv):
        positions = list(range(start_position, start_position + end - begin))
        reference[begin:end] = forward_logits(model, ids[begin:end], positions, past_key_values=kv)
        return start_position + end - begin

    for block in _blocks(sample):
        if block[0].start > cursor:
            next_position = run(cursor, block[0].start, next_position, cache)
        base = cache.get_seq_length()
        keys = [[] for _ in range(len(cache.key_cache))]
        values = [[] for _ in range(len(cache.key_cache))]
        longest = next_position
        for span in block:
            branch = copy.deepcopy(cache)
            end_position = run(span.start, span.end, next_position, branch)
            longest = max(longest, end_position)
            for layer in range(len(keys)):
                keys[layer].append(branch.key_cache[layer][:, :, base:])
                values[layer].append(branch.value_cache[layer][:, :, base:])
        for layer in range(len(keys)):
            cache.update(torch.cat(keys[layer], dim=2), torch.cat(values[layer], dim=2), layer)
        cursor, next_position = block[-1].end, longest
    if cursor < length:
        run(cursor, length, next_position, cache)
    return (logits - reference).abs().max().item()


def runtime_positions(sample):
    """Positions as the runtime assigns them: branches of a block restart after the shared prefix, the token
    after a block continues from the longest branch's last position + 1 (independent of graph_positions)."""
    positions, position, cursor = [], 0, 0
    for block in _blocks(sample):
        positions += range(position, position + block[0].start - cursor)
        position += block[0].start - cursor
        longest = position
        for span in block:
            positions += range(position, position + span.end - span.start)
            longest = max(longest, position + span.end - span.start)
        cursor, position = block[-1].end, longest
    positions += range(position, position + sample['length'] - cursor)
    return positions


def visibility(sample):
    """(L, L) bool from the definition: causal, except a branch never sees a sibling branch of its block."""
    length = sample['length']
    block = torch.zeros(length, dtype=torch.long)
    path = torch.zeros(length, dtype=torch.long)
    for span in sample['spans']:
        block[span.start:span.end] = span.block
        path[span.start:span.end] = span.path
    sibling = (block[:, None] == block[None, :]) & (path[:, None] != path[None, :]) & (block[:, None] > 0)
    return torch.ones(length, length, dtype=torch.bool).tril() & ~sibling


def _rotate_half(x):
    half = x.shape[-1] // 2
    return torch.cat((-x[..., half:], x[..., :half]), dim=-1)


@torch.no_grad()
def eager_reference(model, sample, logits):
    """Max |diff| vs. a from-scratch fp32 Qwen3 forward (weights from `model`) with an explicit visibility
    matrix and runtime positions: checks the HF 4D-mask path itself."""
    config = model.config
    assert getattr(config, 'rope_scaling', None) in (None, {}), 'eager reference implements plain RoPE only'
    device = _device(model)
    base = model.model
    ids = torch.tensor(sample['input_ids'], device=device)
    allowed = visibility(sample).to(device)
    positions = torch.tensor(runtime_positions(sample), device=device, dtype=torch.float32)
    head_dim = getattr(config, 'head_dim', config.hidden_size // config.num_attention_heads)
    inv_freq = 1.0 / (config.rope_theta ** (torch.arange(0, head_dim, 2, device=device).float() / head_dim))
    freqs = positions[:, None] * inv_freq[None]
    emb = torch.cat((freqs, freqs), dim=-1)
    cos, sin = emb.cos(), emb.sin()

    def norm(module, x):
        x = x.float()
        return module.weight.float() * (x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + module.variance_epsilon))

    def linear(module, x):
        out = x @ module.weight.float().T
        return out + module.bias.float() if module.bias is not None else out

    h = base.embed_tokens.weight.float()[ids]
    L = ids.numel()
    for layer in base.layers:
        attn = layer.self_attn
        x = norm(layer.input_layernorm, h)
        q = linear(attn.q_proj, x).view(L, config.num_attention_heads, head_dim)
        k = linear(attn.k_proj, x).view(L, config.num_key_value_heads, head_dim)
        v = linear(attn.v_proj, x).view(L, config.num_key_value_heads, head_dim)
        q, k = norm(attn.q_norm, q), norm(attn.k_norm, k)
        q = q * cos[:, None] + _rotate_half(q) * sin[:, None]
        k = k * cos[:, None] + _rotate_half(k) * sin[:, None]
        group = config.num_attention_heads // config.num_key_value_heads
        k, v = k.repeat_interleave(group, dim=1), v.repeat_interleave(group, dim=1)
        scores = torch.einsum('qhd,khd->hqk', q, k) * head_dim ** -0.5
        scores = scores.masked_fill(~allowed[None], float('-inf')).softmax(-1)
        out = torch.einsum('hqk,khd->qhd', scores, v).reshape(L, -1)
        h = h + linear(attn.o_proj, out)
        x = norm(layer.post_attention_layernorm, h)
        mlp = layer.mlp
        h = h + linear(mlp.down_proj, torch.nn.functional.silu(linear(mlp.gate_proj, x)) * linear(mlp.up_proj, x))
    h = norm(base.norm, h)
    reference = h @ model.get_output_embeddings().weight.float().T
    return (logits - reference).abs().max().item()


@torch.no_grad()
def causal_control(model, sample, logits):
    """Max |diff| on branches 2.. between the graph forward and a plain causal forward (should be large)."""
    plain = forward_logits(model, sample['input_ids'], list(range(sample['length'])))
    later = [i for span in sample['spans'] if span.path > 1 for i in range(span.start, span.end)]
    return (logits[later] - plain[later]).abs().max().item() if later else 0.0


def check_sample(model, sample, pad_id=0, brute_force=True):
    logits = graph_logits(model, sample, pad_id)
    report = dict(path=path_reference(model, sample, logits), kv=kv_reference(model, sample, logits),
                  causal_control=causal_control(model, sample, logits))
    if brute_force:
        report['eager'] = eager_reference(model, sample, logits)
    return report
