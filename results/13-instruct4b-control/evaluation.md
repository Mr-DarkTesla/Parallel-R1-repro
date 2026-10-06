# Оценка exp13: обычный режим, thinking 16k, параллельная математика (evaluation, доработки eval_finalize и eval_repairs, 2026-10-07)

Статус: код, dev (296) и CPU-проверки готовы к ревью родителя. GPU не запускался, моделей SFT ещё нет. Commit и push не делались.
Доработка eval_finalize: детерминированный IFEval opt-in (§3.2, §5), пересборка dev из `dev_untouched` (§4), CPU-проверки на
реальном C0 (§5). Логи: `outputs/instruct4b-2026-10-06/eval_finalize/`.
Доработка eval_repairs (находки F1–F6 независимого ревью `outputs/.../eval_review/review.md`): узкий `--cross-prompt`, вывод по
источникам и метка относительно предложенного порога, настоящая проверка импорта, белый список REUSE с происхождением, отказ при
одинаковых именах кандидатов и отсутствующих метаданных, блокировка и атомарность `meta.json`/`rows`, проверка при возобновлении
(§2, §5, §5a). Логи: `outputs/instruct4b-2026-10-06/eval_repairs/`.

## 1. Что сделано

| файл | назначение |
|---|---|
| `scripts/bench/score.py` | необязательный 4-й аргумент `rows.jsonl`: одна строка на ответ; необязательная переменная `SCORE_IFEVAL_SEED` (§3.2). Без них сводка и CLI прежние |
| `scripts/instruct4b_eval/make_eval_data.py` | dev-parquet (plain/parallel), метаданные срезов для замороженных parquet, `manifest.json` |
| `scripts/instruct4b_eval/generate.py` | `generate_plain.py` с одним изменением: seed строки равен номеру повтора (повтор 0 = seed 0) |
| `scripts/instruct4b_eval/run_eval.sh` | одна модель, режим, набор и GPU; `meta.json` (с коммитом), сводки, `rows/`; проверки импорта, шаблона, REUSE, возобновления |
| `scripts/instruct4b_eval/paired_compare.py` | парное сравнение по задачам, bootstrap 10 000 (seed 0), по источникам и срезам |
| `scripts/instruct4b_eval/test_eval.py` | CPU-тест на синтетике: проверяет поведение кода, это не данные бенчмарка |

Поля `rows.jsonl`:
- `row`, `source`, `problem_id` (`extra_info.id`; если его нет, то `<source>/<порядок промпта>`), `sample`;
- `problem` и `input` (промпт, отрисованный шаблоном), чтобы проверять когорту;
- `acc` (строгий парсер), `acc_robust`;
- для IFEval: prompt strict/loose, списки `inst_level_*`, `instruction_id_list`;
- `parallel`, `tags`/`correct_tags`/`valid_tags`, `no_final_answer`, `chars`;
- `tokens` и `truncated`, если они есть в дампе (в дампе rollout их нет: `null`).

Бюджет, режим, сэмплинг и `ifeval_scorer_seed` записывает драйвер в `meta.json`. `paired_compare` требует их равенства.

## 2. Протокол

- **Обычный режим.**
  - Нативный шаблон Qwen3 с `enable_thinking=False`, бюджет 16384, T=1.0, top_p=1.0.
  - Math/MC: заголовок авторов без параллельного абзаца. IFEval: исходный промпт без математического заголовка.
- **Thinking.** То же с `enable_thinking=True`, 16384.
- **Параллельный режим.**
  - Только математика: промпт авторов с параллельным абзацем и настоящий rollout (`eval_rollout.sh`), `PARALLEL_ROLLOUT_ENABLE_THINKING=false`.
  - Драйвер требует в логе строку `Parallel rollout chat template kwargs: {'enable_thinking': False}`.
  - Параллельный IFEval не входит в оценку сохранения навыков.
