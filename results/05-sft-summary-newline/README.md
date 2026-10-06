# 05: канонический разрыв `</Parallel>\n<Summary>` в SFT-данных

Отличие от 02: в 2062 из 5910 ответов разрыв между `</Parallel>` и `<Summary>` приведён к одному `\n`, как его вставляет роллаут
(`scripts/normalize_summary_gap.py`). Запуск: `bash scripts/run_experiment.sh 05-sft-summary-newline data.train_files=<...>/train_summary_newline.parquet`.

Результат: эффекта нет. Парное сравнение с 02r по 1233 задачам: −0.10 пункта, 95% CI [−1.47, 1.25]. Доля правильных тегов 86.6% против 88.2%.
