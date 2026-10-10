# Selective Blocks v3

`data/sft_selective_blocks_v3_{train,val}.parquet` is v2 with one bounded
answer-only change: every `parallel_th` response is replaced by the audited
same-ID response in `data/pair_expanded_m1_frontblock.jsonl`. The v2 mixture,
row order, IDs, source labels, kinds, replay rows, and no-block controls stay
unchanged.

The frontblock source has the original 337 two-path M1 responses. For 293 it
moves the existing block immediately after `<think>`; 43 retain their
preamble because removing it would lose a numeric literal, and
`math-train/3081` retains context needed by both paths. Its review read 22
full examples plus 30 independent examples, all accepted after the `/3081`
correction. See [frontblock card](DATASET_M1_FRONTBLOCK.md).

## Composition

| split | rows | `parallel_th` replaced | no-block `control_th` | frontblock moved | frontblock retained |
| --- | ---: | ---: | ---: | ---: | ---: |
| train | 2748 | 555 | 510 | 489 | 66 |
| val | 63 | 24 | 0 | 18 | 6 |

Train retains 372 MATH and 183 GSM8K positive rows. Controls retain 252
MATH, 180 GSM8K, and 78 ARC rows. All non-positive structured records equal
their v2 counterparts.

Новых вопросов и ID нет. Совпадение каждого положительного вопроса с v2
проверено; v2, в свою очередь, использует только
[очищенный пул](DATASET_POOL.md), проверенный `dataset_survey/scripts/leakcheck.py`
против всех наших eval-наборов и полного MATH test. GSM8K dev исключён из
train в исходном пуле.

## Gates

The audit checks every positive row against v2 and the matched frontblock
source: exact prompted question, exact source answer, same tagged block, same
suffix after `</think>`, and the same numeric-literal set. `mv_format.parse`
requires one grammatical block, exactly two numbered paths, all tags inside
`<think>`, and no tags after it. Train and validation problem IDs remain
disjoint.

The matched answers and prompts were already tokenized in
`data/m1_frontblock_target_audit.json`: maximum 3838 train tokens and 3513
validation tokens, with zero rows over 4096. v3 only inserts those same
audited answers into unchanged v2 prompts.

Run:

```bash
python3 scripts/exp21/prepare_selective_blocks_v3.py
python3 scripts/exp21/audit_selective_blocks_v3.py
```

Builder report: `data/sft_selective_blocks_v3_audit.json`. Quality report:
`data/sft_selective_blocks_v3_quality.json`.

## Ручное чтение этой смеси

Дополнительно прочитал 20 полных положительных train-строк v3, выбранных
фиксированным seed 2103 поровну из GSM8K и MATH:

- GSM8K: `369`, `525`, `3019`, `4309`, `716`, `7068`, `4461`, `4779`, `6371`, `4426`.
- MATH: `965`, `2369`, `3582`, `46`, `3379`, `5223`, `2256`, `2709`, `1667`, `6286`.

У всех 20 верный итог, два различных вычисления можно выполнить независимо,
а вывод связывает их с ответом. У GSM8K `4426` пути используют длину одной
доли 8 см без явной строки `16/2=8`; она прямо следует из условия, но пример
слабее остальных по пояснению. Это чтение дополняет 22 исходных и 30
независимых проверок frontblock и 20 проверок no-block из карточки v2.
