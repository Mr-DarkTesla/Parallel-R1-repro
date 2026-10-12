# exps/tag-loss-x4-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/tag-loss-x4-20261005/manifest.json](../artifacts/exps/tag-loss-x4-20261005/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "root": "${PROJECT_ROOT}",
  "queue": "${PROJECT_ROOT}/exps/tag-loss-x4-20261005",
  "code": "${PROJECT_ROOT}/exps/fixes-20261005/code/verl",
  "venv": "${PROJECT_ROOT}/.venv",
  "base": "${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2",
  "gpu_budget": 8,
  "models": [
    {
      "id": "seen-tag-x4",
      "name": "Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005",
      "variant": "seen",
      "existing": false,
      "overrides": [
        "model.enable_gradient_checkpointing=false",
        "data.max_length=3072",
        "data.parse_prompt_tags=false",
        "data.micro_batch_size_per_gpu=4"
      ],
      "results": "${PROJECT_ROOT}/exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005",
      "checkpoint_root": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005"
    }
  ],
  "evals": [
    {
      "id": "tag-x4-sync",
      "model": "seen-tag-x4",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=sync"
      ]
    },
    {
      "id": "tag-x4-async",
      "model": "seen-tag-x4",
      "epoch": 5,
      "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
      "overrides": [
        "actor_rollout_ref.rollout.mode=async"
      ]
    }
  ],
  "protocol": "Isolated Seen ablation versus fixes-20261005 Seen control, same seed1/base/data/LR1e-5/global128/micro4/230steps. Six control-token target CE weights4, remaining1, original token count denominator. Prompt/padding masked. Validation unweighted. Both sync and async final eval1916, original batch256/eager settings for direct comparison. Wait until previous training/evaluation and speed benchmark release GPUs."
}
```

</details>

- [exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/model-source.json](../artifacts/exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/model-source.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/resolved-config.yaml](../artifacts/exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/resolved-config.yaml) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
  default_local_dir: ${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005
  default_hdfs_dir: null
  project_name: Parallel-R1
  experiment_name: Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005
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
  final_dir: ${PROJECT_ROOT}/exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/final

```

</details>

## Метрики и полнота результатов

- [exps/tag-loss-x4-20261005/results/eval/tag-x4-async/driver.log](../artifacts/exps/tag-loss-x4-20261005/results/eval/tag-x4-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/tag-loss-x4-20261005/results/eval/tag-x4-async/summary.json](../artifacts/exps/tag-loss-x4-20261005/results/eval/tag-x4-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "tag-x4-async",
    "model": "seen-tag-x4",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
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
      "mean": 0.00625,
      "observed_pass": 0.06666666666666667,
      "bootstrap_best": 0.051866666666666665,
      "parallel": 0.99375,
      "format": 0.9458333333333333,
      "parallel_format": 0.9333333333333333,
      "format_error": 0.06041666666666667,
      "no_tags": 0.00625
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.008333333333333333,
      "observed_pass": 0.13333333333333333,
      "bootstrap_best": 0.08813333333333334,
      "parallel": 0.9895833333333334,
      "format": 0.95625,
      "parallel_format": 0.9375,
      "format_error": 0.052083333333333336,
      "no_tags": 0.010416666666666666
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.103125,
      "observed_pass": 0.475,
      "bootstrap_best": 0.39645,
      "parallel": 0.99375,
      "format": 0.9640625,
      "parallel_format": 0.9546875,
      "format_error": 0.0390625,
      "no_tags": 0.00625
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.23417721518987342,
      "observed_pass": 0.23417721518987342,
      "bootstrap_best": null,
      "parallel": 1.0,
      "format": 0.9873417721518988,
      "parallel_format": 0.9873417721518988,
      "format_error": 0.012658227848101266,
      "no_tags": 0.0
    }
  }
}
```

</details>

- [exps/tag-loss-x4-20261005/results/eval/tag-x4-sync/driver.log](../artifacts/exps/tag-loss-x4-20261005/results/eval/tag-x4-sync/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/tag-loss-x4-20261005/results/eval/tag-x4-sync/summary.json](../artifacts/exps/tag-loss-x4-20261005/results/eval/tag-x4-sync/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "job": {
    "id": "tag-x4-sync",
    "model": "seen-tag-x4",
    "epoch": 5,
    "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
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
      "mean": 0.00625,
      "observed_pass": 0.1,
      "bootstrap_best": 0.0646,
      "parallel": 0.9770833333333333,
      "format": 0.9479166666666666,
      "parallel_format": 0.9104166666666667,
      "format_error": 0.06666666666666667,
      "no_tags": 0.022916666666666665
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "mean": 0.0020833333333333333,
      "observed_pass": 0.03333333333333333,
      "bootstrap_best": 0.021166666666666667,
      "parallel": 0.9854166666666667,
      "format": 0.9291666666666667,
      "parallel_format": 0.8979166666666667,
      "format_error": 0.0875,
      "no_tags": 0.014583333333333334
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "mean": 0.0875,
      "observed_pass": 0.475,
      "bootstrap_best": 0.3955,
      "parallel": 0.9890625,
      "format": 0.9546875,
      "parallel_format": 0.9296875,
      "format_error": 0.059375,
      "no_tags": 0.0109375
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "mean": 0.30063291139240506,
      "observed_pass": 0.30063291139240506,
      "bootstrap_best": null,
      "parallel": 1.0,
      "format": 0.9651898734177216,
      "parallel_format": 0.9556962025316456,
      "format_error": 0.04430379746835443,
      "no_tags": 0.0
    }
  }
}
```

