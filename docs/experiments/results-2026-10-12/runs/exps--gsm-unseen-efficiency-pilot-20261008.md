# exps/gsm-unseen-efficiency-pilot-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/gsm-unseen-efficiency-pilot-20261008/data-audit.json](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train_rows": 4547,
  "train_by_op": {
    "2": 712,
    "3": 746,
    "4": 750,
    "5": 1579,
    "6": 760
  },
  "heldout_gsm_rows": 256,
  "math_validation_only_rows": 316,
  "source_revision": "c6c5ab433565ddfe3e38e22be165b5c40e6bd576",
  "excluded_math_rows": 12500,
  "excluded_sft_rows": 5910,
  "rejections": "285 records; see original artifact",
  "split": "Normalized exact question disjoint; shared generator templates remain. Original 256 screening questions held out.",
  "decontamination": "Normalized exact and number-masked trigram Jaccard>=0.65 against all MATH and SFT; not semantic proof.",
  "gold_histogram": {
    "1": 364,
    "3": 865,
    "2": 882,
    "4": 994,
    "12": 191,
    "20": 20,
    "6": 266,
    "5": 151,
    "10": 115,
    "16": 48,
    "8": 255,
    "15": 44,
    "14": 4,
    "9": 162,
    "7": 114,
    "11": 47,
    "24": 7,
    "18": 6,
    "32": 6,
    "48": 2,
    "23": 2,
    "0": 1,
    "17": 1
  },
  "data_sha256": {
    "train.parquet": "9761c994eb5838177466616fe09d28eefbfeb8de31a7492e0916973556e4542b",
    "validation.parquet": "28f380534762d90fd01015e68789d01c1a856cf157d28f508197fa35595603ec",
    "smoke-validation.parquet": "20ebdf6987b6a91be28292b6bcd506efe7333b13096511d45868234b4a1722e9"
  }
}
```

</details>

- [exps/gsm-unseen-efficiency-pilot-20261008/depth/resolved-config.yaml](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/depth/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 16
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 2
    use_dynamic_bsz: false
    ppo_max_token_len_per_gpu: 16384
    clip_ratio: 0.2
    clip_ratio_low: 0.2
    clip_ratio_high: 0.28
    policy_loss:
      loss_mode: vanilla
      clip_cov_ratio: 0.0002
      clip_cov_lb: 1.0
      clip_cov_ub: 5.0
      kl_cov_ratio: 0.0002
      ppo_kl_coef: 0.1
    clip_ratio_c: 3.0
    loss_agg_mode: token-mean
    entropy_coeff: 0
    use_kl_loss: false
    use_torch_compile: false
    kl_loss_coef: 0.001
    kl_loss_type: low_var_kl
    ppo_epochs: 1
    shuffle: false
    checkpoint:
      save_contents:
      - model
      - optimizer
      - extra
      - hf_model
      load_contents:
      - model
      - optimizer
      - extra
    optim:
      lr: 1.0e-06
      lr_warmup_steps_ratio: 0.0
      total_training_steps: -1
      weight_decay: 0.01
      lr_warmup_steps: -1
      min_lr_ratio: 0.0
      num_cycles: 0.5
      warmup_style: constant
    grad_clip: 1.0
    ulysses_sequence_parallel_size: 1
    entropy_from_logits_with_chunking: false
    entropy_checkpointing: false
    fsdp_config:
      wrap_policy:
        min_num_params: 0
      param_offload: false
      optimizer_offload: false
      offload_policy: false
      reshard_after_forward: true
      fsdp_size: -1
      forward_prefetch: false
      sharding_strategy: NO_SHARD
    sort_microbatches_by_length: false
    trim_parallel_padding: true
    sort_logprob_rows_by_length: true
    sort_microbatch_groups_by_length: true
    defer_gradient_sync: true
    skip_zero_advantage_microbatches: true
  ref:
    strategy: fsdp
    use_torch_compile: false
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: null
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    fsdp_config:
      param_offload: false
      reshard_after_forward: true
      forward_prefetch: false
      wrap_policy:
        min_num_params: 0
    ulysses_sequence_parallel_size: 1
    entropy_from_logits_with_chunking: false
    entropy_checkpointing: false
  rollout:
    name: vllm
    mode: async
    temperature: 1.0
    top_k: -1
    top_p: 1
    prompt_length: 2000
    response_length: 3000
    dtype: bfloat16
    gpu_memory_utilization: 0.45
    ignore_eos: false
    enforce_eager: false
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 64
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 4
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    disable_log_stats: true
    do_sample: true
    'n': 8
    multi_stage_wake_up: false
    engine_kwargs:
      vllm:
        swap_space: null
        disable_mm_preprocessor_cache: false
      sglang:
        attention_backend: null
    val_kwargs:
      top_k: -1
      top_p: 1.0
      temperature: 1.0
      'n': 1
      do_sample: true
    multi_turn:
      enable: false
      max_assistant_turns: null
      tool_config_path: null
      max_user_turns: null
      max_parallel_calls: 1
      max_tool_response_length: 256
      tool_response_truncate_side: middle
      interaction_config_path: null
      completion_callback: null
      use_inference_chat_template: false
      tokenization_sanity_check_mode: strict
      format: hermes
    calculate_log_probs: false
    parallel: false
    agent:
      num_workers: 32
      agent_loop_config_path: null
      max_iterations_for_parallel_thinking: 4
      num_paths: 2
      max_path_response_length: 3000
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: true
    load_format: dummy_dtensor
    layered_summon: false
  hybrid_engine: true
  model:
    path: ${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: false
    enable_activation_offload: false
    use_remove_padding: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
    exclude_modules: null
    use_liger: false
    use_fused_kernels: true
    fused_kernel_options:
      impl_backend: triton
    trust_remote_code: false
  profiler:
    _target_: verl.utils.profiler.ProfilerConfig
    discrete: false
    all_ranks: false
    ranks: []
trainer:
  npu_profile:
    options:
      save_path: ./profiler_data
      level: level1
      with_memory: false
      record_shapes: false
      with_npu: true
      with_cpu: true
      with_module: false
      with_stack: false
      analysis: true
  balance_batch: true
  total_epochs: 100
  total_training_steps: 200
  profile_steps: null
  controller_nsight_options:
    trace: cuda,nvtx,cublas,ucx
    cuda-memory-usage: 'true'
    cuda-graph-trace: graph
  worker_nsight_options:
    trace: cuda,nvtx,cublas,ucx
    cuda-memory-usage: 'true'
    cuda-graph-trace: graph
    capture-range: cudaProfilerApi
    capture-range-end: null
    kill: none
  project_name: Parallel-R1
  experiment_name: gsm-unseen-efficiency-pilot-20261008-depth
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/depth/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/depth/results/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 100
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: false
  val_only: false
  test_freq: 50
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/depth/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/validation.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 32
  val_batch_size: 256
  return_raw_input_ids: false
  return_raw_chat: true
  return_full_prompt: false
  shuffle: true
  dataloader_num_workers: 2
  validation_shuffle: false
  filter_overlong_prompts: true
  filter_overlong_prompts_workers: 1
  truncation: error
  image_key: images
  video_key: videos
  trust_remote_code: false
  custom_cls:
    path: null
    name: null
  return_multi_modal_inputs: true
  sampler:
    class_path: null
    class_name: null
  datagen:
    path: null
    name: null
  seed: 20261008
critic:
  rollout_n: 8
  strategy: fsdp
  optim:
    lr_warmup_steps_ratio: 0.0
    total_training_steps: -1
    weight_decay: 0.01
    lr: 1.0e-05
    min_lr_ratio: null
    warmup_style: constant
  model:
    path: ~/models/deepseek-llm-7b-chat
    tokenizer_path: ${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final
    override_config: {}
    external_lib: null
    enable_gradient_checkpointing: true
    trust_remote_code: false
    use_shm: false
    enable_activation_offload: false
    use_remove_padding: false
    fsdp_config:
      param_offload: false
      optimizer_offload: false
      offload_policy: false
      reshard_after_forward: true
      wrap_policy:
        min_num_params: 0
      fsdp_size: -1
      forward_prefetch: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
  ppo_mini_batch_size: 16
  ppo_micro_batch_size: null
  ppo_micro_batch_size_per_gpu: null
  use_dynamic_bsz: false
  ppo_max_token_len_per_gpu: 32768
  forward_max_token_len_per_gpu: 32768
  ppo_epochs: 1
  shuffle: false
  cliprange_value: 0.5
  loss_agg_mode: token-mean
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents:
    - model
    - optimizer
    - extra
  profiler:
    _target_: verl.utils.profiler.ProfilerConfig
    discrete: false
    all_ranks: false
    ranks: []
  _target_: verl.trainer.config.FSDPCriticConfig
  forward_micro_batch_size: null
  forward_micro_batch_size_per_gpu: null
  ulysses_sequence_parallel_size: 1
  grad_clip: 1.0
reward_model:
  enable: false
  strategy: fsdp
  model:
    input_tokenizer: ${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final
    path: ~/models/FsfairX-LLaMA3-RM-v0.1
    external_lib: null
    trust_remote_code: false
    use_shm: false
    use_remove_padding: false
    use_fused_kernels: true
    fsdp_config:
      wrap_policy:
        min_num_params: 0
      param_offload: false
      reshard_after_forward: true
      fsdp_size: -1
      forward_prefetch: false
  micro_batch_size: null
  micro_batch_size_per_gpu: null
  max_length: null
  use_dynamic_bsz: false
  forward_max_token_len_per_gpu: 32768
  reward_manager: naive
  launch_reward_fn_async: false
  sandbox_fusion:
    url: null
    max_concurrent: 64
    memory_limit_mb: 1024
  profiler:
    _target_: verl.utils.profiler.ProfilerConfig
    discrete: false
    all_ranks: false
    ranks: []
  ulysses_sequence_parallel_size: 1
custom_reward_function:
  path: ${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    mode: depth
algorithm:
  _target_: verl.trainer.config.AlgoConfig
  gamma: 1.0
  lam: 1.0
  adv_estimator: grpo
  norm_adv_by_std_in_grpo: true
  use_kl_in_reward: false
  kl_penalty: kl
  kl_ctrl:
    _target_: verl.trainer.config.KLControlConfig
    type: fixed
    kl_coef: 0.001
    horizon: 10000
    target_kl: 0.1
  use_pf_ppo: false
  pf_ppo:
    _target_: verl.trainer.config.PFPPOConfig
    reweight_method: pow
    weight_pow: 2.0
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-efficiency-pilot-20261008/manifest.json](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "run": "gsm-unseen-efficiency-pilot-20261008",
  "commit": "b656ead",
  "base_commit": "ea3b07d74851739f2c8c41a88948ca8976b6b165",
  "stage": "efficiency",
  "gpus": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7
  ],
  "steps": 200,
  "checkpoint": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
  "data_sha256": {
    "train.parquet": "9761c994eb5838177466616fe09d28eefbfeb8de31a7492e0916973556e4542b",
    "validation.parquet": "28f380534762d90fd01015e68789d01c1a856cf157d28f508197fa35595603ec",
    "smoke-validation.parquet": "20ebdf6987b6a91be28292b6bcd506efe7333b13096511d45868234b4a1722e9"
  },
  "overrides": [
    "ray_init.num_cpus=64",
    "+ray_init.temp_dir=${PROJECT_ROOT}",
    "+ray_init.plasma_directory=${PROJECT_ROOT}/plasma",
    "+ray_init.object_store_memory=8589934592",
    "data.train_batch_size=32",
    "actor_rollout_ref.actor.ppo_mini_batch_size=16",
    "actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2",
    "actor_rollout_ref.actor.loss_agg_mode=token-mean",
    "actor_rollout_ref.actor.sort_microbatches_by_length=false",
    "actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4",
    "actor_rollout_ref.rollout.agent.num_workers=32",
    "trainer.val_before_train=false",
    "actor_rollout_ref.model.use_fused_kernels=true",
    "actor_rollout_ref.model.fused_kernel_options.impl_backend=triton",
    "++actor_rollout_ref.actor.sort_logprob_rows_by_length=true",
    "++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true",
    "++actor_rollout_ref.actor.defer_gradient_sync=true",
    "actor_rollout_ref.actor.clip_ratio_high=0.28",
    "actor_rollout_ref.rollout.max_num_seqs=64",
    "++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD",
    "++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true",
    "data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/train.parquet",
    "data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/validation.parquet",
    "data.val_batch_size=256",
    "data.shuffle=true",
    "++data.seed=20261008",
    "trainer.resume_mode=disable",
    "trainer.save_freq=100",
    "trainer.test_freq=50",
    "trainer.total_training_steps=200",
    "trainer.max_actor_ckpt_to_keep=2",
    "trainer.logger=[console]",
    "actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]",
    "actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]",
    "custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/code/verl/verl/utils/reward_score/gsm_depth.py",
    "custom_reward_function.name=compute_score",
    "+custom_reward_function.reward_kwargs.depth_lambda=0.0001"
  ],
  "extra_env": {
    "PARALLEL_R1_FULL_DECODE_GRAPH": "1",
    "VLLM_ATTENTION_BACKEND": "FLASH_ATTN",
    "CUDA_HOME": "${CUDA_HOME}",
    "PYTHONPATH": "${PROJECT_ROOT}/exps/rl-s1-seen-20261006-1112/flashinfer-deps",
    "PARALLEL_R1_GRAPH_CAPTURE_MIN_USES": "64"
  },
  "hypothesis": "Correctness-gated relative parallel efficiency avoids rewarding shorter wrong/serial answers. Compare matched GSM pilot with original runs at step200.",
  "checkpoint_policy": {
    "save_every": 100,
    "retain": 2,
    "full_training_state": true,
    "hf_weights": true
  },
  "stages": [
    "depth"
  ],
  "lambda_per_decode_depth": null,
  "stage_initialization": "Each starts independently from original Unseen SFT; retry resumes only its own full checkpoint.",
  "depth_definition": "Sum of generated main/summary token counts plus maximum generated path token count per fork. Excludes injected tags and prefill compute; not physical batched GPU forwards.",
  "max_attempts_per_stage": 3,
  "stall_timeout_seconds": 2700,
  "stage_attempt_timeout_seconds": 86400,
  "reward_formula": "I[correct] * (1 + 0.2 * (1 - critical_depth/generated_tokens)); bonus only for valid parallel format",
  "parallel_efficiency_bonus": 0.2,
  "parent_run": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008",
  "caveats": [
    "Relative efficiency may encourage padding parallel paths; inspect traces and actual lengths.",
    "Reward does not directly optimize measured wall-clock throughput or require multiple blocks."
  ]
}
```

