Lane C: exact episode accounting with phase cohort batching

TERMINAL UPDATE: batched-replay completed all five positive updates51–55 on all8, resident20fixtures/all8 guards PASS, all8 exit0, final clean16 FP32 pilot12/16. Worker0 was verified empty and handed to D at terminal14:57:44UTC. Full report: batched-replay/REPORT.md. Final proof SHA e9feed1412fb1f5031e662af2fd80acfac5c6646669d8d93cb7ba65d6a3a5bdd, patch SHA e476b84b7a71388b221243048b0524b4bdd03a2df722ad810f3abcf7fd30e25c (apply--check PASS). No further C GPU jobs. Normal52–55 wall196.06/336.98/295.53/198.39s; warmed53 is only1.03986× vspriorU with different q/token/F work. No3× or strong same-work gain established; no checkpoint selection. Later launch snapshots below are historical.

LATEST STATUS 14:28 UTC: initial launch notes below are historical. Exact FP32 cohort32 is qualified1.179198× warmed full-update speedup. Cohort64 is not free: update51 wall518.960928 vs286.228991s,1.813× slower for2× responses, responses/s +10.3%, tokens/s +10.2%; naturalaggregate32 and45 crossprompt batches exercised. Step52 failed after NCCL ALLGATHER seq459 timeout600s and corrupted object-length requests112.98/165.28GiB. Primary initiating error is unproven; not established as model-capacity OOM. cohort64-failure.json/logSHA preserved.128 never launched, parent explicitly deprioritized it.

Unified stateless BF16q/TIS+C+Dabort completed3 positive Adam updates all8, resident widths2/3/4/6/8×4rounds PASS, all8 exit0. Strict actualaggregate cachedq replayEXACT0, FP32cached/fullp0max.000135422, fullmask/injected0/forkindivisibility/episodeF PASS. Immutable unified-bf16-tis/gpu-stateless-proof-53-1.json SHA17b6d496c7638ea8ce5b0254459f58c00dd51ffd263a648c174fbf28dd6f9706. Warm53 full350.411864/gen191.815580,32314sampledT, globalF11680/episodeF24136, correct19/32 (historicalFP32base23/32).51/52correct28/24. BF16q changed sampled policy/work; apparent1.741× versusFP32base is not a quality-preserving comparison. No3× result.

CURRENT GPU RUN batched-replay: assigned existing worker0 all8, controller6555, actors6558–6565, localport35835, launch14:24:27UTC. Staticconfig/source SHA receipt enforced; config514de21a1954b4e317d6727eeefcf10dd1dae024ac806efbf2121ab7da22a8fd. Reuses qualified BF16q/TIS+statelessCcohort+exactDabort, complete-context FP32 learner batching; no D6 KV bank. CPU fullparameterTISgradient4.40457e-20/logp0 PASS,9000-token singleton complete. A+D peer-review PASS. Admission max4rows/paddedcontext8192/paddedactionhead4096/actionratio2 only changes grouping, oversizedsingletons complete. Allcalls ownadv/immutableq/TISrho, summed4096×world/global32 normalization, finalgroupDDPsync. Everygroup independent scalarFP32p0 comparison at51; firstgroup+q/p0fixtures later, guards unchanged.5updates51–55 fixed32/caps4096/768/16384, residentproof51 then ordinary52–55. ActualGPUutil100% all8/memory55–56GiB; ≥2GPUpositiveAdam, fullshape/memory/numerics, pairedactualqwork and warmedwholewall pending. Worker1 releasedB afterU all8 exit0; no new allocation.

Status: GPU paired benchmark launched. Baseline update51 passed on all8 actors; no measured cohort speedup yet.
Measured baseline51: maximum full update333.669s; criticalrank2 generation235.196s, replay25.624s, backward72.105s, optimizer0.147s. All8 positive optimizer updates, maxreplaydrift0.000120163, rank0 backbone L2=2.77568e-5. 30/32 correct(train), actual episodeF exactly matches independent LaneA baseline (rank2=5644, rank1=1752). Snapshot nextupdate52 executing.
Node: existing RUN_5482aee87e mpiworker-1, GPUs 0..7.
Controller PID1576, torchrun PID1577, actor PIDs1580..1587 (startup snapshot).
Agent port29761, training store29861. Each later arm increments both.
Node-only rendezvous overrides are benchmark scaffolding excluded from patch.diff; generic production retains its own launch/rendezvous contract.

