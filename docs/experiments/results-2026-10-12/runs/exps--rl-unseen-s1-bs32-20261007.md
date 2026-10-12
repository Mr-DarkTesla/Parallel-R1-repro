# exps/rl-unseen-s1-bs32-20261007

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/rl-unseen-s1-bs32-20261007/manifest.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "run": "rl-unseen-s1-bs32-20261007",
  "commit": "b656ead",
  "base_commit": "ea3b07d74851739f2c8c41a88948ca8976b6b165",
  "stage": "s1",
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
  "steps": 300,
  "checkpoint": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
  "data_sha256": {
    "verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e",
    "verl/data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet": "8fd253319384ede4e436d24a4f2884a632e8b1e71e1ee4bc1951ecb68007cec1"
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
    "actor_rollout_ref.actor.clip_ratio_high=0.2",
    "actor_rollout_ref.rollout.max_num_seqs=64",
    "++actor_rollout_ref.actor.fsdp_config.sharding_strategy=FULL_SHARD",
    "++actor_rollout_ref.actor.skip_zero_advantage_microbatches=false",
    "trainer.test_freq=50",
    "trainer.resume_mode=resume_path",
    "trainer.resume_from_path=${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90"
  ],
  "extra_env": {
    "PARALLEL_R1_FULL_DECODE_GRAPH": "1",
    "VLLM_ATTENTION_BACKEND": "FLASH_ATTN",
    "CUDA_HOME": "${CUDA_HOME}",
    "PYTHONPATH": "${PROJECT_ROOT}/exps/rl-s1-seen-20261006-1112/flashinfer-deps",
    "PARALLEL_R1_GRAPH_CAPTURE_MIN_USES": "64"
  },
  "hypothesis": "Repeat the plotted Unseen-S1 from original Unseen-SFT with train batch32 rather than256, preserving n8 and two PPO minibatch updates per RL step via mini16 rather than128. Measure warmed wall time and responses/s; smaller batch is less work, not an algorithmic speedup.",
  "implementation_changes": [
    "User explicitly selected Unseen-S1 batch32, not Seen and not S2; fresh original Unseen-SFT, accuracy_reward, cliphigh0.2, LR1e-6,300steps.",
    "Batch256 to32; PPO mini128 to16 proportionally retains two minibatch optimizer updates; micro2, n8, token-mean and original structured masks/runtime tags retained.",
    "Match plotted S1 optimizer backend FULL_SHARD with deferred sync; S2 NO_SHARD and zero-advantage skip disabled to avoid conflating new optimizations with batch-size comparison.",
    "Use already validated late-S1 fused Triton head, independent logprob sorting, original-pair ordering, and exact decode graphs with capture minimum4; inference64 matches S1 effective admission.",
    "Same17917 DAPO train questions and1916 accuracy-only validation; save and validation every10, retain3; frozen snapshot b656ead with checked hashes.",
    "No optimizer/weights from S1 or S2 reused; baseline SFT validation already measured for the same checkpoint, not rerun before timing.",
    "Resume complete step90 including optimizer/RNG/data on all8 GPUs; validation interval10 to50; checkpoint interval10 unchanged; graph capture threshold64. All300 training updates retained."
  ],
  "validation": [
    "All frozen changed-source and Parquet SHA256 verified before launch",
    "Hydra resolved config preflight",
    "Pending3-5 warm optimizer steps, first durable checkpoint and HF export"
  ],
  "resume_checkpoint": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90",
  "source_comparison": "Unseen-S1 from the user graphs, exps/rl-unseen-s1-20261007-seq128; new independent start at original Unseen-SFT"
}
```

</details>

- [exps/rl-unseen-s1-bs32-20261007/resolved-config.yaml](../artifacts/exps/rl-unseen-s1-bs32-20261007/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.2
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
      sharding_strategy: FULL_SHARD
    sort_microbatches_by_length: false
    trim_parallel_padding: true
    sort_logprob_rows_by_length: true
    sort_microbatch_groups_by_length: true
    defer_gradient_sync: true
    skip_zero_advantage_microbatches: false
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
  total_training_steps: 300
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
  experiment_name: rl-unseen-s1-bs32-20261007
  logger:
  - console
  - wandb
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 10
  esi_redundant_time: 0
  resume_mode: resume_path
  resume_from_path: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90
  val_before_train: false
  val_only: false
  test_freq: 50
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet
  val_files: data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 32
  val_batch_size: null
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
  path: null
  name: compute_score
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

- [exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/config.yaml](../artifacts/exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.2
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
      load_contents: ${.save_contents}
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
      sharding_strategy: FULL_SHARD
    sort_microbatches_by_length: false
    trim_parallel_padding: true
    sort_logprob_rows_by_length: true
    sort_microbatch_groups_by_length: true
    defer_gradient_sync: true
    skip_zero_advantage_microbatches: false
  ref:
    strategy: ${actor_rollout_ref.actor.strategy}
    use_torch_compile: ${oc.select:actor_rollout_ref.actor.use_torch_compile,true}
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: null
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
    fsdp_config:
      param_offload: false
      reshard_after_forward: true
      forward_prefetch: false
      wrap_policy:
        min_num_params: 0
    ulysses_sequence_parallel_size: ${oc.select:actor_rollout_ref.actor.ulysses_sequence_parallel_size,1}
    entropy_from_logits_with_chunking: false
    entropy_checkpointing: false
  rollout:
    name: vllm
    mode: async
    temperature: 1.0
    top_k: -1
    top_p: 1
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
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
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
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
      max_path_response_length: ${data.max_response_length}
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
    path: ${oc.env:PARALLEL_R1_MODEL_PATH}
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
  total_training_steps: 300
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
  experiment_name: ${oc.env:PARALLEL_R1_RL_NAME}
  logger:
  - console
  - wandb
  log_val_generations: 0
  rollout_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/rollouts
  validation_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 10
  esi_redundant_time: 0
  resume_mode: resume_path
  resume_from_path: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90
  val_before_train: false
  val_only: false
  test_freq: 50
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${oc.env:PARALLEL_R1_RL_DIR}/checkpoints
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_${oc.env:PARALLEL_R1_RL_REWARD}/train.parquet
  val_files: data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 32
  val_batch_size: null
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
critic:
  rollout_n: ${oc.select:actor_rollout_ref.rollout.n,1}
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
    tokenizer_path: ${oc.select:actor_rollout_ref.model.path,"~/models/deepseek-llm-7b-chat"}
    override_config: {}
    external_lib: ${oc.select:actor_rollout_ref.model.external_lib,null}
    enable_gradient_checkpointing: true
    trust_remote_code: ${oc.select:actor_rollout_ref.model.trust_remote_code,false}
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
  ppo_mini_batch_size: ${oc.select:actor_rollout_ref.actor.ppo_mini_batch_size,256}
  ppo_micro_batch_size: null
  ppo_micro_batch_size_per_gpu: ${oc.select:.ppo_micro_batch_size,null}
  use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
  ppo_max_token_len_per_gpu: 32768
  forward_max_token_len_per_gpu: ${.ppo_max_token_len_per_gpu}
  ppo_epochs: ${oc.select:actor_rollout_ref.actor.ppo_epochs,1}
  shuffle: ${oc.select:actor_rollout_ref.actor.shuffle,false}
  cliprange_value: 0.5
  loss_agg_mode: ${oc.select:actor_rollout_ref.actor.loss_agg_mode,token-mean}
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents: ${.save_contents}
  profiler:
    _target_: verl.utils.profiler.ProfilerConfig
    discrete: false
    all_ranks: false
    ranks: []
  _target_: verl.trainer.config.FSDPCriticConfig
  forward_micro_batch_size: ${oc.select:.ppo_micro_batch_size,null}
  forward_micro_batch_size_per_gpu: ${oc.select:.ppo_micro_batch_size_per_gpu,null}
  ulysses_sequence_parallel_size: 1
  grad_clip: 1.0
reward_model:
  enable: false
  strategy: fsdp
  model:
    input_tokenizer: ${actor_rollout_ref.model.path}
    path: ~/models/FsfairX-LLaMA3-RM-v0.1
    external_lib: ${actor_rollout_ref.model.external_lib}
    trust_remote_code: false
    use_shm: false
    use_remove_padding: false
    use_fused_kernels: ${actor_rollout_ref.model.use_fused_kernels}
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
  use_dynamic_bsz: ${critic.use_dynamic_bsz}
  forward_max_token_len_per_gpu: ${critic.forward_max_token_len_per_gpu}
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
  path: null
  name: compute_score
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

- [exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/hydra.yaml](../artifacts/exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${oc.env:PARALLEL_R1_RL_DIR}/hydra
  sweep:
    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}
  launcher:
    _target_: hydra._internal.core_plugins.basic_launcher.BasicLauncher
  sweeper:
    _target_: hydra._internal.core_plugins.basic_sweeper.BasicSweeper
    max_batch_size: null
    params: null
  help:
    app_name: ${hydra.job.name}
    header: '${hydra.help.app_name} is powered by Hydra.

      '
    footer: 'Powered by Hydra (https://hydra.cc)

      Use --hydra-help to view Hydra specific help

      '
    template: '${hydra.help.header}

      == Configuration groups ==

      Compose your configuration from those groups (group=option)


      $APP_CONFIG_GROUPS


      == Config ==

      Override anything in the config (foo.bar=value)


      $CONFIG


      ${hydra.help.footer}

      '
  hydra_help:
    template: 'Hydra (${hydra.runtime.version})

      See https://hydra.cc for more info.


      == Flags ==

      $FLAGS_HELP


      == Configuration groups ==

      Compose your configuration from those groups (For example, append hydra/job_logging=disabled
      to command line)


      $HYDRA_CONFIG_GROUPS


      Use ''--cfg hydra'' to Show the Hydra config.

      '
    hydra_help: ???
  hydra_logging:
    version: 1
    formatters:
      simple:
        format: '[%(asctime)s][HYDRA] %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple
        stream: ext://sys.stdout
    root:
      level: INFO
      handlers:
      - console
    loggers:
      logging_example:
        level: DEBUG
    disable_existing_loggers: false
  job_logging:
    version: 1
    formatters:
      simple:
        format: '[%(asctime)s][%(name)s][%(levelname)s] - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple
        stream: ext://sys.stdout
      file:
        class: logging.FileHandler
        formatter: simple
        filename: ${hydra.runtime.output_dir}/${hydra.job.name}.log
    root:
      level: INFO
      handlers:
      - console
      - file
    disable_existing_loggers: false
  env: {}
  mode: RUN
  searchpath: []
  callbacks: {}
  output_subdir: .hydra
  overrides:
    hydra:
    - hydra.mode=RUN
    task:
    - trainer.n_gpus_per_node=8
    - ray_init.num_cpus=64
    - +ray_init.temp_dir=${PROJECT_ROOT}
    - +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
    - +ray_init.object_store_memory=8589934592
    - data.train_batch_size=32
    - actor_rollout_ref.actor.ppo_mini_batch_size=16
    - actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2
    - actor_rollout_ref.actor.loss_agg_mode=token-mean
    - actor_rollout_ref.actor.sort_microbatches_by_length=false
    - actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4
    - actor_rollout_ref.rollout.agent.num_workers=32
    - trainer.val_before_train=false
    - actor_rollout_ref.model.use_fused_kernels=true
    - actor_rollout_ref.model.fused_kernel_options.impl_backend=triton
    - ++actor_rollout_ref.actor.sort_logprob_rows_by_length=true
    - ++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true
    - ++actor_rollout_ref.actor.defer_gradient_sync=true
    - actor_rollout_ref.actor.clip_ratio_high=0.2
    - actor_rollout_ref.rollout.max_num_seqs=64
    - ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=FULL_SHARD
    - ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=false
    - trainer.test_freq=50
    - trainer.resume_mode=resume_path
    - trainer.resume_from_path=${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=FULL_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=false,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.clip_ratio_high=0.2,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,data.train_batch_size=32,ray_init.num_cpus=64,trainer.n_gpus_per_node=8,trainer.resume_from_path=${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90,trainer.resume_mode=resume_path,trainer.test_freq=50,trainer.val_before_train=false
    id: ???
    num: ???
    config_name: rl_qwen3_06b
    env_set: {}
    env_copy: []
    config:
      override_dirname:
        kv_sep: '='
        item_sep: ','
        exclude_keys: []
  runtime:
    version: 1.3.2
    version_base: '1.3'
    cwd: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/hydra
    choices:
      hydra/env: default
      hydra/callbacks: null
      hydra/job_logging: default
      hydra/hydra_logging: default
      hydra/hydra_help: default
      hydra/help: default
      hydra/sweeper: basic
      hydra/launcher: basic
      hydra/output: default
  verbose: false

```

