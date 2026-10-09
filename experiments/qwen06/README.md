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
.venv/bin/python -m pytest repo/experiments/qwen06/test_repro.py -q
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
