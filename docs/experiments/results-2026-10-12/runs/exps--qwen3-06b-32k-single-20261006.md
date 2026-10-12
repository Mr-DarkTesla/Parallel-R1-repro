# exps/qwen3-06b-32k-single-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-32k-single-20261006/manifest.json](../artifacts/exps/qwen3-06b-32k-single-20261006/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "started": "2026-10-06T11:05:17.735238+00:00",
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "weights_sha256": {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
  },
  "max_response_tokens": 32768,
  "samples_per_question": 1,
  "primary_math": "MATH-500",
  "includes_math316": true,
  "answers_per_run": 916,
  "total_answers": 3664,
  "data_sha256": "a611fc8d93635ae962d7403cc379c84ce8aef7c768590d20c4ad49cc8a37c56e",
  "profiles": {
    "baseline-instant": {
      "mode": "instant",
      "temperature": 1.0,
      "top_p": 1.0,
      "top_k": -1,
      "presence_penalty": 0.0
    },
    "baseline-reasoning": {
      "mode": "reasoning",
      "temperature": 1.0,
      "top_p": 1.0,
      "top_k": -1,
      "presence_penalty": 0.0
    },
    "author-instant": {
      "mode": "instant",
      "temperature": 0.7,
      "top_p": 0.8,
      "top_k": 20,
      "presence_penalty": 1.5
    },
    "author-reasoning": {
      "mode": "reasoning",
      "temperature": 0.6,
      "top_p": 0.95,
      "top_k": 20,
      "presence_penalty": 0.0
    }
  },
  "decoder": "ordinary autoregressive sync, TP=1",
  "gpus_per_run": 4,
  "val_batch_size": 128,
  "max_num_batched_tokens": 34816,
  "code_origin_sha256": "3e8b93667c83c3a90361d5b8cb73f6e62b7abcdbac8ce9f1eee6c65c7721e5f1",
  "logging_patch_sha256": {
    "code/verl/verl/workers/rollout/vllm_rollout/vllm_rollout_spmd.py": "5051a5431bc1d4da86a90ed3a1bf16eb4c559b0625a2c5de5b31b7fd40038e40",
    "code/verl/verl/trainer/ppo/ray_trainer.py": "66d510cba4dde4f4eb7a3f1656c1bb1202f64ced8e4d3893d96a6e2434d882ea"
  },
  "scorer_sha256": "1135e648186b5fd1d41f2377dc13d3b0475ed37e26beb42a7b5c04ca9433a1da",
  "author_reference": "https://arxiv.org/html/2505.09388v1#S4.SS6",
  "note": "Authors use 38912 tokens and 64 samples for AIME. Here all four runs use the requested 32768 tokens and one sample per question. Prompts and non-symbolic verifier differ from the public protocol; only author sampling parameters are reproduced. Original and corrected extraction metrics are both retained."
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-32k-single-20261006/status.json](../artifacts/exps/qwen3-06b-32k-single-20261006/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "stopped_by_user",
  "stopped_at": "2026-10-06T11:10:35.466474+00:00",
  "future_datasets": [
    "MATH-316",
    "MATH-500"
  ],
  "queue_cancelled": true,
  "remaining_pids": [],
  "partial_artifacts": {
    "baseline-instant": {
      "batches": 3,
      "saved_answers": 384,
      "final_trace_exists": false
    },
    "baseline-reasoning": {
      "batches": 0,
      "saved_answers": 0,
      "final_trace_exists": false
    },
    "author-instant": {
      "batches": 0,
      "saved_answers": 0,
      "final_trace_exists": false
    },
    "author-reasoning": {
      "batches": 0,
      "saved_answers": 0,
      "final_trace_exists": false
    }
  }
}
```

</details>

- [exps/qwen3-06b-32k-single-20261006/status.json](../history/local_saved/c3a055f9fe27/exps/qwen3-06b-32k-single-20261006/status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "baseline-instant": {
    "updated": "2026-10-06T11:05:17.795745+00:00",
    "status": "running",
    "gpus": "0,1,2,3"
  },
  "baseline-reasoning": {
    "updated": "2026-10-06T11:05:17.903576+00:00",
    "status": "running",
    "gpus": "4,5,6,7"
  },
  "author-instant": {
    "updated": "2026-10-06T11:05:17.751529+00:00",
    "status": "queued"
  },
  "author-reasoning": {
    "updated": "2026-10-06T11:05:17.754559+00:00",
    "status": "queued"
  }
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-32k-single-20261006/run.py](../artifacts/exps/qwen3-06b-32k-single-20261006/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
