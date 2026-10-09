# Strict screen: Qwen thinking traces, batch A

Scope: 71 own Qwen3-0.6B `thinking` responses in `batch_a.jsonl`. No GPU, proxy, or experiment execution.

| Criterion | Count |
|---|---:|
| Input traces | 71 |
| Final answer matches pool gold | 71 / 71 |
| Traces with materially flawed or contradictory reasoning | 8 / 71 |
| Structurally suitable for plan-only two-Path wrapping | 6 / 71 |
| Rejected | 65 / 71 |

Accepted IDs: `gsm8k-train/1283`, `gsm8k-train/238`, `gsm8k-train/2909`, `gsm8k-train/3708`, `gsm8k-train/4774`, `gsm8k-train/6822`. Each already has two independent material calculations followed by a combination step; wrapping needs no changes to original words.

Most rejections have a single dependency chain. Four have three or more natural components, so forcing two branches would be arbitrary. Eight contain a material error, contradiction, or unsupported detour in their `<think>` text.

`screen_a.jsonl` contains a source-order decision for every input ID.