- **Проверка шаблона по дампу.** В no-thinking и parallel каждый промпт должен содержать пустой `<think>\n\n</think>`, в thinking ни один не должен.
- **Импорт.**
  - `PYTHONPATH=$repo/verl` (тот же для `score.py` и rollout).
  - Проверка запускается из `/`, вне каталога репозитория, с тем же `PYTHONPATH`: `verl.__file__ == $repo/verl/verl/__init__.py`.
    Прежняя проверка из `verl/` была пустой: текущий каталог стоит первым в `sys.path`, и она проходила даже без `PYTHONPATH`
    (проверено на поде; новая без `PYTHONPATH` падает, потому что тогда импортируется редактируемая установка `/work/setup-src`).
  - Наблюдение: `python ../scripts/bench/score.py` из `verl/` без `PYTHONPATH` импортировал `verl` из `/work/setup-src`, потому что `sys.path[0]` указывает на каталог скрипта.
- **Замороженный пул.**
  - Тот же `generate_plain.py`, что у готовых прогонов Qwen3-4B. Поэтому их дампы переиспользуются (`REUSE=`) без генерации.
  - **REUSE разрешён только для двух готовых прогонов C0** (белый список в `run_eval.sh`, проверка до любой оценки):
    `/work/bench/qwen3-4b-nothinking-16k` для no-thinking и `/work/bench/qwen3-4b-thinking-16k` для thinking, только `frozen`,
    модель `/work/assets/models/Qwen3-4B`, бюджет 16384. Другой каталог (3k, 8k, чужой режим), модель, бюджет, dev или parallel — отказ.
  - **Происхождение** (журналы очереди, архив `outputs/.../metrics/archive/queue/`): no-thinking — `gpu3.log`, 2026-10-06
    15:01:10–15:38:17, exit 0; thinking — `gpu0.log`, 15:54:08–22:04:09, exit 0; команда
    `cd /work/bench-src && bash scripts/bench/run_bench.sh qwen3-4b-<nothinking|thinking>-16k /work/assets/models/Qwen3-4B <mode> 16384`.
    Коммит `/work/bench-src` тех прогонов в журналах не записан. Строка происхождения пишется в `meta.json` (`reuse_provenance`,
    `reuse_source_logs`) и в `<bench>.log` вместе с путём исходного лога.
  - Перед оценкой каждого бенчмарка лог исходного прогона `<REUSE>/<bench>.log` должен содержать `model='/work/assets/models/Qwen3-4B'`
    и `max_seq_len=18432` (= 16384 + 2048 в `generate_plain.py`). Это запись конфигурации vLLM, а не вывод из длин ответов:
    максимум `tokens` ≤ бюджета бюджет не доказывает и не используется.
- **Dev.** `generate.py` (seed равен номеру повтора).
- **Выбор.** Лучший бюджет не выбирается: везде 16384.

## 3. Наблюдения (данные)

1. **Повторы в старых plain-прогонах не независимы.**
   - `generate_plain.py` даёт каждой строке `seed=0`, поэтому повторы одного промпта различаются только из-за недетерминизма батча.
   - No-thinking 16k, различных ответов на 16 строк: AIME24 14.3, AIME25 10.3, AMC23 8.5; у 18% задач AMC все 16 ответов одинаковы. В thinking около 15.5. В parallel rollout (без seed) 16 из 16.
   - Парный bootstrap по задачам остаётся корректным, но фактическое число сэмплов меньше числа строк. «avg@16» в plain-режиме нельзя читать как 16 сэмплов.
2. **Проверка IFEval недетерминирована.**
   - Тот же дамп при неизменном коде: 79.85 / 79.67 / 79.85.
   - Строка 22: `letter_frequency` с `letter="!"`; lm-eval подставляет случайную букву. Строка 511: `langdetect` без seed.
   - `random.seed(0)` + `DetectorFactory.seed=0` дают 79.85 в 4 из 4 запусков.
   - Установленный checker на реальных ответах C0 (CPU, 40 разных случайных состояний): строка 22 (key 1129) даёт все четыре
     сочетания strict/loose (23/9/7/1), строка 511 (key 3653, `language=ne`) — три (36/3/1).
   - **Исправление (opt-in, eval_finalize).** `SCORE_IFEVAL_SEED=<int>`: перед проверкой каждого промпта `random.seed("<seed>/<doc key>")`
     и `DetectorFactory.seed=<seed>` (langdetect пересевает себя на каждый вызов). Seed на промпт: исход одной строки не зависит от
     порядка строк и других ответов. Без переменной `score.py` работает как раньше (несидированно). `run_eval.sh` всегда ставит 0 —
     это один фиксированный протокол для C0 и всех кандидатов, не настройка.
   - **Прежние агрегаты** (несидированный checker) остаются историческими. Дельты считаются только против C0, переоценённого
     `run_eval.sh REUSE=` с той же настройкой; `paired_compare` иначе отказывает. На этом дампе C0 сидированные сводки совпали с
     историческими JSON (IFEval 79.85), но это наблюдение для одного дампа, не паритет метрики: несидированная оценка давала и 79.67.
