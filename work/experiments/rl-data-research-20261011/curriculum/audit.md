# Curriculum audit, 2026-10-11

Read-only Sirius audit; no jobs or allocations launched. All remote paths below are relative to `${PROJECT_ROOT}`.

## Checkpoint identity and quality floor

`work/experiments/unseen-wide5145-20261009/runs/01_sft/final` completed 180 steps on 2026-10-09 19:55 UTC. Config has hidden_size 1024, 28 layers, intermediate_size 3072: this is the 0.6B architecture, not the current 4B Base. Manifest checkpoint sha256: `fa9e92602b36042e0f4f488b5ccf6a8956826978f9d9d9cbfa9e80792a3be6c6`.

Its `eval-math500-forced-think-20261009/summary.json` is complete: 101/500 = 20.2% primary answer equivalence (Math-Verify 0.8.0, reference-blind extraction independent of think validity). The legacy think-gated value 54/500 = 10.8% is not current primary scoring. The prior non-forced evaluation is partial, 343/500. Protocol: one sample, seed42, temperature0.6/top_p0.95/top_k20, response budget30720/path8192, structured vLLM weight backend, exact Unseen masks/positions, automatic initial think prefix masked out of actions. Mean generation calls5.396 and sampled tokens1053.032 are not actual HF generation-forward counts; branch execution is sequential per GPU.

This historical result cannot establish the current 4B Base quality floor. Rerun the intended unseen-SFT comparator under the same final runtime, questions, scorer, budgets, and seeds before applying the hard floor.

## Current frozen GSM curriculum

`work/experiments/rl-campaign-20261010/runner/revision2/data/manifest.json`: train1024, selection-val128, sealed-final512; 50% ops2–4, 30% ops5–8, 20% ops9–15. Pinned medium/hard GSM-Infinite official sources; split by number-masked core family; excludes current SFT3000, previous evaluations, and all original MATH train/test. It explicitly does not prove absence of semantic overlap.

Train answer frequency: 4=175/1024 (17.09%), 3=113, 2=113, 6=89, 8=69, 1=61. The first nominal ops2 row queries a total directly specified as4 while surrounding dependencies are distractors. Nominal opcount therefore does not establish useful reasoning depth or breadth. Keep these frozen inputs unchanged for current arms.

Distributed-smoke validation0000 has only8 answers,3correct,8format-valid,8parallel-valid. Sampler exact FP32 HF temperature1/top_p1, selection allowed; not frozen128 evaluation. This is insufficient evidence for a bucket difficulty claim.

## Already available math-like sources

Pinned `open-r1/Big-Math-RL-Verified-Processed@c79efbb6d3b75e3a2bcc27a5c569119918132345` cached. Prepared source subsets: `exps/rl-dataset-screen-20261007/bigmath_orca.parquet` (256 selected from79556 source rows) and `bigmath_cn_k12.parquet` (256 from48974). Existing preparation excludes figures/proofs and compares all12500 original MATH rows plus5910 historical SFT rows using normalized exact and number-masked word-trigram Jaccard>=0.65. Semantic paraphrases and AIME were not conclusively excluded. Refilter against current SFT and all reserved AIME years before reuse.

Historical screening (`selection-analysis.json`) had256 prompts x8 samples: GSM accuracy18.55%, mixed groups71.88%,15 distinct golds, best constant23.83%; Orca31.84%, mixed58.59%,153 golds, best constant4.69%; CN K12 21.04%, mixed48.05%,185golds, best constant6.25%; DAPO4.44%, mixed24.22%. These old checkpoint/runtime numbers are candidate-ranking evidence only, not current 4B transfer claims. DAPO audit shows numerous original-MATH exact overlaps; defer this source.

## Proposed pilot, pending root coordination

1. Lock evaluation-only all original MATH train/test and every reserved AIME year before constructing any source. Reject exact, normalized, number-masked family, semantic paraphrase, translation, and solution-equivalent near matches; preserve row provenance and rejection ledger. Split source families before difficulty estimation.
2. Read-only candidate assembly: 64 fresh family-disjoint Orca,64 CN K12,64 higher-school/competition candidates from independently reviewed provenance, plus64 GSM controls across three existing difficulty buckets. Use geometry only when text is self-contained; exclude proofs/ambiguous references.
3. On the actual chosen 4B starting SFT checkpoint, use same RL rollout runtime and8samples/problem. Record k-of-8, all-zero/all-one fractions, reward std, correctness by source/topic, format errors, actual generation forwards, and answer-prior controls. Select useful mixed groups (1<=k<=7); all-zero hard cases need scaffolding/SFT first, all-eight easy cases need less sampling. Never assume operations or publisher solve-rate transfer.
4. Start a new, explicit curriculum revision, not edits to running arms. Initial recommendation after successful pilot: 50% math-like medium mixed groups,30% harder math-like mixed groups,20% GSM/format anchors. Adjust by measured k-of-8/topic coverage, not nominal levels. This ratio is a proposal, not established optimum.
5. Checkpoint selection is lexicographic: accuracy first, then minimize measured actual generation forwards only among candidates satisfying the matched unseen-SFT hard quality floor. Width/round bonuses cannot compensate for below-floor accuracy. Retain correct and incorrect costs separately to prevent early wrong answers appearing efficient. Use independent selection validation; open sealed final once after policy choice. Full MATH/AIME serve final reporting and not curriculum/reward tuning.

No new launch requested or performed.
