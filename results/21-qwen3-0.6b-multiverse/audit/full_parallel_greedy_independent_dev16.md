# Independent manual audit: full masked dev16

Scope: `full_parallel_greedy`, fixed seed-21 indices `[84, 93, 110, 144, 214, 243, 245, 262]` from each source. Reviewed only stated parquet inputs and their `raw.jsonl`, `score_rows.jsonl`, and `block_rows.jsonl`; no other manual verdicts were read.

Strict pass requires all of: correct final answer, a complete consistently numbered `Parallel` block inside `<think>`, at least two correct independent useful paths matching different outlined results or cases, and no contradictory error in Conclusion or chain. Recomputing a stated result inside a path counts as independent when it uses prompt data rather than another path. A pre-block derivation followed by paths that only repeat it does not count.

## GSM8K dev

| index | problem ID | final | final correct | full numbered block | independent paths | chain consistent | strict pass | short reason |
|---:|---|---|---|---|---:|---|---|---|
| 84 | `gsm8k-train/2423` | 208 | yes | yes | 2 | yes | yes | independent area and coverage |
| 93 | `gsm8k-train/2706` | 24 | yes | yes | 2 | yes | yes | independent ride costs |
| 110 | `gsm8k-train/3166` | 26.5 | no | yes | 1 | no | no | Tom's prior age wrong |
| 144 | `gsm8k-train/4127` | 16 | yes | yes | 2 | yes | yes | independent walking and biking time |
| 214 | `gsm8k-train/5659` | 3 | yes | yes | 2 | yes | yes | independent depth and rate |
| 243 | `gsm8k-train/6293` | 3360 | no | no | 0 | no | no | $400 short omitted; duplicated Path 2 |
| 245 | `gsm8k-train/6310` | 6 | yes | yes | 2 | yes | yes | independent price calculations |
| 262 | `gsm8k-train/6648` | 480/7 | no | yes | 0 | no | no | five ordinary rooms, not four |

Aggregate: 8 rows; final-answer correct 5/8; full numbered block 7/8; strict pass 5/8.

## ARC dev

| index | problem ID | final | final correct | full numbered block | independent paths | chain consistent | strict pass | short reason |
|---:|---|---|---|---|---:|---|---|---|
| 84 | `arc-val/Mercury_7238963` | A | yes | yes | 2 | yes | yes | independent maternal allele cases |
| 93 | `arc-val/Mercury_7193043` | D | no | no | 1 | no | no | weathering is B; repeated Path 2 |
| 110 | `arc-val/MEAP_2005_5_1` | C | yes | no | 2 | yes | no | unclosed `<think>` |
| 144 | `arc-val/Mercury_409529` | B | yes | yes | 2 | yes | yes | bait and hook checks |
| 214 | `arc-val/Mercury_414131` | C | yes | no | 1 | no | no | unclosed `<think>`; carbon counterexample |
| 243 | `arc-val/Mercury_7267593` | A | yes | yes | 2 | yes | yes | independent disaster cases |
| 245 | `arc-val/MCAS_2011_5_17673` | C | no | yes | 1 | no | no | like-pole repulsion supports A |
| 262 | `arc-val/Mercury_SC_415397` | C | yes | yes | 2 | yes | yes | independent exclusions of A and B |

Aggregate: 8 rows; final-answer correct 6/8; full numbered block 5/8; strict pass 4/8.

## Total

16 rows, 11/16 correct final answers, 12/16 full numbered blocks, 9/16 strict passes.

All selected indices and IDs were checked against source parquet order and matching output rows. All 16 sampled responses have `truncated: false` in both score and block records.
