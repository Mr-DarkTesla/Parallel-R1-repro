# Independent Unseen-S2, 7 October 2026

## Active tuning, 7 October ~10:39 MSK (overrides capacity/PIDs below)

User requested at least another2x speedup at unchanged budget and asked about the early fast Seen run. No2x additional gain is established. Current S2 capacity64 ordinary steps7–9 ~103–105s; initial warm steps2–6 ~116s. Eight-GPU bounded passive profile completed and automatically restored all methods: forward14.4–15.1s of20.2–20.9s spans, sampling1.13–1.18s, no new graph captures. Per GPU~130k decode tokens plus190–250k prefill tokens. All almost always at64 sequences. Evidence rollout-profile-rank-*.json.

Full S2 checkpoint10 and CPU HF-step10 verified (finite weights, six tags, CPU forward;1,518,118,087bytes). Validation10: MATH27.85%, AMC11.875%, AIME24 .625%, AIME25 .417%; only early signal, no claim of significant gain. S2 parallel ratio93.7%. Save10 took34.94s and validation133.90s, so prior123.44s combined overhead was low; actual168.84s for ETA.

One resize watcher PID603658 (`resize_rollout.py`; verify live identity) waits for **complete checkpoint20 AND validation20 logged**, then stops only descendants of controller583032, archives capacity64 logs/config, resumes **same S2 at20** with inference `max_num_seqs=256`. Original training batch256/n8/mini128/micro2/reward/dataset/300steps remain. Export300 watcher563147 is outside its tree and retained; do not duplicate. Read `resize.json` and `resize-armed.json`; while waiting, original run continues. Do not run the switch or first-step recovery scripts again. Check `status.json` for new controller after resize. Larger capacity is an unproven throughput trial; exclude cold step21 and compare warm steps plus validation. If it fails, restore only this S2 from latest complete checkpoint with known capacity64; preserve logs and report. Do not resurrect S1.


User explicitly chose a fresh S2 from Unseen-SFT, preserving S1 separately; requested maximum acceleration, targeting x5 at unchanged training budget. x5 is **not** measured or promised.

## Live verification at10:18MSK

S2 completed3 optimizer steps successfully; all8 GPU worker PIDs588597,588865,588866,588867,588868,588869,588870,588871 verified. Current controller583032 and driver583253. No active errors or non-finite metrics. Step1 cold223.13s (gen189.05, logprob10.37, update18.18); steps2/3 total118.39/112.63s, gen88.95/82.59, logprob10.00/9.50, update14.05/15.10. Skipped70–71% zero microbatches on steps2/3. Gradient norm0.124/0.141; rewards-0.923/-0.912; entropy0.665/0.706. Only the first accuracy-only part of S2 has run; first parallel-bonus phase is steps9/10.

Preliminary ETA from steps2/3 ~20:52MSK (~10.6h remaining); validation/save overhead still estimated from S1, so re-estimate after S2 step10. Ordinary speed vs original170.91s ~1.48x; early S1 steps2/3 averaged194.24s vs S2 115.51s (~1.68x on different trajectories). **No end-to-end x5 claim.**

Export300 watcher563147 retained; an independent single CPU export10 watcher602800 will validate the first S2 checkpoint/HF (read export-step10.json). Do not duplicate either. Checkpoint10 is NOT full300. No S2 checkpoint was durable yet at this observation. `observation-first-steps.json` is the saved measurement.

## Scope and switch

Only work on sirius inside `${PROJECT_ROOT}` (ROOT). Connect `ssh sirius`. Do not print/transfer SSH keys, operate outside ROOT, kill foreign processes, run global pkill/ray stop, or create fake GPU load.

RUN=`ROOT/exps/rl-unseen-s2-20261007`; OLD=`ROOT/exps/rl-unseen-s1-20261007-seq128`.
Switch completed at09:53MSK. S2 controller PID563146, driver563368, export300 watcher563147. S1 full checkpoint280 and HF280 are verified. Check live identity before actions. `switch.py` PID562778 performed this sequence: it waited for OLD durable280 and validation280, performs CPU HF-export280 and validates weights/tokens/CPU forward, then stops only the recorded descendants of S1 controller534450 and cancels the specific obsolete S1 export300 watcher534399. It launched fresh S2 and a separate CPU export300 watcher. Their PIDs are in `switch.json`. Do not duplicate them. If switch fails, inspect its error before retrying. S1 checkpoint280 is a preserved **partial** S1 run, not completed300. Deadline export270 also exists separately. Never resume S1 automatically after switching.

## Experiment

