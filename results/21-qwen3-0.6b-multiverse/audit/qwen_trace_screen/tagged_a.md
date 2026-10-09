# Plan-only Multiverse annotation: Qwen trace screen A

Initial strict screen selected six traces. Five pass final deterministic validation and are emitted: `gsm8k-train/238`, `gsm8k-train/2909`, `gsm8k-train/3708`, `gsm8k-train/4774`, and `gsm8k-train/6822`.

`gsm8k-train/1283` was rejected during annotation: its original Path 1 contains “from the first part”, which `checks.py` correctly classifies as a cross-path reference. Removing it would alter source text.

Each emitted response has one `<Parallel>` block inside its original `<think>`, after shared setup. Two original independent calculation spans appear in numbered Paths; original combination and final answer follow the block. Only routing tags, two outlines, and a routing-only conclusion were added.

Validation uses `scripts/exp21/checks.py` with gold answers from `results/21-qwen3-0.6b-multiverse/data/pool.jsonl`.
