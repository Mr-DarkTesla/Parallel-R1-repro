# Screened Sol 6.1 teacher trajectories

Статус: **screened_not_accepted**. Ноль строк объявлены принятыми в SFT.
Скрипт сохраняет только строки с `verdict=accept` в обеих точных screen
частях, с распознанной allowlist-группировкой и с подтверждённым `math_verify`
внешним ответом. Он не запускает GPU, proxy или сеть.

## Результат

- candidates: 203
- first102: 102; last101: 101
- screen accept: 201; screen reject: 2
- explicit denylist: 3
- screened rows: 198
- math_verify: available; verified rows: 196
- output rows: 196

Каждый output row имеет `status=screened_not_accepted` и
`answer_verification=verified_math_verify`. Неудачная или недоступная проверка
ответа остаётся причиной пропуска, а не основанием объявить строку принятой.

## Exact reconstruction

Для каждой output строки проверено байтовое равенство исходного `raw_response`
и результата после удаления только добавленных `Goal`/`Outline`, тегов и
обязательных `N:` в `Path`. Исходные символы, формулы, переносы и внешний
`Final Answer:` сохранены; Parallel block целиком находится в `<think>`.

## Пропуски

| ID | Причина |
| --- | --- |
| `gsm8k-train/1130` | gsm8k-train/1130: screen grouping is not in exact convertible allowlist |
| `gsm8k-train/1358` | explicit denylist |
| `gsm8k-train/1551` | screen verdict reject |
| `gsm8k-train/660` | gsm8k-train/660: screen grouping is not in exact convertible allowlist |
| `math-train/1553` | explicit denylist |
| `math-train/2234` | screen verdict reject |
| `math-train/92` | explicit denylist |

## Reproduction

```bash
/tmp/exp21-audit-venv/bin/python -B scripts/exp21/convert_teacher_trajectories.py
```
