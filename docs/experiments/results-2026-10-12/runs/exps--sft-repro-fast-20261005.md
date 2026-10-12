# exps/sft-repro-fast-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/sft-repro-fast-20261005/model-source.json](../artifacts/exps/sft-repro-fast-20261005/model-source.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

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

- [exps/sft-repro-fast-20261005/resolved-config.yaml](../artifacts/exps/sft-repro-fast-20261005/resolved-config.yaml) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

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
  max_length: 4096
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
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B-repro-fast-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Unseen-Qwen3-0.6B-repro-fast-20261005
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
  final_dir: ${PROJECT_ROOT}/verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B-repro-fast-20261005/final

```

</details>

## Исходники рецепта и награды

- [exps/sft-repro-fast-20261005/launch.sh](../artifacts/exps/sft-repro-fast-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
