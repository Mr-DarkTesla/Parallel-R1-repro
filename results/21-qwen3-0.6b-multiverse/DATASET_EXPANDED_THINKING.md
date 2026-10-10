# Расширенные M1 и M2 с блоком внутри `<think>`

10 октября 2026. По 367 разных задач на метод: прежние 187 и дополнительные 180. Методы совпадают по объёму, источнику и типу ответа: 140 GSM8K с целым ответом, 93 MATH с целым, 71 MATH с дробью, 63 MATH с выражением. Новые 180 M1 и 180 M2 взяты из [их проверенных карточек](DATASET_M1_MORE.md) и [карточки M2](DATASET_M2_MORE.md). История очистки исходных 187: [M1](DATASET_M1.md), [M2](DATASET_M2.md). Пул прошёл `leakcheck.py` против наших eval и полного MATH test; GSM8K dev исключён. Ручное чтение и независимое ревью выполнены для исходных строк до этой детерминированной перестановки тегов.

`make_thinking_m1.py` перенёс исходное решение до его последнего заголовка `Final Answer:` внутрь `<think>`, а финальный ответ оставил после `</think>`. Слова, числа и порядок исходного решения не менялись. Одна M2-строка `math-train/329` имеет заголовок `### Step 3: Final Answer`; для неё добавлен распознаватель заголовка без изменения текста. [Простой машинный протокол](data/pair_expanded_thinking_simple_audit.json): у M1 и M2 по **367/367** грамматичных нумерованных блоков внутри `<think>`, 0 тегов после него. Готовые тексты: `data/pair_expanded_{m1,m2}_thinking.jsonl`.

В каждом SFT: 367 решений по три копии, 300 верных собственных ответов Qwen no-thinking по две копии и 300 thinking по две копии. Итого 2301 строка: 2251 train, 50 validation, общий ранее закреплённый список validation ID. Новые 180 каждого метода только в train. [Проверка смеси](data/sft_expanded_th_audit.json) подтверждает одинаковое распределение M1/M2 и точное равенство текстов и порядка размеченного и контрольного плеча после удаления тегов. На подготовленном токенизаторе Qwen3 в обоих наборах максимальная длина 3837, 0/2301 больше 4096; журнал `runs/expanded-th-train-metadata.tgz` содержит `lengths.json`.

Оба размеченных SFT запущены последовательно на собственном `vcharkin-exp-vm-0` с одной H100. Post-trained Qwen3-0.6B, десять отдельно инициализированных спецтокенов, `multiverse_structure.py` с независимостью путей, `tag_lr_mult=100`, 64 шага, batch 32, micro 4, lr `1e-5`, cosine, max 4096. M1 и M2 закончили обучение 10 октября до 10:23 МСК. Финальная validation loss M1 0,304746, M2 0,176987; разница loss не является сравнением качества ответов, поскольку целевые тексты отличаются. Метаданные и журналы без весов сохранены в `runs/expanded-th-train-metadata.tgz`. Веса временно лежат на собственном pod в `/tmp/exp21-expanded-th-runs/` до завершения оценки.

Команды из корня репозитория:

```sh
/tmp/exp21-audit-venv/bin/python scripts/exp21/make_thinking_m1.py results/21-qwen3-0.6b-multiverse/data/pair_expanded_m1.jsonl results/21-qwen3-0.6b-multiverse/data/pair_expanded_m1_thinking.jsonl
/tmp/exp21-audit-venv/bin/python scripts/exp21/make_thinking_m1.py results/21-qwen3-0.6b-multiverse/data/pair_expanded_m2.jsonl results/21-qwen3-0.6b-multiverse/data/pair_expanded_m2_thinking.jsonl
/tmp/exp21-audit-venv/bin/python scripts/exp21/audit_expanded_thinking_simple.py
/tmp/exp21-audit-venv/bin/python scripts/exp21/prepare_expanded_thinking_sft.py
```

SFT на pod выполнен `run_expanded_thinking_sft_pod.sh`, оценка выполняется `run_expanded_thinking_eval_pod.sh`. Контроль на текстах без тегов будет обучен только для метода, выбранного по dev. Frozen, кроме требуемого IFEval, до выбора не открывались.