- Starting checkpoint: `ROOT/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final`.
- No S1 weights, optimizer or step offset. New S2 steps1..300.
- Author reward `accuracy_parallel_interv_reward`: steps1..8 of each10-cycle accuracy +1/-1; steps9/10 correct well-formed parallel +1.2, correct plain +1, otherwise -1. Reward code unchanged.
- All17917 train questions/order/metadata/labels match S1 except reward_method; `data-check.json` verifies every row. Validation1916 rows stays accuracy-only, not S2 reward.
- 8A100, batch256, n8, mini128, micro2, token-mean, LR1e-6; author S2 clip high0.28. Total300. Original author structured actor, path masks, repeatedpositions and runtime-tag loss retained.
- Save/validation every10, retain3. No budget/dataset/response-length reduction for speed.
- Frozen `code`, SHA manifest, resolved-config.yaml, command.json, driver.log. Commits3b270fa (author batch defaults/reward regression), c3a9b34 (replication/zero-gradient skip).

## Performance changes and limits

Already validated optimizations carried forward: fused Triton head, original microbatch-pair ordering, restored log-prob row order, deferred FSDP gradient sync, exact-shape decode graphs with capture minimum4 uses. max_num_seqs64; no untested128/256 claims. Gradient checkpointing already off.

New FSDP1 `NO_SHARD` stores a full small model/optimizer on each GPU and synchronizes gradients. `skip_zero_advantage_microbatches=true` only skips completely zero-advantage microbatches with zero entropy coefficient/no KL/vanilla PPO. Original gradient accumulation denominator stays unchanged; final microbatch ALWAYS runs on every rank; every Adam optimizer update remains, even all-zero minibatches. It is invalid with sharded parameters. `actor/ppo_kl_active_microbatches` explicitly excludes skipped work; full old-log-prob/entropy calculation is unchanged. `perf/skipped_zero_advantage_microbatch_fraction` records actual savings.

Matched no-optimizer-update probes in live S1 workers, 32 real rows/rank:
- Replication alone:5.785s→5.274s, x1.10; gradient relative L2 1.258%.
- Replication+zero skip:5.367s→1.630s, x3.29 for this UPDATE SUBSET; gradient relative L2 1.224%, all8 ranks accepted below2%; 62.5–81.25% original microbatches skipped in this sample. CPU tests also verify gradients, two Adam updates including all-zero second minibatch, and final-sync behavior.
- These are late-S1 batches, not full-step or S2 speedups. Probe overhead affected S1 steps265/278; exclude them from ETA baselines.
- Inference rank0 timing:512 decode forwards,32758 tokens,3.732s wall,2.451s GPU,0.068s Python-forward. Does not include full rollout tails/prefill; cannot infer full-run ETA from this alone.
- Rejected forward packing from earlier S1 changed gradients13.07%; never enable it.

Measure at least3 completed ordinary S2 steps, split gen/logprob/update and include validation/save in ETA. NO_SHARD increases checkpoint storage and save time; validate first durable checkpoint and CPU HF export before reporting success. No x5 achievement without full-step evidence. Current S2 ETA is pending actual live steps.

Heartbeat `rl-unseen-checkpoint-10-00` was updated to S2. Stay quiet on unchanged healthy status. Report failure, important ETA change or verified completion. Stop monitoring only after full300 and verified HF export, then pause heartbeat.

## First-attempt integration fix

At10:00MSK the first attempt failed AFTER generation/log-prob but BEFORE any optimizer update: `fsdp_workers.compute_log_prob` unconditionally called private root `reshard(True)`, invalid for NO_SHARD. Commitb656ead guards all three forced root-reshard sites using `handle.uses_sharded_strategy` and handles empty roots. Three selector/cleanup tests pass. Seven actor CPU tests pass (one CUDA-only test skipped); prior real8GPU probes remain the numerical evidence.

`recover_first_step.py` checked exact old GPU PIDs and process start ticks/cwd, stopped only own orphan workers, preserved all first-attempt logs/results/config under `failed-attempt1`, updated the code/hash manifest, and restarted from the same Unseen-SFT with no lost optimizer updates. New controller583032, driver583253 at10:06MSK. Export300 watcher563147 was retained, not duplicated. Read `recovery.json` and live status; old switch PIDs are historical.

## What x5 would require

Original ordinary S1 baseline170.91s implies34.2s/step for x5; relative to recent125s the target is25s. Recent generation alone was~60s. Even eliminating actor/log-prob entirely cannot achieve x5 while generation stays unchanged. The proven update-subset x3.29 must NOT be presented as end-to-end x3.29. The remaining high-impact investigation is rollout batching/utilization and serial branch tails; a64→128/256 concurrency claim needs warm, matched generation measurements, not cold graph-capture timings. Earlier128 and KV-affinity trials had no established sustained benefit. Quantization, shorter responses, fewer samples, different data/loss and unverified packing are not acceptable substitutes for the requested speedup.
