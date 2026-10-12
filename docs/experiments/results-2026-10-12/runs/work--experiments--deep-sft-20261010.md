# work/experiments/deep-sft-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/judge-prompt.txt](../artifacts/work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/pool-manifest.json](../artifacts/work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "candidates": 7259,
  "pilot": 50,
  "source": "GSM-Infinite ONLY, prior pinned source revisions retained",
  "op_histogram": {
    "27": 927,
    "29": 466,
    "25": 363,
    "28": 669,
    "30": 254,
    "26": 233,
    "22": 1296,
    "21": 1355,
    "24": 700,
    "23": 996
  },
  "pilot_op_histogram": {
    "27": 15,
    "29": 11,
    "25": 7,
    "28": 8,
    "30": 4,
    "26": 5
  },
  "excluded_eval_ids": 128,
  "excluded_eval_questions": 6152,
  "old_train_ids": 5145,
  "disjoint_ids": true,
  "disjoint_normalized_problems": true,
  "exclusions": {
    "prior_id": 2637,
    "ops_below_21": 691
  },
  "source_hashes": {
    "${PROJECT_ROOT}/work/experiments/base-format-20261010/evaluations/questions-128.jsonl": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "${PROJECT_ROOT}/work/experiments/format-diagnosis-20261010/evaluations/questions-128.jsonl": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/questions-128.jsonl": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-24.jsonl": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_cn_k12.parquet": "2882edfb2ca9b9d117c563561aad4e2ccd0787b21fa69f330df4018d48910655",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_orca.parquet": "7df39f2e84380b25b9541a3bf1ccbe8f00c1c6f414976479bca8034be9d4521f",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/dapo.parquet": "35f2733a92fd8a77cdf5c3408c21795343425c797e0279de7386da618d027b68",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/gsm_infinite.parquet": "ae164a57106664a8cb314d60225e5005aa9d9929a103a7b200392dcc0a7afbd6",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/algebra/test-00000-of-00001.parquet": "0e04a850dac9cfc758eac0c80afd2d0cc65e29ea72f916c8ac1045b12af937f5",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/counting_and_probability/test-00000-of-00001.parquet": "c324818949c75a6227c0328a8499d58023cbbf6757cfc1736f5ab24cc8d87966",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/geometry/test-00000-of-00001.parquet": "98720f3a8134ad9784fd8951195245264495df03ffc5c9485a9a54ff5ae2431a",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/intermediate_algebra/test-00000-of-00001.parquet": "e859f72486c951c2017da880541ca729940eaa986b0364eb23e238983df9bfeb",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/number_theory/test-00000-of-00001.parquet": "ba156c9c9fa2040836ba12135fd964e6e67d6bccd8c469ec4a3ad941f8f6fbe9",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/prealgebra/test-00000-of-00001.parquet": "301e5d8ade5c7b5038032532e498bdc9dca799e7f1061a63f2e7d980803240cc",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/precalculus/test-00000-of-00001.parquet": "da37474ba3761ae5727af3844a7ba963a735bd6a14c65e6137593669a4fe3b9c",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/accepted.jsonl": "ec98108b5ead4f1bb35554e69e5017c3edeb621d3a95b8f1069f954489f9369d",
    "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl": "c13c51a87d7189b659795d21a98ada9db5063c44a2135434aa454b3428b28612",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/candidate-pool.jsonl": "b5203a8608dbaa2b549f38e3d4096c5cf59762c820e55da09fb83fa520484c1a"
  },
  "pool_sha256": "f11948e993916650c0a590861c4cfe2a1e72b36de83f1d65910460c55c3e1d76",
  "pilot_sha256": "be6ad2ca3b667e4a71e5fa58bfb0737d521b17ce3baba5510c131e221c3a6b67",
  "limitation": "Text and number-masked trigram screening is not proof against semantic paraphrases."
}
```

</details>

- [work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/teacher-prompt.txt](../artifacts/work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/teacher-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261010/judge-prompt.txt](../artifacts/work/experiments/deep-sft-20261010/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261010/pool-manifest.json](../artifacts/work/experiments/deep-sft-20261010/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "candidates": 7500,
  "pilot": 50,
  "source": "NEW independently generated GSM-style layered arithmetic, not GSM-Infinite or MATH-derived",
  "oracle": "Exact integer Python evaluation of every node and final weighted sum",
  "width_histogram": {
    "4": 3727,
    "3": 1886,
    "5": 1887
  },
  "stages_histogram": {
    "4": 4496,
    "3": 1498,
    "5": 1506
  },
  "pilot_width_histogram": {
    "5": 10,
    "4": 30,
    "3": 10
  },
  "pilot_stages_histogram": {
    "4": 30,
    "3": 10,
    "5": 10
  },
  "pilot_true_width_mean": 4.0,
  "pilot_true_stages_mean": 4.0,
  "all_nodes_reachable": true,
  "all_stage_amounts_updated_simultaneously": true,
  "all_nodes_computational": true,
  "known_eval_or_old_train_normalized_questions": 5273,
  "exact_normalized_question_overlap": 0,
  "generator_sha256": "070cd3a19fa762b870d631c28f2a4600631c6cf2402d7a80af287b36c541431f",
  "seed": 2026101001,
  "pool_sha256": "77ec35ae191165e6d1686a9ba956726e614faf82a6326ee033584ee078ae4945",
  "pilot_sha256": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
  "oracle_sha256": "be5ec8514b49994786077b32af913bdf6fa59418c0c7ed9b8f9bdf007093c7d7",
  "limitations": [
    "New synthetic distribution; it is not evidence of broader mathematical generalization.",
    "Exact normalized contamination screening does not prove absence of semantic resemblance.",
    "Teacher may choose fewer/more rounds; measure actual traces, do not substitute oracle stages for executed trace rounds."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261010/teacher-prompt.txt](../artifacts/work/experiments/deep-sft-20261010/teacher-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/pilot/status.json](../artifacts/work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/pilot/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "waiting_for_teacher",
  "phase": "pilot",
  "started_at": 1791665170.7820535,
  "completed": 0,
  "accepted": 0,
  "target": 50,
  "concurrency": 50,
  "decisions": {},
  "errors": {},
  "inflight": 0,
  "updated_at": 1791665170.7820816
}
```

