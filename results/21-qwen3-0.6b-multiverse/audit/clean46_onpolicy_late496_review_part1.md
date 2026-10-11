# clean46 on-policy late496: blind semantic review, part 1

## Scope and method

Read only `clean46_onpolicy_late496_blind_part1.jsonl`. Pool, gold, and earlier verdicts were not opened. For each of its 20 rows, checked the condition and external answer, factual and arithmetic validity of every Path, sibling independence, usefulness of two distinct intermediate results, and whether Conclusion combines them into the requested result. A correct external answer does not rescue a decorative, duplicated, or logically invalid parallel block.

## Per-row blind verdicts

| row | ID | verdict | reason |
| ---: | --- | --- | --- |
| 1 | `math-train/2306` | REJECT | External removal of 5 is right, but Path 1 omits pairs `(-1,11)` and `(0,10)` and claims 4 instead of 6; denominator after one removal is `choose(12,2)=66`, not 55. Path 2 contradicts it, and Conclusion retains wrong 6/55 claim. |
| 2 | `gsm8k-train/3106` | PASS | Remaining Friday stock and Monday shipment are distinct necessary quantities; Conclusion correctly combines 500 and 2000 to 2500. |
| 3 | `gsm8k-train/2520` | REJECT | Three Paths are allowed, but these repeatedly recompute Grenada's 2000 instead of contributing independent sibling results, and Conclusion leaves total calculation after Parallel. |
| 4 | `math-train/7487` | REJECT | Final cosine is right, but Path 2 uses an invalid law-of-cosines equation and first derives negative `(1-phi)/2`, then changes sign without a valid derivation. Path 1 supplies only context, not an independent needed result. |
| 5 | `math-train/6673` | REJECT | Final digit is right, but Path 2's `130/90` argument does not establish first decimal digit of `13/90`; it changes value to `13/9`. Thus one Path is mathematically invalid. |
| 6 | `gsm8k-train/3248` | PASS | Bombed count and no-show count are distinct necessary quantities; Conclusion correctly removes them and the later 20 failures to get 70. |
| 7 | `gsm8k-train/4020` | REJECT | Paths correctly obtain reading and math counts, but Conclusion stops at science count. Requested history count is computed later outside Conclusion, so Conclusion does not combine branches into result. |
| 8 | `gsm8k-train/6055` | REJECT | Path 2 repeats Path 1's complete Cristobal calculation before subtracting. It is not an independent sibling result. |
| 9 | `gsm8k-train/6811` | REJECT | Path 2 merely restates given red-marble count; it is decorative rather than a computed independent component. |
| 10 | `gsm8k-train/1390` | PASS | Morning and afternoon coffee spending are distinct required components; Conclusion adds $60 and $50 to $110. |
| 11 | `gsm8k-train/2520` | REJECT | Two Paths cover guns and tractors only; uniform calculation and total are deferred to Conclusion/outside Parallel. The block omits a branch for a major required component. |
| 12 | `math-train/7487` | REJECT | Path 2 contradicts Path 1's valid factorization, gives an invalid factorization and roots involving `sqrt(2)`, then states correct answer without derivation. It is mathematically false. |
| 13 | `math-train/4767` | PASS | Four-digit and five-digit palindrome cases are exhaustive distinct candidates; Conclusion compares 97 and 4323 and supports smallest positive x = 97. |
| 14 | `math-train/4767` | REJECT | Paths are duplicate checks of 5775, with Path 1 falsely calling 5775 even. Conclusion declares two identical candidates rather than combining independent cases. |
| 15 | `gsm8k-train/6790` | REJECT | Both Paths derive identical `q=6c+17` by equivalent substitution; no distinct intermediate results are combined, and actual total equation appears only after Parallel. |
| 16 | `gsm8k-train/1390` | REJECT | Path 2 explicitly uses “From part 1” daily cost, so it reads sibling result rather than being independent. |
| 17 | `math-train/3258` | REJECT | Definition and unit-circle Paths are equivalent rechecks of trivial same result; Conclusion only confirms agreement. No two distinct needed subresults exist. |
| 18 | `gsm8k-train/5556` | REJECT | Both Paths restate purchase prices given verbatim. Original-money calculation is left outside Conclusion, making branches decorative. |
| 19 | `gsm8k-train/5653` | REJECT | Path 2 repeats Path 1's sister-weight computation before summing, so it is not sibling-independent. |
| 20 | `gsm8k-train/1726` | REJECT | Path 2 independently recomputes the 100 males needed in Path 1, then Conclusion only says “the rest”; requested 90 is calculated later outside Conclusion. The combined conclusion is incomplete. |

## Blind totals

| category | count |
| --- | ---: |
| rows reviewed | 20 |
| PASS | 4 |
| REJECT: arithmetic or logic error in Path | 4 |
| REJECT: duplicated or decorative sibling Path | 8 |
| REJECT: incomplete Conclusion or missing needed branch | 4 |

Pass IDs: `gsm8k-train/3106`, `gsm8k-train/3248`, `gsm8k-train/1390` (row 10), `math-train/4767` (row 13). Rejected rows may still have correct external answers; this blind review evaluates training usefulness and strict in-think semantics.

CPU-only. Input dataset was not changed.