3. **Переоценка готового дампа Qwen3-4B no-thinking 16k новым `score.py` с `rows`** (CPU, импорт `verl` из checkout): без seed сводки apo, arc, mmlu_pro и limo равны исходным JSON; ifeval отличается на 1 промпт, как в п.2. С `SCORE_IFEVAL_SEED=0` две переоценки дали одинаковые строки по всем 5 бенчмаркам (§5).
4. **Совпадение замороженных наборов с исходными данными.**
   - Выборка MMLU-Pro 2000 воспроизводится кодом `make_bench_data.py`: тексты совпадают, если не считать ведущих пробелов в 47 вопросах.
   - ARC-test и IFEval совпадают построчно.
   - MATH300 найден в MATH test по точному тексту у 290 из 316 задач. По ним даны срезы type/level; у остальных 26 срезов нет.
5. **Близкие дубли** (difflib > 0.8) между выборкой MATH dev (501) и замороженной математикой:
   - 7 переформатированных задач LIMO (старые AIME);
   - 14 «шаблонных братьев» MATH300 (та же форма, другие числа).
   - Порог их не разделяет (0.848 — реальный дубль, 0.852 — нет), поэтому удалены все: 19 задач (некоторые совпали с несколькими). Осталось 482.

## 4. Dev (только для выбора; пересобран на CPU 2026-10-07 из `filter/data/dev_untouched.parquet`, 296)

| набор | источник | задач × сэмплов | срезы |
|---|---|---|---|
| gsm8k_dev | GSM8K train, отложенный фильтром до отбора (вне всех плеч), без просмотренной строки 179 (`gsm8k-train/224`) | 296 × 4 | — |
| math_dev | MATH test без точных и близких совпадений с AIME/AMC/MATH300/LIMO, страт. по type, seed 1 | 482 × 2 | 7 type, 5 level |
| arc_dev | ARC-Challenge validation (не test) | 299 × 4 | — |
| mmlu_pro_dev | MMLU-Pro test вне замороженных 2000 (по id и тексту), страт. по category, seed 1 | 999 × 1 | 14 category, src |

- **Пересечения по точному тексту** (lowercase, схлопнутые пробелы) dev с каждым замороженным набором и с `control_full`: везде 0.
- **ID и манифест.** Актуальные данные: `outputs/.../eval_finalize/data/` (`manifest.json`, `dev/{plain,parallel}/*.parquet`,
  `meta/{dev,frozen}/*.jsonl`); их исполнитель копирует в `/work/bench_data/instruct4b/eval`.
- **Сверка с прежней сборкой по ID** (`eval_finalize/data_check.log`): отличается только удалённый `gsm8k-train/224`; math_dev, arc_dev,
  mmlu_pro_dev, список 19 удалённых близких дублей и метаданные замороженного пула те же. Прежняя сборка (297) сохранена отдельно в
  `outputs/.../evaluation/data/` и не используется.
- **IF-dev: пробел.** Локально есть только 541 промпт IFEval (test), train/val нет. IFEval-541 используется только как диагностика, не для выбора. Регресс следования инструкциям на dev не измеряется.
- **Точность dev.** Dev служит для ранжирования и для того, чтобы ловить крупные регрессии. На ARC dev (299 задач) подтвердить отклонение ≤2 п. в общем случае нельзя. Финальная проверка — парные CI на замороженном пуле. Повторно просмотренные тесты не считаются независимым подтверждением.

## 5. Статистика

