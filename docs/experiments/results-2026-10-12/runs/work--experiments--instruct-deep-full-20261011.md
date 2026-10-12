# work/experiments/instruct-deep-full-20261011

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/instruct-deep-full-20261011/plan.json](../artifacts/work/experiments/instruct-deep-full-20261011/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "CPU_source_draft_not_GPU_released",
  "root": "${PROJECT_ROOT}",
  "namespace": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011",
  "source_namespace": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011",
  "init_checkpoint": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "init_rationale": "Same fixed original Instruct warmup initialization as previous fullSFT; controlled data arm; no benchmark-driven checkpoint selection",
  "train_jsonl": "${PROJECT_ROOT}/work/experiments/deep-sft-20261011-instruct/production-v3/train.jsonl",
  "val_jsonl": "${PROJECT_ROOT}/work/experiments/deep-sft-20261011-instruct/production-v3/val.jsonl",
  "data_manifest": "${PROJECT_ROOT}/work/experiments/deep-sft-20261011-instruct/production-v3/data-manifest.json",
  "data_admission": "${PROJECT_ROOT}/work/experiments/deep-sft-20261011-instruct/production-v3/independent-final-admission-review.json",
  "teacher_drained": "${PROJECT_ROOT}/work/experiments/deep-sft-20261011-instruct/production-v3/teacher-drained-proof.json",
  "train_count": 2700,
  "val_count": 300,
  "lr": 1e-05,
  "global_batch": 64,
  "micro_batch_per_gpu": 1,
  "epochs": 3,
  "steps_per_epoch": 42,
  "total_steps": 126,
  "max_length": 8192,
  "smoke_steps": 2,
  "smoke_global_batch": 8,
  "smoke_choice": "longest ACTUAL compiler-token inputs,16train16val",
  "warmup_ratio": 0.1,
  "full_response_CE": true,
  "prompt_pad_loss_zero": true,
  "native_think": true,
  "native_eos": "<|im_end|>",
  "structured_sibling_attention": true,
  "repeated_sibling_positions": true,
  "checkpoint_observations": [
    42,
    84,
    126
  ],
  "selection_validation": "300 clean teacher-holdout fullresponseCE only; no MATH/128 selection",
  "quality_diagnostics": "Frozen matched128 optional later; separate from optimizer/reward/curriculum/model selection",
  "interpreter": "${PROJECT_ROOT}/.venv/bin/python",
  "gpu_lane": "existing_main_Sirius8_after_teacher_drain_no_new_allocation",
  "production_admission": "autonomous deterministic 2step finite/update/export/isolation actualGPU proof after source/staticrootreceipt and finaldataadmission",
  "main_hostname": "RUN_9c5b5b8949-mpimaster-0"
}
```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
  prompt_key: question
  response_key: answer
  prompt_dict_keys: null
  response_dict_keys: null
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
    path: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation
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
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/final

```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/final
    - trainer.experiment_name=Instruct-4B-full-isolation
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.0,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation,trainer.experiment_name=Instruct-4B-full-isolation,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=2,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_4b_instruct_deep
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/code
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
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra
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

- [work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/isolation/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/isolation/final
- trainer.experiment_name=Instruct-4B-full-isolation
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 64
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/val.parquet
  prompt_key: question
  response_key: answer
  prompt_dict_keys: null
  response_dict_keys: null
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
    path: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Instruct-4B-full-production
  total_epochs: 3
  total_training_steps: 126
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
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final

```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
    - trainer.total_epochs=3
    - trainer.total_training_steps=126
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final
    - trainer.experiment_name=Instruct-4B-full-production
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=64,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.1,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production,trainer.experiment_name=Instruct-4B-full-production,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final,trainer.logger=[console],trainer.total_epochs=3,trainer.total_training_steps=126,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_4b_instruct_deep
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/hydra
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

- [work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/production/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
- trainer.total_epochs=3
- trainer.total_training_steps=126
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final
- trainer.experiment_name=Instruct-4B-full-production
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/config.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
  prompt_key: question
  response_key: answer
  prompt_dict_keys: null
  response_dict_keys: null
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
    path: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke
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
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/final

```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
    - data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/final
    - trainer.experiment_name=Instruct-4B-full-smoke
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,data.custom_cls.name=InstructDataset,data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.0,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke,trainer.experiment_name=Instruct-4B-full-smoke,trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=2,ulysses_sequence_parallel_size=1,use_remove_padding=false
    id: ???
    num: ???
    config_name: sft_qwen3_4b_instruct_deep
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
    cwd: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra
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

- [work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/runs/smoke/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/data/smoke-val.parquet
- data.custom_cls.path=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/dataset.py
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
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/smoke/final
- trainer.experiment_name=Instruct-4B-full-smoke
- trainer.logger=[console]

```

</details>

- [work/experiments/instruct-deep-full-20261011/sft_qwen3_4b_instruct_deep.yaml](../artifacts/work/experiments/instruct-deep-full-20261011/sft_qwen3_4b_instruct_deep.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
defaults:
  - sft_trainer
  - _self_
data:
  max_length: 8192
  train_batch_size: 64
  micro_batch_size_per_gpu: 1
  num_workers: 0
  parallel_attention: true
  trim_padding: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final
  enable_gradient_checkpointing: true
  strategy: fsdp
  lora_rank: 0
trainer:
  project_name: Parallel-R1
  experiment_name: Instruct-4B-deep-full
  total_epochs: 3
  logger: [console]
  default_local_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production
  final_dir: ${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final

```

</details>

- [work/experiments/instruct-deep-full-20261011/system.txt](../artifacts/work/experiments/instruct-deep-full-20261011/system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/instruct-deep-full-20261011/controller-status.json](../artifacts/work/experiments/instruct-deep-full-20261011/controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "steps": 126,
  "epochs": 3,
  "clean_validation_ce": 0.045983172953128815,
  "production_result_sha256": "6e910d6a3871f20420c617efc8d752f86a5f8abd8ec3d9b351453cd94bd4c778",
  "production_export_proof_sha256": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
  "clean_validation_selection_sha256": "0fdb5ce8fa9107646b0b175452e8e1a685fbd7a1049a2b484993005c40ada0ad"
}
```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/production/metrics.jsonl](../artifacts/work/experiments/instruct-deep-full-20261011/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-deep-full-20261011/runs/production/result.json](../artifacts/work/experiments/instruct-deep-full-20261011/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 126,
  "epochs": 3,
  "val_loss": 0.045983172953128815,
  "full_model": true,
  "think_wrapped": true
}
```

</details>

- [work/experiments/instruct-deep-full-20261011/runs/smoke/metrics.jsonl](../artifacts/work/experiments/instruct-deep-full-20261011/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-deep-full-20261011/runs/smoke/result.json](../artifacts/work/experiments/instruct-deep-full-20261011/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 2,
  "epochs": 1,
  "val_loss": 0.24083822965621948,
  "full_model": true,
  "think_wrapped": true
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/instruct-deep-full-20261011/prepare.py](../artifacts/work/experiments/instruct-deep-full-20261011/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
