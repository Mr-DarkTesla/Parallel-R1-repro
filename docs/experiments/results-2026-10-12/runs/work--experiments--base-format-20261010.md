# work/experiments/base-format-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/manifest.json](../artifacts/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/base-format-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/base-format-20261010/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "a430b366b3f0b61bcf4cfc92f8a706ef2412fd2501b4dbb0eb68a074decc03df",
  "system_sha256": "9105d8b88ab3b7e8475a48ef979f67319cee6a1a805d5594d9f3d2d32de1be92",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "8a47fb71ce00121a7bb199fd65ec641b15518d902d8a868f693ae86f0aa81984",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3719d47cb2bc702394d89f901c5cbdc98ab2d2895224b2f661d8b00d384c687c",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/base-format-20261010/runs/production/hydra/.hydra/config.yaml](../artifacts/work/experiments/base-format-20261010/runs/production/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 64
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/base-format-20261010/data/train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/base-format-20261010/data/val.parquet
  prompt_key: problem
  response_key: response
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
    path: null
    name: null
  use_shm: false
  num_workers: 0
  parallel_attention: true
  prompt_messages_key: prompt_messages
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Base-4B-no-think-production
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
  final_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final

```

</details>

- [work/experiments/base-format-20261010/runs/production/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/base-format-20261010/runs/production/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=null
    - data.response_dict_keys=null
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.max_length=8192
    - data.truncation=error
    - data.trim_padding=true
    - data.train_batch_size=64
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=0
    - model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final
    - trainer.experiment_name=Base-4B-no-think-production
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.prompt_dict_keys=null,data.prompt_key=problem,data.response_dict_keys=null,data.response_key=response,data.train_batch_size=64,data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.1,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production,trainer.experiment_name=Base-4B-no-think-production,trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final,trainer.logger=[console],trainer.total_epochs=3,trainer.total_training_steps=126,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/base-format-20261010/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/base-format-20261010/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/hydra
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

- [work/experiments/base-format-20261010/runs/production/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/base-format-20261010/runs/production/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=null
- data.response_dict_keys=null
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.max_length=8192
- data.truncation=error
- data.trim_padding=true
- data.train_batch_size=64
- data.micro_batch_size_per_gpu=1
- data.num_workers=0
- model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final
- trainer.experiment_name=Base-4B-no-think-production
- trainer.logger=[console]

```

</details>

