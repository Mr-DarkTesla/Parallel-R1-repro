# exps/sft-unseen-three-datasets-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/sft-unseen-three-datasets-20261008/base/config.json](../artifacts/exps/sft-unseen-three-datasets-20261008/base/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "architectures": [
    "Qwen3ForCausalLM"
  ],
  "attention_bias": false,
  "attention_dropout": 0.0,
  "bos_token_id": 151643,
  "eos_token_id": 151643,
  "head_dim": 128,
  "hidden_act": "silu",
  "hidden_size": 1024,
  "initializer_range": 0.02,
  "intermediate_size": 3072,
  "layer_types": [
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention",
    "full_attention"
  ],
  "max_position_embeddings": 32768,
  "max_window_layers": 28,
  "model_type": "qwen3",
  "num_attention_heads": 16,
  "num_hidden_layers": 28,
  "num_key_value_heads": 8,
  "rms_norm_eps": 1e-06,
  "rope_scaling": null,
  "rope_theta": 1000000,
  "sliding_window": null,
  "tie_word_embeddings": true,
  "torch_dtype": "bfloat16",
  "transformers_version": "4.53.2",
  "use_cache": true,
  "use_sliding_window": false,
  "vocab_size": 151675
}
```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/config.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 8
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-train.parquet
  val_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 32768
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
  default_local_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 00_longest_canary
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
  final_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/hydra.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=32768
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
    - trainer.experiment_name=00_longest_canary
    - trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/final
    - trainer.total_training_steps=1
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=32768,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=8,data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/checkpoints,trainer.experiment_name=00_longest_canary,trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=1,trainer.total_training_steps=1,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra
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

- [exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/overrides.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-train.parquet
- data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/canary-val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=32768
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
- trainer.experiment_name=00_longest_canary
- trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/final
- trainer.total_training_steps=1

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/config.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/train.parquet
  val_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 32768
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
  default_local_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 01_gsm_infinite
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
  final_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/hydra.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=32768
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
    - trainer.experiment_name=01_gsm_infinite
    - trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=32768,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=128,data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/checkpoints,trainer.experiment_name=01_gsm_infinite,trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=5,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra
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

- [exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/overrides.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/gsm_infinite/val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=32768
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
- trainer.experiment_name=01_gsm_infinite
- trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/config.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/train.parquet
  val_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 32768
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
  default_local_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 02_sft_messages
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
  final_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/hydra.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=32768
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
    - trainer.experiment_name=02_sft_messages
    - trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=32768,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=128,data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/checkpoints,trainer.experiment_name=02_sft_messages,trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=5,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra
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

- [exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/overrides.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/sft_messages/val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=32768
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
- trainer.experiment_name=02_sft_messages
- trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/config.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
data:
  train_batch_size: 128
  micro_batch_size: null
  micro_batch_size_per_gpu: 1
  train_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/train.parquet
  val_files: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/val.parquet
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
  multiturn:
    enable: false
    messages_key: messages
    tools_key: tools
    enable_thinking_key: enable_thinking
  max_length: 32768
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
  default_local_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/checkpoints
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: 03_mixed
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
  final_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/final

```

</details>

