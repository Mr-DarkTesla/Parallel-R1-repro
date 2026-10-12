# Parallel-R1: ночные эксперименты 9–10 октября 2026

Состояние: night_archived_resources_retained. Снимок UTC: 2026-10-10T08:39:36.314438+00:00.

Все ночные обучения, общие валидации, пять заранее назначенных финальных MATH500 и диагностики завершены. Пользователь отменил освобождение Cloud-узлов в12МСК и продлил эксперименты на неопределённый срок при потолке24GPU. Ночные результаты архивированы без остановки ресурсов. Новые SFT-эксперименты Qwen3-4B продолжаются отдельно.

## Данные и выбор моделей

RL обучался на GSM-Infinite train и MATH train, включая MATH levels1/2. Из RL train исключены все5000 задач MATH test и новая SFT val300 по нормализованным ключам. Проверка исходных источников/операций GSM и вложенных SFT-val контекстов дала0 пересечений. Это проверка точных/нормализованных пересечений, а не доказательство отсутствия семантических парафразов.

Для выбора использовалась только общая validation128=64MATH+64GSM с исходным seed42. Порядок: число верных MATH, затем GSM, затем меньшая F на верных. Выбор по каждой линии и secondary math40 записаны до запуска финального теста, в06:43:13UTC. MATH500 и дополнительные inference seeds не использовались для выбора/продолжения обучения.

## SFT

Fresh: Qwen3-0.6B Base, только новые3000 примеров (2700train/300val),5 эпох,105 шагов, Unseen. Итоговый checkpoint: ${PROJECT_ROOT}/work/experiments/night-20261010/sft/runs/01_sft/final. MATH500:92/500, strict464, correctness+compiled-parallel83.

OLD mixed:5145 примеров,180 шагов, другой split; на одинаковом бюджете101/500, strict223, joint28. В101 входят47 верных ответов без закрытого think и1 с повторным закрытием; историческая think-gated метрика54, correct+basic-valid51. Разница с fresh не изолирует причинный эффект качества данных: отличаются объём, шаги, split, формат и инициализация четырёх существующих ChatML/think строк (fresh seed1).

## RL: общая validation128

| Эксперимент | Верно /128 | GSM /64 | MATH /64 | Strict | Correct+parallel |
|---|---:|---:|---:|---:|---:|
| new-sft-baseline-128 | 25 | 15 | 10 | 119 | 24 |
| sft-accuracy-stage1-128 | 29 | 20 | 9 | 124 | 29 |
| sft-math-accuracy40-128 | 48 | 30 | 18 | 127 | 46 |
| sft-math-accuracy80-128 | 45 | 26 | 19 | 123 | 33 |
| sft-math-split40-128 | 40 | 24 | 16 | 127 | 40 |
| sft-mix-accuracy40-128 | 32 | 23 | 9 | 126 | 32 |
| sft-mix-g8-pilot-128 | 36 | 28 | 8 | 124 | 36 |
| sft-scalar-stage1-128 | 26 | 20 | 6 | 126 | 26 |
| sft-sirius-continuation3-128 | 39 | 29 | 10 | 126 | 38 |
| sft-sirius-continuation4-refcorrected-128 | 39 | 24 | 15 | 126 | 39 |
| sft-split-stage1-128 | 32 | 22 | 10 | 124 | 31 |
| sft-split-stage2-128 | 36 | 24 | 12 | 125 | 36 |
| sft-tmp3-continuation3-128 | 33 | 24 | 9 | 125 | 33 |

Первые три arms сравнивали correctness-only, scalar-success-cost и раздельные advantage correctness/cost от одинакового fresh SFT. Затем split80 стал валидационным anchor; исследованы balanced GSM/MATH curriculum, G8, reward-only accuracy на том же mix и MATH-only. Первые три arms: response2048/path1024, G4×8 prompts, LR1e-6, KL.001, eta.05, B0=256, scale1024, bonus0. Split80 сохраняет2048/1024; поздние mix/MATH используют4096/1024, G8 pilot меняет group size на8. Поэтому поздние curriculum-ветки не являются чистой абляцией только reward. Номинальные шаги продолжений включают обязательный smoke. Таблица ниже и JSON содержат фактический train/reference/resume identity; одинаковый sampler seed не делает генерации попарно одинаковыми.

