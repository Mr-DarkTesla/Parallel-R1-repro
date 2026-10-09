# Independent review: Qwen tagged C

Reviewed the six records with `status: tagged` in `tagged_c.jsonl` against their source texts in `batch_c.jsonl` and gold answers in `data/pool.jsonl`.

| Check | Result |
|---|---:|
| Tagged records reviewed | 6 |
| Correct final answers | 6 / 6 |
| Correct material reasoning | 6 / 6 |
| Useful independent two-Path decompositions | 6 / 6 |
| Original Qwen text preserved | 6 / 6 |
| Blocks inside original `<think>` | 6 / 6 |

`scripts/exp21/checks.py` passes all six against their original response and pool gold: grammar, numbering, answer placement, answer correctness, cross-reference, path balance, and verbatim preservation are clean.

`math-train/4511` has `status: rejected` in the input and is outside this six-record review.
