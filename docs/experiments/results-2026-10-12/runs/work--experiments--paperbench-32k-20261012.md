# work/experiments/paperbench-32k-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/paperbench-32k-20261012/manifest.json](../artifacts/work/experiments/paperbench-32k-20261012/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "rerun_only_truncated": true,
  "selected": {
    "AIME2024": 15,
    "AIME2025": 16,
    "AMC2023": 6,
    "AIME2026": 16
  },
  "kept": 77,
  "total": 130,
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "native_source_proof": {
    "at": "2026-10-10T07:02:46.594578+00:00",
    "repo": "Qwen/Qwen3-4B",
    "revision": "1cfa9a7208912126459214e8b04321603b3df60c",
    "original_weights_tokenizer": true,
    "added_tokens": false,
    "enable_thinking": true,
    "force_initial_native_think_prefix": true,
    "template_suffix": "<|im_start|>assistant\n<think>\n",
    "files": {
      "config.json": "8ba006f74fecfaaeb392872a60f4a480e7ec9860153d2e1b769ec81f9a147f8a",
      "generation_config.json": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
      "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
      "model.safetensors.index.json": "6dc0981b8829fead746441f68f38f24c5ca4a3a66351f652c26c6df0efc43ab2",
      "tokenizer.json": "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4",
      "tokenizer_config.json": "d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101",
      "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
      "model-00003-of-00003.safetensors": "e4bf436957184f4eeb86a80e9db394503f1f56446b2e6b7edeac5b81470f4ca1",
      "model-00001-of-00003.safetensors": "328a91d3122359d5547f9d79521205bc0a46e1f79a792dfe650e99fc2d651223",
      "model-00002-of-00003.safetensors": "6cd087b316306a68c562436b5492edbcf6e16c6dba3a1308279caa5a58e21ca5"
    }
  },
  "sha256": {
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/counting_worker.py": "d0d4e70176a9314a7575f6e0a2a3aee3d3f991433934b2e1aa593bcb6c75c8d5",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/finalize.py": "c72a4fdbacfccaa35f8bbb2c1bed58d7752e2b39f4804eee7ff49e748d2abc59",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/launch.py": "9a19c5b2f0d91ceeca504e7bceb41528f1055ee2a8aca88200026a14ed513279",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/native_worker.py": "76027e7e3faa3bea81f09e2a8c172f9a80b37f8e04230992eebf5a88afc1e4ed",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/prepare.py": "fe1978318deb4c5888f9ed22e878a086b3a4f5fd449ef76858e8ec49d29b8ffb",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/rl_worker.py": "45a047b4931c1b2bbb8c90b2e66dc7b7d512b3dc0ad6e62adc961692e6f149b4",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/rl-job.json": "617933d37da7db2d43922708cc291c5735fcd1ec7a959ae228fd83d5e914a0ae",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/native-job.json": "b2e124189917dd468ef8126a68850c2772e51c043e7b3c2d242e2cbc00e70a1f",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/cohort_decoder.py": "6c2e82141948586c8e203d828b89519a68e72bb25d4b6482960927a668287d3f",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/microbatch_decoder.py": "df31d6a43f9efd4b97290e3cad4a5ed9a11b02664973eb1cdf778f31500cf343",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/train.py": "a9aa90d44e9effa8bfbf0ef2165d4ec03609030c205dd4344697b6225a73bc9e",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/core/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/data/all130.jsonl": "5f1697f9a61b5d3fe8da80291b95709b2af903a5bfd8af29441335c9debc8326",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/data/truncated53.jsonl": "04b16f13d7a19dea757fcb664b3561a5049dd41b7b4aac277797f4230723812e",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/data/kept77.jsonl": "e111bf0c1afc0b76e98ace3595eadce95ea7ecd97e5fa55a27f792f81781afa2",
    "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/data/reference-first-calls.json": "e03e32bbf9b72001a70fe8154cc49c8bdf4b7f29a4b80773379503168d3bf620"
  },
  "benchmark_only": true
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/REPORT.md](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/coverage.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/coverage.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete130": true,
  "rl53_plus_kept77": true,
  "native130": true,
  "all8_rl_native_exit0": true,
  "technical_unknown": []
}
```

</details>

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/exits.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "0": {
    "rl": 0,
    "native": 0
  },
  "1": {
    "rl": 0,
    "native": 0
  },
  "2": {
    "rl": 0,
    "native": 0
  },
  "3": {
    "rl": 0,
    "native": 0
  },
  "4": {
    "rl": 0,
    "native": 0
  },
  "5": {
    "rl": 0,
    "native": 0
  },
  "6": {
    "rl": 0,
    "native": 0
  },
  "7": {
    "rl": 0,
    "native": 0
  }
}
```

