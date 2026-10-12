# Mathematical audit of Downloads/train.jsonl and val.jsonl

Inputs were read-only. No generation or training was launched. The executable checker and all evidence use the `mixed-math-*` prefix in this directory.

## Result and coverage

- 5,000 rows: 4,500 procedural rows in 53 families, 500 GSM8K reference rows in two families.
- All 4,500 procedural answers independently match a solver derived from `problem` text. The solver never uses `metadata.parameters`, `metadata.canonical_key`, the supplied answer, or the supplied response to calculate its expected answer. It covers every procedural row, including integer/parity restrictions and candidate uniqueness.
- 14,749 extractable numerical equalities in 4,568 rows match exact rational arithmetic. Of these, 13,678 equalities are procedural and 1,071 are reference. This is limited numerical replay; it does not establish correctness of every sentence, symbolic manipulation, or interpretation of a reference question.
- Another 972 checks in 658 rows match independently computed branch results: all 475 candidate rows have exactly the independently correct candidate accepted; 79 modular-union rows have correct, disjoint, exhaustive residue-class lists; 79 constrained-pair rows have correct complete y lists per x; all 25 grid tasks have the correct full dynamic-programming row.
- No confirmed incorrect mathematical answer or numerical equality was found in the procedural portion. The 500 GSM8K rows have **not** been independently solved from their question text by this audit; numerical replay is insufficient evidence for that claim.

Evidence: `mixed-math-question-checks.jsonl`, `mixed-math-numeric-equalities.jsonl`, `mixed-math-case-candidate-checks.jsonl`, and `mixed-math-summary.json`. `mixed-math-audit.py` reproduces these files and the verification analysis below.

## Suitability for difficult, meaningful multi-round parallel reasoning

There are **zero multi-round traces**. Exactly 4,700 rows have one `<Parallel>` block, and 300 have none. By split, train is 4,230 one-round plus 270 sequential; val is 470 one-round plus 30 sequential. The maximum declared branch count is four. The eight-branch budget is respected, but no trace teaches planning a second fork based on the first fork's results.

The 700 `hard` labels are all legacy procedural rows. They are labels of arithmetic scale or author choice, not evidence of measured model difficulty. The 2,500 newly generated rows explicitly carry `difficulty_basis = author heuristic; not measured model difficulty`. The overall labels are 327 easy, 3,473 medium, 700 hard, 500 unrated.

Examples of `hard` rows that require elementary arithmetic or a short closed-form calculation:

| ID | Source position | Actual task |
| --- | --- | --- |
| psft06b-00991 | train:3 | Test three offered inputs in `9*x+3=2523`, or directly solve `(2523-3)/9=280`. |
| psft06b-00982 | train:29 | Inventory `2263+744-465=2542`. |
| psft06b-01687 | train:77 | Two rates: `(217+170)*9=3483`. |
| psft06b-00034 | train:164 | Count even integers in `[200,519]`: 160. |
| psft06b-01069 | train:278 | Courier bill `7*474+30=3348`. |
| psft06b-00184 | train:80 | `|2*x-412|=39` has no integer solutions because the left inner expression is even. |
| psft06b-00994 | train:32 | Test three widths against one perimeter/area equation. |

Larger numerals do not create additional dependencies, uncertainty, search, or a reason for later rounds. Every procedural candidate task is engineered to have exactly one correct offered candidate. All candidates can be tested independently in one short pass; many candidate families also admit a simpler direct solution.

The mathematical case partitions themselves are valid. The original cases total 300 rows across five families (`absolute_value_cases`, `affine_absolute_value_cases`, `quadratic_factor_cases`, `residue_class_cases`, `consecutive_product_mod4`, each 60). New constrained-pair and modular-union cases add 158, for 458 case rows. No overlapping residue lists, duplicated x-case values, repeated factor roots, or duplicated zero-radius absolute-value roots were found. However, `modular_union_cases` splits divisibility by two or five into residues modulo three solely to manufacture three branches. It is exhaustive, but the partition is unrelated to the structure that makes inclusion-exclusion natural.

