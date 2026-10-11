# Ручное semantic review: Sol6.1-196, step 24, fixed40

Проверены `teacher_sol61_tagged_p24_step24_masked_pilot.tgz` и `teacher_sol61_plain_p24_step24_masked_pilot.tgz`: 40 идентичных GSM8K/MATH вопросов в каждой руке. Внешний ответ засчитывается только после закрытого `</think>`. Полезный блок должен быть complete numbered `<Parallel>` с двумя независимыми, верными и существенными Path, а Conclusion должна их объединять.

Машинная построчная версия: `audit/teacher_sol61_step24_semantic_manifest.json`.

## Итог

| Рука | Ручных внешне верных /40 | `acc_robust` /40 | FP/FN scorer | Начатых blocks | Полных numbered | Строго полезных | Truncation |
|---|---:|---:|---:|---:|---:|---:|---:|
| tagged | **10** | 10 | 0 / 0 | 75 попыток в 40 ответах | 0 | **0** | 3 |
| plain | **26** | 27 | 1 / 0 | 0 | 0 | **0** | 4 |

`plain` false positive: `gsm8k-train/232` содержит правильное `$9`, но только внутри незакрытого `<think>` в truncated output, поэтому внешнего ответа нет. В tagged `math-test/110` оставляет иррациональный denominator, но выражение математически эквивалентно gold и поэтому в semantic answer count засчитано; это отдельное format defect.

## Теги tagged

Ни один из 40 tagged outputs не даёт complete numbered block. Причины:

- 33/40: повторный `<Parallel>` открыт внутри ещё незакрытого `<Outline>` или другого контейнера, затем нет симметричных закрытий.
- 7/40: один outer `<Parallel>`, но обязательные `<Path>` или `<Conclusion>` пропущены либо закрыты без opening tag.
- `math-test/29` и `math-test/38`: генерация зациклилась на тысячах `</Conclusion>` и обрезана.
- `math-test/117`: три `<Parallel>` открыты, но ни один не закрыт перед truncation.

Следовательно strict useful count равен нулю в обеих руках, без субъективной оценки неполных ветвей.

## Внешние ответы и per-ID verdict

`✓` означает верный внешний ответ; `×` означает неверный, отсутствующий или находящийся только в незакрытом think. Tagged damage сокращённо: `nested` означает вложенный `<Parallel>`, `imbal.` означает несбалансированные обязательные теги, `loop` означает массовый повтор закрывающего тега.

### GSM8K_DEV

| ID | tagged final | tagged | tagged damage | plain final | plain | Примечание |
|---|---|---:|---|---|---:|---|
| gsm8k-train/43 | $25 | × | nested, imbal. | $2550 | × | Верно `$75`. |
| gsm8k-train/82 | $100 and $30 | × | imbal. | $41.67 | × | Верно `$60` за wand. |
| gsm8k-train/132 | 36 | ✓ | nested, imbal. | 36 | ✓ | |
| gsm8k-train/228 | 17 | × | imbal. | 20 | ✓ | |
| gsm8k-train/232 | 3 | × | nested, imbal. | $9 | × | Plain `$9` только внутри unclosed think/truncation. |
| gsm8k-train/235 | 9 | ✓ | nested, imbal. | 9 | ✓ | |
| gsm8k-train/260 | 10 | ✓ | nested, imbal. | 10 | ✓ | |
| gsm8k-train/278 | 20 | × | nested, imbal. | 12 | ✓ | |
| gsm8k-train/279 | $10 and $15 | × | imbal. | $10 | ✓ | |
| gsm8k-train/288 | 205 minutes | × | nested, imbal. | 6 | ✓ | Верно 360 minutes = 6 hours. |
| gsm8k-train/300 | 60 | ✓ | imbal. | 60 | ✓ | |
| gsm8k-train/317 | 4 | × | nested, imbal. | 28 | ✓ | |
| gsm8k-train/345 | 3 | ✓ | imbal. | 3 | ✓ | |
| gsm8k-train/369 | 10 | × | nested, imbal. | 13 | ✓ | |
| gsm8k-train/374 | 7.50 | × | imbal. | 9 | ✓ | |
| gsm8k-train/379 | $56,000 | ✓ | nested, imbal. | $56,000 | ✓ | |
| gsm8k-train/462 | 66 | × | imbal. | 174 | × | Верно 150 kg. |
| gsm8k-train/580 | 10 | × | nested, imbal. | 80 | ✓ | |
| gsm8k-train/653 | 7 | × | nested, imbal. | $17 | ✓ | |
| gsm8k-train/684 | 4800 | × | nested, imbal. | 2400 | ✓ | |

### MATH_DEV

| ID | tagged final | tagged | tagged damage | plain final | plain | Примечание |
|---|---|---:|---|---|---:|---|
| math-test/9 | 1/2 | × | nested, imbal. | 1/3 | × | Верно `-1/8`. |
| math-test/29 | missing | × | nested, loop, trunc. | 12 | × | Largest `b=16`. |
| math-test/36 | `(-√5,√5)` | × | nested, imbal. | `(-√3,√3)` | ✓ | |
| math-test/38 | missing | × | nested, loop, trunc. | 24 | × | Maximum `y=49`. |
| math-test/45 | 6 | × | nested, imbal. | `6+9i` | ✓ | |
| math-test/51 | expression, not value | × | nested, imbal. | missing | × | Верно `0`; plain truncated. |
| math-test/53 | 7/2 | ✓ | nested, imbal. | 7/2 | ✓ | |
| math-test/65 | 6 | ✓ | nested, imbal. | 6 | ✓ | |
| math-test/71 | 24 | × | nested, imbal. | 60 | × | Верно 20. |
| math-test/87 | 4 | × | nested, imbal. | -5 | ✓ | |
| math-test/88 | 1.2 | × | nested, imbal. | 2 | ✓ | |
| math-test/93 | 7.5 | × | nested, imbal. | 5 | ✓ | |
| math-test/98 | `(5,7)` | × | nested, imbal. | `(5,7)` | × | Исключается `(9,11)`. |
| math-test/103 | `2x(15x²-4x+10)` | ✓ | nested, imbal. | same | ✓ | |
| math-test/108 | 12 | × | nested, imbal. | 18 | ✓ | |
| math-test/110 | `1/(2√7)` | ✓* | nested, imbal. | `√7/14` | ✓ | `*` эквивалентно gold, denominator не rationalized. |
| math-test/117 | missing | × | nested, unfinished trunc. | missing | × | Верно `(2,12)`. |
| math-test/129 | 1004 | × | nested, imbal. | missing | × | Верно `2009/4`; plain truncated. |
| math-test/130 | 14 | × | nested, imbal. | 12 | × | Верно `-22`. |
| math-test/137 | 10 | × | nested, imbal. | 3 | × | Верно 1. |

## Вывод

У teacher Sol6.1 tagged step24 нет сохранённой синтаксически пригодной структуры. Падение внешней точности с plain 26/40 до tagged 10/40 сопровождается 40/40 malformed attempts, поэтому результат не пригоден для отбора по strict useful blocks. Plain сохраняет 26 внешних ответов при отсутствии protocol blocks; один score false positive вызван завершением генерации до `</think>`.
