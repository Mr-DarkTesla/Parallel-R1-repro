# Parallel-R1 с Qwen3-0.6B

Профиль S1/S2 для одной A100 80 GB: окружение через uv, проверка SFT, GRPO на vendored verl, полные трейсы и восстановление после прерывания ВМ. Базовый код: `f1c63891d7fe77335103eb2c17e542a2b086dafc`.

## Установка

Скрипт рассчитан на Ubuntu 22.04, Python 3.10 и NVIDIA GPU с совместимым драйвером. Для системных пакетов требуется sudo. Основные версии: PyTorch 2.6.0, vLLM 0.8.5.post1, Transformers 4.51.3, Ray 2.43.0, flash-attention 2.7.4.post1. Существующий checkout не переключается автоматически.

```bash
git clone --branch qwen3-0.6b-rl https://github.com/Mr-DarkTesla/Parallel-R1-repro.git ~/parallel-r1/repo
bash ~/parallel-r1/repo/experiments/qwen06/bootstrap_vm.sh
cd ~/parallel-r1
.venv/bin/python repo/experiments/qwen06/prepare.py
```

Корень задаётся через `PARALLEL_R1_ROOT`, по умолчанию `~/parallel-r1`. Окружение, данные, модели и результаты хранятся рядом с `repo`. `prepare.py` сохраняет SHA-256/schema исходных parquet в `data/manifest.json`. Вопросы и порядок S1/S2 совпадают; отличается reward method. Validation в обоих режимах использует accuracy.

| Данные форка | Строк | Назначение |
|---|---:|---|
| DAPO | 17917 | RL train |
| APO-combine | 1916 | Validation: AIME24, AIME25, AMC23, APO_MATH300 |
| GSM8K | 4090 | SFT reference |

Происхождение внешнего SFT нельзя установить по имени архива. APO_MATH300 не доказывает идентичность MATH-500 из статьи.

## SFT и preview

Нужен HF-каталог с config, tokenizer и safetensors. `check_checkpoint.py` проверяет Qwen3-0.6B, размеры embeddings, chat template и шесть различных атомарных тегов: `<Parallel>`, `</Parallel>`, `<Path>`, `</Path>`, `<Summary>`, `</Summary>`. Не добавляйте токены заново к обученному SFT. Проверка архива запрещает обход путей и ссылки; существующий каталог не перезаписывается.

```bash
.venv/bin/python repo/experiments/qwen06/check_checkpoint.py incoming/qwen3-0.6b-unseen-epoch-5.tar.gz --extract-to models/sft-epoch5
# MODEL — model_path из отчёта проверки; архив может иметь вложенные каталоги.
MODEL=/absolute/path/to/validated/hf/checkpoint
# Необязательная загрузка из Google Drive:
bash repo/experiments/qwen06/download_checkpoint.sh 'https://drive.google.com/file/d/FILE_ID/view'

.venv/bin/python repo/experiments/qwen06/prepare_preview.py
RUN_NAME=sft-preview bash repo/experiments/qwen06/preview.sh "$MODEL"
.venv/bin/python repo/experiments/qwen06/analyze.py runs/sft-preview --out reports/sft-preview
```

Preview выполняет только validation, без optimizer update: два GSM8K, два DAPO, по одному из четырёх validation-источников. Восемь вопросов не являются benchmark. Для повторения задайте новое `RUN_NAME`, чтобы не смешивать JSONL. Анализатор поддерживает старые трейсы с повторяющимся upstream worker index: исходный index сохраняется, глобальный восстанавливается по validation output.

## RL

```bash
bash repo/experiments/qwen06/run_rl.sh s1 "$MODEL"
# После завершения S1 на той же GPU:
bash repo/experiments/qwen06/run_rl.sh s2 "$MODEL"
```

| Настройка | Значение |
|---|---:|
| Train batch | 32 вопроса |
| Rollout n | 8 ответов на вопрос |
| PPO mini-batch в конфигурации | 32; verl умножает на rollout n, итого 256 ответов |
| Actor microbatch | 1 ответ |
| Бюджет / LR | 300 шагов / 1e-6 |
| Prompt / response | 2000 / 3000 токенов |
| Ветки / максимум форков | 2 / 4 |
| Validation / сохранение обычного запуска | Каждые 10 / 10 шагов |

