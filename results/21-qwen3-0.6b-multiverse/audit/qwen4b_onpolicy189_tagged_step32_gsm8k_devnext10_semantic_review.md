# Semantic review: qwen4b_onpolicy189 tagged step32 GSM8K devnext10

Strict useful paths require two distinct, nontrivial, correct computations from
problem givens, independence between paths, a Conclusion that uses both, a
complete block inside `<think>`, and a correct external final answer.
`acc_robust` and `full_numbered_block` alone do not establish this.

| ID | Robust final answer check | Full block in `<think>` | Strict useful independent paths | Concise reason |
|---|:---:|:---:|:---:|---|
| `gsm8k-train/300` | Yes, `60` | Yes | No | Path 2 consumes Path 1's derived 120 students in couples, so paths are sequential. |
| `gsm8k-train/317` | Yes, `28` | Yes | No | Path 1 computes attendance; Path 2 only repeats given 4 candies per student, so no second nontrivial calculation. |
| `gsm8k-train/345` | Yes, `3` | Yes | No | Path 2 independently obtains one quarter of original cakes, duplicating the result assembled from Path 1 rather than supplying a distinct component used by Conclusion. |
| `gsm8k-train/369` | No; correct answer is `13` | Yes | No | Total-time equation is wrong: it double counts the penguin term and yields `117/16`; correct equation is `s + 8s + 13 = 130`. |
| `gsm8k-train/374` | Yes, `9` | Yes | Yes | Independently computes six soda bottles and six pizza slices; Conclusion combines both costs. |
| `gsm8k-train/379` | Yes, `56000` | Yes | No | Parents' payment requires the Path 1 down-payment balance, so Path 2 is not independent. |
| `gsm8k-train/462` | Yes, `150` | Yes | No | Fat path repeats the full muscle-gain calculation before dividing it by four; two paths are not distinct independent components. |
| `gsm8k-train/580` | Yes, `80` | Yes | No | Both paths repeat the same 40,000-calorie and 500-calorie-per-day calculation, rather than splitting work. |
| `gsm8k-train/653` | Yes, `17` | Yes | Yes | Independently computes Francis's and Kiera's orders; Conclusion adds both totals. |
| `gsm8k-train/684` | No; correct answer is `2400` | Yes | No | Treats four dance days as seven and calls four sessions four weeks. Weekly dance time is `4 × 2 × 0.5 = 4` hours, hence `4 × 600 = 2400`. |

Result: **8/10** correct final answers, **10/10** complete blocks in `<think>`,
and **2/10** strict useful independent blocks. Automated structural and final
acceptance is a false positive for `gsm8k-train/300`, `gsm8k-train/317`,
`gsm8k-train/345`, `gsm8k-train/379`, `gsm8k-train/462`, and
`gsm8k-train/580` under the strict criterion.
