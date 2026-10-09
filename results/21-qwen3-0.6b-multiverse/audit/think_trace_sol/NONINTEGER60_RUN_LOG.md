# Дополнительная разметка 60 задач, 9 октября 2026

Рабочий каталог: `/Users/v.charkin/Documents/dev/projects/parallel-r1-exp21`. Вся разметка, сборка и проверка выполнялись локально на CPU. VK AI Proxy и GPU не использовались.

1. Отобраны 60 новых MATH train вопросов без gold в `decomposable_noninteger60.jsonl`; отдельный аудит исключений `decomposable_noninteger60_audit.json`.
2. Три независимых Sol 6.1 написали `noninteger60_traces_{1,2,3}.jsonl`, по 20 решений, не видя gold. `noninteger60_trace_answer_precheck.jsonl`: 55/60 строго совпали с эталоном. Пять несовпадений исключены; исходные рассуждения под эталон не исправлялись.
3. `leakcheck_noninteger60.summary.json`: 0 утечек против eval, два слабых сигнала MATH test. `math-train/193` исключён после чтения полной пары с `math-test/547`; `math-train/2368` отличается вопросом и расчётом от пар из MATH test. Для планирования оставлены 54 строки.
4. Три других Sol 6.1 создали `noninteger60_plans_{1,2,3}.jsonl`, не меняя решения. Сборка: 33 `ok`, 20 `no_block`, 1 `filtered` из-за ссылки на соседний путь. Один план `math-train/954` исправлен только в тексте Conclusion, после ложного срабатывания эвристики на слово `check`; исходная трасса сохранена.
5. Все 33 собранных примера независимо проверены двумя рецензентами, случайные 20 прочитаны лично. Ответы и рассуждения: 33/33 верны. Полезность: 32/33 в независимом ревью и 19/20 при личном чтении. Исключены `math-train/2054` и `/43`. `noninteger60_final.jsonl`: 31 строка.
6. `finalize_sol_thinking.py` объединил 29+68+104+31=232 проверенные строки и выбрал 187 с точным совпадением распределения M1/M2: 55 GSM8K integer, 31 MATH integer, 63 MATH fraction, 38 MATH expression. `selected187.jsonl` содержит 25 новых строк.
7. Оба парных SFT parquet пересобраны: 1113 train / 48 val, 1161 всего, 187 primary×3 + 300 replay_nt + 300 replay_th. `audit_sol_thinking_sft.py` под `python -O` сверил фактические строки с исходными JSONL, режим, текст контроля, разделение по ID и максимум 3838 токенов из лимита 4096.

## Команды проверки

```sh
/tmp/exp21-audit-venv/bin/python -B /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/noninteger60_selected_with_gold.jsonl \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/leakcheck_noninteger60

/tmp/exp21-audit-venv/bin/python -B scripts/exp21/assemble_agent_plans.py \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/noninteger60_traces_checked.jsonl \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/noninteger60_plans.jsonl \
  results/21-qwen3-0.6b-multiverse/data/pool.jsonl \
  /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/noninteger60_assembled

/tmp/exp21-audit-venv/bin/python -B scripts/exp21/finalize_sol_thinking.py

/tmp/exp21-audit-venv/bin/python -B -O scripts/exp21/audit_sol_thinking_sft.py \
  /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer
```

Команды пересборки parquet зафиксированы в `scripts/exp21/build_sft.py` и исходных `data/sft_sol_th_187_rows.json`, `data/sft_control_sol_th_187_rows.json`; параметры вызова: `--val 48 --seed 21`, трижды primary и по одному разу каждый replay, контроль с `--val-ids-from` tagged prefix. Модели Sol и Qwen здесь не запускались.