Это вычислительная адаптация: batch статьи — 512, опубликованного скрипта — 256 на 8 GPU. Полное совпадение гиперпараметров не заявляется. `BATCH`, `MINI`, `ROLLOUT_N`, `STEPS`, `RESPONSE`, `PROMPT`, `WORKERS` задаются через environment; дополнительные Hydra overrides передаются после модели. Текущий профиль задаёт `clip_ratio_high=0.28` обоим режимам; исходный S1 использует 0.2, S2 — 0.28. Для отдельного сравнения S1 передайте `actor_rollout_ref.actor.clip_ratio_high=0.2` и новое имя запуска.

Оба режима стартуют из общего SFT. По умолчанию `trainer.resume_mode=disable`; для продолжения своего запуска передайте `trainer.resume_mode=auto`. Сохраняются model/optimizer/extra, последние три actor checkpoint. FSDP checkpoint не является готовым HF-каталогом: `actor/huggingface` содержит config/tokenizer; веса экспортируются model_merger из verl.

Log-probs актора задаёт `LOGPROB_CONTEXT`. По умолчанию `flat_packed`: каждый сэмплированный токен оценивается в том же causal-контексте и на тех же позициях, что и вызов vLLM, который его породил. Пути 2..n каждого блока vLLM генерировал без соседних путей, поэтому актор дописывает их копии в конец последовательности и берёт log-probs из копий; всё считается за один forward (`verl/verl/workers/actor/replay_context.py`). Вставленные рантаймом теги исключены из loss; где рантайм заменил сэмплированный EOS на закрывающий тег, оценивается EOS. `LOGPROB_CONTEXT=tree` возвращает исходную цель: Unseen-маска и multiverse-позиции. Она совпадает с rollout только до первого summary. `ROLLOUT_LOGPROBS=true` (по умолчанию) пишет `rollout_gap/*`: |log-prob vLLM − old_log_prob| по сегментам траектории. Метрика имеет смысл только при temperature 1 без top-p/top-k. `flat_packed` требует `use_remove_padding=False` и выключенных fused kernels, как в этом профиле. Все вызовы одной траектории идут на один vLLM-сервер, чтобы summary попадал в prefix cache путей.

## RL в thinking-режиме

Режим `think` запускает RL для Qwen3-0.6B (не Base) из thinking-SFT. Блоки `<Parallel>` идут внутри `<think>`, ответ пишется после `</think>`.

```bash
.venv/bin/python repo/experiments/qwen06/prepare_think.py          # --template должен совпадать с промптом SFT
                                                                    # --smoke-model: Qwen3-0.6B с 8 необученными тегами, только для SMOKE=1
REWARD=v0 bash repo/experiments/qwen06/run_rl.sh think "$MODEL"    # v0 | v1_low | v1_high | v2
ALLOW_PARALLEL=false REWARD=v0 bash repo/experiments/qwen06/run_rl.sh think "$MODEL"   # последовательный baseline
```

`prepare_think.py` раскладывает данные по ролям, которые заморозила сторона SFT (dataset-plan.md и manifest.json у Codex, seed 20261009). С `--roles DIR` он читает готовые `<role>.jsonl` (ответы можно положить в `<role>.gold.jsonl`), а `--manifest` сверяет их sha256. Без `--roles` те же роли собираются из Hugging Face как запасной вариант: там отсеиваются только точные дубли и задачи с `[asy]`, без фильтра почти-дублей по триграммам, поэтому id отличаются от замороженных.

| Роль | Файл | Зачем |
|---|---|---|
| rl_train, 1024 | `think_train` | RL |
| rl_calibration, 128 | `think_calib` | проверка сложности и шкалы V2; в RL-rollout не идёт |
| dev, 256 | `think_val` | валидация во время RL, выбор чекпоинта и настроек |
| math_extra_test, 512 | `think_math_test` | только финальное сравнение |
| math500_test | `think_math500`, пилот `think_math500_pilot` (128) | только отчёт, ничего по нему не выбирают |
| gsm_retention_test | `think_gsm8k_test`, пилот `think_gsm8k_test_pilot` (128) | проверка, что модель не разучилась |