Some branches have almost no work. For example, weighted average forks the age-sum calculation and the two-term population sum; interval intersection forks a two-argument `max` and a two-argument `min`; 14 of 25 interval questions have empty intersections. All probability-bag questions have 20 balls in each bag. These are useful small demonstrations of aggregation, but do not supply the intended difficulty.

## Verification and planted recovery

There are 1,195 `verify` rows:

| Source of proposal | Rows | Correct proposals confirmed | Wrong proposals corrected |
| --- | ---: | ---: | ---: |
| Six legacy verify families; proposal first appears in assistant | 500 | 374 | 126 |
| Five new methods families relabeled verify; proposal first appears in assistant | 520 | 390 | 130 |
| New arithmetic_checks; user question contains proposed expression result | 175 | 88 | 87 |
| Total | 1,195 | 852 | 343 |

In **764 rows**, the assistant states the correct final answer before the plan and any fork (374 legacy plus 390 new). Both branches subsequently recompute or confirm this value. The resulting branches are correlated through the shared proposal; wording such as "two independent techniques" describes alternate algebraic forms, not independence of the sampled teacher outputs.

The six legacy families carry `metadata.planted_error=true` on precisely the 126 erroneous proposals and `false` on the 374 correct proposals. The student user message contains only the original question, while the erroneous proposal is inserted by the assistant. The metadata flag is not visible to the student. This can model a self-correction sequence, but it does not provide an erroneous derivation to diagnose; the student sees a bare invented candidate followed by a precomputed correction.

For the five new methods families, the 130 wrong assistant proposals are all **correct_answer + 1** (26 per family: profit markup, work completion, divisibility count, percentage recovery, rectangular frame). Their hidden metadata contains `provisional_answer`; it has no explicit `planted_error` flag. They are still controlled synthetic corrections, not observed reasoning failures. The 87 arithmetic-check corrections are better grounded because the proposal is in the question, although their underlying distributive-law tasks remain elementary.

Example: `psft5k-c4f3d8e386a5a55cb30a`, train:26, asks how many multiples of ten are in `[31,311]`. The assistant inserts 29 before the fork; both branches calculate 28, then replace 29 with 28. No preceding reasoning explains why 29 was obtained. The hidden metadata proposal is 29. The mathematical correction is correct, but the entire recovery problem is a controlled one-off counting error.

Example: `psft06b-00467`, train:1, asks for even integers in `[9,35]`. The assistant inserts 12, each branch computes 13, and the summary corrects it. Its hidden planted-error flag agrees with the independently checked difference.

Row-level verification evidence is in `mixed-math-verify-proposals.jsonl`; claims are extracted from visible questions or assistant prefixes and compared with question-derived solutions, not trusted metadata.

## Recommendation

Keep these rows only as optional format/arithmetic warmup after the wider provenance and reference-semantic audit. The best procedural primitives are the 158 constrained-pair/modular cases and 25 grid-count rows, which do require an exhaustive partition or a meaningful second mathematical method. They still have one round and elementary difficulty; retaining them does not meet the stated core requirement. The 87 user-visible erroneous arithmetic proposals are optional elementary verification examples. The 500 GSM8K references need a separate semantic and contamination decision.

For the core dataset, regenerate **tasks**, not assistant prose. Repeating forks or making the arithmetic explanation longer cannot turn `a+b-c`, a two-term average, or testing three supplied options into a difficult multi-round problem. New conditions must create substantial independent subproblems, a first-round result that changes the next plan, meaningful alternatives/cases, and occasional verifiable failed approaches with a visible derivation. Keep a single shared task-level limit of at most eight concurrent branches, and include explicit plans and stable branch IDs before each fork. Validate final answers and branch certificates from the question independently, and measure actual difficulty with model attempts rather than increasing numeral size or inheriting the present `hard` tags.
