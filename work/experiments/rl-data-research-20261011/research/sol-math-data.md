# RL math data recommendation — 2026-10-11

Scope: research only for Qwen3-4B-Base after parallel SFT. No jobs, GPU allocations, remote writes, or frozen-run changes. Candidate counts below are upstream counts, not a clean training inventory. No dataset has been certified clean in this audit.

## Recommended order

1. **NuminaMath-1.5, `source == cn_k12`**, restrictive answer/quality filters, as the first controlled curriculum. Start with a small screened sample rather than ingesting everything.
2. **Big-Math-RL-Verified, `source == cn_k12`**, as a verified-answer alternative to the same family. Deduplicate across Numina and Big-Math; they are not independent sources. Expand to `Orca-Math` only after parent-lineage checks.
3. **DeepMath-103K**, harder expansion only after complete benchmark screening and explicit handling of missing source provenance. Do not infer that difficulty separates SimpleRL-derived rows from new rows.

These are candidate whitelists, not permission to skip contamination screening. School-level problems can reproduce competition tasks; source labels alone prove neither originality nor absence of leakage.

## Primary-source facts and release limitations

### Numina

[Official card](https://huggingface.co/datasets/AI-MO/NuminaMath-1.5): Apache-2.0, 896,215 rows. `cn_k12` has 268,819 rows, including 149,010 word problems before filtering. Schema includes `problem`, `solution`, `answer`, source and validity/type metadata. Use `problem` for prompt and `answer` for rule reward. Require `question_type == math-word-problem`, `problem_is_valid == Yes`, `solution_is_valid == Yes`, `synthetic == false`, concrete nonempty answer; exclude `proof`, `notfound`, MCQ, missing diagrams, multipart/ambiguous answers. Card describes online PDFs/forums and generic source classes; no per-item original source ID appears in released schema. Exclude `amc_aime`, `aops_forum`, `olympiads`, `olympiads_ref`, `metamath`, `synthetic_math` initially. Manually curated `cn_contest`, `number_theory`, `inequalities` are possible later expansions, not automatic whitelists.

### Big-Math

[Official card](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified): Apache-2.0, 251,122 verified problems. `cn_k12` 63,609; `Orca-Math` 83,215. Fields `problem`, `answer`, `source`, `domain`, `llama8b_solve_rate`. The latter uses 64 Llama-3.1-8B rollouts and cannot estimate 4B difficulty directly. Upstream benchmark decontamination targets MATH-500 and Omni-MATH; it does not establish exclusion of full MATH. Exclude `MATH` (9,257), HARP, Omni-MATH, `amc_aime`, `aops_forum`, olympiads, and the undifferentiated reformulated pool initially. Do not include UNVERIFIED. Source tags permit coarse filtering but do not supply original contest IDs in the documented schema. [Paper](https://arxiv.org/abs/2502.17387).

### DeepMath

[Official card](https://huggingface.co/datasets/zwhe99/DeepMath-103K): MIT; `question`, `final_answer`, `difficulty`, `topic`, three `r1_solution_*` fields. Use question/final_answer, never teacher traces as rollout prompts. [Paper](https://arxiv.org/html/2504.11456v2) describes 95K curated hard tasks plus 8K SimpleRL tasks, primarily levels 5–9, using Math StackExchange subsets of MMIQC/WebInstructSub and Numina. It reports semantic screening against MATH/AIME and other benchmarks, but exact planned years/splits must be verified independently. Released schema has no original source URL/ID or SimpleRL-origin label: neither full lineage whitelist nor reliable SimpleRL removal is available from those fields. Difficulty 5–6 is a *pilot sampling heuristic*, not a clean-origin guarantee. The May 2025 card records repair of 48 answer-hint questions; pin a current immutable revision, not a stale cached release.

### OpenMath and DAPO: reserve, not initial training

[OpenMathReasoning official card](https://huggingface.co/datasets/nvidia/OpenMathReasoning): CC-BY-4.0. AoPS-derived problems plus `MATH_training_set`; many solutions per problem. For any later use require `problem_type == has_answer_extracted`, use `expected_answer`, deduplicate `problem`, exclude `MATH_training_set`, and screen AoPS rows individually against all protected contests. `pass_rate_72b_tir` is 72B tool-use difficulty, not 4B difficulty. Converted proofs and majority-voted answers are weaker ground truth; exclude them initially. Forum-category provenance is not an original contest ID.

[DAPO official release](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k): Apache-2.0; `prompt`, `reward_model.ground_truth`, `extra_info.index` UUID, `data_source == math_dapo`. `ability == MATH` denotes task domain, not proof of Hendrycks source membership. Live viewer shows 1,791,700 rows despite the 17k title: audit actual unique prompt count and repetitions before any sizing. README is empty and UUIDs do not restore original problem provenance. Rewritten competition prompts require semantic/number-masked screening. Do not assume integer ground truth semantics without auditing the actual transformation and verifier.

## Provenance manifest before download-to-training conversion

Resolve each HF dataset to immutable commit SHA; record dataset ID, revision, split, shard path and hash, row index, raw problem SHA256, source label, upstream answer, licence metadata and card revision. Row index is stable only within pinned shards. If no upstream original ID exists, record `original_source_id: null` rather than manufacturing one. Assign local `sample_id = sha256(dataset_id + revision + shard + row_index + raw_problem_hash)`. Store the exact normalization version and every exclusion/review decision. Published collection licence is not per-problem lineage evidence.

## Mandatory decontamination contract

Protect **all original MATH train and test** (12,500 total), not only MATH-500; register original IDs/splits. MATH remains evaluation-only under this task. Protect AIME I/II for every planned evaluation year; safest provisional quarantine is all available years, including 2024–2026, until final eval manifest is frozen. Protect both English statements and available translations/reformulations, original answer, contest/year/problem IDs. Pin raw benchmark artefacts with hashes. Do not use benchmark accuracy to choose curriculum rows.

Pipeline, applied across candidate datasets and against protected corpora:

1. Exact raw hashes after extracting problem from wrappers; reject direct matches.
2. Conservative normalized hashes: Unicode NFKC, whitespace, equivalent LaTeX delimiters/macros, formatting-only changes, instruction wrappers and explicit contest headers. Preserve numbers, variable structure and mathematical conditions.
3. Number-masked and variable-normalized structure plus token/shingle retrieval: catches parameter changes, translated formatting and lightly rewritten problem families. Matches enter quarantine; number masking alone has false positives and is not an automatic equivalence proof.
4. Semantic retrieval on text and mathematical structure, nearest-neighbor review across languages; compare constraints, target quantity and solution dependency, not just topic. Human review of high-risk borderline pairs; uncertain rows remain excluded. Embedding threshold alone cannot certify cleanliness.
5. Remove source descendants/reformulations when parent is known protected. Cluster aliases before splitting train/pilot/heldout so no family crosses splits. Audit a random retained sample and deliberately seeded known rephrasings to measure detection recall; report residual unknowns.

Deliver immutable `accepted.jsonl`, `quarantine.jsonl`, `excluded.jsonl`, per-stage counts, benchmark manifest hashes, nearest protected IDs/scores and review reasons. No claim of zero leakage follows merely from passing this finite detector. Existing SFT also needs this audit: clean new RL data cannot undo SFT contamination.

## 4B difficulty and useful-gradient pilot

Difficulty claims for the target checkpoint are currently **unknown**. Expected ordering (hypothesis): filtered school tasks easier; contest tasks harder; DeepMath hard tail risks all-zero reward. Avoid selecting simply the largest or hardest pool.

Proposed pilot after data gates: 96 unique tasks, 4 independently sampled responses each, exact frozen SFT checkpoint/prompt/parser/sampling settings. Stratify 48 school tasks and 48 harder vetted tasks (DeepMath only if its gates pass; otherwise manually reviewed Numina contest rows). This is 384 trajectories, **not 384 generation forwards**: controller rounds, branches, token steps, padding and verifier retries must be measured separately. No pilot launched here.

Report k-of-4 histogram, accuracy numerator/denominator, mixed fraction `count(1<=k<=3)/N`, parser/unknown rate, truncation rate, sampled tokens and actual model generation forwards. Aim approximately half groups mixed; theoretical independent Bernoulli mixed probability is `1-p^4-(1-p)^4`, so signal disappears near p=0/1. Use this to select a difficulty band, not to promise an achieved mixture. Resample future screening tasks rather than replaying the same groups indefinitely; account for screening cost. Keep independent heldout evaluation and a paired SFT baseline at matched actual forward budgets. Acceptance requires accuracy no worse than unseen SFT within the agreed statistical criterion and a demonstrated accuracy/forward improvement; teacher solution quality or source-card verification is insufficient.
