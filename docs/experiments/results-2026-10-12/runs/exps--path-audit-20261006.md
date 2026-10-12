# exps/path-audit-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/path-audit-20261006/math/semantic-summary.json](../artifacts/exps/path-audit-20261006/math/semantic-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "review": "Single Codex manual reviewer. Fixed seed20261006 uniform block sample; each async20 of structurally valid two-path blocks. Block frequency, conditional on parseable structure, not question/response frequency. Both_sound means local path reasoning; not full solution. Invalid incomplete inputs separated; tiny sample does not establish seen/unseen semantic difference.",
  "runs": {
    "seen-async": {
      "sample_blocks": 20,
      "sample_unique_questions": 20,
      "input_incomplete": 2,
      "eligible_semantic_blocks": 18,
      "categories": {
        "same_method": 8,
        "degenerate_or_unclear": 9,
        "distinct": 1
      },
      "both_sound": 6,
      "answer_in_prefix": 6,
      "saved_correct": 4,
      "saved_correct_with_both_sound": 1
    },
    "unseen-async": {
      "sample_blocks": 20,
      "sample_unique_questions": 19,
      "input_incomplete": 2,
      "eligible_semantic_blocks": 18,
      "categories": {
        "same_method": 6,
        "degenerate_or_unclear": 12
      },
      "both_sound": 3,
      "answer_in_prefix": 3,
      "saved_correct": 3,
      "saved_correct_with_both_sound": 1
    }
  }
}
```

</details>

- [exps/path-audit-20261006/sft/semantic-summary.json](../artifacts/exps/path-audit-20261006/sft/semantic-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "sample_n": 60,
  "sample_unit": "uniform random well-formed two-path block",
  "seed": 20261006,
  "unique_rows": 60,
  "category_counts": {
    "arithmetic_reformulation": 35,
    "same_method": 14,
    "unclear": 4,
    "substantive_or_complementary": 7
  },
  "category_wilson95": {
    "arithmetic_reformulation": [
      0.45727854313239624,
      0.6993591351212818
    ],
    "same_method": [
      0.1443943161843107,
      0.3543651134039202
    ],
    "unclear": [
      0.02622827414319792,
      0.15925579893767722
    ],
    "substantive_or_complementary": [
      0.05767647403450049,
      0.2217902059985814
    ]
  },
  "both_sound": 54,
  "result_in_prefix": 18,
  "summary_oversells": 13,
  "category_counts_both_sound": {
    "arithmetic_reformulation": 35,
    "same_method": 13,
    "unclear": 1,
    "substantive_or_complementary": 5
  },
  "category_counts_prefix_results": {
    "arithmetic_reformulation": 8,
    "same_method": 4,
    "unclear": 3,
    "substantive_or_complementary": 3
  },
  "limitations": "Single-reviewer manual labels; arithmetic reformulations not substantive alternatives; intervals reflect sample variance only, not annotation uncertainty; block frequency, not row frequency; excluded malformed and non-two-path blocks; some substantive category items are cases or complementary constraints, not different strategies.",
  "substantive_category_subtypes": {
    "alternative_derivation": {
      "sample_ids": [
        19,
        34
      ],
      "count": 2,
      "both_sound_count": 2
    },
    "maximality_verification": {
      "sample_ids": [
        35
      ],
      "count": 1,
      "both_sound_count": 1
    },
    "complementary_related_targets": {
      "sample_ids": [
        22,
        51
      ],
      "count": 2,
      "both_sound_count": 1
    },
    "explicit_assumption_or_interpretation_cases": {
      "sample_ids": [
        32,
        58
      ],
      "count": 2,
      "both_sound_count": 1
    }
  },
  "substantial_same_target_derivation_or_verification_count": 3
}
```

</details>
