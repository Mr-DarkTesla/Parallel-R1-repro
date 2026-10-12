# exps/deepseek-gsm-only-20261009

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/deepseek-gsm-only-20261009/generation-manifest.json](../artifacts/exps/deepseek-gsm-only-20261009/generation-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "created_at": 1791536160.9024532,
  "source_scope": "GSM_Infinite ONLY",
  "model": "deepseek-v4.1-flash",
  "serving_release": "1f8f58d9ed69ad45",
  "endpoint": "http://127.0.0.1:8005/v1",
  "reasoning_effort": 50,
  "concurrency": 128,
  "target": 5000,
  "train": 4500,
  "val": 500,
  "reused_gsm": 26,
  "pool_summary": {
    "original_eligible": 4660,
    "reserve": 3840,
    "candidates": 8500
  },
  "files_sha256": {
    "produce.py": "b48e3891bf0ed135b68cfb1b5c873670e0515bd99c60ef0fac26f52bc928c907",
    "prepare_pool.py": "2c86237a20dddb81c34d4589f557c4dab10132a1d43e42cda049e48cb2e1363b",
    "validate.py": "68d24ca4a3b51f78ba6883f18d7a0603cfdfe1b7371d66fef8e960bf4676d35e",
    "teacher-prompt-v5.txt": "2c1393ca44d63efc3d23ac9d9465a4dc3d4530b66cebf3f438b3c43afb6f3bec",
    "student-system.txt": "ff9db43554f7b0ea0167443ab971f5b5702eebd336892c9d56ae7c564b72df08",
    "judge-prompt.txt": "2a8d9f8069ff308e089f021cb13db8fe78cc7091d4ba509e2dbb9cd3de301d45",
    "pilot-review.json": "0d713a69cd85a418ba160d8bef4b63222b12737fd4c7cf81be3b70b99c98ca9a",
    "candidate-pool.jsonl": "35a0a345e8e94d66a953d2ee9cdc43eee2b00c6421a472037ea720a152ca07d3",
    "pool-manifest.json": "d8375a657691d0780c4f4289da968f0c08cd867581f2df6e32ed6ffe51c3da31",
    "reused-gsm.json": "b14fbb590928c2334a3b24957001a01de9555b03ae1e7aaf48a90974fcb14fb3"
  }
}
```

</details>

- [exps/deepseek-gsm-only-20261009/judge-prompt.txt](../artifacts/exps/deepseek-gsm-only-20261009/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/pool-manifest.json](../artifacts/exps/deepseek-gsm-only-20261009/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "source": "GSM_Infinite ONLY",
  "target": 5000,
  "original_eligible": 4660,
  "reserve": 3840,
  "candidates": 8500,
  "official_reserve_revision": "49b0c72bca4c257a378d07da41561fe081ec5ad5",
  "exclusions": {
    "question_length": 318,
    "eval_or_pilot_overlap": 2399,
    "duplicate": 962
  },
  "sources_sha256": {
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/algebra/test-00000-of-00001.parquet": "0e04a850dac9cfc758eac0c80afd2d0cc65e29ea72f916c8ac1045b12af937f5",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/counting_and_probability/test-00000-of-00001.parquet": "c324818949c75a6227c0328a8499d58023cbbf6757cfc1736f5ab24cc8d87966",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/geometry/test-00000-of-00001.parquet": "98720f3a8134ad9784fd8951195245264495df03ffc5c9485a9a54ff5ae2431a",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/intermediate_algebra/test-00000-of-00001.parquet": "e859f72486c951c2017da880541ca729940eaa986b0364eb23e238983df9bfeb",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/number_theory/test-00000-of-00001.parquet": "ba156c9c9fa2040836ba12135fd964e6e67d6bccd8c469ec4a3ad941f8f6fbe9",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/prealgebra/test-00000-of-00001.parquet": "301e5d8ade5c7b5038032532e498bdc9dca799e7f1061a63f2e7d980803240cc",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/21a5633873b6a120296cce3e2df9d5550074f4a3/precalculus/test-00000-of-00001.parquet": "da37474ba3761ae5727af3844a7ba963a735bd6a14c65e6137593669a4fe3b9c",
    "${PROJECT_ROOT}/exps/deepseek-sft-counted-20261009/pilot-tasks.jsonl": "ec2585aa3e79226a0fda5c5a3167fb05ab4d59f61afe93c3e4895986257d6f75",
    "${PROJECT_ROOT}/exps/deepseek-sft-counted-20261009/pilot-v3-tasks.jsonl": "188e05a6f6791450b2b08f00fb78f439bc9268c47c6410a78f624b2e190b29ac",
    "${PROJECT_ROOT}/exps/deepseek-sft-counted-20261009/pilot-v4-tasks.jsonl": "45109327c19071614df94d3909f4067a93c47d0a5a21885dca7c6a39e267fd27",
    "${PROJECT_ROOT}/exps/deepseek-sft-counted-20261009/pilot-v5-tasks.jsonl": "963a2a10ff5488342f98aab9eb4373d02be7511cfbc8e2555d23fea1e81620ac",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/gsm_infinite.parquet": "ae164a57106664a8cb314d60225e5005aa9d9929a103a7b200392dcc0a7afbd6",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/dapo.parquet": "35f2733a92fd8a77cdf5c3408c21795343425c797e0279de7386da618d027b68",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_orca.parquet": "7df39f2e84380b25b9541a3bf1ccbe8f00c1c6f414976479bca8034be9d4521f",
    "${PROJECT_ROOT}/exps/rl-dataset-screen-20261007/bigmath_cn_k12.parquet": "2882edfb2ca9b9d117c563561aad4e2ccd0787b21fa69f330df4018d48910655",
    "${PROJECT_ROOT}/exps/sft-unseen-three-datasets-20261008/input/gsm_infinite_adaptive_parallel_5k.jsonl": "a63c0613526338246460b50824dc29f19aa6defcbbc66b73dc8f9a152df72799",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_15-00000-of-00001.parquet": "0d7be1453ac82ce4608d5c1fe2aa57958bf61bc260d2b359b865d47f76dec80f",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_16-00000-of-00001.parquet": "f88e60109b09eb1524ede78e033865203e6646d1a47de836249861ffad7c28f6",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_17-00000-of-00001.parquet": "8cb5d6a840b80402c080c4bde6cac0431b448bcdfa50fce9313579bf2227aa96",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_18-00000-of-00001.parquet": "dd32aed02a7f03703cbfb70eed66f5ecaf5e0c0a9407d4acbf3a0cb091ac1e11",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_19-00000-of-00001.parquet": "7193f9e0070adc544b48d03de1f16beb937947d56baa03bcada6aeb27a4dee33",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_20-00000-of-00001.parquet": "08e14d4fcc4468634420d16ec65179082ef950a41011ee2e412341cc3ad2f425",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_21-00000-of-00001.parquet": "557a95f89a0bd47f2ad730c20287e47f072402b9813f0b93b05e1c5cff00634e",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_22-00000-of-00001.parquet": "98cbc5aa6f4e7c71b516574d121625a3d93a90350cb88cb968142fcac3599f46",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_23-00000-of-00001.parquet": "52eb14a29a66fe13a37692c0e62c6765f6e1409e0430329e366df46197352ff2",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_24-00000-of-00001.parquet": "b3df49caebd6531a799ae3db1c5b968ddba2ac2f460261032ab962b921998c0c",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_25-00000-of-00001.parquet": "93f5bad3b348b89ae52c33a2bf74981f0e8288c11fabbccaf6c0c853107d0ec8",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_26-00000-of-00001.parquet": "d63b80b161e8629068dc0e8b5d0370e5829ef7964d19c914c5c8d86132bf07ef",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_27-00000-of-00001.parquet": "5f14e089743ce2bd469e7bbb96c6a8579ecd0a3fdfcb3d3ff4e1a22f1ebf80b5",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_28-00000-of-00001.parquet": "c2b0df7e68048c5611043adde53460e80171c040ac8ee45a1af9a1ec9530787b",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_29-00000-of-00001.parquet": "ae71c447c6df3f4ff96913f9b1b1bab077eccffa5856095bfc7e159ab8973ab7",
    "${PROJECT_ROOT}/cache/screen-hf/datasets--InfiniAILab--gsm_infinite_hard_0/snapshots/49b0c72bca4c257a378d07da41561fe081ec5ad5/data/ops_30-00000-of-00001.parquet": "acfb39d5ef3bf6af2d57580869b13abd762dfb5dc2e9040338021d7b6e8856a0"
  },
  "seed": 20261009,
  "decontamination": "Normalized exact and number-masked trigram Jaccard >=0.65 against MATH test, previous RL evaluation and pilot tasks. Not semantic proof of decontamination.",
  "max_question_characters": 14000
}
```