</details>

- [work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/prescreen-result.json](../artifacts/work/experiments/deep-sft-20261010/attempts/01-opcount-only-prescreen/prescreen-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 50,
  "generated": 0,
  "accepted": 0,
  "aborted_waiting_runner_pid": 1297876,
  "time": 1791665532.792273,
  "reason": "source fit failed before teacher requests; preserve all 50 planned outcomes",
  "sha256": {
    "candidate-pool.jsonl": "f11948e993916650c0a590861c4cfe2a1e72b36de83f1d65910460c55c3e1d76",
    "pilot-tasks.jsonl": "be6ad2ca3b667e4a71e5fa58bfb0737d521b17ce3baba5510c131e221c3a6b67",
    "planned50-outcomes.jsonl": "50ba27559e0b26d8627a37befbddacf80c575d031592a709b561ad12a0b46b35"
  }
}
```

</details>

- [work/experiments/deep-sft-20261010/pilot-rechecked/report.json](../artifacts/work/experiments/deep-sft-20261010/pilot-rechecked/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 50,
  "completed": 50,
  "first_attempt_only": true,
  "first_math_correct": 50,
  "canonical": 49,
  "accepted_math_canonical": 49,
  "rejected": [
    "synthetic-layered-dag-v1/2026101022"
  ],
  "semantic_judge_missing": [
    "synthetic-layered-dag-v1/2026101003",
    "synthetic-layered-dag-v1/2026101009",
    "synthetic-layered-dag-v1/2026101017",
    "synthetic-layered-dag-v1/2026101022",
    "synthetic-layered-dag-v1/2026101023",
    "synthetic-layered-dag-v1/2026101029",
    "synthetic-layered-dag-v1/2026101036",
    "synthetic-layered-dag-v1/2026101039",
    "synthetic-layered-dag-v1/2026101040",
    "synthetic-layered-dag-v1/2026101051",
    "synthetic-layered-dag-v1/2026101059",
    "synthetic-layered-dag-v1/2026101061"
  ],
  "original_outcomes_preserved": true,
  "new_teacher_calls": 0,
  "production_released": false,
  "status": "HOLD: math/canonical snapshot complete; semantic review and Instruct template pending",
  "independent_report_sha256": "13c9b7ee36dd57441755ab24a77e72170b66c385d9c294ca2ae98f5ae0255279",
  "checker_sha256": {
    "arithmetic_check.py": "059680f92066905230a03666089f6e096aa1a33b9fd96e3d7ed6e999b0acdf61",
    "oracle_check.py": "4d67be269f5764b1ba2171ab78aff0b99e168f3d2632f42c6d23905d6887c111",
    "arithmetic_check_v2.py": "5476def2ad35d15e9840da6c6d9f791ee333efa01962f91caf5803abce46854e",
    "oracle_check_v2.py": "c0b4ae8a43cfc977206b8bc04a51b0bcb001ea8f8db54f14bb46a156dbb017f6",
    "test_checker_repair.py": "fb7b7ccca1a98a716a0296f2b320e17140f0df2db248f1812fde58a29f2c21c6"
  },
  "artifact_sha256": {
    "journal.jsonl": "345fc0228046b8e888016a20b06bd3ef81833164b7e069eeb744b7967f05eb23",
    "accepted.jsonl": "7aaaea92f4f5cca6829077e016ea6404b7e4a685689fc6e602f352aa409af265",
    "first-attempt-raw-responses.jsonl": "473269e163740e13debc1d8621b8549c18e05971adcc6e7ae5f8df187e12a36d"
  },
  "provenance_sha256": {
    "teacher-prompt.txt": "c8963dea43780c26bac19c6a0e7db32bdaaa3e0626747096903e4287e2c36827",
    "judge-prompt.txt": "602c5e12e4fd6b24c005ee9ea18389b87c83556d3406437c515734768587682a",
    "pilot-tasks.jsonl": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
    "oracle-source.jsonl": "be5ec8514b49994786077b32af913bdf6fa59418c0c7ed9b8f9bdf007093c7d7",
    "candidate-pool.jsonl": "77ec35ae191165e6d1686a9ba956726e614faf82a6326ee033584ee078ae4945"
  },
  "limitations": [
    "Failed internal HTTP transport retries were not individually journaled by original generation.",
    "Independent reviewer proves source relations; numeric checker does not prove prose meanings.",
    "Raw 1022 drafting preamble is rejected, not sanitized or replaced with a retry."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261010/pilot-rechecked/trace-statistics-per-task.jsonl](../artifacts/work/experiments/deep-sft-20261010/pilot-rechecked/trace-statistics-per-task.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261010/pilot-rechecked/trace-statistics.json](../artifacts/work/experiments/deep-sft-20261010/pilot-rechecked/trace-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "pilot-rechecked",
  "accepted": 49,
  "width": {
    "count": 207,
    "mean": 3.975845410628019,
    "median": 4.0,
    "p5": 3.0,
    "p95": 5.0,
    "minimum": 2,
    "maximum": 5
  },
  "rounds": {
    "count": 49,
    "mean": 4.224489795918367,
    "median": 4.0,
    "p5": 4.0,
    "p95": 5.0,
    "minimum": 4,
    "maximum": 5
  },
  "path_body_tokens": {
    "count": 823,
    "mean": 33.650060753341435,
    "median": 36.0,
    "p5": 20.0,
    "p95": 41.89999999999998,
    "minimum": 18,
    "maximum": 55
  },
  "whole_path_tokens": {
    "count": 823,
    "mean": 37.650060753341435,
    "median": 40.0,
    "p5": 24.0,
    "p95": 45.89999999999998,
    "minimum": 22,
    "maximum": 59
  },
  "response_tokens": {
    "count": 49,
    "mean": 1281.0816326530612,
    "median": 1244.0,
    "p5": 883.4,
    "p95": 1730.1999999999998,
    "minimum": 835,
    "maximum": 1966
  },
  "student_context_tokens": {
    "count": 49,
    "mean": 2040.8367346938776,
    "median": 1979.0,
    "p5": 1413.0,
    "p95": 2709.9999999999995,
    "minimum": 1369,
    "maximum": 3031
  },
  "critical_path_tokens_split_proxy": {
    "count": 49,
    "mean": 816.2244897959183,
    "median": 776.0,
    "p5": 647.4,
    "p95": 1082.9999999999998,
    "minimum": 623,
    "maximum": 1193
  },
  "serial_tokens_split_proxy": {
    "count": 49,
    "mean": 648.7142857142857,
    "median": 628.0,
    "p5": 481.6,
    "p95": 887.3999999999999,
    "minimum": 468,
    "maximum": 1053
  },
  "width_histogram": {
    "4": 120,
    "5": 45,
    "3": 34,
    "2": 8
  },
  "round_histogram": {
    "4": 38,
    "5": 11
  },
  "accepted_sha256": "7aaaea92f4f5cca6829077e016ea6404b7e4a685689fc6e602f352aa409af265",
  "limitations": [
    "Student tokenizer and compacted training response; teacher hidden reasoning excluded.",
    "Critical path includes entire Path opener/body/closer and all serial text.",
    "Independent segment tokenization can differ at boundaries; split proxy is not runtime forwards or latency.",
    "Prompt/context tokens count once; prompt is excluded from response critical path."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261010/pilot/report.json](../artifacts/work/experiments/deep-sft-20261010/pilot/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "pilot",
  "completed": 50,
  "accepted": 43,
  "rejected": 7,
  "errors": {
    "explicit_arithmetic_mismatch": 6,
    "independent_oracle_replay": 1
  },
  "selected_deep": 41,
  "width": {
    "mean": 4.043715846994536,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "rounds": {
    "mean": 4.255813953488372,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "width_histogram": {
    "3": 25,
    "4": 113,
    "5": 41,
    "2": 4
  },
  "round_histogram": {
    "4": 32,
    "5": 11
  },
  "path_tokens": {
    "mean": 32.6554054054054,
    "median": 35.0,
    "p95": 41.0,
    "max": 43
  },
  "output_tokens": {
    "mean": 1292.1860465116279,
    "median": 1250.0,
    "p95": 1739.8,
    "max": 1966
  },
  "critical_path_tokens_proxy": {
    "mean": 807.3488372093024,
    "median": 764.0,
    "p95": 1073.5,
    "max": 1173
  },
  "explicit_scalar_equalities_checked": 98,
  "mathematically_reference_verified": 43,
  "no_think": true,
  "all_sibling_ids_structurally_consistent": true,
  "hashes": {
    "teacher-prompt.txt": "c8963dea43780c26bac19c6a0e7db32bdaaa3e0626747096903e4287e2c36827",
    "judge-prompt.txt": "602c5e12e4fd6b24c005ee9ea18389b87c83556d3406437c515734768587682a",
    "pool-manifest.json": "482b5f172f52a6c4ee74b871e941cd8e449a52ad2212b64fbbbedebdb3c7d7bd",
    "pilot-tasks.jsonl": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
    "journal.jsonl": "563da649c17e01bc5a48fba71938599e2d6bf661121caba8ebf2468d47c3ded9",
    "accepted.jsonl": "55745652ce53b9223baea62f60757e4d61642e996931b57fb1983a22ef05012f"
  },
  "limitations": [
    "The teacher also acts as semantic judge; not independent proof of every governing relation.",
    "Explicit arithmetic checker covers flat scalar equalities only.",
    "Manual actual-trace review is mandatory before releasing production generation.",
    "F is token critical-path proxy, not measured GPU latency."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261010/pilot/status.json](../artifacts/work/experiments/deep-sft-20261010/pilot/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "phase": "pilot",
  "started_at": 1791676909.9742413,
  "completed": 50,
  "accepted": 43,
  "target": 50,
  "concurrency": 50,
  "decisions": {
    "rejected": 7,
    "accepted": 43
  },
  "errors": {
    "explicit_arithmetic_mismatch": 6,
    "independent_oracle_replay": 1
  },
  "inflight": 0,
  "updated_at": 1791677812.4077804,
  "finished_at": 1791677812.4077778
}
```

