# Finding: run_eval.sh parallel post-check fails on a correct non-thinking rollout (common code 84e2140)

Observed 2026-10-07 13:57 / 14:01 on B (matrix, runtime evidence, not hypothesis):
- 14f-dev-par and 15r-dev-par (scripts/instruct4b_eval/run_eval.sh <name> <model> dev parallel 16384) exit 1 after a complete
  GSM8K_DEV rollout (1184 generations, ~4 min). Queue gpu0 END exit=1; /work/runs/matrix-eval/14f-dev-par.out:
  `AssertionError: 1184 prompts without an empty think block (parallel)`.
- The preceding gate passed: gsm8k_dev.log contains `Parallel rollout chat template kwargs: {'enable_thinking': False}` (32 AgentLoopWorkers).
- Dump input (gsm8k_dev/generations/0.jsonl, column `input`): starts 'user\nSolve the following...' and ends '...How much did he pay?\nassistant\n';
  no '<|im_start|>', no '<think>' in any row.

Cause (code, read-only):
- verl/verl/trainer/ppo/ray_trainer.py:703-705 `_validate`: dumped inputs = tokenizer.decode(test_batch.batch["input_ids"], skip_special_tokens=True),
  i.e. RLHFDataset's prompt, rendered at verl/verl/utils/dataset/rl_dataset.py:261 with apply_chat_template(messages,
  add_generation_prompt=True) WITHOUT enable_thinking -> default (thinking) template, ending 'assistant\n'.
- The prompt actually generated from is built by the agent loop: parallel_thinking_loop_v3.py:104-105
  apply_chat_template(messages, add_generation_prompt=True, tokenize=True, **self.template_kwargs), template_kwargs logged
  {'enable_thinking': False}. CPU test test_rollout_prompt_matches_sft (PASS on B) asserts these tokens equal the SFT prompt.
- Tokenizer check on B (/work/runs/14-filtered/model): '<think>' is NOT a special token; default template decode(skip) ends
  'user\nhi\nassistant\n'; enable_thinking=False decode(skip) ends '<think>\n\n</think>\n\n'. So the dump input is the default
  rendering of the dataset, not stripped of a think block by decoding. For no-thinking/thinking modes (generate.py) the check is valid.

Consequence: every parallel run_eval (13-control, prep, 14f, 15r; dev and frozen) fails the same way after generation; no parallel
rows exist. Generation and scoring are not affected; only the post-check targets the wrong text in parallel mode.

Proposed minimal change (not applied; needs independent review + common commit for all three arms):
run_eval.sh, wrap the "dumped prompts must be rendered in the requested mode" python check in `if [ "$mode" != parallel ]; then ... fi`
with a comment that the rollout dump's `input` is RLHFDataset's default-template prompt (ray_trainer _validate), not the agent-loop
prompt; the parallel prompt is gated by the existing Ray-log grep for {'enable_thinking': False} (and test_rollout_prompt_matches_sft).
No change to generation, scoring, rows or paired_compare (parallel runs of all arms share the same dataset `input` text, so row
alignment is unaffected).

## Second finding (measurement limitation, not fixed): parallel dump text is not the clean block structure
Stale 14f-dev-par GSM8K dump (valid generations, failed only the old post-check): of 1172 rows with a Summary, only 261 have
consistent tag counts (#<Parallel> = #</Parallel> = #<Summary> = #</Summary>, #<Path> = #</Path> = 2 x blocks); mean per row
<Parallel> 1.58, </Parallel> 1.81, <Path> 4.08, </Path> 3.23, <Summary> 2.11. Typical block: '<Parallel><Path>...path 1 text...</</Parallel>\n\n<Summary>...</'
(path 2 text absent, bare '</' fragments); 1164 rows contain '[^>]><Path>' fragments. Tokenizer decode of a hand-built id sequence
(14f model) is correct ('<Parallel><Path>first way</Path><Path>second way</Path></Parallel>\n<Summary>sum</Summary>'), so the
irregularity is in the response ids (model emitting text fragments vs tag tokens, or rollout assembly); not determined.
Consequences: no 'summed branch tokens / decode steps' from dump text (requested by 12:16 steering; the reviewed rollout logs no
per-path lengths and the dump has no token column); score.py valid_tags / parallel share are pipeline-specific and only comparable
across arms run identically. Accuracy (Final Answer) is unaffected. Needs separate owner/decision before any code change.
