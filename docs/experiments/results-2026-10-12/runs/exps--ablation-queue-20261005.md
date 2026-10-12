# exps/ablation-queue-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/ablation-queue-20261005/eval-preflight.yaml](../artifacts/exps/ablation-queue-20261005/eval-preflight.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
      num_workers: 2
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
    path: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
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
  experiment_name: base-v2
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/base-v2
  nnodes: 1
  n_gpus_per_node: 2
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
  default_local_dir: ${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/base-v2
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
  val_batch_size: 256
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
    tokenizer_path: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
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
    input_tokenizer: ${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
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
  num_cpus: 16
  timeline_json_file: null

```

</details>

- [exps/ablation-queue-20261005/manifest-all-epochs.json](../artifacts/exps/ablation-queue-20261005/manifest-all-epochs.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "root": "${PROJECT_ROOT}",
  "queue": "${PROJECT_ROOT}/exps/ablation-queue-20261005",
  "code": "${PROJECT_ROOT}/exps/ablation-queue-20261005/code/verl",
  "venv": "${PROJECT_ROOT}/.venv",
  "base": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2",
  "gpu_budget": 8,
  "models": [
    {
      "id": "padding-fast",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005"
    },
    {
      "id": "prompt-fixed",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005"
    },
    {
      "id": "seen",
      "name": "Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "existing": false,
      "variant": "seen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005"
    },
    {
      "id": "prompt-lr3e6",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "existing": false,
      "variant": "unseen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "optim.lr=3e-6"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005"
    }
  ],
  "evals": [
    {
      "id": "base-v2",
      "model": "base",
      "epoch": 0,
      "checkpoint": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2"
    },
    {
      "id": "padding-fast-epoch-1",
      "model": "padding-fast",
      "epoch": 1,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_46"
    },
    {
      "id": "padding-fast-epoch-2",
      "model": "padding-fast",
      "epoch": 2,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_92"
    },
    {
      "id": "padding-fast-epoch-3",
      "model": "padding-fast",
      "epoch": 3,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_138"
    },
    {
      "id": "padding-fast-epoch-4",
      "model": "padding-fast",
      "epoch": 4,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_184"
    },
    {
      "id": "padding-fast-epoch-5",
      "model": "padding-fast",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_230"
    },
    {
      "id": "prompt-fixed-epoch-1",
      "model": "prompt-fixed",
      "epoch": 1,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_46"
    },
    {
      "id": "prompt-fixed-epoch-2",
      "model": "prompt-fixed",
      "epoch": 2,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_92"
    },
    {
      "id": "prompt-fixed-epoch-3",
      "model": "prompt-fixed",
      "epoch": 3,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_138"
    },
    {
      "id": "prompt-fixed-epoch-4",
      "model": "prompt-fixed",
      "epoch": 4,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_184"
    },
    {
      "id": "prompt-fixed-epoch-5",
      "model": "prompt-fixed",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_230"
    },
    {
      "id": "seen-epoch-1",
      "model": "seen",
      "epoch": 1,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_46"
    },
    {
      "id": "seen-epoch-2",
      "model": "seen",
      "epoch": 2,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_92"
    },
    {
      "id": "seen-epoch-3",
      "model": "seen",
      "epoch": 3,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_138"
    },
    {
      "id": "seen-epoch-4",
      "model": "seen",
      "epoch": 4,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_184"
    },
    {
      "id": "seen-epoch-5",
      "model": "seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230"
    },
    {
      "id": "prompt-lr3e6-epoch-1",
      "model": "prompt-lr3e6",
      "epoch": 1,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_46"
    },
    {
      "id": "prompt-lr3e6-epoch-2",
      "model": "prompt-lr3e6",
      "epoch": 2,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_92"
    },
    {
      "id": "prompt-lr3e6-epoch-3",
      "model": "prompt-lr3e6",
      "epoch": 3,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_138"
    },
    {
      "id": "prompt-lr3e6-epoch-4",
      "model": "prompt-lr3e6",
      "epoch": 4,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_184"
    },
    {
      "id": "prompt-lr3e6-epoch-5",
      "model": "prompt-lr3e6",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_230"
    }
  ],
  "protocol": "author-async-v3;3000 response;mean@16 competition/mean@1 MATH;sanity format;no grad accumulation fix",
  "commit": "787575134f097826c956e8b6c950dbc6db68ba2c",
  "data_sha256": {
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet": "48b9c7ec2fb1e070a8912706b49f7d7ce594401f64b1f68247bc83ed2a34d87b",
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet": "fdaa803b505aaccfc1eded139da8d84c73b43e5e0ccba20232e3ff46dcc1f5d2",
    "verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e"
  }
}
```

</details>

- [exps/ablation-queue-20261005/manifest-final-only.json](../artifacts/exps/ablation-queue-20261005/manifest-final-only.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "root": "${PROJECT_ROOT}",
  "queue": "${PROJECT_ROOT}/exps/ablation-queue-20261005",
  "code": "${PROJECT_ROOT}/exps/ablation-queue-20261005/code/verl",
  "venv": "${PROJECT_ROOT}/.venv",
  "base": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2",
  "gpu_budget": 8,
  "models": [
    {
      "id": "padding-fast",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005"
    },
    {
      "id": "prompt-fixed",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005"
    },
    {
      "id": "seen",
      "name": "Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "existing": true,
      "variant": "seen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005"
    },
    {
      "id": "prompt-lr3e6",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "existing": true,
      "variant": "unseen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "optim.lr=3e-6"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005"
    }
  ],
  "evals": [
    {
      "id": "base-v2",
      "model": "base",
      "epoch": 0,
      "checkpoint": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2"
    },
    {
      "id": "padding-fast-epoch-5",
      "model": "padding-fast",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_230"
    },
    {
      "id": "prompt-fixed-epoch-5",
      "model": "prompt-fixed",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_230"
    },
    {
      "id": "seen-epoch-5",
      "model": "seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230"
    },
    {
      "id": "prompt-lr3e6-epoch-5",
      "model": "prompt-lr3e6",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_230"
    }
  ],
  "protocol": "author-async-v3;3000 response;mean@16 competition/mean@1 MATH;sanity format;no grad accumulation fix",
  "commit": "787575134f097826c956e8b6c950dbc6db68ba2c",
  "data_sha256": {
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet": "48b9c7ec2fb1e070a8912706b49f7d7ce594401f64b1f68247bc83ed2a34d87b",
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet": "fdaa803b505aaccfc1eded139da8d84c73b43e5e0ccba20232e3ff46dcc1f5d2",
    "verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e"
  },
  "eval_selection": "base and final epoch only; changed by user; trainings unchanged"
}
```

</details>

- [exps/ablation-queue-20261005/manifest.json](../artifacts/exps/ablation-queue-20261005/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "root": "${PROJECT_ROOT}",
  "queue": "${PROJECT_ROOT}/exps/ablation-queue-20261005",
  "code": "${PROJECT_ROOT}/exps/ablation-queue-20261005/code/verl",
  "venv": "${PROJECT_ROOT}/.venv",
  "base": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2",
  "gpu_budget": 8,
  "models": [
    {
      "id": "padding-fast",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005"
    },
    {
      "id": "prompt-fixed",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "existing": true,
      "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005"
    },
    {
      "id": "seen",
      "name": "Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "existing": true,
      "variant": "seen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005"
    },
    {
      "id": "prompt-lr3e6",
      "name": "Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "existing": true,
      "variant": "unseen",
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "optim.lr=3e-6"
      ],
      "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005"
    }
  ],
  "evals": [
    {
      "id": "base-v2",
      "model": "base",
      "epoch": 0,
      "checkpoint": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2"
    },
    {
      "id": "padding-fast-epoch-5",
      "model": "padding-fast",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_230"
    },
    {
      "id": "prompt-fixed-epoch-5",
      "model": "prompt-fixed",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_230"
    },
    {
      "id": "seen-epoch-5",
      "model": "seen",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230"
    },
    {
      "id": "prompt-lr3e6-epoch-5",
      "model": "prompt-lr3e6",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_230"
    }
  ],
  "protocol": "author-async-v3;3000 response;mean@16 competition/mean@1 MATH;sanity format;no grad accumulation fix",
  "commit": "787575134f097826c956e8b6c950dbc6db68ba2c",
  "data_sha256": {
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet": "48b9c7ec2fb1e070a8912706b49f7d7ce594401f64b1f68247bc83ed2a34d87b",
    "verl/data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet": "fdaa803b505aaccfc1eded139da8d84c73b43e5e0ccba20232e3ff46dcc1f5d2",
    "verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e"
  },
  "eval_selection": "base and final epoch only; changed by user; trainings unchanged"
}
```

</details>

- [exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/model-source.json](../artifacts/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/resolved-config.yaml](../artifacts/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
${PROJECT_ROOT}/exps/ablation-queue-20261005/code/verl/verl/utils/dataset/rl_dataset.py:38: SyntaxWarning: invalid escape sequence '\*'
  """
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
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
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005
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
  final_dir: ${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/final

```

</details>

- [exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/model-source.json](../artifacts/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/resolved-config.yaml](../artifacts/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
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
  lr: 3.0e-06
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
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005
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
  final_dir: ${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/final

```

</details>

## Метрики и полнота результатов

- [exps/ablation-queue-20261005/comparison.json](../artifacts/exps/ablation-queue-20261005/comparison.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "model": "base",
    "accuracy_pct": {
      "APO_AIME24": 0.0,
      "APO_AIME25": 0.0,
      "APO_AMC23": 0.312,
      "APO_MATH300": 0.949
    },
    "tag_counts": {
      "parallel_format": 0,
      "format_error": 5,
      "no_tags": 1911
    },
    "tag_pct": {
      "parallel_format": 0.0,
      "format_error": 0.261,
      "no_tags": 99.739
    }
  },
  {
    "model": "padding-fast",
    "accuracy_pct": {
      "APO_AIME24": 0.833,
      "APO_AIME25": 0.0,
      "APO_AMC23": 10.312,
      "APO_MATH300": 26.899
    },
    "tag_counts": {
      "parallel_format": 1461,
      "format_error": 117,
      "no_tags": 338
    },
    "tag_pct": {
      "parallel_format": 76.253,
      "format_error": 6.106,
      "no_tags": 17.641
    }
  },
  {
    "model": "prompt-fixed",
    "accuracy_pct": {
      "APO_AIME24": 0.625,
      "APO_AIME25": 0.208,
      "APO_AMC23": 10.0,
      "APO_MATH300": 25.633
    },
    "tag_counts": {
      "parallel_format": 1683,
      "format_error": 124,
      "no_tags": 109
    },
    "tag_pct": {
      "parallel_format": 87.839,
      "format_error": 6.472,
      "no_tags": 5.689
    }
  },
  {
    "model": "seen",
    "accuracy_pct": {
      "APO_AIME24": 0.625,
      "APO_AIME25": 0.208,
      "APO_AMC23": 11.25,
      "APO_MATH300": 28.797
    },
    "tag_counts": {
      "parallel_format": 1693,
      "format_error": 84,
      "no_tags": 139
    },
    "tag_pct": {
      "parallel_format": 88.361,
      "format_error": 4.384,
      "no_tags": 7.255
    }
  },
  {
    "model": "prompt-lr3e6",
    "accuracy_pct": {
      "APO_AIME24": 0.625,
      "APO_AIME25": 0.208,
      "APO_AMC23": 9.219,
      "APO_MATH300": 21.519
    },
    "tag_counts": {
      "parallel_format": 1644,
      "format_error": 207,
      "no_tags": 65
    },
    "tag_pct": {
      "parallel_format": 85.804,
      "format_error": 10.804,
      "no_tags": 3.392
    }
  }
]
```

</details>

- [exps/ablation-queue-20261005/results/eval/base-v2/driver.log](../artifacts/exps/ablation-queue-20261005/results/eval/base-v2/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/ablation-queue-20261005/results/eval/base-v2/summary.json](../artifacts/exps/ablation-queue-20261005/results/eval/base-v2/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "base-v2",
    "model": "base",
    "epoch": 0,
    "checkpoint": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2"
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
      "parallel": 0.0020833333333333333,
      "format": 1.0,
      "parallel_format": 0.0,
      "format_error": 0.0020833333333333333,
      "no_tags": 0.9979166666666667
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0,
      "observed_pass": 0.0,
      "bootstrap_best": 0.0,
      "parallel": 0.0,
      "format": 1.0,
      "parallel_format": 0.0,
      "format_error": 0.0020833333333333333,
      "no_tags": 0.9979166666666667
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.003125,
      "observed_pass": 0.05,
      "bootstrap_best": 0.032850000000000004,
      "parallel": 0.0,
      "format": 0.9984375,
      "parallel_format": 0.0,
      "format_error": 0.0015625,
      "no_tags": 0.9984375
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.00949367088607595,
      "observed_pass": 0.00949367088607595,
      "bootstrap_best": null,
      "parallel": 0.0,
      "format": 0.9936708860759493,
      "parallel_format": 0.0,
      "format_error": 0.006329113924050633,
      "no_tags": 0.9936708860759493
    }
  }
}
```

</details>

- [exps/ablation-queue-20261005/results/eval/padding-fast-epoch-5/driver.log](../artifacts/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/ablation-queue-20261005/results/eval/padding-fast-epoch-5/summary.json](../artifacts/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "padding-fast-epoch-5",
    "model": "padding-fast",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_230"
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.008333333333333333,
      "observed_pass": 0.13333333333333333,
      "bootstrap_best": 0.08643333333333333,
      "parallel": 0.7729166666666667,
      "format": 0.9395833333333333,
      "parallel_format": 0.7145833333333333,
      "format_error": 0.06041666666666667,
      "no_tags": 0.225
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0,
      "observed_pass": 0.0,
      "bootstrap_best": 0.0,
      "parallel": 0.7958333333333333,
      "format": 0.9270833333333334,
      "parallel_format": 0.725,
      "format_error": 0.075,
      "no_tags": 0.2
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.103125,
      "observed_pass": 0.45,
      "bootstrap_best": 0.392975,
      "parallel": 0.8375,
      "format": 0.9359375,
      "parallel_format": 0.7765625,
      "format_error": 0.065625,
      "no_tags": 0.1578125
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.2689873417721519,
      "observed_pass": 0.2689873417721519,
      "bootstrap_best": null,
      "parallel": 0.8955696202531646,
      "format": 0.9683544303797469,
      "parallel_format": 0.8639240506329114,
      "format_error": 0.03164556962025317,
      "no_tags": 0.10443037974683544
    }
  }
}
```

</details>

- [exps/ablation-queue-20261005/results/eval/prompt-fixed-epoch-5/driver.log](../artifacts/exps/ablation-queue-20261005/results/eval/prompt-fixed-epoch-5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/ablation-queue-20261005/results/eval/prompt-fixed-epoch-5/summary.json](../artifacts/exps/ablation-queue-20261005/results/eval/prompt-fixed-epoch-5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "prompt-fixed-epoch-5",
    "model": "prompt-fixed",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_230"
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.00625,
      "observed_pass": 0.1,
      "bootstrap_best": 0.06326666666666667,
      "parallel": 0.9145833333333333,
      "format": 0.9375,
      "parallel_format": 0.8541666666666666,
      "format_error": 0.06666666666666667,
      "no_tags": 0.07916666666666666
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.021233333333333333,
      "parallel": 0.91875,
      "format": 0.9333333333333333,
      "parallel_format": 0.8458333333333333,
      "format_error": 0.075,
      "no_tags": 0.07916666666666666
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.1,
      "observed_pass": 0.475,
      "bootstrap_best": 0.394525,
      "parallel": 0.9578125,
      "format": 0.9328125,
      "parallel_format": 0.8890625,
      "format_error": 0.071875,
      "no_tags": 0.0390625
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.2563291139240506,
      "observed_pass": 0.2563291139240506,
      "bootstrap_best": null,
      "parallel": 0.9715189873417721,
      "format": 0.9683544303797469,
      "parallel_format": 0.9430379746835443,
      "format_error": 0.03164556962025317,
      "no_tags": 0.02531645569620253
    }
  }
}
```

</details>

- [exps/ablation-queue-20261005/results/eval/prompt-lr3e6-epoch-5/driver.log](../artifacts/exps/ablation-queue-20261005/results/eval/prompt-lr3e6-epoch-5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/ablation-queue-20261005/results/eval/prompt-lr3e6-epoch-5/summary.json](../artifacts/exps/ablation-queue-20261005/results/eval/prompt-lr3e6-epoch-5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "prompt-lr3e6-epoch-5",
    "model": "prompt-lr3e6",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_230"
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.00625,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.05090000000000001,
      "parallel": 0.9458333333333333,
      "format": 0.9208333333333333,
      "parallel_format": 0.8604166666666667,
      "format_error": 0.08541666666666667,
      "no_tags": 0.05416666666666667
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.020833333333333332,
      "parallel": 0.95625,
      "format": 0.8895833333333333,
      "parallel_format": 0.8354166666666667,
      "format_error": 0.12291666666666666,
      "no_tags": 0.041666666666666664
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.0921875,
      "observed_pass": 0.6,
      "bootstrap_best": 0.497975,
      "parallel": 0.975,
      "format": 0.8796875,
      "parallel_format": 0.85625,
      "format_error": 0.1234375,
      "no_tags": 0.0203125
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.21518987341772153,
      "observed_pass": 0.21518987341772153,
      "bootstrap_best": null,
      "parallel": 0.9778481012658228,
      "format": 0.9113924050632911,
      "parallel_format": 0.8924050632911392,
      "format_error": 0.08860759493670886,
      "no_tags": 0.0189873417721519
    }
  }
}
```

</details>

- [exps/ablation-queue-20261005/results/eval/seen-epoch-5/driver.log](../artifacts/exps/ablation-queue-20261005/results/eval/seen-epoch-5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/ablation-queue-20261005/results/eval/seen-epoch-5/summary.json](../artifacts/exps/ablation-queue-20261005/results/eval/seen-epoch-5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "seen-epoch-5",
    "model": "seen",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230"
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.00625,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.05223333333333333,
      "parallel": 0.9,
      "format": 0.9479166666666666,
      "parallel_format": 0.8416666666666667,
      "format_error": 0.06041666666666667,
      "no_tags": 0.09791666666666667
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.020933333333333335,
      "parallel": 0.89375,
      "format": 0.9625,
      "parallel_format": 0.8604166666666667,
      "format_error": 0.04375,
      "no_tags": 0.09583333333333334
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.1125,
      "observed_pass": 0.525,
      "bootstrap_best": 0.469125,
      "parallel": 0.9453125,
      "format": 0.965625,
      "parallel_format": 0.9078125,
      "format_error": 0.0375,
      "no_tags": 0.0546875
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.2879746835443038,
      "observed_pass": 0.2879746835443038,
      "bootstrap_best": null,
      "parallel": 0.9651898734177216,
      "format": 0.9715189873417721,
      "parallel_format": 0.9335443037974683,
      "format_error": 0.03164556962025317,
      "no_tags": 0.03481012658227848
    }
  }
}
```

</details>

- [exps/ablation-queue-20261005/status-before-final-only.json](../artifacts/exps/ablation-queue-20261005/status-before-final-only.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train-padding-fast": {
    "status": "complete",
    "updated": "2026-10-05T18:03:36.838711+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005"
  },
  "train-prompt-fixed": {
    "status": "complete",
    "updated": "2026-10-05T18:03:36.845924+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005"
  },
  "train-seen": {
    "status": "complete",
    "updated": "2026-10-05T18:18:26.545603+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005"
  },
  "train-prompt-lr3e6": {
    "status": "complete",
    "updated": "2026-10-05T18:34:47.078777+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005"
  },
  "eval-base-v2": {
    "status": "running",
    "updated": "2026-10-05T18:34:47.084369+00:00",
    "gpus": [
      0,
      1
    ],
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/base-v2"
  },
  "eval-padding-fast-epoch-1": {
    "status": "running",
    "updated": "2026-10-05T18:34:47.092601+00:00",
    "gpus": [
      2,
      3
    ],
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-1"
  },
  "eval-padding-fast-epoch-2": {
    "status": "running",
    "updated": "2026-10-05T18:34:47.086894+00:00",
    "gpus": [
      4,
      5
    ],
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-2"
  },
  "eval-padding-fast-epoch-3": {
    "status": "running",
    "updated": "2026-10-05T18:34:47.089812+00:00",
    "gpus": [
      6,
      7
    ],
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-3"
  },
  "eval-padding-fast-epoch-4": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.796769+00:00"
  },
  "eval-padding-fast-epoch-5": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.799332+00:00"
  },
  "eval-prompt-fixed-epoch-1": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.801600+00:00"
  },
  "eval-prompt-fixed-epoch-2": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.803691+00:00"
  },
  "eval-prompt-fixed-epoch-3": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.805824+00:00"
  },
  "eval-prompt-fixed-epoch-4": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.807953+00:00"
  },
  "eval-prompt-fixed-epoch-5": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.810082+00:00"
  },
  "eval-seen-epoch-1": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.812187+00:00"
  },
  "eval-seen-epoch-2": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.814267+00:00"
  },
  "eval-seen-epoch-3": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.816536+00:00"
  },
  "eval-seen-epoch-4": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.818671+00:00"
  },
  "eval-seen-epoch-5": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.821185+00:00"
  },
  "eval-prompt-lr3e6-epoch-1": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.823501+00:00"
  },
  "eval-prompt-lr3e6-epoch-2": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.825503+00:00"
  },
  "eval-prompt-lr3e6-epoch-3": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.827654+00:00"
  },
  "eval-prompt-lr3e6-epoch-4": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.829891+00:00"
  },
  "eval-prompt-lr3e6-epoch-5": {
    "status": "queued",
    "updated": "2026-10-05T18:03:36.832106+00:00"
  }
}
```

</details>

- [exps/ablation-queue-20261005/status.json](../artifacts/exps/ablation-queue-20261005/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train-padding-fast": {
    "status": "complete",
    "updated": "2026-10-05T18:34:47.347137+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005"
  },
  "train-prompt-fixed": {
    "status": "complete",
    "updated": "2026-10-05T18:34:47.353118+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005"
  },
  "train-seen": {
    "status": "complete",
    "updated": "2026-10-05T18:34:47.358822+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005"
  },
  "train-prompt-lr3e6": {
    "status": "complete",
    "updated": "2026-10-05T18:34:47.363961+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005"
  },
  "eval-base-v2": {
    "status": "complete",
    "updated": "2026-10-05T18:54:05.004641+00:00",
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/base-v2",
    "answers": 1916
  },
  "eval-padding-fast-epoch-5": {
    "status": "complete",
    "updated": "2026-10-05T18:53:47.855943+00:00",
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/padding-fast-epoch-5",
    "answers": 1916
  },
  "eval-prompt-fixed-epoch-5": {
    "status": "complete",
    "updated": "2026-10-05T18:52:15.064275+00:00",
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/prompt-fixed-epoch-5",
    "answers": 1916
  },
  "eval-seen-epoch-5": {
    "status": "complete",
    "updated": "2026-10-05T18:53:31.727345+00:00",
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/seen-epoch-5",
    "answers": 1916
  },
  "eval-prompt-lr3e6-epoch-5": {
    "status": "complete",
    "updated": "2026-10-05T19:10:57.785427+00:00",
    "results": "${PROJECT_ROOT}/exps/ablation-queue-20261005/results/eval/prompt-lr3e6-epoch-5",
    "answers": 1916
  }
}
```

</details>

- [exps/ablation-queue-20261005/summary.csv](../artifacts/exps/ablation-queue-20261005/summary.csv) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/ablation-queue-20261005/summary.json](../artifacts/exps/ablation-queue-20261005/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-05T19:10:57.809306+00:00",
  "evaluations": [
    {
      "complete": true,
      "job": {
        "id": "base-v2",
        "model": "base",
        "epoch": 0,
        "checkpoint": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2"
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
          "parallel": 0.0020833333333333333,
          "format": 1.0,
          "parallel_format": 0.0,
          "format_error": 0.0020833333333333333,
          "no_tags": 0.9979166666666667
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0,
          "observed_pass": 0.0,
          "bootstrap_best": 0.0,
          "parallel": 0.0,
          "format": 1.0,
          "parallel_format": 0.0,
          "format_error": 0.0020833333333333333,
          "no_tags": 0.9979166666666667
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.003125,
          "observed_pass": 0.05,
          "bootstrap_best": 0.032850000000000004,
          "parallel": 0.0,
          "format": 0.9984375,
          "parallel_format": 0.0,
          "format_error": 0.0015625,
          "no_tags": 0.9984375
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.00949367088607595,
          "observed_pass": 0.00949367088607595,
          "bootstrap_best": null,
          "parallel": 0.0,
          "format": 0.9936708860759493,
          "parallel_format": 0.0,
          "format_error": 0.006329113924050633,
          "no_tags": 0.9936708860759493
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "padding-fast-epoch-5",
        "model": "padding-fast",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005/global_step_230"
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.008333333333333333,
          "observed_pass": 0.13333333333333333,
          "bootstrap_best": 0.08643333333333333,
          "parallel": 0.7729166666666667,
          "format": 0.9395833333333333,
          "parallel_format": 0.7145833333333333,
          "format_error": 0.06041666666666667,
          "no_tags": 0.225
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0,
          "observed_pass": 0.0,
          "bootstrap_best": 0.0,
          "parallel": 0.7958333333333333,
          "format": 0.9270833333333334,
          "parallel_format": 0.725,
          "format_error": 0.075,
          "no_tags": 0.2
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.103125,
          "observed_pass": 0.45,
          "bootstrap_best": 0.392975,
          "parallel": 0.8375,
          "format": 0.9359375,
          "parallel_format": 0.7765625,
          "format_error": 0.065625,
          "no_tags": 0.1578125
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.2689873417721519,
          "observed_pass": 0.2689873417721519,
          "bootstrap_best": null,
          "parallel": 0.8955696202531646,
          "format": 0.9683544303797469,
          "parallel_format": 0.8639240506329114,
          "format_error": 0.03164556962025317,
          "no_tags": 0.10443037974683544
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "prompt-fixed-epoch-5",
        "model": "prompt-fixed",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-fixed-20261005/global_step_230"
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.00625,
          "observed_pass": 0.1,
          "bootstrap_best": 0.06326666666666667,
          "parallel": 0.9145833333333333,
          "format": 0.9375,
          "parallel_format": 0.8541666666666666,
          "format_error": 0.06666666666666667,
          "no_tags": 0.07916666666666666
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.021233333333333333,
          "parallel": 0.91875,
          "format": 0.9333333333333333,
          "parallel_format": 0.8458333333333333,
          "format_error": 0.075,
          "no_tags": 0.07916666666666666
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.1,
          "observed_pass": 0.475,
          "bootstrap_best": 0.394525,
          "parallel": 0.9578125,
          "format": 0.9328125,
          "parallel_format": 0.8890625,
          "format_error": 0.071875,
          "no_tags": 0.0390625
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.2563291139240506,
          "observed_pass": 0.2563291139240506,
          "bootstrap_best": null,
          "parallel": 0.9715189873417721,
          "format": 0.9683544303797469,
          "parallel_format": 0.9430379746835443,
          "format_error": 0.03164556962025317,
          "no_tags": 0.02531645569620253
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "seen-epoch-5",
        "model": "seen",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-queue-20261005/global_step_230"
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.00625,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.05223333333333333,
          "parallel": 0.9,
          "format": 0.9479166666666666,
          "parallel_format": 0.8416666666666667,
          "format_error": 0.06041666666666667,
          "no_tags": 0.09791666666666667
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.020933333333333335,
          "parallel": 0.89375,
          "format": 0.9625,
          "parallel_format": 0.8604166666666667,
          "format_error": 0.04375,
          "no_tags": 0.09583333333333334
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.1125,
          "observed_pass": 0.525,
          "bootstrap_best": 0.469125,
          "parallel": 0.9453125,
          "format": 0.965625,
          "parallel_format": 0.9078125,
          "format_error": 0.0375,
          "no_tags": 0.0546875
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.2879746835443038,
          "observed_pass": 0.2879746835443038,
          "bootstrap_best": null,
          "parallel": 0.9651898734177216,
          "format": 0.9715189873417721,
          "parallel_format": 0.9335443037974683,
          "format_error": 0.03164556962025317,
          "no_tags": 0.03481012658227848
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "prompt-lr3e6-epoch-5",
        "model": "prompt-lr3e6",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-prompt-lr3e6-20261005/global_step_230"
      },
      "answers": 1916,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.00625,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.05090000000000001,
          "parallel": 0.9458333333333333,
          "format": 0.9208333333333333,
          "parallel_format": 0.8604166666666667,
          "format_error": 0.08541666666666667,
          "no_tags": 0.05416666666666667
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.020833333333333332,
          "parallel": 0.95625,
          "format": 0.8895833333333333,
          "parallel_format": 0.8354166666666667,
          "format_error": 0.12291666666666666,
          "no_tags": 0.041666666666666664
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.0921875,
          "observed_pass": 0.6,
          "bootstrap_best": 0.497975,
          "parallel": 0.975,
          "format": 0.8796875,
          "parallel_format": 0.85625,
          "format_error": 0.1234375,
          "no_tags": 0.0203125
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.21518987341772153,
          "observed_pass": 0.21518987341772153,
          "bootstrap_best": null,
          "parallel": 0.9778481012658228,
          "format": 0.9113924050632911,
          "parallel_format": 0.8924050632911392,
          "format_error": 0.08860759493670886,
          "no_tags": 0.0189873417721519
        }
      }
    }
  ],
  "failed_or_skipped": [],
  "protocol": "author-async-v3;3000 response;mean@16 competition/mean@1 MATH;sanity format;no grad accumulation fix"
}
```

</details>

## Исходники рецепта и награды

- [exps/ablation-queue-20261005/launch.sh](../artifacts/exps/ablation-queue-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
