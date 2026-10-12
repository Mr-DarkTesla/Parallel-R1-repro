# work/experiments/format-loss-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/manifest.json](../artifacts/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "constrained_decoding": true,
  "format_guard_version": 1,
  "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
  "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/manifest.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "constrained_decoding": true,
  "format_guard_version": 1,
  "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
  "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/manifest.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/format-diagnosis-20261010/parallel-inside-think-example-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/questions-128.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 128,
  "suite": "128",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "constrained_decoding": true,
  "format_guard_version": 1,
  "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
  "system_sha256": "2e0a1836fccd2fd035e04897b5cd2b56795b0ad0cca87028363d5305bb72f8db",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
  "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
  "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9",
  "runtime_sha256": {
    "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
    "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
    "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
    "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
    "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
  }
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json](../artifacts/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 104,
  "pass_at_1_completed_only": 0.8125,
  "format_valid": 103,
  "format_fraction_completed_only": 0.8046875,
  "executed_fork_samples": 2,
  "unfinished_thinking": 18,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 1,
  "parallel_protocol_fraction_completed_only": 0.0078125,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 94,
  "legacy_format_fraction_completed_only": 0.734375,
  "legacy_parallel_protocol_valid": 0,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": true,
    "fork_coverage_at_least_0_2": false,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": false,
    "invalid_width_fraction_at_most_0_05": true,
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
    "completed": 128,
    "basic_valid": 103,
    "executed_fork_samples": 2,
    "valid_parallel_among_fork_samples": 1,
    "invalid_width_samples": 0,
    "correct": 104
  },
  "fork_coverage": 0.015625,
  "valid_parallel_among_executed_forks": 0.5,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 101,
  "correct_and_parallel_valid": 1,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 235906.0,
      "mean": 1843.015625,
      "median": 1278.0,
      "p95": 4094.0,
      "min": 328.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 237267.0,
      "mean": 1853.6484375,
      "median": 1278.0,
      "p95": 4094.0,
      "min": 328.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 283.0,
      "mean": 2.2109375,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 20.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 237550.0,
      "mean": 1855.859375,
      "median": 1280.0,
      "p95": 4096.0,
      "min": 330.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 237267.0,
      "mean": 1853.6484375,
      "median": 1278.0,
      "p95": 4094.0,
      "min": 328.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 139.0,
      "mean": 1.0859375,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 7.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 9104.114355325699,
      "mean": 71.12589340098202,
      "median": 48.84341776371002,
      "p95": 157.89680511951445,
      "min": 12.581478118896484,
      "max": 163.17431902885437
    },
    "forks": {
      "n": 128,
      "sum": 2.0,
      "mean": 0.015625,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 128,
      "sum": 2.0,
      "mean": 0.015625,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 130.0,
      "mean": 1.015625,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 237267.0,
      "mean": 1853.6484375,
      "median": 1278.0,
      "p95": 4094.0,
      "min": 328.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 139.0,
      "mean": 1.0859375,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 7.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 237128.0,
      "mean": 1852.5625,
      "median": 1277.0,
      "p95": 4093.0,
      "min": 327.0,
      "max": 4093.0
    },
    "widths": {
      "n": 2,
      "sum": 6.0,
      "mean": 3.0,
      "median": 3.0,
      "p95": 3.9,
      "min": 2.0,
      "max": 4.0
    },
    "width_histogram": {
      "2": 1,
      "4": 1
    },
    "truncated_samples": 23,
    "truncated_fraction": 0.1796875,
    "invalid_width_samples": 0,
    "forked_samples": 2
  },
  "metrics_correct": {
    "F": {
      "n": 104,
      "sum": 144403.0,
      "mean": 1388.4903846153845,
      "median": 1107.5,
      "p95": 3488.2499999999995,
      "min": 328.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 104,
      "sum": 144478.0,
      "mean": 1389.2115384615386,
      "median": 1107.5,
      "p95": 3488.2499999999995,
      "min": 328.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 104,
      "sum": 217.0,
      "mean": 2.0865384615384617,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 11.0
    },
    "T_assembled": {
      "n": 104,
      "sum": 144695.0,
      "mean": 1391.298076923077,
      "median": 1109.5,
      "p95": 3490.2499999999995,
      "min": 330.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 104,
      "sum": 144478.0,
      "mean": 1389.2115384615386,
      "median": 1107.5,
      "p95": 3488.2499999999995,
      "min": 328.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 104,
      "sum": 109.0,
      "mean": 1.0480769230769231,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 6.0
    },
    "wall_seconds": {
      "n": 104,
      "sum": 5583.388636827469,
      "mean": 53.68642920026412,
      "median": 42.52384150028229,
      "p95": 131.67923074960706,
      "min": 12.581478118896484,
      "max": 150.963036775589
    },
    "forks": {
      "n": 104,
      "sum": 1.0,
      "mean": 0.009615384615384616,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 104,
      "sum": 1.0,
      "mean": 0.009615384615384616,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 104,
      "sum": 105.0,
      "mean": 1.0096153846153846,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 104,
      "sum": 144478.0,
      "mean": 1389.2115384615386,
      "median": 1107.5,
      "p95": 3488.2499999999995,
      "min": 328.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 104,
      "sum": 109.0,
      "mean": 1.0480769230769231,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 6.0
    },
    "decode_calls_inferred": {
      "n": 104,
      "sum": 144369.0,
      "mean": 1388.1634615384614,
      "median": 1106.5,
      "p95": 3487.2499999999995,
      "min": 327.0,
      "max": 4093.0
    },
    "widths": {
      "n": 1,
      "sum": 2.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "width_histogram": {
      "2": 1
    },
    "truncated_samples": 1,
    "truncated_fraction": 0.009615384615384616,
    "invalid_width_samples": 0,
    "forked_samples": 1
  },
  "historical_correct": 103,
  "historical_pass_at_1_completed_only": 0.8046875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 128,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 53,
      "pass_at_1": 0.828125,
      "basic_valid": 54,
      "basic_valid_fraction": 0.84375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 53,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 111966.0,
          "mean": 1749.46875,
          "median": 1168.5,
          "p95": 4094.0,
          "min": 473.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 111966.0,
          "mean": 1749.46875,
          "median": 1168.5,
          "p95": 4094.0,
          "min": 473.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 128.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 112094.0,
          "mean": 1751.46875,
          "median": 1170.5,
          "p95": 4096.0,
          "min": 475.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 111966.0,
          "mean": 1749.46875,
          "median": 1168.5,
          "p95": 4094.0,
          "min": 473.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 4344.0920169353485,
          "mean": 67.87643776461482,
          "median": 45.594804525375366,
          "p95": 158.49822694063187,
          "min": 17.243929862976074,
          "max": 162.84196090698242
        },
        "forks": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 111966.0,
          "mean": 1749.46875,
          "median": 1168.5,
          "p95": 4094.0,
          "min": 473.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 111902.0,
          "mean": 1748.46875,
          "median": 1167.5,
          "p95": 4093.0,
          "min": 472.0,
          "max": 4093.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 10,
        "truncated_fraction": 0.15625,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 53,
          "sum": 69658.0,
          "mean": 1314.301886792453,
          "median": 1085.0,
          "p95": 2908.9999999999995,
          "min": 473.0,
          "max": 3495.0
        },
        "T_sampled": {
          "n": 53,
          "sum": 69658.0,
          "mean": 1314.301886792453,
          "median": 1085.0,
          "p95": 2908.9999999999995,
          "min": 473.0,
          "max": 3495.0
        },
        "T_forced": {
          "n": 53,
          "sum": 106.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 53,
          "sum": 69764.0,
          "mean": 1316.301886792453,
          "median": 1087.0,
          "p95": 2910.9999999999995,
          "min": 475.0,
          "max": 3497.0
        },
        "actual_generated_tokens": {
          "n": 53,
          "sum": 69658.0,
          "mean": 1314.301886792453,
          "median": 1085.0,
          "p95": 2908.9999999999995,
          "min": 473.0,
          "max": 3495.0
        },
        "generation_calls": {
          "n": 53,
          "sum": 53.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 53,
          "sum": 2721.5443031787872,
          "mean": 51.34989251280731,
          "median": 40.52191233634949,
          "p95": 118.77220802307127,
          "min": 17.243929862976074,
          "max": 140.82586193084717
        },
        "forks": {
          "n": 53,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 53,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 53,
          "sum": 53.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 53,
          "sum": 69658.0,
          "mean": 1314.301886792453,
          "median": 1085.0,
          "p95": 2908.9999999999995,
          "min": 473.0,
          "max": 3495.0
        },
        "prefill_calls_inferred": {
          "n": 53,
          "sum": 53.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 53,
          "sum": 69605.0,
          "mean": 1313.301886792453,
          "median": 1084.0,
          "p95": 2907.9999999999995,
          "min": 472.0,
          "max": 3494.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 53,
      "historical_pass_at_1": 0.828125
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 51,
      "pass_at_1": 0.796875,
      "basic_valid": 49,
      "basic_valid_fraction": 0.765625,
      "parallel_valid": 1,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 48,
      "correct_and_parallel_valid": 1,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 123940.0,
          "mean": 1936.5625,
          "median": 1370.5,
          "p95": 4094.0,
          "min": 328.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 125301.0,
          "mean": 1957.828125,
          "median": 1370.5,
          "p95": 4094.0,
          "min": 328.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 155.0,
          "mean": 2.421875,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 20.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 125456.0,
          "mean": 1960.25,
          "median": 1372.5,
          "p95": 4096.0,
          "min": 330.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 125301.0,
          "mean": 1957.828125,
          "median": 1370.5,
          "p95": 4094.0,
          "min": 328.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 75.0,
          "mean": 1.171875,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 7.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 4760.02233839035,
          "mean": 74.37534903734922,
          "median": 54.437711238861084,
          "p95": 156.77120552062988,
          "min": 12.581478118896484,
          "max": 163.17431902885437
        },
        "forks": {
          "n": 64,
          "sum": 2.0,
          "mean": 0.03125,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 2.0,
          "mean": 0.03125,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 66.0,
          "mean": 1.03125,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 125301.0,
          "mean": 1957.828125,
          "median": 1370.5,
          "p95": 4094.0,
          "min": 328.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 75.0,
          "mean": 1.171875,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 7.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 125226.0,
          "mean": 1956.65625,
          "median": 1369.5,
          "p95": 4093.0,
          "min": 327.0,
          "max": 4093.0
        },
        "widths": {
          "n": 2,
          "sum": 6.0,
          "mean": 3.0,
          "median": 3.0,
          "p95": 3.9,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 1,
          "4": 1
        },
        "truncated_samples": 13,
        "truncated_fraction": 0.203125,
        "invalid_width_samples": 0,
        "forked_samples": 2
      },
      "metrics_correct": {
        "F": {
          "n": 51,
          "sum": 74745.0,
          "mean": 1465.5882352941176,
          "median": 1133.0,
          "p95": 3829.5,
          "min": 328.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 51,
          "sum": 74820.0,
          "mean": 1467.0588235294117,
          "median": 1133.0,
          "p95": 3829.5,
          "min": 328.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 51,
          "sum": 111.0,
          "mean": 2.176470588235294,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 11.0
        },
        "T_assembled": {
          "n": 51,
          "sum": 74931.0,
          "mean": 1469.235294117647,
          "median": 1135.0,
          "p95": 3831.5,
          "min": 330.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 51,
          "sum": 74820.0,
          "mean": 1467.0588235294117,
          "median": 1133.0,
          "p95": 3829.5,
          "min": 328.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 51,
          "sum": 56.0,
          "mean": 1.0980392156862746,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 6.0
        },
        "wall_seconds": {
          "n": 51,
          "sum": 2861.8443336486816,
          "mean": 56.11459477742513,
          "median": 43.02755808830261,
          "p95": 146.96831798553467,
          "min": 12.581478118896484,
          "max": 150.963036775589
        },
        "forks": {
          "n": 51,
          "sum": 1.0,
          "mean": 0.0196078431372549,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 51,
          "sum": 1.0,
          "mean": 0.0196078431372549,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 51,
          "sum": 52.0,
          "mean": 1.0196078431372548,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 51,
          "sum": 74820.0,
          "mean": 1467.0588235294117,
          "median": 1133.0,
          "p95": 3829.5,
          "min": 328.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 51,
          "sum": 56.0,
          "mean": 1.0980392156862746,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 6.0
        },
        "decode_calls_inferred": {
          "n": 51,
          "sum": 74764.0,
          "mean": 1465.9607843137255,
          "median": 1132.0,
          "p95": 3828.5,
          "min": 327.0,
          "max": 4093.0
        },
        "widths": {
          "n": 1,
          "sum": 2.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "width_histogram": {
          "2": 1
        },
        "truncated_samples": 1,
        "truncated_fraction": 0.0196078431372549,
        "invalid_width_samples": 0,
        "forked_samples": 1
      },
      "historical_correct": 50,
      "historical_pass_at_1": 0.78125
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
    "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    },
    "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9"
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ],
  "constrained_decoding": true,
  "format_guard_version": 1,
  "format_guard_scope": "No XML after think; exact sampled width/newline; no think/EOS inside Path/Summary; no orphan controls. No semantic repair, Plan grammar or final answer enforcement."
}
```

</details>

- [work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/worker-exits.json](../artifacts/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 82,
  "pass_at_1_completed_only": 0.640625,
  "format_valid": 85,
  "format_fraction_completed_only": 0.6640625,
  "executed_fork_samples": 1,
  "unfinished_thinking": 17,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 78,
  "legacy_format_fraction_completed_only": 0.609375,
  "legacy_parallel_protocol_valid": 0,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": false,
    "fork_coverage_at_least_0_2": false,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": false,
    "invalid_width_fraction_at_most_0_05": true,
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
    "completed": 128,
    "basic_valid": 85,
    "executed_fork_samples": 1,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 82
  },
  "fork_coverage": 0.0078125,
  "valid_parallel_among_executed_forks": 0.0,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 81,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 313419.0,
      "mean": 2448.5859375,
      "median": 2159.5,
      "p95": 4094.0,
      "min": 491.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 313432.0,
      "mean": 2448.6875,
      "median": 2159.5,
      "p95": 4094.0,
      "min": 491.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 266.0,
      "mean": 2.078125,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 12.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 313698.0,
      "mean": 2450.765625,
      "median": 2161.5,
      "p95": 4096.0,
      "min": 493.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 313432.0,
      "mean": 2448.6875,
      "median": 2159.5,
      "p95": 4094.0,
      "min": 491.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 132.0,
      "mean": 1.03125,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 5.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 12290.251554965973,
      "mean": 96.01759027317166,
      "median": 85.87688601016998,
      "p95": 166.88235712051392,
      "min": 18.231022834777832,
      "max": 170.25111269950867
    },
    "forks": {
      "n": 128,
      "sum": 1.0,
      "mean": 0.0078125,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 128,
      "sum": 1.0,
      "mean": 0.0078125,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 129.0,
      "mean": 1.0078125,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 313432.0,
      "mean": 2448.6875,
      "median": 2159.5,
      "p95": 4094.0,
      "min": 491.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 132.0,
      "mean": 1.03125,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 5.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 313300.0,
      "mean": 2447.65625,
      "median": 2158.5,
      "p95": 4093.0,
      "min": 490.0,
      "max": 4093.0
    },
    "widths": {
      "n": 1,
      "sum": 2.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "width_histogram": {
      "2": 1
    },
    "truncated_samples": 44,
    "truncated_fraction": 0.34375,
    "invalid_width_samples": 0,
    "forked_samples": 1
  },
  "metrics_correct": {
    "F": {
      "n": 82,
      "sum": 131606.0,
      "mean": 1604.9512195121952,
      "median": 1322.5,
      "p95": 3081.3000000000006,
      "min": 491.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 82,
      "sum": 131606.0,
      "mean": 1604.9512195121952,
      "median": 1322.5,
      "p95": 3081.3000000000006,
      "min": 491.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 82,
      "sum": 164.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 82,
      "sum": 131770.0,
      "mean": 1606.9512195121952,
      "median": 1324.5,
      "p95": 3083.3000000000006,
      "min": 493.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 82,
      "sum": 131606.0,
      "mean": 1604.9512195121952,
      "median": 1322.5,
      "p95": 3081.3000000000006,
      "min": 491.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 82,
      "sum": 82.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 82,
      "sum": 5164.263073205948,
      "mean": 62.9788179659262,
      "median": 52.41615557670593,
      "p95": 119.85076771974565,
      "min": 18.231022834777832,
      "max": 153.215176820755
    },
    "forks": {
      "n": 82,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 82,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 82,
      "sum": 82.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 82,
      "sum": 131606.0,
      "mean": 1604.9512195121952,
      "median": 1322.5,
      "p95": 3081.3000000000006,
      "min": 491.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 82,
      "sum": 82.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 82,
      "sum": 131524.0,
      "mean": 1603.9512195121952,
      "median": 1321.5,
      "p95": 3080.3000000000006,
      "min": 490.0,
      "max": 4093.0
    },
    "widths": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "width_histogram": {},
    "truncated_samples": 1,
    "truncated_fraction": 0.012195121951219513,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 81,
  "historical_pass_at_1_completed_only": 0.6328125,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 128,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 44,
      "pass_at_1": 0.6875,
      "basic_valid": 46,
      "basic_valid_fraction": 0.71875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 44,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 145566.0,
          "mean": 2274.46875,
          "median": 2097.0,
          "p95": 4094.0,
          "min": 491.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 145566.0,
          "mean": 2274.46875,
          "median": 2097.0,
          "p95": 4094.0,
          "min": 491.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 128.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 145694.0,
          "mean": 2276.46875,
          "median": 2099.0,
          "p95": 4096.0,
          "min": 493.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 145566.0,
          "mean": 2274.46875,
          "median": 2097.0,
          "p95": 4094.0,
          "min": 491.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 5721.596309900284,
          "mean": 89.39994234219193,
          "median": 82.52061212062836,
          "p95": 166.80137763023376,
          "min": 18.231022834777832,
          "max": 169.4980411529541
        },
        "forks": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 145566.0,
          "mean": 2274.46875,
          "median": 2097.0,
          "p95": 4094.0,
          "min": 491.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 145502.0,
          "mean": 2273.46875,
          "median": 2096.0,
          "p95": 4093.0,
          "min": 490.0,
          "max": 4093.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 18,
        "truncated_fraction": 0.28125,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 44,
          "sum": 67588.0,
          "mean": 1536.090909090909,
          "median": 1202.5,
          "p95": 2814.6,
          "min": 491.0,
          "max": 3089.0
        },
        "T_sampled": {
          "n": 44,
          "sum": 67588.0,
          "mean": 1536.090909090909,
          "median": 1202.5,
          "p95": 2814.6,
          "min": 491.0,
          "max": 3089.0
        },
        "T_forced": {
          "n": 44,
          "sum": 88.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 44,
          "sum": 67676.0,
          "mean": 1538.090909090909,
          "median": 1204.5,
          "p95": 2816.6,
          "min": 493.0,
          "max": 3091.0
        },
        "actual_generated_tokens": {
          "n": 44,
          "sum": 67588.0,
          "mean": 1536.090909090909,
          "median": 1202.5,
          "p95": 2814.6,
          "min": 491.0,
          "max": 3089.0
        },
        "generation_calls": {
          "n": 44,
          "sum": 44.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 44,
          "sum": 2672.5969364643097,
          "mean": 60.74083946509795,
          "median": 49.18404686450958,
          "p95": 112.8491173028946,
          "min": 18.231022834777832,
          "max": 119.96100044250488
        },
        "forks": {
          "n": 44,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 44,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 44,
          "sum": 44.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 44,
          "sum": 67588.0,
          "mean": 1536.090909090909,
          "median": 1202.5,
          "p95": 2814.6,
          "min": 491.0,
          "max": 3089.0
        },
        "prefill_calls_inferred": {
          "n": 44,
          "sum": 44.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 44,
          "sum": 67544.0,
          "mean": 1535.090909090909,
          "median": 1201.5,
          "p95": 2813.6,
          "min": 490.0,
          "max": 3088.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 44,
      "historical_pass_at_1": 0.6875
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 38,
      "pass_at_1": 0.59375,
      "basic_valid": 39,
      "basic_valid_fraction": 0.609375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 37,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 167853.0,
          "mean": 2622.703125,
          "median": 2357.0,
          "p95": 4094.0,
          "min": 545.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 167866.0,
          "mean": 2622.90625,
          "median": 2357.0,
          "p95": 4094.0,
          "min": 545.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 138.0,
          "mean": 2.15625,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 12.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 168004.0,
          "mean": 2625.0625,
          "median": 2359.0,
          "p95": 4096.0,
          "min": 547.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 167866.0,
          "mean": 2622.90625,
          "median": 2357.0,
          "p95": 4094.0,
          "min": 545.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 68.0,
          "mean": 1.0625,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 5.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 6568.655245065689,
          "mean": 102.63523820415139,
          "median": 88.51919162273407,
          "p95": 166.63175806999206,
          "min": 21.612882375717163,
          "max": 170.25111269950867
        },
        "forks": {
          "n": 64,
          "sum": 1.0,
          "mean": 0.015625,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 1.0,
          "mean": 0.015625,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 65.0,
          "mean": 1.015625,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 167866.0,
          "mean": 2622.90625,
          "median": 2357.0,
          "p95": 4094.0,
          "min": 545.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 68.0,
          "mean": 1.0625,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 5.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 167798.0,
          "mean": 2621.84375,
          "median": 2356.0,
          "p95": 4093.0,
          "min": 544.0,
          "max": 4093.0
        },
        "widths": {
          "n": 1,
          "sum": 2.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "width_histogram": {
          "2": 1
        },
        "truncated_samples": 26,
        "truncated_fraction": 0.40625,
        "invalid_width_samples": 0,
        "forked_samples": 1
      },
      "metrics_correct": {
        "F": {
          "n": 38,
          "sum": 64018.0,
          "mean": 1684.6842105263158,
          "median": 1482.0,
          "p95": 3657.9999999999995,
          "min": 545.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 38,
          "sum": 64018.0,
          "mean": 1684.6842105263158,
          "median": 1482.0,
          "p95": 3657.9999999999995,
          "min": 545.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 38,
          "sum": 76.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 38,
          "sum": 64094.0,
          "mean": 1686.6842105263158,
          "median": 1484.0,
          "p95": 3659.9999999999995,
          "min": 547.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 38,
          "sum": 64018.0,
          "mean": 1684.6842105263158,
          "median": 1482.0,
          "p95": 3657.9999999999995,
          "min": 545.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 38,
          "sum": 38.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 38,
          "sum": 2491.666136741638,
          "mean": 65.570161493201,
          "median": 57.85875105857849,
          "p95": 146.96154742240904,
          "min": 21.612882375717163,
          "max": 153.215176820755
        },
        "forks": {
          "n": 38,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 38,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 38,
          "sum": 38.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 38,
          "sum": 64018.0,
          "mean": 1684.6842105263158,
          "median": 1482.0,
          "p95": 3657.9999999999995,
          "min": 545.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 38,
          "sum": 38.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 38,
          "sum": 63980.0,
          "mean": 1683.6842105263158,
          "median": 1481.0,
          "p95": 3656.9999999999995,
          "min": 544.0,
          "max": 4093.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 1,
        "truncated_fraction": 0.02631578947368421,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 37,
      "historical_pass_at_1": 0.578125
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
    "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    },
    "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9"
  },
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ],
  "constrained_decoding": true,
  "format_guard_version": 1,
  "format_guard_scope": "No XML after think; exact sampled width/newline; no think/EOS inside Path/Summary; no orphan controls. No semantic repair, Plan grammar or final answer enforcement."
}
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/worker-exits.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/summary.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 98,
  "pass_at_1_completed_only": 0.765625,
  "format_valid": 102,
  "format_fraction_completed_only": 0.796875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 15,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 98,
  "legacy_format_fraction_completed_only": 0.765625,
  "legacy_parallel_protocol_valid": 0,
  "primary_extraction_changed_samples": 0,
  "gate_criteria": {
    "all_planned_completed": true,
    "basic_strict_format_at_least_0_8": false,
    "fork_coverage_at_least_0_2": false,
    "valid_parallel_among_executed_fork_samples_at_least_0_9": false,
    "invalid_width_fraction_at_most_0_05": true,
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
    "completed": 128,
    "basic_valid": 102,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 98
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 97,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 241811.0,
      "mean": 1889.1484375,
      "median": 1422.0,
      "p95": 4094.0,
      "min": 381.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 241811.0,
      "mean": 1889.1484375,
      "median": 1422.0,
      "p95": 4094.0,
      "min": 381.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 256.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 242067.0,
      "mean": 1891.1484375,
      "median": 1424.0,
      "p95": 4096.0,
      "min": 383.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 241811.0,
      "mean": 1889.1484375,
      "median": 1422.0,
      "p95": 4094.0,
      "min": 381.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 128.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 9290.655490159988,
      "mean": 72.58324601687491,
      "median": 52.059601068496704,
      "p95": 160.60687482357025,
      "min": 15.57576608657837,
      "max": 167.5809862613678
    },
    "forks": {
      "n": 128,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 128,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 128.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 241811.0,
      "mean": 1889.1484375,
      "median": 1422.0,
      "p95": 4094.0,
      "min": 381.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 128.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 241683.0,
      "mean": 1888.1484375,
      "median": 1421.0,
      "p95": 4093.0,
      "min": 380.0,
      "max": 4093.0
    },
    "widths": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "width_histogram": {},
    "truncated_samples": 24,
    "truncated_fraction": 0.1875,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 98,
      "sum": 127688.0,
      "mean": 1302.938775510204,
      "median": 1099.0,
      "p95": 2744.449999999999,
      "min": 381.0,
      "max": 3415.0
    },
    "T_sampled": {
      "n": 98,
      "sum": 127688.0,
      "mean": 1302.938775510204,
      "median": 1099.0,
      "p95": 2744.449999999999,
      "min": 381.0,
      "max": 3415.0
    },
    "T_forced": {
      "n": 98,
      "sum": 196.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 98,
      "sum": 127884.0,
      "mean": 1304.938775510204,
      "median": 1101.0,
      "p95": 2746.449999999999,
      "min": 383.0,
      "max": 3417.0
    },
    "actual_generated_tokens": {
      "n": 98,
      "sum": 127688.0,
      "mean": 1302.938775510204,
      "median": 1099.0,
      "p95": 2744.449999999999,
      "min": 381.0,
      "max": 3415.0
    },
    "generation_calls": {
      "n": 98,
      "sum": 98.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 98,
      "sum": 4903.547888040543,
      "mean": 50.03620293918921,
      "median": 42.417346715927124,
      "p95": 104.07829558849335,
      "min": 15.57576608657837,
      "max": 127.91356039047241
    },
    "forks": {
      "n": 98,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 98,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 98,
      "sum": 98.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 98,
      "sum": 127688.0,
      "mean": 1302.938775510204,
      "median": 1099.0,
      "p95": 2744.449999999999,
      "min": 381.0,
      "max": 3415.0
    },
    "prefill_calls_inferred": {
      "n": 98,
      "sum": 98.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 98,
      "sum": 127590.0,
      "mean": 1301.938775510204,
      "median": 1098.0,
      "p95": 2743.449999999999,
      "min": 380.0,
      "max": 3414.0
    },
    "widths": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "width_histogram": {},
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 97,
  "historical_pass_at_1_completed_only": 0.7578125,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 128,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 49,
      "pass_at_1": 0.765625,
      "basic_valid": 51,
      "basic_valid_fraction": 0.796875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 49,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 123610.0,
          "mean": 1931.40625,
          "median": 1448.0,
          "p95": 4094.0,
          "min": 381.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 123610.0,
          "mean": 1931.40625,
          "median": 1448.0,
          "p95": 4094.0,
          "min": 381.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 128.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 123738.0,
          "mean": 1933.40625,
          "median": 1450.0,
          "p95": 4096.0,
          "min": 383.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 123610.0,
          "mean": 1931.40625,
          "median": 1448.0,
          "p95": 4094.0,
          "min": 381.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 4777.2824058532715,
          "mean": 74.64503759145737,
          "median": 55.475990533828735,
          "p95": 160.89207446575165,
          "min": 15.603965520858765,
          "max": 163.9772515296936
        },
        "forks": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 123610.0,
          "mean": 1931.40625,
          "median": 1448.0,
          "p95": 4094.0,
          "min": 381.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 123546.0,
          "mean": 1930.40625,
          "median": 1447.0,
          "p95": 4093.0,
          "min": 380.0,
          "max": 4093.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 13,
        "truncated_fraction": 0.203125,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 49,
          "sum": 64878.0,
          "mean": 1324.0408163265306,
          "median": 1151.0,
          "p95": 2784.999999999999,
          "min": 381.0,
          "max": 3385.0
        },
        "T_sampled": {
          "n": 49,
          "sum": 64878.0,
          "mean": 1324.0408163265306,
          "median": 1151.0,
          "p95": 2784.999999999999,
          "min": 381.0,
          "max": 3385.0
        },
        "T_forced": {
          "n": 49,
          "sum": 98.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 49,
          "sum": 64976.0,
          "mean": 1326.0408163265306,
          "median": 1153.0,
          "p95": 2786.999999999999,
          "min": 383.0,
          "max": 3387.0
        },
        "actual_generated_tokens": {
          "n": 49,
          "sum": 64878.0,
          "mean": 1324.0408163265306,
          "median": 1151.0,
          "p95": 2784.999999999999,
          "min": 381.0,
          "max": 3385.0
        },
        "generation_calls": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 49,
          "sum": 2507.3851425647736,
          "mean": 51.171125358464764,
          "median": 47.27093768119812,
          "p95": 104.27984642982483,
          "min": 15.603965520858765,
          "max": 127.91356039047241
        },
        "forks": {
          "n": 49,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 49,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 49,
          "sum": 64878.0,
          "mean": 1324.0408163265306,
          "median": 1151.0,
          "p95": 2784.999999999999,
          "min": 381.0,
          "max": 3385.0
        },
        "prefill_calls_inferred": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 49,
          "sum": 64829.0,
          "mean": 1323.0408163265306,
          "median": 1150.0,
          "p95": 2783.999999999999,
          "min": 380.0,
          "max": 3384.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 49,
      "historical_pass_at_1": 0.765625
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 49,
      "pass_at_1": 0.765625,
      "basic_valid": 51,
      "basic_valid_fraction": 0.796875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 48,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 118201.0,
          "mean": 1846.890625,
          "median": 1386.5,
          "p95": 4094.0,
          "min": 422.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 118201.0,
          "mean": 1846.890625,
          "median": 1386.5,
          "p95": 4094.0,
          "min": 422.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 128.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 118329.0,
          "mean": 1848.890625,
          "median": 1388.5,
          "p95": 4096.0,
          "min": 424.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 118201.0,
          "mean": 1846.890625,
          "median": 1386.5,
          "p95": 4094.0,
          "min": 422.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 4513.373084306717,
          "mean": 70.52145444229245,
          "median": 51.78242385387421,
          "p95": 158.138856112957,
          "min": 15.57576608657837,
          "max": 167.5809862613678
        },
        "forks": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 64,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 118201.0,
          "mean": 1846.890625,
          "median": 1386.5,
          "p95": 4094.0,
          "min": 422.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 64.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 118137.0,
          "mean": 1845.890625,
          "median": 1385.5,
          "p95": 4093.0,
          "min": 421.0,
          "max": 4093.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 11,
        "truncated_fraction": 0.171875,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 49,
          "sum": 62810.0,
          "mean": 1281.8367346938776,
          "median": 968.0,
          "p95": 2705.6,
          "min": 422.0,
          "max": 3415.0
        },
        "T_sampled": {
          "n": 49,
          "sum": 62810.0,
          "mean": 1281.8367346938776,
          "median": 968.0,
          "p95": 2705.6,
          "min": 422.0,
          "max": 3415.0
        },
        "T_forced": {
          "n": 49,
          "sum": 98.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 49,
          "sum": 62908.0,
          "mean": 1283.8367346938776,
          "median": 970.0,
          "p95": 2707.6,
          "min": 424.0,
          "max": 3417.0
        },
        "actual_generated_tokens": {
          "n": 49,
          "sum": 62810.0,
          "mean": 1281.8367346938776,
          "median": 968.0,
          "p95": 2705.6,
          "min": 422.0,
          "max": 3415.0
        },
        "generation_calls": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 49,
          "sum": 2396.162745475769,
          "mean": 48.901280519913655,
          "median": 38.24521827697754,
          "p95": 101.0001625061035,
          "min": 15.57576608657837,
          "max": 126.22401690483093
        },
        "forks": {
          "n": 49,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 49,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 49,
          "sum": 62810.0,
          "mean": 1281.8367346938776,
          "median": 968.0,
          "p95": 2705.6,
          "min": 422.0,
          "max": 3415.0
        },
        "prefill_calls_inferred": {
          "n": 49,
          "sum": 49.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 49,
          "sum": 62761.0,
          "mean": 1280.8367346938776,
          "median": 967.0,
          "p95": 2704.6,
          "min": 421.0,
          "max": 3414.0
        },
        "widths": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "width_histogram": {},
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 48,
      "historical_pass_at_1": 0.75
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
  "system_file": "${PROJECT_ROOT}/work/experiments/format-diagnosis-20261010/parallel-inside-think-example-system.txt",
  "provenance": {
    "evaluator_sha256": "c531b5990ccf2989a1a912661ef2d91d506164182160121afdda05db38278c72",
    "system_sha256": "2e0a1836fccd2fd035e04897b5cd2b56795b0ad0cca87028363d5305bb72f8db",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "db46dd9c6a459a1740feadba06e8721bbf72a995399326450699cbfdeb2af7fd",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "f42310063082cc6153c092c068623a86430c5b04c8428907174f19cd4d6edf4f",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    },
    "format_guard_sha256": "cf9219dc7745694357c4b0037e08d805674da2f4571c2ec60ba95634bf8f19e9"
  },
  "system_sha256": "2e0a1836fccd2fd035e04897b5cd2b56795b0ad0cca87028363d5305bb72f8db",
  "suite": "128",
  "curriculum_selection_allowed": false,
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "selection_allowed": false,
  "native_eos_ids": [
    151643,
    151645
  ],
  "constrained_decoding": true,
  "format_guard_version": 1,
  "format_guard_scope": "No XML after think; exact sampled width/newline; no think/EOS inside Path/Summary; no orphan controls. No semantic repair, Plan grammar or final answer enforcement."
}
```

