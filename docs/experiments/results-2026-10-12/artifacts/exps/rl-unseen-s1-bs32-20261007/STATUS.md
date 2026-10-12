# Unseen-S1, batch32 — 7 October 2026

## COMPLETE — 7 October, 14:12:28 MSK

300steps completed, exit0; full checkpoint300 verified25nonemptyfiles. HF-step300 complete1518118104bytes; finiteweights, sixcontroltokens and CPUforward verified. Total controller wall3h11m07s from11:01:22. FinalMATH36.7089%,AMC16.5625%; initial25.9494%/8.28125%. Parallelratio4.296875% at300. Finalgraphs with oldbatch256 overlay: charts/batch-comparison.png and training-comparison.png; rawmetrics.json holds bothlogs andtimecomparison. Target2h/max3h missed, do notclaimotherwise.

Next user-authorized independentS2 launched in exps/rl-unseen-s2-bs32-20261007 after choosingbatch32 via observedquality/walltime; see itsSTATUS/batch-decision.json. Controller667589,driver667811,export300watcher667590; liveinitialization stillpendingfirstupdates at14:17MSK. ExistingheartbeatnowtargetsS2; do notlaunchduplicateorresumeS1. Older sections belowarehistorical.

## Verified resumed progress — 7 October, 12:52 MSK

145/300 completed, full checkpoint140. Controller643751/driver643992 alive, restored globalstep90 confirmed. Last5 ordinary steps141–145 mean26.83s; gen18–21s, actor5.0–5.65s. No NaN/Inf or runtime errors. Current ETA14:11MSK including4 remaining validations,16saves and40s export allowance, ~3h10 from initial11:01 start. This does NOT meet2h and remains above3h; do not claim target achieved. Validation50/save10 confirmed in active manifest. Initial validation disabled.

One bounded passive512-call profile on rank0 armed by profile_rollout.py; inspect rollout-profile-rank-0.json. No extra samples/updates. Profile self-removes after512 calls; do not reinstall blindly. Other7workers untouched. compare_wall_quality.py now writes wall-quality.json based on validation artifact timestamps minus original launch, including startup/downtime; no interpolated scores. At~42min,32 MATH24.37%/AMC11.41% vs25629.11%/9.69%. At~73min,32 lastavailable27.22%/11.09% vs25625.63%/10.47%. Mixed results, no established superiority32; do not select32 for S2 merely onstep speed. Recompute with final validations and examine adjacent points.

## Latest decisions and verified transition — 7 October, 12:18 MSK

This section supersedes older launch notes below. User requires all300 RL steps, target2h (earlier maximum3h), and after S1 an independent Unseen-S2 from the original SFT. Choose S2 batch by better quality at equal wall time; if32 is not better, use256. Prior3pp non-inferiority allowance is superseded and must not justify choosing32. Never continue S2 from S1 or the paused old S2 checkpoint20.

Current S1 completed90 including full validation. At12:15 MSK retune_after90.py (watcher640423) stopped only the owned619780 tree after verifying full model/optimizer/RNG/data.pt checkpoint90, archived logs/config to validation-every10/, and resumed90 with controller643751/driver643992. Live identities must be rechecked. retune.json confirms restarted and preflight passed; resumed optimizer steps still pending at this observation. Export300 watcher619781 retained, no duplicate. Old retune_after20.py is UNARMED and obsolete; never run it.

Actual runtime changes: exact CUDA graph capture threshold4→64 applied11:24MSK retaining existing graphcache. Recent ordinary steps17–89 ~26s (generation~18s, actor~6s), versus recent55s before change; trajectories and cachewarmup confound causal attribution. After resume newcache must warm. Validation now every50, full1916examples; save every10 retain3 unchanged. Initial validation remains disabled. All300 training steps, batch32,n8,mini16,micro2,S1 objective,FULL_SHARD and original Unseen semantics unchanged. NO_SHARD and skipzero remain disabled; checkpointconversion not validated.

Before resume ETA with validation10 was14:34MSK, ~3h33 from11:01 start. With validation50 and old26s step, expected around14:00 including resume, but requires new measurements. Two-hour total deadline13:01MSK is NOT supported by measured speed. monitor.py now independently accounts for test50/save10, startup remains an explicit uncertainty until completed steps.

Validation90: MATH316 mean@1=27.53%, AMC23 mean@16=13.4375%. Baseline SFT25.95%/8.28%. Batch32 does not yet establish better quality/time than256. Around63min of loggedcycles,32step80 gives27.22%/11.09%;256step20 at64.7min gives25.63%/10.47%. Adjacent32steps70/90 fluctuate26.90–27.53%/12.50–13.44%. These are preliminary logged-cycle durations, omit startup/restarts, and hardware configs differ; not a matched wall-time superiority result.

Existing heartbeat rl-unseen-checkpoint-10-00 updated for this S1 then new S2 queue and quality/time criterion; no separate S2 serverwatcher yet. Before S2 dispatch inspect all controllers/queue state and verify S1full300+HF. Old S1partial280+HF280 and old S2partial20+HF20 preserved. Do not duplicate jobs or exports. New S2 may use previously validated NO_SHARD/skipzero from freshSFT only. No packing. Stay insideROOT; no foreignprocess or globalstop.