| Run | Статус | Метод | Последний наблюдённый шаг | Production metric rows | Все записанные grad finite | All-wrong batches |
|---|---|---|---:|---:|---|---:|
| rl-sft-accuracy | completed | night_accuracy | 40 | 38 | True | 0 |
| rl-sft-math-accuracy40 | completed | night_accuracy | 40 | 38 | True | 1 |
| rl-sft-math-accuracy80 | completed | night_accuracy | 80 | 38 | True | 0 |
| rl-sft-math-split40 | completed | night_split_success | 40 | 38 | True | 0 |
| rl-sft-mix-accuracy40 | completed | night_accuracy | 40 | 38 | True | 0 |
| rl-sft-mix-g8-pilot | completed | night_split_success | 20 | 18 | True | 0 |
| rl-sft-scalar | completed | night_scalar_success | 40 | 38 | True | 0 |
| rl-sft-sirius-continuation3 | completed | night_split_success | 40 | 38 | True | 0 |
| rl-sft-sirius-continuation4 | production_failed / excluded | night_split_success | 53 | 11 | True | 0 |
| rl-sft-sirius-continuation4-refcorrected | completed | night_split_success | 75 | 33 | True | 0 |
| rl-sft-split | completed | night_split_success | 40 | 38 | True | 1 |
| rl-sft-split-stage2 | completed | night_split_success | 80 | 38 | True | 0 |
| rl-sft-tmp3-continuation3 | completed | night_split_success | 40 | 38 | True | 0 |

MATH accuracy80 продолжает checkpoint40 с исходной reference split80HF и сохранённым optimizer. MATH split40 отличается reward от MATH accuracy40 при том же anchor/data/config и reset optimizer/reference. Mix accuracy40 сравнивает смену reward на прежнем balanced mix. Эти точные пары следует отделять от exploratory веток, одновременно менявших данные и reward. Все12 завершённых production arms использовали schema2 reference-blind extraction. Первые два smoke шага split предшествовали обновлению think-boundary extraction, но независимая проверка всех64 predictions дала точное совпадение с canonical (5 верных), поэтому их фактические accuracy rewards не изменились. Reference-dependent выбор правильного кандидата не использовался. Format bonus у всех завершённых SFT arms равен0; версии бонуса менялись только в исключённых instruct warmups.

## MATH500: заранее зафиксированные модели

Одинаковые500 задач/gold, seed42, response4096/path2048, structured runtime/prompt. Joint = верный ответ + канонический compiled protocol + реально исполненный fork. Это не доказательство осмысленности ветвей.

| Модель | Pass@1 | Strict /500 | Joint /500 | Samples с fork | F mean all | F p95 all | F mean correct | F p95 correct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fresh SFT 3000 | 92/500 (18.4%) | 464 | 83 | 461 | 608.83 | 1270.05 | 403.11 | 654.50 |
| OLD mixed SFT 5145 | 101/500 (20.2%) | 223 | 28 | 359 | 557.51 | 1212.85 | 315.85 | 557.00 |
| Sirius corrected75 | 115/500 (23.0%) | 477 | 108 | 483 | 535.60 | 1081.20 | 397.10 | 611.60 |
| MATH split40 | 102/500 (20.4%) | 487 | 102 | 498 | 539.60 | 1056.30 | 382.54 | 576.90 |
| MATH accuracy80 | 130/500 (26.0%) | 483 | 71 | 351 | 486.75 | 1028.10 | 370.82 | 793.30 |
| MATH accuracy40 (secondary) | 102/500 (20.4%) | 488 | 89 | 461 | 523.25 | 1066.60 | 396.23 | 796.60 |

| Модель | T sampled mean | T assembled mean | Wall mean seconds/question | Width mean | Forks mean | Global truncated /500 |
|---|---:|---:|---:|---:|---:|---:|
| Fresh SFT 3000 | 741.14 | 752.95 | 22.06 | 2.48 | 0.94 | 5 |
| OLD mixed SFT 5145 | 642.27 | 652.48 | 19.05 | 2.33 | 0.82 | 10 |
| Sirius corrected75 | 657.07 | 668.70 | 19.39 | 2.27 | 0.98 | 1 |
| MATH split40 | 681.28 | 693.70 | 18.85 | 2.38 | 1.02 | 5 |
| MATH accuracy80 | 579.73 | 588.87 | 16.16 | 2.38 | 0.70 | 2 |
| MATH accuracy40 (secondary) | 648.69 | 660.21 | 18.02 | 2.40 | 0.93 | 2 |

