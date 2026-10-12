# Lane A: profile / precision, 2026-10-12

**Результат: оставить FP32 / highest / TF32=False.** TF32 и два варианта BF16 провалили неизменённый guard собственного sampler→teacher replay на реальном4B. Ни один precision patch не готов к production. Все8GPU mpimaster-0 освобождены; original wrappers не возобновлялись, full500 не запускался.

## Протокол и подтверждённое завершение

- Existing allocation `RUN_5482aee87e`, только mpimaster-0.
- Baseline: canonical `experiments/parallel_instruct` скопирован в собственный `src`; instrumented copy, fresh checkpoint50, FP32 full weights4,022,468,096, new sharded Adam, lr1e-6. Исходный checkpoint не менялся.
- **8 prompts×4=32 responses/update на8GPU**, rank-independent sampling seeds20261012, data seed20261012, prompt exposure offset1200. Полные budgets4096/768/16384. Frozen1024train/32cleanval, reward/scorer/system без изменений; public benchmarks не использовались.
- Completed updates51–55. Первый update имеет scoped profiler; updates52–55 без profiler capture. Все40 rank updates: finite, positive backbone update, guards passed, optimizer updated. Веса benchmark не экспортировались.
- Baseline workers6694–6701: **все exit0**. Launcher strips cloud32 MPI/TORCHELASTIC variables; separate localhost TCP store/world8. Before every new launch проверялись пустые GPUs.
- FP32 control, TF32 native, BF16 native, BF16 with FP32 attention native: каждый запуск8workers, **все exit0**. Последний microprofile имеет success summary и отсутствующий PID; финальная NVML inventory: GPU0..7 **0MiB/0%**. `final-gpu-release.json`.

Config: `baseline-config.json`, SHA256 `53b83e0bd6e964244dfbd241d3e8091583f05f8241f4958bcd1b215feb816ac3`. Provenance: `canonical-source-hashes.json`, `baseline-source-seal.json`, precision/native/control seals. В `source-snapshots/` сохранены исходные версии gate scripts; SHA совпадение с launch seals проверено отдельно, а не предполагается по текущему имени файла.

## Измеренный baseline

| Update | Wall s | Responses/s | Sampled tokens | Physical generation F | Train correct | Peak GiB |
|---:|---:|---:|---:|---:|---:|---:|
|51 profiled|328.948|0.0973|36,054|24,517|30/32|49.563|
|52|267.377|0.1197|36,443|24,215|30/32|48.962|
|53|614.400|0.0521|59,114|39,706|23/32|43.101|
|54|620.323|0.0516|56,685|38,719|30/32|43.839|
|55|283.041|0.1131|39,890|25,567|31/32|39.008|

Steady52–55: mean446.285s/update, **0.071703responses/s,107.628sampled tokens/s**. Это четыре разных batches, поэтому их среднее нельзя использовать как matched candidate speedup. Train correctness не является validation accuracy.

Wall здесь измерен от начала update до завершения cleanup/metric gather/write и CUDA synchronization; не включает заключительный dump диагностических timers. Runner `seconds` заканчивается раньше cleanup. Exports/validation отключены. Реальный полный controller interval включает также model loading, initialization и diagnostics; он не заменяет steady update measurement.

Максимальный fresh replay drift за5updates0.000334740. Минимальный positive backbone probe L2 за updates1.2940e-5. GPU peaks измерены с resident Adam.

## Где тратится время

На unprofiled52 критический rank2:

| Последовательная host phase | Seconds |
|---|---:|
|Generation+scoring|185.293|
|Reward gather|0.003|
|Replay forward|29.592|
|Backward, включая DDP|51.535|
|Collective parity guard|0.447|
|Clip/active count/Adam|0.057|
|Cleanup/metric write|0.211|

На heavy53 rank7: **generation501.341s из614.400s (81.6%)**, replay34.040s, backward66.838s, guard11.660s, clip/Adam0.063s. F rank7=11,417, rank6=2,494. На51 короткий rank1 generated76.545s и затем ждёт153.846s на reward gather, пока rank2 finishes230.387s.

**Главное — generation и различная длина trajectories.** Optimizer и запись файлов малы. На53 оба самых тяжёлых ranks0/7 имели exact zero advantages и correctness0/4; их дорогой backward даёт нулевой локальный gradient. Это конкретная возможность оптимизации replay без изменения precision.

Nested details нельзя складывать с outer phases. Например53 sampling+host sync122.388s и model decode host368.869s находятся внутри501.341s generation. Generation CPU mask building0.181s; этот timer не покрывает replay masks. Replay host phase содержит также CPU input construction, logp normalization и возможное ожидание предыдущего queued backward.