rl_train, rl_calibration и dev — непересекающиеся части очищенного пула MATH train (algebra, prealgebra, number theory, counting & probability, уровни 2–4); резерв пула в обучение не идёт. Скрипт падает, если роли обучения пересекаются с другими. GSM8K train и разделы MATH geometry, intermediate algebra и precalculus уходят в SFT, в RL их нет. Шаблон по умолчанию — `{problem}` и просьба дать ответ в `\boxed{}`; он должен совпадать с промптом SFT. Ответ сравнивается по нормализации DAPO, а если строки не совпали, то через math-verify (`0.75` = `\frac{3}{4}`). TEST, MATH-500 и GSM8K считаются отдельным прогоном без обучения:

```bash
RUN_NAME=eval-step300 REWARD=v0 bash repo/experiments/qwen06/run_rl.sh think "$CHECKPOINT" \
  trainer.val_only=true trainer.val_before_train=true \
  data.val_files="['$HOME/parallel-r1/data/think_math_test.parquet','$HOME/parallel-r1/data/think_math500.parquet','$HOME/parallel-r1/data/think_gsm8k_test.parquet']"
```

Отличия режима от S1/S2:

| Настройка | think |
|---|---|
| Advantage | RLOO по группе из 8, без деления на std |
| Ответ | 16384 токена, `enable_thinking=true` |
| Блоки / ветки | `protocol=plan_v1`: до `MAX_BLOCKS=2` блоков, 2–4 ветки по плану модели |
| Log-probs актора | `flat_packed` с тем же подавлением тегов, что в vLLM; `rollout_gap/*` (см. выше) |

Формат блока задаёт общий с thinking-SFT модуль `verl/verl/parallel_thinking_generation_v3/contract.py`: парсер плана, подавление тегов, графовые позиции и маска, D/T. SFT берёт его же, своей копии нет.

```
<Parallel><Plan>cases
1: x > 0
2: x <= 0
</Plan><Path>1: …</Path><Path>2: …</Path></Parallel><Summary>…</Summary>
```

- **Кто что пишет.** Модель сэмплирует `<Parallel>`, текст плана и `</Plan>`, текст веток и `</Path>`, summary и `</Summary>`. Рантайм вставляет `<Plan>`, `<Path>` с `i:` и `</Parallel><Summary>` без перевода строки. Вставленные токены не получают log-prob и не входят в D/T.
- **План.** Первая строка — тип: decompose, cases, candidates, methods или verify. Дальше 2–4 строки `i: текст`. Сколько строк, столько веток.
- **Невалидный план.** Если план не разбирается, обрывается EOS или не закрыт за `MAX_PLAN_TOKENS` (256), траектория на этом кончается. Её c = 0, то есть −1 в V0, и она остаётся в группе RLOO. План никто не чинит, пустых блоков не бывает.
- **Подавление.** Каждый узел (основная цепочка, план, ветка, summary) может сэмплировать только свой закрывающий тег, остальным тегам vLLM даёт `logit_bias` −100. После `MAX_BLOCKS` блоков подавлен и `<Parallel>`. Актор прибавляет те же −100 к своим логитам до температуры, поэтому оценивает то распределение, из которого сэмплировали.
- **Ветки.** Все ветки блока сэмплируются после плана, без соседних веток в контексте; `flat_packed` пересчитывает ветки 2..n в этом же контексте.
- **Телеметрия.** `parallel/parallel_triggers_mean` (сколько раз сэмплирован `<Parallel>`), `parallel/valid_plan_blocks_mean`, `parallel/fork_dispatches_mean`, `parallel/path_jobs_mean`, `parallel/plan_valid_ratio`, `parallel/paths_per_block`, `parallel/plan_failed_ratio`; в наградах `plan_failed`.

Награды из дебатов с Codex (8–9 октября). c = 1, только если ответ после последнего `</think>` верен и стоит вне веток. Если `</think>` нет или он внутри ветки, c = 0. Ответ берётся из последнего `\boxed{}` после `</think>`, иначе из строки `Final Answer:`.