- **Отказ без вывода чисел**, если:
  - различается протокол (suite, mode, budget, T, top_p, generator, prompts, `ifeval_scorer_seed`; прогон без него = несидированный,
    совпадает только с таким же);
  - различается набор бенчмарков или общих бенчмарков нет;
  - по строкам не совпадают `source`, `problem_id`, текст задачи, отрисованный промпт или `sample`;
  - внутри одного источника задачи имеют разное число повторов;
  - у двух `--cand` одинаковое имя каталога (раньше один молча затирал другой);
  - `--meta-dir` указан, но в нём нет файла сравниваемого бенчмарка (например, dev-метаданные для замороженного прогона);
  - прогон помечен `unversioned_test_only` (CPU-тест без git, §5a), если не задан `EVAL_ALLOW_UNVERSIONED=1`.
- **Смешанный APO.** Он содержит AIME/AMC ×16 и MATH300 ×1, поэтому равенство повторов проверяется внутри источника, а итоги дополнительно даются по каждому источнику.
- **Порог применяется к каждому источнику.** Рабочий критерий «не более 2 п. на основном бенчмарке» относится к AIME24, AIME25, AMC23
  и MATH300 по отдельности (и к ARC, MMLU-Pro, IFEval, LIMO). Смешанный APO описательный: MATH300 даёт 316 из 416 задач, и −5 п. на
  AIME24 сдвигают смесь примерно на 0.4 п. `paired_compare` печатает смесь и каждый источник; у смеси пометка «blend, descriptive».
- **Метка относительно порога** (только печать, не гейт; порог 2 п. — рабочее предложение, пользователь его не подтвердил):
  нижняя граница CI ≥ −2 — `within`; верхняя < −2 — `below`; иначе `inconclusive`. Точка в пределах 2 п. при CI, заходящем за −2, —
  `inconclusive`, а не «сохранено». AIME24/AIME25 (по 30 задач) и AMC23 (40) слишком малы, чтобы подтвердить малый спад: ожидаемая
  ширина CI там больше порога, поэтому для них ожидается `inconclusive` даже без изменения модели; они диагностические, вывод о
  сохранении по ним не делается. В `--cross-prompt` метка не печатается.
- **Расчёт.** Сначала среднее внутри задачи, затем разность средних. Bootstrap 10 000 по уникальным задачам, seed 0.
- **Отношения** (instruction-level IFEval): числитель и знаменатель ресэмплируются вместе.
- **Что выводится.**
  - Основная метрика: `acc_robust`; для IFEval — prompt-level strict.
  - Остальные с CI: strict, prompt loose, inst strict, truncated, доля `<Parallel>`, valid_tags, no_final.
  - Также средние токены и доля задач с разным исходом.
- **Срезы** (отчёт, не гейт): категория MMLU-Pro, type/level MATH, группы инструкций IFEval.
- **`--cross-prompt`.** Только no-thinking (prompts `<data>/plain`) против parallel (`<data>/parallel` того же каталога данных), в
  любом порядке base/cand. Thinking против no-thinking или parallel и parallel против parallel отвергаются и с флагом.
  - По строкам совпадают `source`, `problem_id`, `sample`. Текст задачи сравнивается после заголовка: строка делится по первому
    `Problem:` (не последнему, так что `Problem:` внутри задачи сравнивается целиком); заголовок parallel без параллельного абзаца
    («During the reasoning process» … до «End your response») должен равняться заголовку plain, как в `make_bench_data.py`/`make_eval_data.py`.
    Поэтому другая задача на той же позиции (позиционные id замороженного пула) — отказ.
  - Сравниваются только общие бенчмарки (остальные в `not_compared`); если общих нет — отказ.
  - Бюджет и сэмплинг совпадают только номинально: rollout использует `max_path_response_length = max(budget, 4096)`, до 4 параллельных
    итераций, `max_prompt_length = 2000` с левым усечением и не задаёт seed; plain — `max_model_len = budget + 2048`, seed по строке.
- **Сиды обучения.**
  - Несколько `--cand` дают отдельный результат для каждого сида (печатаются отдельными строками; имена каталогов должны различаться).
  - `seeds_pooled` — среднее по сидам на задачу. Его интервал условен на эти сиды: дисперсия между сидами в него не входит, её показывает разброс результатов по сидам.
  - Два сида не считаются независимыми сэмплами. Сейчас `trainer.seed` не используется, поэтому второй сид обучения ещё не реализован.
