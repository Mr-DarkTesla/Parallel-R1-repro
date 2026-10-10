# Conclusion fix audit: 16 Qwen3-0.6B traces

Selection is exact intersection of `agent_{a,b,c}/tagged.jsonl` and `independent_review/verdicts.jsonl`; A/B/C = 4/6/6. Existing verdicts identified rows only. CPU-only.

For each accepted row, moved a contiguous existing synthesis span into `<Conclusion>` unchanged and removed only the added imperative placeholder. Removing added Goal content, Path numbering, and structural tags reproduces original input response exactly. Each corrected row has one numbered grammatical block wholly inside `<think>`; Path calculations remain unchanged. Gold checked only after source-restoration and structure checks.

## Result

Accepted 14/16; rejected 2/16. All accepted final answers match gold. Row evidence is in `decisions.jsonl`.

Rejected `math-train/1132` and `math-train/7395`: original text contains false mathematical claims; repair would require rewriting.

`math-train/1128` and `math-train/1961` use independent alternative derivations of one result rather than separate quantities. Included under this task’s explicit independent-Path condition; prior review notes they fall outside the narrower current prompt. `math-train/1961` has a boxed correct answer after `</think>` without a `Final Answer:` label; correctness check recognizes it.

No GPU, Kubernetes, proxy, or SFT use.
