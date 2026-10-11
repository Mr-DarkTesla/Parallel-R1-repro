# Repaired47: журнал подготовки и очередь SFT

11 октября 2026. Локальная подготовка закончена; GPU-обучение **не
запущено** из-за истёкшего Teleport-профиля. Два предыдущих личных pod
могут продолжать свои уже запущенные задачи, но новый статус после
15:16 МСК не подтверждён. Чужие pod и PVC не трогали.

Из 78 автоматически верных, но смыслово отвергнутых Qwen-ответов три
автора на CPU написали 28 открытых исправленных решений и пропустили
50 неподходящих задач. `math_verify` подтвердил 28/28 финальных
ответов. Слепое ревью приняло 13, личное повторное чтение исключило
ещё два из-за зависимости sibling-пути или лишнего пути. Осталось
**11** исправлений. Они добавлены к 36 дважды проверенным сырым
решениям 4B; подробная карточка:
`DATASET_QWEN4B_REPAIRED47.md`.

Ассемблер `scripts/exp21/assemble_qwen4b_repaired_rollouts.py`
заменил только 11 утверждённых output в 189 исходных записях,
обновил длину ответа, сохранил исходные поля генерации отдельно и
пометил авторство каждой строки. Самопроверка: `python3 -m pytest -q
scripts/tests/test_assemble_qwen4b_repaired_rollouts.py`, **2 passed**;
`bash -n` двух SFT runner также прошёл. Одна первая попытка ассемблера
правильно остановилась на пяти ошибочных значениях `answer_type` в
черновике третьей партии и одном отличии записи эквивалентной дроби.
`audit/qwen4b_onpolicy189_repair_batch_3_metadata_fixed.jsonl`
восстанавливает metadata **из исходного candidate**, не меняя ответ.

После сборки тот же `filter_onpolicy_rollouts.py` с `math_verify` и
исходным `math_dapo.py` дал **119/189** provisional, **70/189** reject,
и все 11 заменённых ответов вошли в provisional. Математический
модуль `math_dapo.py` был загружен из файла без инициализации полного
`verl`, поскольку на Mac нет pod-окружения с torch; код scorer и
функции не менялись. Сводка:
`audit/qwen4b_onpolicy189_repaired11_filter/summary.json`.

Затем `build_qwen4b_onpolicy189_pair.py` с новым манифестом 47 ID и
`--replay-thinking-count 53 --replay-no-thinking-count 53` создал по
247 train и 50 val строк на плечо. Автоматический отчёт проверяет
одинаковый порядок, удаление только тегов в контроле, отсутствие
пересечений с val и fixed40, исходный leakcheck и полную длину не
более 1580 токенов train при пределе 4096.

Команды проверок и сборки (пути относительно корня репозитория):

```bash
python3 -m pytest -q scripts/tests/test_assemble_qwen4b_repaired_rollouts.py
bash -n scripts/exp21/run_qwen4b_onpolicy189_pair_pod.sh scripts/exp21/run_qwen4b_repaired47_pair_pod.sh
uv run --offline --no-project --with tokenizers==0.23.2 python scripts/exp21/assemble_qwen4b_repaired_rollouts.py \
  --rollouts results/21-qwen3-0.6b-multiverse/eval_archives/qwen4b_onpolicy189_seed0/rollouts.jsonl \
  --candidates results/21-qwen3-0.6b-multiverse/data/qwen4b_onpolicy189_candidates.jsonl \
  --drafts results/21-qwen3-0.6b-multiverse/audit/qwen4b_onpolicy189_repair_batch_1_drafts.jsonl \
           results/21-qwen3-0.6b-multiverse/audit/qwen4b_onpolicy189_repair_batch_2_drafts.jsonl \
           results/21-qwen3-0.6b-multiverse/audit/qwen4b_onpolicy189_repair_batch_3_metadata_fixed.jsonl \
  --manifest results/21-qwen3-0.6b-multiverse/audit/qwen4b_onpolicy189_repair11_manifest.json \
  --tokenizer /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer/tokenizer.json \
  --output results/21-qwen3-0.6b-multiverse/audit/qwen4b_onpolicy189_repaired11_rollouts.jsonl
```

Выход уже существует: ассемблер специально откажется его
перезаписывать. Следующая GPU-команда после входа Teleport: сначала
проверить `EVAL_DONE` прежней пары и процессы на `vcharkin-exp-vm-0`,
потом перенести четыре parquet и `build_report.json` в личный
`/work/exp21/qwen4b_repaired47`, обновить два runner на pod и запустить
`run_qwen4b_repaired47_pair_pod.sh`. Он последовательно обучает
tagged/plain от своих `mixed401` родителей: по 32 шага,
lr `5e-7`, `tag_lr_mult=100`, одинаковые batch/val; сохраняет шаги
8/16/32 и запускает одинаковый masked fixed40. Только после этого
сравнить точность, полезность, длину, форварды и интервалы и решать,
заслуживает ли один checkpoint места в глобальной пятёрке.