- **Проверка на реальных дампах** (CPU, `eval_finalize/integration*.log`). Дампы C0 no-thinking 16k дважды переоценены
  `run_eval.sh REUSE=` (seed 0, данные новой сборки), затем `paired_compare` со срезами замороженного пула: 90 из 90 сравнений
  (каждая метрика, источники AIME24/AIME25/AMC23/MATH300, 12 срезов MATH, 14 MMLU-Pro, 9 групп IFEval) — разность 0, CI [0, 0],
  0% расходящихся задач; строки `rows/*.jsonl` обеих переоценок совпадают. Повторы APO: AIME/AMC ×16, MATH300 ×1 — принято.
  Это проверка выравнивания и join метаданных, не результат по модели. Thinking-дампы C0 этой версией не переоценивались.
- **Отказы на реальных данных.** Thinking-16k против no-thinking-16k отвергнут и без `--cross-prompt` (`protocol differs {'mode': ...}`),
  и с ним (eval_repairs, §5a).
- **Синтетический тест** отвергает перестановку строк, другую когорту задач, неравные повторы (в том числе внутри одного источника
  при допустимых разных числах между источниками), отсутствующий бенчмарк, другой бюджет, другой и отсутствующий seed скорера.
  Ожидаемые дельты совпали: −12.5, +37.5, pooled +12.5.
- **Тест seed на реальных строках** (под, CPU): строки 22 и 511 с ответами C0 зависят от случайного состояния checker; с
  `SCORE_IFEVAL_SEED=0` три оценки и оценка в другом порядке с другими соседями дают одинаковые исходы по каждому промпту; схема
  сводки и `rows` без переменной та же. Мутация (score.py игнорирует переменную) проваливает тест 3 из 3. Вне пода тест
  печатает `SKIPPED`.

## 5a. Надёжность прогонов (eval_repairs)

- **Код и `meta.json`.** Отслеживаемые файлы `scripts/` и `verl/` должны быть закоммичены (неотслеживаемые, например `__pycache__`, не
  учитываются: `.gitignore` нет). `meta.json` хранит `commit`; поле `uncommitted` убрано, грязное дерево — отказ. Повторный запуск в тот
  же каталог при другом коммите или настройках — отказ, смешивания версий кода нет. Если `git` недоступен, `commit` = `null`, и запуск
  отвергается; `EVAL_ALLOW_UNVERSIONED=1` разрешён только вместе с REUSE (CPU-тест копии, без GPU), тогда в `meta.json`
  `"unversioned_test_only": true`, а `paired_compare` такой прогон по умолчанию отвергает.
- **Блокировка.** `meta.json` создаётся и сверяется под `fcntl.flock` (`meta.json.lock`), запись через tmp + `os.replace`. Два процесса
  одного имени с разными `BENCHES` (thinking на двух GPU) стартуют одновременно без гонки. Один бенчмарк — один процесс.
- **Атомарное завершение.** `score.py` пишет `results/<bench>.json.tmp` и `rows/<bench>.jsonl.tmp`; после успеха они переименовываются,
  `rows` последним (его наличие означает «готово»). `score.py` не менялся для этого.
- **Возобновление.** Если `rows/<bench>.jsonl` есть, перед пропуском проверяются число строк, `source`, текст задачи, `sample`,
  `problem_id` против текущего parquet и наличие сводки. Несовпадение — отказ с инструкцией: отложить `rows/<bench>.jsonl` и
  `results/<bench>.json` (`mv … .stale-<дата>`) и перезапустить; другие файлы прогона не трогаются.
- **Незавершённая попытка.** Ничего не удаляется: прежние `<bench>.log`, дамп `<bench>.jsonl` (plain) и каталог `<bench>/` (rollout)
  переименовываются в `*.incomplete-<время>`. Место на `/work` при повторах parallel-прогонов нужно следить вручную.
- **Ray.** `RAY_TMPDIR=/tmp/ray_<name>_<pid>`: свой кластер на процесс, без общих каталогов. Сокет Ray
  `<dir>/session_<дата>_<pid>/sockets/plasma_store` ограничен 107 байтами, поэтому в parallel-режиме путь длиннее 45 символов — отказ
  до старта (имя прогона ≤ 28 символов при 7-значном pid, например `15-random-control-frozen-par`).