- [exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/hydra.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/hydra.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
hydra:
  run:
    dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra
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
    - hydra.run.dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra
    - hydra.mode=RUN
    task:
    - data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/train.parquet
    - data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/val.parquet
    - data.prompt_key=problem
    - data.response_key=response
    - data.prompt_dict_keys=[]
    - data.response_dict_keys=[]
    - +data.prompt_messages_key=prompt_messages
    - +data.defer_parallel_mask=true
    - data.parallel_attention=true
    - data.multiturn.enable=false
    - data.truncation=error
    - data.max_length=32768
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
    - trainer.experiment_name=03_mixed
    - trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/checkpoints
    - trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/final
  job:
    name: fsdp_parallel_sft_trainer
    chdir: null
    override_dirname: +data.defer_parallel_mask=true,+data.prompt_messages_key=prompt_messages,data.max_length=32768,data.micro_batch_size_per_gpu=1,data.multiturn.enable=false,data.num_workers=2,data.parallel_attention=true,data.prompt_dict_keys=[],data.prompt_key=problem,data.response_dict_keys=[],data.response_key=response,data.train_batch_size=128,data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/train.parquet,data.trim_padding=true,data.truncation=error,data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/val.parquet,model.enable_gradient_checkpointing=true,model.partial_pretrain=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/base,optim.lr=1e-5,trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/checkpoints,trainer.experiment_name=03_mixed,trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/final,trainer.logger=[console],trainer.resume_mode=disable,trainer.seed=1,trainer.total_epochs=5,ulysses_sequence_parallel_size=1,use_remove_padding=false
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
    cwd: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/code/verl/trainer/config
      schema: file
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra
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

- [exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/overrides.yaml](../artifacts/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/hydra/.hydra/overrides.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```yaml
- data.train_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/train.parquet
- data.val_files=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/data/mixed/val.parquet
- data.prompt_key=problem
- data.response_key=response
- data.prompt_dict_keys=[]
- data.response_dict_keys=[]
- +data.prompt_messages_key=prompt_messages
- +data.defer_parallel_mask=true
- data.parallel_attention=true
- data.multiturn.enable=false
- data.truncation=error
- data.max_length=32768
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
- trainer.experiment_name=03_mixed
- trainer.default_local_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/checkpoints
- trainer.final_dir=${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/final

```

</details>

## Метрики и полнота результатов

- [exps/sft-unseen-three-datasets-20261008/data-report.json](../artifacts/exps/sft-unseen-three-datasets-20261008/data-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
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
  "tag_ids": {
    "<Parallel>": [
      151671
    ],
    "</Parallel>": [
      151672
    ],
    "<Path>": [
      151669
    ],
    "</Path>": [
      151670
    ],
    "<Summary>": [
      151673
    ],
    "</Summary>": [
      151674
    ]
  },
  "split_policy": "Adaptive corpora: deterministic SHA256(problem, split-seed-1), 4500/500. Mixed: original splits.",
  "transformation": "Only whitespace outside sibling Path spans is removed; system/user roles preserved.",
  "datasets": [
    {
      "name": "gsm_infinite",
      "sources": {
        "gsm_infinite_adaptive_parallel_5k.jsonl": "a63c0613526338246460b50824dc29f19aa6defcbbc66b73dc8f9a152df72799"
      },
      "splits": {
        "train": {
          "rows": 4500,
          "sha256": "8bf270da09def7e5a124750920352000107528791d98d409d085301e4ba295bf",
          "min": 275,
          "max": 27954,
          "quantiles": {
            "0.5": 1425,
            "0.9": 2812,
            "0.95": 3777,
            "0.99": 11137
          },
          "over": {
            "3072": 365,
            "4096": 191,
            "8192": 163,
            "16384": 38,
            "32768": 0,
            "40960": 0
          }
        },
        "val": {
          "rows": 500,
          "sha256": "fc0c7330a559386d2584e55ef377a51c7d53513dfe40cf49d1cd6f91cae04dc6",
          "min": 319,
          "max": 22793,
          "quantiles": {
            "0.5": 1344,
            "0.9": 2707,
            "0.95": 3413,
            "0.99": 10029
          },
          "over": {
            "3072": 34,
            "4096": 20,
            "8192": 15,
            "16384": 2,
            "32768": 0,
            "40960": 0
          }
        }
      }
    },
    {
      "name": "sft_messages",
      "sources": {
        "sft_messages_5000.jsonl": "ce0bc7febe267be6761d6689e52f5b57bcaaba6ebdb5a9ed7813ffea35a05dda"
      },
      "splits": {
        "train": {
          "rows": 4500,
          "sha256": "0aa7e66856caaf802fc127089ec2b6fab75d1a5cad7419d36aa73b6ed30feea4",
          "min": 392,
          "max": 4147,
          "quantiles": {
            "0.5": 1515,
            "0.9": 2471,
            "0.95": 2741,
            "0.99": 3232
          },
          "over": {
            "3072": 79,
            "4096": 1,
            "8192": 0,
            "16384": 0,
            "32768": 0,
            "40960": 0
          }
        },
        "val": {
          "rows": 500,
          "sha256": "2e29a0ca61985d71d5a17376d1eabeaa67c395c1f6f997b875263cb5f798d055",
          "min": 397,
          "max": 3800,
          "quantiles": {
            "0.5": 1488,
            "0.9": 2406,
            "0.95": 2695,
            "0.99": 3260
          },
          "over": {
            "3072": 6,
            "4096": 0,
            "8192": 0,
            "16384": 0,
            "32768": 0,
            "40960": 0
          }
        }
      }
    },
    {
      "name": "mixed",
      "sources": {
        "train.parquet": "b4b62e72075795db1d33f03805e847acbb67ab20562312eeff2e6a832736d4e6",
        "val.parquet": "765350e7f3c4ec54b77536f541460562e93b9d495c25f0aef811ea594c6db7bd"
      },
      "splits": {
        "train": {
          "rows": 4500,
          "sha256": "c8016cc02c00c3330091e63eff6c14e3a23ee520c14b5b1aadea47ffa0a44cc6",
          "min": 35,
          "max": 528,
          "quantiles": {
            "0.5": 201,
            "0.9": 272,
            "0.95": 310,
            "0.99": 415
          },
          "over": {
            "3072": 0,
            "4096": 0,
            "8192": 0,
            "16384": 0,
            "32768": 0,
            "40960": 0
          }
        },
        "val": {
          "rows": 500,
          "sha256": "18dea1278874cce43da85de64c35bbc9138eb9c00ddaca1a7e7996ecae7bec6a",
          "min": 39,
          "max": 419,
          "quantiles": {
            "0.5": 193,
            "0.9": 257,
            "0.95": 293,
            "0.99": 407
          },
          "over": {
            "3072": 0,
            "4096": 0,
            "8192": 0,
            "16384": 0,
            "32768": 0,
            "40960": 0
          }
        }
      }
    }
  ]
}
```

</details>

- [exps/sft-unseen-three-datasets-20261008/status.json](../artifacts/exps/sft-unseen-three-datasets-20261008/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": "2026-10-08T13:37:38.671111+00:00",
  "policy": "Independent fresh starts from pinned base; serial execution; stop on failure; no restart/resume.",
  "jobs": [
    {
      "name": "00_longest_canary",
      "dataset": "gsm_infinite",
      "canary": true,
      "state": "complete",
      "started_at": "2026-10-08T13:37:38.680909+00:00",
      "log": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/sft.log",
      "finished_at": "2026-10-08T13:38:57.356332+00:00",
      "exit_code": 0,
      "optimizer_steps": 1,
      "expected_steps": 1,
      "final": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/00_longest_canary/final",
      "final_sha256": "b52880ca1dc50b36ce3aad1b922a1eadf3a592eb1df2c59272850a2a1ea68979"
    },
    {
      "name": "01_gsm_infinite",
      "dataset": "gsm_infinite",
      "canary": false,
      "state": "complete",
      "started_at": "2026-10-08T13:38:58.917857+00:00",
      "log": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/sft.log",
      "finished_at": "2026-10-08T15:17:02.183836+00:00",
      "exit_code": 0,
      "optimizer_steps": 175,
      "expected_steps": 175,
      "final": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final",
      "final_sha256": "101d49a2e82b3c3433ae9101a39a92e3c819e547b96f5dc7e0df5cd27d739756"
    },
    {
      "name": "02_sft_messages",
      "dataset": "sft_messages",
      "canary": false,
      "state": "complete",
      "started_at": "2026-10-08T15:17:03.854362+00:00",
      "log": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/sft.log",
      "finished_at": "2026-10-08T15:39:46.221316+00:00",
      "exit_code": 0,
      "optimizer_steps": 175,
      "expected_steps": 175,
      "final": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/02_sft_messages/final",
      "final_sha256": "0b45d350fb935dfe04c8f3a57c9fdb4f450df9ac562eee47f5891736f9a36ee1"
    },
    {
      "name": "03_mixed",
      "dataset": "mixed",
      "canary": false,
      "state": "complete",
      "started_at": "2026-10-08T15:39:47.880762+00:00",
      "log": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/sft.log",
      "finished_at": "2026-10-08T15:56:16.236567+00:00",
      "exit_code": 0,
      "optimizer_steps": 175,
      "expected_steps": 175,
      "final": "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/runs/03_mixed/final",
      "final_sha256": "843925d22fdb7f2bec81600f0b6f2114367bb20a35ca0b332bdc403e72b239af"
    }
  ],
  "finished_at": "2026-10-08T15:56:17.800103+00:00"
}
```

</details>

## Исходники рецепта и награды

- [exps/sft-unseen-three-datasets-20261008/prepare_data.py](../artifacts/exps/sft-unseen-three-datasets-20261008/prepare_data.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
