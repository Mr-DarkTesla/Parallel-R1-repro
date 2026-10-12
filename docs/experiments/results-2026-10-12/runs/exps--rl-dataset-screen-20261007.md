# exps/rl-dataset-screen-20261007

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/rl-dataset-screen-20261007/data-audit.json](../artifacts/exps/rl-dataset-screen-20261007/data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "seed": 20261007,
  "math_rows": 12500,
  "sft_rows": 5910,
  "filter": "normalized exact and number-masked word-trigram Jaccard >=0.65; does not establish absence of semantic paraphrases",
  "datasets": {
    "gsm_infinite_ops2": {
      "selected": 52,
      "rejected": [],
      "max_prompt_tokens": 826
    },
    "gsm_infinite_ops3": {
      "selected": 51,
      "rejected": [],
      "max_prompt_tokens": 685
    },
    "gsm_infinite_ops4": {
      "selected": 51,
      "rejected": [],
      "max_prompt_tokens": 695
    },
    "gsm_infinite_ops5": {
      "selected": 51,
      "rejected": [],
      "max_prompt_tokens": 935
    },
    "gsm_infinite_ops6": {
      "selected": 51,
      "rejected": [],
      "max_prompt_tokens": 919
    },
    "dapo": {
      "selected": 256,
      "rejected": "78 records; see original artifact",
      "max_prompt_tokens": 483
    }
  },
  "blocked": {
    "bigmath_orca": "HF access required (401)",
    "bigmath_cn_k12": "HF access required (401)"
  },
  "gsm_infinite": {
    "rows": 256,
    "sha256": "ae164a57106664a8cb314d60225e5005aa9d9929a103a7b200392dcc0a7afbd6"
  },
  "dapo": {
    "rows": 256,
    "sha256": "35f2733a92fd8a77cdf5c3408c21795343425c797e0279de7386da618d027b68"
  },
  "sources": {
    "gsm": "InfiniAILab/gsm_infinite_medium_0@c6c5ab433565ddfe3e38e22be165b5c40e6bd576",
    "math_exclusion": "EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3",
    "dapo_file": "${PROJECT_ROOT}/exps/rl-unseen-s2-bs32-500-20261007/code/verl/data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet",
    "checkpoint": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final"
  }
}
```

</details>

- [exps/rl-dataset-screen-20261007/more-data-audit.json](../artifacts/exps/rl-dataset-screen-20261007/more-data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "seed": 20261007,
  "math_rows": 12500,
  "sft_rows": 5910,
  "filter": "normalized exact and number-masked word-trigram Jaccard >=0.65; does not establish absence of semantic paraphrases",
  "datasets": {
    "bigmath_orca": {
      "selected": 256,
      "rejected": [
        {
          "id": "71589",
          "match": "SFT/369",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.654320987654321
        },
        {
          "id": "42538",
          "match": "SFT/3435",
          "kind": "normalized_exact"
        },
        {
          "id": "103221",
          "match": "SFT/3381",
          "kind": "normalized_exact"
        },
        {
          "id": "178921",
          "match": "SFT/2499",
          "kind": "normalized_exact"
        },
        {
          "id": "213704",
          "match": "SFT/5272",
          "kind": "normalized_exact"
        },
        {
          "id": "173756",
          "match": "SFT/3150",
          "kind": "normalized_exact"
        },
        {
          "id": "123653",
          "match": "SFT/3625",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.6521739130434783
        },
        {
          "id": "8766",
          "match": "SFT/1349",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.7551020408163265
        },
        {
          "id": "128884",
          "match": "SFT/3767",
          "kind": "normalized_exact"
        },
        {
          "id": "48855",
          "match": "SFT/626",
          "kind": "normalized_exact"
        }
      ],
      "max_prompt_tokens": 429
    },
    "bigmath_cn_k12": {
      "selected": 256,
      "rejected": [
        {
          "id": "143009",
          "match": "MATH/algebra/train/297",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.6666666666666666
        },
        {
          "id": "77090",
          "match": "MATH/counting_and_probability/train/189",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.75
        },
        {
          "id": "128094",
          "match": "MATH/counting_and_probability/train/189",
          "kind": "number_masked_word_trigram_jaccard",
          "similarity": 0.6666666666666666
        }
      ],
      "max_prompt_tokens": 398
    }
  },
  "blocked": {},
  "publication": "open-r1/Big-Math-RL-Verified-Processed@c79efbb6d3b75e3a2bcc27a5c569119918132345",
  "publication_filters": "Removes missing llama8b solve rates and references unparseable by Math-Verify; sample uniformly within each source, without solve-rate filtering.",
  "download_sha256": "db6d8ea52ec4b9bd0bdfc1a2ce38874a95a193cd467e6858c4fecea3db08cbb0",
  "bigmath_orca": {
    "rows": 256,
    "source_rows": 79556,
    "quality_exclusions": {
      "figure_or_proof": 124
    },
    "sha256": "7df39f2e84380b25b9541a3bf1ccbe8f00c1c6f414976479bca8034be9d4521f"
  },
  "bigmath_cn_k12": {
    "rows": 256,
    "source_rows": 48974,
    "quality_exclusions": {
      "figure_or_proof": 149
    },
    "sha256": "2882edfb2ca9b9d117c563561aad4e2ccd0787b21fa69f330df4018d48910655"
  }
}
```

