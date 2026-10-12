# 4B: парное продолжение на 150 проверенных Parallel-задачах

## Сбой экспорта и точечное возобновление, 03:24 МСК

Оба плеча действительно закончили все 32 шага; tagged успел
завершить BF16 экспорты шагов 8/16/32 и `model`, plain записал
`TRAINED` и проверенные BF16 экспорты шагов 8/16/32. На
**повторном экспорте final `model`** plain процесс был убит памятью
pod: первый `ATTEMPT_DONE status=137`, `oom_kill` вырос с 4 до 5.
Это не сбой обучения и не оценка качества. В cgroup было 166,3 GB
из лимита 171,8 GB, из них 165,2 GB файлового кэша наших
временных весов. Свободное место на диске осталось.

Применён имеющийся `evict_own_file_cache_pod.py` только к двум
каталогам временных весов этой пары, без удаления файлов и без
изменения чужих ресурсов: 21 файл, 85,599 GB `POSIX_FADV_DONTNEED`.
`memory.current` снизился с 166,298 до 80,504 GB. Проверены
`TRAINED` plain, все три его проверенные модели, отсутствие другого
GPU-процесса и сохранённый tagged `DONE`. Исходный журнал оставлен
как `/checkpoints/exp21-agent-parallel150/launch.oom_attempt1.log`.

Тот же runner возобновлён с PID **137288** без нового `torchrun`:
он пропустил готовый tagged, проверил и доделал экспорт plain.
`TRAIN_PAIR_DONE` появился в 03:24, после чего началась masked
fixed40 оценка tagged step32, один процесс
`generate_masked_multiverse.py` PID 137855. `oom_kill=5` без
дальнейшего роста. Старый `ATTEMPT_DONE status=137` остаётся до
завершения нового runner, когда будет перезаписан итоговым статусом.
Новый GPU-запуск до конца этой оценки запрещён.

## Запуск, 03:08 МСК 12 октября 2026

После завершения прежнего [сбора 1144 траекторий](CLEAN46_ONPOLICY143_SAMPLE.md)
проверены `FILTER_DONE`, `ATTEMPT_DONE status=0`, отсутствие его PID,
свободная личная H100, неизменный `oom_kill=4`, 19 GiB свободно на
`/checkpoints` и 1,1 TiB под временные файлы на `/tmp`. Сырые ответы
сбора архивированы до нового GPU-запуска. Pod B и чужие ресурсы не
затрагивались.

На одной H100 pod `shared-dzen-ml/vcharkin-exp-vm-0` запущен один
последовательный [runner](../../scripts/exp21/run_qwen4b_agent_parallel_pair_pod.sh),
PID 135307, дочерний `torchrun` PID 135476. Первым идёт tagged.
`torchrun --nproc_per_node=1` подтвердил одну GPU. Обе ветви получают
одного родителя, Qwen3-4B clean46 tagged step32, и [равные парные
данные](DATASET_AGENT_PARALLEL_150_PAIR.md): по 559 train и 50 val
строк, 150 полезных размеченных задач и одинаковый thinking/no-thinking
replay. Тексты tagged/plain различаются только тегами.

Условия: 32 шага на плечо, global batch 16, lr `5e-7`,
`optim.tag_lr_mult=100`, временные шаги 8/16/32. Tagged использует
Multiverse mask и позиции sibling-путей, plain обычную causal mask.
После обоих SFT runner последовательно выполнит одинаковую masked
fixed40 оценку всех шагов, сохранит train logs и сырые ответы в
`/checkpoints/exp21-agent-parallel150/archives`, затем поставит
`EVAL_DONE` и `ATTEMPT_DONE status=0`. Модели остаются временно в
`/tmp`; до ручного ранжирования полезных путей и точности ни одна
не входит в общий TOP-5. За всё время на постоянном томе не более
пяти моделей.

Команда запуска:

```bash
kubectl -n shared-dzen-ml exec vcharkin-exp-vm-0 -- bash -lc \
  'nohup env EXP21_PAIR_DATA=/checkpoints/exp21-agent-parallel150 EXP21_RUN_PREFIX=exp21-4b-agent-parallel150 bash /work/parallel-r1/scripts/exp21/run_qwen4b_agent_parallel_pair_pod.sh > /checkpoints/exp21-agent-parallel150/launch.log 2>&1 < /dev/null & echo RUNNER_PID=$!'
```

После запуска один `torchrun` с tagged data и masked structure
появился; новых OOM нет. При завершении нужно сравнить tagged/plain
и родителя на одних 40 запросах: строгий финал, верное значение,
полный блок внутри `<think>`, ручную полезность каждого Path,
длину, число форвардов по самому длинному Path, обрезания и парные
95% интервалы. Затем выбрать лучший шаг для полного dev в обоих
режимах и IFEval; frozen только для итогового лучшего.
