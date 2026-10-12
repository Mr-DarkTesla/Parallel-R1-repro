# exps/epoch5-format-audit-20261005

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/epoch5-format-audit-20261005/loss-comparison.json](../artifacts/exps/epoch5-format-audit-20261005/loss-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "samples": 16,
  "note": "Teacher forcing on first 16 training samples, not generation or benchmark scores",
  "modes": {
    "sft": {
      "answer_loss": 0.5323888080184087,
      "tag_loss": 2.003948315350032,
      "tag_top1_correct": 0.4559386973180077
    },
    "prompt_positions_normal": {
      "answer_loss": 0.5554887385539556,
      "tag_loss": 2.5058534031170083,
      "tag_top1_correct": 0.32567049808429116
    },
    "ordinary_causal": {
      "answer_loss": 0.589777548056566,
      "tag_loss": 2.65817570412296,
      "tag_top1_correct": 0.32950191570881227
    }
  }
}
```

</details>

- [exps/epoch5-format-audit-20261005/summary.json](../artifacts/exps/epoch5-format-audit-20261005/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "base": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 0,
      "author_valid": 1916,
      "strict_balanced": 1916,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 0,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 0
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 0,
      "author_valid": 480,
      "strict_balanced": 480,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 0,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 0
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 0,
      "author_valid": 640,
      "strict_balanced": 640,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 0,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 0
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 0,
      "author_valid": 480,
      "strict_balanced": 480,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 0,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 0
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 0,
      "author_valid": 316,
      "strict_balanced": 316,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 0,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 0
    }
  },
  "epoch-1": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 55,
      "author_valid": 1662,
      "strict_balanced": 1595,
      "strict_balanced_with_parallel": 28,
      "malformed_before_end": 318,
      "unfinished_without_earlier_error": 3,
      "malformed_before_first_parallel": 5
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 17,
      "author_valid": 404,
      "strict_balanced": 386,
      "strict_balanced_with_parallel": 11,
      "malformed_before_end": 93,
      "unfinished_without_earlier_error": 1,
      "malformed_before_first_parallel": 1
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 16,
      "author_valid": 551,
      "strict_balanced": 528,
      "strict_balanced_with_parallel": 8,
      "malformed_before_end": 111,
      "unfinished_without_earlier_error": 1,
      "malformed_before_first_parallel": 1
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 17,
      "author_valid": 425,
      "strict_balanced": 410,
      "strict_balanced_with_parallel": 8,
      "malformed_before_end": 70,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 2
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 5,
      "author_valid": 282,
      "strict_balanced": 271,
      "strict_balanced_with_parallel": 1,
      "malformed_before_end": 44,
      "unfinished_without_earlier_error": 1,
      "malformed_before_first_parallel": 1
    }
  },
  "epoch-2": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 506,
      "author_valid": 443,
      "strict_balanced": 312,
      "strict_balanced_with_parallel": 30,
      "malformed_before_end": 1604,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 258
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 113,
      "author_valid": 123,
      "strict_balanced": 93,
      "strict_balanced_with_parallel": 7,
      "malformed_before_end": 387,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 61
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 176,
      "author_valid": 137,
      "strict_balanced": 90,
      "strict_balanced_with_parallel": 6,
      "malformed_before_end": 550,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 95
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 130,
      "author_valid": 120,
      "strict_balanced": 90,
      "strict_balanced_with_parallel": 11,
      "malformed_before_end": 390,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 58
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 87,
      "author_valid": 63,
      "strict_balanced": 39,
      "strict_balanced_with_parallel": 6,
      "malformed_before_end": 277,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 44
    }
  },
  "epoch-3": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 1065,
      "author_valid": 47,
      "strict_balanced": 29,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 1887,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 760
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 281,
      "author_valid": 13,
      "strict_balanced": 8,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 472,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 201
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 370,
      "author_valid": 15,
      "strict_balanced": 10,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 630,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 254
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 247,
      "author_valid": 12,
      "strict_balanced": 8,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 472,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 181
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 167,
      "author_valid": 7,
      "strict_balanced": 3,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 313,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 124
    }
  },
  "epoch-4": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 1178,
      "author_valid": 37,
      "strict_balanced": 25,
      "strict_balanced_with_parallel": 1,
      "malformed_before_end": 1891,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 892
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 299,
      "author_valid": 12,
      "strict_balanced": 9,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 471,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 224
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 381,
      "author_valid": 10,
      "strict_balanced": 7,
      "strict_balanced_with_parallel": 1,
      "malformed_before_end": 633,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 300
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 305,
      "author_valid": 11,
      "strict_balanced": 7,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 473,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 228
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 193,
      "author_valid": 4,
      "strict_balanced": 2,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 314,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 140
    }
  },
  "epoch-5": {
    "ALL": {
      "answers": 1916,
      "has_parallel": 1136,
      "author_valid": 67,
      "strict_balanced": 55,
      "strict_balanced_with_parallel": 1,
      "malformed_before_end": 1861,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 815,
      "reached_3000": 16,
      "eos_present": 1899,
      "malformed_and_short": 1849,
      "first_error_within_500_tokens": 1771
    },
    "APO_AIME25": {
      "answers": 480,
      "has_parallel": 270,
      "author_valid": 18,
      "strict_balanced": 16,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 464,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 180,
      "reached_3000": 6,
      "eos_present": 473,
      "malformed_and_short": 460,
      "first_error_within_500_tokens": 424
    },
    "APO_AMC23": {
      "answers": 640,
      "has_parallel": 395,
      "author_valid": 18,
      "strict_balanced": 14,
      "strict_balanced_with_parallel": 1,
      "malformed_before_end": 626,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 287,
      "reached_3000": 3,
      "eos_present": 637,
      "malformed_and_short": 623,
      "first_error_within_500_tokens": 603
    },
    "APO_AIME24": {
      "answers": 480,
      "has_parallel": 272,
      "author_valid": 23,
      "strict_balanced": 18,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 462,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 202,
      "reached_3000": 5,
      "eos_present": 475,
      "malformed_and_short": 458,
      "first_error_within_500_tokens": 439
    },
    "APO_MATH300": {
      "answers": 316,
      "has_parallel": 199,
      "author_valid": 8,
      "strict_balanced": 7,
      "strict_balanced_with_parallel": 0,
      "malformed_before_end": 309,
      "unfinished_without_earlier_error": 0,
      "malformed_before_first_parallel": 146,
      "reached_3000": 2,
      "eos_present": 314,
      "malformed_and_short": 308,
      "first_error_within_500_tokens": 305
    }
  },
  "training_data": {
    "answers": 5910,
    "has_parallel": 5895,
    "strict_balanced": 5894,
    "author_valid": 5910
  }
}
```

</details>
