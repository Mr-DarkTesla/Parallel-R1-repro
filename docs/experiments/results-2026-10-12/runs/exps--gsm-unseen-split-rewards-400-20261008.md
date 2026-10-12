# exps/gsm-unseen-split-rewards-400-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/gsm-unseen-split-rewards-400-20261008/data-audit.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/resolved-config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 400
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
  experiment_name: gsm-unseen-split-rewards-400-20261008-gated_depth
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: gated_depth
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 400
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
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: gated_depth
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=400
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +algorithm.split_accuracy_aux=true
    - +custom_reward_function.reward_kwargs.bonus_alpha=0.2
    - +custom_reward_function.reward_kwargs.mode=gated_depth
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+algorithm.split_accuracy_aux=true,+custom_reward_function.reward_kwargs.bonus_alpha=0.2,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=gated_depth,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${PROJECT_ROOT},actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.test_freq=50,trainer.total_training_steps=400,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra
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

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=400
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +algorithm.split_accuracy_aux=true
- +custom_reward_function.reward_kwargs.bonus_alpha=0.2
- +custom_reward_function.reward_kwargs.mode=gated_depth

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/manifest.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "run": "gsm-unseen-split-rewards-400-20261008",
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
  "steps": 400,
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
    "data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet",
    "data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet",
    "data.val_batch_size=256",
    "data.shuffle=true",
    "++data.seed=20261008",
    "trainer.resume_mode=disable",
    "trainer.save_freq=100",
    "trainer.test_freq=50",
    "trainer.total_training_steps=400",
    "trainer.max_actor_ckpt_to_keep=2",
    "trainer.logger=[console]",
    "actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]",
    "actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]",
    "custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py",
    "custom_reward_function.name=compute_score",
    "+custom_reward_function.reward_kwargs.depth_lambda=0.0001",
    "+algorithm.split_accuracy_aux=true",
    "+custom_reward_function.reward_kwargs.bonus_alpha=0.2"
  ],
  "extra_env": {
    "PARALLEL_R1_FULL_DECODE_GRAPH": "1",
    "VLLM_ATTENTION_BACKEND": "FLASH_ATTN",
    "CUDA_HOME": "${CUDA_HOME}",
    "PYTHONPATH": "${PROJECT_ROOT}/exps/rl-s1-seen-20261006-1112/flashinfer-deps",
    "PARALLEL_R1_GRAPH_CAPTURE_MIN_USES": "64"
  },
  "hypothesis": "Correctness-gated auxiliaries with accuracy-only standardization preserve coefficient scale and avoid all-wrong shortening gradients.",
  "checkpoint_policy": {
    "save_every": 100,
    "retain": 2,
    "full_training_state": true,
    "hf_weights": true
  },
  "stages": [
    "gated_depth",
    "parallel_gain"
  ],
  "lambda_per_decode_depth": 0.0001,
  "stage_initialization": "Each starts independently from original Unseen SFT; retry resumes only its own full checkpoint.",
  "depth_definition": "Sum of generated main/summary token counts plus maximum generated path token count per fork. Excludes injected tags and prefill compute; not physical batched GPU forwards.",
  "max_attempts_per_stage": 3,
  "stall_timeout_seconds": 2700,
  "stage_attempt_timeout_seconds": 86400,
  "parent_run": "${PROJECT_ROOT}/exps/gsm-unseen-two-rewards-20261008",
  "advantage_formula": "standardize_group(accuracy) + aux_reward - group_mean(aux_reward)",
  "reward_formulas": {
    "gated_depth": "c - 0.0001*c*D",
    "parallel_gain": "c + 0.2*c*valid_parallel*(1-D/T)"
  },
  "bonus_alpha": 0.2,
  "caveats": [
    "Gated depth cost can still favor short correct answers.",
    "Relative efficiency may reward extra tokens in parallel paths; audit total length and validation.",
    "Both are separate independent runs from original Unseen-SFT; not continuation of old RL."
  ]
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/resolved-config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 400
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
  experiment_name: gsm-unseen-split-rewards-400-20261008-parallel_gain
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: parallel_gain
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  total_training_steps: 400
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
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: parallel_gain
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=400
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +algorithm.split_accuracy_aux=true
    - +custom_reward_function.reward_kwargs.bonus_alpha=0.2
    - +custom_reward_function.reward_kwargs.mode=parallel_gain
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+algorithm.split_accuracy_aux=true,+custom_reward_function.reward_kwargs.bonus_alpha=0.2,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=parallel_gain,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${PROJECT_ROOT},actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.test_freq=50,trainer.total_training_steps=400,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra
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

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=400
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +algorithm.split_accuracy_aux=true
- +custom_reward_function.reward_kwargs.bonus_alpha=0.2
- +custom_reward_function.reward_kwargs.mode=parallel_gain

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/resolved-config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  experiment_name: gsm-unseen-split-rewards-400-20261008-smoke-gated_depth
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: gated_depth
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: gated_depth
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=400
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +algorithm.split_accuracy_aux=true
    - +custom_reward_function.reward_kwargs.bonus_alpha=0.2
    - +custom_reward_function.reward_kwargs.mode=gated_depth
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+algorithm.split_accuracy_aux=true,+custom_reward_function.reward_kwargs.bonus_alpha=0.2,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=gated_depth,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${PROJECT_ROOT},actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.save_freq=2,trainer.test_freq=2,trainer.test_freq=50,trainer.total_training_steps=2,trainer.total_training_steps=400,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra
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

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=400
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +algorithm.split_accuracy_aux=true
- +custom_reward_function.reward_kwargs.bonus_alpha=0.2
- +custom_reward_function.reward_kwargs.mode=gated_depth
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/resolved-config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  experiment_name: gsm-unseen-split-rewards-400-20261008-smoke-parallel_gain
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/rollouts
  validation_data_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/validation
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
  default_local_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/checkpoints
  max_actor_ckpt_to_keep: 2
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: parallel_gain
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/config.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  train_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
  val_files: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
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
  path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
  name: compute_score
  reward_kwargs:
    depth_lambda: 0.0001
    bonus_alpha: 0.2
    mode: parallel_gain
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
  split_accuracy_aux: true
