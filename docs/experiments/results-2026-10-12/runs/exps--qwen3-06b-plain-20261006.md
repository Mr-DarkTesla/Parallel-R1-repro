# exps/qwen3-06b-plain-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-plain-20261006/manifest.json](../artifacts/exps/qwen3-06b-plain-20261006/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "started": "2026-10-06T09:48:40.581226+00:00",
  "decoding": "ordinary autoregressive, rollout.mode=sync",
  "parallel_tokens_added": false,
  "parallel_instructions": false,
  "temperature": 1.0,
  "max_response_tokens": 3000,
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
  }
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-plain-20261006/results/eval/instant/driver.log](../artifacts/exps/qwen3-06b-plain-20261006/results/eval/instant/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/qwen3-06b-plain-20261006/results/eval/instant/summary.json](../artifacts/exps/qwen3-06b-plain-20261006/results/eval/instant/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-06T10:01:28.877487+00:00",
  "answers": 7156,
  "benchmarks": {
    "APO_AIME24": {
      "questions": 30,
      "samples_per_question": 16,
      "answers": 480,
      "correct": 1,
      "accuracy": 0.0020833333333333333,
      "observed_pass_at_n": 0.03333333333333333,
      "invalid_answer": 0.03125,
      "parallel_tag_responses": 0
    },
    "APO_AIME25": {
      "questions": 30,
      "samples_per_question": 16,
      "answers": 480,
      "correct": 3,
      "accuracy": 0.00625,
      "observed_pass_at_n": 0.06666666666666667,
      "invalid_answer": 0.03333333333333333,
      "parallel_tag_responses": 0
    },
    "APO_AMC23": {
      "questions": 40,
      "samples_per_question": 16,
      "answers": 640,
      "correct": 40,
      "accuracy": 0.0625,
      "observed_pass_at_n": 0.4,
      "invalid_answer": 0.021875,
      "parallel_tag_responses": 0
    },
    "APO_MATH300": {
      "questions": 316,
      "samples_per_question": 16,
      "answers": 5056,
      "correct": 850,
      "accuracy": 0.16811708860759494,
      "observed_pass_at_n": 0.6107594936708861,
      "invalid_answer": 0.011669303797468354,
      "parallel_tag_responses": 0
    },
    "APO_MATH500": {
      "questions": 500,
      "samples_per_question": 1,
      "answers": 500,
      "correct": 84,
      "accuracy": 0.168,
      "observed_pass_at_n": 0.168,
      "invalid_answer": 0.004,
      "parallel_tag_responses": 0
    }
  },
  "traces_sha256": "c44af8b84ec2c12d52015ae06454652920870a0155256bcaa521ab80a60529bf"
}
```

</details>

- [exps/qwen3-06b-plain-20261006/results/eval/reasoning/driver.log](../artifacts/exps/qwen3-06b-plain-20261006/results/eval/reasoning/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/qwen3-06b-plain-20261006/results/eval/reasoning/summary.json](../artifacts/exps/qwen3-06b-plain-20261006/results/eval/reasoning/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-06T10:07:18.084286+00:00",
  "answers": 7156,
  "benchmarks": {
    "APO_AIME24": {
      "questions": 30,
      "samples_per_question": 16,
      "answers": 480,
      "correct": 0,
      "accuracy": 0.0,
      "observed_pass_at_n": 0.0,
      "invalid_answer": 1.0,
      "parallel_tag_responses": 0
    },
    "APO_AIME25": {
      "questions": 30,
      "samples_per_question": 16,
      "answers": 480,
      "correct": 1,
      "accuracy": 0.0020833333333333333,
      "observed_pass_at_n": 0.03333333333333333,
      "invalid_answer": 0.9854166666666667,
      "parallel_tag_responses": 0
    },
    "APO_AMC23": {
      "questions": 40,
      "samples_per_question": 16,
      "answers": 640,
      "correct": 29,
      "accuracy": 0.0453125,
      "observed_pass_at_n": 0.325,
      "invalid_answer": 0.8453125,
      "parallel_tag_responses": 0
    },
    "APO_MATH300": {
      "questions": 316,
      "samples_per_question": 16,
      "answers": 5056,
      "correct": 1135,
      "accuracy": 0.2244857594936709,
      "observed_pass_at_n": 0.6107594936708861,
      "invalid_answer": 0.5261075949367089,
      "parallel_tag_responses": 0
    },
    "APO_MATH500": {
      "questions": 500,
      "samples_per_question": 1,
      "answers": 500,
      "correct": 105,
      "accuracy": 0.21,
      "observed_pass_at_n": 0.21,
      "invalid_answer": 0.578,
      "parallel_tag_responses": 0
    }
  },
  "traces_sha256": "4fd25d9ea93a01ad59eb7c7676442c25e0286b3d05ab48f8bf26451c84701ec7"
}
```

</details>

- [exps/qwen3-06b-plain-20261006/status.json](../artifacts/exps/qwen3-06b-plain-20261006/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "instant": {
    "updated": "2026-10-06T10:01:29.093725+00:00",
    "status": "complete",
    "answers": 7156,
    "summary": "${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/results/eval/instant/summary.json"
  },
  "reasoning": {
    "updated": "2026-10-06T10:07:18.225245+00:00",
    "status": "complete",
    "answers": 7156,
    "summary": "${PROJECT_ROOT}/exps/qwen3-06b-plain-20261006/results/eval/reasoning/summary.json"
  }
}
```

</details>

## Исходники рецепта и награды

- [exps/qwen3-06b-plain-20261006/run.py](../artifacts/exps/qwen3-06b-plain-20261006/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
