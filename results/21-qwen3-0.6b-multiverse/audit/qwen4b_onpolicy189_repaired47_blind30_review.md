# Independent blind review: Qwen3-4B repaired47 positives

Scope: 30 unique IDs from `qwen4b_onpolicy189_repaired47_manifest.json`; full `input` and `output` fields read from `qwen4b_onpolicy189_repaired11_rollouts.jsonl`. This review did not rely on earlier per-row verdicts. A PASS requires a correct final answer, one balanced block inside `<think>`, two genuinely independent and nonduplicative substantive paths, and a Conclusion that combines their outputs without arithmetic or factual error.

Selection is reproducible and stratified. Sort each provenance pool by `sha256("qwen4b_onpolicy189_repaired47_blind30:v1:" + id)`, take the first 7 of the 11 repairs and first 23 of the 36 raw-model rows. This preserves the requested repair coverage while making selection fixed. Provenance comes from each row's `output_provenance`: raw-model means `raw_model_rollout`; repair means `approved_repair_draft`, explicitly declared as an agent-authored rewrite rather than raw model output.

| ID | Provenance | Verdict | Reason |
|---|---|---|---|
| `math-train/5103` | repair | PASS | Quarter and dime leftovers are separate quantities; both values are correct and combined to `$5.50`. |
| `math-train/3533` | repair | PASS | Separate quadratic factors yield disjoint root pairs; conclusion correctly unions them. |
| `gsm8k-train/1450` | repair | PASS | Retained original socks and acquired socks are independent quantities; conclusion correctly totals 25. |
| `math-train/5385` | repair | PASS | Repeating-block and modular-remainder derivations are distinct complete checks of digit 5; conclusion reconciles them. |
| `math-train/986` | repair | PASS | Each path simplifies a different addend; conclusion correctly combines `16x^4` and `3x^4`. |
| `math-train/758` | repair | PASS | Factoring and quadratic formula independently derive the positive physical root `4/3`; conclusion uses both. |
| `math-train/1406` | repair | PASS | Distribution and coefficient-from-factors derivations independently obtain `x^2-5x-24`; conclusion reconciles them. |
| `gsm8k-train/1856` | raw-model | FAIL | Final 45 is correct and tags are valid, but Path 2 only restates the given one watermelon cut into 15 slices as `1 x 15`; it is not a substantive sibling derivation. |
| `math-train/7110` | raw-model | PASS | Independent x and y coordinate calculations correctly combine with unchanged z. |
| `math-train/5658` | raw-model | PASS | Supplement and complement are independently derived expressions used to form and solve the required equation. |
| `gsm8k-train/6195` | raw-model | PASS | Separate percentage calculations for Mara and Luna are correct and combined. |
| `math-train/5746` | raw-model | PASS | Units and tens place counts are distinct exhaustive components; the zero tens contribution is correctly established. |
| `gsm8k-train/6080` | raw-model | PASS | Two disjoint diner groups are independently totaled and correctly subtracted from 24. |
| `gsm8k-train/5759` | raw-model | PASS | Jonathan's and his sister's name lengths are separate inputs and correctly combined. |
| `gsm8k-train/2619` | raw-model | PASS | Monday-Tuesday and Wednesday-Friday attendance totals are independent and correctly averaged. |
| `gsm8k-train/3750` | raw-model | PASS | Doll and accessory production times are separate correct quantities; conclusion combines both. |
| `math-train/7012` | raw-model | FAIL | Final pair is correct and tags are valid, but Path 1 expands to the full expression `l/2 t + 1/2`, already deriving the constant that Path 2 recomputes. Paths duplicate the same expansion rather than independently deriving coefficient and constant. |
| `gsm8k-train/982` | raw-model | PASS | Cookie production and consumption are independent quantities, correctly combined to 134. |
| `gsm8k-train/6713` | raw-model | PASS | Blueberry and cherry fruit costs are independently computed; conclusion correctly selects blueberry before the common crust is added. |
| `gsm8k-train/6149` | raw-model | PASS | Chip and cookie weights are independent and correctly combined before unit conversion. |
| `gsm8k-train/6259` | raw-model | PASS | John's and his mother's ages are independently derived from the father age, then correctly compared. |
| `math-train/1828` | raw-model | PASS | Counts for zero and exactly one 1 are disjoint outcome classes; conclusion correctly identifies the remaining double-one outcome and expectation. |
| `gsm8k-train/6845` | raw-model | PASS | Apple and orange profit computations are independent and correctly summed. |
| `math-train/2361` | raw-model | PASS | Sphere and cube volumes are independent and correctly combined as a probability ratio. |
| `gsm8k-train/5025` | raw-model | PASS | Each applicant's net is independently computed; conclusion correctly takes their difference. |
| `gsm8k-train/4340` | raw-model | PASS | Saturday and Sunday revenue are independent calculations from stated attendance and fee; conclusion combines them. |
| `math-train/1366` | raw-model | FAIL | Final 4 and tag structure are correct, but opening text already derives the requested root sum by Vieta before the block. The block is decorative; Path 2 is also an unsupported abbreviated reuse of the quadratic-formula calculation. |
| `gsm8k-train/5074` | raw-model | PASS | Nose and ear revenues are separate, correctly calculated, and combined. |
| `math-train/446` | raw-model | PASS | Numerator and denominator exponents are separate operands and are correctly combined by exponent subtraction. |
| `gsm8k-train/4013` | raw-model | PASS | Savings and spending are separate totals and correctly combined to 14. |