</details>

- [exps/tag-loss-x4-20261005/status.json](../artifacts/exps/tag-loss-x4-20261005/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "dependencies": {
    "status": "complete",
    "updated": "2026-10-05T21:27:53.048520+00:00"
  },
  "train-seen-tag-x4": {
    "status": "complete",
    "updated": "2026-10-05T21:34:56.900180+00:00",
    "exit_code": 0,
    "results": "${PROJECT_ROOT}/exps/tag-loss-x4-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005"
  },
  "eval-tag-x4-sync": {
    "status": "complete",
    "updated": "2026-10-05T21:45:49.777306+00:00",
    "results": "${PROJECT_ROOT}/exps/tag-loss-x4-20261005/results/eval/tag-x4-sync",
    "answers": 1916
  },
  "eval-tag-x4-async": {
    "status": "complete",
    "updated": "2026-10-05T21:46:24.123232+00:00",
    "results": "${PROJECT_ROOT}/exps/tag-loss-x4-20261005/results/eval/tag-x4-async",
    "answers": 1916
  }
}
```

</details>

- [exps/tag-loss-x4-20261005/summary.csv](../artifacts/exps/tag-loss-x4-20261005/summary.csv) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/tag-loss-x4-20261005/summary.json](../artifacts/exps/tag-loss-x4-20261005/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-05T21:46:24.131228+00:00",
  "evaluations": [
    {
      "complete": true,
      "job": {
        "id": "tag-x4-sync",
        "model": "seen-tag-x4",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
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
          "mean": 0.00625,
          "observed_pass": 0.1,
          "bootstrap_best": 0.0646,
          "parallel": 0.9770833333333333,
          "format": 0.9479166666666666,
          "parallel_format": 0.9104166666666667,
          "format_error": 0.06666666666666667,
          "no_tags": 0.022916666666666665
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.0020833333333333333,
          "observed_pass": 0.03333333333333333,
          "bootstrap_best": 0.021166666666666667,
          "parallel": 0.9854166666666667,
          "format": 0.9291666666666667,
          "parallel_format": 0.8979166666666667,
          "format_error": 0.0875,
          "no_tags": 0.014583333333333334
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.0875,
          "observed_pass": 0.475,
          "bootstrap_best": 0.3955,
          "parallel": 0.9890625,
          "format": 0.9546875,
          "parallel_format": 0.9296875,
          "format_error": 0.059375,
          "no_tags": 0.0109375
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.30063291139240506,
          "observed_pass": 0.30063291139240506,
          "bootstrap_best": null,
          "parallel": 1.0,
          "format": 0.9651898734177216,
          "parallel_format": 0.9556962025316456,
          "format_error": 0.04430379746835443,
          "no_tags": 0.0
        }
      }
    },
    {
      "complete": true,
      "job": {
        "id": "tag-x4-async",
        "model": "seen-tag-x4",
        "epoch": 5,
        "checkpoint": "${MODEL_ROOT}/Parallel-SFT-Seen-Qwen3-0.6B-tag-loss-x4-20261005/global_step_230",
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
          "mean": 0.00625,
          "observed_pass": 0.06666666666666667,
          "bootstrap_best": 0.051866666666666665,
          "parallel": 0.99375,
          "format": 0.9458333333333333,
          "parallel_format": 0.9333333333333333,
          "format_error": 0.06041666666666667,
          "no_tags": 0.00625
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "mean": 0.008333333333333333,
          "observed_pass": 0.13333333333333333,
          "bootstrap_best": 0.08813333333333334,
          "parallel": 0.9895833333333334,
          "format": 0.95625,
          "parallel_format": 0.9375,
          "format_error": 0.052083333333333336,
          "no_tags": 0.010416666666666666
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "mean": 0.103125,
          "observed_pass": 0.475,
          "bootstrap_best": 0.39645,
          "parallel": 0.99375,
          "format": 0.9640625,
          "parallel_format": 0.9546875,
          "format_error": 0.0390625,
          "no_tags": 0.00625
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "mean": 0.23417721518987342,
          "observed_pass": 0.23417721518987342,
          "bootstrap_best": null,
          "parallel": 1.0,
          "format": 0.9873417721518988,
          "parallel_format": 0.9873417721518988,
          "format_error": 0.012658227848101266,
          "no_tags": 0.0
        }
      }
    }
  ],
  "failed_or_skipped": [],
  "protocol": "Isolated Seen ablation versus fixes-20261005 Seen control, same seed1/base/data/LR1e-5/global128/micro4/230steps. Six control-token target CE weights4, remaining1, original token count denominator. Prompt/padding masked. Validation unweighted. Both sync and async final eval1916, original batch256/eager settings for direct comparison. Wait until previous training/evaluation and speed benchmark release GPUs."
}
```

</details>

## Исходники рецепта и награды

- [exps/tag-loss-x4-20261005/launch.sh](../artifacts/exps/tag-loss-x4-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
