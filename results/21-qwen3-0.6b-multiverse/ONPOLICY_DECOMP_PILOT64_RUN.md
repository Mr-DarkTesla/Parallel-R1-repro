# Planned on-policy masked pilot: 64 traces

11 October 2026. One H100 on owned `vcharkin-exp-vm-0`; no proxy calls.
This was a data-quality gate, not SFT or a model benchmark.

The recovery8 step8 model received 32 leak-checked training questions
(16 MATH, 16 GSM8K) and question-derived decomposition plans, never
gold answers. Two traces per question used the same sibling mask and
positions as SFT, temperature 0.6, top-p 0.95, top-k 20, and length
caps of 4096/2048 tokens for MATH/GSM8K. The generator ran once,
completed all 64 rows, and exited. Command:

```bash
cd /work/parallel-r1
/work/venv/bin/python scripts/exp21/generate_onpolicy_masked.py \
  /checkpoints/exp21-v4-recovery8/step_8/model \
  results/21-qwen3-0.6b-multiverse/data/onpolicy46_decomp_pilot_candidates.jsonl \
  /work/exp21/onpolicy_decomp/recovery8_step8_planned_pilot64.jsonl \
  --plans results/21-qwen3-0.6b-multiverse/data/onpolicy46_decomp_pilot_plans.jsonl \
  --math-count 16 --gsm-count 16 --seeds 0 1 \
  --temperature 0.6 --top-p 0.95 --top-k 20
/work/venv/bin/python scripts/exp21/filter_onpolicy_rollouts.py \
  /work/exp21/onpolicy_decomp/recovery8_step8_planned_pilot64.jsonl \
  /work/exp21/onpolicy_decomp/filter_planned64 \
  --candidates results/21-qwen3-0.6b-multiverse/data/onpolicy46_decomp_pilot_candidates.jsonl
```

[Raw outputs](eval_archives/onpolicy_decomp_pilot64/rollouts.jsonl),
[metadata](eval_archives/onpolicy_decomp_pilot64/rollouts.meta.json),
[generation log](eval_archives/onpolicy_decomp_pilot64/generation.log),
[filter summary](eval_archives/onpolicy_decomp_pilot64/summary.json),
[provisional rows](eval_archives/onpolicy_decomp_pilot64/provisional_candidates.jsonl),
and [all rejects](eval_archives/onpolicy_decomp_pilot64/rejected_rollouts.jsonl)
are retained. The filter's rejection reasons overlap:
29 incomplete/multiple blocks, 8 unnumbered blocks, 5 unclosed
`<think>`, 5 truncated outputs, 32 wrong external answers.

| Stage | MATH | GSM8K | Total |
| --- | ---: | ---: | ---: |
| Generated | 32 | 32 | 64 |
| Passed automatic grammar, placement, length, answer checks | 5 | 2 | 7 |
| Strictly useful after semantic review | 1 | 0 | 1 |

The sole accepted trace is `math-train/1024`, seed 0: two disjoint
partial sums are independently correct and added to the right answer.
The other six failed the predeclared criterion: `math-train/110`
seed 0 has a false Conclusion; `gsm8k-train/2528` seed 0 solves the
question before the block; `math-train/1024` seed 1 has a false
intermediate equation; `math-train/986` seed 0 conflicts with its
Outline; `math-train/3440` seed 0 duplicates the numerator and
denominator across Paths and has a false Conclusion. A first reviewer
accepted `gsm8k-train/5392` seed 0, but independent adjudication
rejected it: Path 2 merely restates the given one-log yield as
`9 × 1 = 9`, so the second branch is not substantive.
See [first two](audit/onpolicy_decomp_first16_review.md),
[middle three](audit/onpolicy_decomp_final64_review_a.md),
[last two](audit/onpolicy_decomp_final64_review_b.md), and
[adjudication](audit/onpolicy_decomp_5392_adjudication.md).

The continuation threshold was **six accepted unique questions**,
including two from each source and one non-integer MATH answer.
Observed: **one** unique MATH integer task. This planned-prompt
recipe stopped before the larger generation and SFT. No new model
or checkpoint was created. Existing top-five v4/v5 checkpoints on
our own PVC remain protected.

Separate question-only agent-authored annotation is being assessed
under its own provenance and gate. Its yield must not be combined
with this on-policy yield.
