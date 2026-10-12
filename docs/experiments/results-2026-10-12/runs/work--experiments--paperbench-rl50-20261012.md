# work/experiments/paperbench-rl50-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/paperbench-rl50-20261012/manifest.json](../artifacts/work/experiments/paperbench-rl50-20261012/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "gpus": 8,
  "host_role": "mpiworker-2",
  "checkpoint": 50,
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "samples_per_question": 1,
  "jobs": [
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime26-job.json"
  ],
  "sources": {
    "AIME24_25_canonical_proof": {
      "rows": 60,
      "counts": {
        "2024": 30,
        "2025": 30
      },
      "sha256": "9f2c3049a11bc87f177ab276a8f75e6e9f666e0d9a1bf239d51c594dfb006677",
      "repairs": [
        {
          "year": 2025,
          "id": "18",
          "repair": "bare rac{ restored to backslash frac{; corroborated numbered AllenAI same question and answer"
        },
        {
          "year": 2025,
          "id": "27",
          "repair": "bare rac{ restored to backslash frac{; corroborated numbered AllenAI same question and answer"
        }
      ],
      "cross_source_proof": "aime2025-inventory-proof.json",
      "not_used_for_curriculum_selection": true
    },
    "AMC2023": {
      "repo": "math-ai/amc23",
      "revision": "80815d37005feb82cd7f8fbc6901d5d3eff43057",
      "raw_sha256": "b696e87ba47be4e879a60fd4ef1d4aa522ba78c5ae013c6aff5cc9788a397c5e",
      "file": "test-00000-of-00001.parquet",
      "rows": 40,
      "upstream_schema": [
        "id",
        "answer",
        "url",
        "question"
      ],
      "usage": "evaluation-only; not training, curriculum, reward or checkpoint selection"
    },
    "AIME2026": {
      "repo": "MathArena/aime_2026",
      "revision": "d2de22f3c656b4f56cf8981212186377d1e23bc3",
      "raw_sha256": "d91db799651b4cc1f0734f52792a695c9cc60dac342524b3d8e5b2ff31c3e957",
      "file": "data/train-00000-of-00001.parquet",
      "rows": 30,
      "upstream_schema": [
        "problem_idx",
        "answer",
        "problem"
      ],
      "usage": "evaluation-only; not training, curriculum, reward or checkpoint selection"
    }
  },
  "question_counts": {
    "AIME2024": 30,
    "AIME2025": 30,
    "AMC2023": 40,
    "AIME2026": 30
  },
  "exact_problem_overlaps_with_train1024": [],
  "semantic_decontamination_not_exhaustive": true,
  "all_eval_only": true,
  "full_traces": true,
  "sha256": {
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/worker.py": "467e2f1539da29dc9d3d1f3b8b3accd1204a8564de53b4879939880d40cd1326",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/finalize.py": "114d7f9eaf5bb108fb67d10c7399d918cc349326a5cbbe47b169da081eda2115",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/launch.py": "3fc6cee2c1abb8bfe538c2166ef5a6a4b122526deab3ea24ada11cfb89dc1516",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json": "a23ca7fcc2b7becd44faf43f94be08935778f0ffe08a2125c89fc1a0d6d4b6ef",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime26-job.json": "c12189a90df5e9f84da58f58cc24c6e3694c4c1baf71ac1526fd63cff88270dd",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/data/aime24-25-amc23.jsonl": "01fecf6731099f12a771bfed4a23748fa9bf592b2d9f0d074eaf40ecc9a3cb72",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/data/aime26.jsonl": "21caa3222afc7de1854e78af175d179df31e541574a43c21be4f7242e1af3b4c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch-r1-independent.py": "bb04eec302d11df3d211dfb14da59ed0868a89a81b7e23fc5f4c692810164026",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4"
  }
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json-exits.json](../artifacts/work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "returncodes": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791806003.2170784
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/aime26-job.json-exits.json](../artifacts/work/experiments/paperbench-rl50-20261012/aime26-job.json-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "returncodes": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791806479.1979568
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/aime26-readiness.json](../artifacts/work/experiments/paperbench-rl50-20261012/aime26-readiness.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "time": 1791805765.311552,
  "config_sha256": "c12189a90df5e9f84da58f58cc24c6e3694c4c1baf71ac1526fd63cff88270dd",
  "questions_sha256": "21caa3222afc7de1854e78af175d179df31e541574a43c21be4f7242e1af3b4c",
  "samples_per_question": 1,
  "rows": 30,
  "full_traces": true,
  "fullwidth8": true,
  "current_pipeline_status": {
    "state": "evaluating",
    "host": "RUN_5482aee87e-mpiworker-2",
    "time": 1791804595.2045739,
    "job": "aime24-25-amc23-job.json"
  },
  "automatic_next_after_first100_clean_exits": true
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/result.json](../artifacts/work/experiments/paperbench-rl50-20261012/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "checkpoint": 50,
  "samples_per_question": 1,
  "jobs": [
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json",
    "${PROJECT_ROOT}/work/experiments/paperbench-rl50-20261012/aime26-job.json"
  ],
  "time": 1791806479.4609175
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/runs/aime24-25-amc23/summary.json](../artifacts/work/experiments/paperbench-rl50-20261012/runs/aime24-25-amc23/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "checkpoint": 50,
  "completed": 100,
  "missing": 0,
  "technical_unknowns": 0,
  "samples_per_question": 1,
  "by_dataset": {
    "AIME2024": {
      "completed": 30,
      "correct": 8,
      "accuracy": 0.26666666666666666,
      "format_valid": 15,
      "format_and_fork_count_all": 15,
      "correct_and_parallel": 8,
      "mean_actual_forwards_all": 2279.4333333333334,
      "mean_sampled_tokens_all": 3283.5333333333333,
      "format_conditioned": {
        "n": 15,
        "mean_actual_forwards": 1798.6666666666667,
        "mean_width": 3.9375,
        "mean_depth": 1.0666666666666667
      },
      "truncated": 15
    },
    "AIME2025": {
      "completed": 30,
      "correct": 3,
      "accuracy": 0.1,
      "format_valid": 14,
      "format_and_fork_count_all": 14,
      "correct_and_parallel": 3,
      "mean_actual_forwards_all": 2362.0333333333333,
      "mean_sampled_tokens_all": 3500.266666666667,
      "format_conditioned": {
        "n": 14,
        "mean_actual_forwards": 1998.142857142857,
        "mean_width": 4,
        "mean_depth": 1
      },
      "truncated": 16
    },
    "AMC2023": {
      "completed": 40,
      "correct": 24,
      "accuracy": 0.6,
      "format_valid": 33,
      "format_and_fork_count_all": 33,
      "correct_and_parallel": 23,
      "mean_actual_forwards_all": 1725.6,
      "mean_sampled_tokens_all": 2521.925,
      "format_conditioned": {
        "n": 33,
        "mean_actual_forwards": 1529.7272727272727,
        "mean_width": 4.212121212121212,
        "mean_depth": 1
      },
      "truncated": 6
    }
  },
  "all8_exit0": true,
  "traces": {
    "rank-2.jsonl": "469aecad3c68c7adf93b72cf5bebcc37d25268e1e85edd8ee0bd132a80d885bc",
    "rank-5.jsonl": "0999f917ccad199f987ca8edd143b4a5f233df77ebe5842c3cf151c8034bc3e1",
    "rank-7.jsonl": "b6ae6ae6f0907231bff31104632a008e74743cd25035b5332e269ba09b2f9aa1",
    "rank-0.jsonl": "2b161206207f3ce080fce9985cddb4eff91b29f0471dca89624b3b6674603adf",
    "rank-3.jsonl": "1447fe6caf805140bbbb6196db575b4c08bdebfa97f41806ba20e61e73b81963",
    "rank-6.jsonl": "34c514a326a85f0563a71d340160f76e47703b6bfc2b1d6ce5c185b2aab12e33",
    "rank-1.jsonl": "561bc1ab788875513903b09e50f4ff8aae044f7a3d04a2bc189f16fb427e352d",
    "rank-4.jsonl": "4875824359ddfa5453a0336bc95abe494a7476c47c96cbd0ed2f0cf56306b98a"
  },
  "selection_allowed": false,
  "benchmark": true,
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "protocol": "FP32 HF fullwidth8, temperature1,4096response/768path/16384context, native think prefix, corrected scorer, instrumentedF",
  "time": 1791806003.7237706
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/runs/aime26/summary.json](../artifacts/work/experiments/paperbench-rl50-20261012/runs/aime26/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "checkpoint": 50,
  "completed": 30,
  "missing": 0,
  "technical_unknowns": 0,
  "samples_per_question": 1,
  "by_dataset": {
    "AIME2026": {
      "completed": 30,
      "correct": 4,
      "accuracy": 0.13333333333333333,
      "format_valid": 14,
      "format_and_fork_count_all": 14,
      "correct_and_parallel": 4,
      "mean_actual_forwards_all": 2216.4333333333334,
      "mean_sampled_tokens_all": 3491.266666666667,
      "format_conditioned": {
        "n": 14,
        "mean_actual_forwards": 1850.2142857142858,
        "mean_width": 4.357142857142857,
        "mean_depth": 1
      },
      "truncated": 16
    }
  },
  "all8_exit0": true,
  "traces": {
    "rank-0.jsonl": "fd9c72c968c4c72256ac947545c679646156a9c6a57de73ce339deb3cdb52b5e",
    "rank-5.jsonl": "b1dd2fd0b7e4a68f87b16c3ce82e9222c9a3d595051cf5742b9cfc844c217569",
    "rank-4.jsonl": "e6d3d3714edbe290d43cea96635d4bc538e2f85f9e10b39e0b7fcd68cf8fbb9a",
    "rank-7.jsonl": "cbc48e1ce45a9bdc2cec830025b05fcaefa72b392794adc07509a2678ae83687",
    "rank-1.jsonl": "e19db6303144dbab1d81b093bb0b0fbb7a35ceec5d11efed10f62fe822e64c10",
    "rank-6.jsonl": "eceebf2a43d2d728c22adf95483938f643d663fd93d660c7e446d61c6dbda483",
    "rank-2.jsonl": "9f63cd1846d2222b9b7c950dfc9ec2ca3edb287dc53e9ca49da83885c8c4b614",
    "rank-3.jsonl": "bfd6ce4835ccdb75859cb5648c057806a8d7e08504257f9a21c8adde04be8aec"
  },
  "selection_allowed": false,
  "benchmark": true,
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "protocol": "FP32 HF fullwidth8, temperature1,4096response/768path/16384context, native think prefix, corrected scorer, instrumentedF",
  "time": 1791806479.437409
}
```

</details>

- [work/experiments/paperbench-rl50-20261012/status.json](../artifacts/work/experiments/paperbench-rl50-20261012/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "host": "RUN_5482aee87e-mpiworker-2",
  "time": 1791806479.4587932
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/paperbench-rl50-20261012/launch.py](../artifacts/work/experiments/paperbench-rl50-20261012/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/paperbench-rl50-20261012/prepare.py](../artifacts/work/experiments/paperbench-rl50-20261012/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Дополнительно проверенные конфигурации и формулы

- [work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json-launch.json](../artifacts/work/experiments/paperbench-rl50-20261012/aime24-25-amc23-job.json-launch.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
- [work/experiments/paperbench-rl50-20261012/aime26-job.json-launch.json](../artifacts/work/experiments/paperbench-rl50-20261012/aime26-job.json-launch.json) — remote_nfs, снимок 2026-10-12T20:29:26.107420+00:00.
