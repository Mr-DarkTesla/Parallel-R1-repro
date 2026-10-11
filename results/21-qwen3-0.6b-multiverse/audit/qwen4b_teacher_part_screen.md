# Qwen4B teacher: strict screen of labelled Part 1/Part 2

## Scope and rule

The input had 320 rows. I selected all 57 rows where the stored teacher grade is `correct=true` and the generated answer contains both `Part 1:` and `Part 2:`. Each final answer was then rechecked against its question manually.

Accepted requires two substantive labelled computations that each use only the original problem data, with no result copied from a previous Part; a later merge may use both results. A chain, a restatement of a given value, and a verification-only second Part are rejected. This is deliberately stricter than final-answer correctness.

## Result

| Metric | Count |
|---|---:|
| Screened rows | 57 |
| Accepted independent decompositions | 18 |
| Rejected as sequential/trivial/redundant | 39 |
| Manually correct external final answers | 57 |
| Both Part headings inside `<think>` | 1 |
| Mixed heading placement | 1 |
| Both Part headings outside `<think>` | 55 |

| Source | Accepted | Rejected |
|---|---:|---:|
| gsm8k | 9 | 27 |
| math | 9 | 12 |

## Placement

Only `gsm8k-train/1488` places both Part headings inside `<think>`. `gsm8k-train/2943` is mixed. The other 55 put both headings after `</think>`, so an eventual converter must move selected content into thinking.

## Per-ID decision

