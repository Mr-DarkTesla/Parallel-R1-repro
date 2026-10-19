"""Pure CPU data compiler. target_mask indexes TARGET slots (shift once at CE).

Preserves assistant bytes; sibling separator whitespace belongs to preceding
path. Attention True means allowed, matching torch SDPA boolean convention.
"""
import re
from decimal import Decimal, InvalidOperation

XML = ('<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>')
OPENER = '<think>\n'
CONTROL = re.compile(r'</?(?:Parallel|Path|Summary)>')


def _parse(content, answer=None):
    if not isinstance(content, str) or not content.startswith(OPENER):
        raise ValueError('Assistant must begin exactly with native <think> newline')
    if content.count('<think>') != 1 or content.count('</think>') != 1:
        raise ValueError('Exactly one complete think block required')
    end = content.index('</think>')
    outside = content[end + len('</think>'):]
    finals = list(re.finditer(r'^Final Answer:\s*(.+)$', outside, re.M))
    if len(finals) != 1 or outside[finals[0].end():].strip() or CONTROL.search(outside):
        raise ValueError('Exactly one terminal Final Answer outside think required')
    if re.search(r'<\|[^>]*\|>', content):
        raise ValueError('Source contains native chat/EOS controls')
    if answer is not None:
        final = finals[0].group(1).strip()
        box = re.fullmatch(r'\\boxed\{([^{}]+)\}', final)
        if box is None:
            raise ValueError('Dataset final must be one numeric boxed answer')
        try:
            if Decimal(box.group(1).replace(',', '').strip()) != Decimal(str(answer).strip()):
                raise ValueError('Final boxed answer differs from source gold')
        except InvalidOperation as exc:
            raise ValueError('Non-numeric GSM gold/final') from exc
    blocks, forced, covered = [], [], []
    previous = len(OPENER)
    for match in re.finditer(r'<Parallel>(.*?)</Parallel>', content[:end], re.S):
        body = match.group(1)
        header = re.match(r'([2-8])\n', body)
        if header is None:
            raise ValueError('Width must be 2..8 followed by newline')
        width = int(header.group(1))
        paths = list(re.finditer(r'<Path>([1-8])\n(.*?)</Path>', body, re.S))
        if len(paths) != width or [int(p.group(1)) for p in paths] != list(range(1, width + 1)):
            raise ValueError('Path count/IDs disagree with width')
        rest = body[header.end():]
        if re.sub(r'<Path>[1-8]\n.*?</Path>', '', rest, flags=re.S).strip():
            raise ValueError('Non-whitespace outside sibling paths')
        lead = content[previous:match.start()]
        plan = lead.rsplit('Plan:', 1)[-1] if 'Plan:' in lead else ''
        plan_ids = [int(x) for x in re.findall(r'^\s*([1-8]):', plan, re.M)]
        if plan_ids != list(range(1, width + 1)):
            raise ValueError('Plan IDs disagree with width')
        charpaths = []
        for path in paths:
            if not path.group(2).strip() or CONTROL.search(path.group(2)) or re.search(r'Final Answer:|</?think>|\\(?:boxed|fbox)', path.group(2)):
                raise ValueError('Empty/nested/final answer inside Path')
            start = match.start(1) + path.start()
            header_end = match.start(1) + path.start(2)
            finish = match.start(1) + path.end()
            forced.append((start, header_end, 'path_header'))
            charpaths.append((start, finish))
        summary = re.match(r'\s*<Summary>(.*?)</Summary>', content[match.end():end], re.S)
        if summary is None or not summary.group(1).strip() or CONTROL.search(summary.group(1)) or re.search(r'Final Answer:|</?think>|\\(?:boxed|fbox)', summary.group(1)):
            raise ValueError('Missing/invalid Summary')
        summary_open_end = match.end() + summary.start(1)
        forced.append((match.end() - len('</Parallel>'), summary_open_end, 'compiler_bridge'))
        finish = match.end() + summary.end()
        covered.append((match.start(), finish))
        blocks.append({'width': width, 'paths': charpaths, 'parallel_close': match.end() - len('</Parallel>')})
        previous = finish
    if any(not any(a <= t.start() < b for a, b in covered) for t in CONTROL.finditer(content[:end])):
        raise ValueError('Orphan/misnested XML control')
    return blocks, forced


def _positions(length, spans):
    result = [0] * length
    cursor = pos = 0
    for block in spans:
        first = block[0][0]
        result[cursor:first] = range(pos, pos + first - cursor)
        pos += first - cursor
        for start, finish in block:
            result[start:finish] = range(pos, pos + finish - start)
        pos += max(finish - start for start, finish in block)
        cursor = block[-1][1]
    result[cursor:] = range(pos, pos + length - cursor)
    return result