Implementation:
- One actor/model per GPU, four (or eight/sixteen) concurrent trajectory clients.
- Each full sibling request <=8 rows is indivisible; combined backend batch <=32.
- Canonical model FP32, SDPA, original per-row structure masks/repeated positions, per-row RNG retained.
- Episode F counts the union of steps where any real episode branch participates; inactive dummy slots never contribute.
- Global physical backend calls are separate and never used in R2 reward.
- Canonical native scorer runs on model owner thread, outside threaded rollout jobs.
- All4 samples/prompt remain grouped R-mean with original loss denominator4096 and original Zero1 Adam LR1e-6.

Experiments queued sequentially:
1 baseline32: 8 prompts*4 responses across8 actors, serial4/rank.
2 cohort32: identical32responses/update with same IDs/seeds/caps, aggregate32rows.
3 cohort64: 16 prompts*4, aggregate32rows. Explicitly changes prompt count.
4 cohort128: 32 prompts*4, aggregate32rows. Explicitly changes prompt count.
Each is five updates51..55 from checkpoint50; no validation/exports/full500.
Offset1200, seeds20261012, budgets4096/768/16384.
Resident widths2/3/4/6/8 x four rounds fixture runs at update52, so fullwall52 includes fixture overhead. Compare regular steady update53..55; generation/replay/backward/optimizer timings52 exclude fixture except totalwall. This limits strict updates2..5 evidence.

Proven CPU: instrumented per-backend step accounting32 rows, widths2/3/4/6/8 four rounds, individual episodeF112/132/152/172 vs sharedglobalF172. No splitter fallback.
Unproven: actual cross-prompt GPU likelihood parity, resident aggregate32 memory, two positive updates and clean exit, full-update speedup, quality preservation and 64/128 wall movement.
Boundary: scheduler batches complete phases; it does not admit new clients into an in-flight KV cache. True token-level continuous admission needs follow-up incremental KV engine. No cross-phase KV/replay change in this patch.
Telemetry backward includes DDP NCCL overlap; explicit_collectives records reward gather and parity guard, not independent NCCL kernel elapsed.

Failures preserved remote:
- failed-startup-1: missing canonical source directory; fixed before model load.
- failed-startup-2: TORCHELASTICFalse TCPStore collision with torchrun agent; separate training store fixed.

Artifacts: src/, patch.diff, source-seal.json(remote), local-source-seal.json, cpu-accounting-proof.json, configs, launch-status.json, controller-pid.json, *.log, exits.jsonl, each arm/{metrics*.jsonl,traces*.jsonl,status.json,result.json,resident-fixtures-rank-*.json}.

Final fixed32 qualification (2026-10-12):
Baseline and cohort32 completed5positive updates on all8GPU; both torchrun exit0, all8resident20fixturesPASS. All160paired trajectories have EXACTproblem IDs, sampledIDs, renderedoutputs,rewardcomponents,episodeF,widths,and per-call structured prefix metadata. DirectGPUsampledlogpdrift max0.000226974 acrossall5steps; allcollective replayguardsPASS maxobserved0.0007.
Normalsteady53–55wall1512.81451→1282.91811s:1.179198x (15.20%less time). Generation1.253807x. Globalbackend103992→40558, per-episodeF103992unchanged. Gainisworkloaddependent: step55only1.051064xwholewall.
Immutable complete proof: gpu-proof-baseline32-55-1-cohort32-55-1-cohort64-0-0-cohort128-0-0.json, SHA2562477cc7e7d7ecd35b2df4135e428e0f979bd0f9cb7a81255a6fdc4bb9f664005. Identical localcopy.
Maxnatural cohort GPUrows19; fixed32rankownsoneprompt×4responses, socross-trajectorysharingqualified, notcross-promptsharing. Naturalall1..8forksremainsingle backendgroup. Aggregate32residentproofstillrequired forB+D+C.
Pipeline automatically startedcohort64 torchrun2436 agentport29763/trainingport29863. Cross-prompt steadyfullupdate/64vs32tradeoffpending;128queued. Fixed32default unchanged.
Compositionplan: combined-candidate-plan.md, Bstable rowcompaction plusDfinished bank snapshotsbefore rowselection; Cowner-safe bankclear/version invalidationat fullbatchboundaries. Freshpaired32/aggregate32residentlikelihoodproof required. Nohealthyinputs/controlleredited.
