"""Parallel-thinking serialization contract shared by the generator, SFT and RL (agreed 2026-10-09).

    ... <Parallel><Plan>kind
    1: ...
    2: ...
    </Plan><Path>1: ...</Path><Path>2: ...</Path></Parallel><Summary>...</Summary> ...

The model samples <Parallel> (the only fork decision), the plan text and </Plan>, branch text and
</Path>, summary text and </Summary>. The runtime inserts <Plan> after <Parallel>, <Path> plus "i:"
at the start of branch i, and </Parallel><Summary> after the last branch; inserted tokens are
context only (no SFT loss, no RL log-prob). The model writes " text" after "i:" itself. No token sits
between </Plan> and the first <Path> or between </Path> and the next <Path>: a separator would let
branch B read branch A through it. An invalid, unfinished or over-budget plan ends the trajectory
with c = 0; plans are never repaired and blocks are never empty.

Branches of one block start at the position after their shared prefix (through </Plan>); </Parallel>
takes the longest branch's last position + 1 and positions continue from there. A query never sees a
key in another branch of the same block; everything else is causal in serialization order.
Pure Python + torch so the generator, the SFT dataset and the RL actor import the same code.
"""
import re
from dataclasses import dataclass

import torch

CONTRACT_VERSION = 1
TAGS = ('<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>', '<Plan>', '</Plan>')
PLAN_KINDS = ('decompose', 'cases', 'candidates', 'methods', 'verify')
MIN_PATHS, MAX_PATHS = 2, 4
MAX_BLOCKS = 2  # cap, not quota: the next <Parallel> is suppressed

VALID, INVALID_PLAN, PLAN_INCOMPLETE, PLAN_BUDGET_EXHAUSTED = (
    'valid', 'invalid_plan', 'plan_incomplete', 'plan_budget_exhausted')

# Generation nodes. Each samples one closing tag (main: <Parallel> while blocks remain); every other tag
# gets SUPPRESS_BIAS, identically in sampling (vLLM logit_bias) and in replay (actor logits).
MAIN_OPEN, MAIN_CLOSED, PLAN, PATH, SUMMARY = range(5)
INSERTED = -1  # runtime-inserted token: no log-prob
SAMPLED_TAG = {MAIN_OPEN: '<Parallel>', MAIN_CLOSED: None, PLAN: '</Plan>', PATH: '</Path>', SUMMARY: '</Summary>'}
SUPPRESS_BIAS = -100.0
# Runtime-inserted text: after a sampled <Parallel>, and after the last branch of a block.
PLAN_OPEN, BLOCK_CLOSE = ('<Plan>',), ('</Parallel>', '<Summary>')
_ITEM = re.compile(r'\s*(\d+)\s*:\s*(\S.*?)\s*')


@dataclass(frozen=True)
class Plan:
    kind: str
    items: tuple


def parse_plan(text):
    """Plan between <Plan> and </Plan> (exclusive), or None if it breaks the grammar.

    First line: a kind from PLAN_KINDS. Then MIN_PATHS..MAX_PATHS lines "i: text", i = 1..n in order,
    non-empty one-line text. One trailing newline is allowed; no blank lines or other text.
    Normalization (CRLF, surrounding spaces) happens only here; sampled ids are never rewritten.
    """
    text = text.replace('\r\n', '\n')
    if text.endswith('\n'):
        text = text[:-1]
    kind, *lines = text.split('\n')
    if kind.strip() not in PLAN_KINDS or not MIN_PATHS <= len(lines) <= MAX_PATHS:
        return None
    items = []
    for number, line in enumerate(lines, 1):
        match = _ITEM.fullmatch(line)
        if match is None or int(match.group(1)) != number:
            return None
        items.append(match.group(2))
    return Plan(kind.strip(), tuple(items))


def plan_status(text, stop):
    """Status of a plan call: stop is 'close' (sampled </Plan>), 'eos' or 'budget'."""
    if stop == 'eos':
        return PLAN_INCOMPLETE
    if stop == 'budget':
        return PLAN_BUDGET_EXHAUSTED
    return VALID if parse_plan(text) is not None else INVALID_PLAN


def path_prefix(number):
    """Text the runtime inserts after <Path> for branch `number` (1-based)."""
    return f'{number}:'


