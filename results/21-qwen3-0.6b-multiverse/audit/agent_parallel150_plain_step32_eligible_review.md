# Plain step32: eligible-block review

Strict criterion: both paths independently establish different necessary facts; Conclusion correctly combines them; external final answer is correct.

| ID | Verdict | Evidence |
|---|---:|---|
| `gsm8k-train/132` | pass | Path 1 derives 18 green balls and Path 2 derives 8 yellow balls from separate givens. Both facts are necessary for the total; Conclusion correctly sums all four colors to 36; final is correct. |
| `gsm8k-train/369` | reject | Final seal time 13 is correct through Path 2. Path 1 wrongly calls 130 minus 13 equal to penguin time: 117 is seals plus penguins. Therefore it is not a valid independent necessary fact, and Conclusion falsely states penguins took 117 minutes. |
| `math-test/117` | reject | Algebraic grouping is invalid: the original expression factors as `(1001001-1001)(1010101+989899)=2*10^12`, giving `(2,12)`. Paths and Conclusion instead use an invalid factor and return `(9,3)`. |

Count: 1/3 pass.
