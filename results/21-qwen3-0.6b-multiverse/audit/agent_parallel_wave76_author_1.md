# Agent Parallel wave 76, batch 1

Scope: 25 rows from `data/agent_parallel_wave76_input_1.jsonl`. Every condition was solved before reading `data/pool.jsonl`. The complete pre-gold record is `data/agent_parallel_wave76_draft_1.jsonl`; `data/agent_parallel_wave76_final_1.jsonl` records post-check statuses.

## Method

For each non-skipped item, both paths derive distinct useful quantities from the condition and the Conclusion combines them. No path cites a sibling result. The first independent pass created all 25 draft rows before gold was read. Afterward, final answers were compared to `data/pool.jsonl`; mismatches were rederived from the condition rather than changed to match a reference.

## Post-gold changes

- `math-train/6129`: draft answer 68 was wrong. Recomputed the middle polygon as a `3 by 1` strip plus a `1 by 2` strip, area 5; together with the unit square it is 6. The largest piece is `5 by 1` plus `1 by 4`, area 9. Shading is `(6 + 9) / 25 = 60%`. Final answer corrected to 60, matching gold.
- `gsm8k-train/7364`: draft answer 5 differs from gold 4. The condition gives 12 study hours, 2 hours of hourly breaks, and 1 hour of snack and lunch breaks per day. With a four-hour daily limit, four days provide 16 hours but require 18; five days provide 20 hours and require 19. The final row remains `gold_conflict` with answer 5. It is excluded from ready rows pending reference adjudication.

## Counts and checks

| Status | Count | Meaning |
|---|---:|---|
| `ready` | 23 | Correct final answer after gold comparison, including equivalent `5/11` notation for `math-train/2908`. |
| `skip` | 1 | `math-train/4120`; its nested continued-fraction equation has one coupled derivation, so two independent paths would be artificial. |
| `gold_conflict` | 1 | `gsm8k-train/7364`; condition-consistent answer conflicts with pool gold. |

Validation: draft and final JSONL each have 25 unique input IDs and the required four fields. Every non-skipped row has one `<think>` block containing two `<Outline>` elements, two `<Path>` elements, one `<Conclusion>`, and a `Final Answer:` line. No GPU, Kubernetes, proxy, or live-process operation was used.

## Post-review independence correction

`math-train/6630` Path 2 previously used `S=3` derived by Path 1 before deriving `T=1`, so it was not fully sibling-independent. The final row now independently derives `S=3` from `9:S=3`, then derives `T=1` from `S:T=3`. No other number, conclusion, final answer, or draft row changed.
