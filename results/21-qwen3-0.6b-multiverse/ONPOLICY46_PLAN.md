# On-policy 46: fresh candidate gate

This document prepares a CPU-only task manifest. It does not start a rollout,
training job, pod, proxy request, or paid call.

## Candidate manifest

`scripts/exp21/prepare_onpolicy46_candidates.py` selects 256 questions from
canonical `data/pool.jsonl`: 128 GSM8K and 128 MATH. MATH targets 64 integer,
40 expression, and 24 fraction answers. The fixed seed is
`onpolicy46-candidates-v1-20261011`; each source ID ranks by SHA-256 of the
seed and ID.

Before selection, the script fails if any source is missing or malformed. It
reads all 78 `sft_*_{train,val}.parquet` variants, the fixed 40-question
`c0-greedy-pilot40.tgz`, and the existing leakcheck script plus its eval corpus.
Question comparison uses Unicode NFKC followed by whitespace collapse. For each
parquet prompt it compares both the full stored question and text after its last
`Problem:` marker. The one ID-only validation manifest resolves each ID through
the canonical pool before comparison. Candidate text must differ from every SFT
and pilot question. Any question containing `[asy]` (case-insensitive) is
excluded before ranking because its diagram code cannot be supplied reliably to
the text rollout; its IDs and count appear under `asy_question` in the audit.
The existing leakcheck policy rejects leaks against every non-info eval corpus
and `dup` or `variant` against `math_test_full(info)`.

Run only on a local CPU environment that has pandas/pyarrow and access to the
existing survey artifacts:

```sh
python3 scripts/exp21/prepare_onpolicy46_candidates.py \
  --leakcheck /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py \
  --eval-corpus /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus
```

It writes `data/onpolicy46_candidates.jsonl` and
`data/onpolicy46_candidates.audit.json`. The audit records all input parquet
paths and row counts, seed, selected IDs, selected IDs by source and MATH answer
type, pilot IDs, plus every rejected collision ID. The candidate file retains
gold answers for offline grading only. Rollout prompts receive only `question`.

## Rollout acceptance gate

Each accepted row needs all of these independently verified conditions:

1. External final answer is correct against the candidate gold answer.
2. Exactly one complete, numbered Multiverse block is wholly inside one
   `<think>...</think>` block; no structural tag appears outside it.
3. It contains at least two true independent paths. Neither path depends on,
   references, repeats, or merely checks another path; the conclusion combines
   their separate results.
4. The answer was not precomputed: no gold answer, prior candidate answer,
   cached completion, or solution text is provided to the model prompt or used
   as a substitute for the model's external answer.

Only train after at least 46 unique candidate IDs pass all four conditions,
including at least 18 GSM8K IDs. The accepted MATH subset must contain at least
six integer, six expression, and six fraction answers. Preserve the per-row
acceptance evidence, source ID, generated text, independent review, and failure
reason for rejected rows before forming training data.

## Staged rollout before spending the full GPU budget

First generate two sampled sibling-masked traces for the first 32 MATH and
32 GSM8K questions in the committed candidate order, seeds 0 and 1. Use the
same Multiverse prompt, temperature 0.6, top-p 0.95, top-k 20, at most
4096 new tokens for MATH and 2048 for GSM8K. Store all 128 outputs,
including rejected ones. Automatically filter only grammar, placement,
truncation, external answer and length; then manually judge every remaining
block for mathematical truth and independence.

Continue the 256-question rollout only if this pilot yields at least four
unique accepted tasks, including one GSM8K, with no answer or placement
violation among accepted rows. Otherwise record the failure and stop before
SFT. This early gate is a resource decision, not a claim about the full
candidate pool or model quality.

## Execution log

The selector produced 256 clean candidates: 128 GSM8K and 128 MATH,
including 64 integer, 40 expression and 24 fraction answers in MATH.
It excluded 583 questions containing `[asy]` and 1,424 questions already
represented in SFT texts before ranking. Selection and rejection IDs are
recorded in [candidate audit](data/onpolicy46_candidates.audit.json);
the [candidate JSONL](data/onpolicy46_candidates.jsonl) contains gold answers
only for later grading.

After the previous fixed40 evaluations completed and the one owned GPU was
free, the 32+32 questions × seeds 0,1 rollout was started on
`vcharkin-exp-vm-0` via `generate_onpolicy_masked.py`. Pod shell PID
`40644`; persistent output and log are
`/work/exp21/onpolicy46/recovery8_step8_masked_pilot128.jsonl` and
`/work/exp21/onpolicy46/recovery8_step8_masked_pilot128.log`.
The output is incomplete until 128 distinct `(id, seed)` rows exist and the
process exits successfully. A CPU prefilter smoke test on the first eight
complete rows yielded one provisional MATH row; this is diagnostic only,
not the pilot's final acceptance count.

The first 32 complete rows were snapshotted while generation continued.
The automatic checks passed 5/32. Blind semantic review accepted 2/5:
`math-train/110` seed 1 and `gsm8k-train/2528` seed 0. Two provisional
rows had incorrect or duplicate paths, and one had already computed its
answer before the block. Both GSM8K verdicts were independently reviewed.
The [review](audit/onpolicy46_first32_primary_review.md),
[provisional rows](audit/onpolicy46_first32_provisional.jsonl), and
[filter summary](audit/onpolicy46_first32_summary.json) are interim
evidence only. The predeclared continuation gate applies to all 128 rows.

A second in-progress snapshot at 64 rows had 13 provisional after
automatic checks. Manual review accepted 3/13 unique tasks, including
two GSM8K: the first two above and `gsm8k-train/4597` seed 0.
The latter GSM8K verdict received an independent second review.
The [64-row filter summary](audit/onpolicy46_first64_summary.json),
[provisional rows](audit/onpolicy46_first64_provisional.jsonl), and
[review sheets](audit/onpolicy46_first64_review_a.md) for
[rows 10–13](audit/onpolicy46_first64_review_b.md) are interim only.
The 128-row gate still decides whether to proceed.

At 96 rows, 19 passed automatic checks; blind review kept the same
3 unique tasks and rejected 16 for duplicate, missing, or false paths,
or an answer already computed before the block. Every provisional
row's external answer was correct. The [96-row summary](audit/onpolicy46_first96_summary.json),
[provisional rows](audit/onpolicy46_first96_provisional.jsonl), and
[reviews for rows 14–16](audit/onpolicy46_first96_review_a.md) and
[17–19](audit/onpolicy46_first96_review_b.md) record the interim result.
The continuation threshold remains four unique accepted tasks at 128 rows.
