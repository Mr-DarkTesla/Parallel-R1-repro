# exps/fixes-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/fixes-20261005/final-eval-config.yaml](../artifacts/exps/fixes-20261005/final-eval-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    enforce_eager: false
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 8192
    max_model_len: null
    max_num_seqs: 1024
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
      num_workers: 8
      agent_loop_config_path: null
      max_iterations_for_parallel_thinking: 4
      num_paths: 2
      max_path_response_length: 4096
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
    path: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230
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
  experiment_name: final-config-check
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: checkpoints/eval/final-config-check
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
  default_local_dir: checkpoints/eval/final-config-check
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet
  val_files: data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2000
  max_response_length: 3000
  train_batch_size: 8
  val_batch_size: 1024
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
    tokenizer_path: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230
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
    input_tokenizer: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230
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
  path: training_scripts/eval_score.py
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
  num_cpus: 24
  timeline_json_file: null

```

</details>

- [exps/fixes-20261005/final-sft-config.yaml](../artifacts/exps/fixes-20261005/final-sft-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 4
  train_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet
  val_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet
  prompt_key: extra_info
  response_key: extra_info
  prompt_dict_keys:
  - question
  response_dict_keys:
  - answer
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 3072
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: false
model:
  partial_pretrain: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: false
  trust_remote_code: false
  lora_rank: 0
  lora_alpha: 16
  target_modules: all-linear
  use_liger: false
  strategy: fsdp2
optim:
  lr: 1.0e-05
  betas:
  - 0.9
  - 0.95
  weight_decay: 0.01
  warmup_steps_ratio: 0.1
  clip_grad: 1.0
  lr_scheduler: cosine
ulysses_sequence_parallel_size: 1
use_remove_padding: false
trainer:
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Seen-Qwen3-0.6B
  total_epochs: 5
  total_training_steps: null
  logger:
  - console
  seed: 1
  save_freq: -1
  test_freq: -1
  nnodes: 1
  n_gpus_per_node: 8
  max_ckpt_to_keep: null
  resume_mode: auto
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents:
    - model
    - optimizer
    - extra
  device: cuda
  final_dir: checkpoints/Parallel-SFT-Seen-Qwen3-0.6B/final

```

</details>

- [exps/fixes-20261005/manifest.json](../artifacts/exps/fixes-20261005/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "root": "${PROJECT_ROOT}",
  "queue": "${PROJECT_ROOT}/exps/fixes-20261005",
  "code": "${PROJECT_ROOT}/exps/fixes-20261005/code/verl",
  "venv": "${PROJECT_ROOT}/.venv",
  "base": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2",
  "gpu_budget": 8,
  "models": [
    {
      "id": "seen",
      "name": "Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005",
      "variant": "seen",
      "existing": false,
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "data.micro_batch_size_per_gpu=4"
      ],
      "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005"
    },
    {
      "id": "unseen",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005",
      "variant": "unseen",
      "existing": false,
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "data.micro_batch_size_per_gpu=4"
      ],
      "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005"
    }
  ],
  "evals": [
    {
      "id": "old-seen-async",
      "model": "old-seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=async"
      ]
    },
    {
      "id": "old-seen-sync",
      "model": "old-seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=sync"
      ]
    },
    {
      "id": "seen-async",
      "model": "seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=async"
      ]
    },
    {
      "id": "seen-sync",
      "model": "seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=sync"
      ]
    },
    {
      "id": "unseen-async",
      "model": "unseen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=async"
      ]
    }
  ],
  "protocol": "1916 samples: competition mean@16, MATH mean@1. Temperature1, response limit3000. Corrected accumulation and equal sample weights; full validation1319. Compare fixed-budget parallel versus ordinary autoregressive Seen. Select final defaults from accuracy, format and measured speed; one seed, not statistical proof."
}
```

</details>

- [exps/fixes-20261005/model-source.json](../artifacts/exps/fixes-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B-Base",
  "revision": "da87bfb608c14b7cf20ba1ce41287e8de496c0cd",
  "seed": 1,
  "token_initialization": "normal",
  "tokens": {
    "<Path>": 151669,
    "</Path>": 151670,
    "<Parallel>": 151671,
    "</Parallel>": 151672,
    "<Summary>": 151673,
    "</Summary>": 151674
  }
}
```

