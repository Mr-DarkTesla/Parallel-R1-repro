# Что исправлено и добавлено в код

[← к сводке](README.md)

Код этой ветки — изменения ветки `sft-eval-adaptation` относительно upstream `main` (`f1c6389`) без архивов
запусков. Точка входа — [`scripts/qwen3.sh`](../../scripts/qwen3.sh), настройки этапов —
[`verl/verl/trainer/config`](../../verl/verl/trainer/config).

## Qwen3 SFT

| Что | Где |
|---|---|
| Подготовка данных и явная инициализация шести control-токенов | `verl/training_scripts/prepare_qwen3_parallel.py` |
| Seen/Unseen профили, структурные маски и позиции только для ответа | `verl/verl/utils/dataset/parallel_thinking_sft_dataset.py`, `sft_qwen3_06b*.yaml` |
| Корректное накопление градиента, равный вес ответов | `verl/verl/trainer/fsdp_parallel_sft_trainer.py` |
| Валидация без дублей сэмплера, экспорт BF16 HF checkpoint | там же |
| Нативный chat template и отложенные структурные маски для Instruct | там же, `49b47f9` |

## Оценка checkpoint

Отдельный лаунчер только валидации (`eval_qwen3_06b.yaml`, `eval_qwen3_06b.sh`), общий бюджет ответа на
пути и Summary, обработка пустых генераций, наблюдаемый `pass@N`, отдельная диагностика формата тегов,
JSONL с каждым ответом (`eval_score.py`).

## RL: корректность

| Исправление | Коммит |
|---|---|
| Запись causal-контекстов каждого вызова роллаута, сохранение меток sampled-действий | `ba048e5` |
| PPO likelihood считается в тех же контекстах, что и генерация; вставленные действия исключены из loss | `2ae4b8b` |
| Возвращена исходная структурная RL-цель upstream, задокументирована инициализация Unseen | `86f8d6a` |
| Возвращены batch/loss по умолчанию авторов и проверено расписание S2 | `3b270fa` |
| Fused PPO для padded-словаря и parallel attention | `e6850e0` |
| Конечный sequence-mean loss для пустых ответов | `f62612e` |
| Возврат только завершённых генераций vLLM | `5c90378` |
| Пропуск микробатчей с нулевым градиентом и guard очистки FSDP для реплицированных акторов | `c3a9b34`, `b656ead` |
| Учёт `TMPDIR` для IPC-сокетов vLLM | `198a1f9` |

## RL: награды

- Correctness-gated штраф за глубину и бонус за параллельную эффективность, раздельный advantage
  (`split_grpo.py`, `parallel_efficiency.py`) — [docs/efficiency-rl.md](../efficiency-rl.md).
- 4B: награды R2 и R4, centering без std — `experiments/parallel_instruct/reward.py`.

## Ускорения без изменения loss (0.6B, verl)

Каждое проверено на совпадение loss/градиентов; условия и цена по памяти описаны в корневом README.

- Обрезка паддинга и неиспользуемых logits префикса (`b01d5c0`, `59808bd`).
- Только токены в финальных выходах vLLM (`0694944`).
- Группировка микробатчей по длине без изменения весов ответов (`88f4d2c`, `b0b1440`).
- Отложенная синхронизация градиентов FSDP внутри PPO-минибатча (`48056b1`).
- Опциональные полные decode-графы с точной проверкой forward и отложенный захват редких форм
  (`ffa5657`, `ea3b07d`, `1727d4f`).
- Пробы per-token только по запросу (`9cbdfb0`).

## Где код 4B

| Что | Где | Статус |
|---|---|---|
| HF-рантайм R2 (FP32, RL50) | [`experiments/parallel_instruct`](../../experiments/parallel_instruct/README.md) | переиспользуемый код, тесты |
| Прогрев токенов и Full SFT | [бандл 4B](../reproduction/4b-2026-10-14/README.md), `snapshot/work/experiments/instruct-*` | замороженный снимок |
| Генерация SFT-корпуса (teacher, judge, фильтры) | [бандл 4B](../reproduction/4b-2026-10-14/README.md), `snapshot/exps/deepseek-gsm-wide3000-v2-20261009` и HF Dataset | замороженный снимок |
| vLLM-движок RL300 и R4 (BF16 actor, FP32 learner, TIS) | [бандл 4B](../reproduction/4b-2026-10-14/README.md), `snapshot/work/experiments/rl-vllm-32gpu-batch64-20261012`, `rl-r4-dapo2k-sft-16gpu-20261013` | замороженный снимок |
| Оценка на MATH500/AIME при 32k, random2 | [benchmark-eval](../reproduction/benchmark-eval-2026-10-13/README.md) | замороженный снимок |
| Графики и пересчёт метрик | [benchmark-trajectories](../reproduction/benchmark-trajectories-2026-10-14/README.md), [sources](sources/README.md) | запускается без сервера |

