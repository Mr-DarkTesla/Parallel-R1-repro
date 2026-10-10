"""Thinking-SFT v4 data: JSONL rows -> validated, tokenized samples with graph positions and masks.

Row schema (one per line):
    {"id": str, "source": str, "mode": "parallel"|"sequential", "prompt": str,
     "segments": [{"text": str, "loss": bool, "block": int|null, "path": int|null}, ...], "provenance": {...}}

The assistant text is the concatenation of the segment texts; it starts with '<think>' and ends with a
'<|im_end|>' segment. Every tag, <think>, </think> and <|im_end|> is its own segment. A branch is the run
'<Path>', 'i:', body..., '</Path>' carrying block/path (1-based); every other segment has block=path=None.
Runtime-inserted segments ('branches=', '<Plan>', '<Path>', 'i:', '</Parallel>', '<Summary>') have loss=False,
everything else loss=True. Segments are encoded one by one (add_special_tokens=False) and concatenated, as the
runtime inserts its pieces as separate encodes; the prompt is the Qwen3 chat template with enable_thinking=True.

Labels are aligned with input_ids (the trainer shifts): labels[t] = input_ids[t] if token t is in loss else -100.
The token before a branch's first <Path> in serialization order may be a sibling branch's </Path>; <Path> is
inserted (no loss), so no loss ever crosses a branch boundary.
"""
import hashlib
import json
import random
from collections import Counter

import torch

from common import contract

MODES = ('parallel', 'sequential')
SPECIALS = contract.TAGS + contract.CONTROL_TOKENS
INSERTED_FIXED = ('branches=', '<Plan>', '<Path>', '</Parallel>', '<Summary>')
# Per-token control kinds (index into CONTROL_KINDS, -1 otherwise); the first six are the "control loss".
CONTROL_KINDS = ('<Parallel>', 'count', '</Plan>', '</Path>', '</Summary>', '</think>', '<|im_end|>')
CONTROL_LOSS_KINDS = CONTROL_KINDS[:6]
IGNORE = -100
ASSISTANT_PREFIX = '<|im_start|>assistant\n'


class DataError(ValueError):
    def __init__(self, reason, detail=''):
        super().__init__(f'{reason}: {detail}' if detail else reason)
        self.reason = reason


def _check(condition, reason, detail=''):
    if not condition:
        raise DataError(reason, detail)


# ----------------------------------------------------------------------------------------------- segments

def segment(text, loss, block=None, path=None):
    return dict(text=text, loss=loss, block=block, path=path)


def segment_text(text):
    """Canonical segments of an assistant text (generator helper): splits tags and control tokens into their
    own segments, 'branches=' from the count, 'i:' from the branch body, and sets loss/block/path."""
    import re
    pattern = '(' + '|'.join(re.escape(token) for token in SPECIALS) + ')'
    pieces = [piece for piece in re.split(pattern, text) if piece]
    segments, block, path, previous, in_path = [], 0, 0, None, False
    for piece in pieces:
        if piece in SPECIALS:
            if piece == '<Parallel>':
                block += 1
                path = 0
            if piece == '<Path>':
                path += 1
                in_path = True
            loss = piece not in INSERTED_FIXED
            segments.append(segment(piece, loss, block if in_path else None, path if in_path else None))
            if piece == '</Path>':
                in_path = False
        elif previous == '<Parallel>':
            _check(piece.startswith(contract.BRANCHES), 'no_branches', piece[:20])
            segments.append(segment(contract.BRANCHES, False))
            if piece[len(contract.BRANCHES):]:
                segments.append(segment(piece[len(contract.BRANCHES):], True))
        elif previous == '<Path>':
            prefix = contract.path_prefix(path)
            _check(piece.startswith(prefix), 'bad_path_prefix', piece[:20])
            segments.append(segment(prefix, False, block, path))
            if piece[len(prefix):]:
                segments.append(segment(piece[len(prefix):], True, block, path))
        else:
            segments.append(segment(piece, True, block if in_path else None, path if in_path else None))
        previous = piece
    return segments


def make_row(id, source, prompt, assistant_text, provenance=None):
    """A JSONL row from an assistant text (mode inferred from the presence of <Parallel>); validated."""
    segments = segment_text(assistant_text)
    mode = 'parallel' if any(s['text'] == '<Parallel>' for s in segments) else 'sequential'
    row = dict(id=id, source=source, mode=mode, prompt=prompt, segments=segments, provenance=provenance or {})
    validate_row(row)
    return row


