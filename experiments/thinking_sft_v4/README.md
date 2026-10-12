# thinking_sft_v4: graph-masked SFT of Qwen3-4B (parallel thinking)

Full-parameter SFT of **Qwen/Qwen3-4B** (post-trained, thinking mode, revision
`1cfa9a7208912126459214e8b04321603b3df60c`, tied embeddings, same vocabulary as Qwen3-0.6B) on **one H100 NVL
(94 GB)** with sequences up to **16384 tokens**, prompt included. Qwen3-0.6B still works with
`--model Qwen/Qwen3-0.6B` (its pinned revision is filled in automatically).

| file | role |
| --- | --- |
| `common.py` | contract loaded by path (sha256-checked), pinned model ids/revisions |
| `tags.py` | adds the eight contract tags (151669..151676 on the Qwen3 vocabulary) and initializes their rows |
| `sft_data.py` | row schema, validator, tokenization, graph positions, the additive 4D mask (`collate`) |
| `sft_train.py` | trainer: chunked LM loss, gradient checkpointing, `--optim`, `--memory-report` |
| `select_records.py` | keep rules, dedup, caps, grouped train/val split, stats JSON |
| `fast_repair.py`, `codex_rules.py` | repair pass for the 5k pool (plan / run on one GPU / assemble / export); Codex's generation rules copied verbatim |
| `exactness.py`, `vm_selftest.py` | independent references for the graph forward; GPU self-test |
| `graph_sampler.py`, `eval_graph.py`, `selftest_sampler_vm.py` | exact graph sampler and evaluation |

Semantics are unchanged from the 0.6B version: parallel rows get the contract graph positions and a mask in which
a branch never sees its siblings; loss only on segments with `loss=true`. CPU tests:
`python -m pytest experiments/thinking_sft_v4/tests -q`.

## Memory at 16k tokens (adamw, bf16 autocast, gradient checkpointing)

4B = 4.02e9 parameters (36 layers, hidden 2560, MLP 9728, 32 q / 8 kv heads of 128, vocab rows 151936).
The H100 NVL shows about 93.6 GiB to torch.

| item | GiB |
| --- | --- |
| fp32 weights | 15.0 |
| fp32 grads (exist from the first backward of a step until `zero_grad`) | 15.0 |
| fp32 AdamW `exp_avg` + `exp_avg_sq` (`--optim adamw8bit`: 7.5) | 30.0 |
| **static** | **60.0** |
| checkpointed fp32 layer inputs, 36 x T x 2560 x 4 B | 5.6 |
| additive mask, bf16 T x T, plus the copy `_unmask_unattended` makes on CUDA | 1.0 |
| one decoder layer recomputed in backward (MLP 4 x T x 9728 bf16, q/k/v, norms) + its grads | 4-5 |
| LM-loss chunk of 2048 rows (bf16 + fp32 logits, log-softmax, its grad, bf16 lm_head cast) | 4-5, not at the same time as a layer |
| **expected peak** (second micro-batch of a step: grads already allocated) | **~70-75** |

What makes this fit:
- **Gradient checkpointing** (`--grad-ckpt`, on by default when the longest training row exceeds
  `--grad-ckpt-min-len` 2048). Without it a 16k row stores about 2 GiB per layer (more than 70 GiB).
- **Chunked LM loss** (`token_losses`): the [T, vocab] logits (16k x 151936 fp32 = 10 GB, as much again for the
  softmax grad) are never materialized. The decoder runs to hidden states, only positions whose target token is in
  loss are gathered, and lm_head + fp32 cross entropy run on `--loss-chunk` (2048) rows at a time, each chunk
  checkpointed. The loss and gradients equal the full-logits computation (`tests/test_4b.py`).
- The **mask is built in the compute dtype** (bf16 under autocast), with only one (L, L) bool alive at a time, and T is
  rounded up to 16 on CUDA, so SDPA's memory-efficient kernel gets an aligned mask and makes no per-layer padded copy.
- **`--sdpa-backend efficient`** (the default on CUDA) allows only the memory-efficient SDPA kernel, which takes an
  additive mask in O(T) memory. If that kernel cannot run a shape you get an error, not a silent fallback to the math
  kernel, which would store 32 x T x T scores (17 GB per layer at 16k). `--attn eager` has the same cost and is
  for tests only.
