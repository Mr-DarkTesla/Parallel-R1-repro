# Correctness-gated efficiency rewards

The optional Qwen3-0.6B recipe compares two independent runs from the same
original Unseen-SFT checkpoint. It does not change the existing S1/S2 defaults.
The code was promoted from the October 8 experiment snapshot; that snapshot and
its running processes are independent of this checkout.

## What is measured

- `c`: binary correctness from the existing `math_dapo` answer checker.
- `D`, critical generation depth: sum of main/summary generated token counts,
  plus the maximum generated length among concurrent paths in each fork.
- `T`: total generated tokens, summing every path rather than taking its maximum.
- `v`: at least one executed fork and complete, unnested Parallel/Path/Summary
  blocks with at least two paths per block and a following summary.

For main=10, paths=(30, 50), summary=5, `D=65` and `T=95`.
Both counts include sampled stop tokens and exclude runtime-inserted tags and
prompt prefill. `response_length/mean` measures retained response tokens, which
also include inserted tags. Critical depth is an idealized serial decode count,
not physical GPU forwards, FLOPs or measured wall time. The separate forward
probe is required to count actual eager batched forwards.

## Rewards and advantages

| Mode | Training reward | Default coefficient |
|---|---|---|
| `gated_depth` | `c - lambda*c*D` | `lambda=0.0001` |
| `parallel_gain` | `c + alpha*c*v*(1-D/T)` | `alpha=0.2` |

Efficiency is zero when `T=0`. Wrong answers receive zero auxiliary reward.
Validation always returns `c` alone, while recording depth and format metrics.
Keep `lambda*max(D)<1` so a correct solution scores above an incorrect one;
the 3000-token budget and default lambda bound the cost by 0.3.

Ordinary GRPO standardizes the **entire** scalar reward. In a group where all
answers have the same correctness, this can cancel the auxiliary coefficient.
The opt-in `algorithm.split_accuracy_aux=true` instead computes

```text
A_i = (c_i - mean_group(c)) / (sample_std_group(c) + 1e-6)
      + auxiliary_i - mean_group(auxiliary)
```

This preserves the cost/bonus scale. All-wrong and singleton groups have zero
advantage; all-correct groups can still optimize efficiency. The implementation
requires GRPO, accuracy standardization, finite components, binary correctness,
zero auxiliary reward for incorrect answers, and no in-reward KL. An actor KL
loss is a separate mechanism; the recipe leaves it disabled.

Monitor `reward/accuracy_mean`, `reward/aux_mean`, `reward/total_mean`,
`advantage/accuracy_abs_mean`, `advantage/aux_abs_mean`, and
`grpo/mixed_accuracy_group_fraction`. Reward output additionally contains
`depth_penalty`, `parallel_bonus`, `critical_depth`, `generated_tokens`,
`parallel_efficiency`, `forks`, `format_ok` and `acc`. These fields are saved in
rollout/validation JSONL. Do not interpret higher total reward alone as better
reasoning: the cost can favor short correct shortcuts; the relative bonus can
favor extra tokens in parallel paths. Check held-out accuracy, answer
distribution, depth **and** total length together.

## Launching the pair

Use the existing training environment (PyTorch 2.6.0, Transformers 4.53.2,
vLLM 0.8.5.post1 and the repository dependencies), an original Unseen-SFT HF
checkpoint, and separately prepared train/validation parquet files. Rows follow
the existing verl schema: `prompt` is a chat-message list, `data_source` names
the split, `reward_model.ground_truth` holds the answer, and `extra_info.index`
identifies the question. Preserve the original Parallel-R1 prompt instructions.
The launcher checks separate file paths; dataset decontamination remains a
preparation step, not something this path check proves.

```bash
export NPROC_PER_NODE=8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
SFT=/path/to/original-unseen-sft
TRAIN=/path/to/train.parquet
VAL=/path/to/validation.parquet
RUN=/path/to/new-empty-campaign

# Sequential, independent initialization; the second command requires success.
bash scripts/rl_efficiency.sh gated_depth "$SFT" "$TRAIN" "$VAL" "$RUN/gated_depth" &&
bash scripts/rl_efficiency.sh parallel_gain "$SFT" "$TRAIN" "$VAL" "$RUN/parallel_gain"
```

Defaults: batch32, 8 responses/question, PPO minibatch16, microbatch2/GPU,
400 steps, seed20261008 for data shuffling, maximum prompt2000/response3000,
validation every50 and full model/optimizer/extra/HF checkpoint every100,
retaining two checkpoints. Each stage starts with resume disabled. Use a new
output directory for each recipe/version. Hydra overrides go after the output
directory; for example `custom_reward_function.reward_kwargs.depth_lambda=0.00005`.
`--cfg job --resolve` prints the composed configuration without training.

The October 8 campaign also enabled fused Triton kernels, replicated FSDP
(`NO_SHARD`), logprob-row/microbatch-group scheduling, deferred gradient sync,
zero-advantage skips and delayed full decode graphs. These hardware-dependent
performance options are documented in the main README and are **not** enabled
by this portable reward recipe. It is not a bitwise replay of the frozen run.

This launcher executes a stage in the foreground. The original server queue's
PID ownership, retries and final-artifact verification were deployment-specific
and remain outside Git. For unattended work, use a scheduler/supervisor and an
immutable checkout, not an editable working tree. A successful process exit
alone does not establish a complete experiment: verify the final full checkpoint,
HF weights/tokenizer, complete held-out rows, metrics and released job resources.

## Checks

```bash
python -m unittest discover -s tests -v
```

CPU tests exercise the real reward and advantage functions, the reward-manager
and trainer bridges without Ray/GPU infrastructure, coefficient scaling,
all-wrong/singleton groups, padding, malformed tags and multi-fork depth.
The existing S2 schedule tests remain unchanged. Distributed training and CUDA
performance need their own checks on the intended hardware.
