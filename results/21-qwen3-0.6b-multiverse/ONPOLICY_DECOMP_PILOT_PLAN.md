# Question-derived decomposition pilot

11 October 2026. The generic 128-trace on-policy gate stopped at
3 accepted unique questions against its predeclared minimum of 4.
This is a separate prompt and candidate-selection experiment.

## Candidate preparation

`onpolicy46_questions_only.jsonl` removes gold answers from the
previously leak-checked 256-question candidate pool. Two screeners
read only that file, selected 35/128 MATH and 40/128 GSM8K questions,
and wrote two independent subgoals plus one combine operation per
question. A second reviewer accepted 34/35 MATH and 40/40 GSM8K
plans; `math-train/3110` was rejected because Path 2 requires Path 1.
The [MATH review](audit/onpolicy46_decomp_math_independent_review.md)
and [GSM8K review](audit/onpolicy46_decomp_gsm_independent_review.md)
record the decisions. These plans do not contain gold answers or
computed result values.

`python3 scripts/exp21/prepare_decomp_pilot.py` selects 6 MATH
integer, 6 MATH expression, all 4 accepted MATH fraction, and 16
GSM8K questions, in the original deterministic candidate order.
It writes 32 [candidate records](data/onpolicy46_decomp_pilot_candidates.jsonl)
for offline scoring and a separate [plan file](data/onpolicy46_decomp_pilot_plans.jsonl)
for prompt construction. Exactly 24 tasks also occur in the generic
pilot, allowing same-task, same-seed comparisons of raw data yield.
The model receives the question and question-derived subgoals, not
the `answer` field.

## Predeclared rollout gate

Use the same recovery8 step8 model, sibling mask and positions,
temperature 0.6, top-p 0.95, top-k 20, seeds 0 and 1, and MATH/GSM8K
length caps 4096/2048. Generate 64 traces on the same owned one-GPU
pod. A planned prompt asks for one block inside `<think>`, both
subgoals computed inside independent Paths, and synthesis in
Conclusion. Save all traces and prompt metadata.

The automatic filter checks grammar, placement, truncation, length,
and external answer. Review every provisional block blind for
mathematical truth, independence, and answer not computed before the
block. Continue to a larger generation only if at least **6 unique
questions** pass, including **2 MATH, 2 GSM8K and 1 non-integer
MATH**. Every accepted block must have a correct external answer and
placement. If not, stop this recipe before SFT.

This small gate establishes data viability only. The eventual SFT
set still needs at least 46 unique accepted tasks, including 18
GSM8K and 6 MATH of each answer type. The current plan pool has only
4 MATH fraction questions, so it cannot satisfy that final condition
without further leak-checked fraction candidates. Do not lower the
final dataset requirement to fit this pilot.

Training and checkpoint selection wait until the data gate passes.
The existing five best v4 and five best v5 models on `/checkpoints`
remain protected; a future SFT must export intermediate BF16 steps
and keep its top five after equal pilot evaluation.
