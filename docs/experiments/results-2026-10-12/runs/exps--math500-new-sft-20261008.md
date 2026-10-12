# exps/math500-new-sft-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/config.yaml](../artifacts/exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    temperature: 0.6
    top_k: 20
    top_p: 0.95
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 32768
    max_model_len: 32768
    max_num_seqs: 32
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
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
      top_k: 20
      top_p: 0.95
      temperature: 0.6
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 8192
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
    seed: 42
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_EVAL_MODEL}
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
  experiment_name: ${oc.env:PARALLEL_R1_EVAL_NAME}
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${trainer.default_local_dir}
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
  default_local_dir: ${oc.env:PARALLEL_R1_OUTPUT_ROOT,checkpoints}/eval/${trainer.experiment_name}
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${data.val_files}
  val_files: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2048
  max_response_length: 30720
  train_batch_size: 8
  val_batch_size: 512
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
  path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/score.py
  name: compute_score
algorithm:
  _target_: verl.trainer.config.AlgoConfig
  gamma: 1.0
  lam: 1.0
  adv_estimator: grpo
  norm_adv_by_std_in_grpo: true
  split_accuracy_aux: false
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
  temp_dir: ${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
  object_store_memory: 4294967296
  plasma_directory: ${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/hydra.yaml](../artifacts/exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${oc.env:PARALLEL_R1_SCRATCH_ROOT,checkpoints}/hydra/${trainer.experiment_name}
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
    - data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
    - data.val_batch_size=512
    - data.max_prompt_length=2048
    - data.max_response_length=30720
    - actor_rollout_ref.rollout.mode=async
    - actor_rollout_ref.rollout.tensor_model_parallel_size=1
    - ++actor_rollout_ref.rollout.seed=42
    - actor_rollout_ref.rollout.max_model_len=32768
    - actor_rollout_ref.rollout.max_num_batched_tokens=32768
    - actor_rollout_ref.rollout.max_num_seqs=32
    - actor_rollout_ref.rollout.enable_chunked_prefill=true
    - actor_rollout_ref.rollout.temperature=0.6
    - actor_rollout_ref.rollout.top_p=0.95
    - actor_rollout_ref.rollout.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.temperature=0.6
    - actor_rollout_ref.rollout.val_kwargs.top_p=0.95
    - actor_rollout_ref.rollout.val_kwargs.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.n=1
    - actor_rollout_ref.rollout.agent.num_paths=2
    - actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
    - actor_rollout_ref.rollout.agent.max_path_response_length=8192
    - actor_rollout_ref.rollout.agent.num_workers=8
    - custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/score.py
    - custom_reward_function.name=compute_score
    - ray_init.num_cpus=32
    - ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
    - ++ray_init.object_store_memory=4294967296
    - ++ray_init.plasma_directory=${SHM_ROOT}
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.rollout.seed=42,++ray_init.object_store_memory=4294967296,++ray_init.plasma_directory=${SHM_ROOT},++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5,actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0,actor_rollout_ref.rollout.agent.max_path_response_length=8192,actor_rollout_ref.rollout.agent.num_paths=2,actor_rollout_ref.rollout.agent.num_workers=8,actor_rollout_ref.rollout.enable_chunked_prefill=true,actor_rollout_ref.rollout.max_model_len=32768,actor_rollout_ref.rollout.max_num_batched_tokens=32768,actor_rollout_ref.rollout.max_num_seqs=32,actor_rollout_ref.rollout.mode=async,actor_rollout_ref.rollout.temperature=0.6,actor_rollout_ref.rollout.tensor_model_parallel_size=1,actor_rollout_ref.rollout.top_k=20,actor_rollout_ref.rollout.top_p=0.95,actor_rollout_ref.rollout.val_kwargs.n=1,actor_rollout_ref.rollout.val_kwargs.temperature=0.6,actor_rollout_ref.rollout.val_kwargs.top_k=20,actor_rollout_ref.rollout.val_kwargs.top_p=0.95,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/score.py,data.max_prompt_length=2048,data.max_response_length=30720,data.val_batch_size=512,data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet,ray_init.num_cpus=32,trainer.n_gpus_per_node=8
    id: ???
    num: ???
    config_name: eval_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5
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

- [exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/overrides.yaml](../artifacts/exps/math500-new-sft-20261008/attempts/startup-import-01/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- trainer.n_gpus_per_node=8
- data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
- data.val_batch_size=512
- data.max_prompt_length=2048
- data.max_response_length=30720
- actor_rollout_ref.rollout.mode=async
- actor_rollout_ref.rollout.tensor_model_parallel_size=1
- ++actor_rollout_ref.rollout.seed=42
- actor_rollout_ref.rollout.max_model_len=32768
- actor_rollout_ref.rollout.max_num_batched_tokens=32768
- actor_rollout_ref.rollout.max_num_seqs=32
- actor_rollout_ref.rollout.enable_chunked_prefill=true
- actor_rollout_ref.rollout.temperature=0.6
- actor_rollout_ref.rollout.top_p=0.95
- actor_rollout_ref.rollout.top_k=20
- actor_rollout_ref.rollout.val_kwargs.temperature=0.6
- actor_rollout_ref.rollout.val_kwargs.top_p=0.95
- actor_rollout_ref.rollout.val_kwargs.top_k=20
- actor_rollout_ref.rollout.val_kwargs.n=1
- actor_rollout_ref.rollout.agent.num_paths=2
- actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
- actor_rollout_ref.rollout.agent.max_path_response_length=8192
- actor_rollout_ref.rollout.agent.num_workers=8
- custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/score.py
- custom_reward_function.name=compute_score
- ray_init.num_cpus=32
- ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
- ++ray_init.object_store_memory=4294967296
- ++ray_init.plasma_directory=${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/manifest.json](../artifacts/exps/math500-new-sft-20261008/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "dataset": "HuggingFaceH4/MATH-500",
  "source_sha256": "35dc41080a3680858b27fa7e0533d2d547825316fc5dafe5d316f4ccc5a06132",
  "dataset_sha256": "786c521edbb220b8f3e051c227571c527f0043967574142d1e4e80aa158974dc",
  "questions": 500,
  "samples_per_question": 1,
  "models": [
    {
      "name": "gsm_infinite_ep5",
      "path": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final",
      "epoch": 5,
      "weights_sha256": "101d49a2e82b3c3433ae9101a39a92e3c819e547b96f5dc7e0df5cd27d739756",
      "max_prompt_tokens": 875
    },
    {
      "name": "sft_messages_ep5",
      "path": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final",
      "epoch": 5,
      "weights_sha256": "0b45d350fb935dfe04c8f3a57c9fdb4f450df9ac562eee47f5891736f9a36ee1",
      "max_prompt_tokens": 875
    },
    {
      "name": "mixed_ep1",
      "path": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/checkpoints/global_step_35",
      "epoch": 1,
      "weights_sha256": "28880a9ee008724ab17da967a16bc3d01e5319d5273e5fe92737e2ce1c76ad48",
      "max_prompt_tokens": 875
    }
  ],
  "system_prompt": "Solve the problem step by step. Use <Parallel> only for genuinely independent required subcomputations that can be carried out simultaneously from the information already known at that point; write one <Path> per independent subcomputation, and follow the block with a short <Summary> of the branch results. Otherwise reason sequentially. End with 'Final Answer: <answer>'.",
  "max_prompt_tokens": 2048,
  "max_response_tokens": 30720,
  "max_model_len": 32768,
  "temperature": 0.6,
  "top_p": 0.95,
  "top_k": 20,
  "repetition_penalty": 1.0,
  "engine_seed": 42,
  "branch_seed_policy": "Runtime random seeds saved per call; asynchronous scheduling is not bitwise deterministic.",
  "runtime": "existing async Parallel-R1 v3 fork/join, snapshot sampling fixes only",
  "fixed_num_paths": 2,
  "max_forks": 0,
  "max_forks_meaning": "No fixed round cap; bounded by total response token budget",
  "max_path_response_tokens": 8192,
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
  "models_sequential": true,
  "scorer": "Math-Verify 0.8.0; reference-blind final answer extraction",
  "scorer_tests": 13,
  "reference_tests": 500,
  "limitations": [
    "Width is fixed by runtime, not selected by model.",
    "vLLM summary/main continuation does not apply Unseen custom positions/mask.",
    "One stochastic sample per problem.",
    "Tag validity includes manually inserted tags; raw generation calls are saved separately."
  ],
  "snapshot_patches": [
    {
      "file": "verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py",
      "before": "93385e578f2f17c8ed774b950df52b2e34f0ffc3b8aa8d773d649f358fb767c2",
      "after": "b3f07b8272ce5b1ee0a624f0288d172190749b42f0f8d117483d7ef4b792da62",
      "old": "\"temperature\": 1.0, \"max_tokens\": max_len",
      "new": "\"temperature\": sampling_params[\"temperature\"], \"max_tokens\": max_len"
    },
    {
      "file": "verl/parallel_thinking_generation_v3/agent_loop.py",
      "before": "4b8438240de67ef4638fe4c7ed1e4e76da7e31d300a7f78c7dfed1def55a52ac",
      "after": "f65b216a45b7a0720df28d4267b6e61ffeb80ff94704fd771d0eb027cbf61331",
      "old": "            top_p=config.top_p,",
      "new": "            top_p=config.top_p,\n            top_k=config.top_k,"
    },
    {
      "file": "verl/parallel_thinking_generation_v3/agent_loop.py",
      "before": "f65b216a45b7a0720df28d4267b6e61ffeb80ff94704fd771d0eb027cbf61331",
      "after": "7f027ef7d64779de3f5458f3f2ca80048ede5a8a62628281e63ac745d0f4739e",
      "old": "            sampling_params[\"top_p\"] = config.val_kwargs.top_p",
      "new": "            sampling_params[\"top_k\"] = config.val_kwargs.top_k\n            sampling_params[\"top_p\"] = config.val_kwargs.top_p"
    },
    {
      "file": "verl/parallel_thinking_generation_v3/repro_trace.py",
      "before": "a085e84d076b97600c8dcc5a47ead1cb4edf0bbe9518b638dd137f4943f6bc82",
      "after": "8d2bbcbbffda9b4abc0c65e00e80deb20298c42799758dbd24d9305ba6ba8960",
      "old": "generated_tokens=len(ids), generated_ids=list(ids),",
      "new": "generated_tokens=len(ids), generated_ids=list(ids), sampling_params=dict(sampling_params),"
    }
  ],
  "scorer_isolation": "Persistent clean Python subprocess via reward_bridge.py to avoid verl ANTLR version conflict",
  "evaluation_files_sha256": {
    "score.py": "8b5be1ffb390c0903ac914466e8b64433b20b5ef699ec3484779a8b31d30d125",
    "prepare.py": "e3a03d84f131153e320c630a9c63cdae5cfd20302804a53b6e88742873a1ece6",
    "analyze.py": "22033bca7ebb50ea36d4a018c6c8b152c69b13e1694b269d975310a65a85d2a0",
    "run_queue.py": "d550af2b21ced3a2f278d41efa754b239e3c01e7c7bcaaca895abacb53200564",
    "reward_bridge.py": "a70e25e9682638bb67b4f53f414a55cc127bc2d0dc7c15b35f0dc146219e0261",
    "recover_launch.py": "044873d5c74cec514e582883781d9c45876feea29eaa231419d8ddcc75386d94"
  }
}
```

</details>

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/config.yaml](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    temperature: 0.6
    top_k: 20
    top_p: 0.95
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 32768
    max_model_len: 32768
    max_num_seqs: 32
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
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
      top_k: 20
      top_p: 0.95
      temperature: 0.6
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 8192
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
    seed: 42
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_EVAL_MODEL}
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
  experiment_name: ${oc.env:PARALLEL_R1_EVAL_NAME}
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${trainer.default_local_dir}
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
  default_local_dir: ${oc.env:PARALLEL_R1_OUTPUT_ROOT,checkpoints}/eval/${trainer.experiment_name}
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${data.val_files}
  val_files: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2048
  max_response_length: 30720
  train_batch_size: 8
  val_batch_size: 512
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
  path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
  name: compute_score
algorithm:
  _target_: verl.trainer.config.AlgoConfig
  gamma: 1.0
  lam: 1.0
  adv_estimator: grpo
  norm_adv_by_std_in_grpo: true
  split_accuracy_aux: false
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
  temp_dir: ${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
  object_store_memory: 4294967296
  plasma_directory: ${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/hydra.yaml](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${oc.env:PARALLEL_R1_SCRATCH_ROOT,checkpoints}/hydra/${trainer.experiment_name}
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
    - data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
    - data.val_batch_size=512
    - data.max_prompt_length=2048
    - data.max_response_length=30720
    - actor_rollout_ref.rollout.mode=async
    - actor_rollout_ref.rollout.tensor_model_parallel_size=1
    - ++actor_rollout_ref.rollout.seed=42
    - actor_rollout_ref.rollout.max_model_len=32768
    - actor_rollout_ref.rollout.max_num_batched_tokens=32768
    - actor_rollout_ref.rollout.max_num_seqs=32
    - actor_rollout_ref.rollout.enable_chunked_prefill=true
    - actor_rollout_ref.rollout.temperature=0.6
    - actor_rollout_ref.rollout.top_p=0.95
    - actor_rollout_ref.rollout.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.temperature=0.6
    - actor_rollout_ref.rollout.val_kwargs.top_p=0.95
    - actor_rollout_ref.rollout.val_kwargs.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.n=1
    - actor_rollout_ref.rollout.agent.num_paths=2
    - actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
    - actor_rollout_ref.rollout.agent.max_path_response_length=8192
    - actor_rollout_ref.rollout.agent.num_workers=8
    - custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
    - custom_reward_function.name=compute_score
    - ray_init.num_cpus=32
    - ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
    - ++ray_init.object_store_memory=4294967296
    - ++ray_init.plasma_directory=${SHM_ROOT}
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.rollout.seed=42,++ray_init.object_store_memory=4294967296,++ray_init.plasma_directory=${SHM_ROOT},++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5,actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0,actor_rollout_ref.rollout.agent.max_path_response_length=8192,actor_rollout_ref.rollout.agent.num_paths=2,actor_rollout_ref.rollout.agent.num_workers=8,actor_rollout_ref.rollout.enable_chunked_prefill=true,actor_rollout_ref.rollout.max_model_len=32768,actor_rollout_ref.rollout.max_num_batched_tokens=32768,actor_rollout_ref.rollout.max_num_seqs=32,actor_rollout_ref.rollout.mode=async,actor_rollout_ref.rollout.temperature=0.6,actor_rollout_ref.rollout.tensor_model_parallel_size=1,actor_rollout_ref.rollout.top_k=20,actor_rollout_ref.rollout.top_p=0.95,actor_rollout_ref.rollout.val_kwargs.n=1,actor_rollout_ref.rollout.val_kwargs.temperature=0.6,actor_rollout_ref.rollout.val_kwargs.top_k=20,actor_rollout_ref.rollout.val_kwargs.top_p=0.95,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py,data.max_prompt_length=2048,data.max_response_length=30720,data.val_batch_size=512,data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet,ray_init.num_cpus=32,trainer.n_gpus_per_node=8
    id: ???
    num: ???
    config_name: eval_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5
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

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/overrides.yaml](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/scratch/hydra/gsm_infinite_ep5/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- trainer.n_gpus_per_node=8
- data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
- data.val_batch_size=512
- data.max_prompt_length=2048
- data.max_response_length=30720
- actor_rollout_ref.rollout.mode=async
- actor_rollout_ref.rollout.tensor_model_parallel_size=1
- ++actor_rollout_ref.rollout.seed=42
- actor_rollout_ref.rollout.max_model_len=32768
- actor_rollout_ref.rollout.max_num_batched_tokens=32768
- actor_rollout_ref.rollout.max_num_seqs=32
- actor_rollout_ref.rollout.enable_chunked_prefill=true
- actor_rollout_ref.rollout.temperature=0.6
- actor_rollout_ref.rollout.top_p=0.95
- actor_rollout_ref.rollout.top_k=20
- actor_rollout_ref.rollout.val_kwargs.temperature=0.6
- actor_rollout_ref.rollout.val_kwargs.top_p=0.95
- actor_rollout_ref.rollout.val_kwargs.top_k=20
- actor_rollout_ref.rollout.val_kwargs.n=1
- actor_rollout_ref.rollout.agent.num_paths=2
- actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
- actor_rollout_ref.rollout.agent.max_path_response_length=8192
- actor_rollout_ref.rollout.agent.num_workers=8
- custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
- custom_reward_function.name=compute_score
- ray_init.num_cpus=32
- ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/gsm_infinite_ep5
- ++ray_init.object_store_memory=4294967296
- ++ray_init.plasma_directory=${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/config.yaml](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    temperature: 0.6
    top_k: 20
    top_p: 0.95
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 32768
    max_model_len: 32768
    max_num_seqs: 32
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
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
      top_k: 20
      top_p: 0.95
      temperature: 0.6
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 8192
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
    seed: 42
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_EVAL_MODEL}
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
  experiment_name: ${oc.env:PARALLEL_R1_EVAL_NAME}
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${trainer.default_local_dir}
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
  default_local_dir: ${oc.env:PARALLEL_R1_OUTPUT_ROOT,checkpoints}/eval/${trainer.experiment_name}
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${data.val_files}
  val_files: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2048
  max_response_length: 30720
  train_batch_size: 8
  val_batch_size: 512
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
  path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
  name: compute_score
algorithm:
  _target_: verl.trainer.config.AlgoConfig
  gamma: 1.0
  lam: 1.0
  adv_estimator: grpo
  norm_adv_by_std_in_grpo: true
  split_accuracy_aux: false
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
  temp_dir: ${TMPDIR}/math500sft-20261008/mixed_ep1
  object_store_memory: 4294967296
  plasma_directory: ${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/hydra.yaml](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${oc.env:PARALLEL_R1_SCRATCH_ROOT,checkpoints}/hydra/${trainer.experiment_name}
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
    - data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
    - data.val_batch_size=512
    - data.max_prompt_length=2048
    - data.max_response_length=30720
    - actor_rollout_ref.rollout.mode=async
    - actor_rollout_ref.rollout.tensor_model_parallel_size=1
    - ++actor_rollout_ref.rollout.seed=42
    - actor_rollout_ref.rollout.max_model_len=32768
    - actor_rollout_ref.rollout.max_num_batched_tokens=32768
    - actor_rollout_ref.rollout.max_num_seqs=32
    - actor_rollout_ref.rollout.enable_chunked_prefill=true
    - actor_rollout_ref.rollout.temperature=0.6
    - actor_rollout_ref.rollout.top_p=0.95
    - actor_rollout_ref.rollout.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.temperature=0.6
    - actor_rollout_ref.rollout.val_kwargs.top_p=0.95
    - actor_rollout_ref.rollout.val_kwargs.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.n=1
    - actor_rollout_ref.rollout.agent.num_paths=2
    - actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
    - actor_rollout_ref.rollout.agent.max_path_response_length=8192
    - actor_rollout_ref.rollout.agent.num_workers=8
    - custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
    - custom_reward_function.name=compute_score
    - ray_init.num_cpus=32
    - ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/mixed_ep1
    - ++ray_init.object_store_memory=4294967296
    - ++ray_init.plasma_directory=${SHM_ROOT}
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.rollout.seed=42,++ray_init.object_store_memory=4294967296,++ray_init.plasma_directory=${SHM_ROOT},++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/mixed_ep1,actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0,actor_rollout_ref.rollout.agent.max_path_response_length=8192,actor_rollout_ref.rollout.agent.num_paths=2,actor_rollout_ref.rollout.agent.num_workers=8,actor_rollout_ref.rollout.enable_chunked_prefill=true,actor_rollout_ref.rollout.max_model_len=32768,actor_rollout_ref.rollout.max_num_batched_tokens=32768,actor_rollout_ref.rollout.max_num_seqs=32,actor_rollout_ref.rollout.mode=async,actor_rollout_ref.rollout.temperature=0.6,actor_rollout_ref.rollout.tensor_model_parallel_size=1,actor_rollout_ref.rollout.top_k=20,actor_rollout_ref.rollout.top_p=0.95,actor_rollout_ref.rollout.val_kwargs.n=1,actor_rollout_ref.rollout.val_kwargs.temperature=0.6,actor_rollout_ref.rollout.val_kwargs.top_k=20,actor_rollout_ref.rollout.val_kwargs.top_p=0.95,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py,data.max_prompt_length=2048,data.max_response_length=30720,data.val_batch_size=512,data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet,ray_init.num_cpus=32,trainer.n_gpus_per_node=8
    id: ???
    num: ???
    config_name: eval_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1
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

- [exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/overrides.yaml](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/scratch/hydra/mixed_ep1/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- trainer.n_gpus_per_node=8
- data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
- data.val_batch_size=512
- data.max_prompt_length=2048
- data.max_response_length=30720
- actor_rollout_ref.rollout.mode=async
- actor_rollout_ref.rollout.tensor_model_parallel_size=1
- ++actor_rollout_ref.rollout.seed=42
- actor_rollout_ref.rollout.max_model_len=32768
- actor_rollout_ref.rollout.max_num_batched_tokens=32768
- actor_rollout_ref.rollout.max_num_seqs=32
- actor_rollout_ref.rollout.enable_chunked_prefill=true
- actor_rollout_ref.rollout.temperature=0.6
- actor_rollout_ref.rollout.top_p=0.95
- actor_rollout_ref.rollout.top_k=20
- actor_rollout_ref.rollout.val_kwargs.temperature=0.6
- actor_rollout_ref.rollout.val_kwargs.top_p=0.95
- actor_rollout_ref.rollout.val_kwargs.top_k=20
- actor_rollout_ref.rollout.val_kwargs.n=1
- actor_rollout_ref.rollout.agent.num_paths=2
- actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
- actor_rollout_ref.rollout.agent.max_path_response_length=8192
- actor_rollout_ref.rollout.agent.num_workers=8
- custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
- custom_reward_function.name=compute_score
- ray_init.num_cpus=32
- ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/mixed_ep1
- ++ray_init.object_store_memory=4294967296
- ++ray_init.plasma_directory=${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/config.yaml](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    temperature: 0.6
    top_k: 20
    top_p: 0.95
    prompt_length: ${oc.select:data.max_prompt_length,512}
    response_length: ${oc.select:data.max_response_length,512}
    dtype: bfloat16
    gpu_memory_utilization: 0.7
    ignore_eos: false
    enforce_eager: true
    free_cache_engine: true
    tensor_model_parallel_size: 1
    max_num_batched_tokens: 32768
    max_model_len: 32768
    max_num_seqs: 32
    log_prob_micro_batch_size: null
    log_prob_micro_batch_size_per_gpu: 1
    log_prob_use_dynamic_bsz: ${oc.select:actor_rollout_ref.actor.use_dynamic_bsz,false}
    log_prob_max_token_len_per_gpu: ${oc.select:actor_rollout_ref.actor.ppo_max_token_len_per_gpu,16384}
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
      top_k: 20
      top_p: 0.95
      temperature: 0.6
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
      max_iterations_for_parallel_thinking: 0
      num_paths: 2
      max_path_response_length: 8192
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
    seed: 42
  hybrid_engine: true
  model:
    path: ${oc.env:PARALLEL_R1_EVAL_MODEL}
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
  experiment_name: ${oc.env:PARALLEL_R1_EVAL_NAME}
  logger:
  - console
  log_val_generations: 0
  rollout_data_dir: null
  validation_data_dir: ${trainer.default_local_dir}
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
  default_local_dir: ${oc.env:PARALLEL_R1_OUTPUT_ROOT,checkpoints}/eval/${trainer.experiment_name}
  max_actor_ckpt_to_keep: null
  max_critic_ckpt_to_keep: null
  ray_wait_register_center_timeout: 300
  device: cuda
  use_legacy_worker_impl: auto
data:
  tokenizer: null
  use_shm: false
  train_files: ${data.val_files}
  val_files: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
  prompt_key: prompt
  reward_fn_key: data_source
  max_prompt_length: 2048
  max_response_length: 30720
  train_batch_size: 8
  val_batch_size: 512
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
  path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
  name: compute_score
algorithm:
  _target_: verl.trainer.config.AlgoConfig
  gamma: 1.0
  lam: 1.0
  adv_estimator: grpo
  norm_adv_by_std_in_grpo: true
  split_accuracy_aux: false
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
  temp_dir: ${TMPDIR}/math500sft-20261008/sft_messages_ep5
  object_store_memory: 4294967296
  plasma_directory: ${SHM_ROOT}

```

</details>

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/hydra.yaml](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${oc.env:PARALLEL_R1_SCRATCH_ROOT,checkpoints}/hydra/${trainer.experiment_name}
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
    - data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
    - data.val_batch_size=512
    - data.max_prompt_length=2048
    - data.max_response_length=30720
    - actor_rollout_ref.rollout.mode=async
    - actor_rollout_ref.rollout.tensor_model_parallel_size=1
    - ++actor_rollout_ref.rollout.seed=42
    - actor_rollout_ref.rollout.max_model_len=32768
    - actor_rollout_ref.rollout.max_num_batched_tokens=32768
    - actor_rollout_ref.rollout.max_num_seqs=32
    - actor_rollout_ref.rollout.enable_chunked_prefill=true
    - actor_rollout_ref.rollout.temperature=0.6
    - actor_rollout_ref.rollout.top_p=0.95
    - actor_rollout_ref.rollout.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.temperature=0.6
    - actor_rollout_ref.rollout.val_kwargs.top_p=0.95
    - actor_rollout_ref.rollout.val_kwargs.top_k=20
    - actor_rollout_ref.rollout.val_kwargs.n=1
    - actor_rollout_ref.rollout.agent.num_paths=2
    - actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
    - actor_rollout_ref.rollout.agent.max_path_response_length=8192
    - actor_rollout_ref.rollout.agent.num_workers=8
    - custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
    - custom_reward_function.name=compute_score
    - ray_init.num_cpus=32
    - ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/sft_messages_ep5
    - ++ray_init.object_store_memory=4294967296
    - ++ray_init.plasma_directory=${SHM_ROOT}
  job:
    name: main_ppo
    chdir: null
    override_dirname: ++actor_rollout_ref.rollout.seed=42,++ray_init.object_store_memory=4294967296,++ray_init.plasma_directory=${SHM_ROOT},++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/sft_messages_ep5,actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0,actor_rollout_ref.rollout.agent.max_path_response_length=8192,actor_rollout_ref.rollout.agent.num_paths=2,actor_rollout_ref.rollout.agent.num_workers=8,actor_rollout_ref.rollout.enable_chunked_prefill=true,actor_rollout_ref.rollout.max_model_len=32768,actor_rollout_ref.rollout.max_num_batched_tokens=32768,actor_rollout_ref.rollout.max_num_seqs=32,actor_rollout_ref.rollout.mode=async,actor_rollout_ref.rollout.temperature=0.6,actor_rollout_ref.rollout.tensor_model_parallel_size=1,actor_rollout_ref.rollout.top_k=20,actor_rollout_ref.rollout.top_p=0.95,actor_rollout_ref.rollout.val_kwargs.n=1,actor_rollout_ref.rollout.val_kwargs.temperature=0.6,actor_rollout_ref.rollout.val_kwargs.top_k=20,actor_rollout_ref.rollout.val_kwargs.top_p=0.95,custom_reward_function.name=compute_score,custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py,data.max_prompt_length=2048,data.max_response_length=30720,data.val_batch_size=512,data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet,ray_init.num_cpus=32,trainer.n_gpus_per_node=8
    id: ???
    num: ???
    config_name: eval_qwen3_06b
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
    cwd: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5
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

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/overrides.yaml](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/scratch/hydra/sft_messages_ep5/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- trainer.n_gpus_per_node=8
- data.val_files=${PROJECT_ROOT}/exps/math500-new-sft-20261008/math500.parquet
- data.val_batch_size=512
- data.max_prompt_length=2048
- data.max_response_length=30720
- actor_rollout_ref.rollout.mode=async
- actor_rollout_ref.rollout.tensor_model_parallel_size=1
- ++actor_rollout_ref.rollout.seed=42
- actor_rollout_ref.rollout.max_model_len=32768
- actor_rollout_ref.rollout.max_num_batched_tokens=32768
- actor_rollout_ref.rollout.max_num_seqs=32
- actor_rollout_ref.rollout.enable_chunked_prefill=true
- actor_rollout_ref.rollout.temperature=0.6
- actor_rollout_ref.rollout.top_p=0.95
- actor_rollout_ref.rollout.top_k=20
- actor_rollout_ref.rollout.val_kwargs.temperature=0.6
- actor_rollout_ref.rollout.val_kwargs.top_p=0.95
- actor_rollout_ref.rollout.val_kwargs.top_k=20
- actor_rollout_ref.rollout.val_kwargs.n=1
- actor_rollout_ref.rollout.agent.num_paths=2
- actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0
- actor_rollout_ref.rollout.agent.max_path_response_length=8192
- actor_rollout_ref.rollout.agent.num_workers=8
- custom_reward_function.path=${PROJECT_ROOT}/exps/math500-new-sft-20261008/reward_bridge.py
- custom_reward_function.name=compute_score
- ray_init.num_cpus=32
- ++ray_init.temp_dir=${TMPDIR}/math500sft-20261008/sft_messages_ep5
- ++ray_init.object_store_memory=4294967296
- ++ray_init.plasma_directory=${SHM_ROOT}

```

</details>

## Метрики и полнота результатов

- [exps/math500-new-sft-20261008/attempts/startup-import-01/status.json](../artifacts/exps/math500-new-sft-20261008/attempts/startup-import-01/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "started_at": "2026-10-08T18:42:11.956016+00:00",
  "jobs": [
    {
      "name": "gsm_infinite_ep5",
      "state": "running",
      "started_at": "2026-10-08T18:42:11.966420+00:00",
      "completed_runtime_records": 0,
      "updated_at": "2026-10-08T18:42:42.069870+00:00"
    },
    {
      "name": "sft_messages_ep5",
      "state": "pending"
    },
    {
      "name": "mixed_ep1",
      "state": "pending"
    }
  ],
  "error": "RuntimeError: gsm_infinite_ep5 failed: exit 1",
  "finished_at": "2026-10-08T18:42:52.076592+00:00"
}
```

</details>

- [exps/math500-new-sft-20261008/derived-statistics.json](../artifacts/exps/math500-new-sft-20261008/derived-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "paired_accuracy_comparisons": [
    {
      "a": "gsm_infinite_ep5",
      "b": "sft_messages_ep5",
      "delta_pp": 1.0,
      "paired_bootstrap_ci95_pp": [
        -2.6,
        4.604999999999928
      ],
      "a_only_correct": 47,
      "b_only_correct": 42
    },
    {
      "a": "gsm_infinite_ep5",
      "b": "mixed_ep1",
      "delta_pp": 4.6,
      "paired_bootstrap_ci95_pp": [
        0.8,
        8.6
      ],
      "a_only_correct": 63,
      "b_only_correct": 40
    },
    {
      "a": "sft_messages_ep5",
      "b": "mixed_ep1",
      "delta_pp": 3.5999999999999996,
      "paired_bootstrap_ci95_pp": [
        -0.4,
        7.3999999999999995
      ],
      "a_only_correct": 57,
      "b_only_correct": 39
    }
  ],
  "seed": 42,
  "bootstrap_replicates": 10000,
  "models": {
    "gsm_infinite_ep5": {
      "branch_token_share_weighted": 0.00300542574107683,
      "max_forks": 3,
      "strict_format_parallel_count": 51,
      "budget_reached_correct": 0,
      "total_generated_tokens": 2115840
    },
    "sft_messages_ep5": {
      "branch_token_share_weighted": 0.009810680106638964,
      "max_forks": 1,
      "strict_format_parallel_count": 15,
      "budget_reached_correct": 0,
      "total_generated_tokens": 1147423
    },
    "mixed_ep1": {
      "branch_token_share_weighted": 0.35778223919573715,
      "max_forks": 2,
      "strict_format_parallel_count": 347,
      "budget_reached_correct": 0,
      "total_generated_tokens": 264988
    }
  }
}
```

</details>

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/driver.log](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/summary.json](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
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
}
```

</details>

- [exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/trace-statistics.jsonl](../artifacts/exps/math500-new-sft-20261008/runs/gsm_infinite_ep5/trace-statistics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/runs/mixed_ep1/driver.log](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math500-new-sft-20261008/runs/mixed_ep1/summary.json](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
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
```

</details>

- [exps/math500-new-sft-20261008/runs/mixed_ep1/trace-statistics.jsonl](../artifacts/exps/math500-new-sft-20261008/runs/mixed_ep1/trace-statistics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/driver.log](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/summary.json](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
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
}
```

</details>

- [exps/math500-new-sft-20261008/runs/sft_messages_ep5/trace-statistics.jsonl](../artifacts/exps/math500-new-sft-20261008/runs/sft_messages_ep5/trace-statistics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/status-snapshot.json](../artifacts/exps/math500-new-sft-20261008/status-snapshot.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "started_at": "2026-10-08T20:00:15.839541+00:00",
  "jobs": [
    {
      "name": "gsm_infinite_ep5",
      "state": "running",
      "started_at": "2026-10-08T20:00:15.847646+00:00",
      "completed_runtime_records": 438,
      "updated_at": "2026-10-08T20:06:39.528387+00:00"
    },
    {
      "name": "sft_messages_ep5",
      "state": "pending"
    },
    {
      "name": "mixed_ep1",
      "state": "pending"
    }
  ]
}
```

</details>

- [exps/math500-new-sft-20261008/status.json](../artifacts/exps/math500-new-sft-20261008/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": "2026-10-08T20:00:15.839541+00:00",
  "jobs": [
    {
      "name": "gsm_infinite_ep5",
      "state": "complete",
      "started_at": "2026-10-08T20:00:15.847646+00:00",
      "completed_runtime_records": 504,
      "updated_at": "2026-10-08T20:15:17.283619+00:00",
      "generation_finished_at": "2026-10-08T20:15:27.293563+00:00",
      "finished_at": "2026-10-08T20:15:38.324454+00:00",
      "accuracy": 0.168,
      "parallel_ratio": 0.11
    },
    {
      "name": "sft_messages_ep5",
      "state": "complete",
      "started_at": "2026-10-08T20:15:38.333343+00:00",
      "completed_runtime_records": 504,
      "updated_at": "2026-10-08T20:29:59.664174+00:00",
      "generation_finished_at": "2026-10-08T20:30:09.700636+00:00",
      "finished_at": "2026-10-08T20:30:19.378651+00:00",
      "accuracy": 0.158,
      "parallel_ratio": 0.056
    },
    {
      "name": "mixed_ep1",
      "state": "complete",
      "started_at": "2026-10-08T20:30:19.388037+00:00",
      "completed_runtime_records": 504,
      "updated_at": "2026-10-08T20:44:39.427799+00:00",
      "generation_finished_at": "2026-10-08T20:44:49.435517+00:00",
      "finished_at": "2026-10-08T20:44:58.498612+00:00",
      "accuracy": 0.122,
      "parallel_ratio": 0.97
    }
  ],
  "finished_at": "2026-10-08T20:44:58.506699+00:00"
}
```

</details>

- [exps/math500-new-sft-20261008/summary.json](../artifacts/exps/math500-new-sft-20261008/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished_at": "2026-10-08T20:44:58.504252+00:00",
  "models": {
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

## Графики

- [exps/math500-new-sft-20261008/figures/accuracy_parallelism.pdf](../artifacts/exps/math500-new-sft-20261008/figures/accuracy_parallelism.pdf) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/figures/accuracy_parallelism.png](../artifacts/exps/math500-new-sft-20261008/figures/accuracy_parallelism.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/figures/trace_diagnostics.pdf](../artifacts/exps/math500-new-sft-20261008/figures/trace_diagnostics.pdf) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/figures/trace_diagnostics.png](../artifacts/exps/math500-new-sft-20261008/figures/trace_diagnostics.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_and.png](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_and.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_not.png](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_not.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_or.png](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_or.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_xor.png](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/tests/test_region_xor.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Исходники рецепта и награды

- [exps/math500-new-sft-20261008/prepare.py](../artifacts/exps/math500-new-sft-20261008/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/plot.py](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/plot.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/pygletplot/plot.py](../artifacts/exps/math500-new-sft-20261008/scorer-deps/sympy/plotting/pygletplot/plot.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
