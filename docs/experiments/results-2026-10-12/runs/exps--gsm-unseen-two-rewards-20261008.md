# exps/gsm-unseen-two-rewards-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/gsm-unseen-two-rewards-20261008/data-audit.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [exps/gsm-unseen-two-rewards-20261008/depth/resolved-config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 800
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
  experiment_name: gsm-unseen-two-rewards-20261008-depth
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
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

- [exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 800
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
  log_val_generations: 0
  rollout_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/rollouts
  validation_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/validation
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
  default_local_dir: ${oc.env:PARALLEL_R1_RL_DIR}/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
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

- [exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - actor_rollout_ref.actor.clip_ratio_high=0.28
    - actor_rollout_ref.rollout.max_num_seqs=64
    - ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
    - ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=800
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +custom_reward_function.reward_kwargs.mode=depth
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=depth,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.test_freq=50,trainer.total_training_steps=800,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/hydra
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

- [exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- actor_rollout_ref.actor.clip_ratio_high=0.28
- actor_rollout_ref.rollout.max_num_seqs=64
- ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
- ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=800
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +custom_reward_function.reward_kwargs.mode=depth

```

</details>

- [exps/gsm-unseen-two-rewards-20261008/manifest.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "run": "gsm-unseen-two-rewards-20261008",
  "commit": "b656ead",
  "base_commit": "ea3b07d74851739f2c8c41a88948ca8976b6b165",
  "stage": "s2",
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
  "steps": 800,
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
    "data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet",
    "data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet",
    "data.val_batch_size=256",
    "data.shuffle=true",
    "++data.seed=20261008",
    "trainer.resume_mode=disable",
    "trainer.save_freq=100",
    "trainer.test_freq=50",
    "trainer.total_training_steps=800",
    "trainer.max_actor_ckpt_to_keep=2",
    "trainer.logger=[console]",
    "actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]",
    "actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]",
    "custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py",
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
  "hypothesis": "Matched GSM-Infinite RL: original S2 versus correctness indicator minus critical generation depth; each independently starts from original Unseen SFT.",
  "checkpoint_policy": {
    "save_every": 100,
    "retain": 2,
    "full_training_state": true,
    "hf_weights": true
  },
  "stages": [
    "s2",
    "depth"
  ],
  "lambda_per_decode_depth": 0.0001,
  "stage_initialization": "Each starts independently from original Unseen SFT; retry resumes only its own full checkpoint.",
  "depth_definition": "Sum of generated main/summary token counts plus maximum generated path token count per fork. Excludes injected tags and prefill compute; not physical batched GPU forwards.",
  "max_attempts_per_stage": 3,
  "stall_timeout_seconds": 2700,
  "stage_attempt_timeout_seconds": 86400
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/s2/resolved-config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 800
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
  experiment_name: gsm-unseen-two-rewards-20261008-s2
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    mode: s2
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

- [exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 800
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
  log_val_generations: 0
  rollout_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/rollouts
  validation_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/validation
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
  default_local_dir: ${oc.env:PARALLEL_R1_RL_DIR}/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    mode: s2
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

- [exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - actor_rollout_ref.actor.clip_ratio_high=0.28
    - actor_rollout_ref.rollout.max_num_seqs=64
    - ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
    - ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=800
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +custom_reward_function.reward_kwargs.mode=s2
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=s2,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.test_freq=50,trainer.total_training_steps=800,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/hydra
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

- [exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- actor_rollout_ref.actor.clip_ratio_high=0.28
- actor_rollout_ref.rollout.max_num_seqs=64
- ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
- ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=800
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +custom_reward_function.reward_kwargs.mode=s2

```

</details>

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/resolved-config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 2
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
  experiment_name: gsm-unseen-two-rewards-20261008-smoke-depth
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 2
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: false
  val_only: false
  test_freq: 2
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
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

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 2
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
  log_val_generations: 0
  rollout_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/rollouts
  validation_data_dir: ${oc.env:PARALLEL_R1_RL_DIR}/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 2
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: false
  val_only: false
  test_freq: 2
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${oc.env:PARALLEL_R1_RL_DIR}/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
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

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - actor_rollout_ref.actor.clip_ratio_high=0.28
    - actor_rollout_ref.rollout.max_num_seqs=64
    - ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
    - ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=800
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +custom_reward_function.reward_kwargs.mode=depth
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=depth,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.save_freq=2,trainer.test_freq=2,trainer.test_freq=50,trainer.total_training_steps=2,trainer.total_training_steps=800,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra
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

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- actor_rollout_ref.actor.clip_ratio_high=0.28
- actor_rollout_ref.rollout.max_num_seqs=64
- ++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD
- ++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=800
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +custom_reward_function.reward_kwargs.mode=depth
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet

```

</details>

- [exps/gsm-unseen-two-rewards-20261008/smoke-s2/resolved-config.yaml](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-s2/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 2
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
  experiment_name: gsm-unseen-two-rewards-20261008-smoke-s2
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-s2/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-s2/results/validation
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: 2
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: false
  val_only: false
  test_freq: 2
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-s2/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    mode: s2
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

- [exps/gsm-unseen-two-rewards-20261008/bootstrap-status.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/bootstrap-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-08T04:07:12.205837+00:00"
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/depth/driver-attempt-1.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/depth/final-verification.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 800,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/checkpoints/global_step_800/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "APO_MATH300": {
      "acc": 0.10443037974683544,
      "critical_depth": 5.512658227848101,
      "parallel": 0.0,
      "forks": 0.0,
      "format_ok": 1.0,
      "answers": 316
    },
    "gsm_infinite_heldout": {
      "acc": 0.83984375,
      "critical_depth": 5.0625,
      "parallel": 0.0,
      "forks": 0.0,
      "format_ok": 1.0,
      "answers": 256
    }
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/depth/results/train.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/depth/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/monitoring-20261008-0219-msk.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/monitoring-20261008-0219-msk.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_utc": "2026-10-07T23:19:25.797401+00:00",
  "stage": "s2",
  "step": 279,
  "target_steps": 800,
  "attempt": 1,
  "queued": [
    "depth"
  ],
  "owned_bootstrap_controller_launcher_alive": true,
  "gpu_count": 8,
  "full_nonempty_checkpoint_steps": [
    100,
    200
  ],
  "validation": [
    {
      "step": 50,
      "rows": 572,
      "gsm_correct": 70,
      "gsm_n": 256,
      "math_correct": 96,
      "math_n": 316,
      "gsm_depth": 539.3203125,
      "gsm_parallel": 0.91796875,
      "gsm_forks": 1.62890625
    },
    {
      "step": 100,
      "rows": 572,
      "gsm_correct": 114,
      "gsm_n": 256,
      "math_correct": 93,
      "math_n": 316,
      "gsm_depth": 513.91015625,
      "gsm_parallel": 0.671875,
      "gsm_forks": 0.9921875
    },
    {
      "step": 150,
      "rows": 572,
      "gsm_correct": 134,
      "gsm_n": 256,
      "math_correct": 101,
      "math_n": 316,
      "gsm_depth": 422.21875,
      "gsm_parallel": 0.94921875,
      "gsm_forks": 1.41796875
    },
    {
      "step": 200,
      "rows": 572,
      "gsm_correct": 154,
      "gsm_n": 256,
      "math_correct": 97,
      "math_n": 316,
      "gsm_depth": 417.86328125,
      "gsm_parallel": 0.97265625,
      "gsm_forks": 1.375
    },
    {
      "step": 250,
      "rows": 572,
      "gsm_correct": 182,
      "gsm_n": 256,
      "math_correct": 113,
      "math_n": 316,
      "gsm_depth": 315.2109375,
      "gsm_parallel": 0.96875,
      "gsm_forks": 0.9765625,
      "gsm_format_ok": 1.0
    }
  ],
  "train_last20": {
    "rows": 5120,
    "groups": 640,
    "mixed_accuracy_fraction": 0.5390625,
    "acc": 0.75390625,
    "format_ok": 0.9982421875,
    "top_prediction_fraction": 0.2099609375
  },
  "train_first50": {
    "response_tokens": 672.4884,
    "critical_depth": 581.1609,
    "forks": 1.8828,
    "entropy": 0.9826,
    "grad_norm": 1.0452,
    "step_seconds_including_eval_save": 32.861
  },
  "train_last50": {
    "response_tokens": 400.4225,
    "critical_depth": 361.6069,
    "forks": 0.968,
    "entropy": 0.4166,
    "grad_norm": 1.2035,
    "step_seconds_including_eval_save": 22.8011
  },
  "nonfinite_training_metrics": [],
  "log_issue": "NFS temporary directory cleanup OSError Errno 16 in multiprocessing finalizers; ongoing progress, no restart or OOM. Keep observing, do not mutate frozen run.",
  "decision": "Continue original S2 then depth queue unchanged. Held-out GSM improvement is sustained across five evaluations; no constant-answer collapse. Fork count is falling toward one despite high parallel usage, so do not claim S2 increases block count. MATH fluctuations are not evidence of degradation. No basis to replace dataset now.",
  "eta": "S2 remaining about 3.3-3.6 hours at observed completed-cycle throughput, roughly 05:40-06:00 MSK. Second 800-step run has not started; its completion time remains uncertain."
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/monitoring-20261008-0839-msk.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/monitoring-20261008-0839-msk.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-two-rewards-20261008/report.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "s2": {
    "complete": true,
    "steps": 800,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/checkpoints/global_step_800/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "APO_MATH300": {
        "acc": 0.3924050632911392,
        "critical_depth": 621.9367088607595,
        "parallel": 0.8037974683544303,
        "forks": 0.8037974683544303,
        "format_ok": 0.9841772151898734,
        "answers": 316
      },
      "gsm_infinite_heldout": {
        "acc": 0.91796875,
        "critical_depth": 376.3125,
        "parallel": 0.953125,
        "forks": 0.953125,
        "format_ok": 1.0,
        "answers": 256
      }
    }
  },
  "depth": {
    "complete": true,
    "steps": 800,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/depth/results/checkpoints/global_step_800/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "APO_MATH300": {
        "acc": 0.10443037974683544,
        "critical_depth": 5.512658227848101,
        "parallel": 0.0,
        "forks": 0.0,
        "format_ok": 1.0,
        "answers": 316
      },
      "gsm_infinite_heldout": {
        "acc": 0.83984375,
        "critical_depth": 5.0625,
        "parallel": 0.0,
        "forks": 0.0,
        "format_ok": 1.0,
        "answers": 256
      }
    }
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/reward-analysis.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward-analysis.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "training": {
    "s2": "800 records; see original artifact",
    "depth": "800 records; see original artifact"
  },
  "counterfactual": {
    "original": {
      "all_wrong": {
        "groups": 84,
        "active_fraction": 0.6428571428571429,
        "mean_abs_adv": 0.47617891405868695,
        "mean_reward_std": 0.011729451777248056
      },
      "mixed": {
        "groups": 179,
        "active_fraction": 1,
        "mean_abs_adv": 0.7763975734446614,
        "mean_reward_std": 0.4451294226895598
      },
      "all_correct": {
        "groups": 25,
        "active_fraction": 0.32,
        "mean_abs_adv": 0.2336094459192569,
        "mean_reward_std": 0.0015287377189440584
      }
    },
    "lambda_1e-5": {
      "all_wrong": {
        "groups": 84,
        "active_fraction": 0.6428571428571429,
        "mean_abs_adv": 0.47557677036467527,
        "mean_reward_std": 0.0011729451777248055
      },
      "mixed": {
        "groups": 179,
        "active_fraction": 1,
        "mean_abs_adv": 0.7769882383759212,
        "mean_reward_std": 0.4440794920043302
      },
      "all_correct": {
        "groups": 25,
        "active_fraction": 0.32,
        "mean_abs_adv": 0.232948613772906,
        "mean_reward_std": 0.0001528737718944052
      }
    },
    "lambda_1e-6": {
      "all_wrong": {
        "groups": 84,
        "active_fraction": 0.6428571428571429,
        "mean_abs_adv": 0.4699903236913813,
        "mean_reward_std": 0.00011729451777248055
      },
      "mixed": {
        "groups": 179,
        "active_fraction": 1,
        "mean_abs_adv": 0.776994453156668,
        "mean_reward_std": 0.44400570540927903
      },
      "all_correct": {
        "groups": 25,
        "active_fraction": 0.32,
        "mean_abs_adv": 0.22664550818429413,
        "mean_reward_std": 1.5287377189440503e-05
      }
    },
    "correct_only": {
      "all_wrong": {
        "groups": 84,
        "active_fraction": 0,
        "mean_abs_adv": 0.0,
        "mean_reward_std": 0.0
      },
      "mixed": {
        "groups": 179,
        "active_fraction": 1,
        "mean_abs_adv": 0.7769233460048736,
        "mean_reward_std": 0.4295565675544002
      },
      "all_correct": {
        "groups": 25,
        "active_fraction": 0.32,
        "mean_abs_adv": 0.2336094459192569,
        "mean_reward_std": 0.0015287377189440584
      }
    },
    "correct_only_no_std": {
      "all_wrong": {
        "groups": 84,
        "active_fraction": 0,
        "mean_abs_adv": 0.0,
        "mean_reward_std": 0.0
      },
      "mixed": {
        "groups": 179,
        "active_fraction": 1,
        "mean_abs_adv": 0.34368612081005584,
        "mean_reward_std": 0.4295565675544002
      },
      "all_correct": {
        "groups": 25,
        "active_fraction": 0.32,
        "mean_abs_adv": 0.0010736249999999997,
        "mean_reward_std": 0.0015287377189440584
      }
    }
  },
  "counterfactual_sampling": {
    "steps": [
      1,
      5,
      10,
      20,
      30,
      40,
      50,
      75,
      100
    ],
    "responses": 2304,
    "groups": 288,
    "interpretation": "Offline rewards and advantages on fixed original trajectories, not retrained outcomes."
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/s2/driver-attempt-1.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/s2/final-verification.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 800,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/s2/results/checkpoints/global_step_800/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "APO_MATH300": {
      "acc": 0.3924050632911392,
      "critical_depth": 621.9367088607595,
      "parallel": 0.8037974683544303,
      "forks": 0.8037974683544303,
      "format_ok": 0.9841772151898734,
      "answers": 316
    },
    "gsm_infinite_heldout": {
      "acc": 0.91796875,
      "critical_depth": 376.3125,
      "parallel": 0.953125,
      "forks": 0.953125,
      "format_ok": 1.0,
      "answers": 256
    }
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/s2/results/train.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/s2/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/driver-attempt-1.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/final-verification.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 2,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/checkpoints/global_step_2/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "gsm_infinite_heldout": {
      "acc": 0.0,
      "critical_depth": 482.75,
      "parallel": 1.0,
      "forks": 2.125,
      "format_ok": 0.75,
      "answers": 8
    }
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/train.log](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-two-rewards-20261008/smoke-report.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "depth": {
    "complete": true,
    "steps": 2,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008/smoke-depth/results/checkpoints/global_step_2/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "gsm_infinite_heldout": {
        "acc": 0.0,
        "critical_depth": 482.75,
        "parallel": 1.0,
        "forks": 2.125,
        "format_ok": 0.75,
        "answers": 8
      }
    }
  }
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/smoke-status.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/smoke-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-07T21:18:31.819453+00:00",
  "completed": [
    "depth"
  ]
}
```

</details>

- [exps/gsm-unseen-two-rewards-20261008/status.json](../artifacts/exps/gsm-unseen-two-rewards-20261008/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-08T04:07:12.190610+00:00",
  "completed": [
    "s2",
    "depth"
  ]
}
```

</details>

## Графики

- [exps/gsm-unseen-two-rewards-20261008/reward-decomposition.png](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward-decomposition.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-two-rewards-20261008/reward-decomposition.svg](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward-decomposition.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-two-rewards-20261008/reward-outcomes.png](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward-outcomes.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-two-rewards-20261008/reward-outcomes.svg](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward-outcomes.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [exps/gsm-unseen-two-rewards-20261008/controller.py](../artifacts/exps/gsm-unseen-two-rewards-20261008/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-two-rewards-20261008/prepare_data.py](../artifacts/exps/gsm-unseen-two-rewards-20261008/prepare_data.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-two-rewards-20261008/reward.py](../artifacts/exps/gsm-unseen-two-rewards-20261008/reward.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-two-rewards-20261008/setup.py](../artifacts/exps/gsm-unseen-two-rewards-20261008/setup.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
