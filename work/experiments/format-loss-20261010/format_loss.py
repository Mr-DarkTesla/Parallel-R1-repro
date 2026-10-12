"""Structural CE weights, in TARGET coordinates, preserving runtime action masks.

Epoch 1: supervised format only. Epoch 2+: format weight 5, content weight 1.
This changes the objective, never tokens, attention, positions, or frozen weights.
"""
import re

XML = re.compile(r'</?(?:Parallel|Path|Summary)>')
OPENER = '<think>\n'


def structural_spans(content):
    """Syntax only: no assignment prose, arithmetic, or answer value."""
    spans = [(m.start(), m.end()) for m in XML.finditer(content)]
    for pattern in [r'<Parallel>[2-8]\n', r'<Path>[1-8]\n',
                    r'</think>', r'^Final Answer:[ \t]*']:
        spans.extend((m.start(), m.end()) for m in re.finditer(pattern, content, re.M))
    # Only the last Plan preceding each real round. Numbered arithmetic inside
    # Path/Summary is semantic content, not a planning header.
    previous = len(OPENER)
    for block in re.finditer(r'<Parallel>.*?</Parallel>\s*<Summary>.*?</Summary>', content, re.S):
        plan_at = content.rfind('Plan:', previous, block.start())
        if plan_at < 0:
            raise ValueError('Validated round has no preceding Plan')
        spans.append((plan_at, plan_at + len('Plan:')))
        plan = content[plan_at + len('Plan:'):block.start()]
        base = plan_at + len('Plan:')
        for m in re.finditer(r'^[ \t]*[1-8]:[ \t]*', plan, re.M):
            spans.append((base + m.start(), base + m.end()))
        previous = block.end()
    # Dataset compiler has already validated one terminal numeric boxed answer.
    final = re.search(r'^Final Answer:\s*\\boxed\{([^{}]+)\}\s*$', content, re.M)
    if final:
        boxed_at = content.index('\\boxed{', final.start(), final.end())
        spans.append((boxed_at, boxed_at + len('\\boxed{')))
        spans.append((final.end(1), final.end(1) + 1))
    return spans


def attach_format_mask(sample, row, tokenizer):
    content = row.get('assistant_content', row.get('response'))
    if not content.startswith(OPENER):
        raise ValueError('Expected validated canonical assistant response')
    response = content[len(OPENER):]
    encoded = tokenizer(response, add_special_tokens=False, return_offsets_mapping=True)
    start = sample['prompt_length']
    if sample['input_ids'][start:-1] != list(encoded['input_ids']):
        raise ValueError('Response tokenization differs from baseline compiler')
    spans = [(a - len(OPENER), b - len(OPENER)) for a, b in structural_spans(content)]
    covered_chars = [False] * len(response)
    for a, b in spans:
        covered_chars[max(0, a):max(0, b)] = [True] * (max(0, b) - max(0, a))
    mask = [0] * len(sample['input_ids'])
    for i, (a, b) in enumerate(encoded['offset_mapping']):
        # Fully-covered syntax or whitespace only. Never amplify arithmetic
        # merely because a BPE token straddles a format boundary.
        uncovered = ''.join(response[j] for j in range(a, b) if not covered_chars[j])
        covered = any(covered_chars[a:b])
        if sample['target_mask'][start + i] and covered and not uncovered.strip():
            mask[start + i] = 1
    mask[-1] = sample['target_mask'][-1]  # model-sampled native end-of-message
    if not any(mask):
        raise ValueError('No supervised structural target')
    if any(f and not t for f, t in zip(mask, sample['target_mask'])):
        raise AssertionError('Forced token or prompt entered the loss')
    return {**sample, 'format_mask': mask}


def target_weights(target_mask, format_mask, epoch, format_weight=5.0):
    if epoch < 1 or format_weight <= 0:
        raise ValueError('Positive epoch and structural weight required')
    if len(target_mask) != len(format_mask):
        raise ValueError('Masks must have equal lengths')
    if any(f and not t for t, f in zip(target_mask, format_mask)):
        raise ValueError('Structural mask must be a subset of sampled targets')
    result = [float(f) if epoch == 1 else float(t) * (format_weight if f else 1.0)
              for t, f in zip(target_mask, format_mask)]
    if sum(result) <= 0:
        raise ValueError('Empty objective: refuse silent zero-gradient sample')
    return result


def weighted_ce(ce, sample, epoch, format_weight=5.0):
    # CE[i] predicts input_ids[i+1]; shift TARGET weights exactly once.
    weights = ce.new_tensor(target_weights(sample['target_mask'], sample['format_mask'],
                                         epoch, format_weight)[1:])
    if ce.shape != weights.shape:
        raise ValueError('CE and shifted TARGET weights differ')
    return (ce * weights).sum() / weights.sum()
