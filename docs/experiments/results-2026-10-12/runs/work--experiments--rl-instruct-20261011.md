# work/experiments/rl-instruct-20261011

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-instruct-20261011/direct-full500/forward_only-config.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/forward_only-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 500,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted revision2 train128 val32; immutable plain full500 fromfullSFT",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp3",
  "reward_mode": "forward_only",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/forward_only",
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
    "train128_passes_if_all500": 31.25
  },
  "plain_full500": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/config.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 500,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted revision2 train128 val32; immutable plain full500 fromfullSFT",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp3",
  "reward_mode": "forward_only",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run",
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
    "train128_passes_if_all500": 31.25
  },
  "plain_full500": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/config.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 500,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted revision2 train128 val32; immutable plain full500 fromfullSFT",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp3",
  "reward_mode": "forward_only",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run",
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
    "train128_passes_if_all500": 31.25
  },
  "plain_full500": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/config.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 500,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted revision2 train128 val32; immutable plain full500 fromfullSFT",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp2",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width",
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
    "train128_passes_if_all500": 31.25
  },
  "plain_full500": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/strong_width-config.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/strong_width-config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 500,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    500
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted revision2 train128 val32; immutable plain full500 fromfullSFT",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp2",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width",
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
    "train128_passes_if_all500": 31.25
  },
  "plain_full500": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp2/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp2/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_061f39a04b-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "newdeep-fullSFT-0126",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final",
      "audit": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json",
      "audit_sha256": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832"
    }
  ],
  "launcher_sha256": "edb2ae218494c138f996025508d460ead8476c0db5aed9e46dfd717f648b49d4",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp3/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp3/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_7d061208cd-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "R1-checkpoint-0032",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/complete.json",
      "step": 32
    }
  ],
  "launcher_sha256": "edb2ae218494c138f996025508d460ead8476c0db5aed9e46dfd717f648b49d4",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp2-retry310/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp2-retry310/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_061f39a04b-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "310-R2-checkpoint64-MATH500-fullwidth8-retry",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/complete.json"
    }
  ],
  "launcher_sha256": "929129b74d3ea47a3229de417c03b31df96067f84519a8bbbb5fbf9193a849b5",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  },
  "checkpoint_integrity": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/tmp2-checkpoint64-integrity.json",
  "checkpoint_integrity_sha256": "badd43b508d65325f053c1cec57e4489413256e5bf93b2c779635a273b951bc4"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp2/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp2/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_061f39a04b-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "309-R2-checkpoint64-MATH500-fullwidth8",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/complete.json"
    }
  ],
  "launcher_sha256": "3d04d291ca2848658723529bb48ab845ea8f5b8c394f429691bb45f85b317bfb",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  },
  "checkpoint_integrity": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/tmp2-checkpoint64-integrity.json",
  "checkpoint_integrity_sha256": "badd43b508d65325f053c1cec57e4489413256e5bf93b2c779635a273b951bc4"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp3-retry236/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp3-retry236/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_7d061208cd-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "236-R1-checkpoint64-MATH500-fullwidth8-retry",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/complete.json"
    }
  ],
  "launcher_sha256": "929129b74d3ea47a3229de417c03b31df96067f84519a8bbbb5fbf9193a849b5",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  },
  "checkpoint_integrity": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/tmp3-checkpoint64-integrity.json",
  "checkpoint_integrity_sha256": "beec1d9b8598094d125ad552715f291a70eb055edad52039d5b7a2ee41606227"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp3/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp3/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_7d061208cd-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "235-R1-checkpoint64-MATH500-fullwidth8",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/complete.json"
    }
  ],
  "launcher_sha256": "3d04d291ca2848658723529bb48ab845ea8f5b8c394f429691bb45f85b317bfb",
  "source_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119"
  },
  "checkpoint_integrity": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/tmp3-checkpoint64-integrity.json",
  "checkpoint_integrity_sha256": "beec1d9b8598094d125ad552715f291a70eb055edad52039d5b7a2ee41606227"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-joint/main/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-joint/main/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "rank_offset": 0,
  "after_result": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R2-checkpoint-0064.json",
  "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf",
  "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/complete.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "width8_proof": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json",
  "width8_proof_sha256": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108",
  "sources": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/worker.py": "c9f8c20e62e7c7d722081363dc830b2694e090030f763a86dee3281faa94a9bf",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/aggregate.py": "30b90246dd4dd9242eb6734d794043328538524dca680a04853d31a700f4fec6"
  },
  "launcher_sha256": "3c84a1420153eca60fd3a9279967bf2d0116b33495bf213b2cc53cb2a8e2a55f"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-joint/tmp2/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-joint/tmp2/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_061f39a04b-mpimaster-0",
  "rank_offset": 8,
  "after_result": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp2/results/newdeep-fullSFT-0126.json",
  "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf",
  "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/complete.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "width8_proof": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json",
  "width8_proof_sha256": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108",
  "sources": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/worker.py": "c9f8c20e62e7c7d722081363dc830b2694e090030f763a86dee3281faa94a9bf",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/aggregate.py": "30b90246dd4dd9242eb6734d794043328538524dca680a04853d31a700f4fec6"
  },
  "launcher_sha256": "3c84a1420153eca60fd3a9279967bf2d0116b33495bf213b2cc53cb2a8e2a55f"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-joint/tmp3/plan.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-joint/tmp3/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_7d061208cd-mpimaster-0",
  "rank_offset": 16,
  "after_result": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp3/results/R1-checkpoint-0032.json",
  "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf",
  "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/complete.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "width8_proof": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json",
  "width8_proof_sha256": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108",
  "sources": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/worker.py": "c9f8c20e62e7c7d722081363dc830b2694e090030f763a86dee3281faa94a9bf",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-joint/aggregate.py": "30b90246dd4dd9242eb6734d794043328538524dca680a04853d31a700f4fec6"
  },
  "launcher_sha256": "3c84a1420153eca60fd3a9279967bf2d0116b33495bf213b2cc53cb2a8e2a55f"
}
```

</details>

- [work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/manifest.json](../artifacts/work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 500,
  "suite": "500",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "ee768a765cfe13bfb058975b3afa0e83881275cfd07d61e3f6a324f562983e74",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
  "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/initial-math500-plan.json](../artifacts/work/experiments/rl-instruct-20261011/initial-math500-plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "mode": "structured",
  "diagnostic_only": true,
  "selection_allowed": false,
  "curriculum_selection_allowed": false,
  "checkpoint_selection_allowed": false,
  "init": "six-token-row warmup, not full SFT",
  "generation": {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20,
    "seed_base": 42,
    "response_cap": 4096,
    "path_cap": 2048,
    "workers": 8
  },
  "questions_sha256": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
  "model_config": {
    "architectures": [
      "Qwen3ForCausalLM"
    ],
    "attention_bias": false,
    "attention_dropout": 0.0,
    "bos_token_id": 151643,
    "eos_token_id": 151645,
    "head_dim": 128,
    "hidden_act": "silu",
    "hidden_size": 2560,
    "initializer_range": 0.02,
    "intermediate_size": 9728,
    "layer_types": [
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention",
      "full_attention"
    ],
    "max_position_embeddings": 40960,
    "max_window_layers": 36,
    "model_type": "qwen3",
    "num_attention_heads": 32,
    "num_hidden_layers": 36,
    "num_key_value_heads": 8,
    "rms_norm_eps": 1e-06,
    "rope_scaling": null,
    "rope_theta": 1000000,
    "sliding_window": null,
    "tie_word_embeddings": true,
    "torch_dtype": "bfloat16",
    "transformers_version": "4.53.2",
    "use_cache": true,
    "use_sliding_window": false,
    "vocab_size": 151936
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-main-fallback/plan.json](../artifacts/work/experiments/rl-instruct-20261011/math500-main-fallback/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "R1-checkpoint-0064",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/complete.json"
    },
    {
      "id": "R2-checkpoint-0064",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/complete.json"
    }
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-sparse/plan.json](../artifacts/work/experiments/rl-instruct-20261011/math500-sparse/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "actual verified HF microbatch paths2",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false
  },
  "jobs": [
    {
      "id": "001-fullSFT-baseline",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final"
    },
    {
      "id": "R1-checkpoint-0032",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/complete.json"
    },
    {
      "id": "R2-checkpoint-0032",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/complete.json"
    },
    {
      "id": "R1-checkpoint-0128",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0128/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0128/complete.json"
    },
    {
      "id": "R2-checkpoint-0128",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0128/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0128/complete.json"
    },
    {
      "id": "R1-checkpoint-0256",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0256/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0256/complete.json"
    },
    {
      "id": "R2-checkpoint-0256",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0256/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0256/complete.json"
    },
    {
      "id": "R1-checkpoint-0500",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0500/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0500/complete.json"
    },
    {
      "id": "R2-checkpoint-0500",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0500/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0500/complete.json"
    }
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-successor/plan.json](../artifacts/work/experiments/rl-instruct-20261011/math500-successor/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "actual verified HF microbatch paths2",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false
  },
  "jobs": [
    {
      "id": "001-fullSFT-baseline",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final"
    },
    {
      "id": "R1-checkpoint-0032",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/complete.json"
    },
    {
      "id": "R2-checkpoint-0032",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/complete.json"
    },
    {
      "id": "newdeep-fullSFT-0126",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final",
      "audit": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json",
      "audit_sha256": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832"
    },
    {
      "id": "R1-checkpoint-0128",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0128/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0128/complete.json"
    },
    {
      "id": "R2-checkpoint-0128",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0128/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0128/complete.json"
    },
    {
      "id": "R1-checkpoint-0256",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0256/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0256/complete.json"
    },
    {
      "id": "R2-checkpoint-0256",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0256/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0256/complete.json"
    },
    {
      "id": "R1-checkpoint-0500",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0500/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0500/complete.json"
    },
    {
      "id": "R2-checkpoint-0500",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0500/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0500/complete.json"
    }
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/config.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-launch.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/data/revision2/val.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 16,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_steps": [
    4,
    8,
    16
  ],
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "independently admitted BigMath CNK12+Orca revision2",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "matched clean val32 fixed seed/temp1/top_p1/nofilter; same native think guard; initial SFT at step0",
  "lane": "tmp2",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16"
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/config.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/technical-probes.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/technical-probes.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 2,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_every": 1,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "reward_mode": "strong_width",
  "lane": "tmp2",
  "engineering_only": true,
  "curriculum_allowed": false,
  "production_allowed": false,
  "resume": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runs/technical-step1/checkpoint-0001",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runs/technical-resume-step2"
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-step1/config.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "train": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/technical-probes.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/technical-probes.jsonl",
  "seed": 20261011,
  "validation_seed": 91261011,
  "world_size": 8,
  "group": 4,
  "steps": 1,
  "lr": 1e-06,
  "clip": 0.2,
  "max_grad_norm": 1.0,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "checkpoint_every": 1,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/microbatch_decoder.py",
  "max_batched_paths": 2,
  "reward_mode": "strong_width",
  "lane": "tmp2",
  "engineering_only": true,
  "curriculum_allowed": false,
  "production_allowed": false,
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runs/technical-step1"
}
```

</details>

- [work/experiments/rl-instruct-20261011/technical-config-seal.json](../artifacts/work/experiments/rl-instruct-20261011/technical-config-seal.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "approved": false,
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "requires": [
    "Verified full SFT export bound audit",
    "Root review before retained queue dispatch",
    "All8ranks finite actual updates",
    "Actual replay parity",
    "Save/resume optimizer + RNG identity",
    "Peakmemory and clean launcher/NCCL exit"
  ],
  "sha256": {
    "work/experiments/rl-instruct-20261011/runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "work/experiments/rl-instruct-20261011/runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "work/experiments/rl-instruct-20261011/runner/audit_semantics.py": "62e239704d4feecc8ddf5da7ac3e5c99ac8d280067b3dd66e9b9f9a2d4d866f0",
    "work/experiments/rl-instruct-20261011/runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "work/experiments/rl-instruct-20261011/runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "work/experiments/rl-instruct-20261011/runner/train.py": "5bdb7d2cae3375520d1b097d23c59cd6c269ff855242bb8ad71285c8b3fa3543",
    "work/experiments/rl-instruct-20261011/runner/proof_instruct.py": "20991bba1e68e051b2b44252fc41e43b62b9c645f38fd47fd10aa94e4daa5f76",
    "work/experiments/rl-instruct-20261011/runner/proof_contract.py": "d98e3de42a3c5aeac3898fa00a93bb7511ce4e842819dab3efa3a1a84d3bb82a",
    "work/experiments/rl-instruct-20261011/runner/proof_zero1.py": "0228a93b9da3ceda34b40f05ac6793e753c69ec5f8ef4dab625a950e3926f95b",
    "work/experiments/rl-instruct-20261011/runner/prepare_technical_config.py": "9d8ef57d41c7e764f4428337934b9c28e355b399350d5f43546023d23ab78122",
    "work/experiments/rl-instruct-20261011/runner/prepare_configs.py": "389ea3d6f7442fd33e7d50d0b64f6e477cbd33a96e372155bd6d7392d7f29ad9",
    "work/experiments/rl-instruct-20261011/technical-configs/step1.json": "a6b6b11817c904f19ced95fab333fea1b5b3d805eb0788a800dfa4fdee27d35d",
    "work/experiments/rl-instruct-20261011/technical-configs/resume-step2.json": "b7bb819b6a6bced7e8988b504d7b88e8818b35097a411bde7273c19ac3f38a7e",
    "work/experiments/rl-instruct-20261011/reward.py": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
    "work/experiments/rl-instruct-20261011/runner/technical-probes.jsonl": "5d8f8422b250966f52a44e7bc525398bb5ec54e4f98d2195469250b9c18a6289",
    "work/experiments/instruct-full-20261011/epoch1-export-proof.json": "da80c7f2cd0b3c74c4793a9aa56be93cedc44c07bc01c10dfa9bdf0a75664688",
    "work/experiments/rl-instruct-20261011/runner/launch_readiness.py": "df6e4935291ff3ab23779b006912720ef0c8af3459672f11f41e4e7ee57ac4c3",
    "work/experiments/rl-instruct-20261011/run_technical_readiness.sh": "5b3d028b1cc574d6c8f897aec9929d7ca5a7d28abff31b429a146da4831979a5",
    "work/experiments/night-20261010/cloud-continued/tmp2/queue/305-instruct-rl-technical-step-resume.json": "8f084bdb22802fdc6b803d1501df7afb5d3e369e298f05b1eb74eca6d7106268",
    "work/experiments/rl-instruct-20261011/runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "work/experiments/rl-instruct-20261011/runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e"
  },
  "full_sft_export_audit": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/epoch1-export-proof.json",
  "lane": "tmp2",
  "predecessor_task": "304-instruct-full-matched-guard128"
}
```

</details>

- [work/experiments/rl-instruct-20261011/throughput/source-manifest.json](../artifacts/work/experiments/rl-instruct-20261011/throughput/source-manifest.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "REPORT.md": "002afb7db3e4afde1a9f0c5092eb751b7764fec275fa5e717f762b44e0446d0c",
  "cohort_decoder.py": "3484ed041978cad8f5d065be346aab77080d050280bdca60c6165a7fd228da76",
  "cpu-cohort-proof.json": "7c0940b28c99e73ae8687051983ee2291ff242ae59a09b2e23b1b81d782e29e2",
  "cpu-execute-proof.json": "54915936046254eb35fb0b5b52411914dd12deb8f5828e0eb82c34cea70d9dee",
  "cpu-precision-screen.json": "bcf237d3a87f96ff3999831a1abd49106cb23cde5f7c71c9271e68fdfe198520",
  "execute_candidate.py": "2fb7389b62d501720fe9e128d7401d4786c53f467a75001ef63b1e6c87b18f42",
  "phase_timer.py": "d2796d68ba7108b362d2266082bbd5820d9eed040e2721537b17b7c9ba5ed57f",
  "production306-step1-profile.json": "e1b5735079de05016e72c6eeebf06ff907f2c7bc81bcaa44cc9be283a55adeec",
  "proof_cohort.py": "e605e101001102dcff63d7c101b2c584296b30ea7ca0cb34bf95473551b91279",
  "proof_execute.py": "1352d811b7262c78ac1b8c24b90b6b6f2e00bd850ccbb4b6fbb2691d5171a341",
  "proof_precision.py": "87213e128e33da856bb3d7ebc34df9ecbd60d72ba3875573c3adf7aed8b04334",
  "width8-inference/README.md": "8212ba8f129647a0265e9e8db28c88206835231e33d158c5a61f581e05b8445e",
  "width8-inference/config.json": "c944d9f50bd20df233b8d725df05b1ba4cc83a11e0517c5185e05af0c738083b",
  "width8_inference_proof.py": "f1fc40aa5779c021b7f0fc99cada535749e7a3161c4c4bd63fbed2c0f712fba8"
}
```

