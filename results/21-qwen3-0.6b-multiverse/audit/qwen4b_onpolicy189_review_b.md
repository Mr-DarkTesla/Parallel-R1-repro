# Qwen4B on-policy 189: independent-path audit B

Reviewed `qwen4b_onpolicy189_early100_review_b.jsonl`, 21 assigned rows.

Strict PASS requires: two distinct, nontrivial, mathematically correct paths
derived independently from givens; conclusion materially combines both; correct
final answer; and every Parallel tag is inside `<think>`.

| ID | Verdict | Reason |
|---|---|---|
| math-train/6673 | FAIL | Final `4` is correct, but `13/90 = 0.14444...`, not `0.\\overline{44}`. Path 1 incorrectly calls first digit `4`; claimed two-digit period is false. |
| gsm8k-train/7056 | FAIL | Path 2 depends on Path 1's derived biology count `60`; paths are sequential, not independent. |
| gsm8k-train/5074 | PASS | Independent nose and ear revenue computations are correct; conclusion combines both to correct `390`. |
| gsm8k-train/5556 | FAIL | Path 2 only repeats given `$10` remainder, so it is not a nontrivial independent path. |
| gsm8k-train/3810 | FAIL | Path 2 recomputes Heidi's count and then derives Grant, so it depends on duplicated Path 1 work. |
| math-train/2012 | FAIL | Final `160` is correct, but Path 2's coefficient formula wrongly changes `6^(6-k)` to `6^(6-2k)`; two valid paths absent. |
| gsm8k-train/6055 | FAIL | Path 2 merely repeats Beatrix's given `704`; no second nontrivial path. |
| gsm8k-train/6565 | FAIL | Paths only state fixed `$20` and symbolic `$7m`; neither independently solves a substantive subproblem. |
| gsm8k-train/1856 | PASS | Independent slice totals `30` and `15` are correct; conclusion combines them to `45`. |
| math-train/5638 | FAIL | Path 2 starts from Path 1's `3B=18`; sequential derivation, not independent paths. |
| gsm8k-train/4751 | FAIL | Path 2 repeats Path 1's computation of Katelyn's `96`, so it is dependent. |
| gsm8k-train/7348 | FAIL | Path 2 only repeats given yesterday distance `12`; no second nontrivial path. |
| math-train/7348 | FAIL | `tan x + cot x = 2/sin(2x)`, whose least period is `pi/2`; final `pi` is incorrect. |
| gsm8k-train/1952 | PASS | Daily-sales series and cents-to-dollars conversion are independent, correct paths; conclusion uses both for `$12`. |
| gsm8k-train/3674 | PASS | Each path independently solves one variable from the two given equations; conclusion combines correct `58` and `62`. |
| gsm8k-train/3219 | FAIL | Path 2 only repeats given chair count `4`; it is not a nontrivial independent calculation. |
| math-train/3435 | FAIL | Paths find incompatible separate infima and conclusion only says sum is positive; neither establishes minimum `5`, despite correct later derivative result. |
| gsm8k-train/6080 | PASS | Two independent paired-consumption calculations (`10`, `5`) are correct; conclusion combines them and final `9` is correct. |
| math-train/4472 | FAIL | Path 1 derives both parameters; Path 2 merely repeats `k=3` and has inconsistent focus parameterization. No two independent paths. |
| math-train/3849 | PASS | Products by `x^2` and by `18` are independently correct; conclusion subtracts them to correct `x^6-5832`. |
| gsm8k-train/5172 | FAIL | Path 2 gives only symbolic `8/total` and relies on Path 1's total; it is not an independent nontrivial path. |

Summary: 6 PASS, 15 FAIL. Correct final answers alone do not satisfy this
semantic-path criterion. In particular, rows 6673, 2012, 3435, and 7348 (math)
are scorer false positives if a scorer accepted them from final-answer accuracy.
