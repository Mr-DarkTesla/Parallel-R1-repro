# Sol 6.1 teacher SFT pair

Статус: CPU builder и pod launcher подготовлены. Обучение не запускалось.

## Входной контракт

Builder принимает либо готовый JSONL accepted trajectories, либо converter
proposals вместе с независимыми screen JSONL. Второй вариант соответствует
текущим файлам: screen rows содержат `id` и `verdict: accept|reject`, а
proposal содержит `response`, `question`, `teacher: sol61` и `teacher_source`.
Сам `proposal_not_accepted` без screen решения не может попасть в SFT.

Каждая строка проходит grammar и provenance gates: Sol 6.1 source, чистый
leakcheck, один Parallel block внутри `<think>`, не менее двух Paths и внешний
`Final Answer:`. Plain arm убирает только container/plan markup и сохраняет
Path bodies в исходном порядке. Default minimum: 150 accepted IDs. Поднимать
его можно через `--min-accepted`; уменьшение меняет размер эксперимента.

## CPU build после готового converter output

Выполнять из корня репозитория после появления
`results/21-qwen3-0.6b-multiverse/data/teacher_parallel_accepted.jsonl`:

```bash
python3 -B scripts/exp21/build_teacher_sft.py \
  --accepted results/21-qwen3-0.6b-multiverse/data/teacher_parallel_accepted.jsonl \
  --out-prefix results/21-qwen3-0.6b-multiverse/data/sft_teacher
```

Если converter сохраняет proposals, а review остаётся в отдельных screen
файлах, использовать:

```bash
python3 -B scripts/exp21/build_teacher_sft.py \
  --proposals results/21-qwen3-0.6b-multiverse/data/teacher_parallel_proposals.jsonl \
  --screens results/21-qwen3-0.6b-multiverse/audit/teacher_screen_first102.jsonl \
            results/21-qwen3-0.6b-multiverse/audit/teacher_screen_last101.jsonl \
  --out-prefix results/21-qwen3-0.6b-multiverse/data/sft_teacher
```

`--dry-run` не создаёт Parquet и печатает accepted count, deterministic replay
IDs, final row order и overlap gates. Текущий converter output содержит 66
proposals, поэтому default gate 150 намеренно останавливает build до появления
расширенного accepted converter output.

## Pod launcher

После CPU build скопировать четыре артефакта `sft_teacher_*` на PVC в
`/work/exp21/teacher_sft/`. Launcher использует parent
`/checkpoints/exp21-v4-recovery8/step_8/model` и запускает оба arm одинаково:
8 steps, `LR=3e-6`, `BATCH=32`, `MICRO_BATCH=4`, `MAX_LENGTH=4096`,
`optim.tag_lr_mult=100`.

```bash
bash scripts/exp21/run_teacher_pair_pod.sh
```

До GPU launcher сверяет prepared report, accepted minimum, одинаковые
order/prompts, identical replay, 63-row frozen validation и replay composition.