- **Проверено на поде** (CPU, `vcharkin-exp-vm-extra-0`, копии в `/tmp/eval_repair_vk1007` с git и без, CUDA скрыт, REUSE реальных
  дампов C0 только на чтение; `eval_repairs/wrapper_tests_pod.log`, `FAILS=0`):
  - 9 неверных REUSE (чужой режим, 3k, 8k, бюджет 8192, другая модель, dev, parallel, путь со `/`) отвергнуты до оценки, каталог не создан;
  - без git: отказ; с `EVAL_ALLOW_UNVERSIONED=1` без REUSE — отказ до генерации; с REUSE — `commit: null`, `unversioned_test_only`;
  - два процесса одного имени (`apo ifeval` и `arc`) одновременно: оба успешны, один `meta.json` с коммитом и происхождением, `*.tmp` не осталось;
  - возобновление пропускает готовые бенчмарки, не трогая `rows`; усечённый `rows` и `rows` с другой задачей на той же позиции
    отвергнуты с инструкцией, после неё бенчмарк переоценён, остальные файлы целы;
  - процесс, убитый после REUSE-проверки (до записи `*.tmp`), не оставил готовых `rows`; повтор архивировал лог и завершился.
    Убийство посреди записи `*.tmp` не воспроизведено, атомарность следует из переименования;
  - незакоммиченная правка и другой коммит для существующего прогона — отказ; при исходном коммите возобновление проходит;
  - `paired_compare` двух переоценок C0 (apo, arc, ifeval, срезы frozen): 64 дельты, все 0; печать смеси и AIME24/AIME25/AMC23/MATH300;
    dev-метаданные для frozen, одинаковые имена, thinking против no-thinking (с флагом и без) — отказ;
  - длинное имя parallel-прогона — отказ до `meta.json`.
  Сам запуск Ray с новым `RAY_TMPDIR` не проверялся (нужен GPU-прогон).

## 6. Команды

Каталог `R=/work/exps/13-instruct4b-evaluation` — отдельный detached worktree на коммите оценки (`EVAL_ALLOWED.json`), venv
активирован, `cd $R`. Код в `R` должен быть закоммичен (§5a). Рабочее дерево обучения `/work/exps/13-instruct4b-control` (4e02d79)
не переключать. Пути моделей:
- `C0=/work/assets/models/Qwen3-4B` (исходная);
- `P=/work/assets/models/Qwen3-4B-instruct-add-special-token` (подготовленная, без SFT);
- `M=/work/runs/<arm>/model`.

Данные: исполнитель копирует готовую CPU-сборку `outputs/instruct4b-2026-10-06/eval_finalize/data/` в
`/work/bench_data/instruct4b/eval`. Она получена эквивалентной командой (входы с `/tmp`, см. `eval_finalize/commands.md`);
пересобирать не нужно. Тест после копирования:

```bash
# эквивалент сборки: cd $R/verl && python ../scripts/instruct4b_eval/make_eval_data.py /work/assets/bench \
#   /work/bench_data/instruct4b/sft/dev_untouched.parquet /work/bench_data/instruct4b/sft/control_full.parquet \
#   /work/bench_data/plain /work/bench_data/instruct4b/eval && cd $R
(cd verl && IF=/work/assets/ifeval CUDA_VISIBLE_DEVICES= PYTHONPATH=$PWD:$IF/pkg NLTK_DATA=$IF/nltk_data python ../scripts/instruct4b_eval/test_eval.py)
```

C0, замороженный пул из готовых дампов (CPU, около 1 мин; `run_eval.sh` сам ставит `SCORE_IFEVAL_SEED=0`, это и есть база для всех дельт;
другие пути REUSE отвергаются, §2):

```bash
REUSE=/work/bench/qwen3-4b-nothinking-16k bash scripts/instruct4b_eval/run_eval.sh c0-frozen-nothink $C0 frozen no-thinking 16384
REUSE=/work/bench/qwen3-4b-thinking-16k   bash scripts/instruct4b_eval/run_eval.sh c0-frozen-think   $C0 frozen thinking 16384
```

GPU, по одной задаче на GPU (`CUDA_VISIBLE_DEVICES=<g>`), имя `<arm>-<suite>-<mode>`:

