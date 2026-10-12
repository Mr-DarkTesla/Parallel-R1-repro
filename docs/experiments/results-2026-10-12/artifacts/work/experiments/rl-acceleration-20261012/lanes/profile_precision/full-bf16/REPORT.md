# Полный BF16 autocast: отдельные политики sampler и learner

Предыдущие тесты проверяли только BF16 body + FP32 head и BF16 body + FP32 attention/head. Здесь впервые проверен обычный полный BF16 autocast без таких overrides: `src/same_mode_gate.py`, `config.json`, `seal.json`; cp50, тот же clean16, seed, caps4096/768/16384, fullwidth8. Параметры FP32; optimizer не запускался.

Фактические dtype receipts: q_proj и lm_head outputs BF16, SDPA output BF16; параметры FP32, logits перед logsumexp/softmax FP32. Обычный AMP оставляет embedding/residual FP32, RoPE поднимает pre-autocast Q/K в FP32 (V BF16). Это полный autocast, а не принудительное преобразование всех intermediate tensors и master weights в BF16.

16/16 clean cases завершены, 11/16 correct против 13/16 matched FP32. Маленький descriptive pilot, не доказательство ухудшения качества всей политики. 15183 sampled actions, F11251; FP32 matched pilot имел T24101/F16746. Сумма BF16 episode durations468.938s против FP32702.794s сильно зависит от различной длины output; это не доказанный throughput gain и не update wall.

Native BF16 cached q → BF16 fullteacher: max|Δlogp|0.2081623, worst-rank mean0.0110164/p950.0709732; исходные strict thresholds0.01/0.002/0.005 не проходят. Rho этого сравнения [.812959,1.231413], только1/15183 вне PPO[.8,1.2]. Отключение BF16 reduced-precision GEMM accumulation и math SDPA не исправили расхождение fullteacher (эти variants сравнивались с исходным native q, отдельно не регенерировали свою policy).

**Native BF16 cached q → идентичный cached target-forced replay: все15183 действия дают точное совпадение logprobs, max/mean/p95=0 на8/8 ranks.** Сохранены исходные sibling batch widths, finished rows, padding, repeated positions и raw targets. Это доказывает consistency sampler q при этих frozen inputs; mismatch с fullteacher не означает дефект mask/action provenance.

`src/proximal_gate.py` вычисляет отдельный FP32 fullteacher p0 и сохраняет BOTH immutable q_logprobs и p0_logprobs в `proximal/p0-rank*.jsonl`. Самплерные q не обновлялись. FP32p0/BF16q: max|logrho|7.270294; rho [.0006959,9.530303]; per-rank mean|logrho|.1046–.1718; 13.9–22.7% вне[.8,1.2], cap2 задевает.77–1.37%; rawmeanrho.995–1.003, ESS fraction.880–.937. Это уже различие precision policies, отдельно от cached/fullteacher BF16 rounding.

Matched fixed-action likelihood gradients для8 коротких main calls (95–187 действий, unit-advantage negative mean logprob, НЕ PPO/Adam): BF16 vs FP32 cosine.674–.880, relativeL2.487–.740, peak51.70GB. Нельзя выдавать это за gradient proof TIS или качество RL. Следующий изолированный кандидат — BF16 rollout + FP32 learner/master Adam, explicit detached token TIS cap2, PPO centered at frozen p0, q сохранён.

Native controller8082, diagnostic8188, proximal8367: все8 children каждой стадии завершились exit0. После diagnostic все8 GPU0MiB/0%; после proximal освобождение подтверждается перед следующим launch. Original32 production wrappers не возобновлялись.

Основные evidence: `native/result-rank-*.json`, `native/traces-rank-*.jsonl`, `diagnostic/result-rank-*.json`, `proximal/result-rank-*.json`, `proximal/p0-rank*.jsonl`; источники и config seals рядом. Ни одной GPU Adam update в этой серии; старые thresholds/source/run не изменены.