## First live measurement (2026-10-07T08:13:56.579164+00:00)

Confirmed6/300 completed RL steps; all8 owned GPU PIDs625331,625598,625600,625601,625602,625603,625604,625605. Current driver620003/controller619780. No errors or NaN/Inf; nonzero finite gradients. Measured recent ordinary steps[3, 4, 5, 6]: mean63.64s, range57.49–66.89s. First step150.08s excluded. Graph warm-up still evolving; do not call this fully stabilized. Graph snapshots after completed3 showed359–416 captures/rank.

Comparison: original plotted late S1 batch256, ordinary241–258, averaged125.08s (generation61.79s); this run mean63.64s is1.97x shorter per step but **8x fewer answers per step**. Observed responses/s 4.02 vs16.37 on old batch256. Different trajectories/training stages and warmup: not a matched causal hardware benchmark. Current estimated completion 2026-10-07T17:42:19.881962+03:00 with validation/save still estimated from S1. Re-estimate after validation10 and further graph warming. First checkpoint/HF10 is still pending; no completed-run claim.


Latest explicit user instruction: repeat the **Unseen-S1 shown in the graphs** with batch32, not the early Seen run and not S2. Measure3–5 warm steps and compare speed. New independent300-step run from the original Unseen-SFT, on all8GPU.

## State at launch (~11:01 MSK)

ROOT=${PROJECT_ROOT}; ssh sirius. Only operate inside ROOT. RUN=ROOT/exps/rl-unseen-s1-bs32-20261007. Controller619780, CPU export300 watcher619781, CPU export10 watcher619782; verify identity live, current driver PID in status.json. launched.json records these. Preflight source/data SHA and resolved Hydra config passed. Real optimizer steps and warm speed are still pending; launcher submission is not a completed run. No duplicate controller/export watchers.

## Recipe and comparison

- Initial checkpoint: ROOT/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final.
- Fresh model initialization, no S1/S2 optimizer or trained weights reused, no resume.
- S1 accuracy_reward (+1 correct /-1 incorrect), cliphigh0.2, LR1e-6,300steps,8A100,n8,micro2,token-mean, original structured masks/repeatedpositions/runtime-tag loss.
- Train batch256→32. PPO mini128→16 proportionally preserves **two optimizer minibatch updates per RL step**. Thus256 answers per step instead of2048. User explicitly authorized this smaller batch; do not call it equal-work throughput speedup.
- FULL_SHARD and deferred gradient sync match plotted S1. New S2 NO_SHARD and zero-advantage skipping explicitly disabled so batch-size comparison does not mix those changes.
- Already validated late-S1 optimizations retained: fused Triton head, restored-order independent logprob sort, whole-original-microbatch-pair ordering, exact decodegraphs capture minimum4, effective inference capacity64.
- Same17917 DAPO train rows and1916 accuracy-only validation rows. Validation/save every10, retain3. Original SFT baseline already measured; no duplicate initial validation.
- Frozen code is b656ead with hashed manifest. Changes above are run overrides, not merged one-off experiment code.

## Previous runs preserved

- Original plotted Unseen-S1: exps/rl-unseen-s1-20261007-seq128, partial280 plus verified HF280. Do not resume automatically.
- Unseen-S2: exps/rl-unseen-s2-20261007, deliberately paused at complete checkpoint20 (validation20 complete) following user instruction. Its inference256 resume was stopped during initialization **before any step21 update**. Old controller607148/driver607369 are stopped and GPUs freed. S2 export300 watcher563147 cancelled. CPU export20 PID619392 started once; read its export-step20.json. HF10 already verified. Do not resume S2 or run resize watcher.

## Monitoring

Read monitor.py/status.json/driver.log/export-step10.json/export-step300.json; verify all8GPU process identities, finite metrics and completed optimizer steps. Exclude cold first step from timing, measure3–5 ordinary steps. Include validation/save overhead in full ETA; until first validation it is an estimate from S1. Report seconds/step and responses/second, keeping the8x difference in work explicit. Do not claim2x/5x equal-work acceleration from batch reduction.

On confirmed failure restore only this run from its latest full model/optimizer/extra_state/data.pt checkpoint, preserving logs. No global pkill/ray stop, foreign process changes, fake GPU load or rejected packing. Export watchers verify finite HF weights, all six tags and CPU forward before atomic rename. A step10 HF is intermediate, not a finished300-step run. After300 plus verified HF, schedule the independent S2 described above; do not pause until S2 completes.

Bounded rank0 profile completed and self-removed:512calls,4.50s span,3.41s GPU forward,0.12s logits,0.175s sampling;443exactgraphs,339deferredcalls in sample,1capture costing0.383s. Most sample time is model computation; no evidence of idle-wait bottleneck. Threshold64 trades capture cost for more eager calls. Do not infer2x from this single short profile; no new sampling/loss changes applied.
