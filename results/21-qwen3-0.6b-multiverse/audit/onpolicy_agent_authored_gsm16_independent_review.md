# Independent blind review: agent-authored GSM16

## Scope

Reviewed the 16 rows in `data/onpolicy_agent_authored_gsm16.jsonl` against their literal questions in `data/onpolicy46_questions_only.jsonl` and their decomposition plans in `data/onpolicy46_decomp_pilot_plans.jsonl`. I did not open candidate, gold, or prior-rollout files.

Acceptance requires a semantically correct external answer; two distinct, true, independently executable Path computations; a correct Conclusion that combines them; a block wholly inside `<think>`; and no computed result before the block.

| ID | Verdict | Independent mathematical check |
|---|---|---|
| `gsm8k-train/5851` | **accept** | The 15-week period splits into 80% and 20% portions; their cricket totals are correctly computed and added. |
| `gsm8k-train/2281` | **accept** | Daughter plus three friends gives four girls; their serving requirement and the son's requirement are independent and sum correctly. |
| `gsm8k-train/6467` | **accept** | Miami and San Diego are each derived directly from the New York baseline; the three-city arithmetic mean is correct. |
| `gsm8k-train/1170` | **accept** | Red-light and construction delays are independently derived, then correctly placed on the travel timeline. |
| `gsm8k-train/2528` | **accept** | Rectangle and square areas are independent, correct, and correctly differenced. |
| `gsm8k-train/4597` | **accept** | Oil and vinegar volume-mass calculations are independent and their mass sum is correct. |
| `gsm8k-train/3721` | **accept** | Known gummy-bear and chocolate-chip category costs are independently correct; the remaining bill supports the stated bar price. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/6410` | **accept** | Each plan is priced independently for five lines and the price difference is correct. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/201` | **accept** | The first five-week and last two-week apple totals are independently correct; the seven-week average is correct. |
| `gsm8k-train/5392` | **accept** | Sapling and log yields are independent and add correctly. |
| `gsm8k-train/4780` | **accept** | Weekly earnings use the stated total hours and respective rates; the total is correct. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/6229` | **accept** | The two disjoint drink-group subtotals include every listed item and add correctly. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/3862` | **accept** | Adult and child daily revenues are independently correct and sum correctly. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/6020` | **accept** | Shirts-and-pants and jacket subtotals are independent; applying the one-half payment share is correct. Semantic external answer is correct, but its LaTeX dollar delimiter is unclosed. |
| `gsm8k-train/5215` | **accept** | Washing and brushing losses are separate, correct, and the required one-hair surplus is correctly applied. |
| `gsm8k-train/3576` | **accept** | Completed-lap elapsed time and Billy's winning total time are independent; their difference gives the final-lap duration. |

## Aggregate

- Semantic accepts: **16/16**
- Semantic rejects: **0/16**
- Complete Parallel blocks inside `<think>`: **16/16**
- Precomputed final answers before a block: **0/16**
- External-answer formatting notes: **6/16** have an unclosed final LaTeX dollar delimiter (`3721`, `6410`, `4780`, `6229`, `3862`, `6020`). These are semantically unambiguous, so I did not reject them under the stated semantic criterion; repair them before a stricter text-format gate.
