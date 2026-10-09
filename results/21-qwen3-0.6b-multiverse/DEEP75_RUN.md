# SFT на 75 новых подробных решениях

10 октября 2026. До запуска: два полностью подготовленных и проверенных варианта. Tagged и контроль содержат одинаковые задачи в одинаковом порядке, одинаковые промпты и режимы Qwen; у контроля только удалены структурные теги из тех же ответов. Математические примеры: 24 из `DATASET_SOL_DEEP_PILOT24.md` и 51 из `DATASET_SOL_DEEP_ROUND2_51.md`, все блоки внутри `<think>`.

## Смесь и разделение

| Источник | Уникальных | Копий на задачу | Всего строк |
|---|---:|---:|---:|
| Прежние Sol thinking | 187 | 1 | 187 |
| Новые подробные Sol thinking | 75 | 4 | 300 |
| Собственные верные Qwen no-thinking | 300 | 1 | 300 |
| Собственные верные Qwen thinking | 300 | 1 | 300 |
| Всего | 856 | | 1087 |

Шесть задач встречаются и в replay no-thinking, и в replay thinking; поэтому число уникальных задач 856, а сумма по строкам таблицы больше.

Validation ID взяты из прежнего `sft_sol_th_187_val.parquet`: train 1055, val 32. Новые 75 задач целиком в train. Скрипт `scripts/exp21/prepare_deep_aug75_sft.py` сохранил оба parquet и `data/sft_sol_deep75_audit.json`. Независимая проверка: 2174/2174 строк обоих вариантов точно соответствуют исходным ответам и `build_sft.row`; train/val имеют ноль общих ID и нормализованных вопросов; у контроля primary текст равен `strip_tags(tagged)`, replay совпадает дословно; per-row thinking флаг корректен. Токенизатор `/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer`: максимум 3838 токенов, 0 строк длиннее 4096 в обоих вариантах.

Команда проверки длин на Mac (read-only, без GPU):

```sh
/tmp/exp21-audit-venv/bin/python - <<'PY'
import pandas as pd
from transformers import AutoTokenizer
root='results/21-qwen3-0.6b-multiverse/data'
tok=AutoTokenizer.from_pretrained('/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer', local_files_only=True)
for arm in ('tagged', 'control'):
    lengths=[]
    for split in ('train', 'val'):
        for _, row in pd.read_parquet(f'{root}/sft_sol_deep75_{arm}_{split}.parquet').iterrows():
            info=row.extra_info
            prompt=tok.apply_chat_template([{'role':'user','content':info['question']}], add_generation_prompt=True, tokenize=False, enable_thinking=info['enable_thinking'])
            lengths.append(len(tok.encode(prompt, add_special_tokens=False)) + len(tok.encode(info['answer']+tok.eos_token, add_special_tokens=False)))
    print(arm, len(lengths), max(lengths), sum(n>4096 for n in lengths))
PY
```

Рецепт обоих вариантов: post-trained `Qwen/Qwen3-0.6B` с различно инициализированными 10 спецтокенами, маска и позиции Multiverse из exp/19, `optim.tag_lr_mult=100` из exp/20, 64 шага, основной lr `1e-5`, пакет 32, микро-пакет 4, длина 4096, seed тренера 1. Собственные replay сохранены в thinking и no-thinking. Это один seed; интервалы последующей dev-оценки будут условны на нём.

На pod используется собственный GPU 0. Временные чекпоинты и экспорт размещаются в контейнерном `/tmp/exp21-runs`; после каждого завершения модель и журналы копируются в постоянный `/work/runs/`. Это нужно из-за 5,6 ГиБ свободного места на PVC; само PVC не удаляется. Параметр `RUN_ROOT` добавлен в `scripts/instruct4b/sft.sh` с прежним значением `/work/runs` по умолчанию.

В 02:09 МСК на `vcharkin-exp-vm-0` подтверждены четыре parquet с длинами 1055/32 в обоих вариантах, обновлённый `sft.sh`, синтаксис обоих shell-скриптов и отсутствие других процессов на GPU 0. Запущен **один** последовательный процесс-обёртка PID 17691:

```sh
nohup bash /work/exp21/deep_round2/run_deep75_pod.sh > /work/exp21/deep_round2/train_pair.log 2>&1 < /dev/null &
```

Скрипт обучил `exp21-sol-deep75`, затем `exp21-sol-deep75-control` на том же одном GPU и скопировал оба `DONE`, модели, журналы и `results` в `/work/runs/`. Пара закончилась в 02:15:57 МСК; оба варианта дошли до 64 шагов. Последняя validation loss: 0,48066 у размеченного варианта и 0,49981 у контроля. Эти потери не используются для выбора модели вместо dev-оценки. Размер каждого сохранённого запуска около 1,2 ГиБ. После завершения восстановлена исходная версия `scripts/instruct4b/sft.sh` в pod, чтобы оценочный конвейер видел чистый commit `d774d24`; локальное изменение `RUN_ROOT` сохранено в исходниках этой ветки и журнале опыта.

В 02:16 МСК запущен один последовательный оценочный процесс по `scripts/exp21/run_deep75_eval_pod.sh`. Он проверяет оба варианта на одинаковых dev-наборах с запросом Multiverse внутри `<think>`, на обычных запросах в thinking и no-thinking, затем на IFEval в обоих режимах. Выходы находятся в `/work/exp21/eval/deep75-*`, журнал обёртки в `/work/exp21/deep_round2/eval_pair.log`. Первым идёт размеченный вариант на GSM8K dev с Multiverse-thinking; все итоговые метрики и парные интервалы ещё предстоит рассчитать.
