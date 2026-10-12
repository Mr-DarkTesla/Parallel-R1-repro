# GSM-Infinite semantic audit, 2026-10-08

Read-only input: `${DATA_SOURCE_ROOT}/gsm_infinite_adaptive_parallel_5k.jsonl` (5000 rows).
Reproducible random sample: Python `random.Random(20261008).sample(range(5000), 30)`, sorted only for reading. Exact indices, immutable SHA-256, source keys, and sampled originals are saved alongside this report. Five extrema were selected by explicit metadata criteria and are excluded from random-sample counts. Entity substitutions in `gsm-semantic-read-*` are reading aids only; quotes and archived rows preserve source text.

## Findings and limits

The sampled parallel traces correctly evaluate the intended procedural graph. All 49 waves (123 paths) have operands available beforehand under the intended alias/aggregate interpretation; no same-wave branch reads another branch, and no duplicate alternate full-solution methods were found. All 30 traces have correct arithmetic and agree with original solutions/answers. This is a manual trace audit, not proof of literal well-posedness of every source problem: all 30 assume named species/school/movie categories exhaust each aggregate, without an explicit closed-world statement. Some derived singleton totals are introduced as though the problem literally stated the alias.

26 random rows contain parallel blocks. Their individual branches are elementary additions, subtractions, multiplications, or a short chain; none is a mathematical proof, search, difficult case split, or distinct reasoning method. 16 rows have multiple waves with real dependency handoffs, so the independence is not merely tag syntax. Yet this is a graph-scheduling curriculum, not strong evidence of hard mathematics. Long prose often increases lookup/distractor burden, not conceptual difficulty. Five sampled problems have 70–604 sentences; index3592 has 108706 problem characters but a small arithmetic target chain.

10 sampled rows repeat the same arithmetic or a common subexpression between different named target terms: 371,1759,1839,1966,2292,2393,2986,3267,3323,3827. These terms are used in the final computation, but computing the common value once is sufficient. This is a weaker defect than duplicating whole alternative methods; distinct output entities can legitimately share a formula. Index2986 repeats a sum as an independent total and as the prefix of a scaling formula. Index3323 computes mirrored 12*16 and 16*12 as separate paths.

12 sampled source problems contain a concrete negative count or average: 371,710,1790,1839,1943,2292,2377,3323,3592,3790,3799,4642. These are mostly distractors, so target arithmetic still matches the source solution; the natural-language world is nevertheless physically invalid. Witness sentences and arithmetic derivations are in the annotation JSONL. The other 18 rows were not exhaustively proven globally physically consistent.

Random index710 can be solved through alias equality and zero propagation; computing the entire upstream chain is unnecessary. The targeted maximum-depth index2103 has six valid waves but collapses through zero factors to target 2*3=6. Its tiger-count calculation is unnecessary. It illustrates why dependency depth from an unoptimized expression graph should not be equated with necessary solution depth.

No trace uses a late answer-verification branch as its proof. Matching the supplied answer alone was not counted as semantic validation; operands, alias provenance, arithmetic, output use, and physical witness relationships were read independently.

## Decision implications

Keep these traces if the intended objective is a procedural arithmetic dependency-graph/tag curriculum. For teaching substantial independent reasoning, regenerate or replace the underlying tasks: changing the teacher to DeepSeek alone cannot repair source naturalness, negative distractor quantities, or inherently elementary operations.

A revised generation/transformation contract should specify exhaustive aggregate categories; reject negative counts/averages; simplify aliases, repeated expressions and zero/one factors before measuring necessary work; choose width from genuinely distinct useful subproblems with an upper bound of 8; group cheap local chains; permit depth0 and avoid a minimum depth quota. Preserve stable globally unique row IDs (current small `id` values recur) and full source tuple, plus an explicit plan with branch IDs, inputs, outputs, dependencies and downstream consumer(s). The visible preamble should distinguish directly given facts from derived definitions. Plans help auditability, but they do not make tiny arithmetic branches harder.

Do not infer full-dataset error frequencies from the 30-row audit. No regeneration, training, or input modification was performed.

## Random-sample per-row summary

