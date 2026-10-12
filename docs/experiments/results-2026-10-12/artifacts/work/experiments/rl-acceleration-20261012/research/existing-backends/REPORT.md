# Existing RL backends for the Qwen3-4B Instruct Parallel-R1 run

Research snapshot: 2026-10-12. CPU/read-only source inspection. No GPU allocations, launches, worker stops or production changes. Official GitHub metadata and selected source files are preserved in this directory; `SOURCE_REFERENCES.json` gives immutable URLs, commits, local paths, line counts and SHA-256 hashes. API release metadata is preserved separately. Downloaded code was read, not executed.

## Decision

**Reuse an existing precision/correction/training stack, but do not expect a stock RL launcher to preserve this model's fork-and-merge semantics.** The fastest prototype is the existing HF branch-aware generator with BF16 compute, FP32 master Adam and cached compact decode, plus the separately reviewed bounded lag-1 queue. The smallest useful upstream reuse is verl's three-policy correction implementation and metrics. A full move to slime or AReaL before proving branch KV fork/merge would add a new trainer, checkpoint conversion, distributed scheduler and inference engine simultaneously.

For a later production engine, **SGLang is the stronger candidate for a custom branch-cache adapter**, particularly alongside slime's custom generation hook. It exposes internal paged-KV indirection, positions and attention planning, but its normal generate API does not accept our branch mask or repeated text-token positions. This requires engine development, not a configuration change. AReaL's tree attention is useful source material for learning kernels, but implements an ancestor tree; our post-Parallel suffix attends all sibling branches and therefore forms a merge DAG.

There is no verified Qwen3-4B Instruct Parallel-R1 throughput number in these sources, and no source supports promising a specific multiplier on our eight A100s. The strong opportunity is avoiding repeated full-prefix work and FP32 inference, then batching live branches/trajectories. Async scheduling by itself is a smaller opportunity at the reported 70–82% generation share.

## Versions actually inspected

| System | Official repository / pinned source commit | Latest published release returned by GitHub | Dependency evidence at inspected commit |
|---|---|---|---|
| verl | `verl-project/verl`, `2035f58dcb06d8cad4caee107b30f4045d724367` (2026-10-12 02:03Z) | v0.9.1, 2026-09-20 | `pyproject.toml`: torch 2.13.0, vLLM 0.29.0 or SGLang 0.5.20, separate mutually exclusive extras |
| AReaL | `areal-project/AReaL`, `aedc21ec66ff03f329dcd4139945da8087e0d0e7` (2026-10-12 09:40Z); old inclusionAI URL redirects here | v2.1.0, 2026-08-25 | SGLang 0.5.10.post1; separate vLLM project/lock uses vLLM 0.19.1 |
| slime | `THUDM/slime`, `05e3b017fed9e02de418c2fbac9d75602a534be5` (2026-10-12 08:01Z) | v0.4.0, 2026-10-09 | Docker default SGLang image v0.5.15.post1-cu129, matching patch set; Megatron commit `4b4acac9a1d28ea6829c8d4f566d75698a21249d`; Transformer Engine 2.18.0 |
| OpenRLHF | `OpenRLHF/OpenRLHF`, `dc2a7ad326f619fc5a47737ea47d1920ce2c0b53` (2026-09-17) | v0.11.2, 2026-09-14 | Secondary candidate: Ray/vLLM/DeepSpeed ZeRO-3, async and custom agent generation; only README was inspected |

