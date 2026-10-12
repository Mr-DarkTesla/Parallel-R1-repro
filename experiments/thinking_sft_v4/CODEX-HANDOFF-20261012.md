# Передача Codex, 2026-10-12 ~13:10 UTC: ремонт → SFT 4B → замер → короткий RL

Цель maxim на сегодня: дособрать хороший SFT-датасет, получить SFT-чекпойнт Qwen3-4B, замерить, насколько упало
качество относительно исходной 4B, и запустить RL. Claude останавливается (лимит). Всё нужное ниже.

## 0. Правила (не менять)

- ВМ не останавливать и не удалять, автостопы и ночной мониторинг не ставить без слова maxim. Секреты (ключ в
  `Downloads\parallel-r1\.vast-private\`) никуда не копировать.
- Контракт `verl/verl/parallel_thinking_generation_v3/contract.py` (sha256 2503e4a3…6e346e) не трогать.
- Вопросы из ролей RL/dev/test (rl_train, rl_calibration, dev, math500_test, math_extra_test, gsm_retention_test,
  exec_test, countdown_test) никогда не идут в SFT. Gold только для проверок.
- Исходный пул `pool-20261012/all.raw.jsonl` (sha256 5b48bda7…ae222d) неизменяем.
- Код: ветка `claude/project-thread-cc9a3o`, HEAD не старше 9183920. Пушить только в эту ветку.

## 1. Что сейчас на ВМ (13:05 UTC)

- tmux `fast-repair`: основной проход ремонта (старт 12:48, финиш ~13:20–13:25). Задания: 605 exec-merger, 609
  длинных summary GSM/MATH, 413 записей с обрезанными ветками (869 запросов веток). 3 123 записи годны как есть.
- tmux `baseline`: ждёт окончания ремонта, потом сам делает `assemble` и замер исходной Qwen3-4B
  (`~/parallel-r1/data/baseline_4b/chain.sh`). Сейчас там полный набор (MATH500, GSM8K test, MATH extra 512,
  countdown 256, exec, 1 000 неиспользованных вопросов пула в thinking + non-thinking на MATH500/GSM8K), ~20–40 мин.
  Если время поджимает, достаточно короткого: MATH500 + GSM8K test + countdown_test + heldout pool, только thinking.
  Важно сохранить ответы по каждому вопросу (id, верно/нет, длина): с ними потом попарно сравнивается SFT.
- Пробный прогон ремонта: exec 5/8 (все 3 провала: арифметика в коротком ответе), длинные summary GSM 4/4
  (summary ~3.6k → ~200 символов), обрезанные ветки 2/4.
- Пути: `W=~/parallel-r1/data/fast_repair`, `POOL=~/parallel-r1/data/pool-20261012`, `D=~/parallel-r1/data/sft_v4_4b`,
  репо `~/parallel-r1/repo`, venv `~/parallel-r1/.venv`, `HF_HOME=/workspace/hf-cache`.

## 2. Второй проход ремонта (после основного; код уже в 9183920)

Перепробует только провалившиеся записи: summary должен явно досчитать итог и содержать финальное значение, без
«Final Answer»/`\boxed` внутри summary, 8 вариантов вместо 4; обрезанные ветки с бюджетом на ~512 токенов больше.
Подробно: раздел «Second pass» в `README.md`. Пулл безопасен даже во время работы основного прохода.

```bash
source ~/parallel-r1/.venv/bin/activate
cd ~/parallel-r1/repo && git pull --ff-only && cd experiments/thinking_sft_v4
W=~/parallel-r1/data/fast_repair; POOL=~/parallel-r1/data/pool-20261012; D=~/parallel-r1/data/sft_v4_4b
python fast_repair.py assemble --work-dir $W --strict-v2 && cp $W/assemble_stats.json $W/assemble_stats.before_retry.json
python fast_repair.py run --work-dir $W --retry-failed --limit-jobs 8        # смоук, посмотреть глазами 2–3 summary
tmux new -d -s retry "python fast_repair.py run --work-dir $W --retry-failed 2>&1 | tee -a $W/retry.log"
# после окончания:
python fast_repair.py assemble --work-dir $W --strict-v2
python fast_repair.py export --work-dir $W --out $W/repaired.jsonl
```

Решение по строгости: `--strict-v2` отбраковывает и часть записей, которые первый проход принял. Сравнить
`strict_v2` в `assemble_stats.before_retry.json` и финальном `assemble_stats.json`. Если в итоге принятых
отремонтированных меньше, чем было бы без строгих правил, более чем на ~150 записей, пересобрать с
`--no-strict-v2` (или только `--math-value-check skip`, если теряется в основном MATH) и сказать maxim.

## 3. Отбор

```bash
python select_records.py $POOL/all.raw.jsonl $W/repaired.jsonl --out-dir $D --val-frac 0.05 \
    --tokenizer Qwen/Qwen3-4B --max-len 16384
cat $D/selection_stats.json
```

Ожидание: ~2 800 параллельных + ~1 200 последовательных. Если параллельных заметно меньше 2 000, сказать maxim до SFT.
Перед обучением глазами 5–10 строк из `$D/train.jsonl` (по 2 на источник): summary не пересчитывает ветки, итог в
summary совпадает с ответом.

## 4. SFT (по README, разделы «VM commands» и «Tag warmup»)

```bash
python vm_selftest.py --data $D/train.jsonl                       # должно быть ALL PASSED; иначе чинить, не обучать
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b_mem \
    --memory-report 3 --tag-warmup-steps 60                       # пик < ~89 GiB, печатает fits / DOES NOT FIT
tmux new -d -s sft "python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b \
    --epochs 2 --lr 1e-5 --min-lr-ratio 0.1 --warmup-ratio 0.03 --target-steps-per-epoch 90 \
    --max-len 16384 --save-every-epoch --eval-every 30 \
    --tag-warmup-steps 60 --tag-lr 1e-3 --freeze-check 2>&1 | tee -a runs/sft_v4_4b.log"
```

- **2 эпохи, не 3** (меньше просадка базовых навыков, успеваем сегодня). Чекпойнт после каждой эпохи.
- Если память не влезает: сначала `--optim adamw8bit`, потом `--micro-batch-tokens 12288`. `--max-len` не снижать
  (длинные записи — это и есть thinking-трейсы).
- Следить в `runs/sft_v4_4b/metrics.jsonl`: `loss_tag` должен падать уже на прогреве (stage 1), `val_loss` не расти.
- Время: порядка 2–2.5 ч на эпоху (оценка, на GPU не мерили). Если к вечеру не успевает, eval и RL можно делать от
  чекпойнта первой эпохи.

## 5. Замер: насколько упало качество

Сравнивать с исходной Qwen3-4B (`baseline_4b`) на тех же вопросах, тот же бюджет 16 384, те же сэмплы.

```bash
python selftest_sampler_vm.py --model runs/sft_v4_4b/final
for T in think_math500 think_gsm8k_test; do
  python eval_graph.py --model runs/sft_v4_4b/final --tasks ~/parallel-r1/data/$T.parquet --mode both --backend vllm \
    --budget 16384 --samples 4 --gpu-memory-utilization 0.40 --hf-batch-tokens 120000 --out runs/eval_v4_4b/$T
done
```

Плюс те же countdown_test и heldout pool, что в baseline (так же, как их считает `baseline_4b/chain.sh`).

- `--mode both` даёт два режима: **sequential** (форки запрещены; это «не сломали ли модель») и **graph**
  (форки разрешены).
- Главная цифра — sequential SFT против исходной 4B, попарно по одним и тем же вопросам. Падение больше ~2 п.п. на
  MATH500 или GSM8K — тревога: сказать maxim до RL (варианты: чекпойнт 1-й эпохи, меньше lr).
- Для graph: точность, доля ответов с форком, число невалидных планов (`invalid_plan`, `plan_incomplete` в
  report.json), длина критического пути против sequential.
- Итог одной короткой таблицей в файл `reports/thinking-sft-20261012/sft-eval.md` на устройстве maxim.

## 6. RL (коммит 522e915 сделал launcher годным для 4B)

- `check_checkpoint.py` теперь принимает Qwen3-4B; `OFFLOAD=true` держит fp32-веса и Adam актора в RAM (без этого 4B
  с vLLM на одной H100 не влезет). Оценка ~30 мин на шаг, поэтому сегодня только короткий прогон.
- Данные: `~/parallel-r1/data/think_{train,val}.parquet` из `experiments/qwen06/prepare_think.py --roles <твои
  role-файлы> --manifest <manifest.json>`. Если их нет на этой ВМ, собрать. Шаблон промпта тот же, что в SFT.

```bash
cd ~/parallel-r1
OFFLOAD=true BATCH=16 MINI=16 STEPS=30 RUN_NAME=qwen3-4b-think-v0-short REWARD=v0 \
  bash repo/experiments/qwen06/run_rl.sh think "$HOME/parallel-r1/repo/experiments/thinking_sft_v4/runs/sft_v4_4b/final"
```

- Сначала `SMOKE=1` нельзя (он для необученной 0.6B); вместо этого `STEPS=2` и посмотреть, что шаг проходит и
  память держится. Не проверено на GPU: внимание SDPA на 16k с маской у 4B может не влезть; тогда `GPU_MEM=0.35`,
  `MAX_NUM_SEQS=32`, `ROLLOUT_N=4`.
- Награда V0 (только верность) для первого прогона. Графовый rollout (`GRAPH_ROLLOUT=true`) не включать, пока
  обычный не пройдёт.

## 7. Не сегодня

- Пробник двух последовательных блоков `<Parallel>` (пример math-intermediate_algebra-train-1130) ещё пишется
  Claude, к SFT не нужен.
- Контрольный SFT без тегов, проверка перекрытия веток и пересечения с тестами — после первого RL.
