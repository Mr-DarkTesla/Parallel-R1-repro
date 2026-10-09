# Independent review: four plan-only Multiverse annotations

Reviewer: separate agent; 10 October 2026. Compared `tagged4.jsonl` with `traces_raw20.jsonl` and gold in `../../data/pool.jsonl`. No GPU, proxy, Kubernetes, or source-row edits.

## Findings

- Gold-final correctness: 4/4.
- M2 verbatim recovery: 4/4. Using the repository's intended M2 test (`checks.check`), removing only structural tags, Path numbers, Goal text, and Conclusion text recovers each source trace exactly after whitespace normalization. Source reasoning, numbers, formulas, question text, and final answer are unchanged.
- Grammar: 4/4 full, numbered Multiverse blocks wholly inside one closed `<think>` span. No structural tag occurs after `</think>`.
- Semantics: 4/4 have two genuine sibling computations. The paths do not refer to each other, and each pair supplies needed inputs or constraints.

## Gate result

Only `math-train/6266` passes the current complete automatic `scripts/exp21/checks.py` gate without exception.

- `math-train/1491`: `short_path`; numerator path is 60 characters, below 80.
- `math-train/5580`: `short_path`; paths are 62 and 59 characters, below 80.
- `math-train/7323`: `recheck`; Conclusion says "verify the remaining length condition." This is a legitimate required matrix constraint, so the heuristic flag is a false positive, but it still fails the literal current gate.

Do not admit `1491` or `5580` until their paths are made long enough using only existing source text, or until the documented gate changes. `7323` is semantically acceptable if the reviewer records a waiver for that known heuristic false positive.

Per-row evidence: `tagged4_review.jsonl`.
