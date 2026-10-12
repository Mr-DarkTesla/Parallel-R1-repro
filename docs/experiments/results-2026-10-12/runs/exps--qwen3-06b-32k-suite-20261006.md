# exps/qwen3-06b-32k-suite-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-32k-suite-20261006/manifest.json](../artifacts/exps/qwen3-06b-32k-suite-20261006/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "started": "2026-10-06T10:20:01.622600+00:00",
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "weights_sha256": {
    "model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
  },
  "max_response_tokens": 32768,
  "samples_per_question": 16,
  "primary_math": "MATH-500",
  "includes_math316": true,
  "answers_per_run": 14656,
  "total_answers": 58624,
  "data_sha256": "fab98525125a0c4a2dae5b12e7e099d424a7d22e42f16ed5a35894de42997ba8",
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
    "code/verl/verl/trainer/ppo/ray_trainer.py": "1c7fb7c306610ba462d7c70caa25b578b0af455fda3e7ddcb934d0f06b1eb712"
  },
  "scorer_sha256": "c6448d73b8ed2a1a9cd7807d1f5c08869067117eefd95c42c5d597838a1726c3",
  "author_reference": "https://arxiv.org/html/2505.09388v1#S4.SS6",
  "note": "Authors use 38912 tokens and 64 samples for AIME. Here all four runs use the requested 32768 tokens and 16 samples. Prompts and non-symbolic verifier differ from the public protocol; only author sampling parameters are reproduced. Original and corrected extraction metrics are both retained."
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-32k-suite-20261006/status.json](../artifacts/exps/qwen3-06b-32k-suite-20261006/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "cancelled_for_single_sample",
  "controller": 356519,
  "children": "86 records; see original artifact",
  "reason": "User requested one answer per question with accuracy CI; stop 16-repeat suite",
  "time": "2026-10-06T11:04:34.248169+00:00",
  "remaining": []
}
```

</details>

- [exps/qwen3-06b-32k-suite-20261006/status.json](../history/local_saved/50fe62fe4cd6/exps/qwen3-06b-32k-suite-20261006/status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "baseline-instant": {
    "updated": "2026-10-06T10:20:01.649909+00:00",
    "status": "running",
    "gpus": "0,1,2,3"
  },
  "baseline-reasoning": {
    "updated": "2026-10-06T10:20:01.653425+00:00",
    "status": "running",
    "gpus": "4,5,6,7"
  },
  "author-instant": {
    "updated": "2026-10-06T10:20:01.633155+00:00",
    "status": "queued"
  },
  "author-reasoning": {
    "updated": "2026-10-06T10:20:01.635087+00:00",
    "status": "queued"
  }
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-32k-suite-20261006/run.py](../artifacts/exps/qwen3-06b-32k-suite-20261006/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
