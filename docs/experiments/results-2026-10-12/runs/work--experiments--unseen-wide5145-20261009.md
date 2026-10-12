# work/experiments/unseen-wide5145-20261009

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/manifest-update.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/manifest-update.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": "2026-10-09T20:53:33.307746+00:00",
  "changed": [
    {
      "path": "tests/test_counted_unseen.py",
      "before": "b6c3eceea76c4ab60583dd07a409466ceb4bbf2852fd41186cf353e5c6e8a16b",
      "after": "62f4ea4359825ab1c9215e4c49fbf1a874561369c73eeeb4bdd1955a64e31c79"
    },
    {
      "path": "verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py",
      "before": "6b68c18fc35cad77ba01774c1bf1af523fc65cc5acd25a768ac2e84861238ec4",
      "after": "a5efddd9ee8236dc69e04d8416d1448fbe7ab9a6f98e8524f78e279ec0da8b31"
    }
  ]
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/production-resolved-think-prefix.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/production-resolved-think-prefix.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 32
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    loss_agg_mode: seq-mean-token-mean
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
    sort_microbatches_by_length: true
    trim_parallel_padding: true
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
    top_p: 1.0
    prompt_length: 2000
    response_length: 8192
    dtype: bfloat16
    gpu_memory_utilization: 0.45
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
      num_workers: 4
      agent_loop_config_path: null
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 8192
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
      force_think_prefix: true
      record_policy_calls: true
      min_paths: 2
      max_paths: 8
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: true
    load_format: dummy_dtensor
    layered_summon: false
    structured_unseen: true
  hybrid_engine: true
  model:
    path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: true
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
  experiment_name: counted-unseen-s1
  logger:
  - console
  - wandb
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/config-inspection-output/rollouts
  validation_data_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/config-inspection-output/validation
  nnodes: 1
  n_gpus_per_node: 1
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/config-inspection-output/checkpoints
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
  max_response_length: 8192
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
    tokenizer_path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final
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
  ppo_mini_batch_size: 32
  ppo_micro_batch_size: null
  ppo_micro_batch_size_per_gpu: null
  use_dynamic_bsz: false
  ppo_max_token_len_per_gpu: 32768
  forward_max_token_len_per_gpu: 32768
  ppo_epochs: 1
  shuffle: false
  cliprange_value: 0.5
  loss_agg_mode: seq-mean-token-mean
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
    input_tokenizer: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final
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
  num_cpus: 8
  timeline_json_file: null

