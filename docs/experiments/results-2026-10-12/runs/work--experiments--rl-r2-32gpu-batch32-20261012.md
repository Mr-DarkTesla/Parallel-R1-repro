# work/experiments/rl-r2-32gpu-batch32-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-r2-32gpu-batch32-20261012/production-config-v2.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/production-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
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
  "checkpoint_every": 16,
  "max_replay_drift": 0.01,
  "actor_dtype": "fp32",
  "zero1_optimizer": true,
  "tf32": false,
  "std_normalization": false,
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/production",
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
  "exact_optimizer_resume": false
}
```

</details>

- [work/experiments/rl-r2-32gpu-batch32-20261012/smoke-config-v2.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/smoke-config-v2.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050/hf",
  "system": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/system.txt",
  "scorer": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "format_validator": "${PROJECT_ROOT}/work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py",
  "replay": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/runner/structured_replay.py",
  "reward": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/reward.py",
  "gpu_audit": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/distributed-smoke-proof.json",
  "train": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/train.jsonl",
  "val": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/data/val.jsonl",
  "seed": 20261012,
  "validation_seed": 91261011,
  "world_size": 32,
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
  "batch_decoder": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/runner/microbatch_decoder.py",
  "max_batched_paths": 8,
  "bonus_schedule": "constant_no_annealing",
  "curriculum": "1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion",
  "selection_allowed": true,
  "benchmark_used_for_selection": false,
  "validation_protocol": "Matched clean val32 fixed seed; fullwidth8; weights-only continuation",
  "lane": "one_cloud_job_4x8_one_response_per_gpu",
  "reward_mode": "strong_width",
  "output": "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/smoke",
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
  "skip_validation": true,
  "skip_exports": true,
  "resident_fixture_step": 52
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-r2-32gpu-batch32-20261012/acceleration-audit/REPORT.md](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/acceleration-audit/REPORT.md) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [work/experiments/rl-r2-32gpu-batch32-20261012/attempts/01-tied-export-count/handoff-status.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/attempts/01-tied-export-count/handoff-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "time": 1791797118.2961102,
  "old_job": "RUN_4b43efec89",
  "error": "AssertionError((399, 4411424256))",
  "traceback": "Traceback (most recent call last):\n  File \"${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/handoff.py\", line 165, in <module>\n    main();break\n    ^^^^^^\n  File \"${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/handoff.py\", line 109, in main\n    proof=checkpoint_proof(cp)\n          ^^^^^^^^^^^^^^^^^^^^\n  File \"${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/handoff.py\", line 49, in checkpoint_proof\n    assert tensor_count==398 and count>=4_000_000_000,(tensor_count,count)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError: (399, 4411424256)\n"
}
```

</details>

