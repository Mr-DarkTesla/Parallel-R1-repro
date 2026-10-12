# exps/qwen3-06b-reasoning-16k-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/manifest.json](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "started": "2026-10-06T10:14:41.467888+00:00",
  "decoding": "ordinary autoregressive, rollout.mode=sync",
  "parallel_tokens_added": false,
  "parallel_instructions": false,
  "temperature": 1.0,
  "max_response_tokens": 16384,
  "samples": {
    "APO_AIME24": 16,
    "APO_AIME25": 16,
    "APO_AMC23": 16,
    "APO_MATH300": 16,
    "APO_MATH500": 1
  },
  "answers_per_mode": 7156,
  "source_sha256": {
    "${PROJECT_ROOT}/verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e",
    "${PROJECT_ROOT}/exps/branch-diversity-20261006/math500.parquet": "32317851fa9be3c3d949c4709c18ec3b40c0efbe79b5bdef72a0addad1446658"
  },
  "data_sha256": "755035689ed7a6d0ba44d4ebf4a1c4be874fc0814c505e0ce61384becfed4c71",
  "weights_sha256": {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
  },
  "mode": "reasoning",
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
  "val_batch_size": 512,
  "comparison": "Same questions, prompts, weights, temperature=1, top_p=1, top_k=-1 as the 3k run; response budget increased. Legacy metrics and corrected extraction reported separately.",
  "command": [
    "bash",
    "training_scripts/eval_qwen3_06b.sh",
    "${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/models/reasoning",
    "actor_rollout_ref.rollout.mode=sync",
    "actor_rollout_ref.rollout.enforce_eager=true",
    "actor_rollout_ref.rollout.val_kwargs.n=1",
    "data.max_response_length=16384",
    "data.val_batch_size=512",
    "actor_rollout_ref.rollout.gpu_memory_utilization=0.8",
    "data.val_files=${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/plain.parquet",
    "data.train_files=${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/plain.parquet",
    "ray_init.num_cpus=40"
  ],
  "scorer_sha256": "bc55b01fa03a5dd98b660b4b47196fc794e38f90184193667df9685ff1c97b2d"
}
```

</details>

- [exps/qwen3-06b-reasoning-16k-20261006/manifest.json](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "started": "2026-10-06T10:16:48.856776+00:00",
  "decoding": "ordinary autoregressive, rollout.mode=sync",
  "parallel_tokens_added": false,
  "parallel_instructions": false,
  "temperature": 1.0,
  "max_response_tokens": 16384,
  "samples": {
    "APO_AIME24": 16,
    "APO_AIME25": 16,
    "APO_AMC23": 16,
    "APO_MATH300": 16,
    "APO_MATH500": 1
  },
  "answers_per_mode": 7156,
  "source_sha256": {
    "${PROJECT_ROOT}/verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet": "cee9b99e0645501b0dac3d885e66eae8d36e107c28a2f914864a68021aafc21e",
    "${PROJECT_ROOT}/exps/branch-diversity-20261006/math500.parquet": "32317851fa9be3c3d949c4709c18ec3b40c0efbe79b5bdef72a0addad1446658"
  },
  "data_sha256": "755035689ed7a6d0ba44d4ebf4a1c4be874fc0814c505e0ce61384becfed4c71",
  "weights_sha256": {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
  },
  "mode": "reasoning",
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
  "val_batch_size": 512,
  "comparison": "Same questions, prompts, weights, temperature=1, top_p=1, top_k=-1 as the 3k run; response budget increased. Legacy metrics and corrected extraction reported separately.",
  "command": [
    "bash",
    "training_scripts/eval_qwen3_06b.sh",
    "${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/models/reasoning",
    "actor_rollout_ref.rollout.mode=sync",
    "actor_rollout_ref.rollout.enforce_eager=true",
    "actor_rollout_ref.rollout.val_kwargs.n=1",
    "data.max_response_length=16384",
    "data.val_batch_size=512",
    "actor_rollout_ref.rollout.max_num_batched_tokens=18432",
    "actor_rollout_ref.rollout.gpu_memory_utilization=0.8",
    "data.val_files=${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/plain.parquet",
    "data.train_files=${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/plain.parquet",
    "ray_init.num_cpus=40"
  ],
  "scorer_sha256": "bc55b01fa03a5dd98b660b4b47196fc794e38f90184193667df9685ff1c97b2d"
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/status.json](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "failed",
  "finished": "2026-10-06T10:16:12.156748+00:00",
  "error": "Inference exited 1"
}
```

</details>

- [exps/qwen3-06b-reasoning-16k-20261006/status.json](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "cancelled_for_32k",
  "stopped_at": "2026-10-06T10:17:24.642451+00:00",
  "remaining_pids": []
}
```

</details>

- [exps/qwen3-06b-reasoning-16k-20261006/status.json](../history/local_saved/cfceb8edc55a/exps/qwen3-06b-reasoning-16k-20261006/status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "running",
  "started": "2026-10-06T10:14:41.470229+00:00"
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/run.py](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/attempts/attempt1/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-reasoning-16k-20261006/run.py](../artifacts/exps/qwen3-06b-reasoning-16k-20261006/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