```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/rl-code-manifest.before-header-fix.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/rl-code-manifest.before-header-fix.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "path": "tests/test_counted_unseen.py",
    "sha256": "b6c3eceea76c4ab60583dd07a409466ceb4bbf2852fd41186cf353e5c6e8a16b",
    "added": true
  },
  {
    "path": "tests/legacy_test_parallel_loop.py",
    "sha256": "2e10c2df1198eeeff41db19731c670dffbaf4f222a81e1a1ead1eb9882556a98",
    "added": true
  },
  {
    "path": "verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py",
    "sha256": "6b68c18fc35cad77ba01774c1bf1af523fc65cc5acd25a768ac2e84861238ec4",
    "added": false
  },
  {
    "path": "verl/verl/utils/parallel_structure.py",
    "sha256": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "added": true
  },
  {
    "path": "verl/verl/trainer/config/rl_qwen3_06b.yaml",
    "sha256": "dae66fc0da7f86bed28be232026a2753d02d14a8b24a220f54a516c1eb075d29",
    "added": false
  },
  {
    "path": "verl/verl/utils/reward_score/counted_parallel.py",
    "sha256": "fd3f3cfa45949a48c3c35f1f8f522d1a692dfd0ea62e0520af2321117aeaf8dc",
    "added": true
  },
  {
    "path": "verl/verl/workers/actor/rollout_context.py",
    "sha256": "d34654a792e3ca1ff8507857b628e6da86a14ac1245f05e3cb10f7ac2281977e",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py",
    "sha256": "c4fc7465216763cd48fb2d3cba3e6064557bc44620e4f8afa0d0ee8b3e64ca59",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/vllm_rollout_spmd.py",
    "sha256": "0d55c4fa254023f2bbf5df75b387daf24dc8ba712ad90ab54e38c2e9fa059aae",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/structured_worker.py",
    "sha256": "bc9dc0dc0e4df508a43ca164386f846c7988d0803a1e63bc37658d08f747af14",
    "added": true
  },
  {
    "path": "tests/test_parallel_loop.py",
    "deleted": true,
    "reason": "Preserved as legacy_test_parallel_loop.py"
  }
]
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/manifest.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "dataset": "HuggingFaceH4/MATH-500",
  "questions": 500,
  "samples_per_question": 1,
  "checkpoint": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final",
  "checkpoint_sha256": "fa9e92602b36042e0f4f488b5ccf6a8956826978f9d9d9cbfa9e80792a3be6c6",
  "questions_sha256": "a2645512280d4499c35e9c781f35e04c643b30ebc20b13d118878e4f2f9b3486",
  "previous_questions_sha256": "a2645512280d4499c35e9c781f35e04c643b30ebc20b13d118878e4f2f9b3486",
  "system_prompt": "You solve mathematical problems with clear, accurate worked reasoning.\nPut all your solution work inside one <think>...</think> block. Inside it, use\nordinary prose and equations for setup and necessary sequential work. Define\nquantities and show each governing relation, numeric substitution, arithmetic,\nand meaning of the result. Explain non-obvious dependencies and category totals.\n\nWhen independent useful calculations are available, explain the step, write\nPlan:, and list concrete assignments as 1: ..., 2: ..., through N: .... Choose\nN from 2 through 8 from the available work. Prefer a wider useful cut with 4--6\npaths when available; small dependency graphs can use 2--3 or stay sequential.\nAssignments may return computed counts, rates, subtotals or other useful terms.\nNever precompute unknown assignment results in the plan. Given constants and\nmere aliases do not need their own paths. Do not invent work to increase width.\n\nAfter the plan write exactly <Parallel>N on its own line. Then write N sibling\npaths in order. Each begins with <Path>I and a newline and ends with </Path>.\nIDs are integers 1 through N and restart at 1 in each fork. Each path sees only\nthe problem, the shared prefix before its fork and its own assignment. It can\nfollow dependent calculations locally and recompute a short cheap prerequisite;\nit cannot use a sibling's result from the same fork. No nested forks or round\nlabels. No mandatory Result: field and no Final Answer: inside a path.\n\nClose with </Parallel>, then <Summary>...</Summary>. Combine actual path outputs\nwith explicit calculations and explain their use. An occasional verification\npath may independently recompute the same substantive quantity as another path,\neven by the same method. Mark its purpose in the plan and compare the results\nexplicitly in the summary. Do not copy a sibling's result or use redundant\nbranches merely to increase width. If the results disagree, resolve the issue\nbefore relying on them. Continue with new forks only when useful work remains;\nthere is no fixed number of rounds. Keep shared setup and summaries concise.\n\nAfter the requested result is justified, close </think>. Outside the think\nblock give a short concluding solution with the decisive arithmetic and units,\nthen end on a standalone line: Final Answer: \\boxed{...}. Do not put new forks\nor an extended derivation in the concluding solution. If an essential gap\nremains, explain it honestly and end with Final Answer: unresolved.\n",
  "max_prompt_tokens": 2048,
  "max_response_tokens": 30720,
  "max_model_len": 32768,
  "max_path_tokens": 8192,
  "temperature": 0.6,
  "top_p": 0.95,
  "top_k": 20,
  "seed": 42,
  "min_paths": 2,
  "max_paths": 8,
  "max_forks": 0,
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
  "scorer": "Math-Verify 0.8.0, exact previous reference-blind scorer",
  "runtime": "Same counted Unseen loop and structured vLLM-weight backend, eight independent TP=1 evaluation workers; no Ray/FSDP/optimizer",
  "differences_from_previous": [
    "Current SFT student system prompt",
    "Model chooses 2..8 branches instead of two forced branches",
    "Correct Unseen masks and positions instead of causal inference"
  ],
  "previous_results": {
    "gsm_infinite_ep5": {
      "complete": true,
      "model": "gsm_infinite_ep5",
      "questions": 500,
      "correct": 84,
      "accuracy": 0.168,
      "ci95": [
        0.13778823297684417,
        0.20327432908962656
      ],
      "parallel_ratio": 0.11,
      "multi_round_ratio": 0.012,
      "fork_histogram": {
        "1": 49,
        "0": 445,
        "2": 5,
        "3": 1
      },
      "executed_width_histogram": {
        "2": 62
      },
      "rendered_width_histogram": {
        "2": 62
      },
      "first_fork_relative_position": {
        "mean": 0.23228550308156687,
        "median": 0.2304147465437788,
        "p90": 0.4415841584158416,
        "max": 0.5676392572944297
      },
      "path_token_share": {
        "mean": 0.023287057796204776,
        "median": 0.0,
        "p90": 0.0041100582258248655,
        "max": 0.6139130434782609
      },
      "phase_tokens": {
        "main": 2106573,
        "path": 6359,
        "summary": 2908
      },
      "response_tokens": {
        "mean": 4232.3,
        "median": 256.0,
        "p90": 30720,
        "max": 30720
      },
      "generated_tokens": {
        "mean": 4231.68,
        "median": 254.0,
        "p90": 30720,
        "max": 30720
      },
      "path_generated_tokens": {
        "mean": 51.28225806451613,
        "median": 37.0,
        "p90": 86,
        "max": 518
      },
      "critical_decode_depth": {
        "mean": 4226.608,
        "median": 250.5,
        "p90": 30720,
        "max": 30720
      },
      "theoretical_decode_work_over_depth": {
        "mean": 1.0109148865106101,
        "median": 1.0,
        "p90": 1.0016423533958072,
        "max": 1.3110047846889952
      },
      "generation_calls": {
        "mean": 1.496,
        "median": 1.0,
        "p90": 5,
        "max": 13
      },
      "unbalanced_tags": 6,
      "strict_format_among_parallel": 0.9272727272727272,
      "exact_duplicate_paths": 10,
      "samples_with_duplicate_paths": 10,
      "path_calls_without_sampled_close": 1,
      "summary_calls_without_sampled_close": 0,
      "path_calls_at_token_cap": 0,
      "response_budget_exhausted": 60,
      "truncated": 0,
      "invalid_final_answers": 64,
      "scorer_errors": 0,
      "accuracy_by_parallel": {
        "False": {
          "n": 445,
          "correct": 79,
          "accuracy": 0.17752808988764046
        },
        "True": {
          "n": 55,
          "correct": 5,
          "accuracy": 0.09090909090909091
        }
      },
      "accuracy_by_subject": {
        "Algebra": {
          "n": 124,
          "correct": 28,
          "accuracy": 0.22580645161290322
        },
        "Counting & Probability": {
          "n": 38,
          "correct": 9,
          "accuracy": 0.23684210526315788
        },
        "Geometry": {
          "n": 41,
          "correct": 6,
          "accuracy": 0.14634146341463414
        },
        "Intermediate Algebra": {
          "n": 97,
          "correct": 9,
          "accuracy": 0.09278350515463918
        },
        "Number Theory": {
          "n": 62,
          "correct": 8,
          "accuracy": 0.12903225806451613
        },
        "Prealgebra": {
          "n": 82,
          "correct": 15,
          "accuracy": 0.18292682926829268
        },
        "Precalculus": {
          "n": 56,
          "correct": 9,
          "accuracy": 0.16071428571428573
        }
      },
      "accuracy_by_level": {
        "1": {
          "n": 43,
          "correct": 18,
          "accuracy": 0.4186046511627907
        },
        "2": {
          "n": 90,
          "correct": 27,
          "accuracy": 0.3
        },
        "3": {
          "n": 105,
          "correct": 19,
          "accuracy": 0.18095238095238095
        },
        "4": {
          "n": 128,
          "correct": 12,
          "accuracy": 0.09375
        },
        "5": {
          "n": 134,
          "correct": 8,
          "accuracy": 0.05970149253731343
        }
      },
      "raw_trace_count": 504,
      "scored_unique_traces": 500,
      "limitations": [
        "Two paths are imposed by runtime.",
        "Decode work/depth is not measured wall-clock speedup.",
        "Text equality only detects literal duplicate paths, not semantic duplication or valid reasoning.",
        "Unseen custom mask/positions are not applied to vLLM continuation."
      ]
    },
    "sft_messages_ep5": {
      "complete": true,
      "model": "sft_messages_ep5",
      "questions": 500,
      "correct": 79,
      "accuracy": 0.158,
      "ci95": [
        0.1286526978644355,
        0.19256235101126623
      ],
      "parallel_ratio": 0.056,
      "multi_round_ratio": 0.0,
      "fork_histogram": {
        "0": 472,
        "1": 28
      },
      "executed_width_histogram": {
        "2": 28
      },
      "rendered_width_histogram": {
        "2": 28
      },
      "first_fork_relative_position": {
        "mean": 0.20665706769567338,
        "median": 0.21563088512241052,
        "p90": 0.42065491183879095,
        "max": 0.48788927335640137
      },
      "path_token_share": {
        "mean": 0.012026271198015914,
        "median": 0.0,
        "p90": 0.0,
        "max": 0.673352435530086
      },
      "phase_tokens": {
        "main": 1114872,
        "path": 11257,
        "summary": 21294
      },
      "response_tokens": {
        "mean": 2295.128,
        "median": 135.0,
        "p90": 1052,
        "max": 30720
      },
      "generated_tokens": {
        "mean": 2294.846,
        "median": 135.0,
        "p90": 1047,
        "max": 30720
      },
      "path_generated_tokens": {
        "mean": 201.01785714285714,
        "median": 32.5,
        "p90": 114,
        "max": 8192
      },
      "critical_decode_depth": {
        "mean": 2292.896,
        "median": 135.0,
        "p90": 1044,
        "max": 30720
      },
      "theoretical_decode_work_over_depth": {
        "mean": 1.004431249130656,
        "median": 1.0,
        "p90": 1.0,
        "max": 1.2714285714285714
      },
      "generation_calls": {
        "mean": 1.224,
        "median": 1.0,
        "p90": 1,
        "max": 5
      },
      "unbalanced_tags": 52,
      "strict_format_among_parallel": 0.5357142857142857,
      "exact_duplicate_paths": 5,
      "samples_with_duplicate_paths": 5,
      "path_calls_without_sampled_close": 10,
      "summary_calls_without_sampled_close": 8,
      "path_calls_at_token_cap": 1,
      "response_budget_exhausted": 17,
      "truncated": 0,
      "invalid_final_answers": 46,
      "scorer_errors": 0,
      "accuracy_by_parallel": {
        "False": {
          "n": 472,
          "correct": 78,
          "accuracy": 0.1652542372881356
        },
        "True": {
          "n": 28,
          "correct": 1,
          "accuracy": 0.03571428571428571
        }
      },
      "accuracy_by_subject": {
        "Algebra": {
          "n": 124,
          "correct": 29,
          "accuracy": 0.23387096774193547
        },
        "Counting & Probability": {
          "n": 38,
          "correct": 6,
          "accuracy": 0.15789473684210525
        },
        "Geometry": {
          "n": 41,
          "correct": 4,
          "accuracy": 0.0975609756097561
        },
        "Intermediate Algebra": {
          "n": 97,
          "correct": 12,
          "accuracy": 0.12371134020618557
        },
        "Number Theory": {
          "n": 62,
          "correct": 6,
          "accuracy": 0.0967741935483871
        },
        "Prealgebra": {
          "n": 82,
          "correct": 17,
          "accuracy": 0.2073170731707317
        },
        "Precalculus": {
          "n": 56,
          "correct": 5,
          "accuracy": 0.08928571428571429
        }
      },
      "accuracy_by_level": {
        "1": {
          "n": 43,
          "correct": 20,
          "accuracy": 0.46511627906976744
        },
        "2": {
          "n": 90,
          "correct": 26,
          "accuracy": 0.28888888888888886
        },
        "3": {
          "n": 105,
          "correct": 19,
          "accuracy": 0.18095238095238095
        },
        "4": {
          "n": 128,
          "correct": 7,
          "accuracy": 0.0546875
        },
        "5": {
          "n": 134,
          "correct": 7,
          "accuracy": 0.05223880597014925
        }
      },
      "raw_trace_count": 504,
      "scored_unique_traces": 500,
      "limitations": [
        "Two paths are imposed by runtime.",
        "Decode work/depth is not measured wall-clock speedup.",
        "Text equality only detects literal duplicate paths, not semantic duplication or valid reasoning.",
        "Unseen custom mask/positions are not applied to vLLM continuation."
      ]
    },
    "mixed_ep1": {
      "complete": true,
      "model": "mixed_ep1",
      "questions": 500,
      "correct": 61,
      "accuracy": 0.122,
      "ci95": [
        0.0961592783150937,
        0.15360472307383977
      ],
      "parallel_ratio": 0.97,
      "multi_round_ratio": 0.002,
      "fork_histogram": {
        "1": 484,
        "0": 15,
        "2": 1
      },
      "executed_width_histogram": {
        "2": 486
      },
      "rendered_width_histogram": {
        "2": 483,
        "0": 4,
        "1": 1
      },
      "first_fork_relative_position": {
        "mean": 0.15606282520748724,
        "median": 0.14754098360655737,
        "p90": 0.2589928057553957,
        "max": 0.4444444444444444
      },
      "path_token_share": {
        "mean": 0.5437661236804713,
        "median": 0.5588416323013479,
        "p90": 0.7642276422764228,
        "max": 0.9863523573200993
      },
      "phase_tokens": {
        "main": 85218,
        "path": 94808,
        "summary": 84962
      },
      "response_tokens": {
        "mean": 534.838,
        "median": 223.0,
        "p90": 509,
        "max": 30720
      },
      "generated_tokens": {
        "mean": 529.976,
        "median": 218.0,
        "p90": 504,
        "max": 30715
      },
      "path_generated_tokens": {
        "mean": 97.53909465020575,
        "median": 58.0,
        "p90": 140,
        "max": 8192
      },
      "critical_decode_depth": {
        "mean": 474.498,
        "median": 168.0,
        "p90": 411,
        "max": 30701
      },
      "theoretical_decode_work_over_depth": {
        "mean": 1.2780731941340286,
        "median": 1.2764863268355398,
        "p90": 1.4574468085106382,
        "max": 1.7401129943502824
      },
      "generation_calls": {
        "mean": 4.888,
        "median": 5.0,
        "p90": 5,
        "max": 9
      },
      "unbalanced_tags": 150,
      "strict_format_among_parallel": 0.7154639175257732,
      "exact_duplicate_paths": 8,
      "samples_with_duplicate_paths": 8,
      "path_calls_without_sampled_close": 57,
      "summary_calls_without_sampled_close": 144,
      "path_calls_at_token_cap": 1,
      "response_budget_exhausted": 2,
      "truncated": 0,
      "invalid_final_answers": 2,
      "scorer_errors": 0,
      "accuracy_by_parallel": {
        "False": {
          "n": 15,
          "correct": 3,
          "accuracy": 0.2
        },
        "True": {
          "n": 485,
          "correct": 58,
          "accuracy": 0.11958762886597939
        }
      },
      "accuracy_by_subject": {
        "Algebra": {
          "n": 124,
          "correct": 20,
          "accuracy": 0.16129032258064516
        },
        "Counting & Probability": {
          "n": 38,
          "correct": 2,
          "accuracy": 0.05263157894736842
        },
        "Geometry": {
          "n": 41,
          "correct": 4,
          "accuracy": 0.0975609756097561
        },
        "Intermediate Algebra": {
          "n": 97,
          "correct": 9,
          "accuracy": 0.09278350515463918
        },
        "Number Theory": {
          "n": 62,
          "correct": 6,
          "accuracy": 0.0967741935483871
        },
        "Prealgebra": {
          "n": 82,
          "correct": 15,
          "accuracy": 0.18292682926829268
        },
        "Precalculus": {
          "n": 56,
          "correct": 5,
          "accuracy": 0.08928571428571429
        }
      },
      "accuracy_by_level": {
        "1": {
          "n": 43,
          "correct": 8,
          "accuracy": 0.18604651162790697
        },
        "2": {
          "n": 90,
          "correct": 15,
          "accuracy": 0.16666666666666666
        },
        "3": {
          "n": 105,
          "correct": 22,
          "accuracy": 0.20952380952380953
        },
        "4": {
          "n": 128,
          "correct": 9,
          "accuracy": 0.0703125
        },
        "5": {
          "n": 134,
          "correct": 7,
          "accuracy": 0.05223880597014925
        }
      },
      "raw_trace_count": 504,
      "scored_unique_traces": 500,
      "limitations": [
        "Two paths are imposed by runtime.",
        "Decode work/depth is not measured wall-clock speedup.",
        "Text equality only detects literal duplicate paths, not semantic duplication or valid reasoning.",
        "Unseen custom mask/positions are not applied to vLLM continuation."
      ]
    }
  }
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/student-system.txt](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/manifest.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/student-system.txt](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/rl-adapter-check/manifest.json](../artifacts/work/experiments/unseen-wide5145-20261009/rl-adapter-check/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train": {
    "rows": 8,
    "source": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet",
    "sha256": "230ed1ad91368d48f346a303f6d1fed3d53a99e751ac33db5921116aab5b3684"
  },
  "val": {
    "rows": 2,
    "source": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet",
    "sha256": "1ad3d7d98a933402e425ddf1f40c5632fc2615cadd1dc644cc2d389ef21df3ff"
  },
  "system_sha256": "49efaf2415b43fc6acc8cc4069858aefccebc5a6011d88eb83291d2796d186ca",
  "max_prompt_tokens": 2000,
  "disjoint_validation": true
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-code-manifest.json](../artifacts/work/experiments/unseen-wide5145-20261009/rl-code-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "path": "tests/test_counted_unseen.py",
    "sha256": "72902e5ffd28e865c5b0fbe6d87ce7988693dfa24c86f54a62fd632f407cfeb5",
    "added": true
  },
  {
    "path": "tests/legacy_test_parallel_loop.py",
    "sha256": "2e10c2df1198eeeff41db19731c670dffbaf4f222a81e1a1ead1eb9882556a98",
    "added": true
  },
  {
    "path": "verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py",
    "sha256": "d09306dfc3a91fa1e47dfbf2cddd41ceb95b4e668f03c10a090bc1a5648efe08",
    "added": false
  },
  {
    "path": "verl/verl/utils/parallel_structure.py",
    "sha256": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "added": true
  },
  {
    "path": "verl/verl/trainer/config/rl_qwen3_06b.yaml",
    "sha256": "9f3fd8f59ed59c170632daf63ce4e7b4a85ceb01dd2fc0f841529511c47a0791",
    "added": false
  },
  {
    "path": "verl/verl/utils/reward_score/counted_parallel.py",
    "sha256": "fd3f3cfa45949a48c3c35f1f8f522d1a692dfd0ea62e0520af2321117aeaf8dc",
    "added": true
  },
  {
    "path": "verl/verl/workers/actor/rollout_context.py",
    "sha256": "d34654a792e3ca1ff8507857b628e6da86a14ac1245f05e3cb10f7ac2281977e",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py",
    "sha256": "c4fc7465216763cd48fb2d3cba3e6064557bc44620e4f8afa0d0ee8b3e64ca59",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/vllm_rollout_spmd.py",
    "sha256": "0d55c4fa254023f2bbf5df75b387daf24dc8ba712ad90ab54e38c2e9fa059aae",
    "added": false
  },
  {
    "path": "verl/verl/workers/rollout/vllm_rollout/structured_worker.py",
    "sha256": "bc9dc0dc0e4df508a43ca164386f846c7988d0803a1e63bc37658d08f747af14",
    "added": true
  },
  {
    "path": "tests/test_parallel_loop.py",
    "deleted": true,
    "reason": "Preserved as legacy_test_parallel_loop.py"
  },
  {
    "path": "verl/verl/parallel_thinking_generation_v3/repro_trace.py",
    "sha256": "0472368fcd3aeeb9383ff79476d86435843cf03bb586c2cbf767d2384c36c148",
    "added": false,
    "reason": "Post-audit trace budget telemetry"
  }
]
```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-resolved.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-resolved.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
actor_rollout_ref:
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 2
    ppo_micro_batch_size: null
    ppo_micro_batch_size_per_gpu: 1
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
    loss_agg_mode: seq-mean-token-mean
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
    sort_microbatches_by_length: true
    trim_parallel_padding: true
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
    top_p: 1.0
    prompt_length: 1024
    response_length: 96
    dtype: bfloat16
    gpu_memory_utilization: 0.45
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
    'n': 2
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 96
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
      record_policy_calls: true
      min_paths: 2
      max_paths: 8
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: true
    load_format: dummy_dtensor
    layered_summon: false
    structured_unseen: true
  hybrid_engine: true
  model:
    path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: true
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
  experiment_name: counted-unseen-s1
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke/rollouts
  validation_data_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke/validation
  nnodes: 1
  n_gpus_per_node: 1
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke/checkpoints
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 1024
  max_response_length: 96
  train_batch_size: 2
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
  rollout_n: 2
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
    tokenizer_path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
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
  ppo_mini_batch_size: 2
  ppo_micro_batch_size: null
  ppo_micro_batch_size_per_gpu: null
  use_dynamic_bsz: false
  ppo_max_token_len_per_gpu: 32768
  forward_max_token_len_per_gpu: 32768
  ppo_epochs: 1
  shuffle: false
  cliprange_value: 0.5
  loss_agg_mode: seq-mean-token-mean
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
    input_tokenizer: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
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
  path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
  name: compute_score
  reward_kwargs:
    stage: s1
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
  num_cpus: 32
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.28
    policy_loss:
      loss_mode: vanilla
      clip_cov_ratio: 0.0002
      clip_cov_lb: 1.0
      clip_cov_ub: 5.0
      kl_cov_ratio: 0.0002
      ppo_kl_coef: 0.1
    clip_ratio_c: 3.0
    loss_agg_mode: seq-mean-token-mean
    entropy_coeff: 0.001
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
    sort_microbatches_by_length: true
    trim_parallel_padding: true
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
    top_p: 1.0
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.3
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 1408
    max_model_len: null
    max_num_seqs: 4
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
    disable_log_stats: true
    do_sample: true
    'n': 2
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: ${data.max_response_length}
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
      record_policy_calls: true
      min_paths: 2
      max_paths: 8
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: false
    load_format: dummy_dtensor
    layered_summon: false
    structured_unseen: true
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_MODEL_PATH}
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: true
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
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 1024
  max_response_length: 384
  train_batch_size: 8
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
  path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
  name: compute_score
  reward_kwargs:
    stage: s1
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
  num_cpus: 32
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
    - trainer.n_gpus_per_node=8
    - trainer.logger=[console]
    - custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.stage=s1
    - ray_init.num_cpus=32
    - +ray_init.temp_dir=${PROJECT_ROOT}
    - +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
    - +ray_init.object_store_memory=8589934592
    - trainer.n_gpus_per_node=8
    - data.train_batch_size=8
    - actor_rollout_ref.actor.ppo_mini_batch_size=8
    - actor_rollout_ref.rollout.n=2
    - data.max_response_length=384
    - data.max_prompt_length=1024
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - trainer.val_before_train=false
    - actor_rollout_ref.rollout.agent.num_workers=2
    - actor_rollout_ref.rollout.gpu_memory_utilization=0.3
    - actor_rollout_ref.rollout.max_num_seqs=4
    - actor_rollout_ref.rollout.max_num_batched_tokens=1408
    - actor_rollout_ref.rollout.enable_chunked_prefill=false
    - ray_init.num_cpus=32
    - actor_rollout_ref.actor.entropy_coeff=0.001
  job:
    name: main_ppo
    chdir: null
    override_dirname: +custom_reward_function.reward_kwargs.stage=s1,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.entropy_coeff=0.001,actor_rollout_ref.actor.ppo_mini_batch_size=8,actor_rollout_ref.rollout.agent.num_workers=2,actor_rollout_ref.rollout.enable_chunked_prefill=false,actor_rollout_ref.rollout.gpu_memory_utilization=0.3,actor_rollout_ref.rollout.max_num_batched_tokens=1408,actor_rollout_ref.rollout.max_num_seqs=4,actor_rollout_ref.rollout.n=2,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py,data.max_prompt_length=1024,data.max_response_length=384,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet,ray_init.num_cpus=32,ray_init.num_cpus=32,trainer.logger=[console],trainer.n_gpus_per_node=8,trainer.n_gpus_per_node=8,trainer.save_freq=2,trainer.test_freq=2,trainer.total_training_steps=2,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra
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

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v2/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
- trainer.n_gpus_per_node=8
- trainer.logger=[console]
- custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.stage=s1
- ray_init.num_cpus=32
- +ray_init.temp_dir=${PROJECT_ROOT}
- +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
- +ray_init.object_store_memory=8589934592
- trainer.n_gpus_per_node=8
- data.train_batch_size=8
- actor_rollout_ref.actor.ppo_mini_batch_size=8
- actor_rollout_ref.rollout.n=2
- data.max_response_length=384
- data.max_prompt_length=1024
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- trainer.val_before_train=false
- actor_rollout_ref.rollout.agent.num_workers=2
- actor_rollout_ref.rollout.gpu_memory_utilization=0.3
- actor_rollout_ref.rollout.max_num_seqs=4
- actor_rollout_ref.rollout.max_num_batched_tokens=1408
- actor_rollout_ref.rollout.enable_chunked_prefill=false
- ray_init.num_cpus=32
- actor_rollout_ref.actor.entropy_coeff=0.001

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.28
    policy_loss:
      loss_mode: vanilla
      clip_cov_ratio: 0.0002
      clip_cov_lb: 1.0
      clip_cov_ub: 5.0
      kl_cov_ratio: 0.0002
      ppo_kl_coef: 0.1
    clip_ratio_c: 3.0
    loss_agg_mode: seq-mean-token-mean
    entropy_coeff: 0.001
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
    sort_microbatches_by_length: true
    trim_parallel_padding: true
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
    top_p: 1.0
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.3
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 1408
    max_model_len: null
    max_num_seqs: 4
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
    disable_log_stats: true
    do_sample: true
    'n': 2
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: ${data.max_response_length}
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
      record_policy_calls: true
      min_paths: 2
      max_paths: 8
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: false
    load_format: dummy_dtensor
    layered_summon: false
    structured_unseen: true
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_MODEL_PATH}
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: true
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
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 1024
  max_response_length: 384
  train_batch_size: 8
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
  path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
  name: compute_score
  reward_kwargs:
    stage: s1
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
  num_cpus: 32
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
    - trainer.n_gpus_per_node=8
    - trainer.logger=[console]
    - custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.stage=s1
    - ray_init.num_cpus=32
    - +ray_init.temp_dir=${PROJECT_ROOT}
    - +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
    - +ray_init.object_store_memory=8589934592
    - trainer.n_gpus_per_node=8
    - data.train_batch_size=8
    - actor_rollout_ref.actor.ppo_mini_batch_size=8
    - actor_rollout_ref.rollout.n=2
    - data.max_response_length=384
    - data.max_prompt_length=1024
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - trainer.val_before_train=false
    - actor_rollout_ref.rollout.agent.num_workers=2
    - actor_rollout_ref.rollout.gpu_memory_utilization=0.3
    - actor_rollout_ref.rollout.max_num_seqs=4
    - actor_rollout_ref.rollout.max_num_batched_tokens=1408
    - actor_rollout_ref.rollout.enable_chunked_prefill=false
    - ray_init.num_cpus=32
    - actor_rollout_ref.actor.entropy_coeff=0.001
  job:
    name: main_ppo
    chdir: null
    override_dirname: +custom_reward_function.reward_kwargs.stage=s1,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.entropy_coeff=0.001,actor_rollout_ref.actor.ppo_mini_batch_size=8,actor_rollout_ref.rollout.agent.num_workers=2,actor_rollout_ref.rollout.enable_chunked_prefill=false,actor_rollout_ref.rollout.gpu_memory_utilization=0.3,actor_rollout_ref.rollout.max_num_batched_tokens=1408,actor_rollout_ref.rollout.max_num_seqs=4,actor_rollout_ref.rollout.n=2,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py,data.max_prompt_length=1024,data.max_response_length=384,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet,ray_init.num_cpus=32,ray_init.num_cpus=32,trainer.logger=[console],trainer.n_gpus_per_node=8,trainer.n_gpus_per_node=8,trainer.save_freq=2,trainer.test_freq=2,trainer.total_training_steps=2,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra
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

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v3/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
- trainer.n_gpus_per_node=8
- trainer.logger=[console]
- custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.stage=s1
- ray_init.num_cpus=32
- +ray_init.temp_dir=${PROJECT_ROOT}
- +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
- +ray_init.object_store_memory=8589934592
- trainer.n_gpus_per_node=8
- data.train_batch_size=8
- actor_rollout_ref.actor.ppo_mini_batch_size=8
- actor_rollout_ref.rollout.n=2
- data.max_response_length=384
- data.max_prompt_length=1024
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- trainer.val_before_train=false
- actor_rollout_ref.rollout.agent.num_workers=2
- actor_rollout_ref.rollout.gpu_memory_utilization=0.3
- actor_rollout_ref.rollout.max_num_seqs=4
- actor_rollout_ref.rollout.max_num_batched_tokens=1408
- actor_rollout_ref.rollout.enable_chunked_prefill=false
- ray_init.num_cpus=32
- actor_rollout_ref.actor.entropy_coeff=0.001

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    clip_ratio_high: 0.28
    policy_loss:
      loss_mode: vanilla
      clip_cov_ratio: 0.0002
      clip_cov_lb: 1.0
      clip_cov_ub: 5.0
      kl_cov_ratio: 0.0002
      ppo_kl_coef: 0.1
    clip_ratio_c: 3.0
    loss_agg_mode: seq-mean-token-mean
    entropy_coeff: 0.001
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
    sort_microbatches_by_length: true
    trim_parallel_padding: true
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
    top_p: 1.0
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.3
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 1408
    max_model_len: null
    max_num_seqs: 4
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
    disable_log_stats: true
    do_sample: true
    'n': 2
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: ${data.max_response_length}
      add_diverse_prefix: false
      custom_async_server:
        path: null
        name: null
      record_policy_calls: true
      min_paths: 2
      max_paths: 8
    update_weights_bucket_megabytes: 512
    trace:
      backend: null
      token2text: false
    enable_chunked_prefill: false
    load_format: dummy_dtensor
    layered_summon: false
    structured_unseen: true
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_MODEL_PATH}
    custom_chat_template: null
    use_shm: false
    external_lib: null
    override_config:
      _attn_implementation: sdpa
    enable_gradient_checkpointing: true
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
  max_actor_ckpt_to_keep: 3
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 1024
  max_response_length: 384
  train_batch_size: 8
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
  path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
  name: compute_score
  reward_kwargs:
    stage: s1
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
  num_cpus: 32
  timeline_json_file: null
  temp_dir: ${PROJECT_ROOT}
  plasma_directory: ${PROJECT_ROOT}/plasma
  object_store_memory: 8589934592

