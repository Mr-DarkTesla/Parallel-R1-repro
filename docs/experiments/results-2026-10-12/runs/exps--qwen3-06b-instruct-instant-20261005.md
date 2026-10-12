# exps/qwen3-06b-instruct-instant-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-instruct-instant-20261005/model-source.json](../artifacts/exps/qwen3-06b-instruct-instant-20261005/model-source.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "path": "${MODEL_ROOT}/Qwen3-0.6B-Instruct-Instant",
  "weights_path": "${MODEL_ROOT}/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca",
  "enable_thinking": false
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-instruct-instant-20261005/summary.csv](../artifacts/exps/qwen3-06b-instruct-instant-20261005/summary.csv) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/qwen3-06b-instruct-instant-20261005/summary.json](../artifacts/exps/qwen3-06b-instruct-instant-20261005/summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "model": {
    "model": "Qwen/Qwen3-0.6B",
    "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
    "path": "${MODEL_ROOT}/Qwen3-0.6B-Instruct-Instant",
    "weights_path": "${MODEL_ROOT}/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca",
    "enable_thinking": false
  },
  "answers": 1916,
  "benchmarks": {
    "APO_AIME24": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "accuracy": 0.00625,
      "observed_pass_at_n": 0.06666666666666667,
      "bootstrap_best_at_n": 0.051866666666666665,
      "parallel": 0.8958333333333334,
      "invalid_answer": 0.010416666666666666
    },
    "APO_AIME25": {
      "answers": 480,
      "questions": 30,
      "n": 16,
      "accuracy": 0.0,
      "observed_pass_at_n": 0.0,
      "bootstrap_best_at_n": 0.0,
      "parallel": 0.9104166666666667,
      "invalid_answer": 0.010416666666666666
    },
    "APO_AMC23": {
      "answers": 640,
      "questions": 40,
      "n": 16,
      "accuracy": 0.034375,
      "observed_pass_at_n": 0.3,
      "bootstrap_best_at_n": 0.23017499999999996,
      "parallel": 0.934375,
      "invalid_answer": 0.00625
    },
    "APO_MATH300": {
      "answers": 316,
      "questions": 316,
      "n": 1,
      "accuracy": 0.13924050632911392,
      "observed_pass_at_n": 0.13924050632911392,
      "bootstrap_best_at_n": null,
      "parallel": 0.9620253164556962,
      "invalid_answer": 0.00949367088607595
    }
  },
  "macro_accuracy": 0.04496637658227848
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-instruct-instant-20261005/launch.sh](../artifacts/exps/qwen3-06b-instruct-instant-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