</details>

- [exps/deepseek-gsm-only-20261009/production/sft-think/student-system.txt](../artifacts/exps/deepseek-gsm-only-20261009/production/sft-think/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/production/student-system.txt](../artifacts/exps/deepseek-gsm-only-20261009/production/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/student-system.txt](../artifacts/exps/deepseek-gsm-only-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/teacher-prompt-v5.txt](../artifacts/exps/deepseek-gsm-only-20261009/teacher-prompt-v5.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/think-export-manifest.json](../artifacts/exps/deepseek-gsm-only-20261009/think-export-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "started_at": 1791545874.6539984,
  "canonical_sft_directory": "${PROJECT_ROOT}/exps/deepseek-gsm-only-20261009/production/sft-think",
  "preview_validation": {
    "at": 1791545842.8047307,
    "rows": 1820,
    "all_rendered_single_think": true,
    "all_parallel_blocks_inside_think": true,
    "final_answers_outside_think": true,
    "max_student_tokens": 4160
  }
}
```

</details>

## Метрики и полнота результатов

- [exps/deepseek-gsm-only-20261009/current-statistics.json](../artifacts/exps/deepseek-gsm-only-20261009/current-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791545950.181566,
  "accepted": 1845,
  "completed_decisions": 2081,
  "fresh_decisions": 2055,
  "fresh_accepted": 1819,
  "reused": 26,
  "acceptance_rate": 0.8851581508515816,
  "final_answer_checks": 1883,
  "final_answer_correct": 1878,
  "final_answer_accuracy": 0.997344662772172,
  "judges_returned": 1862,
  "judges_accept": 1819,
  "judge_accept_rate": 0.976906552094522,
  "judges_math_correct": 1849,
  "errors": {
    "structure": 172,
    "answer_verification": 5,
    "semantic_judge_reject": 43,
    "judge_not_finished": 16
  },
  "structure_errors": {
    "structure/missing_prefork_explanation": 129,
    "structure/unresolved": 14,
    "structure/missing_prefork_explanation,unresolved": 2,
    "structure/unparsed_structural_tags": 13,
    "structure/final_answer_not_last": 4,
    "structure/tags_inside_summary": 3,
    "structure/missing_prefork_explanation,unparsed_structural_tags": 3,
    "structure/exact_duplicate_paths,missing_prefork_explanation": 1,
    "structure/final_answer_not_last,missing_prefork_explanation": 1,
    "structure/final_answer_not_last,tags_inside_summary": 1,
    "structure/exact_duplicate_paths": 1
  },
  "rounds": {
    "2": 662,
    "1": 529,
    "4": 168,
    "3": 378,
    "0": 67,
    "5": 33,
    "6": 7,
    "7": 1
  },
  "widths": {
    "2": 2300,
    "3": 924,
    "5": 141,
    "4": 426,
    "6": 46,
    "7": 23,
    "8": 13
  },
  "total_forks": 3873,
  "zero_fork": 67,
  "multi_round": 1249,
  "has_width_gt2": 1107,
  "has_width8": 13,
  "round_stats": {
    "n": 1845,
    "mean": 2.1,
    "percentiles": {
      "0": 0,
      "25": 1,
      "50": 2,
      "75": 3,
      "90": 4,
      "95": 4,
      "99": 5,
      "100": 7
    }
  },
  "width_stats": {
    "n": 3873,
    "mean": 2.7,
    "percentiles": {
      "0": 2,
      "25": 2,
      "50": 2,
      "75": 3,
      "90": 4,
      "95": 5,
      "99": 6,
      "100": 8
    }
  },
  "assistant_tokens": {
    "n": 1845,
    "mean": 932.9,
    "percentiles": {
      "0": 142,
      "25": 706,
      "50": 898,
      "75": 1128,
      "90": 1366,
      "95": 1517,
      "99": 1936,
      "100": 2363
    }
  },
  "assistant_length_bins": {
    "0-511": 164,
    "512-1023": 1042,
    "1024-2047": 625,
    "2048-4095": 14,
    "4096-8191": 0,
    "8192-16384": 0
  },
  "student_tokens": {
    "n": 1845,
    "mean": 1986.1,
    "percentiles": {
      "0": 624,
      "25": 1494,
      "50": 1869,
      "75": 2355,
      "90": 2896,
      "95": 3322,
      "99": 3905,
      "100": 4126
    }
  },
  "op_distribution": {
    "5": 8,
    "6": 10,
    "7": 15,
    "8": 27,
    "9": 26,
    "10": 26,
    "11": 25,
    "12": 29,
    "13": 38,
    "14": 34,
    "15": 49,
    "16": 42,
    "17": 53,
    "18": 68,
    "19": 63,
    "20": 83,
    "21": 107,
    "22": 102,
    "23": 145,
    "24": 125,
    "25": 107,
    "26": 104,
    "27": 136,
    "28": 147,
    "29": 145,
    "30": 131
  },
  "status": {
    "state": "running",
    "started_at": 1791536170.3193612,
    "resumed_at": 1791538335.0529926,
    "concurrency": 256,
    "reasoning_effort": 50,
    "targets": {
      "GSM_Infinite": 5000
    },
    "accepted": {
      "GSM_Infinite": 1845
    },
    "processed": 2081,
    "active_requests": 255,
    "max_active_requests": 256,
    "inflight": {
      "GSM_Infinite": 255
    },
    "errors": {
      "structure": 172,
      "answer_verification": 5,
      "semantic_judge_reject": 43,
      "judge_not_finished": 16
    },
    "accepted_round_histogram": {
      "2": 662,
      "1": 529,
      "4": 168,
      "3": 378,
      "0": 67,
      "5": 33,
      "6": 7,
      "7": 1
    },
    "accepted_width_histogram": {
      "2": 2300,
      "3": 924,
      "5": 141,
      "4": 426,
      "6": 46,
      "7": 23,
      "8": 13
    },
    "updated_at": 1791545948.8374343
  }
}
```

