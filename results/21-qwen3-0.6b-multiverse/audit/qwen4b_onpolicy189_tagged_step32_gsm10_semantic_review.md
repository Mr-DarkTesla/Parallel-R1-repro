# Semantic review: qwen4b_onpolicy189 tagged step32 GSM10

Strict useful paths require two nontrivial, correct computations from problem
givens, independence between paths, a Conclusion that uses both, a complete
block inside `<think>`, and a correct external final answer. `acc_robust` and
`full_numbered_block` alone do not establish this.

| ID | Robust final answer check | Full block in `<think>` | Strict useful independent paths | Concise reason |
|---|:---:|:---:|:---:|---|
| `gsm8k-train/43` | Yes, `75` | No | No | Correct cost split, but first `<Path>` opening tag is missing and paths duplicate the $50 computation. |
| `gsm8k-train/82` | No | Yes | No | Sells all three wands although only two friends buy them; correct unit cost is $60, not $115/3. |
| `gsm8k-train/132` | Yes, `36` | Yes | Yes | Independently derives green and yellow counts; Conclusion combines both with given blue and red counts. |
| `gsm8k-train/228` | Yes, `20` | Yes | No | Path 2 depends on Path 1's derived 40-bag remainder, so it is not independently derived from givens. |
| `gsm8k-train/232` | Yes, `9` | Yes | Yes | Independently computes original dimes and post-discovery nickels; Conclusion adds their values. |
| `gsm8k-train/235` | Yes, `9` | Yes | No | Path 1 already solves the whole task, including Path 2's five-person count; paths duplicate rather than split work. |
| `gsm8k-train/260` | Yes, `10` | Yes | Yes | Independently computes pants and shirt costs; Conclusion sums them before change calculation. |
| `gsm8k-train/278` | Yes, `12` | Yes | No | Path 2 consumes Path 1's result, then falsely substitutes `x=16`; Conclusion's claimed 50-pass check is internally false. |
| `gsm8k-train/279` | Yes, `10` | Yes | No | Path 1 incorrectly assigns the son's three gifts $10 total and $10/3 each; Conclusion contradicts it and relies on Path 2. |
| `gsm8k-train/288` | Yes, `6` | Yes | Yes | Independently computes folding/resting and mixing/baking durations; Conclusion sums both. |

Result: **9/10** correct final answers, **9/10** complete blocks in `<think>`,
and **4/10** strict useful independent blocks. Automated structural and final
acceptance is a false positive for `gsm8k-train/228`, `gsm8k-train/235`,
`gsm8k-train/278`, and `gsm8k-train/279` under the strict criterion.
