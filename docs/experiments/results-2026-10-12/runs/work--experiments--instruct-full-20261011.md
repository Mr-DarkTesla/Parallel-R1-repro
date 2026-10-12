# work/experiments/instruct-full-20261011

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/manifest.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "guard_protocol": "native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094",
  "model_precision": "bf16",
  "scorer_think_tag_fix": true,
  "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/manifest.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/questions-24.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 24,
  "suite": "24",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "guard_protocol": "native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094",
  "model_precision": "bf16",
  "scorer_think_tag_fix": true,
  "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
  "generation_config_sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/manifest.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "guard_protocol": "native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094",
  "model_precision": "bf16",
  "scorer_think_tag_fix": true,
  "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/plot-manifest.json](../artifacts/work/experiments/instruct-full-20261011/reports/plot-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "sources": {
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/reports/matched128-distribution-data.json": "213130d664e7deb079fa13b7395314f7f3a21f38ae07ecf5c25c6c383203c940",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/matched-eval128-comparison.json": "7b537ff9841690a63acda5c846c63b42257bf3372ed25b03aa7f000b208eecd1"
  },
  "benchmark_selection": false,
  "F_semantics": "critical-path proxy, not instrumented physical model.forward",
  "width_semantics": "completed groups with path_calls>0 and summary_call; conditional denominator 4 vs 127"
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/rl-progress-plot-manifest.json](../artifacts/work/experiments/instruct-full-20261011/reports/rl-progress-plot-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "source_sha256": "21ff41af9da216a9dadf5d5ee76a5b5a1daac4b5e44dde4f93741433e4e84c5b",
  "steps": [
    0,
    4,
    8,
    16
  ],
  "validation_count": 32,
  "benchmark": false,
  "F_semantics": "actual instrumented model.forward calls"
}
```

</details>

- [work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 64
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/val.parquet
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
  max_length: 8192
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    name: InstructDataset
  use_shm: false
  num_workers: 0
  parallel_attention: true
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
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
  strategy: fsdp
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Instruct-4B-full-epoch1
  total_epochs: 1
  total_training_steps: 42
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
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final

```

</details>

