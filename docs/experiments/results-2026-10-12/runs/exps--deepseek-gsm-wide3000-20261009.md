# exps/deepseek-gsm-wide3000-20261009

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/deepseek-gsm-wide3000-20261009/judge-prompt.txt](../artifacts/exps/deepseek-gsm-wide3000-20261009/judge-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-20261009/pool-manifest.json](../artifacts/exps/deepseek-gsm-wide3000-20261009/pool-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791548150.0458782,
  "old_accepted_preserved": 2145,
  "old_processed_excluded": 2418,
  "remaining_candidates": 6082,
  "pilot_tasks": 60,
  "new_accepted_target": 3000,
  "pilot_included_in_target": true,
  "seed": 2026100901,
  "source": "GSM_Infinite",
  "original_pool_sha256": "35a0a345e8e94d66a953d2ee9cdc43eee2b00c6421a472037ea720a152ca07d3",
  "new_pool_sha256": "feb5ac149852cdc9f171c4105820f653b0febda4a564ee0f114185b1c070c426",
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
  "old_journal_sha256": "0a36ddbd37c88ff0e2d612281afcd9ae28873ed5ef236454955dcca269fe2d4f"
}
```

</details>

- [exps/deepseek-gsm-wide3000-20261009/prompt-wide-explicit.txt](../artifacts/exps/deepseek-gsm-wide3000-20261009/prompt-wide-explicit.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/deepseek-gsm-wide3000-20261009/student-system.txt](../artifacts/exps/deepseek-gsm-wide3000-20261009/student-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [exps/deepseek-gsm-wide3000-20261009/pilot-statistics.json](../artifacts/exps/deepseek-gsm-wide3000-20261009/pilot-statistics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "at": 1791549480.4588666,
  "pilot_state": {
    "state": "complete",
    "started_at": 1791548159.7650433,
    "total": 60,
    "completed": 60,
    "errors": 20,
    "finished_at": 1791548849.5210388
  },
  "completed": 60,
  "target": 60,
  "final_correct": 59,
  "final_checked": 60,
  "structure_valid": 42,
  "accepted": 35,
  "errors": {
    "AssertionError('structural_or_answer_check')": 18,
    "semantic_judge_reject": 5,
    "AssertionError('judge_not_finished')": 2
  },
  "judge_issues": [
    {
      "id": "gsm_infinite_hard_0/ops_22-00000-of-00001/734",
      "issues": [
        "Second fork Path 3 merely copies the given value L_M=3; it is not a computed contribution, so the no-given-only-path requirement is violated. It is used in T_M, but it should be folded into the summary or replaced by a computed/verification branch.",
        "Because one parallel branch is only a given-value copy, the parallelism is not fully useful even though the other branches are valid."
      ]
    },
    {
      "id": "gsm_infinite/3777",
      "issues": [
        "Path 1 computes S=8 and Path 2 computes O=17, but Path 3 recomputes S and Path 4 recomputes O; the Path 1/2 outputs are not used downstream, so those branches are redundant.",
        "Because Path 1/3 duplicate S and Path 2/4 duplicate O, the fork does not have four distinct useful contributions; useful parallelism is only the two Fisherman-component paths.",
        "The summary lists S and O as established, but the final merge F=16+20=36 and subsequent Ruby/Clearwater calculations do not consume S or O."
      ]
    },
    {
      "id": "gsm_infinite/1036",
      "issues": [
        "Paths 2, 3, and 4 use C = 4 without deriving it in-path; C is computed only in Path 1, so they silently import a sibling result in a parallel fork. They should recompute C = 2 * P = 2 * 2 = 4 or the fork should be sequential."
      ]
    },
    {
      "id": "gsm_infinite_hard_0/ops_27-00000-of-00001/2089",
      "issues": [
        "Path 3 computes A_CM_UMC=2 and N_FIM_UMC=2, but neither value is used in the remaining solution; it is an unused branch output.",
        "The summary says the established values 'feed the remaining chain,' but N_FIM_UMC=2 is never consumed downstream, so the summary overstates downstream use."
      ]
    },
    {
      "id": "gsm_infinite_hard_0/ops_21-00000-of-00001/285",
      "issues": [
        "Undefined abbreviations PB, RB, and FSR are used in the plan/summary without definitions, so the explanation is not fully self-contained for a small student."
      ]
    }
  ],
  "all": {
    "rows": 60,
    "forks": 68,
    "mean_width_per_fork": 3.3529411764705883,
    "width_histogram": {
      "4": 32,
      "3": 25,
      "2": 10,
      "5": 1
    },
    "round_histogram": {
      "1": 50,
      "0": 1,
      "2": 9
    },
    "op_histogram": {
      "22": 9,
      "21": 10,
      "23": 7,
      "27": 7,
      "24": 5,
      "19": 1,
      "29": 4,
      "28": 5,
      "25": 4,
      "26": 3,
      "20": 1,
      "30": 3,
      "18": 1
    },
    "total_tokens": {
      "mean": 738.5,
      "p50": 726.5,
      "p90": 975.6,
      "p95": 1085.35,
      "max": 1211.0
    },
    "sequential_tokens": {
      "mean": 339.43333333333334,
      "p50": 319.5,
      "p90": 490.8,
      "p95": 554.0,
      "max": 731.0
    },
    "critical_path_tokens_proxy": {
      "mean": 507.71666666666664,
      "p50": 486.5,
      "p90": 683.8000000000001,
      "p95": 740.55,
      "max": 824.0
    },
    "parallel_path_tokens": {
      "mean": 395.26666666666665,
      "p50": 381.0,
      "p90": 594.4000000000001,
      "p95": 639.0,
      "max": 752.0
    },
    "student_tokens": {
      "mean": 2169.690476190476,
      "p50": 2205.5,
      "p90": 2574.1,
      "p95": 2643.0,
      "max": 2948.0
    },
    "width_by_op": {
      "22": {
        "forks": 10,
        "mean_width": 3.5
      },
      "21": {
        "forks": 10,
        "mean_width": 3.4
      },
      "23": {
        "forks": 9,
        "mean_width": 2.7777777777777777
      },
      "27": {
        "forks": 8,
        "mean_width": 3.25
      },
      "24": {
        "forks": 6,
        "mean_width": 3.0
      },
      "19": {
        "forks": 1,
        "mean_width": 3.0
      },
      "29": {
        "forks": 4,
        "mean_width": 4.0
      },
      "28": {
        "forks": 6,
        "mean_width": 3.6666666666666665
      },
      "25": {
        "forks": 6,
        "mean_width": 3.3333333333333335
      },
      "26": {
        "forks": 3,
        "mean_width": 3.6666666666666665
      },
      "20": {
        "forks": 1,
        "mean_width": 4.0
      },
      "30": {
        "forks": 3,
        "mean_width": 4.0
      },
      "18": {
        "forks": 1,
        "mean_width": 2.0
      }
    }
  },
  "accepted_subset": {
    "rows": 35,
    "forks": 39,
    "mean_width_per_fork": 3.4615384615384617,
    "width_histogram": {
      "3": 10,
      "4": 22,
      "2": 6,
      "5": 1
    },
    "round_histogram": {
      "1": 31,
      "2": 4
    },
    "op_histogram": {
      "19": 1,
      "21": 7,
      "24": 3,
      "28": 4,
      "25": 2,
      "26": 3,
      "23": 2,
      "22": 3,
      "20": 1,
      "29": 2,
      "27": 3,
      "30": 3,
      "18": 1
    },
    "total_tokens": {
      "mean": 774.5714285714286,
      "p50": 761.0,
      "p90": 1023.4000000000001,
      "p95": 1159.8,
      "max": 1211.0
    },
    "sequential_tokens": {
      "mean": 342.1714285714286,
      "p50": 330.0,
      "p90": 463.2,
      "p95": 514.7999999999998,
      "max": 566.0
    },
    "critical_path_tokens_proxy": {
      "mean": 521.2285714285714,
      "p50": 510.0,
      "p90": 676.4,
      "p95": 721.5999999999999,
      "max": 824.0
    },
    "parallel_path_tokens": {
      "mean": 428.54285714285714,
      "p50": 406.0,
      "p90": 634.2,
      "p95": 657.8999999999999,
      "max": 752.0
    },
    "student_tokens": {
      "mean": 2172.5714285714284,
      "p50": 2225.0,
      "p90": 2544.0,
      "p95": 2617.0,
      "max": 2948.0
    },
    "width_by_op": {
      "19": {
        "forks": 1,
        "mean_width": 3.0
      },
      "21": {
        "forks": 7,
        "mean_width": 3.5714285714285716
      },
      "24": {
        "forks": 5,
        "mean_width": 3.0
      },
      "28": {
        "forks": 4,
        "mean_width": 3.75
      },
      "25": {
        "forks": 3,
        "mean_width": 3.0
      },
      "26": {
        "forks": 3,
        "mean_width": 3.6666666666666665
      },
      "23": {
        "forks": 2,
        "mean_width": 2.5
      },
      "22": {
        "forks": 3,
        "mean_width": 3.6666666666666665
      },
      "20": {
        "forks": 1,
        "mean_width": 4.0
      },
      "29": {
        "forks": 2,
        "mean_width": 4.5
      },
      "27": {
        "forks": 4,
        "mean_width": 3.5
      },
      "30": {
        "forks": 3,
        "mean_width": 4.0
      },
      "18": {
        "forks": 1,
        "mean_width": 2.0
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

- [exps/deepseek-gsm-wide3000-20261009/pilot-status.json](../artifacts/exps/deepseek-gsm-wide3000-20261009/pilot-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "started_at": 1791548159.7650433,
  "total": 60,
  "completed": 60,
  "errors": 20,
  "finished_at": 1791548849.5210388
}
```

</details>
