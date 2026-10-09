# Changes to the authors' code

Base: upstream commit `f1c6389`.

## SFT speedups (`verl/verl/trainer/fsdp_parallel_sft_trainer.py`, `verl/verl/utils/dataset/parallel_thinking_sft_dataset.py`)

1. Padding is cropped to the longest sample instead of `max_length=4096`.
   The dataset still builds the same masks and position ids; it also returns the real `length`.
   `collate_cropped` crops each batch on CPU, `crop_padding` crops each micro batch before the forward.
   Cropping on CPU is needed on 1 GPU: a batch of 128 uncropped 4096x4096 float masks is ~10 GB of host memory per batch.
2. Micro batch 4 instead of 1 (`scripts/sft_qwen3_0.6b.sh`); micro batch 8 ran out of GPU memory on the longest batches (fp32 cross entropy over the 151k vocabulary). The loss is the token mean within each sample,
   then the mean over samples, which is exactly the objective of the authors' micro batch 1.
   `data.balance_dp_token` is no longer used.
3. Gradient checkpointing is off (`scripts/sft_qwen3_0.6b.sh`).
4. DataLoader `num_workers=2` instead of 8. With 8 workers the prefetched batches of float masks (up to ~3 GB per 128-sample batch)
   plus their pinned copies hit the pod memory limit of 122 GiB at the first epoch boundary (process killed with SIGKILL).
   Two workers are enough: a sample takes 0.04 s to build, a 128-sample batch ~5 s per worker, a training step ~6 s.

Verification:
- CPU, tiny random Qwen3, authors' dataset class, 4 samples: same loss, max gradient difference 1.2e-7.
  A token mean over the micro batch (verl default) gives a gradient difference of 1.7e-2, so the per-sample mean is required.
- GPU: `scripts/check_sft_parity.sh` runs 10 steps of the authors' code and of ours on the same data order and init.

## Special tokens (`scripts/add_special_tokens.py`)

The authors add the six tags with `add_special_tokens` + `resize_token_embeddings(151675)`, which gives the tags
the existing unused embedding rows 151669-151674. In Qwen3-4B-Base those rows differ; in Qwen3-0.6B-Base all of them
are the same vector (norm 0.35). With tied embeddings the 0.6B model then cannot tell the tags apart: after SFT the tags
were still nearly identical (cosine 0.999) and only 0.2% of parallel answers had a valid tag structure
(`results/eval_sft_identical_tags`). We initialise each tag with the mean embedding of the pieces of its text
(`<`, `Path`, `>`). The authors' 4B rows match neither this init (cosine 0.40-0.56) nor the unused rows, so their exact
init is unknown; what matters is that their tags are distinct.

## Pod

- StatefulSet `vcharkin-shared-vm`: `/dev/shm` is an in-memory `emptyDir` of 32Gi (was 64M), needed by the DataLoader workers.

## exp/13-instruct4b-control: SFT of the hybrid Qwen3-4B (instruct) in its native template

Verified on the pod CPU by `scripts/instruct4b/test_sft_instruct.py` (tokenizer of `/work/assets/models/Qwen3-4B`, tiny random Qwen3 for gradients).

1. `fsdp_parallel_sft_trainer.py`: the loss is divided by the number of micro batches before `backward()` (`loss_scale`), not after.
   Before, the gradient was `n_micro` times the batch mean, so clipping at 1.0 acted on a scaled norm. The objective
   (token mean within a sample, mean over samples) is unchanged. `train/grad_norm` is logged. A mutation check
   (scale removed) makes the test fail with a 2x gradient.
2. `parallel_thinking_sft_dataset.py`: `data.enable_thinking` (default `None` = old behaviour) is passed to the chat template.
   With `False` the hybrid Qwen3 template renders the native non-thinking prompt (`<think>\n\n</think>\n\n`);
   prompt + response + `<|im_end|>` is then exactly the template's render of the conversation.
3. `parallel_thinking_loop_v3.py`: `PARALLEL_ROLLOUT_ENABLE_THINKING=true|false` (unset = old behaviour) is passed to the
   chat template of the parallel rollout and printed once (`Parallel rollout chat template kwargs: ...`), so the rollout
   prompt has the same tokens as the SFT prompt. An env var because `scripts/bench/eval_rollout.sh` takes no overrides.
