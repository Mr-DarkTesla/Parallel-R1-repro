# Wave71b, batch 1 author log

## Method

- Read 18 input conditions and solved each before reading `data/pool.jsonl`.
- Wrote and structurally validated draft before gold comparison.
- Required every `ready` answer to have two sibling-independent, useful Paths inside `<think>` and a Conclusion that uses both results.

## Gold comparison and corrections

- `math-train/6871`: draft used `R=(6,sqrt(5))`, treating `interp(C,A,6/9)` as one third of the C-to-A segment. Correctly it is two thirds, so `R=(4,2sqrt(5))`, the second slope is `sqrt(5)`, and the answer is `3sqrt(5) + 2sqrt(10)`. Corrected in final after gold comparison; draft remains unchanged as required.
- All other 15 drafted answers agree with pool gold, allowing equivalent notation such as `1/48` for `\\frac{1}{48}`.
- `gsm8k-train/1412` and `math-train/2882` were skipped before gold comparison because each has one coupled dependency chain; two Paths would repeat the same derivation. Both pool answers are consistent with the independently derived result, but were not forced into the parallel format.

## Result

| status | count | meaning |
| --- | ---: | --- |
| ready | 16 | Correct answer, two useful independent Paths, and gold agreement after the stated correction. |
| skip | 2 | Parallel split would be artificial or duplicative. |
| gold_conflict | 0 | No condition-versus-pool disagreement found. |

Validation: draft and final each contain all 18 unique input IDs with fields `id`, `status`, `output`, and `skip_reason`. Every ready row has one `<think>` block, two Outlines, two Paths, one Conclusion, and one external `Final Answer:`. CPU-only; no GPU, Kubernetes, proxy, or commit.

## Post-math_verify format correction

`math-train/2228` had correct probability 56%, but its external final used literal `%`, which the local `answer_checker` rejected against gold `0.56 = 56\\%`. Changed only final output to `Final Answer: 56\\%`; reasoning, numbers, status, and draft are unchanged.