```bash
bash scripts/instruct4b_eval/run_eval.sh c0-dev-nothink   $C0 dev no-thinking 16384
bash scripts/instruct4b_eval/run_eval.sh c0-dev-think     $C0 dev thinking 16384
bash scripts/instruct4b_eval/run_eval.sh prep-dev-nothink $P  dev no-thinking 16384   # подготовка без SFT ничего не меняет?
bash scripts/instruct4b_eval/run_eval.sh prep-dev-par     $P  dev parallel 16384      # parallel без SFT, база для плеч в parallel
bash scripts/instruct4b_eval/run_eval.sh prep-frozen-par  $P  frozen parallel 16384
# каждое плечо X после экспорта /work/runs/X/model:
bash scripts/instruct4b_eval/run_eval.sh X-dev-nothink $M dev no-thinking 16384
bash scripts/instruct4b_eval/run_eval.sh X-dev-par     $M dev parallel 16384
bash scripts/instruct4b_eval/run_eval.sh X-dev-think   $M dev thinking 16384
# после записанного решения по dev:
bash scripts/instruct4b_eval/run_eval.sh X-frozen-nothink $M frozen no-thinking 16384
bash scripts/instruct4b_eval/run_eval.sh X-frozen-par     $M frozen parallel 16384
# финалист, thinking на двух GPU в одном каталоге:
BENCHES=limo                      bash scripts/instruct4b_eval/run_eval.sh X-frozen-think $M frozen thinking 16384   # GPU0
BENCHES="apo arc ifeval mmlu_pro" bash scripts/instruct4b_eval/run_eval.sh X-frozen-think $M frozen thinking 16384   # GPU1
```

Сравнения (CPU), `E=/work/bench/instruct4b`, `D=/work/bench_data/instruct4b/eval/meta`:

```bash
C="python scripts/instruct4b_eval/paired_compare.py"
$C --base $E/c0-dev-nothink   --cand $E/X-dev-nothink    --meta-dir $D/dev    --out $E/cmp/X-dev-nothink.json
$C --base $E/c0-dev-think     --cand $E/X-dev-think      --meta-dir $D/dev    --out $E/cmp/X-dev-think.json
$C --base $E/prep-dev-par     --cand $E/X-dev-par        --meta-dir $D/dev    --out $E/cmp/X-dev-par.json
$C --base $E/X-dev-nothink    --cand $E/X-dev-par        --meta-dir $D/dev --cross-prompt --out $E/cmp/X-dev-par-vs-plain.json  # общие: gsm8k_dev, math_dev
$C --base $E/c0-dev-nothink   --cand $E/prep-dev-nothink --meta-dir $D/dev    --out $E/cmp/prep-dev-nothink.json
$C --base $E/c0-frozen-nothink --cand $E/X-frozen-nothink --meta-dir $D/frozen --out $E/cmp/X-frozen-nothink.json
$C --base $E/prep-frozen-par  --cand $E/X-frozen-par     --meta-dir $D/frozen --out $E/cmp/X-frozen-par.json
$C --base $E/c0-frozen-nothink --cand $E/X-frozen-par    --meta-dir $D/frozen --cross-prompt --out $E/cmp/X-frozen-par-vs-c0-plain.json
# два сида обучения одного плеча: --cand $E/X-s0-... --cand $E/X-s1-... (имена каталогов должны различаться);
# сейчас тренер использует только seed 0 (trainer.seed не применяется), второго сида обучения пока нет
```

## 7. Расписание на под с 2×H100

Обучение занимает оба GPU пода; оценка в это время на нём не идёт. Оценка: одна задача на GPU.

Источники оценок времени:
- замеры 2026-10-06 на одной H100: обычный режим, весь пул, 16k — около 37 мин; rollout 16k, весь пул — 56–70 мин; thinking 16k — около 6.2 ч, из них LIMO около 3.3 ч;
- для dev — **оценки, не замеры**.

