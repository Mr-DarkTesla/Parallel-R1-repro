# work/experiments/rl-r2-24gpu-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-r2-24gpu-20261012/attempts/08-nfs-visibility/smoke/config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/attempts/08-nfs-visibility/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/data-manifest.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/data-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "train": 1024,
  "val": 32,
  "pilot": 16,
  "sources": {
    "cn_k12": 512,
    "orca_math": 512
  },
  "previous128_preserved": true,
  "group_disjoint": true,
  "benchmark_selection": false,
  "preparation_sha256": "39613274300ef17d95512edd853ac083d060f115486f4157a5d4a7a892887466",
  "train_sha256": "6bcab08da6bc6b22ddacc58ac5aeb5a18abcc509c4f68d7457cd79d8acb4e317",
  "val_sha256": "cb02ef017baff97bed5568e60a53f9673c04f657f59d81349f1a6484e3f30a6a",
  "teacher_verdicts_sha256": "3211744626808641f6ffe07b2d27a80ed2870c5727baff0949e1671ec3d63d5b",
  "new_gold_blind_teacher_corroborated": 720,
  "prior_reviewed": 304,
  "rejected_or_unknown": 245,
  "limitations": [
    "Teacher agreement corroborates references; it is not an exact oracle or proof that every semantic paraphrase of benchmarks is absent.",
    "Published original per-item source URLs unavailable; only pinned CNK12/Orca whitelisted."
  ],
  "verifier_sha256": "c28e5f363b9eed004b86091c0a3699cc8d755b2ef93e4e14fc73365d159e0922",
  "scorer_sha256": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/data/manifest.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/data/manifest.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "train": 1024,
  "val": 32,
  "pilot": 16,
  "sources": {
    "cn_k12": 512,
    "orca_math": 512
  },
  "previous128_preserved": true,
  "group_disjoint": true,
  "benchmark_selection": false,
  "preparation_sha256": "39613274300ef17d95512edd853ac083d060f115486f4157a5d4a7a892887466",
  "train_sha256": "6bcab08da6bc6b22ddacc58ac5aeb5a18abcc509c4f68d7457cd79d8acb4e317",
  "val_sha256": "cb02ef017baff97bed5568e60a53f9673c04f657f59d81349f1a6484e3f30a6a",
  "teacher_verdicts_sha256": "3211744626808641f6ffe07b2d27a80ed2870c5727baff0949e1671ec3d63d5b",
  "new_gold_blind_teacher_corroborated": 720,
  "prior_reviewed": 304,
  "rejected_or_unknown": 245,
  "limitations": [
    "Teacher agreement corroborates references; it is not an exact oracle or proof that every semantic paraphrase of benchmarks is absent.",
    "Published original per-item source URLs unavailable; only pinned CNK12/Orca whitelisted."
  ],
  "verifier_sha256": "c28e5f363b9eed004b86091c0a3699cc8d755b2ef93e4e14fc73365d159e0922",
  "scorer_sha256": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production-config-v2.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
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
    200,
    300,
    400,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/production",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  }
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production-config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
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
    200,
    300,
    400,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/production",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  }
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production/config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
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
    200,
    300,
    400,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/production",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  }
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production-config-v2.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
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
    200,
    300,
    400,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
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
    200,
    300,
    400,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke-config-v2.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2,
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2,
  "replay_guard_policy": "Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/smoke-config-v2.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/smoke-config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/smoke/config.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 24,
  "group": 4,
  "steps": 2,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/runner-v2/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "one_cloud_job_3x8",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/smoke",
  "resume": null,
  "total_training_iterations": 500,
  "global_batch": {
    "prompts_per_step": 24,
    "rollouts_per_prompt": 4,
    "responses_per_step": 96
  },
  "historical_batch": {
    "prompts": 32,
    "responses_per_prompt": 8,
    "total_responses": 256
  },
  "data_reuse": {
    "train1024_passes_if_all500": 11.71875
  },
  "plain_full500": true,
  "data_seed": 20261012,
  "expected_world_size": 24,
  "checkpoint_format": {
    "single_safetensors": true,
    "optimizer": false,
    "rng": false
  },
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 2
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-r2-24gpu-20261012/attempts/03-rejected-image/cloud-controller-status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/attempts/03-rejected-image/cloud-controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "time": 1791756425.1414852,
  "error": "RuntimeError('Submission did not return a job id; do not submit again without reconciliation: Error 400: Error resolve image name <base-image>')",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/cloud_controller_v2.py\", line 70, in <module>\n    raise RuntimeError('Submission did not return a job id; do not submit again without reconciliation: '+str(reply))\nRuntimeError: Submission did not return a job id; do not submit again without reconciliation: Error 400: Error resolve image name <base-image>\n"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/attempts/04-rejected-short-image/cloud-controller-status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/attempts/04-rejected-short-image/cloud-controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "time": 1791756602.7086587,
  "error": "RuntimeError('Submission did not return a job id; do not submit again without reconciliation: Error 400: Error resolve image name jupyter-nvcc')",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/cloud_controller_v3.py\", line 70, in <module>\n    raise RuntimeError('Submission did not return a job id; do not submit again without reconciliation: '+str(reply))\nRuntimeError: Submission did not return a job id; do not submit again without reconciliation: Error 400: Error resolve image name jupyter-nvcc\n"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/attempts/08-nfs-visibility/smoke/status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/attempts/08-nfs-visibility/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "loading",
  "started": 1791759075.033254,
  "world_size": 24
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/cloud-controller-status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/cloud-controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "submitted",
  "time": 1791756973.5025668,
  "job_id": "RUN_0e4adb4f2a",
  "job_status": "Job status=Pending"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/latest-launch-status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/latest-launch-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "job_id": "RUN_0e4adb4f2a",
  "status": "Job status=Pending",
  "time": 1791757249.3322964,
  "actual_node_ranks": 0,
  "production_steps": 0
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/launch-report.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/launch-report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "job_id": "RUN_bb32c0eace",
  "checked_at": 1791760896.2233803,
  "state": {
    "state": "validating",
    "step": 0,
    "planned": 32
  },
  "actual_smoke_optimizer_updates": 2,
  "actual_production_iterations": 0,
  "actual_production_updates": 0,
  "production_steps_requested": 500,
  "train_tasks": 1024,
  "global_prompts": 24,
  "responses_per_prompt": 4,
  "checkpoint_steps": [
    50,
    100,
    200,
    300,
    400,
    500
  ],
  "exports": "single model.safetensors; no optimizer/RNG",
  "independent_of_chat": true,
  "smoke_passed": true,
  "smoke_fixture_cases": 480,
  "proof_sha256": "29f6dc3fa6793dded9fe9f11de23975d9d546d699bd9aa8071f05be3d6a5f037",
  "production_children": 24,
  "production_baseline": {
    "step": 0,
    "completed": 32,
    "correct": 16,
    "accuracy": 0.5,
    "format_valid": 29,
    "parallel_valid": 29,
    "fork_tasks": 32,
    "mean_width": 2.727272727272727,
    "mean_rounds": 1.03125,
    "mean_actual_forward_calls": 541.28125,
    "mean_sampled_tokens": 696.53125,
    "protocol": "Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed",
    "benchmark": false,
    "model": "original fullInstruct SFT epoch1; before new RL"
  },
  "training_rollouts_written": 94,
  "phase_observed": "production training rollouts iteration1; baseline32 completed"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production-baseline.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production-baseline.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 0,
  "completed": 32,
  "correct": 16,
  "accuracy": 0.5,
  "format_valid": 29,
  "parallel_valid": 29,
  "fork_tasks": 32,
  "mean_width": 2.727272727272727,
  "mean_rounds": 1.03125,
  "mean_actual_forward_calls": 541.28125,
  "mean_sampled_tokens": 696.53125,
  "protocol": "Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed",
  "benchmark": false,
  "model": "original fullInstruct SFT epoch1; before new RL"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production/metrics.jsonl](../artifacts/work/experiments/rl-r2-24gpu-20261012/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/production/status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 36,
  "steps": 500,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 7.883795779400011e-06,
  "max_replay_logp_drift": 0.0001583099365234375
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/production/validation-0000/summary.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/production/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 0,
  "completed": 32,
  "correct": 16,
  "format_valid": 29,
  "parallel_valid": 29,
  "fork_tasks": 32,
  "widths": [
    3,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    3,
    4,
    4,
    4,
    2,
    2,
    3,
    3,
    3,
    3,
    2,
    2,
    2,
    4,
    4,
    2,
    3,
    3,
    4,
    3,
    2,
    3,
    3,
    2,
    2
  ],
  "actual_rounds": 33,
  "logical_depth": [
    586,
    414,
    721,
    343,
    315,
    363,
    584,
    462,
    886,
    452,
    289,
    178,
    456,
    636,
    881,
    645,
    340,
    598,
    548,
    1609,
    754,
    658,
    504,
    397,
    447,
    603,
    522,
    460,
    372,
    500,
    462,
    336
  ],
  "sampled_tokens": [
    843,
    491,
    791,
    386,
    364,
    475,
    671,
    630,
    1241,
    768,
    382,
    204,
    496,
    828,
    1177,
    985,
    444,
    739,
    668,
    1788,
    1225,
    917,
    675,
    527,
    527,
    814,
    629,
    530,
    495,
    678,
    508,
    393
  ],
  "actual_forward_calls": [
    586,
    414,
    721,
    343,
    315,
    363,
    584,
    462,
    886,
    452,
    289,
    178,
    456,
    636,
    881,
    645,
    340,
    598,
    548,
    1609,
    754,
    658,
    504,
    397,
    447,
    603,
    522,
    460,
    372,
    500,
    462,
    336
  ],
  "sampler": "Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/metrics.jsonl](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 52,
  "steps": 500,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 6.66450261169625e-06,
  "replay_guard_passed": true,
  "replay_parity_skips": 0,
  "max_replay_logp_drift": 0.0002231597900390625
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0000/summary.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 0,
  "completed": 32,
  "correct": 16,
  "format_valid": 29,
  "parallel_valid": 29,
  "fork_tasks": 32,
  "widths": [
    3,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    3,
    4,
    4,
    4,
    2,
    2,
    3,
    3,
    3,
    3,
    2,
    2,
    2,
    4,
    4,
    2,
    3,
    3,
    4,
    3,
    2,
    3,
    3,
    2,
    2
  ],
  "actual_rounds": 33,
  "logical_depth": [
    586,
    414,
    721,
    343,
    315,
    363,
    584,
    462,
    886,
    452,
    289,
    178,
    456,
    636,
    881,
    645,
    340,
    598,
    548,
    1609,
    754,
    658,
    504,
    397,
    447,
    603,
    522,
    460,
    372,
    500,
    462,
    336
  ],
  "sampled_tokens": [
    843,
    491,
    791,
    386,
    364,
    475,
    671,
    630,
    1241,
    768,
    382,
    204,
    496,
    828,
    1177,
    985,
    444,
    739,
    668,
    1788,
    1225,
    917,
    675,
    527,
    527,
    814,
    629,
    530,
    495,
    678,
    508,
    393
  ],
  "actual_forward_calls": [
    586,
    414,
    721,
    343,
    315,
    363,
    584,
    462,
    886,
    452,
    289,
    178,
    456,
    636,
    881,
    645,
    340,
    598,
    548,
    1609,
    754,
    658,
    504,
    397,
    447,
    603,
    522,
    460,
    372,
    500,
    462,
    336
  ],
  "sampler": "Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050/summary.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/validation-0050/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 50,
  "completed": 32,
  "correct": 28,
  "format_valid": 30,
  "parallel_valid": 30,
  "fork_tasks": 32,
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
    4,
    4
  ],
  "actual_rounds": 32,
  "logical_depth": [
    752,
    654,
    1344,
    483,
    463,
    575,
    710,
    580,
    2255,
    636,
    540,
    364,
    710,
    817,
    1069,
    766,
    521,
    2172,
    764,
    1086,
    952,
    921,
    1763,
    724,
    609,
    875,
    690,
    1883,
    559,
    697,
    803,
    399
  ],
  "sampled_tokens": [
    1126,
    890,
    1658,
    718,
    669,
    1009,
    1139,
    802,
    2860,
    1190,
    816,
    581,
    1136,
    1153,
    1392,
    1477,
    798,
    3135,
    1208,
    1578,
    1746,
    1314,
    2507,
    1019,
    831,
    1214,
    972,
    2497,
    812,
    1039,
    1320,
    639
  ],
  "actual_forward_calls": [
    752,
    654,
    1344,
    483,
    463,
    575,
    710,
    580,
    2255,
    636,
    540,
    364,
    710,
    817,
    1069,
    766,
    521,
    2172,
    764,
    1086,
    952,
    921,
    1763,
    724,
    609,
    875,
    690,
    1883,
    559,
    697,
    803,
    399
  ],
  "sampler": "Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/metrics.jsonl](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/result.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 2,
  "world_size": 24,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/checkpoint-0002/hf"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 2,
  "steps": 2
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/smoke/metrics.jsonl](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/smoke/result.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 2,
  "world_size": 24,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/smoke/checkpoint-0002/hf"
}
```

</details>

- [work/experiments/rl-r2-24gpu-20261012/smoke/status.json](../artifacts/work/experiments/rl-r2-24gpu-20261012/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 2,
  "steps": 2
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/launch.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/prepare.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/train.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-pre-fixtures/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/runner-v2/launch.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-v2/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/runner-v2/prepare.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-v2/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-24gpu-20261012/runner-v2/train.py](../artifacts/work/experiments/rl-r2-24gpu-20261012/runner-v2/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