</details>

- [exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/model-source.json](../artifacts/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B-Base",
  "revision": "da87bfb608c14b7cf20ba1ce41287e8de496c0cd",
  "seed": 1,
  "token_initialization": "normal",
  "tokens": {
    "<Path>": 151669,
    "</Path>": 151670,
    "<Parallel>": 151671,
    "</Parallel>": 151672,
    "<Summary>": 151673,
    "</Summary>": 151674
  }
}
```

</details>

- [exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/resolved-config.yaml](../artifacts/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
${PROJECT_ROOT}/exps/fixes-20261005/code/verl/verl/utils/dataset/rl_dataset.py:38: SyntaxWarning: invalid escape sequence '\*'
  """
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 4
  train_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet
  val_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet
  prompt_key: extra_info
  response_key: extra_info
  prompt_dict_keys:
  - question
  response_dict_keys:
  - answer
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 3072
  trim_padding: true
  parse_prompt_tags: false
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: false
model:
  partial_pretrain: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: false
  trust_remote_code: false
  lora_rank: 0
  lora_alpha: 16
  target_modules: all-linear
  use_liger: false
  strategy: fsdp2
optim:
  lr: 1.0e-05
  betas:
  - 0.9
  - 0.95
  weight_decay: 0.01
  warmup_steps_ratio: 0.1
  clip_grad: 1.0
  lr_scheduler: cosine
ulysses_sequence_parallel_size: 1
use_remove_padding: false
trainer:
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005
  total_epochs: 5
  total_training_steps: null
  logger:
  - console
  seed: 1
  save_freq: -1
  test_freq: -1
  nnodes: 1
  n_gpus_per_node: 8
  max_ckpt_to_keep: null
  resume_mode: auto
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents:
    - model
    - optimizer
    - extra
  device: cuda
  final_dir: ${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/final

```

</details>

- [exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/model-source.json](../artifacts/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B-Base",
  "revision": "da87bfb608c14b7cf20ba1ce41287e8de496c0cd",
  "seed": 1,
  "token_initialization": "normal",
  "tokens": {
    "<Path>": 151669,
    "</Path>": 151670,
    "<Parallel>": 151671,
    "</Parallel>": 151672,
    "<Summary>": 151673,
    "</Summary>": 151674
  }
}
```

</details>

- [exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/resolved-config.yaml](../artifacts/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 4
  train_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet
  val_files: data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet
  prompt_key: extra_info
  response_key: extra_info
  prompt_dict_keys:
  - question
  response_dict_keys:
  - answer
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 3072
  trim_padding: true
  parse_prompt_tags: false
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: true
model:
  partial_pretrain: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: false
  trust_remote_code: false
  lora_rank: 0
  lora_alpha: 16
  target_modules: all-linear
  use_liger: false
  strategy: fsdp2
optim:
  lr: 1.0e-05
  betas:
  - 0.9
  - 0.95
  weight_decay: 0.01
  warmup_steps_ratio: 0.1
  clip_grad: 1.0
  lr_scheduler: cosine
ulysses_sequence_parallel_size: 1
use_remove_padding: false
trainer:
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005
  total_epochs: 5
  total_training_steps: null
  logger:
  - console
  seed: 1
  save_freq: -1
  test_freq: -1
  nnodes: 1
  n_gpus_per_node: 8
  max_ckpt_to_keep: null
  resume_mode: auto
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents:
    - model
    - optimizer
    - extra
  device: cuda
  final_dir: ${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final

```

</details>

## Метрики и полнота результатов

