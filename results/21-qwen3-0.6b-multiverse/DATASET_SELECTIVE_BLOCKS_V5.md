# Selective Blocks v5: diverse original merge

`data/sft_selective_blocks_v5_{train,val}.parquet` расширяет positive-часть
v2 до всех 305 исходных train-ID v1. Не-positive train-строки v2 сохранены
точно: 879 `replay_nt`, 804 `replay_th` и 510 `control_th`. Validation из 63
строк полностью равен v2.

Positive-ответы взяты из `data/pair_expanded_m1_two_paths.jsonl`, то есть это
исходный вариант: итоговое объединение остаётся после `</Parallel>` и до
`</think>`. Это не v4 и не `pair_expanded_m1_merge_inside.jsonl`.

| source | distinct train ID | copies per ID | positive rows |
| --- | ---: | --- | ---: |
| MATH | 184 | 180 по 2, 4 по 3 | 372 |
| GSM8K | 121 | 59 по 1, 62 по 2 | 183 |
| total | 305 | | 555 |

Третьи копии MATH и вторые копии GSM8K выбраны детерминированно из всех
исходных ID, seeds 21071 и 21072; перемешивание train использует seed 21073.
Полные списки ID и параметры записаны в `data/sft_selective_blocks_v5_audit.json`.

## Проверки

`audit_selective_blocks_v5.py` проверяет точное мультимножество не-positive
строк v2, неизменный validation, все 305 train positive ID, распределение
копий, раздельность train/validation ID и точные prompted ответы исходного
two-path источника. Все 579 positive train+validation строк имеют один
грамматичный блок внутри `<think>`, два нумерованных `<Path>`, ноль тегов вне
`<think>`, непустое объединение после `</Parallel>` и поле ответа, совпадающее
с `pool.jsonl`.

Проверка лимита наследуется от `data/m1_twopath_target_audit.json`: positive
prompts и answers совпадают с уже токенизированным источником. Максимум 3 838
train-токенов и 3 513 validation-токенов, строк длиннее 4 096 нет. Вопросы
берутся только из v1, который использует очищенный и ранее leakchecked
`data/pool.jsonl`; см. `DATASET_POOL.md`.

Результаты: `data/sft_selective_blocks_v5_audit.json` и
`data/sft_selective_blocks_v5_quality.json`.

## Ручное чтение

Прочитаны 20 разных positive train-ID: 10 GSM8K, seed 21074, и 10 MATH, seed
21075. Во всех 20 оба пути используют данные условия, вычисления и итог верны,
а объединение находится после закрытия блока, как задано v5. У
`gsm8k-train/4426` вычисление длины одной доли 8 см находится во вступлении,
но оба Path вычисляют разные части только из этого общего условия.

- GSM8K: `5854`, `3718`, `7023`, `4426`, `4661`, `2761`, `6725`, `3947`, `5338`, `1265`.
- MATH: `1874`, `5565`, `558`, `6225`, `5124`, `1536`, `5408`, `1038`, `5494`, `3187`.

## Независимое ревью

Другой исполнитель прочитал ещё 30 distinct train-ID: 15 GSM8K и 15 MATH,
детерминированная выборка по SHA-256 от ID. Все **30/30** блоков полезны:
два содержательных независимых Path выполняют новую работу, итоговая
операция стоит после `</Parallel>` внутри `<think>`. Неверных финальных
ответов **0/30**; `checks.py` против эталонов пула не нашёл замечаний.

GSM8K ID: `4045`, `4955`, `5854`, `2947`, `2710`, `596`, `456`, `5524`,
`5081`, `5185`, `2928`, `4461`, `5338`, `7068`, `7053`.
MATH ID: `3158`, `6225`, `6210`, `3582`, `2172`, `399`, `6099`, `271`,
`558`, `1552`, `1642`, `2268`, `4396`, `5871`, `6286`.

Run:

```bash
python3 scripts/exp21/prepare_selective_blocks_v5.py
python3 scripts/exp21/audit_selective_blocks_v5.py
```