| шаг | GPU0 | GPU1 | время (оценка) |
|---|---|---|---|
| 0 (C0, любой свободный под; можно до или после SFT) | c0-dev-nothink → prep-dev-nothink → prep-dev-par | c0-dev-think | около 1–2 ч |
| 0b | prep-frozen-par | — | около 1 ч |
| 1 | SFT плеча X (оба GPU, по рецепту) | | по рецепту |
| 2 | X-dev-nothink → X-dev-par | X-dev-think | около 1–2 ч |
| 3 | решение по dev записать в отчёт до открытия замороженного пула | | — |
| 4 | X-frozen-nothink | X-frozen-par | около 1 ч |
| 5 (только финалист) | X-frozen-think: limo | X-frozen-think: остальное | около 3.3 ч |

- Любая GPU-задача — только после `MIGRATION_READY.json` (проверенный перенос на A/B).
- Владельцы (`EVAL_PLAN.json`): A (executor) — общие оценки C0/P и плечо 13-control; B (matrix) — 14-filtered и 15-random-control.
  Matrix копирует общие rows/meta C0/P с A в свой каталог и не повторяет их на GPU.
- CPU-переоценка C0 (`REUSE`) GPU не занимает.

## 8. Передача после eval_finalize

Сделано: п.1–3 прежней передачи (детерминированный IFEval opt-in, dev 296, CPU-тесты и self-сравнение на `vcharkin-exp-vm-extra-0`,
`/tmp`, CUDA скрыт). Остаётся, без GPU не проверено:
- что `<think>` остаётся во входе дампа rollout (вход декодируется с `skip_special_tokens=True`; в Qwen3 `<think>` не помечен как special, но это не перепроверено);
- что `PARALLEL_ROLLOUT_ENABLE_THINKING` доходит до Ray-воркеров.
Обе проверки падают закрыто (драйвер останавливается), их результат виден в первом parallel-прогоне.

## 9. Ограничения и недостающие домены

- **Покрытие.** Пул (математика, ARC, MMLU-Pro, IFEval) не покрывает код, многоязычность и открытую полезность. Утверждать «сохранение всех навыков» нельзя.
- **IF-dev отсутствует.** IFEval-541 — только диагностика.
- **Модель.** Нативная гибридная Qwen3-4B (thinking/no-thinking в одном чекпойнте, апрель 2025), не Instruct-2507.
- **Thinking 16k обрывается** (доля `truncated` в прежних сводках C0 thinking-16k): AIME24 35.0%, AIME25 47.7%, AMC23 8.0%, MATH300 1.6%,
  LIMO 18.0%, MMLU-Pro 2.6%, ARC и IFEval 0. Строгий парсер там почти нулевой на AIME (нет «Final Answer:»), основная — `acc_robust`.
- **Замороженный baseline** сэмплирован с seed 0 на каждую строку (§3.1): повторы AIME/AMC/LIMO не независимые сэмплы.
- **IFEval-агрегаты до 2026-10-07** получены несидированным checker и остаются историческими (§3.2).
- **Сиды обучения.** Два сида финалиста публикуются отдельно, не усредняются в один результат. `trainer.seed` сейчас тренером не
  используется: фактически обучен только seed 0; второй сид обучения не реализован и не заявляется, пока не будет реализован seed сэмплера данных.
- **Порог 2 п.** — рабочее предложение, пользователь его не подтвердил. AIME/AMC слишком малы для уверенного допуска малого спада (§5).
- **Parallel против plain** (`--cross-prompt`): одинаковы задачи и номинальный бюджет, но не фактические ограничения длины и seed (§5).
- **Неизвестно до первого GPU-прогона:** сохраняется ли `<think>` во входе дампа rollout; доходит ли `PARALLEL_ROLLOUT_ENABLE_THINKING` до
  Ray-воркеров; работает ли Ray с новым `RAY_TMPDIR` (путь с pid) на поде — проверено только ограничение длины, не запуск. Все
  три падают закрыто или видны в логе первого parallel-прогона.
- **Следующее расширение** (по правилам, без LLM-судьи; нужна разрешённая офлайн-загрузка, доступность через прокси не проверялась):
  - MGSM (250 задач × 11 языков, числовой ответ): тот же математический скорер плюс проверка языка ответа;
  - HumanEval+/MBPP+ (EvalPlus, исполнение тестов на CPU в песочнице);
  - для IF: IFBench (новые типы ограничений, свой checker) как отдельный dev/test, после проверки пересечений с IFEval-541.
