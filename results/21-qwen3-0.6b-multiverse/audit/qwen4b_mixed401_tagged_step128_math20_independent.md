# Independent review and arithmetic re-audit: step128 MATH20

Scope: all ten outputs from each of `math_dev10.jsonl` and `math_devnext10.jsonl`, read with their matching `*-rows.jsonl` and `*-block-rows.jsonl` in `eval_archives/qwen4b_mixed401_tagged_step128/`. This review was made from the outputs and source problems, without using earlier manual verdicts.

| Check | Count / 20 |
| --- | ---: |
| Automatic `acc` true | 15 |
| Manually verified final answer correct | 15 |
| Block wholly inside `<think>` and grammatically numbered | 19 |
| Both first two paths substantive and independent | 10 |
| No erroneous intermediate | 14 |
| Correct conclusion | 13 |
| Strictly useful | 4 |

An independent second reviewer checked every problem and calculation after a mistake was found in the first review. The automatic scorer is correct on all 20 finals. `math-test/88` must have `e=2`: the generated solution computed `17*9` as `159` instead of `153`. The other wrong finals are `math-test/98` (correct `(9,11)`), `math-test/117` (correct `(2,12)`), `math-test/129` (correct `2009/4`) and `math-test/137` (correct `1`). The four strictly useful blocks are `math-test/9`, `36`, `93` and `103`.

The dominant failure mode is semantic, not tag parsing: many paths repeat a supplied constant, duplicate the sibling's calculation, or use the sibling result. `math-test/130` additionally has duplicate path numbering. The strict criterion requires a correct final answer, valid block inside `<think>`, substantive independent paths, error-free reasoning, and a correct conclusion.

The per-ID evidence and corrected verdicts are in `qwen4b_mixed401_tagged_step128_math20_independent.jsonl`; the correction list is in `qwen4b_mixed401_tagged_step128_math20_reaudit.json`.
