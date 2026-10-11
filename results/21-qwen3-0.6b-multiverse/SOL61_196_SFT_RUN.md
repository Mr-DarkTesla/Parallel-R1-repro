# Парный SFT: 196 Sol6.1 траекторий

11 октября 2026. Одна личная H100, pod `shared-dzen-ml/vcharkin-exp-vm-0`.
Исходная модель: `/checkpoints/exp21-v4-recovery8/step_8/model`.
Данные: [DATASET_SOL61_196.md](DATASET_SOL61_196.md), 383 train-строки
на плечо, 63 val. Паритет ID, порядка, промптов и фоновых ответов проверен
`data/sft_teacher_sol61_build.json`.

Оба плеча завершили обучение: `tagged` и `plain`, по 24 шага, batch 32,
microbatch 4, lr основной модели `3e-6`, `optim.tag_lr_mult=100`,
`data.structure=multiverse`, `data.parallel_text_loss_weight=1.0`,
позиции и маска из `multiverse_structure.py`. У обоих сохранены bf16
экспорты шагов 4, 8, 12, 16, 20 и 24 на временном диске pod; в постоянное
хранилище попадут только модели, вошедшие в глобальные пять лучших после
одинакового dev-сравнения. Команда:

```bash
EXP21_MIN_ACCEPTED=190 bash scripts/exp21/run_teacher_pair_pod.sh
```

Журнал pod: `/work/exp21/teacher_sft/train_pair.log` и
`/tmp/exp21-selective-runs/exp21-teacher-sol61-{tagged,plain}-p24/results/`.
Одинаковый fixed40 masked greedy пилот обоих шагов 24 запущен отдельно
`scripts/exp21/run_teacher_step24_pilot_pod.sh`. Его результаты и ручную
проверку блоков нужно добавить до выбора чекпоинта. Frozen-наборы не
открывались.
