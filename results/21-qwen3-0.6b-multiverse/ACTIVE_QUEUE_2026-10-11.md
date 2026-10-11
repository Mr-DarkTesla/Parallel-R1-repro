# Очередь опытов, 11 октября 2026

Один наш H100: `shared-dzen-ml/vcharkin-exp-vm-0`. После 09:00 МСК
`vcharkin-shared-vm` и `vcharkin-exp-vm-b` имеют replicas 0.
Чужие поды и тома не менялись. Все GPU-задачи идут последовательно
на этом одном поде. Разметка и ревью выполняются на CPU.

| Этап | Статус на 09:15 МСК | Запуск и выход |
| --- | --- | --- |
| Qwen3-4B teacher, 320 задач | завершён | `scripts/exp21/run_qwen4b_teacher_pilot_pod.sh`; 163 проверенных верных ответа, 144 обрезания; `data/qwen4b_teacher_graded320.jsonl` |
| 4B с десятью необученными тегами, fixed40 | идёт | `scripts/exp21/eval_4b_init_fixed40_pod.sh`; `/tmp/exp21-4b-init-fixed40/DONE` |
| 4B Sol196 tagged/plain equal-text, 16 шагов | ждёт baseline | `scripts/exp21/run_4b_teacher_after_baseline_pod.sh`; `/work/exp21/teacher_sft/FOUR_B_PAIR_DONE` |
| 0.6B M1-367 tagged/plain, 70 шагов | ждёт 4B SFT | `scripts/exp21/run_m1_after_4b_pod.sh`; `/work/exp21/m1_rewrapped_sft/TRAIN_PAIR_DONE` |
| Fixed40 для завершённых SFT | ждёт обучения | `scripts/exp21/run_post_train_fixed40_pod.sh`; `/work/exp21/m1_rewrapped_sft/POST_TRAIN_EVAL_DONE` |
| 0.6B Sol196 tagged, множитель lr тегов 1, 24 шага | ждёт оценок | `scripts/exp21/run_teacher_lr1_after_queue_pod.sh`; `/work/exp21/teacher_sft/LR1_EVAL_DONE` |

Рецепты: основной lr `3e-6`, 4B Sol196 сохраняет шаги 4/8/16,
M1-367 шаги 16/35/70, новый Sol196 lr1 шаги 4/8/24. 4B plain
контроль удаляет только десять тегов из того же текста. В прежнем
0.6B Sol196 контроле была ошибка: удалялся также Conclusion;
он сохранён для воспроизводимости, но не считается чистым сравнением.

Точный порядок обеспечивают маркеры `DONE` и PID ожидающих скриптов,
а не отдельные GPU-поды. Постоянно сохраняются только общие лучшие
пять моделей; новые чекпоинты ранжируются после fixed40 и ручного
смыслового ревью. Отобранные модели копируются на `/checkpoints`.

VK AI Proxy в этой очереди не использовался. Claude Opus вызван
локальным CLI для совета; его стоимость CLI не измерена и не
включена в учтённые расходы VK AI Proxy.
