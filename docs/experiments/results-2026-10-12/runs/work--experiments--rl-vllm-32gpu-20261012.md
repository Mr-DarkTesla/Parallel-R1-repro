# work/experiments/rl-vllm-32gpu-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-vllm-32gpu-20261012/production-config.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/production-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-vllm-32gpu-20261012/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 32,
  "group": 1,
  "steps": 500,
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
  "checkpoint_every": 50,
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
  "output": "${PROJECT_ROOT}/work/experiments/rl-vllm-32gpu-20261012/production",
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
  "skip_validation": false,
  "skip_exports": false,
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
  "worker": "src/train.py",
  "skip_initial_validation": true
}
```

</details>

- [work/experiments/rl-vllm-32gpu-20261012/production/config.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/production/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-vllm-32gpu-20261012/src/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-acceleration-20261012/research/vllm-structured-prototype/learner-attempt1/proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 32,
  "group": 1,
  "steps": 500,
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
  "checkpoint_every": 50,
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
  "output": "${PROJECT_ROOT}/work/experiments/rl-vllm-32gpu-20261012/production",
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
  "skip_validation": false,
  "skip_exports": false,
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
  "worker": "src/train.py",
  "skip_initial_validation": true
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-vllm-32gpu-20261012/control/status-node-0.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/control/status-node-0.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "production",
  "node": 0,
  "host": "RUN_5482aee87e-mpimaster-0",
  "active": {
    "0": 10284,
    "1": 10285,
    "2": 10286,
    "3": 10287,
    "4": 10288,
    "5": 10289,
    "6": 10290,
    "7": 10291
  },
  "exits": {},
  "time": 1791826573.7214184
}
```

</details>

- [work/experiments/rl-vllm-32gpu-20261012/control/status-node-1.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/control/status-node-1.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "production",
  "node": 1,
  "host": "RUN_5482aee87e-mpiworker-0",
  "active": {
    "8": 8507,
    "9": 8508,
    "10": 8509,
    "11": 8510,
    "12": 8511,
    "13": 8512,
    "14": 8513,
    "15": 8514
  },
  "exits": {},
  "time": 1791826573.7201185
}
```

</details>

- [work/experiments/rl-vllm-32gpu-20261012/control/status-node-2.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/control/status-node-2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "production",
  "node": 2,
  "host": "RUN_5482aee87e-mpiworker-1",
  "active": {
    "16": 5481,
    "17": 5482,
    "18": 5483,
    "19": 5484,
    "20": 5485,
    "21": 5486,
    "22": 5487,
    "23": 5488
  },
  "exits": {},
  "time": 1791826578.1343527
}
```

</details>

- [work/experiments/rl-vllm-32gpu-20261012/control/status-node-3.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/control/status-node-3.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "production",
  "node": 3,
  "host": "RUN_5482aee87e-mpiworker-2",
  "active": {
    "24": 4916,
    "25": 4917,
    "26": 4918,
    "27": 4919,
    "28": 4920,
    "29": 4921,
    "30": 4922,
    "31": 4923
  },
  "exits": {},
  "time": 1791826572.1369584
}
```

</details>

- [work/experiments/rl-vllm-32gpu-20261012/production/metrics.jsonl](../artifacts/work/experiments/rl-vllm-32gpu-20261012/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-vllm-32gpu-20261012/production/status.json](../artifacts/work/experiments/rl-vllm-32gpu-20261012/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 58,
  "steps": 500,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 1.0477840036117037e-05,
  "replay_guard_passed": true,
  "replay_parity_skips": 0,
  "max_replay_logp_drift": 5.53131103515625e-05
}
```

</details>
