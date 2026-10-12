Complete-context FP32 learner batching: GPU qualification completed

All eight actors completed five positive Adam updates51–55, all eight resident20-case width fixtures passed, and every actor exited0. Controller6555 finished14:57:44UTC; actors6558–6565 disappeared from the compute process list, all eight GPUs showed0MiB/0%, and worker0 was handed to D. No further C GPU benchmark is queued.

| Step | Full wall, s | Generation, s | Sampled tokens | Episode F | Global F | Correct/32 |
|---|---:|---:|---:|---:|---:|---:|
|51, proofs included|791.620|136.863|26157|19438|7925|28|
|52|196.059|86.871|24238|19104|7474|28|
|53|336.981|155.607|35808|26089|10086|19|
|54|295.534|130.413|33847|25449|11397|20|
|55|198.386|76.614|27056|19883|7172|22|

Whole wall including cleanup/gather52–55:196.547/337.616/296.138/198.967s. CUDA allocated peak across all steps51.795GiB. Actual global backend calls are distinct from episode F; reward uses episode F only. Strict cached q replay is EXACT0 every step, independent FP32 cached/full p0 max.000135422, and grouped versus scalar p0 first-update maximum.000144958. Collective max.01/mean.002/p95.005 limits remain unchanged. Complete action coverage, injected mask0, indivisible sibling groups and episode accounting passed all160 traces. Natural aggregate rows≤17; learner groups≤4.

CPU all-parameter TIS gradient comparison is4.40457e-20, logprob difference0; every long singleton remains complete. First real GPU update versus the scalar learner has loss difference1.1445e-8, gradient norm difference1.7136e-7, and first1024 backbone probe update-norm difference9.55e-11. Full GPU gradient components were not compared.

First32 actual q/actions/outputs/rewards/episode F exactly match the previous stateless BF16 actor route. After Adam, trajectories diverged: only3/32 actions match at52, none at53. Comparing warmed53 wall350.412→336.981 gives1.03986× across different token/F work and does not establish a same-work throughput gain. Historical52 wall641.412 included resident proof, so its apparent3.27× comparison is invalid. This route did not demonstrate3×.

Final fixed clean16 FP32 pilot at55:12/16 correct,15/16 format valid. Previous stateless route at53 had13/16, with a different optimizer-step count. Small pilot coverage does not establish quality preservation. The inherited raw summary contains selection_allowed=true, a legacy unused label; config and qualification explicitly forbid selection, no checkpoint was selected, and the raw summary is preserved unchanged for provenance.

Composition: qualified C stateless BF16 actor q + explicit A TIS cap2 + D abort-safe cohort + complete FP32 learner grouping. No D6 persistent KV. Admission4rows/8192padded-context/4096padded-action-head/actionratio2 only groups calls; oversized singletons remain complete. Per-call masks, repeated positions, immutable q, independent advantage and4096×world/global32 normalization remain intact. Final group alone synchronizes DDP. Actor seeds, prompt IDs,8×4 global32, full4096/768/16384 caps, reward SHA b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce, FP32 masters/learner and Zero1Adam1e-6 remain fixed.

Final evidence gpu-stateless-proof-55-1.json SHA e9feed1412fb1f5031e662af2fd80acfac5c6646669d8d93cb7ba65d6a3a5bdd; actual paired proof paired-unified-bf16-tis-53-updates5.json SHA ce764bbf339d0bdd6c1e9db8f73d6c5bdcc4d3a16e48ba8f23e92e981cab4f3c. Local and NFS copies match. patch.diff SHA e476b84b7a71388b221243048b0524b4bdd03a2df722ad810f3abcf7fd30e25c passed git apply --check against the qualified stateless source. Patches are isolated review artifacts, production was not modified.