def can_attend(query, key, spans):
    if key > query:
        return False
    for block in spans:
        first = block[0][0]
        for start, finish in block[1:]:
            if start <= query < finish and first <= key < start:
                return False
    return True


def build_attention(sample, device=None):
    """Return [L,L] bool mask, True=allowed; caller adds batch/head axes."""
    import torch
    n = len(sample['input_ids'])
    mask = torch.ones((n, n), dtype=torch.bool, device=device).tril_()
    for block in sample['spans']:
        first = block[0][0]
        for start, finish in block[1:]:
            mask[start:finish, first:start] = False
    return mask


def build_sample(row, tok, system, max_length=8192):
    if not getattr(tok, 'is_fast', False):
        raise ValueError('Fast tokenizer offsets required')
    tag_ids = {}
    for tag in XML:
        ids = tok.encode(tag, add_special_tokens=False)
        if len(ids) != 1 or ids[0] == tok.unk_token_id:
            raise ValueError('Six XML tags must each encode as one distinct token')
        tag_ids[tag] = ids[0]
    if len(set(tag_ids.values())) != 6:
        raise ValueError('XML token IDs alias')
    content = row.get('assistant_content', row.get('response'))
    if 'assistant_content' in row and 'response' in row and row['assistant_content'] != row['response']:
        raise ValueError('Ambiguous source assistant content')
    blocks, forced_chars = _parse(content, row.get('answer'))
    problem = row.get('problem')
    if not isinstance(problem, str) or not problem.strip() or not isinstance(system, str) or not system.strip():
        raise ValueError('Nonempty problem and system required')
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': problem}]
    prefix = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
    if prefix.endswith('<think>'):
        prefix += '\n'
    elif not prefix.endswith(OPENER):
        prefix += OPENER
    prompt_ids = tok.encode(prefix, add_special_tokens=False)
    if tok.decode(prompt_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False) != prefix:
        raise ValueError('Prompt token roundtrip differs')
    response = content[len(OPENER):]
    encoded = tok(response, add_special_tokens=False, return_offsets_mapping=True)
    ids = list(encoded['input_ids'])
    offsets = [tuple(x) for x in encoded['offset_mapping']]
    if len(ids) != len(offsets) or any(b <= a for a, b in offsets):
        raise ValueError('Invalid fast tokenizer response offsets')
    if tok.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False) != response:
        raise ValueError('Response token roundtrip differs')
    end_ids = tok.encode('<|im_end|>', add_special_tokens=False)
    if len(end_ids) != 1:
        raise ValueError('Native im_end must be a single token')
    start = len(prompt_ids)
    input_ids = prompt_ids + ids + end_ids
    if len(input_ids) > max_length:
        raise ValueError(f'No truncation permitted: {len(input_ids)} > {max_length}')
    target_mask = [0] * start + [1] * (len(ids) + 1)
    telemetry = []
    forced = [(a-len(OPENER), b-len(OPENER), kind) for a, b, kind in forced_chars]
    for index, (a, b) in enumerate(offsets):
        overlaps = [(s, e, kind) for s, e, kind in forced if a < e and s < b]
        if overlaps:
            target_mask[start + index] = 1 # FULL SFT: learn every response token
            if not any(s <= a and b <= e for s, e, _ in overlaps):
                # Byte-level BPE can merge forced newline with adjacent whitespace.
                spill = ''.join(response[j] for j in range(a, b) if not any(s <= j < e for s, e, _ in overlaps))
                if spill.strip():
                    raise ValueError('Token straddles forced boundary into semantic text')
                telemetry.append({'token_index': start + index, 'char_span': [a, b], 'masked_whitespace_spill': spill, 'reason': 'forced_boundary_whitespace_token'})
    def token_at(char, tag):
        rel = char - len(OPENER)
        candidates = [i for i, (a, b) in enumerate(offsets) if a == rel and ids[i] == tag_ids[tag]]
        if len(candidates) != 1:
            raise ValueError('Control token offset not exact')
        return start + candidates[0]
    spans = []
    for block in blocks:
        opening = [token_at(a, '<Path>') for a, _ in block['paths']]
        closing = token_at(block['parallel_close'], '</Parallel>')
        spans.append([(s, opening[i+1] if i+1 < len(opening) else closing) for i, s in enumerate(opening)])
    position_ids = _positions(len(input_ids), spans)
    assert len(input_ids) == len(position_ids) == len(target_mask)
    assert target_mask[-1] == 1 and input_ids[-1] == end_ids[0]
    return {'input_ids': input_ids, 'position_ids': position_ids, 'target_mask': target_mask,
            'spans': spans, 'prompt_length': start, 'widths': [b['width'] for b in blocks],
            'forced_char_spans': forced_chars, 'boundary_telemetry': telemetry,
            'source_response_preserved': True, 'native_end_id': end_ids[0]}