</details>

- [work/experiments/rl-instruct-20261011/throughput/width8-inference/config.json](../artifacts/work/experiments/rl-instruct-20261011/throughput/width8-inference/config.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "models": [
    {
      "name": "baseline",
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final"
    },
    {
      "name": "r1-step32",
      "path": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0032/hf"
    },
    {
      "name": "r2-step32",
      "path": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0032/hf"
    }
  ],
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "sample_count": 2,
  "seed_base": 42161011,
  "response_budget": 4096,
  "path_budget": 768,
  "max_context": 16384,
  "max_logp_delta": 0.01,
  "mean_logp_delta": 0.002,
  "p95_logp_delta": 0.005,
  "protocol": "separate-width8-inference-FP32",
  "primary_runtime_unchanged": true,
  "queue_predecessors": "primary MATH500 baseline/R1/R2step32 and new deep126; owner-controlled retained main8 only"
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/metrics.jsonl](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/status.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 87,
  "steps": 500,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 5.340993049224108e-06,
  "max_replay_logp_drift": 0.0001087188720703125
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    3,
    3,
    2,
    2,
    2,
    4,
    2,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    4,
    4,
    3,
    4,
    4,
    4,
    3,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    2,
    3
  ],
  "actual_rounds": 33,
  "logical_depth": [
    586,
    340,
    447,
    414,
    721,
    598,
    603,
    343,
    315,
    548,
    522,
    363,
    584,
    1609,
    460,
    462,
    886,
    754,
    372,
    452,
    289,
    658,
    500,
    178,
    456,
    504,
    462,
    636,
    881,
    397,
    336,
    645
  ],
  "sampled_tokens": [
    843,
    444,
    527,
    491,
    791,
    739,
    814,
    386,
    364,
    668,
    629,
    475,
    671,
    1788,
    530,
    630,
    1241,
    1225,
    495,
    768,
    382,
    917,
    678,
    204,
    496,
    675,
    508,
    828,
    1177,
    527,
    393,
    985
  ],
  "actual_forward_calls": [
    672,
    394,
    487,
    414,
    721,
    598,
    685,
    343,
    315,
    548,
    579,
    424,
    584,
    1609,
    460,
    552,
    1060,
    942,
    438,
    571,
    326,
    755,
    596,
    178,
    456,
    504,
    462,
    789,
    1070,
    453,
    336,
    828
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0004/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0004/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 4,
  "completed": 32,
  "correct": 19,
  "format_valid": 32,
  "parallel_valid": 32,
  "fork_tasks": 32,
  "widths": [
    2,
    2,
    4,
    2,
    3,
    4,
    3,
    2,
    2,
    3,
    3,
    2,
    3,
    3,
    2,
    4,
    2,
    3,
    4,
    2,
    3,
    4,
    2,
    2,
    2,
    3,
    4,
    4,
    2,
    4,
    4,
    4,
    4
  ],
  "actual_rounds": 33,
  "logical_depth": [
    796,
    428,
    501,
    394,
    844,
    836,
    648,
    308,
    274,
    546,
    390,
    341,
    566,
    943,
    630,
    570,
    424,
    564,
    303,
    354,
    289,
    390,
    432,
    264,
    515,
    624,
    607,
    431,
    1603,
    511,
    537,
    535
  ],
  "sampled_tokens": [
    950,
    599,
    565,
    541,
    1216,
    1076,
    755,
    355,
    356,
    777,
    452,
    456,
    714,
    1078,
    958,
    753,
    543,
    1060,
    357,
    531,
    382,
    472,
    508,
    306,
    665,
    1063,
    1054,
    474,
    2508,
    791,
    805,
    848
  ],
  "actual_forward_calls": [
    796,
    489,
    501,
    473,
    979,
    996,
    648,
    308,
    316,
    657,
    390,
    401,
    651,
    943,
    741,
    570,
    479,
    742,
    303,
    438,
    326,
    390,
    432,
    264,
    581,
    775,
    758,
    431,
    1996,
    612,
    636,
    671
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0008/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0008/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 8,
  "completed": 32,
  "correct": 21,
  "format_valid": 31,
  "parallel_valid": 31,
  "fork_tasks": 32,
  "widths": [
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    4,
    2,
    3,
    2,
    3,
    4,
    2,
    2,
    2,
    3,
    4,
    2,
    3,
    2,
    2,
    2,
    2,
    3,
    3,
    2,
    3,
    2,
    2,
    2,
    2
  ],
  "actual_rounds": 33,
  "logical_depth": [
    598,
    342,
    377,
    333,
    958,
    1126,
    581,
    360,
    304,
    715,
    391,
    360,
    421,
    696,
    640,
    707,
    451,
    759,
    393,
    307,
    285,
    502,
    435,
    215,
    500,
    590,
    643,
    624,
    1599,
    442,
    393,
    389
  ],
  "sampled_tokens": [
    696,
    408,
    441,
    407,
    1090,
    1433,
    718,
    419,
    431,
    873,
    447,
    483,
    724,
    762,
    733,
    791,
    646,
    1192,
    508,
    484,
    346,
    580,
    504,
    260,
    654,
    880,
    800,
    785,
    1688,
    542,
    456,
    499
  ],
  "actual_forward_calls": [
    598,
    342,
    377,
    333,
    958,
    1298,
    581,
    360,
    342,
    761,
    391,
    427,
    550,
    696,
    640,
    707,
    557,
    967,
    393,
    391,
    285,
    502,
    435,
    215,
    566,
    745,
    643,
    668,
    1599,
    442,
    393,
    389
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0016/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0016/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 16,
  "completed": 32,
  "correct": 24,
  "format_valid": 32,
  "parallel_valid": 32,
  "fork_tasks": 32,
  "widths": [
    3,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    4,
    2,
    3,
    2,
    3,
    2,
    2,
    2,
    3,
    3,
    2,
    3,
    2,
    2,
    3,
    2,
    3,
    3,
    2,
    2,
    3,
    3,
    2,
    2,
    2
  ],
  "actual_rounds": 33,
  "logical_depth": [
    705,
    431,
    524,
    340,
    793,
    723,
    568,
    359,
    342,
    417,
    532,
    363,
    436,
    1787,
    615,
    372,
    460,
    650,
    380,
    537,
    295,
    519,
    477,
    239,
    511,
    681,
    568,
    1037,
    1844,
    465,
    393,
    1441
  ],
  "sampled_tokens": [
    991,
    520,
    649,
    448,
    879,
    807,
    715,
    485,
    492,
    526,
    701,
    487,
    656,
    2194,
    736,
    515,
    617,
    887,
    480,
    732,
    366,
    599,
    631,
    289,
    689,
    1008,
    661,
    1255,
    2261,
    686,
    448,
    1806
  ],
  "actual_forward_calls": [
    853,
    431,
    524,
    340,
    793,
    723,
    568,
    423,
    399,
    417,
    640,
    363,
    564,
    1787,
    615,
    372,
    559,
    740,
    380,
    631,
    295,
    519,
    581,
    239,
    627,
    857,
    568,
    1037,
    2179,
    576,
    393,
    1441
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 32,
  "completed": 32,
  "correct": 24,
  "format_valid": 28,
  "parallel_valid": 26,
  "fork_tasks": 30,
  "widths": [
    3,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    3,
    4,
    2,
    3,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    2
  ],
  "actual_rounds": 34,
  "logical_depth": [
    693,
    463,
    563,
    358,
    845,
    1018,
    446,
    396,
    268,
    504,
    448,
    350,
    681,
    1454,
    1236,
    293,
    971,
    554,
    372,
    569,
    363,
    344,
    549,
    386,
    559,
    705,
    699,
    554,
    1350,
    652,
    405,
    632
  ],
  "sampled_tokens": [
    1075,
    601,
    709,
    451,
    895,
    1313,
    446,
    460,
    297,
    629,
    680,
    431,
    881,
    1650,
    1531,
    293,
    1233,
    845,
    506,
    847,
    450,
    417,
    729,
    502,
    720,
    878,
    895,
    702,
    1822,
    850,
    492,
    779
  ],
  "actual_forward_calls": [
    838,
    463,
    563,
    358,
    845,
    1138,
    446,
    396,
    268,
    569,
    517,
    350,
    758,
    1454,
    1236,
    293,
    971,
    658,
    440,
    710,
    363,
    344,
    549,
    386,
    559,
    705,
    699,
    554,
    1588,
    652,
    405,
    632
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 64,
  "completed": 32,
  "correct": 28,
  "format_valid": 15,
  "parallel_valid": 14,
  "fork_tasks": 31,
  "widths": [
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    3,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    2,
    2,
    2
  ],
  "actual_rounds": 31,
  "logical_depth": [
    720,
    365,
    483,
    353,
    1404,
    820,
    858,
    389,
    419,
    514,
    387,
    513,
    542,
    1348,
    697,
    490,
    425,
    664,
    479,
    699,
    375,
    575,
    601,
    272,
    537,
    850,
    731,
    506,
    1691,
    532,
    525,
    486
  ],
  "sampled_tokens": [
    853,
    436,
    602,
    439,
    1497,
    820,
    998,
    436,
    456,
    657,
    517,
    589,
    677,
    1515,
    859,
    605,
    500,
    832,
    603,
    942,
    445,
    665,
    697,
    332,
    706,
    990,
    1222,
    595,
    2459,
    641,
    596,
    604
  ],
  "actual_forward_calls": [
    720,
    365,
    483,
    353,
    1404,
    820,
    858,
    389,
    419,
    586,
    387,
    513,
    614,
    1348,
    697,
    490,
    425,
    664,
    479,
    818,
    375,
    575,
    601,
    272,
    537,
    850,
    1016,
    506,
    1691,
    532,
    525,
    486
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/metrics.jsonl](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/status.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "training",
  "step": 125,
  "steps": 500,
  "finite": true,
  "optimizer_step": true,
  "backbone_update_l2": 5.142073495669339e-06,
  "max_replay_logp_drift": 0.000213623046875
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    3,
    3,
    2,
    2,
    2,
    4,
    2,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    4,
    4,
    3,
    4,
    4,
    4,
    3,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    2,
    3
  ],
  "actual_rounds": 33,
  "logical_depth": [
    586,
    340,
    447,
    414,
    721,
    598,
    603,
    343,
    315,
    548,
    522,
    363,
    584,
    1609,
    460,
    462,
    886,
    754,
    372,
    452,
    289,
    658,
    500,
    178,
    456,
    504,
    462,
    636,
    881,
    397,
    336,
    645
  ],
  "sampled_tokens": [
    843,
    444,
    527,
    491,
    791,
    739,
    814,
    386,
    364,
    668,
    629,
    475,
    671,
    1788,
    530,
    630,
    1241,
    1225,
    495,
    768,
    382,
    917,
    678,
    204,
    496,
    675,
    508,
    828,
    1177,
    527,
    393,
    985
  ],
  "actual_forward_calls": [
    672,
    394,
    487,
    414,
    721,
    598,
    685,
    343,
    315,
    548,
    579,
    424,
    584,
    1609,
    460,
    552,
    1060,
    942,
    438,
    571,
    326,
    755,
    596,
    178,
    456,
    504,
    462,
    789,
    1070,
    453,
    336,
    828
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0004/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0004/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 4,
  "completed": 32,
  "correct": 19,
  "format_valid": 31,
  "parallel_valid": 29,
  "fork_tasks": 30,
  "widths": [
    2,
    2,
    3,
    3,
    3,
    2,
    3,
    3,
    3,
    2,
    3,
    4,
    2,
    2,
    2,
    4,
    3,
    4,
    3,
    4,
    2,
    4,
    2,
    3,
    4,
    3,
    3,
    3,
    4,
    3
  ],
  "actual_rounds": 30,
  "logical_depth": [
    606,
    460,
    373,
    443,
    333,
    1102,
    570,
    305,
    295,
    548,
    401,
    359,
    398,
    844,
    499,
    464,
    573,
    928,
    480,
    354,
    289,
    791,
    905,
    241,
    493,
    559,
    608,
    355,
    875,
    484,
    683,
    476
  ],
  "sampled_tokens": [
    704,
    514,
    454,
    563,
    333,
    1378,
    598,
    421,
    381,
    774,
    463,
    474,
    677,
    1014,
    603,
    527,
    809,
    1209,
    593,
    531,
    382,
    847,
    1220,
    288,
    653,
    1000,
    895,
    355,
    1330,
    673,
    923,
    710
  ],
  "actual_forward_calls": [
    606,
    460,
    414,
    511,
    333,
    1244,
    570,
    366,
    339,
    666,
    401,
    419,
    505,
    844,
    499,
    464,
    651,
    1086,
    533,
    438,
    326,
    791,
    1025,
    241,
    559,
    710,
    762,
    355,
    1151,
    585,
    799,
    604
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0008/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0008/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 8,
  "completed": 32,
  "correct": 20,
  "format_valid": 31,
  "parallel_valid": 30,
  "fork_tasks": 30,
  "widths": [
    3,
    4,
    3,
    4,
    4,
    3,
    3,
    3,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    2,
    2,
    4,
    3,
    2,
    3,
    3,
    3,
    3,
    4,
    2,
    2
  ],
  "actual_rounds": 30,
  "logical_depth": [
    652,
    288,
    401,
    448,
    1136,
    870,
    426,
    285,
    283,
    502,
    301,
    395,
    586,
    1046,
    654,
    350,
    396,
    680,
    396,
    352,
    331,
    524,
    734,
    297,
    544,
    618,
    505,
    669,
    895,
    474,
    531,
    585
  ],
  "sampled_tokens": [
    879,
    288,
    532,
    548,
    1461,
    1211,
    426,
    380,
    364,
    728,
    354,
    520,
    787,
    1213,
    823,
    401,
    536,
    961,
    487,
    529,
    456,
    574,
    1003,
    404,
    621,
    996,
    682,
    756,
    1376,
    743,
    607,
    684
  ],
  "actual_forward_calls": [
    794,
    288,
    442,
    481,
    1279,
    968,
    426,
    339,
    324,
    620,
    301,
    460,
    720,
    1046,
    654,
    350,
    462,
    838,
    458,
    436,
    331,
    524,
    822,
    352,
    544,
    792,
    619,
    714,
    1145,
    548,
    531,
    585
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0016/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0016/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 16,
  "completed": 32,
  "correct": 18,
  "format_valid": 31,
  "parallel_valid": 30,
  "fork_tasks": 30,
  "widths": [
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    3,
    2,
    2,
    3,
    2,
    2,
    3,
    4,
    2,
    3,
    2,
    3,
    2,
    2,
    2,
    3,
    4,
    4,
    4,
    3,
    2,
    2
  ],
  "actual_rounds": 30,
  "logical_depth": [
    651,
    300,
    449,
    424,
    1426,
    724,
    566,
    402,
    292,
    554,
    309,
    385,
    588,
    1269,
    437,
    470,
    285,
    963,
    343,
    340,
    287,
    324,
    613,
    277,
    471,
    635,
    699,
    970,
    986,
    449,
    388,
    508
  ],
  "sampled_tokens": [
    877,
    300,
    580,
    579,
    1565,
    1095,
    672,
    495,
    359,
    787,
    383,
    442,
    806,
    1437,
    508,
    582,
    285,
    1329,
    419,
    517,
    348,
    429,
    663,
    314,
    532,
    864,
    968,
    1495,
    1789,
    629,
    416,
    623
  ],
  "actual_forward_calls": [
    792,
    300,
    449,
    512,
    1467,
    879,
    566,
    466,
    319,
    684,
    309,
    385,
    739,
    1269,
    437,
    530,
    285,
    1060,
    343,
    424,
    287,
    385,
    613,
    277,
    471,
    769,
    776,
    1206,
    1471,
    557,
    388,
    508
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 32,
  "completed": 32,
  "correct": 25,
  "format_valid": 30,
  "parallel_valid": 30,
  "fork_tasks": 31,
  "widths": [
    3,
    2,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    3,
    3,
    4,
    4,
    4,
    3,
    4,
    4,
    3,
    4,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    2,
    2
  ],
  "actual_rounds": 32,
  "logical_depth": [
    411,
    339,
    426,
    358,
    777,
    790,
    597,
    309,
    384,
    470,
    410,
    411,
    391,
    1215,
    455,
    588,
    353,
    508,
    519,
    425,
    380,
    611,
    744,
    324,
    730,
    556,
    534,
    576,
    1334,
    464,
    377,
    710
  ],
  "sampled_tokens": [
    560,
    378,
    592,
    561,
    1148,
    1183,
    814,
    458,
    535,
    685,
    543,
    594,
    659,
    2323,
    801,
    588,
    476,
    1017,
    707,
    727,
    526,
    744,
    976,
    400,
    1054,
    950,
    875,
    819,
    2089,
    678,
    497,
    938
  ],
  "actual_forward_calls": [
    479,
    339,
    504,
    437,
    914,
    920,
    664,
    372,
    450,
    537,
    486,
    485,
    477,
    1753,
    564,
    588,
    412,
    686,
    575,
    601,
    455,
    676,
    865,
    372,
    857,
    701,
    698,
    695,
    1640,
    550,
    416,
    710
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/summary.json](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 64,
  "completed": 32,
  "correct": 21,
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
    6,
    4,
    4,
    4,
    6,
    4,
    4,
    4,
    4,
    4,
    6,
    4,
    4,
    4,
    6,
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
    412,
    350,
    364,
    343,
    743,
    954,
    641,
    301,
    466,
    479,
    520,
    368,
    398,
    1162,
    480,
    356,
    622,
    495,
    295,
    442,
    466,
    438,
    498,
    419,
    573,
    662,
    687,
    674,
    1725,
    428,
    489,
    425
  ],
  "sampled_tokens": [
    595,
    597,
    526,
    470,
    1045,
    1315,
    924,
    443,
    589,
    587,
    818,
    523,
    665,
    1676,
    718,
    532,
    901,
    901,
    415,
    866,
    664,
    613,
    708,
    534,
    1015,
    862,
    920,
    972,
    2182,
    614,
    638,
    772
  ],
  "actual_forward_calls": [
    481,
    427,
    436,
    387,
    840,
    1079,
    750,
    355,
    492,
    519,
    671,
    455,
    511,
    1369,
    574,
    413,
    769,
    664,
    335,
    612,
    558,
    524,
    555,
    453,
    814,
    704,
    820,
    787,
    1917,
    501,
    544,
    555
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/handoff-preparation-status.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/handoff-preparation-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "prepared": true,
  "launched": false,
  "cloud_trainers_stopped": false,
  "blocking_stage": "concurrent authenticated Cloud process control unavailable",
  "source": {
    "work/experiments/rl-instruct-20261011/eval24-handoff/launch_eval.py": "e9c93043d710d757b4354dbdeb909549fd65d0c3e02bf27de7b0a8c6b819bc9e",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp2.sh": "5f1ad9e408dd378ed909b3acfb466b75e5514acb1e4d7d16e4e8ab7573e06617",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp3.sh": "f0fb2c38b514127f8c7152a4ec548f0d9fee129ce0f5750c1aed8a3dbc231e57",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp2/plan.json": "af9d6a9c2e8d4bd4c0edc2811eb939d11b4a6ea938b27958edeaf536cc61f557",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp3/plan.json": "1b15dba1415e6c60fd7802200af88a5005b0eb222aec1bdae01c49b4e0463423",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp2-checkpoint64-integrity.json": "badd43b508d65325f053c1cec57e4489413256e5bf93b2c779635a273b951bc4",
    "work/experiments/rl-instruct-20261011/eval24-handoff/tmp3-checkpoint64-integrity.json": "beec1d9b8598094d125ad552715f291a70eb055edad52039d5b7a2ee41606227"
  },
  "width8_proof_sha256": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108",
  "last_verified_steps": {
    "R2": 112,
    "R1": 75
  },
  "common_export_step": 64,
  "at": 1791746591.996525
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp2/status.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "evaluating",
  "updated": 1791753662.602718,
  "job": "newdeep-fullSFT-0126",
  "worker_pids": [
    129154,
    129155,
    129156,
    129157,
    129158,
    129159,
    129160,
    129161
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp3/status.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/root-manual-eval24/tmp3/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "evaluating",
  "updated": 1791753637.3110774,
  "job": "R1-checkpoint-0032",
  "worker_pids": [
    128625,
    128626,
    128627,
    128628,
    128629,
    128630,
    128631,
    128632
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp2/status.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "updated": 1791749987.959855,
  "error": "AssertionError()",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/launch_eval.py\", line 39, in <module>\n    if not gate():status('waiting_width8_proof_and_Cloud_empty8');time.sleep(30);continue\n           ^^^^^^\n  File \"${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/launch_eval.py\", line 28, in gate\n    assert str(Path(integrity['checkpoint'])/'hf')==plan['jobs'][0]['model']\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n"
}
```

</details>

- [work/experiments/rl-instruct-20261011/eval24-handoff/tmp3/status.json](../artifacts/work/experiments/rl-instruct-20261011/eval24-handoff/tmp3/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "updated": 1791750010.8529472,
  "error": "AssertionError()",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/launch_eval.py\", line 39, in <module>\n    if not gate():status('waiting_width8_proof_and_Cloud_empty8');time.sleep(30);continue\n           ^^^^^^\n  File \"${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/eval24-handoff/launch_eval.py\", line 28, in gate\n    assert str(Path(integrity['checkpoint'])/'hf')==plan['jobs'][0]['model']\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n"
}
```

</details>

- [work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/recovery-cpu-result-proof.json](../artifacts/work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/recovery-cpu-result-proof.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "coverage": 500,
  "unique_question_ids": 500,
  "missing": 0,
  "technical_unknown_outcomes": 0,
  "correct": 312,
  "format_valid": 281,
  "original_worker_exits_preserved": true,
  "original_task231_returncode": 1,
  "original_failure": "CPU resummarizer missing Path import after successful evaluator",
  "repaired_evaluator_returncode": 0,
  "evaluator_exit_evidence": "set-e wrapper proceeded from evaluator to CPU resummarizer; historical all-GPU-empty R1 launch gate subsequently passed",
  "current_gpu_empty_claim": false,
  "diagnostic_only": true,
  "selection_allowed": false,
  "at": "2026-10-11T13:37:36.513710+00:00",
  "summary_sha256": "9f606516e19693fe1591e40ead90f16e401422aaf56b7edc95f1731509c1ac3e",
  "trace_sha256": {
    "traces-2.jsonl": "e31ca4cabb6fe3f67c936a2fb11505cf367de99d9425d03141c028c307a5ce6b",
    "traces-5.jsonl": "a1d1138bdbfaa1538e10f2f9a4dce21d9a8c0ea5d07a11d259bd48c5a45776e6",
    "traces-6.jsonl": "4ebd2fc057da935d612023d5077052e45690e6c56e1388a0aad1bc29a3dec779",
    "traces-3.jsonl": "a8a7c1f69ff56550e8dffa3545ea8d3f0a1a64d2acf13e06c4474e8027d7980b",
    "traces-7.jsonl": "61c6a9c47297b0bfd7f8672d9b0c5f548310289abde9bd9d0e6655d225c1c130",
    "traces-4.jsonl": "f4595d819384b05d2d1c2b8e97416838706b134fe0995a160ee408395e913c9f",
    "traces-0.jsonl": "6a2ba42edf7617978c6aaa08c60352f6f7b0a415e3a1b71e70d8b0c374427ad8",
    "traces-1.jsonl": "898e17425c7bc60b501030b0a3f2c5979a1161cac0838f8f7519012bda7169cf"
  },
  "evidence_sha256": {
    "${PROJECT_ROOT}/work/experiments/night-20261010/cloud-continued/tmp3/results/231-instruct-math500-worker1-repair.json": "c3d85501d7cf06a02a045ef99715bba4ee777a28e3339caabc48da59eda3b83c",
    "${PROJECT_ROOT}/work/experiments/night-20261010/cloud-continued/tmp3/231-instruct-math500-worker1-repair.log": "cdf5c208fe20463288235ae04915d8c33359e2b8319fdb63cf2e10cc9be0e82c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/repair_worker1.sh": "26be12a4e8b90d55a82a5956555f4ff65b01aa0ac59797fca608a05dbf9e4be4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run-root-gate.json": "8da69e5eb51bd0713645155f7e1e5a005f50bd38e5d0ea608e0c551793dd3d0e"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/summary.json](../artifacts/work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 500,
  "completed": 500,
  "missing": 0,
  "correct": 312,
  "pass_at_1_completed_only": 0.624,
  "format_valid": 281,
  "format_fraction_completed_only": 0.562,
  "executed_fork_samples": 53,
  "unfinished_thinking": 79,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 9,
  "parallel_protocol_fraction_completed_only": 0.018,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 384,
  "parallel_execution_mismatch_samples": 110,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 292,
  "legacy_format_fraction_completed_only": 0.584,
  "legacy_parallel_protocol_valid": 21,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": false,
    "fork_coverage_at_least_0_2": false,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": false,
    "invalid_width_fraction_at_most_0_05": false,
    "at_least_one_correct": true
  },
  "gate_thresholds": {
    "basic_strict_format": 0.8,
    "fork_coverage": 0.2,
    "valid_parallel_among_executed_forks": 0.9,
    "max_invalid_width": 0.05,
    "min_correct": 1
  },
  "gate_raw_counts": {
    "completed": 500,
    "basic_valid": 281,
    "executed_fork_samples": 53,
    "valid_parallel_among_fork_samples": 9,
    "invalid_width_samples": 110,
    "correct": 312
  },
  "fork_coverage": 0.106,
  "valid_parallel_among_executed_forks": 0.16981132075471697,
  "invalid_width_fraction": 0.22,
  "correct_and_basic_valid": 270,
  "correct_and_parallel_valid": 8,
  "metrics_all": {
    "F": {
      "n": 500,
      "sum": 730603.0,
      "mean": 1461.206,
      "median": 901.0,
      "p95": 4094.0,
      "min": 63.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 500,
      "sum": 752536.0,
      "mean": 1505.072,
      "median": 952.5,
      "p95": 4094.0,
      "min": 63.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 500,
      "sum": 1698.0,
      "mean": 3.396,
      "median": 2.0,
      "p95": 14.0,
      "min": 2.0,
      "max": 23.0
    },
    "T_assembled": {
      "n": 500,
      "sum": 754234.0,
      "mean": 1508.468,
      "median": 958.0,
      "p95": 4096.0,
      "min": 65.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 500,
      "sum": 752536.0,
      "mean": 1505.072,
      "median": 952.5,
      "p95": 4094.0,
      "min": 63.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 500,
      "sum": 943.0,
      "mean": 1.886,
      "median": 1.0,
      "p95": 7.0,
      "min": 1.0,
      "max": 11.0
    },
    "wall_seconds": {
      "n": 500,
      "sum": 28019.65246105194,
      "mean": 56.03930492210388,
      "median": 35.21616804599762,
      "p95": 153.50601661205292,
      "min": 2.2441792488098145,
      "max": 162.2895929813385
    },
    "forks": {
      "n": 500,
      "sum": 55.0,
      "mean": 0.11,
      "median": 0.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 500,
      "sum": 55.0,
      "mean": 0.11,
      "median": 0.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 500,
      "sum": 555.0,
      "mean": 1.11,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 500,
      "sum": 752536.0,
      "mean": 1505.072,
      "median": 952.5,
      "p95": 4094.0,
      "min": 63.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 500,
      "sum": 943.0,
      "mean": 1.886,
      "median": 1.0,
      "p95": 7.0,
      "min": 1.0,
      "max": 11.0
    },
    "decode_calls_inferred": {
      "n": 500,
      "sum": 751593.0,
      "mean": 1503.186,
      "median": 948.0,
      "p95": 4093.0,
      "min": 61.0,
      "max": 4093.0
    },
    "widths": {
      "n": 154,
      "sum": 527.0,
      "mean": 3.4220779220779223,
      "median": 3.0,
      "p95": 6.0,
      "min": 2.0,
      "max": 8.0
    },
    "width_histogram": {
      "2": 26,
      "3": 76,
      "4": 30,
      "5": 12,
      "6": 6,
      "7": 1,
      "8": 3
    },
    "truncated_samples": 67,
    "truncated_fraction": 0.134,
    "invalid_width_samples": 110,
    "forked_samples": 53
  },
  "metrics_correct": {
    "F": {
      "n": 312,
      "sum": 315924.0,
      "mean": 1012.5769230769231,
      "median": 771.0,
      "p95": 2474.95,
      "min": 182.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 312,
      "sum": 325870.0,
      "mean": 1044.4551282051282,
      "median": 800.0,
      "p95": 2540.999999999999,
      "min": 192.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 312,
      "sum": 1077.0,
      "mean": 3.451923076923077,
      "median": 2.0,
      "p95": 14.0,
      "min": 2.0,
      "max": 20.0
    },
    "T_assembled": {
      "n": 312,
      "sum": 326947.0,
      "mean": 1047.9070512820513,
      "median": 802.0,
      "p95": 2542.999999999999,
      "min": 203.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 312,
      "sum": 325870.0,
      "mean": 1044.4551282051282,
      "median": 800.0,
      "p95": 2540.999999999999,
      "min": 192.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 312,
      "sum": 547.0,
      "mean": 1.7532051282051282,
      "median": 1.0,
      "p95": 7.0,
      "min": 1.0,
      "max": 11.0
    },
    "wall_seconds": {
      "n": 312,
      "sum": 12145.70161151886,
      "mean": 38.92853080615019,
      "median": 29.848583698272705,
      "p95": 98.69022536277767,
      "min": 7.119068145751953,
      "max": 150.26544547080994
    },
    "forks": {
      "n": 312,
      "sum": 36.0,
      "mean": 0.11538461538461539,
      "median": 0.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "rounds": {
      "n": 312,
      "sum": 36.0,
      "mean": 0.11538461538461539,
      "median": 0.0,
      "p95": 1.0,
      "min": 0.0,
      "max": 2.0
    },
    "generation_turns": {
      "n": 312,
      "sum": 348.0,
      "mean": 1.1153846153846154,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 3.0
    },
    "model_forward_calls_inferred": {
      "n": 312,
      "sum": 325870.0,
      "mean": 1044.4551282051282,
      "median": 800.0,
      "p95": 2540.999999999999,
      "min": 192.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 312,
      "sum": 547.0,
      "mean": 1.7532051282051282,
      "median": 1.0,
      "p95": 7.0,
      "min": 1.0,
      "max": 11.0
    },
    "decode_calls_inferred": {
      "n": 312,
      "sum": 325323.0,
      "mean": 1042.701923076923,
      "median": 796.5,
      "p95": 2539.5499999999993,
      "min": 186.0,
      "max": 4093.0
    },
    "widths": {
      "n": 48,
      "sum": 151.0,
      "mean": 3.1458333333333335,
      "median": 3.0,
      "p95": 4.649999999999999,
      "min": 2.0,
      "max": 5.0
    },
    "width_histogram": {
      "2": 10,
      "3": 24,
      "4": 11,
      "5": 3
    },
    "truncated_samples": 1,
    "truncated_fraction": 0.003205128205128205,
    "invalid_width_samples": 13,
    "forked_samples": 35
  },
  "historical_correct": 296,
  "historical_pass_at_1_completed_only": 0.592,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 500,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "math": {
      "planned": 500,
      "completed": 500,
      "correct": 312,
      "pass_at_1": 0.624,
      "basic_valid": 281,
      "basic_valid_fraction": 0.562,
      "parallel_valid": 9,
      "parallel_syntax_valid": 384,
      "parallel_execution_mismatch_samples": 110,
      "correct_and_basic_valid": 270,
      "correct_and_parallel_valid": 8,
      "metrics_all": {
        "F": {
          "n": 500,
          "sum": 730603.0,
          "mean": 1461.206,
          "median": 901.0,
          "p95": 4094.0,
          "min": 63.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 500,
          "sum": 752536.0,
          "mean": 1505.072,
          "median": 952.5,
          "p95": 4094.0,
          "min": 63.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 500,
          "sum": 1698.0,
          "mean": 3.396,
          "median": 2.0,
          "p95": 14.0,
          "min": 2.0,
          "max": 23.0
        },
        "T_assembled": {
          "n": 500,
          "sum": 754234.0,
          "mean": 1508.468,
          "median": 958.0,
          "p95": 4096.0,
          "min": 65.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 500,
          "sum": 752536.0,
          "mean": 1505.072,
          "median": 952.5,
          "p95": 4094.0,
          "min": 63.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 500,
          "sum": 943.0,
          "mean": 1.886,
          "median": 1.0,
          "p95": 7.0,
          "min": 1.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 500,
          "sum": 28019.65246105194,
          "mean": 56.03930492210388,
          "median": 35.21616804599762,
          "p95": 153.50601661205292,
          "min": 2.2441792488098145,
          "max": 162.2895929813385
        },
        "forks": {
          "n": 500,
          "sum": 55.0,
          "mean": 0.11,
          "median": 0.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "rounds": {
          "n": 500,
          "sum": 55.0,
          "mean": 0.11,
          "median": 0.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 500,
          "sum": 555.0,
          "mean": 1.11,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 500,
          "sum": 752536.0,
          "mean": 1505.072,
          "median": 952.5,
          "p95": 4094.0,
          "min": 63.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 500,
          "sum": 943.0,
          "mean": 1.886,
          "median": 1.0,
          "p95": 7.0,
          "min": 1.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 500,
          "sum": 751593.0,
          "mean": 1503.186,
          "median": 948.0,
          "p95": 4093.0,
          "min": 61.0,
          "max": 4093.0
        },
        "widths": {
          "n": 154,
          "sum": 527.0,
          "mean": 3.4220779220779223,
          "median": 3.0,
          "p95": 6.0,
          "min": 2.0,
          "max": 8.0
        },
        "width_histogram": {
          "2": 26,
          "3": 76,
          "4": 30,
          "5": 12,
          "6": 6,
          "7": 1,
          "8": 3
        },
        "truncated_samples": 67,
        "truncated_fraction": 0.134,
        "invalid_width_samples": 110,
        "forked_samples": 53
      },
      "metrics_correct": {
        "F": {
          "n": 312,
          "sum": 315924.0,
          "mean": 1012.5769230769231,
          "median": 771.0,
          "p95": 2474.95,
          "min": 182.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 312,
          "sum": 325870.0,
          "mean": 1044.4551282051282,
          "median": 800.0,
          "p95": 2540.999999999999,
          "min": 192.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 312,
          "sum": 1077.0,
          "mean": 3.451923076923077,
          "median": 2.0,
          "p95": 14.0,
          "min": 2.0,
          "max": 20.0
        },
        "T_assembled": {
          "n": 312,
          "sum": 326947.0,
          "mean": 1047.9070512820513,
          "median": 802.0,
          "p95": 2542.999999999999,
          "min": 203.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 312,
          "sum": 325870.0,
          "mean": 1044.4551282051282,
          "median": 800.0,
          "p95": 2540.999999999999,
          "min": 192.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 312,
          "sum": 547.0,
          "mean": 1.7532051282051282,
          "median": 1.0,
          "p95": 7.0,
          "min": 1.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 312,
          "sum": 12145.70161151886,
          "mean": 38.92853080615019,
          "median": 29.848583698272705,
          "p95": 98.69022536277767,
          "min": 7.119068145751953,
          "max": 150.26544547080994
        },
        "forks": {
          "n": 312,
          "sum": 36.0,
          "mean": 0.11538461538461539,
          "median": 0.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "rounds": {
          "n": 312,
          "sum": 36.0,
          "mean": 0.11538461538461539,
          "median": 0.0,
          "p95": 1.0,
          "min": 0.0,
          "max": 2.0
        },
        "generation_turns": {
          "n": 312,
          "sum": 348.0,
          "mean": 1.1153846153846154,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 3.0
        },
        "model_forward_calls_inferred": {
          "n": 312,
          "sum": 325870.0,
          "mean": 1044.4551282051282,
          "median": 800.0,
          "p95": 2540.999999999999,
          "min": 192.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 312,
          "sum": 547.0,
          "mean": 1.7532051282051282,
          "median": 1.0,
          "p95": 7.0,
          "min": 1.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 312,
          "sum": 325323.0,
          "mean": 1042.701923076923,
          "median": 796.5,
          "p95": 2539.5499999999993,
          "min": 186.0,
          "max": 4093.0
        },
        "widths": {
          "n": 48,
          "sum": 151.0,
          "mean": 3.1458333333333335,
          "median": 3.0,
          "p95": 4.649999999999999,
          "min": 2.0,
          "max": 5.0
        },
        "width_histogram": {
          "2": 10,
          "3": 24,
          "4": 11,
          "5": 3
        },
        "truncated_samples": 1,
        "truncated_fraction": 0.003205128205128205,
        "invalid_width_samples": 13,
        "forked_samples": 35
      },
      "historical_correct": 296,
      "historical_pass_at_1": 0.592
    }
  },
  "cost_definitions": {
    "model_forward_calls_inferred": "INFERRED, not measured: serial HF structured_generate runs one initial model forward and one for each additional sampled output, hence sum raw generated_ids lengths across ALL calls. Native unavailable.",
    "prefill_calls_inferred": "INFERRED, not measured: one initial HF prefill per positive-output generation call. Native unavailable.",
    "decode_calls_inferred": "INFERRED, not measured: all raw generated tokens minus positive-output generation calls; no speculation in this backend. Native unavailable.",
    "rounds": "Executed parallel fork rounds; native=0",
    "generation_turns": "Parallel rounds+1; native=1",
    "F": "Logical critical sequential sampled-token depth; native F=sampled length. Not measured GPU model-forward invocations.",
    "T_sampled": "Retained sampled response tokens",
    "T_forced": "Forced response tokens including think prefix/protocol bridges",
    "T_assembled": "Total assembled response tokens",
    "actual_generated_tokens": "All generated token outputs across actual generation calls, including discarded outputs if any",
    "wall_seconds": "Per-question generation elapsed, excludes engine startup; backend confounded",
    "backend_confound": "Structured uses HF structured serial backend through vLLM worker RPC; native uses fast vLLM generation. Wall comparisons are descriptive and cannot establish parallel execution speedup."
  },
  "backend_labels": [
    "hf_structured_serial_backend"
  ],
  "matching_protocol": {
    "prompt_policy": "Custom system-file supplied verbatim before native chat-template rendering; see system_file and hash",
    "question_seed": "42+sample_index",
    "response_budget": 4096,
    "path_budget": 2048,
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20
  },
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "provenance": {
    "evaluator_sha256": "ee768a765cfe13bfb058975b3afa0e83881275cfd07d61e3f6a324f562983e74",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "500",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/worker-exits.json](../artifacts/work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  1,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/report.json](../artifacts/work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/report.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "engineering_audit_only": true,
  "inputs_sha256": {
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-0.jsonl": "c43cbc65daa1f461182e3c320bed492dca5a6e80109b76ec8936f9c6d986768a",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-1.jsonl": "4bdde1cde3b1efef3fc4147d7cdf5efc948e7d8d5af89cf37618fa5f3183a528",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-2.jsonl": "3da4a2867b5d886ab87026e6fbfaef8155d2a220082bd62e6bf36fd855d575b2",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-3.jsonl": "16e9d01babaf42f85ce830e71c7b674ace21e6703a9716ee57c9ea688027c495",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-4.jsonl": "6031c03d31600f6a9f1542f0e59663d001c88f39a7b0a0470d72bd926cdfc5d2",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-5.jsonl": "b754843b4a8605ae55194cf46fbaeb12ef1238103cbf4062a3e2f58efb827669",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-6.jsonl": "aab8911e065e9c1d847cae8b9d6aaaac04758b7688446e86ba3514dd21c258c8",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0000/rank-7.jsonl": "081f3f6075ff953990d1f550cdc85800f623cff21123ad9613cc8534db80863e",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-0.jsonl": "939394dde2f8528c47b95762a48561f2e1501ce5639bb7f6849660302fb031b4",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-1.jsonl": "55590c73e845cd99a4176d66dc1d4fffd4871fbc2bf7efb75d7b4d075695405c",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-2.jsonl": "dfc3e2ad45bbc26d3520f57ebf896e978caa9ff77a640b946c903ba55771617f",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-3.jsonl": "b5f69ae6fea35f678c0738d5d947c476d3f44cef1b8b88b529b7b3f2a34f0a1b",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-4.jsonl": "eb99751873baaa5d30ff6119963530b121b7d0a53ce8d2d1687157fa2bc9af94",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-5.jsonl": "28a15047ccad50b760e8c015f1bd6adcae6e81ee2b33fe7aa59b7139acce7e0c",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-6.jsonl": "7fa4e0b7bf04284319b4919486f358d6d61eb0aaeed74b5b7cb4a304a7800cd9",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0032/rank-7.jsonl": "91c4e00a6fc580cfd634038a53e32747d13344f68f1f5f7c5c70eb02dd7d9491",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-0.jsonl": "c80e5421a70c1dd73f35e5a313a73e1e857e4362b35755c82509a8f47f52a221",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-1.jsonl": "b25555a6876ea5802ffa58172a92b7ff00999bfd9641f598bdd9dca5281505b1",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-2.jsonl": "b8241f4849fe342c7f32b4c0c994f79ea0e980821a35833c2b668c878aeb051a",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-3.jsonl": "a9d7dba6e1b2cb820595bce6a17b0b0b57f35cb2c34cf68cc41895e48e78bd00",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-4.jsonl": "7b7557b3355087de84f25bb8c96b4210fd6f6e1ecc9020d688fa8b7cf79eb8c9",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-5.jsonl": "8451dfb1b1a90a5445c2e665c2c52dd4a265e00286ad551c08ec80ef6d4b172d",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-6.jsonl": "7791a11fe8283ccfb95b146fffbfa8cb5daa373ac5d36511d17cd1f8ae2e9158",
    "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-7.jsonl": "4f43dde0a2245851ca8c9ce7dfe6349bbc0344c150ff45798642cb71d0e1fc4c",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-0.jsonl": "fe229ac5b0a5cf9143785a914a968d33ce5e85499a69c0f04d2b1b2fdb5ad133",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-1.jsonl": "435eb93cbbc265f7895f95453e5aeafe640f633d219a056c30665e163a3c1e43",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-2.jsonl": "7d0c5854858842cad59ff1b108c08cc722401acc8495ea13b9bf80ff545a31cf",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-3.jsonl": "d457773ac5adaf60bc3e5bc141578b2b034f8ecb5559d5f04ae57ec8a95c40cd",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-4.jsonl": "5ee1d3768216f83bbba48ff2cc325fc71cf93f9d89dddbe61da5e6e59ac4d1c6",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-5.jsonl": "81e4930ac63aea7c9ac811db668efe61968b71ed9f989f63729a10165a58d6bf",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-6.jsonl": "60491107577fd95b588945a32a0ca703491343c0f3d74eb57146d1a2804e7540",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-7.jsonl": "551df04cebc471d7f3b4a558b5a49ef09a1bc3eb5da37647c202458f773e4046",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-0.jsonl": "c43cbc65daa1f461182e3c320bed492dca5a6e80109b76ec8936f9c6d986768a",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-1.jsonl": "4bdde1cde3b1efef3fc4147d7cdf5efc948e7d8d5af89cf37618fa5f3183a528",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-2.jsonl": "3da4a2867b5d886ab87026e6fbfaef8155d2a220082bd62e6bf36fd855d575b2",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-3.jsonl": "16e9d01babaf42f85ce830e71c7b674ace21e6703a9716ee57c9ea688027c495",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-4.jsonl": "6031c03d31600f6a9f1542f0e59663d001c88f39a7b0a0470d72bd926cdfc5d2",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-5.jsonl": "b754843b4a8605ae55194cf46fbaeb12ef1238103cbf4062a3e2f58efb827669",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-6.jsonl": "aab8911e065e9c1d847cae8b9d6aaaac04758b7688446e86ba3514dd21c258c8",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0000/rank-7.jsonl": "081f3f6075ff953990d1f550cdc85800f623cff21123ad9613cc8534db80863e",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-0.jsonl": "7bbf1684d4718cb00a13c7d5d989999b62eb6d4e3e74e896b5c2878bae8a409a",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-1.jsonl": "c14f2e27f1c4d6d72a8e3e55b86b82f18db435d6fb1fbc35f6c19638d855656b",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-2.jsonl": "e1b6121ea1090e9b9ef50ca99518a8b148464aaf10f53716da8b8085374840b8",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-3.jsonl": "387343e2f3bec5ea42dacb5f81da3fc18668378bb14337daf91f133374aa1ed9",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-4.jsonl": "47ad7522772e5d57db56301061f5d56438ec90830f66c069f37194a132d5296a",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-5.jsonl": "527fe80585ad0045f4c4f66078395c5f1002c577ea09e8466baeb4c609980259",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-6.jsonl": "55c45bdc216721687e5203326be480d6f9bcc6309c693c4cf48a6382c0e43681",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0032/rank-7.jsonl": "53e9133782a402ea2027fd084623cf2ae005e71c443fb51792a117f735f67288",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-0.jsonl": "56b4ba3a8489fe6b7ba7d6b215bf9cc0caf0c5d216c663b4fdf458a97b0734c1",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-1.jsonl": "cbf887eadb0d28e9d9a4811c6db0d12315c2cda430e2e96d93f7d124ac4c5022",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-2.jsonl": "428f09f52893b9c88cc1ca46769c429076111f25a3ad92dd3d41f0fe05c3918a",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-3.jsonl": "ae3c28d3cf2132f8162959b93642d05c09241b336c4c24814b49e21bef2e3442",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-4.jsonl": "d0c04d6b7b4dce223c0cb3e42a79ceb5d566569cf328d6c30491af582b3debcb",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-5.jsonl": "e9f9d745ac77be83967b9a01b45c22ec676dbcee1f28489eff7dc5e3a48cad20",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-6.jsonl": "63f07d54c5586315dfa6e4959512754b2d8e0d48c06d3f261cb458e612e6c4ed",
    "work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/validation-0064/rank-7.jsonl": "260acd61b3f6f88bf8495338aed734af1c56a5f7cc9d1557f5bc8b2e6af76fdd",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-0.jsonl": "2876b6114d5fa6593cfd7cd5fd04f93fd15edf935fc5c0e0d3cb4206726596bf",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-1.jsonl": "cc94405805dfe638f45a62843c11f65e3fe2e6410e60a86b684f6c472ddc8189",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-2.jsonl": "27649f48ce73caed3ca52d49ff0c95082ddf38886c0f8a84f6ccd415b7ebb08c",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-3.jsonl": "36b31d5577a7a6bd4bf29082bb9568cc9ddf0ade02c9a0cc900e6d257280d198",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-4.jsonl": "6b76514613a7a0a3d2d474e67d474dc498a335be9d1b0521a2a004a4b1f1dafe",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-5.jsonl": "de16f1d9fc1b5abb3e5c5800fcfbd079610c022fb79cb41ee9a2741a747ce469",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-6.jsonl": "9812cf9df3497a872b8c84bcf2c82261e2d6288323c779d7ca977224c23bc12f",
    "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R2-traces-rank-7.jsonl": "9b7479ef3e82f1ddef0c68388ae32ef5b9b6434b5a3615be6c4fd1f27630e704"
  },
  "scorer_sha256": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
  "reward_sha256": "b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce",
  "receipts_sha256": "b0d63cd3ef465c95276a741104e7c7dd6b9a787027e75c56bb0434e611375040",
  "n": 2240,
  "summaries": "70 records; see original artifact",
  "changed_correct_cases": [
    {
      "arm": "R1",
      "scope": "validation",
      "id": "bigmath/cn_k12/95257",
      "step": 64,
      "rank": null,
      "sample": null,
      "index": 14,
      "file": "work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/validation-0064/rank-6.jsonl",
      "line": 2,
      "output_sha256": "d1ce5210c7192f9ecc8b75218759fc8977c08d4aab61bc8712747ee54d9eed53",
      "answer": "-\\frac{9}{4}",
      "old_grade": {
        "correct": true,
        "answer": "-\\dfrac{9}{4}",
        "extraction": "boxed",
        "valid": true,
        "error": null
      },
      "native_prefix_grade": {
        "correct": false,
        "answer": null,
        "extraction": "unfinished_thinking",
        "valid": false,
        "error": null
      },
      "stored_correct": true,
      "unfinished": true,
      "truncated": false,
      "format_valid": false,
      "widths": [
        2
      ],
      "F_actual": 850,
      "F_same_lengths_fullwidth_ideal": 850,
      "F_fork_actual": 558,
      "F_fork_ideal": 558,
      "penalty_bucket_actual": 0.08,
      "penalty_bucket_ideal": 0.08,
      "old_reward": 0.92,
      "native_prefix_reward": 0.0,
      "same_lengths_fullwidth_reward": 0.0,
      "strong_bonus_preserved": true,
      "stored_reward": null
    },
    {
      "arm": "R1",
      "scope": "train",
      "id": "bigmath/orca_math/27106",
      "step": 7,
      "rank": 7,
      "sample": 2,
      "index": null,
      "file": "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-7.jsonl",
      "line": 27,
      "output_sha256": "924bc2d3444203c927cbbba32879274d12e8efc9ce1a3d773763b1b62a19309f",
      "answer": "2",
      "old_grade": {
        "correct": true,
        "answer": "2",
        "extraction": "boxed",
        "valid": true,
        "error": null
      },
      "native_prefix_grade": {
        "correct": false,
        "answer": null,
        "extraction": "unfinished_thinking",
        "valid": false,
        "error": null
      },
      "stored_correct": true,
      "unfinished": true,
      "truncated": false,
      "format_valid": false,
      "widths": [
        2
      ],
      "F_actual": 272,
      "F_same_lengths_fullwidth_ideal": 272,
      "F_fork_actual": 75,
      "F_fork_ideal": 75,
      "penalty_bucket_actual": 0.02,
      "penalty_bucket_ideal": 0.02,
      "old_reward": 0.98,
      "native_prefix_reward": 0.0,
      "same_lengths_fullwidth_reward": 0.0,
      "strong_bonus_preserved": true,
      "stored_reward": 0.98
    }
  ],
  "scorer_errors": [],
  "actual_train_wrong_reward_cases": [
    {
      "arm": "R1",
      "scope": "train",
      "id": "bigmath/orca_math/27106",
      "step": 7,
      "rank": 7,
      "sample": 2,
      "index": null,
      "file": "work/experiments/rl-instruct-20261011/independent-review/paired-regrade-20261011/R1-traces-rank-7.jsonl",
      "line": 27,
      "output_sha256": "924bc2d3444203c927cbbba32879274d12e8efc9ce1a3d773763b1b62a19309f",
      "answer": "2",
      "old_grade": {
        "correct": true,
        "answer": "2",
        "extraction": "boxed",
        "valid": true,
        "error": null
      },
      "native_prefix_grade": {
        "correct": false,
        "answer": null,
        "extraction": "unfinished_thinking",
        "valid": false,
        "error": null
      },
      "stored_correct": true,
      "unfinished": true,
      "truncated": false,
      "format_valid": false,
      "widths": [
        2
      ],
      "F_actual": 272,
      "F_same_lengths_fullwidth_ideal": 272,
      "F_fork_actual": 75,
      "F_fork_ideal": 75,
      "penalty_bucket_actual": 0.02,
      "penalty_bucket_ideal": 0.02,
      "old_reward": 0.98,
      "native_prefix_reward": 0.0,
      "same_lengths_fullwidth_reward": 0.0,
      "strong_bonus_preserved": true,
      "stored_reward": 0.98
    }
  ],
  "semantics": "Native opener is already in prompt; visible prepend closes missing native thinking correctly. Same-length fullwidth F is counterfactual max across actual sibling lengths, not a measured new batch8 run. Correctness/validity/strong bonuses held fixed for F comparison. All training steps1:32 and validation0/32/64 reviewed; no weights or frozen artifacts changed; no benchmark inputs."
}
```

</details>

- [work/experiments/rl-instruct-20261011/long-run/batch-proof-gate-status.json](../artifacts/work/experiments/rl-instruct-20261011/long-run/batch-proof-gate-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "waiting_exact306terminal",
  "updated": 1791714008.7949648
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/baseline-native500-audit.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/baseline-native500-audit.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "at": "2026-10-11T19:45:36.383607+00:00",
  "completed": 500,
  "missing": 0,
  "technical_unknowns": 0,
  "correct": 251,
  "accuracy": 0.502,
  "format_valid": 457,
  "parallel_valid": 449,
  "correct_parallel": 231,
  "fork_samples": 486,
  "rounds": 509,
  "widths": "509 records; see original artifact",
  "stats_totals": {
    "critical_depth": 373370,
    "sampled_tokens": 488274,
    "forced_tokens": 6160,
    "actual_model_forward_calls": 373370
  },
  "question_wall_seconds": 15061.193541049957,
  "all8worker_exit_zero": true,
  "current_gpu_empty_claim": false,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "selection_allowed": false,
  "trace_sha256": {
    "rank-7.jsonl": "d5c4a082b215e0dde6610a13ac0c2bf49d2bc2ce70fc0a77458bcae345426c5a",
    "rank-1.jsonl": "72eeeac23cf2b3d39e3e82f982fdde47a7ee8df3d063fac35b1beb66edf9b714",
    "rank-6.jsonl": "22271b1e03e557a442c1721e4c9272d33cc443838fc4e776f27e253e29520638",
    "rank-4.jsonl": "876999b7237223b0d43e867d8eaa24401538a9cc0fc9af642634d1daf13f2f78",
    "rank-5.jsonl": "2c9dde98f9919072df8dcd94c7d2be24a53f29b9a38f197d6acbee5324f8ab55",
    "rank-3.jsonl": "4ef24420a4a05405fe479adefbbdcda184b8aa4aeb3962285b2dd07efe0d5538",
    "rank-0.jsonl": "a6849beaba853dd09fb5ed39239541c063d7e9f722a2e9bf057e15faa5c6b25b",
    "rank-2.jsonl": "60bc7d41cb380f8c4abd74905465898b41308e6ccef497b151ad699037162bc6"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/drain-status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/drain-status.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "corrected_fullwidth8_scores_running",
  "inference_proof_sha256": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108",
  "updated": 1791745392.9132953
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/controller-status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "001-fullSFT-baseline",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final"
    },
    {
      "id": "newdeep-fullSFT-0126",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final",
      "audit": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json",
      "audit_sha256": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832"
    }
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/releases/001-fullSFT-baseline.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/releases/001-fullSFT-baseline.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "id": "001-fullSFT-baseline",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline",
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/config.json": "938d961211217b1b58af4c9dc7c52a34f86c9ca8cace368475161cbd063a93d5",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model.safetensors.index.json": "a4552ba4015e525d61298de02b8b586eaab32ff08b6eac266303c9306edf5392",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00001-of-00002.safetensors": "6912a3e099474bb2e3476dfdc864e813852b86d30de62d3fe365b271792b9339",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00002-of-00002.safetensors": "0339d59522bda178993f328c35a2b9dea9b043b30d526b48655874af167cb438",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "selection_allowed": false,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/releases/newdeep-fullSFT-0126.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/releases/newdeep-fullSFT-0126.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "id": "newdeep-fullSFT-0126",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final",
  "audit": "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json",
  "audit_sha256": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/newdeep-fullSFT-0126",
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/config.json": "938d961211217b1b58af4c9dc7c52a34f86c9ca8cace368475161cbd063a93d5",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/model.safetensors.index.json": "a4552ba4015e525d61298de02b8b586eaab32ff08b6eac266303c9306edf5392",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/model-00001-of-00002.safetensors": "74f7086904d4c67fa82bcb4c67e0cff323c9068a0ae6678ac533cbfe8b50c637",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/model-00002-of-00002.safetensors": "883a173653f13c1340debacb9b3d315bdf243563b78bfa5e3f17fd41397e7a9e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/runs/production/final/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "selection_allowed": false,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/results/001-fullSFT-baseline.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/results/001-fullSFT-baseline.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "job": "001-fullSFT-baseline",
  "completed": 500,
  "missing": 0,
  "correct": 251,
  "accuracy": 0.502,
  "format_valid": 457,
  "parallel_valid": 449,
  "correct_parallel": 231,
  "fork_samples": 486,
  "rounds": 509,
  "widths": "509 records; see original artifact",
  "stats_totals": {
    "critical_depth": 373370,
    "sampled_tokens": 488274,
    "forced_tokens": 6160,
    "actual_model_forward_calls": 373370
  },
  "question_wall_seconds": 15061.193541049957,
  "exit_codes": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/config.json": "938d961211217b1b58af4c9dc7c52a34f86c9ca8cace368475161cbd063a93d5",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model.safetensors.index.json": "a4552ba4015e525d61298de02b8b586eaab32ff08b6eac266303c9306edf5392",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00001-of-00002.safetensors": "6912a3e099474bb2e3476dfdc864e813852b86d30de62d3fe365b271792b9339",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00002-of-00002.safetensors": "0339d59522bda178993f328c35a2b9dea9b043b30d526b48655874af167cb438",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "selection_allowed": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/seal.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/seal.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "sha256": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/plan.json": "9a1f51c41f7230c06b11e01b23d226eb0d6710004239c9f082617186a8f3be61",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py": "f70114dd1c229a7b2fe0b75fddcffe7a840b6a29cec0c64935007a5912418091",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/status.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "evaluating",
  "updated": 1791753650.9760568,
  "job": "newdeep-fullSFT-0126",
  "worker_pids": [
    1394206,
    1394207,
    1394208,
    1394209,
    1394210,
    1394211,
    1394212,
    1394213
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-main-fallback/status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-main-fallback/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "updated": 1791752916.6535015
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-paired-audit/R1-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-paired-audit/R1-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "checkpoint": 64,
  "arm": "R1",
  "coverage": 500,
  "technical_unknown": 0,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "baseline": {
    "correct": 251,
    "accuracy": 0.502,
    "format_valid": 457,
    "parallel_valid": 449,
    "correct_parallel": 231,
    "fork_samples": 486,
    "rounds": 509,
    "width_histogram": {
      "3": 198,
      "4": 125,
      "5": 15,
      "2": 163,
      "6": 8
    },
    "mean_width": 3.031434184675835,
    "actual_F": 373370,
    "mean_actual_F": 746.74,
    "sampled_T": 488274,
    "forced_T": 6160,
    "question_wall_seconds": 15061.193541049957
  },
  "candidate": {
    "correct": 353,
    "accuracy": 0.706,
    "format_valid": 277,
    "parallel_valid": 267,
    "correct_parallel": 217,
    "fork_samples": 485,
    "rounds": 488,
    "width_histogram": {
      "2": 426,
      "4": 10,
      "3": 48,
      "5": 2,
      "6": 2
    },
    "mean_width": 2.168032786885246,
    "actual_F": 449593,
    "mean_actual_F": 899.186,
    "sampled_T": 545768,
    "forced_T": 4696,
    "question_wall_seconds": 17451.924646377563
  },
  "paired": {
    "improved": 133,
    "regressed": 31,
    "same": 336,
    "accuracy_difference": 0.204,
    "bootstrap_95_percentile": [
      0.158,
      0.25
    ],
    "bootstrap_replicates": 20000,
    "seed": 42161011
  },
  "inputs_sha256": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-0.jsonl": "a6849beaba853dd09fb5ed39239541c063d7e9f722a2e9bf057e15faa5c6b25b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-1.jsonl": "72eeeac23cf2b3d39e3e82f982fdde47a7ee8df3d063fac35b1beb66edf9b714",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-2.jsonl": "60bc7d41cb380f8c4abd74905465898b41308e6ccef497b151ad699037162bc6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-3.jsonl": "4ef24420a4a05405fe479adefbbdcda184b8aa4aeb3962285b2dd07efe0d5538",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-4.jsonl": "876999b7237223b0d43e867d8eaa24401538a9cc0fc9af642634d1daf13f2f78",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-5.jsonl": "2c9dde98f9919072df8dcd94c7d2be24a53f29b9a38f197d6acbee5324f8ab55",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-6.jsonl": "22271b1e03e557a442c1721e4c9272d33cc443838fc4e776f27e253e29520638",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-7.jsonl": "d5c4a082b215e0dde6610a13ac0c2bf49d2bc2ce70fc0a77458bcae345426c5a",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/baseline-native500-audit.json": "be5013738f5c7b4bf2fe163fb67681f11b4a1e72b1ac85484c1423c38f633fd8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-0.jsonl": "21cd02b47840bd41afa4afc2f3a06c3b22b44bd4a0923fa32cba3f56763e89b6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-1.jsonl": "88f86bcc7b7e8a5dbd528cf2ed2602ebca81a7ae07228cc284250a5f05bdafef",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-2.jsonl": "41fe8826be633ebaaffa606aa89761403ef095b8b0332b3e44a23c2eadbe02e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-3.jsonl": "156b85c82865e165c24482d0aa48c81218265ea59d14898265475a74ecb3d632",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-4.jsonl": "41dd590e8066690bc61ed0e75975d0c67bac82f284dd41c0f1c105ac7214118c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-5.jsonl": "2c31ae9f416351d2e49966ccac9e3e1e7e9dbce77c2c27d8cb68be2fb01b36f7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-6.jsonl": "cef7c9d96db60f70aa2c53b49596eff3f0f98521b5d572ca51bb76e96737dff0",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064/rank-7.jsonl": "e716533059c3c18f15693be3a1cd55e83268dcde7d66fccc190d5c2979d9597c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R1-checkpoint-0064.json": "82fb3e093cadbc9054320060a69c5ecbf786118ead104a57b8d09244ccb5461b"
  },
  "selection_allowed": false,
  "created": 1791752916.1284313
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-paired-audit/R2-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-paired-audit/R2-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "checkpoint": 64,
  "arm": "R2",
  "coverage": 500,
  "technical_unknown": 0,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "baseline": {
    "correct": 251,
    "accuracy": 0.502,
    "format_valid": 457,
    "parallel_valid": 449,
    "correct_parallel": 231,
    "fork_samples": 486,
    "rounds": 509,
    "width_histogram": {
      "3": 198,
      "4": 125,
      "5": 15,
      "2": 163,
      "6": 8
    },
    "mean_width": 3.031434184675835,
    "actual_F": 373370,
    "mean_actual_F": 746.74,
    "sampled_T": 488274,
    "forced_T": 6160,
    "question_wall_seconds": 15061.193541049957
  },
  "candidate": {
    "correct": 280,
    "accuracy": 0.56,
    "format_valid": 456,
    "parallel_valid": 452,
    "correct_parallel": 262,
    "fork_samples": 494,
    "rounds": 507,
    "width_histogram": {
      "4": 391,
      "5": 24,
      "6": 80,
      "8": 6,
      "3": 4,
      "7": 1,
      "2": 1
    },
    "mean_width": 4.404339250493097,
    "actual_F": 341496,
    "mean_actual_F": 682.992,
    "sampled_T": 519265,
    "forced_T": 8229,
    "question_wall_seconds": 14593.95595574379
  },
  "paired": {
    "improved": 82,
    "regressed": 53,
    "same": 365,
    "accuracy_difference": 0.058,
    "bootstrap_95_percentile": [
      0.012,
      0.102
    ],
    "bootstrap_replicates": 20000,
    "seed": 42161011
  },
  "inputs_sha256": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-0.jsonl": "a6849beaba853dd09fb5ed39239541c063d7e9f722a2e9bf057e15faa5c6b25b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-1.jsonl": "72eeeac23cf2b3d39e3e82f982fdde47a7ee8df3d063fac35b1beb66edf9b714",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-2.jsonl": "60bc7d41cb380f8c4abd74905465898b41308e6ccef497b151ad699037162bc6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-3.jsonl": "4ef24420a4a05405fe479adefbbdcda184b8aa4aeb3962285b2dd07efe0d5538",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-4.jsonl": "876999b7237223b0d43e867d8eaa24401538a9cc0fc9af642634d1daf13f2f78",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-5.jsonl": "2c9dde98f9919072df8dcd94c7d2be24a53f29b9a38f197d6acbee5324f8ab55",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-6.jsonl": "22271b1e03e557a442c1721e4c9272d33cc443838fc4e776f27e253e29520638",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline/rank-7.jsonl": "d5c4a082b215e0dde6610a13ac0c2bf49d2bc2ce70fc0a77458bcae345426c5a",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/baseline-native500-audit.json": "be5013738f5c7b4bf2fe163fb67681f11b4a1e72b1ac85484c1423c38f633fd8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-0.jsonl": "01a22c74f93d27d20cf424d09b53e462a7a90dc4861f1942bd96fac0dbd62cc8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-1.jsonl": "a78289fa85b01b09e5ac760a57d97ceb6c6d115559dd9a0e79ea973c8cd2c5ce",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-2.jsonl": "f14a3061576db0779c6d60fec9023f1144dc20c58b4b9b11318931bf9ec66f39",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-3.jsonl": "6ee71369b81cb2be4fdcdc486768d42280b7373820142f56e8f12344fb8cac45",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-4.jsonl": "d8b8cdc914803d9047f7fa8ecfc42a908180b8f5ff662e1fc27d73a84640777b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-5.jsonl": "94a12a5bfa5ba3c2e4d5c2cf4854e6c12308f05e6c465fe83af9e20f5357cfac",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-6.jsonl": "f77ba1837da927034dd130ad7f49967216dd2162185b26f2ca0bb3ce532ab492",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064/rank-7.jsonl": "18dcd5ea3efd5fca50071f9bbb667e7af5039e59598e94b78c6ec1c075859577",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R2-checkpoint-0064.json": "f1b313dc58d340588ce1e875d1ad8e9ecf272e735c8d6477241061c3b076be6d"
  },
  "selection_allowed": false,
  "created": 1791752917.8209512
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/plan.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/plan.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hostname": "RUN_9c5b5b8949-mpimaster-0",
  "sft_status": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/status.json",
  "baseline": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "jobs": [
    {
      "id": "R1-checkpoint-0064",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/complete.json"
    },
    {
      "id": "R2-checkpoint-0064",
      "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf",
      "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/complete.json"
    }
  ],
  "parent_pid": 1388032,
  "baseline_worker_pids": [
    1388056,
    1388057,
    1388058,
    1388059,
    1388060,
    1388061,
    1388062,
    1388063
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/releases/R1-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/releases/R1-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "id": "R1-checkpoint-0064",
  "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf",
  "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/complete.json",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R1-checkpoint-0064",
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/config.json": "aab1e5eafe978977e5ff8d95f5c3a6fe368099a692804589b914537e20c51097",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model.safetensors.index.json": "460938bd7bd398df9bb83f58388ad0046b4e611b279cf747a8b40f3671c6374c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00001-of-00005.safetensors": "9b28798cef1da7e963f9a1c13d0e7df72b059f07cc011866b414d99ccf650bd9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00002-of-00005.safetensors": "d6d331820bc94a50adb9ac1a112baa8cf21722a6e6db393ebc5b2b7bcdbbfb8d",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00003-of-00005.safetensors": "ac2d079531ea95ff9aabbbfa3dbbd2eb9f9a821dd42200bdd5bf9442854ca281",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00004-of-00005.safetensors": "15de8003950d940cbd07f35c75b33499cbf6c63de6b4fbf25000dca8c5d97d72",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00005-of-00005.safetensors": "f3f8fc9c4b35261086c4b68da0622c45cd51b1b05149df4db4e7ec78d318d6a7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "selection_allowed": false,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/releases/R2-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/releases/R2-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "id": "R2-checkpoint-0064",
  "model": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf",
  "complete": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/complete.json",
  "questions": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "output": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/runs/R2-checkpoint-0064",
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/config.json": "aab1e5eafe978977e5ff8d95f5c3a6fe368099a692804589b914537e20c51097",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model.safetensors.index.json": "460938bd7bd398df9bb83f58388ad0046b4e611b279cf747a8b40f3671c6374c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00001-of-00005.safetensors": "230b14e947047989dced9eaec921726b0871b7224b6964cc2777b380dcd9115a",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00002-of-00005.safetensors": "2f769f2d348d62d1102f72b5cfc3daa9e4f26fcd7dad7c924ca0b4f419304cda",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00003-of-00005.safetensors": "16000b1062d10b34ad8ab14f7213988a2d6e3186c08f68365278995dd3568921",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00004-of-00005.safetensors": "c0df969915ec88bda9ba41cba7ff8c009bb0a71840ac8a6128d3bcb19134827f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00005-of-00005.safetensors": "075b7e70ed2d2345a8340b6805ae1036d3b56b78e01706efa17b568d1a4240c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "selection_allowed": false,
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R1-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R1-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "job": "R1-checkpoint-0064",
  "completed": 500,
  "missing": 0,
  "correct": 353,
  "accuracy": 0.706,
  "format_valid": 277,
  "parallel_valid": 267,
  "correct_parallel": 217,
  "fork_samples": 485,
  "rounds": 488,
  "widths": "488 records; see original artifact",
  "stats_totals": {
    "critical_depth": 449593,
    "sampled_tokens": 545768,
    "forced_tokens": 4696,
    "actual_model_forward_calls": 449593
  },
  "question_wall_seconds": 17451.924646377563,
  "exit_codes": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/config.json": "aab1e5eafe978977e5ff8d95f5c3a6fe368099a692804589b914537e20c51097",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model.safetensors.index.json": "460938bd7bd398df9bb83f58388ad0046b4e611b279cf747a8b40f3671c6374c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00001-of-00005.safetensors": "9b28798cef1da7e963f9a1c13d0e7df72b059f07cc011866b414d99ccf650bd9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00002-of-00005.safetensors": "d6d331820bc94a50adb9ac1a112baa8cf21722a6e6db393ebc5b2b7bcdbbfb8d",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00003-of-00005.safetensors": "ac2d079531ea95ff9aabbbfa3dbbd2eb9f9a821dd42200bdd5bf9442854ca281",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00004-of-00005.safetensors": "15de8003950d940cbd07f35c75b33499cbf6c63de6b4fbf25000dca8c5d97d72",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/model-00005-of-00005.safetensors": "f3f8fc9c4b35261086c4b68da0622c45cd51b1b05149df4db4e7ec78d318d6a7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run/checkpoint-0064/hf/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "selection_allowed": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R2-checkpoint-0064.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/results/R2-checkpoint-0064.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "job": "R2-checkpoint-0064",
  "completed": 500,
  "missing": 0,
  "correct": 280,
  "accuracy": 0.56,
  "format_valid": 456,
  "parallel_valid": 452,
  "correct_parallel": 262,
  "fork_samples": 494,
  "rounds": 507,
  "widths": "507 records; see original artifact",
  "stats_totals": {
    "critical_depth": 341496,
    "sampled_tokens": 519265,
    "forced_tokens": 8229,
    "actual_model_forward_calls": 341496
  },
  "question_wall_seconds": 14593.95595574379,
  "exit_codes": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "model_manifest": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/config.json": "aab1e5eafe978977e5ff8d95f5c3a6fe368099a692804589b914537e20c51097",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/generation_config.json": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model.safetensors.index.json": "460938bd7bd398df9bb83f58388ad0046b4e611b279cf747a8b40f3671c6374c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00001-of-00005.safetensors": "230b14e947047989dced9eaec921726b0871b7224b6964cc2777b380dcd9115a",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00002-of-00005.safetensors": "2f769f2d348d62d1102f72b5cfc3daa9e4f26fcd7dad7c924ca0b4f419304cda",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00003-of-00005.safetensors": "16000b1062d10b34ad8ab14f7213988a2d6e3186c08f68365278995dd3568921",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00004-of-00005.safetensors": "c0df969915ec88bda9ba41cba7ff8c009bb0a71840ac8a6128d3bcb19134827f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/model-00005-of-00005.safetensors": "075b7e70ed2d2345a8340b6805ae1036d3b56b78e01706efa17b568d1a4240c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/special_tokens_map.json": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/runs/strong_width/checkpoint-0064/hf/tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "protocol": {
    "suite": "standard MATH500 full500",
    "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
    "precision": "FP32",
    "backend": "FP32 HF FULLWIDTH8 single subgroup",
    "temperature": 1,
    "top_p": 1,
    "top_k": null,
    "response_budget": 4096,
    "path_budget": 768,
    "max_context": 16384,
    "seed": "42161011+question_index*1000",
    "samples_per_question": 1,
    "scorer": "frozen referenceblind MathVerify",
    "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
    "selection_allowed": false,
    "train_reward_leakage": false,
    "max_batched_paths": 8,
    "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
  },
  "selection_allowed": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/seal.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/seal.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "sha256": {
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/decoder.py": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/structured_replay.py": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/microbatch_decoder.py": "e2c8caaa7f4e5236324b44f08d7d3c2a26290a9e100cc4b2739d781ac16481ec",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/rollout.py": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/train.py": "69b4ad262254acfeae9e22924675c9f3386807d9cf28364dcb17968d8e0cc2a4",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare.py": "3a5b711c4d16e2ec306be03cd67bf1b4c892d499ec93fe14022dc61f5afc161b",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/counted_loop.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/source/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch.py": "2b25989b59e7fa1f279a9f6222d4c3f168d5fbf80c3d9e2394b29b853da006e7",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/prepare_continuation.py": "ded5b39384dd4c1226dc4c3b023e689b53531b0a024c7df9a8bcacf312f4e3f9",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-deep-full-20261011/production-export-proof.json": "777afd5a123fb97e52870145e65e626e612cf791821e14f5abccde2cdad54832",
    "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py": "3aa6d7bea31716a17a9de12c8ca63fe36e3e0eabe41474f414ce21d29bd08119",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/plan.json": "76df0874de8172bf3c03d4072749d09a288474ecd5395fe35735c6a001ae436e",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/controller.py": "df458ce16ddf319ff5faebb7238f84869b998f374ea0d849f08eb243fab93247",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-priority-RL64/worker.py": "24bcc77cc9df4ddef230223058803ed0015a23b58bcfcd800e418559d8ed1afd",
    "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json": "9203737e6c5d75f8dfd12db2277d9ba340e17ad23823f6f4b6fe9e11d0577108"
  }
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/status.json) — remote_nfs, снимок 2026-10-12T17:52:04.931427+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "updated": 1791752908.3682182
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-sparse/status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-sparse/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "evaluating",
  "updated": 1791743380.0419366,
  "job": "001-fullSFT-baseline",
  "worker_pids": [
    1384106,
    1384107,
    1384108,
    1384109,
    1384110,
    1384111,
    1384112,
    1384113
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/math500-successor/handoff-status.json](../artifacts/work/experiments/rl-instruct-20261011/math500-successor/handoff-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "waiting_first_three_terminal_and_idle_original",
  "original_state": "evaluating",
  "first_three_ready": false,
  "updated": 1791743370.417752
}
```

</details>

- [work/experiments/rl-instruct-20261011/parked-bs32-proof/status.json](../artifacts/work/experiments/rl-instruct-20261011/parked-bs32-proof/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "parked_by_latest_plain_full500_user_instruction",
  "no_gpu_proof_launched": true,
  "cpu_gate_stopped": true
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/metrics.jsonl](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/result.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 16,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/checkpoint-0016/hf"
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/stage16-quality-comparison.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/stage16-quality-comparison.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "initial_sft_correct": 16,
  "planned": 32,
  "checkpoints": [
    {
      "step": 4,
      "correct": 19,
      "delta_correct": 3,
      "format_valid": 31,
      "generation_forwards": 19257
    },
    {
      "step": 8,
      "correct": 20,
      "delta_correct": 4,
      "format_valid": 31,
      "generation_forwards": 19210
    },
    {
      "step": 16,
      "correct": 20,
      "delta_correct": 4,
      "format_valid": 29,
      "generation_forwards": 19795
    }
  ],
  "selection_allowed": true,
  "MATH500_selection": false,
  "continuation_target_step": 64
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/status.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 16,
  "steps": 16
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0000/summary.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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
    3,
    3,
    2,
    2,
    2,
    4,
    2,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    4,
    4,
    3,
    4,
    4,
    4,
    3,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    2,
    3
  ],
  "actual_rounds": 33,
  "logical_depth": [
    586,
    340,
    447,
    414,
    721,
    598,
    603,
    343,
    315,
    548,
    522,
    363,
    584,
    1609,
    460,
    462,
    886,
    754,
    372,
    452,
    289,
    658,
    500,
    178,
    456,
    504,
    462,
    636,
    881,
    397,
    336,
    645
  ],
  "sampled_tokens": [
    843,
    444,
    527,
    491,
    791,
    739,
    814,
    386,
    364,
    668,
    629,
    475,
    671,
    1788,
    530,
    630,
    1241,
    1225,
    495,
    768,
    382,
    917,
    678,
    204,
    496,
    675,
    508,
    828,
    1177,
    527,
    393,
    985
  ],
  "actual_forward_calls": [
    672,
    394,
    487,
    414,
    721,
    598,
    685,
    343,
    315,
    548,
    579,
    424,
    584,
    1609,
    460,
    552,
    1060,
    942,
    438,
    571,
    326,
    755,
    596,
    178,
    456,
    504,
    462,
    789,
    1070,
    453,
    336,
    828
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0004/summary.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0004/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 4,
  "completed": 32,
  "correct": 19,
  "format_valid": 31,
  "parallel_valid": 29,
  "fork_tasks": 30,
  "widths": [
    2,
    2,
    3,
    3,
    3,
    2,
    3,
    3,
    3,
    2,
    3,
    4,
    2,
    2,
    2,
    4,
    3,
    4,
    3,
    4,
    2,
    4,
    2,
    3,
    4,
    3,
    3,
    3,
    4,
    3
  ],
  "actual_rounds": 30,
  "logical_depth": [
    606,
    460,
    373,
    443,
    333,
    1102,
    570,
    305,
    295,
    548,
    401,
    359,
    398,
    844,
    499,
    464,
    573,
    928,
    480,
    354,
    289,
    791,
    905,
    241,
    493,
    559,
    608,
    355,
    875,
    484,
    683,
    476
  ],
  "sampled_tokens": [
    704,
    514,
    454,
    563,
    333,
    1378,
    598,
    421,
    381,
    774,
    463,
    474,
    677,
    1014,
    603,
    527,
    809,
    1209,
    593,
    531,
    382,
    847,
    1220,
    288,
    653,
    1000,
    895,
    355,
    1330,
    673,
    923,
    710
  ],
  "actual_forward_calls": [
    606,
    460,
    414,
    511,
    333,
    1244,
    570,
    366,
    339,
    666,
    401,
    419,
    505,
    844,
    499,
    464,
    651,
    1086,
    533,
    438,
    326,
    791,
    1025,
    241,
    559,
    710,
    762,
    355,
    1151,
    585,
    799,
    604
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0008/summary.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0008/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 8,
  "completed": 32,
  "correct": 20,
  "format_valid": 31,
  "parallel_valid": 30,
  "fork_tasks": 30,
  "widths": [
    3,
    4,
    3,
    4,
    4,
    3,
    3,
    3,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    2,
    2,
    4,
    3,
    2,
    3,
    3,
    3,
    3,
    4,
    2,
    2
  ],
  "actual_rounds": 30,
  "logical_depth": [
    652,
    288,
    401,
    448,
    1136,
    870,
    426,
    285,
    283,
    502,
    318,
    395,
    586,
    1046,
    654,
    350,
    396,
    680,
    396,
    352,
    331,
    524,
    734,
    297,
    544,
    618,
    505,
    669,
    895,
    474,
    531,
    585
  ],
  "sampled_tokens": [
    879,
    288,
    532,
    548,
    1461,
    1211,
    426,
    380,
    364,
    728,
    392,
    520,
    787,
    1213,
    823,
    401,
    536,
    961,
    487,
    529,
    456,
    574,
    1003,
    404,
    621,
    996,
    682,
    756,
    1376,
    743,
    607,
    684
  ],
  "actual_forward_calls": [
    794,
    288,
    442,
    481,
    1279,
    968,
    426,
    339,
    324,
    620,
    318,
    460,
    720,
    1046,
    654,
    350,
    462,
    838,
    458,
    436,
    331,
    524,
    822,
    352,
    544,
    792,
    619,
    714,
    1145,
    548,
    531,
    585
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0016/summary.json](../artifacts/work/experiments/rl-instruct-20261011/production-runs/strong_width-stage16/validation-0016/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 16,
  "completed": 32,
  "correct": 20,
  "format_valid": 29,
  "parallel_valid": 29,
  "fork_tasks": 31,
  "widths": [
    3,
    2,
    3,
    4,
    4,
    3,
    3,
    3,
    3,
    2,
    2,
    3,
    4,
    2,
    2,
    4,
    4,
    2,
    3,
    2,
    3,
    2,
    2,
    2,
    4,
    3,
    4,
    3,
    3,
    3,
    4
  ],
  "actual_rounds": 31,
  "logical_depth": [
    574,
    454,
    481,
    330,
    914,
    970,
    533,
    364,
    271,
    512,
    322,
    465,
    464,
    1035,
    593,
    332,
    580,
    901,
    297,
    416,
    255,
    370,
    464,
    252,
    340,
    1091,
    876,
    784,
    784,
    435,
    383,
    623
  ],
  "sampled_tokens": [
    799,
    454,
    624,
    454,
    1192,
    1301,
    670,
    445,
    333,
    700,
    396,
    543,
    670,
    1600,
    704,
    383,
    790,
    1301,
    334,
    603,
    319,
    486,
    535,
    305,
    413,
    1365,
    1014,
    1287,
    1232,
    576,
    453,
    986
  ],
  "actual_forward_calls": [
    714,
    454,
    481,
    381,
    1036,
    1081,
    599,
    416,
    298,
    597,
    322,
    465,
    564,
    1302,
    593,
    332,
    673,
    1023,
    297,
    517,
    255,
    442,
    464,
    252,
    340,
    1207,
    962,
    980,
    1052,
    492,
    425,
    779
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/root-production-gate-status.json](../artifacts/work/experiments/rl-instruct-20261011/root-production-gate-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "released",
  "started_at": 1791711201.819691,
  "updated_at": 1791712549.0903907,
  "finished_at": 1791712554.1462686,
  "arms": [
    {
      "mode": "strong_width",
      "lane": "tmp2",
      "task": "306-instruct-rl-strong-width-stage16",
      "receipt_sha256": "1d6993cb4d26d962637ef71347ef58efe07786cf5ff13a2d8efdb75b70fe82cc"
    },
    {
      "mode": "forward_only",
      "lane": "tmp3",
      "task": "232-instruct-rl-forward-only-stage16",
      "receipt_sha256": "594d505d1a834a63ef6f91939a8e8bbba359ed0a8c2b328807160f91d95ace75"
    }
  ]
}
```

</details>

- [work/experiments/rl-instruct-20261011/root-technical-gate-status.json](../artifacts/work/experiments/rl-instruct-20261011/root-technical-gate-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "released",
  "started_at": 1791710787.8347986,
  "updated_at": 1791711774.062233,
  "finished_at": 1791711779.0939755,
  "receipt_sha256": "eacd74d1cad1a0f8d1b804e790d02ebb1aaae353b2c66ff7849ed9093770cbed"
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/metrics.jsonl](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/result.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 2,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/checkpoint-0002/hf"
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/status.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

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

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/validation-0001/summary.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/validation-0001/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 1,
  "completed": 16,
  "correct": 14,
  "format_valid": 16,
  "parallel_valid": 16,
  "fork_tasks": 16,
  "widths": [
    3,
    3,
    3,
    2,
    2,
    3,
    2,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    3
  ],
  "actual_rounds": 16,
  "logical_depth": [
    308,
    424,
    312,
    440,
    276,
    369,
    271,
    266,
    361,
    596,
    320,
    314,
    322,
    441,
    280,
    375
  ],
  "sampled_tokens": [
    439,
    524,
    393,
    529,
    350,
    480,
    344,
    313,
    420,
    860,
    440,
    389,
    406,
    586,
    407,
    474
  ],
  "actual_forward_calls": [
    374,
    472,
    364,
    440,
    276,
    420,
    271,
    266,
    361,
    726,
    404,
    314,
    322,
    441,
    337,
    421
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-resume-step2/validation-0002/summary.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-resume-step2/validation-0002/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 2,
  "completed": 16,
  "correct": 14,
  "format_valid": 16,
  "parallel_valid": 16,
  "fork_tasks": 16,
  "widths": [
    3,
    2,
    3,
    2,
    2,
    3,
    2,
    2,
    2,
    4,
    3,
    2,
    2,
    4,
    3,
    4
  ],
  "actual_rounds": 16,
  "logical_depth": [
    351,
    322,
    323,
    482,
    318,
    441,
    235,
    353,
    352,
    476,
    346,
    314,
    335,
    703,
    291,
    408
  ],
  "sampled_tokens": [
    482,
    394,
    404,
    598,
    379,
    575,
    260,
    407,
    417,
    594,
    461,
    389,
    428,
    1012,
    415,
    596
  ],
  "actual_forward_calls": [
    417,
    322,
    375,
    482,
    318,
    491,
    235,
    353,
    352,
    516,
    425,
    314,
    335,
    826,
    353,
    479
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-step1/metrics.jsonl](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/runs/technical-step1/result.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "completed": true,
  "steps": 1,
  "world_size": 8,
  "trainable": 4022468096,
  "final": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runs/technical-step1/checkpoint-0001/hf"
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-step1/status.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "step": 1,
  "steps": 1
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-step1/validation-0000/summary.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/validation-0000/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 0,
  "completed": 16,
  "correct": 13,
  "format_valid": 16,
  "parallel_valid": 16,
  "fork_tasks": 16,
  "widths": [
    3,
    2,
    2,
    4,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    2,
    3,
    2,
    2
  ],
  "actual_rounds": 16,
  "logical_depth": [
    293,
    299,
    234,
    629,
    379,
    335,
    339,
    425,
    352,
    365,
    322,
    462,
    263,
    374,
    527,
    340
  ],
  "sampled_tokens": [
    360,
    351,
    289,
    853,
    468,
    393,
    466,
    578,
    371,
    423,
    368,
    633,
    312,
    538,
    572,
    388
  ],
  "actual_forward_calls": [
    329,
    299,
    234,
    735,
    379,
    335,
    418,
    469,
    352,
    365,
    322,
    556,
    263,
    460,
    527,
    340
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/runs/technical-step1/validation-0001/summary.json](../artifacts/work/experiments/rl-instruct-20261011/runs/technical-step1/validation-0001/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "step": 1,
  "completed": 16,
  "correct": 14,
  "format_valid": 16,
  "parallel_valid": 16,
  "fork_tasks": 16,
  "widths": [
    3,
    3,
    3,
    2,
    2,
    3,
    2,
    2,
    2,
    3,
    3,
    2,
    2,
    2,
    3,
    3
  ],
  "actual_rounds": 16,
  "logical_depth": [
    308,
    424,
    312,
    440,
    276,
    369,
    271,
    266,
    361,
    596,
    320,
    314,
    322,
    441,
    280,
    375
  ],
  "sampled_tokens": [
    439,
    524,
    393,
    529,
    350,
    480,
    344,
    313,
    420,
    860,
    440,
    389,
    406,
    586,
    407,
    474
  ],
  "actual_forward_calls": [
    374,
    472,
    364,
    440,
    276,
    420,
    271,
    266,
    361,
    726,
    404,
    314,
    322,
    441,
    337,
    421
  ],
  "sampler": "Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation",
  "selection_allowed": true,
  "benchmark": false
}
```

</details>

- [work/experiments/rl-instruct-20261011/throughput/REPORT.md](../artifacts/work/experiments/rl-instruct-20261011/throughput/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json](../artifacts/work/experiments/rl-instruct-20261011/throughput/width8-inference/actual/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

- [work/experiments/rl-instruct-20261011/user-stop-20261012/metrics.json](../artifacts/work/experiments/rl-instruct-20261011/user-stop-20261012/metrics.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "full": {
    "R1": {
      "passed": true,
      "checkpoint": 64,
      "arm": "R1",
      "coverage": 500,
      "technical_unknown": 0,
      "protocol": {
        "suite": "standard MATH500 full500",
        "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
        "precision": "FP32",
        "backend": "FP32 HF FULLWIDTH8 single subgroup",
        "temperature": 1,
        "top_p": 1,
        "top_k": null,
        "response_budget": 4096,
        "path_budget": 768,
        "max_context": 16384,
        "seed": "42161011+question_index*1000",
        "samples_per_question": 1,
        "scorer": "frozen referenceblind MathVerify",
        "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
        "selection_allowed": false,
        "train_reward_leakage": false,
        "max_batched_paths": 8,
        "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
      },
      "baseline": {
        "correct": 251,
        "accuracy": 0.502,
        "format_valid": 457,
        "parallel_valid": 449,
        "correct_parallel": 231,
        "fork_samples": 486,
        "rounds": 509,
        "width_histogram": {
          "3": 198,
          "4": 125,
          "5": 15,
          "2": 163,
          "6": 8
        },
        "mean_width": 3.031434184675835,
        "actual_F": 373370,
        "mean_actual_F": 746.74,
        "sampled_T": 488274,
        "forced_T": 6160,
        "question_wall_seconds": 15061.193541049957
      },
      "candidate": {
        "correct": 353,
        "accuracy": 0.706,
        "format_valid": 277,
        "parallel_valid": 267,
        "correct_parallel": 217,
        "fork_samples": 485,
        "rounds": 488,
        "width_histogram": {
          "2": 426,
          "4": 10,
          "3": 48,
          "5": 2,
          "6": 2
        },
        "mean_width": 2.168032786885246,
        "actual_F": 449593,
        "mean_actual_F": 899.186,
        "sampled_T": 545768,
        "forced_T": 4696,
        "question_wall_seconds": 17451.924646377563
      },
      "paired": {
        "improved": 133,
        "regressed": 31,
        "same": 336,
        "accuracy_difference": 0.204,
        "bootstrap_95_percentile": [
          0.158,
          0.25
        ],
        "bootstrap_replicates": 20000,
        "seed": 42161011
      },
      "selection_allowed": false,
      "created": 1791752916.1284313
    },
    "R2": {
      "passed": true,
      "checkpoint": 64,
      "arm": "R2",
      "coverage": 500,
      "technical_unknown": 0,
      "protocol": {
        "suite": "standard MATH500 full500",
        "native_prefix": "exact fullSFT native template thinkingTrue opener inprompt",
        "precision": "FP32",
        "backend": "FP32 HF FULLWIDTH8 single subgroup",
        "temperature": 1,
        "top_p": 1,
        "top_k": null,
        "response_budget": 4096,
        "path_budget": 768,
        "max_context": 16384,
        "seed": "42161011+question_index*1000",
        "samples_per_question": 1,
        "scorer": "frozen referenceblind MathVerify",
        "actual_forward_calls": "instrumented model.forward plus exact runtimeledger parity",
        "selection_allowed": false,
        "train_reward_leakage": false,
        "max_batched_paths": 8,
        "scorer_view": "native visible <think> opener plus response; formatflags rawresponse"
      },
      "baseline": {
        "correct": 251,
        "accuracy": 0.502,
        "format_valid": 457,
        "parallel_valid": 449,
        "correct_parallel": 231,
        "fork_samples": 486,
        "rounds": 509,
        "width_histogram": {
          "3": 198,
          "4": 125,
          "5": 15,
          "2": 163,
          "6": 8
        },
        "mean_width": 3.031434184675835,
        "actual_F": 373370,
        "mean_actual_F": 746.74,
        "sampled_T": 488274,
        "forced_T": 6160,
        "question_wall_seconds": 15061.193541049957
      },
      "candidate": {
        "correct": 280,
        "accuracy": 0.56,
        "format_valid": 456,
        "parallel_valid": 452,
        "correct_parallel": 262,
        "fork_samples": 494,
        "rounds": 507,
        "width_histogram": {
          "4": 391,
          "5": 24,
          "6": 80,
          "8": 6,
          "3": 4,
          "7": 1,
          "2": 1
        },
        "mean_width": 4.404339250493097,
        "actual_F": 341496,
        "mean_actual_F": 682.992,
        "sampled_T": 519265,
        "forced_T": 8229,
        "question_wall_seconds": 14593.95595574379
      },
      "paired": {
        "improved": 82,
        "regressed": 53,
        "same": 365,
        "accuracy_difference": 0.058,
        "bootstrap_95_percentile": [
          0.012,
          0.102
        ],
        "bootstrap_replicates": 20000,
        "seed": 42161011
      },
      "selection_allowed": false,
      "created": 1791752917.8209512
    }
  },
  "partial": {
    "newdeepSFT-main-duplicate": {
      "completed": 277,
      "unscored": 223,
      "incomplete_line": 0,
      "correct": 132,
      "accuracy": 0.47653429602888087,
      "matched_subset_baseline_correct": 141,
      "matched_subset_baseline_accuracy": 0.5090252707581228,
      "mean_F": 438.057761732852,
      "format_valid": 0.5595667870036101,
      "parallel_valid": 0.49097472924187724,
      "correct_parallel": 0.30324909747292417,
      "mean_width": 2.6950549450549453,
      "rounds_per_task": 1.3140794223826715,
      "mean_sampled_T": 533.7725631768953
    },
    "newdeepSFT": {
      "completed": 473,
      "unscored": 27,
      "incomplete_line": 0,
      "correct": 221,
      "accuracy": 0.46723044397463004,
      "matched_subset_baseline_correct": 240,
      "matched_subset_baseline_accuracy": 0.507399577167019,
      "mean_F": 465.9873150105708,
      "format_valid": 0.5581395348837209,
      "parallel_valid": 0.49682875264270615,
      "correct_parallel": 0.30021141649048627,
      "mean_width": 2.6978653530377668,
      "rounds_per_task": 1.2875264270613107,
      "mean_sampled_T": 567.7019027484143
    },
    "R1-checkpoint32": {
      "completed": 305,
      "unscored": 195,
      "incomplete_line": 0,
      "correct": 212,
      "accuracy": 0.6950819672131148,
      "matched_subset_baseline_correct": 161,
      "matched_subset_baseline_accuracy": 0.5278688524590164,
      "mean_F": 802.6655737704918,
      "format_valid": 0.8557377049180328,
      "parallel_valid": 0.8459016393442623,
      "correct_parallel": 0.6295081967213115,
      "mean_width": 2.340764331210191,
      "rounds_per_task": 1.0295081967213116,
      "mean_sampled_T": 1011.4196721311475
    }
  },
  "at": 1791753750.2309206
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/rl-instruct-20261011/campaign500/controller.py](../artifacts/work/experiments/rl-instruct-20261011/campaign500/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/campaign500/launch.py](../artifacts/work/experiments/rl-instruct-20261011/campaign500/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run.sh](../artifacts/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/run.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/eval24-joint/launch.py](../artifacts/work/experiments/rl-instruct-20261011/eval24-joint/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/long-run/launch.py](../artifacts/work/experiments/rl-instruct-20261011/long-run/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/long-run/prepare.py](../artifacts/work/experiments/rl-instruct-20261011/long-run/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py](../artifacts/work/experiments/rl-instruct-20261011/math500-fullwidth8/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/math500-main-fallback/controller.py](../artifacts/work/experiments/rl-instruct-20261011/math500-main-fallback/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/math500-priority-RL64/controller.py](../artifacts/work/experiments/rl-instruct-20261011/math500-priority-RL64/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/math500-sparse/controller.py](../artifacts/work/experiments/rl-instruct-20261011/math500-sparse/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/math500-successor/controller.py](../artifacts/work/experiments/rl-instruct-20261011/math500-successor/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/production-runner/launch.py](../artifacts/work/experiments/rl-instruct-20261011/production-runner/launch.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/production-runner/prepare.py](../artifacts/work/experiments/rl-instruct-20261011/production-runner/prepare.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/production-runner/train.py](../artifacts/work/experiments/rl-instruct-20261011/production-runner/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-instruct-20261011/reward.py](../artifacts/work/experiments/rl-instruct-20261011/reward.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Дополнительно проверенные конфигурации и формулы

- [work/experiments/rl-instruct-20261011/data/revision2/manifest.json](../artifacts/work/experiments/rl-instruct-20261011/data/revision2/manifest.json) — remote_nfs, снимок 2026-10-12T20:27:50.324246+00:00.