def validate_row(row):
    """Raise DataError(reason) unless the row follows the schema and the contract grammar; returns a summary."""
    _check(isinstance(row, dict), 'not_object')
    for key, kind in (('id', str), ('source', str), ('mode', str), ('prompt', str), ('segments', list)):
        _check(isinstance(row.get(key), kind), 'bad_field', key)
    _check(row['mode'] in MODES, 'bad_mode', row['mode'])
    segs = row['segments']
    _check(len(segs) >= 3, 'too_few_segments')
    for s in segs:
        _check(isinstance(s, dict) and isinstance(s.get('text'), str) and isinstance(s.get('loss'), bool),
               'bad_segment', str(s)[:80])
        _check(s['text'] != '', 'empty_segment')
        for key in ('block', 'path'):
            _check(key in s and (s[key] is None or (isinstance(s[key], int) and not isinstance(s[key], bool))),
                   'bad_segment', f'{key} in {str(s)[:80]}')
        if s['text'] not in SPECIALS:
            _check(not any(token in s['text'] for token in SPECIALS), 'tag_not_own_segment', s['text'][:80])
    _check(contract.plain_text(row['prompt']), 'tag_in_prompt')

    n = len(segs)
    state = dict(pos=0, blocks=[])

    def take(text=None, loss=True, block=None, path=None, what=''):
        _check(state['pos'] < n, 'truncated', what)
        s = segs[state['pos']]
        if text is not None:
            _check(s['text'] == text, 'unexpected_segment', f'want {text!r} got {s["text"][:40]!r} at {state["pos"]}')
        _check(s['loss'] is loss, 'bad_loss', f'{s["text"][:40]!r} at {state["pos"]} should have loss={loss}')
        _check(s['block'] == block and s['path'] == path, 'bad_block_path',
               f'{s["text"][:40]!r} at {state["pos"]}: ({s["block"]}, {s["path"]}) != ({block}, {path})')
        state['pos'] += 1
        return s['text']

    def body(block=None, path=None, stop=None, what=''):
        texts = []
        while state['pos'] < n and segs[state['pos']]['text'] not in SPECIALS:
            texts.append(take(None, True, block, path, what))
        _check(state['pos'] < n and segs[state['pos']]['text'] == stop, 'unterminated_' + what,
               segs[state['pos']]['text'][:40] if state['pos'] < n else 'end')
        text = ''.join(texts)
        _check(contract.plain_text(text), 'tag_in_' + what)
        return text

    take('<think>', what='think')
    think_closed = False
    while state['pos'] < n - 1:
        text = segs[state['pos']]['text']
        if text == '</think>':
            _check(not think_closed, 'think_closed_twice')
            take('</think>')
            think_closed = True
        elif text == '<Parallel>':
            b = len(state['blocks']) + 1
            _check(b <= contract.MAX_BLOCKS, 'too_many_blocks')
            take('<Parallel>')
            take(contract.BRANCHES, loss=False)
            count = take(None, True, what='count')
            _check(count in contract.COUNTS, 'bad_count', count[:20])
            branches = int(count)
            take('<Plan>', loss=False)
            plan_text = body(stop='</Plan>', what='plan')
            plan = contract.parse_plan(plan_text, branches)
            _check(plan is not None, 'invalid_plan', plan_text[:120])
            take('</Plan>')
            for k in range(1, branches + 1):
                take('<Path>', False, b, k)
                take(contract.path_prefix(k), False, b, k, what='path_prefix')
                body(b, k, stop='</Path>', what='path')
                take('</Path>', True, b, k)
            take('</Parallel>', loss=False)
            take('<Summary>', loss=False)
            body(stop='</Summary>', what='summary')
            take('</Summary>')
            state['blocks'].append(dict(kind=plan.kind, branches=branches))
        elif text in SPECIALS:
            raise DataError('unexpected_' + text.strip('<>/|'), f'at {state["pos"]}')
        else:
            take(None, True, what='main')
    _check(think_closed, 'no_think_close')
    _check(state['pos'] == n - 1, 'truncated')
    take('<|im_end|>', what='im_end')
    # A tag or control token split across adjacent text segments (main/answer runs included) is not caught per
    # segment; re-tokenizing the assistant string would then give ids the sample does not have.
    run = []
    for s in segs + [None]:
        if s is not None and s['text'] not in SPECIALS:
            run.append(s['text'])
            continue
        _check(contract.plain_text(''.join(run)), 'tag_in_text', ''.join(run)[:80])
        run = []
    _check(''.join(s['text'] for s in segs).endswith('<|im_end|>'), 'no_im_end')
    _check((row['mode'] == 'parallel') == bool(state['blocks']), 'mode_mismatch',
           f'{row["mode"]} with {len(state["blocks"])} blocks')
    return dict(blocks=state['blocks'])


# ------------------------------------------------------------------------------------------- tokenization

