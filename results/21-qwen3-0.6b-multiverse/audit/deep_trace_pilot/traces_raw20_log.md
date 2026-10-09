# Blind mathematical solution pilot, 20 problems

Date: 2026-10-10.

Problem source: `questions_blind20.jsonl` only. No pool, gold answers, evaluation files, previous solutions, model calls, GPU operations, Kubernetes, or proxy operations were used. Applicable AGENTS.md files and the requested caveman skill were read as instructions.

Output: `traces_raw20.jsonl`. Only this output and this log were written. Each response contains a public mathematical explanation and explicit verification, enclosed in the requested tags for dataset compatibility. These are solution explanations, not a record of private internal deliberation.

Work: solve each question independently from its statement, write exact arithmetic or algebra, and check the result by substitution, a second identity, or conservation/counting. The inverse-cosine solution includes domain and sign restrictions. The functional equation excludes the second affine candidate by direct contradiction and verifies the surviving function for all real x,y. The matrix solution verifies all row lengths and all row dot products.

Validation command, run locally with Python 3:

```python
import json
from pathlib import Path
p = Path('/Users/v.charkin/Documents/dev/projects/parallel-r1-exp21/results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot')
rows = [json.loads(line) for line in (p/'traces_raw20.jsonl').read_text().splitlines()]
questions = [json.loads(line) for line in (p/'questions_blind20.jsonl').read_text().splitlines()]
assert len(rows) == 20
assert len({r['id'] for r in rows}) == 20
assert [r['id'] for r in rows] == [q['id'] for q in questions]
assert [r['question'] for r in rows] == [q['question'] for q in questions]
for r in rows:
    assert set(r) == {'id','question','response','parallelizable','status','notes'}
    assert type(r['parallelizable']) is bool
    assert r['status'] == 'solved'
    assert r['response'].startswith('<think>\n')
    assert r['response'].count('<think>') == r['response'].count('</think>') == 1
    assert '</think>\nFinal Answer: ' in r['response']
```

Results: validation passed. 20 valid rows, 20 unique IDs in original order, original question wording preserved, all 20 marked solved, all 20 have exactly one closed think block. Four rows are marked parallelizable: independent numerator/denominator evaluation, independent subgroup totals, independent disk areas, and fixed-row compatibility versus third-row constraints. The remaining rows have dependent derivations.

Explanation character counts: mean 941.8, minimum 756, maximum 1078. Some simple problems remain below the approximate 1000-character target; all explanations include actual calculations and checks, and were not padded to a target length.

Interpretive limits: the probability question uses the standard independent-birth assumption; equal individual boy/girl probabilities alone do not establish it. The rotation question uses the usual nonnegative angle measure, so the representative is 300 degrees. If arbitrary signed x were permitted with only x<360, infinitely many equivalent negative values would also occur. Both conventions are noted in the corresponding rows. No unresolved mathematical candidate remains under the standard interpretations; correctness has not been compared to external gold.
