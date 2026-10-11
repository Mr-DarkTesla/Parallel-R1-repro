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