4. `scripts/instruct4b/prepare_model.py` (new; `scripts/add_special_tokens.py` is unchanged): the six tags get ids
   151669-151674, which already lie inside the 151936 embedding rows of Qwen3-4B (unused, identical rows, cosine 1.0).
   No resize, so `vocab_size` stays 151936; only these six rows of the tied embedding / lm_head change (mean of the
   pieces, as in `add_special_tokens.py`); saved in bf16 like the source, with the native chat template. Checked on the
   pod CPU: changed rows are exactly the six, no other parameter changes, same generation config. As in the authors'
   checkpoint, `additional_special_tokens` lists only the six tags; the Qwen control tokens stay special in
   `added_tokens_decoder` and are still skipped by `decode(skip_special_tokens=True)`.
5. `parallel_thinking_sft_dataset.py`: the structure mask is built on the response only; the prompt stays fully causal.
   Before, the mask was built on prompt + response, so a user instruction with two literal `<Path>` blocks hid them
   from each other (the authors' prompt has one pair and gets the same mask as before: checked by a test).
   Positions were already response-only.
6. `fsdp_parallel_sft_trainer.py`, only when `trainer.total_training_steps` is set (unset = old behaviour):
   the lr schedule spans these steps (before, its length was steps per epoch x epochs, so arms of different size had
   different lr curves for the same number of updates), and no validation or checkpoint at the end of an earlier epoch
   (each is a 16 GB fp32 checkpoint). `train/target_tokens` (target tokens of the global batch) is logged every step.
7. `scripts/bench/score.py` (our script, not the authors' code): optional 4th argument writes one outcome row per answer for paired
   comparisons; with `SCORE_IFEVAL_SEED=<int>` the IFEval checker's random fallbacks are seeded per prompt key (unset = old behaviour,
   same summary). Used by `scripts/instruct4b_eval/` (run_eval.sh always sets 0); verified by CPU tests in
   `results/13-instruct4b-control/checks/eval-*.log`, details in `results/13-instruct4b-control/evaluation.md`. Training code unchanged.

## exp/21-qwen3-0.6b-multiverse

1. `scripts/exp21/prepare_model.py` adds the ten Multiverse tags to the post-trained Qwen3-0.6B in unused tied-embedding rows,
   with a distinct vector for each tag. The vocabulary tensor shape stays 151936. Pod B preparation checked that only those ten
   rows changed, each tag is one token, their maximum pairwise cosine is 0.48 and the model remains bf16.
2. `verl/utils/dataset/multiverse_structure.py` supplies sibling-path attention masking and positions from exp/19;
   `parallel_thinking_sft_dataset.py` selects it with `data.structure=multiverse` and reads per-row thinking mode;
   `fsdp_parallel_sft_trainer.py` applies `optim.tag_lr_mult` to the new tied rows (exp/20). Replay rows without blocks retain
   ordinary causal masking. These changes are needed to train the requested format without a path reading a sibling.
3. `scripts/exp21/` builds the leak-filtered pool, M1 and M2 data, training parquets and evaluations. M2 keeps Qwen's text
   verbatim except whitespace and inserted tags/outline/conclusion: any proposed edit is rejected, and a content comparison
   checks recovery of the original answer. Both methods require grammar, independence heuristics, answer, number and length checks.
4. The experiment uses one GPU per pod and one queue per pod. Short training responses use at most 2048 tokens and full
   prompt plus response at most 4096; the SFT dense Multiverse mask scales quadratically with this limit. The experiment
   report records data quality gates, training parameters, benchmark results and paired intervals.
5. `scripts/bench/score.py` reports model-token length and sequential forward-pass counts for every response, including
   responses without a parallel block (whose forward-pass count is their full length). Before this correction, such rows
   had an empty forward-pass field. Truncation and grammar validity remain separate metrics.
6. `scripts/exp21/generate_pool.py` can ask Qwen for independent parts in separate paragraphs during an M2 pilot; Qwen still
   writes every solution word, and the converter must preserve that text exactly. `paired_compare.py` checks the Multiverse
   prompt against the plain prompt and reports paired intervals for response length and forward passes as well as accuracy.
7. `scripts/exp21/prepare_m2_alternates.py` selects other already generated, correct Qwen answers only for problems where M1
   passed and the first M2 plan did not. It keeps a maximum of two alternatives per problem; the same M2 converter and checks
   apply. This can raise the paired yield without changing the candidate problem pool or using evaluation results.
8. `scripts/exp21/add_efficiency.py` derives token length and sequential forward-pass counts from saved evaluation dumps in
   separate run directories. It checks row alignment, preserves the original scores, and counts the paths of each grammatical
   Multiverse block by their longest path. All variants use this same derivation for efficiency comparisons.
9. Forward-pass savings now require the whole response to have valid, numbered Multiverse blocks. The benchmark scorer and
   saved-dump derivation also report the share of attempted blocks that parse and have numbered paths; malformed responses
   get their full token count as sequential work. The legacy `valid_tags` field uses an older grammar and is not used in exp 21.
10. `scripts/exp21/audit_sft_parity.py` checks the completed SFT parquets before GPU training: paired M1/M2 problem IDs,
    identical replay texts and split membership, equal repetitions and prompts, and control answers equal the chosen method
    after removing only the structural tags. A mismatch stops the run before training.
11. `scripts/exp21/sample_review.py` selects the same 30 problem IDs for independent review of M1 and M2, stratified across
    GSM8K and MATH integer, fraction and expression answers. The seed and sampled JSONL are saved with the audit.
12. Exp 21 publishes the 187 paired M1/M2 rows, shared replay, exact training parquets, dataset cards and manual audit in
    `results/21-qwen3-0.6b-multiverse/`. Both SFT runs use 64 updates and the same recipe. `score.py` now starts the
    forward-pass count from generated token count, so the final EOS step is included even for an answer without blocks.
    Runs scored before this change are corrected from saved dumps by `add_efficiency.py` into separate analysis directories.
13. `scripts/exp21/generate_multiverse.py` adds an inference diagnostic that generates every numbered sibling path from the
    same Goal prefix, then joins the paths and continues. This matches the training mask's independence constraint at the
    path stage. Plain sequential generation is kept as a separate diagnostic: it gives the token after the first path a
    sibling-path context absent in SFT and often jumps straight to the conclusion. `run_eval.sh` names the new protocol
    `multiverse-branch`; its prompts, seed, budget and generator are recorded in run metadata. The joined conclusion still
    uses ordinary vLLM positions, so this is an approximation to the full custom-position Multiverse rollout.
14. The tag-free control now keeps the same Multiverse training prompt as its tagged source and removes only the structural
    tags from the answer. `audit_sft_parity.py` checks prompt equality in addition to exact source text after tag removal,
    replay, split and repetition equality. This isolates the tag change within the available SFT comparison.
15. `scripts/exp21/collect_eval.py` records each source within each benchmark's accuracy, grammar, response length, sequential forward passes,
    truncation, evaluation mode and code commit in one CSV from the corrected run directories. It reads scored rows to add
    grammatical-response rate over all responses, distinct from validity among tag users or attempted blocks. A partial run
    over baseline directories produced 28 rows; the report uses the final CSV for its tables.
16. `scripts/exp21/audit_branch_rollout.py` reports how often the independent-path decoder joined a block and whether the
    model closed its paths. It explicitly records the Path delimiters and numbers supplied by the decoder, so the resulting
    grammar rate cannot be mistaken for unconstrained left-to-right tag generation.
17. The first dev Multiverse parquets were created before `make_mv_prompts.py` narrowed the first instruction from
    "separate cases, separate quantities, or independent checks" to "separate cases or separate quantities" for SFT.
    Every original dev variant used the same earlier prompt, so comparisons between variants remain paired, but it differs
    slightly from training. `paired_compare.py` accepts both exact prompt paragraphs and still checks all problem texts.
    A separate matched-prompt dev evaluation uses newly generated parquets without replacing the earlier artifacts.
18. A second independent M2 review found seven substantive reasoning errors in 30 responses despite correct final answers.
    `audit_reasoning.py` audits every candidate's intermediate text through the VK AI Proxy; `select_m2_audited.py` excludes
    errors, incomplete proofs and uncertain cases. The audited M2 set keeps 187 rows and the original source/answer-type
    distribution, with 147 task IDs shared with M1 and 40 replacements. `verify_audited_m2.py` rechecks grammar, answer,
    lengths and original-Qwen text on the pod; only two percentage suffixes require explicit semantic normalization.
    A fresh, disjoint manual sample of 20 plus independent 40 passes the quality gate. The old M2 model and data remain
    as preliminary provenance; a new M2 SFT uses the audited set with identical row counts and kind counts to M1.
19. The auditor now persists the exact question, answer and response in every verdict and checks them before resuming.
    Audited selection verifies each task against the leak-checked pool and each verdict against its candidate; it recovers
    original Qwen sample IDs for all 187 rows. `verify_audited_m2.py` checks every selected row verbatim against its
    original generation, including two correct percentage answers normalized under an explicit rule. The 40+20 review
    sample has a saved seed, exclusions, quotas and IDs. Nine failed audit calls have no recorded price, so the known
    proxy cost is a lower bound. The IFEval completion jobs use the benchmark's frozen-suite location after correcting
    an invalid `suite=ifeval` invocation in the first control queue script.
20. `compare_final.py` also emits paired confidence intervals for the exact SFT-prompt Multiverse sensitivity runs.
    This leaves the earlier common dev prompt and its paired comparisons intact. `collect_eval.py` writes LF CSV lines,
    so the consolidated metrics table remains reviewable in Git. The experiment report distinguishes full-response
    grammar from valid attempted blocks, branch decoding from autonomous sequential generation, and `accuracy_robust`
    per response from pass@k on repeated frozen tasks. The previously unopened APO, ARC, MMLU-Pro and LIMO sets are
    evaluated only for the dev-selected M1 model; IFEval is a separate selection metric for all variants.
21. M1 completed the held-out APO, ARC, MMLU-Pro and LIMO evaluations in both thinking modes. The report includes
    per-answer robust accuracy, output tokens, sequential forwards and truncation for every source, with the actual
    repeated-sample counts. Both frozen jobs and efficiency postprocessing exited successfully. The corrected source
    summaries add 14 rows to `metrics.csv` (142 total). After transferring the analysis archive, pod B was scaled to
    zero alongside A; its 200Gi PVC remains Bound.
22. A follow-up tests why M1 cannot emit full blocks with ordinary sequential decoding. `diagnose_mask_gap.py` and
    `check_masked_decode_state.py` check a one-block incremental mask and positions against the exact SFT structure.
    `diagnose_tag_transition.py` compares teacher-forced token probabilities under the training and causal masks;
    `verify_cached_mask.py` checks cached logits against a full structured pass. `generate_masked_multiverse.py`
    generates flat blocks autonomously with the training mask and positions, inserting no tags or path numbers;
    `compare_masked_pilot.py` pairs its dev rows with previously saved sequential and branch results. No authors'
    code changed. The scripts passed syntax checks, mask-position toy checks and a cached-logit check; pilot outcomes
    and limitations are recorded in `results/21-qwen3-0.6b-multiverse/FOLLOWUP_AUTONOMY.md`.
23. A thinking-specific scorer separates Multiverse tags inside `<think>` from tags after `</think>`.
    Matched 20-problem GSM8K dev pilots cover C0, M1, audited M2, the tag-free control, and a new M1-thmix SFT.
    `make_thinking_m1.py` moves one of each M1 problem's three structured copies into `<think>` without changing
    solution text; `audit_thinking_sft.py` checks every pair, answer, grammar, split, and length. M1-thmix was trained
    for the same 64 steps and audited with sequential and training-mask decoding. The latter restores internal block
    grammar but not answer quality in this pilot. `score_thinking_blocks.py` and `compare_thinking_blocks.py` save
    per-response outcomes and paired intervals. The new dataset card, training log, raw responses, and limitations
    are in `results/21-qwen3-0.6b-multiverse/`.