- **autocast with `cache_enabled=False`** under checkpointing. The cast cache would otherwise keep a bf16 copy of every
  weight (7.5 GiB) for the whole forward.
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` is set by the trainer unless you already set it.
- `--optim adamw8bit` (bitsandbytes, only if installed; it is not a dependency) saves 22.5 GiB if the report shows a
  problem.

Rows longer than `--max-len` (default 16384) are dropped and counted as `too_long`. They are never truncated.

## Data selection

The real generator file is `all.raw.jsonl`, 1,536 rows: exec/math/gsm/countdown, 384 of each. The default rules are
`model_finished`, `correct`, `not over_budget`, every `branch_checks[].ok`, and `plan_status != gold_in_plan`. Then
come the trainer validator and a split grouped by task id or prompt. The dry run (`selection-dryrun.json`) keeps
1003 rows: 656 parallel and 347 sequential, generator n_tokens mean 4.8k, max 15.2k. Each relaxing flag is listed in
`python select_records.py -h`.

```bash
cd ~/Parallel-R1-repro/experiments/thinking_sft_v4
python select_records.py /path/to/thinking-sft-4b/all.raw.jsonl [repaired.jsonl] \
    --out-dir ~/parallel-r1/data/sft_v4_4b --val-frac 0.05 \
    --tokenizer Qwen/Qwen3-4B --max-len 16384     # on the VM: trainer token lengths + too_long
```

## Repair pass for the 5k pool (`fast_repair.py`)

Input: `pool-20261012/all.raw.jsonl` (5,000 rows, sha256 `5b48bda7...`) and Codex's audit `details.jsonl`. Triage
(reproduces the agreed counts; `plan` checks them): seq_clean 1,199 and par_clean 1,924 kept as they are;
exec_summary_resolves 605 and GSM/MATH par_clean rows whose Summary is longer than 0.5x the longest branch (614)
get a new merger; branch_truncated_only 416 get their truncated branches regenerated and then a new merger;
wrong_final 541, plan_or_branch_solves_whole 122, branch_wrong_other 149, unfinished_final_or_mixed 35 and
seq_unfinished 9 are dropped. Details (prompts, acceptance rules, budgets, seeds) are in the module docstring.

- Merger: a non-thinking Summary call (n=4, <=1024 tokens) that sees the plan items and the branch Result lines only
  (exec: no production inputs; GSM/MATH/Countdown: the question plus "these Results are verified, combine them"),
  then a short non-thinking answer call per surviving summary. Accepted: both finished, final correct by Codex's
  scorer, summary <= 0.5x the longest branch, exec summary and answer each repeat <= 1 input product, no tags,
  <= 16,384 tokens, trainer validator. Shortest accepted pair wins; none -> the raw row is exported with
  `provenance.repair_failed=true`, which `select_records.py` drops unless `--keep-repair-failed`.
- Branch: the raw run's own request (from its `wave-*/raw_branches.jsonl`; the records do not store the planner's
  mini-problems), thinking mode, n=2, budget = 16,384 - 2,048 summary reserve - the rest of the record, Codex's
  `check_branch`. Without the raw run's files these records are skipped and counted.
- Only the replaced texts change; prefix, plan and kept branches stay byte-identical. Provenance flags are
  recomputed (`model_finished`, `correct`, `grade`, `branch_checks`, `n_tokens`) and `provenance.repair` records kind,
  nodes, every sample's verdict, the accepted index, prompt hashes, seeds and lengths.
- Estimate (`fast-repair-plan.json`): merger-only 1,214 jobs, 1,214 summary + <=4,856 answer requests, ~5 min on an
  H100 NVL; with the branch requests 413 truncated records more (869 branch requests at n=2, ~7.5M expected
  generated tokens), ~30 min expected, <50 min upper bound (A100 80GB about 1.7x).

## VM commands: repair, select, train (one H100 NVL or A100 80GB)

```bash
# 0. environment: the venv of experiments/qwen06/bootstrap_vm.sh (vllm 0.8.5.post1, transformers 4.51.3, math-verify)
source ~/parallel-r1/.venv/bin/activate
cd ~/parallel-r1/repo && git fetch origin && git checkout claude/project-thread-cc9a3o && git pull --ff-only
cd experiments/thinking_sft_v4
POOL=~/parallel-r1/data/pool-20261012          # all.raw.jsonl + details.jsonl from the shared folder
RAWRUN=/workspace/thinking-sft-v4-4b/runs/raw-full   # Codex's raw run (wave-*/raw_branches.jsonl), if available
W=~/parallel-r1/data/fast_repair
D=~/parallel-r1/data/sft_v4_4b
mkdir -p $W
sha256sum $POOL/all.raw.jsonl                   # 5b48bda734214f7dfb42886a7ad2f3fa08e6b8f0c477b4a2fd5aad03c9ae222d
python -m pytest tests -q                       # CPU tests (FAST_REPAIR_POOL=$POOL also runs the real-pool checks)

