# On-policy masked pilot: 128 traces

11 October 2026. One H100 on owned `vcharkin-exp-vm-0`; no proxy calls.
This is a data-quality gate, not a model benchmark or SFT run.

## Setup and retained evidence

The existing `exp21-v4-recovery8/step_8` BF16 model generated two
sampled traces each for 32 fresh MATH and 32 fresh GSM8K training
questions. Candidate selection and leak checks are in
[ONPOLICY46_PLAN.md](ONPOLICY46_PLAN.md). The model saw questions,
never gold answers. Decoding used the same independent sibling mask
and positions as training: temperature 0.6, top-p 0.95, top-k 20,
MATH limit 4096, GSM8K limit 2048, seeds 0 and 1.

Reproduction on the prepared pod:

```bash
cd /work/parallel-r1
/work/venv/bin/python scripts/exp21/generate_onpolicy_masked.py \
  /checkpoints/exp21-v4-recovery8/step_8/model \
  results/21-qwen3-0.6b-multiverse/data/onpolicy46_candidates.jsonl \
  /work/exp21/onpolicy46/recovery8_step8_masked_pilot128.jsonl \
  --math-count 32 --gsm-count 32 --seeds 0 1 \
  --temperature 0.6 --top-p 0.95 --top-k 20
/work/venv/bin/python scripts/exp21/filter_onpolicy_rollouts.py \
  /work/exp21/onpolicy46/recovery8_step8_masked_pilot128.jsonl \
  /work/exp21/onpolicy46/filter_full128 \
  --candidates results/21-qwen3-0.6b-multiverse/data/onpolicy46_candidates.jsonl
```

All 128 rows have distinct `(id, seed)` pairs and cover 64 distinct
questions, 32 per source. The process exited after writing row 128.
Full [raw outputs](eval_archives/onpolicy46_pilot128/rollouts.jsonl),
[generation log](eval_archives/onpolicy46_pilot128/generation.log),
[run metadata](eval_archives/onpolicy46_pilot128/rollouts.meta.json),
[automatic filter summary](eval_archives/onpolicy46_pilot128/summary.json),
[provisional rows](eval_archives/onpolicy46_pilot128/provisional_candidates.jsonl),
and [rejected rows](eval_archives/onpolicy46_pilot128/rejected_rollouts.jsonl)
are retained locally in the branch.

## Quality gate

| Stage | MATH | GSM8K | Total |
| --- | ---: | ---: | ---: |
| Generated | 64 | 64 | 128 |
| Passed structure, placement, length, external-answer checks | 14 | 11 | 25 |
| Accepted after blind semantic review | 1 | 2 | 3 |

The automatic rejection reasons overlap: 62 lacked exactly one
complete block, 8 had an unclosed `<think>`, 8 were truncated, and
48 lacked a correct external final answer. Mean generation length
was 780 tokens, median 400, maximum 4096. Among the 25 provisional
rows, all external answers were correct by construction. Reviewers
rejected 22 for repeated, missing, or mathematically false paths,
or an answer computed before the block. Review sheets cover
[rows 1–5](audit/onpolicy46_first32_primary_review.md),
[6–9](audit/onpolicy46_first64_review_a.md),
[10–13](audit/onpolicy46_first64_review_b.md),
[14–16](audit/onpolicy46_first96_review_a.md),
[17–19](audit/onpolicy46_first96_review_b.md),
[20–22](audit/onpolicy46_final128_review_a.md), and
[23–25](audit/onpolicy46_final128_review_b.md).

Accepted unique tasks: `math-train/110` seed 1,
`gsm8k-train/2528` seed 0, and `gsm8k-train/4597` seed 0.
The MATH task has an integer answer. Neither fraction nor expression
MATH answers passed manual review. The three accepted blocks meet
the answer and placement conditions; the two GSM8K blocks and the
MATH block received independent second reviews.

The predeclared continuation gate required at least **four** unique
accepted tasks, including one GSM8K. Result: **three**. The full
256-question rollout and SFT are therefore stopped for this recipe.
No new checkpoint was trained or selected. Ten earlier v4/v5
top-five models remain on the owned checkpoint PVC.

Failure analysis: generic instructions often made the model solve
the problem before `<Parallel>`, repeat one calculation in both
`<Path>` branches, or put the actual work in `<Conclusion>`. A
subsequent data attempt should select only questions with two
necessary, independently computable quantities and specify those
subgoals from the question alone. Gold must remain only in the
offline answer checker. Any changed prompt or selection needs its
own staged gate before SFT.
