# Semantic review: qwen4b_onpolicy189 tagged step32 MATH devnext10

Strict useful paths require two nontrivial, mathematically correct calculations
derived independently from problem givens, no sibling dependence or answer
leak, a Conclusion that materially uses both results, a complete block inside
`<think>`, and a correct external final answer. `acc_robust` and
`full_numbered_block` alone do not establish this.

| ID | Robust final answer check | Full block in `<think>` | Strict useful independent paths | Concise reason |
|---|:---:|:---:|:---:|---|
| `math-test/88` | Yes, `2` | Yes | **FAIL** | Both paths derive `d=2e+9` from the second condition. Path 2 ignores its outline, and Conclusion imports the unused first condition instead of combining two independent path results. |
| `math-test/93` | Yes, `5` | Yes | **FAIL** | Each path only doubles one stated average. Conclusion merely lists the two equations; their material combination to obtain `a+b+c=15` happens after the block. |
| `math-test/98` | No; correct point is `(9,11)` | Yes | **FAIL** | The paths find incompatible slopes `9/7` and `1`, but Conclusion falsely calls them the same line. The other three points have slope `5/3`, so `(9,11)` is the outlier. |
| `math-test/103` | No; correct factorization over the integers is `2x(15x^2-4x+10)` | Yes | **FAIL** | Path 2 invents factors: `(6x-10)(5x+2)=30x^2-38x-20`, not `30x^2-8x+20`. The final expression therefore does not expand to the given polynomial. |
| `math-test/108` | Yes, `18` | Yes | **FAIL** | Path 2 only repeats the given equation `y=4x-36`; it supplies no nontrivial calculation. Thus the block lacks two nontrivial independent paths despite a correct combination. |
| `math-test/110` | Yes, `sqrt(7)/14` | Yes | **FAIL** | This is an artificial numerator/denominator split of one multiplication. Path 1 is only `1*sqrt(7)=sqrt(7)`, so there are not two nontrivial calculations. |
| `math-test/117` | No; correct pair is `(2,12)` | Yes | **FAIL** | The original expression factors as `(1001001-1001)(1010101+989899)=10^6*2,000,000=2*10^12`. The paths analyze unrelated quantities, Path 1 also mis-expands its product, and Conclusion does not derive the claimed factorization. |
| `math-test/129` | No; correct minimum is `2009/4=502.25` | Yes | **FAIL** | The square difference is `4*2009*x=8036x`, not `4018x`. Both paths then duplicate the same simplification of the already incorrect bound. |
| `math-test/130` | Yes, `-22` | Yes | **PASS** | Path 1 independently supplies `ab=5/2`, Path 2 supplies `12(a+b)=60`, and Conclusion combines both in the correct expansion. |
| `math-test/137` | Yes, `1` | Yes | **FAIL** | Path 2 gives the false root `-2-sqrt(3)` and appears to preserve the leaked target sum `1`. Conclusion silently replaces it with the correct second root while still citing the wrong `m,n`. |

Result: **6/10** correct external final answers, **10/10** complete blocks inside
`<think>`, and **1/10** strict useful independent blocks. Joint automated
acceptance from `acc_robust=true` plus `full_numbered_block=true` is a strict
semantic false positive for `math-test/88`, `math-test/93`, `math-test/108`,
`math-test/110`, and `math-test/137`. The answer scorer correctly rejects
`math-test/98`, `math-test/103`, `math-test/117`, and `math-test/129`.
