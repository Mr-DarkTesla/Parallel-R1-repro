# 20-instruct4b-tagfix: 14-filtered + learning rate of the new tag rows

Control arm of cycle 2: exactly the 14-filtered SFT (`results/14-instruct4b-filtered/recipe.md`) plus one change,
`optim.tag_lr_mult=100` (commit "sft: optional lr multiplier for the embedding rows of the new tag tokens").

| | value |
|---|---|
| run | `/work/runs/20-tagfix` on pod B, GPUs 0,1 via `scripts/instruct4b/gpu_pair.sh`, entry `scripts/run_experiment.sh 20-tagfix` |
| train / val | `filtered.parquet` 4248 rows / `dev_untouched.parquet` 296 rows (as 14f) |
| init | `/work/assets/models/Qwen3-4B-instruct-add-special-token` (as 14f) |
| updates / batch / lr | 64 / global 64 / 1e-5, warmup 6, cosine to 0; micro batch 2 per GPU (as 14f) |
| template, length | native Qwen3 `enable_thinking=False`, max_length 4096, FSDP2, gradient checkpointing (as 14f) |
| data order | `DistributedSampler` seed 0 (as 14f: the same 4096 rows in the same updates) |
| **change** | rows 151669..151674 (`<Path>` ... `</Summary>`) of the tied embedding: lr x100 (peak 1e-3); everything else unchanged |

Why: teacher-forced on SFT rows, 13/14f/15r pick the right tag (top-1 0.95, p(right | some tag) 0.95, like the authors' SFT)
but leave ~10% of the probability on the text pieces `>`, `</`, `<` the tags were initialised from (authors' SFT: 0.000);
at T=1 about half of the sampled blocks break. With lr 1e-5 for 64 updates AdamW moves each row element by at most the sum of
the lr schedule, ~3e-4, so the tag rows stay at their init (measured: moved ~2% of their norm). Multiplier from a CPU proxy (only the 6 rows trained on cached
hidden states with this optimizer and schedule): held-out p(right tag) grows and saturates (from P's states x30 0.70, x100 0.81,
x300 0.86; from 14f's x100 0.93 = x300), x1000 overshoots (worse tag NLL, row norms 1.4-2.8); x100 keeps the row norms in the range of
ordinary tokens. Proxy limits: hidden states frozen, output side only; it predicts slightly more tag mass at non-tag positions
(measured in the evaluation of 20). Independent review: ACCEPT (tagfix_review/verdict.md). Evidence: tagfix/FINDING-diagnosis.md and tagfix/ in the project state folder.

Checks after the SFT (the fix must have applied, otherwise the arm does not count): train.log prints `tag_lr_mult=100.0` with 0 tag rows on
rank 0 and 6 on rank 1; results/recipe.txt has `overrides=optim.tag_lr_mult=100`; results/rows.csv equals 14f's; exported tag rows moved
from P by ~0.2-0.5 L2 (14f: 0.011-0.013), other rows by the same order as in 14f.
