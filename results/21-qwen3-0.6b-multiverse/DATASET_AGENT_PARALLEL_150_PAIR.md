# Парные tagged/plain данные на 150 проверенных задачах

12 октября 2026, 02:03 МСК. Это расширение [пары на 91 задаче](DATASET_AGENT_PARALLEL_91_PAIR.md) ещё 59 новыми принятыми [после независимого ревью](DATASET_AGENT_PARALLEL_WAVE71B.md). Новые задачи вне обоих masked holdout, val и полного clean46 train по ID и тексту. Все 150 обучающих ответов с полезными независимыми блоками внутри `<think>` прошли тот же `math_verify`: 150/150, неверных финалов в независимом чтении 0. Это проверка меток, не модели.

Сборщик `scripts/exp21/build_agent_parallel_pair.py` получил явные `--positive-count 150` и [гейт ревью](audit/agent_parallel_150_review_gate.json). Обе ветви содержат те же 150 ID, порядок и промпты. Для каждой положительной задачи три копии; плюс в обе ветви одинаково добавлены 55 собственных правильных thinking и 54 no-thinking replay исходной 4B. Итого **559 train и 50 val строк на плечо**. Plain удаляет только теги, оставляя весь текст. Tagged обучается Multiverse-маской и отдельным `optim.tag_lr_mult=100`; plain обычной causal-маской. Максимальная точная длина по шаблону чата: 1603 токена train, 3513 val, лимит 4096. Отчёт сборки: `data/agent_parallel150_pair/sft_build_report.json` со статусом `ready_for_paired_sft`; четыре parquet лежат там же. Они уже скопированы на собственный persistent `/checkpoints/exp21-agent-parallel150`, свободно 19 GiB на момент копирования.

Фактический [CPU-preflight на личном pod](audit/agent_parallel150_pod_preflight.json) повторно прочитал оба parquet каждым плечом с токенизатором родительской 4B модели: 559/50 строк, одинаковые ID/порядок/промпты, те же максимумы 1603/3513. Единственный GPU-сборщик не затронут.

Команда локальной сборки:

```bash
uv run --offline --no-project --with math-verify --with tokenizers==0.23.2 --with pandas --with pyarrow --with transformers --with jinja2 python scripts/exp21/build_agent_parallel_pair.py --accepted results/21-qwen3-0.6b-multiverse/data/agent_parallel_150_accepted.jsonl --out-prefix results/21-qwen3-0.6b-multiverse/data/agent_parallel150_pair/sft --positive-count 150 --review-report results/21-qwen3-0.6b-multiverse/audit/agent_parallel_150_review_gate.json
```

**SFT на этих данных ещё не запущен.** После успешного окончания прежнего on-policy генератора можно использовать уже проверенный [однопроцессный runner](QWEN4B_AGENT_PARALLEL91_RUN.md) с `EXP21_PAIR_DATA=/checkpoints/exp21-agent-parallel150` и уникальным `EXP21_RUN_PREFIX=exp21-4b-agent-parallel150`. Оба плеча должны начинаться с одного clean46 tagged step32 parent, иметь по 32 шага, batch 16, lr `5e-7`, одинаковые ступени 8/16/32 и fixed40. Архивировать сырые ответы, считать ручную полезность блоков и парные ДИ до решения о полном dev. 91-задачная пара остаётся контролем размера данных; её запускать только последовательно, если он нужен после оценки 150.
