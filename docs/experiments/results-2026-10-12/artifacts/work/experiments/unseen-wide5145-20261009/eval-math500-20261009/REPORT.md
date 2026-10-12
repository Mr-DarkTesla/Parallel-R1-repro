> **SUPERSEDED PARTIAL BASELINE — 343/500, not a complete MATH-500 score.** Preserved before switching to user-requested automatic first think prefix. New full evaluation: `../eval-math500-forced-think-20261009/`.

# Qwen3-0.6B Base counted Unseen SFT: MATH-500

State: **partial**, 343/500 answers. Report generated 2026-10-10T00:11:01.344971+03:00.

Checkpoint: `${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/runs/01_sft/final`.

One independently sampled answer per question (pass@1 estimate), all 500 previous MATH-500 questions. Temperature 0.6, top-p 0.95, top-k 20, seed 42; response budget 30720, path budget 8192, model context 32768. Model-selected widths 2..8, unlimited fork rounds subject to total tokens. Exact protocol and question/checkpoint hashes are in `manifest.json`.

## Accuracy

| Model/run | Historical extraction | Final-answer-only diagnostic |
|---|---:|---:|
| gsm_infinite_ep5 | 84/500 = 16.8% | 84/500 = 16.8% |
| sft_messages_ep5 | 79/500 = 15.8% | 79/500 = 15.8% |
| mixed_ep1 | 61/500 = 12.2% | 61/500 = 12.2% |
| New SFT, 343 answers | 40/343 (11.7%) | 64/343 (18.7%) |

Historical metric Wilson 95% CI: 8.7–15.5%. Final-answer-only diagnostic CI: 14.9–23.1%. Scorer errors: 0. Historical extraction-invalid outputs: 127; final-answer-only extraction-invalid: 9.

Historical extraction uses the previous reference-blind extraction and Math-Verify 0.8.0 symbolic equivalence unchanged. It rejects an opening `<think>` without any closing, but its inherited logic can accept a reopened think after an earlier closing. The separate diagnostic removes think tags before the same reference-blind final-answer extraction; it does not inspect the gold answer to select candidate text. Both methods reproduce every historical score (84/79/61) on all previous saved outputs. This diagnostic is not a claim of proper format or sound reasoning.

This comparison changes more than weights/data: the new run uses the trained long system prompt, genuine Unseen masks/positions and model-selected width. Previous runs used a shorter prompt, causal vLLM inference and forced two-branch forks. Treat differences as end-to-end system results, not a controlled attribution to SFT alone.

## Traces

- Parallel questions: 251/343 (73.2%); more than one fork: 17/343 (5.0%).
- Forks per response: `{'0': 92, '1': 234, '2': 13, '23': 1, '3': 1, '4': 1, '59': 1}`. Completed fork widths: `{'2': 264, '3': 34, '4': 42, '5': 7, '6': 2}`.
- Invalid counted width: 5; invalid assembled parallel structure: 11. Runtime inserts numbered path openings and repairs path/summary stops, so assembled format validity is partly guaranteed by runtime.
- Exactly one balanced think pair: 63; fully valid think placement (all forks inside, final outside): 62. Counts of emitted open/close think tags: `{'open=0,close=0': 12, 'open=0,close=1': 78, 'open=0,close=2': 32, 'open=1,close=0': 69, 'open=1,close=1': 98, 'open=2,close=0': 53, 'open=2,close=1': 1}`.
- Response-budget exhausted: 1; generation calls reaching their individual budgets by phase: `{'path': 2, 'main': 1}`. A branch cap can cause an injected closing and still permit a later final answer.
- Runtime closing-label replacements: 6; original sampled labels remain in policy-call records.
- Exact duplicate branch texts within a trace: 166. Paths with repeated 5-gram fraction >50%: 3. Lexical repetition flags do not measure semantic redundancy.

| Metric | Mean | Median | p90 | Max |
|---|---:|---:|---:|---:|
| response_tokens | 981.33 | 519.00 | 1044.00 | 30720.00 |
| sampled_tokens | 970.88 | 510.00 | 1034.40 | 30711.00 |
| forced_tokens | 10.45 | 9.00 | 15.00 | 531.00 |
| critical_depth | 858.07 | 431.00 | 895.40 | 30645.00 |
| sampled_work_over_critical_depth | 1.14 | 1.12 | 1.32 | 1.62 |
| elapsed_seconds_per_question | 35.19 | 15.03 | 30.69 | 1566.09 |
| generation_calls | 6.53 | 6.00 | 8.00 | 296.00 |

Work/depth is theoretical sampled-token work divided by longest serial token depth. Paths execute sequentially on each GPU in this correctness evaluator; no wall-clock parallel speedup was measured.

### Accuracy by subject

| Subject | Correct / n | Historical pass@1 | Final-answer-only |
|---|---:|---:|---:|
| Algebra | 21/80 | 26.2% | 38.8% |
| Counting & Probability | 3/25 | 12.0% | 12.0% |
| Geometry | 3/32 | 9.4% | 15.6% |
| Intermediate Algebra | 3/71 | 4.2% | 4.2% |
| Number Theory | 2/39 | 5.1% | 10.3% |
| Prealgebra | 5/52 | 9.6% | 23.1% |
| Precalculus | 3/44 | 6.8% | 13.6% |

