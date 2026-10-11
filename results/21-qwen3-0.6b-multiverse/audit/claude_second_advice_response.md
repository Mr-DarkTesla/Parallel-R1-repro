## 1. Fastest discriminating experiment after the 196-row pair

Before adding new data, find out whether the accuracy drop comes from the recipe or from the parallel data. In the 78-row pair, both arms fell by the same amount (34 → 23 tagged, 34 → 22 plain), so the tags are probably not what cost accuracy. The likely causes are the shared replay mix, the ×100 repetition, or optimizer drift from the recovery checkpoint.

The cheapest runs that separate these:

- **Replay-only arm.** Same recovery checkpoint, same 300+300 Qwen replay, same lr and steps, no positives. One extra run. If it also drops to about 22–23/40, the damage is in the recipe, and further data work on 0.6B won't show anything until that's fixed.
- **Forced-prefix probe, no training.** Prefill the opening parallel tag on fixed40 for the recovery checkpoint and for the 196-tagged checkpoint, then score useful independent blocks. This separates "can't produce useful parallel paths" from "doesn't trigger them."
- **Intermediate checkpoints.** If the 24-step run saves checkpoints (say 8/16/24), score them on fixed40 as well. This costs no extra training.

Decision rule for the 196 pair: count it as a signal only if tagged useful blocks clearly beat 2/40 (≥8/40, with a manual review that is blind to the arm) and tagged correctness is within about 3 of plain. With n=40, a gap of fewer than about 5 correct answers is noise unless the discordant pairs are lopsided. Use McNemar on the pair, not raw counts.

## 2. The 2251-row M1 pair: is 16 steps enough, and what grid?

At batch 32, 16 steps is 512 rows, about 0.23 epoch. About half of those are positives (1101 of 2251 rows). After tripling, that is roughly 250 positive rows, or about 85 unique M1 examples seen once.

16 steps is not hopeless for learning the syntax: the 78-row pair reached 19/40 numbered blocks in 8 steps. It is too little to say anything about the M1 data as a whole, because it only tests a small sample of it.

Suggested grid:

- One run per arm, constant lr after warmup, so the checkpoints of a single run form the grid instead of separate decayed runs.
- Save at **16, 35 (≈0.5 epoch), 70 (≈1 epoch)**.
- Extend to **140 steps** only if the 70-step checkpoint still improves useful blocks and plain correctness hasn't dropped further.
- Keep lr at 3e-6 and change only the number of steps, so the results stay comparable with the 78-row and 196-row pairs.
- Add a stop criterion: if correctness falls more than 3 below that arm's 16-step score while useful blocks stay flat, stop.

The wrapped M1 text was written outside thinking, so its style differs from Qwen's own thinking. If it learns tags but useful blocks stay flat, suspect that style gap before blaming the step count.

## 3. Threshold for moving the SFT target from 0.6B to 4B

Switch only when the evidence points to 0.6B capacity, not to the recipe. My proposed thresholds:

1. **The recipe isn't the cause.** The replay-only control holds correctness within about 3 of 34/40. Otherwise 4B inherits the same damage and nothing is learned.
2. **0.6B has a ceiling.** Across both data sources (196 Sol6.1 and M1) and at least two step points, the best 0.6B tagged checkpoint stays at ≤5/40 useful independent blocks, even though the syntax is learned (≥15/40 numbered blocks).
3. **4B has headroom.** The untrained 4B forced-prefix probe on fixed40 gives at least 3× the useful blocks of the 0.6B best, for example ≥15/40.
4. **The eval can still measure gains.** 4B base on fixed40 must be below the ceiling. If it scores about 38–40/40, first build a harder dev set (still around 40 prompts) before training 4B, or accuracy changes can't be detected.

If conditions 1–3 hold, 4B is justified, and its first run should copy the best 0.6B recipe unchanged. If condition 1 fails, fix the replay/lr recipe on 0.6B first; that is much cheaper than any 4B run.

These thresholds are my judgment, not measured breakpoints. Adjust them to how noisy you've found the manual usefulness review to be.
