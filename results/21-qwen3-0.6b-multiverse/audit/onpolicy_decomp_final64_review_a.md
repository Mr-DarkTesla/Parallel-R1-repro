# Blind semantic review: planned-prompt pilot64 rows 3–5

Scope: only 1-based rows 3–5 of `eval_archives/onpolicy_decomp_pilot64/provisional_candidates.jsonl`. Acceptance requires two independent substantive and mathematically true paths, a correct combination in the conclusion, no precomputed answer before the block, and a correct external answer.

| Row | ID / seed | Verdict | Precise reason |
|---:|---|---|---|
| 3 | `math-train/1024` / 0 | **accept** | The two Paths independently sum disjoint five-term groups. Both partial sums are correct, the Conclusion adds them to the correct external answer `11`, and the pre-block text is setup only. |
| 4 | `math-train/1024` / 1 | **reject** | The external answer `11` and the intended split are correct, with no precomputed answer. However, Path 2 falsely equates the second fractional sum to `$5\\times\\frac{6+7+8+9+10}{5}=40$`; the actual fractional sum is `$\\frac{40}{5}=8$`. It later states the correct result, but the false intermediate makes the Path mathematically defective under the strict criterion. |
| 5 | `gsm8k-train/5392` / 0 | **accept** | Sapling and log yields are two independent true computations. The Conclusion correctly adds them to `27`; no answer is computed before the block and the external answer is correct. |

Accepted: **2/3**.
