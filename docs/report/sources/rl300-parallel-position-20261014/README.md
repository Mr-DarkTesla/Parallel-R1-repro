# Начало parallel-блока: первые 300 итераций

Метрика [Figure 3, раздел 4.4](https://arxiv.org/html/2509.07980#S4.SS4):
нулевой индекс токена `<Parallel>` / длина `response_ids`.
Среднее по всем блокам, независимо от правильности и формата ответа.
Prompt/padding исключены; видимые токены сборки веток включены.
Ответы без `<Parallel>` исключены из среднего. Усечённые ответы включены.

Цепочка источников подтверждена конфигурациями `initial_checkpoint`:

- 1–50: `rl-r2-24gpu-20261012/recovery-20261012-global-parity/production`,
  96 ответов/update, 4800 ответов, 4743 блока.
- 51–300: `rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory/production`,
  продолжение от checkpoint50 с новым Adam, 64 ответа/update,
  16000 ответов, 15907 блоков.
- Общий серверный корень: `${PROJECT_ROOT}/work/experiments`.
- Лимиты обеих фаз: ответ 4096, ветка 768.

Проверено покрытие всех 300 global commits, число ответов каждого rank,
уникальность `(rank, prompt, sample)` и диапазон относительных позиций.
Это динамика sampled train-батчей. После шага50 изменены batch и runtime.

`collect.py` читает серверные логи через stdin Python; `data.json` сохраняет
позиции отдельных ответов, источники и SHA256. `positions.csv` содержит агрегаты.
`plot.py` строит PNG/PDF/SVG с Matplotlib из `data.json`.
Тонкая линия — среднее за update; толстая — среднее по блокам за 10 последних
updates. `summary.json` содержит сводные окна и абсолютные token indices.
Снимок 14.10.2026.
