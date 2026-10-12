# exps/qwen3-06b-unseen-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/qwen3-06b-unseen-20261005/summary.json](../artifacts/exps/qwen3-06b-unseen-20261005/summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "benchmark_counts": {
    "APO_AIME24": 480,
    "APO_AIME25": 480,
    "APO_AMC23": 640,
    "APO_MATH300": 316
  },
  "code_commit": "7875751",
  "models": {
    "base": {
      "gsm_validation_loss": null,
      "macro_accuracy": 0.0031645569620253164,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.0,
          "format": 1.0,
          "invalid_answer": 0.825
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.0,
          "format": 1.0,
          "invalid_answer": 0.8416666666666667
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.0,
          "format": 1.0,
          "invalid_answer": 0.8046875
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.012658227848101266,
          "pass_at_n": 0.012658227848101266,
          "parallel": 0.0,
          "format": 1.0,
          "invalid_answer": 0.7626582278481012
        }
      }
    },
    "epoch-1": {
      "gsm_validation_loss": 1.1427466869354248,
      "macro_accuracy": 0.05614286656118144,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.004166666666666667,
          "pass_at_n": 0.06666666666666667,
          "parallel": 0.035416666666666666,
          "format": 0.8854166666666666,
          "invalid_answer": 0.04583333333333333
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.004166666666666667,
          "pass_at_n": 0.06666666666666667,
          "parallel": 0.035416666666666666,
          "format": 0.8416666666666667,
          "invalid_answer": 0.041666666666666664
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.0421875,
          "pass_at_n": 0.35,
          "parallel": 0.025,
          "format": 0.8609375,
          "invalid_answer": 0.046875
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.17405063291139242,
          "pass_at_n": 0.17405063291139242,
          "parallel": 0.015822784810126583,
          "format": 0.8924050632911392,
          "invalid_answer": 0.04746835443037975
        }
      }
    },
    "epoch-2": {
      "gsm_validation_loss": 1.1355059146881104,
      "macro_accuracy": 0.052948641877637134,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0020833333333333333,
          "pass_at_n": 0.03333333333333333,
          "parallel": 0.2708333333333333,
          "format": 0.25,
          "invalid_answer": 0.04583333333333333
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.23541666666666666,
          "format": 0.25625,
          "invalid_answer": 0.05625
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.0578125,
          "pass_at_n": 0.375,
          "parallel": 0.275,
          "format": 0.2140625,
          "invalid_answer": 0.0453125
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.1518987341772152,
          "pass_at_n": 0.1518987341772152,
          "parallel": 0.27531645569620256,
          "format": 0.19936708860759494,
          "invalid_answer": 0.05379746835443038
        }
      }
    },
    "epoch-3": {
      "gsm_validation_loss": 1.174557089805603,
      "macro_accuracy": 0.0775959256329114,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.008333333333333333,
          "pass_at_n": 0.03333333333333333,
          "parallel": 0.5145833333333333,
          "format": 0.025,
          "invalid_answer": 0.05
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.004166666666666667,
          "pass_at_n": 0.06666666666666667,
          "parallel": 0.5854166666666667,
          "format": 0.027083333333333334,
          "invalid_answer": 0.05416666666666667
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.0921875,
          "pass_at_n": 0.575,
          "parallel": 0.578125,
          "format": 0.0234375,
          "invalid_answer": 0.04375
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.20569620253164558,
          "pass_at_n": 0.20569620253164558,
          "parallel": 0.5284810126582279,
          "format": 0.022151898734177215,
          "invalid_answer": 0.04113924050632911
        }
      }
    },
    "epoch-4": {
      "gsm_validation_loss": 1.2116732597351074,
      "macro_accuracy": 0.083082805907173,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.6354166666666666,
          "format": 0.022916666666666665,
          "invalid_answer": 0.027083333333333334
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.004166666666666667,
          "pass_at_n": 0.06666666666666667,
          "parallel": 0.6229166666666667,
          "format": 0.025,
          "invalid_answer": 0.03958333333333333
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.075,
          "pass_at_n": 0.5,
          "parallel": 0.5953125,
          "format": 0.015625,
          "invalid_answer": 0.0328125
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.25316455696202533,
          "pass_at_n": 0.25316455696202533,
          "parallel": 0.6107594936708861,
          "format": 0.012658227848101266,
          "invalid_answer": 0.028481012658227847
        }
      }
    },
    "epoch-5": {
      "gsm_validation_loss": 1.2279167175292969,
      "macro_accuracy": 0.08705003955696203,
      "benchmarks": {
        "APO_AIME24": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.0,
          "pass_at_n": 0.0,
          "parallel": 0.5666666666666667,
          "format": 0.04791666666666667,
          "invalid_answer": 0.03958333333333333
        },
        "APO_AIME25": {
          "answers": 480,
          "questions": 30,
          "n": 16,
          "accuracy": 0.00625,
          "pass_at_n": 0.1,
          "parallel": 0.5625,
          "format": 0.0375,
          "invalid_answer": 0.04583333333333333
        },
        "APO_AMC23": {
          "answers": 640,
          "questions": 40,
          "n": 16,
          "accuracy": 0.1109375,
          "pass_at_n": 0.625,
          "parallel": 0.6171875,
          "format": 0.028125,
          "invalid_answer": 0.034375
        },
        "APO_MATH300": {
          "answers": 316,
          "questions": 316,
          "n": 1,
          "accuracy": 0.2310126582278481,
          "pass_at_n": 0.2310126582278481,
          "parallel": 0.629746835443038,
          "format": 0.02531645569620253,
          "invalid_answer": 0.0379746835443038
        }
      }
    }
  }
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-unseen-20261005/launch.sh](../artifacts/exps/qwen3-06b-unseen-20261005/launch.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
