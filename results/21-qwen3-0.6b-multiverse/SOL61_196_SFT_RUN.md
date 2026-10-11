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
Одинаковый fixed40 masked greedy пилот обоих шагов 24 завершён через
`scripts/exp21/run_teacher_step24_pilot_pod.sh`. Автоматические результаты:

| Модель | Верный ответ /40 | Нумерованный блок /40 | Обрезано /40 | Токенов и форвардов в среднем |
| --- | ---: | ---: | ---: | ---: |
| Родитель recovery8 step8 | 29 | 12 | 2 | 650.13 / 632.73 |
| Sol196 tagged, шаг 24 | 10 | 0 | 3 | 408.3 / 408.3 |
| Sol196 plain, шаг 24 | 27 | 0 | 4 | 855.3 / 855.3 |

Ручная проверка всех 80 ответов: tagged **10/40**, plain **26/40**
внешне верных. Автоматический счёт plain ошибочно принял один
обрезанный ответ, где правильное число было только внутри незакрытого
`<think>`. Парная разница по ручной точности: **−40 п.п.**,
95% ДИ [−55, −25]. Все 40 tagged-разметок повреждены: 33 вложенных
`<Parallel>`, ещё 7 с пропущенными или лишними обязательными тегами.
Полных и строго полезных блоков **0/40**. Автоматическая разница
−42.5 [−57.5, −27.5] п.п.; tagged против родителя −47.5
[−65, −30] п.п. по автоматическому счёту.

Важная оговорка к этому конкретному парному SFT: его прежний
plain-контроль удалял вместе с тегами весь текст `<Conclusion>`.
Следовательно 10 против 26 нельзя считать чистым эффектом одних
тегов. Для следующего парного 4B-опыта создан отдельный контроль,
сохраняющий каждый символ текста, кроме десяти Multiverse-тегов:
`data/sft_teacher_sol61_equaltext_plain_train.parquet` и
`audit/teacher_sol61_equaltext_plain_audit.json`. Старый контроль
сохранён для воспроизводимости этого опыта. Шаг 24 не выбран для
полного dev; frozen-наборы не открывались.

Архивы строк: `eval_archives/teacher_sol61_{tagged,plain}_p24_step24_masked_pilot.tgz`.
Парные интервалы: `audit/teacher_sol61_step24_tagged_vs_{plain,parent}.json`.
Ручное ревью и интервал: `audit/teacher_sol61_step24_semantic_review.md`,
`audit/teacher_sol61_step24_semantic_manifest.json`,
`audit/teacher_sol61_step24_manual_vs_plain.json`.
