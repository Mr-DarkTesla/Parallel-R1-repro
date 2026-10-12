# Independent Unseen-S2 batch32 — 7 October 2026

## PAUSED BY USER — do not resume automatically

All owned training processes and export300 watcher stopped. All8 GPUs freed. Existing heartbeat paused. Preserve checkpoints/logs and resume only on a new direct user request. Details in user-stop.json.

## Interpretation correction after user review — 14:22 MSK

Historical quality/walltime comparison is confounded:256 initially~171s before117–125s aftertuning, probes/restart/validation10;32 inheritedoptimizations andvalidation50. Batch32 superiority with equal runtime is NOT established. Treat current S2batch32 as exploratory; do not claimoptimalbatch fromthesegraphs. User has not asked tostop/switch thisrun. RewardauditS1: trainpositive32 first20=4.32%,last30=5.89%;~75.5%groupszeroadvantage,~7.8informativeprompts/32. Sameperiod256last30=9.27%,~78informative/256. NegativeS1reward maps to accuracy via(R+1)/2; DAPOtrain differsfromMATHvalidation.

This is the user-authorized next run after completed Unseen-S1 batch32. Read live launched.json/status.json before acting; no duplicate controllers/export watchers. Work ONLY inside ${PROJECT_ROOT} on sirius. Never global pkill/ray stop, foreign processes or artificial GPU load.

S1 exps/rl-unseen-s1-bs32-20261007 completed300, exit0 at14:12:28MSK, ~3h11m from11:01:22. Final MATH36.7089%, AMC16.5625%; SFT25.9494%/8.28125%. HF-step300 verified finite weights, six control tokens and finite CPU forward,1518118104bytes. Full source checkpoint300 retained. Earlier S1batch256 endedpartial280 (49.37%/26.875%) after much longer training; no300 claim. Original S2partial20 preserved and not resumed.

Batch choice in batch-decision.json. User criterion: quality at equal actual wall time, not seconds/step or equal steps; supersedes earlier3pp allowance. At2h13m32 hasMATH+3.48pp/AMCequal; at2h36m32 hasMATH+2.85pp/AMC+4.69pp relative to historical256 latest available validation. Later32validations200/250/300 remain above old256step50 within3h11m. Thus32 chosen provisionally for observed quality/time; not a statistically proven causal batch effect (different runtime tuning, single seeds, sparse validation). Comparison graphs/data in S1/charts, wall-quality.json; do not compare300vs280 as equal compute.

Recipe: original Unseen-SFT (not S1 checkpoint), authorS2 accuracy_parallel_interv_reward8accuracy-only/2accuracy+parallel;300steps,8GPU,batch32,n8,mini16,micro2,token-mean,LR1e-6,cliphigh0.28. NO_SHARD+defer_gradient_sync+skip_zero_advantage_microbatches from validated b656ead snapshot. Original microbatch group normalization retained; last microbatch always executes forsync; no skipped optimizer updates. Packing previously failed13.07%gradient parity, never use. Original Unseen masks/repeatedpositions/runtime-tag loss unchanged.

Exact decodegraphs capture threshold64, max_num_seqs64, fusedTriton, sorted original pairs/logprob rows. Validation accuracy-only every50 on1916rows; save10retain3; noinitialvalidation. Fresh launch has coldcache; wait3–5completed steps forETA and include allvalidation/save/export costs. Target2h/max3h is an aspiration, NOT measured or guaranteed. S1needed3h11 including earlierfrequentvalidation/restart; S2 mayhave different response lengths.

run.py preflight validates source/dataSHA, controltokens and resolvedconfig. export_checkpoint.py singleCPUwatcher writes export-step300.json and atomically renames verified exports/hf-step300. Completion requires300, full model/optimizer/extra/data checkpoint, successfulHF andfilechecks. Restore only this S2 fromlatestfullcheckpoint onconfirmed failure. Controller launching/running is not proof of optimizer updates. Monitor.py/driver.log/telemetry/rollouts/validation carry metrics. NFS tempcleanup OSError16 aftervalidation was nonfatal inS1; inspectfollowingprogress before restarting.

Existing heartbeat rl-unseen-checkpoint-10-00 should nowmonitor THIS run and pause onlyafterverifiedS2complete300+HF. Do not start anotherS2 or resumeoldS2. Notifyonlyfailure,meaningfulETAchange,actionneeded,orverifiedHF.

Launch confirmed14:17MSK: controller667589, driver667811, export300watcher667590. Fresh resume_checkpoint null. Preflight source/data/tokenizer/configpassed;300steps,batch32,mini16,NO_SHARD,skipzero,clip.28,val50,save10. Driver initialized, no completedoptimizerstepverifiedyet.
