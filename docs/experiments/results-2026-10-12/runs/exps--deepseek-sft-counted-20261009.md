# exps/deepseek-sft-counted-20261009

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/deepseek-sft-counted-20261009/generation-manifest.json](../artifacts/exps/deepseek-sft-counted-20261009/generation-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "created_at": 1791533967.5084424,
  "model": "deepseek-v4.1-flash",
  "serving_release": "1f8f58d9ed69ad45",
  "endpoint": "http://127.0.0.1:8005/v1",
  "gpus": 8,
  "reasoning_effort": 50,
  "concurrency": 64,
  "targets": {
    "MATH_train": 3500,
    "BigMath": 1000,
    "GSM_Infinite": 500
  },
  "train": 4500,
  "val": 500,
  "teacher": {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 32768
  },
  "judge": {
    "temperature": 0,
    "max_tokens": 16384
  },
  "student_context_limit": 16384,
  "files_sha256": {
    "produce.py": "cfc09c6d618745b9570386117507cadf55d3bb0d3fdc22b039554809bd5aa0c4",
    "validate.py": "68d24ca4a3b51f78ba6883f18d7a0603cfdfe1b7371d66fef8e960bf4676d35e",
    "teacher-prompt-v5.txt": "2c1393ca44d63efc3d23ac9d9465a4dc3d4530b66cebf3f438b3c43afb6f3bec",
    "student-system.txt": "ff9db43554f7b0ea0167443ab971f5b5702eebd336892c9d56ae7c564b72df08",
    "judge-prompt.txt": "2a8d9f8069ff308e089f021cb13db8fe78cc7091d4ba509e2dbb9cd3de301d45",
    "pilot-review.json": "47719f92c8c17d8d18b0d2ff4390672d6554f323fab273f80fc031bb5497d6da",
    "candidate-pool.jsonl": "b433f8662ca2ac1345f3e059320f330e1d35e110e15e494e561004cf0a8c387b",
    "pool-manifest.json": "6f2aec3ce769a88652e6db026653d6f164f0550f328153520c25b6ae025afa3c"
  }
}
```

</details>

- [exps/deepseek-sft-counted-20261009/judge-prompt.txt](../artifacts/exps/deepseek-sft-counted-20261009/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/pilot-manifest.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "pilot_requests": 10,
  "teacher_prompt_sha256": "859fe299f1d68281cd5e3acc4f2d3addd1c5ac408c73f3c28b1549de22bfacf7",
  "reference_not_sent_to_teacher": true
}
```

</details>