MATH accuracy80:130 correct =71 joint+55 без fork+4 с невалидным fork. Увеличение pass@1 сопровождается снижением joint против fresh83 и ухудшением p95 F на верных (793.3 против654.5). Sirius115=108joint+5безfork+2invalid; split102 всеjoint. Выбор моделей после просмотра теста не менялся.

F — логическая критическая глубина sampled-токенов. Текущий HF backend исполняет siblings последовательно; F и RPC calls не являются измеренной телеметрией model-forward и не доказывают реального параллельного ускорения. Wall — наблюдаемое время этого backend, с различающимися длинами ответов.

## Вариативность и интерпретация

| Inference seed | Fresh /128 | MATH accuracy40 /128 | Fresh MATH /64 | RL MATH /64 |
|---|---:|---:|---:|---:|
|42|25|48|10|18|
|10042|36|42|15|12|
|20042|37|40|13|14|

Те же128 вопросов и те же однократно обученные модели; это не384 независимые задачи и не три training seeds. Направление MATH-изменения меняется между seeds. Exact paired tests в JSON не скорректированы за adaptive exploration/multiple comparisons; устойчивого multi-seed улучшения не установлено.

## Проваленные ветки, исправления и аудит

Instruct0.6B со случайными новыми token rows не выучил добровольный opener: guided fork не равен learned fork. Старый V2 остановлен и исключён из отбора. Semantic alpha.010 pilot дал0fork и не продолжен. В ранних Native TEXT v1/v2 были реальные дефекты BPE-boundary и dual-EOS; они исправлялись в отдельных последующих snapshots. Финальные проверенные v3/v4prompt/phase не прошли qualitygate при исправленном RAW/position/mask accounting; phase guided копировал placeholder paths, unguided имел0fork. Для финального phase нет2PPO и нет длинного RL.

В Sirius continuation4 обнаружена смена KL reference на freshSFT при корректно resumed actor/optimizer. Собственный запуск остановлен, faulty updates сохранены и исключены. Исправленный запуск возобновлён с чистого continuation3 step40, прежней accuracyHF reference и optimizer; actual41/42 smoke и итог75 проверены. Неверная ветка не использована в выборе.

Legacy compiler иногда нормализует неверный terminal control в закрывающий тег. RAW labels сохраняются, replay/mask leakage в проверенных трассах не обнаружены; compiled strict скрывает часть RAW compliance. Неверные terminal controls и EOS учитываются раздельно. Local path max_tokens reached отдельно от global truncation; достижение cap не доказывает незавершённость.

Финальные primary1500+secondary1000:14442 RAW calls,5247 paths,0 RAW-label/actionmask/positions/Unseen/sibling/F-T ошибок в независимых аудитах. Все final aliases byte-identical выбранным экспортам; committed steps75/40/80,8model+8optimizer shards подтверждены. Отдельный GPU007 audit сравнил committed instruct-step10 HF export с приватным обновлением aliases/parameters:32 сравнения ширин2–8/двух раундов, logit delta0 и replay delta около1.23e-6. Это не измерение активной передачи post-optimizer trainer weights через rollout RPC; этот предел проверки остаётся. Также нет прямой телеметрии всех GPU-forward вызовов.

Целевые качественные разборы нашли противоречивые paths, ложное согласование в Summary и декоративные форки даже при правильном финале. Это purposive examples, доля таких случаев не оценена. Joint нельзя интерпретировать как semantic usefulness.

## Instruct baselines и отдельный4B warmup

Оригинальный Qwen3-0.6B instruct:297/500 canonical, включая17 correct truncated. Этот runtime/prompt отличается от structured SFT-RL; сравнение полезно как baseline способности модели, не как чистая абляция SFT или wall-speed.

Официальный Qwen3-4B native,48 диагностических генераций (24optional+24requested):correct21/24 и23/24;18/24 в каждом варианте содержали тег Parallel, все после закрытого think; это не18 валидных полных блоков. Заголовки width3 найдены в9 optional и17 requested ответах;0/48 форков внутри think. Не добавлялись токены и не исполнялись Unseen forks. Диагностика завершена, дополнительных prompt search/RL не запускали.

