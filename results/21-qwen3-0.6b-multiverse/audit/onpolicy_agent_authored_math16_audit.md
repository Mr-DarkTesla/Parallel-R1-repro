# Agent-authored MATH16 audit

## Scope

Authored from scratch for the 16 MATH IDs in `data/onpolicy46_decomp_pilot_plans.jsonl`. I read only that plan file and the corresponding literal questions in `data/onpolicy46_questions_only.jsonl`; no candidate, prior-rollout, generated-answer, or gold-containing file was read.

## Result

- Requested MATH IDs: 16
- Authored rows: 16
- Skipped IDs: none

Each row has a complete `<think>` block containing one `<Parallel>` block with two numbered outlines, two numbered paths, and a conclusion. The pre-block text is setup only. Each path carries a different necessary calculation or disjoint case, and the conclusion combines them before the external final answer.

## Manual solution checks

I checked the arithmetic and algebra for every authored row while writing. Higher-risk cases received explicit checks:

- `math-train/3947`: all sign cases of the nested absolute value were retained only when their case condition held.
- `math-train/4730`: the two evaluated operands differ by 15; divisibility establishes the stated GCD.
- `math-train/5531`: the nonrepeating prefix and shifted repeating tail were represented over denominator 99900.
- `math-train/505`: the two five-term geometric blocks were added with a common denominator.
- `math-train/2368`: heart-ten and non-ten-heart first-card cases are disjoint and exhaust the event.