- V0 = 2c − 1.
- V1 = 2c − 1 − c·(α·D/16384 + β·T/16384). Для V1-low α = 0.10, β = 0.05; для V1-high α = 0.50, β = 0.25.
- V2 = 2c − 1 − c·(0.10·g(D/s_D) + 0.05·g(T/s_T)), где g(x) = x/(1+x).

D — критическая глубина: сэмплированные токены основной цепочки плюс самая длинная ветка и summary каждого блока. T — все сэмплированные токены. Вставленные рантаймом теги не входят ни в D, ни в T. В телеметрии это `parallel/critical_depth_mean` и `parallel/sampled_tokens_mean`, в наградах — `critical_depth`, `sampled_tokens`, `cost`.

Масштабы s_D и s_T для V2 замораживаются один раз по верным ответам SFT-чекпоинта на `think_calib` (rl_calibration). Берётся медиана по источнику данных; у rl_train, rl_calibration и dev он общий (`math`), поэтому шкала с калибровки применяется к обучению. Собственные медианы задач из калибровки к rl_train не относятся: роли не пересекаются. RL-сэмплы файл не меняют.

```bash
RUN_NAME=calib-sft REWARD=v0 bash repo/experiments/qwen06/run_rl.sh think "$MODEL" \
  trainer.val_only=true trainer.val_before_train=true \
  data.val_files="['$HOME/parallel-r1/data/think_calib.parquet']" actor_rollout_ref.rollout.val_kwargs.n=8
.venv/bin/python repo/experiments/qwen06/calibrate_cost_scales.py runs/calib-sft/validation --out data/cost_scales.json
REWARD=v2 COST_SCALES=$PWD/data/cost_scales.json bash repo/experiments/qwen06/run_rl.sh think "$MODEL"
```

Ограничения:
- Rollout пока плоский: summary и всё после первого блока vLLM сэмплирует без маски веток, а `flat_packed` оценивает ровно эти контексты. Графовый rollout, как в графовом SFT, требует патча vLLM (вариант B в `/mnt/project-files/analysis/kv-merge-unseen-plan.md`).
- Ветки 2..n каждого блока vLLM заново считает при prefill summary.
- `rollout_gap/*` сравнивает с log-prob vLLM по сырым логитам, до `logit_bias`, так что в plan_v1 в разрыв входит и масса подавленных тегов. Точное совпадение актора с сэмплирующим распределением проверяет `tests/test_flat_packed_context.py`.
- vLLM 0.8.5 V1 применяет `logit_bias` питоновским циклом по запросам и токенам на каждом шаге декодирования. На smoke-прогоне стоит посмотреть, сколько это добавляет ко времени генерации.
- Актор строит плотную маску T×T. Для 18k токенов это ~1 ГБ на ответ при microbatch 1.

## Трейсы и Figure 3

В `runs/<name>` записываются происхождение запуска (`checkpoint.json`, `source_commit.txt`, `source.patch`, `environment.freeze.txt`), стандартные тексты/награды verl, offline W&B и telemetry:

- `events-*.jsonl`: реальные форки, шаг RL, sample/rollout и позиция в ответе.
- `traces-*.jsonl`: вопрос, текст/IDs ответа, calls main/path/summary, длины входов и генераций, position IDs, окна attention mask, response mask, обрезание.
- `forwards-*.jsonl`: фактические участия request в model.forward, scheduler steps и scheduled tokens, включая prefill и prefix cache.
- `engine-*.jsonl`: фактические общие batched forwards. Один forward обслуживает несколько requests; сумму participations нельзя называть числом GPU forwards.

Точный forward probe требует eager rollout. Без `PARALLEL_R1_TRACE_DIR` запись JSONL и probe отключены. Console/W&B содержат parallel ratio, число форков, generation calls, токенов и долю обрезаний. Средняя позиция при отсутствии тегов не подменяется нулём.

```bash
.venv/bin/python repo/experiments/qwen06/analyze.py runs/qwen06-s1-seed1 runs/qwen06-s2-seed1 --out reports/comparison
.venv/bin/python repo/experiments/qwen06/plot_progress.py runs/qwen06-s1-seed1 --out reports/progress-s1 --expected-samples 256
.venv/bin/python repo/experiments/qwen06/check_step_telemetry.py runs/qwen06-s1-seed1 --step 1
.venv/bin/python repo/experiments/qwen06/read_progress.py runs/qwen06-s1-seed1
.venv/bin/python repo/experiments/qwen06/check_save_overhead.py runs/qwen06-s1-seed1
```