</details>

- [exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/overrides.yaml](../artifacts/exps/rl-unseen-s1-bs32-20261007/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- trainer.n_gpus_per_node=8
- ray_init.num_cpus=64
- +ray_init.temp_dir=${PROJECT_ROOT}
- +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
- +ray_init.object_store_memory=8589934592
- data.train_batch_size=32
- actor_rollout_ref.actor.ppo_mini_batch_size=16
- actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2
- actor_rollout_ref.actor.loss_agg_mode=token-mean
- actor_rollout_ref.actor.sort_microbatches_by_length=false
- actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4
- actor_rollout_ref.rollout.agent.num_workers=32
- trainer.val_before_train=false
- actor_rollout_ref.model.use_fused_kernels=true
- actor_rollout_ref.model.fused_kernel_options.impl_backend=triton
- ++actor_rollout_ref.actor.sort_logprob_rows_by_length=true
- ++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true
- ++actor_rollout_ref.actor.defer_gradient_sync=true
- actor_rollout_ref.actor.clip_ratio_high=0.2
- actor_rollout_ref.rollout.max_num_seqs=64
- ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=FULL_SHARD
- ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=false
- trainer.test_freq=50
- trainer.resume_mode=resume_path
- trainer.resume_from_path=${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_90

```

</details>

- [exps/rl-unseen-s1-bs32-20261007/validation-every10/manifest.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/validation-every10/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "run": "rl-unseen-s1-bs32-20261007",
  "commit": "b656ead",
  "base_commit": "ea3b07d74851739f2c8c41a88948ca8976b6b165",
  "stage": "s1",
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
  "steps": 300,
  "checkpoint": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
  "data_sha256": {
    "verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e",
    "verl/data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet": "8fd253319384ede4e436d24a4f2884a632e8b1e71e1ee4bc1951ecb68007cec1"
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
    "trainer.resume_mode=disable",
    "actor_rollout_ref.actor.clip_ratio_high=0.2",
    "actor_rollout_ref.rollout.max_num_seqs=64",
    "++actor_rollout_ref.actor.fsdp_config.sharding_strategy=FULL_SHARD",
    "++actor_rollout_ref.actor.skip_zero_advantage_microbatches=false"
  ],
  "extra_env": {
    "PARALLEL_R1_FULL_DECODE_GRAPH": "1",
    "VLLM_ATTENTION_BACKEND": "FLASH_ATTN",
    "CUDA_HOME": "${CUDA_HOME}",
    "PYTHONPATH": "${PROJECT_ROOT}/exps/rl-s1-seen-20261006-1112/flashinfer-deps",
    "PARALLEL_R1_GRAPH_CAPTURE_MIN_USES": "4"
  },
  "hypothesis": "Repeat the plotted Unseen-S1 from original Unseen-SFT with train batch32 rather than256, preserving n8 and two PPO minibatch updates per RL step via mini16 rather than128. Measure warmed wall time and responses/s; smaller batch is less work, not an algorithmic speedup.",
  "implementation_changes": [
    "User explicitly selected Unseen-S1 batch32, not Seen and not S2; fresh original Unseen-SFT, accuracy_reward, cliphigh0.2, LR1e-6,300steps.",
    "Batch256 to32; PPO mini128 to16 proportionally retains two minibatch optimizer updates; micro2, n8, token-mean and original structured masks/runtime tags retained.",
    "Match plotted S1 optimizer backend FULL_SHARD with deferred sync; S2 NO_SHARD and zero-advantage skip disabled to avoid conflating new optimizations with batch-size comparison.",
    "Use already validated late-S1 fused Triton head, independent logprob sorting, original-pair ordering, and exact decode graphs with capture minimum4; inference64 matches S1 effective admission.",
    "Same17917 DAPO train questions and1916 accuracy-only validation; save and validation every10, retain3; frozen snapshot b656ead with checked hashes.",
    "No optimizer/weights from S1 or S2 reused; baseline SFT validation already measured for the same checkpoint, not rerun before timing."
  ],
  "validation": [
    "All frozen changed-source and Parquet SHA256 verified before launch",
    "Hydra resolved config preflight",
    "Pending3-5 warm optimizer steps, first durable checkpoint and HF export"
  ],
  "resume_checkpoint": null,
  "source_comparison": "Unseen-S1 from the user graphs, exps/rl-unseen-s1-20261007-seq128; new independent start at original Unseen-SFT"
}
```

</details>

- [exps/rl-unseen-s1-bs32-20261007/validation-every10/resolved-config.yaml](../artifacts/exps/rl-unseen-s1-bs32-20261007/validation-every10/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.2
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
      sharding_strategy: FULL_SHARD
    sort_microbatches_by_length: false
    trim_parallel_padding: true
    sort_logprob_rows_by_length: true
    sort_microbatch_groups_by_length: true
    defer_gradient_sync: true
    skip_zero_advantage_microbatches: false
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
  total_training_steps: 300
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
  experiment_name: rl-unseen-s1-bs32-20261007
  logger:
  - console
  - wandb
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 10
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: false
  val_only: false
  test_freq: 10
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet
  val_files: data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 32
  val_batch_size: null
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
  path: null
  name: compute_score
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

## Метрики и полнота результатов

- [exps/rl-unseen-s1-bs32-20261007/STATUS.md](../artifacts/exps/rl-unseen-s1-bs32-20261007/STATUS.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/metrics.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/metrics.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/driver.log](../artifacts/exps/rl-unseen-s1-bs32-20261007/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-unseen-s1-bs32-20261007/quality-comparison-summary.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/quality-comparison-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "equal_time_snapshots": [
    {
      "budget_minutes": 41.788066347440086,
      "bs256": {
        "step": 10,
        "elapsed_minutes": 41.788066347440086,
        "math": 0.2911392405063291,
        "amc": 0.096875,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/validation/10.jsonl"
      },
      "bs32": {
        "step": 40,
        "elapsed_minutes": 39.816589923699695,
        "math": 0.24367088607594936,
        "amc": 0.1140625,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation/40.jsonl"
      },
      "math_delta_pp": -4.746835443037975,
      "amc_delta_pp": 1.7187499999999996
    },
    {
      "budget_minutes": 72.81484694083532,
      "bs256": {
        "step": 20,
        "elapsed_minutes": 72.81484694083532,
        "math": 0.2563291139240506,
        "amc": 0.1046875,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/validation/20.jsonl"
      },
      "bs32": {
        "step": 80,
        "elapsed_minutes": 66.7003340959549,
        "math": 0.2721518987341772,
        "amc": 0.1109375,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation/80.jsonl"
      },
      "math_delta_pp": 1.582278481012661,
      "amc_delta_pp": 0.6249999999999991
    },
    {
      "budget_minutes": 103.59534597794215,
      "bs256": {
        "step": 30,
        "elapsed_minutes": 103.59534597794215,
        "math": 0.2689873417721519,
        "amc": 0.11875,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/validation/30.jsonl"
      },
      "bs32": {
        "step": 100,
        "elapsed_minutes": 87.9754499355952,
        "math": 0.27531645569620256,
        "amc": 0.1171875,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation/100.jsonl"
      },
      "math_delta_pp": 0.6329113924050667,
      "amc_delta_pp": -0.15624999999999944
    },
    {
      "budget_minutes": 133.1401432911555,
      "bs256": {
        "step": 40,
        "elapsed_minutes": 133.1401432911555,
        "math": 0.27531645569620256,
        "amc": 0.1265625,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/validation/40.jsonl"
      },
      "bs32": {
        "step": 150,
        "elapsed_minutes": 113.75578198432922,
        "math": 0.310126582278481,
        "amc": 0.1265625,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation/150.jsonl"
      },
      "math_delta_pp": 3.4810126582278444,
      "amc_delta_pp": 0.0
    },
    {
      "budget_minutes": 156.48614013989766,
      "bs256": {
        "step": 50,
        "elapsed_minutes": 156.48614013989766,
        "math": 0.27531645569620256,
        "amc": 0.115625,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/validation/50.jsonl"
      },
      "bs32": {
        "step": 200,
        "elapsed_minutes": 138.22183198928832,
        "math": 0.3037974683544304,
        "amc": 0.1625,
        "artifact": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/validation/200.jsonl"
      },
      "math_delta_pp": 2.848101265822783,
      "amc_delta_pp": 4.6875
    }
  ]
}
```

</details>

- [exps/rl-unseen-s1-bs32-20261007/results/train.log](../artifacts/exps/rl-unseen-s1-bs32-20261007/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-unseen-s1-bs32-20261007/status.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-07T11:12:28.866241+00:00",
  "exit_code": 0
}
```

</details>

- [exps/rl-unseen-s1-bs32-20261007/validation-every10/driver.log](../artifacts/exps/rl-unseen-s1-bs32-20261007/validation-every10/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-unseen-s1-bs32-20261007/validation-every10/status.json](../artifacts/exps/rl-unseen-s1-bs32-20261007/validation-every10/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "observed_utc": "2026-10-07T08:01:22.031173+00:00",
  "steps": 300,
  "resume_checkpoint": null,
  "gpus": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7
  ]
}
```

</details>

## Графики

- [exps/rl-unseen-s1-bs32-20261007/charts/batch-comparison.png](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/batch-comparison.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/batch-comparison.svg](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/batch-comparison.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/current-rl.png](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/current-rl.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/current-rl.svg](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/current-rl.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/training-comparison.png](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/training-comparison.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/rl-unseen-s1-bs32-20261007/charts/training-comparison.svg](../artifacts/exps/rl-unseen-s1-bs32-20261007/charts/training-comparison.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [exps/rl-unseen-s1-bs32-20261007/run.py](../artifacts/exps/rl-unseen-s1-bs32-20261007/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