</details>

- [exps/deepseek-gsm-only-20261009/production/status.json](../artifacts/exps/deepseek-gsm-only-20261009/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "started_at": 1791536170.3193612,
  "resumed_at": 1791538335.0529926,
  "concurrency": 256,
  "reasoning_effort": 50,
  "targets": {
    "GSM_Infinite": 5000
  },
  "accepted": {
    "GSM_Infinite": 2145
  },
  "processed": 2418,
  "active_requests": 70,
  "max_active_requests": 256,
  "inflight": {
    "GSM_Infinite": 70
  },
  "errors": {
    "structure": 200,
    "answer_verification": 6,
    "semantic_judge_reject": 46,
    "judge_not_finished": 21
  },
  "accepted_round_histogram": {
    "2": 758,
    "1": 626,
    "4": 191,
    "3": 450,
    "0": 76,
    "5": 35,
    "6": 8,
    "7": 1
  },
  "accepted_width_histogram": {
    "2": 2647,
    "3": 1087,
    "5": 164,
    "4": 494,
    "6": 54,
    "7": 25,
    "8": 15
  },
  "updated_at": 1791547211.6520224
}
```

</details>

- [exps/deepseek-gsm-only-20261009/think-export-status.json](../artifacts/exps/deepseek-gsm-only-20261009/think-export-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "waiting_for_raw_completion",
  "at": 1791547202.862014,
  "accepted": {
    "GSM_Infinite": 2142
  }
}
```

</details>

- [exps/deepseek-gsm-only-20261009/user-stop-summary.json](../artifacts/exps/deepseek-gsm-only-20261009/user-stop-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791547213.0129266,
  "state": "terminated_by_user",
  "accepted": 2145,
  "processed": 2418,
  "new_target": 3000,
  "new_pilot": 60,
  "pending_requests": "cancelled; not accepted without completed checks"
}
```

</details>

## Графики

- [exps/deepseek-gsm-only-20261009/current-statistics.png](../artifacts/exps/deepseek-gsm-only-20261009/current-statistics.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-only-20261009/current-statistics.svg](../artifacts/exps/deepseek-gsm-only-20261009/current-statistics.svg) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
