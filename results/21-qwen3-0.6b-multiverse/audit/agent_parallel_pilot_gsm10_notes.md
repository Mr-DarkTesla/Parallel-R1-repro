# Agent parallel GSM8K pilot: annotation notes

Input: `/tmp/exp21-agent-pilot-gsm10.jsonl`, 10 leakchecked unseen GSM8K questions without answers. All ten were independently solved and written to `data/agent_parallel_pilot_gsm10.jsonl` before pool gold was read. Every draft has one balanced `<Parallel>` block inside `<think>`, two independent paths, a conclusion that combines both path results, and a final-answer line. No question required a forced decomposition or a `skip` row.

Post-draft pool-gold check: 9 of 10 final answers match `data/pool.jsonl` exactly: `6111=180`, `1810=92`, `6392=1234`, `6824=13`, `5088=40`, `7417=170`, `271=250`, `5750=1800`, and `5789=6`.

`gsm8k-train/108` requires adjudication. Pool gold is `41`, which is only the daily cost: `4 x $1.50 + 5 x ($1.50 + $5.50) = $41`. The question explicitly says Henry takes these pills for 14 days, so the independently derived total is `14 x $41 = $574`. The drafted output remains mathematically consistent and is marked `gold_conflict`; it must not enter a gold-supervised set until its reference answer is corrected or the question wording is changed.

Post-gold corrections to draft answers: none. The only discrepancy is the pool-label defect above; no model answer was changed to fit it.

## Replacement after exclusion of `gsm8k-train/108`

`gsm8k-train/1647` was independently drafted before gold was read. Its two paths separately compute Sarah's 55 and Ellie's 33 reflections, and the Conclusion combines them to 88. Post-draft pool gold is `88`; the row is marked `ready`. No correction was needed.

Post-review readability correction: `gsm8k-train/1810` Path 1 and Path 2 now express the same `80/5=16` and `60/2=30` calculations in plain text, avoiding malformed dollar-delimited spans. No answer, tag, number, or reasoning change.