class Vocab:
    """Single-token ids the dataset asserts against (computed once per tokenizer)."""

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.special = dict(contract.token_ids(tokenizer))
        im_end = tokenizer.encode('<|im_end|>', add_special_tokens=False)
        _check(len(im_end) == 1, 'im_end_not_single_token')
        self.special['<|im_end|>'] = im_end[0]
        self.counts = contract.count_ids(tokenizer)
        self.branches = contract.branches_ids(tokenizer)
        self.prefixes = {k: contract.path_prefix_ids(tokenizer, k) for k in range(1, contract.MAX_PATHS + 1)}
        self.pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id


def prompt_text(tokenizer, prompt):
    text = tokenizer.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=False,
                                         add_generation_prompt=True, enable_thinking=True)
    _check(text.endswith(ASSISTANT_PREFIX), 'bad_chat_template', repr(text[-40:]))
    return text


def tokenize_row(row, vocab):
    """Validated row -> sample dict (python lists + Span list); raises DataError."""
    validate_row(row)
    tokenizer = vocab.tokenizer
    prompt_ids = tokenizer.encode(prompt_text(tokenizer, row['prompt']), add_special_tokens=False)
    texts = [s['text'] for s in row['segments']]
    encoded = tokenizer(texts, add_special_tokens=False)['input_ids']
    input_ids, labels, control = list(prompt_ids), [IGNORE] * len(prompt_ids), [-1] * len(prompt_ids)
    spans, start, previous = [], None, None
    for s, ids in zip(row['segments'], encoded):
        text = s['text']
        if text in vocab.special:
            _check(ids == [vocab.special[text]], 'tag_not_single_token', f'{text} -> {ids}')
        elif text == contract.BRANCHES and previous == '<Parallel>':
            _check(ids == vocab.branches, 'branches_ids', str(ids))
        elif previous == '<Path>':
            _check(ids == vocab.prefixes[s['path']], 'path_prefix_ids', str(ids))
        elif previous == contract.BRANCHES and text in contract.COUNTS:
            _check(len(ids) == 1 and ids[0] in vocab.counts, 'count_not_single_token', str(ids))
        _check(len(ids) > 0, 'empty_encoding', repr(text[:40]))
        if text == '<Path>':
            start = len(input_ids)
        kind = -1
        if text in CONTROL_KINDS:
            kind = CONTROL_KINDS.index(text)
        elif previous == contract.BRANCHES and text in contract.COUNTS:
            kind = CONTROL_KINDS.index('count')
        input_ids += ids
        labels += ids if s['loss'] else [IGNORE] * len(ids)
        control += [kind] * len(ids)
        if text == '</Path>':
            spans.append(contract.Span(start, len(input_ids), s['block'], s['path']))
        previous = text
    length = len(input_ids)
    if spans:
        positions = contract.graph_positions(length, spans)
        for span in spans:  # no loss crosses a branch boundary (the branch's first token is the inserted <Path>)
            assert labels[span.start] == IGNORE
    else:
        positions = list(range(length))
    return dict(id=row['id'], source=row['source'], mode=row['mode'], group=group_key(row), input_ids=input_ids,
                labels=labels, position_ids=positions, spans=spans, control=control, length=length,
                prompt_length=len(prompt_ids), n_loss=sum(label != IGNORE for label in labels))


def read_jsonl(path):
    with open(path) as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as error:
                    yield DataError('bad_json', f'line {number}: {error}')


def build_dataset(rows, tokenizer, max_len, strict=False):
    """(samples, stats). Rows failing validation or longer than max_len are dropped and counted by reason
    (strict=True raises on the first invalid row instead; too-long rows are always only dropped)."""
    vocab = tokenizer if isinstance(tokenizer, Vocab) else Vocab(tokenizer)
    samples, dropped, examples = [], Counter(), {}
    total = 0
    for row in rows:
        total += 1
        try:
            if isinstance(row, DataError):
                raise row
            sample = tokenize_row(row, vocab)
        except DataError as error:
            if strict:
                raise
            dropped[error.reason] += 1
            examples.setdefault(error.reason, f'{row.get("id") if isinstance(row, dict) else "?"}: {error}'[:300])
            continue
        if sample['length'] > max_len:
            dropped['too_long'] += 1
            examples.setdefault('too_long', f'{sample["id"]}: {sample["length"]} > {max_len}')
            continue
        samples.append(sample)
    stats = dict(total=total, kept=len(samples), dropped=dict(dropped), invalid=sum(
        count for reason, count in dropped.items() if reason != 'too_long'), drop_examples=examples,
        by_mode=dict(Counter(s['mode'] for s in samples)), by_source=dict(Counter(s['source'] for s in samples)),
        tokens=sum(s['length'] for s in samples), loss_tokens=sum(s['n_loss'] for s in samples),
        max_length=max((s['length'] for s in samples), default=0))
    return samples, stats


