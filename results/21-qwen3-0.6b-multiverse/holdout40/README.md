# Свежие 40 задач для masked-оценки блоков

Подготовлены 11 октября 2026 на CPU. Генерация 12 октября
в 00:18–00:27 МСК прошла на личной одной H100, PID 132409.
Все 80 ответов прочитаны независимыми рецензентами по 40 на модель.
Цель: проверить полезность независимых блоков внутри
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

Подготовленный [runner](../../../scripts/exp21/run_masked_holdout40_pod.sh)
запущен после маркера `EVAL_DONE` полной dev-оценки, проверки
свободного GPU, входных данных и моделей. Тот же один H100
последовательно оценил clean46 и mixed401: masked greedy, thinking,
2048 токенов для GSM8K и 4096 для MATH, та же маска и позиции, что
на fixed40. Маркер `EVAL_DONE` получен в 00:27:24. Новых OOM нет.

Команда запуска после проверки маркера прежнего runner, пустого GPU,
входных parquet и моделей:

```bash
kubectl -n shared-dzen-ml exec vcharkin-exp-vm-0 -- bash -lc \
  'mkdir -p /checkpoints/exp21-masked-holdout40-eval; nohup env EXP21_COMMIT=06a331b bash /tmp/exp21-eval-code/scripts/exp21/run_masked_holdout40_pod.sh > /checkpoints/exp21-masked-holdout40-eval/launch.log 2>&1 < /dev/null & echo RUNNER_PID=$!'
```

| Fresh masked dev, 20 GSM8K + 20 MATH | Clean46 | Mixed401 | Mixed401−clean46, п.п.; 95% парный ДИ |
| --- | ---: | ---: | ---: |
| Верное значение | 29/40 (72,5%) | 28/40 (70,0%) | −2,5 [−10; +5] |
| Каркас блока внутри `<think>` | 40/40 | 40/40 | 0 [0; 0] |
| Все Outline согласованы с Path, ручная проверка | 38/40 (95,0%) | 37/40 (92,5%) | −2,5 [−7,5; 0] |
| Полезные независимые пути, корректное сведение и верный итог | 12/40 (30,0%) | 7/40 (17,5%) | −12,5 [−25; 0] |
| Обрезано | 0/40 | 0/40 | 0 [0; 0] |
| Средняя длина, токены | 274,8 | 294,1 | +19,3 [+9,8; +29,4] |
| Идеальные форварды с одновременными путями | 232,5 | 252,1 | +19,7 [+9,5; +30,5] |

Парные интервалы: 10 000 bootstrap-повторов по одним и тем же 40
задачам, отдельно ресэмплированы 20 GSM8K и 20 MATH, чтобы их доли
оставались равными. Проверены идентичные ID, вопросы, запросы и порядок
двух запусков; ручной итог верных значений по каждому ID совпал с
`acc_robust`. По наборам clean46: 17/20 верных и 8/20 полезных на
GSM8K, 12/20 и 4/20 на MATH; mixed401: 17/20 и 6/20 на GSM8K,
11/20 и 1/20 на MATH. Рецензенты видели модель, поэтому разницу
полезности следует считать пилотной, тем более её ДИ достигает нуля.

Грамматический оценщик видит закрытый блок 40/40 в обеих моделях,
но не проверяет зависимость путей и истинность промежуточных шагов.
Построчные причины: [clean46](../audit/qwen4b_clean46_holdout40_semantic_review.md),
[mixed401](../audit/qwen4b_mixed401_holdout40_semantic_review.md).
Сырые ответы, оценки, журналы и метаданные сохранены в
`eval_archives/{clean46,mixed401}.tgz`; в каждом архиве проверены
20+20 строк сырых, оценённых и блочных ответов и четыре сводки.
Числовое сравнение:
[`masked_pair_summary.json`](masked_pair_summary.json),
ручное сравнение:
[`manual_pair_summary.json`](manual_pair_summary.json).
Воспроизведение: [summarize_masked_holdout40.py](../../../scripts/exp21/summarize_masked_holdout40.py)
и [compare_holdout_semantic_audits.py](../../../scripts/exp21/compare_holdout_semantic_audits.py).
Архивы можно извлечь в один временный каталог, а затем запустить:

```bash
mkdir -p /tmp/exp21-holdout40-local
tar -xzf results/21-qwen3-0.6b-multiverse/holdout40/eval_archives/clean46.tgz -C /tmp/exp21-holdout40-local
tar -xzf results/21-qwen3-0.6b-multiverse/holdout40/eval_archives/mixed401.tgz -C /tmp/exp21-holdout40-local
touch /tmp/exp21-holdout40-local/EVAL_DONE
python3 scripts/exp21/summarize_masked_holdout40.py /tmp/exp21-holdout40-local \
  results/21-qwen3-0.6b-multiverse/holdout40/masked_pair_summary.json
python3 scripts/exp21/compare_holdout_semantic_audits.py /tmp/exp21-holdout40-local \
  results/21-qwen3-0.6b-multiverse/audit/qwen4b_clean46_holdout40_semantic_review.md \
  results/21-qwen3-0.6b-multiverse/audit/qwen4b_mixed401_holdout40_semantic_review.md \
  results/21-qwen3-0.6b-multiverse/holdout40/manual_pair_summary.json
```
Первый скрипт требует локального `EVAL_DONE`, соответствующего
проверенному маркеру pod; для расчёта он не меняет ответы.

Оба лидера слабы по содержательному критерию. Обычный полный dev
clean46 не превращает 12/40 полезных блоков в успешный итог.
Следующий опыт следует выбирать по необходимости обоих путей,
отбирая собственные корректные траектории, а не по наличию тегов.
