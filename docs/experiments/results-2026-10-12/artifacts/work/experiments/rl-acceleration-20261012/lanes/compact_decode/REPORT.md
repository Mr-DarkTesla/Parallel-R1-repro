# Compact finished-row decoding GPU proof

Passed on mpiworker-0 of the existing 32-GPU job, using all eight assigned GPUs. Two actual FP32 Adam/Zero1 updates (51,52), fixed 8 prompts × 4 responses = 32. Every rank updated backbone weights and passed unchanged replay thresholds; all eight children exited 0 and GPU inventory was empty.

Checkpoint: `${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf`. Trainable parameters: 4,022,468,096. Reward SHA256: `b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce`. No changes to 4096 response / 768 path / 16384 context budgets or fullwidth8.

## Matched frozen quality and accounting

- Clean16: exact sampled tokens/output/loss masks 16/16; correctness 13/16 for both. Maximum old-logprob difference 1.71661377e-05.
- Actual step51 train batch: exact output/raw sampled actions/seeds/masks/widths/stats/physicalF/reward components 32/32 against laneA baseline.
- Resident Adam fixtures: 160 cases across 8 ranks, widths 2/3/4/6/8, four repetitions each, uneven lengths. One subgroup per complete fork, GPU forward counter equals max branch raw sampled length; sampled terminal tokens count and forced tokens do not. Max fixture replay drift 0.000566482544; paired baseline/compact drift 4.19616699e-05.
- Natural clean16 fork slots 21032→12613; physical fork F 5258 unchanged. Full-trajectory physical F 16746 vs raw sampled token work 24101.

## Timing and memory

- Matched clean16 elapsed sum across per-GPU sequential examples: 702.794s baseline→659.552s compact, 1.0656×, 6.153% time reduction. This sum is not distributed wall clock.
- Compact per-GPU average throughput: 0.024259 responses/s; 36.541 sampled tokens/s.
- Resident fixture summed baseline 1608.103s→compact 1539.601s; median paired speedup 1.0407×. Kernel-row-slot reduction 26.01%.
- Step 52 pre-fixture critical update phase time 257.129s, including rollout+replay/backward/collectives+optimizer; the JSON contains all rank phase timings. Step 51 total duration is contaminated by unsynchronized pilot completion; step 52 total includes fixtures.
- Peak allocated GPU memory 53,213,193,728 bytes (49.559 GiB reported in training metrics). Max training replay drift 0.000120162964. No OOM.

## Change and limits

Within each call, remove completed rows using explicit KV cache batch selection while preserving logical branch ID→generator→result ordering, masks and positions. All remaining live rows share one forward. Transfer sampled IDs and logprobs twice per complete fork step instead of twice per row. No cross-phase cache or cross-trajectory cohorts.

Baseline always preceded compact in each pair; timing is descriptive, not randomized or a confidence interval. Two optimizer updates only. Four fixture repetitions are independent calls; clean16 contains one natural width 4 fork per trace. Explicit multiple-fork trajectory reuse and sibling perturbation are separate lane D coverage. Removed dummy slots do not imply proportional wall-time improvement. Clean16 exact-normalized problem overlap with frozen MATH500 was 0; source manifest marks group-disjoint selection and excludes benchmark selection but does not prove absence of semantic paraphrases.

Source/config and external input hashes are bound in `proof.json`; detailed paired traces live in `smoke/paired-pilot-rank-*.json`, full train parity in `training-paired-step51.json`, rank metrics and resident fixtures in `smoke/`. `patch.diff` contains only the mergeable decoder change.

Additional actual step 52 comparison: all 32 responses again match baseline exactly for output/raw sampled IDs/masks/widths/stats/F/reward components after each arm performed its step 51 Adam update. Baseline and compact are both correct on 30/32 training responses. Baseline critical rollout 185.293s vs compact 175.481s (1.0559x). Baseline pre-cleanup runner 267.165s vs compact pre-fixture optimizer boundary 257.129s (1.0390x); timer boundaries differ by small backbone/check overhead, so this is a descriptive update comparison. Baseline selected step 52 phase rows are snapshotted and canonically hashed in baseline-phase-step52.json; live append-only phase files are not treated as immutable whole files.