```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
    - trainer.n_gpus_per_node=8
    - trainer.logger=[console]
    - custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
    - custom_reward_function.name=compute_score
    - +custom_reward_function.reward_kwargs.stage=s1
    - ray_init.num_cpus=32
    - +ray_init.temp_dir=${PROJECT_ROOT}
    - +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
    - +ray_init.object_store_memory=8589934592
    - trainer.n_gpus_per_node=8
    - data.train_batch_size=8
    - actor_rollout_ref.actor.ppo_mini_batch_size=8
    - actor_rollout_ref.rollout.n=2
    - data.max_response_length=384
    - data.max_prompt_length=1024
    - trainer.total_training_steps=2
    - trainer.save_freq=2
    - trainer.test_freq=2
    - trainer.val_before_train=false
    - actor_rollout_ref.rollout.agent.num_workers=2
    - actor_rollout_ref.rollout.gpu_memory_utilization=0.3
    - actor_rollout_ref.rollout.max_num_seqs=4
    - actor_rollout_ref.rollout.max_num_batched_tokens=1408
    - actor_rollout_ref.rollout.enable_chunked_prefill=false
    - ray_init.num_cpus=32
    - actor_rollout_ref.actor.entropy_coeff=0.001
  job:
    name: main_ppo
    chdir: null
    override_dirname: +custom_reward_function.reward_kwargs.stage=s1,+ray_init.object_store_memory=8589934592,+ray_init.plasma_directory=${PROJECT_ROOT}/plasma,+ray_init.temp_dir=${SHARED_ROOT}/larin${TMPDIR}/r1,actor_rollout_ref.actor.entropy_coeff=0.001,actor_rollout_ref.actor.ppo_mini_batch_size=8,actor_rollout_ref.rollout.agent.num_workers=2,actor_rollout_ref.rollout.enable_chunked_prefill=false,actor_rollout_ref.rollout.gpu_memory_utilization=0.3,actor_rollout_ref.rollout.max_num_batched_tokens=1408,actor_rollout_ref.rollout.max_num_seqs=4,actor_rollout_ref.rollout.n=2,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py,data.max_prompt_length=1024,data.max_response_length=384,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet,ray_init.num_cpus=32,ray_init.num_cpus=32,trainer.logger=[console],trainer.n_gpus_per_node=8,trainer.n_gpus_per_node=8,trainer.save_freq=2,trainer.test_freq=2,trainer.total_training_steps=2,trainer.val_before_train=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke/hydra
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

- [work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-data/val.parquet
- trainer.n_gpus_per_node=8
- trainer.logger=[console]
- custom_reward_function.path=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-code/verl/verl/utils/reward_score/counted_parallel.py
- custom_reward_function.name=compute_score
- +custom_reward_function.reward_kwargs.stage=s1
- ray_init.num_cpus=32
- +ray_init.temp_dir=${PROJECT_ROOT}
- +ray_init.plasma_directory=${PROJECT_ROOT}/plasma
- +ray_init.object_store_memory=8589934592
- trainer.n_gpus_per_node=8
- data.train_batch_size=8
- actor_rollout_ref.actor.ppo_mini_batch_size=8
- actor_rollout_ref.rollout.n=2
- data.max_response_length=384
- data.max_prompt_length=1024
- trainer.total_training_steps=2
- trainer.save_freq=2
- trainer.test_freq=2
- trainer.val_before_train=false
- actor_rollout_ref.rollout.agent.num_workers=2
- actor_rollout_ref.rollout.gpu_memory_utilization=0.3
- actor_rollout_ref.rollout.max_num_seqs=4
- actor_rollout_ref.rollout.max_num_batched_tokens=1408
- actor_rollout_ref.rollout.enable_chunked_prefill=false
- ray_init.num_cpus=32
- actor_rollout_ref.actor.entropy_coeff=0.001

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 16384
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: true
  prompt_messages_key: prompt_messages
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: true
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 00_canary
  total_epochs: 1
  total_training_steps: 1
  logger:
  - console
  seed: 1
  save_freq: -1
  test_freq: -1
  nnodes: 1
  n_gpus_per_node: 8
  max_ckpt_to_keep: null
  resume_mode: disable
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/final

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=16384
    - data.train_batch_size=8
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=2
    - data.trim_padding=true
    - model.enable_gradient_checkpointing=true
    - model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
    - use_remove_padding=false
    - ulysses_sequence_parallel_size=1
    - optim.lr=1e-5
    - trainer.total_epochs=1
    - trainer.resume_mode=disable
    - trainer.logger=[console]
    - trainer.seed=1
    - trainer.experiment_name=00_canary
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/final
    - trainer.total_training_steps=1
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=16384,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/checkpoints,trainer.experiment_name=00_canary,trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=1,trainer.total_training_steps=1,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra
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

- [work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=16384
- data.train_batch_size=8
- data.micro_batch_size_per_gpu=1
- data.num_workers=2
- data.trim_padding=true
- model.enable_gradient_checkpointing=true
- model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
- use_remove_padding=false
- ulysses_sequence_parallel_size=1
- optim.lr=1e-5
- trainer.total_epochs=1
- trainer.resume_mode=disable
- trainer.logger=[console]
- trainer.seed=1
- trainer.experiment_name=00_canary
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary/final
- trainer.total_training_steps=1

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 16384
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: true
  prompt_messages_key: prompt_messages
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: true
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 00_canary_v2
  total_epochs: 1
  total_training_steps: 1
  logger:
  - console
  seed: 1
  save_freq: -1
  test_freq: -1
  nnodes: 1
  n_gpus_per_node: 8
  max_ckpt_to_keep: null
  resume_mode: disable
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/final

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=16384
    - data.train_batch_size=8
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=2
    - data.trim_padding=true
    - model.enable_gradient_checkpointing=true
    - model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
    - use_remove_padding=false
    - ulysses_sequence_parallel_size=1
    - optim.lr=1e-5
    - trainer.total_epochs=1
    - trainer.resume_mode=disable
    - trainer.logger=[console]
    - trainer.seed=1
    - trainer.experiment_name=00_canary_v2
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/final
    - trainer.total_training_steps=1
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=16384,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/checkpoints,trainer.experiment_name=00_canary_v2,trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=1,trainer.total_training_steps=1,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra
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

- [work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/canary-val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=16384
- data.train_batch_size=8
- data.micro_batch_size_per_gpu=1
- data.num_workers=2
- data.trim_padding=true
- model.enable_gradient_checkpointing=true
- model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
- use_remove_padding=false
- ulysses_sequence_parallel_size=1
- optim.lr=1e-5
- trainer.total_epochs=1
- trainer.resume_mode=disable
- trainer.logger=[console]
- trainer.seed=1
- trainer.experiment_name=00_canary_v2
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/final
- trainer.total_training_steps=1

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/config.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 16384
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: null
    name: null
  use_shm: false
  num_workers: 2
  parallel_attention: true
  prompt_messages_key: prompt_messages
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
  use_shm: false
  fsdp_config:
    model_dtype: fp32
    wrap_policy:
      min_num_params: 0
    cpu_offload: false
    offload_params: false
  external_lib: null
  enable_gradient_checkpointing: true
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 01_sft
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
  resume_mode: disable
  resume_from_path: null
  checkpoint:
    save_contents:
    - model
    - optimizer
    - extra
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final

```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=16384
    - data.train_batch_size=128
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=2
    - data.trim_padding=true
    - model.enable_gradient_checkpointing=true
    - model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
    - use_remove_padding=false
    - ulysses_sequence_parallel_size=1
    - optim.lr=1e-5
    - trainer.total_epochs=5
    - trainer.resume_mode=disable
    - trainer.logger=[console]
    - trainer.seed=1
    - trainer.experiment_name=01_sft
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=16384,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=128,data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/checkpoints,trainer.experiment_name=01_sft,trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=5,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/sft-code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra
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