Новый пользовательский4B warmup: ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010. Только6 shared embedding/output rows,15360 параметров; mean native subpieces,2700/300,3epochs129steps,Unseen. Actual8GPU2steps smoke и независимый аудит PASS. Все прочие веса frozen; оценка retention/format ещё ожидается. Это отдельная авторизация, не результат ночного0.6B RL и не цель09Cloud cleanup.

## Артефакты и завершение

Полные результаты/paired grades/checkpoint aliases: reports/final-math500-comparison.json. Неизменённый выбор: orchestration/final-freeze.json. Машиночитаемый текущий отчёт содержит run/model/train/resume identities, KL/advantages/gradients/all-wrong, source/proof hashes и дополнительные независимые reviews.

В09UTC после сохранения финального отчёта освобождаются только tmp2 f58cf2e8-d57f-4a4e-accb-28f98a291516 и tmp3 984c4577-4afe-42f9-a508-75b70956552e через a100_jupyter с обязательной skill activation. Cleanup receipts сохраняются отдельно. Исходный Sirius и новый4B warmup сохраняются. До фактических receipts освобождение узлов не считается выполненным.


## Independent synthesis: night-final-reward-review.md

Night reward/selection review — PASS

Checked 2026-10-10T08:13:37.316952+00:00. Controller1238649/source3dd9f40e andhelper002f4855 unchanged; finalfreeze matches pretest06:43:13 record. All pinned freeze/proof hashes match. No GPU/API/process actions.

Rewards: c=clip((F−B0)+/Fscale,0,1). Accuracy: y−groupmean(y). Scalar-success: y(1−eta*c)−groupmean[y(1−eta*c)]. Split-success: y−mean(y)+eta*y(mean_success(c)−c), efficiency0 with fewerthan2successes. No groupstd/finalwhitening; actorloss seq-mean-token-mean andactorKL.001.

Completed SFT-RL roster (common128: GSM/MATH; joint):
- rl-sft-accuracy: night_accuracy, targetstep40, G4, response2048, 29/128 (20/9), joint29.
- rl-sft-math-accuracy40: night_accuracy, targetstep40, G4, response4096, 48/128 (30/18), joint46.
- rl-sft-math-accuracy80: night_accuracy, targetstep80, G4, response4096, 45/128 (26/19), joint33.
- rl-sft-math-split40: night_split_success, targetstep40, G4, response4096, 40/128 (24/16), joint40.
- rl-sft-mix-accuracy40: night_accuracy, targetstep40, G4, response4096, 32/128 (23/9), joint32.
- rl-sft-mix-g8-pilot: night_split_success, targetstep20, G8, response4096, 36/128 (28/8), joint36.
- rl-sft-scalar: night_scalar_success, targetstep40, G4, response2048, 26/128 (20/6), joint26.
- rl-sft-sirius-continuation3: night_split_success, targetstep40, G4, response4096, 39/128 (29/10), joint38.
- rl-sft-sirius-continuation4-refcorrected: night_split_success, targetstep75, G4, response4096, 39/128 (24/15), joint39.
- rl-sft-split: night_split_success, targetstep40, G4, response2048, 32/128 (22/10), joint31.
- rl-sft-split-stage2: night_split_success, targetstep80, G4, response2048, 36/128 (24/12), joint36.
- rl-sft-tmp3-continuation3: night_split_success, targetstep40, G4, response4096, 33/128 (24/9), joint33.

InitialfreshSFT baseline25/128=15GSM10MATH. Initialthree40step arms use2048response; latermix/math4096 andG8pilotconfound directmethodcomparison.

Pretest frozen primarychoices: Sirius corrected75; tmp2MATHsplit40; tmp3MATHaccuracy80. Math40secondary predeclared before500. Ranking onlyoriginal common128MATH→GSM→correctF; rejectedoldinstruct62/joint0 andwrongreferencecontinuation.

| MATH500 evaluation | Correct | Strict | Joint | Correct nofork | Correct invalidfork | Mean F |
|---|---:|---:|---:|---:|---:|---:|
| new-sft-math500 | 92 | 464 | 83 | 9 | 0 | 608.828 |
| old-mixed-sft-commonbudget-math500 | 101 | 223 | 28 | 48 | 25 | 557.506 |
| final-sirius-math500 | 115 | 477 | 108 | 5 | 2 | 535.596 |
| final-tmp2-math500 | 102 | 487 | 102 | 0 | 0 | 539.604 |
| final-tmp3-math500 | 130 | 483 | 71 | 55 | 4 | 486.750 |
| secondary-mathaccuracy40-math500 | 102 | 488 | 89 | 12 | 1 | 523.254 |

