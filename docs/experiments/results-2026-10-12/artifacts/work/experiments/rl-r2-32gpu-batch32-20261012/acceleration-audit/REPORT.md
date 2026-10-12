# Аудит ускорения RL: 2026-10-12

Вывод: резерв ускорения есть, но старая ветка vLLM не реализует текущую политику Parallel-R1. Наиболее прямой путь — оптимизировать текущий HF decode, затем сделать отдельный scheduler нескольких траекторий на одном actor/GPU. Больше responses при прежнем wall time пока не доказано.

Аудит только на чтение. RL, GPU proofs, benchmarks и allocation не запускались; процессы не сигналились, active sources не менялись. Создан только этот локальный отчёт. SSH напрямую с Mac через `8a100_jupyter`; все удалённые команды выполнялись после `cd ${PROJECT_ROOT}`.

## Проверенное состояние и измерения

- Single allocation: `RUN_5482aee87e`, 32 GPU. `control/RL-USER-HOLD.json` содержит explicit user hold, 32 остановленных CPU wrappers, eval children untouched, resume requires user instruction. Удержание не менялось.
- На 10:05:41 UTC готовы 459/500 eval traces checkpoint50. Это промежуточный набор для диагностики runtime, не итоговая accuracy. При последнем последующем чтении было 484/500.
- SHA-256 удалённых `runner/train.py`, `decoder.py`, `microbatch_decoder.py`, `structured_replay.py`, `rollout.py` совпадают с локальными копиями.
- Текущий frozen runner: FP32, TF32 отключён, HF SDPA, width≤8, один response/rank; 8 prompts × 4 responses = 32/update; mean centering внутри prompt group, denominator 4096, all weights trainable. Реальный throughput нового 32-GPU RL ещё не измерен.
- Старый 24-GPU run: 52 completed updates; latest 12 updates41–52 имеют timer **438.24–661.62 s, среднее555.38 s на96responses**, то есть 0.1729 responses/s по этому таймеру. Все52: среднее413.41s. Последние updates заметно тяжелее; раннее среднее нельзя использовать как текущий прогноз.
- Timer `seconds` включает generation, scoring/writes, replay/backward, DDP synchronization, clipping и Adam; исключает cleanup, metric gather/write, validation и checkpoint export. Настоящий start-to-next-start wall time больше. В сохранённых данных нет phase timings; их нельзя восстановить делением wall time на F.
- На latest12 old updates отношение max/min суммарного F по ranks в среднем6.13×. Например step52: F1748–10355, но все ranks показывают570.944–570.960s из-за collective synchronization. Это подтверждает неравномерность работы, но не разделяет generation и backward.

## Что decoder уже делает и чего не делает

`runner/decoder.py:49–72` строит полный structured input каждой строки, объединяет rows и выполняет один batched prefill. `:116–118` использует KV-cache при последующих токенах **внутри этого вызова**. `runner/rollout.py:56–69,71–103,134–143` запускает отдельные вызовы для main, width, paths, summary и post-think: между ними KV не передаётся.

Следствия:

1. Общий prefix width4 повторно вычисляется в четырёх rows. Он не prefills один раз с последующим fork cache. KV-cache каждой ветви независим и хранит повторную копию prefix.
2. На Summary весь assembled prefix вместе с уже готовыми Paths обрабатывается заново. Structured mask сохраняет sibling isolation, repeated positions — это нельзя заменить обычным causal prefill.
3. `decoder.py:100–118` маскирует finished rows, но физический batch остаётся исходной ширины до longest Path. Пустые rows продолжают проходить модель.
4. `decoder.py:84–95` выполняет отдельные `int(cuda_tensor)` и `float(cuda_tensor)` для каждой active row каждого токена: это явные точки GPU→CPU synchronization. Помимо forward остаются Python loops, allocation масок/токенов, softmax и logsumexp.

Диагностика459 current eval trajectories:

