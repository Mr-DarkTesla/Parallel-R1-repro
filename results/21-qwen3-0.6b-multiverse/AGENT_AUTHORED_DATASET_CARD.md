# Question-only authored parallel blocks: accepted 78

11 October 2026. This is a third data-construction method, distinct
from M1, M2, and Qwen-generated on-policy traces. Subagents wrote
solutions from questions and question-derived plans only; they did
not see candidate gold answers or prior Qwen rollouts. One reviewer
later checked each solution against the held-out answer. The target
text contains one two-path `<Parallel>` block wholly inside `<think>`
and a final answer after `</think>`. Solution wording was allowed to
change. No VK AI Proxy calls and no GPU generation were used to
author this batch.

## Provenance and screening

All 82 proposed tasks came from the previously leak-checked
[on-policy candidate pool](ONPOLICY46_PLAN.md), which excludes SFT
and fixed40 task collisions, GSM8K dev, all eval sets, and full MATH
test duplicates/variants. Original [pool card](DATASET_POOL.md) and
[candidate audit](data/onpolicy46_candidates.audit.json) retain the
selection history. Four author batches were expanded to five when
additional fractions were needed:

| Batch | Source | Authored | Independently accepted |
| --- | --- | ---: | ---: |
| [pilot MATH](data/onpolicy_agent_authored_math16.jsonl) | MATH | 16 | 16 |
| [remaining MATH](data/onpolicy_agent_authored_math_remaining.jsonl) | MATH | 18 | 18 |
| [extra fractions](data/onpolicy_agent_authored_fraction8.jsonl) | MATH | 8 | 8 |
| [pilot GSM8K](data/onpolicy_agent_authored_gsm16.jsonl) | GSM8K | 16 | 14 |
| [remaining GSM8K](data/onpolicy_agent_authored_gsm_remaining.jsonl) | GSM8K | 24 | 22 |
| **Total** | | **82** | **78** |

The first 32 complete question/solution pairs received a separate
[primary full-text review](audit/agent_authored32/primary_full_review.md),
and eight additional fraction solutions were read in full. Independent
reviews cover [pilot MATH](audit/onpolicy_agent_authored_math16_independent_review.md),
[remaining MATH](audit/onpolicy_agent_authored_math_remaining_independent_review.md),
[extra fractions](audit/onpolicy_agent_authored_fraction8_independent_review.md),
[pilot GSM8K](audit/onpolicy_agent_authored_gsm16_independent_review.md),
and [remaining GSM8K](audit/onpolicy_agent_authored_gsm_remaining_independent_review.md).
The first GSM8K reviewer accepted two blocks later rejected by the
primary strict substantive-path adjudication. Final decisions take
the stricter verdict. Four rejected IDs and reasons are in
[`semantic_rejected.json`](audit/agent_authored82/semantic_rejected.json):
`gsm8k-train/5392`, `/5215`, `/2502`, `/5172` each has a Path that
only repeats a number already supplied in the question.

## Automatic gate and repairs

The same `filter_onpolicy_rollouts.py` used for Qwen data checked
grammar, exactly one numbered block inside one closed `<think>`,
external answer with `math_verify`, token length and truncation.
The Qwen3 tokenizer on the pod counted output tokens. The accepted
rows span 118–395 tokens (median 199.5), with zero above 2048 or
4096. Authors did not receive gold keys or prior Qwen rollouts;
their final answers were checked only after authorship.

Commands on the local checkout and owned pod:

```bash
python3 scripts/exp21/merge_authored_batch.py \
  results/21-qwen3-0.6b-multiverse/data/onpolicy46_candidates.jsonl \
  results/21-qwen3-0.6b-multiverse/audit/agent_authored82 \
  results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_math16.jsonl \
  results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_math_remaining.jsonl \
  results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_fraction8.jsonl \
  results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_gsm16.jsonl \
  results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_gsm_remaining.jsonl
kubectl -n shared-dzen-ml cp \
  results/21-qwen3-0.6b-multiverse/audit/agent_authored82 \
  vcharkin-exp-vm-0:/work/exp21/agent_authored82
```

On `vcharkin-exp-vm-0`:

```bash
cd /work/parallel-r1
/work/venv/bin/python scripts/exp21/prepare_agent_authored_rollouts.py \
  /work/exp21/agent_authored82/candidates.jsonl \
  /work/exp21/agent_authored82/math.jsonl \
  /work/exp21/agent_authored82/gsm.jsonl \
  /checkpoints/exp21-v4-recovery8/step_8/model \
  /work/exp21/agent_authored82/rollouts.jsonl
/work/venv/bin/python scripts/exp21/filter_onpolicy_rollouts.py \
  /work/exp21/agent_authored82/rollouts.jsonl \
  /work/exp21/agent_authored82/filter \
  --candidates /work/exp21/agent_authored82/candidates.jsonl
```

The [archived filter](audit/agent_authored82/filter/summary.json)
passed 81/82 automatically. The sole automatic reject was `/5172`:
its semantic answer `20%` differs from the numeric gold key `20` to
the strict parser, and its first Path is weak anyway. Three other
weak blocks passed automatic checks, then failed manual review.
The clean [accepted 78](data/onpolicy_agent_authored_accepted78.jsonl)
are all among automatic passes. There are **78/82 = 95.1% useful
blocks** after strict review and **zero incorrect external answers**
in the retained set. Composition: **36 GSM8K integers, 17 MATH
integers, 13 MATH expressions, 12 MATH fractions**. This clears the
predeclared minimum of 46 accepted unique tasks, 18 GSM8K, and six
MATH tasks of each answer type. It is eligible for a new SFT recipe;
no accuracy claim follows from data quality alone.

Formatting fixes before the final gate: six GSM8K final currency
answers were written as bare numbers, and `math-train/2361` changed
the TeX form `\frac\pi6` to `\frac{\pi}{6}` in the Conclusion and
final answer. The original files are preserved in
[`audit/agent_authored32`](audit/agent_authored32/) and
[`math_remaining_before_fraction_format_fix.jsonl`](audit/agent_authored74/math_remaining_before_fraction_format_fix.jsonl).
No arithmetic result changed. `math-train/1982` gold displays both
an exact fraction and a requested rounded currency value; the
answer checker was corrected to compare the displayed rounded value.
Rechecking the generic 128 Qwen traces left its automatic 25/128
count unchanged.

The accepted set is a quality-screened small SFT addition. It must
be compared with a control trained on exactly the same plain text,
with tags removed, and evaluated on the same dev tasks. Frozen sets
remain reserved for the selected winner.