def path_prefix_ids(tokenizer, number):
    """Token ids of path_prefix(number), encoded on their own (the model's text after them is a separate call)."""
    return tokenizer.encode(path_prefix(number), add_special_tokens=False)


def main_node(blocks_done, max_blocks=MAX_BLOCKS, allow_parallel=True):
    return MAIN_OPEN if allow_parallel and blocks_done < max_blocks else MAIN_CLOSED


def suppressed_tags(node):
    return tuple(tag for tag in TAGS if tag != SAMPLED_TAG[node])


def tag_ids(tokenizer):
    """Single-token ids of all tags; raises if the tokenizer lacks one."""
    ids = {}
    for tag in TAGS:
        encoded = tokenizer.encode(tag, add_special_tokens=False)
        if len(encoded) != 1:
            raise ValueError(f'{tag} must be one token, got {encoded}')
        ids[tag] = encoded[0]
    if len(set(ids.values())) != len(TAGS):
        raise ValueError(f'Tags must have distinct ids: {ids}')
    return ids


def logit_bias(node, ids):
    return {ids[tag]: SUPPRESS_BIAS for tag in suppressed_tags(node)}


def suppression_table(ids):
    """(nodes, len(TAGS)) tensor of suppressed token ids per node code, -1 padded."""
    rows = [[ids[tag] for tag in suppressed_tags(node)] for node in range(len(SAMPLED_TAG))]
    width = max(map(len, rows))
    return torch.tensor([row + [-1] * (width - len(row)) for row in rows], dtype=torch.long)


def apply_suppression(logits, nodes, table):
    """Add SUPPRESS_BIAS in place to suppressed tags where logits[b, t] predicts a token of node nodes[b, t]."""
    for node in range(table.size(0)):
        rows, columns = (nodes == node).nonzero(as_tuple=True)
        banned = table[node][table[node] >= 0].to(logits.device)
        if rows.numel() and banned.numel():
            logits.index_put_((rows[:, None], columns[:, None], banned[None, :]),
                              torch.tensor(SUPPRESS_BIAS, dtype=logits.dtype, device=logits.device), accumulate=True)
    return logits


@dataclass(frozen=True, order=True)
class Span:
    """Branch [start, end) in sequence coordinates: <Path> through </Path> (or the cut)."""
    start: int
    end: int
    block: int
    path: int


def graph_positions(length, spans, first=0):
    """Position ids for a serialized sequence of `length` tokens with branch spans."""
    blocks = {}
    for span in spans:
        if span.start < length:
            blocks.setdefault(span.block, []).append(span)
    starts = {}
    for block in blocks.values():
        block.sort(key=lambda span: span.start)
        for left, right in zip(block, block[1:]):
            assert left.end == right.start, f'tokens between branches {left} and {right}'
        starts[block[0].start] = block
    positions, position, index = [], first, 0
    while index < length:
        block = starts.get(index)
        if block is None:
            positions.append(position)
            position, index = position + 1, index + 1
            continue
        longest = position - 1
        for span in block:
            size = min(span.end, length) - span.start
            positions.extend(range(position, position + size))
            longest = max(longest, position + size - 1)
        index = min(block[-1].end, length)
        position = longest + 1
    return positions


def isolation_pairs(spans):
    """Ordered (query span, key span) pairs that must not attend: different branches of one block."""
    return [(a, b) for a in spans for b in spans if a.block == b.block and a.path != b.path]


def graph_attention_mask(length, spans, offset=0):
    """(length, length) bool mask, True = may attend; spans are shifted by offset (e.g. left padding)."""
    mask = torch.ones(length, length, dtype=torch.bool).tril()
    for query, key in isolation_pairs(spans):
        mask[offset + query.start:offset + query.end, offset + key.start:offset + key.end] = False
    return mask


def depth_and_tokens(calls):
    """(D, T) from sampled-token counts per generation call.

    calls: dicts with node (MAIN_*, PLAN, PATH, SUMMARY), block (None for main) and sampled.
    T counts every sampled token, a failed plan included. D adds main segments and, per block,
    plan + longest branch + summary. Runtime-inserted tokens count in neither.
    """
    depth = tokens = 0
    longest = {}
    for call in calls:
        tokens += call['sampled']
        if call['node'] == PATH:
            longest[call['block']] = max(longest.get(call['block'], 0), call['sampled'])
        else:
            depth += call['sampled']
    return depth + sum(longest.values()), tokens