| Index (0-based) | Depth / widths | Arithmetic | Semantic note |
|---|---|---|---|
| 227 | 1 / [2] | correct under intended graph | Independent penguin increment and farm penguin increment feed different arms of a long total/count chain. Singleton totals are silently converted into aliases in the preamble. |
| 371 | 1 / [3] | correct; negative source quantity | Three early independent contributions; two different categories both compute 2*2=4. Remaining problem is a long serial arithmetic chain. |
| 490 | 0 / [] | correct under intended graph | Appropriate fully sequential solution: one multiplication then dependent totals. Total-school categories are assumed exhaustive. |
| 710 | 0 / [] | correct; negative source quantity | Equality aliases imply two teacher averages are equal; their difference is zero, so the detailed 2→4→6→12→48 chain is unnecessary for the final zero product. |
| 767 | 2 / [3, 3] | correct under intended graph | First wave computes three independent counts; second wave prepares one remaining count and two total contributions. These are required target terms, each tiny arithmetic. |
| 997 | 2 / [2, 2] | correct under intended graph | Two valid waves prepare separate count/total arms then merge. Totals use an unstated exhaustive-species convention. |
| 1255 | 2 / [2, 3] | correct under intended graph | Two first-wave arms seed three second-wave results, which all merge into the Middleton total. Several preamble aliases are derived singleton totals rather than literal given statements. |
| 1578 | 0 / [] | correct under intended graph | Appropriate sequential chain of aggregate sums and increments, with direct aliases propagated ahead of use. |
| 1759 | 2 / [3, 2] | correct under intended graph | School counts in distinct cities have the same 3+3 formula; both named quantities are needed, but one computed value can serve both. Product wave is independent. |
| 1790 | 0 / [] | correct; negative source quantity | Only one doubling and one sum determine target. Problem has 144 sentences, mostly distractors, and physically negative quantities; context length is not reasoning hardness. |
| 1839 | 2 / [2, 3] | correct; negative source quantity | Valid two-wave fork/merge DAG, but wolf and lion increments repeat exactly 2+8=10; 84-sentence source has negative distractor counts. |
| 1943 | 3 / [2, 4, 2] | correct; negative source quantity | All three waves independent. A two-operation local path computes fox count then its product, a useful example of grouping a short chain. Distinct 12-valued products are not a shared formula. |
| 1966 | 1 / [2] | correct under intended graph | Two categories each evaluate the same 4*4 product after aliases. Target needs both contributions, but parallel recomputation teaches no additional reasoning. |
| 2292 | 2 / [2, 3] | correct; negative source quantity | First wave prepares an average and an early contribution; second wave repeats mirrored 10*4 and 4*10 products from aliases, plus one distinct product. |
| 2348 | 4 / [2, 2, 4, 3] | correct under intended graph | Four waves form a real dependency DAG with early term preparation. Every path remains one elementary arithmetic step; DAG depth does not create conceptual difficulty. |
| 2377 | 3 / [2, 3, 3] | correct; negative source quantity | Three causal waves with singleton-total aliases established before use. Products with factor one are a trivial fragmentation symptom. |
| 2393 | 3 / [4, 2, 2] | correct under intended graph | Three valid waves, including one local two-operation chain. First wave duplicates 4*3=12 and mirrored 1*3/3*1=3 between distinct quantities. |
| 2542 | 1 / [2] | correct under intended graph | One valid early fork computes medical count and school count independently, then a long serial total chain. |
| 2986 | 2 / [2, 2] | correct under intended graph | Causally independent from supplied counts, but the first-wave paths repeat the same 3+3+3 sum; a shared total followed by scaling would avoid the common subexpression. |
| 3267 | 2 / [3, 2] | correct under intended graph | Two early waves legitimately precompute a long-chain result and an early total contribution. First wave repeats 4*4=16 for distinct quantities. |
| 3323 | 1 / [2] | correct; negative source quantity | The only parallel block computes 12*16 and 16*12, which are identical after aliases/commutativity. A factor-two total is clearer. |
| 3355 | 2 / [2, 2] | correct under intended graph | Two independent waves compute separate total/count arms then a final count and merge. No alternative-method duplication. |
| 3592 | 1 / [3] | correct; negative source quantity | Three tiny early branches are valid; source has 604 sentences and 108706 characters but only a short arithmetic target chain. Huge distractor context includes negative counts. |
| 3690 | 4 / [2, 2, 2, 2] | correct under intended graph | Four valid waves; last wave groups three dependent operations in one path and another contribution in the other. This demonstrates legal local sequencing, though arithmetic remains trivial. |
| 3790 | 2 / [2, 3] | correct; negative source quantity | Two independent waves, then one parrot count and total. Problem has 70 sentences and negative distractor animals; challenge is dependency lookup. |
| 3799 | 2 / [4, 2] | correct; negative source quantity | Four independent early results feed two final products. Equality of some numeric outputs does not make them identical computations. |
| 3827 | 1 / [4] | correct under intended graph | The width-four wave repeats 3+3=6 as two counts with the identical declared formula. Their contributions matter, but work can be coalesced. |
| 4045 | 1 / [4] | correct under intended graph | Four independent early computations with a later sequential total/product chain. No artificial requirement for additional rounds. |
| 4529 | 1 / [2] | correct under intended graph | Two distinct formulas share output 8 but are not the same computation (4+4 versus 4*2); both target terms are independently prepared. |
| 4642 | 1 / [2] | correct; negative source quantity | One fork prepares the fox count and a bear contribution; later total and wolf chain is sequential. Source has 90 sentences and impossible negative distractor counts/birth averages. |

## Targeted extrema (excluded from random counts)

- Index 2103, max_depth, widths [2, 2, 2, 2, 2, 2]: Six-round maximum is zero propagation: singleton adult total minus same count is 0. E1=0, E5=0, E2=0; both Westside birth contributions vanish independently of tiger count, so adult total E9 and tiger count E12 are not necessary. Pine deer newborns=0 and lion newborns=3, target=2*0+2*3=6. Depth is not substantive work.
- Index 691, depth5_max_width, widths [2, 4, 2, 2, 2]: Five waves causally valid; source contains negative sports-academy teacher average Sunset=1−25=−24 and technical-junior teacher average Hawkesbury=1−2=−1. Within-wave 5*2 is repeated for different contributions; small integer operations throughout.
- Index 22, max_width, widths [5]: Maximum width-five wave is legal but one path average=2*7 and another contribution=2*7 are repeated arithmetic. Only the following 8*14 contribution needs those prior count/average results; micro-fragmentation inflates width.
- Index 156, zero_depth_max_op, widths []: Depth zero despite op30 is appropriate: sequential chain with no independent nontrivial target arms, constants and aliases shared. op counts original micro-operations rather than mathematical difficulty.
- Index 18, single_depth_max_op, widths [2]: Depth one op30 has an independent early eagle arm and count arm; then sequential aggregate chain. Preamble derives Westside singleton total alias under implicit closure.

## Artifacts

- `gsm-semantic-annotations.jsonl`: per-row rubric, original text evidence, and negative witnesses.
- `gsm-semantic-counts.json`: sample counts and explicit limitations.
- `gsm-semantic-sample.json`: reproducibility manifest with source SHA-256.
- `gsm-semantic-sample-rows.jsonl`: exact sampled input rows.
- `gsm-semantic-targeted-*`: separately selected and labeled extremes.
