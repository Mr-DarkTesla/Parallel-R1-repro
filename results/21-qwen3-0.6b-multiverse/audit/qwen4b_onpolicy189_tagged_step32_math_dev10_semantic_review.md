# Semantic review: qwen4b_onpolicy189 tagged step32 MATH_DEV10

Strict useful paths require two nontrivial, mathematically correct calculations
derived independently from problem givens, no sibling dependence or answer leak,
a Conclusion that materially uses both results, a complete block inside `<think>`,
and a correct external final answer. `acc_robust` and `full_numbered_block` alone
do not establish this.

| ID | Robust final answer check | Full block in `<think>` | Strict useful independent paths | Concise reason |
|---|:---:|:---:|:---:|---|
| `math-test/9` | Yes, `-1/8` | Yes | **PASS** | The two sign cases independently give `3/2` and `-1/8`; Conclusion uses both to select the smaller solution. |
| `math-test/29` | Yes, `16` | Yes | **FAIL** | Path 2 repeats Path 1's sum relation `b=-4s` and already derives both possible values of `b`; Conclusion does not materially combine two independent results. |
| `math-test/36` | Yes, `(-sqrt(3),sqrt(3))` | Yes | **PASS** | Paths independently solve the lower and upper inequalities; Conclusion intersects their solution sets to obtain the correct interval. |
| `math-test/38` | Yes, `49` | Yes | **FAIL** | Both paths perform the same completion of squares and obtain the same circle equation; the radius path duplicates the center path rather than supplying independent work. |
| `math-test/45` | No; correct value is `6+9i` | Yes | **FAIL** | Path 2 only restates the term `-3i`, then the solution subtracts it a second time: `(6+12i)-(-3i)`. The original expression is `6+12i-3i`. |
| `math-test/51` | Yes, `0` | Yes | **FAIL** | The complete answer `f^{-1}(x)=f(x)` and difference `0` are stated before the block. Path 1 merely restates the given involution condition, while Path 2 solves the task alone. |
| `math-test/53` | Yes, `7/2` | Yes | **FAIL** | Paths only make the elementary conversions `8=2^3` and `sqrt(2)=2^(1/2)`; Conclusion lists both exponents but does not add them. The actual combination occurs after the block. |
| `math-test/65` | Yes, `6` | Yes | **FAIL** | Paths are an artificial split into the single elementary calculations `8^2=64` and `4*7=28`; they do not meet the two-nontrivial-path requirement, although Conclusion combines them correctly. |
| `math-test/71` | Yes, `20` | Yes | **FAIL** | Path 1 solves `x=4`; Path 2 only states that the greater number is `5x` and explicitly still needs `x`. Conclusion therefore depends on Path 1 rather than combining two independent calculations. |
| `math-test/87` | Yes, `-5` | Yes | **FAIL** | Both paths repeat the same substitution and simplification at `x=-4`; there are not two distinct independent calculations. |

Result: **9/10** correct external final answers, **10/10** complete blocks inside
`<think>`, and **2/10** strict useful independent blocks. Automated acceptance
from `acc_robust=true` plus `full_numbered_block=true` is a strict-semantic false
positive for `math-test/29`, `math-test/38`, `math-test/51`, `math-test/53`,
`math-test/65`, `math-test/71`, and `math-test/87`. `math-test/45` is correctly
rejected by the answer scorer.