</details>

- [work/experiments/deep-sft-20261010/pilot/trace-statistics-per-task.jsonl](../artifacts/work/experiments/deep-sft-20261010/pilot/trace-statistics-per-task.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261010/pilot/trace-statistics.json](../artifacts/work/experiments/deep-sft-20261010/pilot/trace-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "pilot",
  "accepted": 43,
  "width": {
    "count": 183,
    "mean": 4.043715846994536,
    "median": 4.0,
    "p5": 3.0,
    "p95": 5.0,
    "minimum": 2,
    "maximum": 5
  },
  "rounds": {
    "count": 43,
    "mean": 4.255813953488372,
    "median": 4.0,
    "p5": 4.0,
    "p95": 5.0,
    "minimum": 4,
    "maximum": 5
  },
  "path_body_tokens": {
    "count": 740,
    "mean": 32.6554054054054,
    "median": 35.0,
    "p5": 20.0,
    "p95": 41.0,
    "minimum": 18,
    "maximum": 43
  },
  "whole_path_tokens": {
    "count": 740,
    "mean": 36.6554054054054,
    "median": 39.0,
    "p5": 24.0,
    "p95": 45.0,
    "minimum": 22,
    "maximum": 47
  },
  "response_tokens": {
    "count": 43,
    "mean": 1292.0697674418604,
    "median": 1250.0,
    "p5": 915.4,
    "p95": 1739.8,
    "minimum": 865,
    "maximum": 1966
  },
  "student_context_tokens": {
    "count": 43,
    "mean": 2074.3953488372094,
    "median": 1982.0,
    "p5": 1551.8,
    "p95": 2728.0,
    "minimum": 1378,
    "maximum": 3031
  },
  "critical_path_tokens_split_proxy": {
    "count": 43,
    "mean": 824.3720930232558,
    "median": 780.0,
    "p5": 644.0,
    "p95": 1093.5,
    "minimum": 609,
    "maximum": 1193
  },
  "serial_tokens_split_proxy": {
    "count": 43,
    "mean": 661.2558139534884,
    "median": 638.0,
    "p5": 477.0,
    "p95": 901.3,
    "minimum": 456,
    "maximum": 1053
  },
  "width_histogram": {
    "3": 25,
    "4": 113,
    "5": 41,
    "2": 4
  },
  "round_histogram": {
    "4": 32,
    "5": 11
  },
  "accepted_sha256": "55745652ce53b9223baea62f60757e4d61642e996931b57fb1983a22ef05012f",
  "limitations": [
    "Student tokenizer and compacted training response; teacher hidden reasoning excluded.",
    "Critical path includes entire Path opener/body/closer and all serial text.",
    "Independent segment tokenization can differ at boundaries; split proxy is not runtime forwards or latency.",
    "Prompt/context tokens count once; prompt is excluded from response critical path."
  ]
}
```

</details>
