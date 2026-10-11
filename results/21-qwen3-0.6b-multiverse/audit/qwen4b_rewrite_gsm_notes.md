# Qwen 4B GSM rewrite proposals

Status: author-written CPU-only candidates for later review. Not mixed into SFT or training.

## Selection

- 8 GSM8K rows from `data/qwen4b_teacher_graded320.jsonl`.
- Every source row has `clean=true`, `correct=true`, and `truncated=false`.
- Excluded all 36 IDs in `audit/qwen4b_teacher_conversion_accepted.jsonl`.
- Excluded the union of historical positive IDs from `pair_final_m1.jsonl`, `more_m1_matched180.jsonl`, `teacher_trajectory_candidates.jsonl`, and `onpolicy_agent_authored_accepted78.jsonl`.
- Chose cases where two meaningful quantities can be calculated from the question without a sibling Path result.

## Author checks

Each response has one `<think>` wrapper, one numbered `<Parallel>` block inside it, two self-contained Paths, and a Conclusion. Its external line is exactly `Final Answer: <gold>`. Manual arithmetic: 4051: $35 + $20 = $55; $55 / 5 = 11$. 5845: $80 + $60 = 140$. 2065: $63 - 17 = 46$. 144: $25 - 17 = 8$. 1093: $360 + $90 = 450$. 61: $1000 - 200 - 400 - 200 = 200$. 6735: $4 + 8 + 4 = 16$. 1046: $18 - 6 = 12$.

Focused parser and provenance validation follows file creation.