«Замороженный снимок» — код в том виде, в каком он запускался, с заменёнными путями; он опирается на дерево
`work/experiments/`, которое восстанавливает `restore.py` бандла, и в отрыве от него не запускается.
Переиспользуемым модулем в `experiments/` оформлен только HF-рантайм.

### HF-рантайм `experiments/parallel_instruct`

- одна и та же эффективная батч (8 промптов × 4 ответа) на 1/2/4/8/16/24/32 GPU; число GPU меняет только
  владение ответами, не оптимизацию;
- fullwidth8: все живые ветки (до 8) в одном forward, счётчик траектории обязан совпасть с физическим
  счётчиком `model.forward`;
- точный structured replay: изоляция соседних веток и повторяющиеся позиции воспроизводятся при обучении;
  коллективное отклонение батча при расхождении (max 0.01, mean 0.002, p95 0.005) — без обновления Adam;
- экспорт только весов на шагах 50/100/200/300/400/500, продолжение с `initial_step` и `prompt_exposure_offset`.

## Ускорение RL 4B

Замеры на checkpoint50, 8 GPU, 32 ответа на шаг, те же seeds и бюджеты (4096 / 768 / 16384); каждый вариант
проверен на точное совпадение ответов, наград и replay с базовым.

| Вариант | Результат |
|---|---|
| Базовый HF FP32 | ≈334 с на шаг, из них генерация ≈235 с (critical rank) |
| TF32 / BF16 в learner | не прошли replay guard — оставлен FP32 без TF32 |
| Compact decode (выкидывать завершённые строки из батча) | тот же F и те же ответы, слотов на форк 21 032 → 12 613 |
| Cohort batching (батч фаз от разных траекторий) | 1.18× на полном шаге; batch64 даёт +10% ответов/с при 1.8× более долгом шаге |
| Compact decode + cohort + KV replay | **1.62×**: 614 → 380 с на прогретом шаге, ответы совпадают точно |
| vLLM-движок со структурными масками (BF16 actor + FP32 learner + TIS) | использован для RL300 и R4. Парного замера нет: по генерации ≈2.5× быстрее HF BF16 и ≈1.3× быстрее HF BF16 с CUDA graphs (описательное сравнение фаз). BF16 не проходит строгий паритет логитов с FP32 (max 0.13), поэтому вводится token-TIS |

Подробности — `docs/experiments/results-2026-10-12/artifacts/work/experiments/rl-acceleration-20261012/` в ветке
`sft-eval-adaptation`.

## Проверки

```bash
python -m unittest discover -s tests -v
```

CPU-тесты: генерация, PPO loss/градиенты, порядок, guards шардирования, награды S2 и efficiency,
батчинг Instruct. На CUDA дополнительно — fused kernels и decode graphs. CPU-проверки не подтверждают
распределённое FSDP-исполнение и скорость на GPU.

## Чего здесь нет

- Архив запусков `docs/experiments/results-2026-10-12/` (84 каталога, ~2.1k файлов) и датированные снимки
  `work/` — в ветке `sft-eval-adaptation`.
- Код абляций SFT 0.6B — в ветках `exp/*` (часть изменений пересекается с SFT-кодом этой ветки,
  поэтому они не слиты).
- Профиль 0.6B для одной GPU, трейсы и Figure 3 (`experiments/qwen06/` кроме `run_rl.sh`) — в ветке `qwen3-0.6b-rl`.
- Инструменты оценки SFT 0.6B (`tag_validator.py`, `paired_compare.py`, LIMO, MATH300×8) — в ветках `exp/*`.
