# Внутренние блоки, партия 120, 9 октября 2026

Рабочий каталог: `/Users/v.charkin/Documents/dev/projects/parallel-r1-exp21`. Разметка и проверки выполнены только локально на CPU, без GPU и VK AI Proxy.

## Ход работы

1. `decomposable120_next.jsonl`: 120 вопросов без gold, 70 MATH и 50 GSM8K. Аудит исключений и схемы: `decomposable120_next_audit.json`.
2. Четыре Sol 6.1 создали по 30 самостоятельных публичных решений в `next120_traces_{a,b,c,d}.jsonl`, не видя gold и чужие ответы. Один воздержался по `gsm8k-train/2289`. Только запись `Final Answer` с символами `√` и `pi` у пяти решений до планирования переведена в LaTeX по собственным вычислениям исполнителей; численное значение и текст внутри `<think>` сохранены.
3. Сверка с gold `checks.correct`: неверны `gsm8k-train/1991` и `/2189`; они не исправлялись под эталон, а исключены. `math-train/1925` исключён как близкий шаблон полного MATH test после просмотра слабого сигнала `leakcheck.py`. `next120_traces_checked.jsonl` содержит 116 строк, полный разбор по ID в `next120_trace_answer_precheck.jsonl`.
4. Четыре других Sol 6.1 создали `next120_plans_{a,b,c,d}.jsonl` только с диапазонами юнитов, Outline и Conclusion, без изменения текста решений. 10 честных `no_block`.
5. Сборка приняла 106, отказов `filtered`/`rejected` нет. Автоматика проверила ответ, грамматику, неизменность слов и чисел, длину и размещение внутри `<think>`.
6. Полностью прочитаны все 106. Из случайных независимых 30 полезны 29, ответ и рассуждения верны 30; из личных 20 полезны 19, ответ и рассуждения верны 20; два отдельных рецензента прочитали остаток 56, все 56 полезны и верны. `math-train/6170` и `/3569` исключены. Финал `next120_final.jsonl`: 104 строки.

## Команды проверки

```sh
/tmp/exp21-audit-venv/bin/python -B /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/selected120_next_with_gold.jsonl \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/leakcheck120_next

/tmp/exp21-audit-venv/bin/python -B scripts/exp21/assemble_agent_plans.py \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/next120_traces_checked.jsonl \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/next120_plans.jsonl \
  results/21-qwen3-0.6b-multiverse/data/pool.jsonl \
  /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer \
  results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/next120_assembled

/tmp/exp21-audit-venv/bin/python -B scripts/exp21/finalize_sol_thinking.py
```

`leakcheck120_next.summary.json`: 0 утечек против eval, 0 автоматических дублей/вариантов полного MATH test, 1 вручную исключённый слабый шаблонный вариант. `next120_assembled/summary.json`: 116 трасс, 106 `ok`, 10 `no_block`, 0 ошибок. `final_review_and_selection.json`: 29+68+104 = 201 полностью проверенная строка, из них 187 отобраны для сравниваемого SFT фиксированным правилом. Соответствующая карточка: `DATASET_SOL_THINKING_NEXT120.md`.

GPU-сессий, обучения и оценки при создании этой партии не было. Собственный B после неудачного монтирования PVC остаётся масштабированным до 0; PVC не удалён. Права на A после 09:00 запрошены у пользователя отдельно.