| Метрика | Наблюдение |
|---|---:|
| Время одной eval trajectory | mean51.09s, median37.36s, p95130.73s |
| Physical generation F | mean1183.31, median896 |
| Prefill forwards | mean5.81/trajectory |
| Sum prefix input lengths по всем policy calls | mean9070.82 tokens/trajectory |
| Rows общего path prefill | mean4.12, median4 |
| Доля finished dummy row slots в fork batches | mean32.07%, p9552.22% |
| Seconds/F одной eval trajectory | mean42.5ms/F |

Последняя величина включает prefill и весь execute/scoring; это не чистая latency одного decode kernel. 32% пустых row slots — доля вычислительных слотов, **не прогноз32% wall speedup**. Малый batch может быть ограничен чтением весов, и уменьшениеrows не обязано пропорционально сокращать время.

## Почему старую vLLM-ветку нельзя просто включить

Проверенный remote git ref: `origin/qwen3-0.6b-rl`, commit `c93133e049cd57558109330bdc4ed94adec433e4`.

- `verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py:316–331` передаёт только `TokensPrompt(prompt_token_ids=prompt_ids)` и возвращает только token IDs. Ни structured 4D mask, ни repeated positions, ни реальные rollout logprobs не передаются.
- `verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py:158–206` создаёт repeated positions и sibling mask metadata после generation; `:432–435` отправляет в Summary flattened siblings.
- `verl/verl/workers/actor/dp_actor.py:294–310` применяет sibling mask и custom positions при actor replay. Поэтому distribution generation отличается от distribution PPO, начиная с merged Summary/continuation; первый fork из causal prefix сам по себе ещё не доказывает корректность остальных фаз.
- `parallel_thinking_loop_v3.py:130–147` ставит loss mask1 всем appended tokens. Переданный manual-mask список не применяется. Это включает injected headers/bridges.
- `verl/verl/trainer/ppo/ray_trainer.py:1248–1258` recomputes old_log_probs actor-ом. Маленький PPO KL при таком recompute не подтверждает likelihood реального vLLM sampler.
- Изменения vLLM server в текущей ветке добавляют max_num_seqs/final-only/detokenize optimization; исправления structured context contract в этом интерфейсе нет.

