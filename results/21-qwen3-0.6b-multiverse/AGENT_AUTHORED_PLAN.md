# Separate annotation method: question-only authored blocks

11 October 2026. This method is separate from the on-policy Qwen
rollouts and earlier M1/M2 datasets. The generic Qwen pilot yielded
3 accepted tasks out of 128 traces. The planned Qwen pilot continues
on one GPU under its own predeclared gate.

For this annotation pilot, two independent writers receive only
the 32 leak-checked questions in
[`onpolicy46_questions_only.jsonl`](data/onpolicy46_questions_only.jsonl)
and question-derived, independently screened
[`decomposition plans`](data/onpolicy46_decomp_pilot_plans.jsonl).
They do not receive gold answers or previous model rollouts. One
writer owns 16 MATH questions, the other 16 GSM8K. Each may omit a
question if its solution or parallel split is uncertain; omissions
and reasons must be recorded. The target contains one substantive
two-path `<Parallel>` block wholly inside `<think>`, followed by an
external `Final Answer:`. The entire solution text may be corrected;
this is authored annotation, not verbatim Qwen trace conversion.

Before SFT, run the same strict structural and external-answer
checks used for Qwen data, verify token limits, and independently
review at least 30 new examples with at least 90% useful blocks and
zero wrong answers. Also read at least 20 full examples directly.
Keep only accepted unique tasks. A training set still requires at
least 46 accepted tasks, including 18 GSM8K and six MATH each with
integer, expression, and fraction answers. This 32-question pilot
alone cannot satisfy the training minimum. The larger pool needs
more leak-checked MATH fractions before SFT.

Raw writer outputs, skipped IDs, automatic rejection reasons,
manual decisions, and accepted subset must be saved separately.
This method will not be counted as on-policy data in comparisons.

The expanded batch is complete: 82 authored rows, 81 automatic
passes, and [78 strict accepts](AGENT_AUTHORED_DATASET_CARD.md)
after independent review. All source and answer-type minimums are
met. The next step is matched SFT and dev selection with intermediate
BF16 checkpoints; the two failed Qwen on-policy prompts remain
separate negative results.