Allsix500 summaries match finalcomparison/progress snapshots; eightworkers eachRC0. Independentfullgrader+RAW/layout/mask/siblingproofs pinned. No testadaptation.

GPU007 alignment: 32comparisons, maxlogitdelta0.0, maxRAWreplaydelta1.23e-06. Committedexport/privatealiasrefresh only; livepostoptimizertrainerRPC remainsunmeasured.

Inference seed42/10042/20042 fresh→math40: overall25→48,36→42,37→40; MATH10→18,15→12,13→14. Theseareinferencevariabilitydiagnostics, nottrainingseedreplication.

Excluded: stopped0.6Binstructzeroautoforks; allnativeTEXT/prompt/phasequalityfail; wrongreferencecontinuation replacedcleanly. Native4B48diagnostic (causalXML) andNEWsix-rowwarmup areseparate, notnightRLsuccess.

Initial accuracy/split/scalar40 arms share freshSFT,easyGSM,G4,batch8,response2048/path1024,costB0256/scale1024,eta.05,LR1e-6,actorKL.001,bonus0; configured seeds do not guarantee paired rollout draws. Results29/32/26 of128 are exploratory, not robust method ordering.
Later math/mix runs use response4096 and changed curricula/anchors/reset or resume; G8pilot changes group size/rollout count. Do not pool as a controlled three-reward comparison.
All12 completed SFT-RL production oracles used canonical schema2, reference-blind lastFinalAnswer after stripping all think tags. Initial split steps1–2 predate schema2; all64 actual selected predictions match canonical exactly, hence no actual reward difference. No version selected answers by matching the reference. Strict-format bonus changes affected only excluded instruct warmups; all completed SFT-RL bonuses0. Historical think-gated grades remain separate.
No groupstd or finalwhitening in night estimators; constant sampleadvantage repeated only across sampledresponsemask. seq-mean-token-mean averages within each trajectory then trajectories; forced/compiler tokens carry no actorloss. ActorKLloss separate from reward.
F logical sampled criticaldepth is sequential main/width/summary plusmaxsiblinglength eachround; notsumoutputtokens. Branch backend runsserially: no measuredGPU-forward or wall-speedup claim.
Compiledjoint requirescorrectfinal+strictformat+executedfork+syntax/runtimeagreement. It is not semantic usefulness, faithfulmerge or RAWcontrolcompliance; nonEOS wrongPath/Summary controls may becompiler-normalized while RAWpolicylabels stayoriginal.
ActualGPU007 proves exactlogits/replay at committedpostoptimizerexport andprivatealiasrefresh, notactive trainerpostoptimizerweight-transferRPC. The latter remainsunmeasured.
Singletrainingseed, adaptivevalidation curriculum/selection and multiplecomparisons. ExactunadjustedMcNemar numbers are descriptive; inference-seedreplicas are nottraining-seedreplication and MATHdirection varies.
OldmixedvsnewSFT differs5145vs3000examples,train/valsplit,and180vs105SFTsteps. Same inferencebudget doesnotisolatedataqualitycausally. Old101 includes47correctunfinishedTHINK+1duplicateclose;historical54/basiccorrect51/joint28 distinct.
Finalmath80_130 includes55correctnofork+4correctinvalidfork; only71jointvsfresh83. No testreselection; secondarymath40waspredeclared based onvalidation.
No oldnight training/eval pending. TwoownedCloudjobs cleanup due09UTC; not yet executed bythisreview. NEW4B15360-row warmup is separateuserauthorizedexperiment outsideN andEXCLUDEDfromoldcleanup.

Cached summaries add only the reporting annotation `predeclared_role`; every actual summary field matches exactly.

Training accuracy semantics: all 12 completed SFT-RL production oracles used canonical schema 2. Initial split smoke steps 1–2 predated that update, but all 64 logged predictions match canonical extraction exactly (5 correct), so their actual accuracy rewards are unchanged. Other completed SFT smokes used schema 2. All extractor versions were reference-blind; no reference-matching candidate selection occurred. Strict format bonus changes were confined to excluded instruct warmups, while every completed SFT arm had bonus 0.