- [work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    - data.custom_cls.name=InstructDataset
    - +data.defer_parallel_mask=true
    - data.max_length=8192
    - data.truncation=error
    - data.trim_padding=true
    - data.train_batch_size=64
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=0
    - model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
    - model.strategy=fsdp
    - model.lora_rank=0
    - model.enable_gradient_checkpointing=true
    - model.fsdp_config.model_dtype=fp32
    - optim.lr=1e-5
    - optim.warmup_steps_ratio=0.1
    - ulysses_sequence_parallel_size=1
    - use_remove_padding=false
    - trainer.total_epochs=1
    - trainer.total_training_steps=42
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final
    - trainer.experiment_name=Instruct-4B-full-epoch1
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=64,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.1,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1,trainer.experiment_name=Instruct-4B-full-epoch1,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=42,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/hydra
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

- [work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/epoch1/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
- data.custom_cls.name=InstructDataset
- +data.defer_parallel_mask=true
- data.max_length=8192
- data.truncation=error
- data.trim_padding=true
- data.train_batch_size=64
- data.micro_batch_size_per_gpu=1
- data.num_workers=0
- model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
- model.strategy=fsdp
- model.lora_rank=0
- model.enable_gradient_checkpointing=true
- model.fsdp_config.model_dtype=fp32
- optim.lr=1e-5
- optim.warmup_steps_ratio=0.1
- ulysses_sequence_parallel_size=1
- use_remove_padding=false
- trainer.total_epochs=1
- trainer.total_training_steps=42
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final
- trainer.experiment_name=Instruct-4B-full-epoch1
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
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
  max_length: 8192
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    name: InstructDataset
  use_shm: false
  num_workers: 0
  parallel_attention: true
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
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
  strategy: fsdp
optim:
  lr: 1.0e-05
  betas:
  - 0.9
  - 0.95
  weight_decay: 0.01
  warmup_steps_ratio: 0.0
  clip_grad: 1.0
  lr_scheduler: cosine
ulysses_sequence_parallel_size: 1
use_remove_padding: false
trainer:
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Instruct-4B-full-isolation
  total_epochs: 1
  total_training_steps: 2
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
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/final

```

</details>

- [work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    - data.custom_cls.name=InstructDataset
    - +data.defer_parallel_mask=true
    - data.max_length=8192
    - data.truncation=error
    - data.trim_padding=true
    - data.train_batch_size=8
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=0
    - model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
    - model.strategy=fsdp
    - model.lora_rank=0
    - model.enable_gradient_checkpointing=true
    - model.fsdp_config.model_dtype=fp32
    - optim.lr=1e-5
    - optim.warmup_steps_ratio=0.0
    - ulysses_sequence_parallel_size=1
    - use_remove_padding=false
    - trainer.total_epochs=1
    - trainer.total_training_steps=2
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/final
    - trainer.experiment_name=Instruct-4B-full-isolation
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.0,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation,trainer.experiment_name=Instruct-4B-full-isolation,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=2,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: verl.trainer.config
      schema: pkg
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/hydra
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

- [work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/isolation/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
- data.custom_cls.name=InstructDataset
- +data.defer_parallel_mask=true
- data.max_length=8192
- data.truncation=error
- data.trim_padding=true
- data.train_batch_size=8
- data.micro_batch_size_per_gpu=1
- data.num_workers=0
- model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
- model.strategy=fsdp
- model.lora_rank=0
- model.enable_gradient_checkpointing=true
- model.fsdp_config.model_dtype=fp32
- optim.lr=1e-5
- optim.warmup_steps_ratio=0.0
- ulysses_sequence_parallel_size=1
- use_remove_padding=false
- trainer.total_epochs=1
- trainer.total_training_steps=2
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/isolation/final
- trainer.experiment_name=Instruct-4B-full-isolation
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
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
  max_length: 8192
  trim_padding: true
  truncation: error
  balance_dp_token: false
  chat_template: null
  custom_cls:
    path: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    name: InstructDataset
  use_shm: false
  num_workers: 0
  parallel_attention: true
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
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
  strategy: fsdp
optim:
  lr: 1.0e-05
  betas:
  - 0.9
  - 0.95
  weight_decay: 0.01
  warmup_steps_ratio: 0.0
  clip_grad: 1.0
  lr_scheduler: cosine
ulysses_sequence_parallel_size: 1
use_remove_padding: false
trainer:
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Instruct-4B-full-smoke
  total_epochs: 1
  total_training_steps: 2
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
    load_contents: ${trainer.checkpoint.save_contents}
  device: cuda
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/final

```

</details>

- [work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
    - data.custom_cls.name=InstructDataset
    - +data.defer_parallel_mask=true
    - data.max_length=8192
    - data.truncation=error
    - data.trim_padding=true
    - data.train_batch_size=8
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=0
    - model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
    - model.strategy=fsdp
    - model.lora_rank=0
    - model.enable_gradient_checkpointing=true
    - model.fsdp_config.model_dtype=fp32
    - optim.lr=1e-5
    - optim.warmup_steps_ratio=0.0
    - ulysses_sequence_parallel_size=1
    - use_remove_padding=false
    - trainer.total_epochs=1
    - trainer.total_training_steps=2
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/final
    - trainer.experiment_name=Instruct-4B-full-smoke
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.0,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke,trainer.experiment_name=Instruct-4B-full-smoke,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=2,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/hydra
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

- [work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-full-20261011/runs/smoke/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/data/smoke-val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/dataset.py
- data.custom_cls.name=InstructDataset
- +data.defer_parallel_mask=true
- data.max_length=8192
- data.truncation=error
- data.trim_padding=true
- data.train_batch_size=8
- data.micro_batch_size_per_gpu=1
- data.num_workers=0
- model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
- model.strategy=fsdp
- model.lora_rank=0
- model.enable_gradient_checkpointing=true
- model.fsdp_config.model_dtype=fp32
- optim.lr=1e-5
- optim.warmup_steps_ratio=0.0
- ulysses_sequence_parallel_size=1
- use_remove_padding=false
- trainer.total_epochs=1
- trainer.total_training_steps=2
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/smoke/final
- trainer.experiment_name=Instruct-4B-full-smoke
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-full-20261011/system.txt](../artifacts/work/experiments/instruct-full-20261011/system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/summary.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 86,
  "pass_at_1_completed_only": 0.671875,
  "format_valid": 126,
  "format_fraction_completed_only": 0.984375,
  "executed_fork_samples": 125,
  "unfinished_thinking": 1,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 124,
  "parallel_protocol_fraction_completed_only": 0.96875,
  "gate_passed": true,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 126,
  "legacy_format_fraction_completed_only": 0.984375,
  "legacy_parallel_protocol_valid": 124,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": true,
    "fork_coverage_at_least_0_2": true,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": true,
    "invalid_width_fraction_at_most_0_05": true,
    "at_least_one_correct": true
  },
  "gate_thresholds": {
    "basic_strict_format": 0.8,
    "fork_coverage": 0.2,
    "valid_parallel_among_executed_forks": 0.9,
    "max_invalid_width": 0.05,
    "min_correct": 1
  },
  "gate_raw_counts": {
    "completed": 128,
    "basic_valid": 126,
    "executed_fork_samples": 125,
    "valid_parallel_among_fork_samples": 124,
    "invalid_width_samples": 0,
    "correct": 86
  },
  "fork_coverage": 0.9765625,
  "valid_parallel_among_executed_forks": 0.992,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 85,
  "correct_and_parallel_valid": 83,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 72837.0,
      "mean": 569.0390625,
      "median": 449.0,
      "p95": 1325.2499999999989,
      "min": 215.0,
      "max": 3820.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 92483.0,
      "mean": 722.5234375,
      "median": 559.0,
      "p95": 1803.5499999999993,
      "min": 215.0,
      "max": 4076.0
    },
    "T_forced": {
      "n": 128,
      "sum": 1455.0,
      "mean": 11.3671875,
      "median": 12.0,
      "p95": 15.0,
      "min": 0.0,
      "max": 24.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 93938.0,
      "mean": 733.890625,
      "median": 569.5,
      "p95": 1817.4999999999993,
      "min": 215.0,
      "max": 4094.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 92483.0,
      "mean": 722.5234375,
      "median": 559.0,
      "p95": 1803.5499999999993,
      "min": 215.0,
      "max": 4076.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 994.0,
      "mean": 7.765625,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 3490.0140607357025,
      "mean": 27.265734849497676,
      "median": 21.293344616889954,
      "p95": 67.7867847919464,
      "min": 8.25828218460083,
      "max": 154.7655909061432
    },
    "forks": {
      "n": 128,
      "sum": 127.0,
      "mean": 0.9921875,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 128,
      "sum": 127.0,
      "mean": 0.9921875,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 255.0,
      "mean": 1.9921875,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 92483.0,
      "mean": 722.5234375,
      "median": 559.0,
      "p95": 1803.5499999999993,
      "min": 215.0,
      "max": 4076.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 994.0,
      "mean": 7.765625,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 91489.0,
      "mean": 714.7578125,
      "median": 551.5,
      "p95": 1794.8999999999992,
      "min": 213.0,
      "max": 4067.0
    },
    "widths": {
      "n": 127,
      "sum": 358.0,
      "mean": 2.8188976377952755,
      "median": 3.0,
      "p95": 4.0,
      "min": 2.0,
      "max": 6.0
    },
    "width_histogram": {
      "2": 58,
      "3": 37,
      "4": 30,
      "5": 1,
      "6": 1
    },
    "truncated_samples": 1,
    "truncated_fraction": 0.0078125,
    "invalid_width_samples": 0,
    "forked_samples": 125
  },
  "metrics_correct": {
    "F": {
      "n": 86,
      "sum": 39720.0,
      "mean": 461.86046511627904,
      "median": 422.0,
      "p95": 757.0,
      "min": 215.0,
      "max": 1595.0
    },
    "T_sampled": {
      "n": 86,
      "sum": 49181.0,
      "mean": 571.8720930232558,
      "median": 535.5,
      "p95": 993.25,
      "min": 215.0,
      "max": 1836.0
    },
    "T_forced": {
      "n": 86,
      "sum": 954.0,
      "mean": 11.093023255813954,
      "median": 12.0,
      "p95": 15.0,
      "min": 0.0,
      "max": 24.0
    },
    "T_assembled": {
      "n": 86,
      "sum": 50135.0,
      "mean": 582.9651162790698,
      "median": 547.5,
      "p95": 1007.5,
      "min": 215.0,
      "max": 1851.0
    },
    "actual_generated_tokens": {
      "n": 86,
      "sum": 49181.0,
      "mean": 571.8720930232558,
      "median": 535.5,
      "p95": 993.25,
      "min": 215.0,
      "max": 1836.0
    },
    "generation_calls": {
      "n": 86,
      "sum": 660.0,
      "mean": 7.674418604651163,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "wall_seconds": {
      "n": 86,
      "sum": 1859.3527688980103,
      "mean": 21.620381033697793,
      "median": 19.879701495170593,
      "p95": 38.49344223737717,
      "min": 8.25828218460083,
      "max": 68.02036190032959
    },
    "forks": {
      "n": 86,
      "sum": 85.0,
      "mean": 0.9883720930232558,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 86,
      "sum": 85.0,
      "mean": 0.9883720930232558,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 86,
      "sum": 171.0,
      "mean": 1.9883720930232558,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 86,
      "sum": 49181.0,
      "mean": 571.8720930232558,
      "median": 535.5,
      "p95": 993.25,
      "min": 215.0,
      "max": 1836.0
    },
    "prefill_calls_inferred": {
      "n": 86,
      "sum": 660.0,
      "mean": 7.674418604651163,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "decode_calls_inferred": {
      "n": 86,
      "sum": 48521.0,
      "mean": 564.1976744186046,
      "median": 527.5,
      "p95": 984.5,
      "min": 213.0,
      "max": 1827.0
    },
    "widths": {
      "n": 85,
      "sum": 233.0,
      "mean": 2.7411764705882353,
      "median": 3.0,
      "p95": 4.0,
      "min": 2.0,
      "max": 6.0
    },
    "width_histogram": {
      "2": 41,
      "3": 27,
      "4": 16,
      "6": 1
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 0,
    "forked_samples": 83
  },
  "historical_correct": 86,
  "historical_pass_at_1_completed_only": 0.671875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 128,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 47,
      "pass_at_1": 0.734375,
      "basic_valid": 63,
      "basic_valid_fraction": 0.984375,
      "parallel_valid": 61,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 47,
      "correct_and_parallel_valid": 45,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 32148.0,
          "mean": 502.3125,
          "median": 423.5,
          "p95": 757.4,
          "min": 215.0,
          "max": 3820.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 38351.0,
          "mean": 599.234375,
          "median": 484.0,
          "p95": 997.9499999999997,
          "min": 215.0,
          "max": 4076.0
        },
        "T_forced": {
          "n": 64,
          "sum": 708.0,
          "mean": 11.0625,
          "median": 9.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 24.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 39059.0,
          "mean": 610.296875,
          "median": 494.5,
          "p95": 1012.4999999999998,
          "min": 215.0,
          "max": 4094.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 38351.0,
          "mean": 599.234375,
          "median": 484.0,
          "p95": 997.9499999999997,
          "min": 215.0,
          "max": 4076.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 491.0,
          "mean": 7.671875,
          "median": 7.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 14.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 1465.3354132175446,
          "mean": 22.895865831524134,
          "median": 18.332512259483337,
          "p95": 38.741939079761494,
          "min": 8.25828218460083,
          "max": 154.7655909061432
        },
        "forks": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "rounds": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 128.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 38351.0,
          "mean": 599.234375,
          "median": 484.0,
          "p95": 997.9499999999997,
          "min": 215.0,
          "max": 4076.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 491.0,
          "mean": 7.671875,
          "median": 7.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 14.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 37860.0,
          "mean": 591.5625,
          "median": 476.5,
          "p95": 989.0999999999997,
          "min": 213.0,
          "max": 4067.0
        },
        "widths": {
          "n": 64,
          "sum": 172.0,
          "mean": 2.6875,
          "median": 2.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 5.0
        },
        "width_histogram": {
          "2": 34,
          "3": 17,
          "4": 12,
          "5": 1
        },
        "truncated_samples": 1,
        "truncated_fraction": 0.015625,
        "invalid_width_samples": 0,
        "forked_samples": 62
      },
      "metrics_correct": {
        "F": {
          "n": 47,
          "sum": 21242.0,
          "mean": 451.9574468085106,
          "median": 384.0,
          "p95": 756.8,
          "min": 215.0,
          "max": 1595.0
        },
        "T_sampled": {
          "n": 47,
          "sum": 25713.0,
          "mean": 547.0851063829788,
          "median": 473.0,
          "p95": 990.8999999999997,
          "min": 215.0,
          "max": 1836.0
        },
        "T_forced": {
          "n": 47,
          "sum": 519.0,
          "mean": 11.042553191489361,
          "median": 9.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 24.0
        },
        "T_assembled": {
          "n": 47,
          "sum": 26232.0,
          "mean": 558.1276595744681,
          "median": 482.0,
          "p95": 1004.9999999999998,
          "min": 215.0,
          "max": 1851.0
        },
        "actual_generated_tokens": {
          "n": 47,
          "sum": 25713.0,
          "mean": 547.0851063829788,
          "median": 473.0,
          "p95": 990.8999999999997,
          "min": 215.0,
          "max": 1836.0
        },
        "generation_calls": {
          "n": 47,
          "sum": 361.0,
          "mean": 7.680851063829787,
          "median": 7.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 14.0
        },
        "wall_seconds": {
          "n": 47,
          "sum": 980.7117900848389,
          "mean": 20.86620829967742,
          "median": 17.607953786849976,
          "p95": 38.36919381618499,
          "min": 8.25828218460083,
          "max": 68.02036190032959
        },
        "forks": {
          "n": 47,
          "sum": 47.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "rounds": {
          "n": 47,
          "sum": 47.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 47,
          "sum": 94.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 47,
          "sum": 25713.0,
          "mean": 547.0851063829788,
          "median": 473.0,
          "p95": 990.8999999999997,
          "min": 215.0,
          "max": 1836.0
        },
        "prefill_calls_inferred": {
          "n": 47,
          "sum": 361.0,
          "mean": 7.680851063829787,
          "median": 7.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 14.0
        },
        "decode_calls_inferred": {
          "n": 47,
          "sum": 25352.0,
          "mean": 539.4042553191489,
          "median": 466.0,
          "p95": 982.1999999999998,
          "min": 213.0,
          "max": 1827.0
        },
        "widths": {
          "n": 47,
          "sum": 126.0,
          "mean": 2.6808510638297873,
          "median": 2.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 24,
          "3": 14,
          "4": 9
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 45
      },
      "historical_correct": 47,
      "historical_pass_at_1": 0.734375
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 39,
      "pass_at_1": 0.609375,
      "basic_valid": 63,
      "basic_valid_fraction": 0.984375,
      "parallel_valid": 63,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 38,
      "correct_and_parallel_valid": 38,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 40689.0,
          "mean": 635.765625,
          "median": 507.0,
          "p95": 1373.25,
          "min": 239.0,
          "max": 2561.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 54132.0,
          "mean": 845.8125,
          "median": 673.5,
          "p95": 1976.799999999999,
          "min": 305.0,
          "max": 3753.0
        },
        "T_forced": {
          "n": 64,
          "sum": 747.0,
          "mean": 11.671875,
          "median": 12.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 21.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 54879.0,
          "mean": 857.484375,
          "median": 685.5,
          "p95": 1991.799999999999,
          "min": 314.0,
          "max": 3768.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 54132.0,
          "mean": 845.8125,
          "median": 673.5,
          "p95": 1976.799999999999,
          "min": 305.0,
          "max": 3753.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 503.0,
          "mean": 7.859375,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 2024.678647518158,
          "mean": 31.635603867471218,
          "median": 24.876929998397827,
          "p95": 76.05115505456921,
          "min": 11.4881911277771,
          "max": 133.68628191947937
        },
        "forks": {
          "n": 64,
          "sum": 63.0,
          "mean": 0.984375,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 63.0,
          "mean": 0.984375,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 127.0,
          "mean": 1.984375,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 54132.0,
          "mean": 845.8125,
          "median": 673.5,
          "p95": 1976.799999999999,
          "min": 305.0,
          "max": 3753.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 503.0,
          "mean": 7.859375,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 53629.0,
          "mean": 837.953125,
          "median": 665.5,
          "p95": 1967.799999999999,
          "min": 298.0,
          "max": 3744.0
        },
        "widths": {
          "n": 63,
          "sum": 186.0,
          "mean": 2.9523809523809526,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 6.0
        },
        "width_histogram": {
          "2": 24,
          "3": 20,
          "4": 18,
          "6": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 63
      },
      "metrics_correct": {
        "F": {
          "n": 39,
          "sum": 18478.0,
          "mean": 473.79487179487177,
          "median": 428.0,
          "p95": 748.6000000000004,
          "min": 239.0,
          "max": 1024.0
        },
        "T_sampled": {
          "n": 39,
          "sum": 23468.0,
          "mean": 601.7435897435897,
          "median": 561.0,
          "p95": 960.7000000000004,
          "min": 305.0,
          "max": 1198.0
        },
        "T_forced": {
          "n": 39,
          "sum": 435.0,
          "mean": 11.153846153846153,
          "median": 12.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 21.0
        },
        "T_assembled": {
          "n": 39,
          "sum": 23903.0,
          "mean": 612.8974358974359,
          "median": 573.0,
          "p95": 970.0000000000003,
          "min": 314.0,
          "max": 1207.0
        },
        "actual_generated_tokens": {
          "n": 39,
          "sum": 23468.0,
          "mean": 601.7435897435897,
          "median": 561.0,
          "p95": 960.7000000000004,
          "min": 305.0,
          "max": 1198.0
        },
        "generation_calls": {
          "n": 39,
          "sum": 299.0,
          "mean": 7.666666666666667,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 39,
          "sum": 878.6409788131714,
          "mean": 22.529255867004395,
          "median": 21.2803795337677,
          "p95": 35.3300931453705,
          "min": 11.4881911277771,
          "max": 46.372793197631836
        },
        "forks": {
          "n": 39,
          "sum": 38.0,
          "mean": 0.9743589743589743,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 39,
          "sum": 38.0,
          "mean": 0.9743589743589743,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 39,
          "sum": 77.0,
          "mean": 1.9743589743589745,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 39,
          "sum": 23468.0,
          "mean": 601.7435897435897,
          "median": 561.0,
          "p95": 960.7000000000004,
          "min": 305.0,
          "max": 1198.0
        },
        "prefill_calls_inferred": {
          "n": 39,
          "sum": 299.0,
          "mean": 7.666666666666667,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 39,
          "sum": 23169.0,
          "mean": 594.0769230769231,
          "median": 553.0,
          "p95": 953.6000000000004,
          "min": 298.0,
          "max": 1191.0
        },
        "widths": {
          "n": 38,
          "sum": 107.0,
          "mean": 2.8157894736842106,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 6.0
        },
        "width_histogram": {
          "2": 17,
          "3": 13,
          "4": 7,
          "6": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 38
      },
      "historical_correct": 39,
      "historical_pass_at_1": 0.609375
    }
  },
  "cost_definitions": {
    "model_forward_calls_inferred": "INFERRED, not measured: serial HF structured_generate runs one initial model forward and one for each additional sampled output, hence sum raw generated_ids lengths across ALL calls. Native unavailable.",
    "prefill_calls_inferred": "INFERRED, not measured: one initial HF prefill per positive-output generation call. Native unavailable.",
    "decode_calls_inferred": "INFERRED, not measured: all raw generated tokens minus positive-output generation calls; no speculation in this backend. Native unavailable.",
    "rounds": "Executed parallel fork rounds; native=0",
    "generation_turns": "Parallel rounds+1; native=1",
    "F": "Logical critical sequential sampled-token depth; native F=sampled length. Not measured GPU model-forward invocations.",
    "T_sampled": "Retained sampled response tokens",
    "T_forced": "Forced response tokens including think prefix/protocol bridges",
    "T_assembled": "Total assembled response tokens",
    "actual_generated_tokens": "All generated token outputs across actual generation calls, including discarded outputs if any",
    "wall_seconds": "Per-question generation elapsed, excludes engine startup; backend confounded",
    "backend_confound": "Structured uses HF structured serial backend through vLLM worker RPC; native uses fast vLLM generation. Wall comparisons are descriptive and cannot establish parallel execution speedup."
  },
  "backend_labels": [
    "hf_structured_serial_backend"
  ],
  "matching_protocol": {
    "prompt_policy": "Custom system-file supplied verbatim before native chat-template rendering; see system_file and hash",
    "question_seed": "42+sample_index",
    "response_budget": 4096,
    "path_budget": 2048,
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20
  },
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "provenance": {
    "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ]
}
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/worker-exits.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/summary.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 24,
  "completed": 24,
  "missing": 0,
  "correct": 18,
  "pass_at_1_completed_only": 0.75,
  "format_valid": 24,
  "format_fraction_completed_only": 1.0,
  "executed_fork_samples": 23,
  "unfinished_thinking": 0,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 23,
  "parallel_protocol_fraction_completed_only": 0.9583333333333334,
  "gate_passed": true,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "parallel_syntax_valid": 24,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 24,
  "legacy_format_fraction_completed_only": 1.0,
  "legacy_parallel_protocol_valid": 23,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": true,
    "fork_coverage_at_least_0_2": true,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": true,
    "invalid_width_fraction_at_most_0_05": true,
    "at_least_one_correct": true
  },
  "gate_thresholds": {
    "basic_strict_format": 0.8,
    "fork_coverage": 0.2,
    "valid_parallel_among_executed_forks": 0.9,
    "max_invalid_width": 0.05,
    "min_correct": 1
  },
  "gate_raw_counts": {
    "completed": 24,
    "basic_valid": 24,
    "executed_fork_samples": 23,
    "valid_parallel_among_fork_samples": 23,
    "invalid_width_samples": 0,
    "correct": 18
  },
  "fork_coverage": 0.9583333333333334,
  "valid_parallel_among_executed_forks": 1.0,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 18,
  "correct_and_parallel_valid": 17,
  "metrics_all": {
    "F": {
      "n": 24,
      "sum": 11549.0,
      "mean": 481.2083333333333,
      "median": 443.5,
      "p95": 805.4499999999999,
      "min": 263.0,
      "max": 1244.0
    },
    "T_sampled": {
      "n": 24,
      "sum": 15040.0,
      "mean": 626.6666666666666,
      "median": 536.5,
      "p95": 1185.2499999999998,
      "min": 369.0,
      "max": 1934.0
    },
    "T_forced": {
      "n": 24,
      "sum": 285.0,
      "mean": 11.875,
      "median": 12.0,
      "p95": 15.0,
      "min": 0.0,
      "max": 24.0
    },
    "T_assembled": {
      "n": 24,
      "sum": 15325.0,
      "mean": 638.5416666666666,
      "median": 545.5,
      "p95": 1199.7999999999997,
      "min": 381.0,
      "max": 1949.0
    },
    "actual_generated_tokens": {
      "n": 24,
      "sum": 15040.0,
      "mean": 626.6666666666666,
      "median": 536.5,
      "p95": 1185.2499999999998,
      "min": 369.0,
      "max": 1934.0
    },
    "generation_calls": {
      "n": 24,
      "sum": 191.0,
      "mean": 7.958333333333333,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "wall_seconds": {
      "n": 24,
      "sum": 581.1651086807251,
      "mean": 24.21521286169688,
      "median": 21.09261119365692,
      "p95": 44.26220347881316,
      "min": 14.408092498779297,
      "max": 67.78043031692505
    },
    "forks": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 24,
      "sum": 48.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 24,
      "sum": 15040.0,
      "mean": 626.6666666666666,
      "median": 536.5,
      "p95": 1185.2499999999998,
      "min": 369.0,
      "max": 1934.0
    },
    "prefill_calls_inferred": {
      "n": 24,
      "sum": 191.0,
      "mean": 7.958333333333333,
      "median": 8.0,
      "p95": 9.0,
      "min": 2.0,
      "max": 14.0
    },
    "decode_calls_inferred": {
      "n": 24,
      "sum": 14849.0,
      "mean": 618.7083333333334,
      "median": 529.5,
      "p95": 1176.3999999999999,
      "min": 361.0,
      "max": 1925.0
    },
    "widths": {
      "n": 24,
      "sum": 71.0,
      "mean": 2.9583333333333335,
      "median": 3.0,
      "p95": 4.0,
      "min": 2.0,
      "max": 4.0
    },
    "width_histogram": {
      "2": 8,
      "3": 9,
      "4": 7
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 0,
    "forked_samples": 23
  },
  "metrics_correct": {
    "F": {
      "n": 18,
      "sum": 7862.0,
      "mean": 436.77777777777777,
      "median": 400.0,
      "p95": 672.4499999999998,
      "min": 263.0,
      "max": 811.0
    },
    "T_sampled": {
      "n": 18,
      "sum": 9883.0,
      "mean": 549.0555555555555,
      "median": 513.0,
      "p95": 825.2999999999994,
      "min": 372.0,
      "max": 1201.0
    },
    "T_forced": {
      "n": 18,
      "sum": 207.0,
      "mean": 11.5,
      "median": 12.0,
      "p95": 16.349999999999987,
      "min": 0.0,
      "max": 24.0
    },
    "T_assembled": {
      "n": 18,
      "sum": 10090.0,
      "mean": 560.5555555555555,
      "median": 523.5,
      "p95": 837.7499999999993,
      "min": 383.0,
      "max": 1216.0
    },
    "actual_generated_tokens": {
      "n": 18,
      "sum": 9883.0,
      "mean": 549.0555555555555,
      "median": 513.0,
      "p95": 825.2999999999994,
      "min": 372.0,
      "max": 1201.0
    },
    "generation_calls": {
      "n": 18,
      "sum": 141.0,
      "mean": 7.833333333333333,
      "median": 8.0,
      "p95": 9.749999999999993,
      "min": 2.0,
      "max": 14.0
    },
    "wall_seconds": {
      "n": 18,
      "sum": 384.50037479400635,
      "mean": 21.36113193300035,
      "median": 19.44746994972229,
      "p95": 32.55591893196104,
      "min": 14.408092498779297,
      "max": 44.877455949783325
    },
    "forks": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.1499999999999986,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.1499999999999986,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 18,
      "sum": 36.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.1499999999999986,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 18,
      "sum": 9883.0,
      "mean": 549.0555555555555,
      "median": 513.0,
      "p95": 825.2999999999994,
      "min": 372.0,
      "max": 1201.0
    },
    "prefill_calls_inferred": {
      "n": 18,
      "sum": 141.0,
      "mean": 7.833333333333333,
      "median": 8.0,
      "p95": 9.749999999999993,
      "min": 2.0,
      "max": 14.0
    },
    "decode_calls_inferred": {
      "n": 18,
      "sum": 9742.0,
      "mean": 541.2222222222222,
      "median": 505.5,
      "p95": 817.1499999999994,
      "min": 364.0,
      "max": 1192.0
    },
    "widths": {
      "n": 18,
      "sum": 51.0,
      "mean": 2.8333333333333335,
      "median": 3.0,
      "p95": 4.0,
      "min": 2.0,
      "max": 4.0
    },
    "width_histogram": {
      "2": 7,
      "3": 7,
      "4": 4
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 0,
    "forked_samples": 17
  },
  "historical_correct": 18,
  "historical_pass_at_1_completed_only": 0.75,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 24,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 12,
      "completed": 12,
      "correct": 8,
      "pass_at_1": 0.6666666666666666,
      "basic_valid": 12,
      "basic_valid_fraction": 1.0,
      "parallel_valid": 12,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 8,
      "correct_and_parallel_valid": 8,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 4877.0,
          "mean": 406.4166666666667,
          "median": 347.5,
          "p95": 629.3,
          "min": 276.0,
          "max": 648.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 5980.0,
          "mean": 498.3333333333333,
          "median": 425.0,
          "p95": 780.3499999999999,
          "min": 369.0,
          "max": 826.0
        },
        "T_forced": {
          "n": 12,
          "sum": 153.0,
          "mean": 12.75,
          "median": 12.0,
          "p95": 19.049999999999994,
          "min": 9.0,
          "max": 24.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 6133.0,
          "mean": 511.0833333333333,
          "median": 438.5,
          "p95": 793.6999999999999,
          "min": 381.0,
          "max": 841.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 5980.0,
          "mean": 498.3333333333333,
          "median": 425.0,
          "p95": 780.3499999999999,
          "min": 369.0,
          "max": 826.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 101.0,
          "mean": 8.416666666666666,
          "median": 8.0,
          "p95": 11.249999999999996,
          "min": 7.0,
          "max": 14.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 242.8354263305664,
          "mean": 20.2362855275472,
          "median": 17.060492873191833,
          "p95": 31.165247094631194,
          "min": 14.408092498779297,
          "max": 32.86839246749878
        },
        "forks": {
          "n": 12,
          "sum": 13.0,
          "mean": 1.0833333333333333,
          "median": 1.0,
          "p95": 1.4499999999999993,
          "min": 1.0,
          "max": 2.0
        },
        "rounds": {
          "n": 12,
          "sum": 13.0,
          "mean": 1.0833333333333333,
          "median": 1.0,
          "p95": 1.4499999999999993,
          "min": 1.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 25.0,
          "mean": 2.0833333333333335,
          "median": 2.0,
          "p95": 2.4499999999999993,
          "min": 2.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 5980.0,
          "mean": 498.3333333333333,
          "median": 425.0,
          "p95": 780.3499999999999,
          "min": 369.0,
          "max": 826.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 101.0,
          "mean": 8.416666666666666,
          "median": 8.0,
          "p95": 11.249999999999996,
          "min": 7.0,
          "max": 14.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 5879.0,
          "mean": 489.9166666666667,
          "median": 416.5,
          "p95": 771.9,
          "min": 361.0,
          "max": 817.0
        },
        "widths": {
          "n": 13,
          "sum": 38.0,
          "mean": 2.923076923076923,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 5,
          "3": 4,
          "4": 4
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 12
      },
      "metrics_correct": {
        "F": {
          "n": 8,
          "sum": 3208.0,
          "mean": 401.0,
          "median": 347.5,
          "p95": 592.6999999999999,
          "min": 292.0,
          "max": 648.0
        },
        "T_sampled": {
          "n": 8,
          "sum": 3853.0,
          "mean": 481.625,
          "median": 421.0,
          "p95": 693.6499999999999,
          "min": 372.0,
          "max": 743.0
        },
        "T_forced": {
          "n": 8,
          "sum": 102.0,
          "mean": 12.75,
          "median": 12.0,
          "p95": 20.849999999999994,
          "min": 9.0,
          "max": 24.0
        },
        "T_assembled": {
          "n": 8,
          "sum": 3955.0,
          "mean": 494.375,
          "median": 431.5,
          "p95": 709.8499999999999,
          "min": 383.0,
          "max": 755.0
        },
        "actual_generated_tokens": {
          "n": 8,
          "sum": 3853.0,
          "mean": 481.625,
          "median": 421.0,
          "p95": 693.6499999999999,
          "min": 372.0,
          "max": 743.0
        },
        "generation_calls": {
          "n": 8,
          "sum": 68.0,
          "mean": 8.5,
          "median": 8.0,
          "p95": 12.249999999999996,
          "min": 7.0,
          "max": 14.0
        },
        "wall_seconds": {
          "n": 8,
          "sum": 154.726895570755,
          "mean": 19.340861946344376,
          "median": 16.444857001304626,
          "p95": 28.179733753204342,
          "min": 14.408092498779297,
          "max": 29.771764516830444
        },
        "forks": {
          "n": 8,
          "sum": 9.0,
          "mean": 1.125,
          "median": 1.0,
          "p95": 1.6499999999999995,
          "min": 1.0,
          "max": 2.0
        },
        "rounds": {
          "n": 8,
          "sum": 9.0,
          "mean": 1.125,
          "median": 1.0,
          "p95": 1.6499999999999995,
          "min": 1.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 8,
          "sum": 17.0,
          "mean": 2.125,
          "median": 2.0,
          "p95": 2.6499999999999995,
          "min": 2.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 8,
          "sum": 3853.0,
          "mean": 481.625,
          "median": 421.0,
          "p95": 693.6499999999999,
          "min": 372.0,
          "max": 743.0
        },
        "prefill_calls_inferred": {
          "n": 8,
          "sum": 68.0,
          "mean": 8.5,
          "median": 8.0,
          "p95": 12.249999999999996,
          "min": 7.0,
          "max": 14.0
        },
        "decode_calls_inferred": {
          "n": 8,
          "sum": 3785.0,
          "mean": 473.125,
          "median": 413.5,
          "p95": 683.55,
          "min": 364.0,
          "max": 735.0
        },
        "widths": {
          "n": 9,
          "sum": 25.0,
          "mean": 2.7777777777777777,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 4,
          "3": 3,
          "4": 2
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 8
      },
      "historical_correct": 8,
      "historical_pass_at_1": 0.6666666666666666
    },
    "math": {
      "planned": 12,
      "completed": 12,
      "correct": 10,
      "pass_at_1": 0.8333333333333334,
      "basic_valid": 12,
      "basic_valid_fraction": 1.0,
      "parallel_valid": 11,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 10,
      "correct_and_parallel_valid": 9,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 6672.0,
          "mean": 556.0,
          "median": 494.0,
          "p95": 1005.8499999999997,
          "min": 263.0,
          "max": 1244.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 9060.0,
          "mean": 755.0,
          "median": 592.0,
          "p95": 1530.8499999999995,
          "min": 403.0,
          "max": 1934.0
        },
        "T_forced": {
          "n": 12,
          "sum": 132.0,
          "mean": 11.0,
          "median": 12.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 15.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 9192.0,
          "mean": 766.0,
          "median": 602.5,
          "p95": 1545.8499999999995,
          "min": 415.0,
          "max": 1949.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 9060.0,
          "mean": 755.0,
          "median": 592.0,
          "p95": 1530.8499999999995,
          "min": 403.0,
          "max": 1934.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 90.0,
          "mean": 7.5,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 9.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 338.3296823501587,
          "mean": 28.194140195846558,
          "median": 22.680529952049255,
          "p95": 55.18379441499708,
          "min": 15.159160614013672,
          "max": 67.78043031692505
        },
        "forks": {
          "n": 12,
          "sum": 11.0,
          "mean": 0.9166666666666666,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 12,
          "sum": 11.0,
          "mean": 0.9166666666666666,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 23.0,
          "mean": 1.9166666666666667,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 9060.0,
          "mean": 755.0,
          "median": 592.0,
          "p95": 1530.8499999999995,
          "min": 403.0,
          "max": 1934.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 90.0,
          "mean": 7.5,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 9.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 8970.0,
          "mean": 747.5,
          "median": 584.5,
          "p95": 1521.8499999999995,
          "min": 395.0,
          "max": 1925.0
        },
        "widths": {
          "n": 11,
          "sum": 33.0,
          "mean": 3.0,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 3,
          "3": 5,
          "4": 3
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 11
      },
      "metrics_correct": {
        "F": {
          "n": 10,
          "sum": 4654.0,
          "mean": 465.4,
          "median": 460.5,
          "p95": 709.2999999999997,
          "min": 263.0,
          "max": 811.0
        },
        "T_sampled": {
          "n": 10,
          "sum": 6030.0,
          "mean": 603.0,
          "median": 561.0,
          "p95": 1002.0999999999996,
          "min": 403.0,
          "max": 1201.0
        },
        "T_forced": {
          "n": 10,
          "sum": 105.0,
          "mean": 10.5,
          "median": 12.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 15.0
        },
        "T_assembled": {
          "n": 10,
          "sum": 6135.0,
          "mean": 613.5,
          "median": 573.0,
          "p95": 1015.7499999999995,
          "min": 415.0,
          "max": 1216.0
        },
        "actual_generated_tokens": {
          "n": 10,
          "sum": 6030.0,
          "mean": 603.0,
          "median": 561.0,
          "p95": 1002.0999999999996,
          "min": 403.0,
          "max": 1201.0
        },
        "generation_calls": {
          "n": 10,
          "sum": 73.0,
          "mean": 7.3,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 9.0
        },
        "wall_seconds": {
          "n": 10,
          "sum": 229.77347922325134,
          "mean": 22.977347922325134,
          "median": 21.24863874912262,
          "p95": 38.35428929328917,
          "min": 15.159160614013672,
          "max": 44.877455949783325
        },
        "forks": {
          "n": 10,
          "sum": 9.0,
          "mean": 0.9,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 10,
          "sum": 9.0,
          "mean": 0.9,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 10,
          "sum": 19.0,
          "mean": 1.9,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 10,
          "sum": 6030.0,
          "mean": 603.0,
          "median": 561.0,
          "p95": 1002.0999999999996,
          "min": 403.0,
          "max": 1201.0
        },
        "prefill_calls_inferred": {
          "n": 10,
          "sum": 73.0,
          "mean": 7.3,
          "median": 8.0,
          "p95": 9.0,
          "min": 2.0,
          "max": 9.0
        },
        "decode_calls_inferred": {
          "n": 10,
          "sum": 5957.0,
          "mean": 595.7,
          "median": 553.0,
          "p95": 993.5499999999995,
          "min": 395.0,
          "max": 1192.0
        },
        "widths": {
          "n": 9,
          "sum": 26.0,
          "mean": 2.888888888888889,
          "median": 3.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 3,
          "3": 4,
          "4": 2
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 9
      },
      "historical_correct": 10,
      "historical_pass_at_1": 0.8333333333333334
    }
  },
  "cost_definitions": {
    "model_forward_calls_inferred": "INFERRED, not measured: serial HF structured_generate runs one initial model forward and one for each additional sampled output, hence sum raw generated_ids lengths across ALL calls. Native unavailable.",
    "prefill_calls_inferred": "INFERRED, not measured: one initial HF prefill per positive-output generation call. Native unavailable.",
    "decode_calls_inferred": "INFERRED, not measured: all raw generated tokens minus positive-output generation calls; no speculation in this backend. Native unavailable.",
    "rounds": "Executed parallel fork rounds; native=0",
    "generation_turns": "Parallel rounds+1; native=1",
    "F": "Logical critical sequential sampled-token depth; native F=sampled length. Not measured GPU model-forward invocations.",
    "T_sampled": "Retained sampled response tokens",
    "T_forced": "Forced response tokens including think prefix/protocol bridges",
    "T_assembled": "Total assembled response tokens",
    "actual_generated_tokens": "All generated token outputs across actual generation calls, including discarded outputs if any",
    "wall_seconds": "Per-question generation elapsed, excludes engine startup; backend confounded",
    "backend_confound": "Structured uses HF structured serial backend through vLLM worker RPC; native uses fast vLLM generation. Wall comparisons are descriptive and cannot establish parallel execution speedup."
  },
  "backend_labels": [
    "hf_structured_serial_backend"
  ],
  "matching_protocol": {
    "prompt_policy": "Custom system-file supplied verbatim before native chat-template rendering; see system_file and hash",
    "question_seed": "42+sample_index",
    "response_budget": 4096,
    "path_budget": 2048,
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20
  },
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "provenance": {
    "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
    "generation_config_sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "24",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ]
}
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/worker-exits.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/epoch1-guard-structured-24/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/summary.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 103,
  "pass_at_1_completed_only": 0.8046875,
  "format_valid": 107,
  "format_fraction_completed_only": 0.8359375,
  "executed_fork_samples": 4,
  "unfinished_thinking": 17,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 1,
  "parallel_protocol_fraction_completed_only": 0.0078125,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 123,
  "parallel_execution_mismatch_samples": 5,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 105,
  "legacy_format_fraction_completed_only": 0.8203125,
  "legacy_parallel_protocol_valid": 0,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": true,
    "fork_coverage_at_least_0_2": false,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": false,
    "invalid_width_fraction_at_most_0_05": true,
    "at_least_one_correct": true
  },
  "gate_thresholds": {
    "basic_strict_format": 0.8,
    "fork_coverage": 0.2,
    "valid_parallel_among_executed_forks": 0.9,
    "max_invalid_width": 0.05,
    "min_correct": 1
  },
  "gate_raw_counts": {
    "completed": 128,
    "basic_valid": 107,
    "executed_fork_samples": 4,
    "valid_parallel_among_fork_samples": 1,
    "invalid_width_samples": 5,
    "correct": 103
  },
  "fork_coverage": 0.03125,
  "valid_parallel_among_executed_forks": 0.25,
  "invalid_width_fraction": 0.0390625,
  "correct_and_basic_valid": 101,
  "correct_and_parallel_valid": 1,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 186299.0,
      "mean": 1455.4609375,
      "median": 966.0,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 188348.0,
      "mean": 1471.46875,
      "median": 986.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 66.0,
      "mean": 0.515625,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 25.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 188414.0,
      "mean": 1471.984375,
      "median": 986.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 188348.0,
      "mean": 1471.46875,
      "median": 986.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 272.0,
      "mean": 2.125,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 12.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 7045.101237297058,
      "mean": 55.03985341638327,
      "median": 36.922866344451904,
      "p95": 153.11052583456038,
      "min": 3.8875763416290283,
      "max": 156.91198468208313
    },
    "forks": {
      "n": 128,
      "sum": 4.0,
      "mean": 0.03125,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 128,
      "sum": 4.0,
      "mean": 0.03125,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 132.0,
      "mean": 1.03125,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 188348.0,
      "mean": 1471.46875,
      "median": 986.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 272.0,
      "mean": 2.125,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 12.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 188076.0,
      "mean": 1469.34375,
      "median": 984.5,
      "p95": 4093.0,
      "min": 101.0,
      "max": 4093.0
    },
    "widths": {
      "n": 9,
      "sum": 34.0,
      "mean": 3.7777777777777777,
      "median": 3.0,
      "p95": 6.199999999999999,
      "min": 2.0,
      "max": 7.0
    },
    "width_histogram": {
      "2": 1,
      "3": 4,
      "4": 2,
      "5": 1,
      "7": 1
    },
    "truncated_samples": 14,
    "truncated_fraction": 0.109375,
    "invalid_width_samples": 5,
    "forked_samples": 4
  },
  "metrics_correct": {
    "F": {
      "n": 103,
      "sum": 122241.0,
      "mean": 1186.8058252427184,
      "median": 922.0,
      "p95": 3263.3999999999974,
      "min": 139.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 103,
      "sum": 123060.0,
      "mean": 1194.7572815533981,
      "median": 940.0,
      "p95": 3263.3999999999974,
      "min": 139.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 103,
      "sum": 34.0,
      "mean": 0.3300970873786408,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 25.0
    },
    "T_assembled": {
      "n": 103,
      "sum": 123094.0,
      "mean": 1195.0873786407767,
      "median": 940.0,
      "p95": 3263.3999999999974,
      "min": 139.0,
      "max": 4094.0
    },
    "actual_generated_tokens": {
      "n": 103,
      "sum": 123060.0,
      "mean": 1194.7572815533981,
      "median": 940.0,
      "p95": 3263.3999999999974,
      "min": 139.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 103,
      "sum": 220.0,
      "mean": 2.1359223300970873,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 12.0
    },
    "wall_seconds": {
      "n": 103,
      "sum": 4610.421470403671,
      "mean": 44.76137349906477,
      "median": 34.62513446807861,
      "p95": 122.77431814670554,
      "min": 5.312189102172852,
      "max": 154.78808403015137
    },
    "forks": {
      "n": 103,
      "sum": 2.0,
      "mean": 0.019417475728155338,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 103,
      "sum": 2.0,
      "mean": 0.019417475728155338,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 103,
      "sum": 105.0,
      "mean": 1.0194174757281553,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 103,
      "sum": 123060.0,
      "mean": 1194.7572815533981,
      "median": 940.0,
      "p95": 3263.3999999999974,
      "min": 139.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 103,
      "sum": 220.0,
      "mean": 2.1359223300970873,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 12.0
    },
    "decode_calls_inferred": {
      "n": 103,
      "sum": 122840.0,
      "mean": 1192.621359223301,
      "median": 938.0,
      "p95": 3261.3999999999974,
      "min": 137.0,
      "max": 4092.0
    },
    "widths": {
      "n": 2,
      "sum": 9.0,
      "mean": 4.5,
      "median": 4.5,
      "p95": 6.75,
      "min": 2.0,
      "max": 7.0
    },
    "width_histogram": {
      "2": 1,
      "7": 1
    },
    "truncated_samples": 1,
    "truncated_fraction": 0.009708737864077669,
    "invalid_width_samples": 0,
    "forked_samples": 2
  },
  "historical_correct": 101,
  "historical_pass_at_1_completed_only": 0.7890625,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 128,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 52,
      "pass_at_1": 0.8125,
      "basic_valid": 52,
      "basic_valid_fraction": 0.8125,
      "parallel_valid": 1,
      "parallel_syntax_valid": 61,
      "parallel_execution_mismatch_samples": 3,
      "correct_and_basic_valid": 51,
      "correct_and_parallel_valid": 1,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 91951.0,
          "mean": 1436.734375,
          "median": 999.0,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 94000.0,
          "mean": 1468.75,
          "median": 1012.5,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 66.0,
          "mean": 1.03125,
          "median": 0.0,
          "p95": 7.649999999999949,
          "min": 0.0,
          "max": 25.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 94066.0,
          "mean": 1469.78125,
          "median": 1012.5,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 94000.0,
          "mean": 1468.75,
          "median": 1012.5,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 149.0,
          "mean": 2.328125,
          "median": 2.0,
          "p95": 5.399999999999977,
          "min": 1.0,
          "max": 12.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 3520.2962465286255,
          "mean": 55.00462885200977,
          "median": 37.99865019321442,
          "p95": 151.6307996749878,
          "min": 3.8875763416290283,
          "max": 156.91198468208313
        },
        "forks": {
          "n": 64,
          "sum": 4.0,
          "mean": 0.0625,
          "median": 0.0,
          "p95": 0.8499999999999943,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 4.0,
          "mean": 0.0625,
          "median": 0.0,
          "p95": 0.8499999999999943,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 68.0,
          "mean": 1.0625,
          "median": 1.0,
          "p95": 1.8499999999999943,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 94000.0,
          "mean": 1468.75,
          "median": 1012.5,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 149.0,
          "mean": 2.328125,
          "median": 2.0,
          "p95": 5.399999999999977,
          "min": 1.0,
          "max": 12.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 93851.0,
          "mean": 1466.421875,
          "median": 1010.5,
          "p95": 4093.0,
          "min": 101.0,
          "max": 4093.0
        },
        "widths": {
          "n": 7,
          "sum": 28.0,
          "mean": 4.0,
          "median": 4.0,
          "p95": 6.399999999999999,
          "min": 2.0,
          "max": 7.0
        },
        "width_histogram": {
          "2": 1,
          "3": 2,
          "4": 2,
          "5": 1,
          "7": 1
        },
        "truncated_samples": 7,
        "truncated_fraction": 0.109375,
        "invalid_width_samples": 3,
        "forked_samples": 4
      },
      "metrics_correct": {
        "F": {
          "n": 52,
          "sum": 61424.0,
          "mean": 1181.2307692307693,
          "median": 965.5,
          "p95": 2944.449999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "T_sampled": {
          "n": 52,
          "sum": 62243.0,
          "mean": 1196.9807692307693,
          "median": 986.5,
          "p95": 2944.449999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "T_forced": {
          "n": 52,
          "sum": 34.0,
          "mean": 0.6538461538461539,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 25.0
        },
        "T_assembled": {
          "n": 52,
          "sum": 62277.0,
          "mean": 1197.6346153846155,
          "median": 986.5,
          "p95": 2944.449999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "actual_generated_tokens": {
          "n": 52,
          "sum": 62243.0,
          "mean": 1196.9807692307693,
          "median": 986.5,
          "p95": 2944.449999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "generation_calls": {
          "n": 52,
          "sum": 118.0,
          "mean": 2.269230769230769,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 12.0
        },
        "wall_seconds": {
          "n": 52,
          "sum": 2336.7687690258026,
          "mean": 44.937860942803894,
          "median": 36.922866344451904,
          "p95": 111.17136794328678,
          "min": 5.312189102172852,
          "max": 154.11506366729736
        },
        "forks": {
          "n": 52,
          "sum": 2.0,
          "mean": 0.038461538461538464,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 52,
          "sum": 2.0,
          "mean": 0.038461538461538464,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 52,
          "sum": 54.0,
          "mean": 1.0384615384615385,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 52,
          "sum": 62243.0,
          "mean": 1196.9807692307693,
          "median": 986.5,
          "p95": 2944.449999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "prefill_calls_inferred": {
          "n": 52,
          "sum": 118.0,
          "mean": 2.269230769230769,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 12.0
        },
        "decode_calls_inferred": {
          "n": 52,
          "sum": 62125.0,
          "mean": 1194.7115384615386,
          "median": 984.5,
          "p95": 2942.449999999997,
          "min": 137.0,
          "max": 4065.0
        },
        "widths": {
          "n": 2,
          "sum": 9.0,
          "mean": 4.5,
          "median": 4.5,
          "p95": 6.75,
          "min": 2.0,
          "max": 7.0
        },
        "width_histogram": {
          "2": 1,
          "7": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 2
      },
      "historical_correct": 51,
      "historical_pass_at_1": 0.796875
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 51,
      "pass_at_1": 0.796875,
      "basic_valid": 55,
      "basic_valid_fraction": 0.859375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 62,
      "parallel_execution_mismatch_samples": 2,
      "correct_and_basic_valid": 50,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 94348.0,
          "mean": 1474.1875,
          "median": 928.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 94348.0,
          "mean": 1474.1875,
          "median": 928.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 94348.0,
          "mean": 1474.1875,
          "median": 928.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 94348.0,
          "mean": 1474.1875,
          "median": 928.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 123.0,
          "mean": 1.921875,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 3524.8049907684326,
          "mean": 55.07507798075676,
          "median": 34.408695220947266,
          "p95": 153.4827780842781,
          "min": 3.9903221130371094,
          "max": 155.6802384853363
        },
        "forks": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 94348.0,
          "mean": 1474.1875,
          "median": 928.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 123.0,
          "mean": 1.921875,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 94225.0,
          "mean": 1472.265625,
          "median": 926.0,
          "p95": 4093.0,
          "min": 108.0,
          "max": 4093.0
        },
        "widths": {
          "n": 2,
          "sum": 6.0,
          "mean": 3.0,
          "median": 3.0,
          "p95": 3.0,
          "min": 3.0,
          "max": 3.0
        },
        "width_histogram": {
          "3": 2
        },
        "truncated_samples": 7,
        "truncated_fraction": 0.109375,
        "invalid_width_samples": 2,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 51,
          "sum": 60817.0,
          "mean": 1192.4901960784314,
          "median": 792.0,
          "p95": 3133.0,
          "min": 226.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 51,
          "sum": 60817.0,
          "mean": 1192.4901960784314,
          "median": 792.0,
          "p95": 3133.0,
          "min": 226.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 51,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "T_assembled": {
          "n": 51,
          "sum": 60817.0,
          "mean": 1192.4901960784314,
          "median": 792.0,
          "p95": 3133.0,
          "min": 226.0,
          "max": 4094.0
        },
        "actual_generated_tokens": {
          "n": 51,
          "sum": 60817.0,
          "mean": 1192.4901960784314,
          "median": 792.0,
          "p95": 3133.0,
          "min": 226.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 51,
          "sum": 102.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 51,
          "sum": 2273.6527013778687,
          "mean": 44.58142551721311,
          "median": 29.417937994003296,
          "p95": 118.8286429643631,
          "min": 8.353388786315918,
          "max": 154.78808403015137
        },
        "forks": {
          "n": 51,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 51,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 51,
          "sum": 51.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 51,
          "sum": 60817.0,
          "mean": 1192.4901960784314,
          "median": 792.0,
          "p95": 3133.0,
          "min": 226.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 51,
          "sum": 102.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 51,
          "sum": 60715.0,
          "mean": 1190.4901960784314,
          "median": 790.0,
          "p95": 3131.0,
          "min": 224.0,
          "max": 4092.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 1,
        "truncated_fraction": 0.0196078431372549,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 50,
      "historical_pass_at_1": 0.78125
    }
  },
  "cost_definitions": {
    "model_forward_calls_inferred": "INFERRED, not measured: serial HF structured_generate runs one initial model forward and one for each additional sampled output, hence sum raw generated_ids lengths across ALL calls. Native unavailable.",
    "prefill_calls_inferred": "INFERRED, not measured: one initial HF prefill per positive-output generation call. Native unavailable.",
    "decode_calls_inferred": "INFERRED, not measured: all raw generated tokens minus positive-output generation calls; no speculation in this backend. Native unavailable.",
    "rounds": "Executed parallel fork rounds; native=0",
    "generation_turns": "Parallel rounds+1; native=1",
    "F": "Logical critical sequential sampled-token depth; native F=sampled length. Not measured GPU model-forward invocations.",
    "T_sampled": "Retained sampled response tokens",
    "T_forced": "Forced response tokens including think prefix/protocol bridges",
    "T_assembled": "Total assembled response tokens",
    "actual_generated_tokens": "All generated token outputs across actual generation calls, including discarded outputs if any",
    "wall_seconds": "Per-question generation elapsed, excludes engine startup; backend confounded",
    "backend_confound": "Structured uses HF structured serial backend through vLLM worker RPC; native uses fast vLLM generation. Wall comparisons are descriptive and cannot establish parallel execution speedup."
  },
  "backend_labels": [
    "hf_structured_serial_backend"
  ],
  "matching_protocol": {
    "prompt_policy": "Custom system-file supplied verbatim before native chat-template rendering; see system_file and hash",
    "question_seed": "42+sample_index",
    "response_budget": 4096,
    "path_budget": 2048,
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20
  },
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "provenance": {
    "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ]
}
```

</details>

- [work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/worker-exits.json](../artifacts/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/instruct-full-20261011/matched-eval128-comparison.json](../artifacts/work/experiments/instruct-full-20261011/matched-eval128-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "matched_explicit_protocol": true,
  "generation_config_hashes_differ": true,
  "explicit_sampling": {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20,
    "repetition_penalty": 1,
    "seed": "42+sample_index"
  },
  "results": {
    "epoch1-guard-structured-128": {
      "completed": 128,
      "correct": 86,
      "format_valid": 126,
      "parallel_valid": 124,
      "unfinished_thinking": 1,
      "by_dataset": {
        "gsm": {
          "correct": 47,
          "completed": 64
        },
        "math": {
          "correct": 39,
          "completed": 64
        }
      },
      "actual_policy_width_attempt_groups": {
        "count": 127,
        "histogram": {
          "4": 30,
          "2": 58,
          "3": 37,
          "5": 1,
          "6": 1
        },
        "mean": 2.8188976377952755
      },
      "actual_completed_path_summary_groups": {
        "count": 127,
        "histogram": {
          "4": 30,
          "2": 58,
          "3": 37,
          "5": 1,
          "6": 1
        },
        "mean": 2.8188976377952755
      },
      "executed_forks_stats_total": 127,
      "details": "125 records; see original artifact",
      "critical_path_proxy_F_mean": 569.0390625,
      "inferred_sampled_token_work_mean": 722.5234375,
      "manifest": {
        "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
        "mode": "structured",
        "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
        "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/questions-128.jsonl",
        "response_cap": 4096,
        "path_cap": 2048,
        "planned": 128,
        "suite": "128",
        "native_eos_ids": [
          151643,
          151645
        ],
        "diagnostic_only": true,
        "checkpoint_selection_allowed": false,
        "guard_protocol": "native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094",
        "model_precision": "bf16",
        "scorer_think_tag_fix": true,
        "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
        "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
        "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
        "generation_config_sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
        "runtime_sha256": {
          "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
          "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
          "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
          "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
          "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
        }
      },
      "generation_config": {
        "bos_token_id": 151643,
        "do_sample": true,
        "eos_token_id": [
          151645,
          151643
        ],
        "pad_token_id": 151643,
        "temperature": 0.6,
        "top_k": 20,
        "top_p": 0.95,
        "transformers_version": "4.53.2"
      }
    },
    "warmup-lr1e3-guard-structured-128": {
      "completed": 128,
      "correct": 103,
      "format_valid": 107,
      "parallel_valid": 1,
      "unfinished_thinking": 17,
      "by_dataset": {
        "gsm": {
          "correct": 52,
          "completed": 64
        },
        "math": {
          "correct": 51,
          "completed": 64
        }
      },
      "actual_policy_width_attempt_groups": {
        "count": 9,
        "histogram": {
          "0": 5,
          "2": 1,
          "4": 2,
          "7": 1
        },
        "mean": 1.8888888888888888
      },
      "actual_completed_path_summary_groups": {
        "count": 4,
        "histogram": {
          "2": 1,
          "4": 2,
          "7": 1
        },
        "mean": 4.25
      },
      "executed_forks_stats_total": 4,
      "details": [
        {
          "id": "math_train/intermediate_algebra/1266",
          "groups": [
            {
              "path_calls": 0,
              "summary_call": false
            }
          ],
          "executed_forks_stat": 0
        },
        {
          "id": "gsm_infinite_ops2/ops2/34",
          "groups": [
            {
              "path_calls": 2,
              "summary_call": true
            }
          ],
          "executed_forks_stat": 1
        },
        {
          "id": "gsm_infinite_ops3/ops3/441",
          "groups": [
            {
              "path_calls": 4,
              "summary_call": true
            }
          ],
          "executed_forks_stat": 1
        },
        {
          "id": "gsm_infinite_ops3/ops3/396",
          "groups": [
            {
              "path_calls": 4,
              "summary_call": true
            }
          ],
          "executed_forks_stat": 1
        },
        {
          "id": "gsm_infinite_ops6/ops6/367",
          "groups": [
            {
              "path_calls": 0,
              "summary_call": false
            }
          ],
          "executed_forks_stat": 0
        },
        {
          "id": "math_train/intermediate_algebra/856",
          "groups": [
            {
              "path_calls": 0,
              "summary_call": false
            }
          ],
          "executed_forks_stat": 0
        },
        {
          "id": "gsm_infinite_ops6/ops6/497",
          "groups": [
            {
              "path_calls": 7,
              "summary_call": true
            }
          ],
          "executed_forks_stat": 1
        },
        {
          "id": "gsm_infinite_ops6/ops6/476",
          "groups": [
            {
              "path_calls": 0,
              "summary_call": false
            }
          ],
          "executed_forks_stat": 0
        },
        {
          "id": "gsm_infinite_ops3/ops3/695",
          "groups": [
            {
              "path_calls": 0,
              "summary_call": false
            }
          ],
          "executed_forks_stat": 0
        }
      ],
      "critical_path_proxy_F_mean": 1455.4609375,
      "inferred_sampled_token_work_mean": 1471.46875,
      "manifest": {
        "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "mode": "structured",
        "system_file": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
        "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/questions-128.jsonl",
        "response_cap": 4096,
        "path_cap": 2048,
        "planned": 128,
        "suite": "128",
        "native_eos_ids": [
          151643,
          151645
        ],
        "diagnostic_only": true,
        "checkpoint_selection_allowed": false,
        "guard_protocol": "native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094",
        "model_precision": "bf16",
        "scorer_think_tag_fix": true,
        "evaluator_sha256": "18a0a9f6245eba0b072fcc98be8bf26f0fdea440c443ba43d55ea234ebcabf93",
        "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
        "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
        "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
        "runtime_sha256": {
          "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
          "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
          "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "59489cc00c70e83ce6f66b199dab342d2a54150c7d88554c48d32b846d5a03ce",
          "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
          "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
        }
      },
      "generation_config": {
        "bos_token_id": 151643,
        "do_sample": true,
        "eos_token_id": [
          151645,
          151643
        ],
        "pad_token_id": 151643,
        "temperature": 0.6,
        "top_k": 20,
        "top_p": 0.95,
        "transformers_version": "4.51.0"
      }
    }
  },
  "accuracy_difference_full_minus_warmup": -17,
  "accuracy_percentage_points": -13.28125,
  "width_definition": "Counts actual raw policy phase=path calls grouped after each actual width call; completed means summary call present with >=2 actual paths; width attempts with zero paths preserved separately. No textual headers counted.",
  "forward_semantics": "F critical sequential sampled-token depth proxy and inferred raw sampled-token work are not physical forward invocation counts."
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/format-conditioned-metrics-20261012.json](../artifacts/work/experiments/instruct-full-20261011/reports/format-conditioned-metrics-20261012.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "definition": "Accuracy_all uses every task; all cost/width/depth statistics condition on format_valid. Serial valid tasks count as depth0; mean width averages executed completed rounds only, not textual tags.",
  "models": [
    {
      "model": "Original Instruct",
      "suite": "MATH64 from mixed128",
      "total": 64,
      "correct": 45,
      "accuracy_all_pct": 70.3125,
      "valid_format_count": 7,
      "valid_format_pct": 10.9375,
      "accuracy_given_valid_format_pct": 100.0,
      "mean_F_given_valid_format": 1989,
      "median_F_given_valid_format": 1819,
      "mean_width_given_valid_format": null,
      "width_denominator_rounds": 0,
      "mean_rounds_given_valid_format": 0,
      "total_rounds_given_valid_format": 0,
      "max_rounds_given_valid_format": 0,
      "forked_tasks_given_valid_format": 0,
      "forked_task_fraction_given_valid_format": 0.0,
      "mean_sampled_tokens_given_valid_format": 1989,
      "forward_kind": "reconstructed serial AR forwards; not instrumented",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128",
      "source_sha256": {
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/scores.jsonl": "935ab03361779768dae09e20db61bc5b6450f37548b25983fa9cf1cefa06c9d0"
      },
      "task_rows": [
        {
          "id": "math_train/prealgebra/8",
          "correct": true,
          "forwards": 2224,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/algebra/340",
          "correct": true,
          "forwards": 1655,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/number_theory/76",
          "correct": true,
          "forwards": 2032,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/algebra/216",
          "correct": true,
          "forwards": 1594,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/algebra/457",
          "correct": true,
          "forwards": 1819,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/intermediate_algebra/464",
          "correct": true,
          "forwards": 3235,
          "widths": [],
          "rounds": 0
        },
        {
          "id": "math_train/algebra/106",
          "correct": true,
          "forwards": 1364,
          "widths": [],
          "rounds": 0
        }
      ]
    },
    {
      "model": "Instruct +6token rows",
      "suite": "MATH64 from mixed128",
      "total": 64,
      "correct": 51,
      "accuracy_all_pct": 79.6875,
      "valid_format_count": 55,
      "valid_format_pct": 85.9375,
      "accuracy_given_valid_format_pct": 90.9090909090909,
      "mean_F_given_valid_format": 1189.9454545454546,
      "median_F_given_valid_format": 836,
      "mean_width_given_valid_format": null,
      "width_denominator_rounds": 0,
      "mean_rounds_given_valid_format": 0,
      "total_rounds_given_valid_format": 0,
      "max_rounds_given_valid_format": 0,
      "forked_tasks_given_valid_format": 0,
      "forked_task_fraction_given_valid_format": 0.0,
      "mean_sampled_tokens_given_valid_format": 1189.9454545454546,
      "forward_kind": "reconstructed serial AR forwards; not instrumented",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128",
      "source_sha256": {
        "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128/scores.jsonl": "fa6b7dff917eae614a85c2fea6d1df135bd99884fbc08d122f42a75b53642923"
      },
      "task_rows": "55 records; see original artifact"
    },
    {
      "model": "Full SFT42",
      "suite": "MATH500",
      "total": 500,
      "correct": 251,
      "accuracy_all_pct": 50.2,
      "valid_format_count": 457,
      "valid_format_pct": 91.4,
      "accuracy_given_valid_format_pct": 51.64113785557987,
      "mean_F_given_valid_format": 716.8490153172867,
      "median_F_given_valid_format": 598,
      "mean_width_given_valid_format": 3.025586353944563,
      "width_denominator_rounds": 469,
      "mean_rounds_given_valid_format": 1.026258205689278,
      "total_rounds_given_valid_format": 469,
      "max_rounds_given_valid_format": 2,
      "forked_tasks_given_valid_format": 449,
      "forked_task_fraction_given_valid_format": 0.9824945295404814,
      "mean_sampled_tokens_given_valid_format": 943.7374179431072,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline",
      "source_sha256": {
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-0.jsonl": "a6849beaba853dd09fb5ed39239541c063d7e9f722a2e9bf057e15faa5c6b25b",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-1.jsonl": "72eeeac23cf2b3d39e3e82f982fdde47a7ee8df3d063fac35b1beb66edf9b714",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-2.jsonl": "60bc7d41cb380f8c4abd74905465898b41308e6ccef497b151ad699037162bc6",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-3.jsonl": "4ef24420a4a05405fe479adefbbdcda184b8aa4aeb3962285b2dd07efe0d5538",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-4.jsonl": "876999b7237223b0d43e867d8eaa24401538a9cc0fc9af642634d1daf13f2f78",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-5.jsonl": "2c9dde98f9919072df8dcd94c7d2be24a53f29b9a38f197d6acbee5324f8ab55",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-6.jsonl": "22271b1e03e557a442c1721e4c9272d33cc443838fc4e776f27e253e29520638",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-7.jsonl": "d5c4a082b215e0dde6610a13ac0c2bf49d2bc2ce70fc0a77458bcae345426c5a"
      },
      "task_rows": "457 records; see original artifact"
    },
    {
      "model": "RL R1 step64",
      "suite": "MATH500",
      "total": 500,
      "correct": 353,
      "accuracy_all_pct": 70.6,
      "valid_format_count": 277,
      "valid_format_pct": 55.4,
      "accuracy_given_valid_format_pct": 81.94945848375451,
      "mean_F_given_valid_format": 685.9025270758123,
      "median_F_given_valid_format": 546,
      "mean_width_given_valid_format": 2.2059925093632957,
      "width_denominator_rounds": 267,
      "mean_rounds_given_valid_format": 0.9638989169675091,
      "total_rounds_given_valid_format": 267,
      "max_rounds_given_valid_format": 1,
      "forked_tasks_given_valid_format": 267,
      "forked_task_fraction_given_valid_format": 0.9638989169675091,
      "mean_sampled_tokens_given_valid_format": 847.2274368231047,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064",
      "source_sha256": {
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-0.jsonl": "21cd02b47840bd41afa4afc2f3a06c3b22b44bd4a0923fa32cba3f56763e89b6",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-1.jsonl": "88f86bcc7b7e8a5dbd528cf2ed2602ebca81a7ae07228cc284250a5f05bdafef",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-2.jsonl": "41fe8826be633ebaaffa606aa89761403ef095b8b0332b3e44a23c2eadbe02e7",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-3.jsonl": "156b85c82865e165c24482d0aa48c81218265ea59d14898265475a74ecb3d632",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-4.jsonl": "41dd590e8066690bc61ed0e75975d0c67bac82f284dd41c0f1c105ac7214118c",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-5.jsonl": "2c31ae9f416351d2e49966ccac9e3e1e7e9dbce77c2c27d8cb68be2fb01b36f7",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-6.jsonl": "cef7c9d96db60f70aa2c53b49596eff3f0f98521b5d572ca51bb76e96737dff0",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-7.jsonl": "e716533059c3c18f15693be3a1cd55e83268dcde7d66fccc190d5c2979d9597c"
      },
      "task_rows": "277 records; see original artifact"
    },
    {
      "model": "RL R2 step64",
      "suite": "MATH500",
      "total": 500,
      "correct": 280,
      "accuracy_all_pct": 56.0,
      "valid_format_count": 456,
      "valid_format_pct": 91.2,
      "accuracy_given_valid_format_pct": 58.1140350877193,
      "mean_F_given_valid_format": 656.813596491228,
      "median_F_given_valid_format": 546.0,
      "mean_width_given_valid_format": 4.382289416846652,
      "width_denominator_rounds": 463,
      "mean_rounds_given_valid_format": 1.0153508771929824,
      "total_rounds_given_valid_format": 463,
      "max_rounds_given_valid_format": 3,
      "forked_tasks_given_valid_format": 452,
      "forked_task_fraction_given_valid_format": 0.9912280701754386,
      "mean_sampled_tokens_given_valid_format": 1000.609649122807,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064",
      "source_sha256": {
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-0.jsonl": "01a22c74f93d27d20cf424d09b53e462a7a90dc4861f1942bd96fac0dbd62cc8",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-1.jsonl": "a78289fa85b01b09e5ac760a57d97ceb6c6d115559dd9a0e79ea973c8cd2c5ce",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-2.jsonl": "f14a3061576db0779c6d60fec9023f1144dc20c58b4b9b11318931bf9ec66f39",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-3.jsonl": "6ee71369b81cb2be4fdcdc486768d42280b7373820142f56e8f12344fb8cac45",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-4.jsonl": "d8b8cdc914803d9047f7fa8ecfc42a908180b8f5ff662e1fc27d73a84640777b",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-5.jsonl": "94a12a5bfa5ba3c2e4d5c2cf4854e6c12308f05e6c465fe83af9e20f5357cfac",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-6.jsonl": "f77ba1837da927034dd130ad7f49967216dd2162185b26f2ca0bb3ce532ab492",
        "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-7.jsonl": "18dcd5ea3efd5fca50071f9bbb667e7af5039e59598e94b78c6ec1c075859577"
      },
      "task_rows": "456 records; see original artifact"
    }
  ],
  "historical_format_schema_caveat": "MATH64 native/warmup use their saved basic schema_v2; MATH500 uses canonical counted Instruct schema. Different suites/backends must not be interpreted as matched improvements."
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/latest-rl-compact.json](../artifacts/work/experiments/instruct-full-20261011/reports/latest-rl-compact.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "R2": {
    "status": {
      "state": "training",
      "step": 83,
      "steps": 500,
      "finite": true,
      "optimizer_step": true,
      "backbone_update_l2": 5.27348440440145e-06,
      "max_replay_logp_drift": 0.0004024505615234375
    },
    "val": [
      {
        "step": 0,
        "completed": 32,
        "correct": 16,
        "format_valid": 29,
        "parallel_valid": 29,
        "fork_tasks": 32,
        "actual_rounds": 33,
        "width": 2.727272727272727,
        "F": 598.40625,
        "T": 696.53125
      },
      {
        "step": 4,
        "completed": 32,
        "correct": 19,
        "format_valid": 31,
        "parallel_valid": 29,
        "fork_tasks": 30,
        "actual_rounds": 30,
        "width": 2.933333333333333,
        "F": 601.78125,
        "T": 696.75
      },
      {
        "step": 8,
        "completed": 32,
        "correct": 20,
        "format_valid": 31,
        "parallel_valid": 30,
        "fork_tasks": 30,
        "actual_rounds": 30,
        "width": 2.8666666666666667,
        "F": 599.78125,
        "T": 697.8125
      },
      {
        "step": 16,
        "completed": 32,
        "correct": 18,
        "format_valid": 31,
        "parallel_valid": 30,
        "fork_tasks": 30,
        "actual_rounds": 30,
        "width": 2.7333333333333334,
        "F": 622.59375,
        "T": 721.46875
      },
      {
        "step": 32,
        "completed": 32,
        "correct": 25,
        "format_valid": 30,
        "parallel_valid": 30,
        "fork_tasks": 31,
        "actual_rounds": 32,
        "width": 3.5625,
        "F": 652.4375,
        "T": 809.21875
      },
      {
        "step": 64,
        "completed": 32,
        "correct": 21,
        "format_valid": 30,
        "parallel_valid": 30,
        "fork_tasks": 32,
        "actual_rounds": 32,
        "width": 4.25,
        "F": 652.21875,
        "T": 800
      }
    ]
  },
  "R1": {
    "status": {
      "state": "training",
      "step": 49,
      "steps": 500,
      "finite": true,
      "optimizer_step": true,
      "backbone_update_l2": 7.893786842168987e-06,
      "max_replay_logp_drift": 9.5367431640625e-05
    },
    "val": [
      {
        "step": 0,
        "completed": 32,
        "correct": 16,
        "format_valid": 29,
        "parallel_valid": 29,
        "fork_tasks": 32,
        "actual_rounds": 33,
        "width": 2.727272727272727,
        "F": 598.40625,
        "T": 696.53125
      },
      {
        "step": 4,
        "completed": 32,
        "correct": 19,
        "format_valid": 32,
        "parallel_valid": 32,
        "fork_tasks": 32,
        "actual_rounds": 33,
        "width": 2.9393939393939394,
        "F": 615.40625,
        "T": 749
      },
      {
        "step": 8,
        "completed": 32,
        "correct": 21,
        "format_valid": 31,
        "parallel_valid": 31,
        "fork_tasks": 32,
        "actual_rounds": 33,
        "width": 2.4242424242424243,
        "F": 579.71875,
        "T": 677.5
      },
      {
        "step": 16,
        "completed": 32,
        "correct": 24,
        "format_valid": 32,
        "parallel_valid": 32,
        "fork_tasks": 32,
        "actual_rounds": 33,
        "width": 2.4242424242424243,
        "F": 669.8125,
        "T": 788
      },
      {
        "step": 32,
        "completed": 32,
        "correct": 24,
        "format_valid": 28,
        "parallel_valid": 26,
        "fork_tasks": 30,
        "actual_rounds": 34,
        "width": 2.2941176470588234,
        "F": 647.09375,
        "T": 781.53125
      }
    ]
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/matched128-distribution-data.json](../artifacts/work/experiments/instruct-full-20261011/reports/matched128-distribution-data.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "runs": {
    "warmup-lr1e3-guard-structured-128": {
      "rows": "128 records; see original artifact",
      "score_sha256": "fa6b7dff917eae614a85c2fea6d1df135bd99884fbc08d122f42a75b53642923"
    },
    "epoch1-guard-structured-128": {
      "rows": "128 records; see original artifact",
      "score_sha256": "18235b20e9ce9d1ce913cca8045ec347de5d959db77009d83bd6cb8e615875e3"
    }
  },
  "rl_cleanval32": {
    "0": {
      "step": 0,
      "completed": 32,
      "correct": 16,
      "format_valid": 29,
      "parallel_valid": 29,
      "fork_tasks": 32,
      "widths": [
        3,
        2,
        3,
        3,
        2,
        2,
        2,
        4,
        2,
        2,
        2,
        3,
        3,
        2,
        2,
        2,
        3,
        4,
        4,
        3,
        4,
        4,
        4,
        3,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        2,
        3
      ],
      "actual_rounds": 33,
      "logical_depth": [
        586,
        340,
        447,
        414,
        721,
        598,
        603,
        343,
        315,
        548,
        522,
        363,
        584,
        1609,
        460,
        462,
        886,
        754,
        372,
        452,
        289,
        658,
        500,
        178,
        456,
        504,
        462,
        636,
        881,
        397,
        336,
        645
      ],
      "sampled_tokens": [
        843,
        444,
        527,
        491,
        791,
        739,
        814,
        386,
        364,
        668,
        629,
        475,
        671,
        1788,
        530,
        630,
        1241,
        1225,
        495,
        768,
        382,
        917,
        678,
        204,
        496,
        675,
        508,
        828,
        1177,
        527,
        393,
        985
      ],
      "actual_forward_calls": [
        672,
        394,
        487,
        414,
        721,
        598,
        685,
        343,
        315,
        548,
        579,
        424,
        584,
        1609,
        460,
        552,
        1060,
        942,
        438,
        571,
        326,
        755,
        596,
        178,
        456,
        504,
        462,
        789,
        1070,
        453,
        336,
        828
      ],
      "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
      "selection_allowed": true,
      "benchmark": false
    },
    "4": {
      "step": 4,
      "completed": 32,
      "correct": 19,
      "format_valid": 31,
      "parallel_valid": 29,
      "fork_tasks": 30,
      "widths": [
        2,
        2,
        3,
        3,
        3,
        2,
        3,
        3,
        3,
        2,
        3,
        4,
        2,
        2,
        2,
        4,
        3,
        4,
        3,
        4,
        2,
        4,
        2,
        3,
        4,
        3,
        3,
        3,
        4,
        3
      ],
      "actual_rounds": 30,
      "logical_depth": [
        606,
        460,
        373,
        443,
        333,
        1102,
        570,
        305,
        295,
        548,
        401,
        359,
        398,
        844,
        499,
        464,
        573,
        928,
        480,
        354,
        289,
        791,
        905,
        241,
        493,
        559,
        608,
        355,
        875,
        484,
        683,
        476
      ],
      "sampled_tokens": [
        704,
        514,
        454,
        563,
        333,
        1378,
        598,
        421,
        381,
        774,
        463,
        474,
        677,
        1014,
        603,
        527,
        809,
        1209,
        593,
        531,
        382,
        847,
        1220,
        288,
        653,
        1000,
        895,
        355,
        1330,
        673,
        923,
        710
      ],
      "actual_forward_calls": [
        606,
        460,
        414,
        511,
        333,
        1244,
        570,
        366,
        339,
        666,
        401,
        419,
        505,
        844,
        499,
        464,
        651,
        1086,
        533,
        438,
        326,
        791,
        1025,
        241,
        559,
        710,
        762,
        355,
        1151,
        585,
        799,
        604
      ],
      "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
      "selection_allowed": true,
      "benchmark": false
    }
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/results-overview-20261012.json](../artifacts/work/experiments/instruct-full-20261011/reports/results-overview-20261012.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen3-4B Instruct",
  "verified_on": "2026-10-12",
  "math500_protocol": {
    "coverage": 500,
    "samples_per_question": 1,
    "precision": "FP32",
    "temperature": 1,
    "top_p": 1,
    "response_budget": 4096,
    "path_budget": 768,
    "max_batched_paths": 8,
    "scorer_native_think_prefix": true,
    "forward_count": "instrumented physical generation model.forward"
  },
  "math500": [
    {
      "model": "fullSFT epoch1",
      "updates": 42,
      "correct": 251,
      "accuracy_pct": 50.2,
      "format_pct": 91.4,
      "parallel_valid_pct": 89.8,
      "correct_parallel_pct": 46.2,
      "fork_tasks_pct": 97.2,
      "mean_width": 3.031434184675835,
      "rounds_per_task": 1.018,
      "mean_actual_F": 746.74,
      "mean_sampled_tokens": 976.548
    },
    {
      "model": "old RL R1 checkpoint64",
      "reward": "correctness and forward cost",
      "correct": 353,
      "accuracy_pct": 70.6,
      "format_pct": 55.4,
      "parallel_valid_pct": 53.4,
      "correct_parallel_pct": 43.4,
      "fork_tasks_pct": 97.0,
      "mean_width": 2.168032786885246,
      "rounds_per_task": 0.976,
      "mean_actual_F": 899.186,
      "mean_sampled_tokens": 1091.536
    },
    {
      "model": "old RL R2 checkpoint64",
      "reward": "constant width/round bonus plus forward cost",
      "correct": 280,
      "accuracy_pct": 56.0,
      "format_pct": 91.2,
      "parallel_valid_pct": 90.4,
      "correct_parallel_pct": 52.4,
      "fork_tasks_pct": 98.8,
      "mean_width": 4.404339250493097,
      "rounds_per_task": 1.014,
      "mean_actual_F": 682.992,
      "mean_sampled_tokens": 1038.53
    }
  ],
  "old_RL_training_caveat": "These8GPU runs trained on128tasks with the earlier cap2 runtime and pre-fix training scorer; benchmark table is the corrected fullwidth8 rescore, not results of the current1024task run.",
  "mixed128": {
    "protocol": "Separate64GSM+64MATH diagnostic; not MATH500. Native baseline differs from the paired guarded structured warmup/fullSFT comparison.",
    "native_original": {
      "correct": 98,
      "accuracy_pct": 76.5625,
      "completed": 128,
      "gsm_correct": 53,
      "gsm_completed": 64,
      "math_correct": 45,
      "math_completed": 64,
      "format_valid": 55,
      "actual_fork_tasks": 0,
      "model_kind": "Original4B Instruct backbone, native thinking; no SFT",
      "source": "work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json",
      "mean_generated_tokens": 2791.5703125,
      "mean_forward_calls_inferred": 2791.5703125,
      "median_forward_calls_inferred": 2753.0,
      "p95_forward_calls_inferred": 4094.0,
      "forward_count_kind": "reconstructed serial AR work; not directly instrumented",
      "forward_audit": "work/experiments/instruct-full-20261011/reports/native-baseline-forward-audit.json",
      "gsm_mean_forward_calls_inferred": 2582.109375,
      "math_mean_forward_calls_inferred": 3001.03125
    },
    "six_token_row_warmup": {
      "correct": 103,
      "accuracy_pct": 80.46875,
      "format_valid": 107,
      "parallel_valid": 1,
      "actual_fork_tasks": 4
    },
    "fullSFT_epoch1": {
      "correct": 86,
      "accuracy_pct": 67.1875,
      "format_valid": 126,
      "parallel_valid": 124,
      "actual_fork_tasks": 125
    },
    "delta_full_minus_warmup_pp": -13.28125
  },
  "deep_SFT_partial": {
    "training_updates": 126,
    "dataset": "3000 synthetic layeredDAG;2700train300val",
    "completed": 277,
    "planned": 500,
    "correct": 132,
    "accuracy_pct": 47.65342960288809,
    "format_valid": 155,
    "format_pct": 55.95667870036101,
    "mean_F": 438.057761732852,
    "mean_width": 2.6950549450549453,
    "rounds_per_task": 1.3140794223826715,
    "matched_original_fullSFT_correct": 141,
    "matched_original_fullSFT_accuracy_pct": 50.90252707581227,
    "matched_original_fullSFT_format_valid": 255,
    "partial": true,
    "full_benchmark_missing": 223
  },
  "current_RL": {
    "train_tasks": 1024,
    "iterations_verified": 39,
    "post_RL_evaluation_available": false,
    "initial_clean_val_correct": 16,
    "initial_clean_val_completed": 32,
    "initial_clean_val_F": 541.28125
  },
  "source_roots": [
    "work/experiments/rl-instruct-20261011/math500-paired-audit",
    "work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/newdeep-fullSFT-0126",
    "work/experiments/instruct-full-20261011/matched-eval128-comparison.json"
  ],
  "plain_instruct_math500": {
    "completed": 0,
    "accuracy_pct": null,
    "matched_score_available": false,
    "reason": "Only separate native mixed128 score verified; do not substitute token-row warmup or fullSFT baseline for plain Instruct."
  },
  "comparison_table": [
    {
      "model": "Plain4B Instruct native",
      "suite": "64GSM+64MATH mixed128",
      "completed": 128,
      "correct": 98,
      "accuracy_pct": 76.5625,
      "mean_width": null,
      "mean_actual_F": null,
      "matched_math500": false,
      "mean_forward_calls_inferred": 2791.5703125,
      "forward_count_kind": "inferred serial; actual counter unavailable"
    },
    {
      "model": "fullSFT epoch1",
      "suite": "MATH500",
      "completed": 500,
      "correct": 251,
      "accuracy_pct": 50.2,
      "mean_width": 3.031434184675835,
      "mean_actual_F": 746.74,
      "matched_math500": true
    },
    {
      "model": "old RL R1 checkpoint64",
      "suite": "MATH500",
      "completed": 500,
      "correct": 353,
      "accuracy_pct": 70.6,
      "mean_width": 2.168032786885246,
      "mean_actual_F": 899.186,
      "matched_math500": true
    },
    {
      "model": "old RL R2 checkpoint64",
      "suite": "MATH500",
      "completed": 500,
      "correct": 280,
      "accuracy_pct": 56.0,
      "mean_width": 4.404339250493097,
      "mean_actual_F": 682.992,
      "matched_math500": true
    }
  ],
  "format_conditioned_table": {
    "definitions": {
      "accuracy_all": "Correctness on all tasks; no format filtering.",
      "cost_condition": "Only records with the saved format_valid verdict true.",
      "depth": "Number of completed executable fork-to-merge rounds per format-valid task; serial valid tasks contribute zero.",
      "width": "Mean executed branch count across completed rounds within format-valid tasks; serial tasks have no width.",
      "forwards": "Physical generation model.forward calls for MATH500; reconstructed serial autoregressive calls for the two MATH64 evaluations, not instrumented.",
      "format_protocol_caveat": "MATH64 uses saved basic native Instruct format validation; MATH500 uses strict canonical counted Instruct validation. These protocols and task sets differ.",
      "rl_caveat": "R1/R2 step64 are previous 8-GPU controls trained on 128 tasks with cap2 and earlier training scorer, then rescored with corrected fullwidth8 evaluation. These are not results of the current 1024-task campaign.",
      "valid_format_and_fork_rate_all": "Count of tasks with format_valid=true AND at least one completed executable fork-to-merge round, divided by all evaluated tasks. Mathematical correctness is not part of this metric."
    },
    "models": [
      {
        "model": "Original Instruct",
        "suite": "MATH64 from mixed128",
        "total": 64,
        "correct": 45,
        "accuracy_all_pct": 70.3125,
        "valid_format_count": 7,
        "valid_format_pct": 10.9375,
        "accuracy_given_valid_format_pct": 100.0,
        "mean_F_given_valid_format": 1989,
        "median_F_given_valid_format": 1819,
        "mean_width_given_valid_format": null,
        "width_denominator_rounds": 0,
        "mean_rounds_given_valid_format": 0,
        "total_rounds_given_valid_format": 0,
        "max_rounds_given_valid_format": 0,
        "forked_tasks_given_valid_format": 0,
        "forked_task_fraction_given_valid_format": 0.0,
        "mean_sampled_tokens_given_valid_format": 1989,
        "forward_kind": "reconstructed serial AR forwards; not instrumented",
        "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128",
        "valid_format_and_fork_count_all": 0,
        "valid_format_and_fork_rate_all_pct": 0.0
      },
      {
        "model": "Instruct +6token rows",
        "suite": "MATH64 from mixed128",
        "total": 64,
        "correct": 51,
        "accuracy_all_pct": 79.6875,
        "valid_format_count": 55,
        "valid_format_pct": 85.9375,
        "accuracy_given_valid_format_pct": 90.9090909090909,
        "mean_F_given_valid_format": 1189.9454545454546,
        "median_F_given_valid_format": 836,
        "mean_width_given_valid_format": null,
        "width_denominator_rounds": 0,
        "mean_rounds_given_valid_format": 0,
        "total_rounds_given_valid_format": 0,
        "max_rounds_given_valid_format": 0,
        "forked_tasks_given_valid_format": 0,
        "forked_task_fraction_given_valid_format": 0.0,
        "mean_sampled_tokens_given_valid_format": 1189.9454545454546,
        "forward_kind": "reconstructed serial AR forwards; not instrumented",
        "source": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128",
        "valid_format_and_fork_count_all": 0,
        "valid_format_and_fork_rate_all_pct": 0.0
      },
      {
        "model": "Full SFT42",
        "suite": "MATH500",
        "total": 500,
        "correct": 251,
        "accuracy_all_pct": 50.2,
        "valid_format_count": 457,
        "valid_format_pct": 91.4,
        "accuracy_given_valid_format_pct": 51.64113785557987,
        "mean_F_given_valid_format": 716.8490153172867,
        "median_F_given_valid_format": 598,
        "mean_width_given_valid_format": 3.025586353944563,
        "width_denominator_rounds": 469,
        "mean_rounds_given_valid_format": 1.026258205689278,
        "total_rounds_given_valid_format": 469,
        "max_rounds_given_valid_format": 2,
        "forked_tasks_given_valid_format": 449,
        "forked_task_fraction_given_valid_format": 0.9824945295404814,
        "mean_sampled_tokens_given_valid_format": 943.7374179431072,
        "forward_kind": "instrumented physical generation forwards",
        "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline",
        "valid_format_and_fork_count_all": 449,
        "valid_format_and_fork_rate_all_pct": 89.8
      },
      {
        "model": "RL R1 step64",
        "suite": "MATH500",
        "total": 500,
        "correct": 353,
        "accuracy_all_pct": 70.6,
        "valid_format_count": 277,
        "valid_format_pct": 55.4,
        "accuracy_given_valid_format_pct": 81.94945848375451,
        "mean_F_given_valid_format": 685.9025270758123,
        "median_F_given_valid_format": 546,
        "mean_width_given_valid_format": 2.2059925093632957,
        "width_denominator_rounds": 267,
        "mean_rounds_given_valid_format": 0.9638989169675091,
        "total_rounds_given_valid_format": 267,
        "max_rounds_given_valid_format": 1,
        "forked_tasks_given_valid_format": 267,
        "forked_task_fraction_given_valid_format": 0.9638989169675091,
        "mean_sampled_tokens_given_valid_format": 847.2274368231047,
        "forward_kind": "instrumented physical generation forwards",
        "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064",
        "valid_format_and_fork_count_all": 267,
        "valid_format_and_fork_rate_all_pct": 53.4
      },
      {
        "model": "RL R2 step64",
        "suite": "MATH500",
        "total": 500,
        "correct": 280,
        "accuracy_all_pct": 56.0,
        "valid_format_count": 456,
        "valid_format_pct": 91.2,
        "accuracy_given_valid_format_pct": 58.1140350877193,
        "mean_F_given_valid_format": 656.813596491228,
        "median_F_given_valid_format": 546.0,
        "mean_width_given_valid_format": 4.382289416846652,
        "width_denominator_rounds": 463,
        "mean_rounds_given_valid_format": 1.0153508771929824,
        "total_rounds_given_valid_format": 463,
        "max_rounds_given_valid_format": 3,
        "forked_tasks_given_valid_format": 452,
        "forked_task_fraction_given_valid_format": 0.9912280701754386,
        "mean_sampled_tokens_given_valid_format": 1000.609649122807,
        "forward_kind": "instrumented physical generation forwards",
        "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064",
        "valid_format_and_fork_count_all": 452,
        "valid_format_and_fork_rate_all_pct": 90.4
      }
    ],
    "warmup_decoder_sha256": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
    "audit_source": "format_conditioned_metrics.py"
  }
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/rl-strong-width-progress-data.json](../artifacts/work/experiments/instruct-full-20261011/reports/rl-strong-width-progress-data.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "validation-0000": {
    "step": 0,
    "completed": 32,
    "correct": 16,
    "format_valid": 29,
    "parallel_valid": 29,
    "fork_tasks": 32,
    "widths": [
      3,
      2,
      3,
      3,
      2,
      2,
      2,
      4,
      2,
      2,
      2,
      3,
      3,
      2,
      2,
      2,
      3,
      4,
      4,
      3,
      4,
      4,
      4,
      3,
      2,
      2,
      2,
      2,
      3,
      3,
      3,
      2,
      3
    ],
    "actual_rounds": 33,
    "logical_depth": [
      586,
      340,
      447,
      414,
      721,
      598,
      603,
      343,
      315,
      548,
      522,
      363,
      584,
      1609,
      460,
      462,
      886,
      754,
      372,
      452,
      289,
      658,
      500,
      178,
      456,
      504,
      462,
      636,
      881,
      397,
      336,
      645
    ],
    "sampled_tokens": [
      843,
      444,
      527,
      491,
      791,
      739,
      814,
      386,
      364,
      668,
      629,
      475,
      671,
      1788,
      530,
      630,
      1241,
      1225,
      495,
      768,
      382,
      917,
      678,
      204,
      496,
      675,
      508,
      828,
      1177,
      527,
      393,
      985
    ],
    "actual_forward_calls": [
      672,
      394,
      487,
      414,
      721,
      598,
      685,
      343,
      315,
      548,
      579,
      424,
      584,
      1609,
      460,
      552,
      1060,
      942,
      438,
      571,
      326,
      755,
      596,
      178,
      456,
      504,
      462,
      789,
      1070,
      453,
      336,
      828
    ],
    "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
    "selection_allowed": true,
    "benchmark": false
  },
  "validation-0004": {
    "step": 4,
    "completed": 32,
    "correct": 19,
    "format_valid": 31,
    "parallel_valid": 29,
    "fork_tasks": 30,
    "widths": [
      2,
      2,
      3,
      3,
      3,
      2,
      3,
      3,
      3,
      2,
      3,
      4,
      2,
      2,
      2,
      4,
      3,
      4,
      3,
      4,
      2,
      4,
      2,
      3,
      4,
      3,
      3,
      3,
      4,
      3
    ],
    "actual_rounds": 30,
    "logical_depth": [
      606,
      460,
      373,
      443,
      333,
      1102,
      570,
      305,
      295,
      548,
      401,
      359,
      398,
      844,
      499,
      464,
      573,
      928,
      480,
      354,
      289,
      791,
      905,
      241,
      493,
      559,
      608,
      355,
      875,
      484,
      683,
      476
    ],
    "sampled_tokens": [
      704,
      514,
      454,
      563,
      333,
      1378,
      598,
      421,
      381,
      774,
      463,
      474,
      677,
      1014,
      603,
      527,
      809,
      1209,
      593,
      531,
      382,
      847,
      1220,
      288,
      653,
      1000,
      895,
      355,
      1330,
      673,
      923,
      710
    ],
    "actual_forward_calls": [
      606,
      460,
      414,
      511,
      333,
      1244,
      570,
      366,
      339,
      666,
      401,
      419,
      505,
      844,
      499,
      464,
      651,
      1086,
      533,
      438,
      326,
      791,
      1025,
      241,
      559,
      710,
      762,
      355,
      1151,
      585,
      799,
      604
    ],
    "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
    "selection_allowed": true,
    "benchmark": false
  },
  "validation-0008": {
    "step": 8,
    "completed": 32,
    "correct": 20,
    "format_valid": 31,
    "parallel_valid": 30,
    "fork_tasks": 30,
    "widths": [
      3,
      4,
      3,
      4,
      4,
      3,
      3,
      3,
      2,
      3,
      3,
      2,
      2,
      2,
      3,
      3,
      3,
      3,
      2,
      2,
      4,
      3,
      2,
      3,
      3,
      3,
      3,
      4,
      2,
      2
    ],
    "actual_rounds": 30,
    "logical_depth": [
      652,
      288,
      401,
      448,
      1136,
      870,
      426,
      285,
      283,
      502,
      301,
      395,
      586,
      1046,
      654,
      350,
      396,
      680,
      396,
      352,
      331,
      524,
      734,
      297,
      544,
      618,
      505,
      669,
      895,
      474,
      531,
      585
    ],
    "sampled_tokens": [
      879,
      288,
      532,
      548,
      1461,
      1211,
      426,
      380,
      364,
      728,
      354,
      520,
      787,
      1213,
      823,
      401,
      536,
      961,
      487,
      529,
      456,
      574,
      1003,
      404,
      621,
      996,
      682,
      756,
      1376,
      743,
      607,
      684
    ],
    "actual_forward_calls": [
      794,
      288,
      442,
      481,
      1279,
      968,
      426,
      339,
      324,
      620,
      301,
      460,
      720,
      1046,
      654,
      350,
      462,
      838,
      458,
      436,
      331,
      524,
      822,
      352,
      544,
      792,
      619,
      714,
      1145,
      548,
      531,
      585
    ],
    "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
    "selection_allowed": true,
    "benchmark": false
  },
  "validation-0016": {
    "step": 16,
    "completed": 32,
    "correct": 18,
    "format_valid": 31,
    "parallel_valid": 30,
    "fork_tasks": 30,
    "widths": [
      3,
      2,
      3,
      3,
      4,
      2,
      3,
      3,
      3,
      2,
      2,
      3,
      2,
      2,
      3,
      4,
      2,
      3,
      2,
      3,
      2,
      2,
      2,
      3,
      4,
      4,
      4,
      3,
      2,
      2
    ],
    "actual_rounds": 30,
    "logical_depth": [
      651,
      300,
      449,
      424,
      1426,
      724,
      566,
      402,
      292,
      554,
      309,
      385,
      588,
      1269,
      437,
      470,
      285,
      963,
      343,
      340,
      287,
      324,
      613,
      277,
      471,
      635,
      699,
      970,
      986,
      449,
      388,
      508
    ],
    "sampled_tokens": [
      877,
      300,
      580,
      579,
      1565,
      1095,
      672,
      495,
      359,
      787,
      383,
      442,
      806,
      1437,
      508,
      582,
      285,
      1329,
      419,
      517,
      348,
      429,
      663,
      314,
      532,
      864,
      968,
      1495,
      1789,
      629,
      416,
      623
    ],
    "actual_forward_calls": [
      792,
      300,
      449,
      512,
      1467,
      879,
      566,
      466,
      319,
      684,
      309,
      385,
      739,
      1269,
      437,
      530,
      285,
      1060,
      343,
      424,
      287,
      385,
      613,
      277,
      471,
      769,
      776,
      1206,
      1471,
      557,
      388,
      508
    ],
    "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
    "selection_allowed": true,
    "benchmark": false
  },
  "validation-0032": [
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-2.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-6.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-4.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-3.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-5.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-7.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-1.jsonl",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-0.jsonl"
  ]
}
```

</details>

- [work/experiments/instruct-full-20261011/runs/epoch1/metrics.jsonl](../artifacts/work/experiments/instruct-full-20261011/runs/epoch1/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-full-20261011/runs/epoch1/result.json](../artifacts/work/experiments/instruct-full-20261011/runs/epoch1/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 42,
  "epochs": 1,
  "val_loss": 0.3917267322540283,
  "full_model": true,
  "think_wrapped": true
}
```

</details>

- [work/experiments/instruct-full-20261011/runs/smoke/metrics.jsonl](../artifacts/work/experiments/instruct-full-20261011/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-full-20261011/runs/smoke/result.json](../artifacts/work/experiments/instruct-full-20261011/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 2,
  "epochs": 1,
  "val_loss": 0.8409368991851807,
  "full_model": true,
  "think_wrapped": true
}
```

</details>

- [work/experiments/instruct-full-20261011/reports/format-conditioned-metrics-20261012.json](../history/local_saved/d043ce350819/work/experiments/instruct-full-20261011/reports/format-conditioned-metrics-20261012.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "definitions": {
    "accuracy_all": "Correctness on all tasks; no format filtering.",
    "cost_condition": "Only records with the saved format_valid verdict true.",
    "depth": "Number of completed executable fork-to-merge rounds per format-valid task; serial valid tasks contribute zero.",
    "width": "Mean executed branch count across completed rounds within format-valid tasks; serial tasks have no width.",
    "forwards": "Physical generation model.forward calls for MATH500; reconstructed serial autoregressive calls for the two MATH64 evaluations, not instrumented.",
    "format_protocol_caveat": "MATH64 uses saved basic native Instruct format validation; MATH500 uses strict canonical counted Instruct validation. These protocols and task sets differ.",
    "rl_caveat": "R1/R2 step64 are previous 8-GPU controls trained on 128 tasks with cap2 and earlier training scorer, then rescored with corrected fullwidth8 evaluation. These are not results of the current 1024-task campaign.",
    "valid_format_and_fork_rate_all": "Count of tasks with format_valid=true AND at least one completed executable fork-to-merge round, divided by all evaluated tasks. Mathematical correctness is not part of this metric."
  },
  "models": [
    {
      "model": "Original Instruct",
      "suite": "MATH64 from mixed128",
      "total": 64,
      "correct": 45,
      "accuracy_all_pct": 70.3125,
      "valid_format_count": 7,
      "valid_format_pct": 10.9375,
      "accuracy_given_valid_format_pct": 100.0,
      "mean_F_given_valid_format": 1989,
      "median_F_given_valid_format": 1819,
      "mean_width_given_valid_format": null,
      "width_denominator_rounds": 0,
      "mean_rounds_given_valid_format": 0,
      "total_rounds_given_valid_format": 0,
      "max_rounds_given_valid_format": 0,
      "forked_tasks_given_valid_format": 0,
      "forked_task_fraction_given_valid_format": 0.0,
      "mean_sampled_tokens_given_valid_format": 1989,
      "forward_kind": "reconstructed serial AR forwards; not instrumented",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128",
      "valid_format_and_fork_count_all": 0,
      "valid_format_and_fork_rate_all_pct": 0.0
    },
    {
      "model": "Instruct +6token rows",
      "suite": "MATH64 from mixed128",
      "total": 64,
      "correct": 51,
      "accuracy_all_pct": 79.6875,
      "valid_format_count": 55,
      "valid_format_pct": 85.9375,
      "accuracy_given_valid_format_pct": 90.9090909090909,
      "mean_F_given_valid_format": 1189.9454545454546,
      "median_F_given_valid_format": 836,
      "mean_width_given_valid_format": null,
      "width_denominator_rounds": 0,
      "mean_rounds_given_valid_format": 0,
      "total_rounds_given_valid_format": 0,
      "max_rounds_given_valid_format": 0,
      "forked_tasks_given_valid_format": 0,
      "forked_task_fraction_given_valid_format": 0.0,
      "mean_sampled_tokens_given_valid_format": 1189.9454545454546,
      "forward_kind": "reconstructed serial AR forwards; not instrumented",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128",
      "valid_format_and_fork_count_all": 0,
      "valid_format_and_fork_rate_all_pct": 0.0
    },
    {
      "model": "Full SFT42",
      "suite": "MATH500",
      "total": 500,
      "correct": 251,
      "accuracy_all_pct": 50.2,
      "valid_format_count": 457,
      "valid_format_pct": 91.4,
      "accuracy_given_valid_format_pct": 51.64113785557987,
      "mean_F_given_valid_format": 716.8490153172867,
      "median_F_given_valid_format": 598,
      "mean_width_given_valid_format": 3.025586353944563,
      "width_denominator_rounds": 469,
      "mean_rounds_given_valid_format": 1.026258205689278,
      "total_rounds_given_valid_format": 469,
      "max_rounds_given_valid_format": 2,
      "forked_tasks_given_valid_format": 449,
      "forked_task_fraction_given_valid_format": 0.9824945295404814,
      "mean_sampled_tokens_given_valid_format": 943.7374179431072,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline",
      "valid_format_and_fork_count_all": 449,
      "valid_format_and_fork_rate_all_pct": 89.8
    },
    {
      "model": "RL R1 step64",
      "suite": "MATH500",
      "total": 500,
      "correct": 353,
      "accuracy_all_pct": 70.6,
      "valid_format_count": 277,
      "valid_format_pct": 55.4,
      "accuracy_given_valid_format_pct": 81.94945848375451,
      "mean_F_given_valid_format": 685.9025270758123,
      "median_F_given_valid_format": 546,
      "mean_width_given_valid_format": 2.2059925093632957,
      "width_denominator_rounds": 267,
      "mean_rounds_given_valid_format": 0.9638989169675091,
      "total_rounds_given_valid_format": 267,
      "max_rounds_given_valid_format": 1,
      "forked_tasks_given_valid_format": 267,
      "forked_task_fraction_given_valid_format": 0.9638989169675091,
      "mean_sampled_tokens_given_valid_format": 847.2274368231047,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064",
      "valid_format_and_fork_count_all": 267,
      "valid_format_and_fork_rate_all_pct": 53.4
    },
    {
      "model": "RL R2 step64",
      "suite": "MATH500",
      "total": 500,
      "correct": 280,
      "accuracy_all_pct": 56.0,
      "valid_format_count": 456,
      "valid_format_pct": 91.2,
      "accuracy_given_valid_format_pct": 58.1140350877193,
      "mean_F_given_valid_format": 656.813596491228,
      "median_F_given_valid_format": 546.0,
      "mean_width_given_valid_format": 4.382289416846652,
      "width_denominator_rounds": 463,
      "mean_rounds_given_valid_format": 1.0153508771929824,
      "total_rounds_given_valid_format": 463,
      "max_rounds_given_valid_format": 3,
      "forked_tasks_given_valid_format": 452,
      "forked_task_fraction_given_valid_format": 0.9912280701754386,
      "mean_sampled_tokens_given_valid_format": 1000.609649122807,
      "forward_kind": "instrumented physical generation forwards",
      "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064",
      "valid_format_and_fork_count_all": 452,
      "valid_format_and_fork_rate_all_pct": 90.4
    }
  ],
  "warmup_decoder_sha256": "0aa0a6233ac96e3d32ac00a51ddc71f3c394d6c7b2d8ff02e97f92d504206cb5",
  "audit_source": "format_conditioned_metrics.py"
}
```

</details>

## Графики

- [work/experiments/instruct-full-20261011/reports/matched128-distributions.pdf](../artifacts/work/experiments/instruct-full-20261011/reports/matched128-distributions.pdf) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/matched128-distributions.png](../artifacts/work/experiments/instruct-full-20261011/reports/matched128-distributions.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/rl-both-progress.pdf](../artifacts/work/experiments/instruct-full-20261011/reports/rl-both-progress.pdf) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/rl-both-progress.png](../artifacts/work/experiments/instruct-full-20261011/reports/rl-both-progress.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/rl-strong-width-progress.pdf](../artifacts/work/experiments/instruct-full-20261011/reports/rl-strong-width-progress.pdf) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/rl-strong-width-progress.png](../artifacts/work/experiments/instruct-full-20261011/reports/rl-strong-width-progress.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [work/experiments/instruct-full-20261011/evaluations/run_eval.sh](../artifacts/work/experiments/instruct-full-20261011/evaluations/run_eval.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-full-20261011/prepare.py](../artifacts/work/experiments/instruct-full-20261011/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-full-20261011/reports/format_conditioned_metrics.py](../artifacts/work/experiments/instruct-full-20261011/reports/format_conditioned_metrics.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-full-20261011/reports/plot_distributions.py](../artifacts/work/experiments/instruct-full-20261011/reports/plot_distributions.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/plot_rl_both.py](../artifacts/work/experiments/instruct-full-20261011/reports/plot_rl_both.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/instruct-full-20261011/reports/plot_rl_progress.py](../artifacts/work/experiments/instruct-full-20261011/reports/plot_rl_progress.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
