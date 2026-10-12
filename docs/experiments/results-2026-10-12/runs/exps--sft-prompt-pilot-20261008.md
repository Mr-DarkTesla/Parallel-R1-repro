# exps/sft-prompt-pilot-20261008

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/sft-prompt-pilot-20261008/manifest.json](../artifacts/exps/sft-prompt-pilot-20261008/manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "gpt-6-luna",
  "reasoning_effort": "high",
  "method": "fresh subagents fork_turns=none; read designated input and write response only; no math tools or reference access",
  "prompt_v1_sha256": "665055f4fd357ea93913d973b0b3c764357e393423a6d9f447a3b02f8506b11c",
  "tasks": [
    "math_3722",
    "math_2110",
    "math_2156",
    "math_5292",
    "math_6949",
    "simple_control"
  ],
  "scope": "qualitative prompt pilot; no training and no DeepSeek run; no claim of heldout evaluation or benchmark accuracy",
  "completed_outputs": 20,
  "versions": {
    "v1": {
      "sha256": "665055f4fd357ea93913d973b0b3c764357e393423a6d9f447a3b02f8506b11c",
      "n": 8
    },
    "v2": {
      "sha256": "f6a595b739637918f3d57fe29e552afff54e1a30a034283ce0c08d124e147ed1",
      "n": 8
    },
    "v3": {
      "sha256": "6bc038f3b0f0005bc3865ce3150b0e629b0ab7ab49637e2c6602e196aad900ff",
      "n": 4
    }
  },
  "task_selection": "First six: five hand-picked MATH train Level 5 questions and one constructed simple control. After examining v1, add two constructed classification/extremum diagnostics. v3 reruns four deliberately selected tasks; not the full suite.",
  "repetitions": "one fresh generation per task/version; seeds unavailable; not a statistical comparison",
  "date_local": "2026-10-08 Europe/Moscow",
  "reference_access": "generator inputs contain problem and prompt only; references and other files prohibited by wrapper",
  "artifact_scope": "prompt development diagnostics, not training data; no full train/test decontamination claimed",
  "decision": "v2 retained as a provisional prompt candidate; v3 not selected because observed local-correctness and final-answer regressions. No version demonstrates widths >=4 or depth >=3."
}
```

</details>

- [exps/sft-prompt-pilot-20261008/prompt-v1.txt](../artifacts/exps/sft-prompt-pilot-20261008/prompt-v1.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/sft-prompt-pilot-20261008/prompt-v2.txt](../artifacts/exps/sft-prompt-pilot-20261008/prompt-v2.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/sft-prompt-pilot-20261008/prompt-v3.txt](../artifacts/exps/sft-prompt-pilot-20261008/prompt-v3.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/sft-prompt-pilot-20261008/prompt-v4-counted-forks.txt](../artifacts/exps/sft-prompt-pilot-20261008/prompt-v4-counted-forks.txt) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
