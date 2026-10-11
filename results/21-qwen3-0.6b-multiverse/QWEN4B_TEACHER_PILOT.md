# Qwen3-4B: новые thinking-траектории

Статус 11 октября 2026: **генерация поставлена после парной оценки Sol196;
ни один выход пока не принят в SFT**. Используется постобученная
`/work/assets/models/Qwen3-4B`, скачанная ранее прямо на личном pod.
Новых расходов через VK AI Proxy нет.

Вход `data/qwen4b_teacher_pool320.jsonl` детерминированно выбран из
`data/pool.jsonl`, уже очищенного `dataset_survey/scripts/leakcheck.py`
от наших eval-наборов и полного MATH test. Исключены 647 ранее выбранных
ID из M1-187, M1-180, Sol203 и agent78. Выбрано по 80 задач GSM8K integer,
MATH integer, MATH fraction, MATH expression. Для каждого типа MATH взяты
60 задач уровней 1–3 и 20 остальных, чтобы получить и простой, и более
сложный материал. Ни один ID не повторяется.

План на одной H100: один свободный thinking-ответ на задачу,
`max_tokens=1536`, структурный текстовый запрос `Part 1/Part 2` без
Multiverse-тегов, температура 0.6, top-p 0.95, top-k 20.
`scripts/exp21/generate_pool.py` сохраняет полный raw-трейс;
`scripts/exp21/grade_gen.py` затем отбрасывает неверные, обрезанные и
повреждённые ответы через `math_verify`. Только после просмотра
независимости частей ответы могут стать предложениями для разметки
`<Parallel>` внутри `<think>`. Скрипт очереди и журналы:
`scripts/exp21/run_qwen4b_teacher_pilot_pod.sh`,
`/work/exp21/qwen4b_teacher/` на личном pod.
