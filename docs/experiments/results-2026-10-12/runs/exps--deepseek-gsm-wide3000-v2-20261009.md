# exps/deepseek-gsm-wide3000-v2-20261009

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/deepseek-gsm-wide3000-v2-20261009/expanded-source-manifest.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/expanded-source-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "source": "GSM_Infinite ONLY",
  "target": 3000,
  "original_eligible": 4660,
  "reserve": 8345,
  "candidates": 13005,
  "official_reserve_revision": "49b0c72bca4c257a378d07da41561fe081ec5ad5",
  "exclusions": {
    "question_length": 318,
    "eval_or_pilot_overlap": 5154,
    "duplicate": 2054
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

- [exps/deepseek-gsm-wide3000-v2-20261009/judge-prompt.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/pilot-correction-manifest.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/pilot-correction-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791552705.3912373,
  "unique_questions": 60,
  "verification_cases_regenerated": 8,
  "original_responses_preserved": true,
  "production_prompt_sha256": "e9455d5993162286be9ee24db5070268abd0b73c8e88da5fe37e1d13c7ac1ba5",
  "note": "Verification wording was aligned with student and judge; non-verification cases retain the initial wide-cut pilot outputs."
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/pool-manifest.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791553149.5232365,
  "old_accepted_preserved": 2145,
  "old_processed_excluded": 2418,
  "remaining_candidates": 6082,
  "pilot_tasks": 60,
  "new_accepted_target": 3000,
  "pilot_included_in_target": true,
  "seed": 2026100901,
  "source": "GSM_Infinite",
  "original_pool_sha256": "35a0a345e8e94d66a953d2ee9cdc43eee2b00c6421a472037ea720a152ca07d3",
  "new_pool_sha256": "b5203a8608dbaa2b549f38e3d4096c5cf59762c820e55da09fb83fa520484c1a",
  "pilot_op_histogram": {
    "23": 7,
    "29": 4,
    "21": 10,
    "27": 7,
    "30": 3,
    "25": 4,
    "22": 9,
    "28": 5,
    "24": 5,
    "26": 3,
    "19": 1,
    "20": 1,
    "18": 1
  },
  "pilot_source_histogram": {
    "InfiniAILab/gsm_infinite_hard_0": 50,
    "InfiniAILab/gsm_infinite_medium_0": 10
  },
  "old_journal_sha256": "0a36ddbd37c88ff0e2d612281afcd9ae28873ed5ef236454955dcca269fe2d4f",
  "candidate_pool_sha256": "91f93532b4473c2c7e9bce4a021ea9c6f495dec35b3035fd823e504c7f9190e0",
  "verification_eligible_pilot": 8,
  "pilot_parent": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-20261009",
  "prompt_version": "wide-cut-explicit-verified-v2",
  "serialization_version": "counted-forks-think-tail-final-v4",
  "expanded_candidates": 10587,
  "source_expansion_manifest": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/expanded-source-manifest.json",
  "mean_width_acceptance_target": null,
  "narrow_valid_candidates_retained": true,
  "width_filter_enabled": false
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/student-system.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/production/student-system.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit-before-pathcheck.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit-before-pathcheck.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit-v2-noverify.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit-v2-noverify.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [exps/deepseek-gsm-wide3000-v2-20261009/final-statistics.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/final-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished_moscow": "2026-10-09T21:12:27.745747+03:00",
  "new_examples": 3000,
  "old_examples_preserved": 2145,
  "combined_if_used": 5145,
  "train": 2700,
  "val": 300,
  "decisions": 3551,
  "acceptance_percent": 84.48324415657561,
  "sources": {
    "GSM_Infinite": 3000
  },
  "source_datasets": {
    "InfiniAILab/gsm_infinite_medium_0": 375,
    "InfiniAILab/gsm_infinite_hard_0": 2449,
    "InfiniAILab/gsm_infinite_hard_8k": 104,
    "InfiniAILab/gsm_infinite_medium_8k": 72
  },
  "op_histogram": {
    "26": 125,
    "23": 375,
    "21": 463,
    "19": 50,
    "24": 219,
    "28": 240,
    "22": 393,
    "20": 46,
    "27": 340,
    "25": 161,
    "29": 196,
    "30": 125,
    "8": 11,
    "16": 32,
    "12": 16,
    "11": 22,
    "18": 42,
    "14": 28,
    "17": 35,
    "13": 13,
    "10": 11,
    "15": 27,
    "6": 7,
    "9": 10,
    "7": 9,
    "5": 4
  },
  "forks": 3486,
  "mean_width_per_fork": 3.291738382099828,
  "width_histogram": {
    "4": 1493,
    "3": 943,
    "2": 865,
    "5": 166,
    "6": 19
  },
  "round_histogram": {
    "1": 2510,
    "2": 473,
    "3": 10,
    "0": 7
  },
  "mean_rounds": 1.162,
  "width_above_two_percent": 75.18646012621916,
  "verification_rows": 784,
  "verification_rows_percent": 26.133333333333333,
  "verification_paths": 830,
  "all_accepted_reference_match": true,
  "pipeline_final_answer_checks": {
    "checked": 3303,
    "correct": 3285,
    "note": "Conditional on pipeline reaching the answer-check stage; not all teacher responses."
  },
  "output_tokens": {
    "mean": 815.636,
    "p50": 786.0,
    "p90": 1082.2999999999997,
    "p95": 1194.0499999999997,
    "p99": 1412.039999999999,
    "max": 2073.0
  },
  "student_sequence_tokens": {
    "mean": 2277.854,
    "p50": 2278.0,
    "p90": 2839.2,
    "p95": 3096.0499999999997,
    "p99": 3610.159999999996,
    "max": 4214.0
  },
  "critical_path_tokens_proxy": {
    "mean": 586.6103333333333,
    "p50": 566.0,
    "p90": 772.0,
    "p95": 855.0499999999997,
    "p99": 1010.0,
    "max": 1368.0
  },
  "sequential_output_tokens": {
    "mean": 435.46133333333336,
    "p50": 420.0,
    "p90": 589.0999999999999,
    "p95": 649.0499999999997,
    "p99": 797.0099999999998,
    "max": 1077.0
  },
  "path_tokens": {
    "mean": 98.3920697167756,
    "p50": 86.0,
    "p90": 159.0,
    "p95": 194.0,
    "p99": 293.0,
    "max": 807.0
  },
  "validation": {
    "unique_ids": true,
    "train_val_group_disjoint": true,
    "hashes_match": true,
    "single_think": true,
    "all_parallel_blocks_inside_think": true,
    "final_solution_outside_think": true
  },
  "limitations": [
    "Semantic critic is the teacher model; final-answer matching is not a proof of every reasoning step.",
    "Critical-path token count is a proxy, not measured forwards or student accuracy."
  ],
  "all_accepted_journal_grades_checked": 3000
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/pilot-statistics.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/pilot-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791553415.3304732,
  "pilot_state": {
    "state": "complete",
    "started_at": 1791549779.0861397,
    "total": 60,
    "completed": 60,
    "errors": 4,
    "finished_at": 1791550506.9898608
  },
  "completed": 60,
  "target": 60,
  "final_correct": 59,
  "final_checked": 60,
  "structure_valid": 46,
  "accepted": 40,
  "errors": {
    "AssertionError('structural_or_answer_check')": 3,
    "deterministic_path_audit/path_without_explicit_computation": 10,
    "semantic_judge_reject": 6,
    "AssertionError('judge_not_finished')": 1
  },
  "judge_issues": [
    {
      "id": "gsm_infinite_hard_0/ops_30-00000-of-00001/471",
      "issues": [
        "In the second fork, Path 2 mislabels the Oldhevan sports-academy average as a_RO: it says a_RO = 4 + a_CW = 68, but the problem gives a_AO = 4 + a_CW, while a_RO is the requested final quantity and equals 514. This creates a contradiction a_RO = 68 versus the final a_RO = 514, even though the subsequent a_CH = 64 and final answer 514 are numerically correct."
      ]
    },
    {
      "id": "gsm_infinite/2195",
      "issues": [
        "Path 3 recomputes M_E=4 exactly as Path 1 does; it is not a valid verification because the summary never compares the two M_E outputs, so it is redundant and not a distinct useful contribution."
      ]
    },
    {
      "id": "gsm_infinite/3867",
      "issues": [
        "Second fork Path 1 computes p_SZ=6, but Path 2 recomputes p_SZ and uses it to compute c_HF; p_SZ is not used in the final answer, and the summary's check is not an independent verification, so this branch output is redundant/unused."
      ]
    },
    {
      "id": "gsm_infinite_hard_0/ops_27-00000-of-00001/764",
      "issues": [
        "Path 2 computes adult crow in South Zoo = 12, but this main output is not used in the final calculation; Path 3 recomputes it, and the summary does not use Path 2's result. This violates the requirement that every branch output be used.",
        "The summary's comparison of the Edison Park owl value from Path 1 with Paths 2 and 4 is an unplanned verification; the plan did not identify a verification branch or state what it verifies, so verification_paths_valid is false.",
        "Path 1's output is only used in that unplanned verification, not in the final calculation."
      ]
    },
    {
      "id": "gsm_infinite_hard_0/ops_23-00000-of-00001/1057",
      "issues": [
        "Second fork Path 4 uses D_S=22 without recomputing D_S=T_C+D_C=20+2, so it imports sibling Path 1's result; this breaks path independence and makes the T_S verification non-independent."
      ]
    },
    {
      "id": "gsm_infinite/649",
      "issues": [
        "First fork Path 2 recomputes FKAC_S already computed in Path 1 and Path 3; it is not planned as a verification branch, so its output is redundant/unused except an unplanned comparison.",
        "Abbreviations FSM_B, CRM_B, IDT_M, RBMM_M, FKAC_P, SPD_P, IDT_S, RBMM_V are used without defining their meanings, reducing teachability.",
        "Summary says FKAC_S values are used next, but FKAC_S is not used in later calculations."
      ]
    }
  ],
  "all": {
    "rows": 60,
    "forks": 74,
    "mean_width_per_fork": 3.2567567567567566,
    "width_histogram": {
      "4": 34,
      "3": 22,
      "2": 17,
      "5": 1
    },
    "round_histogram": {
      "0": 2,
      "1": 43,
      "2": 14,
      "3": 1
    },
    "op_histogram": {
      "25": 4,
      "26": 3,
      "22": 9,
      "23": 7,
      "21": 10,
      "19": 1,
      "24": 5,
      "28": 5,
      "20": 1,
      "27": 7,
      "29": 4,
      "30": 3,
      "18": 1
    },
    "total_tokens": {
      "mean": 854.7833333333333,
      "p50": 835.5,
      "p90": 1071.2,
      "p95": 1201.3999999999999,
      "max": 1411.0
    },
    "sequential_tokens": {
      "mean": 457.73333333333335,
      "p50": 450.5,
      "p90": 600.3,
      "p95": 610.5,
      "max": 732.0
    },
    "critical_path_tokens_proxy": {
      "mean": 615.4,
      "p50": 622.0,
      "p90": 767.0,
      "p95": 801.8,
      "max": 900.0
    },
    "parallel_path_tokens": {
      "mean": 393.03333333333336,
      "p50": 398.5,
      "p90": 576.9,
      "p95": 598.9999999999998,
      "max": 836.0
    },
    "student_tokens": {
      "mean": 2274.5789473684213,
      "p50": 2363.0,
      "p90": 2766.2,
      "p95": 2946.399999999999,
      "max": 3221.0
    },
    "verification_paths": 11,
    "rows_with_verification": 11,
    "mean_distinct_work_width_proxy_judged": 3.0833333333333335,
    "mean_critical_to_total_ratio": 0.7267297280028236,
    "width_by_op": {
      "25": {
        "forks": 4,
        "mean_width": 3.0
      },
      "26": {
        "forks": 4,
        "mean_width": 3.5
      },
      "22": {
        "forks": 8,
        "mean_width": 3.125
      },
      "23": {
        "forks": 9,
        "mean_width": 3.111111111111111
      },
      "21": {
        "forks": 14,
        "mean_width": 3.142857142857143
      },
      "19": {
        "forks": 1,
        "mean_width": 4.0
      },
      "24": {
        "forks": 6,
        "mean_width": 3.0
      },
      "28": {
        "forks": 7,
        "mean_width": 3.142857142857143
      },
      "20": {
        "forks": 1,
        "mean_width": 4.0
      },
      "27": {
        "forks": 9,
        "mean_width": 3.5555555555555554
      },
      "29": {
        "forks": 4,
        "mean_width": 4.0
      },
      "30": {
        "forks": 5,
        "mean_width": 3.4
      },
      "18": {
        "forks": 2,
        "mean_width": 2.5
      }
    }
  },
  "accepted_subset": {
    "rows": 40,
    "forks": 48,
    "mean_width_per_fork": 3.1875,
    "width_histogram": {
      "4": 23,
      "3": 11,
      "2": 14
    },
    "round_histogram": {
      "1": 33,
      "2": 6,
      "3": 1
    },
    "op_histogram": {
      "26": 3,
      "23": 6,
      "21": 8,
      "19": 1,
      "24": 4,
      "28": 3,
      "22": 5,
      "20": 1,
      "27": 4,
      "25": 2,
      "29": 2,
      "30": 1
    },
    "total_tokens": {
      "mean": 844.425,
      "p50": 808.0,
      "p90": 1083.9,
      "p95": 1231.6499999999999,
      "max": 1411.0
    },
    "sequential_tokens": {
      "mean": 439.1,
      "p50": 437.5,
      "p90": 592.8,
      "p95": 603.3,
      "max": 610.0
    },
    "critical_path_tokens_proxy": {
      "mean": 599.1,
      "p50": 573.5,
      "p90": 788.4,
      "p95": 819.7499999999999,
      "max": 900.0
    },
    "parallel_path_tokens": {
      "mean": 401.5,
      "p50": 398.5,
      "p90": 594.2,
      "p95": 658.4499999999998,
      "max": 836.0
    },
    "student_tokens": {
      "mean": 2212.9,
      "p50": 2275.0,
      "p90": 2574.9000000000005,
      "p95": 2919.0999999999995,
      "max": 3127.0
    },
    "verification_paths": 7,
    "rows_with_verification": 7,
    "mean_distinct_work_width_proxy_judged": 3.0416666666666665,
    "mean_critical_to_total_ratio": 0.7159822150049717,
    "width_by_op": {
      "26": {
        "forks": 4,
        "mean_width": 3.5
      },
      "23": {
        "forks": 7,
        "mean_width": 2.857142857142857
      },
      "21": {
        "forks": 12,
        "mean_width": 3.0
      },
      "19": {
        "forks": 1,
        "mean_width": 4.0
      },
      "24": {
        "forks": 5,
        "mean_width": 3.0
      },
      "28": {
        "forks": 3,
        "mean_width": 4.0
      },
      "22": {
        "forks": 5,
        "mean_width": 2.8
      },
      "20": {
        "forks": 1,
        "mean_width": 4.0
      },
      "27": {
        "forks": 4,
        "mean_width": 3.75
      },
      "25": {
        "forks": 3,
        "mean_width": 2.6666666666666665
      },
      "29": {
        "forks": 2,
        "mean_width": 3.5
      },
      "30": {
        "forks": 1,
        "mean_width": 4.0
      }
    }
  },
  "limitations": [
    "Teacher answer correctness is measured against source references; acceptance also uses the same model as semantic critic.",
    "Critical-path tokens are a tokenizer-based proxy, not measured runtime forwards or small-student accuracy.",
    "Mean width is weighted per fork; examples with no forks do not enter this mean."
  ]
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/pilot-status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/pilot-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791549779.0861397,
  "total": 60,
  "completed": 60,
  "errors": 4,
  "finished_at": 1791550506.9898608
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/pipeline-status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/pipeline-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791555386.5366151,
  "target": 3000,
  "mean_width_target": null,
  "concurrency": 256,
  "source": "GSM_Infinite",
  "stage": "serialize_think.py",
  "updated_at": 1791569521.3060184,
  "child_pid": 1012618,
  "finished_at": 1791569547.7457466,
  "output": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think"
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/final-statistics.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/final-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished_moscow": "2026-10-09T21:12:27.745747+03:00",
  "new_examples": 3000,
  "old_examples_preserved": 2145,
  "combined_if_used": 5145,
  "train": 2700,
  "val": 300,
  "decisions": 3551,
  "acceptance_percent": 84.48324415657561,
  "sources": {
    "GSM_Infinite": 3000
  },
  "source_datasets": {
    "InfiniAILab/gsm_infinite_medium_0": 375,
    "InfiniAILab/gsm_infinite_hard_0": 2449,
    "InfiniAILab/gsm_infinite_hard_8k": 104,
    "InfiniAILab/gsm_infinite_medium_8k": 72
  },
  "op_histogram": {
    "26": 125,
    "23": 375,
    "21": 463,
    "19": 50,
    "24": 219,
    "28": 240,
    "22": 393,
    "20": 46,
    "27": 340,
    "25": 161,
    "29": 196,
    "30": 125,
    "8": 11,
    "16": 32,
    "12": 16,
    "11": 22,
    "18": 42,
    "14": 28,
    "17": 35,
    "13": 13,
    "10": 11,
    "15": 27,
    "6": 7,
    "9": 10,
    "7": 9,
    "5": 4
  },
  "forks": 3486,
  "mean_width_per_fork": 3.291738382099828,
  "width_histogram": {
    "4": 1493,
    "3": 943,
    "2": 865,
    "5": 166,
    "6": 19
  },
  "round_histogram": {
    "1": 2510,
    "2": 473,
    "3": 10,
    "0": 7
  },
  "mean_rounds": 1.162,
  "width_above_two_percent": 75.18646012621916,
  "verification_rows": 784,
  "verification_rows_percent": 26.133333333333333,
  "verification_paths": 830,
  "all_accepted_reference_match": true,
  "pipeline_final_answer_checks": {
    "checked": 3303,
    "correct": 3285,
    "note": "Conditional on pipeline reaching the answer-check stage; not all teacher responses."
  },
  "output_tokens": {
    "mean": 815.636,
    "p50": 786.0,
    "p90": 1082.2999999999997,
    "p95": 1194.0499999999997,
    "p99": 1412.039999999999,
    "max": 2073.0
  },
  "student_sequence_tokens": {
    "mean": 2277.854,
    "p50": 2278.0,
    "p90": 2839.2,
    "p95": 3096.0499999999997,
    "p99": 3610.159999999996,
    "max": 4214.0
  },
  "critical_path_tokens_proxy": {
    "mean": 586.6103333333333,
    "p50": 566.0,
    "p90": 772.0,
    "p95": 855.0499999999997,
    "p99": 1010.0,
    "max": 1368.0
  },
  "sequential_output_tokens": {
    "mean": 435.46133333333336,
    "p50": 420.0,
    "p90": 589.0999999999999,
    "p95": 649.0499999999997,
    "p99": 797.0099999999998,
    "max": 1077.0
  },
  "path_tokens": {
    "mean": 98.3920697167756,
    "p50": 86.0,
    "p90": 159.0,
    "p95": 194.0,
    "p99": 293.0,
    "max": 807.0
  },
  "validation": {
    "unique_ids": true,
    "train_val_group_disjoint": true,
    "hashes_match": true,
    "single_think": true,
    "all_parallel_blocks_inside_think": true,
    "final_solution_outside_think": true
  },
  "limitations": [
    "Semantic critic is the teacher model; final-answer matching is not a proof of every reasoning step.",
    "Critical-path token count is a proxy, not measured forwards or student accuracy."
  ],
  "all_accepted_journal_grades_checked": 3000
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/summary.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "accepted": 3000,
  "train": 2700,
  "val": 300,
  "serialization_version": "counted-forks-think-tail-final-v4",
  "all_rendered_single_think": true,
  "all_parallel_blocks_inside_think": true,
  "final_answers_outside_think": true,
  "sources": {
    "GSM_Infinite": 3000
  },
  "sha256": {
    "train.jsonl": "7379ecfc7053771313df1bc63c6324a3f3f8ee72bdfc818015bdc35ae600b24a",
    "val.jsonl": "d5a868ef8fc42a50f21a7e9cb657da1a894b882ddeabb256b6f1eeb6112a23c5",
    "train.parquet": "6948d849e8104e268e77a63e0eedb5f26459fe2b0234f8de0ab6e21d2bed44b5",
    "val.parquet": "5729683b015430681da8aa1e267e8e897b10416fc8c33c911d9553a0af112344",
    "student-system.txt": "49efaf2415b43fc6acc8cc4069858aefccebc5a6011d88eb83291d2796d186ca"
  }
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/production/status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791553648.631078,
  "resumed_at": 1791555396.298789,
  "concurrency": 256,
  "reasoning_effort": 50,
  "targets": {
    "GSM_Infinite": 3000
  },
  "accepted": {
    "GSM_Infinite": 3000
  },
  "processed": 3551,
  "active_requests": 0,
  "max_active_requests": 256,
  "inflight": {
    "GSM_Infinite": 0
  },
  "errors": {
    "AssertionError('structural_or_answer_check')": 3,
    "deterministic_path_audit": 10,
    "semantic_judge_reject": 236,
    "AssertionError('judge_not_finished')": 1,
    "structure": 248,
    "judge_not_finished": 36,
    "answer_verification": 17
  },
  "accepted_round_histogram": {
    "1": 2510,
    "2": 473,
    "3": 10,
    "0": 7
  },
  "accepted_width_histogram": {
    "4": 1493,
    "3": 943,
    "2": 865,
    "5": 166,
    "6": 19
  },
  "updated_at": 1791569518.335289,
  "finished_at": 1791569518.33528
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/production/summary.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/production/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "accepted": 3000,
  "sources": {
    "GSM_Infinite": 3000
  },
  "train": 2700,
  "val": 300,
  "rounds": {
    "1": 2510,
    "2": 473,
    "3": 10,
    "0": 7
  },
  "widths": {
    "4": 1493,
    "3": 943,
    "2": 865,
    "5": 166,
    "6": 19
  },
  "total_requests_max_concurrency": 256,
  "rejections": {
    "AssertionError('structural_or_answer_check')": 3,
    "deterministic_path_audit": 10,
    "semantic_judge_reject": 236,
    "AssertionError('judge_not_finished')": 1,
    "structure": 248,
    "judge_not_finished": 36,
    "answer_verification": 17
  },
  "mean_width_target": null,
  "mean_width_actual": 3.291738382099828,
  "valid_narrow_traces_preserved": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/valid-narrow-deferred.jsonl",
  "limitations": [
    "Semantic judge uses the same teacher model and is not a formal proof checker.",
    "Decontamination is textual, not a guarantee against semantic paraphrases.",
    "Serving inference was teacher serialization, not separate isolated worker generation.",
    "Requires counted-fork-aware SFT loader and rollout runtime."
  ],
  "sha256": {
    "train.jsonl": "7131400db09ef5df846388b5049a08af9f3ad651c2f1a0b028fa2a0f0adc40fb",
    "val.jsonl": "3f56e6037c65a5cec1e4fb918bc46cb4f75e07401e88933fe04a77f9c3930251",
    "train.parquet": "6851db93ec911b49ad62cdfa90c401ecd4fa28c5a1f59560a17e492fec185873",
    "val.parquet": "44bee448e774328f96ff7647bc27a5f7b37e6962cb9abae882120e92df3151d2"
  }
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/remove-width-filter-status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/remove-width-filter-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "resumed",
  "requested_at": 1791554425.6414073,
  "width_filter_enabled": false,
  "old_controller_pid": 1010072,
  "updated_at": 1791555381.2979186,
  "resumed_at": 1791555386.4933028,
  "new_pipeline_pid": 1010781,
  "accepted_at_resume": 289,
  "restored_count": 141,
  "restored_ids": "141 records; see original artifact",
  "previous_journal_sha256": "17db5460424d366e3a92e4207b5102a6253494c41ff8e354255b2907c023bbce"
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/think-export-status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/think-export-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": 1791569547.086743,
  "output": "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think"
}
```

</details>

- [exps/deepseek-gsm-wide3000-v2-20261009/verification-pilot-status.json](../artifacts/exps/deepseek-gsm-wide3000-v2-20261009/verification-pilot-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791550733.364699,
  "total": 8,
  "completed": 8,
  "errors": 0,
  "finished_at": 1791551122.862545
}
```

</details>
