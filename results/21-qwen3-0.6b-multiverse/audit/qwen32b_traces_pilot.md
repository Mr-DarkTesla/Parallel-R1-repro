# Qwen3-32B reasoning trace pilot

Статус: **stopped_request_error**. Сборщик запросил 1 из 400 задач;
0 ответов содержат `reasoning_content`, 0 имеют
верный неусечённый final-ответ. Цель: минимум 200 таких сырых трейсов.

## Ограничения

- Модель: `qwen3-32b`. Запросы последовательные, без повторов.
- Сохраняются исходные `content` и `reasoning_content`. Текст рассуждений не создаётся и не исправляется локально.
- Только GSM8K integer и MATH integer/fraction/expression. Выбор равный: 100 задач каждого типа.
- До выбора исключаются все найденные ранее positive, replay, validation и eval ID, а также нормализованные тексты вопросов. Источник `data/pool.jsonl` ранее прошёл leakcheck.
- Любой пустой/отсутствующий `reasoning_content`, ответ без безопасного `usage` или транспортная ошибка останавливает сбор.

## Расходы

В API не обнаружен текущий тариф или invoice-поле. Поэтому это не заявленная фактическая стоимость: перед каждым запросом применяется явный верхний тариф `10.0` USD/M input и `30.0` USD/M output, максимум `1024` input bytes и `1024` output tokens. Верхняя граница на 400 запросов: `16.384000` USD, меньше жёстких $20. Накопленная граница по фактическому `usage`: `0.000000` USD. Proxy invoice: `unavailable`.

## Артефакты

- `data/qwen32b_traces_raw.jsonl`: исходные задача, ответ, reasoning, модель, параметры, usage и проверка final-ответа.
- `audit/qwen32b_traces_accounting.jsonl`: один accounting record на запрос.
- `audit/qwen32b_traces_state.json`: прогресс, stop reason и cumulative counts.

    Запуск: `/tmp/exp21-audit-venv/bin/python -B scripts/exp21/collect_deepseek_traces.py --output-prefix qwen32b_traces`.

## Pilot request

HTTP status: `400`. Usage present: `False`. Content present: `False`. reasoning_content present: `False`.
