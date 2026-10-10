# Selective Blocks v2

`data/sft_selective_blocks_v2_train.parquet` is the second selective-block SFT
variant.  It starts from `sft_selective_blocks_m1_text1_train.parquet`; the
validation rows are unchanged from v1 in `sft_selective_blocks_v2_val.parquet`.
Training has 2,748 rows and validation has 63.

The Multiverse prompt remains present for every no-block example.  Each
`control_th` answer is the exact Qwen response from `data/replay_th.jsonl`,
with one `<think>...</think>` pair and no Multiverse tags.  These examples teach
the model that an atomic problem needs no parallel block.

## Composition

| group | selected IDs | copies per ID | control rows |
| --- | ---: | ---: | ---: |
| ARC, v1 retained | 26 | 3 | 78 |
| MATH, v1 retained plus 2023 and 6378 | 14 | 18 | 252 |
| GSM8K, newly screened | 10 | 18 | 180 |
| total no-block Multiverse rows | 50 | | 510 |

The 360 added MATH/GSM8K controls replace 360 `parallel_th` rows in whole
three-copy groups of the same source and answer type.  Thus source and answer
type counts remain equal to v1.  v2 has 555 positive `parallel_th` rows:
372 MATH and 183 GSM8K.  Training row count, validation IDs, replay mixture,
and existing scheduling/LR choices remain comparable to v1.

`gsm8k-train/4824` passed trace-quality screening but is excluded by design.

## Review provenance

Previously independently reviewed examples are the 12 v1 MATH and 26 v1 ARC
IDs.  The 12 newly selected IDs are MATH `2023`, `6378` and GSM8K `2098`,
`2221`, `2334`, `2587`, `2793`, `3663`, `4765`, `4952`, `6932`, `7415`.
Their trace-quality evidence is in
`audit/think_trace_sol/qwen_trace_quality.jsonl`; independent no-split screens
are in `audit/qwen_trace_screen/screen_a.jsonl`, `screen_b.jsonl`, and
`screen_c.jsonl`.

Every selected question is matched exactly against the prior leakchecked
`data/pool.jsonl`; see [pool card](DATASET_POOL.md). Builder decisions are recorded
in `data/sft_selective_blocks_v2_audit.json`; local integrity checks are in
`data/sft_selective_blocks_v2_quality.json`.

## Проверка полных трасс

Я прочитал 20 ответов этой смеси: все 12 новых MATH/GSM8K и 8 прежних
(MATH `5901`, `6060`, `5361`, `7243`; ARC `MCAS_2005_5_36`,
`Mercury_401315`, `Mercury_7228498`, `MDSA_2009_5_46`). Существенных ошибок
в рассуждениях и финалах не нашёл. У `math-train/2023` Qwen также показывает
другой способ вычисления того же выражения; отдельных независимых частей
задачи нет, поэтому пример оставлен без блока. Новые 24 MATH/GSM8K задачи
повторяются по 18 раз. Это сильное переутяжеление, и его обобщение следует
проверять на отложенном пилоте.
