# Independent review: `extra30_m2.jsonl`

Scope: 30 M2 responses from `extra30_m2.jsonl`. Review was manual and CPU-only. It checks the prompt condition, every displayed calculation, text inside and after `<Parallel>`, final answer, and whether paths are independent and useful. No automatic verifier was used as evidence.

Definitions used below:

- **Final answer correct** means it is mathematically equivalent to the reference answer and meets the requested form.
- **Paths useful** means every path is mathematically sound, addresses a separable subproblem, and can be relied upon as a reasoning trace.
- **Exclude** means the response has a substantive false claim, false equality, invalid enumeration, or invalid derivation anywhere in its text, even if its final answer happens to be correct.

## Summary

| Measure | Result |
|---|---:|
| Rows reviewed | 30 |
| Correct final answers | 30 |
| Incorrect final answers | 0 |
| Useful and independent Parallel blocks | 24 |
| Fully clean, retainable responses | 23 |
| Exclude for substantive content error | 7 |

All 30 final answers match the reference mathematically. Seven outputs must nevertheless be excluded because the reasoning contains a substantive error. `math-train/1368` has a proof-completeness gap, recorded below, but no false calculation.

## Per-ID review

| ID | Final answer correct | Paths useful | Review |
|---|---|---|---|
| math-train/2909 | Yes | No | Final `40` matches reference. Response falsely identifies Q as the centre although prompt states Q lies on circle; it then applies centre/chord claims at wrong points. Geometry does not establish result. Exclude. |
| gsm8k-train/5583 | Yes | Yes | Team scores are 26, 28, 27; mean `(26+28+27)/3=27`. Three independent team-score paths. |
| gsm8k-train/4661 | Yes | Yes | Knobs `18*2.50=45`, pulls `8*4=32`, total 77. |
| gsm8k-train/592 | Yes | Yes | Separate trips use 150 and 100 litres; total 250. |
| gsm8k-train/4018 | Yes | Yes | Hubert costs 130 and Ian 167; total 297. |
| gsm8k-train/7024 | Yes | Yes | Rice costs 10 and meat 15; total 25. |
| math-train/5035 | Yes | Yes | `4609=1 mod 12`, `2104=4 mod 12`, hence `x=3 mod 12`; least positive value 3. |
| math-train/5462 | Yes | Yes | Base expansions `7d+4=8d+1` give digit `d=3`, valid in both bases. |
| math-train/2465 | Yes | Yes | `C(14,6)-C(11,3)=3003-165=2838`. |
| math-train/3684 | Yes | No | Product is 3, but response changes given decomposition from `B/(x+2)+C/(x-3)` to `B/(x-3)+C/(x+2)`. B and C happen both to equal -1, so product survives. Invalid intermediate re-labelling. Exclude. |
| math-train/1536 | Yes | Yes | Ceiling 1.25 is 2; floor -1.25 is -2; sum 0. |
| math-train/1368 | Yes | Yes, with proof gap | `(a,b)=(3,2)` gives 15 and sum 5. Response checks only selected cases and does not prove that `b>=5` for `a=2`, or `a>=4`, cannot work. No false arithmetic; result correct. |
| math-train/6210 | Yes | Yes | `gcd(30,81)=3`, `lcm(36,12)=36`, sum 39. |
| math-train/7261 | Yes | No | Bisector length is 3. Path 1 falsely states `angle A = 1/8`; given condition is `cos angle A = 1/8`. Later half-angle calculation uses the correct cosine, so final number survives. Exclude. |
| math-train/1997 | Yes | Yes | Four of six unordered city pairs are below 7000 miles; probability `4/6=2/3`. |
| math-train/2362 | Yes | Yes | `sqrt(n)<8` means `10<=n<=63`: 54 favourable of 90, yielding `3/5`. |
| math-train/1552 | Yes | Yes | Equating squared distances gives `4+y^2=1+(4-y)^2`, so `y=13/8`. |
| math-train/2242 | Yes | No | Final `3/8` is correct, but Path 2 lists `HHH, HHT, TTH` as two-tail/one-head outcomes. Only TTH fits; correct set is HTT, THT, TTH. Exclude. |
| math-train/2559 | Yes | Yes | Areas are `16sqrt(3)` and `4sqrt(3)`; trapezoid is `12sqrt(3)`; ratio `1/3`. |
| math-train/2289 | Yes | Yes | Inclusion-exclusion gives `12+5-2=15` multiples; `15/25=3/5`. |
| math-train/3196 | Yes | Yes | Larger radius 6, smaller volume `36pi` and radius 3; ratio `1/2`. |
| math-train/2219 | Yes | No | Final `2/9` is correct, but enumeration is not. Path for hundreds digit 3 omits 331, 333, 332; after block it calls 322 and 222 divisible by 4, though both are not, and omits valid 132, 232, 332. Exclude. |
| math-train/469 | Yes | Yes | All nine products and collection of terms yield `-6t^4+11t^3-19t^2+17t-10`. |
| math-train/7349 | Yes | Yes | `BA=(1,1,4)`, `BC=(-1,0,1)`, dot product 3, norms `3sqrt(2)` and `sqrt(2)`, so cosine 1/2 and angle 60 degrees. |
| math-train/4258 | Yes | Yes | Linear remainder conditions are `19m+n=99`, `99m+n=19`; solution is `-x+118`. |
| math-train/6635 | Yes | Yes | `3/4` is mean of `7/10` and `4/5`. After its correct block, however, response falsely says mean of `7/10` and `3/4` is `3/4`; it had just computed that mean as `29/40`. Exclude. |
| math-train/5408 | Yes | Yes | Six complete cycles pay `6*21=126`; final three hours pay 6; total 132. |
| math-train/2904 | Yes | No | Final 178% is correct by cancellation, but areas use diameters as radii: semicircle diameters 6 and 10 have areas `9pi/2` and `25pi/2`, not `18pi` and `50pi`. Exclude. |
| math-train/4561 | Yes | Yes | Distributive products cancel middle terms, leaving `8x^9-125y^6`. |
| math-train/6266 | Yes | Yes | Weighted total is `30*72+6*78=2628`; mean `2628/36=73%`. |