def group_key(row):
    """Validation-split key shared by every row of one problem (parallel and sequential modes, several samples):
    provenance problem_id when the generator records one, else the sha256 of the prompt."""
    provenance = row.get('provenance') if isinstance(row.get('provenance'), dict) else {}
    problem = provenance.get('problem_id')
    if problem not in (None, ''):
        return f'problem:{problem}'
    return 'prompt:' + hashlib.sha256(row['prompt'].encode()).hexdigest()


def id_in_val(key, frac):
    """True if the split key (group_key of a sample) falls in the validation fraction."""
    digest = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
    return digest % 100000 < frac * 100000


# ----------------------------------------------------------------------------------------------- batching

def collate(samples, pad_id, dtype=torch.float32, device=None):
    """Right-padded batch with an additive (B, 1, T, T) mask in `dtype` (0 = attend, finfo.min = blocked).

    Real queries see their sample's contract.graph_attention_mask and never a padded key; a padded query
    attends to itself only (no fully masked row, so no NaN). Padded positions continue the last position."""
    lengths = [s['length'] for s in samples]
    B, T = len(samples), max(lengths)
    input_ids = torch.full((B, T), pad_id, dtype=torch.long)
    labels = torch.full((B, T), IGNORE, dtype=torch.long)
    position_ids = torch.zeros((B, T), dtype=torch.long)
    control = torch.full((B, T), -1, dtype=torch.long)
    allowed = torch.zeros((B, T, T), dtype=torch.bool, device=device)
    for b, s in enumerate(samples):
        L = s['length']
        input_ids[b, :L] = torch.tensor(s['input_ids'])
        labels[b, :L] = torch.tensor(s['labels'])
        position_ids[b, :L] = torch.tensor(s['position_ids'])
        last = s['position_ids'][-1]
        position_ids[b, L:] = torch.arange(last + 1, last + 1 + T - L)
        control[b, :L] = torch.tensor(s['control'])
        allowed[b, :L, :L] = contract.graph_attention_mask(L, s['spans'], device=device)
        pad = torch.arange(L, T, device=device)
        allowed[b, pad, pad] = True
    mask = torch.zeros((B, 1, T, T), dtype=dtype, device=device)
    mask.masked_fill_(~allowed[:, None], torch.finfo(dtype).min)
    batch = dict(input_ids=input_ids, labels=labels, position_ids=position_ids, control=control)
    if device is not None:
        batch = {key: value.to(device) for key, value in batch.items()}
    batch.update(attention_mask=mask, lengths=lengths, modes=[s['mode'] for s in samples],
                 mode_index=torch.tensor([MODES.index(s['mode']) for s in samples], device=device),
                 ids=[s['id'] for s in samples])
    return batch


def token_batches(lengths, max_tokens, seed=0, shuffle=True, window=512):
    """Micro-batches of sample indices with batch_size * longest <= max_tokens (a longer sample is alone).
    Shuffled, then sorted by length within windows of `window` samples so padding stays small."""
    order = list(range(len(lengths)))
    rng = random.Random(seed)
    if shuffle:
        rng.shuffle(order)
    batches = []
    for begin in range(0, len(order), window):
        chunk = sorted(order[begin:begin + window], key=lambda i: -lengths[i])
        current, longest = [], 0
        for index in chunk:
            new_longest = max(longest, lengths[index])
            if current and new_longest * (len(current) + 1) > max_tokens:
                batches.append(current)
                current, new_longest = [], lengths[index]
            current.append(index)
            longest = new_longest
        if current:
            batches.append(current)
    if shuffle:
        rng.shuffle(batches)
    return batches


def group_steps(batches, lengths, accum_tokens):
    """Optimizer steps: consecutive micro-batches until their real (unpadded) tokens reach accum_tokens."""
    steps, current, tokens = [], [], 0
    for batch in batches:
        current.append(batch)
        tokens += sum(lengths[i] for i in batch)
        if tokens >= accum_tokens:
            steps.append(current)
            current, tokens = [], 0
    if current:
        steps.append(current)
    return steps


def render(sample, tokenizer, max_chars=None):
    """Decoded sample with no-loss assistant tokens in [[...]] (the prompt is shown as <prompt>)."""
    out, open_ = [], False
    for t, (token, label) in enumerate(zip(sample['input_ids'], sample['labels'])):
        if t < sample['prompt_length']:
            continue
        piece = tokenizer.decode([token])
        if label == IGNORE and not open_:
            out.append('[[')
            open_ = True
        elif label != IGNORE and open_:
            out.append(']]')
            open_ = False
        out.append(piece)
    if open_:
        out.append(']]')
    text = '<prompt>' + ''.join(out)
    return text if max_chars is None else text[:max_chars]
