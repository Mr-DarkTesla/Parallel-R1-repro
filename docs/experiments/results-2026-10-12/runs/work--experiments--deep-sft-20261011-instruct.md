# work/experiments/deep-sft-20261011-instruct

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/deep-sft-20261011-instruct/production-v2/seed-manifest.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v2/seed-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "original_tasks": 128,
  "seed_accepted": 124,
  "seed_rejected": 4,
  "exclusions": {
    "synthetic-layered-dag-v1/2026104114": "Independent substantive review: stage prose update count off by one."
  },
  "teacher_calls": 0,
  "hashes": {
    "work/experiments/deep-sft-20261011-instruct/production/journal.jsonl": "23fbe11cdca5793ec7b56a3dbc673165da660dcb07b11429eda7b2dbfff50a98",
    "work/experiments/deep-sft-20261011-instruct/production/teacher-responses.jsonl": "fcab447aec77d48ce5af7dad1ba017c1f5efa761c16e3529178ab3738bc2f2f3",
    "work/experiments/deep-sft-20261011-instruct/first128-rechecked/receipts.jsonl": "5743b1ea9d9279b0e40bfafa726cc0789b8bcd3564645321a54794df34378cc8",
    "work/experiments/deep-sft-20261011-instruct/production-v2/journal.jsonl": "3949dfe2f16491946e96c5e0eafc85d799c359d75072d6a5f8796e068f062c2c",
    "work/experiments/deep-sft-20261011-instruct/production-v2/seed-accepted.jsonl": "22955854a52613d308bae8f4ce63e8e82e748ecc8a931dd8a20951776cccf85d"
  },
  "status": "staged no new teacher requests"
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v3/data-manifest.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v3/data-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "train": 2700,
  "val": 300,
  "split_group_disjoint": true,
  "hashes": {
    "train.jsonl": "ed40c2ae8c163ce3e2762060bd05c5d63a9c4d58b2e6e37ce329d17d35515ff8",
    "val.jsonl": "cfd9f6dd4be9e4b071ac8cdf627d0c3377e8732be7508ea9e853a660904b3b3c",
    "train.parquet": "43b86816bd6ed2c5cb623e31e604ed0444885f01c2b23d86392c8953744ef6f2",
    "val.parquet": "ad3d5e28870c2bac845a8bb6e1c3e30d743a148e32d32dc7a27650b809f8d9a7"
  }
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v3/seed-manifest.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v3/seed-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "original_tasks": 571,
  "seed_accepted": 554,
  "seed_rejected": 17,
  "new_teacher_calls": 0,
  "style_exclusions": [
    {
      "id": "synthetic-layered-dag-v1/2026107816",
      "raw_response_sha256": "778f9603591b620ca996facf55a2b0d81a13287fb09a02316e4415827d9a7cdf",
      "findings": [
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "Return only"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "[Ll]et.s final"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "[Ww]e won.t"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "[Nn]eed [\"“]"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "^\\s*\\.\\s*[\"”]"
        }
      ]
    },
    {
      "id": "synthetic-layered-dag-v1/2026101151",
      "raw_response_sha256": "d00bfa6dc40097f8ff535583ba24f4f2c511b776629ef6866129f307f72f9825",
      "findings": [
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "[Ll]et.s final"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "[Ww]e.(?:ll| will) output only"
        },
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "^\\s*\\.\\s*[\"”]"
        }
      ]
    },
    {
      "id": "synthetic-layered-dag-v1/2026105154",
      "raw_response_sha256": "819b647c4b565a9c5ca1259a93dd262f6a38d1a85a7fafabbac3ac4f78d961cb",
      "findings": [
        {
          "type": "drafting_or_parser_leak",
          "round": 1,
          "pattern": "^\\s*\\.\\s*[\"”]"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": " 2*10+14-2=32"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "2*14+4-1=31"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "3*4+10-4=18"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "3*10+10-2=38"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "3*38+31-3=114"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "31-3=142"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "3*31+18-1=93"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "18-1=110"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "3*18+32+2=54"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "32+2=88"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "2*32+38-3=64"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "38-3=99"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "1*88+99-3=184"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "2*99+110+3=198"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "110+3=311"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "2*110+142-1=220"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "142-1=361"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "2*142+88+2=284"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": "88+2=374"
        },
        {
          "type": "serial_prefork_arithmetic",
          "round": 1,
          "expression": " 184+622+722+374=1902"
        }
      ]
    }
  ],
  "hashes": {
    "work/experiments/deep-sft-20261011-instruct/production-v2/journal.jsonl": "814346b7a35fd593e2cfca33c14cac83ba7384220b296bb066f30847d5e99a4a",
    "work/experiments/deep-sft-20261011-instruct/production-v2/teacher-responses.jsonl": "f2b4ecce325eb1f3ddc65b0ff6ddee2b1344979a69ef8ab78442cfd9e40e325c",
    "work/experiments/deep-sft-20261011-instruct/production-v3/journal.jsonl": "f66b3f5b7d65edb7d891f2c65ddda05efc821c2ed308a8d101fe358af2b1564e",
    "work/experiments/deep-sft-20261011-instruct/production-v3/seed-accepted.jsonl": "a4016e0707d0b733761c64072c11f6d3a343396d55ac36099bdf42a5af6c6aa8",
    "work/experiments/deep-sft-20261011-instruct/production-v3/seed-style-exclusions.json": "7e3c7121d79853f5108ee3ce572f7c12f49b2dd04da81cac4e015a1f52ef167f"
  },
  "status": "staged root release pending; original immutable"
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/teacher-prompt-v3.txt](../artifacts/work/experiments/deep-sft-20261011-instruct/teacher-prompt-v3.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/deep-sft-20261011-instruct/teacher-prompt.txt](../artifacts/work/experiments/deep-sft-20261011-instruct/teacher-prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/deep-sft-20261011-instruct/first128-rechecked/report.json](../artifacts/work/experiments/deep-sft-20261011-instruct/first128-rechecked/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "raw_responses": 178,
  "unique_tasks": 128,
  "accepted_math_canonical": 125,
  "accepted_attempts": 157,
  "first_attempt_passed": 112,
  "failures": {
    "missing_named_stage_results": 5,
    "reference_unavailable_to_sibling": 12,
    "final_weighted_merge_unproven": 16,
    "path_without_proven_computation": 39,
    "missing_source_nodes": 3,
    "unknown_path_lhs": 12
  },
  "selected_attempts": {
    "synthetic-layered-dag-v1/2026106419": 1,
    "synthetic-layered-dag-v1/2026102780": 1,
    "synthetic-layered-dag-v1/2026103874": 1,
    "synthetic-layered-dag-v1/2026102501": 1,
    "synthetic-layered-dag-v1/2026105790": 1,
    "synthetic-layered-dag-v1/2026108115": 1,
    "synthetic-layered-dag-v1/2026101117": 1,
    "synthetic-layered-dag-v1/2026103110": 1,
    "synthetic-layered-dag-v1/2026108324": 1,
    "synthetic-layered-dag-v1/2026102846": 1,
    "synthetic-layered-dag-v1/2026102560": 1,
    "synthetic-layered-dag-v1/2026105387": 1,
    "synthetic-layered-dag-v1/2026107829": 1,
    "synthetic-layered-dag-v1/2026107059": 1,
    "synthetic-layered-dag-v1/2026103780": 1,
    "synthetic-layered-dag-v1/2026104014": 1,
    "synthetic-layered-dag-v1/2026101524": 1,
    "synthetic-layered-dag-v1/2026102133": 1,
    "synthetic-layered-dag-v1/2026104160": 1,
    "synthetic-layered-dag-v1/2026107816": 1,
    "synthetic-layered-dag-v1/2026102768": 1,
    "synthetic-layered-dag-v1/2026106611": 1,
    "synthetic-layered-dag-v1/2026105326": 1,
    "synthetic-layered-dag-v1/2026104977": 1,
    "synthetic-layered-dag-v1/2026108190": 1,
    "synthetic-layered-dag-v1/2026105248": 1,
    "synthetic-layered-dag-v1/2026106689": 1,
    "synthetic-layered-dag-v1/2026102466": 1,
    "synthetic-layered-dag-v1/2026102948": 1,
    "synthetic-layered-dag-v1/2026101664": 1,
    "synthetic-layered-dag-v1/2026104810": 1,
    "synthetic-layered-dag-v1/2026103490": 1,
    "synthetic-layered-dag-v1/2026106097": 1,
    "synthetic-layered-dag-v1/2026102679": 1,
    "synthetic-layered-dag-v1/2026103750": 1,
    "synthetic-layered-dag-v1/2026108447": 1,
    "synthetic-layered-dag-v1/2026102468": 1,
    "synthetic-layered-dag-v1/2026104049": 1,
    "synthetic-layered-dag-v1/2026107378": 1,
    "synthetic-layered-dag-v1/2026101541": 1,
    "synthetic-layered-dag-v1/2026104495": 1,
    "synthetic-layered-dag-v1/2026103151": 1,
    "synthetic-layered-dag-v1/2026106682": 1,
    "synthetic-layered-dag-v1/2026104922": 1,
    "synthetic-layered-dag-v1/2026105402": 1,
    "synthetic-layered-dag-v1/2026104056": 1,
    "synthetic-layered-dag-v1/2026105358": 1,
    "synthetic-layered-dag-v1/2026108183": 1,
    "synthetic-layered-dag-v1/2026106289": 1,
    "synthetic-layered-dag-v1/2026107490": 1,
    "synthetic-layered-dag-v1/2026101396": 1,
    "synthetic-layered-dag-v1/2026106199": 1,
    "synthetic-layered-dag-v1/2026101880": 1,
    "synthetic-layered-dag-v1/2026104114": 1,
    "synthetic-layered-dag-v1/2026105625": 1,
    "synthetic-layered-dag-v1/2026101376": 1,
    "synthetic-layered-dag-v1/2026105493": 1,
    "synthetic-layered-dag-v1/2026106933": 1,
    "synthetic-layered-dag-v1/2026103233": 1,
    "synthetic-layered-dag-v1/2026107105": 1,
    "synthetic-layered-dag-v1/2026101683": 1,
    "synthetic-layered-dag-v1/2026101946": 1,
    "synthetic-layered-dag-v1/2026105954": 1,
    "synthetic-layered-dag-v1/2026101281": 1,
    "synthetic-layered-dag-v1/2026102603": 1,
    "synthetic-layered-dag-v1/2026105806": 1,
    "synthetic-layered-dag-v1/2026106514": 1,
    "synthetic-layered-dag-v1/2026105329": 1,
    "synthetic-layered-dag-v1/2026101326": 1,
    "synthetic-layered-dag-v1/2026104472": 1,
    "synthetic-layered-dag-v1/2026103322": 1,
    "synthetic-layered-dag-v1/2026102918": 1,
    "synthetic-layered-dag-v1/2026104427": 1,
    "synthetic-layered-dag-v1/2026106707": 1,
    "synthetic-layered-dag-v1/2026104551": 1,
    "synthetic-layered-dag-v1/2026105606": 1,
    "synthetic-layered-dag-v1/2026104321": 1,
    "synthetic-layered-dag-v1/2026101979": 1,
    "synthetic-layered-dag-v1/2026105385": 1,
    "synthetic-layered-dag-v1/2026102969": 1,
    "synthetic-layered-dag-v1/2026106937": 1,
    "synthetic-layered-dag-v1/2026103979": 1,
    "synthetic-layered-dag-v1/2026106161": 1,
    "synthetic-layered-dag-v1/2026103085": 1,
    "synthetic-layered-dag-v1/2026105589": 1,
    "synthetic-layered-dag-v1/2026103239": 1,
    "synthetic-layered-dag-v1/2026103942": 1,
    "synthetic-layered-dag-v1/2026107830": 1,
    "synthetic-layered-dag-v1/2026101814": 1,
    "synthetic-layered-dag-v1/2026105503": 1,
    "synthetic-layered-dag-v1/2026107189": 1,
    "synthetic-layered-dag-v1/2026103367": 1,
    "synthetic-layered-dag-v1/2026101593": 1,
    "synthetic-layered-dag-v1/2026105928": 1,
    "synthetic-layered-dag-v1/2026103994": 1,
    "synthetic-layered-dag-v1/2026104617": 1,
    "synthetic-layered-dag-v1/2026106804": 1,
    "synthetic-layered-dag-v1/2026103729": 1,
    "synthetic-layered-dag-v1/2026108226": 1,
    "synthetic-layered-dag-v1/2026104324": 1,
    "synthetic-layered-dag-v1/2026103547": 1,
    "synthetic-layered-dag-v1/2026104159": 1,
    "synthetic-layered-dag-v1/2026105665": 1,
    "synthetic-layered-dag-v1/2026104554": 1,
    "synthetic-layered-dag-v1/2026101629": 1,
    "synthetic-layered-dag-v1/2026107912": 1,
    "synthetic-layered-dag-v1/2026103472": 1,
    "synthetic-layered-dag-v1/2026102749": 1,
    "synthetic-layered-dag-v1/2026104081": 2,
    "synthetic-layered-dag-v1/2026105179": 1,
    "synthetic-layered-dag-v1/2026105962": 1,
    "synthetic-layered-dag-v1/2026106231": 1,
    "synthetic-layered-dag-v1/2026103057": 2,
    "synthetic-layered-dag-v1/2026106054": 2,
    "synthetic-layered-dag-v1/2026107020": 2,
    "synthetic-layered-dag-v1/2026106874": 2,
    "synthetic-layered-dag-v1/2026102354": 1,
    "synthetic-layered-dag-v1/2026105165": 2,
    "synthetic-layered-dag-v1/2026103495": 2,
    "synthetic-layered-dag-v1/2026105147": 2,
    "synthetic-layered-dag-v1/2026101565": 2,
    "synthetic-layered-dag-v1/2026103534": 2,
    "synthetic-layered-dag-v1/2026101632": 2,
    "synthetic-layered-dag-v1/2026104700": 2,
    "synthetic-layered-dag-v1/2026105434": 2
  },
  "excluded_ids": [
    "synthetic-layered-dag-v1/2026104114"
  ],
  "new_teacher_calls": 0,
  "release_status": "HOLD independent substantive review required"
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/independent-review/v3-seed-reviewed-coverage.json](../artifacts/work/experiments/deep-sft-20261011-instruct/independent-review/v3-seed-reviewed-coverage.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "exact_substantive_reviewed_passes_preserved": 147,
  "note": "Earlier seed receipt counted only newer status schema (50). This supplement includes substantive_review_pass booleans in original97 receipts; all147 exactraw PASS variants are preserved.",
  "seed_manifest_sha256": "d9ed27a11ae3f03bc60834ddbaabfd928e87390ba51ba6745a559dba4095cf83",
  "seed_accepted_sha256": "a4016e0707d0b733761c64072c11f6d3a343396d55ac36099bdf42a5af6c6aa8"
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v2/drafting-prefix-findings.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v2/drafting-prefix-findings.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "scanned_accepted": 352,
  "findings": [
    {
      "id": "synthetic-layered-dag-v1/2026107816",
      "raw_response_sha256": "778f9603591b620ca996facf55a2b0d81a13287fb09a02316e4415827d9a7cdf",
      "patterns": [
        "Return only",
        "[Ll]et.s final",
        "[Ww]e won.t",
        "[Nn]eed [\"“]",
        "^\\s*\\.\\s*[\"”]"
      ],
      "prefix": ".\" We won't.\n\nNeed \"Return only worked solution.\" Yes.\n\nLet's final.Initial amounts: Alpha_0 = 12, Gamma_0 = 15, Delta_0 = 7.\n\nStage 1 updates all three stations simultaneously from the initial amounts.\n"
    },
    {
      "id": "synthetic-layered-dag-v1/2026101151",
      "raw_response_sha256": "d00bfa6dc40097f8ff535583ba24f4f2c511b776629ef6866129f307f72f9825",
      "patterns": [
        "[Ll]et.s final",
        "[Ww]e.ll output only",
        "^\\s*\\.\\s*[\"”]"
      ],
      "prefix": ".\" We'll output only.\n\nNeed maybe avoid \"I update\" first person? Fine.\n\nLet's final. \nI update Cedar, Aster, and Elm simultaneously for four stages, then combine the final amounts as 2*Cedar_4 + Aster_4 + 2*Elm_4.\n\nStage 1 establishes the three post-stage-1 amounts from the initial values.\n"
    },
    {
      "id": "synthetic-layered-dag-v1/2026105154",
      "raw_response_sha256": "819b647c4b565a9c5ca1259a93dd262f6a38d1a85a7fafabbac3ac4f78d961cb",
      "patterns": [
        "^\\s*\\.\\s*[\"”]"
      ],
      "prefix": ".\" We will output only.\n\nNeed final answer exactly last line. The final solution heading and sentence before final line. Last line \"Final Answer: \\boxed{1902}\". Good.\n\nShould we include units? Problem amounts no units. No units in box. Good.\n\nLet's ensure arithmetic:\nStage1 N1: 2*10+14-2=32. E1:2*14+4-1=31. W1:3*4+10-4=18. S1:3*10+10-2=38.\nStage2 N2:3*38+31-3=114+31-3=142. E2:3*31+18-1=93+18-1=110. W2:3*18+32+2=54+32+2=88. S2:2*32+38-3=64+38-3=99.\nStage3 N3:1*88+99-3=184. E3:2*99+110+3=198+110+3=311. W3:2*110+142-1=220+142-1=361. S3:2*142+88+2=284+88+2=374.\nFinal: 184+622+722+374=1902. Yes.\n\nNeed maybe mention \"North + 2 times East + 2 times West + South\" corresponds to N3 + 2E3 + 2W3 + S3. Good.\n\nNow final.Initial amounts are North_0 = 4, East_0 = 10, West_0 = 10, South_0 = 14; all Stage 1 updates use only these initial amounts.\nStage 1 establishes the four warehouse amounts after the first simultaneous update.\n"
    }
  ],
  "automatic_admission": false,
  "limitations": "Known drafting markers only; no proof of all unflagged prose semantics."
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v2/report.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v2/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "production",
  "completed": 571,
  "accepted": 557,
  "rejected": 14,
  "errors": {
    "independent_substantive_quarantine": 1,
    "repaired_checks_no_valid_attempt": 3,
    "source_relation_unproven": 8,
    "independent_oracle_replay": 1,
    "structure/missing_plan,missing_prefork_explanation,path_without_explicit_computation,plan_ids_or_count,unexpected_tags_between_blocks": 1
  },
  "selected_deep": 557,
  "width": {
    "mean": 4.001339285714286,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "rounds": {
    "mean": 4.021543985637343,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "width_histogram": {
    "3": 547,
    "4": 1143,
    "5": 550
  },
  "round_histogram": {
    "3": 106,
    "4": 333,
    "5": 118
  },
  "path_tokens": {
    "mean": 37.86812451188218,
    "median": 38.0,
    "p95": 42.0,
    "max": 48
  },
  "output_tokens": {
    "mean": 1314.9012567324955,
    "median": 1302.0,
    "p95": 1771.3999999999987,
    "max": 2146
  },
  "critical_path_tokens_proxy": {
    "mean": 797.439856373429,
    "median": 798.0,
    "p95": 1057.1999999999998,
    "max": 1258
  },
  "explicit_scalar_equalities_checked": 9634,
  "mathematically_reference_verified": 557,
  "no_think": false,
  "instruct_think": true,
  "all_sibling_ids_structurally_consistent": true,
  "hashes": {
    "teacher-prompt.txt": "5a3a8888c401b7df223e2b431e5c9dc1edc724fd9ce6db33a0242557e2e91cd8",
    "production-v2-protocol.json": "25683834fdd3b653b8b9f5c102815379142ebaec664a4df19dc24bf96af0dee2",
    "pool-manifest.json": "482b5f172f52a6c4ee74b871e941cd8e449a52ad2212b64fbbbedebdb3c7d7bd",
    "pilot-tasks.jsonl": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
    "journal.jsonl": "814346b7a35fd593e2cfca33c14cac83ba7384220b296bb066f30847d5e99a4a",
    "accepted.jsonl": "0f0e8e40a247e3d319457c984d2a6bcc043be303442c5700edb22c45555371fb"
  },
  "limitations": [
    "No same-teacher semantic judge; independent stratified substantive review required for final release.",
    "Explicit arithmetic checker covers flat scalar equalities only.",
    "Manual actual-trace review is mandatory before releasing production generation.",
    "F is token critical-path proxy, not measured GPU latency."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v2/status.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "stopped",
  "phase": "production",
  "started_at": 1791709689.7811913,
  "completed": 571,
  "accepted": 557,
  "target": 3000,
  "concurrency": 128,
  "decisions": {
    "accepted": 557,
    "rejected": 14
  },
  "errors": {
    "independent_substantive_quarantine": 1,
    "repaired_checks_no_valid_attempt": 3,
    "source_relation_unproven": 8,
    "independent_oracle_replay": 1,
    "structure/missing_plan,missing_prefork_explanation,path_without_explicit_computation,plan_ids_or_count,unexpected_tags_between_blocks": 1
  },
  "inflight": 0,
  "updated_at": 1791710851.0152526,
  "finished_at": 1791710851.0152493
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v3/question-replay-report.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v3/question-replay-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "checked_rows": 3000,
  "passed": 3000,
  "failures": [],
  "source_relations_recomputed": 48020,
  "oracle_source_used": false,
  "method": "Exact integer stage simulation from the original question sentences; matched to saved relation receipts and final reference.",
  "limitations": "Secondary artifact audit, not independent reviewer narrative admission; source prose grammar is restricted to this synthetic generator."
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v3/report.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v3/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "production",
  "completed": 3036,
  "accepted": 3000,
  "rejected": 36,
  "errors": {
    "independent_substantive_quarantine": 1,
    "drafting_or_serial_prefork_quarantine": 3,
    "repaired_checks_no_valid_attempt": 3,
    "source_relation_unproven": 24,
    "independent_oracle_replay": 4,
    "structure/missing_plan,missing_prefork_explanation,path_without_explicit_computation,plan_ids_or_count,unexpected_tags_between_blocks": 1
  },
  "selected_deep": 3000,
  "width": {
    "mean": 4.0009998333611065,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "rounds": {
    "mean": 4.000666666666667,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "width_histogram": {
    "3": 2954,
    "4": 6082,
    "5": 2966
  },
  "round_histogram": {
    "3": 602,
    "4": 1794,
    "5": 604
  },
  "path_tokens": {
    "mean": 37.90558100791337,
    "median": 38.0,
    "p95": 42.0,
    "max": 53
  },
  "output_tokens": {
    "mean": 1307.325,
    "median": 1296.0,
    "p95": 1776.2999999999984,
    "max": 2206
  },
  "critical_path_tokens_proxy": {
    "mean": 791.881,
    "median": 786.5,
    "p95": 1053.0499999999997,
    "max": 1304
  },
  "explicit_scalar_equalities_checked": 51503,
  "mathematically_reference_verified": 3000,
  "no_think": false,
  "instruct_think": true,
  "all_sibling_ids_structurally_consistent": true,
  "hashes": {
    "teacher-prompt-v3.txt": "6c5c369539f00ac1c017f92a5421d1654f65477214a3a50831a68790df515955",
    "production-v3-protocol.json": "a26111e73c9dd8b5b73efd3ebf358c90ff093f2645de2c4175a668a9300dfc7b",
    "pool-manifest.json": "482b5f172f52a6c4ee74b871e941cd8e449a52ad2212b64fbbbedebdb3c7d7bd",
    "pilot-tasks.jsonl": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
    "journal.jsonl": "b6664eb9a1954007639b0508ea51f269adbbdec2a00f6e47d2b481b0b71d9ff3",
    "accepted.jsonl": "01c805f8bc20c682e091f23a11825ce989313978d8ec09c3249378d4aa0433d1"
  },
  "limitations": [
    "No same-teacher semantic judge; independent stratified substantive review required for final release.",
    "Explicit arithmetic checker covers flat scalar equalities only.",
    "Manual actual-trace review is mandatory before releasing production generation.",
    "F is token critical-path proxy, not measured GPU latency."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production-v3/status.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production-v3/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "phase": "production",
  "started_at": 1791711167.872327,
  "completed": 3036,
  "accepted": 3000,
  "target": 3000,
  "concurrency": 128,
  "decisions": {
    "accepted": 3000,
    "rejected": 36
  },
  "errors": {
    "independent_substantive_quarantine": 1,
    "drafting_or_serial_prefork_quarantine": 3,
    "repaired_checks_no_valid_attempt": 3,
    "source_relation_unproven": 24,
    "independent_oracle_replay": 4,
    "structure/missing_plan,missing_prefork_explanation,path_without_explicit_computation,plan_ids_or_count,unexpected_tags_between_blocks": 1
  },
  "inflight": 0,
  "updated_at": 1791716932.7717497,
  "finished_at": 1791716932.771741
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production/report.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "phase": "production",
  "completed": 128,
  "accepted": 98,
  "rejected": 30,
  "errors": {
    "independent_oracle_replay": 5,
    "source_relation_unproven": 25
  },
  "selected_deep": 98,
  "width": {
    "mean": 4.005154639175258,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "rounds": {
    "mean": 3.9591836734693877,
    "median": 4.0,
    "p95": 5.0,
    "max": 5
  },
  "width_histogram": {
    "3": 91,
    "4": 204,
    "5": 93
  },
  "round_histogram": {
    "3": 26,
    "4": 50,
    "5": 22
  },
  "path_tokens": {
    "mean": 37.98391248391248,
    "median": 38.0,
    "p95": 42.0,
    "max": 46
  },
  "output_tokens": {
    "mean": 1293.0102040816328,
    "median": 1292.0,
    "p95": 1799.4499999999994,
    "max": 2060
  },
  "critical_path_tokens_proxy": {
    "mean": 781.7244897959183,
    "median": 788.0,
    "p95": 1034.0499999999997,
    "max": 1217
  },
  "explicit_scalar_equalities_checked": 1651,
  "mathematically_reference_verified": 98,
  "no_think": false,
  "instruct_think": true,
  "all_sibling_ids_structurally_consistent": true,
  "hashes": {
    "teacher-prompt.txt": "5a3a8888c401b7df223e2b431e5c9dc1edc724fd9ce6db33a0242557e2e91cd8",
    "production-protocol.json": "bc8ef5e9987916074f27236e6da63f66ce62f9990afeb62b3b1b4380bda80896",
    "pool-manifest.json": "482b5f172f52a6c4ee74b871e941cd8e449a52ad2212b64fbbbedebdb3c7d7bd",
    "pilot-tasks.jsonl": "afddde5d864f47a07afe75b1c924b37c02dfb32913d4de2aad19db2a288bdefd",
    "journal.jsonl": "23fbe11cdca5793ec7b56a3dbc673165da660dcb07b11429eda7b2dbfff50a98",
    "accepted.jsonl": "c595fc4e5e5c955ef41913bdb6a8150f97aa5fb659303247671bf911105f3522"
  },
  "limitations": [
    "No same-teacher semantic judge; independent stratified substantive review required for final release.",
    "Explicit arithmetic checker covers flat scalar equalities only.",
    "Manual actual-trace review is mandatory before releasing production generation.",
    "F is token critical-path proxy, not measured GPU latency."
  ]
}
```

</details>

- [work/experiments/deep-sft-20261011-instruct/production/status.json](../artifacts/work/experiments/deep-sft-20261011-instruct/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "stopped",
  "phase": "production",
  "started_at": 1791708543.8299289,
  "completed": 128,
  "accepted": 98,
  "target": 3000,
  "concurrency": 128,
  "decisions": {
    "accepted": 98,
    "rejected": 30
  },
  "errors": {
    "independent_oracle_replay": 5,
    "source_relation_unproven": 25
  },
  "inflight": 0,
  "updated_at": 1791709530.554546,
  "finished_at": 1791709530.5545385
}
```

</details>