### Accuracy by difficulty

| Level | Correct / n | Historical pass@1 | Final-answer-only |
|---|---:|---:|---:|
| 1 | 8/30 | 26.7% | 46.7% |
| 2 | 14/61 | 23.0% | 24.6% |
| 3 | 10/76 | 13.2% | 25.0% |
| 4 | 6/86 | 7.0% | 9.3% |
| 5 | 2/90 | 2.2% | 8.9% |

## Manual semantic review

Reviewed 27 deliberately selected traces spanning sequential/parallel, correct/incorrect, wider and repeated forks, and long/repetitive outputs. This is a purposive diagnostic review, not a random estimate of a semantic quality rate.

The model sometimes makes useful independent assignments (e.g. separate function evaluations) and combines their results correctly. Other forks merely repeat already computed values, extract given constants, or calculate irrelevant quantities. Some summaries alter or invent path results. Correct final answers can coexist with invalid reasoning. Long arithmetic loops remain possible. The numeric ID supplies the branch assignment; isolation prevents observing sibling content but cannot guarantee the model follows the intended assignment or invents no facts.

- Question index 0, **partly_sound**: Правильный ответ (3,pi/2), но arctan(3/0) записан через деление на ноль; лучше вывод по положительной полуоси y.
- Question index 2, **useful_parallel_correct**: Три независимых подстановки f(-2),f(-1),f(0) выполнены верно и корректно объединены в14/3. Think-теги перепутаны: close до work/open после.
- Question index 4, **correct_answer_invalid_reasoning**: Evelyn угадана/получена при неверной интерпретации графика: придуманы времена, вместо distance/time произведения; сравнение не обосновывает ответ. Верный pass@1 не гарантирует валидный трейс.
- Question index 6, **format_loss_and_gap**: Итог27 верен, primary отвергает из-за<think>вместо</think>. Минимальность недостаточно обоснована, формулировка что n must multiple3 сама по себе недостаточна.
- Question index 8, **correct_but_precomputed**: Расстояние3sqrt13 вычислено верно. Обе разности уже вычислены до fork, ветви повторяют известные результаты. Итог потерян primary только из-за think-тега.
- Question index 1, **wrong_decomposition_and_math**: Двойная сумма требует группировки по j+k; вместо этого бессмысленный план p²,q² и ложные равенства Коши. Правильно p-q, ответp²+q².
- Question index 3, **wrong_path_and_summary**: Path2 ошибочно считает9 делителей7²; summary складывает вместо умножения количества выборов. Ответ12 вместо9.
- Question index 10, **decorative_wide_and_wrong**: Width4 искусственный: почти одинаковые задачи про22, неверные counts и подмена цифровой записи2^n; ответ10 не кратен30 и содержит запрещенную1. Правильно2220.
- Question index 11, **useful_local_paths_failed_global**: Width5 корректно считает p(2)..p(6), но пропускает данноеp(7), объявляет5точек достаточными, подменяет значения коэффициентами и незаконно применяет исходнуюформулу к8. Правильно3/56.
- Question index 21, **multi_round_failed_integration**: Два fork реально исполняются. В первом неверное раскрытиеa², во втором Path1 не доводит вычисление; summary выдумывает результатa6, итоготрицательный вместо13535.
- Question index 35, **multi_round_decorative_and_corrupted_summary**: Первыйwidth3 вычисляет заданныеконстанты2,4,6. Во втором независимые остатки полезны, ноsummary меняетостатокn+4с6на1 и получает4 вместо3.
- Question index 28, **correct_answer_decorative_fork**: Поворот наi вычисленверно. Ветки реальнаячасть7,мнимая2,ихпроизведение14 тривиальны;14 неиспользуется врешении. Правильныйответ маскирует лишнийfork.
- Question index 18, **nonsensical_geometry**: Придуманпрямойугол, неверныеравныеуглы и отрицательныйугол-192 названсогласованным. Правильныйответ28.
- Question index 19, **wrong_algebra_and_constraints**: Ошибочныйдискриминант, неверныефакторизации иa=-1нарушаетусловиеa>0. Правильныйответ3.
- Question index 101, **repetition_and_wrong_math**: Width4 затем5: Path4 первогоfork зацикливается на13-13 и упирается в8192pathcap; runtimeзакрываетего, модельпродолжаетотнесуществующихфактов. Итог145.846необоснован.
- Question index 145, **repetition_and_wrong_math**: Path2 зациклен наrz²-z-r до8192pathcap; summary продолжаетложныепреобразования. Финальныйответ неверен.
- Question index 247, **false_conjugate_and_algebra**: Ошибочныйодинаковыйсопряженныйкорень, потеряconstantterm, неверныеподстановки. В summary и заключении повторяетсяложныйвывод, итог0.
- Question index 248, **incorrect_matrix_operations**: Триbranchзадачипонезависимымстепенямформальноразумны, но покомпонентноевозведениевстепень,подменатargetматрицыследом ифальшивыеправиластепеней делаюттрейсневерным.
- Question index 109, **independent_terms_wrong_math**: Width4частичноразумнаядекомпозициятригонометрическихчленов, но изменены знаки и формулы; summaryзаменяетнеполученныезначения. Итогневерен.
- Question index 67, **correct_answer_precomputed_and_summary_error**: Ответ10верен, но весьрасчетвыполнендоwidth3fork. Веткиповторяютготовое, summary путает60%сохраненияс60%уменьшения.
- Question index 121, **correct_but_redundant_verification**: Триветки самивыводятоднутожесистему; Path3 объявленverification,нонеподставляетнайденноеxдоsummary иутверждаетсовпадениесневидимымиsiblings. Итог6верен; summaryкорректнопроверяет3+2=5.
- Question index 137, **invalid_width_one_terminates**: Первыйforkдо108/2=54содержательноработает, затеммодельоткрывает<Parallel>1дляодногоперевода54вbase5. Runtimeзакономернопрерываетневалиднуюширину; итог204_5невысказан.
- Question index 141, **fabricated_inputs_contradiction_and_width_one**: Вветкахнезависимопридуманычислапенсилов9и51, summaryназываетихсовпавшими. Затем<Parallel>1терминируетответ. Этоошибкагенерации, неизоляциимаски.
- Question index 122, **correct_core_contradictory_conclusion**: Основноеобратнопропорциональноевычисление22500/2500=9верно; заключениесодержитложно15*6=9. Correctpass@1неслужитпроверкойкаждойстроки.
- Question index 132, **correct_math_invalid_think**: Последовательноиправильноперечисленыобщиеделители1,2,7,14. Ответ4верен, ноявнооткрытthinkдваждыбеззакрытия, primaryотвергает.
- Question index 83, **59_repeated_fork_rounds_no_progress**: Уравнение3^(2x)+19=10^x:59двухветочныхраундовповторяюттождественныепереписыванияy=10^x; затемтекстдеградируетвповторяющиесяобрывки.26332responseтокенов,1365.8s,нетфинальногоответа. Runtimeобработал296generationcallsбезконтекстныхошибок.
- Question index 380, **width6_then4_wrong_sign_analysis**: Неправильноопределеныкритическиеточки0,±6вместо0,36,±9; однаветкаошибается(-6)^2, summaryподменяетdenominator-180на252. Первыйwidth6выполняется,второйwidth4повторяетзадачи;решениеинтерваловневерно.

