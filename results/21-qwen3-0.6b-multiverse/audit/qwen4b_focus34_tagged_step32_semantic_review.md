# Semantic audit: qwen4b_focus34_tagged_step32

## Scope and criteria

Read-only audit of all 40 generated outputs in
`eval_archives/qwen4b_focus34_tagged_step32/`:

- four generation files, 10 rows each;
- corresponding `*-block-rows.jsonl` and `*-rows.jsonl` metadata;
- external final-answer correctness, independently checked from each problem;
- exactly one `Parallel` block inside `think`;
- exactly two nontrivial, independent, mathematically correct Paths used by the
  Conclusion.

`Useful` requires every criterion above. A correct final answer alone does not
qualify when paths duplicate work, are sequential, are mathematically wrong, or
are not used by the Conclusion.

## Aggregate

- External final answer correct: **30 / 40**.
- Strict useful parallel reasoning: **8 / 40**.
- Parser false negatives corrected by manual review: **0**. All 10 rows marked
  `acc_robust: false` have externally wrong final answers.
- Every response contains one outer `Parallel` block inside `think` and no tags
  outside `think`. `math-test/98` has a malformed nested `Conclusion` tag;
  `math-test/117` has four `Path` tags and repeats path number `2`.

## Per-row verdicts

| Generation | ID | Final correct | Semantic verdict | Useful |
|---|---:|:---:|---|:---:|
| `gsm8k_dev10` | `gsm8k-train/43` | Yes | Paths duplicate each other; outline 1 is not solved. | No |
| `gsm8k_dev10` | `gsm8k-train/82` | No | Treats all three wands as resold although only two friends buy them. | No |
| `gsm8k_dev10` | `gsm8k-train/132` | Yes | Independent blue/red and green/yellow totals; conclusion uses both. | Yes |
| `gsm8k_dev10` | `gsm8k-train/228` | Yes | Path 2 repeats path 1's first-two-weeks calculation. | No |
| `gsm8k_dev10` | `gsm8k-train/232` | Yes | Independent original-value and found-nickels totals; conclusion uses both. | Yes |
| `gsm8k_dev10` | `gsm8k-train/235` | Yes | Path 2 repeats path 1 and solves the whole task. | No |
| `gsm8k_dev10` | `gsm8k-train/260` | Yes | Independent pants and shirts totals; conclusion uses both. | Yes |
| `gsm8k_dev10` | `gsm8k-train/278` | Yes | Path 1 states the complete system; path 2 is only a relation. | No |
| `gsm8k_dev10` | `gsm8k-train/279` | Yes | Path 2 defers its calculation until after path 1. | No |
| `gsm8k_dev10` | `gsm8k-train/288` | Yes | Independent folding/resting and mixing/baking durations; conclusion uses both. | Yes |
| `gsm8k_devnext10` | `gsm8k-train/300` | Yes | Couples computation depends on the students-as-couples result. | No |
| `gsm8k_devnext10` | `gsm8k-train/317` | Yes | Path 2 incorrectly says 9 students and conclusion ignores it. | No |
| `gsm8k_devnext10` | `gsm8k-train/345` | Yes | Sequential calculation is repeated across paths. | No |
| `gsm8k_devnext10` | `gsm8k-train/369` | Yes | Path 2 only repeats a stated relation. | No |
| `gsm8k_devnext10` | `gsm8k-train/374` | Yes | Independent soda and pizza totals; conclusion uses both. | Yes |
| `gsm8k_devnext10` | `gsm8k-train/379` | Yes | Parents' payment depends on the down-payment result. | No |
| `gsm8k_devnext10` | `gsm8k-train/462` | Yes | Fat-gain path recomputes muscle gain. | No |
| `gsm8k_devnext10` | `gsm8k-train/580` | Yes | Path 2 recomputes the daily calorie deficit. | No |
| `gsm8k_devnext10` | `gsm8k-train/653` | Yes | Independent Francis and Kiera totals; conclusion uses both. | Yes |
| `gsm8k_devnext10` | `gsm8k-train/684` | No | Omits the second daily dance session; correct total is 2400 calories. | No |
| `math_dev10` | `math-test/9` | No | Omits a mixed-sign absolute-value case; minimum is `-1/8`. | No |
| `math_dev10` | `math-test/29` | Yes | Both paths duplicate the full root derivation. | No |
| `math_dev10` | `math-test/36` | Yes | Independent upper and lower inequality constraints; conclusion intersects them. | Yes |
| `math_dev10` | `math-test/38` | Yes | Path 2 incorrectly computes 74; conclusion falsely says paths agree. | No |
| `math_dev10` | `math-test/45` | No | Misreads `6(1+2i)-3i`; correct value is `6+9i`. | No |
| `math_dev10` | `math-test/51` | Yes | Both paths repeat the same self-inverse argument. | No |
| `math_dev10` | `math-test/53` | Yes | Independent log components; conclusion correctly adds them. | Yes |
| `math_dev10` | `math-test/65` | No | Path 2 makes an invalid substitution; correct value is 6. | No |
| `math_dev10` | `math-test/71` | Yes | Path 2 depends on path 1's result. | No |
| `math_dev10` | `math-test/87` | Yes | Both paths repeat the same substitution. | No |
| `math_devnext10` | `math-test/88` | Yes | Solving path depends on the `d(e)` path. | No |
| `math_devnext10` | `math-test/93` | No | Average is determined and equals 5. | No |
| `math_devnext10` | `math-test/98` | Yes | Nested/unclosed `Conclusion` tag makes the block malformed. | No |
| `math_devnext10` | `math-test/103` | Yes | Path 2 uses the wrong residual quadratic and is not used correctly. | No |
| `math_devnext10` | `math-test/108` | Yes | Both paths duplicate the ratio solution. | No |
| `math_devnext10` | `math-test/110` | Yes | Path 1 completes rationalization; path 2 repeats only its denominator step. | No |
| `math_devnext10` | `math-test/117` | No | Four paths with repeated number 2; arithmetic is wrong. Correct pair is `(2,12)`. | No |
| `math_devnext10` | `math-test/129` | No | Derives `x >= 2009/4`, then unjustifiably rounds to 503. | No |
| `math_devnext10` | `math-test/130` | No | Assigns the same root to both factors; correct product is -22. | No |
| `math_devnext10` | `math-test/137` | No | Path 1 does not move the equation's right side; correct `m+n` is 1. | No |

## Strictly useful IDs

`gsm8k-train/132`, `gsm8k-train/232`, `gsm8k-train/260`,
`gsm8k-train/288`, `gsm8k-train/374`, `gsm8k-train/653`,
`math-test/36`, and `math-test/53`.