# 1. exact branch requests of the raw run (skip if $RAWRUN is not there; truncated records are then skipped)
python fast_repair.py requests --raw-run-root $RAWRUN --out $W/branch_requests.jsonl

# 2. plan (CPU, seconds): triage, jobs.jsonl, plan.json with counts and the time estimate
python fast_repair.py plan --raw $POOL/all.raw.jsonl --details $POOL/details.jsonl --work-dir $W \
    --branch-requests $W/branch_requests.jsonl          # drop this flag without step 1

# 3. GPU: a smoke run on 8 jobs, inspect, then everything (resumes; results checkpointed to $W/results.jsonl)
python fast_repair.py run --work-dir $W --limit-jobs 8
python fast_repair.py assemble --work-dir $W && cat $W/assemble_stats.json
tmux new -d -s repair "python fast_repair.py run --work-dir $W 2>&1 | tee -a $W/run.log"
#    (A100 80GB: same command; if the streaming engine API misbehaves use --engine chunks)

# 4. assemble + export (CPU)
python fast_repair.py assemble --work-dir $W
python fast_repair.py export --work-dir $W --out $W/repaired.jsonl

# 5. selection: raw first, repaired second (repaired rows replace raw rows by id)
python select_records.py $POOL/all.raw.jsonl $W/repaired.jsonl --out-dir $D --val-frac 0.05 \
    --tokenizer Qwen/Qwen3-4B --max-len 16384

# 6. trainer: self-test, memory report, full run (as in the next section)
python vm_selftest.py --data $D/train.jsonl
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b_mem --memory-report 3
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b \
    --epochs 3 --lr 1e-5 --min-lr-ratio 0.1 --warmup-ratio 0.03 --target-steps-per-epoch 90 \
    --max-len 16384 --save-every-epoch --eval-every 30
```

## VM commands (one H100 NVL)

```bash
cd ~/Parallel-R1-repro/experiments/thinking_sft_v4
D=~/parallel-r1/data/sft_v4_4b

# 1. self-test on the real 4B model: tag ids, chat template, mask semantics, fp32 exactness on the built-in row
#    and on 2 real parallel rows clipped to 3072 tokens, a bf16 autocast + grad-ckpt train step. Must print ALL PASSED.
python vm_selftest.py --data $D/train.jsonl

# 2. memory fit: 3 optimizer steps (two micro-batches each) on the 3 longest training rows; peak GiB per phase.
#    Needs a peak below ~89 GiB (it prints fits / DOES NOT FIT); written to runs/sft_v4_4b_mem/memory_report.json.
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b_mem --memory-report 3

# 3. full run: 3 epochs, lr 1e-5, cosine to 10%, warmup 3%, 60-120 optimizer steps per epoch.
#    --target-steps-per-epoch 90 derives --grad-accum-tokens from the data (~51k tokens for the 959 training rows
#    selected now; with ~5k rows of ~7.2k tokens it gives ~400k, the same as the default 393216).
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b \
    --epochs 3 --lr 1e-5 --min-lr-ratio 0.1 --warmup-ratio 0.03 --target-steps-per-epoch 90 \
    --max-len 16384 --save-every-epoch --eval-every 30

