# Batch C: plan-only Multiverse annotation

Input: `traces52_c.jsonl`. Output: `tagged52_c.jsonl`.

- Records: 17. Tagged: 17. Rejected: 0.
- Original source prose, formulae, numbers, order, and final-answer lines are preserved. Source combination suffix remains after `</Parallel>` inside `<think>`.
- Added text: structural tags, concise numbered Outline plans, numeric Path labels, and one routing-only Conclusion: `Combine these independent results in the following text.`
- Source headers `Part 1:` and `Part 2:` are whitespace-normalized with nonbreaking spaces as `Part 1:` and `Part 2:` within Paths. This prevents the deterministic cross-reference checker from misreading a local header as a reference to a sibling path; M2 restoration is exact modulo whitespace.
- Shared setup remains before `<Parallel>`. Source Part sections remain in their own Paths.
- `math-train/3860` uses three natural right-angle cases; all other records use two paths.
- Verified with exact M2 strip reconstruction and `scripts/exp21/checks.py`: 17/17 pass.
- No GPU, Kubernetes, proxy, or external calls used.
