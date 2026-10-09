# Tagged accepted24 source B

Input: `accepted24_source_b.jsonl`, 12 rows in original order. Read source B only. No gold/eval content, GPU, Kubernetes, or proxy access.

Method: shared setup retained before one numbered Multiverse block inside the existing `<think>`. Original first and second calculation passages placed unchanged in sibling Paths, in original order. Original merge retained after block. Only Goal/Conclusion text and tag/path labels added.

Validation: actual `scripts/exp21/mv_format.py` and `checks.py`, run with `/tmp/exp21-audit-venv/bin/python`. Reference for answer preservation is each source response's own final answer; this does not independently score correctness against gold. Recovery compares every non-whitespace character after removing added Goal/Conclusion, tags and path labels. Existing `checks.py` also checks numeric-token preservation. Final answer suffix preserved exactly. Every block is singular, numbered, and inside `<think>`; every Path is at least 80 characters.

Command: `/tmp/exp21-audit-venv/bin/python - <<'PY'` with source read, span extraction at original calculation headers, one block insertion, `mv_format.parse(response)`, and `checks.check(response, checks.candidate(original), "blind_public", original=original)`; output order follows input order.

## Results

- `math-train/4047`: tagged; Path characters [294, 405]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/3699`: tagged; Path characters [217, 155]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/2843`: tagged; Path characters [233, 356]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/4099`: tagged; Path characters [237, 327]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/4156`: tagged; Path characters [394, 251]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/1177`: tagged; Path characters [283, 254]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/7294`: tagged; Path characters [384, 352]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/2326`: tagged; Path characters [283, 292]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/2204`: tagged; Path characters [200, 208]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/6288`: tagged; Path characters [222, 236]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/2789`: tagged; Path characters [184, 269]; issues []; original text recovery True; final answer unchanged True; one block inside think True.
- `math-train/7420`: tagged; Path characters [219, 225]; issues []; original text recovery True; final answer unchanged True; one block inside think True.

Tagged: 12/12. Flagged: 0.

## Saved-file validation command

```bash
/tmp/exp21-audit-venv/bin/python -B - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'scripts/exp21')
import checks, mv_format
root = Path('results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot')
load = lambda name: [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]
sources, outputs = load('accepted24_source_b.jsonl'), load('tagged24_b.jsonl')
assert len(sources) == len(outputs) == 12
for source, output in zip(sources, outputs):
    assert (source['id'], source['question']) == (output['id'], output['question'])
    assert output['status'] == 'tagged'
    parsed = mv_format.parse(output['response'])
    assert parsed['valid'] and len(parsed['blocks']) == 1 and parsed['blocks'][0]['numbered']
    assert output['response'].index('<think>') < parsed['blocks'][0]['start'] < parsed['blocks'][0]['end'] < output['response'].index('</think>')
    result = checks.check(output['response'], checks.candidate(source['response']), 'blind_public', original=source['response'])
    assert result['ok'], (source['id'], result)
    assert output['response'].split('</think>', 1)[1] == source['response'].split('</think>', 1)[1]
print('12/12 saved rows pass; IDs, questions, order, numbered grammar, text/numbers recovery, block location and final answer preserved.')
PY
```

Result: `12/12 saved rows pass; IDs, questions, order, numbered grammar, text/numbers recovery, block location and final answer preserved.`