- [exps/deepseek-sft-counted-20261009/pool-manifest.json](../artifacts/exps/deepseek-sft-counted-20261009/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "seed": 20261009,
  "counts": {
    "MATH_train": 5945,
    "BigMath": 3000,
    "GSM_Infinite": 1500
  },
  "exclusions": {
    "diagram_or_url": 711,
    "eval_overlap/number_masked_trigram_jaccard>=0.65": 697,
    "eval_overlap/normalized_exact": 36,
    "missing_reference": 4,
    "question_length": 266,
    "duplicate": 6
  },
  "evaluation_exclusion_questions": 6552,
  "sources_sha256": {
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/algebra/test-00000-of-00001.parquet": "0e04a850dac9cfc758eac0c80afd2d0cc65e29ea72f916c8ac1045b12af937f5",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/counting_and_probability/test-00000-of-00001.parquet": "c324818949c75a6227c0328a8499d58023cbbf6757cfc1736f5ab24cc8d87966",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/geometry/test-00000-of-00001.parquet": "98720f3a8134ad9784fd8951195245264495df03ffc5c9485a9a54ff5ae2431a",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/intermediate_algebra/test-00000-of-00001.parquet": "e859f72486c951c2017da880541ca729940eaa986b0364eb23e238983df9bfeb",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/number_theory/test-00000-of-00001.parquet": "ba156c9c9fa2040836ba12135fd964e6e67d6bccd8c469ec4a3ad941f8f6fbe9",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/prealgebra/test-00000-of-00001.parquet": "301e5d8ade5c7b5038032532e498bdc9dca799e7f1061a63f2e7d980803240cc",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/precalculus/test-00000-of-00001.parquet": "da37474ba3761ae5727af3844a7ba963a735bd6a14c65e6137593669a4fe3b9c",
    "${PROJECT_ROOT}/exps/math500-new-sft-20261008/questions.jsonl": "a2645512280d4499c35e9c781f35e04c643b30ebc20b13d118878e4f2f9b3486",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/gsm_infinite.parquet": "ae164a57106664a8cb314d60225e5005aa9d9929a103a7b200392dcc0a7afbd6",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/dapo.parquet": "35f2733a92fd8a77cdf5c3408c21795343425c797e0279de7386da618d027b68",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_orca.parquet": "7df39f2e84380b25b9541a3bf1ccbe8f00c1c6f414976479bca8034be9d4521f",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_cn_k12.parquet": "2882edfb2ca9b9d117c563561aad4e2ccd0787b21fa69f330df4018d48910655",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/algebra/train-00000-of-00001.parquet": "73347f5b55869f21ff094361025dbd12d291e971aa4d72142eacee10438e449f",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/counting_and_probability/train-00000-of-00001.parquet": "d37ae017930df41678edee50dcde18c17fb06afaff9eb505c1b95f1002bfcb31",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/geometry/train-00000-of-00001.parquet": "9dbf5e5b55499e696e0ba72da9d85d4f0be3acbf7eaa6cb014b0fc78bb63784f",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/intermediate_algebra/train-00000-of-00001.parquet": "0c87f3798ebdfb915b1f9b6fc13c1a8d064c3cb91631ccbe85b83ed5d71150f6",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/number_theory/train-00000-of-00001.parquet": "81c08649149b39811f2d1d7ddf5dfccf6c4c8044a2e169cfb24db09160c941f4",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/prealgebra/train-00000-of-00001.parquet": "765b526fb5c0b8385cb7be2c16bf4f6f28cf71f2bc15c826abfbb5fa7f8616cc",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/precalculus/train-00000-of-00001.parquet": "28bb1ff95525c8d32521509bef91de76339659f5467a381e6e8deea204538f0e",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--open-r1--Big-Math-RL-Verified-Processed/snapshots/c79efbb6d3b75e3a2bcc27a5c569119918132345/all/train-00000-of-00001.parquet": "db6d8ea52ec4b9bd0bdfc1a2ce38874a95a193cd467e6858c4fecea3db08cbb0",
    "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/input/gsm_infinite_adaptive_parallel_5k.jsonl": "a63c0613526338246460b50824dc29f19aa6defcbbc66b73dc8f9a152df72799"
  },
  "decontamination": "All 5000 MATH test questions + pilot + previous RL screen. Normalized exact and number-masked word-trigram Jaccard >=0.65, top10 candidates. Does not guarantee removal of semantic paraphrases.",
  "targets": {
    "MATH_train": 3500,
    "BigMath": 1000,
    "GSM_Infinite": 500
  },
  "pilot_excluded": true
}
```

</details>

- [exps/deepseek-sft-counted-20261009/production/student-system.txt](../artifacts/exps/deepseek-sft-counted-20261009/production/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/student-system.txt](../artifacts/exps/deepseek-sft-counted-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/teacher-prompt-v1.txt](../artifacts/exps/deepseek-sft-counted-20261009/teacher-prompt-v1.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/teacher-prompt-v2.txt](../artifacts/exps/deepseek-sft-counted-20261009/teacher-prompt-v2.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/teacher-prompt-v3.txt](../artifacts/exps/deepseek-sft-counted-20261009/teacher-prompt-v3.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/teacher-prompt-v4.txt](../artifacts/exps/deepseek-sft-counted-20261009/teacher-prompt-v4.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-sft-counted-20261009/teacher-prompt-v5.txt](../artifacts/exps/deepseek-sft-counted-20261009/teacher-prompt-v5.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [exps/deepseek-sft-counted-20261009/pilot-v1/status.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-v1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791532145.6964376,
  "total": 10,
  "completed": 10,
  "failed": 0,
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "prompt_sha256": "859fe299f1d68281cd5e3acc4f2d3addd1c5ac408c73f3c28b1549de22bfacf7",
  "finished_at": 1791532499.0894916
}
```

