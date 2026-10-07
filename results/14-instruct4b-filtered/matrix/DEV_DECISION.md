# Dev decision record: 14-filtered / 15-random-control (written BEFORE any frozen job of 14/15 was queued)

Scope: the pre-registered first cycle (13 full / 14 filtered / 15 size- and length-matched random). Frozen no-thinking, thinking16k
and parallel are pre-authorized for all three arms (EVAL_ALLOWED + scope clarification) and are run regardless of the dev outcome,
to measure the trade-off. Nothing below selects a recipe, retunes anything, or adds an arm. The proposed 2 pp margin is a working
proposal, not user-confirmed. Primary metric: pass@1 (mean over samples), robust parser; strict shown where it diverges.
All numbers: scripts/instruct4b_eval/paired_compare.py (84e2140), 95% bootstrap CI over unique problems, files in compare/.

## Training (identical recipe, B GPU0/1, commits baad652 / dbe704b = 84e2140 + recipe.md)
64 updates, global batch 64, micro batch 2 (as accepted 13), lr 1e-5 warmup 6 cosine, max len 4096, GC, FSDP2, sampler seed 0
(trainer.seed not implemented; one training seed only). Both: 4096 distinct rows processed of 4248, finite grads, bf16 export.
| arm | val/loss@64 (dev_untouched 296) | processed target tokens |
|---|---|---|
| 13-control (recovery/executor) | 0.5342 | 1,723,182 |
| 14-filtered | 0.5342 | 1,674,287 |
| 15-random | 0.5336 | 1,680,811 |

## Dev no-thinking (vs C0 = original Qwen3-4B)
| bench | 13 | 14f | 15r | 14f-15r |
|---|---|---|---|---|
| ARC | -0.92 [-2.93,+1.17] | -1.42 [-3.51,+0.67] | -2.01 [-4.18,+0.17] | +0.59 [-1.00,+2.26] |
| GSM8K | +1.27 [-1.94,+4.65] | +2.36 [-0.51,+5.32] | +2.11 [-0.84,+5.24] | +0.25 [-1.44,+1.94] |
| MATH | -7.88 [-11.31,-4.46] | -9.44 [-13.07,-5.81] | -8.51 [-11.93,-4.98] | -0.93 [-3.73,+1.87] |
| MMLU-Pro | -0.60 [-3.60,+2.40] | +0.70 [-2.30,+3.80] | +0.40 [-2.60,+3.40] | +0.30 [-2.50,+3.20] |
Prepared-no-SFT (P) vs C0 ~0 everywhere (recovery/executor). Strict (format) accuracy rises strongly after SFT (MATH 20 -> 54).
MATH loss partly parser: Unicode-math final lines in robust-wrong rows 14f 36/316, 15r 47/307, C0 0 (diag-unicode.log); upper
bound still leaves >= ~6 pp. Manual sample: broken final lines + some real errors (audit-math-dev-nothink-14f.txt).

## Dev thinking 16k (vs C0 thinking)
| bench | 14f vs C0 | 15r vs C0 | 14f-15r | truncation C0 / 14f / 15r (%) |
|---|---|---|---|---|
| ARC | -2.34 [-4.18,-0.59] | -3.68 [-5.69,-1.76] | +1.34 [-0.17,+2.93] | 0 / 25.8 / 20.9 |
| GSM8K | -11.40 [-13.94,-8.87] | -13.01 [-15.62,-10.39] | +1.60 [-1.18,+4.39] | 0 / 26.2 / 32.8 |
| MATH | -17.43 [-20.12,-14.73] | -18.46 [-21.37,-15.56] | +1.04 [-1.87,+3.94] | 2.5 / 27.4 / 31.6 |
| MMLU-Pro | +9.11 [+5.91,+12.31] | +6.21 [+3.00,+9.41] | +2.90 [+0.10,+5.61] | 2.3 / 22.2 / 39.6 |
MMLU-Pro gain vs C0 is unexpected (C0 thinking 55.96 < C0 no-thinking 60.66 on the same problems); not interpreted as a skill gain
without inspection. Truncation 14f-15r: ARC +4.8 [+1.5,+8.3], GSM8K -6.6 [-10.2,-3.0], MATH -4.3 [-7.9,-0.6], MMLU -17.4 [-21.3,-13.6].
Manual (14f GSM8K): answers early, no </think> in 88% of truncated rows, loops "Final Answer" to budget. Thinking-mode termination
is lost after SFT in both arms; this is the largest observed regression. 13-control dev thinking: pending recovery owner.

## Dev parallel (opt-in prompt, genuine rollout, enable_thinking False; post-check fix 9227d52, reviewed)
| bench | 14f-15r | 14f par - own nothink | 15r par - own nothink |
|---|---|---|---|
| GSM8K | -1.18 [-3.89,+1.52] | -10.22 [-12.75,-7.69] | -8.78 [-11.23,-6.42] |
| MATH | -3.73 [-6.95,-0.52] (strict +0.73 [-2.39,+3.73]) | -9.02 [-12.24,-5.91] | -6.22 [-9.34,-3.22] |
Parallel share ~89-92%, valid_tags 15-21% (dump structure irregular, FINDING-parallel-dump-check.md §2), no arm difference in
structure metrics.
vs P (prepared, no SFT) with the same parallel prompt (prep-dev-par, recovery owner's run, rows copied read-only): P uses blocks
in 0-1% of answers (ignores the opt-in instruction) and scores GSM8K 92.82 / MATH 77.28 (robust). 14f: -11.40 [-14.44,-8.53] /
-19.09 [-22.72,-15.46]; 15r: -10.22 [-13.09,-7.51] / -15.35 [-18.98,-11.72]. SFT teaches the format (~90% blocks) but the
learned parallel behaviour costs 10-19 pp accuracy vs the untrained model on the same prompt (added after the frozen queueing;
no decision changed).

## Decision (no selection)
1. Filter hypothesis on dev (14f vs matched random 15r): no-thinking no detectable difference (all CIs include 0); parallel MATH
   robust favours random -3.7 [-7.0,-0.5] but strict shows none (+0.7, fragile); thinking: 14f >= 15r everywhere (MMLU-Pro +2.9
   [+0.1,+5.6], others include 0) and less truncation on 3/4 benches. Mixed, small, mode-dependent; single training seed, so
   between-seed noise is not in these intervals. No claim that filtering helps or hurts.
2. Shared SFT effects dominate arm differences: no-thinking MATH loss ~8-9 pp, thinking termination failure, parallel mode below
   plain. These are recipe/data-style effects common to all arms.
3. Proceed to frozen for 14/15 as pre-registered: no-thinking + parallel first, thinking16k last (most expensive: looping to 16k
   on ~25% of samples, LIMO 3268 rows). Frozen results are diagnostic (already-viewed benchmarks), not independent confirmation.