- [work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/config.yaml](../artifacts/work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-train.parquet
  val_files: ${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-val.parquet
  prompt_key: problem
  response_key: response
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
    path: null
    name: null
  use_shm: false
  num_workers: 0
  parallel_attention: true
  prompt_messages_key: prompt_messages
  defer_parallel_mask: true
model:
  partial_pretrain: ${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
  default_local_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Base-4B-no-think-smoke
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
  final_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/final

```

</details>

- [work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/hydra.yaml](../artifacts/work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-train.parquet
    - data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=null
    - data.response_dict_keys=null
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.max_length=8192
    - data.truncation=error
    - data.trim_padding=true
    - data.train_batch_size=8
    - data.micro_batch_size_per_gpu=1
    - data.num_workers=0
    - model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
    - trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke
    - trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/final
    - trainer.experiment_name=Base-4B-no-think-smoke
    - trainer.logger=[console]
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=8192,data.micro_batch_size_per_gpu=1,data.num_workers=0,data.prompt_dict_keys=null,data.prompt_key=problem,data.response_dict_keys=null,data.response_key=response,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-val.parquet,model.enable_gradient_checkpointing=true,model.fsdp_config.model_dtype=fp32,model.lora_rank=0,model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model,model.strategy=fsdp,optim.lr=1e-5,optim.warmup_steps_ratio=0.0,trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke,trainer.experiment_name=Base-4B-no-think-smoke,trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/final,trainer.logger=[console],trainer.total_epochs=1,trainer.total_training_steps=2,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/work/experiments/base-format-20261010/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/work/experiments/base-format-20261010/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/hydra
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

- [work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/overrides.yaml](../artifacts/work/experiments/base-format-20261010/runs/smoke/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-train.parquet
- data.val_files=${PROJECT_ROOT}/work/experiments/base-format-20261010/data/smoke-val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=null
- data.response_dict_keys=null
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.max_length=8192
- data.truncation=error
- data.trim_padding=true
- data.train_batch_size=8
- data.micro_batch_size_per_gpu=1
- data.num_workers=0
- model.partial_pretrain=${PROJECT_ROOT}/work/experiments/base-format-20261010/model
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
- trainer.default_local_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke
- trainer.final_dir=${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/final
- trainer.experiment_name=Base-4B-no-think-smoke
- trainer.logger=[console]

```

</details>

- [work/experiments/base-format-20261010/source-pin.json](../artifacts/work/experiments/base-format-20261010/source-pin.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-4B-Base",
  "revision": "906bfd4b4dc7f14ee4320094d8b41684abff8539"
}
```

</details>

- [work/experiments/base-format-20261010/system.txt](../artifacts/work/experiments/base-format-20261010/system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/base-format-20261010/attempts/01-wrong-interpreter/status.json](../artifacts/work/experiments/base-format-20261010/attempts/01-wrong-interpreter/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "full_model": true,
  "think_wrapped": false,
  "epochs": 3,
  "steps": 126,
  "lr": 1e-05,
  "eval_questions": 128,
  "host": "sirius",
  "gpus": 8,
  "at": "2026-10-10T10:45:04.600846+00:00",
  "active": "smoke",
  "active_pid": null,
  "error": "AssertionError(('smoke', 1))"
}
```

</details>

- [work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json](../artifacts/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 84,
  "pass_at_1_completed_only": 0.65625,
  "format_valid": 126,
  "format_fraction_completed_only": 0.984375,
  "executed_fork_samples": 120,
  "unfinished_thinking": 128,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 120,
  "parallel_protocol_fraction_completed_only": 0.9375,
  "gate_passed": true,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
  "parallel_syntax_valid": 126,
  "parallel_execution_mismatch_samples": 2,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 3,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 0,
  "legacy_format_fraction_completed_only": 0.0,
  "legacy_parallel_protocol_valid": 0,
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
    "executed_fork_samples": 120,
    "valid_parallel_among_fork_samples": 120,
    "invalid_width_samples": 2,
    "correct": 84
  },
  "fork_coverage": 0.9375,
  "valid_parallel_among_executed_forks": 1.0,
  "invalid_width_fraction": 0.015625,
  "correct_and_basic_valid": 84,
  "correct_and_parallel_valid": 78,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 60762.0,
      "mean": 474.703125,
      "median": 431.5,
      "p95": 942.8499999999996,
      "min": 158.0,
      "max": 1608.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 76330.0,
      "mean": 596.328125,
      "median": 532.0,
      "p95": 1124.1999999999998,
      "min": 158.0,
      "max": 1964.0
    },
    "T_forced": {
      "n": 128,
      "sum": 1272.0,
      "mean": 9.9375,
      "median": 9.0,
      "p95": 16.949999999999974,
      "min": 0.0,
      "max": 27.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 77602.0,
      "mean": 606.265625,
      "median": 542.5,
      "p95": 1133.1999999999998,
      "min": 158.0,
      "max": 1980.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 76330.0,
      "mean": 596.328125,
      "median": 532.0,
      "p95": 1124.1999999999998,
      "min": 158.0,
      "max": 1964.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 804.0,
      "mean": 6.28125,
      "median": 6.0,
      "p95": 8.649999999999991,
      "min": 1.0,
      "max": 16.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 2973.2823140621185,
      "mean": 23.2287680786103,
      "median": 20.97005271911621,
      "p95": 42.64241672754288,
      "min": 6.054238557815552,
      "max": 79.2642171382904
    },
    "forks": {
      "n": 128,
      "sum": 125.0,
      "mean": 0.9765625,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 3.0
    },
    "rounds": {
      "n": 128,
      "sum": 125.0,
      "mean": 0.9765625,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 3.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 253.0,
      "mean": 1.9765625,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 4.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 76330.0,
      "mean": 596.328125,
      "median": 532.0,
      "p95": 1124.1999999999998,
      "min": 158.0,
      "max": 1964.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 804.0,
      "mean": 6.28125,
      "median": 6.0,
      "p95": 8.649999999999991,
      "min": 1.0,
      "max": 16.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 75526.0,
      "mean": 590.046875,
      "median": 526.0,
      "p95": 1118.1999999999998,
      "min": 157.0,
      "max": 1956.0
    },
    "widths": {
      "n": 125,
      "sum": 299.0,
      "mean": 2.392,
      "median": 2.0,
      "p95": 4.0,
      "min": 2.0,
      "max": 6.0
    },
    "width_histogram": {
      "2": 88,
      "3": 29,
      "4": 5,
      "5": 2,
      "6": 1
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 2,
    "forked_samples": 120
  },
  "metrics_correct": {
    "F": {
      "n": 84,
      "sum": 35534.0,
      "mean": 423.0238095238095,
      "median": 395.0,
      "p95": 725.7499999999997,
      "min": 158.0,
      "max": 1169.0
    },
    "T_sampled": {
      "n": 84,
      "sum": 43927.0,
      "mean": 522.9404761904761,
      "median": 465.5,
      "p95": 910.3999999999996,
      "min": 158.0,
      "max": 1964.0
    },
    "T_forced": {
      "n": 84,
      "sum": 804.0,
      "mean": 9.571428571428571,
      "median": 9.0,
      "p95": 14.549999999999983,
      "min": 0.0,
      "max": 27.0
    },
    "T_assembled": {
      "n": 84,
      "sum": 44731.0,
      "mean": 532.5119047619048,
      "median": 474.5,
      "p95": 919.3999999999996,
      "min": 158.0,
      "max": 1979.0
    },
    "actual_generated_tokens": {
      "n": 84,
      "sum": 43927.0,
      "mean": 522.9404761904761,
      "median": 465.5,
      "p95": 910.3999999999996,
      "min": 158.0,
      "max": 1964.0
    },
    "generation_calls": {
      "n": 84,
      "sum": 514.0,
      "mean": 6.119047619047619,
      "median": 6.0,
      "p95": 7.849999999999994,
      "min": 1.0,
      "max": 16.0
    },
    "wall_seconds": {
      "n": 84,
      "sum": 1708.386519908905,
      "mean": 20.337934760820296,
      "median": 17.97675061225891,
      "p95": 34.4292883992195,
      "min": 6.054238557815552,
      "max": 78.82783246040344
    },
    "forks": {
      "n": 84,
      "sum": 81.0,
      "mean": 0.9642857142857143,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 3.0
    },
    "rounds": {
      "n": 84,
      "sum": 81.0,
      "mean": 0.9642857142857143,
      "median": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 3.0
    },
    "generation_turns": {
      "n": 84,
      "sum": 165.0,
      "mean": 1.9642857142857142,
      "median": 2.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 4.0
    },
    "model_forward_calls_inferred": {
      "n": 84,
      "sum": 43927.0,
      "mean": 522.9404761904761,
      "median": 465.5,
      "p95": 910.3999999999996,
      "min": 158.0,
      "max": 1964.0
    },
    "prefill_calls_inferred": {
      "n": 84,
      "sum": 514.0,
      "mean": 6.119047619047619,
      "median": 6.0,
      "p95": 7.849999999999994,
      "min": 1.0,
      "max": 16.0
    },
    "decode_calls_inferred": {
      "n": 84,
      "sum": 43413.0,
      "mean": 516.8214285714286,
      "median": 459.5,
      "p95": 904.3999999999996,
      "min": 157.0,
      "max": 1956.0
    },
    "widths": {
      "n": 81,
      "sum": 187.0,
      "mean": 2.308641975308642,
      "median": 2.0,
      "p95": 3.0,
      "min": 2.0,
      "max": 4.0
    },
    "width_histogram": {
      "2": 59,
      "3": 19,
      "4": 3
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 0,
    "forked_samples": 78
  },
  "historical_correct": 84,
  "historical_pass_at_1_completed_only": 0.65625,
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
      "correct": 46,
      "pass_at_1": 0.71875,
      "basic_valid": 64,
      "basic_valid_fraction": 1.0,
      "parallel_valid": 58,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 40,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 23761.0,
          "mean": 371.265625,
          "median": 337.5,
          "p95": 641.1499999999997,
          "min": 158.0,
          "max": 793.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 28734.0,
          "mean": 448.96875,
          "median": 400.5,
          "p95": 792.6499999999997,
          "min": 158.0,
          "max": 1044.0
        },
        "T_forced": {
          "n": 64,
          "sum": 615.0,
          "mean": 9.609375,
          "median": 9.0,
          "p95": 17.549999999999983,
          "min": 0.0,
          "max": 27.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 29349.0,
          "mean": 458.578125,
          "median": 411.0,
          "p95": 803.4499999999998,
          "min": 158.0,
          "max": 1056.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 28734.0,
          "mean": 448.96875,
          "median": 400.5,
          "p95": 792.6499999999997,
          "min": 158.0,
          "max": 1044.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 395.0,
          "mean": 6.171875,
          "median": 6.0,
          "p95": 10.549999999999983,
          "min": 1.0,
          "max": 16.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 1123.3120725154877,
          "mean": 17.551751133054495,
          "median": 15.90388536453247,
          "p95": 30.104123735427844,
          "min": 6.054238557815552,
          "max": 39.59783148765564
        },
        "forks": {
          "n": 64,
          "sum": 63.0,
          "mean": 0.984375,
          "median": 1.0,
          "p95": 1.8499999999999943,
          "min": 0.0,
          "max": 3.0
        },
        "rounds": {
          "n": 64,
          "sum": 63.0,
          "mean": 0.984375,
          "median": 1.0,
          "p95": 1.8499999999999943,
          "min": 0.0,
          "max": 3.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 127.0,
          "mean": 1.984375,
          "median": 2.0,
          "p95": 2.8499999999999943,
          "min": 1.0,
          "max": 4.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 28734.0,
          "mean": 448.96875,
          "median": 400.5,
          "p95": 792.6499999999997,
          "min": 158.0,
          "max": 1044.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 395.0,
          "mean": 6.171875,
          "median": 6.0,
          "p95": 10.549999999999983,
          "min": 1.0,
          "max": 16.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 28339.0,
          "mean": 442.796875,
          "median": 394.5,
          "p95": 785.7499999999997,
          "min": 157.0,
          "max": 1037.0
        },
        "widths": {
          "n": 63,
          "sum": 142.0,
          "mean": 2.253968253968254,
          "median": 2.0,
          "p95": 3.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 49,
          "3": 12,
          "4": 2
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 58
      },
      "metrics_correct": {
        "F": {
          "n": 46,
          "sum": 15718.0,
          "mean": 341.69565217391306,
          "median": 312.5,
          "p95": 566.25,
          "min": 158.0,
          "max": 793.0
        },
        "T_sampled": {
          "n": 46,
          "sum": 18839.0,
          "mean": 409.54347826086956,
          "median": 374.0,
          "p95": 734.5,
          "min": 158.0,
          "max": 948.0
        },
        "T_forced": {
          "n": 46,
          "sum": 417.0,
          "mean": 9.065217391304348,
          "median": 9.0,
          "p95": 14.25,
          "min": 0.0,
          "max": 27.0
        },
        "T_assembled": {
          "n": 46,
          "sum": 19256.0,
          "mean": 418.60869565217394,
          "median": 383.0,
          "p95": 754.0,
          "min": 158.0,
          "max": 975.0
        },
        "actual_generated_tokens": {
          "n": 46,
          "sum": 18839.0,
          "mean": 409.54347826086956,
          "median": 374.0,
          "p95": 734.5,
          "min": 158.0,
          "max": 948.0
        },
        "generation_calls": {
          "n": 46,
          "sum": 271.0,
          "mean": 5.891304347826087,
          "median": 6.0,
          "p95": 7.75,
          "min": 1.0,
          "max": 16.0
        },
        "wall_seconds": {
          "n": 46,
          "sum": 737.173052072525,
          "mean": 16.025501132011414,
          "median": 14.760244250297546,
          "p95": 27.80678755044937,
          "min": 6.054238557815552,
          "max": 36.34007668495178
        },
        "forks": {
          "n": 46,
          "sum": 43.0,
          "mean": 0.9347826086956522,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 3.0
        },
        "rounds": {
          "n": 46,
          "sum": 43.0,
          "mean": 0.9347826086956522,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 3.0
        },
        "generation_turns": {
          "n": 46,
          "sum": 89.0,
          "mean": 1.934782608695652,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 4.0
        },
        "model_forward_calls_inferred": {
          "n": 46,
          "sum": 18839.0,
          "mean": 409.54347826086956,
          "median": 374.0,
          "p95": 734.5,
          "min": 158.0,
          "max": 948.0
        },
        "prefill_calls_inferred": {
          "n": 46,
          "sum": 271.0,
          "mean": 5.891304347826087,
          "median": 6.0,
          "p95": 7.75,
          "min": 1.0,
          "max": 16.0
        },
        "decode_calls_inferred": {
          "n": 46,
          "sum": 18568.0,
          "mean": 403.6521739130435,
          "median": 368.0,
          "p95": 723.5,
          "min": 157.0,
          "max": 932.0
        },
        "widths": {
          "n": 43,
          "sum": 96.0,
          "mean": 2.2325581395348837,
          "median": 2.0,
          "p95": 3.0,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 34,
          "3": 8,
          "4": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 40
      },
      "historical_correct": 46,
      "historical_pass_at_1": 0.71875
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 38,
      "pass_at_1": 0.59375,
      "basic_valid": 62,
      "basic_valid_fraction": 0.96875,
      "parallel_valid": 62,
      "parallel_syntax_valid": 62,
      "parallel_execution_mismatch_samples": 2,
      "correct_and_basic_valid": 38,
      "correct_and_parallel_valid": 38,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 37001.0,
          "mean": 578.140625,
          "median": 503.5,
          "p95": 1001.7499999999999,
          "min": 264.0,
          "max": 1608.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 47596.0,
          "mean": 743.6875,
          "median": 641.0,
          "p95": 1319.4499999999996,
          "min": 264.0,
          "max": 1964.0
        },
        "T_forced": {
          "n": 64,
          "sum": 657.0,
          "mean": 10.265625,
          "median": 9.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 21.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 48253.0,
          "mean": 753.953125,
          "median": 651.5,
          "p95": 1330.9999999999995,
          "min": 264.0,
          "max": 1980.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 47596.0,
          "mean": 743.6875,
          "median": 641.0,
          "p95": 1319.4499999999996,
          "min": 264.0,
          "max": 1964.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 409.0,
          "mean": 6.390625,
          "median": 6.0,
          "p95": 8.0,
          "min": 2.0,
          "max": 10.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 1849.9702415466309,
          "mean": 28.905785024166107,
          "median": 25.988987803459167,
          "p95": 51.08578305244445,
          "min": 10.282099962234497,
          "max": 79.2642171382904
        },
        "forks": {
          "n": 64,
          "sum": 62.0,
          "mean": 0.96875,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 62.0,
          "mean": 0.96875,
          "median": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 126.0,
          "mean": 1.96875,
          "median": 2.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 47596.0,
          "mean": 743.6875,
          "median": 641.0,
          "p95": 1319.4499999999996,
          "min": 264.0,
          "max": 1964.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 409.0,
          "mean": 6.390625,
          "median": 6.0,
          "p95": 8.0,
          "min": 2.0,
          "max": 10.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 47187.0,
          "mean": 737.296875,
          "median": 634.5,
          "p95": 1312.5999999999995,
          "min": 262.0,
          "max": 1956.0
        },
        "widths": {
          "n": 62,
          "sum": 157.0,
          "mean": 2.532258064516129,
          "median": 2.0,
          "p95": 4.0,
          "min": 2.0,
          "max": 6.0
        },
        "width_histogram": {
          "2": 39,
          "3": 17,
          "4": 3,
          "5": 2,
          "6": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 2,
        "forked_samples": 62
      },
      "metrics_correct": {
        "F": {
          "n": 38,
          "sum": 19816.0,
          "mean": 521.4736842105264,
          "median": 474.5,
          "p95": 844.8499999999999,
          "min": 306.0,
          "max": 1169.0
        },
        "T_sampled": {
          "n": 38,
          "sum": 25088.0,
          "mean": 660.2105263157895,
          "median": 600.5,
          "p95": 970.5999999999997,
          "min": 376.0,
          "max": 1964.0
        },
        "T_forced": {
          "n": 38,
          "sum": 387.0,
          "mean": 10.18421052631579,
          "median": 9.0,
          "p95": 12.449999999999996,
          "min": 9.0,
          "max": 15.0
        },
        "T_assembled": {
          "n": 38,
          "sum": 25475.0,
          "mean": 670.3947368421053,
          "median": 609.5,
          "p95": 979.5999999999997,
          "min": 385.0,
          "max": 1979.0
        },
        "actual_generated_tokens": {
          "n": 38,
          "sum": 25088.0,
          "mean": 660.2105263157895,
          "median": 600.5,
          "p95": 970.5999999999997,
          "min": 376.0,
          "max": 1964.0
        },
        "generation_calls": {
          "n": 38,
          "sum": 243.0,
          "mean": 6.394736842105263,
          "median": 6.0,
          "p95": 7.149999999999999,
          "min": 6.0,
          "max": 8.0
        },
        "wall_seconds": {
          "n": 38,
          "sum": 971.21346783638,
          "mean": 25.558249153588946,
          "median": 23.367681980133057,
          "p95": 36.8399566411972,
          "min": 13.71924901008606,
          "max": 78.82783246040344
        },
        "forks": {
          "n": 38,
          "sum": 38.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "rounds": {
          "n": 38,
          "sum": 38.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 38,
          "sum": 76.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 38,
          "sum": 25088.0,
          "mean": 660.2105263157895,
          "median": 600.5,
          "p95": 970.5999999999997,
          "min": 376.0,
          "max": 1964.0
        },
        "prefill_calls_inferred": {
          "n": 38,
          "sum": 243.0,
          "mean": 6.394736842105263,
          "median": 6.0,
          "p95": 7.149999999999999,
          "min": 6.0,
          "max": 8.0
        },
        "decode_calls_inferred": {
          "n": 38,
          "sum": 24845.0,
          "mean": 653.8157894736842,
          "median": 594.5,
          "p95": 964.5999999999997,
          "min": 370.0,
          "max": 1956.0
        },
        "widths": {
          "n": 38,
          "sum": 91.0,
          "mean": 2.3947368421052633,
          "median": 2.0,
          "p95": 3.1499999999999986,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 25,
          "3": 11,
          "4": 2
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 38
      },
      "historical_correct": 38,
      "historical_pass_at_1": 0.59375
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
  "think_wrapped": false,
  "constrained_decoding": false,
  "base_format_schema_version": 1,
  "prompt_mode": "plain Instruction/Problem/Solution",
  "learned_parallel_measurement": "autonomous sampled Parallel opener and width; runtime injects Path headers and synchronization bridges",
  "system_file": "${PROJECT_ROOT}/work/experiments/base-format-20261010/system.txt",
  "provenance": {
    "evaluator_sha256": "a430b366b3f0b61bcf4cfc92f8a706ef2412fd2501b4dbb0eb68a074decc03df",
    "system_sha256": "9105d8b88ab3b7e8475a48ef979f67319cee6a1a805d5594d9f3d2d32de1be92",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "8a47fb71ce00121a7bb199fd65ec641b15518d902d8a868f693ae86f0aa81984",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3719d47cb2bc702394d89f901c5cbdc98ab2d2895224b2f661d8b00d384c687c",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "9105d8b88ab3b7e8475a48ef979f67319cee6a1a805d5594d9f3d2d32de1be92",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643
  ]
}
```

</details>

- [work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/worker-exits.json](../artifacts/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/base-format-20261010/final-report.json](../artifacts/work/experiments/base-format-20261010/final-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "verified_at": "2026-10-10T19:31:06.212773+00:00",
  "original_baseline_unchanged": true,
  "runs": {
    "original_instruct_native": {
      "accuracy_count": 98,
      "accuracy": 0.765625,
      "basic_valid": 55,
      "parallel_valid": 0,
      "correct_and_parallel_valid": 0,
      "fork_tasks": 0,
      "fork_task_fraction": 0.0,
      "actual_rounds": 0,
      "mean_rounds_per_task": 0.0,
      "actual_mean_width": null,
      "actual_width_histogram": {},
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 53,
          "parallel_valid": 0
        },
        "math": {
          "n": 64,
          "correct": 45,
          "parallel_valid": 0
        }
      },
      "format_schema_version": 2,
      "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
      "summary_path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": 0.0
    },
    "base_full_sft_no_think": {
      "accuracy_count": 84,
      "accuracy": 0.65625,
      "basic_valid": 126,
      "parallel_valid": 120,
      "correct_and_parallel_valid": 78,
      "fork_tasks": 120,
      "fork_task_fraction": 0.9375,
      "actual_rounds": 125,
      "mean_rounds_per_task": 0.9765625,
      "actual_mean_width": 2.392,
      "actual_width_histogram": {
        "2": 88,
        "3": 29,
        "4": 5,
        "5": 2,
        "6": 1
      },
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 46,
          "parallel_valid": 58
        },
        "math": {
          "n": 64,
          "correct": 38,
          "parallel_valid": 62
        }
      },
      "format_schema_version": 3,
      "model": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
      "summary_path": "${PROJECT_ROOT}/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": -10.9375
    },
    "weighted_instruct_guard": {
      "accuracy_count": 82,
      "accuracy": 0.640625,
      "basic_valid": 85,
      "parallel_valid": 0,
      "correct_and_parallel_valid": 0,
      "fork_tasks": 1,
      "fork_task_fraction": 0.0078125,
      "actual_rounds": 1,
      "mean_rounds_per_task": 0.0078125,
      "actual_mean_width": 2.0,
      "actual_width_histogram": {
        "2": 1
      },
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 44,
          "parallel_valid": 0
        },
        "math": {
          "n": 64,
          "correct": 38,
          "parallel_valid": 0
        }
      },
      "format_schema_version": 2,
      "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
      "summary_path": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": -12.5
    },
    "weighted_instruct_fewshot_guard": {
      "accuracy_count": 98,
      "accuracy": 0.765625,
      "basic_valid": 102,
      "parallel_valid": 0,
      "correct_and_parallel_valid": 0,
      "fork_tasks": 0,
      "fork_task_fraction": 0.0,
      "actual_rounds": 0,
      "mean_rounds_per_task": 0.0,
      "actual_mean_width": null,
      "actual_width_histogram": {},
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 49,
          "parallel_valid": 0
        },
        "math": {
          "n": 64,
          "correct": 49,
          "parallel_valid": 0
        }
      },
      "format_schema_version": 2,
      "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
      "summary_path": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": 0.0
    },
    "original_instruct_hf_diagnostic": {
      "accuracy_count": 95,
      "accuracy": 0.7421875,
      "basic_valid": 52,
      "parallel_valid": 0,
      "correct_and_parallel_valid": 0,
      "fork_tasks": 0,
      "fork_task_fraction": 0.0,
      "actual_rounds": 0,
      "mean_rounds_per_task": 0.0,
      "actual_mean_width": null,
      "actual_width_histogram": {},
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 50,
          "parallel_valid": 0
        },
        "math": {
          "n": 64,
          "correct": 45,
          "parallel_valid": 0
        }
      },
      "format_schema_version": 2,
      "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
      "summary_path": "${PROJECT_ROOT}/work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": -2.34375
    },
    "old_sft_instruct_guard": {
      "accuracy_count": 104,
      "accuracy": 0.8125,
      "basic_valid": 103,
      "parallel_valid": 1,
      "correct_and_parallel_valid": 1,
      "fork_tasks": 2,
      "fork_task_fraction": 0.015625,
      "actual_rounds": 2,
      "mean_rounds_per_task": 0.015625,
      "actual_mean_width": 3.0,
      "actual_width_histogram": {
        "2": 1,
        "4": 1
      },
      "by_dataset": {
        "gsm": {
          "n": 64,
          "correct": 53,
          "parallel_valid": 0
        },
        "math": {
          "n": 64,
          "correct": 51,
          "parallel_valid": 1
        }
      },
      "format_schema_version": 2,
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
      "summary_path": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json",
      "delta_vs_fixed_original_baseline_pp": 4.6875
    }
  },
  "source_sha256": {
    "work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json": "bbae2ec1481d306742a1c9a88c9c7583c7662e98c48391d02e76c062aaf550ec",
    "work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/scores.jsonl": "935ab03361779768dae09e20db61bc5b6450f37548b25983fa9cf1cefa06c9d0",
    "work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/manifest.json": "d6b0dc2b537d77997a075d3fe04fd9a19819a72150c2c4b61c142dd37592c273",
    "work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json": "afab658268e7fb75549b73c3c343f2fc16189d38ca5bd259608d8019c76b41b0",
    "work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/scores.jsonl": "9d33de966d5909e2ffc8cfe9bb8000be8bd8e529257c616fdb591a39135e53be",
    "work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/manifest.json": "c644bd6df9db8b02e452f46fadbb92a046437de5932f87b597cec37bfaf891a4",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json": "0355cb42065c43c6a379ec415048da9342f6c58538f0e5469ac65d7505bee5f5",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/scores.jsonl": "53c356e7cceb2a8785d34f0cbef93286a55ca1794e262370233ab720afdbe3bd",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/manifest.json": "098550256a16bce54227bb3e7ee69dd874dcc87946990cb04349bfc41a4936b2",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/summary.json": "092be5405978d3c5487b0db4ad52c49590af69c852bc29f032b231e7dfe98232",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/scores.jsonl": "6a18c5e242cbc63d1907ef9668a6968e4e9c9b84406227f46b6279bf94e1260f",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/manifest.json": "37084f159cfbf361b84e3f93589cb34cf86aab64e0a4ca503b138cdcfb0effaa",
    "work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/summary.json": "553a1306ce6fa95cccb1305335fd8ca252ab9a98c1b70d6bade7f2e47ebe2075",
    "work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/scores.jsonl": "601e4a2eca5fc4bb151c854d24637293417aafb8d71470f29fb4a9ca62f6fd5a",
    "work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/manifest.json": "15633f57a768462b5ad0d8f164636725ecb0f97e41d02091a9be9e9c2f88de12",
    "work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json": "011af451839f8effacd75c752d6b93125b5f0f8e86f6af5c62450332203fb5a6",
    "work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/scores.jsonl": "bff2d5b01f9dbf899335a7dddcfaacb41cbf5221330ee7919894a3fa009597fa",
    "work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/worker-exits.json": "7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6",
    "work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/manifest.json": "5214b94934ca2d24fe42b19cb685918169acbe644e402d92c758254369958afb"
  },
  "comparison_limit": "Same fixed questions/scorer; model family, prompt and runtime differ. Accuracy delta is a target comparison, not a causal estimate of SFT degradation.",
  "curriculum_selection_allowed": false,
  "checkpoint_selection_allowed": false,
  "paired_outcomes": {
    "baseline_only_correct": 26,
    "base_only_correct": 12,
    "both_correct": 72,
    "both_wrong": 18
  },
  "autonomy_proof": {
    "forced_think_prefix_tokens": 0,
    "sampled_parallel_openers": 127,
    "constrained_decoding": false,
    "runtime_forced": "Path IDs/headers and synchronization bridges; Plan, Parallel opener and width sampled"
  },
  "training": {
    "state": "complete",
    "steps": 126,
    "epochs": 3,
    "val_loss": 0.3373735249042511,
    "full_model": true,
    "think_wrapped": false,
    "finite_optimizer_steps": 126,
    "sampled_backbone_positive_updates": 125,
    "initial_zero_update": "First optimizer step has zero LR during warmup",
    "validation_losses": [
      0.37333112955093384,
      0.34007543325424194,
      0.3373735249042511
    ]
  },
  "trace_observations": [
    {
      "id": "math_train/prealgebra/566",
      "finding": "Both paths compute correct GCD/factorizations; Summary incorrectly evaluates 8*9*37 as 2952 instead of 2664.",
      "format_valid": true,
      "parallel_valid": true,
      "reference_answer": "2664",
      "extracted_answer": "2952"
    },
    {
      "id": "math_train/algebra/1558",
      "finding": "Plan asks for endpoint sum rather than decline; 450000+500 replaces required 450000-500.",
      "format_valid": true,
      "parallel_valid": true,
      "reference_answer": "112,\\!875",
      "extracted_answer": "112125"
    },
    {
      "id": "gsm_infinite_ops4/ops4/510",
      "finding": "Path correctly computes 5-3=2, labels it non-owl; Summary subtracts 3 again and answers -1.",
      "format_valid": true,
      "parallel_valid": true,
      "reference_answer": "2",
      "extracted_answer": "-1"
    },
    {
      "id": "math_train/algebra/786",
      "finding": "Plan creates a trivial zero branch; another branch reverses the wrong interval endpoints under negation.",
      "format_valid": true,
      "parallel_valid": true,
      "reference_answer": "(-1,0]",
      "extracted_answer": "[-1,0)"
    }
  ],
  "objective_assessment": {
    "autonomous_format_learned": true,
    "accuracy_retention_met": false,
    "note": "Base fork coverage 93.75%, but 84/128 vs original Instruct98/128; syntax validity does not prove useful independent computations."
  }
}
```

</details>

- [work/experiments/base-format-20261010/runs/production/metrics.jsonl](../artifacts/work/experiments/base-format-20261010/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/runs/production/result.json](../artifacts/work/experiments/base-format-20261010/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 126,
  "epochs": 3,
  "val_loss": 0.3373735249042511,
  "full_model": true,
  "think_wrapped": false
}
```

</details>

- [work/experiments/base-format-20261010/runs/smoke/metrics.jsonl](../artifacts/work/experiments/base-format-20261010/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/runs/smoke/result.json](../artifacts/work/experiments/base-format-20261010/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "steps": 2,
  "epochs": 1,
  "val_loss": 0.810695469379425,
  "full_model": true,
  "think_wrapped": false
}
```

</details>

- [work/experiments/base-format-20261010/statistics/all-experiments.json](../artifacts/work/experiments/base-format-20261010/statistics/all-experiments.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "verified_at": "2026-10-10T20:05:10.019864+00:00",
  "fixed_original_native_baseline": 98,
  "records": [
    {
      "name": "base-no-think-unconstrained-128",
      "completed": 128,
      "correct": 84,
      "accuracy": 0.65625,
      "fork_tasks": 120,
      "fork_fraction": 0.9375,
      "actual_rounds": 125,
      "actual_width": {
        "n": 125,
        "mean": 2.392,
        "median": 2.0,
        "p95": 4.0,
        "max": 6.0
      },
      "width_histogram": {
        "2": 88,
        "4": 5,
        "3": 29,
        "5": 2,
        "6": 1
      },
      "basic_valid": 126,
      "format_fraction": 0.984375,
      "parallel_valid": 120,
      "correct_and_parallel": 78,
      "by_dataset": {
        "gsm": {
          "correct": 46,
          "n": 64
        },
        "math": {
          "correct": 38,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 596.328125,
        "median": 532.0,
        "p95": 1124.1999999999998,
        "max": 1964.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 474.703125,
        "median": 431.5,
        "p95": 942.8499999999996,
        "max": 1608.0
      },
      "format_schema": 3,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json"
    },
    {
      "name": "original-instruct-thinking-hf-128",
      "completed": 128,
      "correct": 95,
      "accuracy": 0.7421875,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 52,
      "format_fraction": 0.40625,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 50,
          "n": 64
        },
        "math": {
          "correct": 45,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2794.96875,
        "median": 2626.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2794.96875,
        "median": 2626.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "native_thinking_HF_serial_SDPA"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
      "source": "${PROJECT_ROOT}/work/experiments/format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128/summary.json"
    },
    {
      "name": "baseline-lr-5e-4-constrained-128",
      "completed": 128,
      "correct": 104,
      "accuracy": 0.8125,
      "fork_tasks": 2,
      "fork_fraction": 0.015625,
      "actual_rounds": 2,
      "actual_width": {
        "n": 2,
        "mean": 3.0,
        "median": 3.0,
        "p95": 3.9,
        "max": 4.0
      },
      "width_histogram": {
        "2": 1,
        "4": 1
      },
      "basic_valid": 103,
      "format_fraction": 0.8046875,
      "parallel_valid": 1,
      "correct_and_parallel": 1,
      "by_dataset": {
        "gsm": {
          "correct": 53,
          "n": 64
        },
        "math": {
          "correct": 51,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 1853.6484375,
        "median": 1278.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 1843.015625,
        "median": 1278.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json"
    },
    {
      "name": "weighted-format-constrained-128",
      "completed": 128,
      "correct": 82,
      "accuracy": 0.640625,
      "fork_tasks": 1,
      "fork_fraction": 0.0078125,
      "actual_rounds": 1,
      "actual_width": {
        "n": 1,
        "mean": 2.0,
        "median": 2.0,
        "p95": 2.0,
        "max": 2.0
      },
      "width_histogram": {
        "2": 1
      },
      "basic_valid": 85,
      "format_fraction": 0.6640625,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 44,
          "n": 64
        },
        "math": {
          "correct": 38,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2448.6875,
        "median": 2159.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2448.5859375,
        "median": 2159.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json"
    },
    {
      "name": "weighted-format-fewshot-128",
      "completed": 128,
      "correct": 98,
      "accuracy": 0.765625,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 102,
      "format_fraction": 0.796875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 49,
          "n": 64
        },
        "math": {
          "correct": 49,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 1889.1484375,
        "median": 1422.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 1889.1484375,
        "median": 1422.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/summary.json"
    },
    {
      "name": "initial-structured-128",
      "completed": 128,
      "correct": 106,
      "accuracy": 0.828125,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 103,
      "format_fraction": 0.8046875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 54,
          "n": 64
        },
        "math": {
          "correct": 52,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2064.484375,
        "median": 1815.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2064.484375,
        "median": 1815.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/summary.json"
    },
    {
      "name": "lr-1e-3-trained-native-128",
      "completed": 128,
      "correct": 98,
      "accuracy": 0.765625,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 55,
      "format_fraction": 0.4296875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 53,
          "n": 64
        },
        "math": {
          "correct": 45,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "native_vllm_fast"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/summary.json"
    },
    {
      "name": "lr-1e-3-trained-structured-128",
      "completed": 128,
      "correct": 90,
      "accuracy": 0.703125,
      "fork_tasks": 5,
      "fork_fraction": 0.0390625,
      "actual_rounds": 5,
      "actual_width": {
        "n": 5,
        "mean": 4.0,
        "median": 4.0,
        "p95": 6.3999999999999995,
        "max": 7.0
      },
      "width_histogram": {
        "4": 2,
        "7": 1,
        "2": 1,
        "3": 1
      },
      "basic_valid": 90,
      "format_fraction": 0.703125,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 49,
          "n": 64
        },
        "math": {
          "correct": 41,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 1425.203125,
        "median": 946.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 1407.2578125,
        "median": 946.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/summary.json"
    },
    {
      "name": "lr-2e-4-trained-native-128",
      "completed": 128,
      "correct": 98,
      "accuracy": 0.765625,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 55,
      "format_fraction": 0.4296875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 53,
          "n": 64
        },
        "math": {
          "correct": 45,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "native_vllm_fast"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/summary.json"
    },
    {
      "name": "lr-2e-4-trained-structured-128",
      "completed": 128,
      "correct": 81,
      "accuracy": 0.6328125,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 73,
      "format_fraction": 0.5703125,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 44,
          "n": 64
        },
        "math": {
          "correct": 37,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 1942.390625,
        "median": 1489.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 1942.390625,
        "median": 1489.5,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "hf_structured_serial_backend"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/summary.json"
    },
    {
      "name": "original-native-128",
      "completed": 128,
      "correct": 98,
      "accuracy": 0.765625,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 55,
      "format_fraction": 0.4296875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 53,
          "n": 64
        },
        "math": {
          "correct": 45,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "native_vllm_fast"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json"
    },
    {
      "name": "trained-native-128",
      "completed": 128,
      "correct": 98,
      "accuracy": 0.765625,
      "fork_tasks": 0,
      "fork_fraction": 0.0,
      "actual_rounds": 0,
      "actual_width": {
        "n": 0,
        "mean": null,
        "median": null,
        "p95": null,
        "max": null
      },
      "width_histogram": {},
      "basic_valid": 55,
      "format_fraction": 0.4296875,
      "parallel_valid": 0,
      "correct_and_parallel": 0,
      "by_dataset": {
        "gsm": {
          "correct": 53,
          "n": 64
        },
        "math": {
          "correct": 45,
          "n": 64
        }
      },
      "sampled_tokens": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "critical_depth": {
        "n": 128,
        "mean": 2791.5703125,
        "median": 2753.0,
        "p95": 4094.0,
        "max": 4094.0
      },
      "format_schema": 2,
      "backend": [
        "native_vllm_fast"
      ],
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/summary.json"
    }
  ],
  "training": [
    {
      "label": "LR5e-4",
      "steps": 129,
      "epochs": 3,
      "val_loss": 0.8435613149404526,
      "trainable_parameters": 15360,
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production"
    },
    {
      "label": "LR1e-3",
      "steps": 129,
      "epochs": 3,
      "val_loss": 0.8052124019463857,
      "trainable_parameters": 15360,
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production"
    },
    {
      "label": "LR2e-4",
      "steps": 129,
      "epochs": 3,
      "val_loss": 1.1880315870046616,
      "trainable_parameters": 15360,
      "source": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production"
    },
    {
      "label": "Format x5",
      "steps": 129,
      "epochs": 3,
      "val_loss": 1.1032854282855988,
      "trainable_parameters": 15360,
      "source": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production"
    },
    {
      "label": "Base full",
      "steps": 126,
      "epochs": 3,
      "val_loss": 0.3373735249042511,
      "trainable_parameters": 4022468096,
      "source": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production"
    }
  ],
  "limits": [
    "Native, old structured, new guard, and no-think Base have different protocols and format schemas.",
    "Old summary regex widths replaced by actual policy path-call groups.",
    "No scores pooled across modes; native XML format score is not a native-quality criterion."
  ]
}
```

</details>

- [work/experiments/base-format-20261010/statistics/statistics.json](../artifacts/work/experiments/base-format-20261010/statistics/statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "verified_at": "2026-10-10T20:05:08.814937+00:00",
  "n": 128,
  "user_accepts_current_accuracy_tradeoff": true,
  "original_baseline": {
    "correct": 98,
    "n": 128,
    "accuracy": 0.765625
  },
  "accuracy": {
    "correct": 84,
    "n": 128,
    "fraction": 0.65625,
    "delta_pp": -10.9375
  },
  "fork_coverage": {
    "tasks": 120,
    "n": 128,
    "fraction": 0.9375
  },
  "basic_format": {
    "valid": 126,
    "n": 128,
    "fraction": 0.984375
  },
  "canonical_parallel": {
    "valid": 120,
    "n": 128,
    "fraction": 0.9375
  },
  "correct_and_parallel": {
    "count": 78,
    "n": 128,
    "fraction": 0.609375,
    "among_forked": 0.65
  },
  "rounds_histogram": {
    "0": 8,
    "1": 116,
    "2": 3,
    "3": 1
  },
  "width_histogram": {
    "2": 88,
    "3": 29,
    "4": 5,
    "5": 2,
    "6": 1
  },
  "width": {
    "n": 125,
    "sum": 299.0,
    "mean": 2.392,
    "median": 2.0,
    "p25": 2.0,
    "p75": 3.0,
    "p90": 3.0,
    "p95": 4.0,
    "min": 2.0,
    "max": 6.0
  },
  "branch_sampled_tokens": {
    "n": 299,
    "sum": 34834.0,
    "mean": 116.50167224080268,
    "median": 84.0,
    "p25": 60.0,
    "p75": 142.5,
    "p90": 212.79999999999995,
    "p95": 292.1999999999989,
    "min": 21.0,
    "max": 908.0
  },
  "metrics": {
    "fork_rounds": {
      "n": 128,
      "sum": 125.0,
      "mean": 0.9765625,
      "median": 1.0,
      "p25": 1.0,
      "p75": 1.0,
      "p90": 1.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 3.0
    },
    "critical_depth": {
      "n": 128,
      "sum": 60762.0,
      "mean": 474.703125,
      "median": 431.5,
      "p25": 324.75,
      "p75": 551.5,
      "p90": 742.3999999999999,
      "p95": 942.8499999999996,
      "min": 158.0,
      "max": 1608.0
    },
    "sampled_tokens": {
      "n": 128,
      "sum": 76330.0,
      "mean": 596.328125,
      "median": 532.0,
      "p25": 386.25,
      "p75": 719.25,
      "p90": 963.6999999999999,
      "p95": 1124.1999999999998,
      "min": 158.0,
      "max": 1964.0
    },
    "forced_tokens": {
      "n": 128,
      "sum": 1272.0,
      "mean": 9.9375,
      "median": 9.0,
      "p25": 9.0,
      "p75": 12.0,
      "p90": 12.0,
      "p95": 16.949999999999974,
      "min": 0.0,
      "max": 27.0
    },
    "assembled_tokens": {
      "n": 128,
      "sum": 77602.0,
      "mean": 606.265625,
      "median": 542.5,
      "p25": 395.25,
      "p75": 729.0,
      "p90": 983.3999999999999,
      "p95": 1133.1999999999998,
      "min": 158.0,
      "max": 1980.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 804.0,
      "mean": 6.28125,
      "median": 6.0,
      "p25": 6.0,
      "p75": 7.0,
      "p90": 7.0,
      "p95": 8.649999999999991,
      "min": 1.0,
      "max": 16.0
    },
    "path_calls": {
      "n": 128,
      "sum": 299.0,
      "mean": 2.3359375,
      "median": 2.0,
      "p25": 2.0,
      "p75": 3.0,
      "p90": 3.0,
      "p95": 4.0,
      "min": 0.0,
      "max": 6.0
    },
    "elapsed_seconds": {
      "n": 128,
      "sum": 2973.2823140621185,
      "mean": 23.2287680786103,
      "median": 20.97005271911621,
      "p25": 14.828881800174713,
      "p75": 28.122509360313416,
      "p90": 37.073436760902396,
      "p95": 42.64241672754288,
      "min": 6.054238557815552,
      "max": 79.2642171382904
    },
    "logical_work_over_depth": {
      "n": 128,
      "sum": 158.08964620572567,
      "mean": 1.2350753609822318,
      "median": 1.2033910229351343,
      "p25": 1.1504402460068137,
      "p75": 1.2722844243792326,
      "p90": 1.4289088283828382,
      "p95": 1.533363960086834,
      "min": 1.0,
      "max": 2.150384193194292
    }
  },
  "by_correctness": {
    "True": {
      "n": 84,
      "metrics": {
        "fork_rounds": {
          "n": 84,
          "sum": 81.0,
          "mean": 0.9642857142857143,
          "median": 1.0,
          "p25": 1.0,
          "p75": 1.0,
          "p90": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 3.0
        },
        "critical_depth": {
          "n": 84,
          "sum": 35534.0,
          "mean": 423.0238095238095,
          "median": 395.0,
          "p25": 304.5,
          "p75": 501.75,
          "p90": 656.8000000000001,
          "p95": 725.7499999999997,
          "min": 158.0,
          "max": 1169.0
        },
        "sampled_tokens": {
          "n": 84,
          "sum": 43927.0,
          "mean": 522.9404761904761,
          "median": 465.5,
          "p25": 361.5,
          "p75": 636.25,
          "p90": 797.6,
          "p95": 910.3999999999996,
          "min": 158.0,
          "max": 1964.0
        },
        "forced_tokens": {
          "n": 84,
          "sum": 804.0,
          "mean": 9.571428571428571,
          "median": 9.0,
          "p25": 9.0,
          "p75": 12.0,
          "p90": 12.0,
          "p95": 14.549999999999983,
          "min": 0.0,
          "max": 27.0
        },
        "assembled_tokens": {
          "n": 84,
          "sum": 44731.0,
          "mean": 532.5119047619048,
          "median": 474.5,
          "p25": 371.25,
          "p75": 645.25,
          "p90": 807.5,
          "p95": 919.3999999999996,
          "min": 158.0,
          "max": 1979.0
        },
        "generation_calls": {
          "n": 84,
          "sum": 514.0,
          "mean": 6.119047619047619,
          "median": 6.0,
          "p25": 6.0,
          "p75": 7.0,
          "p90": 7.0,
          "p95": 7.849999999999994,
          "min": 1.0,
          "max": 16.0
        },
        "path_calls": {
          "n": 84,
          "sum": 187.0,
          "mean": 2.2261904761904763,
          "median": 2.0,
          "p25": 2.0,
          "p75": 3.0,
          "p90": 3.0,
          "p95": 3.8499999999999943,
          "min": 0.0,
          "max": 6.0
        },
        "elapsed_seconds": {
          "n": 84,
          "sum": 1708.386519908905,
          "mean": 20.337934760820296,
          "median": 17.97675061225891,
          "p25": 14.290162205696106,
          "p75": 24.887727439403534,
          "p90": 30.68575713634491,
          "p95": 34.4292883992195,
          "min": 6.054238557815552,
          "max": 78.82783246040344
        },
        "logical_work_over_depth": {
          "n": 84,
          "sum": 102.0254224201818,
          "mean": 1.2145883621450213,
          "median": 1.2050543784948444,
          "p25": 1.162798036465638,
          "p75": 1.2533514986376022,
          "p90": 1.3369211409395974,
          "p95": 1.397223116892188,
          "min": 1.0,
          "max": 1.6800684345594525
        }
      },
      "widths": {
        "n": 81,
        "sum": 187.0,
        "mean": 2.308641975308642,
        "median": 2.0,
        "p25": 2.0,
        "p75": 3.0,
        "p90": 3.0,
        "p95": 3.0,
        "min": 2.0,
        "max": 4.0
      }
    },
    "False": {
      "n": 44,
      "metrics": {
        "fork_rounds": {
          "n": 44,
          "sum": 44.0,
          "mean": 1.0,
          "median": 1.0,
          "p25": 1.0,
          "p75": 1.0,
          "p90": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "critical_depth": {
          "n": 44,
          "sum": 25228.0,
          "mean": 573.3636363636364,
          "median": 485.0,
          "p25": 363.25,
          "p75": 708.75,
          "p90": 971.2,
          "p95": 1001.75,
          "min": 242.0,
          "max": 1608.0
        },
        "sampled_tokens": {
          "n": 44,
          "sum": 32403.0,
          "mean": 736.4318181818181,
          "median": 669.0,
          "p25": 432.0,
          "p75": 961.75,
          "p90": 1146.3000000000002,
          "p95": 1319.45,
          "min": 264.0,
          "max": 1959.0
        },
        "forced_tokens": {
          "n": 44,
          "sum": 468.0,
          "mean": 10.636363636363637,
          "median": 9.0,
          "p25": 9.0,
          "p75": 12.0,
          "p90": 17.10000000000001,
          "p95": 18.0,
          "min": 0.0,
          "max": 21.0
        },
        "assembled_tokens": {
          "n": 44,
          "sum": 32871.0,
          "mean": 747.0681818181819,
          "median": 681.0,
          "p25": 447.75,
          "p75": 973.75,
          "p90": 1155.3000000000002,
          "p95": 1331.0,
          "min": 264.0,
          "max": 1980.0
        },
        "generation_calls": {
          "n": 44,
          "sum": 290.0,
          "mean": 6.590909090909091,
          "median": 6.0,
          "p25": 6.0,
          "p75": 7.0,
          "p90": 8.700000000000003,
          "p95": 9.850000000000001,
          "min": 2.0,
          "max": 11.0
        },
        "path_calls": {
          "n": 44,
          "sum": 112.0,
          "mean": 2.5454545454545454,
          "median": 2.0,
          "p25": 2.0,
          "p75": 3.0,
          "p90": 4.0,
          "p95": 4.850000000000001,
          "min": 0.0,
          "max": 6.0
        },
        "elapsed_seconds": {
          "n": 44,
          "sum": 1264.8957941532135,
          "mean": 28.747631685300306,
          "median": 25.898893237113953,
          "p25": 16.9070885181427,
          "p75": 36.909546077251434,
          "p90": 44.384861826896675,
          "p95": 51.08578305244446,
          "min": 10.282099962234497,
          "max": 79.2642171382904
        },
        "logical_work_over_depth": {
          "n": 44,
          "sum": 56.06422378554385,
          "mean": 1.2741869042169058,
          "median": 1.1882733665129446,
          "p25": 1.134093824445666,
          "p75": 1.3943151163467697,
          "p90": 1.5236503167337394,
          "p95": 1.5964447640232933,
          "min": 1.0,
          "max": 2.150384193194292
        }
      },
      "widths": {
        "n": 44,
        "sum": 112.0,
        "mean": 2.5454545454545454,
        "median": 2.0,
        "p25": 2.0,
        "p75": 3.0,
        "p90": 3.700000000000003,
        "p95": 4.850000000000001,
        "min": 2.0,
        "max": 6.0
      }
    }
  },
  "by_dataset": {
    "gsm": {
      "n": 64,
      "correct": 46,
      "fork_tasks": 58,
      "basic_valid": 64,
      "metrics": {
        "fork_rounds": {
          "n": 64,
          "sum": 63.0,
          "mean": 0.984375,
          "median": 1.0,
          "p25": 1.0,
          "p75": 1.0,
          "p90": 1.0,
          "p95": 1.8499999999999943,
          "min": 0.0,
          "max": 3.0
        },
        "critical_depth": {
          "n": 64,
          "sum": 23761.0,
          "mean": 371.265625,
          "median": 337.5,
          "p25": 270.75,
          "p75": 442.25,
          "p90": 556.7,
          "p95": 641.1499999999997,
          "min": 158.0,
          "max": 793.0
        },
        "sampled_tokens": {
          "n": 64,
          "sum": 28734.0,
          "mean": 448.96875,
          "median": 400.5,
          "p25": 331.0,
          "p75": 549.0,
          "p90": 692.0,
          "p95": 792.6499999999997,
          "min": 158.0,
          "max": 1044.0
        },
        "forced_tokens": {
          "n": 64,
          "sum": 615.0,
          "mean": 9.609375,
          "median": 9.0,
          "p25": 9.0,
          "p75": 12.0,
          "p90": 12.0,
          "p95": 17.549999999999983,
          "min": 0.0,
          "max": 27.0
        },
        "assembled_tokens": {
          "n": 64,
          "sum": 29349.0,
          "mean": 458.578125,
          "median": 411.0,
          "p25": 342.25,
          "p75": 558.0,
          "p90": 704.9,
          "p95": 803.4499999999998,
          "min": 158.0,
          "max": 1056.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 395.0,
          "mean": 6.171875,
          "median": 6.0,
          "p25": 6.0,
          "p75": 7.0,
          "p90": 7.0,
          "p95": 10.549999999999983,
          "min": 1.0,
          "max": 16.0
        },
        "path_calls": {
          "n": 64,
          "sum": 142.0,
          "mean": 2.21875,
          "median": 2.0,
          "p25": 2.0,
          "p75": 3.0,
          "p90": 3.0,
          "p95": 4.0,
          "min": 0.0,
          "max": 6.0
        },
        "elapsed_seconds": {
          "n": 64,
          "sum": 1123.3120725154877,
          "mean": 17.551751133054495,
          "median": 15.90388536453247,
          "p25": 13.184414327144623,
          "p75": 21.29788488149643,
          "p90": 27.160561585426333,
          "p95": 30.104123735427844,
          "min": 6.054238557815552,
          "max": 39.59783148765564
        },
        "logical_work_over_depth": {
          "n": 64,
          "sum": 76.25719124046611,
          "mean": 1.191518613132283,
          "median": 1.1852839824640258,
          "p25": 1.1393283582089553,
          "p75": 1.232990962120121,
          "p90": 1.3018845746218326,
          "p95": 1.3617775354416575,
          "min": 1.0,
          "max": 1.5519630484988454
        }
      },
      "widths": {
        "n": 63,
        "sum": 142.0,
        "mean": 2.253968253968254,
        "median": 2.0,
        "p25": 2.0,
        "p75": 2.0,
        "p90": 3.0,
        "p95": 3.0,
        "min": 2.0,
        "max": 4.0
      }
    },
    "math": {
      "n": 64,
      "correct": 38,
      "fork_tasks": 62,
      "basic_valid": 62,
      "metrics": {
        "fork_rounds": {
          "n": 64,
          "sum": 62.0,
          "mean": 0.96875,
          "median": 1.0,
          "p25": 1.0,
          "p75": 1.0,
          "p90": 1.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 1.0
        },
        "critical_depth": {
          "n": 64,
          "sum": 37001.0,
          "mean": 578.140625,
          "median": 503.5,
          "p25": 413.5,
          "p75": 674.5,
          "p90": 945.3000000000002,
          "p95": 1001.7499999999999,
          "min": 264.0,
          "max": 1608.0
        },
        "sampled_tokens": {
          "n": 64,
          "sum": 47596.0,
          "mean": 743.6875,
          "median": 641.0,
          "p25": 522.75,
          "p75": 838.0,
          "p90": 1124.6,
          "p95": 1319.4499999999996,
          "min": 264.0,
          "max": 1964.0
        },
        "forced_tokens": {
          "n": 64,
          "sum": 657.0,
          "mean": 10.265625,
          "median": 9.0,
          "p25": 9.0,
          "p75": 12.0,
          "p90": 12.0,
          "p95": 15.0,
          "min": 0.0,
          "max": 21.0
        },
        "assembled_tokens": {
          "n": 64,
          "sum": 48253.0,
          "mean": 753.953125,
          "median": 651.5,
          "p25": 538.5,
          "p75": 849.25,
          "p90": 1133.6,
          "p95": 1330.9999999999995,
          "min": 264.0,
          "max": 1980.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 409.0,
          "mean": 6.390625,
          "median": 6.0,
          "p25": 6.0,
          "p75": 7.0,
          "p90": 7.0,
          "p95": 8.0,
          "min": 2.0,
          "max": 10.0
        },
        "path_calls": {
          "n": 64,
          "sum": 157.0,
          "mean": 2.453125,
          "median": 2.0,
          "p25": 2.0,
          "p75": 3.0,
          "p90": 3.0,
          "p95": 4.0,
          "min": 0.0,
          "max": 6.0
        },
        "elapsed_seconds": {
          "n": 64,
          "sum": 1849.9702415466309,
          "mean": 28.905785024166107,
          "median": 25.988987803459167,
          "p25": 20.096790492534637,
          "p75": 32.54583191871643,
          "p90": 42.64350221157074,
          "p95": 51.08578305244445,
          "min": 10.282099962234497,
          "max": 79.2642171382904
        },
        "logical_work_over_depth": {
          "n": 64,
          "sum": 81.83245496525956,
          "mean": 1.2786321088321806,
          "median": 1.2378770382852118,
          "p25": 1.1702530029828286,
          "p75": 1.3360528523489932,
          "p90": 1.5106456245237678,
          "p95": 1.5952185348543724,
          "min": 1.0,
          "max": 2.150384193194292
        }
      },
      "widths": {
        "n": 62,
        "sum": 157.0,
        "mean": 2.532258064516129,
        "median": 2.0,
        "p25": 2.0,
        "p75": 3.0,
        "p90": 3.0,
        "p95": 4.0,
        "min": 2.0,
        "max": 6.0
      }
    }
  },
  "native_tokens": {
    "F": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p25": 1872.5,
      "p75": 4094.0,
      "p90": 4094.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p25": 1872.5,
      "p75": 4094.0,
      "p90": 4094.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 256.0,
      "mean": 2.0,
      "median": 2.0,
      "p25": 2.0,
      "p75": 2.0,
      "p90": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 357577.0,
      "mean": 2793.5703125,
      "median": 2755.0,
      "p25": 1874.5,
      "p75": 4096.0,
      "p90": 4096.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    }
  },
  "token_phases": {
    "main": {
      "tokens": 25964,
      "fraction": 0.34015459190357655,
      "calls": 253
    },
    "width": {
      "tokens": 255,
      "fraction": 0.0033407572383073497,
      "calls": 127
    },
    "path": {
      "tokens": 34834,
      "fraction": 0.45636053976156166,
      "calls": 299
    },
    "summary": {
      "tokens": 15277,
      "fraction": 0.20014411109655444,
      "calls": 125
    }
  },
  "invalid_width_tasks": 2,
  "truncations": 0,
  "definitions": {
    "width": "Executed sibling path calls per actual fork round; 125 rounds.",
    "rounds": "Actual fork rounds per task; zero included.",
    "critical_depth": "F: logical sequential sampled-token critical path, not GPU forwards or measured parallel time.",
    "sampled_tokens": "T: all retained sampled output tokens across main, width, paths and summary calls.",
    "forced_tokens": "Runtime-injected Path headers/IDs and synchronization bridges; no forced think, Plan, opener or width.",
    "elapsed_seconds": "Generation elapsed per task, excluding engine startup; HF executes path calls serially.",
    "logical_work_over_depth": "T/F: logical cost ratio, not measured speedup.",
    "native_comparison": "Same fixed128 questions; different model/template/backend. Token counts are descriptive, not a causal SFT or latency comparison."
  },
  "protocol": {
    "model": "Qwen3-4B-Base full SFT126steps, no think",
    "seed": "42+sample_index",
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20,
    "response_cap": 4096,
    "path_cap": 2048,
    "constrained_decoding": false,
    "backend": "hf_structured_serial_backend",
    "source_sha256": "9d33de966d5909e2ffc8cfe9bb8000be8bd8e529257c616fdb591a39135e53be",
    "baseline_source_sha256": "935ab03361779768dae09e20db61bc5b6450f37548b25983fa9cf1cefa06c9d0"
  }
}
```

</details>

- [work/experiments/base-format-20261010/status.json](../artifacts/work/experiments/base-format-20261010/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "full_model": true,
  "think_wrapped": false,
  "epochs": 3,
  "steps": 126,
  "lr": 1e-05,
  "eval_questions": 128,
  "host": "sirius",
  "gpus": 8,
  "at": "2026-10-10T11:23:32.236284+00:00",
  "active": null,
  "active_pid": null,
  "smoke_artifacts_sha256": {
    "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/result.json": "ce56dcbde905d354cc9cb37472664ad2982382040c87cc16a13d99bf6be538c9",
    "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/initialization-proof.json": "092d24faea47d835d1cbd6f0aaccd95971aba347032c3debb168fe00f63cff68",
    "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/smoke/metrics.jsonl": "bc3cafb3a969bcddcde042d7d71f2bb8961f68a5691cf0c0b52c38fd9fa13345"
  },
  "training": {
    "state": "complete",
    "steps": 126,
    "epochs": 3,
    "val_loss": 0.3373735249042511,
    "full_model": true,
    "think_wrapped": false
  },
  "summary_path": "${PROJECT_ROOT}/work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128/summary.json"
}
```

</details>

## Графики

- [work/experiments/base-format-20261010/statistics/base-distributions.png](../artifacts/work/experiments/base-format-20261010/statistics/base-distributions.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/statistics/base-distributions.svg](../artifacts/work/experiments/base-format-20261010/statistics/base-distributions.svg) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/statistics/experiment-comparison.png](../artifacts/work/experiments/base-format-20261010/statistics/experiment-comparison.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/statistics/experiment-comparison.svg](../artifacts/work/experiments/base-format-20261010/statistics/experiment-comparison.svg) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/statistics/token-and-path-distributions.png](../artifacts/work/experiments/base-format-20261010/statistics/token-and-path-distributions.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/statistics/token-and-path-distributions.svg](../artifacts/work/experiments/base-format-20261010/statistics/token-and-path-distributions.svg) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Исходники рецепта и награды

- [work/experiments/base-format-20261010/compare_experiments.py](../artifacts/work/experiments/base-format-20261010/compare_experiments.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/controller.py](../artifacts/work/experiments/base-format-20261010/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/evaluations/run_eval.sh](../artifacts/work/experiments/base-format-20261010/evaluations/run_eval.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/plot_statistics.py](../artifacts/work/experiments/base-format-20261010/plot_statistics.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/base-format-20261010/prepare.py](../artifacts/work/experiments/base-format-20261010/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