vLLM как новый backend возможен только с custom structured attention/KV positions и sampler-logprob provenance для каждой фазы. Обычный TokensPrompt здесь недостаточен. [Текущая официальная схема TokensPrompt](https://docs.vllm.ai/en/stable/api/vllm/inputs/llm/) также не содержит structured mask или explicit position_ids. [Prefix caching vLLM](https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/) ускоряет prefill, не autoregressive decode; название backend само по себе не гарантирует решение нынешнего bottleneck.

## Приоритет кандидатов

| Приоритет | Кандидат и ожидаемый резерв | Что требуется доказать отдельно |
|---|---|---|
| 1 | Убрать per-row host sync из sampling/logp записи: собрать GPU tensors, переносить результаты одним batch transfer, сохранять independent per-row RNG. Уменьшить transient allocations. Небольшой implementation scope; выигрыш пока не измерен. | Совпадение raw sampled actions/seeds, blocked logits, stop decisions и old logps; guards без ослабления; whole-update measurement. Нельзя заменить generators общей batch RNG. |
| 2 | Компактировать completed branch rows и cache, сохраняя все **live** siblings одного fork в одном forward. Подтверждён mean32% dummy-slot резерв, wall effect неизвестен. | KV row remapping, masks/positions и RNG identity; width2..8, unequal lengths, early EOS, repeated rounds; independent physical-forward hook. |
| 3 | Несколько independent trajectories одновременно на одном actor/GPU, batch sequential sections и complete sibling groups. Наибольший очевидный резерв для больше responses/GPU; уменьшает weight-streaming overhead и idle tail. | Новый adapter/scheduler: fullwidth8 per trajectory, no split fallback; cross-episode isolation; actual participating-forward ledger отдельно от global server count; 4B optimizer-resident memory; same32responses, gradients и Adam update. |
| 4 | Сохранять inference KV между main/width/fork/summary, fork shared prefix один раз, merged KV собирать с isolated branch states и повторными RoPE positions. Убирает подтверждённый повторный prefix compute. | Более сложная semantic proof: raw terminal token иногда заменён visible close tag — неправильный KV для replacement переиспользовать нельзя; injected bridges, branch whitespace, Summary merge и cache reset after optimizer. Inference detached KV нельзя использовать для training replay: пропадут prefix gradients. |
| 5 | Batched replay независимых policy_calls и/или sibling score calls. Сейчас `train.py:334–349` отдельный full-prefix forward/backward для каждого call; mean8.90calls/trajectory. | Точные исторические per-call prefixes/raw targets, loss mask/normalizer, gradient и Adam parity. Простая flattened assembled replay неверна при EOS→visible tag replacement. Memory worst-case logits/activations. |
| 6 | TF32 или BF16/autocast для rollout **и** replay; потенциально большой arithmetic/memory gain, но policy изменится численно. | Real4B fullwidth fixtures и full trajectories; existing max.01/mean.002/p95.005 guards; FP32 master parameters/Adam при BF16; quality matched cleanval; memory и whole-update throughput. TinyCPU BF16 drift max.002719/mean.000937/p95.002258 — не 4B доказательство, строгая FP321e-5 equivalence уже не совпала. |

Изолированный `work/experiments/rl-instruct-20261011/throughput/cohort_decoder.py` — полезная заготовка, а не готовая current implementation: defaults max_paths2 (`:15`), дробит fork (`:85–87`), reward F получает как counterfactual max generated length (`:96–106`). CPU proofs подтвердили tiny-model sampled decoder и forced full-execute semantics, включая raw-stop replacements; real4B GPU parity, fullwidth8 adaptation, memory и throughput не доказаны. Включить этот файл напрямую нарушит frozen fullwidth/physical-accounting contract.

## Batch32 при другом количестве GPU; «больше responses бесплатно»

`experiments/parallel_instruct/batching.py:5–26,29–60` уже описывает fixed8×4=32 на1/2/4/8/16/24/32 ranks; DDP scale `world/32` превращает rank sums в global response mean. Это верная идея распределения без изменения effective batch. Generic `train.py:289–320` пока исполняет local assignments последовательно: готовая partition logic не является trajectory batching.

Следующая архитектура: **один actor/DDP rank на GPU, несколько episode clients на этот actor**. На16GPU — два responses/GPU, на8GPU — четыре; сохранить8prompts×4, global normalization и one fresh-policy update. Несколько отдельных model/DDP ranks на одном GPU дублируют16GB FP32weights+gradients и осложняют collectives; это не batching.

Полные8branches должны оставаться в одном forward. Одновременные trajectories требуют aggregate rows16/32, хотя текущий `microbatch_decoder.py:22–23` запрещает больше8rows. Нужен отдельный adapter; max_rows — batch capacity, а allowed path width остаётся≤8.

Проверенная config:36layers,8KVheads,128head_dim. FP32KV =288KiB/row/token:8rows×4096 ≈9GiB,8×16384≈36GiB. Dense prefill mask дополнительно0.5/8GiB. На старом24GPU run peak40.8–41.6GiB в тяжёлых updates; это не memory proof для32rows или1GPU unsharded Adam.16/8GPU меняют sharded optimizer state per rank и worst-case memory.

64/128responses вместо32 — новый training budget: либо больше prompts при прежних4siblings, либо больше samples/prompt с другим advantage estimator. Удвоение responses потребует generation **и replay/backward**. Даже при равном measured wall time optimizer увидит другую batch и число примеров; «500steps» станет другим объёмом обучения. Сравнение старого24GPU96responses с новым32GPU32responses confounded; ускорение нельзя приписать backend/GPU count.

При следующем явно разрешённом GPU proof: фиксировать те же32 trajectories/prompts/checkpoint/seeds/reward, измерять start-to-next-start wall time и responses/s, phase boundaries и peak memory, сначала parity/gradients/Adam, затем2–5steady updates. Отдельно сравнивать cleanval quality и F, не только update count. До такого proof ни x-speedup, ни сохранённый wall time при большем generation обещать нельзя.