## Independent code audits

All-trace accounting checks: `{'forks_checked': 349, 'sibling_prefix_mismatches': 0, 'policy_label_or_mask_errors': []}`.

- `audit-inference.md`: independent 234-trace snapshot plus CPU tests verified sampled labels/action masks, exact shared/sibling contexts and IDs, Unseen positions, and sampling parameters. Historical scorer caveat is recorded. The new scorer CLI now delegates to the actual analyzer.
- `audit-sft-findings.json`, `audit-sft-check.json`, `audit-sft-provenance.json`: all 5145 examples reconstructed and retokenized, no truncation, causal shift/EOS checked, no change to frozen code or sources. Four-layer synthetic Qwen checks widths 2..8 and repeated forks; these check semantics, not checkpoint quality. Width 8 has only 15 training fork occurrences and zero validation occurrences. Old 2145 examples omit the short concluding arithmetic requested by the common prompt.
- `audit-rl.md`: per-call PPO replay, forced-token exclusion, live weight aliases, collective count synchronization and published S1/S2 rewards checked. Production width parser was tightened to exact ASCII `[2-8]\n`; trace truncation telemetry was corrected. CPU tests include mixed widths 2→8→3. Production fixes do not mutate the running evaluation snapshot; observed evaluation headers are recorded in trace data.
- Additional single-GPU production canary: width8, 8190 response tokens plus2padding, 11 exact per-call replay forwards, 8163 sampled labels and finite backward gradients; peak allocated8.43GiB. Actual vLLM cached decode on8067-token summary prefix versus actor replay: mean log-probability error0.00368, max0.02112. No optimizer/checkpoint write. See audit-rl/long-context-results.json.
- Prior eight-GPU RL smoke ran two PPO steps with a short384-token response budget. A full-length distributed8192-token production RL run and a fresh direct post-PPO GPU logit comparison were not performed in this audit. No production RL training was started.

## Artifacts and reproduction

- `traces-0.jsonl` through `traces-7.jsonl`: complete outputs, questions, raw generation calls/contexts/labels/parameters and assembled tokens/masks/positions.
- `scores.jsonl`, `trace-statistics.jsonl`, `summary.json`: reference-blind grades and detailed statistics.
- `previous-comparison.json`, `previous-*-scores.jsonl`: independent historical output rescores.
- `trace-review.json`: saved manual assessments.
- `final-validation.json`: final sample coverage, hashes, immutable checkpoint/source verification and process completion evidence (created at the end).

CPU analysis from project root:

```bash
.venv/bin/python work/experiments/unseen-wide5145-20261009/eval-math500-20261009/score.py --final
.venv/bin/python work/experiments/unseen-wide5145-20261009/eval-math500-20261009/report.py
```