</details>

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/resolved-config.yaml](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 8
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 64
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    disable_log_stats: true
    do_sample: true
    'n': 1
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
      'n': 8
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
    override_config: {}
    enable_gradient_checkpointing: false
    enable_activation_offload: false
    use_remove_padding: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
    exclude_modules: null
    use_liger: false
    use_fused_kernels: false
    fused_kernel_options:
      impl_backend: torch
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
  total_epochs: 1
  total_training_steps: null
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
  experiment_name: bigmath_cn_k12
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: -1
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: true
  val_only: true
  test_freq: -1
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_cn_k12.parquet
  val_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_cn_k12.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 8
  val_batch_size: 32
  return_raw_input_ids: false
  return_raw_chat: true
  return_full_prompt: false
  shuffle: true
  dataloader_num_workers: 8
  validation_shuffle: false
  filter_overlong_prompts: false
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
  rollout_n: 1
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
  ppo_mini_batch_size: 8
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
    use_fused_kernels: false
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
  path: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/score.py
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

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/resolved-config.yaml](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 8
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 64
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    disable_log_stats: true
    do_sample: true
    'n': 1
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
      'n': 8
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
    override_config: {}
    enable_gradient_checkpointing: false
    enable_activation_offload: false
    use_remove_padding: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
    exclude_modules: null
    use_liger: false
    use_fused_kernels: false
    fused_kernel_options:
      impl_backend: torch
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
  total_epochs: 1
  total_training_steps: null
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
  experiment_name: bigmath_orca
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/bigmath_orca
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: -1
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: true
  val_only: true
  test_freq: -1
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/bigmath_orca
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_orca.parquet
  val_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_orca.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 8
  val_batch_size: 32
  return_raw_input_ids: false
  return_raw_chat: true
  return_full_prompt: false
  shuffle: true
  dataloader_num_workers: 8
  validation_shuffle: false
  filter_overlong_prompts: false
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
  rollout_n: 1
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
  ppo_mini_batch_size: 8
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
    use_fused_kernels: false
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
  path: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/score.py
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

- [exps/rl-dataset-screen-20261007/results/eval/dapo/resolved-config.yaml](../artifacts/exps/rl-dataset-screen-20261007/results/eval/dapo/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 8
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 64
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    disable_log_stats: true
    do_sample: true
    'n': 1
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
      'n': 8
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
    override_config: {}
    enable_gradient_checkpointing: false
    enable_activation_offload: false
    use_remove_padding: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
    exclude_modules: null
    use_liger: false
    use_fused_kernels: false
    fused_kernel_options:
      impl_backend: torch
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
  total_epochs: 1
  total_training_steps: null
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
  experiment_name: dapo
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/dapo
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: -1
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: true
  val_only: true
  test_freq: -1
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/dapo
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/dapo.parquet
  val_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/dapo.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 8
  val_batch_size: 32
  return_raw_input_ids: false
  return_raw_chat: true
  return_full_prompt: false
  shuffle: true
  dataloader_num_workers: 8
  validation_shuffle: false
  filter_overlong_prompts: false
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
  rollout_n: 1
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
  ppo_mini_batch_size: 8
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
    use_fused_kernels: false
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
  path: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/score.py
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

- [exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/resolved-config.yaml](../artifacts/exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 8
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 64
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: false
    log_prob_max_token_len_per_gpu: 16384
    disable_log_stats: true
    do_sample: true
    'n': 1
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
      'n': 8
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
    override_config: {}
    enable_gradient_checkpointing: false
    enable_activation_offload: false
    use_remove_padding: false
    lora_rank: 0
    lora_alpha: 16
    target_modules: all-linear
    exclude_modules: null
    use_liger: false
    use_fused_kernels: false
    fused_kernel_options:
      impl_backend: torch
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
  total_epochs: 1
  total_training_steps: null
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
  experiment_name: gsm_infinite
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/gsm_infinite
  nnodes: 1
  n_gpus_per_node: 8
  save_freq: -1
  esi_redundant_time: 0
  resume_mode: disable
  resume_from_path: null
  val_before_train: true
  val_only: true
  test_freq: -1
  critic_warmup: 0
  default_hdfs_dir: null
  del_local_ckpt_after_load: false
  default_local_dir: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/results/eval/gsm_infinite
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/gsm_infinite.parquet
  val_files: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/gsm_infinite.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 8
  val_batch_size: 32
  return_raw_input_ids: false
  return_raw_chat: true
  return_full_prompt: false
  shuffle: true
  dataloader_num_workers: 8
  validation_shuffle: false
  filter_overlong_prompts: false
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
  rollout_n: 1
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
  ppo_mini_batch_size: 8
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
    use_fused_kernels: false
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
  path: ${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/score.py
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

- [exps/rl-dataset-screen-20261007/extension-status.json](../artifacts/exps/rl-dataset-screen-20261007/extension-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "exit_code": 0
}
```

</details>

- [exps/rl-dataset-screen-20261007/more-status.json](../artifacts/exps/rl-dataset-screen-20261007/more-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "observed_utc": "2026-10-07T19:20:15.100974+00:00",
  "completed": [
    "bigmath_orca",
    "bigmath_cn_k12"
  ],
  "blocked": {}
}
```

</details>

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/driver.log](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/summary.json](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_cn_k12/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "questions": 256,
  "accuracy": 0.21044921875,
  "accuracy_cluster_bootstrap_ci95": [
    0.17578125,
    0.248046875
  ],
  "k_of_8": {
    "0": 127,
    "1": 38,
    "2": 26,
    "3": 9,
    "4": 17,
    "5": 16,
    "6": 1,
    "7": 16,
    "8": 6
  },
  "mixed_fraction": 0.48046875,
  "correct_parallel_and_plain_groups": 4,
  "answers": 2048,
  "legacy_accuracy": 0.18505859375,
  "scorer_disagreements": 94,
  "scorer_errors": 0,
  "extraction_failures": 33,
  "parallel_fraction": 0.978515625,
  "format_error_fraction": 0.0537109375,
  "by_op": {
    "-1": {
      "questions": 256,
      "accuracy": 0.21044921875,
      "accuracy_cluster_bootstrap_ci95": [
        0.17578125,
        0.248046875
      ],
      "k_of_8": {
        "0": 127,
        "1": 38,
        "2": 26,
        "3": 9,
        "4": 17,
        "5": 16,
        "6": 1,
        "7": 16,
        "8": 6
      },
      "mixed_fraction": 0.48046875,
      "correct_parallel_and_plain_groups": 4
    }
  },
  "trace_count": 2048,
  "response_tokens": 1665353,
  "at_token_budget": 22,
  "generation_wall_seconds": 488.655645608902,
  "mixed_groups_per_generation_minute": 15.102659851200452,
  "mixed_groups_per_million_response_tokens": 73.85821504509855,
  "total_wall_seconds": 887.7934865951538
}
```

</details>

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/driver.log](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/summary.json](../artifacts/exps/rl-dataset-screen-20261007/results/eval/bigmath_orca/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "questions": 256,
  "accuracy": 0.318359375,
  "accuracy_cluster_bootstrap_ci95": [
    0.2783203125,
    0.359375
  ],
  "k_of_8": {
    "0": 94,
    "1": 36,
    "2": 16,
    "3": 17,
    "4": 18,
    "5": 24,
    "6": 28,
    "7": 11,
    "8": 12
  },
  "mixed_fraction": 0.5859375,
  "correct_parallel_and_plain_groups": 1,
  "answers": 2048,
  "legacy_accuracy": 0.3056640625,
  "scorer_disagreements": 30,
  "scorer_errors": 0,
  "extraction_failures": 44,
  "parallel_fraction": 0.9951171875,
  "format_error_fraction": 0.03125,
  "by_op": {
    "-1": {
      "questions": 256,
      "accuracy": 0.318359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.2783203125,
        0.359375
      ],
      "k_of_8": {
        "0": 94,
        "1": 36,
        "2": 16,
        "3": 17,
        "4": 18,
        "5": 24,
        "6": 28,
        "7": 11,
        "8": 12
      },
      "mixed_fraction": 0.5859375,
      "correct_parallel_and_plain_groups": 1
    }
  },
  "trace_count": 2048,
  "response_tokens": 1215945,
  "at_token_budget": 12,
  "generation_wall_seconds": 449.60237073898315,
  "mixed_groups_per_generation_minute": 20.0176880411179,
  "mixed_groups_per_million_response_tokens": 123.36084280127803,
  "total_wall_seconds": 845.9828708171844
}
```

</details>

- [exps/rl-dataset-screen-20261007/results/eval/dapo/driver.log](../artifacts/exps/rl-dataset-screen-20261007/results/eval/dapo/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-dataset-screen-20261007/results/eval/dapo/summary.json](../artifacts/exps/rl-dataset-screen-20261007/results/eval/dapo/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "questions": 256,
  "accuracy": 0.04443359375,
  "accuracy_cluster_bootstrap_ci95": [
    0.03369140625,
    0.056640625
  ],
  "k_of_8": {
    "0": 194,
    "1": 43,
    "2": 13,
    "3": 3,
    "4": 2,
    "5": 1,
    "6": 0,
    "7": 0,
    "8": 0
  },
  "mixed_fraction": 0.2421875,
  "correct_parallel_and_plain_groups": 0,
  "answers": 2048,
  "legacy_accuracy": 0.044921875,
  "scorer_disagreements": 3,
  "scorer_errors": 0,
  "extraction_failures": 62,
  "parallel_fraction": 0.91650390625,
  "format_error_fraction": 0.06298828125,
  "by_op": {
    "-1": {
      "questions": 256,
      "accuracy": 0.04443359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.03369140625,
        0.056640625
      ],
      "k_of_8": {
        "0": 194,
        "1": 43,
        "2": 13,
        "3": 3,
        "4": 2,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.2421875,
      "correct_parallel_and_plain_groups": 0
    }
  },
  "trace_count": 2048,
  "response_tokens": 2061333,
  "at_token_budget": 49,
  "generation_wall_seconds": 507.6208481788635,
  "mixed_groups_per_generation_minute": 7.328304212377884,
  "mixed_groups_per_million_response_tokens": 30.07762452742958,
  "total_wall_seconds": 932.8691782951355
}
```

</details>

- [exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/driver.log](../artifacts/exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/summary.json](../artifacts/exps/rl-dataset-screen-20261007/results/eval/gsm_infinite/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "questions": 256,
  "accuracy": 0.185546875,
  "accuracy_cluster_bootstrap_ci95": [
    0.1640625,
    0.20703125
  ],
  "k_of_8": {
    "0": 72,
    "1": 78,
    "2": 55,
    "3": 27,
    "4": 15,
    "5": 5,
    "6": 2,
    "7": 2,
    "8": 0
  },
  "mixed_fraction": 0.71875,
  "correct_parallel_and_plain_groups": 12,
  "answers": 2048,
  "legacy_accuracy": 0.18701171875,
  "scorer_disagreements": 3,
  "scorer_errors": 0,
  "extraction_failures": 126,
  "parallel_fraction": 0.9619140625,
  "format_error_fraction": 0.04345703125,
  "by_op": {
    "2": {
      "questions": 52,
      "accuracy": 0.19471153846153846,
      "accuracy_cluster_bootstrap_ci95": [
        0.14423076923076922,
        0.25
      ],
      "k_of_8": {
        "0": 16,
        "1": 15,
        "2": 8,
        "3": 5,
        "4": 7,
        "5": 0,
        "6": 0,
        "7": 1,
        "8": 0
      },
      "mixed_fraction": 0.6923076923076923,
      "correct_parallel_and_plain_groups": 2
    },
    "3": {
      "questions": 51,
      "accuracy": 0.1715686274509804,
      "accuracy_cluster_bootstrap_ci95": [
        0.12745098039215685,
        0.22058823529411764
      ],
      "k_of_8": {
        "0": 14,
        "1": 19,
        "2": 9,
        "3": 6,
        "4": 1,
        "5": 1,
        "6": 1,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.7254901960784313,
      "correct_parallel_and_plain_groups": 3
    },
    "4": {
      "questions": 51,
      "accuracy": 0.22794117647058823,
      "accuracy_cluster_bootstrap_ci95": [
        0.17647058823529413,
        0.2818627450980392
      ],
      "k_of_8": {
        "0": 9,
        "1": 16,
        "2": 13,
        "3": 7,
        "4": 3,
        "5": 1,
        "6": 1,
        "7": 1,
        "8": 0
      },
      "mixed_fraction": 0.8235294117647058,
      "correct_parallel_and_plain_groups": 4
    },
    "5": {
      "questions": 51,
      "accuracy": 0.19117647058823528,
      "accuracy_cluster_bootstrap_ci95": [
        0.14460784313725492,
        0.2426470588235294
      ],
      "k_of_8": {
        "0": 15,
        "1": 13,
        "2": 12,
        "3": 5,
        "4": 4,
        "5": 2,
        "6": 0,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.7058823529411765,
      "correct_parallel_and_plain_groups": 0
    },
    "6": {
      "questions": 51,
      "accuracy": 0.14215686274509803,
      "accuracy_cluster_bootstrap_ci95": [
        0.1053921568627451,
        0.18137254901960784
      ],
      "k_of_8": {
        "0": 18,
        "1": 15,
        "2": 13,
        "3": 4,
        "4": 0,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.6470588235294118,
      "correct_parallel_and_plain_groups": 3
    }
  },
  "trace_count": 2048,
  "response_tokens": 1418840,
  "at_token_budget": 31,
  "generation_wall_seconds": 501.73539185523987,
  "mixed_groups_per_generation_minute": 22.003630158873165,
  "mixed_groups_per_million_response_tokens": 129.68340334357643,
  "total_wall_seconds": 897.3597013950348
}
```

</details>

- [exps/rl-dataset-screen-20261007/selection-analysis.json](../artifacts/exps/rl-dataset-screen-20261007/selection-analysis.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_utc": "2026-10-07T19:26:14.520463+00:00",
  "datasets": {
    "gsm_infinite": {
      "questions": 256,
      "accuracy": 0.185546875,
      "accuracy_cluster_bootstrap_ci95": [
        0.1640625,
        0.20703125
      ],
      "k_of_8": {
        "0": 72,
        "1": 78,
        "2": 55,
        "3": 27,
        "4": 15,
        "5": 5,
        "6": 2,
        "7": 2,
        "8": 0
      },
      "mixed_fraction": 0.71875,
      "correct_parallel_and_plain_groups": 12,
      "answers": 2048,
      "legacy_accuracy": 0.18701171875,
      "scorer_disagreements": 3,
      "scorer_errors": 0,
      "extraction_failures": 126,
      "parallel_fraction": 0.9619140625,
      "format_error_fraction": 0.04345703125,
      "trace_count": 2048,
      "response_tokens": 1418840,
      "at_token_budget": 31,
      "generation_wall_seconds": 501.73539185523987,
      "mixed_groups_per_generation_minute": 22.003630158873165,
      "mixed_groups_per_million_response_tokens": 129.68340334357643,
      "total_wall_seconds": 897.3597013950348,
      "unique_gold_strings": 15,
      "top_gold": [
        [
          "4",
          61
        ],
        [
          "2",
          59
        ],
        [
          "3",
          41
        ],
        [
          "1",
          25
        ],
        [
          "6",
          18
        ]
      ],
      "best_constant_answer_accuracy": 0.23828125,
      "mean_prompt_tokens": 592.30859375,
      "mean_response_tokens": 692.79296875
    },
    "dapo": {
      "questions": 256,
      "accuracy": 0.04443359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.03369140625,
        0.056640625
      ],
      "k_of_8": {
        "0": 194,
        "1": 43,
        "2": 13,
        "3": 3,
        "4": 2,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.2421875,
      "correct_parallel_and_plain_groups": 0,
      "answers": 2048,
      "legacy_accuracy": 0.044921875,
      "scorer_disagreements": 3,
      "scorer_errors": 0,
      "extraction_failures": 62,
      "parallel_fraction": 0.91650390625,
      "format_error_fraction": 0.06298828125,
      "trace_count": 2048,
      "response_tokens": 2061333,
      "at_token_budget": 49,
      "generation_wall_seconds": 507.6208481788635,
      "mixed_groups_per_generation_minute": 7.328304212377884,
      "mixed_groups_per_million_response_tokens": 30.07762452742958,
      "total_wall_seconds": 932.8691782951355,
      "unique_gold_strings": 142,
      "top_gold": [
        [
          "1",
          15
        ],
        [
          "4",
          12
        ],
        [
          "7",
          10
        ],
        [
          "3",
          9
        ],
        [
          "5",
          9
        ]
      ],
      "best_constant_answer_accuracy": 0.05859375,
      "mean_prompt_tokens": 275.3359375,
      "mean_response_tokens": 1006.51025390625
    },
    "bigmath_orca": {
      "questions": 256,
      "accuracy": 0.318359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.2783203125,
        0.359375
      ],
      "k_of_8": {
        "0": 94,
        "1": 36,
        "2": 16,
        "3": 17,
        "4": 18,
        "5": 24,
        "6": 28,
        "7": 11,
        "8": 12
      },
      "mixed_fraction": 0.5859375,
      "correct_parallel_and_plain_groups": 1,
      "answers": 2048,
      "legacy_accuracy": 0.3056640625,
      "scorer_disagreements": 30,
      "scorer_errors": 0,
      "extraction_failures": 44,
      "parallel_fraction": 0.9951171875,
      "format_error_fraction": 0.03125,
      "trace_count": 2048,
      "response_tokens": 1215945,
      "at_token_budget": 12,
      "generation_wall_seconds": 449.60237073898315,
      "mixed_groups_per_generation_minute": 20.0176880411179,
      "mixed_groups_per_million_response_tokens": 123.36084280127803,
      "total_wall_seconds": 845.9828708171844,
      "unique_gold_strings": 153,
      "top_gold": [
        [
          "2",
          12
        ],
        [
          "10",
          11
        ],
        [
          "6",
          10
        ],
        [
          "4",
          8
        ],
        [
          "8",
          6
        ]
      ],
      "best_constant_answer_accuracy": 0.046875,
      "mean_prompt_tokens": 246.5234375,
      "mean_response_tokens": 593.72314453125
    },
    "bigmath_cn_k12": {
      "questions": 256,
      "accuracy": 0.21044921875,
      "accuracy_cluster_bootstrap_ci95": [
        0.17578125,
        0.248046875
      ],
      "k_of_8": {
        "0": 127,
        "1": 38,
        "2": 26,
        "3": 9,
        "4": 17,
        "5": 16,
        "6": 1,
        "7": 16,
        "8": 6
      },
      "mixed_fraction": 0.48046875,
      "correct_parallel_and_plain_groups": 4,
      "answers": 2048,
      "legacy_accuracy": 0.18505859375,
      "scorer_disagreements": 94,
      "scorer_errors": 0,
      "extraction_failures": 33,
      "parallel_fraction": 0.978515625,
      "format_error_fraction": 0.0537109375,
      "trace_count": 2048,
      "response_tokens": 1665353,
      "at_token_budget": 22,
      "generation_wall_seconds": 488.655645608902,
      "mixed_groups_per_generation_minute": 15.102659851200452,
      "mixed_groups_per_million_response_tokens": 73.85821504509855,
      "total_wall_seconds": 887.7934865951538,
      "unique_gold_strings": 185,
      "top_gold": [
        [
          "1",
          16
        ],
        [
          "2",
          13
        ],
        [
          "4",
          10
        ],
        [
          "10",
          7
        ],
        [
          "9",
          6
        ]
      ],
      "best_constant_answer_accuracy": 0.0625,
      "mean_prompt_tokens": 241.1953125,
      "mean_response_tokens": 813.16064453125
    }
  },
  "controller_status": {
    "state": "complete",
    "observed_utc": "2026-10-07T19:20:15.100974+00:00",
    "completed": [
      "bigmath_orca",
      "bigmath_cn_k12"
    ],
    "blocked": {}
  },
  "extension_status": {
    "state": "complete",
    "exit_code": 0
  }
}
```

</details>

- [exps/rl-dataset-screen-20261007/status.json](../artifacts/exps/rl-dataset-screen-20261007/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "available_sets_complete_bigmath_blocked",
  "observed_utc": "2026-10-07T18:50:51.837563+00:00",
  "completed": [
    "gsm_infinite",
    "dapo"
  ],
  "blocked": {
    "bigmath_orca": "HF access required (401)",
    "bigmath_cn_k12": "HF access required (401)"
  }
}
```

</details>

## Исходники рецепта и награды

- [exps/rl-dataset-screen-20261007/prepare.py](../artifacts/exps/rl-dataset-screen-20261007/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/rl-dataset-screen-20261007/run.py](../artifacts/exps/rl-dataset-screen-20261007/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