</details>

- [work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/worker-exits.json](../artifacts/work/experiments/format-loss-20261010/evaluations/weighted-format-fewshot-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
[
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
]
```

</details>

- [work/experiments/format-loss-20261010/failed-before-model-load-1/sft-status.json](../artifacts/work/experiments/format-loss-20261010/failed-before-model-load-1/sft-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "at": "2026-10-10T09:55:37.801785+00:00",
  "only_six_rows": true,
  "epochs": 3,
  "target_steps": 129,
  "base_lr": 0.0005,
  "constrained_eval_planned": 128,
  "active": "smoke",
  "argv": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/format-loss-20261010/run_train.sh",
    "smoke"
  ],
  "active_pid": null,
  "error": "AssertionError(('smoke', 1))"
}
```

</details>

- [work/experiments/format-loss-20261010/guard128-status.json](../artifacts/work/experiments/format-loss-20261010/guard128-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T10:50:13.967326+00:00",
  "constrained_decoding": true,
  "summary": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128/summary.json",
  "metrics": {
    "planned": 128,
    "completed": 128,
    "correct": 104,
    "format_valid": 103,
    "parallel_protocol_valid": 1,
    "executed_fork_samples": 2
  }
}
```

</details>

- [work/experiments/format-loss-20261010/runs/production/metrics.jsonl](../artifacts/work/experiments/format-loss-20261010/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/format-loss-20261010/runs/production/result.json](../artifacts/work/experiments/format-loss-20261010/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T10:13:16.334295+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 816.6539832185954,
  "final": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final"
}
```

</details>

- [work/experiments/format-loss-20261010/runs/production/status.json](../artifacts/work/experiments/format-loss-20261010/runs/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T10:13:16.334295+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 816.6539832185954,
  "final": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final"
}
```

</details>

- [work/experiments/format-loss-20261010/runs/smoke/metrics.jsonl](../artifacts/work/experiments/format-loss-20261010/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/format-loss-20261010/runs/smoke/result.json](../artifacts/work/experiments/format-loss-20261010/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:57:58.619319+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 43.2772106891498,
  "final": null
}
```

</details>

- [work/experiments/format-loss-20261010/runs/smoke/status.json](../artifacts/work/experiments/format-loss-20261010/runs/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:57:58.619319+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 43.2772106891498,
  "final": null
}
```

</details>

- [work/experiments/format-loss-20261010/sft-status.json](../artifacts/work/experiments/format-loss-20261010/sft-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T10:42:50.711190+00:00",
  "only_six_rows": true,
  "epochs": 3,
  "target_steps": 129,
  "base_lr": 0.0005,
  "constrained_eval_planned": 128,
  "active": null,
  "argv": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final",
    "--mode",
    "structured",
    "--name",
    "weighted-format-constrained-128",
    "--suite",
    "128",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt"
  ],
  "active_pid": null,
  "approval_request": {
    "artifacts_sha256": {
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/result.json": "110849340a89fe179db8b3490016bda2230f61075fcd17f2f057c769abe8b573",
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/initialization-proof.json": "6b1ee8ffc2833fd1ab086943e7ea11294cda1f2e10152db0fe3141f886cd02d0",
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/metrics.jsonl": "99dca7d6fa57e99b7a0a299b5745688c9215de3b711db66c23e1137b5129245c"
    },
    "ready_sha256": "1e153d40c36fd89c47ea5b42d23abfbfb76d6be4d2460637ee9c960f57d68176"
  },
  "finished_at": "2026-10-10T10:42:50.711151+00:00",
  "training": {
    "state": "complete",
    "at": "2026-10-10T10:13:16.334295+00:00",
    "steps": 129,
    "epochs": 3,
    "trainable_parameters": 15360,
    "only_six_rows_updated": true,
    "all_other_parameters_frozen_version_checks_passed": true,
    "elapsed_seconds": 816.6539832185954,
    "final": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/production/final"
  },
  "evaluation_summary": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/evaluations/weighted-format-constrained-128/summary.json"
}
```

</details>

- [work/experiments/format-loss-20261010/sft-status.json](../history/local_saved/1b2a4486913f/work/experiments/format-loss-20261010/sft-status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "at": "2026-10-10T09:59:19.376868+00:00",
  "only_six_rows": true,
  "epochs": 3,
  "target_steps": 129,
  "base_lr": 0.0005,
  "constrained_eval_planned": 128,
  "active": "production",
  "argv": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/format-loss-20261010/run_train.sh",
    "production"
  ],
  "active_pid": 1266265,
  "approval_request": {
    "artifacts_sha256": {
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/result.json": "110849340a89fe179db8b3490016bda2230f61075fcd17f2f057c769abe8b573",
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/initialization-proof.json": "6b1ee8ffc2833fd1ab086943e7ea11294cda1f2e10152db0fe3141f886cd02d0",
      "${PROJECT_ROOT}/work/experiments/format-loss-20261010/runs/smoke/metrics.jsonl": "99dca7d6fa57e99b7a0a299b5745688c9215de3b711db66c23e1137b5129245c"
    },
    "ready_sha256": "1e153d40c36fd89c47ea5b42d23abfbfb76d6be4d2460637ee9c960f57d68176"
  }
}
```

</details>

- [work/experiments/format-loss-20261010/guard128-status.json](../history/local_saved/2ce827912fbc/work/experiments/format-loss-20261010/guard128-status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "queued",
  "at": "2026-10-10T09:44:12.968674+00:00",
  "constrained_decoding": true,
  "planned": 128,
  "queue_file": "${PROJECT_ROOT}/work/experiments/night-20261010/cloud-continued/tmp3/queue/110-baseline-format-guard-128.json",
  "job_id": "RUN_7d061208cd",
  "awaiting": "Existing tmp3 native128 and structured128 evaluations complete; no interruption",
  "GPU_launched": false,
  "source_sha256": "c53222772c67ca2da26ce685fce5116c4c051024177d654abee2c92fcb898821",
  "ready_sha256": "b464eed918d2ac4b5a92d3839e16e840063833f94226443c7a53a72826d50a10"
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/format-loss-20261010/evaluations/run_eval.sh](../artifacts/work/experiments/format-loss-20261010/evaluations/run_eval.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/format-loss-20261010/train.py](../artifacts/work/experiments/format-loss-20261010/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
