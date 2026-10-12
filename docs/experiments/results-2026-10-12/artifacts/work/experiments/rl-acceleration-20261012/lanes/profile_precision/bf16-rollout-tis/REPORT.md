# BF16 rollout + FP32 learner: explicit token TIS

NEW estimator mode, не byte-identical продолжение исходной FP32 sampling policy. q raw sampled likelihood остаётся в traces и в отдельном proximal journal; p0 FP32 proximal до единственного optimizer update; rho=detach(clamp(exp(p0−q),0,2)); PPO ratio=exp(pθ−detach(p0)). Fixed32 responses/4096, 8prompts×4, centeredadvantages/noStd, R2/data/caps unchanged. FP32 master params/Adam; BF16 autocast только rollout, FP32 learner/backward. Config запрещает async/epochs>1/updates>1; при будущем async p0 нужно независимое frozen snapshot, current.detach не подходит.

Source-pinned cap: slime05e3b017fed9e02de418c2fbac9d75602a534be5 importance_weights tokenTIS[0,2]; verl2035f58dcb06d8cad4caee107b30f4045d724367 correction explicit tokenTIS upper2 (OFF default), batchnorm/bypassfalse. Kernel SHA c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114.

Own CPU24cases passed exact loss/gradient reference; independent B18 clipping/sign/cap cases, detachedq/p0, legacyq=p0, mask forced0/terminal1, freshp0 detach; actual8Gloo fixed32/4096 loss-scale parity gradienterror2.965e-21/Adamerror0, bad actorrank collective skip preservesAdam. Proof saved B-three-policy-proof.json. Root internal engineering review ROOT-REVIEW.json authorizes only isolated2updates51/52, controller8470 onnodeA8; originals не возобновлялись.

Every update includes short real-main and full-branch-group checks: cachedBF16q targetreplay vs immutableq and independent FP32cachedp0 vsfullteacher; each policy сохраняет max.01/mean.002/p95.005 collectiveguard. p0/q drift is separate ratio telemetry. End52 adds160resident fullwidth fixtures (FP32cached/full plus BF16cached repeats), followed by FP32 clean16 evaluation at unchanged caps. Fixed16 cleanpilot is evaluation only, not training-budget reduction. Actual GPU proof completed; details below. This is numerical/Adam qualification of the NEW estimator, not demonstrated full500 convergence or a token-throughput gain.

Numerical caveat: tokenTIS cap introduces bias, does not correct complete prefix-state sampling distribution. Tiny quality and2update proof не доказывают full500 convergence. PairedFP32/BF16 natural trajectories differ; compare real updatewall and T/F quantities together. First51profiled,52unprofiled; residentfixtures/validation отдельно от ordinary updatewall. No exports.


## Completed GPU proof

All8 workers exit0, GPUs0MiB/0% live verified after controller8470 completed. 2positive Adam updates perrank (16/16 rank-updates), backboneL2 step51=2.840655e-5,52=1.965852e-5. Actorq cached checks max/mean/p95=0. Independent FP32p0 cached/full maximum6.67572e-5, worstmean4.99189e-6/p952.47955e-5, unchanged strict collectiveguard allpassed/no skips. Peak53.137GB. Resident160fixtures allpassed, including repeatBF16actorcache exact after residentFP32Adam and FP32 cached/full mask/position checks.

Final FP32learner clean16 13/16 correct matches frozencp50 13/16; format14/16. Initial BF16q clean16 was11/16; trainingq correct26/32 at51,25/32 at52 vsFP32baseline30/32 both. Tiny paired quality proof does not establish convergence or equivalence of sampling policies.

| step | true wholewall | generation critical | replay | backward | proof fixtures | T | physicalF | correctq |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|51 profiled|265.924s|186.682s|26.177s|46.641s|4.855s short numeric|24026|17869|26/32|
|52 unprofiled|691.687s inclresident|133.027s|24.674s|42.780s|6.092s short + large resident block|22296|17184|25/32|

52 critical pre-resident disjoint phase sum207.071s; this is a phase-sum proxy, NOT independently sampled exact steady wholewall. FP32baseline52 exactwhole267.377s,T36443/F24215/correct30. BF16T/F arelower39%/29%; wallcomparison is confounded by changedq trajectories/length and estimator. 51 exactwall265.924 vsFP32first328.948 (−19.2%), butT−33.4%/F−27.1%, sampledT/s90.35 vs109.60 actuallylower. No qualified overallthroughput improvement claim yet.

Scoped identical-shape first450-tokenprefill+8decode GPUkernel sum FP32.405339s→BF16.176623s (2.295×). HostCUDAlaunch.457310s→.487005s; kernelcount16888→21622. BF16largeweights cast once/layer across9forwards (q_proj36casts,gate/up72,down36), proving weightcacheworks. GPUtensorcoreGEMM+BF16cutlassSDPA exist; extraactivationcasts/CPUlaunch floor dominate. These artifacts support cached CUDAgraph as next measured route, not blind wholeautoregressive-loop compilation.

Evidence: `proof.json`, `training/metrics-rank-*.jsonl`, `training/profile/phase-rank-*.jsonl`, Chrome profiles, `training/traces-rank-*.jsonl` immutableq, `training/proximal-rank-*.jsonl` separatep0, residentfixtures, validation0052, config-launch.json and ROOT-REVIEW.json. `candidate.patch` includes isolated changes; allruntime sources sealed before launch and unchanged whilelive. OriginalM sources/wrappers untouched; no exports/production500.
