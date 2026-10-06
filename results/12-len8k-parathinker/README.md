# 12: GSM8K + ParaThinker в SFT, лимиты 8192

Отличие от 11: к 5910 примерам GSM8K добавлены 1633 примера из ParaThinker (`Leslie04/parathinker-math-6K`), микробатч 1 вместо 4 (с микробатчем 2 первый шаг упал с CUDA OOM на fp32 cross-entropy),
маска внимания передаётся из датасета как bool и превращается в float на GPU (`docs/changes.md`, п. 5).
Запуск: `bash scripts/run_experiment.sh 12-len8k-parathinker data.train_files=/work/assets/parathinker/train_mix.parquet data.micro_batch_size_per_gpu=1`.

Данные (`scripts/make_parathinker_sft.py`). Пример ParaThinker — 2-6 независимых полных решений задачи и шаблонный summary с ответом.
Берём два самых коротких законченных решения с ответом summary и пишем один блок в начале ответа:
`<Parallel><Path>a</Path><Path>b</Path></Parallel>\n<Summary>Both paths give X.</Summary>\n\nFinal Answer: X`.
Из 5949 примеров: 2559 без двух законченных решений с ответом summary (40% решений в данных обрезаны на середине),
1204 с задачей из eval-наборов (общий фрагмент из 13 слов с LIMO, MATH300, AIME, AMC23 или GSM8K test), 553 длиннее 8192 токенов,
осталось 1633. Длина примера ParaThinker: медиана 5253 токена, 90% — 7452. Parquet не в репозитории (у датасета нет лицензии):
`/work/assets/parathinker/train_mix.parquet` на PVC.

Ожидания и оговорки: в отличие от GSM8K-данных здесь ветвление всегда в начале и пути — целые решения, а не шаги;
summary не синтезирует пути. Выбор самых коротких решений смещает выборку к более лёгким задачам. Микробатч и bool-маска
не меняют целевую функцию: лосс — среднее по токенам внутри примера, затем по примерам; float-маска совпадает побитово.
