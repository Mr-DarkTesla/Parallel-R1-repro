# 14-instruct4b-filtered: arm of the exp13 SFT matrix

Training code and recipe are exactly those of `exp/13-instruct4b-control` at `ab090b1`
(`results/13-instruct4b-control/recipe.md`, `scripts/instruct4b/sft.sh`). This branch only changes the data arm:

| | value |
|---|---|
| run | `/work/runs/14-filtered` on pod B (`vcharkin-exp-vm-b-0`, GPUs 0,1 via `scripts/instruct4b/gpu_pair.sh`) |
| train | `/work/bench_data/instruct4b/sft/filtered.parquet`, 4248 rows |
| val | `dev_untouched.parquet`, 296 rows (dev row 179 / source 224 excluded) |
| init | `/work/assets/models/Qwen3-4B-instruct-add-special-token` (same as 13, not re-prepared) |
| updates / batch / lr | 64 / global 64 / 1e-5, warmup 6, cosine to 0 |
| micro batch per GPU | same as the accepted 13-control run (recorded in `results/recipe.txt` of the run) |
| template | native Qwen3, `enable_thinking=False`; max_length 4096; FSDP2; gradient checkpointing |
| data order | `DistributedSampler` seed 0; `trainer.seed` is not used, so no separate training seeds are claimed |

Arm: control_full minus confident answer-first rows (answer already stated before a parallel block that repeats it; v6 filter, all blocks): 1310 rows removed (218 first block, 1092 later blocks).

Filter v6 is frozen. random_control is a same-size sample of control_full matched on 54 joint strata (length decile x
blocks 4+ x paths 6+); target tokens filtered 1732780 vs random_control 1737281 (+0.26%). filtered and random_control share
3303 of 4248 rows. Processed rows per update: `results/rows.csv` of the run (4096 rows, one partial epoch).