## Independent synthesis: night-final-data-review.md

# Independent NIGHT data/runtime factual review

Completed proof synthesis; source hashes remained unchanged. No runtime/data/model/process actions. The new4B token warmup is a separate authorized experiment and is excluded from09UTC NIGHT cleanup.

NEW SFT used only3000 GSM-Infinite examples (2700/300), fresh pinned0.6B-Base,5epochs105steps. Four existing ChatML/think rows received distinct seeded normal initialization; all other rows/EOS preserved. Maximum source-token length4210, no truncation. OLD5145 comparison changes data mixture, split,180vs105steps, initialization and format; matching inference budgets does not make it a controlled data-only comparison.

Audited RL sources are original TRAIN data; allMATHtest5000 excluded. GSM source/op and normalized300SFT-validation context checks found no overlap. Common128 was adaptively reused for curriculum and selection, so it is validation, not untouched test. Final500 was excluded from learning/selection; choices were frozen06:43:13. Exact checks cannot rule out every semantic near-duplicate.

|500-question structured evaluation|Correct|Strict|Correct + valid executed fork|
|---|---:|---:|---:|
|new-sft-math500|92|464|83|
|old-mixed-sft-commonbudget-math500|101|223|28|
|final-sirius-math500|115|477|108|
|final-tmp2-math500|102|487|102|
|final-tmp3-math500|130|483|71|
|secondary-mathaccuracy40-math500|102|488|89|

Full primary+secondary runtime audits cover2500traces,14442RAWcalls,5247isolatedpaths with no recorded label/actionmask/position/pathmask/Unseen/sibling/F-T bookkeeping errors. Export/checkpoint/source/tokenizer identities were checked. This is CPU metadata proof, not live model-logprob/forward-speed measurement. Wrong-terminal compiler normalizations remain an explicit limitation;55of130correct math80 answers use no fork. OLDmixed has265unfinished-think outputs,47correct under canonical primary extraction.

|Inference seed|Fresh correct GSM/MATH|MATH40 correct GSM/MATH|Total|Losses/gains|
|---|---|---|---|---|
|42|[15, 10]|[30, 18]|25→48|7/30|
|10042|[21, 15]|[30, 12]|36→42|17/23|
|20042|[24, 13]|[26, 14]|37→40|20/23|

MATH direction flips(+8,-3,+1). These are inference draws on the same128questions and one trained checkpoint per condition, not independent training replicas or384 independent questions. Diagnostic replicas never entered selection; adaptive comparisons and unadjusted tests do not support a robust significance/causal claim.

Failed branches remain failed: semantic six-row initialization had5/24correct but0executedforks; special-token instructV2 stopped after two actual post-guided steps showed0autonomousforks; nativeTEXT v3/v4/phase failed protocol quality gates. Phase summary-import failure was recovered externally on unchanged traces; recovered unguided24 had12correct/21strict/0joint and guided24 had3correct/7strict/1joint. No phase PPO/long run started. Isolated TEXT versions fixed real BPE-boundary and dualEOS defects, so failures are not all prompt failures.

The Sirius continuation reference bug was real: actor/optimizer resumed while the KL reference loaded freshSFT. Faulty updates were discarded; corrected run restarted the original pre-error step40 with the prior accuracy-stage1HF reference, verified41/42smoke and committed checkpoints, and finished75. The wrong run and evidence were preserved and excluded.

Joint means correct final plus strict syntax and actual fork, not semantic usefulness. Selected algebra216/392 traces contain contradictory paths and summaries falsely claiming agreement; prealgebra609 paths repeat givens. These targeted examples do not estimate prevalence. F is logical depth, not total work or speedup; structured HF branches are serial. Source-inferred forward counts and native-vLLM wall times must not be presented as measured acceleration. Primary strips think markup before answer extraction; historical think-gated scores and format validity stay separate.

Original4B diagnostic:21/24optional and23/24requested answers correct. Each arm18/24writes XML only after closing think;0/48validinside-thinkforks. Requested outside-think width3 headers17vsoptional9. No SFT, added tokens, embedding changes, Unseen or executed parallel branches occurred in this probe; it is a small prompt diagnostic.

Evidence paths and exact source SHA256 pins are in the companion JSON, including SFT/data proofs, final comparison, full runtime proofs, replica analysis, failed gates, reference recovery, and full-response4B accounting.