</details>

## Метрики и полнота результатов

- [exps/gsm-unseen-efficiency-pilot-20261008/review-status.json](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/review-status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "not_launched",
  "gpu_jobs_started": 0,
  "preflight": "failed synthetic malformed-format assertion; legacy format checker accepts missing Summary closure",
  "decision": "User is reviewing reward plots and proposes correctness-only penalty or lower lambda. Defer relative-efficiency pilot; analyze normalization before selecting next run. Original two 800-step runs complete.",
  "proposed_ablations": [
    "correctness-gated depth penalty, unchanged GRPO normalization",
    "correctness-gated depth penalty with separately scaled depth advantage"
  ],
  "original_analysis": "../gsm-unseen-two-rewards-20261008/reward-analysis.json"
}
```

</details>

- [exps/gsm-unseen-efficiency-pilot-20261008/status.json](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "observed_utc": "2026-10-08T05:42:58.598181+00:00",
  "error": "CalledProcessError(1, ['${PROJECT_ROOT}/.venv/bin/python', '${PROJECT_ROOT}/exps/gsm-unseen-efficiency-pilot-20261008/check_reward.py'])"
}
```

</details>

## Исходники рецепта и награды

- [exps/gsm-unseen-efficiency-pilot-20261008/controller.py](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-efficiency-pilot-20261008/reward.py](../artifacts/exps/gsm-unseen-efficiency-pilot-20261008/reward.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
