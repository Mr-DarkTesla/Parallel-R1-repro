# Agent-authored remaining MATH proposals

## Scope

The source was limited to `data/onpolicy46_decomp_math_proposals.jsonl` and the matching literal questions in `data/onpolicy46_questions_only.jsonl`. I did not read candidate, gold, or prior-Qwen-rollout files.

Excluded before authoring:

- the 16 MATH pilot IDs in `data/onpolicy46_decomp_pilot_plans.jsonl`, because they were assigned to the earlier MATH16 file;
- `math-train/3110`, as explicitly requested.

## Result

- Accepted proposal IDs after exclusions: 18
- Authored rows: 18
- Skipped for uncertainty: none

Each authored output has setup-only text before `<Parallel>`, then two numbered, independent substantive paths, a conclusion that combines them, and a final answer outside `</think>`.

## Manual checks

I checked all arithmetic and algebra while authoring. Cases with additional verification included:

- `math-train/3833`: adjacent binomial-term ratios independently imply the same exponent.
- `math-train/5473`: prime-power minima were used to count common divisors.
- `math-train/827`: the $y$-containing expansion terms were partitioned to avoid counting $2y\cdot4y$ twice.
- `math-train/530`: subtracting the two power relations gives the two integer powers before identifying $(x,y)$.
- `math-train/7241`: forward and backward shoelace sums were computed separately.
- `math-train/4713`: binary addition was checked through the two shifted partial products.
