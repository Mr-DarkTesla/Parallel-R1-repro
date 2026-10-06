
# **Parallel-R1**
The official repository for "**Parallel-R1: Towards Parallel Thinking via Reinforcement Learning**".

## **Updates**
* **2026-1-26**: 🎉Parallel-R1 was accepted at ICLR2026.
* **2025-10-15**: 🎉Parallel-R1 was accepted at [Neurips 2025 Efficient Reasoning workshop (Spotlight)](https://efficient-reasoning.github.io/).
* **2025-10-05**: Released Training/Evaluation code; Released [Qwen3-4B-Base with adding special tokens](https://huggingface.co/Parallel-R1) with special tokens, along with the [Parallel-Unseen (S2) 200-step](https://huggingface.co/Parallel-R1) checkpoint to support reproduction of mid-training experiments.
* **2025-09-11**: The cold-start dataset, [Parallel-GSM8K](https://huggingface.co/Parallel-R1), is now available on Hugging Face. (Stay tuned for training/evaluation codes)
* **2025-09-10**: We have released our paper, "[Parallel-R1: Towards Parallel Thinking via Reinforcement Learning](https://arxiv.org/abs/2509.07980)".


## **About**
This project introduces **Parallel-R1**, a new **reinforcement learning (RL)** framework designed to teach large language models (LLMs) **parallel thinking** for complex, real-world reasoning tasks. Unlike existing methods that rely on supervised fine-tuning (SFT) over costly, synthetic data, our approach enables models to learn parallel behaviors through RL.

![Parallel-R1框架图](./fig/framework.jpg)

## **Key Contributions**

* **A Novel RL Framework:** We present the first RL framework to learn parallel thinking on general mathematical reasoning tasks.
* **Progressive Curriculum:** The framework uses a progressive curriculum to overcome the "cold-start" problem. It begins with SFT on simpler tasks to teach the model the basic format of parallel thinking before transitioning to RL on harder problems.
* **Simple and Scalable Data Pipeline:** We developed a simple data pipeline that uses prompting on easy math problems (like GSM8K) to generate high-quality "cold-start" data, which is then used to teach the model the parallel thinking format.
* **Strategic Evolution Analysis:** We provide an in-depth analysis showing that the model's strategy evolves over the course of training. It shifts from using parallel paths for early-stage computational exploration to using them for late-stage multi-perspective verification.
* **Mid-Training Exploration Scaffold:** We empirically validate the concept of using parallel thinking as a temporary "mid-training exploration scaffold" to unlock a higher performance ceiling after RL training.

## **Main Results**

| Method | Parallel Ratio (%) | AIME25 Mean@16 | AIME25 Pass@16 | AIME24 Mean@16 | AIME24 Pass@16 | AMC23 Mean@16 | AMC23 Pass@16 | MATH Mean@1 | Avg. |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Qwen3-4B-Base** | 0.0 | 1.3 | 10.2 | 2.9 | 16.5 | 8.1 | 51.2 | 13.9 | 6.6 |
| **SFT + Parallel** | | | | | | | | | |
| Parallel-SFT-Seen | 95.6 | 8.0 | 29.8 | 10.6 | 26.4 | 48.9 | 79.2 | 76.6 | 36.0 |
| Parallel-SFT-Unseen | 95.6 | 5.2 | 20.9 | 8.5 | 26.7 | 41.7 | 80.1 | 71.5 | 31.7 |
| **RL Approach** | | | | | | | | | |
| GRPO (DAPO) | 0.0 | 14.8 | 32.4 | 18.5 | 30.6 | 63.6 | 85.1 | 83.5 | 45.1 |
| + RL on GSM8K | 0.0 | 13.3 | 26.3 | 18.8 | 34.9 | 66.4 | 82.2 | 82.6 | 45.3 |
| Parallel-R1-Seen | 27.3 | 19.2 | 38.9 | 19.4 | 37.1 | 70.5 | 85.0 | 86.7 | 48.9 |
| Parallel-R1-Unseen (S1) | 13.6 | 17.7 | 37.8 | 18.3 | 33.2 | 69.7 | 88.9 | 82.6 | 47.1 |
| Parallel-R1-Unseen (S2) | 63.0 | 19.0 | 42.2 | 16.3 | 31.8 | 67.5 | 91.5 | 84.5 | 46.8 |


## 🧱 Release Overview

| Category | Name | Description | Link |
|-----------|------|--------------|------|
| 🧠 **Models** | Qwen3-4B-Base-Special | Base model with added special tokens `<Parallel>`, `<Path>`, `<Summary>` | [🤗 Hugging Face](https://huggingface.co/Parallel-R1) |
|  | Parallel-R1-Unseen (S2) | 200-step mid-training checkpoint for reproduction of mid-training experiments| [🤗 Hugging Face](https://huggingface.co/Parallel-R1) |
| 📘 **Datasets** | Parallel-GSM8K | Cold-start dataset for teaching parallel format | [🤗 Hugging Face](https://huggingface.co/Parallel-R1) |

##  Training Logs



[🤗 Training Logs](https://api.wandb.ai/links/logical_reasoning/a538trv4)


## 🚀 Usage

### **1️⃣ Environment Setup**

We recommend using **Python 3.10+** and creating a fresh conda environment:

```bash
cd verl
conda create -n parallel-r1 python=3.10 -y
conda activate parallel-r1
USE_MEGATRON=0 bash scripts/install_vllm_sglang_mcore.sh
pip install --no-deps -e .
```

### **2️⃣ Perform SFT**

```bash
cd verl
sh training_scripts/sft_exp.sh
```

For Qwen3-0.6B, all stages have one entry point (run from the repository root
in the active Python environment):

```bash
NPROC_PER_NODE=8 bash scripts/qwen3.sh sft seen
NPROC_PER_NODE=2 bash scripts/qwen3.sh eval verl/checkpoints/Parallel-SFT-Seen-Qwen3-0.6B/final
NPROC_PER_NODE=1 bash scripts/qwen3.sh rl s1 verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B/final
NPROC_PER_NODE=1 bash scripts/qwen3.sh rl s2 verl/checkpoints/Parallel-SFT-Unseen-Qwen3-0.6B/final
```

Arguments after the stage/model are ordinary Hydra overrides. All stages use
`NPROC_PER_NODE`, `PARALLEL_R1_OUTPUT_ROOT` and `PARALLEL_R1_SCRATCH_ROOT`.
The existing SFT/eval launchers remain available. SFT/eval default to 8 GPUs;
the RL profile defaults to 1 A100 80 GB. Select the count explicitly when switching stages.

RL uses `rl_qwen3_06b.yaml`: batch 32, rollout n=8, microbatch 4, LR 1e-6,
300 steps, save/validation every 10 steps, offline W&B and rollout telemetry.
It uses CUDA graphs and trims padding while retaining the parallel attention mask.
Microbatches are grouped by length and the loss keeps the original equal weight per response.
Activation checkpointing is disabled for A100 80 GB. For an 8-GPU run, use
`NPROC_PER_NODE=8` with overrides `ray_init.num_cpus=32 actor_rollout_ref.rollout.agent.num_workers=8`.
Per-token forward counting is opt-in: set `PARALLEL_R1_FORWARD_PROBE=1` and
`actor_rollout_ref.rollout.enforce_eager=true` when profiling.
On vLLM 0.8.5.post1, Qwen3 and rollout TP=1, full decode graphs can be enabled with
`PARALLEL_R1_FULL_DECODE_GRAPH=1 VLLM_ATTENTION_BACKEND=FLASH_ATTN`.
They retain the compiled kernels and exact batch shapes, check each new graph
against the original forward, and use the existing path for prefill.
Set `PARALLEL_R1_GRAPH_CAPTURE_MIN_USES=4` to run the first three occurrences of a
new shape through the original forward before paying the capture cost (default: 1).
Run `PARALLEL_R1_TEST_MODEL=/path/to/qwen3 python tests/test_vllm_decode_graph.py`
with `PYTHONPATH=verl` for the GPU check, including variable batches and sleep/wake.
The published S1/S2 scripts target Unseen-SFT. Use an Unseen checkpoint to reproduce
that setup; the launcher accepts any checkpoint and does not infer its SFT mode.
S1 and S2 start independently from the same SFT. Existing repository Parquets
have identical questions/order (17,917 train, 1,916 validation); only the S2
train reward differs. Validation always uses accuracy. No dataset copying is needed.
Results go to `<output>/rl/<PARALLEL_R1_RL_NAME>` (default name `qwen06-s1-seed1`
or `qwen06-s2-seed1`); set a new name for each independent run. Continue an
existing run by passing `trainer.resume_mode=auto trainer.val_before_train=true`.
RL saves optimizer state; SFT does not. The old `experiments/qwen06/run_rl.sh`
command is a compatibility adapter for the previous environment variables.

For runs using the author's `token-mean` loss, keep
`actor_rollout_ref.actor.sort_microbatches_by_length=false`. Optional
`++actor_rollout_ref.actor.sort_microbatch_groups_by_length=true` reorders whole
original microbatches without changing their loss weights;
`++actor_rollout_ref.actor.sort_logprob_rows_by_length=true` restores log-prob
outputs to their original row order. FSDP1 can defer gradient synchronization with
`++actor_rollout_ref.actor.defer_gradient_sync=true` when parameters stay on GPU;
this uses more gradient memory and changes BF16 accumulation rounding.
`actor_rollout_ref.rollout.max_num_seqs` controls inference concurrency separately
from the training batch. Re-measure full steps after changing it, including
validation/checkpoint time in the completion estimate.

The shared dependency file remains `verl/requirements-qwen3.txt`. It uses
Transformers 4.53.2, Ray 2.48.0 and TensorDict 0.8.3; the earlier RL environment
used 4.51.3/2.43.0/0.6.2. The integrated interface and generation loop have CPU
checks, including padding/gradient equivalence, and an 8-GPU training smoke. RL retains the
upstream structured actor mask/positions and loss on runtime-inserted tags;
its inference/training mismatch is unchanged. Our bounded total response budget
also differs from the original RL branch, so old runs are not protocol-identical.

One-off VM provisioning, queues, plots, reports and smoke experiments remain on
`qwen3-0.6b-rl`; no `exp/*` branch is merged here.

For SFT setup:

```bash
cd verl  # from the repository root
uv venv --python 3.12 ../.venv
source ../.venv/bin/activate
uv pip install -r requirements-qwen3.txt setuptools ninja
uv pip install --no-build-isolation flash-attn==2.7.4.post1
bash training_scripts/sft_qwen3_06b.sh  # Seen is the default
# Optional Unseen comparison:
bash training_scripts/sft_qwen3_06b.sh unseen
```

The same environment runs SFT and evaluation: PyTorch 2.6, vLLM 0.8.5.post1,
and FlashAttention 2.7.4.post1. The environment lives in the project.

The Qwen3-0.6B profile uses Parallel-GSM8K, global batch 128, microbatch 4,
length 3072, LR 1e-5, and five epochs. Seen uses ordinary causal attention;
Unseen isolates response paths. Prompt instructions always retain ordinary
positions and causal attention. The selected profile was checked on 8 A100 80GB;
use Hydra overrides for other GPU memory limits.

The launcher prepares six control tokens once, explicitly initializes their
embeddings, and uses `Qwen3-0.6B-Base-special-v2`. Existing checkpoints from the
old token initialization need retraining. Right padding is trimmed before forward;
tokens, positions and the attention mask are preserved. Gradient checkpointing
is disabled. Microbatch 8 ran out of memory on the longest examples.

Training averages token loss within each response and then across examples,
with accumulation scaling applied before backward. Validation covers every
example once, excluding duplicated sampler padding. Weighted token loss is an
experiment only and is not part of the shared trainer.
Override `NPROC_PER_NODE` for another GPU count and pass Hydra
overrides after the variant. By default, the prepared model, HF cache, and all
five epoch checkpoints are stored under `verl/checkpoints/` in the project.
The epoch weights use BF16 (about 6 GB per variant) and can be scored separately.
A final HF checkpoint is also copied to
`verl/checkpoints/<experiment>/final`. Set `PARALLEL_R1_SCRATCH_ROOT` and
`PARALLEL_R1_OUTPUT_ROOT` to use different storage locations; absolute paths
are recommended. Optimizer
states are not saved. Weight-only checkpoints do not resume optimizer/scheduler
state. Kaggle-specific changes are deferred.

To evaluate an epoch checkpoint in the same environment:

```bash
bash training_scripts/eval_qwen3_06b.sh checkpoints/Parallel-SFT-Seen-Qwen3-0.6B/final
```

The launcher runs validation only through the parallel-generation loop, with
batch 1024 in eager mode (CUDA Graphs disabled). The response budget includes
all paths, injected tags and the summary. On two A100s, measured full eval time
was 6.9 min with this profile versus 12.3 min at batch 256 and 7.8 min with
batch 1024 and CUDA Graphs. One stochastic pass does not establish a quality
advantage for either engine configuration; eager is selected for measured speed.

Use `actor_rollout_ref.rollout.mode=sync` for ordinary autoregressive decoding
and `actor_rollout_ref.rollout.enforce_eager=false` to enable CUDA Graphs.
The parallel vLLM loop does not apply Unseen's custom summary positions/mask;
Unseen train/inference alignment remains an open limitation.
The default benchmark file contains 30 AIME24, 30 AIME25, and 40 AMC23 questions,
each repeated 16 times, plus 316 MATH questions once. Keep `val_kwargs.n=1` for
this file. Metrics include accuracy, observed `pass@N`, parallel ratio, and tag
format validity, using the original answer verifiers. Logs and per-response
JSONL are saved under `PARALLEL_R1_OUTPUT_ROOT/eval` (default: `verl/checkpoints/eval`).
The format sanity metrics are `parallel_format` (control tags are balanced and
properly nested), `format_error` (unmatched or misnested tags), and `no_tags`
(no control tags); their fractions sum to one. The sanity check imposes no
minimum number of paths and does not require a summary. The separate `format`
metric retains the original author checker, which requires at least two paths
and a summary after each parallel block. They check the assembled response, including tags inserted by the
parallel agent, and do not change accuracy or reward. Bootstrap best/worst/majority metrics
are omitted for these auxiliary format flags; accuracy statistics are retained.
Override `data.val_files` for another Parquet dataset and `NPROC_PER_NODE` for
another GPU count.

### **2️⃣ Perform RL**
To train Parallel-R1-Unseen (S1) from scratch 
```bash
cd verl
sh training_scripts/rl_exp_s1.sh
```
To train Parallel-R1-Unseen (S2) from scratch 
```bash
cd verl
sh training_scripts/rl_exp_s2.sh
```

To reproduce results of mid-training experiments
```bash
cd verl
sh training_scripts/mid_training_exp.sh
```


### Citation

If you think this work is useful, please cite our paper.

```bibtex
@article{zheng2025parallel,
  title={Parallel-r1: Towards parallel thinking via reinforcement learning},
  author={Zheng, Tong and Zhang, Hongming and Yu, Wenhao and Wang, Xiaoyang and Yang, Xinyu and Dai, Runpeng and Liu, Rui and Bao, Huiwen and Huang, Chengsong and Huang, Heng and others},
  journal={arXiv preprint arXiv:2509.07980},
  year={2025}
}