- [work/experiments/rl-r2-32gpu-batch32-20261012/before-stop.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/before-stop.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/rl-r2-32gpu-batch32-20261012/checkpoint-0050-handoff-proof.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/checkpoint-0050-handoff-proof.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "step": 50,
  "checkpoint": "${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050",
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "tensors": 399,
  "parameters": 4022468096,
  "serialized_parameters": 4411424256,
  "tied_alias_parameters": 388956160,
  "finite": true,
  "unsharded": true,
  "optimizer_reset": true,
  "exact_optimizer_resume": false,
  "source_validation_summary": {
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
  },
  "time": 1791798541.5375202
}
```

</details>

- [work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/summary.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "checkpoint": 50,
  "completed": 500,
  "missing": 0,
  "technical_unknowns": 0,
  "correct": 392,
  "format_valid": 443,
  "parallel_valid": 441,
  "correct_and_parallel": 382,
  "fork_tasks": 493,
  "format_and_fork_count_all": 441,
  "mean_actual_forwards": 1209.236,
  "mean_sampled_tokens": 1834.346,
  "mean_width": 4.127016129032258,
  "mean_depth": 0.992,
  "format_conditioned": {
    "n": 443,
    "mean_actual_forwards": 1052.0880361173815,
    "mean_width": 4.099099099099099,
    "mean_depth": 1.002257336343115
  },
  "all32_worker_exit0": true,
  "traces": {
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-0.jsonl": "8e84776d9411d07584fa30006742357717cc292874a57b2991826c4bb779383d",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-1.jsonl": "9a0fd64bea0906b65492638ffcaf2326c8aab0dc261d4d359865d621e5a768e9",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-2.jsonl": "69017acc184f03a6ffce90b7094a809dcbba4e99dedee99eb5a1ee131ac1edce",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-3.jsonl": "2562a7d97781ede362108fe302f262cd68e53901edc27d72e46e97a2990f75f2",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-4.jsonl": "28677f76d3942bb1b806897e8405c7a7ab3c87b707e97e6812934ca307408094",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-5.jsonl": "36cdbc931482c28eba8bdfb14208eee0cc327527e9866d02b69eda81f02b8031",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-6.jsonl": "ec34ebb0bf8ada181c8867314efb4110c313d6b356503e4a199f610cf265f462",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-7.jsonl": "81427707fa2ccde4a5cf4cc099c046e957191e88833e2797cf9111bad6d0df8a",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-8.jsonl": "923524a55bdde5f499644baa7d887bbe795010dc846af3e6d186d9b455235e61",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-9.jsonl": "8619d18b9e6d025d7144af231375a3d84ff2e983841c77249a290a75d76b09a3",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-10.jsonl": "6fd0b779a2f9e90d7ed6d8baf0edbaa97315d424e68cc342ac3bd4b034761ca2",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-11.jsonl": "3632bb8eac73eaf8250bd24e62f1e0630a0f69b2060aaf8ff3a3a603f29089ec",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-12.jsonl": "fa8d22f9c52b6c8dd77924abc3969e8aed43598f8c319ab3ba95f566b04b8607",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-13.jsonl": "a222d708310a94541d80974e1af7c41525b502dcc37d32854d7c0940be8b69f0",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-14.jsonl": "0e6982056c7e3a9ab333d8515df031e415899e6e9cd94debc6062fe63d6a7dd7",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-15.jsonl": "ba85f46697606778c874da8b318d483685051116b3462b6c74572219b5f6941d",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-16.jsonl": "24c04d89561371063879a862acd5a9ab8e25b19c21f77c9f2948049e128ccfc4",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-17.jsonl": "5d4bc71a9e8b468ce62d5bea9c84884dcaa50d4f91d7999c9953aeb7cf51970c",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-18.jsonl": "be1652b997bbf89da0a1c95c187262a726f3e277b3b40e6710514c67fb757145",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-19.jsonl": "7e86b19a75e94b64f01f9b66c51e4221200d78ad70ebf81460a786a1620e3ed0",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-20.jsonl": "97035c82abb373e77ee86a75905a89126fd6af605537fd1c3a9361e9eaa0448b",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-21.jsonl": "0866fb6b8a4f21df149c3673a1449fd113dc1c7ac27bb3bc587b0a838d14076f",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-22.jsonl": "515667f2e9557420d9d56feacfe45580503d714949df79a0326357ffb1f334d1",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-23.jsonl": "827bdac93dcbc19ec68756f15dadcfbc2e0d58f056daa962dd44246f1aae44a0",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-24.jsonl": "255437b4897aef83c4a20d3704d5d97a065e281772357cedc052b046cd7eec1e",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-25.jsonl": "ff083177a102faf1e49651ff36433563ebc35ecae65a40a7f1d6950c8bbc6681",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-26.jsonl": "0b5e8e9fa2955de03539fbff28b81412269d9f5275f20208a6bbcb07906ff668",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-27.jsonl": "31a271582845dd4e2ada9b825d0bce7cae70cfd26acf406b855cceac2fce1eea",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-28.jsonl": "853e85bff53bc742e72dad64d0d8f7b7c415c16368de8be790d266ea02486f2e",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-29.jsonl": "769e26f16a3138ccee20fc92afcf17f7d276b40cc4eb05c938d7d3ba6825e19f",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-30.jsonl": "4934c6db4e26dd180afa80344a4a5d14eed27f8656de67652aa20241c069cc4e",
    "${PROJECT_ROOT}/work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/rank-31.jsonl": "92c9f721f47fba52ff02a7ed06fa2ded93f0a6b4728ffe233e0cd40bc5843230"
  },
  "traces_always_retained": true,
  "eval_worker_sha256": "bc2ce3952f6defc21178d053508932f353d244f085af4b8d4872ae1b620370af",
  "questions_sha256": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
  "model_sha256": "727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c",
  "protocol": "FP32 fullwidth8; native think prefix; temperature1 top_p1; response4096 path768 context16384; seed42161011+index*1000; corrected final-answer scorer; instrumented F",
  "selection_allowed": false,
  "benchmark": true,
  "finished_at": 1791800231.747727,
  "accuracy": 0.784,
  "format_and_fork_fraction_all": 0.882,
  "matched_fullSFT_baseline": {
    "correct": 251,
    "completed": 500,
    "mean_actual_forwards": 746.74,
    "improved": 156,
    "regressed": 15,
    "source": "${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline"
  }
}
```

</details>

- [work/experiments/rl-r2-32gpu-batch32-20261012/handoff-status.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/handoff-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "submitted32_eval_then_smoke_then_rl",
  "time": 1791798570.874114,
  "old_job": "RUN_4b43efec89",
  "job_id": "RUN_5482aee87e",
  "initial_step": 50,
  "optimizer_reset": true
}
```

</details>

- [work/experiments/rl-r2-32gpu-batch32-20261012/maintenance/20261012T085057Z/handoff-status.json](../artifacts/work/experiments/rl-r2-32gpu-batch32-20261012/maintenance/20261012T085057Z/handoff-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "waiting_verified_checkpoint",
  "time": 1791795055.4164367,
  "old_job": "RUN_4b43efec89",
  "current_step": 46,
  "next_anchor": 50
}
```

</details>
