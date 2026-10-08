# Independent manual review: `audited_m2_independent40.jsonl`

Scope: all 40 M2 rows. Review is manual and CPU-only. It checks the prompt condition, all displayed equalities and arithmetic inside and outside `<Parallel>`, final answer, and whether Parallel paths are independent and useful. No Claude-auditor verdict or `math_verify` result was used as evidence.

Criteria:

- **Final correct**: final answer matches the requested mathematical value and form.
- **Useful paths**: paths solve separable subproblems, are mutually independent except for prompt facts, and contain no mathematical error.
- **Exclude**: any substantive false claim, false equality, invalid case enumeration, wrong formula, or non-useful Parallel block.

## Summary

| Measure | Result |
|---|---:|
| Rows reviewed | 40 |
| Correct final answers | 40 |
| Incorrect final answers | 0 |
| Useful independent Parallel blocks | 40 |
| IDs with substantive error or non-useful block | 0 |
| Required useful-path threshold | at least 36/40 |
| Threshold result | pass: 40/40 |

No row needs exclusion. The requested gate, at least 36 useful blocks and zero incorrect final answers, is satisfied.

## Per-row review

| ID | Final correct | Paths useful | Manual verification |
|---|---|---|---|
| gsm8k-train/3362 | Yes | Yes | Flock composition is 60 American and 30 European; capacities 5 and 10; total 600. |
| gsm8k-train/697 | Yes | Yes | Weekly study time is `2*5 + 3*2 = 16`; six weeks gives 96. |
| gsm8k-train/4396 | Yes | Yes | Forest has `4*6*600=14400` trees; eight loggers cut 48 daily, 1440 monthly, so 10 months. |
| gsm8k-train/3004 | Yes | Yes | 48 oz need eight blueberry cartons for 40 dollars or six raspberry cartons for 18 dollars; saving 22. |
| gsm8k-train/4400 | Yes | Yes | Uphill 3 miles at 2 mph takes 1.5 h; downhill 2 miles at 3 mph takes 2/3 h; total 130 min. |
| gsm8k-train/3504 | Yes | Yes | Five courses contain 2000 bricks; removal of half of final 400-brick course leaves 1800. |
| gsm8k-train/539 | Yes | Yes | Replanting is `200*3=600` plus `300*3=900`, total 1500. |
| math-train/1931 | Yes | Yes | Complement count: `5^4-3^4=625-81=544`. |
| math-train/4997 | Yes | Yes | Residues of squares mod 10 are exactly 0,1,4,5,6,9: six digits. |
| math-train/3632 | Yes | Yes | Polynomial is even, hence `f(-91)=f(91)=1`; displayed derivation also gives sum 2. |
| math-train/4115 | Yes | Yes | Substituting 1 and -1 gives two valid equations; solving yields `f(2)=0`. |
| math-train/1564 | Yes | Yes | Midpoint equations give B=(5,2), product 10. |
| math-train/210 | Yes | Yes | Quadratic roots are -1/3 and -1/2; values of `2a+1` are 1/3 and 0, minimum 0. |
| math-train/2190 | Yes | Yes | Fibonacci recurrence gives 144 valid binary strings of length 10; `144/1024=9/64`, sum 73. |
| math-train/2249 | Yes | Yes | `3*C(5,2)*C(5,1)^2 = 750`. |
| math-train/46 | Yes | Yes | Completing squares yields centre (-2,3), radius 4, sum 5. |
| math-train/5010 | Yes | Yes | Base-h equality reduces to `h^2(h^2-7h-8)=0`; only valid base is 8. Digits also require base at least 8. |
| math-train/327 | Yes | Yes | Numerator is `(x^3-8)^2`; at x=6 quotient is `216-8=208`. |
| math-train/3582 | Yes | Yes | `f(2)=b`; inverse is `b/(2x)+3/2`; condition gives roots `(1±sqrt(7))/2`, product -3/2. |
| math-train/259 | Yes | Yes | Completed squares give `(x-1)^2+(y+2)^2=1/9`; radius 1/3. |
| math-train/3512 | Yes | Yes | Correct branch choices: `f(2,1)=1/2`, `f(2,4)=-1/4`, sum 1/4. |
| math-train/1774 | Yes | Yes | Parity patterns are equiprobable with probability `2^-6`; exactly three even choices give `C(6,3)/2^6=5/16`. |
| math-train/2770 | Yes | Yes | Intersections are (-4,1), (2.5,1), (1.2,3.6); shoelace/base-height area is 8.45. |
| math-train/2493 | Yes | Yes | Inclusion-exclusion count `10+7-1=16`; probability `16/50=8/25`. |
| math-train/1846 | Yes | Yes | Six distinct values require a permutation of 1 through 6; `6!/6^6=5/324`. |
| math-train/2240 | Yes | Yes | There are 90 two-digit integers and `9*9=81` with unequal digits; probability 9/10. |
| math-train/1171 | Yes | Yes | y-axis intercepts are (0,-2),(0,4); other intersection is (9/5,17/5); area `(1/2)*6*(9/5)=27/5`. |
| math-train/6887 | Yes | Yes | Direction (2,3,6), plane normal (-10,-2,11), dot 40, norms 7 and 15; sine 8/21. |
| math-train/5995 | Yes | Yes | Doubling diameter doubles radius and quadruples area; original/enlarged ratio 1/4. |
| math-train/1678 | Yes | Yes | With `u=sqrt(1+4a^2)`, equation is `(7u-u^2)/(u+3)=2`; u=2 or 3 produces ±sqrt(3)/2, ±sqrt(2); greatest sqrt(2). |
| math-train/4114 | Yes | Yes | Squared denominator is positive except undefined x=2; numerator negative for x<4, giving `(-infinity,2) union (2,4)`. |
| math-train/1210 | Yes | Yes | Midpoint equations yield other endpoint (-2,-9). |
| math-train/4032 | Yes | Yes | Vieta gives sum roots 1/2 and pairwise sum 2; squared sum `1/4-4=-15/4`. |
| math-train/2649 | Yes | Yes | Hemisphere total area is curved `2pi r^2` plus base `pi r^2`; base condition gives 300pi. |
| math-train/3227 | Yes | Yes | Two-inch cube volume is 8 and value per cubic inch is 25; volume 27 gives 675 dollars. |
| math-train/1147 | Yes | Yes | Conjugate product denominator -1 and numerator `1-sqrt(6)`; quotient `sqrt(6)-1`. |
| math-train/4716 | Yes | Yes | Base-10 values are 213 and 159, difference 54, which is `66_8`. |
| math-train/3327 | Yes | Yes | Second hand makes 30 revolutions in 30 minutes; circumference is 12pi; distance 360pi. |
| math-train/1253 | Yes | Yes | Constraints give `(1/2,1)` and `(1/3,2/3)`; intersection `(1/2,2/3)`. |
| math-train/3170 | Yes | Yes | Unit-cube triangle ABC has area 1/2; perpendicular height from H is 1; pyramid volume 1/6. |

## Error / exclusion list

None. No substantive incorrect equality, arithmetic operation, geometric claim, branch choice, enumeration, or post-block contradiction was found in these 40 rows.