| ID | Result | Final correct | Reason |
|---|---|---:|---|
| `gsm8k-train/6798` | rejected | yes | Part 2 requires the 210 minutes computed in Part 1. |
| `gsm8k-train/532` | accepted | yes | Independent purchase quantities: Dan and Gus each use only stated counts and dozen conversion. |
| `gsm8k-train/3572` | accepted | yes | Blouse and dress counts use separate time/rate data, then are summed. |
| `gsm8k-train/2050` | rejected | yes | Part 1 only repeats the given 4 days; it is not a substantive independent branch. |
| `gsm8k-train/4051` | rejected | yes | Part 1 merely restates the given salad price, so the labelled pair is not two substantive computations. |
| `gsm8k-train/6465` | rejected | yes | Part 2 subtracts the Part 1 total rainfall (82 cm). |
| `gsm8k-train/1488` | rejected | yes | Part 2 substitutes Monica=40 obtained in Part 1. |
| `gsm8k-train/5845` | rejected | yes | Part 2 needs the 80 slices from Part 1. |
| `gsm8k-train/2065` | rejected | yes | Part 2 subtracts from the 63 eggs computed in Part 1. |
| `gsm8k-train/5956` | accepted | yes | Option 1 total and option 2 all-inclusive total are separate alternatives compared afterwards. |
| `gsm8k-train/6263` | rejected | yes | Part 2 triples the 30 blankets computed in Part 1. |
| `gsm8k-train/4423` | rejected | yes | Part 2 needs the four bottles computed in Part 1. |
| `gsm8k-train/3483` | rejected | yes | Part 2 halves the 100 households computed in Part 1. |
| `gsm8k-train/2943` | rejected | yes | Temperature changes form an ordered state transition, not parallel branches. |
| `gsm8k-train/4238` | rejected | yes | Part 2 adds avocado to the discounted price obtained in Part 1. |
| `gsm8k-train/3099` | accepted | yes | Natasha and Esteban totals use separate person/day inputs, then are added. |
| `gsm8k-train/1538` | rejected | yes | Part 2 sums the day counts generated in Part 1. |
| `gsm8k-train/4901` | rejected | yes | Part 2 substitutes the age relation established in Part 1. |
| `gsm8k-train/1093` | rejected | yes | Part 2 uses the 120 tacks-per-can result of Part 1. |
| `gsm8k-train/6530` | rejected | yes | Part 2 sets its equation equal to the total number of papers computed in Part 1. |
| `gsm8k-train/3381` | accepted | yes | Costs of the $15 and $20 shirt groups are disjoint quantities from the question. |
| `gsm8k-train/5582` | rejected | yes | Part 2 subtracts the first-100-floor height computed in Part 1. |
| `gsm8k-train/7034` | accepted | yes | Trout and catfish weights are independent species-level contributions; bluegills are a third such contribution. |
| `gsm8k-train/1623` | rejected | yes | Part 2 uses the 45 husbands derived in Part 1. |
| `gsm8k-train/1046` | rejected | yes | Part 2 acts on the 18 roses remaining from Part 1. |
| `gsm8k-train/6315` | rejected | yes | Part 2 only restates the given $700 window cost; it is not substantive work. |
| `gsm8k-train/61` | rejected | yes | Part 2 explicitly uses the 200 pounds from Part 1, and later steps are sequential too. |
| `gsm8k-train/5168` | rejected | yes | Part 2 requires the $102 remainder from Part 1. |
| `gsm8k-train/3238` | accepted | yes | Uphill and downhill times use the same stated distance but independent speed calculations. |
| `gsm8k-train/3053` | rejected | yes | Part 2 takes one third of the $150 computed in Part 1. |
| `gsm8k-train/1918` | rejected | yes | Part 2 halves the first-bounce height from Part 1; the recurrence is sequential. |
| `gsm8k-train/771` | rejected | yes | Part 2 divides the 16 slices computed in Part 1. |
| `gsm8k-train/6283` | accepted | yes | Ticket and dinner-plus-tip costs are separate bill components; limo is another independent component. |
| `gsm8k-train/6290` | rejected | yes | Part 2 halves the middle-tree height found in Part 1. |
| `gsm8k-train/6735` | rejected | yes | Part 1 is a given number and Part 2 depends on it, so it is not a substantive pair. |
| `gsm8k-train/3526` | accepted | yes | Per-apple and per-orange prices are independently computable before selecting the cheaper fruit. |
| `math-train/316` | rejected | yes | Part 2 needs the slope 1/4 computed in Part 1. |
| `math-train/150` | accepted | yes | The difference and sum factors are independently evaluated from x and y before multiplication. |
| `math-train/684` | rejected | yes | Currency conversion in Part 2 consumes the rah amount from Part 1. |
| `math-train/582` | rejected | yes | Part 2 is an alternative verification of the same target, not a necessary independent branch. |
| `math-train/164` | accepted | yes | Numerator and denominator use the given x,y independently before the final division. |
| `math-train/1257` | rejected | yes | The outer operation in Part 2 requires the Part 1 value -3. |
| `math-train/1491` | accepted | yes | Numerator and denominator of the fraction are computed independently. |
| `math-train/4821` | rejected | yes | Part 1 only lists the immediate reciprocals and Part 2 consumes them; no independent pair. |
| `math-train/574` | rejected | yes | Part 2 uses the common ratio derived in Part 1. |
| `math-train/2299` | accepted | yes | Green probability for container I and for II/III comes from disjoint container cases, then weighted. |
| `math-train/6350` | rejected | yes | Part 2 takes the square root of the Part 1 improper fraction. |
| `math-train/285` | accepted | yes | The two zero-product factors give independent root equations; their root sum is a valid merge. |
| `math-train/2240` | accepted | yes | Total sample count and favourable distinct-digit count are independent combinatorial quantities. |
| `math-train/1458` | rejected | yes | Part 2 only verifies the same common ratio, so it is redundant rather than a complementary branch. |
| `math-train/6376` | accepted | yes | The first and second denominator terms are independently evaluated; the third is another such term. |
| `math-train/2610` | rejected | yes | Part 2 divides the large-bowl volume computed in Part 1. |
| `math-train/3235` | rejected | yes | Second reflection acts on C′ from Part 1. |
| `math-train/6177` | rejected | yes | Part 2 substitutes x=-2 from Part 1. |
| `math-train/1238` | rejected | yes | Part 2 combines the distributed expression produced in Part 1. |
| `math-train/737` | accepted | yes | FOIL term products are independent products of input terms and are then combined. |
| `math-train/7138` | accepted | yes | x and y coordinates use the given spherical coordinates directly; z is a third independent coordinate. |

## Main rejection modes

- **Sequential dependency:** 32/39 rejections. Later Part directly uses an earlier intermediate value.
- **Trivial branch:** 5/39. At least one Part only repeats a supplied quantity.
- **Redundant verification:** 2/39. The second Part recomputes or checks the same answer, rather than contributing a distinct necessary quantity.
