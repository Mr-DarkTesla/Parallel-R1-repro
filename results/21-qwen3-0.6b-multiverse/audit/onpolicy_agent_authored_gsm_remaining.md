# Agent-authored remaining GSM24 dataset note

Использованы только `data/onpolicy46_questions_only.jsonl` и `data/onpolicy46_decomp_gsm_proposals.jsonl`. Уже созданные 16 ID исключены через `data/onpolicy_agent_authored_gsm16.jsonl`; файлы candidates, gold и Qwen rollout не открывались.

Из 40 предложений после исключения первых 16 осталось 24 GSM8K ID. Для всех 24 подготовлены решения, пропусков нет. Каждое решение содержит один блок внутри `<think>` с двумя независимыми Path и Conclusion, который объединяет их результаты. Во внешней строке `Final Answer:` используются чистые числа без символа валюты.

Самопроверка: 24 уникальных ID, точное дополнение к первому GSM16 файлу в proposal manifest, соответствие source=`gsm8k`, полная структура тегов и отсутствие `$` в каждом внешнем Final Answer.
