# Следующий SFT: принятые agent-authored решения

## Что строит builder

`scripts/exp21/build_agent_authored_sft.py` готовит только CPU-артефакты. Он
не запускает pod, GPU, прокси или SFT.

Финальный explicit manifest уже находится в
`data/onpolicy_agent_authored_accepted78.jsonl`: он одновременно содержит
78 accepted ID и окончательные дословные output. Builder принимает JSON-массив
ID, JSONL с полем `id`, либо один ID на строку. Для JSONL accepted-строка может
содержать `{"id": "...", "verdict": "accept"}`.

Вызов также принимает optional rejected manifest или повторяемый
`--rejected-id`. Для final78 фиксированы четыре reject ID:
`gsm8k-train/5392`, `gsm8k-train/5215`, `gsm8k-train/2502`,
`gsm8k-train/5172`. Любое пересечение с accepted останавливает сборку.

В общем случае builder умеет объединять пять исходных authoring-файлов,
но для следующего SFT нужно передать именно `accepted78.jsonl` также в
`--authored`: так в tagged target попадут исправленные шесть валютных
внешних ответов, а не более ранние raw-варианты.

Для каждой принятой строки tagged-ветка сохраняет исходный output дословно.
Plain-ветка имеет те же ID, prompt и порядок; из ответа удаляются только
`Parallel`, `Goal`, `Outline`, `Conclusion` и теги Path. Тела обоих Path
остаются в исходном порядке. В обоих случаях prompt просит формат Multiverse:
это изолирует именно target-структуру, а не изменение инструкции.

## Жёсткие gates

Скрипт останавливается до записи parquet, если хотя бы один пункт не выполнен:

- accepted и rejected пересекаются;
- accepted ID отсутствует в `audit/agent_authored82/candidates.jsonl`, в
  leakchecked selection `data/onpolicy46_candidates.audit.json` или в одном
  из пяти authoring-файлов;
- менее 46 принятых решений, менее 18 GSM8K или менее шести MATH каждого
  типа: `integer`, `expression`, `fraction`;
- tagged response не содержит ровно один грамматичный, нумерованный блок с
  двумя Path внутри единственного `<think>`, либо отсутствует внешний
  `Final Answer:`;
- control/replay содержит теги, имеет неверный thinking mode, повторяет
  positive по ID или нормализованному вопросу;
- train пересекается с frozen validation по нормализованному вопросу.

Никакой текст не исправляется автоматически: builder копирует final78
verbatim. Шесть валютных GSM-ответов в final78 уже исправлены отдельным
решением; более ранние raw-варианты остаются только источником provenance.

В accepted manifest уже исключены четыре GSM rejects. Для `2502` и `5172`
независимое ревью показало, что один Path лишь повторяет заданное в вопросе
число; `5392` и `5215` исключены финальным semantic gate.

## Replay и validation provenance

Рецепт повторяет ближайшую парную абляцию Deep69:

| Часть на одну ветку | Источник | Строк |
| --- | --- | ---: |
| Agent-authored positive | explicit accepted manifest | зависит от accepted |
| `control_th` | `sft_v4_recovery8_train.parquet` | 45 |
| `replay_th` | `sft_selective_blocks_v4_train.parquet` | 71: 36 MATH, 22 GSM8K, 13 ARC |
| `replay_nt` | `sft_selective_blocks_v4_train.parquet` | 71: 36 MATH, 22 GSM8K, 13 ARC |
| Validation | `sft_v4_recovery8_val.parquet` | 63 строк, дословная копия |

Контроли и оба replay режима идентичны в tagged/plain. Выбор deterministic:
SHA-256 rank с отдельными seed для control, `replay_th`, `replay_nt` и порядка
строк; ID и нормализованные вопросы positive/control уже исключены до
выборки replay. Выходной JSON хранит ID, seed, источники, квоты, порядок и
все проверенные gates.

На final78 builder в `--dry-run` получает 265 строк на ветку:

| Positive | Число |
| --- | ---: |
| Всего | 78 |
| GSM8K | 36 |
| MATH integer / expression / fraction | 17 / 13 / 12 |
| `control_th` + replay | 45 + 71 + 71 |

Это выполняет все минимальные квоты. Финальное число должно определяться
только подписанным accepted manifest, а не этой предварительной проверкой.

## Команды

Builder можно проверить без записи так:

```bash
python3 -B scripts/exp21/build_agent_authored_sft.py \
  --accepted-ids results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_accepted78.jsonl \
  --authored results/21-qwen3-0.6b-multiverse/data/onpolicy_agent_authored_accepted78.jsonl \
  --rejected-id gsm8k-train/5392 \
  --rejected-id gsm8k-train/5215 \
  --rejected-id gsm8k-train/2502 \
  --rejected-id gsm8k-train/5172 \
  --dry-run
```

После проверки manifest тот же вызов без `--dry-run` создаст только:

```text
results/21-qwen3-0.6b-multiverse/data/sft_agent_authored_tagged_train.parquet
results/21-qwen3-0.6b-multiverse/data/sft_agent_authored_plain_train.parquet
results/21-qwen3-0.6b-multiverse/data/sft_agent_authored_val.parquet
results/21-qwen3-0.6b-multiverse/data/sft_agent_authored_build.json
```

CPU gate пройден: обе train-ветки имеют по 265 строк, validation 63;
маска и позиции проверены на pod. Парный SFT запущен 11 октября
последовательно на одной собственной H100 по рецепту Deep69:

```bash
RUN_ROOT=/tmp/exp21-selective-runs \
RUN_NAME=exp21-agent-authored-tagged-p8 \
MODEL=/checkpoints/exp21-v4-recovery8/step_8/model \
DATA_PATH=/work/exp21/agent_authored_sft/sft_agent_authored_tagged_train.parquet \
VAL_PATH=/work/exp21/agent_authored_sft/sft_agent_authored_val.parquet \
NGPUS=1 STEPS=8 SAVE_STEPS=1,2,3,4,5,6,7,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse \
  +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
```

Plain control повторяет эту команду без изменения model, steps, lr, batch,
validation или seed, меняются только `RUN_NAME` и
`DATA_PATH=.../sft_agent_authored_plain_train.parquet`. Реальный
вызов записан в `scripts/exp21/run_agent_authored_pair_pod.sh`.

После SFT каждый из восьми checkpoint каждой ветки проходит одинаковый
fixed40 masked greedy-пилот. Новый checkpoint переносится на
`/checkpoints` только если входит в
[общий TOP-5 за весь проект](CHECKPOINT_RETENTION.md#общий-top-5-проекта-11-октября)
по зафиксированному правилу, с учётом сохранённого parent recovery8.
Остальные временные веса не удалять до завершения оценки и проверки
обновлённой общей пятёрки. Полный dev и frozen не использовать для
подбора этих восьми шагов.
