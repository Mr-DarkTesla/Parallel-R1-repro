# Blind semantic review: final pilot128 rows 20–22

Scope: only 1-based rows 20–22 of `eval_archives/onpolicy46_pilot128/provisional_candidates.jsonl`. Acceptance requires two independent, substantive, mathematically true paths, a correct synthesis, no answer computed before the block, and a correct external answer.

| Row | ID / seed | Verdict | Precise reason |
|---:|---|---|---|
| 20 | `gsm8k-train/4780` / 1 | **reject** | The external answer `770` is correct. But the entire calculation, including `$420+350=770`, appears before `<Parallel>`, so this violates the no-precomputed-answer condition. The Conclusion also never actually performs the stated sum and repeats the component values. |
| 21 | `math-train/5881` / 0 | **reject** | The external answer `54.55` is correct, but the internal reasoning is not. Path 1 calls the second decimal digit `5`; in `54.545454…`, the hundredths digit is `4` and it rounds up because the thousandths digit is `5`. Path 2 then says the residual rounds down, which does not justify the final rounding to `54.55`. The two paths also substantially duplicate the same rounding subtask rather than independently supplying components. |
| 22 | `gsm8k-train/3862` / 0 | **reject** | The external answer `2200` and both within-block patient-count paths are correct; the Conclusion combines them correctly as `$32\\cdot50+24\\cdot25=2200`. However, before the block the response already performs a full, erroneous computation and states `$4800`. That is both a material mathematical defect and a violation of the no-precomputed-answer condition. |

Accepted: **0/3**.
