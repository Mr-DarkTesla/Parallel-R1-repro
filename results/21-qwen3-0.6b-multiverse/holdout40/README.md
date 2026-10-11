# Свежие 40 задач для masked-оценки блоков

Подготовлены 11 октября 2026 на CPU; генерация и ручное ревью ещё не
начинались. Цель: проверить полезность независимых блоков внутри
`<think>` вне fixed40, который уже много раз использовался для отбора
чекпоинтов. Это dev, не frozen.

Источник: `/work/bench_data/instruct4b/eval/dev/plain/{gsm8k_dev,math_dev}.parquet`
на личном pod. В каждом наборе выбраны по 20 уникальных задач: GSM8K
из 296, MATH из 482. Повторные строки одной задачи сведены к одной.
Использован тот же текст Multiverse-инструкции, что на fixed40;
остальные поля исходной строки сохранены. Выбор воспроизводимый:
алфавитная сортировка ID, `random.Random(21)` для GSM8K и `(22)`
для MATH. Точные ID в [манифесте](manifest.json).

Исключены все 40 задач fixed40 по ID и тексту, затем задачи из двух
train-наборов по ID и тексту: 4B mixed401 и clean46. После этого
оставались 263 задачи GSM8K и 462 MATH. У mixed401 нашлось 12
совпадающих сырых GSM8K ID, у clean46 ещё четыре; ни в одном случае
тексты вопросов не совпадали. Из этих ID девять для mixed401 и четыре
для clean46 находятся вне fixed40; они всё равно исключены.
Совпадающих текстов с обоими train-наборами нет. Выбранные 40 задач
не пересекаются с ними ни по ID, ни по нормализованному тексту.

Команда подготовки на pod, без GPU:

```bash
/work/venv/bin/python /tmp/exp21-eval-code/scripts/exp21/build_masked_holdout40.py \
  /work/bench_data/instruct4b/eval/dev/plain \
  /work/exp21/masked_pilot \
  /checkpoints/exp21-masked-holdout40 \
  --train /work/exp21/qwen4b_mixed401/tagged_train.parquet \
  --train /work/exp21/qwen4b_clean46/tagged_train.parquet
```

Скрипт: [build_masked_holdout40.py](../../../scripts/exp21/build_masked_holdout40.py).
Файлы `gsm8k_holdout20.parquet` и `math_holdout20.parquet` прочитаны
после записи: по 20 строк и по 20 уникальных ID. Подготовка не
использовала GPU и не меняла текущую полную dev-оценку.
