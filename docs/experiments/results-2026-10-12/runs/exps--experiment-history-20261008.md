# exps/experiment-history-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/experiment-history-20261008/summary.json](../artifacts/exps/experiment-history-20261008/summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "window_start_msk": "2026-10-07T16:00:00+03:00",
  "observed_utc": "2026-10-08T08:51:13.724035+00:00",
  "training": [
    {
      "run": "rl-unseen-s2-bs32-500-20261007",
      "dataset": "DAPO",
      "reward": "S2",
      "start_msk": "2026-10-07T15:40:37+03:00",
      "finish_msk": "2026-10-07T18:43:24+03:00",
      "status": "complete",
      "steps_total": 500,
      "resumed_from_step": 30,
      "math316_accuracy": 0.3860759493670886
    },
    {
      "run": "gsm-unseen-two-rewards-20261008/s2",
      "dataset": "GSM-Infinite",
      "reward": "S2",
      "start_msk": "2026-10-08T00:19:09+03:00",
      "finish_msk": "2026-10-08T05:21:39+03:00",
      "status": "complete",
      "steps_total": 800,
      "gsm256_accuracy": 0.91796875,
      "math316_accuracy": 0.3924050632911392
    },
    {
      "run": "gsm-unseen-two-rewards-20261008/depth",
      "dataset": "GSM-Infinite",
      "reward": "c - 1e-4 D",
      "start_msk": "2026-10-08T05:21:41+03:00",
      "finish_msk": "2026-10-08T07:07:11+03:00",
      "status": "complete",
      "steps_total": 800,
      "gsm256_accuracy": 0.83984375,
      "math316_accuracy": 0.10443037974683544
    },
    {
      "run": "gsm-unseen-split-rewards-400-20261008/gated_depth",
      "dataset": "GSM-Infinite",
      "reward": "c(1 - 1e-4 D), split advantage",
      "start_msk": "2026-10-08T09:13:40+03:00",
      "status": "running",
      "steps_observed": 394,
      "steps_target": 400,
      "last_validation_step": 350,
      "gsm256_accuracy": 0.8515625,
      "math316_accuracy": 0.3670886075949367
    },
    {
      "run": "gsm-unseen-split-rewards-400-20261008/parallel_gain",
      "dataset": "GSM-Infinite",
      "reward": "c + 0.2 c valid_parallel (1-D/T), split advantage",
      "status": "queued",
      "steps_target": 400
    }
  ],
  "screening": {
    "gsm_infinite": {
      "questions": 256,
      "accuracy": 0.185546875,
      "accuracy_cluster_bootstrap_ci95": [
        0.1640625,
        0.20703125
      ],
      "k_of_8": {
        "0": 72,
        "1": 78,
        "2": 55,
        "3": 27,
        "4": 15,
        "5": 5,
        "6": 2,
        "7": 2,
        "8": 0
      },
      "mixed_fraction": 0.71875,
      "correct_parallel_and_plain_groups": 12,
      "answers": 2048,
      "legacy_accuracy": 0.18701171875,
      "scorer_disagreements": 3,
      "scorer_errors": 0,
      "extraction_failures": 126,
      "parallel_fraction": 0.9619140625,
      "format_error_fraction": 0.04345703125,
      "trace_count": 2048,
      "response_tokens": 1418840,
      "at_token_budget": 31,
      "generation_wall_seconds": 501.73539185523987,
      "mixed_groups_per_generation_minute": 22.003630158873165,
      "mixed_groups_per_million_response_tokens": 129.68340334357643,
      "total_wall_seconds": 897.3597013950348,
      "unique_gold_strings": 15,
      "top_gold": [
        [
          "4",
          61
        ],
        [
          "2",
          59
        ],
        [
          "3",
          41
        ],
        [
          "1",
          25
        ],
        [
          "6",
          18
        ]
      ],
      "best_constant_answer_accuracy": 0.23828125,
      "mean_prompt_tokens": 592.30859375,
      "mean_response_tokens": 692.79296875
    },
    "dapo": {
      "questions": 256,
      "accuracy": 0.04443359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.03369140625,
        0.056640625
      ],
      "k_of_8": {
        "0": 194,
        "1": 43,
        "2": 13,
        "3": 3,
        "4": 2,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0
      },
      "mixed_fraction": 0.2421875,
      "correct_parallel_and_plain_groups": 0,
      "answers": 2048,
      "legacy_accuracy": 0.044921875,
      "scorer_disagreements": 3,
      "scorer_errors": 0,
      "extraction_failures": 62,
      "parallel_fraction": 0.91650390625,
      "format_error_fraction": 0.06298828125,
      "trace_count": 2048,
      "response_tokens": 2061333,
      "at_token_budget": 49,
      "generation_wall_seconds": 507.6208481788635,
      "mixed_groups_per_generation_minute": 7.328304212377884,
      "mixed_groups_per_million_response_tokens": 30.07762452742958,
      "total_wall_seconds": 932.8691782951355,
      "unique_gold_strings": 142,
      "top_gold": [
        [
          "1",
          15
        ],
        [
          "4",
          12
        ],
        [
          "7",
          10
        ],
        [
          "3",
          9
        ],
        [
          "5",
          9
        ]
      ],
      "best_constant_answer_accuracy": 0.05859375,
      "mean_prompt_tokens": 275.3359375,
      "mean_response_tokens": 1006.51025390625
    },
    "bigmath_orca": {
      "questions": 256,
      "accuracy": 0.318359375,
      "accuracy_cluster_bootstrap_ci95": [
        0.2783203125,
        0.359375
      ],
      "k_of_8": {
        "0": 94,
        "1": 36,
        "2": 16,
        "3": 17,
        "4": 18,
        "5": 24,
        "6": 28,
        "7": 11,
        "8": 12
      },
      "mixed_fraction": 0.5859375,
      "correct_parallel_and_plain_groups": 1,
      "answers": 2048,
      "legacy_accuracy": 0.3056640625,
      "scorer_disagreements": 30,
      "scorer_errors": 0,
      "extraction_failures": 44,
      "parallel_fraction": 0.9951171875,
      "format_error_fraction": 0.03125,
      "trace_count": 2048,
      "response_tokens": 1215945,
      "at_token_budget": 12,
      "generation_wall_seconds": 449.60237073898315,
      "mixed_groups_per_generation_minute": 20.0176880411179,
      "mixed_groups_per_million_response_tokens": 123.36084280127803,
      "total_wall_seconds": 845.9828708171844,
      "unique_gold_strings": 153,
      "top_gold": [
        [
          "2",
          12
        ],
        [
          "10",
          11
        ],
        [
          "6",
          10
        ],
        [
          "4",
          8
        ],
        [
          "8",
          6
        ]
      ],
      "best_constant_answer_accuracy": 0.046875,
      "mean_prompt_tokens": 246.5234375,
      "mean_response_tokens": 593.72314453125
    },
    "bigmath_cn_k12": {
      "questions": 256,
      "accuracy": 0.21044921875,
      "accuracy_cluster_bootstrap_ci95": [
        0.17578125,
        0.248046875
      ],
      "k_of_8": {
        "0": 127,
        "1": 38,
        "2": 26,
        "3": 9,
        "4": 17,
        "5": 16,
        "6": 1,
        "7": 16,
        "8": 6
      },
      "mixed_fraction": 0.48046875,
      "correct_parallel_and_plain_groups": 4,
      "answers": 2048,
      "legacy_accuracy": 0.18505859375,
      "scorer_disagreements": 94,
      "scorer_errors": 0,
      "extraction_failures": 33,
      "parallel_fraction": 0.978515625,
      "format_error_fraction": 0.0537109375,
      "trace_count": 2048,
      "response_tokens": 1665353,
      "at_token_budget": 22,
      "generation_wall_seconds": 488.655645608902,
      "mixed_groups_per_generation_minute": 15.102659851200452,
      "mixed_groups_per_million_response_tokens": 73.85821504509855,
      "total_wall_seconds": 887.7934865951538,
      "unique_gold_strings": 185,
      "top_gold": [
        [
          "1",
          16
        ],
        [
          "2",
          13
        ],
        [
          "4",
          10
        ],
        [
          "10",
          7
        ],
        [
          "9",
          6
        ]
      ],
      "best_constant_answer_accuracy": 0.0625,
      "mean_prompt_tokens": 241.1953125,
      "mean_response_tokens": 813.16064453125
    }
  },
  "screening_window_msk": [
    "2026-10-07T21:20:07+03:00",
    "2026-10-07T22:20:15+03:00"
  ],
  "acceptance_tests": [
    {
      "run": "gsm-unseen-two-rewards-20261008/smoke-depth",
      "steps": 2,
      "complete": true
    },
    {
      "run": "gsm-unseen-split-rewards-400-20261008/smoke-gated_depth",
      "steps": 2,
      "complete": true
    },
    {
      "run": "gsm-unseen-split-rewards-400-20261008/smoke-parallel_gain",
      "steps": 2,
      "complete": true
    }
  ],
  "not_trained": {
    "run": "gsm-unseen-efficiency-pilot-20261008",
    "reason": "Prepared 200-step proposal failed preflight; no GPU training launched. Replaced by agreed pair400."
  }
}
```

</details>

## Графики

- [exps/experiment-history-20261008/dapo-s2-500.png](../artifacts/exps/experiment-history-20261008/dapo-s2-500.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/dapo-s2-500.svg](../artifacts/exps/experiment-history-20261008/dapo-s2-500.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/gsm-all-experiments-1156.png](../artifacts/exps/experiment-history-20261008/gsm-all-experiments-1156.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/gsm-all-experiments-1156.svg](../artifacts/exps/experiment-history-20261008/gsm-all-experiments-1156.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/gsm-all-experiments-final.png](../artifacts/exps/experiment-history-20261008/gsm-all-experiments-final.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/gsm-all-experiments-final.svg](../artifacts/exps/experiment-history-20261008/gsm-all-experiments-final.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/reward-components-final.png](../artifacts/exps/experiment-history-20261008/reward-components-final.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/reward-components-final.svg](../artifacts/exps/experiment-history-20261008/reward-components-final.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [exps/experiment-history-20261008/plot_by_dataset.py](../artifacts/exps/experiment-history-20261008/plot_by_dataset.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/experiment-history-20261008/plot_final.py](../artifacts/exps/experiment-history-20261008/plot_final.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