These are source snapshots, not installed or locally compatible versions. Latest main must not be mixed with an older release container. See [verl pins](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/pyproject.toml#L88-L121), [AReaL SGLang pins](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/pyproject.toml#L144-L150), [AReaL vLLM pins](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/pyproject.vllm.toml#L160-L165), [slime container](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/docker/Dockerfile#L1-L14).

## Concrete implementation contracts

### verl

The [Qwen3-4B GRPO/FSDP recipe](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/examples/grpo_trainer/run_qwen3_4b_fsdp.sh) uses `Qwen/Qwen3-4B`, vLLM, eight GPUs, TP=2, dynamic token microbatches, gradient checkpointing and LR 1e-6. Defaults are 512 prompts, five responses each and prompt/response caps 1024/1024. This is architecture support evidence, not the exact Instruct CP50/checkpoint or our 8×4 recipe. Its KL, batch, advantage and loss-reduction defaults must not be imported unchanged.

The [FSDP engine](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/workers/engine/fsdp/transformer_impl.py#L260-L268) loads training storage in FP32 unless configured otherwise; [mixed precision](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/workers/engine/fsdp/transformer_impl.py#L391-L405) defaults parameter compute BF16, reduction/buffers FP32. That supports FP32 master optimizer storage while forwards use BF16. Changing storage to BF16 is a different optimizer contract.

The [V1 async trainer guide](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/docs/advance/v1_async_trainer.md) distinguishes shared-GPU `colocate_async` from dedicated-pool `separate_async`, supports optional lending of idle trainer GPUs, and requires non-naive NCCL/NIXL/Mooncake weight transport for standalone rollout replicas. Model-version staleness is measured separately from versions spanned within a trajectory. It defaults to threshold 8 and group-wide drop; partial rollout can retry unfinished generation under newer weights. Merely setting threshold 1 does **not** enforce one immutable behavior snapshot for every trajectory or all four responses. CP50 recovery must also account for pending prompts already consumed by the dataloader.

Separate async's proximal model is fixed through a `parameter_sync_step` cycle. With multiple controller mini-batches it saves/restores CPU model copies around recomputing old probabilities; bypass skips that cost but changes the clipping center. Our batch should be a single complete 32-response update, avoiding default streamed mini-update semantics and retaining deterministic prompt order.

### AReaL

The [current GSM8K recipe](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/examples/math/gsm8k_grpo.yaml) uses 4 rollout + 4 FSDP trainer GPUs, BF16, four samples, max-head offpolicyness 2, XCCL weight sync and decoupled loss. It targets Qwen2.5-1.5B Instruct; no Qwen3-4B-named recipe was found in the complete current tree. Qwen3 architecture support is documented, but a 4B migration is a new configured recipe, not a validated copied command.

[FSDP configuration](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/areal/api/cli_args.py#L1425-L1453) separates BF16 compute, FP32 gradient reduction and FP32 optimizer storage. [Optimizer creation](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/areal/engine/fsdp_engine.py#L1262-L1307) uses AdamW over FP32 masters by default and explicitly warns about plain Adam with BF16 storage; Kahan BF16 Adam is a different alternative. This is direct reusable evidence for preserving master weights at LR 1e-6.

[StalenessManager](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/areal/infra/staleness_manager.py#L66-L140) limits pending work to `(eta+1)*consumer_batch_size` and admission to the smaller of concurrency capacity and `(eta+version+1)*batch_size-(accepted+running)`. Recovery sets accepted count to `version*batch_size` to avoid an admission burst. It is useful scheduler design, but does not prove immutable group leases; the [async guide](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/docs/en/algorithms/async.md) allows segmented multi-version trajectories.

[Tree training](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/docs/en/reference/tree_training.md#L1-L84) packs common-prefix sequences in a trie and allows each node to attend its ancestors, using FlexAttention or experimental Triton kernels. The documented up-to-7× acceleration is a tau2 training example. It neither accelerates our rollout automatically nor implements suffix attention to multiple non-ancestor siblings. Its block-mask wrapper can inform a custom DAG kernel, but token-to-loss and branch-source mappings still need adaptation.

### slime

[Qwen3-4B](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/scripts/run-qwen3-4B.sh) is a concrete Megatron+SGLang recipe: TP=2, packed dynamic batches, LR 1e-6, Adam, FP32 gradient accumulation, full recomputation. [Instruct-2507 tau-bench](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/examples/tau-bench/run_qwen3_4B.sh) explicitly uses Qwen3-4B-Instruct-2507 and a custom generate hook, with TP=2 training and TP=1 rollout. Neither path is our CP50/template/protocol. Conversion must preserve trained extra embeddings/head rows, optimizer/RNG and exact RoPE; the [Instruct model config](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/scripts/models/qwen3-4B-Instruct-2507.sh) changes rotary-base to 5,000,000.

[Megatron defaults](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/slime/backends/megatron_utils/arguments.py#L151-L165) select distributed optimizer and BF16 unless FP16 was requested. The pinned official [Megatron optimizer config](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/optimizer/optimizer_config.py#L184-L207) defaults main parameters, main gradients, Adam first and second moments to FP32; the non-precision-aware path [enforces these types](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/optimizer/optimizer_config.py#L469-L480). BF16 alone is insufficient evidence of every state dtype when configuration overrides are possible. A future migration must verify actual optimizer state tensors after CP50 load, not infer them from a launcher flag.

[Fully async](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/examples/fully_async/README.md) keeps background prompt-group generation and drains completed groups, pauses admission for weight sync and supports arbitrary custom generation/reward hooks. Ordering across rollout batches is best-effort; partial continuation can span versions, and restored queues do not restore GPU KV or identical future RNG. Consequently it needs stricter group4 leases, ordered batch receipts and no partial cross-version resume for our requested lag-1 contract. Its training sample/loss masks and no-std option are reusable; fixed denominator 4096 requires an explicit reduction override.

The example shell scripts contain broad `pkill` and Ray stop commands. They were inspected only; a future adapted launcher must scope cleanup to its owned job. This is an actual recipe detail, not authorization to stop existing workers.

### Other serious option

[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF/blob/dc2a7ad326f619fc5a47737ea47d1920ce2c0b53/README.md#L82-L101) provides an established Ray/vLLM/DeepSpeed stack with async/custom-agent hooks and importance correction. It remains subject to the same branch-mask/cache-merge blocker; switching to it adds no evidenced solution for our semantics. No Qwen3-4B-specific current recipe was identified by filename, and this narrower inspection is not an exhaustive negative proof.

## BF16 + lag-1 must be an explicit three-policy objective

For any future upstream port, these are **schema-verified overrides**, not a runnable production launcher (custom generation, checkpoint loading and R2 reward still need an adapter):

```yaml
# verl: replace the generic recipe's model with the exact Instruct CP50 path.
data.train_batch_size: 8                  # prompts; n=4 gives 32 responses
actor_rollout_ref.rollout.n: 4
actor_rollout_ref.actor.ppo_mini_batch_size: 8
actor_rollout_ref.actor.use_kl_loss: false
algorithm.use_kl_in_reward: false
algorithm.norm_adv_by_std_in_grpo: false
actor_rollout_ref.actor.entropy_coeff: 0
actor_rollout_ref.actor.loss_agg_mode: seq-mean-token-sum-norm
actor_rollout_ref.actor.loss_scale_factor: 4096
algorithm.rollout_correction.rollout_is: token
algorithm.rollout_correction.rollout_is_threshold: 2.0
algorithm.rollout_correction.bypass_mode: false
algorithm.rollout_correction.rollout_is_batch_normalize: false
algorithm.rollout_correction.rollout_rs: null
```

The loss adapter must supply the actual global response count 32 and use the audited distributed scaling, including zero-signal responses, rather than infer that count from retained tokens. [verl aggregation](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/trainer/ppo/core_algos.py#L1140-L1203) explicitly separates global batch size and fixed loss scale. No DAPO nonzero-std group filter or dynamic reward-driven refill may silently replace the eight prompts; current PPO clip/epochs/Adam betas/weight decay and all three native caps must be copied from CP50's approved recipe.

For AReaL, retain `actor.dtype=bfloat16`, `actor.optimizer_dtype=float32`, `actor.grad_reduce_dtype=float32`, and configure group mean over four with `reward_norm.std_level=null`, `adv_norm=null`, `reward_scaling=1`, `reward_bias=0`, `kl_ctl=0`; its recipe's group std, batch advantage whitening and reward scale/bias otherwise change R2. Its reduction needs fixed-length 4096 support/adaptation. For slime, use `--disable-grpo-std-normalization`, omit `--normalize-advantages`, remove the tau-bench nonzero-std filter and keep KL/entropy zero; select explicit token TIS, and override its default mean-over-live-tokens or per-sample-length reduction with fixed 4096. Do not blindly use `--disable-rewards-normalization` if it would also remove the required group mean: verify the selected advantage path. These additional defaults are why minimal estimator reuse is safer than replacing the whole pipeline first.

Use `q` for the actual BF16 actor distribution that sampled actions, `p0` for the learner's frozen proximal policy before an update, and `pθ` for the differentiable current learner. At each sampled action and its **same structured state**:

```
behavior_logp = immutable sampled log q
proximal_logp = frozen replay log p0, computed once before this update's epochs
current_logp  = differentiable log pθ
rho = stop_gradient(exp(proximal_logp - behavior_logp))
r   = exp(current_logp - proximal_logp)
loss = -sum(mask * clamp(rho, 0, C) * min(r*A, clip(r,1-eps,1+eps)*A))
       / (32 * 4096)
A = reward - mean(rewards in this prompt's four responses)
```

No advantage std/whitening, no correction-weight batch normalization and no new reward transform. Runtime-injected headers/bridges keep mask 0; sampled terminal/control tokens keep mask 1. The loss needs the source-index mapping of sibling live-logit rows, not a naive shift of the flattened string. Store `q` unchanged across all epochs, with behavior version, actor hash, dtype/kernel/sampling identity and group4 lease receipt. Group version age ≤1 is an additional condition, not a replacement for correction.

This is evidenced by [verl correction code](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/trainer/ppo/rollout_corr_helper.py#L786-L856), [slime TIS](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/slime/backends/megatron_utils/loss.py#L901-L924), and [AReaL PPO loss](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/areal/utils/functional/functional.py#L456-L580). AReaL's `rejection_sampling` controls whether behavior weighting/masking is applied; enabling `use_decoupled_loss` alone must not be assumed to enable a particular cap. verl defaults correction **off** (`rollout_is=null`); explicitly set token correction, cap 2.0, bypass false, normalization false. slime TIS defaults clamp [0,2]. These are upstream starting values for an experimental estimator, not validated thresholds for this task.

Changing exact replay's `.01/.002/.005` assertions into looser assertions is not this algorithm. For a signed numeric difference of +0.20, `exp(0.20)=1.221`, already beyond a +20% PPO clip before the learner moves. A separate frozen proximal center makes initial PPO `r≈1`; `rho` measures behavior mismatch independently. Still require strict replay within the **same BF16 actor version and branch/KV semantics**. Report signed/absolute Δlogp, ratio tails, correction cap fraction, ESS, learner clipping/KL, invalid mappings and stale groups separately; ratio containment does not prove semantic parity.

Sampling must also match the density contract. Temperature, top-k/top-p, close guards and forced-token policies can change `q`'s support/normalization. Record raw model probabilities and actual transformed sampled probabilities distinctly if transforms are active; a raw pre-truncation logp is not automatically the actual sampling density. Importance correction cannot repair a wrong branch mask, bad position IDs, missing probability support or stale KV weights.

Token TIS is a practical **biased surrogate**: capping biases action weights, and token weights alone do not correct the distribution of visited prefixes; a full trajectory density ratio would multiply action ratios and often has high variance. The [slime explanation](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/docs/en/advanced/policy-mismatch.md#L62-L107) explicitly states this limitation. Preserve the original strict FP32 lane as the reference; BF16+lag1 changes numerical policy and estimator and therefore needs a named experimental protocol, not a declaration of bitwise equivalence.

## Sibling-isolated cache strategy: feasible, but needs an adapter

Verified local layout: `experiments/parallel_instruct/source/parallel_structure.py` assigns repeated branch positions, isolates every sibling, attaches inter-path whitespace to the preceding sibling to prevent multi-layer leakage, and lets the suffix see all completed branches. The request and engine inspection used SGLang v0.5.15.post1 commit `0b3bb0cbe31873994c9f989fddfe2f87ca839fdd`, matching slime's default image family.

1. Prefill the shared context and `<Parallel>` count/header once. Fork read-only prefix KV references for each `<Path>`; each path receives exactly the prefix plus its own path header/body. Decode one token per live branch per logical round, width ≤8, preserving guards, stops, sampling seed contract and logical forward counter F.
2. Finish every path and its attached whitespace using the isolated path cache. The shorter path's bridge tokens use its own next positions, exactly as local layout specifies. Do not let bridge caches inherit another sibling.
3. Assemble a merged request KV index list: one shared prefix, then every branch's distinct tokens in flattened trace order, including headers/bridges. Each layer's already-computed KV carries that token's correct repeated RoPE position. Keep each prefix token once, never sum/average KVs or duplicate the prefix as separate attention keys.
4. Decode `</Parallel>` and suffix against this union; its first position is shared start + longest attached branch span, not the sum of branch lengths. Ordinary one-query decode can attend all union keys, but position calculation and request-to-KV mapping must be overridden. Future forks repeat from the merged cache. Restore/refill must use a structured prefill or per-branch replay; a standard flat causal prefill corrupts earlier branch hidden states even if the final suffix mask is permissive.

Sources: [normal request schema](https://github.com/sgl-project/sglang/blob/0b3bb0cbe31873994c9f989fddfe2f87ca839fdd/python/sglang/srt/managers/io_struct.py#L155-L244), [decode/extend position construction](https://github.com/sgl-project/sglang/blob/0b3bb0cbe31873994c9f989fddfe2f87ca839fdd/python/sglang/srt/model_executor/forward_batch_info.py#L803-L840), [request-to-token pool](https://github.com/sgl-project/sglang/blob/0b3bb0cbe31873994c9f989fddfe2f87ca839fdd/python/sglang/srt/mem_cache/memory_pool.py#L242-L276), [FlashInfer planning](https://github.com/sgl-project/sglang/blob/0b3bb0cbe31873994c9f989fddfe2f87ca839fdd/python/sglang/srt/layers/attention/flashinfer_backend.py#L1590-L1649). Internal speculative/custom masks are not evidence of a public arbitrary-mask generate API. The normal [verl SGLang request](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/workers/rollout/sglang_rollout/async_sglang_server.py#L590-L623) passes input IDs and sampling parameters, not our mask/positions.

Adapter cost spans request/controller state, prefix ownership/reference counts, append/merge KV table construction, logical positions versus cache lengths, and cache invalidation on weight sync. Prefix-cache keys must include the relevant structured layout/positions and actor version; token IDs alone are unsafe. Start graph-disabled for the unusual transitions, then add CUDA graph buckets only after exact source/mask parity. Arbitrary standard HTTP requests can generate isolated individual paths, but cannot export/merge their live engine KVs; returning text and then ordinary causal-refitting concatenated paths does not preserve semantics. A mixed engine/HF fallback needs explicit KV interoperability or exact structured rebuild and could erase the gains.

## Expected limits and a reviewable prototype order

Given reported generation fraction `p=.70–.82`, merely replacing serial generation+training by perfect overlap with **unchanged per-stage capacity** gives `(G+T)/max(G,T)=1/p=1.22–1.43×`. On 267–620 s/update, the removable serial training portion is only 18–30%; actual fixed-eight-GPU pool splitting may slow either stage and synchronization adds cost. Larger gains need generation acceleration, not an async label. These are analytical bounds from the supplied profile, not new measurements.

AReaL's 2.77× result comes from older R1-Distill-Qwen 1.5B/7B runs on 16/24 nodes, 1000 PPO steps; its current [benchmark README](https://github.com/areal-project/AReaL/blob/aedc21ec66ff03f329dcd4139945da8087e0d0e7/benchmark/README.md) says legacy realhf configs require old commit 820ca49 and are incompatible with current code. The tree-training 7× claim is tau2 prefix reuse. Neither is a matched predictor for our 32 responses, A100s and DAG masks.

Prototype order within the existing aggregate GPU budget, when GPU work is separately authorized: (1) exact cached/forked HF decode parity against the same actor, fixed CP50/seed/caps 4096/768/16384; (2) BF16 compute with explicit FP32 masters and same-BF16-actor parity; (3) frozen-proximal/token-TIS experimental loss on a fixed saved batch, CPU gradient checks and unchanged mask/denominator; (4) lag-1 immutable group4 leases, bounded one-future-batch queue, atomic weights/KV invalidation and ordered exactly-once receipts; (5) only then a SGLang branch adapter and migration to upstream trainer if it demonstrates a further gain.

Measure 32-response update wall time, sampled tokens/sec, unique prefills, cache bytes, physical logical F per trajectory and backend calls separately, sync time, learner time and distribution of completion tails. Continuous batching can reduce global kernel calls while preserving per-trajectory F; it must not accidentally reduce our reward cost through unrelated cross-trajectory batching. Final acceptance retains CP50 identity, nativeThink/postThink close guards, group4 mean/noStd, R2 correctness-gated reward, all sampled terminal masks, full-width ≤8 and exact branch-source probability mapping. Numerical BF16/async policy changes are reported as such.
