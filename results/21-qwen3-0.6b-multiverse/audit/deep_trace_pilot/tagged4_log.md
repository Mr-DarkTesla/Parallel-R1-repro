# Deep trace plan-only pilot: four examples

Source: `traces_raw20.jsonl`; selected IDs only. Each response contains one block inside `<think>`. Outline and Conclusion add a plan/synthesis; original reasoning inside Paths and outside block preserves exact order and wording. No GPU, Kubernetes, or proxy used.

- `math-train/1491`: paths independent; original reasoning and final answer restored exactly after removing inserted block; tags balanced, block inside `<think>`.
- `math-train/6266`: paths independent; original reasoning and final answer restored exactly after removing inserted block; tags balanced, block inside `<think>`.
- `math-train/5580`: paths independent; original reasoning and final answer restored exactly after removing inserted block; tags balanced, block inside `<think>`.
- `math-train/7323`: paths independent; original reasoning and final answer restored exactly after removing inserted block; tags balanced, block inside `<think>`.

Syntax and source restoration checked programmatically for all four. Independent reasoning read manually: numerator/denominator; score totals for two groups; areas of two disks; fixed-row compatibility/third-row orthogonality. Third-row equations use fixed row values but do not depend on result of the fixed-row compatibility check.

Verified with `scripts/exp21/mv_format.py::parse`: all four blocks valid and numbered, each with two paths; no structural tags after `</think>`. Original response restored exactly by removing the inserted block and replacing it with its two original path segments and original separator. Answers manually checked: 15/4, 73%, 64π, (-2,-1).
