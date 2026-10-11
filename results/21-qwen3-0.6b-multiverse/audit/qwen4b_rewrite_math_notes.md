# Qwen 4B MATH rewrite proposals

- Source: `results/21-qwen3-0.6b-multiverse/data/qwen4b_teacher_graded320.jsonl`.
- Selection: 25 MATH rows where `correct`, `clean`, and `not truncated` are true.
- Exclusions: every ID found in existing audit files whose path contains `accepted` or `positive`, including `qwen4b_teacher_conversion_accepted.jsonl`; no proposal ID intersects that set.
- Each row preserves the full teacher output in `source_output`. The external `Final Answer:` is copied verbatim from the final such field in its source output.
- Structural check: each response has one `<think>`, one nested `<Parallel>`, two `<Path>` blocks, and one `<Conclusion>`.
- Mathematical review: manually recomputed all 25 conclusions; paths use either independent quantities, independent cases, or a second substantive derivation/check.

## Validation result

- Parsed 25 JSONL rows; all IDs are unique.
- Rebuilt the prior-positive ID set from the current audit directory: 415 IDs; intersection with proposals: 0.
- Confirmed the source filters, six-field schema, tag counts, nesting, and verbatim final-answer suffix for every row.
