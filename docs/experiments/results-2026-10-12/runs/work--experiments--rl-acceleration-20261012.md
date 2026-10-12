# work/experiments/rl-acceleration-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32.failed-startup-1/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32.failed-startup-1/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpiworker-0",
  "started": 1791815067.3444269,
  "port": 35835,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config.json",
  "config_sha256": "514de21a1954b4e317d6727eeefcf10dd1dae024ac806efbf2121ab7da22a8fd",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791817064.6604614
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "BF16q_TIS_Cstateless_cohort_exact_FP32_batched_replay_Dabort",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 51,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "cohort_rows": 32,
  "replay_max_rows": 4,
  "replay_padded_token_budget": 8192,
  "replay_head_token_budget": 4096
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "BF16q_TIS_Cstateless_cohort_exact_FP32_batched_replay_Dabort",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 51,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "cohort_rows": 32,
  "replay_max_rows": 4,
  "replay_padded_token_budget": 8192,
  "replay_head_token_budget": 4096
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort128-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort128-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort128",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 32,
    "rollouts_per_prompt": 4,
    "responses_per_step": 128
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 16,
    "rollouts_per_prompt": 4,
    "responses_per_step": 64
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 16,
    "rollouts_per_prompt": 4,
    "responses_per_step": 64
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpiworker-1",
  "started": 1791811363.6184099,
  "port": 41931,
  "config": "work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config.json",
  "config_sha256": "81f90a70c6f279d96ec015d1d61fa076c2953e277d7f8a3a9bc1800d3cc82cfd",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791812830.8557012
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "A_BF16q_TIS_C_phase_cohort_D_abort_stateless_core",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 52,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "A_BF16q_TIS_C_phase_cohort_D_abort_stateless_core",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 52,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "cohort_rows": 32
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "paired_pilot": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "paired_pilot": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "failed_fixture_reference": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": true,
  "cohort_rows": 32,
  "resident_cohort_rows": 32,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "failed_fixture_reference": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": false,
  "cohort_rows": 32,
  "resident_cohort_rows": 0,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "learner_precision": "bf16_autocast_fp32_master_gradient_adam",
  "actor_implementation": "C+B+D+lazy_exact_shape_CUDAgraph",
  "max_total_KV_row_tokens": 131072,
  "fixture_reuse_scope": "D4/D6 semantic layout + A9795 master teacher; new combined B8/16/32 resident gate remains required",
  "controller_owner": "D worker0 AFTER C terminal and GPU-empty"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": false,
  "cohort_rows": 32,
  "resident_cohort_rows": 0,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "learner_precision": "bf16_autocast_fp32_master_gradient_adam",
  "actor_implementation": "C+B+D+lazy_exact_shape_CUDAgraph",
  "max_total_KV_row_tokens": 131072,
  "fixture_reuse_scope": "D4/D6 semantic layout + A9795 master teacher; new combined B8/16/32 resident gate remains required",
  "controller_owner": "D worker0 AFTER C terminal and GPU-empty"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": false,
  "cohort_rows": 32,
  "resident_cohort_rows": 0,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "learner_precision": "bf16_autocast_fp32_master_gradient_adam",
  "actor_implementation": "C+B+D+lazy_exact_shape_CUDAgraph",
  "max_total_KV_row_tokens": 131072,
  "fixture_reuse_scope": "D4/D6 semantic layout + A9795 master teacher; new combined B8/16/32 resident gate remains required",
  "controller_owner": "D worker0 AFTER C terminal and GPU-empty"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 51,
  "processes_per_node": 8,
  "zero_advantage_replay": true,
  "kv_preflight": false,
  "cohort_rows": 32,
  "resident_cohort_rows": 0,
  "precision_mode": "fp32",
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "learner_precision": "bf16_autocast_fp32_master_gradient_adam",
  "actor_implementation": "C+B+D+lazy_exact_shape_CUDAgraph",
  "max_total_KV_row_tokens": 131072,
  "fixture_reuse_scope": "D4/D6 semantic layout + A9795 master teacher; new combined B8/16/32 resident gate remains required",
  "controller_owner": "D worker0 AFTER C terminal and GPU-empty"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "paired_pilot": true,
  "kv_semantic_cache": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 1,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52,
  "processes_per_node": 8,
  "paired_pilot": true,
  "kv_semantic_cache": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791800769.3024888,
  "port": 33297,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config.json",
  "config_sha256": "53b83e0bd6e964244dfbd241d3e8091583f05f8241f4958bcd1b215feb816ac3",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791802920.6667612
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791803894.6492448,
  "port": 37389,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config.json",
  "config_sha256": "d440fcf64ff9eee69f434f33cf7398da2bf3d4ef9a60964d13be5d91b9d667c0",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791804023.6746488
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_autocast_fp32_attention_head",
  "worker": "src/same_mode_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791815942.839883,
  "port": 54337,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config.json",
  "config_sha256": "8393fd4e9a1b085a441420cc3bfb1200218d6992ab07d9c85087a8b2f49c2035",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791817083.0285213
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 1,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-1",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 1,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 1,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": false,
    "not_a_launcher": true,
    "multinode_launch_required": false,
    "memory_performance_unverified": true,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 2,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-2",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 2,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 2,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": false,
    "not_a_launcher": true,
    "multinode_launch_required": false,
    "memory_performance_unverified": true,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-24.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-24.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-24",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": false,
    "not_a_launcher": true,
    "multinode_launch_required": true,
    "memory_performance_unverified": true,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-32.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-32.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 32,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-32",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 32,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": false,
    "not_a_launcher": true,
    "multinode_launch_required": true,
    "memory_performance_unverified": true,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 4,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-4",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 4,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 4,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": false,
    "not_a_launcher": true,
    "multinode_launch_required": false,
    "memory_performance_unverified": true,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-8.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/config-world-8.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/proof-world-8",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "readiness": {
    "cpu_fixed32_assignment_advantage_gradient_scale_pass": true,
    "actual_gpu_proof": true,
    "not_a_launcher": true,
    "multinode_launch_required": false,
    "memory_performance_unverified": false,
    "no_production_permission_receipt": true
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791815753.269402,
  "port": 34617,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config.json",
  "config_sha256": "62290f8c5edf9c7c690c25f9e091d0419f91fc0f3a2907d9521a5dd621d5ad4d",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-0.log",
      "exit_code": 1
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-1.log",
      "exit_code": 1
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-2.log",
      "exit_code": 1
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-3.log",
      "exit_code": 1
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-4.log",
      "exit_code": 1
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-5.log",
      "exit_code": 1
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-6.log",
      "exit_code": 1
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config-rank-7.log",
      "exit_code": 1
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791815772.2754369
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791803648.4319181,
  "port": 52183,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config.json",
  "config_sha256": "314dbbafc67b18882c0560a68141ca0819fcc90d5fcacd400ffd179e4b11a54a",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791803765.4560084
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_autocast_fp32_head",
  "worker": "src/same_mode_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791807028.8157523,
  "port": 46639,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config.json",
  "config_sha256": "8f9cb7ae2c801ad2fab04d330a67f87d97db0dde71623f0b8d0a9bf16565ac97",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791808176.999431
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "bf16_rollout_fp32_learner_tis",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 52,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "bf16_rollout_fp32_learner_tis",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 52,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791803212.2273629,
  "port": 49159,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config.json",
  "config_sha256": "a2595f8b7d82a41a4d0a5a01eac6da2b0ee6bf56d91db6fb698abe9d7c1aa5c1",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791803269.2425828
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/fp32-control",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "fp32_control",
  "worker": "src/precision_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791805522.311661,
  "port": 60673,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config.json",
  "config_sha256": "e579ca7955ca50654eb673e6541f3e31ab46857f323fa16bb49235868cd67939",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791805638.3377948
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "full_bf16_native_guard",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_full_autocast",
  "worker": "src/same_mode_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791805763.3359594,
  "port": 54305,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config.json",
  "config_sha256": "3b890040bf8c17269da454bab0615b7b1dc8b3b01322ae548a65c0f2423b448a",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791805879.3607895
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "full_bf16_native_guard",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_full_autocast",
  "worker": "src/diagnose.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791806020.4935744,
  "port": 37827,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config.json",
  "config_sha256": "461e360580d4d4f57464f7d76fcfe22d306bb64c51520a3b7078c97b466ef031",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791806061.5080333
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "full_bf16_native_guard",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_full_autocast",
  "worker": "src/proximal_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791811310.8067882,
  "port": 52991,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config.json",
  "config_sha256": "449d79dce2faabbfb9bfe61a2c9eabe6ffa69cc9f7c0f0cf577f7cc267eef32f",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791811346.8192372
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "graph_preflight_no_Adam",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_full_autocast",
  "worker": "src/graph_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791811002.5038311,
  "port": 42653,
  "config": "work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config.json",
  "config_sha256": "0068ebc33521aaf949a3de3f758d7ca823fdf9394a19f88395236f7a9b801d2e",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-1.log",
      "exit_code": 1
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-2.log",
      "exit_code": 1
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-3.log",
      "exit_code": -15
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-4.log",
      "exit_code": -15
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-5.log",
      "exit_code": -15
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-6.log",
      "exit_code": -15
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config-rank-7.log",
      "exit_code": -15
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791811036.5190203
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "graph_preflight_no_Adam",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "bf16_full_autocast",
  "worker": "src/graph_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/attempt2/config-single.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/attempt2/config-single.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/attempt2/single",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "slot_capacity": 65536,
  "actor_port_base": 54845,
  "rank": 0,
  "world": 1
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/config-single.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/config-single.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 53,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "standard_BF16_learner_graph_actor_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/ipc-weight-refresh/single",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": 53,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "slot_capacity": 65536,
  "actor_port_base": 59123,
  "rank": 0,
  "world": 1
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791802933.4670076,
  "port": 42765,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config.json",
  "config_sha256": "bff1d4c4760de57ffd252a861ef740e6186f3c637d5d9a0b84301a0ba7b7688e",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791802969.4785514
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": true,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "tf32",
  "worker": "src/precision_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-launch.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-launch.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "node": "RUN_5482aee87e-mpimaster-0",
  "started": 1791803444.7035236,
  "port": 40137,
  "config": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config.json",
  "config_sha256": "3feca87096781629d699215c0db6a902af2c109f320deedb31ff79780012e6c5",
  "workers": [
    {
      "rank": 0,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-0.log",
      "exit_code": 0
    },
    {
      "rank": 1,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-1.log",
      "exit_code": 0
    },
    {
      "rank": 2,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-2.log",
      "exit_code": 0
    },
    {
      "rank": 3,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-3.log",
      "exit_code": 0
    },
    {
      "rank": 4,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-4.log",
      "exit_code": 0
    },
    {
      "rank": 5,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-5.log",
      "exit_code": 0
    },
    {
      "rank": 6,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-6.log",
      "exit_code": 0
    },
    {
      "rank": 7,
      "log": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config-rank-7.log",
      "exit_code": 0
    }
  ],
  "world": 8,
  "no_new_allocation": true,
  "full_run": false,
  "finished": 1791803599.7342522
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": true,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "tf32",
  "worker": "src/same_mode_gate.py",
  "baseline_output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline",
  "reference_cleanval": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050",
  "likelihood_only": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-train-config.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-train-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 55,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": true,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/src/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "profile_precision_baseline8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-train",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "tf32",
  "worker": "src/train.py",
  "resident_fixture_step": 52
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/async-lag1/SOURCE_MANIFEST.json](../artifacts/work/experiments/rl-acceleration-20261012/research/async-lag1/SOURCE_MANIFEST.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "CPU engineering artifacts only",
  "files": {
    "three-policy-proof.json": "7e03f982a3910579ac1af7261dc3429547f252dc7d8793cac743a5aba5ea469b",
    "SOURCE_PROVENANCE.json": "da14d9e2e3a76a9dc06f4c5ea5e7f7d41ae6f935478f80600f3c4736782cefa4",
    "REPORT.md": "701fbfd470927943daef1ba39930b22c3e30acdb2ff2e67b731c7645fc6f997c",
    "proximal.py": "87555325f6a0bd286a91feb8d2ac373a1c106344dc2c1e0a230ae20ee94ec0a7",
    "prove_three_policy.py": "e8a9bc2bd127d47eec3247eda0802657ec64514b8869d015a877be85f63886b9",
    "three_policy.py": "eee0a44c7844b986d82140a069798c5c94616cc57e64f8fbd33081c922b942de",
    "test_scheduler.py": "1d8e30506da96c38e27a31381e58645a6c38da403c9a11a54d40387e2c0eb62f",
    "example-batch.json": "85102058f3b1c461cec274417d92a71af5a89d7284a890ddcde672349f5cbe9a",
    "batch.schema.json": "aa8e4bfb648a0e0d1652a2ac12d3b2703546eb925379fa18191d9a0fe6e41fd1",
    "scheduler.py": "d8ea6af078d7796c549b7b8f41a1b36a3ee09811c3e61b1b926081906a4350e1",
    "demo.py": "1b4774cac59532c16641635ce40f09e431df9b16abed140ab326dd5b1f1bdf8b",
    "queue-proof.json": "3ebf87b7ee70a2ac865637e6eec9e82ac90d882b19cd1cb59144b4228864dc9a",
    "prove_queue.py": "0e14427a6a11f738d44826d728e53f3f3a6c5be80331a863b832fdd9453ce4fc",
    "proof-sources/prove_three_policy.py": "e8a9bc2bd127d47eec3247eda0802657ec64514b8869d015a877be85f63886b9",
    "proof-sources/three_policy.py": "eee0a44c7844b986d82140a069798c5c94616cc57e64f8fbd33081c922b942de",
    "proof-sources/scheduler.py": "54252660dfdf85f3d9f81f364a35de322613de18ba4abf5eb7df713230ac9f4b"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/engine_patch/manifest.json](../artifacts/work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/engine_patch/manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "repo": "sgl-project/sglang",
  "release": "v0.4.6.post3",
  "commit": "678d8cc98768cfda795bd60c05e6ab84576fb0bd",
  "files": [
    {
      "path": "python/sglang/srt/model_executor/forward_batch_info.py",
      "upstream_sha256": "2b3df446e123b8e00df7ff2196fbe49c5e2a7a88726acecdad2f7414246d20c8",
      "patched_sha256": "e193acc8448b4d0d1a7ad2154e73616bf8fbf7672965c513aa160faabacca39e",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/model_executor/forward_batch_info.py"
    },
    {
      "path": "python/sglang/srt/layers/attention/flashinfer_backend.py",
      "upstream_sha256": "e774d7866069539aecd38fb8bbec97725c09e54620ed625fc8b0d927c9d20ce5",
      "patched_sha256": "e8dfa46201f86f62595948a1d6e6582e9dd699539b1728d05c5496d3093c20fc",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/layers/attention/flashinfer_backend.py"
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/prototype-manifest.json](../artifacts/work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/prototype-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "CPU adapter and pinned SGLang schema qualified; native kernels NOT run",
  "CUDA_GPU_runs": 0,
  "native_package_installations": 0,
  "files": [
    {
      "path": "README.md",
      "sha256": "cd9845f27f9aac3fc8becd9846047a1385673063f1fbac834b0c2b26d6764438",
      "bytes": 8510
    },
    {
      "path": "build_engine_patch.py",
      "sha256": "409224f0a3e7b1afbb720eb68323868cf9ae87ae382763ebeb587f6b781c5e08",
      "bytes": 2793
    },
    {
      "path": "dependencies-current.json",
      "sha256": "3036878c36e3dd780aab526d5ee55782e19346470b6c9737334b1bd623a6b014",
      "bytes": 5153
    },
    {
      "path": "engine_patch/manifest.json",
      "sha256": "6655a968805ea3c60074a20544efc9bfd9ffe33aa97c10ab11af2584538aac16",
      "bytes": 989
    },
    {
      "path": "engine_patch/python/sglang/srt/layers/attention/flashinfer_backend.py",
      "sha256": "e8dfa46201f86f62595948a1d6e6582e9dd699539b1728d05c5496d3093c20fc",
      "bytes": 48193
    },
    {
      "path": "engine_patch/python/sglang/srt/model_executor/forward_batch_info.py",
      "sha256": "e193acc8448b4d0d1a7ad2154e73616bf8fbf7672965c513aa160faabacca39e",
      "bytes": 27868
    },
    {
      "path": "engine_patch/structured-self-mask.patch",
      "sha256": "c100b6422291319c773c28746f1459fcb93da666dda2dd1f937df40d1e548680",
      "bytes": 2025
    },
    {
      "path": "probe_dependencies.py",
      "sha256": "2f611ec69b19f13bcceefbb85f01d77dd2b5221664e0230480cfa3f64f182f35",
      "bytes": 1327
    },
    {
      "path": "proof_adapter_cpu.json",
      "sha256": "186cadbb259be4724fcbc1ce54b852a5fb9372f34e45ccc709b34c940f730f35",
      "bytes": 22550
    },
    {
      "path": "proof_adapter_cpu.py",
      "sha256": "69f2b3c34c3dc9551a530998ffd4aeeb82c6bd413d1b6fc13a9211e6ac43b2f2",
      "bytes": 6025
    },
    {
      "path": "proof_sglang_schema_cpu.json",
      "sha256": "1687dfd9263f190656c68dcb4b8bd58a31344309480e7fd123f400044627193e",
      "bytes": 22638
    },
    {
      "path": "run_sglang_gpu_probe.py",
      "sha256": "729a75e6e6bb3d0659545f0102c1d2623263f63a99bbb11959fe102486c93fc8",
      "bytes": 5394
    },
    {
      "path": "sglang-046-pyproject.toml",
      "sha256": "fd9b36b1a10e061f5a731e61eb00cc58d8f3ba8bdca11acf61ceaa53685682c2",
      "bytes": 4158
    },
    {
      "path": "sglang-046-source-manifest.json",
      "sha256": "6ced1a44028fbfdbabb4298a89c20b18dd31f7352a603e31460287bd0715d392",
      "bytes": 2831
    },
    {
      "path": "sglang_schema_fixture.py",
      "sha256": "d1ca864bbddb4f05af37fd1726f7d08310cc89ac38a97a7e221e0d506754175f",
      "bytes": 3907
    },
    {
      "path": "sglang_slot_backend.py",
      "sha256": "4e78b8b9af98b0f91793387ab757ff41dfca57bea5ab54a5d3421ddd980f28bb",
      "bytes": 5281
    },
    {
      "path": "structured_adapter.py",
      "sha256": "129f90b0a1e531cb28b16d7ffa1049fef73bd4fb8320906c5c4a61074a24344f",
      "bytes": 13078
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/sglang-046-source-manifest.json](../artifacts/work/experiments/rl-acceleration-20261012/research/structured-serving/prototype/sglang-046-source-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "pin": {
    "repo": "sgl-project/sglang",
    "tag": "v0.4.6.post3",
    "commit": "678d8cc98768cfda795bd60c05e6ab84576fb0bd"
  },
  "files": [
    {
      "path": "python/pyproject.toml",
      "sha256": "fd9b36b1a10e061f5a731e61eb00cc58d8f3ba8bdca11acf61ceaa53685682c2",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/pyproject.toml"
    },
    {
      "path": "python/sglang/srt/configs/model_config.py",
      "sha256": "dd0f5849fe884aeeb36e047a3de302480e443d91631b209c850084e078c083ba",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/configs/model_config.py"
    },
    {
      "path": "python/sglang/srt/layers/attention/flashinfer_backend.py",
      "sha256": "e774d7866069539aecd38fb8bbec97725c09e54620ed625fc8b0d927c9d20ce5",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/layers/attention/flashinfer_backend.py"
    },
    {
      "path": "python/sglang/srt/layers/logits_processor.py",
      "sha256": "44c7208a674108e4e0fe293252fcaa3c9fc173fd2b2812b902d0d304fc90640a",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/layers/logits_processor.py"
    },
    {
      "path": "python/sglang/srt/mem_cache/memory_pool.py",
      "sha256": "0c6d36b59ee33d1a21d7f39572f9a1c8783cbbe60a944b817bd02fc81f3ca7a6",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/mem_cache/memory_pool.py"
    },
    {
      "path": "python/sglang/srt/model_executor/forward_batch_info.py",
      "sha256": "2b3df446e123b8e00df7ff2196fbe49c5e2a7a88726acecdad2f7414246d20c8",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/model_executor/forward_batch_info.py"
    },
    {
      "path": "python/sglang/srt/model_executor/model_runner.py",
      "sha256": "2f2da64836c8f37501a26e051c330f20a742a92e26ff6b7b3be8195a36079d81",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/model_executor/model_runner.py"
    },
    {
      "path": "python/sglang/srt/models/qwen3.py",
      "sha256": "ade6a8c06928b580061d2e734c25abbe7cb1b6ef7640abacd7d9fed9a9ad31ae",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/models/qwen3.py"
    },
    {
      "path": "python/sglang/srt/server_args.py",
      "sha256": "e7333bbe632e66c0c348f12a17efe081964fc0676159c830ccb2b25f74398835",
      "url": "https://github.com/sgl-project/sglang/blob/678d8cc98768cfda795bd60c05e6ab84576fb0bd/python/sglang/srt/server_args.py"
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/structured-serving/upstream_manifest.json](../artifacts/work/experiments/rl-acceleration-20261012/research/structured-serving/upstream_manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "retrieved": "2026-10-12",
  "pins": {
    "sglang": {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb"
    },
    "vllm": {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6"
    },
    "parallel": {
      "repo": "zhengkid/Parallel-R1",
      "commit": "f1c63891d7fe77335103eb2c17e542a2b086dafc"
    }
  },
  "files": [
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/entrypoints/engine.py",
      "bytes": 81135,
      "sha256": "32dc558091b56c1145c29fd80efd976b8e40255fc8dcd8d39ac70e5449c7a7dc",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/entrypoints/engine.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/layers/attention/flashinfer_backend.py",
      "bytes": 106071,
      "sha256": "5c8baba0d14eeca4c9d4bef8674318be1697b0160f105224282cd4aa27575810",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/layers/attention/flashinfer_backend.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/managers/io_struct.py",
      "bytes": 106368,
      "sha256": "c1a1863e431b84836ece23a3a5550c562e34148c771811064a81c810ecd68554",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/managers/io_struct.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/managers/schedule_batch.py",
      "bytes": 169729,
      "sha256": "b2f78c781de88c36ce27cc5d44b343420338b4da299e885c575665d6fab843ca",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/managers/schedule_batch.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/managers/scheduler.py",
      "bytes": 268724,
      "sha256": "b61df5b750adc748a99ceb381b8494c199fb3f704d793da5a0217bd6bbb606c4",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/managers/scheduler.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/mem_cache/memory_pool.py",
      "bytes": 241850,
      "sha256": "47e13954eb8b06836a5279fedd1f79f03dbd40245819ae152af3a02f3887c1ac",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/mem_cache/memory_pool.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/mem_cache/radix_cache.py",
      "bytes": 30883,
      "sha256": "3a98ff02d5bb990fab3ff6700a4acd1ed865f9fc522daa17768f28fc6fe424e6",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/mem_cache/radix_cache.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/model_executor/forward_batch_info.py",
      "bytes": 93984,
      "sha256": "ef4426b3ece1b515eeb5223d394de6a8d154d912bcf62e7ed4bae20e17064797",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/model_executor/forward_batch_info.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/model_executor/model_runner.py",
      "bytes": 99431,
      "sha256": "36e7a69f345cf09f24699eea36a4ab0a2a305acb8b8a7e9b4e975f3fd09527f3",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/model_executor/model_runner.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/model_executor/runner/decode_cuda_graph_runner.py",
      "bytes": 70704,
      "sha256": "1ec64d53550012a006d2fb7acbcabeefb6d3a3729864373d870314aed19f94cd",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/model_executor/runner/decode_cuda_graph_runner.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/models/qwen3.py",
      "bytes": 27165,
      "sha256": "21e42f97190a30d6c27cb7ae5438eb94ae6c3be1ee97f7a9f3b6008b38648510",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/models/qwen3.py"
    },
    {
      "repo": "sgl-project/sglang",
      "commit": "e00930c5489053f26d86b179cee0d087f846acbb",
      "path": "python/sglang/srt/speculative/spec_info.py",
      "bytes": 19594,
      "sha256": "43e59f9d15b711753a9170807452f5643085cc9d9811345761559b0e908d2fa9",
      "url": "https://github.com/sgl-project/sglang/blob/e00930c5489053f26d86b179cee0d087f846acbb/python/sglang/srt/speculative/spec_info.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/inputs/engine.py",
      "bytes": 11402,
      "sha256": "98a19626a7b918bf180e08c654091b3eb108615a98cd6da4de3e433eb082a425",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/inputs/engine.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/inputs/llm.py",
      "bytes": 7679,
      "sha256": "6ce1849b1951d7c84c3955634dae04371c51596fc86b7146cdb7849cde76cddd",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/inputs/llm.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/model_executor/models/qwen3.py",
      "bytes": 12680,
      "sha256": "05a05b2e00b8b8ac31f8c2508e2f5462a276348439fe8fc565c75510eaca7c81",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/model_executor/models/qwen3.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/attention/backends/flashinfer.py",
      "bytes": 120087,
      "sha256": "9e65e124edc2a8e36c7e29306159dc51d345978ed7987ac3164983a2c17cb94c",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/attention/backends/flashinfer.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/core/kv_cache_manager.py",
      "bytes": 41801,
      "sha256": "bd9bf46a2101f9368d4941867415a239d18d95e0b956f82f885ce25e10e69f3b",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/core/kv_cache_manager.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/core/sched/scheduler.py",
      "bytes": 159016,
      "sha256": "f820bee4f42b878b262a30f3728a97d7413477b2a277748e20f2528ac2ec2f2a",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/core/sched/scheduler.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/engine/async_llm.py",
      "bytes": 53708,
      "sha256": "ff933ed78aa3195782cf1c6d18c53897adfa5bf920421bd2bcc330f2adc84d1e",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/engine/async_llm.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/worker/block_table.py",
      "bytes": 20501,
      "sha256": "a700a5c511326c8a6272954635ebadd29043deef91f5d4327e40a5bca9ba612c",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/worker/block_table.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/worker/gpu_input_batch.py",
      "bytes": 48691,
      "sha256": "e7e57887b396014a84d64cab26bf678f982844fea15361b09d95f36bd78bc58d",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/worker/gpu_input_batch.py"
    },
    {
      "repo": "vllm-project/vllm",
      "commit": "db9527a46873454610df6dbedf79a36d6bf1a7f6",
      "path": "vllm/v1/worker/gpu_model_runner.py",
      "bytes": 335342,
      "sha256": "bb903dffcb5a6e5b8a477daf0854b3812e135349d61fc20c6133f91cd3c9752a",
      "url": "https://github.com/vllm-project/vllm/blob/db9527a46873454610df6dbedf79a36d6bf1a7f6/vllm/v1/worker/gpu_model_runner.py"
    },
    {
      "repo": "zhengkid/Parallel-R1",
      "commit": "f1c63891d7fe77335103eb2c17e542a2b086dafc",
      "path": "README.md",
      "bytes": 5404,
      "sha256": "4ee9a94bccc721e7a6f48b63ea3bed10c3b74363ee77c3ced5c8caf43676c432",
      "url": "https://github.com/zhengkid/Parallel-R1/blob/f1c63891d7fe77335103eb2c17e542a2b086dafc/README.md"
    },
    {
      "repo": "zhengkid/Parallel-R1",
      "commit": "f1c63891d7fe77335103eb2c17e542a2b086dafc",
      "path": "verl/scripts/install_vllm_sglang_mcore.sh",
      "bytes": 2456,
      "sha256": "0650b974d3540058f3170ab7f58739ca6f387b5ea8289844177a277f945dd7c8",
      "url": "https://github.com/zhengkid/Parallel-R1/blob/f1c63891d7fe77335103eb2c17e542a2b086dafc/verl/scripts/install_vllm_sglang_mcore.sh"
    },
    {
      "repo": "zhengkid/Parallel-R1",
      "commit": "f1c63891d7fe77335103eb2c17e542a2b086dafc",
      "path": "verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py",
      "bytes": 21519,
      "sha256": "c25d3a8fbce2a4d5cd242d545b771a04b76669dc201dc3aeba7043970b14eb81",
      "url": "https://github.com/zhengkid/Parallel-R1/blob/f1c63891d7fe77335103eb2c17e542a2b086dafc/verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py"
    },
    {
      "repo": "zhengkid/Parallel-R1",
      "commit": "f1c63891d7fe77335103eb2c17e542a2b086dafc",
      "path": "verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py",
      "bytes": 13695,
      "sha256": "67c8b1edcc04c8ba71f94c3ff5c1e3e09e1ee1369b506760e29a0e5217a9bc8e",
      "url": "https://github.com/zhengkid/Parallel-R1/blob/f1c63891d7fe77335103eb2c17e542a2b086dafc/verl/verl/workers/rollout/vllm_rollout/vllm_async_server.py"
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/config.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "vllm_bf16",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": null,
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "vLLM_CUDA_IPC_actor_fullBF16_learner_FP32masters_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": null,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "actor_port_base": 29921,
  "slot_capacity": 65536,
  "validation_after_final": false,
  "worker": "src/train.py"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/config.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 52,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "vllm_bf16",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": null,
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": false,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "vLLM_CUDA_IPC_actor_fullBF16_learner_FP32masters_TIS",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 8,
    "rollouts_per_prompt": 4,
    "responses_per_step": 32
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "prior_prompts": 1200,
    "remaining_prompts": 3600
  },
  "plain_full500": false,
  "data_seed": 20261012,
  "expected_world_size": 8,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20",
  "initial_checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "initial_step": 50,
  "prompt_exposure_offset": 1200,
  "reward_group": 4,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "processes_per_node": 8,
  "skip_validation": true,
  "skip_exports": true,
  "precision_mode": "full_bf16_compute_fp32_master",
  "rollout_correction": {
    "mode": "token_tis",
    "upper": 2.0,
    "lower": 0.0,
    "batch_normalize": false,
    "bypass": false
  },
  "resident_fixture_step": null,
  "ppo_epochs": 1,
  "updates_per_fresh_batch": 1,
  "async_rollout": false,
  "master_dtype": "fp32",
  "learner_compute_dtype": "bf16",
  "gradient_reduce_dtype": "fp32",
  "allow_natural_precision_output_change": true,
  "actor_port_base": 29921,
  "slot_capacity": 65536,
  "validation_after_final": false,
  "worker": "src/train.py"
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32.failed-startup-1/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32.failed-startup-1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "loading",
  "started": 1791800914.2612033,
  "world_size": 8
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 55,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/checkpoint-0055/hf",
  "initial_step": 50,
  "positive_updates": 5,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/baseline32/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 55,
  "steps": 55
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 55,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/checkpoint-0055/hf",
  "initial_step": 50,
  "positive_updates": 5,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 55,
  "steps": 55
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/validation-0055/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/batched-replay/training/validation-0055/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 55,
  "completed": 16,
  "correct": 12,
  "format_valid": 15,
  "parallel_valid": 15,
  "fork_tasks": 16,
  "widths": [
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4
  ],
  "actual_rounds": 16,
  "logical_depth": [
    678,
    527,
    2446,
    1031,
    483,
    753,
    686,
    1082,
    915,
    836,
    468,
    818,
    673,
    812,
    2347,
    689
  ],
  "sampled_tokens": [
    985,
    949,
    2756,
    1660,
    712,
    1070,
    1159,
    1947,
    1465,
    1432,
    682,
    1221,
    1130,
    1262,
    3522,
    1168
  ],
  "actual_forward_calls": [
    678,
    527,
    2446,
    1031,
    483,
    753,
    686,
    1082,
    915,
    836,
    468,
    818,
    673,
    812,
    2347,
    689
  ],
  "sampler": "FP32 learner HF fullwidth8, temperature1 top_p1 nofilter; fixed clean16 validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 55,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/checkpoint-0055/hf",
  "initial_step": 50,
  "positive_updates": 5,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort32/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 55,
  "steps": 55
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/cohort64/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 51,
  "steps": 55,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 2.7167260412634723e-05,
  "replay_guard_passed": true,
  "replay_parity_skips": 0,
  "max_replay_logp_drift": 0.00012969970703125
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/combined-candidate-plan.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/combined-candidate-plan.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "arm": "cohort64",
  "exit_code": 1
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/validation-0053/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/cohort_batching/unified-bf16-tis/training/validation-0053/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 53,
  "completed": 16,
  "correct": 13,
  "format_valid": 15,
  "parallel_valid": 15,
  "fork_tasks": 16,
  "widths": [
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4
  ],
  "actual_rounds": 16,
  "logical_depth": [
    587,
    526,
    974,
    1387,
    486,
    724,
    715,
    1884,
    1480,
    664,
    436,
    573,
    1054,
    924,
    3501,
    678
  ],
  "sampled_tokens": [
    1122,
    939,
    1392,
    2380,
    705,
    1167,
    1171,
    3390,
    2915,
    1312,
    625,
    920,
    1629,
    1416,
    4080,
    1370
  ],
  "actual_forward_calls": [
    587,
    526,
    974,
    1387,
    486,
    724,
    715,
    1884,
    1480,
    664,
    436,
    573,
    1054,
    924,
    3501,
    678
  ],
  "sampler": "FP32 learner HF fullwidth8, temperature1 top_p1 nofilter; fixed clean16 validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 1243,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791802077.1765876,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke-config.json": "852483ed889797c41fd0a520dfb8226de978aa45462f549a19a58ececa53128e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._node_entry.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/decoder.py": "8928a6d798ed0a2ccfb98caf021ae95af3b4edda6fcce08578b3d4c84bec8c95",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._batching.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._prepare_run.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._structured_replay.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._microbatch_decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/microbatch_decoder.py": "df31d6a43f9efd4b97290e3cad4a5ed9a11b02664973eb1cdf778f31500cf343",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._baseline_decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._baseline_microbatch_decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/baseline_microbatch_decoder.py": "8da067cdc1ed0d4c8f7d3f87472cd25259bbf3944f712784368e03482905a0b3",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._rollout.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._train.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/train.py": "b39339eec83d85b0c7a6989dd4a9be5417590c33b452663b5fc1e4db381ddc77",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._replay_guard.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._proof_distributed_batch.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._reward.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/._gpu_ownership.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/source/._counted_loop.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/source/._parallel_structure.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/compact_decode/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 52,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/checkpoint-0052/hf",
  "initial_step": 50,
  "positive_updates": 2,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 52,
  "steps": 52
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/gpu-kv-preflight-summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/gpu-kv-preflight-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "ranks": 8,
  "widths": [
    2,
    3,
    4,
    6,
    8
  ],
  "full_logits_max": 0.002795696258544922,
  "action_logp_max": 0.000141143798828125,
  "replay_max": 0.0001316070556640625,
  "sibling_max": 0.0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 1852,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791805226.443958,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke-config.json": "7aa92a9cb4470c2649d9efd8cd0655831ddc85ca6ae71c63c5b5653326cb2586",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/decoder.py": "e91eeec467ce905255bac71f89438f340409cee3952e59d1354a5f8cc9161d88",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/train.py": "30ef442f769d78f34a1a648b304e8411528b7576d83c3583c937314b3cc66be9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/semantic_cache.py": "24a860f0a3f8a93445a18883f8d482200231878d7785651a3c9301771532ce67",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/kv_preflight.py": "93a2922e0fd2aca9a3cc16eb56d997f593923c766e465cd45564c63914389263",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/pilot-launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/pilot-launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "gpu_empty": true,
  "time": 1791805550.9699798
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 2769,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791807347.8951607,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke-config.json": "1f7587977e4f7a6491b1aecd678e36f3975e28158ace11ddbeec15ec5d00e36c",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/decoder.py": "6674d7c17667902059b119307567469ba421f31d3c664406ca42113174db7d81",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/train.py": "30ef442f769d78f34a1a648b304e8411528b7576d83c3583c937314b3cc66be9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/semantic_cache.py": "24a860f0a3f8a93445a18883f8d482200231878d7785651a3c9301771532ce67",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/pilot-launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/pilot-launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "gpu_empty": true,
  "time": 1791807660.8401344
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4-finalizer-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4-finalizer-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "terminal_PASS",
  "proof": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4-proof.json",
  "archive": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4-immutable.tar.gz",
  "archive_sha256": "536ca6aa6f6f6ed9bdf5501883d3de3677684b61499badbf3c26de6bee9f6467",
  "time": 1791811111.6154282
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 3813,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791810818.7129054,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke-config.json": "46cdc0f6b6cfef00ab02e2f02623f517c53ffa74c27dcd30738302ac113b116d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/decoder.py": "82749b94750b69df2b2e9d07d60d27b9e0f223db278342df74191399c8606e81",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/cohort_decoder.py": "9446e6e11bcc2dfe76b2829ceca900c70bd6a35f3738f7eb5e4256148f1ed09a",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/train.py": "baf8af5a9c241571649be228d71f6f287e8e4764bff9bc62b38866963e602ea5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/semantic_cache.py": "c49eac6cdd9419952b8e0b80c9b65622c7d9d06066a502d8f429829be280f094",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/resident_cohort.py": "a98992ec5fd52c3d5c079bd8c8718cefd44217771635305089d1975c8c22d4a2",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/pilot-launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/pilot-launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "gpu_empty": true,
  "time": 1791811102.700084
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "hostname": "RUN_5482aee87e-mpiworker-0",
  "assigned_node": "mpiworker-0",
  "launcher_pid": 4774,
  "child_pids": [
    4778,
    4779,
    4780,
    4781,
    4782,
    4783,
    4784,
    4785
  ],
  "world": 8,
  "time": 1791812917.7508194,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke-config.json": "74c3c3d8c9f0cf99468770b95ec0b1ddf44bf0b9c0b04bd13db943ebe4b896b8",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/proof_tis_kernel.py": "035bb9433fb74f00601d047667f05310b659496b445e150af655930e25a442e9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/decoder.py": "08346e24f509b6884007e164884bf55f26bb95cd2a08df730191184b30c6daae",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/precision_fixtures.py": "7f5da9a9fe4f533dfdd19966135ca5fa287814206301e3505631089926988f14",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/cohort_decoder.py": "64c4d6ebb786f630669fcf0523b0fc08a0fbc37fc143010112f24bc78d1d4710",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/resident_cohort.py": "a98992ec5fd52c3d5c079bd8c8718cefd44217771635305089d1975c8c22d4a2",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/train.py": "8557b3321e4ef0b08ced9d20f8e909f5c71a656ed552db7c961f62b08713c137",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/cohort_precision_fixtures.py": "f649d5602732007ab7db34d88edbca72a20a668a16db85c4055a151d472ab41e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/semantic_cache.py": "3bf896f01988ff073d3d3a6e6c56377e76f3680a39460899034aec07cce89d2b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/tis_loss.py": "c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  },
  "failure_reason": "Seven peer CUDA OOM at residentaggregate32; rank0 and waitingcontrollers identity-safe stopped",
  "terminated_owned_pids": [
    4778,
    4774,
    5287
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "loading",
  "started": 1791811847.734603,
  "world_size": 8
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6-finalizer-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6-finalizer-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "terminal_PASS_bounded_TIS",
  "proof": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6-proof.json",
  "archive_sha256": "4df4aad81ced87f034bc96832c5b635f613d97522aac184fafbd4a6ef943718b",
  "time": 1791814168.1149359
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 5522,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791813922.256441,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke-config.json": "d5c4fa97b0d0708b36e495f5f229c25b386ad452c85ea3bc3a970473afa150f5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/proof_tis_kernel.py": "035bb9433fb74f00601d047667f05310b659496b445e150af655930e25a442e9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/decoder.py": "08346e24f509b6884007e164884bf55f26bb95cd2a08df730191184b30c6daae",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/precision_fixtures.py": "7f5da9a9fe4f533dfdd19966135ca5fa287814206301e3505631089926988f14",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/cohort_decoder.py": "64c4d6ebb786f630669fcf0523b0fc08a0fbc37fc143010112f24bc78d1d4710",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/resident_cohort.py": "2dd96803d246ac9dd7c8cd115808f1e74effbb0759eba2c49ac5d5fe6dbe2b53",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/train.py": "06d0917da3874f8e999ee0bcacfa0a6b44780571182649630ca8610d6462f14a",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/cohort_precision_fixtures.py": "f649d5602732007ab7db34d88edbca72a20a668a16db85c4055a151d472ab41e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/semantic_cache.py": "3bf896f01988ff073d3d3a6e6c56377e76f3680a39460899034aec07cce89d2b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/tis_loss.py": "c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/pilot-launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/pilot-launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "gpu_empty": true,
  "time": 1791814164.8936577
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 52,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/checkpoint-0052/hf",
  "initial_step": 50,
  "positive_updates": 2,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 52,
  "steps": 52
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/finalizer-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/finalizer-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "time": 1791821854.7517798,
  "state": "terminal_PASS_bounded_full_mixed",
  "proof": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/proof.json",
  "gpu_empty": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "launcher_pid": 7912,
  "exits": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "time": 1791821851.4984999,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke-config.json": "2177de40c2493215469d8ef8640f9b802f540617ca75544622f9667dba2ede9c",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/proof_tis_kernel.py": "035bb9433fb74f00601d047667f05310b659496b445e150af655930e25a442e9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/decoder.py": "233290b328f5082e16e5c789ea4d75348a099768aec704fff7371b22d9a8939b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/precision_fixtures.py": "7f5da9a9fe4f533dfdd19966135ca5fa287814206301e3505631089926988f14",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/cohort_decoder.py": "0e3c37d2b1f29af8f671e2d0f13a2158d5f9ed3cf5f555412b95d3e5fe91672b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/actor_shadow.py": "99f8b669cb94274f74eaa7928a582dd1626ddf9dbf2c7963165964526e3ecba5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/resident_cohort.py": "2dd96803d246ac9dd7c8cd115808f1e74effbb0759eba2c49ac5d5fe6dbe2b53",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/graph_proxy.py": "5a025bdd568b7e2f9f9770773c328cd9445804932d38d98f1243bfdbc55e71c3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/microbatch_decoder.py": "7d089bddb22c6546ebb0657bb76b407f11d4ce284964fbe053fe3fbaf42835e2",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/graph_cache.py": "215c0f76b808ab24e01b1ba9250d911abd002a5a3ec49baaa10529e731cd30d3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/prove_bf16_master.py": "58c5f88e195d33f2aaa45700ad348ef399e7795ee25775f57cc965b087912c57",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/train.py": "7d05c4c6bd51f0ef91f06487b8f8af8dae3d07c11a2c7b0a48f7a120705030fc",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/cohort_precision_fixtures.py": "2f762bc7ad3f7a931b96f15b80eacfc4bce3446add4d0ba4b05e3578b463270b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/semantic_cache.py": "3bf896f01988ff073d3d3a6e6c56377e76f3680a39460899034aec07cce89d2b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/static_pool.py": "bc2e3b4f37dc5c3bb0470a78762e1b6f8def04be3bb70dee2a488184cf487d73",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/resident_combined.py": "6c2da5650959e2ac751b17f44a9cae7d91713355028b5114e6b698209a99f78a",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/tis_loss.py": "c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "passed",
  "exit_code": 0,
  "start": 1791820840.5033274,
  "end": 1791820898.4594707,
  "cpu_only": true,
  "source_unchanged": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/finalizer-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/finalizer-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "time": 1791820353.8153262,
  "state": "failed_artifacts_retained",
  "error": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/finalize.py\", line 13, in <module>\n    if train['state']=='failed':raise RuntimeError('Owned distributed qualification failed; all artifacts preserved')\n                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nRuntimeError: Owned distributed qualification failed; all artifacts preserved\n"
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "launcher_pid": 7390,
  "exits": [
    -15,
    -15,
    -15,
    1,
    1,
    -15,
    -15,
    -15
  ],
  "time": 1791820331.0004435,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke-config.json": "235c6059a49e4ce077c9e641dfaede99a37c58d099c1904d2754375d9e5e7a01",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/proof_tis_kernel.py": "035bb9433fb74f00601d047667f05310b659496b445e150af655930e25a442e9",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/decoder.py": "233290b328f5082e16e5c789ea4d75348a099768aec704fff7371b22d9a8939b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/precision_fixtures.py": "7f5da9a9fe4f533dfdd19966135ca5fa287814206301e3505631089926988f14",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/cohort_decoder.py": "0e3c37d2b1f29af8f671e2d0f13a2158d5f9ed3cf5f555412b95d3e5fe91672b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/actor_shadow.py": "a0b5f4fd93600a31f8fe7f6eea89601bbf901f0a4b88ceb8b29e4debda0b957d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/lane_profile.py": "5778a5ff3b31659da2999eb4df0b3f10a8586d067e96ca30f22b89bdc325ccb5",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/resident_cohort.py": "2dd96803d246ac9dd7c8cd115808f1e74effbb0759eba2c49ac5d5fe6dbe2b53",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/graph_proxy.py": "8c7885610693c506884500faa58b0f53047585d45fca154747b84fa6d095c3fd",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/microbatch_decoder.py": "7d089bddb22c6546ebb0657bb76b407f11d4ce284964fbe053fe3fbaf42835e2",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/graph_cache.py": "215c0f76b808ab24e01b1ba9250d911abd002a5a3ec49baaa10529e731cd30d3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/prove_bf16_master.py": "58c5f88e195d33f2aaa45700ad348ef399e7795ee25775f57cc965b087912c57",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/train.py": "7d05c4c6bd51f0ef91f06487b8f8af8dae3d07c11a2c7b0a48f7a120705030fc",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/cohort_precision_fixtures.py": "2f762bc7ad3f7a931b96f15b80eacfc4bce3446add4d0ba4b05e3578b463270b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/semantic_cache.py": "3bf896f01988ff073d3d3a6e6c56377e76f3680a39460899034aec07cce89d2b",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/static_pool.py": "bc2e3b4f37dc5c3bb0470a78762e1b6f8def04be3bb70dee2a488184cf487d73",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/kv_preflight.py": "dede205fbbcfba8ebea84d83011d3198b186377ea5b77ca77a4010d6efd44ad3",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/resident_combined.py": "4d82b02331918c80160f80f39bcda5a76c54c17838cd332d59523bf342d45802",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/tis_loss.py": "c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "loading",
  "started": 1791820024.3528714,
  "world_size": 8
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "passed",
  "exit_code": 0,
  "start": 1791819889.9302392,
  "end": 1791819946.4066446,
  "cpu_only": true,
  "source_unchanged": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/graph-composition-cpu-v2/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/graph-composition-cpu-v2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "passed",
  "exit_code": 0,
  "start": 1791816179.369102,
  "end": 1791816202.4933102,
  "cpu_only": true,
  "source_unchanged": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/launch-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "launcher_pid": 1720,
  "child_pids": [
    1722,
    1723,
    1724,
    1725,
    1726,
    1727,
    1728,
    1729
  ],
  "world": 8,
  "time": 1791801067.6509888,
  "source_hashes": {
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke-config.json": "0563944991761b458c6a2ba79fa413f4e870190a8ab887e2369a63968f3bf3e4",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._node_entry.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/node_entry.py": "976a61d1ccb75c937055241cca58c5a2dd39c8817272eb3b007db8c175287a91",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/decoder.py": "0c4ab5ed84b35e84c00023db96aff0f1b40cf50e436539dc5eb4b8f36925a259",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._batching.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._prepare_run.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/prepare_run.py": "c7cb20aada6cf1b49fbf729f152611a0127f99f2b2f80203f60cf623fe35df5d",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._structured_replay.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._microbatch_decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/microbatch_decoder.py": "ad7a7955bcc1a7be32d283bcde73c0568159078c8c913856ee05432b075f13ce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._baseline_decoder.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/baseline_decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._rollout.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/rollout.py": "ae30067f35957445d47cfb2e9f211cbcd08a3b09de0cf549ef07e2dc0b8b2f98",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._train.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/train.py": "0dd48916dd4f95ea92abc326276dc8717441dc87d68dbf1268a14794b1e23342",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._replay_guard.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/replay_guard.py": "d22d7b0a3f0c514d6e97a90a9b26e79562dd20cc937992bfdd86eb03a0e45f03",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._semantic_cache.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/semantic_cache.py": "1293f0889f06f3d70cfa46a2a8f82f5bdf8dd8a91fdc717045eb26d9c4429d76",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._proof_distributed_batch.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/proof_distributed_batch.py": "6a9e179ff343c7e84cc6a6a1d30529c76fd56abd3a0dad5e90f51eddc84c5fc0",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._reward.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/._gpu_ownership.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/gpu_ownership.py": "0e5928ce7e3a4625b436e4859e34b7855fea460e5db6c4f9a7422e246072cc75",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/source/._counted_loop.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/source/._parallel_structure.py": "5f5746684e6e76fed309a4e96e9462a56668463310a0dc5bbf2047ec004d150e",
    "work/experiments/rl-acceleration-20261012/lanes/kv_replay/src/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/report.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "inference_proof_passed_optimizer_held_for_benchmarks",
  "production_ready": false,
  "proof_gpu_model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "proof_cases": 87,
  "widths": [
    2,
    3,
    4,
    6,
    8
  ],
  "assembled_rounds_per_width": 4,
  "paired_action_logp_max": 3.528594970703125e-05,
  "replay_action_logp_max": 5.340576171875e-05,
  "peak_gpu_bytes": 21545335808,
  "synthetic_phase_baseline_seconds": 43.51694473903626,
  "synthetic_phase_candidate_seconds": 36.319375021383166,
  "synthetic_speedup": 1.1981743825001256,
  "physical_generation_forward_count_unchanged": true,
  "verified_decoder_sha256": "0c4ab5ed84b35e84c00023db96aff0f1b40cf50e436539dc5eb4b8f36925a259",
  "current_decoder_sha256": "e91eeec467ce905255bac71f89438f340409cee3952e59d1354a5f8cc9161d88",
  "mapping_only_optimization": "Hoist cached-index set construction out of token loop; CPU mapping equality verified for lengths 1, 100, and 16000.",
  "limits": [
    "Teacher-forced structured fixtures; actual clean16 sampled quality and mask parity remain pending.",
    "Full-vocabulary raw logits comparison remains pending; proof compares sampled-action normalized log-probabilities.",
    "Full 4B / 8 GPU resident Zero1 Adam, two positive updates, finite backbone gradient, step52-55 wall time, and clean GPU exits remain pending; user reassigned resources.",
    "Prefix KV bank must clear before changed model weights and between independent episodes; canonical execute clears at start and end.",
    "Persistent bank stores inference-only detached KV and must never be used for autograd replay.",
    "Index-set hoist preserves every model input, mask, position and cache mapping, but the current source hash still requires another GPU run for exact-source qualification."
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "loading",
  "started": 1791801191.120229,
  "world_size": 8
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 55,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/checkpoint-0055/hf",
  "initial_step": 50,
  "positive_updates": 5,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/baseline/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 55,
  "steps": 55
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 8,
    "id": "bigmath/cn_k12/23250",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 416,
    "reference_F": 521,
    "generation_seconds": 17.236048687249422,
    "T": 575,
    "native_replay_max": 0.0576171875,
    "native_replay_mean": 0.003133651101961732,
    "native_replay_p95": 0.01914614997804165,
    "phases": [
      {
        "phase": "main",
        "n": 163,
        "max": 0.0576171875,
        "mean": 0.00433748634532094,
        "p95": 0.026351921260356903
      },
      {
        "phase": "width",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "path",
        "n": 101,
        "max": 0.035991668701171875,
        "mean": 0.003307927865535021,
        "p95": 0.018095016479492188
      },
      {
        "phase": "path",
        "n": 77,
        "max": 0.019983291625976562,
        "mean": 0.0014125031884759665,
        "p95": 0.007154461927711964
      },
      {
        "phase": "path",
        "n": 82,
        "max": 0.04848670959472656,
        "mean": 0.002366601023823023,
        "p95": 0.012421786785125732
      },
      {
        "phase": "summary",
        "n": 102,
        "max": 0.0367889404296875,
        "mean": 0.0038602491840720177,
        "p95": 0.022365760058164597
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "main",
        "n": 46,
        "max": 0.0144500732421875,
        "mean": 0.0013946450781077147,
        "p95": 0.007374763488769531
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 9,
    "id": "bigmath/cn_k12/64731",
    "correct": false,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 815,
    "reference_F": 2172,
    "generation_seconds": 35.31101864203811,
    "T": 1457,
    "native_replay_max": 0.14973068237304688,
    "native_replay_mean": 0.0034266309812664986,
    "native_replay_p95": 0.01932486891746521,
    "phases": [
      {
        "phase": "main",
        "n": 154,
        "max": 0.08106613159179688,
        "mean": 0.004622756503522396,
        "p95": 0.029246777296066284
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.288818359375e-05,
        "mean": 1.1444091796875e-05,
        "p95": 2.174377368646674e-05
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.023885726928710938,
        "mean": 0.0015128962695598602,
        "p95": 0.009746935218572617
      },
      {
        "phase": "path",
        "n": 281,
        "max": 0.14973068237304688,
        "mean": 0.0031746698077768087,
        "p95": 0.015079498291015625
      },
      {
        "phase": "path",
        "n": 272,
        "max": 0.0492401123046875,
        "mean": 0.003435162827372551,
        "p95": 0.018424125388264656
      },
      {
        "phase": "path",
        "n": 220,
        "max": 0.09919548034667969,
        "mean": 0.005380647722631693,
        "p95": 0.028269290924072266
      },
      {
        "phase": "summary",
        "n": 205,
        "max": 0.07527732849121094,
        "mean": 0.003960697911679745,
        "p95": 0.02235603891313076
      },
      {
        "phase": "main",
        "n": 2,
        "max": 7.62939453125e-06,
        "mean": 3.814697265625e-06,
        "p95": 7.24792471373803e-06
      },
      {
        "phase": "main",
        "n": 171,
        "max": 0.05402183532714844,
        "mean": 0.0013543848181143403,
        "p95": 0.006237983703613281
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 10,
    "id": "bigmath/cn_k12/204933",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 552,
    "reference_F": 764,
    "generation_seconds": 22.808997777756304,
    "T": 985,
    "native_replay_max": 0.08598709106445312,
    "native_replay_mean": 0.0044342949986457825,
    "native_replay_p95": 0.023337554186582565,
    "phases": [
      {
        "phase": "main",
        "n": 146,
        "max": 0.06122016906738281,
        "mean": 0.006623627617955208,
        "p95": 0.031038284301757812
      },
      {
        "phase": "width",
        "n": 2,
        "max": 9.5367431640625e-06,
        "mean": 4.76837158203125e-06,
        "p95": 9.059906005859375e-06
      },
      {
        "phase": "path",
        "n": 105,
        "max": 0.042449951171875,
        "mean": 0.0024391720071434975,
        "p95": 0.010729976929724216
      },
      {
        "phase": "path",
        "n": 166,
        "max": 0.08598709106445312,
        "mean": 0.004133086651563644,
        "p95": 0.018130779266357422
      },
      {
        "phase": "path",
        "n": 162,
        "max": 0.04726409912109375,
        "mean": 0.004434308968484402,
        "p95": 0.023611729964613914
      },
      {
        "phase": "path",
        "n": 175,
        "max": 0.075653076171875,
        "mean": 0.0032415336463600397,
        "p95": 0.01787358522415161
      },
      {
        "phase": "summary",
        "n": 183,
        "max": 0.06459808349609375,
        "mean": 0.006168344523757696,
        "p95": 0.027385689318180084
      },
      {
        "phase": "main",
        "n": 2,
        "max": 2.47955322265625e-05,
        "mean": 1.239776611328125e-05,
        "p95": 2.3555754523840733e-05
      },
      {
        "phase": "main",
        "n": 44,
        "max": 0.012170791625976562,
        "mean": 0.0010013147257268429,
        "p95": 0.0057443613186478615
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 11,
    "id": "bigmath/cn_k12/147481",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 938,
    "reference_F": 1086,
    "generation_seconds": 39.15099321724847,
    "T": 1318,
    "native_replay_max": 0.09171867370605469,
    "native_replay_mean": 0.0036498773843050003,
    "native_replay_p95": 0.02119598723948002,
    "phases": [
      {
        "phase": "main",
        "n": 352,
        "max": 0.06771659851074219,
        "mean": 0.003940725699067116,
        "p95": 0.022432418540120125
      },
      {
        "phase": "width",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "path",
        "n": 100,
        "max": 0.022487640380859375,
        "mean": 0.0016122626839205623,
        "p95": 0.008962130174040794
      },
      {
        "phase": "path",
        "n": 118,
        "max": 0.04262351989746094,
        "mean": 0.002698267810046673,
        "p95": 0.015267564915120602
      },
      {
        "phase": "path",
        "n": 355,
        "max": 0.06416130065917969,
        "mean": 0.0037890688981860876,
        "p95": 0.020588869228959084
      },
      {
        "phase": "path",
        "n": 162,
        "max": 0.03827476501464844,
        "mean": 0.002303582616150379,
        "p95": 0.013035958632826805
      },
      {
        "phase": "summary",
        "n": 111,
        "max": 0.09171867370605469,
        "mean": 0.008291210047900677,
        "p95": 0.0449066162109375
      },
      {
        "phase": "main",
        "n": 44,
        "max": 0.04541015625,
        "mean": 0.0038126164581626654,
        "p95": 0.015369795262813568
      },
      {
        "phase": "main",
        "n": 74,
        "max": 0.022016525268554688,
        "mean": 0.001856778166256845,
        "p95": 0.013189309276640415
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 12,
    "id": "bigmath/cn_k12/61311",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1141,
    "reference_F": 952,
    "generation_seconds": 46.510242386721075,
    "T": 1609,
    "native_replay_max": 0.09227180480957031,
    "native_replay_mean": 0.003177373670041561,
    "native_replay_p95": 0.019794456660747528,
    "phases": [
      {
        "phase": "main",
        "n": 173,
        "max": 0.09227180480957031,
        "mean": 0.005313200876116753,
        "p95": 0.02857627160847187
      },
      {
        "phase": "width",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "path",
        "n": 144,
        "max": 0.04068183898925781,
        "mean": 0.003305620513856411,
        "p95": 0.02190827764570713
      },
      {
        "phase": "path",
        "n": 118,
        "max": 0.03413581848144531,
        "mean": 0.002916691591963172,
        "p95": 0.02032642439007759
      },
      {
        "phase": "path",
        "n": 359,
        "max": 0.05139923095703125,
        "mean": 0.002330891555175185,
        "p95": 0.01516285166144371
      },
      {
        "phase": "path",
        "n": 206,
        "max": 0.05180931091308594,
        "mean": 0.0026314235292375088,
        "p95": 0.018874168395996094
      },
      {
        "phase": "summary",
        "n": 498,
        "max": 0.08386993408203125,
        "mean": 0.003112270263954997,
        "p95": 0.017746444791555405
      },
      {
        "phase": "main",
        "n": 2,
        "max": 2.86102294921875e-05,
        "mean": 1.52587890625e-05,
        "p95": 2.727508581301663e-05
      },
      {
        "phase": "main",
        "n": 107,
        "max": 0.06169700622558594,
        "mean": 0.00415162043645978,
        "p95": 0.022982213646173477
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 13,
    "id": "bigmath/cn_k12/155313",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 424,
    "reference_F": 921,
    "generation_seconds": 16.88454056624323,
    "T": 501,
    "native_replay_max": 0.10188102722167969,
    "native_replay_mean": 0.004661521874368191,
    "native_replay_p95": 0.019987106323242188,
    "phases": [
      {
        "phase": "main",
        "n": 208,
        "max": 0.10188102722167969,
        "mean": 0.005232765339314938,
        "p95": 0.023231392726302147
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "path",
        "n": 95,
        "max": 0.06205940246582031,
        "mean": 0.004362266976386309,
        "p95": 0.01854781247675419
      },
      {
        "phase": "path",
        "n": 77,
        "max": 0.05381011962890625,
        "mean": 0.006861153990030289,
        "p95": 0.03099970892071724
      },
      {
        "phase": "summary",
        "n": 65,
        "max": 0.021638870239257812,
        "mean": 0.0033569629304111004,
        "p95": 0.013341140002012253
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "main",
        "n": 52,
        "max": 0.012929916381835938,
        "mean": 0.0016551017761230469,
        "p95": 0.008815385401248932
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 14,
    "id": "bigmath/cn_k12/95257",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 816,
    "reference_F": 1763,
    "generation_seconds": 33.34378248406574,
    "T": 1219,
    "native_replay_max": 0.27329444885253906,
    "native_replay_mean": 0.0034212006721645594,
    "native_replay_p95": 0.018128395080566406,
    "phases": [
      {
        "phase": "main",
        "n": 226,
        "max": 0.05263328552246094,
        "mean": 0.0038318170700222254,
        "p95": 0.020656108856201172
      },
      {
        "phase": "width",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "path",
        "n": 137,
        "max": 0.07705307006835938,
        "mean": 0.0016899944748729467,
        "p95": 0.008623119443655014
      },
      {
        "phase": "path",
        "n": 110,
        "max": 0.27329444885253906,
        "mean": 0.004697921220213175,
        "p95": 0.00997580774128437
      },
      {
        "phase": "path",
        "n": 156,
        "max": 0.09527969360351562,
        "mean": 0.002228211145848036,
        "p95": 0.013582229614257812
      },
      {
        "phase": "path",
        "n": 201,
        "max": 0.17448043823242188,
        "mean": 0.0032838659826666117,
        "p95": 0.018154144287109375
      },
      {
        "phase": "summary",
        "n": 319,
        "max": 0.09129524230957031,
        "mean": 0.004067800473421812,
        "p95": 0.02522679790854454
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "main",
        "n": 66,
        "max": 0.035678863525390625,
        "mean": 0.0038007679395377636,
        "p95": 0.02052927017211914
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 15,
    "id": "bigmath/cn_k12/3177",
    "correct": false,
    "reference_correct": false,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 614,
    "reference_F": 724,
    "generation_seconds": 24.403585652820766,
    "T": 946,
    "native_replay_max": 0.07379341125488281,
    "native_replay_mean": 0.0029406496323645115,
    "native_replay_p95": 0.016543865203857422,
    "phases": [
      {
        "phase": "main",
        "n": 160,
        "max": 0.030893325805664062,
        "mean": 0.00275249476544559,
        "p95": 0.013870056718587875
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "path",
        "n": 108,
        "max": 0.047138214111328125,
        "mean": 0.003246024716645479,
        "p95": 0.014872455969452858
      },
      {
        "phase": "path",
        "n": 74,
        "max": 0.06862449645996094,
        "mean": 0.004384247120469809,
        "p95": 0.018011659383773804
      },
      {
        "phase": "path",
        "n": 233,
        "max": 0.050083160400390625,
        "mean": 0.0020791245624423027,
        "p95": 0.01468200609087944
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.028963088989257812,
        "mean": 0.001980438129976392,
        "p95": 0.010766602121293545
      },
      {
        "phase": "summary",
        "n": 160,
        "max": 0.07379341125488281,
        "mean": 0.004574596881866455,
        "p95": 0.022505681961774826
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "main",
        "n": 57,
        "max": 0.02205657958984375,
        "mean": 0.002684409264475107,
        "p95": 0.013339618220925331
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 0,
      "id": "bigmath/cn_k12/26444",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 539,
      "reference_F": 752,
      "generation_seconds": 23.843221546150744,
      "T": 865,
      "native_replay_max": 0.07457733154296875,
      "native_replay_mean": 0.001860167714767158,
      "native_replay_p95": 0.010924139991402626,
      "phases": [
        {
          "phase": "main",
          "n": 169,
          "max": 0.03426361083984375,
          "mean": 0.0018758605001494288,
          "p95": 0.00977096427232027
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 95,
          "max": 0.019336700439453125,
          "mean": 0.0007552498136647046,
          "p95": 0.004160114098340273
        },
        {
          "phase": "path",
          "n": 74,
          "max": 0.015773773193359375,
          "mean": 0.0008743131766095757,
          "p95": 0.005155275110155344
        },
        {
          "phase": "path",
          "n": 157,
          "max": 0.07457733154296875,
          "mean": 0.0026103341951966286,
          "p95": 0.014584729447960854
        },
        {
          "phase": "path",
          "n": 261,
          "max": 0.05927848815917969,
          "mean": 0.0021528631914407015,
          "p95": 0.015148162841796875
        },
        {
          "phase": "summary",
          "n": 66,
          "max": 0.027820587158203125,
          "mean": 0.0021704472601413727,
          "p95": 0.01214742660522461
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 39,
          "max": 0.008024215698242188,
          "mean": 0.0010408255038782954,
          "p95": 0.007528685964643955
        }
      ]
    },
    {
      "index": 8,
      "id": "bigmath/cn_k12/23250",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 416,
      "reference_F": 521,
      "generation_seconds": 17.236048687249422,
      "T": 575,
      "native_replay_max": 0.0576171875,
      "native_replay_mean": 0.003133651101961732,
      "native_replay_p95": 0.01914614997804165,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.0576171875,
          "mean": 0.00433748634532094,
          "p95": 0.026351921260356903
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 101,
          "max": 0.035991668701171875,
          "mean": 0.003307927865535021,
          "p95": 0.018095016479492188
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.019983291625976562,
          "mean": 0.0014125031884759665,
          "p95": 0.007154461927711964
        },
        {
          "phase": "path",
          "n": 82,
          "max": 0.04848670959472656,
          "mean": 0.002366601023823023,
          "p95": 0.012421786785125732
        },
        {
          "phase": "summary",
          "n": 102,
          "max": 0.0367889404296875,
          "mean": 0.0038602491840720177,
          "p95": 0.022365760058164597
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "main",
          "n": 46,
          "max": 0.0144500732421875,
          "mean": 0.0013946450781077147,
          "p95": 0.007374763488769531
        }
      ]
    }
  ],
  "actions": 1440,
  "native_replay_max": 0.07457733154296875,
  "native_replay_mean": 0.002368676709011197,
  "native_replay_p95": 0.014452263712882996,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24437112832,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 1,
      "id": "bigmath/cn_k12/88253",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 938,
      "reference_F": 1344,
      "generation_seconds": 38.17746828915551,
      "T": 1000,
      "native_replay_max": 0.07848548889160156,
      "native_replay_mean": 0.0032145539298653603,
      "native_replay_p95": 0.016892526298761368,
      "phases": [
        {
          "phase": "main",
          "n": 131,
          "max": 0.04817008972167969,
          "mean": 0.003523178631439805,
          "p95": 0.015465736389160156
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "path",
          "n": 62,
          "max": 0.02455902099609375,
          "mean": 0.0015252329176291823,
          "p95": 0.008685399778187275
        },
        {
          "phase": "path",
          "n": 177,
          "max": 0.07848548889160156,
          "mean": 0.0034823876339942217,
          "p95": 0.0191753301769495
        },
        {
          "phase": "summary",
          "n": 548,
          "max": 0.061824798583984375,
          "mean": 0.003390601137652993,
          "p95": 0.017456337809562683
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 78,
          "max": 0.03542900085449219,
          "mean": 0.0023592435754835606,
          "p95": 0.015332127921283245
        }
      ]
    },
    {
      "index": 9,
      "id": "bigmath/cn_k12/64731",
      "correct": false,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 815,
      "reference_F": 2172,
      "generation_seconds": 35.31101864203811,
      "T": 1457,
      "native_replay_max": 0.14973068237304688,
      "native_replay_mean": 0.0034266309812664986,
      "native_replay_p95": 0.01932486891746521,
      "phases": [
        {
          "phase": "main",
          "n": 154,
          "max": 0.08106613159179688,
          "mean": 0.004622756503522396,
          "p95": 0.029246777296066284
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.288818359375e-05,
          "mean": 1.1444091796875e-05,
          "p95": 2.174377368646674e-05
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.023885726928710938,
          "mean": 0.0015128962695598602,
          "p95": 0.009746935218572617
        },
        {
          "phase": "path",
          "n": 281,
          "max": 0.14973068237304688,
          "mean": 0.0031746698077768087,
          "p95": 0.015079498291015625
        },
        {
          "phase": "path",
          "n": 272,
          "max": 0.0492401123046875,
          "mean": 0.003435162827372551,
          "p95": 0.018424125388264656
        },
        {
          "phase": "path",
          "n": 220,
          "max": 0.09919548034667969,
          "mean": 0.005380647722631693,
          "p95": 0.028269290924072266
        },
        {
          "phase": "summary",
          "n": 205,
          "max": 0.07527732849121094,
          "mean": 0.003960697911679745,
          "p95": 0.02235603891313076
        },
        {
          "phase": "main",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "main",
          "n": 171,
          "max": 0.05402183532714844,
          "mean": 0.0013543848181143403,
          "p95": 0.006237983703613281
        }
      ]
    }
  ],
  "actions": 2457,
  "native_replay_max": 0.14973068237304688,
  "native_replay_mean": 0.0033403155393898487,
  "native_replay_p95": 0.018367374315857887,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24548494336,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 2,
      "id": "bigmath/cn_k12/163846",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 538,
      "reference_F": 463,
      "generation_seconds": 23.81835557287559,
      "T": 724,
      "native_replay_max": 0.20364952087402344,
      "native_replay_mean": 0.0051729995757341385,
      "native_replay_p95": 0.02821779064834118,
      "phases": [
        {
          "phase": "main",
          "n": 116,
          "max": 0.0476837158203125,
          "mean": 0.003648963524028659,
          "p95": 0.024951457977294922
        },
        {
          "phase": "width",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "path",
          "n": 23,
          "max": 0.04550743103027344,
          "mean": 0.006636661011725664,
          "p95": 0.028550907969474792
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.06597518920898438,
          "mean": 0.005290861241519451,
          "p95": 0.026190942153334618
        },
        {
          "phase": "path",
          "n": 195,
          "max": 0.06194877624511719,
          "mean": 0.004565278068184853,
          "p95": 0.02210083417594433
        },
        {
          "phase": "path",
          "n": 86,
          "max": 0.0625762939453125,
          "mean": 0.004837867803871632,
          "p95": 0.03107595443725586
        },
        {
          "phase": "summary",
          "n": 158,
          "max": 0.20364952087402344,
          "mean": 0.008565299212932587,
          "p95": 0.043215442448854446
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 65,
          "max": 0.019407272338867188,
          "mean": 0.0015741788083687425,
          "p95": 0.010668562725186348
        }
      ]
    },
    {
      "index": 10,
      "id": "bigmath/cn_k12/204933",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 552,
      "reference_F": 764,
      "generation_seconds": 22.808997777756304,
      "T": 985,
      "native_replay_max": 0.08598709106445312,
      "native_replay_mean": 0.0044342949986457825,
      "native_replay_p95": 0.023337554186582565,
      "phases": [
        {
          "phase": "main",
          "n": 146,
          "max": 0.06122016906738281,
          "mean": 0.006623627617955208,
          "p95": 0.031038284301757812
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.5367431640625e-06,
          "mean": 4.76837158203125e-06,
          "p95": 9.059906005859375e-06
        },
        {
          "phase": "path",
          "n": 105,
          "max": 0.042449951171875,
          "mean": 0.0024391720071434975,
          "p95": 0.010729976929724216
        },
        {
          "phase": "path",
          "n": 166,
          "max": 0.08598709106445312,
          "mean": 0.004133086651563644,
          "p95": 0.018130779266357422
        },
        {
          "phase": "path",
          "n": 162,
          "max": 0.04726409912109375,
          "mean": 0.004434308968484402,
          "p95": 0.023611729964613914
        },
        {
          "phase": "path",
          "n": 175,
          "max": 0.075653076171875,
          "mean": 0.0032415336463600397,
          "p95": 0.01787358522415161
        },
        {
          "phase": "summary",
          "n": 183,
          "max": 0.06459808349609375,
          "mean": 0.006168344523757696,
          "p95": 0.027385689318180084
        },
        {
          "phase": "main",
          "n": 2,
          "max": 2.47955322265625e-05,
          "mean": 1.239776611328125e-05,
          "p95": 2.3555754523840733e-05
        },
        {
          "phase": "main",
          "n": 44,
          "max": 0.012170791625976562,
          "mean": 0.0010013147257268429,
          "p95": 0.0057443613186478615
        }
      ]
    }
  ],
  "actions": 1709,
  "native_replay_max": 0.20364952087402344,
  "native_replay_mean": 0.0047472394071519375,
  "native_replay_p95": 0.025078177452087402,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24311777280,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 3,
      "id": "bigmath/cn_k12/210293",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 394,
      "reference_F": 710,
      "generation_seconds": 17.36548827541992,
      "T": 461,
      "native_replay_max": 0.07797431945800781,
      "native_replay_mean": 0.003993146121501923,
      "native_replay_p95": 0.021001815795898438,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.05597686767578125,
          "mean": 0.004091005306690931,
          "p95": 0.020653704181313515
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 83,
          "max": 0.021869659423828125,
          "mean": 0.002296723425388336,
          "p95": 0.013124467805027962
        },
        {
          "phase": "path",
          "n": 67,
          "max": 0.07797431945800781,
          "mean": 0.004467494320124388,
          "p95": 0.021504784002900124
        },
        {
          "phase": "summary",
          "n": 72,
          "max": 0.056789398193359375,
          "mean": 0.004945688880980015,
          "p95": 0.02277267351746559
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 72,
          "max": 0.07241439819335938,
          "mean": 0.004555013496428728,
          "p95": 0.02245289646089077
        }
      ]
    },
    {
      "index": 11,
      "id": "bigmath/cn_k12/147481",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 938,
      "reference_F": 1086,
      "generation_seconds": 39.15099321724847,
      "T": 1318,
      "native_replay_max": 0.09171867370605469,
      "native_replay_mean": 0.0036498773843050003,
      "native_replay_p95": 0.02119598723948002,
      "phases": [
        {
          "phase": "main",
          "n": 352,
          "max": 0.06771659851074219,
          "mean": 0.003940725699067116,
          "p95": 0.022432418540120125
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "path",
          "n": 100,
          "max": 0.022487640380859375,
          "mean": 0.0016122626839205623,
          "p95": 0.008962130174040794
        },
        {
          "phase": "path",
          "n": 118,
          "max": 0.04262351989746094,
          "mean": 0.002698267810046673,
          "p95": 0.015267564915120602
        },
        {
          "phase": "path",
          "n": 355,
          "max": 0.06416130065917969,
          "mean": 0.0037890688981860876,
          "p95": 0.020588869228959084
        },
        {
          "phase": "path",
          "n": 162,
          "max": 0.03827476501464844,
          "mean": 0.002303582616150379,
          "p95": 0.013035958632826805
        },
        {
          "phase": "summary",
          "n": 111,
          "max": 0.09171867370605469,
          "mean": 0.008291210047900677,
          "p95": 0.0449066162109375
        },
        {
          "phase": "main",
          "n": 44,
          "max": 0.04541015625,
          "mean": 0.0038126164581626654,
          "p95": 0.015369795262813568
        },
        {
          "phase": "main",
          "n": 74,
          "max": 0.022016525268554688,
          "mean": 0.001856778166256845,
          "p95": 0.013189309276640415
        }
      ]
    }
  ],
  "actions": 1779,
  "native_replay_max": 0.09171867370605469,
  "native_replay_mean": 0.0037388300988823175,
  "native_replay_p95": 0.021129034459590912,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24739811328,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 4,
      "id": "bigmath/cn_k12/88674",
      "correct": true,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 442,
      "reference_F": 2255,
      "generation_seconds": 18.758081004954875,
      "T": 589,
      "native_replay_max": 0.053984642028808594,
      "native_replay_mean": 0.0055548097006976604,
      "native_replay_p95": 0.02217063680291176,
      "phases": [
        {
          "phase": "main",
          "n": 116,
          "max": 0.0503387451171875,
          "mean": 0.00578418280929327,
          "p95": 0.022203922271728516
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "path",
          "n": 91,
          "max": 0.03624916076660156,
          "mean": 0.00520535372197628,
          "p95": 0.021866798400878906
        },
        {
          "phase": "path",
          "n": 61,
          "max": 0.041351318359375,
          "mean": 0.0059792096726596355,
          "p95": 0.02170562744140625
        },
        {
          "phase": "path",
          "n": 86,
          "max": 0.0294952392578125,
          "mean": 0.003993810620158911,
          "p95": 0.016202926635742188
        },
        {
          "phase": "summary",
          "n": 109,
          "max": 0.053984642028808594,
          "mean": 0.007699056528508663,
          "p95": 0.027105141431093216
        },
        {
          "phase": "main",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "main",
          "n": 122,
          "max": 0.05044364929199219,
          "mean": 0.004751838743686676,
          "p95": 0.01823701709508896
        }
      ]
    },
    {
      "index": 12,
      "id": "bigmath/cn_k12/61311",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1141,
      "reference_F": 952,
      "generation_seconds": 46.510242386721075,
      "T": 1609,
      "native_replay_max": 0.09227180480957031,
      "native_replay_mean": 0.003177373670041561,
      "native_replay_p95": 0.019794456660747528,
      "phases": [
        {
          "phase": "main",
          "n": 173,
          "max": 0.09227180480957031,
          "mean": 0.005313200876116753,
          "p95": 0.02857627160847187
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 144,
          "max": 0.04068183898925781,
          "mean": 0.003305620513856411,
          "p95": 0.02190827764570713
        },
        {
          "phase": "path",
          "n": 118,
          "max": 0.03413581848144531,
          "mean": 0.002916691591963172,
          "p95": 0.02032642439007759
        },
        {
          "phase": "path",
          "n": 359,
          "max": 0.05139923095703125,
          "mean": 0.002330891555175185,
          "p95": 0.01516285166144371
        },
        {
          "phase": "path",
          "n": 206,
          "max": 0.05180931091308594,
          "mean": 0.0026314235292375088,
          "p95": 0.018874168395996094
        },
        {
          "phase": "summary",
          "n": 498,
          "max": 0.08386993408203125,
          "mean": 0.003112270263954997,
          "p95": 0.017746444791555405
        },
        {
          "phase": "main",
          "n": 2,
          "max": 2.86102294921875e-05,
          "mean": 1.52587890625e-05,
          "p95": 2.727508581301663e-05
        },
        {
          "phase": "main",
          "n": 107,
          "max": 0.06169700622558594,
          "mean": 0.00415162043645978,
          "p95": 0.022982213646173477
        }
      ]
    }
  ],
  "actions": 2198,
  "native_replay_max": 0.09227180480957031,
  "native_replay_mean": 0.003814457217231393,
  "native_replay_p95": 0.02111547812819481,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24663757824,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 5,
      "id": "bigmath/cn_k12/165159",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 347,
      "reference_F": 540,
      "generation_seconds": 14.864217762835324,
      "T": 480,
      "native_replay_max": 0.0827789306640625,
      "native_replay_mean": 0.004245440009981394,
      "native_replay_p95": 0.02113313227891922,
      "phases": [
        {
          "phase": "main",
          "n": 161,
          "max": 0.05822563171386719,
          "mean": 0.0035207998007535934,
          "p95": 0.01682281494140625
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 55,
          "max": 0.054874420166015625,
          "mean": 0.009524727240204811,
          "p95": 0.04074067994952202
        },
        {
          "phase": "path",
          "n": 46,
          "max": 0.07965087890625,
          "mean": 0.004448559135198593,
          "p95": 0.01409006118774414
        },
        {
          "phase": "path",
          "n": 66,
          "max": 0.0827789306640625,
          "mean": 0.005273500923067331,
          "p95": 0.021369457244873047
        },
        {
          "phase": "path",
          "n": 32,
          "max": 0.021795272827148438,
          "mean": 0.002562403678894043,
          "p95": 0.011158941313624382
        },
        {
          "phase": "summary",
          "n": 62,
          "max": 0.029399871826171875,
          "mean": 0.0024844908621162176,
          "p95": 0.014225962571799755
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0030155181884765625,
          "mean": 0.0015077590942382812,
          "p95": 0.002864742185920477
        },
        {
          "phase": "main",
          "n": 54,
          "max": 0.030298233032226562,
          "mean": 0.0028770940843969584,
          "p95": 0.015365500003099442
        }
      ]
    },
    {
      "index": 13,
      "id": "bigmath/cn_k12/155313",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 424,
      "reference_F": 921,
      "generation_seconds": 16.88454056624323,
      "T": 501,
      "native_replay_max": 0.10188102722167969,
      "native_replay_mean": 0.004661521874368191,
      "native_replay_p95": 0.019987106323242188,
      "phases": [
        {
          "phase": "main",
          "n": 208,
          "max": 0.10188102722167969,
          "mean": 0.005232765339314938,
          "p95": 0.023231392726302147
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 95,
          "max": 0.06205940246582031,
          "mean": 0.004362266976386309,
          "p95": 0.01854781247675419
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.05381011962890625,
          "mean": 0.006861153990030289,
          "p95": 0.03099970892071724
        },
        {
          "phase": "summary",
          "n": 65,
          "max": 0.021638870239257812,
          "mean": 0.0033569629304111004,
          "p95": 0.013341140002012253
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "main",
          "n": 52,
          "max": 0.012929916381835938,
          "mean": 0.0016551017761230469,
          "p95": 0.008815385401248932
        }
      ]
    }
  ],
  "actions": 981,
  "native_replay_max": 0.10188102722167969,
  "native_replay_mean": 0.004457934759557247,
  "native_replay_p95": 0.0206756591796875,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24316192768,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 6,
      "id": "bigmath/cn_k12/176142",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 428,
      "reference_F": 710,
      "generation_seconds": 18.92057308368385,
      "T": 641,
      "native_replay_max": 0.05908775329589844,
      "native_replay_mean": 0.003463760018348694,
      "native_replay_p95": 0.019021987915039062,
      "phases": [
        {
          "phase": "main",
          "n": 157,
          "max": 0.033016204833984375,
          "mean": 0.0027080948930233717,
          "p95": 0.012261573225259781
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 114,
          "max": 0.05338287353515625,
          "mean": 0.002504649804905057,
          "p95": 0.010924147441983223
        },
        {
          "phase": "path",
          "n": 62,
          "max": 0.00728607177734375,
          "mean": 0.0010062494548037648,
          "p95": 0.005420781206339598
        },
        {
          "phase": "path",
          "n": 91,
          "max": 0.028203964233398438,
          "mean": 0.002802356146275997,
          "p95": 0.015284538269042969
        },
        {
          "phase": "path",
          "n": 60,
          "max": 0.04788398742675781,
          "mean": 0.0051064807921648026,
          "p95": 0.022575564682483673
        },
        {
          "phase": "summary",
          "n": 100,
          "max": 0.05908775329589844,
          "mean": 0.006108779925853014,
          "p95": 0.03596801683306694
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.00011444091796875,
          "mean": 5.7220458984375e-05,
          "p95": 0.0001087188720703125
        },
        {
          "phase": "main",
          "n": 53,
          "max": 0.03706550598144531,
          "mean": 0.005184245761483908,
          "p95": 0.029268642887473106
        }
      ]
    },
    {
      "index": 14,
      "id": "bigmath/cn_k12/95257",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 816,
      "reference_F": 1763,
      "generation_seconds": 33.34378248406574,
      "T": 1219,
      "native_replay_max": 0.27329444885253906,
      "native_replay_mean": 0.0034212006721645594,
      "native_replay_p95": 0.018128395080566406,
      "phases": [
        {
          "phase": "main",
          "n": 226,
          "max": 0.05263328552246094,
          "mean": 0.0038318170700222254,
          "p95": 0.020656108856201172
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 137,
          "max": 0.07705307006835938,
          "mean": 0.0016899944748729467,
          "p95": 0.008623119443655014
        },
        {
          "phase": "path",
          "n": 110,
          "max": 0.27329444885253906,
          "mean": 0.004697921220213175,
          "p95": 0.00997580774128437
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.09527969360351562,
          "mean": 0.002228211145848036,
          "p95": 0.013582229614257812
        },
        {
          "phase": "path",
          "n": 201,
          "max": 0.17448043823242188,
          "mean": 0.0032838659826666117,
          "p95": 0.018154144287109375
        },
        {
          "phase": "summary",
          "n": 319,
          "max": 0.09129524230957031,
          "mean": 0.004067800473421812,
          "p95": 0.02522679790854454
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "main",
          "n": 66,
          "max": 0.035678863525390625,
          "mean": 0.0038007679395377636,
          "p95": 0.02052927017211914
        }
      ]
    }
  ],
  "actions": 1860,
  "native_replay_max": 0.27329444885253906,
  "native_replay_mean": 0.0034358676057308912,
  "native_replay_p95": 0.018485449254512787,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24473731584,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-attention-native/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "precision": "bf16_autocast_fp32_attention_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "attention_forced_fp32": true,
  "cases": [
    {
      "index": 7,
      "id": "bigmath/cn_k12/60327",
      "correct": false,
      "reference_correct": true,
      "format_valid": false,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1873,
      "reference_F": 1069,
      "generation_seconds": 73.10654664365575,
      "T": 1946,
      "native_replay_max": 0.23046493530273438,
      "native_replay_mean": 0.004698628559708595,
      "native_replay_p95": 0.023529052734375,
      "phases": [
        {
          "phase": "main",
          "n": 95,
          "max": 0.03814125061035156,
          "mean": 0.004296754486858845,
          "p95": 0.01889970898628235
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 73,
          "max": 0.039325714111328125,
          "mean": 0.0026811312418431044,
          "p95": 0.012982564978301525
        },
        {
          "phase": "path",
          "n": 116,
          "max": 0.0382537841796875,
          "mean": 0.0034029565285891294,
          "p95": 0.022692203521728516
        },
        {
          "phase": "summary",
          "n": 167,
          "max": 0.23046493530273438,
          "mean": 0.006214906927198172,
          "p95": 0.0288722924888134
        },
        {
          "phase": "main",
          "n": 1269,
          "max": 0.10161972045898438,
          "mean": 0.005090620368719101,
          "p95": 0.02423209138214588
        },
        {
          "phase": "main",
          "n": 224,
          "max": 0.06381797790527344,
          "mean": 0.002888283459469676,
          "p95": 0.014300239272415638
        }
      ]
    },
    {
      "index": 15,
      "id": "bigmath/cn_k12/3177",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 614,
      "reference_F": 724,
      "generation_seconds": 24.403585652820766,
      "T": 946,
      "native_replay_max": 0.07379341125488281,
      "native_replay_mean": 0.0029406496323645115,
      "native_replay_p95": 0.016543865203857422,
      "phases": [
        {
          "phase": "main",
          "n": 160,
          "max": 0.030893325805664062,
          "mean": 0.00275249476544559,
          "p95": 0.013870056718587875
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "path",
          "n": 108,
          "max": 0.047138214111328125,
          "mean": 0.003246024716645479,
          "p95": 0.014872455969452858
        },
        {
          "phase": "path",
          "n": 74,
          "max": 0.06862449645996094,
          "mean": 0.004384247120469809,
          "p95": 0.018011659383773804
        },
        {
          "phase": "path",
          "n": 233,
          "max": 0.050083160400390625,
          "mean": 0.0020791245624423027,
          "p95": 0.01468200609087944
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.028963088989257812,
          "mean": 0.001980438129976392,
          "p95": 0.010766602121293545
        },
        {
          "phase": "summary",
          "n": 160,
          "max": 0.07379341125488281,
          "mean": 0.004574596881866455,
          "p95": 0.022505681961774826
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 57,
          "max": 0.02205657958984375,
          "mean": 0.002684409264475107,
          "p95": 0.013339618220925331
        }
      ]
    }
  ],
  "actions": 2892,
  "native_replay_max": 0.23046493530273438,
  "native_replay_mean": 0.004123577382415533,
  "native_replay_p95": 0.02149122580885887,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 0,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25882758144,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/readiness.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/portable-configs/readiness.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "fixed_batch": "8prompts×4=32responses",
  "denominator": 4096,
  "worlds": [
    {
      "world": 1,
      "local_responses": [
        32
      ],
      "ddp_scale": 0.03125,
      "cpu_math_pass": true,
      "gpu_qualified": false,
      "multinode_required": false
    },
    {
      "world": 2,
      "local_responses": [
        16,
        16
      ],
      "ddp_scale": 0.0625,
      "cpu_math_pass": true,
      "gpu_qualified": false,
      "multinode_required": false
    },
    {
      "world": 4,
      "local_responses": [
        8,
        8,
        8,
        8
      ],
      "ddp_scale": 0.125,
      "cpu_math_pass": true,
      "gpu_qualified": false,
      "multinode_required": false
    },
    {
      "world": 8,
      "local_responses": [
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4
      ],
      "ddp_scale": 0.25,
      "cpu_math_pass": true,
      "gpu_qualified": true,
      "multinode_required": false
    },
    {
      "world": 24,
      "local_responses": [
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1,
        2,
        1,
        1
      ],
      "ddp_scale": 0.75,
      "cpu_math_pass": true,
      "gpu_qualified": false,
      "multinode_required": true
    },
    {
      "world": 32,
      "local_responses": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "ddp_scale": 1.0,
      "cpu_math_pass": true,
      "gpu_qualified": false,
      "multinode_required": true
    }
  ],
  "warning": "Only8GPU actual memory/Adam/throughput validated.1/2/4/24/32 templates are CPU math readiness only;1GPU FP32Adam plus shadows/KV may exceed80GB. Existing launcher is node-local8 only. Root must provide explicit distributed launch for24/32; no launch is performed."
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 53,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/checkpoint-0053/hf",
  "initial_step": 50,
  "positive_updates": 3,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 53,
  "steps": 53
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/validation-0053/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-learner-graph/attempt2/training/validation-0053/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 53,
  "completed": 16,
  "correct": 13,
  "format_valid": 14,
  "parallel_valid": 14,
  "fork_tasks": 16,
  "widths": [
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    5,
    4,
    4,
    4
  ],
  "actual_rounds": 16,
  "logical_depth": [
    717,
    498,
    1842,
    1302,
    529,
    725,
    710,
    1537,
    1967,
    873,
    634,
    749,
    725,
    1907,
    2455,
    725
  ],
  "sampled_tokens": [
    1123,
    890,
    2175,
    1958,
    723,
    1350,
    1141,
    2411,
    2452,
    1567,
    921,
    1155,
    1445,
    2708,
    2763,
    1216
  ],
  "actual_forward_calls": [
    717,
    498,
    1842,
    1302,
    529,
    725,
    710,
    1537,
    1967,
    873,
    634,
    749,
    725,
    1907,
    2455,
    725
  ],
  "sampler": "FP32 learner HF fullwidth8, temperature1 top_p1 nofilter; fixed clean16 validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 8,
    "id": "bigmath/cn_k12/23250",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 416,
    "reference_F": 521,
    "generation_seconds": 18.702754213940352,
    "T": 575,
    "native_replay_max": 0.05078411102294922,
    "native_replay_mean": 0.003383548464626074,
    "native_replay_p95": 0.018609045073390007,
    "phases": [
      {
        "phase": "main",
        "n": 163,
        "max": 0.05078411102294922,
        "mean": 0.004470690619200468,
        "p95": 0.030411895364522934
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.33514404296875e-05,
        "mean": 6.67572021484375e-06,
        "p95": 1.2683868590102065e-05
      },
      {
        "phase": "path",
        "n": 101,
        "max": 0.04351234436035156,
        "mean": 0.002944172127172351,
        "p95": 0.01305389404296875
      },
      {
        "phase": "path",
        "n": 77,
        "max": 0.049129486083984375,
        "mean": 0.002521093701943755,
        "p95": 0.013315555639564991
      },
      {
        "phase": "path",
        "n": 82,
        "max": 0.043704986572265625,
        "mean": 0.002374672330915928,
        "p95": 0.008527849800884724
      },
      {
        "phase": "summary",
        "n": 102,
        "max": 0.03363609313964844,
        "mean": 0.004300098866224289,
        "p95": 0.025324903428554535
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 46,
        "max": 0.017704010009765625,
        "mean": 0.0019996478222310543,
        "p95": 0.013004779815673828
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 9,
    "id": "bigmath/cn_k12/64731",
    "correct": false,
    "reference_correct": true,
    "format_valid": false,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1018,
    "reference_F": 2172,
    "generation_seconds": 40.6976250926964,
    "T": 1405,
    "native_replay_max": 0.11976051330566406,
    "native_replay_mean": 0.0031565052922815084,
    "native_replay_p95": 0.017027273774147034,
    "phases": [
      {
        "phase": "main",
        "n": 155,
        "max": 0.06254768371582031,
        "mean": 0.0051407720893621445,
        "p95": 0.027034761384129524
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.09808349609375e-05,
        "mean": 1.049041748046875e-05,
        "p95": 1.9931792849092744e-05
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.03357887268066406,
        "mean": 0.0014412307646125555,
        "p95": 0.0075296442955732346
      },
      {
        "phase": "path",
        "n": 316,
        "max": 0.0385589599609375,
        "mean": 0.0013943503145128489,
        "p95": 0.008848190307617188
      },
      {
        "phase": "path",
        "n": 102,
        "max": 0.11976051330566406,
        "mean": 0.005517567042261362,
        "p95": 0.023088829591870308
      },
      {
        "phase": "path",
        "n": 135,
        "max": 0.10818862915039062,
        "mean": 0.0037802166771143675,
        "p95": 0.017866214737296104
      },
      {
        "phase": "summary",
        "n": 208,
        "max": 0.09079551696777344,
        "mean": 0.004994346760213375,
        "p95": 0.026639258489012718
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.71661376953125e-05,
        "mean": 8.58306884765625e-06,
        "p95": 1.6307831174344756e-05
      },
      {
        "phase": "main",
        "n": 335,
        "max": 0.08209228515625,
        "mean": 0.002594887977465987,
        "p95": 0.015677250921726227
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 10,
    "id": "bigmath/cn_k12/204933",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 551,
    "reference_F": 764,
    "generation_seconds": 22.595574126113206,
    "T": 997,
    "native_replay_max": 0.07244110107421875,
    "native_replay_mean": 0.005001061595976353,
    "native_replay_p95": 0.02777137979865074,
    "phases": [
      {
        "phase": "main",
        "n": 146,
        "max": 0.054840087890625,
        "mean": 0.005691541358828545,
        "p95": 0.027920246124267578
      },
      {
        "phase": "width",
        "n": 2,
        "max": 9.5367431640625e-06,
        "mean": 4.76837158203125e-06,
        "p95": 9.059906005859375e-06
      },
      {
        "phase": "path",
        "n": 105,
        "max": 0.07244110107421875,
        "mean": 0.0032100314274430275,
        "p95": 0.013971704989671707
      },
      {
        "phase": "path",
        "n": 166,
        "max": 0.0616455078125,
        "mean": 0.0051214261911809444,
        "p95": 0.030896663665771484
      },
      {
        "phase": "path",
        "n": 195,
        "max": 0.06597518920898438,
        "mean": 0.006055567879229784,
        "p95": 0.03323249891400337
      },
      {
        "phase": "path",
        "n": 175,
        "max": 0.06380081176757812,
        "mean": 0.004297289066016674,
        "p95": 0.02080383710563183
      },
      {
        "phase": "summary",
        "n": 162,
        "max": 0.06204032897949219,
        "mean": 0.005968817975372076,
        "p95": 0.02710827998816967
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.0517578125e-05,
        "mean": 1.52587890625e-05,
        "p95": 2.899169885495212e-05
      },
      {
        "phase": "main",
        "n": 44,
        "max": 0.017625808715820312,
        "mean": 0.001546209561638534,
        "p95": 0.008207987062633038
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 11,
    "id": "bigmath/cn_k12/147481",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 917,
    "reference_F": 1086,
    "generation_seconds": 35.15923238405958,
    "T": 1070,
    "native_replay_max": 0.09697628021240234,
    "native_replay_mean": 0.004449583124369383,
    "native_replay_p95": 0.026213064789772034,
    "phases": [
      {
        "phase": "main",
        "n": 409,
        "max": 0.061829566955566406,
        "mean": 0.005621488206088543,
        "p95": 0.030360795557498932
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.09808349609375e-05,
        "mean": 1.049041748046875e-05,
        "p95": 1.9931792849092744e-05
      },
      {
        "phase": "path",
        "n": 153,
        "max": 0.034709930419921875,
        "mean": 0.0026191885117441416,
        "p95": 0.01429594587534666
      },
      {
        "phase": "path",
        "n": 216,
        "max": 0.03922843933105469,
        "mean": 0.0028976246248930693,
        "p95": 0.01596832275390625
      },
      {
        "phase": "summary",
        "n": 219,
        "max": 0.09697628021240234,
        "mean": 0.0060757980681955814,
        "p95": 0.04033125936985016
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 69,
        "max": 0.030210494995117188,
        "mean": 0.001516231568530202,
        "p95": 0.0055282567627727985
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 12,
    "id": "bigmath/cn_k12/61311",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 871,
    "reference_F": 952,
    "generation_seconds": 34.742302044294775,
    "T": 1311,
    "native_replay_max": 0.10818099975585938,
    "native_replay_mean": 0.0034683840349316597,
    "native_replay_p95": 0.019529342651367188,
    "phases": [
      {
        "phase": "main",
        "n": 173,
        "max": 0.09175682067871094,
        "mean": 0.005071358755230904,
        "p95": 0.03016737289726734
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "path",
        "n": 144,
        "max": 0.08847808837890625,
        "mean": 0.003351648570969701,
        "p95": 0.016617095097899437
      },
      {
        "phase": "path",
        "n": 118,
        "max": 0.06885528564453125,
        "mean": 0.004398345947265625,
        "p95": 0.02748633176088333
      },
      {
        "phase": "path",
        "n": 359,
        "max": 0.06255149841308594,
        "mean": 0.0022903005592525005,
        "p95": 0.015460210852324963
      },
      {
        "phase": "path",
        "n": 178,
        "max": 0.05990409851074219,
        "mean": 0.002715142909437418,
        "p95": 0.01569431833922863
      },
      {
        "phase": "summary",
        "n": 268,
        "max": 0.10818099975585938,
        "mean": 0.004106201231479645,
        "p95": 0.01886892132461071
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.4332275390625e-05,
        "mean": 1.71661376953125e-05,
        "p95": 3.261566234868951e-05
      },
      {
        "phase": "main",
        "n": 67,
        "max": 0.08147811889648438,
        "mean": 0.003911089617758989,
        "p95": 0.01877155527472496
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 13,
    "id": "bigmath/cn_k12/155313",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 430,
    "reference_F": 921,
    "generation_seconds": 18.575511091388762,
    "T": 513,
    "native_replay_max": 0.05043220520019531,
    "native_replay_mean": 0.004615054931491613,
    "native_replay_p95": 0.022880544885993004,
    "phases": [
      {
        "phase": "main",
        "n": 204,
        "max": 0.05043220520019531,
        "mean": 0.0047668335027992725,
        "p95": 0.022094814106822014
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.86102294921875e-05,
        "mean": 1.430511474609375e-05,
        "p95": 2.7179718017578125e-05
      },
      {
        "phase": "path",
        "n": 93,
        "max": 0.04475975036621094,
        "mean": 0.0038334836717694998,
        "p95": 0.021019762381911278
      },
      {
        "phase": "path",
        "n": 83,
        "max": 0.03954887390136719,
        "mean": 0.004876906517893076,
        "p95": 0.02075786702334881
      },
      {
        "phase": "summary",
        "n": 49,
        "max": 0.03510856628417969,
        "mean": 0.005184640642255545,
        "p95": 0.017287826165556908
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.0517578125e-05,
        "mean": 1.52587890625e-05,
        "p95": 2.899169885495212e-05
      },
      {
        "phase": "main",
        "n": 80,
        "max": 0.041675567626953125,
        "mean": 0.004746067337691784,
        "p95": 0.02638159692287445
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 14,
    "id": "bigmath/cn_k12/95257",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1246,
    "reference_F": 1763,
    "generation_seconds": 48.98521015001461,
    "T": 1649,
    "native_replay_max": 0.17393875122070312,
    "native_replay_mean": 0.00329616223461926,
    "native_replay_p95": 0.019212720915675163,
    "phases": [
      {
        "phase": "main",
        "n": 226,
        "max": 0.07836341857910156,
        "mean": 0.004355063661932945,
        "p95": 0.023740291595458984
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.288818359375e-05,
        "mean": 1.1444091796875e-05,
        "p95": 2.174377368646674e-05
      },
      {
        "phase": "path",
        "n": 137,
        "max": 0.03952217102050781,
        "mean": 0.0018403965514153242,
        "p95": 0.012486261315643787
      },
      {
        "phase": "path",
        "n": 110,
        "max": 0.1255340576171875,
        "mean": 0.003129525575786829,
        "p95": 0.014079470187425613
      },
      {
        "phase": "path",
        "n": 156,
        "max": 0.04663658142089844,
        "mean": 0.0019956491887569427,
        "p95": 0.015114784240722656
      },
      {
        "phase": "path",
        "n": 403,
        "max": 0.17393875122070312,
        "mean": 0.002145024249330163,
        "p95": 0.01242026500403881
      },
      {
        "phase": "summary",
        "n": 525,
        "max": 0.07831954956054688,
        "mean": 0.004317098297178745,
        "p95": 0.026042547076940536
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0001239776611328125,
        "mean": 6.198883056640625e-05,
        "p95": 0.00011777877807617188
      },
      {
        "phase": "main",
        "n": 88,
        "max": 0.047039031982421875,
        "mean": 0.004685856867581606,
        "p95": 0.03420926257967949
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 15,
    "id": "bigmath/cn_k12/3177",
    "correct": false,
    "reference_correct": false,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 614,
    "reference_F": 724,
    "generation_seconds": 24.142190960235894,
    "T": 963,
    "native_replay_max": 0.09606170654296875,
    "native_replay_mean": 0.0030869655311107635,
    "native_replay_p95": 0.019098659977316856,
    "phases": [
      {
        "phase": "main",
        "n": 160,
        "max": 0.04583549499511719,
        "mean": 0.0031644939444959164,
        "p95": 0.017896559089422226
      },
      {
        "phase": "width",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "path",
        "n": 108,
        "max": 0.0526885986328125,
        "mean": 0.0029370873235166073,
        "p95": 0.01517801359295845
      },
      {
        "phase": "path",
        "n": 91,
        "max": 0.07331657409667969,
        "mean": 0.004939676728099585,
        "p95": 0.027029037475585938
      },
      {
        "phase": "path",
        "n": 233,
        "max": 0.07928466796875,
        "mean": 0.001817965181544423,
        "p95": 0.009931561537086964
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.06336784362792969,
        "mean": 0.002734082518145442,
        "p95": 0.01705886237323284
      },
      {
        "phase": "summary",
        "n": 160,
        "max": 0.09606170654296875,
        "mean": 0.00416797399520874,
        "p95": 0.023675348609685898
      },
      {
        "phase": "main",
        "n": 2,
        "max": 5.7220458984375e-06,
        "mean": 2.86102294921875e-06,
        "p95": 5.435943421616685e-06
      },
      {
        "phase": "main",
        "n": 57,
        "max": 0.05230140686035156,
        "mean": 0.0034935600124299526,
        "p95": 0.015702445060014725
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 0,
      "id": "bigmath/cn_k12/26444",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 522,
      "reference_F": 752,
      "generation_seconds": 22.790329400915653,
      "T": 826,
      "native_replay_max": 0.08494949340820312,
      "native_replay_mean": 0.0019829566590487957,
      "native_replay_p95": 0.012860774993896484,
      "phases": [
        {
          "phase": "main",
          "n": 187,
          "max": 0.05371284484863281,
          "mean": 0.002823426853865385,
          "p95": 0.012594028376042843
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.6702880859375e-05,
          "mean": 1.33514404296875e-05,
          "p95": 2.536773718020413e-05
        },
        {
          "phase": "path",
          "n": 79,
          "max": 0.018426895141601562,
          "mean": 0.0010873818537220359,
          "p95": 0.004986749030649662
        },
        {
          "phase": "path",
          "n": 74,
          "max": 0.017406463623046875,
          "mean": 0.0013191377511247993,
          "p95": 0.01127280481159687
        },
        {
          "phase": "path",
          "n": 151,
          "max": 0.02713775634765625,
          "mean": 0.0013903181534260511,
          "p95": 0.009466171264648438
        },
        {
          "phase": "path",
          "n": 226,
          "max": 0.08494949340820312,
          "mean": 0.0022007934749126434,
          "p95": 0.016823291778564453
        },
        {
          "phase": "summary",
          "n": 66,
          "max": 0.05126190185546875,
          "mean": 0.002826112788170576,
          "p95": 0.015065193176269531
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 39,
          "max": 0.011318206787109375,
          "mean": 0.0008346851100213826,
          "p95": 0.0034990254789590836
        }
      ]
    },
    {
      "index": 8,
      "id": "bigmath/cn_k12/23250",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 416,
      "reference_F": 521,
      "generation_seconds": 18.702754213940352,
      "T": 575,
      "native_replay_max": 0.05078411102294922,
      "native_replay_mean": 0.003383548464626074,
      "native_replay_p95": 0.018609045073390007,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.05078411102294922,
          "mean": 0.004470690619200468,
          "p95": 0.030411895364522934
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 101,
          "max": 0.04351234436035156,
          "mean": 0.002944172127172351,
          "p95": 0.01305389404296875
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.049129486083984375,
          "mean": 0.002521093701943755,
          "p95": 0.013315555639564991
        },
        {
          "phase": "path",
          "n": 82,
          "max": 0.043704986572265625,
          "mean": 0.002374672330915928,
          "p95": 0.008527849800884724
        },
        {
          "phase": "summary",
          "n": 102,
          "max": 0.03363609313964844,
          "mean": 0.004300098866224289,
          "p95": 0.025324903428554535
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 46,
          "max": 0.017704010009765625,
          "mean": 0.0019996478222310543,
          "p95": 0.013004779815673828
        }
      ]
    }
  ],
  "actions": 1401,
  "native_replay_max": 0.08494949340820312,
  "native_replay_mean": 0.002557789208367467,
  "native_replay_p95": 0.015169143676757812,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24403539456,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 1,
      "id": "bigmath/cn_k12/88253",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 958,
      "reference_F": 1344,
      "generation_seconds": 38.88683386426419,
      "T": 1024,
      "native_replay_max": 0.11869239807128906,
      "native_replay_mean": 0.004648228175938129,
      "native_replay_p95": 0.024261759594082832,
      "phases": [
        {
          "phase": "main",
          "n": 131,
          "max": 0.04820442199707031,
          "mean": 0.0036242245696485043,
          "p95": 0.017065048217773438
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.71661376953125e-05,
          "mean": 8.58306884765625e-06,
          "p95": 1.6307831174344756e-05
        },
        {
          "phase": "path",
          "n": 66,
          "max": 0.04376792907714844,
          "mean": 0.00303962011821568,
          "p95": 0.02038860321044922
        },
        {
          "phase": "path",
          "n": 177,
          "max": 0.03538322448730469,
          "mean": 0.0034940363839268684,
          "p95": 0.0210189800709486
        },
        {
          "phase": "summary",
          "n": 545,
          "max": 0.11869239807128906,
          "mean": 0.005615306086838245,
          "p95": 0.02529296837747097
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 101,
          "max": 0.07167434692382812,
          "mean": 0.004015761893242598,
          "p95": 0.021516799926757812
        }
      ]
    },
    {
      "index": 9,
      "id": "bigmath/cn_k12/64731",
      "correct": false,
      "reference_correct": true,
      "format_valid": false,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1018,
      "reference_F": 2172,
      "generation_seconds": 40.6976250926964,
      "T": 1405,
      "native_replay_max": 0.11976051330566406,
      "native_replay_mean": 0.0031565052922815084,
      "native_replay_p95": 0.017027273774147034,
      "phases": [
        {
          "phase": "main",
          "n": 155,
          "max": 0.06254768371582031,
          "mean": 0.0051407720893621445,
          "p95": 0.027034761384129524
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.03357887268066406,
          "mean": 0.0014412307646125555,
          "p95": 0.0075296442955732346
        },
        {
          "phase": "path",
          "n": 316,
          "max": 0.0385589599609375,
          "mean": 0.0013943503145128489,
          "p95": 0.008848190307617188
        },
        {
          "phase": "path",
          "n": 102,
          "max": 0.11976051330566406,
          "mean": 0.005517567042261362,
          "p95": 0.023088829591870308
        },
        {
          "phase": "path",
          "n": 135,
          "max": 0.10818862915039062,
          "mean": 0.0037802166771143675,
          "p95": 0.017866214737296104
        },
        {
          "phase": "summary",
          "n": 208,
          "max": 0.09079551696777344,
          "mean": 0.004994346760213375,
          "p95": 0.026639258489012718
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.71661376953125e-05,
          "mean": 8.58306884765625e-06,
          "p95": 1.6307831174344756e-05
        },
        {
          "phase": "main",
          "n": 335,
          "max": 0.08209228515625,
          "mean": 0.002594887977465987,
          "p95": 0.015677250921726227
        }
      ]
    }
  ],
  "actions": 2429,
  "native_replay_max": 0.11976051330566406,
  "native_replay_mean": 0.0037853748071938753,
  "native_replay_p95": 0.021543115377426147,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24539991040,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 2,
      "id": "bigmath/cn_k12/163846",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 487,
      "reference_F": 463,
      "generation_seconds": 21.034886864945292,
      "T": 673,
      "native_replay_max": 0.05848407745361328,
      "native_replay_mean": 0.0043082586489617825,
      "native_replay_p95": 0.02234838716685772,
      "phases": [
        {
          "phase": "main",
          "n": 116,
          "max": 0.044915199279785156,
          "mean": 0.0036849728785455227,
          "p95": 0.023573875427246094
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.52587890625e-05,
          "mean": 7.62939453125e-06,
          "p95": 1.449584942747606e-05
        },
        {
          "phase": "path",
          "n": 23,
          "max": 0.014173507690429688,
          "mean": 0.0027722069062292576,
          "p95": 0.009618186391890049
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.04358673095703125,
          "mean": 0.004912909120321274,
          "p95": 0.023207075893878937
        },
        {
          "phase": "path",
          "n": 195,
          "max": 0.05566596984863281,
          "mean": 0.0051181744784116745,
          "p95": 0.025279240682721138
        },
        {
          "phase": "path",
          "n": 86,
          "max": 0.03192901611328125,
          "mean": 0.0035238710697740316,
          "p95": 0.01439523696899414
        },
        {
          "phase": "summary",
          "n": 97,
          "max": 0.05848407745361328,
          "mean": 0.005313401576131582,
          "p95": 0.02094077318906784
        },
        {
          "phase": "main",
          "n": 2,
          "max": 5.7220458984375e-06,
          "mean": 2.86102294921875e-06,
          "p95": 5.435943421616685e-06
        },
        {
          "phase": "main",
          "n": 75,
          "max": 0.042392730712890625,
          "mean": 0.0028457134030759335,
          "p95": 0.010398090817034245
        }
      ]
    },
    {
      "index": 10,
      "id": "bigmath/cn_k12/204933",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 551,
      "reference_F": 764,
      "generation_seconds": 22.595574126113206,
      "T": 997,
      "native_replay_max": 0.07244110107421875,
      "native_replay_mean": 0.005001061595976353,
      "native_replay_p95": 0.02777137979865074,
      "phases": [
        {
          "phase": "main",
          "n": 146,
          "max": 0.054840087890625,
          "mean": 0.005691541358828545,
          "p95": 0.027920246124267578
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.5367431640625e-06,
          "mean": 4.76837158203125e-06,
          "p95": 9.059906005859375e-06
        },
        {
          "phase": "path",
          "n": 105,
          "max": 0.07244110107421875,
          "mean": 0.0032100314274430275,
          "p95": 0.013971704989671707
        },
        {
          "phase": "path",
          "n": 166,
          "max": 0.0616455078125,
          "mean": 0.0051214261911809444,
          "p95": 0.030896663665771484
        },
        {
          "phase": "path",
          "n": 195,
          "max": 0.06597518920898438,
          "mean": 0.006055567879229784,
          "p95": 0.03323249891400337
        },
        {
          "phase": "path",
          "n": 175,
          "max": 0.06380081176757812,
          "mean": 0.004297289066016674,
          "p95": 0.02080383710563183
        },
        {
          "phase": "summary",
          "n": 162,
          "max": 0.06204032897949219,
          "mean": 0.005968817975372076,
          "p95": 0.02710827998816967
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.0517578125e-05,
          "mean": 1.52587890625e-05,
          "p95": 2.899169885495212e-05
        },
        {
          "phase": "main",
          "n": 44,
          "max": 0.017625808715820312,
          "mean": 0.001546209561638534,
          "p95": 0.008207987062633038
        }
      ]
    }
  ],
  "actions": 1670,
  "native_replay_max": 0.07244110107421875,
  "native_replay_mean": 0.004721865989267826,
  "native_replay_p95": 0.02461879700422287,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24304155136,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 3,
      "id": "bigmath/cn_k12/210293",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 410,
      "reference_F": 710,
      "generation_seconds": 16.307979070581496,
      "T": 477,
      "native_replay_max": 0.07386970520019531,
      "native_replay_mean": 0.00377426715567708,
      "native_replay_p95": 0.01970481313765049,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.06050300598144531,
          "mean": 0.004320764914155006,
          "p95": 0.021249761804938316
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "path",
          "n": 83,
          "max": 0.042835235595703125,
          "mean": 0.002374120522290468,
          "p95": 0.01274204533547163
        },
        {
          "phase": "path",
          "n": 67,
          "max": 0.03825569152832031,
          "mean": 0.0024083550088107586,
          "p95": 0.014488797634840012
        },
        {
          "phase": "summary",
          "n": 88,
          "max": 0.04264640808105469,
          "mean": 0.005574139766395092,
          "p95": 0.02513285167515278
        },
        {
          "phase": "main",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "main",
          "n": 72,
          "max": 0.07386970520019531,
          "mean": 0.0034318764228373766,
          "p95": 0.01463173795491457
        }
      ]
    },
    {
      "index": 11,
      "id": "bigmath/cn_k12/147481",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 917,
      "reference_F": 1086,
      "generation_seconds": 35.15923238405958,
      "T": 1070,
      "native_replay_max": 0.09697628021240234,
      "native_replay_mean": 0.004449583124369383,
      "native_replay_p95": 0.026213064789772034,
      "phases": [
        {
          "phase": "main",
          "n": 409,
          "max": 0.061829566955566406,
          "mean": 0.005621488206088543,
          "p95": 0.030360795557498932
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 153,
          "max": 0.034709930419921875,
          "mean": 0.0026191885117441416,
          "p95": 0.01429594587534666
        },
        {
          "phase": "path",
          "n": 216,
          "max": 0.03922843933105469,
          "mean": 0.0028976246248930693,
          "p95": 0.01596832275390625
        },
        {
          "phase": "summary",
          "n": 219,
          "max": 0.09697628021240234,
          "mean": 0.0060757980681955814,
          "p95": 0.04033125936985016
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 69,
          "max": 0.030210494995117188,
          "mean": 0.001516231568530202,
          "p95": 0.0055282567627727985
        }
      ]
    }
  ],
  "actions": 1547,
  "native_replay_max": 0.09697628021240234,
  "native_replay_mean": 0.0042413570918142796,
  "native_replay_p95": 0.02373790740966797,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24286622208,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 4,
      "id": "bigmath/cn_k12/88674",
      "correct": true,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 483,
      "reference_F": 2255,
      "generation_seconds": 20.10050451103598,
      "T": 659,
      "native_replay_max": 0.07795906066894531,
      "native_replay_mean": 0.005394060164690018,
      "native_replay_p95": 0.026583857834339142,
      "phases": [
        {
          "phase": "main",
          "n": 148,
          "max": 0.0564727783203125,
          "mean": 0.005255512427538633,
          "p95": 0.020606692880392075
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.5367431640625e-06,
          "mean": 4.76837158203125e-06,
          "p95": 9.059906005859375e-06
        },
        {
          "phase": "path",
          "n": 85,
          "max": 0.055350303649902344,
          "mean": 0.00395760266110301,
          "p95": 0.016618719324469566
        },
        {
          "phase": "path",
          "n": 76,
          "max": 0.07795906066894531,
          "mean": 0.00862259604036808,
          "p95": 0.03531217575073242
        },
        {
          "phase": "path",
          "n": 54,
          "max": 0.041973114013671875,
          "mean": 0.006763352081179619,
          "p95": 0.03002995252609253
        },
        {
          "phase": "path",
          "n": 46,
          "max": 0.02860260009765625,
          "mean": 0.0035200740676373243,
          "p95": 0.017293453216552734
        },
        {
          "phase": "summary",
          "n": 169,
          "max": 0.05523490905761719,
          "mean": 0.006109299603849649,
          "p95": 0.03218838945031166
        },
        {
          "phase": "main",
          "n": 2,
          "max": 2.47955322265625e-05,
          "mean": 1.239776611328125e-05,
          "p95": 2.3555754523840733e-05
        },
        {
          "phase": "main",
          "n": 77,
          "max": 0.026922225952148438,
          "mean": 0.0029286472126841545,
          "p95": 0.013180919922888279
        }
      ]
    },
    {
      "index": 12,
      "id": "bigmath/cn_k12/61311",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 871,
      "reference_F": 952,
      "generation_seconds": 34.742302044294775,
      "T": 1311,
      "native_replay_max": 0.10818099975585938,
      "native_replay_mean": 0.0034683840349316597,
      "native_replay_p95": 0.019529342651367188,
      "phases": [
        {
          "phase": "main",
          "n": 173,
          "max": 0.09175682067871094,
          "mean": 0.005071358755230904,
          "p95": 0.03016737289726734
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 144,
          "max": 0.08847808837890625,
          "mean": 0.003351648570969701,
          "p95": 0.016617095097899437
        },
        {
          "phase": "path",
          "n": 118,
          "max": 0.06885528564453125,
          "mean": 0.004398345947265625,
          "p95": 0.02748633176088333
        },
        {
          "phase": "path",
          "n": 359,
          "max": 0.06255149841308594,
          "mean": 0.0022903005592525005,
          "p95": 0.015460210852324963
        },
        {
          "phase": "path",
          "n": 178,
          "max": 0.05990409851074219,
          "mean": 0.002715142909437418,
          "p95": 0.01569431833922863
        },
        {
          "phase": "summary",
          "n": 268,
          "max": 0.10818099975585938,
          "mean": 0.004106201231479645,
          "p95": 0.01886892132461071
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.4332275390625e-05,
          "mean": 1.71661376953125e-05,
          "p95": 3.261566234868951e-05
        },
        {
          "phase": "main",
          "n": 67,
          "max": 0.08147811889648438,
          "mean": 0.003911089617758989,
          "p95": 0.01877155527472496
        }
      ]
    }
  ],
  "actions": 1970,
  "native_replay_max": 0.10818099975585938,
  "native_replay_mean": 0.004112557042390108,
  "native_replay_p95": 0.021851301193237305,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24629432320,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 5,
      "id": "bigmath/cn_k12/165159",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 533,
      "reference_F": 540,
      "generation_seconds": 22.744069282431155,
      "T": 809,
      "native_replay_max": 0.11617279052734375,
      "native_replay_mean": 0.005428923759609461,
      "native_replay_p95": 0.026743687689304352,
      "phases": [
        {
          "phase": "main",
          "n": 186,
          "max": 0.05578041076660156,
          "mean": 0.004886222071945667,
          "p95": 0.024785518646240234
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.52587890625e-05,
          "mean": 7.62939453125e-06,
          "p95": 1.449584942747606e-05
        },
        {
          "phase": "path",
          "n": 79,
          "max": 0.09689140319824219,
          "mean": 0.0055153281427919865,
          "p95": 0.024794384837150574
        },
        {
          "phase": "path",
          "n": 50,
          "max": 0.05733489990234375,
          "mean": 0.006714591756463051,
          "p95": 0.03301943838596344
        },
        {
          "phase": "path",
          "n": 56,
          "max": 0.07233619689941406,
          "mean": 0.004903861321508884,
          "p95": 0.01911640167236328
        },
        {
          "phase": "path",
          "n": 33,
          "max": 0.026464462280273438,
          "mean": 0.004181601572781801,
          "p95": 0.01734313555061817
        },
        {
          "phase": "path",
          "n": 49,
          "max": 0.034648895263671875,
          "mean": 0.003635756904259324,
          "p95": 0.0120010357350111
        },
        {
          "phase": "path",
          "n": 56,
          "max": 0.11617279052734375,
          "mean": 0.009230579249560833,
          "p95": 0.041947364807128906
        },
        {
          "phase": "path",
          "n": 32,
          "max": 0.028890609741210938,
          "mean": 0.0047251880168914795,
          "p95": 0.023366156965494156
        },
        {
          "phase": "summary",
          "n": 189,
          "max": 0.04609489440917969,
          "mean": 0.006764543242752552,
          "p95": 0.028033826500177383
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 75,
          "max": 0.03908729553222656,
          "mean": 0.002324345987290144,
          "p95": 0.01557234302163124
        }
      ]
    },
    {
      "index": 13,
      "id": "bigmath/cn_k12/155313",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 430,
      "reference_F": 921,
      "generation_seconds": 18.575511091388762,
      "T": 513,
      "native_replay_max": 0.05043220520019531,
      "native_replay_mean": 0.004615054931491613,
      "native_replay_p95": 0.022880544885993004,
      "phases": [
        {
          "phase": "main",
          "n": 204,
          "max": 0.05043220520019531,
          "mean": 0.0047668335027992725,
          "p95": 0.022094814106822014
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.86102294921875e-05,
          "mean": 1.430511474609375e-05,
          "p95": 2.7179718017578125e-05
        },
        {
          "phase": "path",
          "n": 93,
          "max": 0.04475975036621094,
          "mean": 0.0038334836717694998,
          "p95": 0.021019762381911278
        },
        {
          "phase": "path",
          "n": 83,
          "max": 0.03954887390136719,
          "mean": 0.004876906517893076,
          "p95": 0.02075786702334881
        },
        {
          "phase": "summary",
          "n": 49,
          "max": 0.03510856628417969,
          "mean": 0.005184640642255545,
          "p95": 0.017287826165556908
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.0517578125e-05,
          "mean": 1.52587890625e-05,
          "p95": 2.899169885495212e-05
        },
        {
          "phase": "main",
          "n": 80,
          "max": 0.041675567626953125,
          "mean": 0.004746067337691784,
          "p95": 0.02638159692287445
        }
      ]
    }
  ],
  "actions": 1322,
  "native_replay_max": 0.11617279052734375,
  "native_replay_mean": 0.005113103426992893,
  "native_replay_p95": 0.025956913828849792,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24929274368,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 6,
      "id": "bigmath/cn_k12/176142",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 428,
      "reference_F": 710,
      "generation_seconds": 17.99006543168798,
      "T": 641,
      "native_replay_max": 0.05636405944824219,
      "native_replay_mean": 0.0036853933706879616,
      "native_replay_p95": 0.022159576416015625,
      "phases": [
        {
          "phase": "main",
          "n": 157,
          "max": 0.0424652099609375,
          "mean": 0.003375217318534851,
          "p95": 0.017594141885638237
        },
        {
          "phase": "width",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "path",
          "n": 114,
          "max": 0.04367256164550781,
          "mean": 0.0026311539113521576,
          "p95": 0.015651891008019447
        },
        {
          "phase": "path",
          "n": 62,
          "max": 0.008127212524414062,
          "mean": 0.0010563019895926118,
          "p95": 0.00638694828376174
        },
        {
          "phase": "path",
          "n": 91,
          "max": 0.04427909851074219,
          "mean": 0.0036268129479140043,
          "p95": 0.027736663818359375
        },
        {
          "phase": "path",
          "n": 60,
          "max": 0.05636405944824219,
          "mean": 0.005800342652946711,
          "p95": 0.030047884210944176
        },
        {
          "phase": "summary",
          "n": 100,
          "max": 0.050106048583984375,
          "mean": 0.005025253165513277,
          "p95": 0.0249295923858881
        },
        {
          "phase": "main",
          "n": 2,
          "max": 7.43865966796875e-05,
          "mean": 3.719329833984375e-05,
          "p95": 7.06672653905116e-05
        },
        {
          "phase": "main",
          "n": 53,
          "max": 0.049282073974609375,
          "mean": 0.005402223207056522,
          "p95": 0.029555508866906166
        }
      ]
    },
    {
      "index": 14,
      "id": "bigmath/cn_k12/95257",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1246,
      "reference_F": 1763,
      "generation_seconds": 48.98521015001461,
      "T": 1649,
      "native_replay_max": 0.17393875122070312,
      "native_replay_mean": 0.00329616223461926,
      "native_replay_p95": 0.019212720915675163,
      "phases": [
        {
          "phase": "main",
          "n": 226,
          "max": 0.07836341857910156,
          "mean": 0.004355063661932945,
          "p95": 0.023740291595458984
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.288818359375e-05,
          "mean": 1.1444091796875e-05,
          "p95": 2.174377368646674e-05
        },
        {
          "phase": "path",
          "n": 137,
          "max": 0.03952217102050781,
          "mean": 0.0018403965514153242,
          "p95": 0.012486261315643787
        },
        {
          "phase": "path",
          "n": 110,
          "max": 0.1255340576171875,
          "mean": 0.003129525575786829,
          "p95": 0.014079470187425613
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.04663658142089844,
          "mean": 0.0019956491887569427,
          "p95": 0.015114784240722656
        },
        {
          "phase": "path",
          "n": 403,
          "max": 0.17393875122070312,
          "mean": 0.002145024249330163,
          "p95": 0.01242026500403881
        },
        {
          "phase": "summary",
          "n": 525,
          "max": 0.07831954956054688,
          "mean": 0.004317098297178745,
          "p95": 0.026042547076940536
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0001239776611328125,
          "mean": 6.198883056640625e-05,
          "p95": 0.00011777877807617188
        },
        {
          "phase": "main",
          "n": 88,
          "max": 0.047039031982421875,
          "mean": 0.004685856867581606,
          "p95": 0.03420926257967949
        }
      ]
    }
  ],
  "actions": 2290,
  "native_replay_max": 0.17393875122070312,
  "native_replay_mean": 0.003405112773180008,
  "native_replay_p95": 0.01958952099084854,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24634776576,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-native/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "precision": "bf16_autocast_fp32_head",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 7,
      "id": "bigmath/cn_k12/60327",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1553,
      "reference_F": 1069,
      "generation_seconds": 61.85179492365569,
      "T": 1729,
      "native_replay_max": 0.09578514099121094,
      "native_replay_mean": 0.004436512943357229,
      "native_replay_p95": 0.024081414565443993,
      "phases": [
        {
          "phase": "main",
          "n": 95,
          "max": 0.038482666015625,
          "mean": 0.004849744960665703,
          "p95": 0.027505869045853615
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 73,
          "max": 0.03365898132324219,
          "mean": 0.0033573254477232695,
          "p95": 0.01533279474824667
        },
        {
          "phase": "path",
          "n": 116,
          "max": 0.04682731628417969,
          "mean": 0.004449137486517429,
          "p95": 0.026491641998291016
        },
        {
          "phase": "summary",
          "n": 76,
          "max": 0.04594230651855469,
          "mean": 0.004438249859958887,
          "p95": 0.026916027069091797
        },
        {
          "phase": "main",
          "n": 118,
          "max": 0.06904411315917969,
          "mean": 0.007762965280562639,
          "p95": 0.03493587672710419
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 103,
          "max": 0.051334381103515625,
          "mean": 0.003707108087837696,
          "p95": 0.022826576605439186
        },
        {
          "phase": "path",
          "n": 254,
          "max": 0.09578514099121094,
          "mean": 0.006367965135723352,
          "p95": 0.025580788031220436
        },
        {
          "phase": "summary",
          "n": 786,
          "max": 0.09099960327148438,
          "mean": 0.0037027799990028143,
          "p95": 0.021184444427490234
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 102,
          "max": 0.0333251953125,
          "mean": 0.002801745431497693,
          "p95": 0.01744593307375908
        }
      ]
    },
    {
      "index": 15,
      "id": "bigmath/cn_k12/3177",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 614,
      "reference_F": 724,
      "generation_seconds": 24.142190960235894,
      "T": 963,
      "native_replay_max": 0.09606170654296875,
      "native_replay_mean": 0.0030869655311107635,
      "native_replay_p95": 0.019098659977316856,
      "phases": [
        {
          "phase": "main",
          "n": 160,
          "max": 0.04583549499511719,
          "mean": 0.0031644939444959164,
          "p95": 0.017896559089422226
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "path",
          "n": 108,
          "max": 0.0526885986328125,
          "mean": 0.0029370873235166073,
          "p95": 0.01517801359295845
        },
        {
          "phase": "path",
          "n": 91,
          "max": 0.07331657409667969,
          "mean": 0.004939676728099585,
          "p95": 0.027029037475585938
        },
        {
          "phase": "path",
          "n": 233,
          "max": 0.07928466796875,
          "mean": 0.001817965181544423,
          "p95": 0.009931561537086964
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.06336784362792969,
          "mean": 0.002734082518145442,
          "p95": 0.01705886237323284
        },
        {
          "phase": "summary",
          "n": 160,
          "max": 0.09606170654296875,
          "mean": 0.00416797399520874,
          "p95": 0.023675348609685898
        },
        {
          "phase": "main",
          "n": 2,
          "max": 5.7220458984375e-06,
          "mean": 2.86102294921875e-06,
          "p95": 5.435943421616685e-06
        },
        {
          "phase": "main",
          "n": 57,
          "max": 0.05230140686035156,
          "mean": 0.0034935600124299526,
          "p95": 0.015702445060014725
        }
      ]
    }
  ],
  "actions": 2692,
  "native_replay_max": 0.09606170654296875,
  "native_replay_mean": 0.003953743726015091,
  "native_replay_p95": 0.022880839183926582,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 24995399680,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/result.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 52,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/checkpoint-0052/hf",
  "initial_step": 50,
  "positive_updates": 2,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 52,
  "steps": 52
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/validation-0052/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/bf16-rollout-tis/training/validation-0052/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 52,
  "completed": 16,
  "correct": 13,
  "format_valid": 14,
  "parallel_valid": 14,
  "fork_tasks": 16,
  "widths": [
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    5,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4
  ],
  "actual_rounds": 16,
  "logical_depth": [
    693,
    466,
    1235,
    1142,
    486,
    1083,
    675,
    1576,
    2203,
    1179,
    522,
    858,
    919,
    1117,
    2440,
    862
  ],
  "sampled_tokens": [
    1062,
    793,
    1582,
    1909,
    686,
    1456,
    1127,
    3641,
    2872,
    1911,
    741,
    1190,
    1520,
    1588,
    4079,
    1295
  ],
  "actual_forward_calls": [
    693,
    466,
    1235,
    1142,
    486,
    1083,
    675,
    1576,
    2203,
    1179,
    522,
    858,
    919,
    1117,
    2440,
    862
  ],
  "sampler": "FP32 learner HF fullwidth8, temperature1 top_p1 nofilter; fixed clean16 validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1427,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 41.835834744852036
  },
  "no_reduced_bf16_accum": {
    "n": 1427,
    "max": 0.1840229034423828,
    "mean": 0.005101256538182497,
    "p95": 0.03766610845923424,
    "ratio_min": 0.8319167494773865,
    "ratio_max": 1.1227530241012573,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005064792465418577,
    "seconds": 1.1827070591971278
  },
  "no_reduced_math_sdpa": {
    "n": 1427,
    "max": 0.188385009765625,
    "mean": 0.005339649971574545,
    "p95": 0.03457723930478096,
    "ratio_min": 0.8282957673072815,
    "ratio_max": 1.1780587434768677,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005310504697263241,
    "seconds": 2.140427067875862
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2415,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 80.84689754294232
  },
  "no_reduced_bf16_accum": {
    "n": 2415,
    "max": 0.20808792114257812,
    "mean": 0.007063607219606638,
    "p95": 0.048496462404727936,
    "ratio_min": 0.8291888236999512,
    "ratio_max": 1.2313214540481567,
    "clip_fraction": 0.00041407867684029043,
    "ratio_abs_mean": 0.007056655827909708,
    "seconds": 1.4045582921244204
  },
  "no_reduced_math_sdpa": {
    "n": 2415,
    "max": 0.20299530029296875,
    "mean": 0.006621985230594873,
    "p95": 0.046650148928165436,
    "ratio_min": 0.8162820935249329,
    "ratio_max": 1.1425718069076538,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.006602610927075148,
    "seconds": 2.8484451891854405
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1653,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 51.12582642072812
  },
  "no_reduced_bf16_accum": {
    "n": 1653,
    "max": 0.12487030029296875,
    "mean": 0.007612011395394802,
    "p95": 0.05492058023810387,
    "ratio_min": 0.8884265422821045,
    "ratio_max": 1.133001446723938,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.007582842838019133,
    "seconds": 1.233372869901359
  },
  "no_reduced_math_sdpa": {
    "n": 1653,
    "max": 0.1971759796142578,
    "mean": 0.008143271319568157,
    "p95": 0.057400137186050415,
    "ratio_min": 0.8814185857772827,
    "ratio_max": 1.2179583311080933,
    "clip_fraction": 0.0006049606599844992,
    "ratio_abs_mean": 0.008103501982986927,
    "seconds": 2.2874839450232685
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1856,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 53.58585720229894
  },
  "no_reduced_bf16_accum": {
    "n": 1856,
    "max": 0.1677703857421875,
    "mean": 0.008682271465659142,
    "p95": 0.06518840789794922,
    "ratio_min": 0.8841632008552551,
    "ratio_max": 1.1826649904251099,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.008716858923435211,
    "seconds": 1.4788881284184754
  },
  "no_reduced_math_sdpa": {
    "n": 1856,
    "max": 0.2461986541748047,
    "mean": 0.00917220301926136,
    "p95": 0.07058286666870117,
    "ratio_min": 0.7817668914794922,
    "ratio_max": 1.1461338996887207,
    "clip_fraction": 0.0005387931014411151,
    "ratio_abs_mean": 0.00917468685656786,
    "seconds": 2.792898308020085
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1695,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 47.1431276560761
  },
  "no_reduced_bf16_accum": {
    "n": 1695,
    "max": 0.22608566284179688,
    "mean": 0.008175305090844631,
    "p95": 0.05287398025393486,
    "ratio_min": 0.8814303874969482,
    "ratio_max": 1.253683090209961,
    "clip_fraction": 0.0005899704992771149,
    "ratio_abs_mean": 0.008227004669606686,
    "seconds": 1.3046614597551525
  },
  "no_reduced_math_sdpa": {
    "n": 1695,
    "max": 0.20009803771972656,
    "mean": 0.008683828637003899,
    "p95": 0.06170841306447983,
    "ratio_min": 0.8710949420928955,
    "ratio_max": 1.2215224504470825,
    "clip_fraction": 0.0005899704992771149,
    "ratio_abs_mean": 0.008735244162380695,
    "seconds": 2.5188404959626496
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1754,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 53.95013520680368
  },
  "no_reduced_bf16_accum": {
    "n": 1754,
    "max": 0.22924041748046875,
    "mean": 0.012275268323719501,
    "p95": 0.07768971472978592,
    "ratio_min": 0.795137345790863,
    "ratio_max": 1.1657227277755737,
    "clip_fraction": 0.0005701254121959209,
    "ratio_abs_mean": 0.012289630249142647,
    "seconds": 1.4111276199109852
  },
  "no_reduced_math_sdpa": {
    "n": 1754,
    "max": 0.2446441650390625,
    "mean": 0.012198041193187237,
    "p95": 0.07838386297225952,
    "ratio_min": 0.8663080930709839,
    "ratio_max": 1.277166724205017,
    "clip_fraction": 0.0005701254121959209,
    "ratio_abs_mean": 0.012209339067339897,
    "seconds": 2.610355088952929
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2165,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 64.95876739919186
  },
  "no_reduced_bf16_accum": {
    "n": 2165,
    "max": 0.1757965087890625,
    "mean": 0.005583602469414473,
    "p95": 0.03851243481040001,
    "ratio_min": 0.8826231360435486,
    "ratio_max": 1.1921954154968262,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005595067050307989,
    "seconds": 1.4528761231340468
  },
  "no_reduced_math_sdpa": {
    "n": 2165,
    "max": 0.2579498291015625,
    "mean": 0.006018822081387043,
    "p95": 0.04232444614171982,
    "ratio_min": 0.8530122637748718,
    "ratio_max": 1.294273853302002,
    "clip_fraction": 0.0009237875347025692,
    "ratio_abs_mean": 0.006030121352523565,
    "seconds": 2.910650397185236
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2218,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 67.33400574000552
  },
  "no_reduced_bf16_accum": {
    "n": 2218,
    "max": 0.2468128204345703,
    "mean": 0.0073055727407336235,
    "p95": 0.05544469878077507,
    "ratio_min": 0.781286895275116,
    "ratio_max": 1.1639519929885864,
    "clip_fraction": 0.00045085663441568613,
    "ratio_abs_mean": 0.007318818476051092,
    "seconds": 1.8068394912406802
  },
  "no_reduced_math_sdpa": {
    "n": 2218,
    "max": 0.2187938690185547,
    "mean": 0.00838546548038721,
    "p95": 0.0606086365878582,
    "ratio_min": 0.8034873008728027,
    "ratio_max": 1.2050873041152954,
    "clip_fraction": 0.00045085663441568613,
    "ratio_abs_mean": 0.008383814245462418,
    "seconds": 3.604113691020757
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1427,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 41.835834744852036
  },
  "no_reduced_bf16_accum": {
    "n": 1427,
    "max": 0.1840229034423828,
    "mean": 0.005101256538182497,
    "p95": 0.03766610845923424,
    "ratio_min": 0.8319167494773865,
    "ratio_max": 1.1227530241012573,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005064792465418577,
    "seconds": 1.1827070591971278
  },
  "no_reduced_math_sdpa": {
    "n": 1427,
    "max": 0.188385009765625,
    "mean": 0.005339649971574545,
    "p95": 0.03457723930478096,
    "ratio_min": 0.8282957673072815,
    "ratio_max": 1.1780587434768677,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005310504697263241,
    "seconds": 2.140427067875862
  },
  "matched_likelihood_gradient": {
    "actions": 187,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.30777621269226074,
    "fp32_loss": 0.35446980595588684,
    "cosine": 0.8131767109863463,
    "relative_l2": 0.5865962251850297,
    "fp32_norm": 9.545121450515607,
    "bf16_norm": 7.063607502196119,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51697809408,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2415,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 80.84689754294232
  },
  "no_reduced_bf16_accum": {
    "n": 2415,
    "max": 0.20808792114257812,
    "mean": 0.007063607219606638,
    "p95": 0.048496462404727936,
    "ratio_min": 0.8291888236999512,
    "ratio_max": 1.2313214540481567,
    "clip_fraction": 0.00041407867684029043,
    "ratio_abs_mean": 0.007056655827909708,
    "seconds": 1.4045582921244204
  },
  "no_reduced_math_sdpa": {
    "n": 2415,
    "max": 0.20299530029296875,
    "mean": 0.006621985230594873,
    "p95": 0.046650148928165436,
    "ratio_min": 0.8162820935249329,
    "ratio_max": 1.1425718069076538,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.006602610927075148,
    "seconds": 2.8484451891854405
  },
  "matched_likelihood_gradient": {
    "actions": 131,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.4674346148967743,
    "fp32_loss": 0.604005753993988,
    "cosine": 0.8146994371615348,
    "relative_l2": 0.594918970670469,
    "fp32_norm": 17.15843369385793,
    "bf16_norm": 11.698523639105959,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51694528512,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1653,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 51.12582642072812
  },
  "no_reduced_bf16_accum": {
    "n": 1653,
    "max": 0.12487030029296875,
    "mean": 0.007612011395394802,
    "p95": 0.05492058023810387,
    "ratio_min": 0.8884265422821045,
    "ratio_max": 1.133001446723938,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.007582842838019133,
    "seconds": 1.233372869901359
  },
  "no_reduced_math_sdpa": {
    "n": 1653,
    "max": 0.1971759796142578,
    "mean": 0.008143271319568157,
    "p95": 0.057400137186050415,
    "ratio_min": 0.8814185857772827,
    "ratio_max": 1.2179583311080933,
    "clip_fraction": 0.0006049606599844992,
    "ratio_abs_mean": 0.008103501982986927,
    "seconds": 2.2874839450232685
  },
  "matched_likelihood_gradient": {
    "actions": 116,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.5094447135925293,
    "fp32_loss": 0.6094920635223389,
    "cosine": 0.8202728623827352,
    "relative_l2": 0.5866565345694255,
    "fp32_norm": 17.803622469196053,
    "bf16_norm": 12.281601326974194,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51696301056,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1856,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 53.58585720229894
  },
  "no_reduced_bf16_accum": {
    "n": 1856,
    "max": 0.1677703857421875,
    "mean": 0.008682271465659142,
    "p95": 0.06518840789794922,
    "ratio_min": 0.8841632008552551,
    "ratio_max": 1.1826649904251099,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.008716858923435211,
    "seconds": 1.4788881284184754
  },
  "no_reduced_math_sdpa": {
    "n": 1856,
    "max": 0.2461986541748047,
    "mean": 0.00917220301926136,
    "p95": 0.07058286666870117,
    "ratio_min": 0.7817668914794922,
    "ratio_max": 1.1461338996887207,
    "clip_fraction": 0.0005387931014411151,
    "ratio_abs_mean": 0.00917468685656786,
    "seconds": 2.792898308020085
  },
  "matched_likelihood_gradient": {
    "actions": 163,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.5435050129890442,
    "fp32_loss": 0.7189908027648926,
    "cosine": 0.7588146052077988,
    "relative_l2": 0.6624773224339284,
    "fp32_norm": 16.790607263951603,
    "bf16_norm": 10.706880917590405,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51695962112,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1695,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 47.1431276560761
  },
  "no_reduced_bf16_accum": {
    "n": 1695,
    "max": 0.22608566284179688,
    "mean": 0.008175305090844631,
    "p95": 0.05287398025393486,
    "ratio_min": 0.8814303874969482,
    "ratio_max": 1.253683090209961,
    "clip_fraction": 0.0005899704992771149,
    "ratio_abs_mean": 0.008227004669606686,
    "seconds": 1.3046614597551525
  },
  "no_reduced_math_sdpa": {
    "n": 1695,
    "max": 0.20009803771972656,
    "mean": 0.008683828637003899,
    "p95": 0.06170841306447983,
    "ratio_min": 0.8710949420928955,
    "ratio_max": 1.2215224504470825,
    "clip_fraction": 0.0005899704992771149,
    "ratio_abs_mean": 0.008735244162380695,
    "seconds": 2.5188404959626496
  },
  "matched_likelihood_gradient": {
    "actions": 148,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.8017825484275818,
    "fp32_loss": 0.8734075427055359,
    "cosine": 0.8639212829748918,
    "relative_l2": 0.5057499369634428,
    "fp32_norm": 16.889700811872373,
    "bf16_norm": 13.809508008020646,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51693430784,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 1754,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 53.95013520680368
  },
  "no_reduced_bf16_accum": {
    "n": 1754,
    "max": 0.22924041748046875,
    "mean": 0.012275268323719501,
    "p95": 0.07768971472978592,
    "ratio_min": 0.795137345790863,
    "ratio_max": 1.1657227277755737,
    "clip_fraction": 0.0005701254121959209,
    "ratio_abs_mean": 0.012289630249142647,
    "seconds": 1.4111276199109852
  },
  "no_reduced_math_sdpa": {
    "n": 1754,
    "max": 0.2446441650390625,
    "mean": 0.012198041193187237,
    "p95": 0.07838386297225952,
    "ratio_min": 0.8663080930709839,
    "ratio_max": 1.277166724205017,
    "clip_fraction": 0.0005701254121959209,
    "ratio_abs_mean": 0.012209339067339897,
    "seconds": 2.610355088952929
  },
  "matched_likelihood_gradient": {
    "actions": 186,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.5144799947738647,
    "fp32_loss": 0.5966660976409912,
    "cosine": 0.8802999339689076,
    "relative_l2": 0.4868860619227991,
    "fp32_norm": 14.882343911053587,
    "bf16_norm": 11.4715977917597,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51693606912,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2165,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 64.95876739919186
  },
  "no_reduced_bf16_accum": {
    "n": 2165,
    "max": 0.1757965087890625,
    "mean": 0.005583602469414473,
    "p95": 0.03851243481040001,
    "ratio_min": 0.8826231360435486,
    "ratio_max": 1.1921954154968262,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.005595067050307989,
    "seconds": 1.4528761231340468
  },
  "no_reduced_math_sdpa": {
    "n": 2165,
    "max": 0.2579498291015625,
    "mean": 0.006018822081387043,
    "p95": 0.04232444614171982,
    "ratio_min": 0.8530122637748718,
    "ratio_max": 1.294273853302002,
    "clip_fraction": 0.0009237875347025692,
    "ratio_abs_mean": 0.006030121352523565,
    "seconds": 2.910650397185236
  },
  "matched_likelihood_gradient": {
    "actions": 110,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.6341524720191956,
    "fp32_loss": 0.7799887657165527,
    "cosine": 0.6735587413084981,
    "relative_l2": 0.7400588066037102,
    "fp32_norm": 19.22497365094638,
    "bf16_norm": 13.660321140069248,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51687781376,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/diagnostic/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "all_master_fp32": true,
  "native_source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "guard_thresholds_unchanged": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "same_shape_cached_replay": {
    "n": 2218,
    "max": 0.0,
    "mean": 0.0,
    "p95": 0.0,
    "ratio_min": 1.0,
    "ratio_max": 1.0,
    "clip_fraction": 0.0,
    "ratio_abs_mean": 0.0,
    "seconds": 67.33400574000552
  },
  "no_reduced_bf16_accum": {
    "n": 2218,
    "max": 0.2468128204345703,
    "mean": 0.0073055727407336235,
    "p95": 0.05544469878077507,
    "ratio_min": 0.781286895275116,
    "ratio_max": 1.1639519929885864,
    "clip_fraction": 0.00045085663441568613,
    "ratio_abs_mean": 0.007318818476051092,
    "seconds": 1.8068394912406802
  },
  "no_reduced_math_sdpa": {
    "n": 2218,
    "max": 0.2187938690185547,
    "mean": 0.00838546548038721,
    "p95": 0.0606086365878582,
    "ratio_min": 0.8034873008728027,
    "ratio_max": 1.2050873041152954,
    "clip_fraction": 0.00045085663441568613,
    "ratio_abs_mean": 0.008383814245462418,
    "seconds": 3.604113691020757
  },
  "matched_likelihood_gradient": {
    "actions": 95,
    "phase": "main",
    "objective": "negative mean raw sampled logprob, unit advantage; no PPO/Adam",
    "bf16_loss": 0.4549734890460968,
    "fp32_loss": 0.5951551198959351,
    "cosine": 0.7906005065135178,
    "relative_l2": 0.6141225075575981,
    "fp32_norm": 18.645263977915672,
    "bf16_norm": 13.867286701219987,
    "fp32_master": true
  },
  "peak_gpu_bytes": 51694338048,
  "optimizer_updates": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 8,
    "id": "bigmath/cn_k12/23250",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 434,
    "reference_F": 521,
    "generation_seconds": 17.219177848659456,
    "T": 573,
    "native_replay_max": 0.177825927734375,
    "native_replay_mean": 0.008498333394527435,
    "native_replay_p95": 0.06368406862020493,
    "phases": [
      {
        "phase": "main",
        "n": 166,
        "max": 0.12476921081542969,
        "mean": 0.0099031375721097,
        "p95": 0.061675071716308594
      },
      {
        "phase": "width",
        "n": 2,
        "max": 2.09808349609375e-05,
        "mean": 1.049041748046875e-05,
        "p95": 1.9931792849092744e-05
      },
      {
        "phase": "path",
        "n": 67,
        "max": 0.11289596557617188,
        "mean": 0.009179727174341679,
        "p95": 0.06118413433432579
      },
      {
        "phase": "path",
        "n": 72,
        "max": 0.177825927734375,
        "mean": 0.01015061791986227,
        "p95": 0.0914594903588295
      },
      {
        "phase": "path",
        "n": 110,
        "max": 0.12278366088867188,
        "mean": 0.007354337722063065,
        "p95": 0.05670604854822159
      },
      {
        "phase": "summary",
        "n": 80,
        "max": 0.12385940551757812,
        "mean": 0.0069779157638549805,
        "p95": 0.0523533821105957
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 74,
        "max": 0.07079315185546875,
        "mean": 0.006925737485289574,
        "p95": 0.05515306070446968
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 9,
    "id": "bigmath/cn_k12/64731",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 798,
    "reference_F": 2172,
    "generation_seconds": 32.791218681726605,
    "T": 1185,
    "native_replay_max": 0.2081623077392578,
    "native_replay_mean": 0.005566335283219814,
    "native_replay_p95": 0.035197824239730835,
    "phases": [
      {
        "phase": "main",
        "n": 155,
        "max": 0.12133026123046875,
        "mean": 0.008461367338895798,
        "p95": 0.05665874481201172
      },
      {
        "phase": "width",
        "n": 2,
        "max": 9.34600830078125e-05,
        "mean": 4.673004150390625e-05,
        "p95": 8.878707740223035e-05
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.10093879699707031,
        "mean": 0.0026537703815847635,
        "p95": 0.013078499585390091
      },
      {
        "phase": "path",
        "n": 316,
        "max": 0.12126541137695312,
        "mean": 0.0030318512581288815,
        "p95": 0.022129058837890625
      },
      {
        "phase": "path",
        "n": 102,
        "max": 0.2081623077392578,
        "mean": 0.007303162943571806,
        "p95": 0.034736987203359604
      },
      {
        "phase": "path",
        "n": 135,
        "max": 0.09843635559082031,
        "mean": 0.005150858778506517,
        "p95": 0.02644708752632141
      },
      {
        "phase": "summary",
        "n": 152,
        "max": 0.10103416442871094,
        "mean": 0.007566075772047043,
        "p95": 0.05875147879123688
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.002117156982421875,
        "mean": 0.0010585784912109375,
        "p95": 0.0020112991333007812
      },
      {
        "phase": "main",
        "n": 171,
        "max": 0.1763629913330078,
        "mean": 0.007812410593032837,
        "p95": 0.049126625061035156
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 10,
    "id": "bigmath/cn_k12/204933",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 779,
    "reference_F": 764,
    "generation_seconds": 32.88241997174919,
    "T": 1039,
    "native_replay_max": 0.1332111358642578,
    "native_replay_mean": 0.007618289906531572,
    "native_replay_p95": 0.056174635887145996,
    "phases": [
      {
        "phase": "main",
        "n": 208,
        "max": 0.108062744140625,
        "mean": 0.006690648850053549,
        "p95": 0.03832544758915901
      },
      {
        "phase": "width",
        "n": 2,
        "max": 0.000141143798828125,
        "mean": 7.05718994140625e-05,
        "p95": 0.0001340866001555696
      },
      {
        "phase": "path",
        "n": 125,
        "max": 0.11722373962402344,
        "mean": 0.006839508190751076,
        "p95": 0.04477538540959358
      },
      {
        "phase": "path",
        "n": 258,
        "max": 0.1332111358642578,
        "mean": 0.008589308708906174,
        "p95": 0.05732392519712448
      },
      {
        "phase": "path",
        "n": 135,
        "max": 0.10712814331054688,
        "mean": 0.004634828772395849,
        "p95": 0.026513271033763885
      },
      {
        "phase": "summary",
        "n": 217,
        "max": 0.11798095703125,
        "mean": 0.010576002299785614,
        "p95": 0.06587256491184235
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.4332275390625e-05,
        "mean": 1.71661376953125e-05,
        "p95": 3.261566234868951e-05
      },
      {
        "phase": "main",
        "n": 92,
        "max": 0.09281349182128906,
        "mean": 0.005781505256891251,
        "p95": 0.03872406482696533
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 11,
    "id": "bigmath/cn_k12/147481",
    "correct": true,
    "reference_correct": true,
    "format_valid": false,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 890,
    "reference_F": 1086,
    "generation_seconds": 37.96232661418617,
    "T": 1379,
    "native_replay_max": 0.20189857482910156,
    "native_replay_mean": 0.009368445724248886,
    "native_replay_p95": 0.06808065623044968,
    "phases": [
      {
        "phase": "main",
        "n": 348,
        "max": 0.12311744689941406,
        "mean": 0.012601874768733978,
        "p95": 0.07454288005828857
      },
      {
        "phase": "width",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "path",
        "n": 183,
        "max": 0.12430572509765625,
        "mean": 0.004136247094720602,
        "p95": 0.03809183090925217
      },
      {
        "phase": "path",
        "n": 110,
        "max": 0.20189857482910156,
        "mean": 0.011704531498253345,
        "p95": 0.07131105661392212
      },
      {
        "phase": "path",
        "n": 196,
        "max": 0.10903549194335938,
        "mean": 0.00714215449988842,
        "p95": 0.058293819427490234
      },
      {
        "phase": "path",
        "n": 278,
        "max": 0.1677703857421875,
        "mean": 0.01101626269519329,
        "p95": 0.07938049733638763
      },
      {
        "phase": "summary",
        "n": 194,
        "max": 0.1481342315673828,
        "mean": 0.009747485630214214,
        "p95": 0.07056168466806412
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "main",
        "n": 66,
        "max": 0.07594108581542969,
        "mean": 0.002057624515146017,
        "p95": 0.008872032165527344
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 12,
    "id": "bigmath/cn_k12/61311",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 674,
    "reference_F": 952,
    "generation_seconds": 27.956692113075405,
    "T": 1054,
    "native_replay_max": 0.15840530395507812,
    "native_replay_mean": 0.007076160050928593,
    "native_replay_p95": 0.04722508043050766,
    "phases": [
      {
        "phase": "main",
        "n": 110,
        "max": 0.09157180786132812,
        "mean": 0.008096469566226006,
        "p95": 0.04986445978283882
      },
      {
        "phase": "width",
        "n": 2,
        "max": 0.00022125244140625,
        "mean": 0.000110626220703125,
        "p95": 0.0002101898135151714
      },
      {
        "phase": "path",
        "n": 244,
        "max": 0.14151763916015625,
        "mean": 0.007984857074916363,
        "p95": 0.05572599917650223
      },
      {
        "phase": "path",
        "n": 197,
        "max": 0.1170501708984375,
        "mean": 0.0070169903337955475,
        "p95": 0.04992293938994408
      },
      {
        "phase": "path",
        "n": 183,
        "max": 0.15840530395507812,
        "mean": 0.004691129084676504,
        "p95": 0.03186453878879547
      },
      {
        "phase": "summary",
        "n": 219,
        "max": 0.11620140075683594,
        "mean": 0.008369680494070053,
        "p95": 0.047709640115499496
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.006153106689453125,
        "mean": 0.0030765533447265625,
        "p95": 0.005845451261848211
      },
      {
        "phase": "main",
        "n": 97,
        "max": 0.10056495666503906,
        "mean": 0.0055587412789464,
        "p95": 0.031352218240499496
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 13,
    "id": "bigmath/cn_k12/155313",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 448,
    "reference_F": 921,
    "generation_seconds": 17.739986462984234,
    "T": 558,
    "native_replay_max": 0.12000846862792969,
    "native_replay_mean": 0.010707725770771503,
    "native_replay_p95": 0.07222211360931396,
    "phases": [
      {
        "phase": "main",
        "n": 219,
        "max": 0.11519050598144531,
        "mean": 0.009599127806723118,
        "p95": 0.06171083077788353
      },
      {
        "phase": "width",
        "n": 2,
        "max": 0.0002613067626953125,
        "mean": 0.00013065338134765625,
        "p95": 0.0002482414129190147
      },
      {
        "phase": "path",
        "n": 71,
        "max": 0.11787223815917969,
        "mean": 0.015771087259054184,
        "p95": 0.08876419067382812
      },
      {
        "phase": "path",
        "n": 103,
        "max": 0.11020851135253906,
        "mean": 0.00907240528613329,
        "p95": 0.064436174929142
      },
      {
        "phase": "path",
        "n": 39,
        "max": 0.03758049011230469,
        "mean": 0.005220315419137478,
        "p95": 0.033132363110780716
      },
      {
        "phase": "summary",
        "n": 50,
        "max": 0.12000846862792969,
        "mean": 0.018596230074763298,
        "p95": 0.09017818421125412
      },
      {
        "phase": "main",
        "n": 2,
        "max": 7.62939453125e-06,
        "mean": 3.814697265625e-06,
        "p95": 7.24792471373803e-06
      },
      {
        "phase": "main",
        "n": 72,
        "max": 0.10479736328125,
        "mean": 0.009511444717645645,
        "p95": 0.06432272493839264
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 14,
    "id": "bigmath/cn_k12/95257",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1133,
    "reference_F": 1763,
    "generation_seconds": 45.51130814803764,
    "T": 1536,
    "native_replay_max": 0.2070751190185547,
    "native_replay_mean": 0.00515118008479476,
    "native_replay_p95": 0.03294849395751953,
    "phases": [
      {
        "phase": "main",
        "n": 226,
        "max": 0.2070751190185547,
        "mean": 0.008100408129394054,
        "p95": 0.04355669021606445
      },
      {
        "phase": "width",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "path",
        "n": 137,
        "max": 0.12194061279296875,
        "mean": 0.0034686040598899126,
        "p95": 0.015995781868696213
      },
      {
        "phase": "path",
        "n": 110,
        "max": 0.17406463623046875,
        "mean": 0.00577813945710659,
        "p95": 0.04037035256624222
      },
      {
        "phase": "path",
        "n": 156,
        "max": 0.1191864013671875,
        "mean": 0.00423184409737587,
        "p95": 0.020495891571044922
      },
      {
        "phase": "path",
        "n": 201,
        "max": 0.11437225341796875,
        "mean": 0.003316110698506236,
        "p95": 0.019151687622070312
      },
      {
        "phase": "summary",
        "n": 618,
        "max": 0.11937713623046875,
        "mean": 0.005236344877630472,
        "p95": 0.03520926460623741
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.017669677734375,
        "mean": 0.0088348388671875,
        "p95": 0.01678619347512722
      },
      {
        "phase": "main",
        "n": 84,
        "max": 0.054309844970703125,
        "mean": 0.004646255634725094,
        "p95": 0.03092021495103836
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 15,
    "id": "bigmath/cn_k12/3177",
    "correct": false,
    "reference_correct": false,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 614,
    "reference_F": 724,
    "generation_seconds": 24.61308516608551,
    "T": 963,
    "native_replay_max": 0.12459373474121094,
    "native_replay_mean": 0.005775426048785448,
    "native_replay_p95": 0.039630115032196045,
    "phases": [
      {
        "phase": "main",
        "n": 160,
        "max": 0.11716079711914062,
        "mean": 0.005128311924636364,
        "p95": 0.03417092561721802
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "path",
        "n": 108,
        "max": 0.09683990478515625,
        "mean": 0.006510999519377947,
        "p95": 0.04982509836554527
      },
      {
        "phase": "path",
        "n": 91,
        "max": 0.12459373474121094,
        "mean": 0.007541803177446127,
        "p95": 0.04903411865234375
      },
      {
        "phase": "path",
        "n": 233,
        "max": 0.1077423095703125,
        "mean": 0.0038457715418189764,
        "p95": 0.024288136512041092
      },
      {
        "phase": "path",
        "n": 150,
        "max": 0.12293624877929688,
        "mean": 0.0058410135097801685,
        "p95": 0.039527323096990585
      },
      {
        "phase": "summary",
        "n": 160,
        "max": 0.12194633483886719,
        "mean": 0.005733168218284845,
        "p95": 0.030421266332268715
      },
      {
        "phase": "main",
        "n": 2,
        "max": 5.7220458984375e-06,
        "mean": 2.86102294921875e-06,
        "p95": 5.435943421616685e-06
      },
      {
        "phase": "main",
        "n": 57,
        "max": 0.11877059936523438,
        "mean": 0.011617225594818592,
        "p95": 0.07873192429542542
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 414, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(414, 414)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 415)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(4, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 600, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(600, 600)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 187, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 602, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(602, 602)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8370881080627441,
  "ratio_max": 1.1334272623062134,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.005666808225214481,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 0,
      "id": "bigmath/cn_k12/26444",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 552,
      "reference_F": 752,
      "generation_seconds": 22.805812689010054,
      "T": 854,
      "native_replay_max": 0.1252460479736328,
      "native_replay_mean": 0.00382494879886508,
      "native_replay_p95": 0.02169646881520748,
      "phases": [
        {
          "phase": "main",
          "n": 187,
          "max": 0.1252460479736328,
          "mean": 0.006502783857285976,
          "p95": 0.038086116313934326
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0001163482666015625,
          "mean": 5.817413330078125e-05,
          "p95": 0.0001105308547266759
        },
        {
          "phase": "path",
          "n": 79,
          "max": 0.04724311828613281,
          "mean": 0.0019904752261936665,
          "p95": 0.017024990171194077
        },
        {
          "phase": "path",
          "n": 74,
          "max": 0.08092498779296875,
          "mean": 0.003478127531707287,
          "p95": 0.013628276064991951
        },
        {
          "phase": "path",
          "n": 149,
          "max": 0.10113143920898438,
          "mean": 0.0024733704049140215,
          "p95": 0.00822486449033022
        },
        {
          "phase": "path",
          "n": 226,
          "max": 0.123565673828125,
          "mean": 0.002970442408695817,
          "p95": 0.013947486877441406
        },
        {
          "phase": "summary",
          "n": 80,
          "max": 0.10809898376464844,
          "mean": 0.005451989360153675,
          "p95": 0.04130464047193527
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 55,
          "max": 0.05657196044921875,
          "mean": 0.0029041289817541838,
          "p95": 0.017522985115647316
        }
      ]
    },
    {
      "index": 8,
      "id": "bigmath/cn_k12/23250",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 434,
      "reference_F": 521,
      "generation_seconds": 17.219177848659456,
      "T": 573,
      "native_replay_max": 0.177825927734375,
      "native_replay_mean": 0.008498333394527435,
      "native_replay_p95": 0.06368406862020493,
      "phases": [
        {
          "phase": "main",
          "n": 166,
          "max": 0.12476921081542969,
          "mean": 0.0099031375721097,
          "p95": 0.061675071716308594
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 67,
          "max": 0.11289596557617188,
          "mean": 0.009179727174341679,
          "p95": 0.06118413433432579
        },
        {
          "phase": "path",
          "n": 72,
          "max": 0.177825927734375,
          "mean": 0.01015061791986227,
          "p95": 0.0914594903588295
        },
        {
          "phase": "path",
          "n": 110,
          "max": 0.12278366088867188,
          "mean": 0.007354337722063065,
          "p95": 0.05670604854822159
        },
        {
          "phase": "summary",
          "n": 80,
          "max": 0.12385940551757812,
          "mean": 0.0069779157638549805,
          "p95": 0.0523533821105957
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 74,
          "max": 0.07079315185546875,
          "mean": 0.006925737485289574,
          "p95": 0.05515306070446968
        }
      ]
    }
  ],
  "actions": 1427,
  "native_replay_max": 0.177825927734375,
  "native_replay_mean": 0.005701507441699505,
  "native_replay_p95": 0.041286468505859375,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25179694592,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 418, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(418, 418)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 419)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(2, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 548, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(548, 548)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 131, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 550, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(550, 550)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8193894028663635,
  "ratio_max": 1.2314130067825317,
  "ratio_outside_clip_fraction": 0.00041407867684029043,
  "ratio_abs_mean": 0.0070798397064208984,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 1,
      "id": "bigmath/cn_k12/88253",
      "correct": false,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1164,
      "reference_F": 1344,
      "generation_seconds": 50.57821628404781,
      "T": 1230,
      "native_replay_max": 0.19919586181640625,
      "native_replay_mean": 0.00855953712016344,
      "native_replay_p95": 0.0628810003399849,
      "phases": [
        {
          "phase": "main",
          "n": 131,
          "max": 0.12456512451171875,
          "mean": 0.009619254618883133,
          "p95": 0.06251335144042969
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 66,
          "max": 0.11583328247070312,
          "mean": 0.007167440373450518,
          "p95": 0.055078983306884766
        },
        {
          "phase": "path",
          "n": 177,
          "max": 0.11487388610839844,
          "mean": 0.00667899614199996,
          "p95": 0.054005421698093414
        },
        {
          "phase": "summary",
          "n": 797,
          "max": 0.19919586181640625,
          "mean": 0.00938351359218359,
          "p95": 0.06709175556898117
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 55,
          "max": 0.053447723388671875,
          "mean": 0.002440157812088728,
          "p95": 0.01746443845331669
        }
      ]
    },
    {
      "index": 9,
      "id": "bigmath/cn_k12/64731",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 798,
      "reference_F": 2172,
      "generation_seconds": 32.791218681726605,
      "T": 1185,
      "native_replay_max": 0.2081623077392578,
      "native_replay_mean": 0.005566335283219814,
      "native_replay_p95": 0.035197824239730835,
      "phases": [
        {
          "phase": "main",
          "n": 155,
          "max": 0.12133026123046875,
          "mean": 0.008461367338895798,
          "p95": 0.05665874481201172
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.34600830078125e-05,
          "mean": 4.673004150390625e-05,
          "p95": 8.878707740223035e-05
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.10093879699707031,
          "mean": 0.0026537703815847635,
          "p95": 0.013078499585390091
        },
        {
          "phase": "path",
          "n": 316,
          "max": 0.12126541137695312,
          "mean": 0.0030318512581288815,
          "p95": 0.022129058837890625
        },
        {
          "phase": "path",
          "n": 102,
          "max": 0.2081623077392578,
          "mean": 0.007303162943571806,
          "p95": 0.034736987203359604
        },
        {
          "phase": "path",
          "n": 135,
          "max": 0.09843635559082031,
          "mean": 0.005150858778506517,
          "p95": 0.02644708752632141
        },
        {
          "phase": "summary",
          "n": 152,
          "max": 0.10103416442871094,
          "mean": 0.007566075772047043,
          "p95": 0.05875147879123688
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.002117156982421875,
          "mean": 0.0010585784912109375,
          "p95": 0.0020112991333007812
        },
        {
          "phase": "main",
          "n": 171,
          "max": 0.1763629913330078,
          "mean": 0.007812410593032837,
          "p95": 0.049126625061035156
        }
      ]
    }
  ],
  "actions": 2415,
  "native_replay_max": 0.2081623077392578,
  "native_replay_mean": 0.007090823259204626,
  "native_replay_p95": 0.0526006780564785,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25537376256,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 411, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(411, 411)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 412)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(4, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 526, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(526, 526)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 116, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 528, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(528, 528)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8752802610397339,
  "ratio_max": 1.1857458353042603,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.007856597192585468,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 2,
      "id": "bigmath/cn_k12/163846",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 432,
      "reference_F": 463,
      "generation_seconds": 18.462784834206104,
      "T": 614,
      "native_replay_max": 0.17037200927734375,
      "native_replay_mean": 0.008262566290795803,
      "native_replay_p95": 0.05753101408481598,
      "phases": [
        {
          "phase": "main",
          "n": 116,
          "max": 0.10113716125488281,
          "mean": 0.007205338217318058,
          "p95": 0.05180215835571289
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 23,
          "max": 0.09555625915527344,
          "mean": 0.016244225203990936,
          "p95": 0.08321132510900497
        },
        {
          "phase": "path",
          "n": 77,
          "max": 0.10503387451171875,
          "mean": 0.00847893301397562,
          "p95": 0.06371644139289856
        },
        {
          "phase": "path",
          "n": 130,
          "max": 0.1160888671875,
          "mean": 0.008967957459390163,
          "p95": 0.04999691620469093
        },
        {
          "phase": "path",
          "n": 82,
          "max": 0.07117462158203125,
          "mean": 0.005181452259421349,
          "p95": 0.03712678700685501
        },
        {
          "phase": "summary",
          "n": 97,
          "max": 0.17037200927734375,
          "mean": 0.008376367390155792,
          "p95": 0.058169834315776825
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.71661376953125e-05,
          "mean": 8.58306884765625e-06,
          "p95": 1.6307831174344756e-05
        },
        {
          "phase": "main",
          "n": 85,
          "max": 0.11935997009277344,
          "mean": 0.009501759894192219,
          "p95": 0.05966566130518913
        }
      ]
    },
    {
      "index": 10,
      "id": "bigmath/cn_k12/204933",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 779,
      "reference_F": 764,
      "generation_seconds": 32.88241997174919,
      "T": 1039,
      "native_replay_max": 0.1332111358642578,
      "native_replay_mean": 0.007618289906531572,
      "native_replay_p95": 0.056174635887145996,
      "phases": [
        {
          "phase": "main",
          "n": 208,
          "max": 0.108062744140625,
          "mean": 0.006690648850053549,
          "p95": 0.03832544758915901
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.000141143798828125,
          "mean": 7.05718994140625e-05,
          "p95": 0.0001340866001555696
        },
        {
          "phase": "path",
          "n": 125,
          "max": 0.11722373962402344,
          "mean": 0.006839508190751076,
          "p95": 0.04477538540959358
        },
        {
          "phase": "path",
          "n": 258,
          "max": 0.1332111358642578,
          "mean": 0.008589308708906174,
          "p95": 0.05732392519712448
        },
        {
          "phase": "path",
          "n": 135,
          "max": 0.10712814331054688,
          "mean": 0.004634828772395849,
          "p95": 0.026513271033763885
        },
        {
          "phase": "summary",
          "n": 217,
          "max": 0.11798095703125,
          "mean": 0.010576002299785614,
          "p95": 0.06587256491184235
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.4332275390625e-05,
          "mean": 1.71661376953125e-05,
          "p95": 3.261566234868951e-05
        },
        {
          "phase": "main",
          "n": 92,
          "max": 0.09281349182128906,
          "mean": 0.005781505256891251,
          "p95": 0.03872406482696533
        }
      ]
    }
  ],
  "actions": 1653,
  "native_replay_max": 0.17037200927734375,
  "native_replay_mean": 0.007857603952288628,
  "native_replay_p95": 0.056871041655540466,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25049239040,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 387, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(387, 387)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 388)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(2, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 549, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(549, 549)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 163, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 551, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(551, 551)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8171778321266174,
  "ratio_max": 1.1826649904251099,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.00923959817737341,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 3,
      "id": "bigmath/cn_k12/210293",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 410,
      "reference_F": 710,
      "generation_seconds": 18.06925299623981,
      "T": 477,
      "native_replay_max": 0.12591171264648438,
      "native_replay_mean": 0.008714688010513783,
      "native_replay_p95": 0.06690478324890137,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.12591171264648438,
          "mean": 0.012582112103700638,
          "p95": 0.09263511747121811
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "path",
          "n": 83,
          "max": 0.07512474060058594,
          "mean": 0.004697639029473066,
          "p95": 0.03436071053147316
        },
        {
          "phase": "path",
          "n": 67,
          "max": 0.09834861755371094,
          "mean": 0.004133594688028097,
          "p95": 0.019539646804332733
        },
        {
          "phase": "summary",
          "n": 88,
          "max": 0.12257003784179688,
          "mean": 0.01219580415636301,
          "p95": 0.08273811638355255
        },
        {
          "phase": "main",
          "n": 2,
          "max": 2.47955322265625e-05,
          "mean": 1.239776611328125e-05,
          "p95": 2.3555754523840733e-05
        },
        {
          "phase": "main",
          "n": 72,
          "max": 0.07387542724609375,
          "mean": 0.00508210388943553,
          "p95": 0.030751880258321762
        }
      ]
    },
    {
      "index": 11,
      "id": "bigmath/cn_k12/147481",
      "correct": true,
      "reference_correct": true,
      "format_valid": false,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 890,
      "reference_F": 1086,
      "generation_seconds": 37.96232661418617,
      "T": 1379,
      "native_replay_max": 0.20189857482910156,
      "native_replay_mean": 0.009368445724248886,
      "native_replay_p95": 0.06808065623044968,
      "phases": [
        {
          "phase": "main",
          "n": 348,
          "max": 0.12311744689941406,
          "mean": 0.012601874768733978,
          "p95": 0.07454288005828857
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 183,
          "max": 0.12430572509765625,
          "mean": 0.004136247094720602,
          "p95": 0.03809183090925217
        },
        {
          "phase": "path",
          "n": 110,
          "max": 0.20189857482910156,
          "mean": 0.011704531498253345,
          "p95": 0.07131105661392212
        },
        {
          "phase": "path",
          "n": 196,
          "max": 0.10903549194335938,
          "mean": 0.00714215449988842,
          "p95": 0.058293819427490234
        },
        {
          "phase": "path",
          "n": 278,
          "max": 0.1677703857421875,
          "mean": 0.01101626269519329,
          "p95": 0.07938049733638763
        },
        {
          "phase": "summary",
          "n": 194,
          "max": 0.1481342315673828,
          "mean": 0.009747485630214214,
          "p95": 0.07056168466806412
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 66,
          "max": 0.07594108581542969,
          "mean": 0.002057624515146017,
          "p95": 0.008872032165527344
        }
      ]
    }
  ],
  "actions": 1856,
  "native_replay_max": 0.20189857482910156,
  "native_replay_mean": 0.009200426749885082,
  "native_replay_p95": 0.06811714172363281,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25404784640,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 427, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(427, 427)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 428)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(4, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 574, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(574, 574)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 148, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 576, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(576, 576)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8822579383850098,
  "ratio_max": 1.1796889305114746,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.008347657509148121,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 4,
      "id": "bigmath/cn_k12/88674",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 465,
      "reference_F": 2255,
      "generation_seconds": 19.86216636793688,
      "T": 641,
      "native_replay_max": 0.1652507781982422,
      "native_replay_mean": 0.010341200977563858,
      "native_replay_p95": 0.07014846801757812,
      "phases": [
        {
          "phase": "main",
          "n": 148,
          "max": 0.11371421813964844,
          "mean": 0.010502016171813011,
          "p95": 0.049932096153497696
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.86102294921875e-05,
          "mean": 1.430511474609375e-05,
          "p95": 2.7179718017578125e-05
        },
        {
          "phase": "path",
          "n": 85,
          "max": 0.10788345336914062,
          "mean": 0.007821520790457726,
          "p95": 0.039240606129169464
        },
        {
          "phase": "path",
          "n": 76,
          "max": 0.12274169921875,
          "mean": 0.011239352636039257,
          "p95": 0.0716409683227539
        },
        {
          "phase": "path",
          "n": 54,
          "max": 0.1140594482421875,
          "mean": 0.020207157358527184,
          "p95": 0.10539931803941727
        },
        {
          "phase": "path",
          "n": 46,
          "max": 0.11581230163574219,
          "mean": 0.009291856549680233,
          "p95": 0.04920244216918945
        },
        {
          "phase": "summary",
          "n": 149,
          "max": 0.12527084350585938,
          "mean": 0.009970773942768574,
          "p95": 0.06781996786594391
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.52587890625e-05,
          "mean": 7.62939453125e-06,
          "p95": 1.449584942747606e-05
        },
        {
          "phase": "main",
          "n": 79,
          "max": 0.1652507781982422,
          "mean": 0.006975825875997543,
          "p95": 0.037360940128564835
        }
      ]
    },
    {
      "index": 12,
      "id": "bigmath/cn_k12/61311",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 674,
      "reference_F": 952,
      "generation_seconds": 27.956692113075405,
      "T": 1054,
      "native_replay_max": 0.15840530395507812,
      "native_replay_mean": 0.007076160050928593,
      "native_replay_p95": 0.04722508043050766,
      "phases": [
        {
          "phase": "main",
          "n": 110,
          "max": 0.09157180786132812,
          "mean": 0.008096469566226006,
          "p95": 0.04986445978283882
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.00022125244140625,
          "mean": 0.000110626220703125,
          "p95": 0.0002101898135151714
        },
        {
          "phase": "path",
          "n": 244,
          "max": 0.14151763916015625,
          "mean": 0.007984857074916363,
          "p95": 0.05572599917650223
        },
        {
          "phase": "path",
          "n": 197,
          "max": 0.1170501708984375,
          "mean": 0.0070169903337955475,
          "p95": 0.04992293938994408
        },
        {
          "phase": "path",
          "n": 183,
          "max": 0.15840530395507812,
          "mean": 0.004691129084676504,
          "p95": 0.03186453878879547
        },
        {
          "phase": "summary",
          "n": 219,
          "max": 0.11620140075683594,
          "mean": 0.008369680494070053,
          "p95": 0.047709640115499496
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.006153106689453125,
          "mean": 0.0030765533447265625,
          "p95": 0.005845451261848211
        },
        {
          "phase": "main",
          "n": 97,
          "max": 0.10056495666503906,
          "mean": 0.0055587412789464,
          "p95": 0.031352218240499496
        }
      ]
    }
  ],
  "actions": 1695,
  "native_replay_max": 0.1652507781982422,
  "native_replay_mean": 0.00831090472638607,
  "native_replay_p95": 0.05419938638806343,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25110887936,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 383, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(383, 383)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 384)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(7, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 568, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(568, 568)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 186, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 570, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(570, 570)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8339327573776245,
  "ratio_max": 1.1346558332443237,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.011045076884329319,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 5,
      "id": "bigmath/cn_k12/165159",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 917,
      "reference_F": 540,
      "generation_seconds": 37.9710245821625,
      "T": 1196,
      "native_replay_max": 0.18160247802734375,
      "native_replay_mean": 0.011160360649228096,
      "native_replay_p95": 0.06916618347167969,
      "phases": [
        {
          "phase": "main",
          "n": 186,
          "max": 0.09195709228515625,
          "mean": 0.007660373579710722,
          "p95": 0.06060171127319336
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0001373291015625,
          "mean": 6.866455078125e-05,
          "p95": 0.00013046264939475805
        },
        {
          "phase": "path",
          "n": 53,
          "max": 0.06143760681152344,
          "mean": 0.008835810236632824,
          "p95": 0.05262717232108116
        },
        {
          "phase": "path",
          "n": 84,
          "max": 0.1263294219970703,
          "mean": 0.014840307645499706,
          "p95": 0.08400991559028625
        },
        {
          "phase": "path",
          "n": 56,
          "max": 0.11875724792480469,
          "mean": 0.012208836153149605,
          "p95": 0.06038188934326172
        },
        {
          "phase": "path",
          "n": 33,
          "max": 0.05291748046875,
          "mean": 0.0052623748779296875,
          "p95": 0.031981270760297775
        },
        {
          "phase": "path",
          "n": 49,
          "max": 0.11156272888183594,
          "mean": 0.00838707946240902,
          "p95": 0.06376379728317261
        },
        {
          "phase": "path",
          "n": 56,
          "max": 0.18160247802734375,
          "mean": 0.014403547160327435,
          "p95": 0.0731353759765625
        },
        {
          "phase": "path",
          "n": 32,
          "max": 0.11988639831542969,
          "mean": 0.01327669620513916,
          "p95": 0.061181217432022095
        },
        {
          "phase": "summary",
          "n": 524,
          "max": 0.12364387512207031,
          "mean": 0.012523028999567032,
          "p95": 0.07157555222511292
        },
        {
          "phase": "main",
          "n": 2,
          "max": 8.7738037109375e-05,
          "mean": 4.38690185546875e-05,
          "p95": 8.335113670909777e-05
        },
        {
          "phase": "main",
          "n": 119,
          "max": 0.12277984619140625,
          "mean": 0.009630363434553146,
          "p95": 0.08619613200426102
        }
      ]
    },
    {
      "index": 13,
      "id": "bigmath/cn_k12/155313",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 448,
      "reference_F": 921,
      "generation_seconds": 17.739986462984234,
      "T": 558,
      "native_replay_max": 0.12000846862792969,
      "native_replay_mean": 0.010707725770771503,
      "native_replay_p95": 0.07222211360931396,
      "phases": [
        {
          "phase": "main",
          "n": 219,
          "max": 0.11519050598144531,
          "mean": 0.009599127806723118,
          "p95": 0.06171083077788353
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0002613067626953125,
          "mean": 0.00013065338134765625,
          "p95": 0.0002482414129190147
        },
        {
          "phase": "path",
          "n": 71,
          "max": 0.11787223815917969,
          "mean": 0.015771087259054184,
          "p95": 0.08876419067382812
        },
        {
          "phase": "path",
          "n": 103,
          "max": 0.11020851135253906,
          "mean": 0.00907240528613329,
          "p95": 0.064436174929142
        },
        {
          "phase": "path",
          "n": 39,
          "max": 0.03758049011230469,
          "mean": 0.005220315419137478,
          "p95": 0.033132363110780716
        },
        {
          "phase": "summary",
          "n": 50,
          "max": 0.12000846862792969,
          "mean": 0.018596230074763298,
          "p95": 0.09017818421125412
        },
        {
          "phase": "main",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "main",
          "n": 72,
          "max": 0.10479736328125,
          "mean": 0.009511444717645645,
          "p95": 0.06432272493839264
        }
      ]
    }
  ],
  "actions": 1754,
  "native_replay_max": 0.18160247802734375,
  "native_replay_mean": 0.011016364209353924,
  "native_replay_p95": 0.07097320258617401,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25707317760,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 387, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(387, 387)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 388)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(3, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 496, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(496, 496)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 110, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 498, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(498, 498)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8129585981369019,
  "ratio_max": 1.19013249874115,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.005765193607658148,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 6,
      "id": "bigmath/cn_k12/176142",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 468,
      "reference_F": 710,
      "generation_seconds": 20.1417102990672,
      "T": 629,
      "native_replay_max": 0.158447265625,
      "native_replay_mean": 0.0072681233286857605,
      "native_replay_p95": 0.05380432680249214,
      "phases": [
        {
          "phase": "main",
          "n": 110,
          "max": 0.1484375,
          "mean": 0.0159896332770586,
          "p95": 0.08774518221616745
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0001697540283203125,
          "mean": 8.487701416015625e-05,
          "p95": 0.00016126631817314774
        },
        {
          "phase": "path",
          "n": 183,
          "max": 0.10347747802734375,
          "mean": 0.004104228690266609,
          "p95": 0.038846179842948914
        },
        {
          "phase": "path",
          "n": 52,
          "max": 0.0724029541015625,
          "mean": 0.00343003636226058,
          "p95": 0.014218054711818695
        },
        {
          "phase": "path",
          "n": 109,
          "max": 0.158447265625,
          "mean": 0.008459178730845451,
          "p95": 0.06548690050840378
        },
        {
          "phase": "summary",
          "n": 84,
          "max": 0.1118927001953125,
          "mean": 0.006004991941154003,
          "p95": 0.04228438064455986
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 87,
          "max": 0.10549545288085938,
          "mean": 0.005249571520835161,
          "p95": 0.03593764081597328
        }
      ]
    },
    {
      "index": 14,
      "id": "bigmath/cn_k12/95257",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1133,
      "reference_F": 1763,
      "generation_seconds": 45.51130814803764,
      "T": 1536,
      "native_replay_max": 0.2070751190185547,
      "native_replay_mean": 0.00515118008479476,
      "native_replay_p95": 0.03294849395751953,
      "phases": [
        {
          "phase": "main",
          "n": 226,
          "max": 0.2070751190185547,
          "mean": 0.008100408129394054,
          "p95": 0.04355669021606445
        },
        {
          "phase": "width",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "path",
          "n": 137,
          "max": 0.12194061279296875,
          "mean": 0.0034686040598899126,
          "p95": 0.015995781868696213
        },
        {
          "phase": "path",
          "n": 110,
          "max": 0.17406463623046875,
          "mean": 0.00577813945710659,
          "p95": 0.04037035256624222
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.1191864013671875,
          "mean": 0.00423184409737587,
          "p95": 0.020495891571044922
        },
        {
          "phase": "path",
          "n": 201,
          "max": 0.11437225341796875,
          "mean": 0.003316110698506236,
          "p95": 0.019151687622070312
        },
        {
          "phase": "summary",
          "n": 618,
          "max": 0.11937713623046875,
          "mean": 0.005236344877630472,
          "p95": 0.03520926460623741
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.017669677734375,
          "mean": 0.0088348388671875,
          "p95": 0.01678619347512722
        },
        {
          "phase": "main",
          "n": 84,
          "max": 0.054309844970703125,
          "mean": 0.004646255634725094,
          "p95": 0.03092021495103836
        }
      ]
    }
  ],
  "actions": 2165,
  "native_replay_max": 0.2070751190185547,
  "native_replay_mean": 0.005766218062490225,
  "native_replay_p95": 0.0404064767062664,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25271628288,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "precision": "bf16_full_autocast",
  "master_dtype": "float32",
  "lm_head_dtype": "bfloat16",
  "dtype_receipt": {
    "generation:q_proj:(1, 475, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(475, 475)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(1, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:q_proj:(1, 1, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "generation:sdpa:(1, 476)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "generation:lm_head:(2, 1, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 569, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(569, 569)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 95, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:q_proj:(1, 571, 4096)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    },
    "teacher:sdpa:(571, 571)": {
      "query": "torch.float32",
      "key": "torch.float32",
      "value": "torch.bfloat16",
      "output": "torch.bfloat16"
    },
    "teacher:lm_head:(1, 2, 151936)": {
      "input": "torch.float32",
      "output": "torch.bfloat16",
      "weight": "torch.float32",
      "autocast_enabled": true,
      "cache_enabled": true
    }
  },
  "ratio_min": 0.8772323727607727,
  "ratio_max": 1.1563488245010376,
  "ratio_outside_clip_fraction": 0.0,
  "ratio_abs_mean": 0.008202098309993744,
  "logits_normalizer_dtype": "float32",
  "autocast_weight_cache": true,
  "attention_forced_fp32": false,
  "cases": [
    {
      "index": 7,
      "id": "bigmath/cn_k12/60327",
      "correct": false,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1073,
      "reference_F": 1069,
      "generation_seconds": 44.37101138290018,
      "T": 1255,
      "native_replay_max": 0.14526748657226562,
      "native_replay_mean": 0.010067070834338665,
      "native_replay_p95": 0.07700307667255402,
      "phases": [
        {
          "phase": "main",
          "n": 95,
          "max": 0.11728096008300781,
          "mean": 0.01030255388468504,
          "p95": 0.08367723971605301
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0003070831298828125,
          "mean": 0.00015354156494140625,
          "p95": 0.0002917289675679058
        },
        {
          "phase": "path",
          "n": 73,
          "max": 0.114227294921875,
          "mean": 0.0060265944339334965,
          "p95": 0.0513351671397686
        },
        {
          "phase": "path",
          "n": 116,
          "max": 0.12716102600097656,
          "mean": 0.010206896811723709,
          "p95": 0.07855415344238281
        },
        {
          "phase": "summary",
          "n": 76,
          "max": 0.11425399780273438,
          "mean": 0.009150530211627483,
          "p95": 0.06961393356323242
        },
        {
          "phase": "main",
          "n": 118,
          "max": 0.13414955139160156,
          "mean": 0.018584800884127617,
          "p95": 0.11352138966321945
        },
        {
          "phase": "width",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "path",
          "n": 109,
          "max": 0.08681106567382812,
          "mean": 0.004853484686464071,
          "p95": 0.025842271745204926
        },
        {
          "phase": "path",
          "n": 220,
          "max": 0.11709785461425781,
          "mean": 0.010086900554597378,
          "p95": 0.0717146024107933
        },
        {
          "phase": "summary",
          "n": 257,
          "max": 0.14526748657226562,
          "mean": 0.010488362051546574,
          "p95": 0.06978756934404373
        },
        {
          "phase": "main",
          "n": 97,
          "max": 0.12493896484375,
          "mean": 0.012474197894334793,
          "p95": 0.0787532776594162
        },
        {
          "phase": "main",
          "n": 90,
          "max": 0.10518646240234375,
          "mean": 0.0054342481307685375,
          "p95": 0.033407095819711685
        }
      ]
    },
    {
      "index": 15,
      "id": "bigmath/cn_k12/3177",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 614,
      "reference_F": 724,
      "generation_seconds": 24.61308516608551,
      "T": 963,
      "native_replay_max": 0.12459373474121094,
      "native_replay_mean": 0.005775426048785448,
      "native_replay_p95": 0.039630115032196045,
      "phases": [
        {
          "phase": "main",
          "n": 160,
          "max": 0.11716079711914062,
          "mean": 0.005128311924636364,
          "p95": 0.03417092561721802
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "path",
          "n": 108,
          "max": 0.09683990478515625,
          "mean": 0.006510999519377947,
          "p95": 0.04982509836554527
        },
        {
          "phase": "path",
          "n": 91,
          "max": 0.12459373474121094,
          "mean": 0.007541803177446127,
          "p95": 0.04903411865234375
        },
        {
          "phase": "path",
          "n": 233,
          "max": 0.1077423095703125,
          "mean": 0.0038457715418189764,
          "p95": 0.024288136512041092
        },
        {
          "phase": "path",
          "n": 150,
          "max": 0.12293624877929688,
          "mean": 0.0058410135097801685,
          "p95": 0.039527323096990585
        },
        {
          "phase": "summary",
          "n": 160,
          "max": 0.12194633483886719,
          "mean": 0.005733168218284845,
          "p95": 0.030421266332268715
        },
        {
          "phase": "main",
          "n": 2,
          "max": 5.7220458984375e-06,
          "mean": 2.86102294921875e-06,
          "p95": 5.435943421616685e-06
        },
        {
          "phase": "main",
          "n": 57,
          "max": 0.11877059936523438,
          "mean": 0.011617225594818592,
          "p95": 0.07873192429542542
        }
      ]
    }
  ],
  "actions": 2218,
  "native_replay_max": 0.14526748657226562,
  "native_replay_mean": 0.008203746750950813,
  "native_replay_p95": 0.06560343503952026,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 0,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 25130601984,
  "actual_backend_flags": {
    "cuda_tf32": false,
    "float32_precision": "highest"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "n": 1427,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 7.683731517288834,
  "max_abs_logratio": 6.615556716918945,
  "mean_abs_logratio": 0.10816743969917297,
  "p95_abs_logratio": 0.5744960308074951,
  "signed_mean": -0.04065975546836853,
  "ratio_min": 0.0013393689878284931,
  "ratio_max": 5.129889488220215,
  "ratio_mean": 0.9988059997558594,
  "ratio_std": 0.2592386305332184,
  "ratio_quantiles": {
    "0.001": 0.05879002809524536,
    "0.01": 0.21451815962791443,
    "0.05": 0.6351504325866699,
    "0.5": 1.0000114440917969,
    "0.95": 1.233267068862915,
    "0.99": 1.854028582572937,
    "0.999": 3.703158140182495
  },
  "ppo_clip_fraction": 0.14295725524425507,
  "cap_fraction": {
    "1.2": 0.05956552177667618,
    "1.5": 0.025227749720215797,
    "2.0": 0.007708479184657335,
    "3.0": 0.002102312631905079,
    "5.0": 0.000700770819094032,
    "10.0": 0.0
  },
  "ESS_fraction": 0.9369277358055115,
  "peak_gpu_bytes": 16626736640
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "n": 2415,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 8.877315846271813,
  "max_abs_logratio": 3.9284725189208984,
  "mean_abs_logratio": 0.10957803577184677,
  "p95_abs_logratio": 0.5847517848014832,
  "signed_mean": -0.03922819346189499,
  "ratio_min": 0.019673701375722885,
  "ratio_max": 7.611753940582275,
  "ratio_mean": 0.9982885718345642,
  "ratio_std": 0.2884463369846344,
  "ratio_quantiles": {
    "0.001": 0.03237840160727501,
    "0.01": 0.2689199149608612,
    "0.05": 0.6268286108970642,
    "0.5": 1.0000190734863281,
    "0.95": 1.243661642074585,
    "0.99": 1.9816362857818604,
    "0.999": 3.84128999710083
  },
  "ppo_clip_fraction": 0.14865423738956451,
  "cap_fraction": {
    "1.2": 0.05921325087547302,
    "1.5": 0.02153209038078785,
    "2.0": 0.009523809887468815,
    "3.0": 0.0028985508251935244,
    "5.0": 0.0008281573536805809,
    "10.0": 0.0
  },
  "ESS_fraction": 0.9229757189750671,
  "peak_gpu_bytes": 17675496448
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "n": 1653,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 7.9822572357952595,
  "max_abs_logratio": 5.42989444732666,
  "mean_abs_logratio": 0.12934310734272003,
  "p95_abs_logratio": 0.6922150254249573,
  "signed_mean": -0.04893302917480469,
  "ratio_min": 0.00438355840742588,
  "ratio_max": 8.271026611328125,
  "ratio_mean": 0.9952409267425537,
  "ratio_std": 0.30137893557548523,
  "ratio_quantiles": {
    "0.001": 0.028476187959313393,
    "0.01": 0.2218940109014511,
    "0.05": 0.5777847766876221,
    "0.5": 1.0000190734863281,
    "0.95": 1.2627044916152954,
    "0.99": 1.993164300918579,
    "0.999": 3.017934799194336
  },
  "ppo_clip_fraction": 0.1712038666009903,
  "cap_fraction": {
    "1.2": 0.07017543911933899,
    "1.5": 0.026618270203471184,
    "2.0": 0.010284331627190113,
    "3.0": 0.0012099213199689984,
    "5.0": 0.0006049606599844992,
    "10.0": 0.0
  },
  "ESS_fraction": 0.916049063205719,
  "peak_gpu_bytes": 16686689280
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "n": 1856,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 8.80043784622103,
  "max_abs_logratio": 7.270294189453125,
  "mean_abs_logratio": 0.13192018866539001,
  "p95_abs_logratio": 0.726280689239502,
  "signed_mean": -0.04610241577029228,
  "ratio_min": 0.0006959072197787464,
  "ratio_max": 9.440837860107422,
  "ratio_mean": 1.0033951997756958,
  "ratio_std": 0.3617057800292969,
  "ratio_quantiles": {
    "0.001": 0.07520812004804611,
    "0.01": 0.23761948943138123,
    "0.05": 0.5541074275970459,
    "0.5": 1.0000076293945312,
    "0.95": 1.284693717956543,
    "0.99": 2.0299527645111084,
    "0.999": 4.289030075073242
  },
  "ppo_clip_fraction": 0.17025862634181976,
  "cap_fraction": {
    "1.2": 0.07004310190677643,
    "1.5": 0.02801724150776863,
    "2.0": 0.010775862261652946,
    "3.0": 0.005387931130826473,
    "5.0": 0.0005387931014411151,
    "10.0": 0.0
  },
  "ESS_fraction": 0.8850520849227905,
  "peak_gpu_bytes": 16849729024
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "n": 1695,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 8.486872219014913,
  "max_abs_logratio": 5.987895965576172,
  "mean_abs_logratio": 0.13135278224945068,
  "p95_abs_logratio": 0.6621242165565491,
  "signed_mean": -0.04073644429445267,
  "ratio_min": 0.002508937381207943,
  "ratio_max": 4.665778160095215,
  "ratio_mean": 1.002730369567871,
  "ratio_std": 0.2844372093677521,
  "ratio_quantiles": {
    "0.001": 0.03790564835071564,
    "0.01": 0.2639923393726349,
    "0.05": 0.6061686873435974,
    "0.5": 1.0000324249267578,
    "0.95": 1.2969251871109009,
    "0.99": 2.096919298171997,
    "0.999": 3.3563318252563477
  },
  "ppo_clip_fraction": 0.17935103178024292,
  "cap_fraction": {
    "1.2": 0.07433628290891647,
    "1.5": 0.02890855446457863,
    "2.0": 0.011799409985542297,
    "3.0": 0.0029498524963855743,
    "5.0": 0.0,
    "10.0": 0.0
  },
  "ESS_fraction": 0.9255683422088623,
  "peak_gpu_bytes": 16661735936
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "n": 1754,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 9.213038837071508,
  "max_abs_logratio": 5.504184722900391,
  "mean_abs_logratio": 0.17181850969791412,
  "p95_abs_logratio": 0.7804060578346252,
  "signed_mean": -0.06567391753196716,
  "ratio_min": 0.004069705028086901,
  "ratio_max": 7.983762264251709,
  "ratio_mean": 0.9979491829872131,
  "ratio_std": 0.36849063634872437,
  "ratio_quantiles": {
    "0.001": 0.01627931371331215,
    "0.01": 0.19036830961704254,
    "0.05": 0.5180113911628723,
    "0.5": 1.0000114440917969,
    "0.95": 1.379492998123169,
    "0.99": 2.285031795501709,
    "0.999": 4.196332931518555
  },
  "ppo_clip_fraction": 0.22748003900051117,
  "cap_fraction": {
    "1.2": 0.08722919225692749,
    "1.5": 0.0404789038002491,
    "2.0": 0.013683009892702103,
    "3.0": 0.0045610032975673676,
    "5.0": 0.0011402508243918419,
    "10.0": 0.0
  },
  "ESS_fraction": 0.8800753355026245,
  "peak_gpu_bytes": 17177011200
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "n": 2165,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 9.193004061933607,
  "max_abs_logratio": 5.85472297668457,
  "mean_abs_logratio": 0.10455366224050522,
  "p95_abs_logratio": 0.5816909670829773,
  "signed_mean": -0.03767668455839157,
  "ratio_min": 0.002866329625248909,
  "ratio_max": 6.891115665435791,
  "ratio_mean": 1.0005359649658203,
  "ratio_std": 0.2898317575454712,
  "ratio_quantiles": {
    "0.001": 0.05469074100255966,
    "0.01": 0.25855547189712524,
    "0.05": 0.6535226702690125,
    "0.5": 1.0000076293945312,
    "0.95": 1.2345187664031982,
    "0.99": 1.8837485313415527,
    "0.999": 3.949395179748535
  },
  "ppo_clip_fraction": 0.13856813311576843,
  "cap_fraction": {
    "1.2": 0.05542725324630737,
    "1.5": 0.021709006279706955,
    "2.0": 0.00923787523061037,
    "3.0": 0.003233256284147501,
    "5.0": 0.0009237875347025692,
    "10.0": 0.0
  },
  "ESS_fraction": 0.9226167798042297,
  "peak_gpu_bytes": 17353126400
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/proximal/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "n": 2218,
  "source": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/native",
  "q": "immutable full-BF16 cached native sampler",
  "p0": "FP32 fullteacher at unchanged checkpoint50",
  "optimizer_updates": 0,
  "no_q_refresh": true,
  "seconds": 11.379371461924165,
  "max_abs_logratio": 3.8872909545898438,
  "mean_abs_logratio": 0.12246107310056686,
  "p95_abs_logratio": 0.6576072573661804,
  "signed_mean": -0.04188648238778114,
  "ratio_min": 0.02050080895423889,
  "ratio_max": 9.530303001403809,
  "ratio_mean": 1.002029538154602,
  "ratio_std": 0.34615597128868103,
  "ratio_quantiles": {
    "0.001": 0.06849773228168488,
    "0.01": 0.24763068556785583,
    "0.05": 0.5860893726348877,
    "0.5": 1.0000114440917969,
    "0.95": 1.2867012023925781,
    "0.99": 2.013340711593628,
    "0.999": 5.259618282318115
  },
  "ppo_clip_fraction": 0.1645626723766327,
  "cap_fraction": {
    "1.2": 0.064472496509552,
    "1.5": 0.029305681586265564,
    "2.0": 0.011271415278315544,
    "3.0": 0.002254283055663109,
    "5.0": 0.0013525699032470584,
    "10.0": 0.0
  },
  "ESS_fraction": 0.8934275507926941,
  "peak_gpu_bytes": 16690243584
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/summary-partial.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/full-bf16/summary-partial.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "full_bf16_actually_tested": true,
  "workers": 8,
  "cases": 16,
  "correct": 11,
  "reference_correct": 13,
  "actions": 15183,
  "generation_episode_seconds_sum": 468.93819444207475,
  "generation_critical_two_cases_seconds": 83.36943496577442,
  "F": 11251,
  "T": 15183,
  "max_native_fullteacher_drift": 0.2081623077392578,
  "worst_rank_mean": 0.011016364209353924,
  "worst_rank_p95": 0.07097320258617401,
  "same_cached_exact_all_actions": true,
  "gradient_cosine_range": [
    0.6735587413084981,
    0.8802999339689076
  ],
  "gradient_relative_l2_range": [
    0.4868860619227991,
    0.7400588066037102
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 0,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 1,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 2,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 3,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 4,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 5,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 6,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 7,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "width": 1,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.883171807974577
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8602411169558764
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 32,
  "capture_seconds": 0.4182829027995467,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 51995689984,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "width": 2,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8867811351083219
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8387518036179245
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.4418260343372822,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 52222628864,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "width": 3,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9410631679929793
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9020742950960994
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.4353851219639182,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 52473273344,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "width": 4,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9595278138294816
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9185315258800983
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.4509961628355086,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 52597149696,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "width": 5,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9728829292580485
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9402068089693785
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.4560542069375515,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 52898845184,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "width": 6,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9696033629588783
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9313271888531744
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.5375340562313795,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 52963417088,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "width": 7,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 1.0160882249474525
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.971412300132215
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.5915242503397167,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 53200318976,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/attempt2/preflight/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "width": 8,
  "bucket": 2048,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 1.401244387961924
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 1.3271899498067796
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 34,
  "capture_seconds": 0.69246940407902,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 53746287616,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "completed",
  "rank": 0,
  "passed": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 1,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8971614600159228
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8692994341254234
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 2,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9179691043682396
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8824474280700088
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 3,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9260016735643148
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9167472459375858
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 4,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9406412658281624
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9140134691260755
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 5,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 1.0063027748838067
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "numeric_phase_complete",
  "rank": 6,
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.9868610701523721
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "graph_captured",
  "rank": 7,
  "capture_seconds": 0.44241590704768896,
  "width": 8,
  "bucket": 2048,
  "pool_bytes": 19327352832
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/graph-decode/preflight/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "width": 1,
  "bucket": 512,
  "passed": true,
  "shadow_fullmodel_every_linear_exact": true,
  "shadow_receipt": {
    "version": 0,
    "linear_layers": 253,
    "shadow_bytes": 8044544000,
    "all_master_fp32": true,
    "linear_weights_only": true,
    "embedding_residual_norm_fp32": true,
    "nonpersistent_buffers": true,
    "stable_addresses": true
  },
  "phases": [
    {
      "version": 0,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8769478048197925
    },
    {
      "version": 1,
      "max_fullvocab_logit_error": 0.0,
      "max_target_logprob_error": 0.0,
      "mean_target_logprob_error": 0.0,
      "p95_target_logprob_error": 0.0,
      "seconds_paired_eager_graph": 0.8158249091356993
    }
  ],
  "sibling_isolation_max": 0.0,
  "physical_counter_exact": true,
  "physical_graph_replays": 32,
  "capture_seconds": 0.5333230160176754,
  "warm_forwards": 3,
  "captured_fake_forward": 1,
  "capture_not_rewarded": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 51995689984,
  "master_params_fp32": true,
  "original_caps_preserved": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/precision-pipeline-status.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/precision-pipeline-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "tf32_rejected_by_unchanged_likelihood_guard",
  "time": 1791802969.4995317,
  "summary": {
    "cross_precision_guard_passed": false,
    "max": 0.4760608673095703,
    "mean": 0.010209650680294247,
    "rank_p95_max": 0.0661899745464325,
    "actions": 36054,
    "unchanged_thresholds": {
      "max": 0.01,
      "mean": 0.002,
      "p95": 0.005
    },
    "optimizer_master_dtype": "float32",
    "benchmark_used_for_selection": false
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/precision-summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/precision-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "fp32-control": {
    "ranks": 8,
    "pass_all": true,
    "max": 0.0001201629638671875,
    "worst_rank_mean": 4.856178748013917e-06,
    "worst_rank_p95": 2.47955322265625e-05
  },
  "tf32-native": {
    "ranks": 8,
    "pass_all": false,
    "max": 0.132720947265625,
    "worst_rank_mean": 0.0026032286696135998,
    "worst_rank_p95": 0.013930120505392551,
    "correct": 14,
    "reference_correct": 13,
    "exact_response_count": 0,
    "T": 22675
  },
  "bf16-native": {
    "ranks": 8,
    "pass_all": false,
    "max": 0.17393875122070312,
    "worst_rank_mean": 0.005113103426992893,
    "worst_rank_p95": 0.025956913828849792,
    "correct": 13,
    "reference_correct": 13,
    "exact_response_count": 0,
    "T": 15321
  },
  "bf16-attention-native": {
    "ranks": 8,
    "pass_all": false,
    "max": 0.27329444885253906,
    "worst_rank_mean": 0.0047472394071519375,
    "worst_rank_p95": 0.025078177452087402,
    "correct": 12,
    "reference_correct": 13,
    "exact_response_count": 0,
    "T": 15316
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/summary-console.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/summary-console.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "baseline": [
    {
      "step": 51,
      "runner_timer": 328.62837648391724,
      "full_measured_wall": 328.9481957498938,
      "responses": 32,
      "response_per_second": 0.09727975533366437,
      "sampled_tokens": 36054,
      "sampled_tokens_per_second": 109.60388433749797,
      "physical_generation_forwards": 24517,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.0001201629638671875,
      "mean_drift_max": 4.856178748013917e-06,
      "p95_drift_max": 2.47955322265625e-05,
      "backbone_update_l2_min": 2.7756752204135794e-05,
      "peak_gpu_bytes": 53217406464,
      "critical_generation_rank": 2,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.2044815798290074,
        "detail.model.generation.prefill": 10.23366286419332,
        "detail.cpu_gpu_sampling_and_host_sync": 47.091186706442386,
        "detail.model.generation.decode": 171.0437788516283,
        "rollout_execute_and_scoring": 230.38665137207136,
        "reward_gather_and_advantages": 0.005046084988862276,
        "detail.model.replay": 11.54071963019669,
        "replay_forward": 34.38403901504353,
        "backward": 62.803956381976604,
        "collective_parity_guard": 0.546473415568471,
        "clip_active_collective_optimizer": 0.2223821198567748,
        "serialization": 0.0002777399495244026,
        "cleanup": 0.31229178979992867,
        "metric_gather_write": 0.0027184272184967995
      }
    },
    {
      "step": 52,
      "runner_timer": 267.1650552749634,
      "full_measured_wall": 267.3768829908222,
      "responses": 32,
      "response_per_second": 0.11968125158037096,
      "sampled_tokens": 36443,
      "sampled_tokens_per_second": 136.2982453544831,
      "physical_generation_forwards": 24215,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.000133514404296875,
      "mean_drift_max": 6.002300779073266e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 2.075288719310541e-05,
      "peak_gpu_bytes": 52572883968,
      "critical_generation_rank": 2,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.11356584262102842,
        "detail.model.generation.prefill": 7.932925797533244,
        "detail.cpu_gpu_sampling_and_host_sync": 33.01905883103609,
        "detail.model.generation.decode": 142.96917398367077,
        "rollout_execute_and_scoring": 185.29311890574172,
        "reward_gather_and_advantages": 0.0034236260689795017,
        "detail.model.replay": 9.808736765291542,
        "replay_forward": 29.591544159688056,
        "backward": 51.53488450497389,
        "collective_parity_guard": 0.44669475266709924,
        "clip_active_collective_optimizer": 0.056929206009954214,
        "serialization": 0.00020478013902902603,
        "cleanup": 0.1301021222025156,
        "metric_gather_write": 0.08076405804604292
      }
    },
    {
      "step": 53,
      "runner_timer": 614.1606800556183,
      "full_measured_wall": 614.3999879374169,
      "responses": 32,
      "response_per_second": 0.052083334355891193,
      "sampled_tokens": 59114,
      "sampled_tokens_per_second": 96.21419459731725,
      "physical_generation_forwards": 39706,
      "correct": 23,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.00033473968505859375,
      "mean_drift_max": 5.364731805457268e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 1.7812249684676693e-05,
      "peak_gpu_bytes": 46281128448,
      "critical_generation_rank": 7,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.1813362562097609,
        "detail.model.generation.prefill": 6.8879348947666585,
        "detail.cpu_gpu_sampling_and_host_sync": 122.38787000300363,
        "detail.model.generation.decode": 368.8689144202508,
        "rollout_execute_and_scoring": 501.34053923003376,
        "reward_gather_and_advantages": 0.003537846263498068,
        "detail.model.replay": 11.238733946345747,
        "replay_forward": 34.03973247855902,
        "backward": 66.83814768353477,
        "collective_parity_guard": 11.660146350972354,
        "clip_active_collective_optimizer": 0.06287559727206826,
        "serialization": 0.00028405897319316864,
        "cleanup": 0.23052647709846497,
        "metric_gather_write": 0.0020658280700445175
      }
    },
    {
      "step": 54,
      "runner_timer": 620.0931172370911,
      "full_measured_wall": 620.3233416602015,
      "responses": 32,
      "response_per_second": 0.05158600015655842,
      "sampled_tokens": 56685,
      "sampled_tokens_per_second": 91.37976308982857,
      "physical_generation_forwards": 38719,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.0001201629638671875,
      "mean_drift_max": 4.804951458936557e-06,
      "p95_drift_max": 2.47955322265625e-05,
      "backbone_update_l2_min": 1.556426626106358e-05,
      "peak_gpu_bytes": 47071357440,
      "critical_generation_rank": 7,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.519445848185569,
        "detail.model.generation.prefill": 14.434393257368356,
        "detail.cpu_gpu_sampling_and_host_sync": 131.59334085788578,
        "detail.model.generation.decode": 305.4415867542848,
        "rollout_execute_and_scoring": 454.5943093271926,
        "reward_gather_and_advantages": 0.0035036159679293633,
        "detail.model.replay": 19.020176413469017,
        "replay_forward": 58.35135613568127,
        "backward": 105.61396916396916,
        "collective_parity_guard": 1.1958783976733685,
        "clip_active_collective_optimizer": 0.06483317585662007,
        "serialization": 0.00020068883895874023,
        "cleanup": 0.13505636528134346,
        "metric_gather_write": 0.0964167001657188
      }
    },
    {
      "step": 55,
      "runner_timer": 282.8445303440094,
      "full_measured_wall": 283.0413832999766,
      "responses": 32,
      "response_per_second": 0.11305767243967058,
      "sampled_tokens": 39890,
      "sampled_tokens_per_second": 140.93345480057687,
      "physical_generation_forwards": 25567,
      "correct": 31,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.000141143798828125,
      "mean_drift_max": 4.974618605046999e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 1.294011051718898e-05,
      "peak_gpu_bytes": 41884538880,
      "critical_generation_rank": 3,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.13986897375434637,
        "detail.model.generation.prefill": 8.923590948805213,
        "detail.cpu_gpu_sampling_and_host_sync": 46.10319405607879,
        "detail.model.generation.decode": 130.35922221373767,
        "rollout_execute_and_scoring": 186.6487042233348,
        "reward_gather_and_advantages": 0.0033166659995913506,
        "detail.model.replay": 10.776959808543324,
        "replay_forward": 33.04941036738455,
        "backward": 58.95332987140864,
        "collective_parity_guard": 3.911685898900032,
        "clip_active_collective_optimizer": 0.059967291075736284,
        "serialization": 0.0002459986135363579,
        "cleanup": 0.18628615560010076,
        "metric_gather_write": 0.010167617816478014
      }
    }
  ],
  "tf32": [],
  "warnings": [
    "First step51 profiled; candidate52 includes resident_width8 fixtures. Compare matched unprofiled53..55 when available.",
    "full_measured_wall includes cleanup and metric writes, ending before phase diagnostic dump; nested events overlap and cannot be summed.",
    "Backward includes DDP gradient synchronization; first-backward scoped trace is a no_sync call, so it does not measure all NCCL kernel time."
  ],
  "tf32_gate": {
    "cross_precision_guard_passed": false,
    "max": 0.4760608673095703,
    "mean": 0.010209650680294247,
    "rank_p95_max": 0.0661899745464325,
    "actions": 36054,
    "unchanged_thresholds": {
      "max": 0.01,
      "mean": 0.002,
      "p95": 0.005
    },
    "optimizer_master_dtype": "float32",
    "benchmark_used_for_selection": false
  },
  "paired_steady_steps": []
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "baseline": [
    {
      "step": 51,
      "runner_timer": 328.62837648391724,
      "full_measured_wall": 328.9481957498938,
      "responses": 32,
      "response_per_second": 0.09727975533366437,
      "sampled_tokens": 36054,
      "sampled_tokens_per_second": 109.60388433749797,
      "physical_generation_forwards": 24517,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.0001201629638671875,
      "mean_drift_max": 4.856178748013917e-06,
      "p95_drift_max": 2.47955322265625e-05,
      "backbone_update_l2_min": 2.7756752204135794e-05,
      "peak_gpu_bytes": 53217406464,
      "critical_generation_rank": 2,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.2044815798290074,
        "detail.model.generation.prefill": 10.23366286419332,
        "detail.cpu_gpu_sampling_and_host_sync": 47.091186706442386,
        "detail.model.generation.decode": 171.0437788516283,
        "rollout_execute_and_scoring": 230.38665137207136,
        "reward_gather_and_advantages": 0.005046084988862276,
        "detail.model.replay": 11.54071963019669,
        "replay_forward": 34.38403901504353,
        "backward": 62.803956381976604,
        "collective_parity_guard": 0.546473415568471,
        "clip_active_collective_optimizer": 0.2223821198567748,
        "serialization": 0.0002777399495244026,
        "cleanup": 0.31229178979992867,
        "metric_gather_write": 0.0027184272184967995
      }
    },
    {
      "step": 52,
      "runner_timer": 267.1650552749634,
      "full_measured_wall": 267.3768829908222,
      "responses": 32,
      "response_per_second": 0.11968125158037096,
      "sampled_tokens": 36443,
      "sampled_tokens_per_second": 136.2982453544831,
      "physical_generation_forwards": 24215,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.000133514404296875,
      "mean_drift_max": 6.002300779073266e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 2.075288719310541e-05,
      "peak_gpu_bytes": 52572883968,
      "critical_generation_rank": 2,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.11356584262102842,
        "detail.model.generation.prefill": 7.932925797533244,
        "detail.cpu_gpu_sampling_and_host_sync": 33.01905883103609,
        "detail.model.generation.decode": 142.96917398367077,
        "rollout_execute_and_scoring": 185.29311890574172,
        "reward_gather_and_advantages": 0.0034236260689795017,
        "detail.model.replay": 9.808736765291542,
        "replay_forward": 29.591544159688056,
        "backward": 51.53488450497389,
        "collective_parity_guard": 0.44669475266709924,
        "clip_active_collective_optimizer": 0.056929206009954214,
        "serialization": 0.00020478013902902603,
        "cleanup": 0.1301021222025156,
        "metric_gather_write": 0.08076405804604292
      }
    },
    {
      "step": 53,
      "runner_timer": 614.1606800556183,
      "full_measured_wall": 614.3999879374169,
      "responses": 32,
      "response_per_second": 0.052083334355891193,
      "sampled_tokens": 59114,
      "sampled_tokens_per_second": 96.21419459731725,
      "physical_generation_forwards": 39706,
      "correct": 23,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.00033473968505859375,
      "mean_drift_max": 5.364731805457268e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 1.7812249684676693e-05,
      "peak_gpu_bytes": 46281128448,
      "critical_generation_rank": 7,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.1813362562097609,
        "detail.model.generation.prefill": 6.8879348947666585,
        "detail.cpu_gpu_sampling_and_host_sync": 122.38787000300363,
        "detail.model.generation.decode": 368.8689144202508,
        "rollout_execute_and_scoring": 501.34053923003376,
        "reward_gather_and_advantages": 0.003537846263498068,
        "detail.model.replay": 11.238733946345747,
        "replay_forward": 34.03973247855902,
        "backward": 66.83814768353477,
        "collective_parity_guard": 11.660146350972354,
        "clip_active_collective_optimizer": 0.06287559727206826,
        "serialization": 0.00028405897319316864,
        "cleanup": 0.23052647709846497,
        "metric_gather_write": 0.0020658280700445175
      }
    },
    {
      "step": 54,
      "runner_timer": 620.0931172370911,
      "full_measured_wall": 620.3233416602015,
      "responses": 32,
      "response_per_second": 0.05158600015655842,
      "sampled_tokens": 56685,
      "sampled_tokens_per_second": 91.37976308982857,
      "physical_generation_forwards": 38719,
      "correct": 30,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.0001201629638671875,
      "mean_drift_max": 4.804951458936557e-06,
      "p95_drift_max": 2.47955322265625e-05,
      "backbone_update_l2_min": 1.556426626106358e-05,
      "peak_gpu_bytes": 47071357440,
      "critical_generation_rank": 7,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.519445848185569,
        "detail.model.generation.prefill": 14.434393257368356,
        "detail.cpu_gpu_sampling_and_host_sync": 131.59334085788578,
        "detail.model.generation.decode": 305.4415867542848,
        "rollout_execute_and_scoring": 454.5943093271926,
        "reward_gather_and_advantages": 0.0035036159679293633,
        "detail.model.replay": 19.020176413469017,
        "replay_forward": 58.35135613568127,
        "backward": 105.61396916396916,
        "collective_parity_guard": 1.1958783976733685,
        "clip_active_collective_optimizer": 0.06483317585662007,
        "serialization": 0.00020068883895874023,
        "cleanup": 0.13505636528134346,
        "metric_gather_write": 0.0964167001657188
      }
    },
    {
      "step": 55,
      "runner_timer": 282.8445303440094,
      "full_measured_wall": 283.0413832999766,
      "responses": 32,
      "response_per_second": 0.11305767243967058,
      "sampled_tokens": 39890,
      "sampled_tokens_per_second": 140.93345480057687,
      "physical_generation_forwards": 25567,
      "correct": 31,
      "guard_all_passed": true,
      "optimizer_all_updated": true,
      "max_drift": 0.000141143798828125,
      "mean_drift_max": 4.974618605046999e-06,
      "p95_drift_max": 2.6702880859375e-05,
      "backbone_update_l2_min": 1.294011051718898e-05,
      "peak_gpu_bytes": 41884538880,
      "critical_generation_rank": 3,
      "critical_host_phases": {
        "detail.cpu_structured_mask": 0.13986897375434637,
        "detail.model.generation.prefill": 8.923590948805213,
        "detail.cpu_gpu_sampling_and_host_sync": 46.10319405607879,
        "detail.model.generation.decode": 130.35922221373767,
        "rollout_execute_and_scoring": 186.6487042233348,
        "reward_gather_and_advantages": 0.0033166659995913506,
        "detail.model.replay": 10.776959808543324,
        "replay_forward": 33.04941036738455,
        "backward": 58.95332987140864,
        "collective_parity_guard": 3.911685898900032,
        "clip_active_collective_optimizer": 0.059967291075736284,
        "serialization": 0.0002459986135363579,
        "cleanup": 0.18628615560010076,
        "metric_gather_write": 0.010167617816478014
      }
    }
  ],
  "tf32": [],
  "warnings": [
    "First step51 profiled; candidate52 includes resident_width8 fixtures. Compare matched unprofiled53..55 when available.",
    "full_measured_wall includes cleanup and metric writes, ending before phase diagnostic dump; nested events overlap and cannot be summed.",
    "Backward includes DDP gradient synchronization; first-backward scoped trace is a no_sync call, so it does not measure all NCCL kernel time."
  ],
  "tf32_gate": {
    "cross_precision_guard_passed": false,
    "max": 0.4760608673095703,
    "mean": 0.010209650680294247,
    "rank_p95_max": 0.0661899745464325,
    "actions": 36054,
    "unchanged_thresholds": {
      "max": 0.01,
      "mean": 0.002,
      "p95": 0.005
    },
    "optimizer_master_dtype": "float32",
    "benchmark_used_for_selection": false
  },
  "paired_steady_steps": []
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-gate-summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "cross_precision_guard_passed": false,
  "max": 0.4760608673095703,
  "mean": 0.010209650680294247,
  "rank_p95_max": 0.0661899745464325,
  "actions": 36054,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "optimizer_master_dtype": "float32",
  "benchmark_used_for_selection": false
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-kernels/summary.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-kernels/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "cached-three-tokens": {
    "kernel_names": [
      "void gemmk1_kernel<int, float, 256, 5, false, false, false, false, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, 0>(cublasGemmk1Params<float, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, biasType<cublasGemvTensorStridedBatched<float>::value_type, float>::type>)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_256x128_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_256x128_32x3_tn_align4::Params)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_128x128_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_128x128_32x3_tn_align4::Params)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_128x256_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_128x256_32x3_tn_align4::Params)",
      "void gemv2T_kernel_val<int, int, float, float, float, float, 128, 16, 4, 4, false, false, cublasGemvParamsEx<int, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float> >(cublasGemvParamsEx<int, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float>, float, float)",
      "void gemmk1_kernel<int, float, 256, 5, true, false, false, false, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, 0>(cublasGemmk1Params<float, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, biasType<cublasGemvTensorStridedBatched<float>::value_type, float>::type>)",
      "std::enable_if<!(false), void>::type internal::gemvx::kernel<int, int, float, float, float, float, false, true, true, false, 7, false, cublasGemvParamsEx<int, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float> >(cublasGemvParamsEx<int, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float>)"
    ],
    "kernel_seconds": 0.09873452700000006
  },
  "teacher-three-tokens": {
    "kernel_names": [
      "void gemmk1_kernel<int, float, 256, 5, false, false, false, false, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, 0>(cublasGemmk1Params<float, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float, biasType<cublasGemvTensorStridedBatched<float>::value_type, float>::type>)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_256x128_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_256x128_32x3_tn_align4::Params)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_128x128_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_128x128_32x3_tn_align4::Params)",
      "void cutlass::Kernel2<cutlass_80_tensorop_s1688gemm_128x256_32x3_tn_align4>(cutlass_80_tensorop_s1688gemm_128x256_32x3_tn_align4::Params)",
      "void gemmSN_TN_kernel<float, 128, 16, 2, 4, 4, 4, false, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float> >(cublasGemmSmallNParams<cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float const>, cublasGemvTensorStridedBatched<float>, float>)"
    ],
    "kernel_seconds": 0.06182047900000002
  },
  "logp_deltas": [
    0.0,
    0.00229644775390625,
    0.0076007843017578125
  ],
  "targets": [
    1654,
    525,
    4588
  ],
  "tf32_enabled": true,
  "float32_precision": "high",
  "master_dtype": "torch.float32",
  "note": "Teacher-forced3tokenmicroprofile only; no speed or quality estimate."
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 8,
    "id": "bigmath/cn_k12/23250",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 534,
    "reference_F": 521,
    "generation_seconds": 19.606840312946588,
    "T": 879,
    "native_replay_max": 0.08813667297363281,
    "native_replay_mean": 0.0019351592054590583,
    "native_replay_p95": 0.010074611753225327,
    "phases": [
      {
        "phase": "main",
        "n": 129,
        "max": 0.08813667297363281,
        "mean": 0.005713115446269512,
        "p95": 0.03315772861242294
      },
      {
        "phase": "width",
        "n": 2,
        "max": 7.62939453125e-06,
        "mean": 3.814697265625e-06,
        "p95": 7.24792471373803e-06
      },
      {
        "phase": "path",
        "n": 165,
        "max": 0.006214141845703125,
        "mean": 0.0002929456240963191,
        "p95": 0.001667786156758666
      },
      {
        "phase": "path",
        "n": 113,
        "max": 0.00548553466796875,
        "mean": 0.00025492641725577414,
        "p95": 0.001412201439961791
      },
      {
        "phase": "path",
        "n": 67,
        "max": 0.00262451171875,
        "mean": 0.0003022151067852974,
        "p95": 0.0016523362137377262
      },
      {
        "phase": "path",
        "n": 196,
        "max": 0.0024738311767578125,
        "mean": 0.00013521740038413554,
        "p95": 0.00092315673828125
      },
      {
        "phase": "summary",
        "n": 122,
        "max": 0.04353904724121094,
        "mean": 0.004833276383578777,
        "p95": 0.02461652271449566
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 83,
        "max": 0.0564117431640625,
        "mean": 0.003017471404746175,
        "p95": 0.017878539860248566
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 9,
    "id": "bigmath/cn_k12/64731",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1427,
    "reference_F": 2172,
    "generation_seconds": 54.49747964460403,
    "T": 2389,
    "native_replay_max": 0.08221244812011719,
    "native_replay_mean": 0.0009210010757669806,
    "native_replay_p95": 0.003775389399379492,
    "phases": [
      {
        "phase": "main",
        "n": 208,
        "max": 0.056182861328125,
        "mean": 0.003652811050415039,
        "p95": 0.015315532684326172
      },
      {
        "phase": "width",
        "n": 2,
        "max": 9.5367431640625e-06,
        "mean": 4.76837158203125e-06,
        "p95": 9.059906005859375e-06
      },
      {
        "phase": "path",
        "n": 182,
        "max": 0.003345489501953125,
        "mean": 0.00018247666594106704,
        "p95": 0.0012119290186092257
      },
      {
        "phase": "path",
        "n": 345,
        "max": 0.009584426879882812,
        "mean": 0.0001361681061098352,
        "p95": 0.0008647918002679944
      },
      {
        "phase": "path",
        "n": 435,
        "max": 0.0075244903564453125,
        "mean": 0.00016148446593433619,
        "p95": 0.0010055538732558489
      },
      {
        "phase": "path",
        "n": 738,
        "max": 0.0042362213134765625,
        "mean": 0.00022910669213160872,
        "p95": 0.001364514697343111
      },
      {
        "phase": "summary",
        "n": 295,
        "max": 0.08221244812011719,
        "mean": 0.0031856149435043335,
        "p95": 0.021494099870324135
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 182,
        "max": 0.03674507141113281,
        "mean": 0.0009956255089491606,
        "p95": 0.008669553324580193
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 10,
    "id": "bigmath/cn_k12/204933",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 602,
    "reference_F": 764,
    "generation_seconds": 21.97192501835525,
    "T": 1000,
    "native_replay_max": 0.13114166259765625,
    "native_replay_mean": 0.0022616805508732796,
    "native_replay_p95": 0.012234872207045555,
    "phases": [
      {
        "phase": "main",
        "n": 163,
        "max": 0.13114166259765625,
        "mean": 0.006094037555158138,
        "p95": 0.03166484087705612
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.33514404296875e-05,
        "mean": 6.67572021484375e-06,
        "p95": 1.2683868590102065e-05
      },
      {
        "phase": "path",
        "n": 187,
        "max": 0.00336456298828125,
        "mean": 0.00023563405557069927,
        "p95": 0.0013193129561841488
      },
      {
        "phase": "path",
        "n": 178,
        "max": 0.0031642913818359375,
        "mean": 0.00025751348584890366,
        "p95": 0.0013811102835461497
      },
      {
        "phase": "path",
        "n": 60,
        "max": 0.0062618255615234375,
        "mean": 0.00037298203096725047,
        "p95": 0.0014635083498433232
      },
      {
        "phase": "path",
        "n": 160,
        "max": 0.013608932495117188,
        "mean": 0.0005142688751220703,
        "p95": 0.002839660970494151
      },
      {
        "phase": "summary",
        "n": 187,
        "max": 0.06442070007324219,
        "mean": 0.005193893797695637,
        "p95": 0.03137664496898651
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 61,
        "max": 0.021625518798828125,
        "mean": 0.0016805930063128471,
        "p95": 0.011751174926757812
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 11,
    "id": "bigmath/cn_k12/147481",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 1110,
    "reference_F": 1086,
    "generation_seconds": 40.82329851295799,
    "T": 1801,
    "native_replay_max": 0.09502220153808594,
    "native_replay_mean": 0.0019491800339892507,
    "native_replay_p95": 0.011135101318359375,
    "phases": [
      {
        "phase": "main",
        "n": 542,
        "max": 0.09502220153808594,
        "mean": 0.004055209923535585,
        "p95": 0.022695835679769516
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.9073486328125e-05,
        "mean": 9.5367431640625e-06,
        "p95": 1.811981201171875e-05
      },
      {
        "phase": "path",
        "n": 205,
        "max": 0.00298309326171875,
        "mean": 0.0001334120606770739,
        "p95": 0.0009178161853924394
      },
      {
        "phase": "path",
        "n": 253,
        "max": 0.008516311645507812,
        "mean": 0.0002605754998512566,
        "p95": 0.001305770711041987
      },
      {
        "phase": "path",
        "n": 288,
        "max": 0.004375457763671875,
        "mean": 0.000273393263341859,
        "p95": 0.0016633985796943307
      },
      {
        "phase": "path",
        "n": 233,
        "max": 0.003643035888671875,
        "mean": 0.00018742770771495998,
        "p95": 0.0012680049985647202
      },
      {
        "phase": "summary",
        "n": 189,
        "max": 0.06942367553710938,
        "mean": 0.004943524487316608,
        "p95": 0.024516288191080093
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "main",
        "n": 87,
        "max": 0.03901863098144531,
        "mean": 0.0018680616049095988,
        "p95": 0.009404557757079601
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 12,
    "id": "bigmath/cn_k12/61311",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 909,
    "reference_F": 952,
    "generation_seconds": 33.18680120212957,
    "T": 1602,
    "native_replay_max": 0.10259056091308594,
    "native_replay_mean": 0.0016089961864054203,
    "native_replay_p95": 0.009822364896535873,
    "phases": [
      {
        "phase": "main",
        "n": 156,
        "max": 0.10259056091308594,
        "mean": 0.006456081755459309,
        "p95": 0.027561664581298828
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "path",
        "n": 283,
        "max": 0.00653839111328125,
        "mean": 0.00019926064123865217,
        "p95": 0.0010412211995571852
      },
      {
        "phase": "path",
        "n": 254,
        "max": 0.01233673095703125,
        "mean": 0.0003420837165322155,
        "p95": 0.0016448942478746176
      },
      {
        "phase": "path",
        "n": 156,
        "max": 0.0040264129638671875,
        "mean": 0.00020521115220617503,
        "p95": 0.0010318756103515625
      },
      {
        "phase": "path",
        "n": 315,
        "max": 0.0064449310302734375,
        "mean": 0.00021167936210986227,
        "p95": 0.0015335080679506063
      },
      {
        "phase": "summary",
        "n": 318,
        "max": 0.05766868591308594,
        "mean": 0.002638258971273899,
        "p95": 0.015489194542169571
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "main",
        "n": 116,
        "max": 0.07367515563964844,
        "mean": 0.004219943191856146,
        "p95": 0.017931461334228516
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 13,
    "id": "bigmath/cn_k12/155313",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 677,
    "reference_F": 921,
    "generation_seconds": 24.025099406018853,
    "T": 993,
    "native_replay_max": 0.09304618835449219,
    "native_replay_mean": 0.0027176078874617815,
    "native_replay_p95": 0.015945812687277794,
    "phases": [
      {
        "phase": "main",
        "n": 349,
        "max": 0.09304618835449219,
        "mean": 0.004511535167694092,
        "p95": 0.020206451416015625
      },
      {
        "phase": "width",
        "n": 2,
        "max": 7.62939453125e-06,
        "mean": 3.814697265625e-06,
        "p95": 7.24792471373803e-06
      },
      {
        "phase": "path",
        "n": 113,
        "max": 0.003604888916015625,
        "mean": 0.00023430005239788443,
        "p95": 0.0012096407590433955
      },
      {
        "phase": "path",
        "n": 118,
        "max": 0.0020122528076171875,
        "mean": 0.00019075103045906872,
        "p95": 0.0010326388292014599
      },
      {
        "phase": "path",
        "n": 102,
        "max": 0.004634857177734375,
        "mean": 0.00030631644767709076,
        "p95": 0.0017360677011311054
      },
      {
        "phase": "path",
        "n": 101,
        "max": 0.00603485107421875,
        "mean": 0.00035501233651302755,
        "p95": 0.0012493133544921875
      },
      {
        "phase": "summary",
        "n": 123,
        "max": 0.08955192565917969,
        "mean": 0.006483302917331457,
        "p95": 0.030646707862615585
      },
      {
        "phase": "main",
        "n": 2,
        "max": 0.0,
        "mean": 0.0,
        "p95": 0.0
      },
      {
        "phase": "main",
        "n": 83,
        "max": 0.0442962646484375,
        "mean": 0.002536382991820574,
        "p95": 0.01054477971047163
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 14,
    "id": "bigmath/cn_k12/95257",
    "correct": true,
    "reference_correct": true,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 982,
    "reference_F": 1763,
    "generation_seconds": 35.85037494683638,
    "T": 1321,
    "native_replay_max": 0.11869239807128906,
    "native_replay_mean": 0.0020441305823624134,
    "native_replay_p95": 0.012834548950195312,
    "phases": [
      {
        "phase": "main",
        "n": 462,
        "max": 0.06084251403808594,
        "mean": 0.002972371643409133,
        "p95": 0.015839193016290665
      },
      {
        "phase": "width",
        "n": 2,
        "max": 7.62939453125e-06,
        "mean": 3.814697265625e-06,
        "p95": 7.24792471373803e-06
      },
      {
        "phase": "path",
        "n": 97,
        "max": 0.0023937225341796875,
        "mean": 0.00015305980923585594,
        "p95": 0.0009765620925463736
      },
      {
        "phase": "path",
        "n": 113,
        "max": 0.00298309326171875,
        "mean": 0.0002031410695053637,
        "p95": 0.001083756098523736
      },
      {
        "phase": "path",
        "n": 130,
        "max": 0.005741119384765625,
        "mean": 0.00021250797726679593,
        "p95": 0.0013165470445528626
      },
      {
        "phase": "path",
        "n": 129,
        "max": 0.003849029541015625,
        "mean": 0.0001738348655635491,
        "p95": 0.0009342188131995499
      },
      {
        "phase": "summary",
        "n": 302,
        "max": 0.11869239807128906,
        "mean": 0.003395825857296586,
        "p95": 0.019138136878609657
      },
      {
        "phase": "main",
        "n": 2,
        "max": 3.814697265625e-06,
        "mean": 1.9073486328125e-06,
        "p95": 3.623962356869015e-06
      },
      {
        "phase": "main",
        "n": 84,
        "max": 0.03167724609375,
        "mean": 0.0025435402058064938,
        "p95": 0.01596326380968094
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/progress-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": 2,
  "latest": {
    "index": 15,
    "id": "bigmath/cn_k12/3177",
    "correct": false,
    "reference_correct": false,
    "format_valid": true,
    "reference_format_valid": true,
    "exact_ids": false,
    "F": 750,
    "reference_F": 724,
    "generation_seconds": 24.991211500018835,
    "T": 1207,
    "native_replay_max": 0.06701278686523438,
    "native_replay_mean": 0.0018851700006052852,
    "native_replay_p95": 0.011677922680974007,
    "phases": [
      {
        "phase": "main",
        "n": 173,
        "max": 0.06701278686523438,
        "mean": 0.0033819605596363544,
        "p95": 0.01398466806858778
      },
      {
        "phase": "width",
        "n": 2,
        "max": 1.1444091796875e-05,
        "mean": 5.7220458984375e-06,
        "p95": 1.087188684323337e-05
      },
      {
        "phase": "path",
        "n": 132,
        "max": 0.0048828125,
        "mean": 0.00019207867444492877,
        "p95": 0.000807380594778806
      },
      {
        "phase": "path",
        "n": 155,
        "max": 0.00283050537109375,
        "mean": 0.0002194558474002406,
        "p95": 0.0011772159487009048
      },
      {
        "phase": "path",
        "n": 255,
        "max": 0.004322052001953125,
        "mean": 0.00015709073340985924,
        "p95": 0.0009054186521098018
      },
      {
        "phase": "path",
        "n": 170,
        "max": 0.003849029541015625,
        "mean": 0.00010800080781336874,
        "p95": 0.00066633231472224
      },
      {
        "phase": "summary",
        "n": 183,
        "max": 0.06531524658203125,
        "mean": 0.005018140655010939,
        "p95": 0.026674244552850723
      },
      {
        "phase": "main",
        "n": 2,
        "max": 1.9073486328125e-06,
        "mean": 9.5367431640625e-07,
        "p95": 1.8119811784345075e-06
      },
      {
        "phase": "main",
        "n": 135,
        "max": 0.05817985534667969,
        "mean": 0.004845922812819481,
        "p95": 0.0314168781042099
      }
    ]
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-0.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 0,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 0,
      "id": "bigmath/cn_k12/26444",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 663,
      "reference_F": 752,
      "generation_seconds": 24.501509244088084,
      "T": 1035,
      "native_replay_max": 0.032817840576171875,
      "native_replay_mean": 0.0009608061518520117,
      "native_replay_p95": 0.006487837061285973,
      "phases": [
        {
          "phase": "main",
          "n": 153,
          "max": 0.027334213256835938,
          "mean": 0.002685783663764596,
          "p95": 0.013596720062196255
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 163,
          "max": 0.00189971923828125,
          "mean": 9.811729250941426e-05,
          "p95": 0.0005388258141465485
        },
        {
          "phase": "path",
          "n": 117,
          "max": 0.0030117034912109375,
          "mean": 0.00017790509446058422,
          "p95": 0.0008644103654660285
        },
        {
          "phase": "path",
          "n": 92,
          "max": 0.001407623291015625,
          "mean": 0.00011010791786247864,
          "p95": 0.0007193563506007195
        },
        {
          "phase": "path",
          "n": 293,
          "max": 0.0058383941650390625,
          "mean": 9.521119500277564e-05,
          "p95": 0.00045394879998639226
        },
        {
          "phase": "summary",
          "n": 166,
          "max": 0.032817840576171875,
          "mean": 0.0023615160025656223,
          "p95": 0.01234292984008789
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 47,
          "max": 0.024129867553710938,
          "mean": 0.002481906907632947,
          "p95": 0.012018585577607155
        }
      ]
    },
    {
      "index": 8,
      "id": "bigmath/cn_k12/23250",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 534,
      "reference_F": 521,
      "generation_seconds": 19.606840312946588,
      "T": 879,
      "native_replay_max": 0.08813667297363281,
      "native_replay_mean": 0.0019351592054590583,
      "native_replay_p95": 0.010074611753225327,
      "phases": [
        {
          "phase": "main",
          "n": 129,
          "max": 0.08813667297363281,
          "mean": 0.005713115446269512,
          "p95": 0.03315772861242294
        },
        {
          "phase": "width",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "path",
          "n": 165,
          "max": 0.006214141845703125,
          "mean": 0.0002929456240963191,
          "p95": 0.001667786156758666
        },
        {
          "phase": "path",
          "n": 113,
          "max": 0.00548553466796875,
          "mean": 0.00025492641725577414,
          "p95": 0.001412201439961791
        },
        {
          "phase": "path",
          "n": 67,
          "max": 0.00262451171875,
          "mean": 0.0003022151067852974,
          "p95": 0.0016523362137377262
        },
        {
          "phase": "path",
          "n": 196,
          "max": 0.0024738311767578125,
          "mean": 0.00013521740038413554,
          "p95": 0.00092315673828125
        },
        {
          "phase": "summary",
          "n": 122,
          "max": 0.04353904724121094,
          "mean": 0.004833276383578777,
          "p95": 0.02461652271449566
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 83,
          "max": 0.0564117431640625,
          "mean": 0.003017471404746175,
          "p95": 0.017878539860248566
        }
      ]
    }
  ],
  "actions": 1914,
  "native_replay_max": 0.08813667297363281,
  "native_replay_mean": 0.0014082755660638213,
  "native_replay_p95": 0.008205079473555088,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17353508352,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-1.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 1,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 1,
      "id": "bigmath/cn_k12/88253",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 962,
      "reference_F": 1344,
      "generation_seconds": 35.14693601289764,
      "T": 1267,
      "native_replay_max": 0.11616706848144531,
      "native_replay_mean": 0.0018413305515423417,
      "native_replay_p95": 0.00984630174934864,
      "phases": [
        {
          "phase": "main",
          "n": 204,
          "max": 0.06502151489257812,
          "mean": 0.003593557048588991,
          "p95": 0.022437462583184242
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.52587890625e-05,
          "mean": 7.62939453125e-06,
          "p95": 1.449584942747606e-05
        },
        {
          "phase": "path",
          "n": 82,
          "max": 0.0043506622314453125,
          "mean": 0.0002763329539448023,
          "p95": 0.0012412065407261252
        },
        {
          "phase": "path",
          "n": 103,
          "max": 0.0025539398193359375,
          "mean": 0.00022769668430555612,
          "p95": 0.0015220643253996968
        },
        {
          "phase": "path",
          "n": 120,
          "max": 0.00379180908203125,
          "mean": 0.00023496945505030453,
          "p95": 0.0012608517426997423
        },
        {
          "phase": "path",
          "n": 388,
          "max": 0.0056018829345703125,
          "mean": 0.0002972907677758485,
          "p95": 0.0015496253035962582
        },
        {
          "phase": "summary",
          "n": 207,
          "max": 0.11616706848144531,
          "mean": 0.003526116255670786,
          "p95": 0.014436528086662292
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 159,
          "max": 0.09050941467285156,
          "mean": 0.004278614651411772,
          "p95": 0.01994342729449272
        }
      ]
    },
    {
      "index": 9,
      "id": "bigmath/cn_k12/64731",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1427,
      "reference_F": 2172,
      "generation_seconds": 54.49747964460403,
      "T": 2389,
      "native_replay_max": 0.08221244812011719,
      "native_replay_mean": 0.0009210010757669806,
      "native_replay_p95": 0.003775389399379492,
      "phases": [
        {
          "phase": "main",
          "n": 208,
          "max": 0.056182861328125,
          "mean": 0.003652811050415039,
          "p95": 0.015315532684326172
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.5367431640625e-06,
          "mean": 4.76837158203125e-06,
          "p95": 9.059906005859375e-06
        },
        {
          "phase": "path",
          "n": 182,
          "max": 0.003345489501953125,
          "mean": 0.00018247666594106704,
          "p95": 0.0012119290186092257
        },
        {
          "phase": "path",
          "n": 345,
          "max": 0.009584426879882812,
          "mean": 0.0001361681061098352,
          "p95": 0.0008647918002679944
        },
        {
          "phase": "path",
          "n": 435,
          "max": 0.0075244903564453125,
          "mean": 0.00016148446593433619,
          "p95": 0.0010055538732558489
        },
        {
          "phase": "path",
          "n": 738,
          "max": 0.0042362213134765625,
          "mean": 0.00022910669213160872,
          "p95": 0.001364514697343111
        },
        {
          "phase": "summary",
          "n": 295,
          "max": 0.08221244812011719,
          "mean": 0.0031856149435043335,
          "p95": 0.021494099870324135
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 182,
          "max": 0.03674507141113281,
          "mean": 0.0009956255089491606,
          "p95": 0.008669553324580193
        }
      ]
    }
  ],
  "actions": 3656,
  "native_replay_max": 0.11616706848144531,
  "native_replay_mean": 0.0012399445986375213,
  "native_replay_p95": 0.006131172180175781,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17980936704,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-2.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 2,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 2,
      "id": "bigmath/cn_k12/163846",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 432,
      "reference_F": 463,
      "generation_seconds": 16.547977556940168,
      "T": 659,
      "native_replay_max": 0.05200386047363281,
      "native_replay_mean": 0.0017952376510947943,
      "native_replay_p95": 0.010357855819165707,
      "phases": [
        {
          "phase": "main",
          "n": 128,
          "max": 0.045871734619140625,
          "mean": 0.002897121012210846,
          "p95": 0.018284037709236145
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 76,
          "max": 0.0020389556884765625,
          "mean": 0.00024011261120904237,
          "p95": 0.0010666847229003906
        },
        {
          "phase": "path",
          "n": 61,
          "max": 0.00433349609375,
          "mean": 0.0003913504187949002,
          "p95": 0.0018520355224609375
        },
        {
          "phase": "path",
          "n": 103,
          "max": 0.0046291351318359375,
          "mean": 0.00035328540252521634,
          "p95": 0.0014844895340502262
        },
        {
          "phase": "path",
          "n": 90,
          "max": 0.004535675048828125,
          "mean": 0.0003840552526526153,
          "p95": 0.0024575211573392153
        },
        {
          "phase": "summary",
          "n": 134,
          "max": 0.041233062744140625,
          "mean": 0.0038498551584780216,
          "p95": 0.024791905656456947
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 63,
          "max": 0.05200386047363281,
          "mean": 0.0029089185409247875,
          "p95": 0.013295553624629974
        }
      ]
    },
    {
      "index": 10,
      "id": "bigmath/cn_k12/204933",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 602,
      "reference_F": 764,
      "generation_seconds": 21.97192501835525,
      "T": 1000,
      "native_replay_max": 0.13114166259765625,
      "native_replay_mean": 0.0022616805508732796,
      "native_replay_p95": 0.012234872207045555,
      "phases": [
        {
          "phase": "main",
          "n": 163,
          "max": 0.13114166259765625,
          "mean": 0.006094037555158138,
          "p95": 0.03166484087705612
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 187,
          "max": 0.00336456298828125,
          "mean": 0.00023563405557069927,
          "p95": 0.0013193129561841488
        },
        {
          "phase": "path",
          "n": 178,
          "max": 0.0031642913818359375,
          "mean": 0.00025751348584890366,
          "p95": 0.0013811102835461497
        },
        {
          "phase": "path",
          "n": 60,
          "max": 0.0062618255615234375,
          "mean": 0.00037298203096725047,
          "p95": 0.0014635083498433232
        },
        {
          "phase": "path",
          "n": 160,
          "max": 0.013608932495117188,
          "mean": 0.0005142688751220703,
          "p95": 0.002839660970494151
        },
        {
          "phase": "summary",
          "n": 187,
          "max": 0.06442070007324219,
          "mean": 0.005193893797695637,
          "p95": 0.03137664496898651
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 61,
          "max": 0.021625518798828125,
          "mean": 0.0016805930063128471,
          "p95": 0.011751174926757812
        }
      ]
    }
  ],
  "actions": 1659,
  "native_replay_max": 0.13114166259765625,
  "native_replay_mean": 0.002076396718621254,
  "native_replay_p95": 0.01170654222369194,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17222279168,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-3.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 3,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 3,
      "id": "bigmath/cn_k12/210293",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 819,
      "reference_F": 710,
      "generation_seconds": 29.9422858459875,
      "T": 1327,
      "native_replay_max": 0.057170867919921875,
      "native_replay_mean": 0.0012393705546855927,
      "native_replay_p95": 0.006729691755026579,
      "phases": [
        {
          "phase": "main",
          "n": 116,
          "max": 0.057170867919921875,
          "mean": 0.003984533715993166,
          "p95": 0.02294301986694336
        },
        {
          "phase": "width",
          "n": 2,
          "max": 9.5367431640625e-06,
          "mean": 4.76837158203125e-06,
          "p95": 9.059906005859375e-06
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.004497528076171875,
          "mean": 0.00019637132936622947,
          "p95": 0.000957489013671875
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.0068187713623046875,
          "mean": 0.00015767414879519492,
          "p95": 0.0006680488586425781
        },
        {
          "phase": "path",
          "n": 196,
          "max": 0.0052661895751953125,
          "mean": 0.00020482589025050402,
          "p95": 0.0010328292846679688
        },
        {
          "phase": "path",
          "n": 339,
          "max": 0.005512237548828125,
          "mean": 0.0001647099561523646,
          "p95": 0.0009197235340252519
        },
        {
          "phase": "summary",
          "n": 260,
          "max": 0.05585670471191406,
          "mean": 0.0033270029816776514,
          "p95": 0.017574980854988098
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 100,
          "max": 0.022737503051757812,
          "mean": 0.0016619492089375854,
          "p95": 0.01188305951654911
        }
      ]
    },
    {
      "index": 11,
      "id": "bigmath/cn_k12/147481",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 1110,
      "reference_F": 1086,
      "generation_seconds": 40.82329851295799,
      "T": 1801,
      "native_replay_max": 0.09502220153808594,
      "native_replay_mean": 0.0019491800339892507,
      "native_replay_p95": 0.011135101318359375,
      "phases": [
        {
          "phase": "main",
          "n": 542,
          "max": 0.09502220153808594,
          "mean": 0.004055209923535585,
          "p95": 0.022695835679769516
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.9073486328125e-05,
          "mean": 9.5367431640625e-06,
          "p95": 1.811981201171875e-05
        },
        {
          "phase": "path",
          "n": 205,
          "max": 0.00298309326171875,
          "mean": 0.0001334120606770739,
          "p95": 0.0009178161853924394
        },
        {
          "phase": "path",
          "n": 253,
          "max": 0.008516311645507812,
          "mean": 0.0002605754998512566,
          "p95": 0.001305770711041987
        },
        {
          "phase": "path",
          "n": 288,
          "max": 0.004375457763671875,
          "mean": 0.000273393263341859,
          "p95": 0.0016633985796943307
        },
        {
          "phase": "path",
          "n": 233,
          "max": 0.003643035888671875,
          "mean": 0.00018742770771495998,
          "p95": 0.0012680049985647202
        },
        {
          "phase": "summary",
          "n": 189,
          "max": 0.06942367553710938,
          "mean": 0.004943524487316608,
          "p95": 0.024516288191080093
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 87,
          "max": 0.03901863098144531,
          "mean": 0.0018680616049095988,
          "p95": 0.009404557757079601
        }
      ]
    }
  ],
  "actions": 3128,
  "native_replay_max": 0.09502220153808594,
  "native_replay_mean": 0.0016480556223541498,
  "native_replay_p95": 0.009671589359641075,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 18011250176,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-4.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 4,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 4,
      "id": "bigmath/cn_k12/88674",
      "correct": true,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": false,
      "exact_ids": false,
      "F": 1712,
      "reference_F": 2255,
      "generation_seconds": 62.80294936988503,
      "T": 2174,
      "native_replay_max": 0.12339591979980469,
      "native_replay_mean": 0.0021091315429657698,
      "native_replay_p95": 0.012638659216463566,
      "phases": [
        {
          "phase": "main",
          "n": 226,
          "max": 0.12339591979980469,
          "mean": 0.004755965434014797,
          "p95": 0.0198974609375
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.52587890625e-05,
          "mean": 7.62939453125e-06,
          "p95": 1.449584942747606e-05
        },
        {
          "phase": "path",
          "n": 193,
          "max": 0.002529144287109375,
          "mean": 0.000182344505446963,
          "p95": 0.0010887144599109888
        },
        {
          "phase": "path",
          "n": 100,
          "max": 0.003261566162109375,
          "mean": 0.0002424240083200857,
          "p95": 0.001349449041299522
        },
        {
          "phase": "path",
          "n": 169,
          "max": 0.0035228729248046875,
          "mean": 0.0003593038418330252,
          "p95": 0.001699447282589972
        },
        {
          "phase": "path",
          "n": 434,
          "max": 0.0068874359130859375,
          "mean": 0.0005163223249837756,
          "p95": 0.002716255374252796
        },
        {
          "phase": "summary",
          "n": 959,
          "max": 0.05884742736816406,
          "mean": 0.002840279834344983,
          "p95": 0.014988889917731285
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 89,
          "max": 0.11020088195800781,
          "mean": 0.004969853907823563,
          "p95": 0.016344832256436348
        }
      ]
    },
    {
      "index": 12,
      "id": "bigmath/cn_k12/61311",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 909,
      "reference_F": 952,
      "generation_seconds": 33.18680120212957,
      "T": 1602,
      "native_replay_max": 0.10259056091308594,
      "native_replay_mean": 0.0016089961864054203,
      "native_replay_p95": 0.009822364896535873,
      "phases": [
        {
          "phase": "main",
          "n": 156,
          "max": 0.10259056091308594,
          "mean": 0.006456081755459309,
          "p95": 0.027561664581298828
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 283,
          "max": 0.00653839111328125,
          "mean": 0.00019926064123865217,
          "p95": 0.0010412211995571852
        },
        {
          "phase": "path",
          "n": 254,
          "max": 0.01233673095703125,
          "mean": 0.0003420837165322155,
          "p95": 0.0016448942478746176
        },
        {
          "phase": "path",
          "n": 156,
          "max": 0.0040264129638671875,
          "mean": 0.00020521115220617503,
          "p95": 0.0010318756103515625
        },
        {
          "phase": "path",
          "n": 315,
          "max": 0.0064449310302734375,
          "mean": 0.00021167936210986227,
          "p95": 0.0015335080679506063
        },
        {
          "phase": "summary",
          "n": 318,
          "max": 0.05766868591308594,
          "mean": 0.002638258971273899,
          "p95": 0.015489194542169571
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 116,
          "max": 0.07367515563964844,
          "mean": 0.004219943191856146,
          "p95": 0.017931461334228516
        }
      ]
    }
  ],
  "actions": 3776,
  "native_replay_max": 0.12339591979980469,
  "native_replay_mean": 0.0018969448283314705,
  "native_replay_p95": 0.011370182037353516,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17986467328,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-5.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 5,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 5,
      "id": "bigmath/cn_k12/165159",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 467,
      "reference_F": 540,
      "generation_seconds": 17.071274040732533,
      "T": 657,
      "native_replay_max": 0.12002944946289062,
      "native_replay_mean": 0.0024303540121763945,
      "native_replay_p95": 0.011124424636363983,
      "phases": [
        {
          "phase": "main",
          "n": 133,
          "max": 0.05920696258544922,
          "mean": 0.003760094055905938,
          "p95": 0.020089726895093918
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 63,
          "max": 0.0025234222412109375,
          "mean": 0.0003315456269774586,
          "p95": 0.0019359583966434002
        },
        {
          "phase": "path",
          "n": 65,
          "max": 0.0073261260986328125,
          "mean": 0.00033296438050456345,
          "p95": 0.0012458800338208675
        },
        {
          "phase": "path",
          "n": 62,
          "max": 0.0038051605224609375,
          "mean": 0.0002985615865327418,
          "p95": 0.0012866022298112512
        },
        {
          "phase": "path",
          "n": 145,
          "max": 0.0054950714111328125,
          "mean": 0.0003246833512093872,
          "p95": 0.0017620099242776632
        },
        {
          "phase": "summary",
          "n": 140,
          "max": 0.048168182373046875,
          "mean": 0.004884079564362764,
          "p95": 0.026228144764900208
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "main",
          "n": 45,
          "max": 0.12002944946289062,
          "mean": 0.006772083695977926,
          "p95": 0.04071367532014847
        }
      ]
    },
    {
      "index": 13,
      "id": "bigmath/cn_k12/155313",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 677,
      "reference_F": 921,
      "generation_seconds": 24.025099406018853,
      "T": 993,
      "native_replay_max": 0.09304618835449219,
      "native_replay_mean": 0.0027176078874617815,
      "native_replay_p95": 0.015945812687277794,
      "phases": [
        {
          "phase": "main",
          "n": 349,
          "max": 0.09304618835449219,
          "mean": 0.004511535167694092,
          "p95": 0.020206451416015625
        },
        {
          "phase": "width",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "path",
          "n": 113,
          "max": 0.003604888916015625,
          "mean": 0.00023430005239788443,
          "p95": 0.0012096407590433955
        },
        {
          "phase": "path",
          "n": 118,
          "max": 0.0020122528076171875,
          "mean": 0.00019075103045906872,
          "p95": 0.0010326388292014599
        },
        {
          "phase": "path",
          "n": 102,
          "max": 0.004634857177734375,
          "mean": 0.00030631644767709076,
          "p95": 0.0017360677011311054
        },
        {
          "phase": "path",
          "n": 101,
          "max": 0.00603485107421875,
          "mean": 0.00035501233651302755,
          "p95": 0.0012493133544921875
        },
        {
          "phase": "summary",
          "n": 123,
          "max": 0.08955192565917969,
          "mean": 0.006483302917331457,
          "p95": 0.030646707862615585
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 83,
          "max": 0.0442962646484375,
          "mean": 0.002536382991820574,
          "p95": 0.01054477971047163
        }
      ]
    }
  ],
  "actions": 1650,
  "native_replay_max": 0.12002944946289062,
  "native_replay_mean": 0.0026032286696135998,
  "native_replay_p95": 0.013930120505392551,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17641915392,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-6.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 6,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 6,
      "id": "bigmath/cn_k12/176142",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 762,
      "reference_F": 710,
      "generation_seconds": 28.96483332896605,
      "T": 1440,
      "native_replay_max": 0.051990509033203125,
      "native_replay_mean": 0.0014114114455878735,
      "native_replay_p95": 0.007985012605786324,
      "phases": [
        {
          "phase": "main",
          "n": 187,
          "max": 0.05145454406738281,
          "mean": 0.004928384907543659,
          "p95": 0.020949549973011017
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.33514404296875e-05,
          "mean": 6.67572021484375e-06,
          "p95": 1.2683868590102065e-05
        },
        {
          "phase": "path",
          "n": 270,
          "max": 0.00411224365234375,
          "mean": 0.0001489427377237007,
          "p95": 0.0008992196526378393
        },
        {
          "phase": "path",
          "n": 210,
          "max": 0.0036258697509765625,
          "mean": 0.00016849154781084508,
          "p95": 0.0009519577142782509
        },
        {
          "phase": "path",
          "n": 198,
          "max": 0.003871917724609375,
          "mean": 0.00028440688038244843,
          "p95": 0.0015420907875522971
        },
        {
          "phase": "path",
          "n": 323,
          "max": 0.0041561126708984375,
          "mean": 0.0001981575769605115,
          "p95": 0.0012018200941383839
        },
        {
          "phase": "summary",
          "n": 176,
          "max": 0.051990509033203125,
          "mean": 0.0042802635580301285,
          "p95": 0.022179603576660156
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 72,
          "max": 0.048675537109375,
          "mean": 0.0022439956665039062,
          "p95": 0.014331434853374958
        }
      ]
    },
    {
      "index": 14,
      "id": "bigmath/cn_k12/95257",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 982,
      "reference_F": 1763,
      "generation_seconds": 35.85037494683638,
      "T": 1321,
      "native_replay_max": 0.11869239807128906,
      "native_replay_mean": 0.0020441305823624134,
      "native_replay_p95": 0.012834548950195312,
      "phases": [
        {
          "phase": "main",
          "n": 462,
          "max": 0.06084251403808594,
          "mean": 0.002972371643409133,
          "p95": 0.015839193016290665
        },
        {
          "phase": "width",
          "n": 2,
          "max": 7.62939453125e-06,
          "mean": 3.814697265625e-06,
          "p95": 7.24792471373803e-06
        },
        {
          "phase": "path",
          "n": 97,
          "max": 0.0023937225341796875,
          "mean": 0.00015305980923585594,
          "p95": 0.0009765620925463736
        },
        {
          "phase": "path",
          "n": 113,
          "max": 0.00298309326171875,
          "mean": 0.0002031410695053637,
          "p95": 0.001083756098523736
        },
        {
          "phase": "path",
          "n": 130,
          "max": 0.005741119384765625,
          "mean": 0.00021250797726679593,
          "p95": 0.0013165470445528626
        },
        {
          "phase": "path",
          "n": 129,
          "max": 0.003849029541015625,
          "mean": 0.0001738348655635491,
          "p95": 0.0009342188131995499
        },
        {
          "phase": "summary",
          "n": 302,
          "max": 0.11869239807128906,
          "mean": 0.003395825857296586,
          "p95": 0.019138136878609657
        },
        {
          "phase": "main",
          "n": 2,
          "max": 3.814697265625e-06,
          "mean": 1.9073486328125e-06,
          "p95": 3.623962356869015e-06
        },
        {
          "phase": "main",
          "n": 84,
          "max": 0.03167724609375,
          "mean": 0.0025435402058064938,
          "p95": 0.01596326380968094
        }
      ]
    }
  ],
  "actions": 2761,
  "native_replay_max": 0.11869239807128906,
  "native_replay_mean": 0.0017141357529908419,
  "native_replay_p95": 0.010869979858398438,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 2,
  "reference_correct": 2,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 17876691456,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/lanes/profile_precision/tf32-native/result-rank-7.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "rank": 7,
  "precision": "tf32",
  "master_dtype": "float32",
  "lm_head_dtype": "float32",
  "cases": [
    {
      "index": 7,
      "id": "bigmath/cn_k12/60327",
      "correct": true,
      "reference_correct": true,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 2509,
      "reference_F": 1069,
      "generation_seconds": 97.45404178509489,
      "T": 2924,
      "native_replay_max": 0.132720947265625,
      "native_replay_mean": 0.002162820426747203,
      "native_replay_p95": 0.012365140952169895,
      "phases": [
        {
          "phase": "main",
          "n": 294,
          "max": 0.04360771179199219,
          "mean": 0.004060972481966019,
          "p95": 0.020407967269420624
        },
        {
          "phase": "width",
          "n": 2,
          "max": 2.09808349609375e-05,
          "mean": 1.049041748046875e-05,
          "p95": 1.9931792849092744e-05
        },
        {
          "phase": "path",
          "n": 113,
          "max": 0.002719879150390625,
          "mean": 0.00027838849928230047,
          "p95": 0.001478576916269958
        },
        {
          "phase": "path",
          "n": 122,
          "max": 0.002445220947265625,
          "mean": 0.00012360243999864906,
          "p95": 0.0006518359296023846
        },
        {
          "phase": "path",
          "n": 180,
          "max": 0.005603790283203125,
          "mean": 0.00044700835132971406,
          "p95": 0.002238178625702858
        },
        {
          "phase": "path",
          "n": 768,
          "max": 0.008855819702148438,
          "mean": 0.0003103961644228548,
          "p95": 0.0017398814670741558
        },
        {
          "phase": "summary",
          "n": 1280,
          "max": 0.132720947265625,
          "mean": 0.00334947113879025,
          "p95": 0.017845232039690018
        },
        {
          "phase": "main",
          "n": 2,
          "max": 0.0,
          "mean": 0.0,
          "p95": 0.0
        },
        {
          "phase": "main",
          "n": 163,
          "max": 0.04243659973144531,
          "mean": 0.0029290439561009407,
          "p95": 0.015556521713733673
        }
      ]
    },
    {
      "index": 15,
      "id": "bigmath/cn_k12/3177",
      "correct": false,
      "reference_correct": false,
      "format_valid": true,
      "reference_format_valid": true,
      "exact_ids": false,
      "F": 750,
      "reference_F": 724,
      "generation_seconds": 24.991211500018835,
      "T": 1207,
      "native_replay_max": 0.06701278686523438,
      "native_replay_mean": 0.0018851700006052852,
      "native_replay_p95": 0.011677922680974007,
      "phases": [
        {
          "phase": "main",
          "n": 173,
          "max": 0.06701278686523438,
          "mean": 0.0033819605596363544,
          "p95": 0.01398466806858778
        },
        {
          "phase": "width",
          "n": 2,
          "max": 1.1444091796875e-05,
          "mean": 5.7220458984375e-06,
          "p95": 1.087188684323337e-05
        },
        {
          "phase": "path",
          "n": 132,
          "max": 0.0048828125,
          "mean": 0.00019207867444492877,
          "p95": 0.000807380594778806
        },
        {
          "phase": "path",
          "n": 155,
          "max": 0.00283050537109375,
          "mean": 0.0002194558474002406,
          "p95": 0.0011772159487009048
        },
        {
          "phase": "path",
          "n": 255,
          "max": 0.004322052001953125,
          "mean": 0.00015709073340985924,
          "p95": 0.0009054186521098018
        },
        {
          "phase": "path",
          "n": 170,
          "max": 0.003849029541015625,
          "mean": 0.00010800080781336874,
          "p95": 0.00066633231472224
        },
        {
          "phase": "summary",
          "n": 183,
          "max": 0.06531524658203125,
          "mean": 0.005018140655010939,
          "p95": 0.026674244552850723
        },
        {
          "phase": "main",
          "n": 2,
          "max": 1.9073486328125e-06,
          "mean": 9.5367431640625e-07,
          "p95": 1.8119811784345075e-06
        },
        {
          "phase": "main",
          "n": 135,
          "max": 0.05817985534667969,
          "mean": 0.004845922812819481,
          "p95": 0.0314168781042099
        }
      ]
    }
  ],
  "actions": 4131,
  "native_replay_max": 0.132720947265625,
  "native_replay_mean": 0.0020816961769014597,
  "native_replay_p95": 0.012302398681640625,
  "unchanged_thresholds": {
    "max": 0.01,
    "mean": 0.002,
    "p95": 0.005
  },
  "native_guard_passed": false,
  "correct": 1,
  "reference_correct": 1,
  "quality_not_benchmark": true,
  "optimizer_updates": 0,
  "peak_gpu_bytes": 18588331008,
  "actual_backend_flags": {
    "cuda_tf32": true,
    "float32_precision": "high"
  },
  "generation_is_cached": true,
  "teacher_is_full_prefix": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/async-lag1/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/async-lag1/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/existing-backends/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/existing-backends/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-acceleration-20261012/research/structured-serving/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/structured-serving/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/RESULT.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/RESULT.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/all8-exits.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/all8-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "0": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "7": 0,
  "1": 0,
  "6": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/pilot-exits.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/pilot-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "1": 0,
  "0": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/status.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/attempt1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "host": "RUN_5482aee87e-mpiworker-2",
  "time": 1791821867.0580482,
  "all8_exit0": true,
  "all8_GPU_empty": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/exits.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "1": 0,
  "7": 0,
  "0": 0,
  "4": 0,
  "6": 0,
  "3": 0,
  "5": 0,
  "2": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-0.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 0,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 22.55732887517661,
  "responses_per_s": 0.17732596009635837,
  "sampled_tokens": 2627,
  "raw_tokens_per_s": 116.45882429328337,
  "global_backend_F": 612,
  "sum_episode_F": 1873,
  "peak_allocated_bytes": 18357167104,
  "peak_reserved_bytes": 22177382400,
  "physical_slot_high_water": 3113,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-1.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 1,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 19.765358191914856,
  "responses_per_s": 0.20237427326949353,
  "sampled_tokens": 1968,
  "raw_tokens_per_s": 99.56814244859082,
  "global_backend_F": 529,
  "sum_episode_F": 1543,
  "peak_allocated_bytes": 18353243136,
  "peak_reserved_bytes": 20040384512,
  "physical_slot_high_water": 2432,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-2.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 2,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 73.1695837713778,
  "responses_per_s": 0.05466752431581693,
  "sampled_tokens": 5339,
  "raw_tokens_per_s": 72.96747808053665,
  "global_backend_F": 2047,
  "sum_episode_F": 4212,
  "peak_allocated_bytes": 18384659456,
  "peak_reserved_bytes": 21034434560,
  "physical_slot_high_water": 5773,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-3.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 3,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 27.153430693782866,
  "responses_per_s": 0.14731103576226381,
  "sampled_tokens": 3267,
  "raw_tokens_per_s": 120.31628845882898,
  "global_backend_F": 721,
  "sum_episode_F": 2198,
  "peak_allocated_bytes": 18433763840,
  "peak_reserved_bytes": 20740833280,
  "physical_slot_high_water": 3717,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-4.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-4.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 4,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 20.613477080129087,
  "responses_per_s": 0.19404780593061163,
  "sampled_tokens": 2499,
  "raw_tokens_per_s": 121.23136675514962,
  "global_backend_F": 555,
  "sum_episode_F": 1853,
  "peak_allocated_bytes": 18274173952,
  "peak_reserved_bytes": 19778240512,
  "physical_slot_high_water": 2954,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-5.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-5.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 5,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 27.947308523580432,
  "responses_per_s": 0.14312648377660467,
  "sampled_tokens": 2862,
  "raw_tokens_per_s": 102.40699914216064,
  "global_backend_F": 752,
  "sum_episode_F": 2264,
  "peak_allocated_bytes": 18388272128,
  "peak_reserved_bytes": 21084766208,
  "physical_slot_high_water": 3312,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-6.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-6.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 6,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 22.394823107868433,
  "responses_per_s": 0.1786127079786845,
  "sampled_tokens": 2321,
  "raw_tokens_per_s": 103.64002380463168,
  "global_backend_F": 605,
  "sum_episode_F": 1832,
  "peak_allocated_bytes": 18441940992,
  "peak_reserved_bytes": 19864223744,
  "physical_slot_high_water": 2820,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-7.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/output/metrics-rank-7.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
  "rank": 7,
  "trajectories": 4,
  "actual_model_type": "Qwen3ForCausalLM",
  "actual_runner_type": "StructuredModelRunner",
  "actor_dtype": "bfloat16",
  "generation_wall": 18.529954022727907,
  "responses_per_s": 0.21586669859481583,
  "sampled_tokens": 2141,
  "raw_tokens_per_s": 115.54265042287517,
  "global_backend_F": 517,
  "sum_episode_F": 1677,
  "peak_allocated_bytes": 18173719040,
  "peak_reserved_bytes": 19386073088,
  "physical_slot_high_water": 2568,
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "source_sha256": {
    "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
    "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
    "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
    "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
    "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
    "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
    "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
    "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
    "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
    "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
    "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
    "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
    "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
  },
  "unknown": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/result.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "scope": "Frozen checkpoint50 vLLM BF16 actual actor-only fixed32; no learner/optimizer/full-RL3x claim",
  "responses": 32,
  "prompts": 8,
  "rollouts_per_prompt": 4,
  "n_per_trajectory": 1,
  "critical_generation_wall": 73.1695837713778,
  "responses_per_s": 0.43734019452653544,
  "sampled_tokens": 23024,
  "raw_tokens_per_s": 314.66626996184226,
  "backend_global_F": 6338,
  "sum_episode_F": 17452,
  "max_peak_allocated_bytes": 18441940992,
  "all8_exit0": true,
  "all8_GPU_empty": true,
  "correct": 27,
  "source_seal_sha256": "b29406fbfd8815e3163ff667ede8f1b00e6348f047c7d701eb13b1c88b678609",
  "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
  "metrics": [
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 0,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 22.55732887517661,
      "responses_per_s": 0.17732596009635837,
      "sampled_tokens": 2627,
      "raw_tokens_per_s": 116.45882429328337,
      "global_backend_F": 612,
      "sum_episode_F": 1873,
      "peak_allocated_bytes": 18357167104,
      "peak_reserved_bytes": 22177382400,
      "physical_slot_high_water": 3113,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 1,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 19.765358191914856,
      "responses_per_s": 0.20237427326949353,
      "sampled_tokens": 1968,
      "raw_tokens_per_s": 99.56814244859082,
      "global_backend_F": 529,
      "sum_episode_F": 1543,
      "peak_allocated_bytes": 18353243136,
      "peak_reserved_bytes": 20040384512,
      "physical_slot_high_water": 2432,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 2,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 73.1695837713778,
      "responses_per_s": 0.05466752431581693,
      "sampled_tokens": 5339,
      "raw_tokens_per_s": 72.96747808053665,
      "global_backend_F": 2047,
      "sum_episode_F": 4212,
      "peak_allocated_bytes": 18384659456,
      "peak_reserved_bytes": 21034434560,
      "physical_slot_high_water": 5773,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 3,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 27.153430693782866,
      "responses_per_s": 0.14731103576226381,
      "sampled_tokens": 3267,
      "raw_tokens_per_s": 120.31628845882898,
      "global_backend_F": 721,
      "sum_episode_F": 2198,
      "peak_allocated_bytes": 18433763840,
      "peak_reserved_bytes": 20740833280,
      "physical_slot_high_water": 3717,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 4,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 20.613477080129087,
      "responses_per_s": 0.19404780593061163,
      "sampled_tokens": 2499,
      "raw_tokens_per_s": 121.23136675514962,
      "global_backend_F": 555,
      "sum_episode_F": 1853,
      "peak_allocated_bytes": 18274173952,
      "peak_reserved_bytes": 19778240512,
      "physical_slot_high_water": 2954,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 5,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 27.947308523580432,
      "responses_per_s": 0.14312648377660467,
      "sampled_tokens": 2862,
      "raw_tokens_per_s": 102.40699914216064,
      "global_backend_F": 752,
      "sum_episode_F": 2264,
      "peak_allocated_bytes": 18388272128,
      "peak_reserved_bytes": 21084766208,
      "physical_slot_high_water": 3312,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 6,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 22.394823107868433,
      "responses_per_s": 0.1786127079786845,
      "sampled_tokens": 2321,
      "raw_tokens_per_s": 103.64002380463168,
      "global_backend_F": 605,
      "sum_episode_F": 1832,
      "peak_allocated_bytes": 18441940992,
      "peak_reserved_bytes": 19864223744,
      "physical_slot_high_water": 2820,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    },
    {
      "passed": true,
      "scope": "Actual vLLM actor-only fixed32 shard; no optimizer/full-RL3x claim",
      "rank": 7,
      "trajectories": 4,
      "actual_model_type": "Qwen3ForCausalLM",
      "actual_runner_type": "StructuredModelRunner",
      "actor_dtype": "bfloat16",
      "generation_wall": 18.529954022727907,
      "responses_per_s": 0.21586669859481583,
      "sampled_tokens": 2141,
      "raw_tokens_per_s": 115.54265042287517,
      "global_backend_F": 517,
      "sum_episode_F": 1677,
      "peak_allocated_bytes": 18173719040,
      "peak_reserved_bytes": 19386073088,
      "physical_slot_high_water": 2568,
      "config_sha256": "d3d0f9cf4c2887afc3c72c98c49ad62f2998e158d4cbe57a68aefc3c596c84f1",
      "source_sha256": {
        "engine_patch.py": "c8f21f8960f8848f22a78f4c3b1ddf86bcf22319136a5613b05a4b8aac32b0d1",
        "structured_adapter.py": "cc0eb8c1546b776037359b187e76f1499d6537a343b5f0aa74fb41fda2536a50",
        "proof_cpu.py": "ce4f1e3fca9f7ffba9fb91a83535ddda6b6badfb66d32968165ca15a49dc219d",
        "dag_backend.py": "56274b51eb68ef5ea0b638e122cb763614a5420b950e0e2f62cdb661ce689907",
        "proof_rollout_cpu.py": "4c264f156adff3f430be8df5a11ec957f39bead533c480e3a8e5a8621cb97240",
        "rollout.py": "c82112f4ea5d3ee1106663321ae6995e3f1d31b7336e9e5ba936bd959f8d6677",
        "slot_decoder.py": "4c42030c4c0d7ec6d89a403b27df27b09f4f175abd05e39655bc37373619be82",
        "structured_runner.py": "a89427b9f48cc2df2f27ec4f7448d89db238a00e6ab87defca8478e2dd39695e",
        "batching.py": "01facf67f7448a3813b7d4090ed56e8447dca6469dd0c9f9485773bd3f4bb3da",
        "cohort_decoder.py": "6942cdf138e9c17597a52e53033cb28e98ebdfcfb2dda3f995851ff6ed44e13f",
        "gpu_probe.py": "501fe1edd47832709d8fa94542a16e59a5af799595baae536361e9a758dfe216",
        "formatting.py": "a3a6f9790264f96b8e89ef9b176529335e428cc0e962fcc88899d438cc00ee6f",
        "fixed32_worker.py": "71b2f1be7838173e14901d66ad445e793d9f523e657b88162461b06254964eff"
      },
      "unknown": 0
    }
  ]
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/status.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/fixed32-attempt1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "host": "RUN_5482aee87e-mpiworker-1",
  "time": 1791820001.2585824,
  "critical_generation_wall": 73.1695837713778,
  "exits": {
    "1": 0,
    "7": 0,
    "0": 0,
    "4": 0,
    "6": 0,
    "3": 0,
    "5": 0,
    "2": 0
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/gpu-attempt1/exits.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/gpu-attempt1/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "1": 0,
  "3": 0,
  "5": 0,
  "7": 0,
  "0": 0,
  "2": 0,
  "4": 0,
  "6": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/gpu-attempt1/status.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/gpu-attempt1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "host": "RUN_5482aee87e-mpiworker-1",
  "time": 1791820001.2721307,
  "exits": {
    "1": 0,
    "3": 0,
    "5": 0,
    "7": 0,
    "0": 0,
    "2": 0,
    "4": 0,
    "6": 0
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/REPORT.md](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/REPORT.md) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/SUMMARY.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/SUMMARY.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "steps": [
    {
      "step": 51,
      "runner_wall_max": 107.346923828125,
      "full_wall_max": 107.87311280146241,
      "critical_rank": 5,
      "critical_host_phases": {
        "actor_weight_refresh": 0.0006964923813939095,
        "rollout_execute_and_scoring": 28.451371108181775,
        "reward_gather_and_advantages": 45.766935804858804,
        "fp32_layout_oracle": 3.00296725705266,
        "replay_forward": 4.3384439973160625,
        "backward": 7.586246155202389,
        "collective_parity_guard": 17.1333576021716,
        "clip_active_collective_optimizer": 0.8625826146453619,
        "serialization": 0.0003368314355611801,
        "cleanup": 0.47802263870835304,
        "metric_gather_write": 0.04124484583735466
      },
      "rank2_host_phases": {
        "actor_weight_refresh": 0.0004981318488717079,
        "rollout_execute_and_scoring": 73.40071031730622,
        "reward_gather_and_advantages": 0.006971490569412708,
        "fp32_layout_oracle": 4.349702478386462,
        "replay_forward": 5.019256567582488,
        "backward": 9.056510291993618,
        "collective_parity_guard": 13.63089652825147,
        "clip_active_collective_optimizer": 0.863342965953052,
        "serialization": 0.00022529065608978271,
        "cleanup": 0.5135489972308278,
        "metric_gather_write": 0.006279138848185539
      },
      "correct": 27,
      "tokens": 23024,
      "episode_F": 17452,
      "backend_generation_F": 6338,
      "backend_technical_F": 64,
      "same_actor_guard_max": 0.0,
      "FP32_layout_oracle_max": 6.67572021484375e-05,
      "peak_learner_allocated": 58409108480,
      "peak_actor_allocated": 18943004672,
      "min_free_stage": 2585919488,
      "all8positive_finite": true
    },
    {
      "step": 52,
      "runner_wall_max": 80.34493947029114,
      "full_wall_max": 80.63727418333292,
      "critical_rank": 0,
      "critical_host_phases": {
        "actor_weight_refresh": 0.00010538101196289062,
        "rollout_execute_and_scoring": 28.259150297380984,
        "reward_gather_and_advantages": 33.49145981762558,
        "fp32_layout_oracle": 2.260198164731264,
        "replay_forward": 3.7372412690892816,
        "backward": 7.403012934140861,
        "collective_parity_guard": 4.103722487576306,
        "clip_active_collective_optimizer": 0.964361266233027,
        "serialization": 0.0002707410603761673,
        "cleanup": 0.17233982682228088,
        "metric_gather_write": 0.13965195696800947
      },
      "rank2_host_phases": {
        "actor_weight_refresh": 0.00015700142830610275,
        "rollout_execute_and_scoring": 61.74333164282143,
        "reward_gather_and_advantages": 0.006110428832471371,
        "fp32_layout_oracle": 3.168406509794295,
        "replay_forward": 4.993690107949078,
        "backward": 9.225882405415177,
        "collective_parity_guard": 0.07274431269615889,
        "clip_active_collective_optimizer": 0.992659293115139,
        "serialization": 0.00026008952409029007,
        "cleanup": 0.17495958507061005,
        "metric_gather_write": 0.11277373507618904
      },
      "correct": 28,
      "tokens": 23033,
      "episode_F": 18071,
      "backend_generation_F": 7870,
      "backend_technical_F": 64,
      "same_actor_guard_max": 0.0,
      "FP32_layout_oracle_max": 3.24249267578125e-05,
      "peak_learner_allocated": 52571834368,
      "peak_actor_allocated": 18951524352,
      "min_free_stage": 10154541056,
      "all8positive_finite": true
    }
  ],
  "source_seal_sha256": "62feee9ac7ae7beef2ad4c6171e8422de08bc61fb088a67d4ebf3336a9095e05",
  "proof_sha256": "fcdee507dbb50f3e83ad5b647b48f11f97edaf2ffd93ef87f459f52ed60cf29c",
  "config_sha256": "c422c868c0f537dfd0b53638fa56e4026671c40f4cf4cdb007dfe1e71ea9c072",
  "all8_exit0_GPUempty": true,
  "time": 1791821743.9232485
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/exits.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "1": 0,
  "0": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 0,
  "7": 0
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/status.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "host": "RUN_5482aee87e-mpiworker-1",
  "time": 1791821442.5104733,
  "exits": {
    "1": 0,
    "0": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0
  }
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/metrics.jsonl](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/result.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 52,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/checkpoint-0052/hf",
  "initial_step": 50,
  "positive_updates": 2,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/status.json](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/training/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 52,
  "steps": 52
}
```

</details>

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/REPORT.md](../history/local_saved/818bc1b5fd12/work/experiments/rl-acceleration-20261012/lanes/kv_replay/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [work/experiments/rl-acceleration-20261012/lanes/compact_decode/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/compact_decode/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt2/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt3/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt4/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt5/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined-v2/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/full-mixed-combined/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/lanes/kv_replay/launch.py](../artifacts/work/experiments/rl-acceleration-20261012/lanes/kv_replay/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/controller.py](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-learner-contract/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/controller.py](../artifacts/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
