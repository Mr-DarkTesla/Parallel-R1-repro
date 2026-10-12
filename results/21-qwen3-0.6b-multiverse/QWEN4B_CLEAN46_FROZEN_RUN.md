# Qwen3-4B clean46: закрытые наборы после выбора модели

## Выбор до просмотра наборов, 12 октября 2026

После двух masked dev40 проверок выбран clean46 tagged step32:
строго полезные независимые блоки с верным итогом 13/40 на fixed40
и 13/40 на другом dev40. Новые plain16 и tagged32 дали на другом
наборе 12/40 и 11/40; [таблица и интервалы](QWEN4B_AGENT_PARALLEL150_RUN.md).
Решение и сырые dev-ответы зафиксированы локальным коммитом
`73995bf` до открытия здесь APO, ARC, MMLU-Pro и LIMO. Уже
выполненные [полный обычный dev и IFEval](QWEN4B_CLEAN46_FULL_DEV_RUN.md)
относятся к выбранной модели. Остальные checkpoint не оцениваются на
этих frozen-наборах.

## Запуск, 04:25 МСК

На одном нашем H100 pod `shared-dzen-ml/vcharkin-exp-vm-0`
последовательно запущены `no-thinking`, затем `thinking`, каждый для
`apo arc mmlu_pro limo`, бюджет 16 384 токена. Это обычная
последовательная генерация на plain-промптах, не masked-декодер.
Использован проверенный 4B BF16 экспорт
`/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model`,
код оценки чистого pod-worktree `14880be`, тот же что в полном dev.
Runner: [`run_qwen4b_clean46_frozen_pod.sh`](../../scripts/exp21/run_qwen4b_clean46_frozen_pod.sh),
PID **143079**. Первый активный генератор APO no-thinking:
PID **143141**. Выход и возобновляемые метаданные на личном
`/checkpoints/exp21-qwen4b-clean46-frozen-final/`.

До запуска проверены маркеры конца парного holdout40 и полного dev,
свободная GPU, четыре входных parquet, чистый tracked-код оценщика,
весовая модель и 6,1 GiB свободного места на личном PVC. Только
сгенерированный tracked `__pycache__` в чистом оценочном worktree
восстановлен до исходных файлов; исходный код не менялся. `oom_kill=5`
без роста. Pod B и чужие ресурсы не затрагивались. Новую GPU-задачу
не запускать до `EVAL_DONE` и `ATTEMPT_DONE status=0`. Прокси не
используется.

Команда запуска:

```bash
kubectl -n shared-dzen-ml cp scripts/exp21/run_qwen4b_clean46_frozen_pod.sh \
  vcharkin-exp-vm-0:/tmp/exp21-eval-code/scripts/exp21/run_qwen4b_clean46_frozen_pod.sh
kubectl -n shared-dzen-ml exec vcharkin-exp-vm-0 -- python3 -c \
  'import os,pathlib,subprocess; s="/tmp/exp21-eval-code/scripts/exp21/run_qwen4b_clean46_frozen_pod.sh"; r=pathlib.Path("/checkpoints/exp21-qwen4b-clean46-frozen-final"); r.mkdir(parents=True,exist_ok=True); f=(r/"launch.log").open("ab",buffering=0); p=subprocess.Popen(["bash",s],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}); f.close(); print(p.pid)'
```

После каждого законченного бенчмарка надо архивировать сырые ответы,
строки оценщика, журнал и meta.json, записать точность, среднюю длину,
форварды и обрезания отдельно для обоих режимов. Для математических
APO и LIMO отдельно отслеживать обрезания при лимите 16 384. Frozen
не использовать для выбора между уже проверенными моделями.
