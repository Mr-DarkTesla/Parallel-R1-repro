# exps/branch-diversity-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/branch-diversity-20261006/manifest.json](../artifacts/exps/branch-diversity-20261006/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "dataset": "HuggingFaceH4/MATH-500",
  "revision": "6e4ed1a2a79af7d8630a6b768ec859cb5af4d3be",
  "rows": 500,
  "unique_questions": 500,
  "dataset_sha256": "32317851fa9be3c3d949c4709c18ec3b40c0efbe79b5bdef72a0addad1446658",
  "checkpoint": "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/final",
  "mode": "async",
  "temperature": 1.0,
  "gpus": [
    0,
    1
  ],
  "command": [
    "bash",
    "training_scripts/eval_qwen3_06b.sh",
    "${PROJECT_ROOT}/exps/fixes-20261005/results/train/Parallel-SFT-Seen-Qwen3-0.6B-fixed-mb4-20261005/final",
    "data.val_batch_size=1024",
    "data.val_files=${PROJECT_ROOT}/exps/branch-diversity-20261006/math500.parquet",
    "ray_init.num_cpus=16"
  ],
  "started": "2026-10-06T07:18:49.641818+00:00"
}
```

</details>

## Метрики и полнота результатов

- [exps/branch-diversity-20261006/eval-summary.json](../artifacts/exps/branch-diversity-20261006/eval-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "answers": 500,
  "correct": 105,
  "accuracy": 0.21,
  "traces_sha256": "992e43541087a4f9584a378bc9c213dfab0d4792430b6a85c219928e30067e79"
}
```

</details>

- [exps/branch-diversity-20261006/math500-analysis/semantic-summary.json](../artifacts/exps/branch-diversity-20261006/math500-analysis/semantic-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "review": "Manual semantic review by Codex, one reviewer; not an external judge benchmark",
  "denominator": "60 uniformly sampled structurally readable two-path blocks out of958; block frequency, not answer frequency",
  "sample_seed": 20261006,
  "sample_unique_questions": 59,
  "categories": {
    "same_method": 28,
    "degenerate_or_unclear": 26,
    "distinct": 6
  },
  "percent": {
    "same_method": 46.666666666666664,
    "degenerate_or_unclear": 43.333333333333336,
    "distinct": 10.0
  },
  "correct_answer_sample_categories": {
    "same_method": 6,
    "distinct": 2,
    "degenerate_or_unclear": 2
  }
}
```

</details>

- [exps/branch-diversity-20261006/results/eval/seen-math500-async/driver.log](../artifacts/exps/branch-diversity-20261006/results/eval/seen-math500-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.