CUDA events показывают current-stream interval, включая waits/host submission gaps; это не сумма kernel durations. В scoped first-prefill+8decode kernel-only window:0.4053s GPU kernels, aten::mm317.8ms (~78%), attention31.7ms (~7.8%). First-backward kernel-only window0.8145s, основные kernels SGEMM. Первый backward использует no_sync; **он не профилирует NCCL**, DDP synchronization остаётся внутри backward/collective wait phases и не выделена как аддитивный kernel timer.

## Precision: различать две проверки

1. **FP32 policy→TF32 teacher:** намеренно меняется precision policy. На36,054actions maxdelta0.476061, weightedmean0.010210, worst rank p950.066190. Эта проверка сама по себе не доказывает ошибку собственного TF32 sampler или ухудшение качества.
2. **Native candidate sampling→teacher в том же режиме:** проверяет непосредственно нужное совпадение old/new likelihood. На этой проверке все tested modes ниже fail на всех8ranks.

Неизменённый collective contract: max≤.01, mean≤.002, p95≤.005; any rank bad запрещает optimizer. В таблице mean/p95 — максимум rank statistics, соответствующий этому contract.

| Mode | Max delta | Worst rank mean | Worst rank p95 | Clean16 correct / FP32 ref | Verdict |
|---|---:|---:|---:|---:|---|
|FP32 no_grad control,36,054actions|0.000120|0.00000486|0.0000248|не генерировал заново|PASS8/8|
|TF32 native→TF32 replay|0.132721|0.002603|0.013930|14/16 vs13/16|FAIL8/8|
|BF16 autocast body, FP32 master/head|0.173939|0.005113|0.025957|13/16 vs13/16|FAIL8/8|
|BF16 body, FP32 master/attention/head|0.273294|0.004747|0.025078|12/16 vs13/16|FAIL8/8|

Каждый native pilot использует первые16 **fixed cleanval** cases, одинаковые prompts/seeds/checkpoint и полные budgets. Это не public benchmark. Exact generated response match с FP32 reference:0/16 у каждого precision mode. Correctness маленького pilot не доказывает общую регрессию/неухудшение, но позволяет не путать guard failure с quality claim.

FP32 master parameters и FP32 LM head сохранены в BF16 screens; BF16 cached weight casts ограничены context lifetime. **Candidate Adam updates не запускались**, поскольку native likelihood guard fail. Нельзя утверждать FP32-master Adam validation или accepted precision throughput. BF16-direct-parameter training не применялся.

Kernel inspection на том же4B под TF32/high подтвердил shape-dependent path: cached single-row decode запускает `gemv2T` / `gemvx` с float operands, full teacher — `cutlass_80_tensorop_s1688gemm`. На трёх одинаковых forced targets logp deltas `[0,0.00229645,0.00760078]`. Это поддерживает объяснение разных GEMV/GEMM arithmetic paths; только эта3token microprofile не доказывает причину каждого full-trace outlier и не является speed benchmark. FP32 matched no_grad control исключает ошибку references/gate как объяснение большого TF32 drift.

## Что отдаётся для объединения

- `patch.diff`: instrumented experiment sources/gates, **не production-ready optimization**.
- `tf32-candidate-only.patch`: три precision flags, **REJECTED; не применять**.
- `summary.json`, `precision-summary.json`: completed-step и guard statistics.
- `baseline/profile/*.json`: scoped Chrome traces и rank phase journals; `tf32-kernels/*.json`: actual kernel-path microprofile.
- Source/config hashes, worker PID/exit ledgers, all native traces и FP32 reference-control likelihoods находятся рядом.

Рекомендация: объединять прошедшие отдельно FP32 improvements (compact decode/cohort batching) и проверенный zero-advantage replay, когда его собственный GPU proof завершён. Zero-advantage предложение: сохранить likelihood checks каждого action под no_grad, затем один настоящий shortest-context zero-loss DDP backward для участия всех параметров в collective. Local gradient математически0; guard не пропускается. Read-only review patch laneD не выявил проблемы; его CPU8Gloo gradient/Adam/forced-bad guard proof прошёл, real4B GPU proof принадлежит laneD и здесь не объявляется завершённым.

Больший generation count при прежнем wall time не доказан этим lane. Для такого утверждения нужен matched scheduler benchmark, включая replay/backward и global batch semantics. Не переносить отрицательные precision результаты на прочие численные режимы или модели.