## Exclusion evidence

### `math-train/2909`

Quote: “`point Q is the center of the circle`.”

Prompt explicitly says Q lies on the circle. The response then calls AQ and CQ radii and asserts angle Q is 180 degrees, which is incompatible with the diagram and the stated configuration. It also treats exterior P as an intersection of chords. Final 40 is coincidentally correct; trace is unusable.

### `math-train/3684`

Quote: “`= A/(x - 1) + B/(x - 3) + C/(x + 2)`.”

Given decomposition assigns B to `x+2` and C to `x-3`. The response swaps these denominators before solving. The resulting values are both -1, so `ABC=3` remains correct only because the swap is numerically invisible here.

### `math-train/7261`

Quote: “`angle A = 1/8`.”

The prompt gives `cos angle A = 1/8`, not the angle itself. The following half-angle work uses the right input, but displayed premise is false.

### `math-train/2242`

Quote: “`The number of favorable outcomes (two tails and one head) is 3: HHH, HHT, TTH.`”

HHH has zero tails and HHT has one tail. Correct favourable outcomes are HTT, THT, TTH. Count 3 and final probability remain correct by coincidence.

### `math-train/2219`

Quote: “`The numbers divisible by 4 are: ... 312, 322, ... 222`.”

322 and 222 are not divisible by 4. The response also omits valid 132, 232 and 332; Path 2 itself fails to enumerate three possible 3xx outcomes. It obtains the correct count six despite invalid enumeration.

### `math-train/6635`

Quote: “`the arithmetic mean of 7/10 and 3/4 is 3/4`.”

That mean is `29/40`, as its preceding Path 2 correctly computes. The requested final answer is still 3/4 because it is the mean of 7/10 and 4/5.

### `math-train/2904`

Quote: “`A semicircle with diameter 6 m has an area ... 18pi`.”

Diameter 6 gives radius 3, hence area `(1/2)*pi*3^2=9pi/2`; diameter 10 gives `25pi/2`. The response squares diameters rather than radii. Their ratio happens to be unchanged, so 178% is still correct.

## Retention decision

Exclude: `math-train/2909`, `math-train/3684`, `math-train/7261`, `math-train/2242`, `math-train/2219`, `math-train/6635`, `math-train/2904`.

`math-train/1368` can be retained if a missing uniqueness argument is acceptable; otherwise review it for a proof-completeness standard. It contains no factual or arithmetic error.