</details>

- [exps/deepseek-sft-counted-20261009/pilot-v2/status.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-v2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791532445.2640538,
  "total": 10,
  "completed": 10,
  "failed": 0,
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "prompt_sha256": "7144c103d6671fbc2ae0a1cc157eeafbd44ebed22fd6dedd7c454a3d6cb371b8",
  "finished_at": 1791532729.1318724
}
```

</details>

- [exps/deepseek-sft-counted-20261009/pilot-v3/status.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-v3/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791532733.6483922,
  "total": 5,
  "completed": 5,
  "failed": 0,
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "prompt_sha256": "86e8259e6b385c093bbfbf62f27e9497a406b65c861bcfdb8cc03eb756730675",
  "finished_at": 1791533008.804096
}
```

</details>

- [exps/deepseek-sft-counted-20261009/pilot-v4/status.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-v4/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791533016.7587678,
  "total": 3,
  "completed": 3,
  "failed": 0,
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "prompt_sha256": "faf610211b22944a451943fba1dfeb47503ceb394e036b6691aec6ff6d92a9d1",
  "finished_at": 1791533247.1761546
}
```

</details>

- [exps/deepseek-sft-counted-20261009/pilot-v5/status.json](../artifacts/exps/deepseek-sft-counted-20261009/pilot-v5/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791533301.2403095,
  "total": 10,
  "completed": 10,
  "failed": 0,
  "model": "deepseek-v4.1-flash",
  "reasoning_effort": 50,
  "concurrency": 64,
  "prompt_sha256": "2c1393ca44d63efc3d23ac9d9465a4dc3d4530b66cebf3f438b3c43afb6f3bec",
  "finished_at": 1791533604.6516292
}
```

</details>

- [exps/deepseek-sft-counted-20261009/production-status-snapshot.json](../artifacts/exps/deepseek-sft-counted-20261009/production-status-snapshot.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "started_at": 1791533976.830515,
  "concurrency": 64,
  "reasoning_effort": 50,
  "targets": {
    "MATH_train": 3500,
    "BigMath": 1000,
    "GSM_Infinite": 500
  },
  "accepted": {
    "BigMath": 10,
    "MATH_train": 13
  },
  "processed": 24,
  "active_requests": 63,
  "max_active_requests": 64,
  "inflight": {
    "MATH_train": 47,
    "BigMath": 7,
    "GSM_Infinite": 9
  },
  "errors": {
    "structure": 1
  },
  "accepted_round_histogram": {
    "0": 5,
    "1": 17,
    "2": 1
  },
  "accepted_width_histogram": {
    "2": 16,
    "3": 3
  },
  "updated_at": 1791534121.2556083
}
```

</details>

- [exps/deepseek-sft-counted-20261009/production/status.json](../artifacts/exps/deepseek-sft-counted-20261009/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "stopped_user_scope_correction",
  "started_at": 1791533976.830515,
  "concurrency": 64,
  "reasoning_effort": 50,
  "targets": {
    "MATH_train": 3500,
    "BigMath": 1000,
    "GSM_Infinite": 500
  },
  "accepted": {
    "BigMath": 62,
    "MATH_train": 204,
    "GSM_Infinite": 26
  },
  "processed": 336,
  "active_requests": 20,
  "max_active_requests": 64,
  "inflight": {
    "MATH_train": 17,
    "BigMath": 0,
    "GSM_Infinite": 3
  },
  "errors": {
    "structure": 26,
    "answer_verification": 12,
    "semantic_judge_reject": 4,
    "judge_not_finished": 2
  },
  "accepted_round_histogram": {
    "0": 13,
    "1": 213,
    "2": 53,
    "3": 8,
    "4": 5
  },
  "accepted_width_histogram": {
    "2": 269,
    "3": 61,
    "4": 21,
    "5": 7,
    "7": 1,
    "6": 4
  },
  "updated_at": 1791535463.3919694,
  "stopped_at": 1791535480.972152,
  "stop_reason": "Only GSM-Infinite authorized; mixed-source assumption corrected."
}
```

</details>