- [exps/fixes-20261005/bench/seen-check/gradient-comparison.json](../artifacts/exps/fixes-20261005/bench/seen-check/gradient-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "microbatch": 4,
    "defer_sync": false,
    "loss": 1.5808993875980377,
    "reference_loss": 1.5822883546352386,
    "finite": true,
    "relative_l2": 0.03513351459955086,
    "cosine": 0.9993836290648995
  },
  {
    "microbatch": 4,
    "defer_sync": true,
    "loss": 1.5808993875980377,
    "reference_loss": 1.5822883546352386,
    "finite": true,
    "relative_l2": 0.03527822928138607,
    "cosine": 0.9993782292355989
  },
  {
    "microbatch": 8,
    "defer_sync": true,
    "loss": 1.5808993577957153,
    "reference_loss": 1.5822883546352386,
    "finite": true,
    "relative_l2": 0.03553626868024597,
    "cosine": 0.9993693491689882
  }
]
```

</details>

- [exps/fixes-20261005/metrics-check.json](../artifacts/exps/fixes-20261005/metrics-check.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "answers": 1916,
  "old_seconds": 61.49223885778338,
  "new_seconds": 17.771565530449152,
  "retained_metrics_identical": true,
  "removed_only": "bootstrap best/worst/majority for format flags",
  "errors": []
}
```

</details>

- [exps/fixes-20261005/results/eval/old-seen-async/driver.log](../artifacts/exps/fixes-20261005/results/eval/old-seen-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/fixes-20261005/results/eval/old-seen-async/summary.json](../artifacts/exps/fixes-20261005/results/eval/old-seen-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "old-seen-async",
    "model": "old-seen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
    "overrides": [
      "actor_rollout_ref.rollout.mode=async"
    ]
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0,
      "observed_pass": 0.0,
      "bootstrap_best": 0.0,
      "parallel": 0.9229166666666667,
      "format": 0.94375,
      "parallel_format": 0.86875,
      "format_error": 0.0625,
      "no_tags": 0.06875
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.0217,
      "parallel": 0.8645833333333334,
      "format": 0.9520833333333333,
      "parallel_format": 0.8166666666666667,
      "format_error": 0.05,
      "no_tags": 0.13333333333333333
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.109375,
      "observed_pass": 0.55,
      "bootstrap_best": 0.44544999999999996,
      "parallel": 0.946875,
      "format": 0.9609375,
      "parallel_format": 0.90625,
      "format_error": 0.040625,
      "no_tags": 0.053125
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.2911392405063291,
      "observed_pass": 0.2911392405063291,
      "bootstrap_best": null,
      "parallel": 0.9746835443037974,
      "format": 0.9778481012658228,
      "parallel_format": 0.9525316455696202,
      "format_error": 0.02531645569620253,
      "no_tags": 0.022151898734177215
    }
  }
}
```

</details>

- [exps/fixes-20261005/results/eval/old-seen-sync/driver.log](../artifacts/exps/fixes-20261005/results/eval/old-seen-sync/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/fixes-20261005/results/eval/old-seen-sync/summary.json](../artifacts/exps/fixes-20261005/results/eval/old-seen-sync/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "old-seen-sync",
    "model": "old-seen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
    "overrides": [
      "actor_rollout_ref.rollout.mode=sync"
    ]
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.004166666666666667,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.0434,
      "parallel": 0.8833333333333333,
      "format": 0.93125,
      "parallel_format": 0.7958333333333333,
      "format_error": 0.0875,
      "no_tags": 0.11666666666666667
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.020466666666666668,
      "parallel": 0.88125,
      "format": 0.9583333333333334,
      "parallel_format": 0.8354166666666667,
      "format_error": 0.05,
      "no_tags": 0.11458333333333333
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.1125,
      "observed_pass": 0.5,
      "bootstrap_best": 0.4316,
      "parallel": 0.9515625,
      "format": 0.9421875,
      "parallel_format": 0.8796875,
      "format_error": 0.071875,
      "no_tags": 0.0484375
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.30063291139240506,
      "observed_pass": 0.30063291139240506,
      "bootstrap_best": null,
      "parallel": 0.9556962025316456,
      "format": 0.9588607594936709,
      "parallel_format": 0.9018987341772152,
      "format_error": 0.056962025316455694,
      "no_tags": 0.04113924050632911
    }
  }
}
```

</details>