`analyze.py` создаёт CSV, PNG/PDF, enriched JSONL и `traces.html`. Для ответа доступны длины до первого форка, каждого Path, Summary, между форками и после последнего. HTML экранирует модельный текст. Отсутствующие forward-счётчики отображаются как `null`.

Положение для Figure 3 — индекс открывающего токена / длина сохранённого ответа: prompt исключён, управляющие теги включены. `analyze.py` считает все `<Parallel>`. `plot_progress.py` отдельно показывает теги и реальные fork events. Тег внутри Path/Summary не запускает вложенные ветки; тег на пределе длины также может не вызвать форк.

Train/validation разделены; позиции усредняются по блокам. SEM описателен: блоки одного ответа не независимы. `plot_progress.py` проверяет полноту завершённых train-шагов; `--expected-samples` равен batch × rollout n. Сдвиг позиции сам по себе не доказывает переход от exploration к verification. Проверка эффекта требует законченных S1/S2 и нескольких seeds.

## Проверки

```bash
.venv/bin/python -m pytest repo/experiments/qwen06/test_repro.py repo/experiments/qwen06/test_think.py -q
.venv/bin/python -m pytest repo/tests/test_flat_packed_context.py repo/tests/test_unseen_kv_reference.py -q
.venv/bin/python repo/experiments/qwen06/prepare.py --smoke-model
SMOKE=1 RUN_NAME=smoke-sanity bash repo/experiments/qwen06/run_rl.sh s2 models/smoke-qwen3-0.6b-special
```

Тесты проверяют fork/merge, position masks, пустые генерации и S2-награду 8/2. `tests/` на крошечной Qwen3 на CPU проверяют, что `flat_packed` воспроизводит log-probs и градиенты каждого вызова vLLM (2 блока × 3 пути), а Unseen-маска с multiverse-позициями совпадает с конкатенацией независимо посчитанных KV путей. Smoke использует disposable base-модель с необученными тегами, два вопроса, два rollout, 128 tokens, один update и искусственные награды для проверки ненулевого градиента. Это проверка инфраструктуры. Production запрещает модель с файлом `SMOKE_ONLY`.

## Прерываемая ВМ

`overnight.sh` последовательно запускает S1/S2, по 300 шагов из общего SFT `models/sft-epoch5/global_step_230`. Для другого расположения измените `MODEL` в скрипте. Каждый режим продолжает собственный checkpoint. Сохранение выполняется каждый шаг до validation; tracker заменяется атомарно. Восстановление финального шага повторяет validation без дополнительного update.

```bash
bash repo/experiments/qwen06/launch_night.sh
tmux attach -t parallel-r1-rl
# Отсоединиться: Ctrl+b, затем d.
.venv/bin/python repo/experiments/qwen06/night_status.py
tail -f runs/night/queue.log
```

Для автозапуска адаптируйте пользователя и абсолютные пути в `parallel-r1-night.service`, установите шаблон в `/etc/systemd/system`, выполните `sudo systemctl daemon-reload` и `sudo systemctl enable --now parallel-r1-night.service`.

```bash
# После устранения ошибки:
sudo systemctl restart parallel-r1-night.service
# Остановить очередь и отключить запуск после reboot:
sudo systemctl disable parallel-r1-night.service
tmux send-keys -t parallel-r1-rl C-c
```

Launcher не создаёт вторую очередь. Ошибка Python оставляет мёртвую tmux-панель с логом. Systemd `active (exited)` означает запуск tmux, не завершение обучения. tmux переживает разрыв SSH и сон локального компьютера; восстановление после reboot требует сохранённого диска ВМ. Удаление диска не покрывается механизмом. Теряется незавершённый шаг; побитовое совпадение семплирования не гарантируется.

Сравнение статьи и реализации, включая различия inference/training attention и loss на runtime-вставках: [PAPER_CODE_AUDIT.md](PAPER_CODE_AUDIT.md).