# 4. evaluation of the checkpoint with the exact graph sampler (vLLM for causal stages, HF for graph stages).
#    Smaller HF batches than the 0.6B defaults: the 4B KV cache is 144 KiB per token.
python selftest_sampler_vm.py --model runs/sft_v4_4b/final
python eval_graph.py --model runs/sft_v4_4b/final --tasks ~/parallel-r1/data/think_math500_pilot.parquet \
    --mode both --backend vllm --budget 16384 --gpu-memory-utilization 0.40 --hf-batch-tokens 120000 \
    --out runs/eval_v4_4b/math500_pilot
```

`metrics.jsonl` logs `max_mem_gb` (the peak of each optimizer step) and `tokens_per_s`. The checkpoint goes to
`runs/sft_v4_4b/final` as bf16 safetensors, with the tokenizer (tags added) and `train_manifest.json`.

## Tag warmup (two-stage schedule for the eight new tag rows)

At lr 1e-5 the freshly initialized tag rows (mean of their spelling pieces plus noise) barely move. Stage 1 trains
them alone first; stage 2 is the unchanged full run. One invocation runs both:

```bash
python sft_train.py --data $D/train.jsonl --val $D/val.jsonl --out runs/sft_v4_4b \
    --epochs 3 --lr 1e-5 --min-lr-ratio 0.1 --warmup-ratio 0.03 --target-steps-per-epoch 90 \
    --max-len 16384 --save-every-epoch --eval-every 30 \
    --tag-warmup-steps 60 --tag-lr 1e-3 --freeze-check      # recommended; add --tag-lr-mult 10 to try faster tags
# memory of both stages: --memory-report 3 --tag-warmup-steps 60 (stage 1 is reported under "tag_warmup")
```

- **Stage 1** (`--tag-warmup-steps K`, default 0 = off; recommended 60): K optimizer steps on the first K steps of the
  main shuffled stream (same collate, chunked loss, normalization, `--grad-clip`). Every parameter has
  `requires_grad=False` except the tied embedding matrix, whose gradient is masked in place to the eight tag rows by
  a hook. `RowAdam` (Adam, weight decay 0, fp32 moments only for the [8, 2560] slice) runs at `--tag-lr` (default
  1e-3) with a linear warmup over 10% of K, then constant. Logged as `stage=tag_warmup`, `tag_step` 1..K; the main
  run's steps, warmup and cosine schedule are exactly as without it. `--freeze-check` asserts afterwards (on-device
  checksums) that every other row and parameter is bit-identical and the tag rows changed.
- **Stage 2**: the full run, fresh optimizer. `--tag-lr-mult M` (default 1 = off; 10 is the option to try) gives the
  tag rows M x the current main lr. Scaling their gradient would do nothing under Adam, so their gradient rows are
  zeroed before the main AdamW step, the rows are restored after it (no main weight decay or 8-bit noise reaches
  them) and a separate `RowAdam` steps them at M x lr. Other parameters get the ordinary AdamW update.
- **Logs**: every train record has `tag_row_norm` (mean L2 norm of the 8 rows; the manifest has `base_row_norm` of
  ordinary rows for scale), `tag_row_delta` (mean distance from the initialized rows) and `loss_tag` /
  `val_loss_tag` (CE on targets `<Parallel>`, count digit, `</Plan>`, `</Path>`, `</Summary>`, from the chunked loss).
  `train_manifest.json` (also in each checkpoint) has `tag_schedule` with both stages' settings and stage-1 results.
- **Stage-1 memory on 4B** (static): fp32 weights 15.0 GiB + one gradient, the embedding matrix's 1.45 GiB (no
  other parameter requires grad) + 160 KiB of Adam moments = **16.4 GiB**, against 60.0 GiB for the full run (15 GiB
  of grads and 30 GiB of AdamW states disappear). Activations are those of a full step (the backward still runs
  through all 36 layers to reach the embedding, minus the weight gradients), so expect a peak of roughly 27-30 GiB.
  A stage-1 step skips the weight-gradient matmuls, about 3/4 of a full step's time; 60 steps cost about half an
  epoch at 90 steps per epoch.