- [work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/unseen-wide5145-20261009/runs/01_sft/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=16384
- data.train_batch_size=128
- data.micro_batch_size_per_gpu=1
- data.num_workers=2
- data.trim_padding=true
- model.enable_gradient_checkpointing=true
- model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base
- use_remove_padding=false
- ulysses_sequence_parallel_size=1
- optim.lr=1e-5
- trainer.total_epochs=5
- trainer.resume_mode=disable
- trainer.logger=[console]
- trainer.seed=1
- trainer.experiment_name=01_sft
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final

```

</details>

## Метрики и полнота результатов

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/row-coverage.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/row-coverage.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
"5145 records; see original artifact"
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/split-summary.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/split-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "new/train": {
    "rows": 2700,
    "affected_rows": 602,
    "unresolved_no_witness": 2098,
    "unsupported_condition_rows": 2289
  },
  "new/val": {
    "rows": 300,
    "affected_rows": 65,
    "unresolved_no_witness": 235,
    "unsupported_condition_rows": 271
  },
  "old/accepted": {
    "rows": 2145,
    "affected_rows": 332,
    "unresolved_no_witness": 1813,
    "unsupported_condition_rows": 1687
  }
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/summary.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/local-context-validator/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "self_tests_passed": 9,
  "by_source": {
    "new": {
      "rows": 3000,
      "rows_with_explicit_total_convention": 3000,
      "supported_constraints": 54532,
      "unsupported_constraints": 18995,
      "rows_with_any_supported_constraint": 2997,
      "rows_with_unsupported_constraints": 2560,
      "rows_with_bounded_quantities": 2986,
      "rows_with_duplicate_definition_skip": 3,
      "rows_with_negative_witness": 667,
      "negative_witnesses": 973,
      "rows_without_detected_witness_unresolved": 2333,
      "rows_all_candidate_surface_constraints_supported": 440
    },
    "old": {
      "rows": 2145,
      "rows_with_explicit_total_convention": 0,
      "supported_constraints": 36204,
      "unsupported_constraints": 10851,
      "rows_with_any_supported_constraint": 2139,
      "rows_with_unsupported_constraints": 1687,
      "rows_with_bounded_quantities": 2127,
      "rows_with_duplicate_definition_skip": 5,
      "rows_with_negative_witness": 332,
      "negative_witnesses": 510,
      "rows_without_detected_witness_unresolved": 1813,
      "rows_all_candidate_surface_constraints_supported": 458
    }
  },
  "input_sha256": {
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/train.jsonl": "7379ecfc7053771313df1bc63c6324a3f3f8ee72bdfc818015bdc35ae600b24a",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/val.jsonl": "d5a868ef8fc42a50f21a7e9cb657da1a894b882ddeabb256b6f1eeb6112a23c5",
    "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl": "c13c51a87d7189b659795d21a98ada9db5063c44a2135434aa454b3428b28612"
  },
  "limitations": [
    "Affected-row counts divided by corpus size are lower bounds on the fraction with a proved witness under ordinary ordered arithmetic and nonnegative quantity semantics; they are not the full inconsistency prevalence.",
    "Unsupported sentences/quantities are unresolved, never classified clean.",
    "Totals use safe lower bounds from available positive components, never complete-category or zero assumptions.",
    "Only source problem conditions are read; target answers and teacher solutions are excluded."
  ],
  "arithmetic_interpretation": "ordinary ordered arithmetic",
  "nonnegative_domain_assumed": true,
  "official_generator_commit": "caa5388043bd5d34aa6f03738c2b9aa3764fa284",
  "modular_generation_caveat": "Official generator optionally applies modulo after subtraction and its CLI defaults to mod=23. This validator does not assume an unmentioned modulus in the SFT problem text and does not attribute contradictions to teacher arithmetic."
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/random-review/report.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/random-review/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "selection": {
    "selection": "random.Random(seed).sample(sorted(rows,key=id),15) for old then new; interleave old/new in draw order; sampling without replacement, independent of heuristic flags",
    "seed": 20261009,
    "n": 30,
    "counts": {
      "old": 15,
      "new": 15
    },
    "blind_to_existing_heuristic_flags": true,
    "scope": [
      "Read full problem and solution for every selected row",
      "Judge useful substantive computed contributions and whether each is consumed later",
      "Separate given/alias-only paths from substantive derivations",
      "Flag artificial plus-zero or equivalent padding",
      "Check plan ownership, summary numerical fidelity and final arithmetic in shown target chain"
    ],
    "non_goals": [
      "No guarantee of full global-context consistency",
      "No proof of causal contribution to MATH-500 score"
    ],
    "definitions": {
      "given_or_alias_only": "A standalone path only copies a given/shared value or propagates equalities; no substantive calculation beyond that alias",
      "unused_output": "A returned output is not consumed by later target calculations or an explicitly planned verification comparison; partner recomputation does not itself consume it",
      "padding_operation": "Artificial neutral arithmetic, e.g. a stated given rewritten as x+0, used to present alias/given work as computation",
      "useful_verification": "Explicitly assigned independent calculation of a meaningful quantity, compared in summary",
      "clear_scheduling_issue": "At least one confirmed given/alias-only path, unused/irrelevant output, artificial neutral-operation padding, or materially unfaithful summary"
    },
    "input_sha256": {
      "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/train.jsonl": "0821bfb7d2ea468594f51e88e95c29441f050137f116fb5ffa5a09f2e9628aad",
      "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/data/val.jsonl": "994599658e42beda549725cfbdadce8f0ec1becf0fff55796fc7b8521c3103ad"
    },
    "ids": [
      "old:gsm_infinite/2686",
      "new:gsm_infinite_hard_0/ops_22-00000-of-00001/1990",
      "old:gsm_infinite/4978",
      "new:gsm_infinite_hard_0/ops_23-00000-of-00001/1991",
      "old:gsm_infinite/2148",
      "new:gsm_infinite_hard_0/ops_27-00000-of-00001/446",
      "old:gsm_infinite/3838",
      "new:gsm_infinite/1512",
      "old:gsm_infinite/1684",
      "new:gsm_infinite_hard_0/ops_24-00000-of-00001/1401",
      "old:gsm_infinite/2615",
      "new:gsm_infinite_hard_0/ops_23-00000-of-00001/18",
      "old:gsm_infinite/4976",
      "new:gsm_infinite_hard_0/ops_22-00000-of-00001/3019",
      "old:gsm_infinite/2959",
      "new:gsm_infinite/4367",
      "old:gsm_infinite/1775",
      "new:gsm_infinite_hard_0/ops_23-00000-of-00001/1040",
      "old:gsm_infinite/4984",
      "new:gsm_infinite_hard_0/ops_22-00000-of-00001/4450",
      "old:gsm_infinite/3235",
      "new:gsm_infinite/4193",
      "old:gsm_infinite/3255",
      "new:gsm_infinite_hard_0/ops_25-00000-of-00001/689",
      "old:gsm_infinite/3906",
      "new:gsm_infinite_hard_0/ops_24-00000-of-00001/1328",
      "old:gsm_infinite/3578",
      "new:gsm_infinite_hard_0/ops_21-00000-of-00001/1003",
      "old:gsm_infinite/4334",
      "new:gsm_infinite_hard_0/ops_27-00000-of-00001/910"
    ]
  },
  "summary": {
    "old": {
      "reviewed_rows": 15,
      "forks": 32,
      "paths": 89,
      "clear_scheduling_issue_rows": 14,
      "given_alias_rows": 14,
      "given_alias_paths": 34,
      "unused_output_rows": 0,
      "padding_rows": 0,
      "unfaithful_summary_rows": 0,
      "same_chain_verification_low_value_rows": 0,
      "nested_prefix_overlap_rows": 0,
      "incidental_negative_witness_rows": 1,
      "widths": [
        2,
        3,
        4,
        5
      ]
    },
    "new": {
      "reviewed_rows": 15,
      "forks": 17,
      "paths": 58,
      "clear_scheduling_issue_rows": 0,
      "given_alias_rows": 0,
      "given_alias_paths": 0,
      "unused_output_rows": 0,
      "padding_rows": 0,
      "unfaithful_summary_rows": 0,
      "same_chain_verification_low_value_rows": 3,
      "nested_prefix_overlap_rows": 1,
      "incidental_negative_witness_rows": 4,
      "widths": [
        2,
        3,
        4
      ]
    }
  },
  "witness_ids": [
    "new:gsm_infinite/4367",
    "new:gsm_infinite/4193",
    "new:gsm_infinite_hard_0/ops_25-00000-of-00001/689",
    "new:gsm_infinite_hard_0/ops_27-00000-of-00001/910"
  ],
  "all_selected_source_rows_match_inputs": true,
  "input_hashes_unchanged": true,
  "sampling_reproduction_verified": true,
  "limitations": [
    "15 per stratum is small; these are sample counts, not exact dataset rates.",
    "Blind means no existing heuristic flags were consulted during selection/manual judgment; source origin and full responses were visible.",
    "Same reviewer, separate re-reading of source arithmetic; no claim of second human reviewer.",
    "No exhaustive global consistency validator was run; incidental negative counts are separately reported, absence of a witness proves nothing.",
    "No inference about causal effect on completed SFT/eval.",
    "Planned independent verification counts as consumption when explicitly compared; identical computation can still have low extra value."
  ]
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/report.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "format_and_data_summary": {
    "rows": 5145,
    "by_source": {
      "old": {
        "think_exact_pair_and_opening": 2145,
        "single_final_answer_line": 2145,
        "boxed_final_answer": 2145,
        "plain_final_answer": 0,
        "final_after_think_and_last": 2145,
        "all_control_blocks_inside_think": 2145,
        "valid_plan_assignment_counts_and_ids": 2145,
        "valid_control_headers_and_ordering": 2145,
        "has_postthink_concluding_solution": 0,
        "explicit_zero_convention_prefix": 0,
        "rows": 2145,
        "forks": 4486,
        "paths": 11970,
        "sequential": 76,
        "gold_answer_match": 2145,
        "grade_error": 0,
        "width:2": 2647,
        "flag:path_no_detected_numeric_operation": 3852,
        "flag:numeric_result_or_given_in_plan": 4491,
        "flagged_rows": 1956,
        "width:3": 1087,
        "width:5": 164,
        "flag:short_path_lt100chars": 6701,
        "width:4": 494,
        "width:6": 54,
        "width:7": 25,
        "width:8": 15,
        "loss_tokens": 2004540,
        "control_tag_eos_tokens": 48319,
        "count_id_newline_tokens": 32912,
        "first_think_equal_example_mean_loss_fraction": 0.001249881896000257,
        "protocol_tag_header_loss_fraction": 0.04052351162860307
      },
      "new": {
        "think_exact_pair_and_opening": 3000,
        "single_final_answer_line": 3000,
        "boxed_final_answer": 3000,
        "plain_final_answer": 0,
        "final_after_think_and_last": 3000,
        "all_control_blocks_inside_think": 3000,
        "valid_plan_assignment_counts_and_ids": 3000,
        "valid_control_headers_and_ordering": 3000,
        "has_postthink_concluding_solution": 3000,
        "explicit_zero_convention_prefix": 3000,
        "rows": 3000,
        "forks": 3486,
        "paths": 11475,
        "sequential": 7,
        "gold_answer_match": 3000,
        "grade_error": 0,
        "width:4": 1493,
        "flagged_rows": 474,
        "width:3": 943,
        "flag:numeric_result_or_given_in_plan": 694,
        "width:2": 865,
        "width:5": 166,
        "flag:short_path_lt100chars": 328,
        "width:6": 19,
        "loss_tokens": 2438433,
        "control_tag_eos_tokens": 45894,
        "count_id_newline_tokens": 29922,
        "first_think_equal_example_mean_loss_fraction": 0.0013064254919603626,
        "protocol_tag_header_loss_fraction": 0.03109209890122058
      }
    },
    "source_acceptance_checks": {
      "('old', 'judge_accept_true')": 2145,
      "('old', 'judge_no_issues')": 2145,
      "('old', 'verification_mathverify')": 2145,
      "('new', 'judge_accept_true')": 3000,
      "('new', 'judge_no_issues')": 3000,
      "('new', 'verification_mathverify')": 3000
    },
    "source_templates": {
      "('old', 'crazy_zootopia')": 1036,
      "('old', 'teachers_in_school')": 522,
      "('old', 'movie_festival_awards')": 587,
      "('new', 'crazy_zootopia')": 1512,
      "('new', 'movie_festival_awards')": 732,
      "('new', 'teachers_in_school')": 756
    },
    "normalized_problem_duplicate_groups": [],
    "numeric_abstract_problem_duplicate_groups": [],
    "normalized_response_duplicate_groups": [],
    "similar_path_pairs_ge_0_80": 5061,
    "exact_path_pairs": 1,
    "flag_counts": {
      "path_no_detected_numeric_operation": 3852,
      "numeric_result_or_given_in_plan": 5185,
      "short_path_lt100chars": 7029
    },
    "manual_samples": 32,
    "limitations": [
      "Automatic arithmetic/plan/similarity flags are heuristics, not semantic errors.",
      "Gold-answer equivalence does not prove reasoning validity.",
      "Source semantic judge was the same teacher model.",
      "Manual selection is stratified/purposeful, not a random error-rate estimate."
    ]
  },
  "quality_heuristics_with_denominators": {
    "old": {
      "no_numeric_operation_path_flags": {
        "count": 3852,
        "denominator_paths": 11970
      },
      "short_path_lt100char_flags": {
        "count": 6701,
        "denominator_paths": 11970
      },
      "plan_numeric_rhs_flags": {
        "count": 4491,
        "denominator_plan_assignments": 11970
      },
      "any_heuristic_flag_rows": {
        "count": 1956,
        "denominator_rows": 2145
      },
      "note": "Flags are review candidates, not proven errors; given constants in plans can be legitimate and short paths can be useful."
    },
    "new": {
      "no_numeric_operation_path_flags": {
        "count": 0,
        "denominator_paths": 11475
      },
      "short_path_lt100char_flags": {
        "count": 328,
        "denominator_paths": 11475
      },
      "plan_numeric_rhs_flags": {
        "count": 694,
        "denominator_plan_assignments": 11475
      },
      "any_heuristic_flag_rows": {
        "count": 474,
        "denominator_rows": 3000
      },
      "note": "Flags are review candidates, not proven errors; given constants in plans can be legitimate and short paths can be useful. In particular, zero no-numeric-operation flags is largely guaranteed by the new deterministic source validator; 4+0 demonstrates that passing the regex does not prove substantive work."
    }
  },
  "manual_sample": {
    "old": {
      "n": 22,
      "rows_with_findings": 19,
      "issue_categories": {
        "unstated_zero_category_convention": 9,
        "given_only_path": 1,
        "given_only_or_alias_only_all_paths": 1,
        "given_only_alias_paths": 16,
        "negative_irrelevant_average": 4,
        "unused_branch_output": 1,
        "negative_irrelevant_count": 2,
        "unused_branch_outputs": 5,
        "excessive_fragmentation": 4,
        "irrelevant_branch_work": 3
      },
      "interpretation": "Purposeful stratified sample includes shortest examples and highest heuristic/similarity flags; not a population error-rate estimate."
    },
    "new": {
      "n": 10,
      "rows_with_findings": 4,
      "issue_categories": {
        "negative_irrelevant_count": 1,
        "low_value_verification_or_alias_parallelism": 1,
        "given_only_disguised_as_plus_zero": 1,
        "negative_irrelevant_average": 1
      },
      "interpretation": "Purposeful stratified sample includes shortest examples and highest heuristic/similarity flags; not a population error-rate estimate."
    }
  },
  "high_confidence_manifest_entries": 35,
  "high_confidence_manifest_unique_rows": 23,
  "acceptance_pipeline": {
    "old": {
      "selected_accepted_journal_rows": 2145,
      "all_final_grades_correct": true,
      "all_structure_checks_valid": true,
      "all_required_judge_flags_true": true,
      "required_judge_fields": [
        "mathematically_correct",
        "complete",
        "independent_paths",
        "plan_faithful",
        "summary_faithful",
        "useful_parallelism",
        "scheduling_faithful"
      ],
      "selected_teacher_prompt_hashes": {
        "2c1393ca44d63efc3d23ac9d9465a4dc3d4530b66cebf3f438b3c43afb6f3bec": 2145
      },
      "current_approved_teacher_prompt": "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/teacher-prompt-v5.txt",
      "current_teacher_prompt_sha256": "2c1393ca44d63efc3d23ac9d9465a4dc3d4530b66cebf3f438b3c43afb6f3bec",
      "journal_decisions_all_rows": {
        "accepted": 2145,
        "rejected": 273
      },
      "journal_rejection_categories_all_rows": {
        "structure": 200,
        "answer_verification": 6,
        "semantic_judge_reject": 46,
        "judge_not_finished": 21
      },
      "deterministic_global_nonnegative_solver": false,
      "judge_model": "deepseek-v4.1-flash, same as teacher",
      "judge_prompt": "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/judge-prompt.txt"
    },
    "new": {
      "selected_accepted_journal_rows": 3000,
      "all_final_grades_correct": true,
      "all_structure_checks_valid": true,
      "all_required_judge_flags_true": true,
      "required_judge_fields": [
        "mathematically_correct",
        "complete",
        "independent_paths",
        "plan_faithful",
        "summary_faithful",
        "useful_parallelism",
        "scheduling_faithful",
        "all_branch_outputs_used",
        "no_given_only_paths",
        "sufficient_explanation",
        "verification_paths_valid"
      ],
      "selected_teacher_prompt_hashes": {
        "8136ffd0d7f2a5e15cc942beb71c249b64ca381047f00cab7c1496f115c0f403": 34,
        "e9455d5993162286be9ee24db5070268abd0b73c8e88da5fe37e1d13c7ac1ba5": 6,
        "3f1e91b62b5f12e6a37d7a8d14abcda0e24ceb0d3ca7e605ef7c69540670d8d4": 2960
      },
      "current_approved_teacher_prompt": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit.txt",
      "current_teacher_prompt_sha256": "3f1e91b62b5f12e6a37d7a8d14abcda0e24ceb0d3ca7e605ef7c69540670d8d4",
      "journal_decisions_all_rows": {
        "rejected": 551,
        "accepted": 3000
      },
      "journal_rejection_categories_all_rows": {
        "AssertionError('structural_or_answer_check')": 3,
        "deterministic_path_audit": 10,
        "semantic_judge_reject": 236,
        "AssertionError('judge_not_finished')": 1,
        "structure": 248,
        "judge_not_finished": 36,
        "answer_verification": 17
      },
      "deterministic_global_nonnegative_solver": false,
      "judge_model": "deepseek-v4.1-flash, same as teacher",
      "judge_prompt": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/judge-prompt.txt",
      "prompt_provenance_note": "2960 rows use current production prompt; 34+6 accepted pilot/review rows retain two earlier recorded prompt hashes. All3000 have checked journal acceptances and required semantic flags."
    }
  },
  "integrity_checks": {
    "negative_witnesses": 8,
    "zero_convention_counterexamples_checked": 2,
    "all_high_confidence_issues_accepted_by_source_judge": true,
    "original_source_hashes_unchanged": true,
    "frozen_sft_code_hashes_unchanged": true,
    "completed_sft_sha256_unchanged": true,
    "new_initializer_created": false,
    "training_or_gpu_run_started": false
  },
  "recommendation": [
    "Do not alter the completed model/data. For the next controlled baseline, exclude the old2145 and train afresh on a context-validated new3000; compare against full5145. This tests mixing policy rather than assuming the old data caused all observed model errors.",
    "Before regenerating teacher reasoning, independently validate SOURCE equations, nonnegative counts/averages and explicit missing-category conventions. Rewording a trace cannot repair an inconsistent problem.",
    "Use the issue manifest as concrete review/regeneration candidates; do not drop all heuristic-flagged rows automatically.",
    "New3000 is a better decomposition foundation but not clean: two manually checked new source contexts require negative values, and two examples still show low-value or plus-zero work.",
    "Excluding old2145 removes all observed width7/8 coverage: create useful, nondecorative width7/8 examples and held-out coverage if these widths matter.",
    "Treat MATH-500 transfer separately: all5145 examples come from three GSM-Infinite templates, not geometry/algebra/proof diversity.",
    "Keep explicit first-think injection separate from dataset quality: it handles one boundary, not invalid contexts or decorative scheduling."
  ]
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/row-statistics.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/row-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
"5145 records; see original artifact"
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-quality-audit/summary.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-quality-audit/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rows": 5145,
  "by_source": {
    "old": {
      "think_exact_pair_and_opening": 2145,
      "single_final_answer_line": 2145,
      "boxed_final_answer": 2145,
      "plain_final_answer": 0,
      "final_after_think_and_last": 2145,
      "all_control_blocks_inside_think": 2145,
      "valid_plan_assignment_counts_and_ids": 2145,
      "valid_control_headers_and_ordering": 2145,
      "has_postthink_concluding_solution": 0,
      "explicit_zero_convention_prefix": 0,
      "rows": 2145,
      "forks": 4486,
      "paths": 11970,
      "sequential": 76,
      "gold_answer_match": 2145,
      "grade_error": 0,
      "width:2": 2647,
      "flag:path_no_detected_numeric_operation": 3852,
      "flag:numeric_result_or_given_in_plan": 4491,
      "flagged_rows": 1956,
      "width:3": 1087,
      "width:5": 164,
      "flag:short_path_lt100chars": 6701,
      "width:4": 494,
      "width:6": 54,
      "width:7": 25,
      "width:8": 15,
      "loss_tokens": 2004540,
      "control_tag_eos_tokens": 48319,
      "count_id_newline_tokens": 32912,
      "first_think_equal_example_mean_loss_fraction": 0.001249881896000257,
      "protocol_tag_header_loss_fraction": 0.04052351162860307
    },
    "new": {
      "think_exact_pair_and_opening": 3000,
      "single_final_answer_line": 3000,
      "boxed_final_answer": 3000,
      "plain_final_answer": 0,
      "final_after_think_and_last": 3000,
      "all_control_blocks_inside_think": 3000,
      "valid_plan_assignment_counts_and_ids": 3000,
      "valid_control_headers_and_ordering": 3000,
      "has_postthink_concluding_solution": 3000,
      "explicit_zero_convention_prefix": 3000,
      "rows": 3000,
      "forks": 3486,
      "paths": 11475,
      "sequential": 7,
      "gold_answer_match": 3000,
      "grade_error": 0,
      "width:4": 1493,
      "flagged_rows": 474,
      "width:3": 943,
      "flag:numeric_result_or_given_in_plan": 694,
      "width:2": 865,
      "width:5": 166,
      "flag:short_path_lt100chars": 328,
      "width:6": 19,
      "loss_tokens": 2438433,
      "control_tag_eos_tokens": 45894,
      "count_id_newline_tokens": 29922,
      "first_think_equal_example_mean_loss_fraction": 0.0013064254919603626,
      "protocol_tag_header_loss_fraction": 0.03109209890122058
    }
  },
  "source_acceptance_checks": {
    "('old', 'judge_accept_true')": 2145,
    "('old', 'judge_no_issues')": 2145,
    "('old', 'verification_mathverify')": 2145,
    "('new', 'judge_accept_true')": 3000,
    "('new', 'judge_no_issues')": 3000,
    "('new', 'verification_mathverify')": 3000
  },
  "source_templates": {
    "('old', 'crazy_zootopia')": 1036,
    "('old', 'teachers_in_school')": 522,
    "('old', 'movie_festival_awards')": 587,
    "('new', 'crazy_zootopia')": 1512,
    "('new', 'movie_festival_awards')": 732,
    "('new', 'teachers_in_school')": 756
  },
  "normalized_problem_duplicate_groups": [],
  "numeric_abstract_problem_duplicate_groups": [],
  "normalized_response_duplicate_groups": [],
  "similar_path_pairs_ge_0_80": 5061,
  "exact_path_pairs": 1,
  "flag_counts": {
    "path_no_detected_numeric_operation": 3852,
    "numeric_result_or_given_in_plan": 5185,
    "short_path_lt100chars": 7029
  },
  "manual_samples": 32,
  "limitations": [
    "Automatic arithmetic/plan/similarity flags are heuristics, not semantic errors.",
    "Gold-answer equivalence does not prove reasoning validity.",
    "Source semantic judge was the same teacher model.",
    "Manual selection is stratified/purposeful, not a random error-rate estimate."
  ]
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/data-report.json](../artifacts/work/experiments/unseen-wide5145-20261009/data-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rows": 5145,
  "train": 4630,
  "val": 515,
  "widths": {
    "2": 3512,
    "3": 2030,
    "5": 330,
    "4": 1987,
    "6": 73,
    "7": 25,
    "8": 15
  },
  "max_tokens": 4407,
  "quantiles": {
    "0.5": 2191.0,
    "0.9": 2883.2000000000007,
    "0.99": 3872.13
  },
  "base": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base",
  "base_source": {
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
  },
  "source_sha256": {
    "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl": "c13c51a87d7189b659795d21a98ada9db5063c44a2135434aa454b3428b28612",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/train.jsonl": "7379ecfc7053771313df1bc63c6324a3f3f8ee72bdfc818015bdc35ae600b24a",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/val.jsonl": "d5a868ef8fc42a50f21a7e9cb657da1a894b882ddeabb256b6f1eeb6112a23c5"
  },
  "split_policy": "Keep new train/val; deterministic problem hash old 1930/215; no overlap",
  "transformations": "Common counted-fork system prompt; old reasoning wrapped in think, final outside; remove external sibling whitespace only"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/REPORT.md](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/analysis-status.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/analysis-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "superseded",
  "reason": "User requested automatic first think prefix; full MATH-500 restarted under a separate protocol.",
  "completed": 343,
  "total": 500,
  "updated_at": "2026-10-09T21:10:45.451381+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/cpu-results.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/cpu-results.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "test": "test_counted_unseen",
    "tests": 7,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_rollout_context",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_actor_padding",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_rl_microbatch_loss",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  }
]
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/long-context-results.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/long-context-results.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "gpu": 0,
  "gpu0_initial_free_mib": 81153,
  "model": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final",
  "actor_replay": {
    "response_tokens": 8190,
    "response_budget": 8192,
    "padding_tokens": 2,
    "prompt_tokens": 19,
    "assembled_padded_tokens": 10192,
    "width": 8,
    "calls": 11,
    "sampled_tokens": 8163,
    "loss": 0.05702853575348854,
    "grad_l2": 2.844059467315674,
    "finite": true,
    "seconds": 4.266103267669678,
    "peak_allocated_gib": 8.42767333984375,
    "peak_reserved_gib": 10.94921875
  },
  "cached_backend_sampled_label_replay": {
    "physical_prompt_tokens": 8067,
    "sampled_tokens": 8,
    "mean_logp_error": 0.003679647110402584,
    "max_logp_error": 0.02111637592315674,
    "threshold": 0.15
  },
  "seconds": 36.631418228149414,
  "scope": "One width8 padded long-context replay/backward and eight-token backend probe; no optimizer or checkpoint writes; not distributed FSDP validation."
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/telemetry-test-results.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/telemetry-test-results.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/think-prefix-test-results.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-rl/think-prefix-test-results.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  {
    "test": "test_counted_unseen",
    "tests": 9,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_rollout_context",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_actor_padding",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  },
  {
    "test": "test_rl_microbatch_loss",
    "tests": 1,
    "errors": 0,
    "failures": 0,
    "successful": true
  }
]
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-sft-findings.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/audit-sft-findings.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "verdict": "No blocking implementation defect found in completed frozen SFT; counted Unseen sibling isolation, positions and shifted labels are correct for widths 2..8. Quality on MATH-500 is a separate question.",
  "checks": [
    "audit-sft-check.json",
    "audit-sft-provenance.json"
  ],
  "findings": [
    {
      "severity": "coverage limitation",
      "finding": "Width 8 has 15 train forks and 0 validation forks; widths 7/6 have 23/68 train and 2/5 validation forks. Overall validation loss cannot establish widest-width format reliability.",
      "evidence": "audit-sft-check.json corpus.widths_by_split",
      "recommendation": "Report width-specific format/answer metrics in evaluations; for future SFT consider deliberate width-stratified held-out coverage before changing train data."
    },
    {
      "severity": "format inconsistency",
      "finding": "All 2145 old responses close think then immediately provide Final Answer, while the common new system also asks for a short concluding solution with decisive arithmetic and units.",
      "files": [
        {
          "path": "work/experiments/unseen-wide5145-20261009/prepare.py",
          "line": 22
        },
        {
          "path": "exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt",
          "line": 33
        }
      ],
      "evidence": "audit-sft-provenance.json response_after_think_old.true=2145",
      "recommendation": "Document the mixed target style; standardize a future dataset only if concluding-solution format matters."
    },
    {
      "severity": "objective observation",
      "finding": "SFT applies loss to all response tokens, including forced runtime <Path>I headers and merge tags. The <Path> marker for sibling k>1 is a next-token target at prior sibling closing token. This affects metadata-only losses and does not leak prior sibling content into the hidden states used to predict branch content.",
      "files": [
        {
          "path": "work/experiments/unseen-wide5145-20261009/sft-code/verl/utils/dataset/parallel_thinking_sft_dataset.py",
          "line": 327
        },
        {
          "path": "work/experiments/unseen-wide5145-20261009/sft-code/verl/trainer/fsdp_parallel_sft_trainer.py",
          "line": 346
        }
      ],
      "recommendation": "Keep protocol metadata distinct from branch-content diagnostics; forced-token masking can be an explicit future objective choice rather than a repair to the completed SFT."
    }
  ],
  "verified": [
    {
      "item": "Count header and branch positions",
      "file": "work/experiments/unseen-wide5145-20261009/sft-code/verl/utils/parallel_structure.py",
      "lines": [
        33,
        40,
        42
      ],
      "evidence": "all 5145 tokenized records; counts 2..8; IDs 1..N; counts/ID newlines preserved; merge begins after longest branch"
    },
    {
      "item": "Sibling and indirect whitespace isolation",
      "file": "work/experiments/unseen-wide5145-20261009/sft-code/verl/utils/parallel_structure.py",
      "lines": [
        38,
        54
      ],
      "evidence": "four-layer Qwen CPU content perturbation, widths 2..8, three repeated forks, gaps on/off; sibling hidden difference zero and merged suffix changes"
    },
    {
      "item": "Causal shift, EOS, trimming and collation",
      "file": "work/experiments/unseen-wide5145-20261009/sft-code/verl/utils/dataset/parallel_thinking_sft_dataset.py",
      "lines": [
        283,
        329,
        330
      ],
      "evidence": "first response label trained at last prompt query, EOS target trained at final content query; trimmed length retains EOS; production deferred dataset/default collation exercised"
    },
    {
      "item": "Think template agreement",
      "file": "work/experiments/unseen-wide5145-20261009/prepare.py",
      "lines": [
        38,
        39
      ],
      "evidence": "all 5145 responses start <think>; default SFT/eval generation prefix has no <think>; eval system exactly equals SFT system"
    },
    {
      "item": "Token init and checkpoint provenance",
      "file": "exps/sft-unseen-three-datasets-20261008/code/training_scripts/prepare_qwen3_parallel.py",
      "lines": [
        23,
        28
      ],
      "evidence": "six actual embedding rows finite, std 0.0191..0.0209, changed during SFT; final SHA256 matches step180 and final-audit; frozen 585 Python hashes and three source hashes unchanged; source-to-final data reconstruction exact 5145"
    },
    {
      "item": "Completed training",
      "file": "work/experiments/unseen-wide5145-20261009/runs/01_sft/sft.log",
      "evidence": "exit 0, 180 finite logged steps, no nonfinite-grad skipped updates, epoch validation losses 0.500874/0.400999/0.374001/0.364715/0.363822; no optimizer/scheduler state saved"
    }
  ],
  "additional_first_token_diagnostic": {
    "files": [
      "audit-sft-first-token.py",
      "audit-sft-first-token.json",
      "audit-sft-first-token.log",
      "audit-sft-first-token-think-embeddings.json"
    ],
    "method": "24 HF BF16 SDPA next-token forwards, 8 evenly spaced train/val/MATH-500 examples, exact system/template, temperature-1 raw softmax, no generation or sampling",
    "conclusion": "Weak opening-vs-closing think discrimination exists on in-domain train and validation prefixes; MATH shows an additional domain effect. Base original special tokens including think and ChatML have identical embeddings; final think pair remains nearly parallel. This is a model initialization/training-quality limitation, not an Unseen mask or template mismatch.",
    "evidence": {
      "base_151644_to_151668_exact_equal": true,
      "final_think_close_cosine": 0.9993906617164612,
      "train_p_think_mean": 0.05562243750318885,
      "train_p_close_mean": 0.04400807060301304,
      "val_p_think_mean": 0.05708217108622193,
      "val_p_close_mean": 0.045139548368752,
      "math_p_think_mean": 0.03268137068311294,
      "math_p_close_mean": 0.025545957482412174,
      "argmax_think_counts": {
        "train": 8,
        "val": 8,
        "math": 5
      }
    },
    "recommendation": "For a future explicitly authorized training experiment, test distinct initialization of unused Base thinking special tokens and/or explicit weighting of format-critical targets; preserve this completed checkpoint as the audited baseline. The small 8-example groups are diagnostic, not an accuracy estimate."
  }
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/controller-status-at-stop.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/controller-status-at-stop.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "error": "KeyboardInterrupt('Signal 15')",
  "updated_at": "2026-10-09T21:09:20.150885+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/previous-comparison.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/previous-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "gsm_infinite_ep5": {
    "n": 500,
    "historical_correct": 84,
    "historical_pass_at_1": 0.168,
    "final_answer_only_correct": 84,
    "final_answer_only_pass_at_1": 0.168,
    "old_summary_correct": 84,
    "errors": []
  },
  "sft_messages_ep5": {
    "n": 500,
    "historical_correct": 79,
    "historical_pass_at_1": 0.158,
    "final_answer_only_correct": 79,
    "final_answer_only_pass_at_1": 0.158,
    "old_summary_correct": 79,
    "errors": []
  },
  "mixed_ep1": {
    "n": 500,
    "historical_correct": 61,
    "historical_pass_at_1": 0.122,
    "final_answer_only_correct": 61,
    "final_answer_only_pass_at_1": 0.122,
    "old_summary_correct": 61,
    "errors": []
  }
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/status.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "superseded",
  "reason": "User requested automatic first think prefix; full MATH-500 restarted under a separate protocol.",
  "completed": 343,
  "total": 500,
  "updated_at": "2026-10-09T21:10:45.451381+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/summary.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "partial",
  "updated_at": "2026-10-09T21:10:00.453016+00:00",
  "questions": 343,
  "total_questions": 500,
  "samples_per_question": 1,
  "correct": 40,
  "pass_at_1": 0.11661807580174927,
  "ci95": [
    0.08681994674120178,
    0.1549085337748413
  ],
  "invalid_answers": 127,
  "extraction": {
    "boxed": 216,
    "missing_final_answer": 5,
    "unfinished_thinking": 122
  },
  "scorer_errors": [],
  "final_answer_only_diagnostic": {
    "correct": 64,
    "pass_at_1": 0.18658892128279883,
    "ci95": [
      0.14891375134876486,
      0.23120648937727797
    ],
    "invalid_answers": 9,
    "description": "Remove think tags before reference-blind extraction. Diagnostic, not primary previous-comparison metric."
  },
  "by_subject": {
    "Algebra": {
      "n": 80,
      "correct": 21,
      "pass_at_1": 0.2625,
      "ci95": [
        0.1785740148850936,
        0.36818959664428175
      ],
      "final_answer_only_correct": 31,
      "final_answer_only_pass_at_1": 0.3875
    },
    "Counting & Probability": {
      "n": 25,
      "correct": 3,
      "pass_at_1": 0.12,
      "ci95": [
        0.04166817150440358,
        0.2995579392092732
      ],
      "final_answer_only_correct": 3,
      "final_answer_only_pass_at_1": 0.12
    },
    "Geometry": {
      "n": 32,
      "correct": 3,
      "pass_at_1": 0.09375,
      "ci95": [
        0.032401551298366194,
        0.24218154728387864
      ],
      "final_answer_only_correct": 5,
      "final_answer_only_pass_at_1": 0.15625
    },
    "Intermediate Algebra": {
      "n": 71,
      "correct": 3,
      "pass_at_1": 0.04225352112676056,
      "ci95": [
        0.014473260620475319,
        0.11702416040484681
      ],
      "final_answer_only_correct": 3,
      "final_answer_only_pass_at_1": 0.04225352112676056
    },
    "Number Theory": {
      "n": 39,
      "correct": 2,
      "pass_at_1": 0.05128205128205128,
      "ci95": [
        0.014177955415274113,
        0.16885640047613612
      ],
      "final_answer_only_correct": 4,
      "final_answer_only_pass_at_1": 0.10256410256410256
    },
    "Prealgebra": {
      "n": 52,
      "correct": 5,
      "pass_at_1": 0.09615384615384616,
      "ci95": [
        0.04177435105257249,
        0.20609630120131633
      ],
      "final_answer_only_correct": 12,
      "final_answer_only_pass_at_1": 0.23076923076923078
    },
    "Precalculus": {
      "n": 44,
      "correct": 3,
      "pass_at_1": 0.06818181818181818,
      "ci95": [
        0.023459395907381622,
        0.18225044370221527
      ],
      "final_answer_only_correct": 6,
      "final_answer_only_pass_at_1": 0.13636363636363635
    }
  },
  "by_level": {
    "1": {
      "n": 30,
      "correct": 8,
      "pass_at_1": 0.26666666666666666,
      "ci95": [
        0.14182663319596317,
        0.4444796169518888
      ],
      "final_answer_only_correct": 14,
      "final_answer_only_pass_at_1": 0.4666666666666667
    },
    "2": {
      "n": 61,
      "correct": 14,
      "pass_at_1": 0.22950819672131148,
      "ci95": [
        0.1419323035287129,
        0.34913405123584
      ],
      "final_answer_only_correct": 15,
      "final_answer_only_pass_at_1": 0.2459016393442623
    },
    "3": {
      "n": 76,
      "correct": 10,
      "pass_at_1": 0.13157894736842105,
      "ci95": [
        0.07306881567918964,
        0.22554119436880626
      ],
      "final_answer_only_correct": 19,
      "final_answer_only_pass_at_1": 0.25
    },
    "4": {
      "n": 86,
      "correct": 6,
      "pass_at_1": 0.06976744186046512,
      "ci95": [
        0.032365414509921336,
        0.14396140641036848
      ],
      "final_answer_only_correct": 8,
      "final_answer_only_pass_at_1": 0.09302325581395349
    },
    "5": {
      "n": 90,
      "correct": 2,
      "pass_at_1": 0.022222222222222223,
      "ci95": [
        0.006115441986325208,
        0.07744526688625372
      ],
      "final_answer_only_correct": 8,
      "final_answer_only_pass_at_1": 0.08888888888888889
    }
  },
  "by_parallel": {
    "False": {
      "n": 92,
      "correct": 14,
      "pass_at_1": 0.15217391304347827,
      "ci95": [
        0.09286540270143614,
        0.23936512897551807
      ],
      "final_answer_only_correct": 22,
      "final_answer_only_pass_at_1": 0.2391304347826087
    },
    "True": {
      "n": 251,
      "correct": 26,
      "pass_at_1": 0.10358565737051793,
      "ci95": [
        0.07167442985961422,
        0.147447918125311
      ],
      "final_answer_only_correct": 42,
      "final_answer_only_pass_at_1": 0.16733067729083664
    }
  },
  "forks": {
    "0": 92,
    "1": 234,
    "2": 13,
    "23": 1,
    "3": 1,
    "4": 1,
    "59": 1
  },
  "widths": {
    "2": 264,
    "3": 34,
    "4": 42,
    "5": 7,
    "6": 2
  },
  "parallel_questions": 251,
  "multi_round_questions": 17,
  "format_invalid_questions": 11,
  "invalid_width_questions": 5,
  "budget_exhausted_questions": 1,
  "response_tokens": {
    "n": 343,
    "sum": 336597,
    "mean": 981.332361516035,
    "median": 519,
    "p90": 1044.0,
    "p95": 1365.4999999999995,
    "max": 30720,
    "min": 83
  },
  "sampled_tokens": {
    "n": 343,
    "sum": 333013,
    "mean": 970.8833819241983,
    "median": 510,
    "p90": 1034.4,
    "p95": 1353.7999999999997,
    "max": 30711,
    "min": 83
  },
  "forced_tokens": {
    "n": 343,
    "sum": 3584,
    "mean": 10.448979591836734,
    "median": 9,
    "p90": 15.0,
    "p95": 18.0,
    "max": 531,
    "min": 0
  },
  "phase_tokens": {
    "main": {
      "n": 692,
      "sum": 180998,
      "mean": 261.5578034682081,
      "median": 129.0,
      "p90": 302.0,
      "p95": 424.749999999999,
      "max": 30277,
      "min": 12
    },
    "width": {
      "n": 354,
      "sum": 708,
      "mean": 2,
      "median": 2.0,
      "p90": 2.0,
      "p95": 2.0,
      "max": 2,
      "min": 2
    },
    "path": {
      "n": 845,
      "sum": 95666,
      "mean": 113.21420118343195,
      "median": 70,
      "p90": 171.0,
      "p95": 233.79999999999995,
      "max": 8192,
      "min": 9
    },
    "summary": {
      "n": 349,
      "sum": 55641,
      "mean": 159.4297994269341,
      "median": 68,
      "p90": 181.39999999999998,
      "p95": 251.79999999999956,
      "max": 20333,
      "min": 18
    }
  },
  "critical_depth": {
    "n": 343,
    "sum": 294319,
    "mean": 858.072886297376,
    "median": 431,
    "p90": 895.4000000000001,
    "p95": 1148.8999999999996,
    "max": 30645,
    "min": 83
  },
  "sampled_work_over_critical_depth": {
    "n": 343,
    "sum": 390.1484170006507,
    "mean": 1.137458941692859,
    "median": 1.116991643454039,
    "p90": 1.316964533555399,
    "p95": 1.4033547459252156,
    "max": 1.6241258741258742,
    "min": 1.0
  },
  "elapsed_seconds_per_question": {
    "n": 343,
    "sum": 12071.67303442955,
    "mean": 35.19438202457595,
    "median": 15.032788753509521,
    "p90": 30.690776109695438,
    "p95": 40.904174327850335,
    "max": 1566.0891604423523,
    "min": 2.4431560039520264
  },
  "generation_calls": {
    "n": 343,
    "sum": 2240,
    "mean": 6.530612244897959,
    "median": 6,
    "p90": 8.0,
    "p95": 9.899999999999977,
    "max": 296,
    "min": 1
  },
  "call_budget_reached": {
    "path": 2,
    "main": 1
  },
  "sampled_eos_by_phase": {
    "main_sampled_eos": 337,
    "summary_sampled_eos": 3
  },
  "runtime_closure_label_replacements": 6,
  "exact_duplicate_paths_within_trace": 166,
  "path_repeated_5gram_fraction": {
    "n": 845,
    "sum": 46.01443160467347,
    "mean": 0.05445494864458399,
    "median": 0.0,
    "p90": 0.16000000000000003,
    "p95": 0.4444444444444444,
    "max": 0.9727917981072555,
    "min": 0.0
  },
  "paths_with_repeated_5gram_fraction_over_half": 3,
  "think_markup": {
    "open=0,close=0": 12,
    "open=0,close=1": 78,
    "open=0,close=2": 32,
    "open=1,close=0": 69,
    "open=1,close=1": 98,
    "open=2,close=0": 53,
    "open=2,close=1": 1
  },
  "think_structure": {
    "exactly_one_balanced_think": 63,
    "all_forks_inside_think": 62,
    "final_after_think": 63,
    "fully_valid": 62
  },
  "by_max_width": {
    "0": {
      "n": 92,
      "correct": 14,
      "pass_at_1": 0.15217391304347827,
      "ci95": [
        0.09286540270143614,
        0.23936512897551807
      ],
      "final_answer_only_correct": 22,
      "final_answer_only_pass_at_1": 0.2391304347826087
    },
    "2": {
      "n": 190,
      "correct": 19,
      "pass_at_1": 0.1,
      "ci95": [
        0.06495707849098338,
        0.1508969450767923
      ],
      "final_answer_only_correct": 35,
      "final_answer_only_pass_at_1": 0.18421052631578946
    },
    "3": {
      "n": 31,
      "correct": 6,
      "pass_at_1": 0.1935483870967742,
      "ci95": [
        0.09187008361586096,
        0.36280257811795463
      ],
      "final_answer_only_correct": 6,
      "final_answer_only_pass_at_1": 0.1935483870967742
    },
    "4": {
      "n": 21,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        0,
        0.154639018924847
      ],
      "final_answer_only_correct": 0,
      "final_answer_only_pass_at_1": 0.0
    },
    "5": {
      "n": 7,
      "correct": 1,
      "pass_at_1": 0.14285714285714285,
      "ci95": [
        0.02567962434474355,
        0.5131278292743189
      ],
      "final_answer_only_correct": 1,
      "final_answer_only_pass_at_1": 0.14285714285714285
    },
    "6": {
      "n": 2,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        0,
        0.6576197724933469
      ],
      "final_answer_only_correct": 0,
      "final_answer_only_pass_at_1": 0.0
    }
  },
  "context_audit": {
    "forks_checked": 349,
    "sibling_prefix_mismatches": 0,
    "policy_label_or_mask_errors": []
  },
  "theoretical_ratio_note": "Sampled work / serial critical token depth. Branches execute sequentially per GPU in this evaluator; this ratio is not measured speedup.",
  "extraction_tests": 13
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/trace-statistics.jsonl](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/trace-statistics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/REPORT.md](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/analysis-status.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/analysis-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "historical_pass_at_1": 0.108,
  "final_answer_only_pass_at_1": 0.202,
  "updated_at": "2026-10-09T22:24:17.895430+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/previous-comparison.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/previous-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "gsm_infinite_ep5": {
    "n": 500,
    "historical_correct": 84,
    "historical_pass_at_1": 0.168,
    "final_answer_only_correct": 84,
    "final_answer_only_pass_at_1": 0.168,
    "old_summary_correct": 84,
    "errors": []
  },
  "sft_messages_ep5": {
    "n": 500,
    "historical_correct": 79,
    "historical_pass_at_1": 0.158,
    "final_answer_only_correct": 79,
    "final_answer_only_pass_at_1": 0.158,
    "old_summary_correct": 79,
    "errors": []
  },
  "mixed_ep1": {
    "n": 500,
    "historical_correct": 61,
    "historical_pass_at_1": 0.122,
    "final_answer_only_correct": 61,
    "final_answer_only_pass_at_1": 0.122,
    "old_summary_correct": 61,
    "errors": []
  }
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/status.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "generated",
  "started_at": "2026-10-09T21:13:06.724404+00:00",
  "completed": 500,
  "total": 500,
  "worker_pids": [
    1060734,
    1060735,
    1060736,
    1060737,
    1060738,
    1060739,
    1060740,
    1060741
  ],
  "elapsed_seconds": 4249.050662994385,
  "total_sampled_tokens": 526516,
  "mean_trace_seconds": 39.56669182443619,
  "eta_utc": "2026-10-09T22:23:55.775532+00:00",
  "finished_at": "2026-10-09T22:23:55.779088+00:00",
  "updated_at": "2026-10-09T22:23:55.779097+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/summary.json](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "force_think_prefix": true,
  "forced_initial_prefix_action_mask": 0,
  "state": "complete",
  "updated_at": "2026-10-09T22:24:14.698141+00:00",
  "questions": 500,
  "total_questions": 500,
  "samples_per_question": 1,
  "correct": 54,
  "pass_at_1": 0.108,
  "ci95": [
    0.08372280963705037,
    0.13825467328480662
  ],
  "invalid_answers": 264,
  "extraction": {
    "boxed": 236,
    "unfinished_thinking": 264
  },
  "scorer_errors": [],
  "final_answer_only_diagnostic": {
    "correct": 101,
    "pass_at_1": 0.202,
    "ci95": [
      0.16914122067557874,
      0.23940288623950645
    ],
    "invalid_answers": 11,
    "description": "Primary answer-equivalence metric: remove think tags before the same reference-blind extraction. Historical think-gated scoring and format compliance are retained separately; this legacy field name is kept for compatibility."
  },
  "by_subject": {
    "Algebra": {
      "n": 124,
      "correct": 19,
      "pass_at_1": 0.1532258064516129,
      "ci95": [
        0.10034252876653711,
        0.2269492528407071
      ],
      "final_answer_only_correct": 39,
      "final_answer_only_pass_at_1": 0.31451612903225806
    },
    "Counting & Probability": {
      "n": 38,
      "correct": 3,
      "pass_at_1": 0.07894736842105263,
      "ci95": [
        0.027214595506987724,
        0.20799371457771454
      ],
      "final_answer_only_correct": 4,
      "final_answer_only_pass_at_1": 0.10526315789473684
    },
    "Geometry": {
      "n": 41,
      "correct": 2,
      "pass_at_1": 0.04878048780487805,
      "ci95": [
        0.013480945365169042,
        0.16138978870370846
      ],
      "final_answer_only_correct": 6,
      "final_answer_only_pass_at_1": 0.14634146341463414
    },
    "Intermediate Algebra": {
      "n": 97,
      "correct": 5,
      "pass_at_1": 0.05154639175257732,
      "ci95": [
        0.022216051037510606,
        0.11504355411462804
      ],
      "final_answer_only_correct": 8,
      "final_answer_only_pass_at_1": 0.08247422680412371
    },
    "Number Theory": {
      "n": 62,
      "correct": 6,
      "pass_at_1": 0.0967741935483871,
      "ci95": [
        0.045111872023193916,
        0.19548818612307423
      ],
      "final_answer_only_correct": 14,
      "final_answer_only_pass_at_1": 0.22580645161290322
    },
    "Prealgebra": {
      "n": 82,
      "correct": 15,
      "pass_at_1": 0.18292682926829268,
      "ci95": [
        0.1141102185364291,
        0.2801218842914394
      ],
      "final_answer_only_correct": 24,
      "final_answer_only_pass_at_1": 0.2926829268292683
    },
    "Precalculus": {
      "n": 56,
      "correct": 4,
      "pass_at_1": 0.07142857142857142,
      "ci95": [
        0.028126036578876953,
        0.16975448060863452
      ],
      "final_answer_only_correct": 6,
      "final_answer_only_pass_at_1": 0.10714285714285714
    }
  },
  "by_level": {
    "1": {
      "n": 43,
      "correct": 12,
      "pass_at_1": 0.27906976744186046,
      "ci95": [
        0.16746613786237488,
        0.42691028681878873
      ],
      "final_answer_only_correct": 23,
      "final_answer_only_pass_at_1": 0.5348837209302325
    },
    "2": {
      "n": 90,
      "correct": 14,
      "pass_at_1": 0.15555555555555556,
      "ci95": [
        0.09498275594910817,
        0.24432845277298365
      ],
      "final_answer_only_correct": 24,
      "final_answer_only_pass_at_1": 0.26666666666666666
    },
    "3": {
      "n": 105,
      "correct": 19,
      "pass_at_1": 0.18095238095238095,
      "ci95": [
        0.11901666335076498,
        0.26540908097542887
      ],
      "final_answer_only_correct": 33,
      "final_answer_only_pass_at_1": 0.3142857142857143
    },
    "4": {
      "n": 128,
      "correct": 5,
      "pass_at_1": 0.0390625,
      "ci95": [
        0.016798610797803704,
        0.08818702076683686
      ],
      "final_answer_only_correct": 12,
      "final_answer_only_pass_at_1": 0.09375
    },
    "5": {
      "n": 134,
      "correct": 4,
      "pass_at_1": 0.029850746268656716,
      "ci95": [
        0.011668334655484836,
        0.07423803141176379
      ],
      "final_answer_only_correct": 9,
      "final_answer_only_pass_at_1": 0.06716417910447761
    }
  },
  "by_parallel": {
    "False": {
      "n": 141,
      "correct": 24,
      "pass_at_1": 0.1702127659574468,
      "ci95": [
        0.11713332577992983,
        0.24078532018504242
      ],
      "final_answer_only_correct": 48,
      "final_answer_only_pass_at_1": 0.3404255319148936
    },
    "True": {
      "n": 359,
      "correct": 30,
      "pass_at_1": 0.08356545961002786,
      "ci95": [
        0.05916066658202963,
        0.11678796681888158
      ],
      "final_answer_only_correct": 53,
      "final_answer_only_pass_at_1": 0.14763231197771587
    }
  },
  "forks": {
    "0": 141,
    "1": 320,
    "13": 1,
    "2": 35,
    "3": 3
  },
  "widths": {
    "2": 322,
    "3": 57,
    "4": 27,
    "5": 2,
    "6": 3,
    "8": 1
  },
  "parallel_questions": 359,
  "multi_round_questions": 39,
  "format_invalid_questions": 12,
  "invalid_width_questions": 4,
  "budget_exhausted_questions": 5,
  "response_tokens": {
    "n": 500,
    "sum": 531630,
    "mean": 1063.26,
    "median": 482.0,
    "p90": 1151.1,
    "p95": 1561.349999999997,
    "max": 30720,
    "min": 57
  },
  "sampled_tokens": {
    "n": 500,
    "sum": 526516,
    "mean": 1053.032,
    "median": 473.0,
    "p90": 1129.0000000000002,
    "p95": 1549.4499999999978,
    "max": 30718,
    "min": 55
  },
  "forced_tokens": {
    "n": 500,
    "sum": 5114,
    "mean": 10.228,
    "median": 11.0,
    "p90": 17.0,
    "p95": 23.0,
    "max": 120,
    "min": 2
  },
  "phase_tokens": {
    "main": {
      "n": 911,
      "sum": 365440,
      "mean": 401.14160263446763,
      "median": 131,
      "p90": 343.0,
      "p95": 475.5,
      "max": 30718,
      "min": 1
    },
    "width": {
      "n": 416,
      "sum": 833,
      "mean": 2.0024038461538463,
      "median": 2.0,
      "p90": 2.0,
      "p95": 2.0,
      "max": 3,
      "min": 2
    },
    "path": {
      "n": 959,
      "sum": 95184,
      "mean": 99.2533889468196,
      "median": 75,
      "p90": 181.0,
      "p95": 247.59999999999945,
      "max": 752,
      "min": 10
    },
    "summary": {
      "n": 412,
      "sum": 65059,
      "mean": 157.9101941747573,
      "median": 77.5,
      "p90": 158.90000000000003,
      "p95": 227.4999999999999,
      "max": 26126,
      "min": 20
    }
  },
  "critical_depth": {
    "n": 500,
    "sum": 483992,
    "mean": 967.984,
    "median": 411.0,
    "p90": 956.9000000000002,
    "p95": 1212.8499999999992,
    "max": 30718,
    "min": 55
  },
  "sampled_work_over_critical_depth": {
    "n": 500,
    "sum": 568.923234381505,
    "mean": 1.13784646876301,
    "median": 1.1289861261058025,
    "p90": 1.2989958096128482,
    "p95": 1.358448257711338,
    "max": 2.0329557157569518,
    "min": 1.0
  },
  "elapsed_seconds_per_question": {
    "n": 500,
    "sum": 19783.345912218094,
    "mean": 39.56669182443619,
    "median": 14.002795577049255,
    "p90": 33.448477029800415,
    "p95": 45.68418424129484,
    "max": 1572.8322384357452,
    "min": 1.5724787712097168
  },
  "generation_calls": {
    "n": 500,
    "sum": 2698,
    "mean": 5.396,
    "median": 6.0,
    "p90": 8.0,
    "p95": 11.0,
    "max": 65,
    "min": 1
  },
  "call_budget_reached": {
    "main": 4,
    "summary": 1
  },
  "sampled_eos_by_phase": {
    "main_sampled_eos": 491,
    "summary_sampled_eos": 2
  },
  "runtime_closure_label_replacements": 10,
  "exact_duplicate_paths_within_trace": 1,
  "path_repeated_5gram_fraction": {
    "n": 960,
    "sum": 29.171795357630238,
    "mean": 0.03038728683086483,
    "median": 0.0,
    "p90": 0.10209314495028782,
    "p95": 0.1696635656938956,
    "max": 0.4631578947368421,
    "min": 0.0
  },
  "paths_with_repeated_5gram_fraction_over_half": 0,
  "think_markup": {
    "open=1,close=0": 30,
    "open=1,close=1": 228,
    "open=1,close=2": 3,
    "open=2,close=0": 231,
    "open=2,close=1": 5,
    "open=3,close=0": 3
  },
  "think_structure": {
    "exactly_one_balanced_think": 228,
    "all_forks_inside_think": 227,
    "final_after_think": 228,
    "fully_valid": 227
  },
  "answer_format": {
    "explicit_final_header": 481,
    "standalone_final_header": 480,
    "multiple_final_headers": 2,
    "boxed_after_final_header": 480,
    "final_header_inside_path": 0,
    "explicit_unresolved": 0
  },
  "by_max_width": {
    "0": {
      "n": 141,
      "correct": 24,
      "pass_at_1": 0.1702127659574468,
      "ci95": [
        0.11713332577992983,
        0.24078532018504242
      ],
      "final_answer_only_correct": 48,
      "final_answer_only_pass_at_1": 0.3404255319148936
    },
    "2": {
      "n": 273,
      "correct": 27,
      "pass_at_1": 0.0989010989010989,
      "ci95": [
        0.06886334030280082,
        0.1400701737275422
      ],
      "final_answer_only_correct": 47,
      "final_answer_only_pass_at_1": 0.17216117216117216
    },
    "3": {
      "n": 55,
      "correct": 3,
      "pass_at_1": 0.05454545454545454,
      "ci95": [
        0.01872321555468448,
        0.14853060544053792
      ],
      "final_answer_only_correct": 4,
      "final_answer_only_pass_at_1": 0.07272727272727272
    },
    "4": {
      "n": 26,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        0,
        0.1287289218592153
      ],
      "final_answer_only_correct": 2,
      "final_answer_only_pass_at_1": 0.07692307692307693
    },
    "5": {
      "n": 1,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        0,
        0.7934506856227626
      ],
      "final_answer_only_correct": 0,
      "final_answer_only_pass_at_1": 0.0
    },
    "6": {
      "n": 3,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        5.551115123125783e-17,
        0.5614970317550454
      ],
      "final_answer_only_correct": 0,
      "final_answer_only_pass_at_1": 0.0
    },
    "8": {
      "n": 1,
      "correct": 0,
      "pass_at_1": 0.0,
      "ci95": [
        0,
        0.7934506856227626
      ],
      "final_answer_only_correct": 0,
      "final_answer_only_pass_at_1": 0.0
    }
  },
  "context_audit": {
    "forks_checked": 412,
    "sibling_prefix_mismatches": 0,
    "policy_label_or_mask_errors": []
  },
  "theoretical_ratio_note": "Sampled work / serial critical token depth. Branches execute sequentially per GPU in this evaluator; this ratio is not measured speedup.",
  "extraction_tests": 13,
  "primary_metric": "Math-Verify final-answer equivalence, independent of think-tag validity",
  "primary_correct": 101,
  "primary_pass_at_1": 0.202,
  "primary_ci95": [
    0.16914122067557874,
    0.23940288623950645
  ],
  "historical_extraction_pass_at_1": 0.108
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/trace-statistics.jsonl](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/trace-statistics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/rl-smoke-status.json](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "exit_code": 0,
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-v3/smoke.log",
  "at": "2026-10-09T20:08:40.368505+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v1-status.json](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v1-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "exit_code": 1,
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke/smoke.log",
  "at": "2026-10-09T19:57:13.893917+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/rl-smoke-v2-status.json](../artifacts/work/experiments/unseen-wide5145-20261009/rl-smoke-v2-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "exit_code": 2,
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/rl-smoke-v2/smoke.log",
  "at": "2026-10-09T20:03:31.650074+00:00"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/result.json](../artifacts/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "stage": "00_canary_v2",
  "started_at": "2026-10-09T19:28:10.013521+00:00",
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
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/sft.log",
  "target_steps": 1,
  "finished_at": "2026-10-09T19:28:57.774515+00:00",
  "steps": 1,
  "final": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/00_canary_v2/final"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/runs/01_sft/result.json](../artifacts/work/experiments/unseen-wide5145-20261009/runs/01_sft/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "stage": "01_sft",
  "started_at": "2026-10-09T19:28:57.779271+00:00",
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
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/sft.log",
  "target_steps": 180,
  "finished_at": "2026-10-09T19:55:31.454250+00:00",
  "steps": 180,
  "final": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/status-canary-v1-failed.json](../artifacts/work/experiments/unseen-wide5145-20261009/status-canary-v1-failed.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "at": "2026-10-09T19:28:03.297319+00:00",
  "error": "AssertionError(('00_canary', 1, 0, 1))"
}
```

</details>

- [work/experiments/unseen-wide5145-20261009/status.json](../artifacts/work/experiments/unseen-wide5145-20261009/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "stage": "01_sft",
  "started_at": "2026-10-09T19:28:57.779271+00:00",
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
  "log": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/sft.log",
  "target_steps": 180,
  "finished_at": "2026-10-09T19:55:31.454250+00:00",
  "steps": 180,
  "final": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final"
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/unseen-wide5145-20261009/controller.py](../artifacts/work/experiments/unseen-wide5145-20261009/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-20261009/controller.py](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-20261009/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/controller.py](../artifacts/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/unseen-wide5145-20261009/prepare.py](../artifacts/work/experiments/unseen-wide5145-20261009/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