Aggregate: **27/30 PASS** for useful independent parallel reasoning; **3/30 FAIL**. Raw-model: **20/23 PASS**, **3/23 FAIL**. Agent-authored repair: **7/7 PASS**. All 30 have a correct final answer, a non-truncated balanced `<think>`/parallel tag tree, and a Conclusion containing both path results; failures are semantic usefulness/independence only. Therefore this sample does not support treating all 47 manifest positives as equally clean training positives. The three failed IDs should be excluded or re-reviewed before a strict positive-only SFT claim.

## Completion: remaining 17 manifest IDs

The same full-response review was applied to every manifest ID absent from the blind-30 section. Provenance labels use the same `output_provenance` rule.

| ID | Provenance | Verdict | Reason |
|---|---|---|---|
| `gsm8k-train/1362` | raw-model | PASS | Joanna's and Jacques's post-purchase totals are independent, correctly combined, and evenly divided. |
| `gsm8k-train/346` | raw-model | PASS | The two identical small walls and the two other walls are disjoint area groups; conclusion correctly totals and divides by coverage. |
| `gsm8k-train/5711` | raw-model | PASS | Total expenses and hourly net earnings are distinct required quantities; conclusion correctly computes break even at 3 hours. |
| `gsm8k-train/1295` | raw-model | PASS | Friend and relative sales revenue are independent and correctly combined. |
| `gsm8k-train/4374` | raw-model | FAIL | Final 4 and tag structure are correct, but both paths repeat the same calculation `1 serving/day x 30 days = 30`; naming Phoebe and the dog does not create two nonduplicative substantive paths. |
| `math-train/5843` | raw-model | PASS | Independent denominator clearing for the left and right sides produces the correct combined linear equation and final value. |
| `gsm8k-train/1952` | raw-model | PASS | Daily sales progression and cent-to-dollar unit conversion are distinct required quantities, correctly combined to 12 dollars. |
| `gsm8k-train/3674` | raw-model | PASS | Separate substitutions independently derive female and male attendee counts; conclusion uses both and final correctly returns 62. |
| `math-train/3849` | raw-model | PASS | Products by `x^2` and by 18 are distinct distributive components; conclusion correctly subtracts them. |
| `gsm8k-train/1746` | raw-model | PASS | Original-worker and new-hire payrolls are independent group totals, correctly combined. |
| `math-train/529` | raw-model | PASS | Numerator and denominator powers are separate operands, correctly combined into the eighth term. |
| `gsm8k-train/1103` | raw-model | PASS | Rose and orchid totals are independent non-lily counts; conclusion correctly combines them before the final lily calculation. |
| `math-train/1007` | raw-model | PASS | Horizontal and vertical coordinate changes are independent components; conclusion correctly applies their squared distances. |
| `gsm8k-train/4149` | repair | PASS | Capacities of the first two and last two levels are independent subtotals, correctly combined and adjusted for occupied spaces. |
| `gsm8k-train/6960` | repair | PASS | Total-pay and hourly-deficit calculations independently derive the required 45-dollar planting charge. |
| `gsm8k-train/3303` | repair | PASS | Event-by-event accounting and remaining-fraction calculation are distinct complete derivations of 196. |
| `math-train/505` | repair | PASS | Finite-series formula and shifted-series cancellation independently derive the same correct fraction. |

## Full-manifest aggregate

All **47/47** manifest IDs were read in full. **43/47 PASS** and **4/47 FAIL** under the stated strict semantic criterion. Raw-model: **32/36 PASS**, **4/36 FAIL**. Agent-authored repair: **11/11 PASS**. All 47 have a correct final answer, a non-truncated balanced tag tree inside `<think>`, and a Conclusion that refers to both paths. The four failures are limited to semantic path quality: `gsm8k-train/1856` has a trivial second path; `math-train/7012` duplicates the same expansion in both paths; `math-train/1366` solves the requested result before a decorative block and gives an unsupported abbreviated second path; `gsm8k-train/4374` duplicates the same serving calculation. A strict positive-only SFT set should exclude or re-review those four IDs.
