# Shared Qwen3-4B Instruct RL runtime

GPU count and effective batch are separate configuration fields. All presets
(`configs/r2-{8,16,24,32}gpu.json`) keep **8 prompts × 4 responses = 32 responses
per update**, the same R2 reward, and the same global target of 500 iterations.
They use the same `train.py`, decoder, replay, reward, and distributed entry.

| GPUs | Ranks per prompt | Responses per rank within a prompt |
| --- | --- | --- |
| 8 | 1 | 4 |
| 16 | 2 | 2 |
| 24 | 3 | 2, 1, 1 |
| 32 | 4 | 1 |

`batching.py` validates ownership and complete prompt groups. Rewards are centered
within each prompt's four responses, without division by std. Each rank sums its
response losses with scale `world_size / responses_per_step`; DDP averages these
rank gradients. Thus both equal and unequal local response counts produce the
same global response mean. Data order and per-response seeds are independent of
GPU ownership. Other explicit batch sizes are supported; GPU count never changes
the effective batch implicitly.

The fullwidth decoder executes all live branches (width up to 8) in one forward.
The trajectory ledger must equal the physical model.forward counter. Runtime
headers/bridges have policy loss 0, raw sampled actions including terminal tokens
have loss 1, and replay preserves sibling isolation and repeated positions.
The correctness scorer receives the native Think opener plus raw output.

Replay violations use the same collective rejection thresholds: max .01,
mean .002, p95 .005. A rejected batch updates no Adam state on any rank and remains
a technical unknown. Three consecutive rejections, or over 10% after 20 phase
iterations, stop the run for investigation.

## Prepare and launch

Fill the model, train, validation, scorer, and system paths in a copied preset.
If the platform entry Python differs from the installed training environment,
set `python_executable` to that environment's standalone Python.

```sh
python experiments/parallel_instruct/prepare_run.py \
  --config /path/to/filled-r2-8gpu.json \
  --run-root "$PWD/work/experiments/my-r2-run"
export PARALLEL_R1_RUN_ROOT="$PWD/work/experiments/my-r2-run"
torchrun --standalone --nproc_per_node=8 experiments/parallel_instruct/node_entry.py
```

For multiple nodes, use the platform launcher with `expected_world_size / 8`
nodes, 8 processes per node, and `PARALLEL_R1_RUN_ROOT` in the job environment.
`prepare_run.py` does not allocate GPUs, submit a job, or stop existing workers.
`node_entry.py` performs two actual full-model smoke updates and resident-Adam
width 2/3/4/6/8 fixtures on every rank, verifies clean exits, and then releases
production automatically. CPU tests do not substitute for this per-run GPU gate.

Exports are a single `model.safetensors` plus tokenizer/config on steps
50/100/200/300/400/500, with no optimizer or RNG states. For continuation, set
`initial_step`, `initial_checkpoint`, `model=<checkpoint>/hf`, and the exact
`prompt_exposure_offset` from the earlier phase. Adam is reset; this is a
weights-only continuation to the global target, not an exact optimizer resume.

## Verification and frozen runs

```sh
python -m unittest discover -s tests -p test_parallel_instruct_batching.py
python experiments/parallel_instruct/proof_distributed_batch.py \
  --output "$PWD/work/experiments/common-batch-cpu-proof" --world 8
```

The dated `work/experiments/` sources preserve earlier experiments, including the
8-GPU controls, the 24-GPU run, and the validated pending 32-GPU handoff. Those
frozen run inputs are not overwritten by this shared runtime. Every preset above
must pass its actual distributed GPU smoke before production; this code does not
claim new 8/16/24/32-GPU production results.
