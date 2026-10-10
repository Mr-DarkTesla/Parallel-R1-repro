# GPU и чекпоинты, 11 октября 2026

Около 00:00 МСК запрошен только наш `vcharkin-exp-vm-0` с одной H100.
`vcharkin-exp-vm-b`, `vcharkin-shared-vm` и `vcharkin-setup-vm` остались
в нуле. Pod назначен на `ml-kub-node803.i`. Старый `/work` сначала дал
`FailedMount`, затем pod стал `Running` через 6 минут 18 секунд;
PVC не удаляли и чужие ресурсы не меняли. Перед запуском обучения
`nvidia-smi` показал 0 MiB и отсутствие процессов.

Новый собственный PVC `vcharkin-exp21-checkpoints-pvc` на 20 GiB создан
по `scripts/exp21/checkpoints-pvc.yaml`, имеет статус `Bound` и
подключён к этому pod в `/checkpoints`. До обучения было 19 GiB свободно.
На старом `/work` свободно около 1,5 GiB, поэтому временные состояния
обучения и все промежуточные экспорты пишутся в `/tmp` (745 GiB свободно).
На новый PVC будут перенесены только пять отобранных BF16 экспортов.
Пять прежних экспортов на `/work` пока защищены и не удалялись.

В 00:04 МСК перенесены только две подготовленные v4 parquet и две
изменённые части кода: `sft.sh` и `fsdp_parallel_sft_trainer.py`.
На pod проверены синтаксис оболочки, компиляция Python и наличие
модели Qwen3-0.6B-mv и окружения. Первая попытка драйвера сразу
завершилась до GPU: на pod не оказалось `run_selective_blocks_shared.sh`.
Файл перенесён из того же checkout; повторно запущен PID 407.

Команда обучения:

```bash
SAVE_STEPS=8,16,24,32,40,48,56,64 \
EXP21_VENV=/work/venv EXP21_WORK=/work EXP21_REPO=/work/parallel-r1 \
EXP21_RUN_NAME=exp21-m1-selective-v4 EXP21_DATA_PREFIX=sft_selective_blocks_v4 \
EXP21_EVAL_OUT=/tmp/exp21-selective-v4-eval \
bash /work/parallel-r1/scripts/exp21/run_selective_blocks_shared.sh
```

Начальное подтверждение из `train.log`: ровно 64 шага, одна H100,
`tag_lr_mult=100` для 10 новых токенов, `structure=multiverse`,
`parallel_text_loss_weight=1.0`, сохранения на шагах
8, 16, 24, 32, 40, 48, 56, 64. Процесс torchrun использует GPU.
Оценка и перенос пяти лучших чекпоинтов ещё не завершены.
