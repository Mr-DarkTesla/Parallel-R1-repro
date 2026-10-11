# Batch 1 repair notes

Repaired 12 rows: `gsm8k-train/5505`, `2502`, `5764`, `math-train/1628`, `4532`, `gsm8k-train/5647`, `5257`, `1450`, `math-train/5103`, `3533`, `gsm8k-train/5653`, and `math-train/986`.

Skipped 14 rows because two independent, nontrivial task-data paths would be artificial, duplicate work, or leave one path merely checking the other:

- `gsm8k-train/2003`: buyer count must precede conversion to boxes.
- `gsm8k-train/5203`: both proposed duration conversions determine the same album duration rather than separate needed quantities.
- `gsm8k-train/6853`: balance after the first installment requires the discounted price, so the apparent second path repeats the first calculation.
- `gsm8k-train/6598`: calculating the female complement fully resolves the task; calculating males is only a check.
- `math-train/387`: one unit conversion and one division, without independent subproblems.
- `gsm8k-train/7290`: residential and nonresidential counts restate complementary halves; restaurant split follows sequentially.
- `gsm8k-train/4508`: initial dislikes must be found before the later addition.
- `gsm8k-train/1333`: each baking action depends on the preceding remainder.
- `gsm8k-train/4110`: one subtotal followed by one discount; the discount itself has no separate task-data computation.
- `gsm8k-train/2864`: Trey’s count depends on Kris’s count, which depends on Kristen’s count.
- `math-train/1943`: a single binomial-coefficient calculation.
- `math-train/3258`: a single direct trigonometric value.
- `math-train/7487`: a single trigonometric evaluation; independent paths would only duplicate a derivation.
- `gsm8k-train/6950`: the direct four-fifths calculation fully resolves Jerusha's earnings, while solving for L only verifies it.

No source values or gold answers were changed. Every repaired response has the required think block, two numbered paths, a conclusion that uses both paths, and the preserved final answer.
