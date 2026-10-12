# exps/downloaded-sft-audit-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/downloaded-sft-audit-20261008/prompt-strategy-recommendation.txt](../artifacts/exps/downloaded-sft-audit-20261008/prompt-strategy-recommendation.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/prompt-strategy-single-call-candidate.txt](../artifacts/exps/downloaded-sft-audit-20261008/prompt-strategy-single-call-candidate.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/realistic-semantic-safe-plan-example.json](../artifacts/exps/downloaded-sft-audit-20261008/realistic-semantic-safe-plan-example.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "source_row_1based": 3779,
  "source_id": "realistic_parallel_03778",
  "quantity_dictionary": {
    "q01": "number of astronomy books at Stonegate Library",
    "q02": "number of cookbooks at Lakeside Library",
    "q03": "number of cookbooks at Stonegate Library",
    "q04": "number of mystery novels at Oak Lane Library",
    "q05": "number of engineering manuals at Grandview Library",
    "q06": "number of art books at Pine Street Library",
    "q07": "number of music books at Eastbridge Library",
    "q08": "number of science books at Silverbrook Library",
    "q09": "number of architecture books at Pine Street Library"
  },
  "plan_text": "Plan: compute q02 from the given q01. For block B1, both paths may read q02. Path B1.P1 computes q03 then q04. Path B1.P2 computes q05 then q06 then q07. After joining q04 and q07, compute q08, then the requested q09.",
  "branch_metadata": [
    {
      "block_id": "B1",
      "shared_inputs": [
        "q02"
      ],
      "paths": [
        {
          "path_id": "B1.P1",
          "ordered_outputs": [
            "q03",
            "q04"
          ],
          "terminal_result": "q04"
        },
        {
          "path_id": "B1.P2",
          "ordered_outputs": [
            "q05",
            "q06",
            "q07"
          ],
          "terminal_result": "q07"
        }
      ],
      "join_outputs": [
        "q08"
      ]
    }
  ],
  "safety_boundary": "Illustrative metadata plus proposed nonnumeric assistant prelude only; source row is unchanged. The plan contains no computed branch answers. Do not introduce Path tag attributes without checking loader/parser support. Keep complete quantity type and referent in dictionary. This fixes missing explicit planning/identity, not story realism or arithmetic diversity."
}
```

</details>

## Метрики и полнота результатов

- [exps/downloaded-sft-audit-20261008/gsm-semantic-report.md](../artifacts/exps/downloaded-sft-audit-20261008/gsm-semantic-report.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/mixed-math-report.md](../artifacts/exps/downloaded-sft-audit-20261008/mixed-math-report.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/mixed-math-summary.json](../artifacts/exps/downloaded-sft-audit-20261008/mixed-math-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "total_rows": 5000,
  "procedural_question_checks": 4500,
  "procedural_answers_correct": 4500,
  "reference_rows_not_independently_solved": 500,
  "numeric_equalities": 14749,
  "numeric_equality_rows": 4568,
  "numeric_equality_mismatches": 0,
  "case_candidate_grid_checks": 972,
  "case_candidate_grid_rows": 658,
  "case_candidate_grid_mismatches": 0,
  "parallel_rounds": {
    "1": 4700,
    "0": 300
  },
  "verify_rows": 1195,
  "verify_wrong_claims": 343,
  "verify_correct_claims": 852,
  "correct_answer_in_assistant_before_plan": 764,
  "new_method_verify_wrong_claims": 130,
  "new_method_verify_wrong_claim_delta_counts": {
    "1": 130
  },
  "families": "55 records; see original artifact"
}
```

</details>

- [exps/downloaded-sft-audit-20261008/realistic-math-summary.json](../artifacts/exps/downloaded-sft-audit-20261008/realistic-math-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "source": "${DATA_SOURCE_ROOT}/sft_messages_5000.jsonl",
  "source_sha256": "ce0bc7febe267be6761d6689e52f5b57bcaaba6ebdb5a9ed7813ffea35a05dda",
  "counts": {
    "rows": 5000,
    "context_supported": 5000,
    "equations": 115139,
    "graph_solved": 5000,
    "independent_answer_match": 5000,
    "trace_steps": 115139,
    "parallel_blocks": 8250,
    "paths": 29444,
    "summary_entries": 29444,
    "fully_passed": 5000
  },
  "error_counts": {},
  "templates": {
    "movie_festival_awards": {
      "rows": 1234,
      "context_supported": 1234,
      "independent_answer_match": 1234,
      "fully_passed": 1234
    },
    "crazy_zootopia": {
      "rows": 1231,
      "context_supported": 1231,
      "independent_answer_match": 1231,
      "fully_passed": 1231
    },
    "library_collections": {
      "rows": 1302,
      "context_supported": 1302,
      "independent_answer_match": 1302,
      "fully_passed": 1302
    },
    "teachers_in_school": {
      "rows": 1233,
      "context_supported": 1233,
      "independent_answer_match": 1233,
      "fully_passed": 1233
    }
  },
  "equation_kinds": {
    "sum": 21194,
    "mul": 29743,
    "const": 5000,
    "offset": 59202
  },
  "min_value": 1,
  "max_value": 58936,
  "limitations": [
    "Restricted grammar solver covers only the observed constant, sum, twice, integer multiplier, more/fewer relations.",
    "Entity parsing is textual normalization of known template prefixes; no independent review of natural-language realism, ontological consistency or data contamination.",
    "Dependency visibility check models sibling isolation and post-block access to Summary exports; it does not inspect actual training attention masks or inference runtime.",
    "Trace expression checks require exact operator and ordered concrete operands from independent context solution; same-valued distinct dependencies are distinguished via entity graph but numeric expressions alone cannot prove semantic intent."
  ]
}
```

</details>

- [exps/downloaded-sft-audit-20261008/realistic-semantic-report.md](../artifacts/exps/downloaded-sft-audit-20261008/realistic-semantic-report.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/runtime-fit-report.md](../artifacts/exps/downloaded-sft-audit-20261008/runtime-fit-report.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/downloaded-sft-audit-20261008/structure-report.json](../artifacts/exps/downloaded-sft-audit-20261008/structure-report.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