- [exps/fixes-20261005/results/eval/seen-async/driver.log](../artifacts/exps/fixes-20261005/results/eval/seen-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/fixes-20261005/results/eval/seen-async/summary.json](../artifacts/exps/fixes-20261005/results/eval/seen-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "seen-async",
    "model": "seen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
    "overrides": [
      "actor_rollout_ref.rollout.mode=async"
    ]
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.004166666666666667,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.04283333333333334,
      "parallel": 0.9104166666666667,
      "format": 0.9395833333333333,
      "parallel_format": 0.8479166666666667,
      "format_error": 0.06458333333333334,
      "no_tags": 0.0875
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0,
      "observed_pass": 0.0,
      "bootstrap_best": 0.0,
      "parallel": 0.8958333333333334,
      "format": 0.9458333333333333,
      "parallel_format": 0.8416666666666667,
      "format_error": 0.05625,
      "no_tags": 0.10208333333333333
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.109375,
      "observed_pass": 0.525,
      "bootstrap_best": 0.44877500000000003,
      "parallel": 0.9390625,
      "format": 0.9375,
      "parallel_format": 0.878125,
      "format_error": 0.0671875,
      "no_tags": 0.0546875
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.29430379746835444,
      "observed_pass": 0.29430379746835444,
      "bootstrap_best": null,
      "parallel": 0.9715189873417721,
      "format": 0.9651898734177216,
      "parallel_format": 0.9367088607594937,
      "format_error": 0.03481012658227848,
      "no_tags": 0.028481012658227847
    }
  }
}
```

</details>

- [exps/fixes-20261005/results/eval/seen-sync/driver.log](../artifacts/exps/fixes-20261005/results/eval/seen-sync/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/fixes-20261005/results/eval/seen-sync/summary.json](../artifacts/exps/fixes-20261005/results/eval/seen-sync/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "seen-sync",
    "model": "seen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
    "overrides": [
      "actor_rollout_ref.rollout.mode=sync"
    ]
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0,
      "observed_pass": 0.0,
      "bootstrap_best": 0.0,
      "parallel": 0.8916666666666667,
      "format": 0.95,
      "parallel_format": 0.8270833333333333,
      "format_error": 0.06666666666666667,
      "no_tags": 0.10625
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.004166666666666667,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.0435,
      "parallel": 0.9,
      "format": 0.9416666666666667,
      "parallel_format": 0.83125,
      "format_error": 0.06875,
      "no_tags": 0.1
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.1015625,
      "observed_pass": 0.5,
      "bootstrap_best": 0.41980000000000006,
      "parallel": 0.934375,
      "format": 0.940625,
      "parallel_format": 0.8703125,
      "format_error": 0.065625,
      "no_tags": 0.0640625
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.29430379746835444,
      "observed_pass": 0.29430379746835444,
      "bootstrap_best": null,
      "parallel": 0.9746835443037974,
      "format": 0.9588607594936709,
      "parallel_format": 0.930379746835443,
      "format_error": 0.04430379746835443,
      "no_tags": 0.02531645569620253
    }
  }
}
```

</details>

- [exps/fixes-20261005/results/eval/unseen-async/driver.log](../artifacts/exps/fixes-20261005/results/eval/unseen-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/fixes-20261005/results/eval/unseen-async/summary.json](../artifacts/exps/fixes-20261005/results/eval/unseen-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "unseen-async",
    "model": "unseen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
    "overrides": [
      "actor_rollout_ref.rollout.mode=async"
    ]
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.02146666666666667,
      "parallel": 0.9145833333333333,
      "format": 0.93125,
      "parallel_format": 0.8458333333333333,
      "format_error": 0.07291666666666667,
      "no_tags": 0.08125
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.004166666666666667,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.0436,
      "parallel": 0.8979166666666667,
      "format": 0.9375,
      "parallel_format": 0.83125,
      "format_error": 0.06875,
      "no_tags": 0.1
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.0953125,
      "observed_pass": 0.6,
      "bootstrap_best": 0.47275,
      "parallel": 0.9453125,
      "format": 0.934375,
      "parallel_format": 0.878125,
      "format_error": 0.071875,
      "no_tags": 0.05
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.27848101265822783,
      "observed_pass": 0.27848101265822783,
      "bootstrap_best": null,
      "parallel": 0.9778481012658228,
      "format": 0.9588607594936709,
      "parallel_format": 0.9335443037974683,
      "format_error": 0.04430379746835443,
      "no_tags": 0.022151898734177215
    }
  }
}
```

</details>

- [exps/fixes-20261005/status.json](../artifacts/exps/fixes-20261005/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train-seen": {
    "status": "complete",
    "updated": "2026-10-05T20:48:46.863129+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005"
  },
  "train-unseen": {
    "status": "complete",
    "updated": "2026-10-05T20:57:23.268923+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005"
  },
  "eval-old-seen-async": {
    "status": "complete",
    "updated": "2026-10-05T21:09:24.785404+00:00",
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/eval/old-seen-async",
    "answers": 1916
  },
  "eval-old-seen-sync": {
    "status": "complete",
    "updated": "2026-10-05T21:08:36.533825+00:00",
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/eval/old-seen-sync",
    "answers": 1916
  },
  "eval-seen-async": {
    "status": "complete",
    "updated": "2026-10-05T21:09:40.241484+00:00",
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/eval/seen-async",
    "answers": 1916
  },
  "eval-seen-sync": {
    "status": "complete",
    "updated": "2026-10-05T21:08:40.121490+00:00",
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/eval/seen-sync",
    "answers": 1916
  },
  "eval-unseen-async": {
    "status": "complete",
    "updated": "2026-10-05T21:20:00.581747+00:00",
    "results": "${PROJECT_ROOT}/exps/fixes-20261005/results/eval/unseen-async",
    "answers": 1916
  }
}
```