</details>

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/result.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rl50": {
    "passed": true,
    "label": "RL50 keep77 + completed rerun53 at32k",
    "samples_per_question": 1,
    "response_limit": 32768,
    "rows": 130,
    "unknown": 0,
    "by_dataset": {
      "AIME2024": {
        "n": 30,
        "correct": 10,
        "accuracy": 0.3333333333333333,
        "format_valid": 26,
        "format_and_fork_all": 0.8666666666666667,
        "truncated": 0,
        "mean_episode_forward_participation": 4556.966666666666,
        "mean_tokens": 5621.2,
        "format_conditioned": {
          "n": 26,
          "width": 3.9642857142857144,
          "depth": 1.0769230769230769,
          "forward_participation": 3304.5
        }
      },
      "AIME2025": {
        "n": 30,
        "correct": 4,
        "accuracy": 0.13333333333333333,
        "format_valid": 25,
        "format_and_fork_all": 0.8333333333333334,
        "truncated": 0,
        "mean_episode_forward_participation": 4420.366666666667,
        "mean_tokens": 5622.166666666667,
        "format_conditioned": {
          "n": 25,
          "width": 4.04,
          "depth": 1,
          "forward_participation": 3375.08
        }
      },
      "AIME2026": {
        "n": 30,
        "correct": 4,
        "accuracy": 0.13333333333333333,
        "format_valid": 25,
        "format_and_fork_all": 0.8,
        "truncated": 0,
        "mean_episode_forward_participation": 4530.866666666667,
        "mean_tokens": 5838.866666666667,
        "format_conditioned": {
          "n": 25,
          "width": 4.208333333333333,
          "depth": 0.96,
          "forward_participation": 3223.08
        }
      },
      "AMC2023": {
        "n": 40,
        "correct": 25,
        "accuracy": 0.625,
        "format_valid": 38,
        "format_and_fork_all": 0.95,
        "truncated": 0,
        "mean_episode_forward_participation": 2234.375,
        "mean_tokens": 3118.225,
        "format_conditioned": {
          "n": 38,
          "width": 4.25,
          "depth": 1.0526315789473684,
          "forward_participation": 2149.4736842105262
        }
      }
    },
    "all_gpu_children_exit0": true,
    "time": 1791817174.5620604
  },
  "native": {
    "passed": true,
    "label": "Original Qwen3-4B native thinking BF16 vLLM32k",
    "samples_per_question": 1,
    "response_limit": 32768,
    "rows": 130,
    "unknown": 0,
    "by_dataset": {
      "AIME2024": {
        "n": 30,
        "correct": 22,
        "accuracy": 0.7333333333333333,
        "format_valid": 29,
        "format_and_fork_all": 0.0,
        "truncated": 1,
        "mean_episode_forward_participation": 15463.266666666666,
        "mean_tokens": 15462.266666666666,
        "format_conditioned": {
          "n": 29,
          "width": null,
          "depth": 0,
          "forward_participation": 14866.51724137931
        }
      },
      "AIME2025": {
        "n": 30,
        "correct": 19,
        "accuracy": 0.6333333333333333,
        "format_valid": 24,
        "format_and_fork_all": 0.0,
        "truncated": 6,
        "mean_episode_forward_participation": 18348.1,
        "mean_tokens": 18347.1,
        "format_conditioned": {
          "n": 24,
          "width": null,
          "depth": 0,
          "forward_participation": 14742.875
        }
      },
      "AIME2026": {
        "n": 30,
        "correct": 22,
        "accuracy": 0.7333333333333333,
        "format_valid": 29,
        "format_and_fork_all": 0.0,
        "truncated": 1,
        "mean_episode_forward_participation": 15718.266666666666,
        "mean_tokens": 15717.266666666666,
        "format_conditioned": {
          "n": 29,
          "width": null,
          "depth": 0,
          "forward_participation": 15130.310344827587
        }
      },
      "AMC2023": {
        "n": 40,
        "correct": 37,
        "accuracy": 0.925,
        "format_valid": 40,
        "format_and_fork_all": 0.0,
        "truncated": 0,
        "mean_episode_forward_participation": 8980.95,
        "mean_tokens": 8979.95,
        "format_conditioned": {
          "n": 40,
          "width": null,
          "depth": 0,
          "forward_participation": 8980.95
        }
      }
    },
    "all_gpu_children_exit0": true,
    "time": 1791817174.5625684
  },
  "repair": {
    "main_thread_scoring": true,
    "original_sources_unchanged": true,
    "coverage": {
      "complete130": true,
      "rl53_plus_kept77": true,
      "native130": true,
      "all8_rl_native_exit0": true,
      "technical_unknown": []
    }
  },
  "notes": [
    "RL50 FP32/native BF16 vLLM differ; no exact-compute claim",
    "F participation differs from global backend forwards"
  ]
}
```

</details>

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/status.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "time": 1791817174.7343338,
  "ranks": {
    "0": "completed",
    "1": "completed",
    "2": "completed",
    "3": "completed",
    "4": "completed",
    "5": "completed",
    "6": "completed",
    "7": "completed"
  },
  "exits": {
    "0": {
      "rl": 0,
      "native": 0
    },
    "1": {
      "rl": 0,
      "native": 0
    },
    "2": {
      "rl": 0,
      "native": 0
    },
    "3": {
      "rl": 0,
      "native": 0
    },
    "4": {
      "rl": 0,
      "native": 0
    },
    "5": {
      "rl": 0,
      "native": 0
    },
    "6": {
      "rl": 0,
      "native": 0
    },
    "7": {
      "rl": 0,
      "native": 0
    }
  }
}
```