ray_init:
  num_cpus: 64
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/hydra.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
    - data.val_batch_size=256
    - data.shuffle=true
    - ++data.seed=20261008
    - trainer.resume_mode=disable
    - trainer.save_freq=100
    - trainer.test_freq=50
    - trainer.total_training_steps=400
    - trainer.max_actor_ckpt_to_keep=2
    - trainer.logger=[console]
    - actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
    - actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
    - custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.depth_lambda=0.0001
    - +algorithm.split_accuracy_aux=true
    - +custom_reward_function.reward_kwargs.bonus_alpha=0.2
    - +custom_reward_function.reward_kwargs.mode=parallel_gain
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.actor.defer_gradient_sync=true,++actor_rollout_ref.actor.fsdp_config.sharding_strategy=NO_SHARD,++actor_rollout_ref.actor.skip_zero_advantage_microbatches=true,++actor_rollout_ref.actor.sort_logprob_rows_by_length=true,++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true,++data.seed=20261008,+algorithm.split_accuracy_aux=true,+custom_reward_function.reward_kwargs.bonus_alpha=0.2,+custom_reward_function.reward_kwargs.depth_lambda=0.0001,+custom_reward_function.reward_kwargs.mode=parallel_gain,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${PROJECT_ROOT},actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra],actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model],actor_rollout_ref.actor.clip_ratio_high=0.28,actor_rollout_ref.actor.loss_agg_mode=token-mean,actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2,actor_rollout_ref.actor.ppo_mini_batch_size=16,actor_rollout_ref.actor.sort_microbatches_by_length=false,actor_rollout_ref.model.fused_kernel_options.impl_backend=triton,actor_rollout_ref.model.use_fused_kernels=true,actor_rollout_ref.rollout.agent.num_workers=32,actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4,actor_rollout_ref.rollout.max_num_seqs=64,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py,data.shuffle=true,data.train_batch_size=32,data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet,data.val_batch_size=256,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet,data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet,ray_init.num_cpus=64,trainer.logger=[console],trainer.max_actor_ckpt_to_keep=2,trainer.n_gpus_per_node=8,trainer.resume_mode=disable,trainer.save_freq=100,trainer.save_freq=2,trainer.test_freq=2,trainer.test_freq=50,trainer.total_training_steps=2,trainer.total_training_steps=400,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra
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

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/overrides.yaml](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
- data.train_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/validation.parquet
- data.val_batch_size=256
- data.shuffle=true
- ++data.seed=20261008
- trainer.resume_mode=disable
- trainer.save_freq=100
- trainer.test_freq=50
- trainer.total_training_steps=400
- trainer.max_actor_ckpt_to_keep=2
- trainer.logger=[console]
- actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]
- actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]
- custom_reward_function.path=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/code/verl/verl/utils/reward_score/gsm_depth.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.depth_lambda=0.0001
- +algorithm.split_accuracy_aux=true
- +custom_reward_function.reward_kwargs.bonus_alpha=0.2
- +custom_reward_function.reward_kwargs.mode=parallel_gain
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- data.val_files=${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-validation.parquet

```

</details>

## Метрики и полнота результатов

- [exps/gsm-unseen-split-rewards-400-20261008/bootstrap-status.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/bootstrap-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-08T11:54:36.243900+00:00"
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/completed-snapshot-20261008.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/completed-snapshot-20261008.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/first-progress.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/first-progress.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": {
    "state": "running",
    "observed_utc": "2026-10-08T06:43:39.939908+00:00",
    "stage": "gated_depth",
    "attempt": 1,
    "step": 53,
    "target_steps": 400,
    "initialized_from": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
    "resumed_from": null,
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
    "queued": [
      "parallel_gain"
    ]
  },
  "smoke": {
    "gated_depth": {
      "complete": true,
      "steps": 2,
      "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/checkpoints/global_step_2/actor/huggingface",
      "full_state": true,
      "finite_weights": true,
      "finite_forward": true,
      "validation": {
        "gsm_infinite_heldout": {
          "acc": 0.25,
          "critical_depth": 670.25,
          "parallel": 1.0,
          "forks": 2.25,
          "format_ok": 1.0,
          "answers": 8
        }
      }
    },
    "parallel_gain": {
      "complete": true,
      "steps": 2,
      "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/checkpoints/global_step_2/actor/huggingface",
      "full_state": true,
      "finite_weights": true,
      "finite_forward": true,
      "validation": {
        "gsm_infinite_heldout": {
          "acc": 0.125,
          "critical_depth": 769.25,
          "parallel": 0.875,
          "forks": 1.375,
          "format_ok": 1.0,
          "answers": 8
        }
      }
    }
  },
  "last_metrics": {
    "reward/accuracy_mean": 0.28515625,
    "reward/aux_mean": -0.012938280589878559,
    "reward/total_mean": 0.2722179591655731,
    "advantage/accuracy_abs_mean": 0.615379273891449,
    "advantage/aux_abs_mean": 0.013816991820931435,
    "grpo/mixed_accuracy_group_fraction": 0.75,
    "actor/grad_norm": 1.0390875935554504,
    "response_length/mean": 553.234375,
    "parallel/critical_depth_mean": 465.55078125,
    "parallel/ratio": 0.984375,
    "parallel/forks_mean": 1.9921875,
    "timing_s/step": 22.444644312374294
  },
  "mean_last20": {
    "reward/accuracy_mean": 0.3318359375,
    "reward/aux_mean": -0.014545605378225445,
    "reward/total_mean": 0.3172903284430504,
    "advantage/accuracy_abs_mean": 0.6539158791303634,
    "advantage/aux_abs_mean": 0.014417412271723152,
    "grpo/mixed_accuracy_group_fraction": 0.809375,
    "actor/grad_norm": 1.081709823012352,
    "response_length/mean": 568.5548828125,
    "parallel/critical_depth_mean": 485.73671875,
    "parallel/ratio": 0.948828125,
    "parallel/forks_mean": 1.90234375,
    "timing_s/step": 26.073688519652933
  },
  "completed_steps": 53,
  "val50": {
    "APO_MATH300": {
      "rows": 316,
      "acc": 0.28164556962025317,
      "depth": 601.8322784810126,
      "parallel": 0.9683544303797469
    },
    "gsm_infinite_heldout": {
      "rows": 256,
      "acc": 0.35546875,
      "depth": 521.296875,
      "parallel": 0.953125
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/driver-attempt-1.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/final-verification.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 400,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/checkpoints/global_step_400/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "APO_MATH300": {
      "acc": 0.370253164556962,
      "critical_depth": 651.4841772151899,
      "parallel": 0.16455696202531644,
      "forks": 0.1930379746835443,
      "format_ok": 0.990506329113924,
      "answers": 316
    },
    "gsm_infinite_heldout": {
      "acc": 0.875,
      "critical_depth": 347.33203125,
      "parallel": 0.0078125,
      "forks": 0.0078125,
      "format_ok": 0.9921875,
      "answers": 256
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/train.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/latest-progress.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/latest-progress.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_utc": "2026-10-08T08:51:13.724035+00:00",
  "status": {
    "state": "running",
    "observed_utc": "2026-10-08T08:51:03.715338+00:00",
    "stage": "gated_depth",
    "attempt": 1,
    "step": 394,
    "target_steps": 400,
    "initialized_from": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
    "resumed_from": null,
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
    "queued": [
      "parallel_gain"
    ]
  },
  "bootstrap-status": {
    "state": "production",
    "observed_utc": "2026-10-08T06:13:01.076900+00:00"
  },
  "stages": {
    "gated_depth": {
      "attempt_logs": [
        "driver-attempt-1.log"
      ],
      "metric_steps": 394,
      "first50": {
        "actor/entropy": 0.9283148646354675,
        "actor/grad_norm": 1.0409876096248627,
        "actor/ppo_kl_active_microbatches": 8.875315967654847e-05,
        "grpo/informative_prompts": 25.24,
        "response_length/mean": 620.998515625,
        "parallel/critical_depth_mean": 533.419453125,
        "parallel/forks_mean": 1.96390625,
        "parallel/ratio": 0.945390625,
        "reward/accuracy_mean": 0.266015625,
        "reward/aux_mean": -0.012573179639875889,
        "advantage/accuracy_abs_mean": 0.6196119058132171,
        "advantage/aux_abs_mean": 0.01422415640205145,
        "response_length/clip_ratio": 0.00625,
        "timing_s/step": 30.431596245057882
      },
      "last50": {
        "actor/entropy": 0.15930498778820038,
        "actor/grad_norm": 0.7119229322671891,
        "actor/ppo_kl_active_microbatches": 2.8501350813125256e-06,
        "grpo/informative_prompts": 31.56,
        "response_length/mean": 430.001796875,
        "parallel/critical_depth_mean": 428.040859375,
        "parallel/forks_mean": 0.044375,
        "parallel/ratio": 0.041328125,
        "reward/accuracy_mean": 0.86359375,
        "reward/aux_mean": -0.03120531242340803,
        "advantage/accuracy_abs_mean": 0.2762395958602428,
        "advantage/aux_abs_mean": 0.01204934373497963,
        "response_length/clip_ratio": 0.01453125,
        "timing_s/step": 22.377956270556897
      },
      "last100": {
        "actor/entropy": 0.1683461521565914,
        "actor/grad_norm": 0.7304007384181023,
        "actor/ppo_kl_active_microbatches": 5.1044390411378276e-05,
        "grpo/informative_prompts": 31.4,
        "response_length/mean": 430.3970703125,
        "parallel/critical_depth_mean": 427.63203125,
        "parallel/forks_mean": 0.0604296875,
        "parallel/ratio": 0.05671875,
        "reward/accuracy_mean": 0.8441796875,
        "reward/aux_mean": -0.029882195368409158,
        "advantage/accuracy_abs_mean": 0.3037754002958536,
        "advantage/aux_abs_mean": 0.012014166992157698,
        "response_length/clip_ratio": 0.016484375,
        "timing_s/step": 23.481711212573572
      },
      "nonfinite": [],
      "error_counts": {
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964b039dacce00000c98'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89648037ec1d400000c99'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e02193f1100000c9b'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e02193f0f00000c9a'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964903bd7c0300000c9d'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964b03d72de300000c9c'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964a04c1209600000c9f'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964a04c1209800000c9e'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964a041ed26200000ca0'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964c0413712300000ca1'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89648037ef97400000ca2'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89649025d4bdc00000ca3'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89648030743b000000ca4'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89648030743a500000ca5'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e034ee2b800000ca7'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e034ee31600000ca6'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e03af4de900000ca8'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e03af4de400000ca9'": 1
      },
      "validation": [
        {
          "step": 50,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.28164556962025317,
              "critical_depth": 601.8322784810126,
              "parallel": 0.9683544303797469,
              "forks": 1.8006329113924051,
              "format_ok": 0.9683544303797469,
              "n": 316,
              "correct": 89,
              "top_predictions": [
                [
                  "1",
                  24
                ],
                [
                  "2",
                  20
                ],
                [
                  "4",
                  17
                ],
                [
                  "5",
                  14
                ],
                [
                  "3",
                  14
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.35546875,
              "critical_depth": 521.296875,
              "parallel": 0.953125,
              "forks": 1.9375,
              "format_ok": 0.95703125,
              "n": 256,
              "correct": 91,
              "top_predictions": [
                [
                  "2",
                  50
                ],
                [
                  "4",
                  41
                ],
                [
                  "3",
                  31
                ],
                [
                  "1",
                  29
                ],
                [
                  "5",
                  17
                ]
              ]
            }
          }
        },
        {
          "step": 100,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.3037974683544304,
              "critical_depth": 595.8449367088608,
              "parallel": 0.9873417721518988,
              "forks": 1.8417721518987342,
              "format_ok": 0.9778481012658228,
              "n": 316,
              "correct": 96,
              "top_predictions": [
                [
                  "1",
                  29
                ],
                [
                  "4",
                  26
                ],
                [
                  "2",
                  23
                ],
                [
                  "0",
                  18
                ],
                [
                  "3",
                  16
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.4140625,
              "critical_depth": 436.03515625,
              "parallel": 0.97265625,
              "forks": 1.93359375,
              "format_ok": 0.984375,
              "n": 256,
              "correct": 106,
              "top_predictions": [
                [
                  "4",
                  67
                ],
                [
                  "2",
                  51
                ],
                [
                  "1",
                  34
                ],
                [
                  "3",
                  29
                ],
                [
                  "6",
                  19
                ]
              ]
            }
          }
        },
        {
          "step": 150,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.28164556962025317,
              "critical_depth": 637.0727848101266,
              "parallel": 0.870253164556962,
              "forks": 1.4968354430379747,
              "format_ok": 0.9367088607594937,
              "n": 316,
              "correct": 89,
              "top_predictions": [
                [
                  "2",
                  27
                ],
                [
                  "3",
                  17
                ],
                [
                  "1",
                  17
                ],
                [
                  "0",
                  15
                ],
                [
                  "4",
                  14
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.5390625,
              "critical_depth": 476.77734375,
              "parallel": 0.83203125,
              "forks": 1.5,
              "format_ok": 0.890625,
              "n": 256,
              "correct": 138,
              "top_predictions": [
                [
                  "4",
                  58
                ],
                [
                  "2",
                  50
                ],
                [
                  "3",
                  34
                ],
                [
                  "1",
                  22
                ],
                [
                  "8",
                  21
                ]
              ]
            }
          }
        },
        {
          "step": 200,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.3670886075949367,
              "critical_depth": 636.4398734177215,
              "parallel": 0.870253164556962,
              "forks": 1.4367088607594938,
              "format_ok": 0.9588607594936709,
              "n": 316,
              "correct": 116,
              "top_predictions": [
                [
                  "4",
                  28
                ],
                [
                  "2",
                  25
                ],
                [
                  "1",
                  21
                ],
                [
                  "0",
                  17
                ],
                [
                  "6",
                  10
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.62890625,
              "critical_depth": 387.6015625,
              "parallel": 0.8515625,
              "forks": 1.52734375,
              "format_ok": 0.9609375,
              "n": 256,
              "correct": 161,
              "top_predictions": [
                [
                  "4",
                  60
                ],
                [
                  "2",
                  60
                ],
                [
                  "3",
                  36
                ],
                [
                  "1",
                  19
                ],
                [
                  "6",
                  17
                ]
              ]
            }
          }
        },
        {
          "step": 250,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.34810126582278483,
              "critical_depth": 611.0696202531645,
              "parallel": 0.7341772151898734,
              "forks": 1.1265822784810127,
              "format_ok": 0.9936708860759493,
              "n": 316,
              "correct": 110,
              "top_predictions": [
                [
                  "2",
                  29
                ],
                [
                  "1",
                  23
                ],
                [
                  "4",
                  18
                ],
                [
                  "3",
                  17
                ],
                [
                  "9",
                  13
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.70703125,
              "critical_depth": 457.00390625,
              "parallel": 0.62890625,
              "forks": 0.90234375,
              "format_ok": 0.96875,
              "n": 256,
              "correct": 181,
              "top_predictions": [
                [
                  "4",
                  53
                ],
                [
                  "2",
                  48
                ],
                [
                  "3",
                  41
                ],
                [
                  "1",
                  24
                ],
                [
                  "8",
                  21
                ]
              ]
            }
          }
        },
        {
          "step": 300,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.3575949367088608,
              "critical_depth": 585.2911392405064,
              "parallel": 0.37658227848101267,
              "forks": 0.48417721518987344,
              "format_ok": 0.9873417721518988,
              "n": 316,
              "correct": 113,
              "top_predictions": [
                [
                  "2",
                  29
                ],
                [
                  "1",
                  25
                ],
                [
                  "4",
                  23
                ],
                [
                  "3",
                  17
                ],
                [
                  "9",
                  10
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.74609375,
              "critical_depth": 391.11328125,
              "parallel": 0.1015625,
              "forks": 0.10546875,
              "format_ok": 1.0,
              "n": 256,
              "correct": 191,
              "top_predictions": [
                [
                  "2",
                  58
                ],
                [
                  "4",
                  50
                ],
                [
                  "3",
                  33
                ],
                [
                  "1",
                  24
                ],
                [
                  "8",
                  23
                ]
              ]
            }
          }
        },
        {
          "step": 350,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.3670886075949367,
              "critical_depth": 694.8227848101266,
              "parallel": 0.20569620253164558,
              "forks": 0.2310126582278481,
              "format_ok": 0.9841772151898734,
              "n": 316,
              "correct": 116,
              "top_predictions": [
                [
                  "1",
                  27
                ],
                [
                  "4",
                  26
                ],
                [
                  "2",
                  24
                ],
                [
                  "3",
                  14
                ],
                [
                  "6",
                  12
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.8515625,
              "critical_depth": 539.1875,
              "parallel": 0.0546875,
              "forks": 0.05859375,
              "format_ok": 0.99609375,
              "n": 256,
              "correct": 218,
              "top_predictions": [
                [
                  "4",
                  56
                ],
                [
                  "2",
                  54
                ],
                [
                  "3",
                  34
                ],
                [
                  "1",
                  22
                ],
                [
                  "6",
                  21
                ]
              ]
            }
          }
        }
      ],
      "last_rollout": 395,
      "recent20": {
        "rows": 5120,
        "groups": 640,
        "mixed_accuracy_fraction": 0.2953125,
        "acc": 0.8986328125,
        "format_ok": 0.9982421875,
        "top_predictions": [
          [
            "4",
            1065
          ],
          [
            "3",
            969
          ],
          [
            "2",
            924
          ],
          [
            "1",
            397
          ],
          [
            "8",
            372
          ]
        ]
      },
      "checkpoints": {
        "global_step_100": false,
        "global_step_200": true,
        "global_step_300": true
      },
      "final_verification": null
    },
    "parallel_gain": {
      "attempt_logs": [],
      "metric_steps": 0,
      "first50": {},
      "last50": {},
      "last100": {},
      "nonfinite": [],
      "error_counts": {},
      "validation": [],
      "last_rollout": null,
      "checkpoints": {},
      "final_verification": null
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/driver-attempt-1.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/final-verification.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 400,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/checkpoints/global_step_400/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "APO_MATH300": {
      "acc": 0.36075949367088606,
      "critical_depth": 710.5822784810126,
      "parallel": 0.9430379746835443,
      "forks": 1.1360759493670887,
      "format_ok": 0.9651898734177216,
      "answers": 316
    },
    "gsm_infinite_heldout": {
      "acc": 0.85546875,
      "critical_depth": 517.109375,
      "parallel": 0.95703125,
      "forks": 0.96484375,
      "format_ok": 0.98046875,
      "answers": 256
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/train.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-20261008-1008-msk.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-20261008-1008-msk.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_utc": "2026-10-08T07:08:39.790776+00:00",
  "status": {
    "state": "running",
    "observed_utc": "2026-10-08T07:08:38.603359+00:00",
    "stage": "gated_depth",
    "attempt": 1,
    "step": 122,
    "target_steps": 400,
    "initialized_from": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final",
    "resumed_from": null,
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
    "queued": [
      "parallel_gain"
    ]
  },
  "bootstrap-status": {
    "state": "production",
    "observed_utc": "2026-10-08T06:13:01.076900+00:00"
  },
  "stages": {
    "gated_depth": {
      "attempt_logs": [
        "driver-attempt-1.log"
      ],
      "metric_steps": 122,
      "first50": {
        "actor/entropy": 0.9283148646354675,
        "actor/grad_norm": 1.0409876096248627,
        "actor/ppo_kl_active_microbatches": 8.875315967654847e-05,
        "grpo/informative_prompts": 25.24,
        "response_length/mean": 620.998515625,
        "parallel/critical_depth_mean": 533.419453125,
        "parallel/forks_mean": 1.96390625,
        "parallel/ratio": 0.945390625,
        "reward/accuracy_mean": 0.266015625,
        "reward/aux_mean": -0.012573179639875889,
        "advantage/accuracy_abs_mean": 0.6196119058132171,
        "advantage/aux_abs_mean": 0.01422415640205145,
        "response_length/clip_ratio": 0.00625,
        "timing_s/step": 30.431596245057882
      },
      "last50": {
        "actor/entropy": 0.7031633150577545,
        "actor/grad_norm": 1.0858524233102798,
        "actor/ppo_kl_active_microbatches": 1.0671092107659636e-05,
        "grpo/informative_prompts": 27.82,
        "response_length/mean": 526.168359375,
        "parallel/critical_depth_mean": 446.58421875,
        "parallel/forks_mean": 1.85265625,
        "parallel/ratio": 0.957421875,
        "reward/accuracy_mean": 0.4353125,
        "reward/aux_mean": -0.018066452983766794,
        "advantage/accuracy_abs_mean": 0.658414409160614,
        "advantage/aux_abs_mean": 0.014350367225706578,
        "response_length/clip_ratio": 0.0021875,
        "timing_s/step": 21.171668419856577
      },
      "last100": {
        "actor/entropy": 0.7736296784877777,
        "actor/grad_norm": 1.0797825542092323,
        "actor/ppo_kl_active_microbatches": 5.3491995290385346e-05,
        "grpo/informative_prompts": 27.2,
        "response_length/mean": 551.287890625,
        "parallel/critical_depth_mean": 470.3672265625,
        "parallel/forks_mean": 1.866796875,
        "parallel/ratio": 0.9492578125,
        "reward/accuracy_mean": 0.3803125,
        "reward/aux_mean": -0.01626486317254603,
        "advantage/accuracy_abs_mean": 0.6551885533332825,
        "advantage/aux_abs_mean": 0.014435755899176,
        "response_length/clip_ratio": 0.0033984375,
        "timing_s/step": 23.249106349535285
      },
      "nonfinite": [],
      "error_counts": {
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964b039dacce00000c98'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f89648037ec1d400000c99'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e02193f1100000c9b'": 1,
        "OSError: [Errno 16] Device or resource busy: '.nfs80f8964e02193f0f00000c9a'": 1
      },
      "validation": [
        {
          "step": 50,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.28164556962025317,
              "critical_depth": 601.8322784810126,
              "parallel": 0.9683544303797469,
              "forks": 1.8006329113924051,
              "format_ok": 0.9683544303797469,
              "n": 316,
              "correct": 89,
              "top_predictions": [
                [
                  "1",
                  24
                ],
                [
                  "2",
                  20
                ],
                [
                  "4",
                  17
                ],
                [
                  "5",
                  14
                ],
                [
                  "3",
                  14
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.35546875,
              "critical_depth": 521.296875,
              "parallel": 0.953125,
              "forks": 1.9375,
              "format_ok": 0.95703125,
              "n": 256,
              "correct": 91,
              "top_predictions": [
                [
                  "2",
                  50
                ],
                [
                  "4",
                  41
                ],
                [
                  "3",
                  31
                ],
                [
                  "1",
                  29
                ],
                [
                  "5",
                  17
                ]
              ]
            }
          }
        },
        {
          "step": 100,
          "rows": 572,
          "sources": {
            "APO_MATH300": {
              "acc": 0.3037974683544304,
              "critical_depth": 595.8449367088608,
              "parallel": 0.9873417721518988,
              "forks": 1.8417721518987342,
              "format_ok": 0.9778481012658228,
              "n": 316,
              "correct": 96,
              "top_predictions": [
                [
                  "1",
                  29
                ],
                [
                  "4",
                  26
                ],
                [
                  "2",
                  23
                ],
                [
                  "0",
                  18
                ],
                [
                  "3",
                  16
                ]
              ]
            },
            "gsm_infinite_heldout": {
              "acc": 0.4140625,
              "critical_depth": 436.03515625,
              "parallel": 0.97265625,
              "forks": 1.93359375,
              "format_ok": 0.984375,
              "n": 256,
              "correct": 106,
              "top_predictions": [
                [
                  "4",
                  67
                ],
                [
                  "2",
                  51
                ],
                [
                  "1",
                  34
                ],
                [
                  "3",
                  29
                ],
                [
                  "6",
                  19
                ]
              ]
            }
          }
        }
      ],
      "last_rollout": 122,
      "recent20": {
        "rows": 5120,
        "groups": 640,
        "mixed_accuracy_fraction": 0.8015625,
        "acc": 0.465625,
        "format_ok": 0.95546875,
        "top_predictions": [
          [
            "4",
            1007
          ],
          [
            "3",
            911
          ],
          [
            "2",
            858
          ],
          [
            "1",
            464
          ],
          [
            "6",
            415
          ]
        ]
      },
      "checkpoints": {
        "global_step_100": true
      },
      "final_verification": null
    },
    "parallel_gain": {
      "attempt_logs": [],
      "metric_steps": 0,
      "first50": {},
      "last50": {},
      "last100": {},
      "nonfinite": [],
      "error_counts": {},
      "validation": [],
      "last_rollout": null,
      "checkpoints": {},
      "final_verification": null
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/report.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "gated_depth": {
    "complete": true,
    "steps": 400,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/gated_depth/results/checkpoints/global_step_400/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "APO_MATH300": {
        "acc": 0.370253164556962,
        "critical_depth": 651.4841772151899,
        "parallel": 0.16455696202531644,
        "forks": 0.1930379746835443,
        "format_ok": 0.990506329113924,
        "answers": 316
      },
      "gsm_infinite_heldout": {
        "acc": 0.875,
        "critical_depth": 347.33203125,
        "parallel": 0.0078125,
        "forks": 0.0078125,
        "format_ok": 0.9921875,
        "answers": 256
      }
    }
  },
  "parallel_gain": {
    "complete": true,
    "steps": 400,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/parallel_gain/results/checkpoints/global_step_400/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "APO_MATH300": {
        "acc": 0.36075949367088606,
        "critical_depth": 710.5822784810126,
        "parallel": 0.9430379746835443,
        "forks": 1.1360759493670887,
        "format_ok": 0.9651898734177216,
        "answers": 316
      },
      "gsm_infinite_heldout": {
        "acc": 0.85546875,
        "critical_depth": 517.109375,
        "parallel": 0.95703125,
        "forks": 0.96484375,
        "format_ok": 0.98046875,
        "answers": 256
      }
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/driver-attempt-1.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/final-verification.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 2,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/checkpoints/global_step_2/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "gsm_infinite_heldout": {
      "acc": 0.25,
      "critical_depth": 670.25,
      "parallel": 1.0,
      "forks": 2.25,
      "format_ok": 1.0,
      "answers": 8
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/train.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/driver-attempt-1.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/driver-attempt-1.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/final-verification.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/final-verification.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "steps": 2,
  "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/checkpoints/global_step_2/actor/huggingface",
  "full_state": true,
  "finite_weights": true,
  "finite_forward": true,
  "validation": {
    "gsm_infinite_heldout": {
      "acc": 0.125,
      "critical_depth": 769.25,
      "parallel": 0.875,
      "forks": 1.375,
      "format_ok": 1.0,
      "answers": 8
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/train.log](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/train.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-report.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "gated_depth": {
    "complete": true,
    "steps": 2,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-gated_depth/results/checkpoints/global_step_2/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "gsm_infinite_heldout": {
        "acc": 0.25,
        "critical_depth": 670.25,
        "parallel": 1.0,
        "forks": 2.25,
        "format_ok": 1.0,
        "answers": 8
      }
    }
  },
  "parallel_gain": {
    "complete": true,
    "steps": 2,
    "hf_model": "${PROJECT_ROOT}/exps/gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain/results/checkpoints/global_step_2/actor/huggingface",
    "full_state": true,
    "finite_weights": true,
    "finite_forward": true,
    "validation": {
      "gsm_infinite_heldout": {
        "acc": 0.125,
        "critical_depth": 769.25,
        "parallel": 0.875,
        "forks": 1.375,
        "format_ok": 1.0,
        "answers": 8
      }
    }
  }
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/smoke-status.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/smoke-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-08T06:13:01.063524+00:00",
  "completed": [
    "gated_depth",
    "parallel_gain"
  ]
}
```

</details>

- [exps/gsm-unseen-split-rewards-400-20261008/status.json](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-08T11:54:36.230492+00:00",
  "completed": [
    "gated_depth",
    "parallel_gain"
  ]
}
```

</details>

## Графики

- [exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step246.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step246.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step369.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step369.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step394.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-comparison-step394.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-comparison.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-comparison.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-comparison.svg](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-comparison.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step246.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step246.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step369.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step369.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step394.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components-step394.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components.png](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components.svg](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/progress-reward-components.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [exps/gsm-unseen-split-rewards-400-20261008/controller.py](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/prepare.py](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/gsm-unseen-split-rewards-400-20261008/reward.py](../artifacts/exps/gsm-unseen-split-rewards-400-20261008/reward.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