</details>

- [exps/fixes-20261005/summary.csv](../artifacts/exps/fixes-20261005/summary.csv) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/fixes-20261005/summary.json](../artifacts/exps/fixes-20261005/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-05T21:20:00.610080+00:00",
  "evaluations": [
    {
      "complete": true,
      "job": {
        "id": "old-seen-async",
        "model": "old-seen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
        "overrides": [
          "actor_rollout_ref.rollout.mode=async"
        ]
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0,
          "observed_pass": 0.0,
          "bootstrap_best": 0.0,
          "parallel": 0.9229166666666667,
          "format": 0.94375,
          "parallel_format": 0.86875,
          "format_error": 0.0625,
          "no_tags": 0.06875
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.0217,
          "parallel": 0.8645833333333334,
          "format": 0.9520833333333333,
          "parallel_format": 0.8166666666666667,
          "format_error": 0.05,
          "no_tags": 0.13333333333333333
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.109375,
          "observed_pass": 0.55,
          "bootstrap_best": 0.44544999999999996,
          "parallel": 0.946875,
          "format": 0.9609375,
          "parallel_format": 0.90625,
          "format_error": 0.040625,
          "no_tags": 0.053125
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.2911392405063291,
          "observed_pass": 0.2911392405063291,
          "bootstrap_best": null,
          "parallel": 0.9746835443037974,
          "format": 0.9778481012658228,
          "parallel_format": 0.9525316455696202,
          "format_error": 0.02531645569620253,
          "no_tags": 0.022151898734177215
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "old-seen-sync",
        "model": "old-seen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230",
        "overrides": [
          "actor_rollout_ref.rollout.mode=sync"
        ]
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.004166666666666667,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.0434,
          "parallel": 0.8833333333333333,
          "format": 0.93125,
          "parallel_format": 0.7958333333333333,
          "format_error": 0.0875,
          "no_tags": 0.11666666666666667
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.020466666666666668,
          "parallel": 0.88125,
          "format": 0.9583333333333334,
          "parallel_format": 0.8354166666666667,
          "format_error": 0.05,
          "no_tags": 0.11458333333333333
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.1125,
          "observed_pass": 0.5,
          "bootstrap_best": 0.4316,
          "parallel": 0.9515625,
          "format": 0.9421875,
          "parallel_format": 0.8796875,
          "format_error": 0.071875,
          "no_tags": 0.0484375
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.30063291139240506,
          "observed_pass": 0.30063291139240506,
          "bootstrap_best": null,
          "parallel": 0.9556962025316456,
          "format": 0.9588607594936709,
          "parallel_format": 0.9018987341772152,
          "format_error": 0.056962025316455694,
          "no_tags": 0.04113924050632911
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "seen-async",
        "model": "seen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
        "overrides": [
          "actor_rollout_ref.rollout.mode=async"
        ]
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.004166666666666667,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.04283333333333334,
          "parallel": 0.9104166666666667,
          "format": 0.9395833333333333,
          "parallel_format": 0.8479166666666667,
          "format_error": 0.06458333333333334,
          "no_tags": 0.0875
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0,
          "observed_pass": 0.0,
          "bootstrap_best": 0.0,
          "parallel": 0.8958333333333334,
          "format": 0.9458333333333333,
          "parallel_format": 0.8416666666666667,
          "format_error": 0.05625,
          "no_tags": 0.10208333333333333
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.109375,
          "observed_pass": 0.525,
          "bootstrap_best": 0.44877500000000003,
          "parallel": 0.9390625,
          "format": 0.9375,
          "parallel_format": 0.878125,
          "format_error": 0.0671875,
          "no_tags": 0.0546875
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.29430379746835444,
          "observed_pass": 0.29430379746835444,
          "bootstrap_best": null,
          "parallel": 0.9715189873417721,
          "format": 0.9651898734177216,
          "parallel_format": 0.9367088607594937,
          "format_error": 0.03481012658227848,
          "no_tags": 0.028481012658227847
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "seen-sync",
        "model": "seen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
        "overrides": [
          "actor_rollout_ref.rollout.mode=sync"
        ]
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0,
          "observed_pass": 0.0,
          "bootstrap_best": 0.0,
          "parallel": 0.8916666666666667,
          "format": 0.95,
          "parallel_format": 0.8270833333333333,
          "format_error": 0.06666666666666667,
          "no_tags": 0.10625
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.004166666666666667,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.0435,
          "parallel": 0.9,
          "format": 0.9416666666666667,
          "parallel_format": 0.83125,
          "format_error": 0.06875,
          "no_tags": 0.1
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.1015625,
          "observed_pass": 0.5,
          "bootstrap_best": 0.41980000000000006,
          "parallel": 0.934375,
          "format": 0.940625,
          "parallel_format": 0.8703125,
          "format_error": 0.065625,
          "no_tags": 0.0640625
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.29430379746835444,
          "observed_pass": 0.29430379746835444,
          "bootstrap_best": null,
          "parallel": 0.9746835443037974,
          "format": 0.9588607594936709,
          "parallel_format": 0.930379746835443,
          "format_error": 0.04430379746835443,
          "no_tags": 0.02531645569620253
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "unseen-async",
        "model": "unseen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/global_step_230",
        "overrides": [
          "actor_rollout_ref.rollout.mode=async"
        ]
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.02146666666666667,
          "parallel": 0.9145833333333333,
          "format": 0.93125,
          "parallel_format": 0.8458333333333333,
          "format_error": 0.07291666666666667,
          "no_tags": 0.08125
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.004166666666666667,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.0436,
          "parallel": 0.8979166666666667,
          "format": 0.9375,
          "parallel_format": 0.83125,
          "format_error": 0.06875,
          "no_tags": 0.1
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.0953125,
          "observed_pass": 0.6,
          "bootstrap_best": 0.47275,
          "parallel": 0.9453125,
          "format": 0.934375,
          "parallel_format": 0.878125,
          "format_error": 0.071875,
          "no_tags": 0.05
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.27848101265822783,
          "observed_pass": 0.27848101265822783,
          "bootstrap_best": null,
          "parallel": 0.9778481012658228,
          "format": 0.9588607594936709,
          "parallel_format": 0.9335443037974683,
          "format_error": 0.04430379746835443,
          "no_tags": 0.022151898734177215
        }
      }
    }
  ],
  "failed_or_skipped": [],
  "protocol": "1916 samples: competition mean@16, MATH mean@1. Temperature1, response limit3000. Corrected accumulation and equal sample weights; full validation1319. Compare fixed-budget parallel versus ordinary autoregressive Seen. Select final defaults from accuracy, format and measured speed; one seed, not statistical proof."
}
```

</details>

## Исходники рецепта и награды

- [exps/fixes-20261005/bench/run.sh](../artifacts/exps/fixes-20261005/bench/run.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/fixes-20261005/launch.sh](../artifacts/exps/fixes-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