</details>

- [work/experiments/paperbench-32k-20261012/exits.json](../artifacts/work/experiments/paperbench-32k-20261012/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "0": {},
  "1": {},
  "2": {},
  "3": {},
  "4": {},
  "5": {},
  "6": {
    "rl": 1
  },
  "7": {}
}
```

</details>

- [work/experiments/paperbench-32k-20261012/parallel-native-tail/exits.json](../artifacts/work/experiments/paperbench-32k-20261012/parallel-native-tail/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 0
}
```

</details>

- [work/experiments/paperbench-32k-20261012/parallel-native-tail/result.json](../artifacts/work/experiments/paperbench-32k-20261012/parallel-native-tail/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "exits": {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0
  },
  "saved": 16,
  "expected": 16,
  "source_protocol_unchanged": true,
  "batch_composition_changed": true,
  "parent_will_skip_already_saved_ids": true,
  "raw_backend_ledgers_preserved": "${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/parallel-native-tail/runs",
  "time": 1791817068.3599148
}
```

</details>

- [work/experiments/paperbench-32k-20261012/status.json](../artifacts/work/experiments/paperbench-32k-20261012/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "time": 1791808631.4223742,
  "host": "RUN_5482aee87e-mpiworker-2",
  "error": "RuntimeError('rl rank6 failed rc1; preserve healthy children')",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/paperbench-32k-20261012/launch.py\", line 38, in <module>\n    if code!=0:raise RuntimeError(f'{stage} rank{rank} failed rc{code}; preserve healthy children')\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nRuntimeError: rl rank6 failed rc1; preserve healthy children\n"
}
```

</details>

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/status.json](../history/local_saved/26ee6e0ecd5b/work/experiments/paperbench-32k-20261012/attempt2-main-thread/status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "host": "RUN_5482aee87e-mpiworker-2",
  "time": 1791809834.0848083,
  "ranks": {
    "0": "rl",
    "1": "rl",
    "2": "rl",
    "3": "rl",
    "4": "await_old_rl",
    "5": "rl",
    "6": "rl",
    "7": "rl"
  },
  "exits": {
    "0": {},
    "1": {},
    "2": {},
    "3": {},
    "4": {},
    "5": {},
    "6": {},
    "7": {}
  },
  "errors": {},
  "native_hash_proof_ready": true,
  "no_gpu_worker_signals": true
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/controller.py](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-32k-20261012/core/reward.py](../artifacts/work/experiments/paperbench-32k-20261012/core/reward.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-32k-20261012/core/train.py](../artifacts/work/experiments/paperbench-32k-20261012/core/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-32k-20261012/launch.py](../artifacts/work/experiments/paperbench-32k-20261012/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-32k-20261012/prepare.py](../artifacts/work/experiments/paperbench-32k-20261012/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Дополнительно проверенные конфигурации и формулы

- [work/experiments/paperbench-32k-20261012/rl-job.json](../artifacts/work/experiments/paperbench-32k-20261012/rl-job.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
- [work/experiments/paperbench-32k-20261012/native-job.json](../artifacts/work/experiments/paperbench-32k-20261012/native-job.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/rl-job.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/rl-job.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
- [work/experiments/paperbench-32k-20261012/attempt2-main-thread/native-job.json](../artifacts/work/experiments/paperbench-32k-20261012/attempt2-main-thread/native-job.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
