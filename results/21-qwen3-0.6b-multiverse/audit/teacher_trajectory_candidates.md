# Teacher trajectory candidates

Статус: **candidate_manifest_only**. Это 203 кандидатов для
последующей разметки. Они не приняты в SFT, не содержат `<Parallel>` и не
должны попадать в обучение без отдельной проверки качества и разметки путей.

## Источник

Из трёх сохранённых партий Sol 6.1 взяты только raw thinking-трейсы, чьи ID
вошли в final full-review списка соответствующей партии. Для каждого ID
проверены answer-precheck, принадлежность очищенному `pool.jsonl`, один
`<think>`, внешний `Final Answer:`, отсутствие Parallel-тегов и минимум 200
символов reasoning.

| Партия | Full-review ID | Raw candidates |
| --- | ---: | ---: |
| `sol61_next80` | 68 | 68 |
| `sol61_next120` | 104 | 104 |
| `sol61_noninteger60` | 31 | 31 |

Текущий `onpolicy_agent_authored_accepted78.jsonl` исключён полностью:
0 пересечений. Это защищает новую
очередь от повторного использования current accepted78.

## Leakage provenance

Все три исходные партии имеют `leakcheck.py` summary с нулём для наших eval,
точных дублей и вариантов eval. Глобальная повторная проверка очищенного pool
также сообщает 0 eval leak pairs, 0 MATH-test dup/variant и 0 exact prompt
duplicates. Final full-review списки применяют уже принятые ручные исключения
слабых MATH-test сигналов; extractor не использует более широкие raw партии.

## Состав

| Answer type | Кандидатов |
| --- | ---: |
| `expression` | 46 |
| `fraction` | 52 |
| `integer` | 105 |

- MATH: 127
- GSM8K: 76
- Thinking chars: min 225, median 368, max 639
- Correct-answer provenance: 203/203
- Raw tag-free thinking: 203/203

## Reproduction

```bash
python3 -B scripts/exp21/extract_teacher_trajectories.py
```

Скрипт CPU-only и не выполняет GPU, прокси, сетевые или платные вызовы.
