# Передача проекта Parallel-R1: контекст для продолжения работы

Состояние на 2026-10-06 ~17:00 MSK. Документ самодостаточный: что за проект, где код и данные, как устроена инфраструктура,
как запускать эксперименты и бенчмарки, что уже сделано, что идёт сейчас и что дальше. Правила кода и git — в `AGENTS.md`.

## 1. Цель

Воспроизвести SFT-этап Parallel-R1 (arXiv 2509.07980, код https://github.com/zhengkid/Parallel-R1) и улучшить его минимальными
изолированными изменениями. Основная гипотеза проекта (mid-training exploration scaffold) проверяется на RL, SFT — cold start.
Пользователь также просит: на instruct-чекпоинте научить модель параллельному рассуждению без просадки в других доменах,
оценивая на широком пуле бенчмарков.

Требования пользователя к работе:
- код максимально короткий и понятный, без лишнего; изменения в коде авторов минимальны и перечислены в `docs/changes.md`;
- один эксперимент = одно изменение = одна ветка `exp/NN-name`; метрики и отчёт хранятся в ветке в `results/<NN-name>/`;
- после каждого эксперимента коммит и push;
- сравнение всегда на всех 5 бенчмарках (AIME24, AIME25, AMC23, MATH300, LIMO); решения — парным сравнением (`scripts/paired_compare.py`);
- можно использовать до 4 GPU H100;
- тексты для людей — на русском, без канцелярита.

## 2. Репозиторий и git

- Локально: `/Users/v.charkin/Documents/dev/projects/parallel-r1` (форк авторов, `upstream` = их GitHub, туда не пушить).
- `origin`: https://github.com/Mr-DarkTesla/Parallel-R1-repro, push только по SSH через порт 443:
  `ssh://git@ssh.github.com:443/Mr-DarkTesla/Parallel-R1-repro.git`, ключ `~/.ssh/id_ed25519_github`
  (в репозитории настроено `core.sshCommand`). Сеть до GitHub нестабильна — пушить в цикле с повторами.
- Ветки (все запушены, кроме 11/12 другой сессии):

| Ветка | Содержимое |
|---|---|
| `exp/01-sft-baseline` | ускорения SFT (обрезка паддинга, micro batch 4, без grad checkpointing, 2 воркера), различимая инициализация тегов; отчёт `results/README.md` |
| `exp/02-sft-prompt-positions` | 01 + позиции промпта подряд (баг авторов); **база для следующих экспериментов**; здесь же вся инфраструктура (runner, очередь, метрики) |
| `exp/03-sft-token-mean` | 02 + loss по токенам батча (без эффекта) |
| `exp/04-sft-seen` | 02 + Seen (`+data.parallel_structure=False`); лучший средний, не значимо; итоговая сводка `results/SUMMARY.md` |
| `exp/05-sft-summary-newline` | 02 + канонический `</Parallel>\n<Summary>` в данных (без эффекта) |
| `exp/06-sft-filter-malformed` | 02 + выброшены 38 битых примеров — **не запускался** |
| `exp/07-sft-mask-forced-tokens` | 02 + нет loss на токенах, которые вставляет роллаут — **не запускался** |
| `exp/10-sft-rollout-views` | 04 + копии веток ≥2 в «роллаут-видах» (`+data.rollout_path_views=True`); эквивалентность логитов проверена (3.6e-7); **не обучен** (был ~57 с/шаг) |
| `exp/11-len8k-control`, `exp/12-len8k-parathinker` | **созданы другой сессией** (worktree `../parallel-r1-exp11`, `../parallel-r1-exp12`), в моей работе не участвовали |
| `eval/4b-benchmarks` | бенчмарки 4B-чекпоинтов (`scripts/bench/`), результаты `results/bench4b/`, этот документ |

Отличия от кода авторов: `docs/changes.md` (по веткам). Итоговые цифры 0.6B: `results/SUMMARY.md` в `exp/04-sft-seen`.

## 3. Инфраструктура

Кластер `k8s_ml_MNTINFRA_3322`, namespace `shared-dzen-ml`. Доступ через Teleport:
`tsh login --proxy=tele.corp.mail.ru` и `tsh kube login k8s_ml_MNTINFRA_3322` (логин делает пользователь). kubectl иногда
отвечает `cluster ... not found` или обрывает поток — повторять с `timeout`.

| Ресурс | Что это |
|---|---|
| StatefulSet `vcharkin-exp-vm` (`infra/exp-vm.yaml`) | основной GPU-под, 4×H100, 108 CPU, 488Gi, `/dev/shm` 64Gi, PVC на `/work` |
| StatefulSet `vcharkin-exp-vm-extra` | создан **другой сессией** (1×H100, 26 CPU, 160Gi, тот же PVC `work`) |
| StatefulSet `vcharkin-setup-vm` (`infra/setup-vm.yaml`) | под без GPU (32 `vk.team/cpu.slots` = 8 CPU / 32Gi) для загрузок и установок, сейчас 0 реплик |
| PVC `vcharkin-parallel-r1-pvc` (`infra/parallel-r1-pvc.yaml`) | 200Gi, RWO, всё проектное: `/work` |
| `vcharkin-shared-vm` | старый личный под (PVC почти полон), сейчас 0, для проекта не используется |

Особенности кластера (каждая уже стоила времени):
- **Простаивающий GPU-под масштабируется в 0 автоматикой** примерно через 1.5–2 ч без нагрузки GPU. Загрузки и установки делать на
  `vcharkin-setup-vm` (PVC RWO: перед этим GPU-под выключить), GPU-под поднимать, когда сразу есть что запускать. Фиктивную нагрузку
  не делать.
- **Узлы могут выселить под** (`TaintManagerEviction`). Всё ценное — только на PVC `/work`.
- **Под без GPU** обязан запрашивать `vk.team/cpu.slots` (gatekeeper), 1 слот = 0.25 CPU / 1Gi. При 8Gi pip и `hf download` падают по OOM.
- **Интернета на подах нет**, PyPI-зеркала (`mirror.i`, `devpi`) не резолвятся. Hugging Face доступен через внутренний прокси:
  `export HF_ENDPOINT=http://huggingface.proxy` (быстро, до ~150 МБ/с; качать на поде с большой памятью, иначе OOM от page cache).
  Python-пакеты — из офлайн wheelhouse `/work/assets/wheelhouse_batch{1,2,3}` (`env/install_pod.sh`, lock `env/requirements.lock`).
  Недостающие пакеты качать на Mac через `pip download --platform ... --python-version 3.10` и заливать.
- **Стримы `kubectl exec` обрываются молча** на больших объёмах. Файлы забирать как `tar czf - ... | base64 -w0` с проверкой
  `tar tzf` и повторами; загрузку на под проверять по размерам файлов.
- CLI `ray` в окружении сломан (падает при импорте) — `ray stop` не вызывать.

## 4. Окружение на PVC

- `/work/venv`: python 3.10, torch 2.6.0+cu124, vllm 0.8.5.post1, transformers 4.51.3, flash-attn 2.7.4.post1, + nltk, langdetect,
  immutabledict (для IFEval). Активировать `source /work/venv/bin/activate`.
- `verl` установлен editable из `/work/setup-src` (worktree ветки 02). **Ловушка:** `python ../scripts/x.py` импортирует `verl` оттуда,
  а не из worktree эксперимента. `torchrun -m ...` из каталога `verl/` worktree берёт его код (так работает SFT). Для проверок кода
  эксперимента запускать с `PYTHONPATH=.` из `verl/` его worktree.
- Модели: `/work/assets/Qwen3-0.6B-Base`, `/work/assets/Qwen3-0.6B-Base-add-special-token` (с различимой инициализацией тегов),
  `/work/assets/models/{Parallel-SFT-Unseen, Parallel-R1-Unseen_Step_200, Qwen3-4B-Base-add-special-token, Qwen3-4B}`.
  Чекпоинты авторов в fp32 — в vLLM грузить с `dtype="bfloat16"`.
- Данные бенчмарков: `/work/assets/bench/{MMLU-Pro, ai2_arc, IFEval}`, собранные parquet: `/work/bench_data/{parallel,plain}/*.parquet`.
- IFEval-чекер: `PYTHONPATH=/work/assets/ifeval/pkg NLTK_DATA=/work/assets/ifeval/nltk_data` (код из lm-eval v0.4.9).
- Репозиторий на поде: `/work/parallel-r1` (ветки приходят через `git bundle` с Mac: `git bundle create b.bundle <branches> ^d58b0dd`,
  на поде `git fetch b.bundle "+refs/heads/*:refs/heads/*"`). Эксперименты работают в worktree `/work/exps/<name>`, бенчмарки — в
  `/work/bench-src` (ветка `eval/4b-benchmarks`).

## 5. Как запускать

Очередь: на каждую GPU свой цикл, берёт строки из `/work/queue/gpu<N>.txt`, лог `/work/queue/gpu<N>.log`:
`nohup bash -c "git -C /work/parallel-r1 show exp/02-sft-prompt-positions:scripts/queue_runner.sh | bash -s <N>" &`.
Добавить задачу = дописать строку в файл очереди. Очередь работает на поде сама, без подключения с Mac.

SFT-эксперимент 0.6B (SFT → eval авторов → LIMO → MATH300×8 → проверка тегов; повторный запуск продолжает с места остановки):
```
git -C /work/parallel-r1 show exp/02-sft-prompt-positions:scripts/start_experiment.sh | bash -s <branch> <name> [hydra overrides]
```
Результаты: `/work/runs/<name>/results/` (`sft_metrics.txt`, `eval_apo.txt`, `eval_limo.txt`, `eval_math300_x8.txt`,
`free_generation_tags.jsonl`). Сравнение: `scripts/compare_runs.py results/<a> results/<b>`;
парное: на поде из `verl/`: `python ../scripts/paired_compare.py /work/runs/<a> /work/runs/<b>`.
Время: SFT 0.6B ~25 мин на H100, eval ~35 мин.

Бенчмарки 4B (`eval/4b-benchmarks`):
```
cd /work/bench-src && bash scripts/bench/run_bench.sh <name> <model> <parallel|plain|thinking|no-thinking> <budget>
```
Бенчмарки: `apo` (AIME24/25 ×16, AMC23 ×16, MATH300 — набор авторов), `arc` (1172), `ifeval` (541), `mmlu_pro` (2000, стратифицированно,
seed 0), `limo` (817×4). Результаты `/work/bench/<name>/results/<bench>.json`; пересчёт метрик без генерации:
`bash scripts/bench/rescore_all.sh`; таблицы: `python scripts/bench/table.py <dir с run/*.json>`; диагностика IFEval:
`scripts/bench/ifeval_breakdown.py`.

Метрики (`scripts/bench/score.py`): `accuracy` — проверка авторов (`Final Answer:` в одной строке) / буква для ARC и MMLU-Pro;
`accuracy_robust` — также `\boxed{}`, ответ на следующей строке (math_verify), номер варианта; `with_parallel`,
`valid_tagged_responses` (`scripts/tag_validator.py`), `no_final_answer`, `truncated`, `mean_chars`; IFEval — strict/loose.
Проверка авторов занижает модели с другим форматом ответа (Qwen3-4B: MATH300 23 вместо 82) — сравнивать по `accuracy_robust`.

## 6. Что сделано

### SFT 0.6B (Qwen3-0.6B-Base, рецепт авторов, один сид)

| | Изменение | Итог |
|---|---|---|
| 01 | различимая инициализация тегов (в 0.6B у всех 6 тегов одинаковый эмбеддинг) | правильных тегов 1.7% → 67% |
| 02 | позиции промпта подряд (баг авторов: теги в инструкции принимались за блок) | 67% → 88%; без роллаута 0% → 71–80% |
| 03 | loss по токенам батча, нормировка до backward | без эффекта |
| 04 | Seen | Avg 10.6 против 9.7 у 02r; парно +0.66 [−0.75, 2.09] — не значимо |
| 05 | канонический разрыв перед `<Summary>` | без эффекта |

Шум eval большой (02 и 02r: AIME24 pass@16 10.0 против 3.3). Точность 0.6B около 10 против 31.7 у авторов на 4B.

### Бенчмарки 4B, бюджет 3k (готово), `accuracy_robust`, %

| Модель, режим | AIME24 | AIME25 | AMC23 | MATH300 | LIMO | ARC-C | MMLU-Pro | IFEval |
|---|---|---|---|---|---|---|---|---|
| Base + теги, обычный | 0.6 | 0.0 | 6.7 | 18.7 | 2.2 | 45.6 | 20.2 | 21.6 |
| Base + теги, параллельный | 3.3 | 4.0 | 17.0 | 31.6 | 7.4 | 34.9 | 17.2 | 24.9 |
| SFT авторов, обычный | 4.2 | 3.1 | 48.9 | 73.4 | 21.9 | 88.0 | 46.0 | 30.7 |
| SFT авторов, параллельный | 7.5 | 5.2 | 44.4 | 67.4 | 17.6 | 85.9 | 46.5 | 13.5 |
| RL step 200, обычный | 15.6 | 13.8 | 65.2 | 82.0 | 36.1 | 85.9 | 36.9 | 31.8 |
| RL step 200, параллельный | 17.5 | 15.6 | 62.3 | 82.0 | 36.4 | 82.7 | 39.6 | 17.4 |
| Qwen3-4B, non-thinking | 19.2 | 18.1 | 59.5 | 81.7 | 35.2 | 90.7 | 57.3 | 80.4 |
| Qwen3-4B, thinking | 0.0 | 1.7 | 24.8 | 57.3 | 3.7 | 92.4 | 48.4 | 81.0 |

- Протокол авторов воспроизведён: их SFT в параллельном режиме даёт AIME25 5.2 / AIME24 7.5 / AMC 44.4 / MATH 67.4 (в статье 5.2 / 8.5 / 41.7 / 71.5).
- Низкий IFEval моделей авторов — свойство моделей (Base, дообученная только на математике), а не пайплайна: на Qwen3-4B тот же
  пайплайн даёт 80.4; ошибки SFT настоящие (запятые при запрете, не повторяет запрос, заглавные буквы). Параллельный режим добавляет
  инструкцию авторов, которая конфликтует с IFEval, поэтому честная оценка — обычный режим.
- temperature 1.0 / top_p 1.0 для всех (протокол авторов); для Qwen жёстче рекомендованного. Greedy-проверка IFEval стоит в очереди.
- Thinking при бюджете 3k обрывается (40% ответов на MATH300) — смотреть 16k.

## 7. Что идёт сейчас (2026-10-06 ~16:55)

GPU-под `vcharkin-exp-vm-0` (4×H100):
- gpu0: `qwen3-4b-thinking-16k` (с 15:54, результатов ещё нет);
- gpu1: `11-len8k-control` — **задача другой сессии** (с 16:42); за ней 4 строки greedy IFEval (`/work/bench/greedy-ifeval/`);
- gpu2: `parallel-base-16k` (с 15:03, готово apo/arc/ifeval);
- gpu3: `plain-base-16k` (с 16:10, готово apo/arc/ifeval/mmlu_pro).
Готовые 16k: `parallel-sft-16k`, `parallel-rl200-16k`, `plain-sft-16k`, `plain-rl200-16k`, `qwen3-4b-nothinking-16k`.
На PVC также `/work/runs/12-len8k-parathinker` (другая сессия).

Забрать все результаты бенчмарков:
```
kubectl exec -n shared-dzen-ml vcharkin-exp-vm-0 -- bash -c 'cd /work/bench && tar czf - */results/*.json | base64 -w0' > r.b64
base64 -d -i r.b64 > r.tgz && tar tzf r.tgz >/dev/null && tar xzf r.tgz -C results/bench4b
```
(затем разложить `*/results/*.json` в `results/bench4b/<run>/`), прогнать `rescore_all.sh` на поде перед сбором, если менялся `score.py`.

## 8. Что дальше

1. Дождаться 16k и greedy IFEval, собрать таблицу 3k vs 16k, закоммитить в `eval/4b-benchmarks` (`results/bench4b/`).
2. Instruct-направление (запрос пользователя): SFT параллельного формата поверх Qwen3-4B / Qwen3-0.6B instruct без просадки:
   оценивать на этом же пуле (математика + ARC, IFEval, MMLU-Pro, LIMO) против исходного instruct; рычаги — самодистилляция трасс
   самой instruct-моделью, примесь общих данных, привязка поведения к инструкции в промпте, мягкий режим (lr, эпохи, LoRA), WiSE.
3. SFT 0.6B: незапущенные 06, 07, 08 (`trainer.total_epochs=3`), 09 (`optim.lr=2e-5`), 10 (ускорить: маска строится на CPU, 57 с/шаг).
   Для решений: 2 сида на финалистов, dev-набор вместо многократно просмотренных тестов, MATH300×8 и LIMO×8.
4. Идеи (оценки Codex): instruct-инициализация (+4–12), учебные трассы под размер ученика на MATH (+1–5), rejection sampling (+0–3),
   примесь CoT без тегов (+0–2). 4B Seen-чекпоинтов авторы не публиковали — при необходимости обучать самим (4 GPU, FSDP).

## 9. Ловушки, на которые уже наступали

- Скрипт авторов отдаёт новым токенам неиспользуемые строки эмбеддингов; в Qwen3-0.6B они одинаковые → использовать
  `scripts/add_special_tokens.py` (инициализация средним эмбеддингом кусков тега).
- Парсер структуры авторов видит теги в тексте инструкции промпта (исправлено в 02).
- Шаблон авторов делит loss на число микробатчей после `backward()` (исправлено в 03; на результат не повлияло из-за клиппинга).
- `fsdp_parallel_sft_trainer` при `use_remove_padding=True` выкидывает 4D-маску — для Unseen не включать.
- verl валидация по умолчанию перемешивает данные: в бенчмарках `data.validation_shuffle=False` (ключ существует, без `+`).
- Forward HF может менять переданные маску/позиции на месте — в проверках передавать копии.
- Новый `run_experiment.sh` с `set -e`: любая ошибка останавливает эксперимент; повторный запуск продолжает со следующего этапа.
