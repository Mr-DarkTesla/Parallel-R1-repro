# work/experiments/instruct-token-warmup-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/instruct-token-warmup-20261010/data-audit.json](../artifacts/work/experiments/instruct-token-warmup-20261010/data-audit.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "source_sha256": {
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/train.jsonl": "7379ecfc7053771313df1bc63c6324a3f3f8ee72bdfc818015bdc35ae600b24a",
    "${PROJECT_ROOT}/exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/val.jsonl": "d5a868ef8fc42a50f21a7e9cb657da1a894b882ddeabb256b6f1eeb6112a23c5"
  },
  "splits": {
    "train": {
      "rows": 2700,
      "unique_questions": 2700,
      "min_length": 860,
      "max_length": 4050,
      "mean_length": 2112.3403703703702,
      "p50_length": 2114,
      "p95_length": 2932,
      "width_histogram": {
        "4": 1335,
        "3": 858,
        "2": 778,
        "5": 147,
        "6": 17
      },
      "total_supervised_targets": 2161963,
      "boundary_telemetry": [],
      "all_direct_and_indirect_isolation_invariants": true,
      "no_truncation": true
    },
    "val": {
      "rows": 300,
      "unique_questions": 300,
      "min_length": 832,
      "max_length": 3746,
      "mean_length": 2127.4766666666665,
      "p50_length": 2115,
      "p95_length": 2911,
      "width_histogram": {
        "4": 158,
        "3": 85,
        "2": 87,
        "5": 19,
        "6": 2
      },
      "total_supervised_targets": 237062,
      "boundary_telemetry": [],
      "all_direct_and_indirect_isolation_invariants": true,
      "no_truncation": true
    }
  },
  "tokenizer_sha256": {
    "chat_template.jinja": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8",
    "tokenizer_config.json": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba",
    "special_tokens_map.json": "caca9dbcb841cc4bf3e5429fb0022a3056fe1b3dcac75797c067b0e109c2bb8a",
    "added_tokens.json": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
    "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
    "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "tokenizer.json": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
  },
  "data_module_sha256": "7a9415bc70d8c237452a47dadb0c1b8ca5e9bbd8f4d877f3c1c599cc47315919",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "torch_GPU_launches": false,
  "response_transformations": "Only separate native initialthink into prompt and append native im_end; all source assistant bytes preserved; sibling whitespace retained on preceding path.",
  "train_val_question_overlap": 0
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-24.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 24,
  "suite": "24",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-24.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 24,
  "suite": "24",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-24.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 24,
  "suite": "24",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-24.jsonl",
  "response_cap": 4096,
  "path_cap": 2048,
  "planned": 24,
  "suite": "24",
  "native_eos_ids": [
    151643,
    151645
  ],
  "diagnostic_only": true,
  "checkpoint_selection_allowed": false,
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/math500-predeclared-plan.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/math500-predeclared-plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "predeclared_at": "2026-10-10T08:44:12.607514+00:00",
  "CPU_only": true,
  "GPU_launches": false,
  "suite": "500",
  "fixed_questions_sha256": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
  "question_source": "${PROJECT_ROOT}/work/experiments/night-20261010/rl-eval/questions-math500.jsonl",
  "selection_allowed": false,
  "checkpoint_selection_allowed": false,
  "curriculum_selection_allowed": false,
  "all_learning_rate_arms_reported_no_test_based_winner_selection": true,
  "original_control_runtime_prompt_differs_from_structured": true,
  "generation": {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20,
    "response_cap": 4096,
    "path_cap": 2048,
    "seed_base": 42,
    "8workers": true
  },
  "requires_before_root_launch": [
    "completed production+CPU398tensor audit for each trained arm",
    "actual24 runtime audit+ROOTapproval before128/500",
    "ROOT explicit dispatch only; not integrated into variant training pipeline"
  ],
  "models": [
    {
      "label": "original-native",
      "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
      "mode": "native",
      "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
      "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
        "--mode",
        "native",
        "--suite",
        "500",
        "--name",
        "math500-original-native"
      ]
    },
    {
      "label": "meaninit-structured",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
      "mode": "structured",
      "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
      "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--mode",
        "structured",
        "--suite",
        "500",
        "--name",
        "math500-meaninit-structured"
      ]
    },
    {
      "label": "lr5e-4-structured",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
      "mode": "structured",
      "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
      "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--mode",
        "structured",
        "--suite",
        "500",
        "--name",
        "math500-lr5e-4-structured"
      ]
    },
    {
      "label": "lr1e-3-structured",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
      "mode": "structured",
      "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
      "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--mode",
        "structured",
        "--suite",
        "500",
        "--name",
        "math500-lr1e-3-structured"
      ]
    },
    {
      "label": "lr2e-4-structured",
      "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
      "mode": "structured",
      "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
      "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--mode",
        "structured",
        "--suite",
        "500",
        "--name",
        "math500-lr2e-4-structured"
      ]
    }
  ],
  "sha256": {
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/evaluate.py": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/evaluate_math500.py": "ee768a765cfe13bfb058975b3afa0e83881275cfd07d61e3f6a324f562983e74",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh": "c3f9a68bda63f85f0c15206d12141f39f5c6d711e580cb0cb82371b23d7204a0",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_math500.sh": "02cef88e28debdd8ed439aec290b99f38db73d5f54ad6dfd8d5aa049de21dec9",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-500.jsonl": "ddde77ef9dbf78d911a6bc2db2040332bbd33e097ae95a4afb81dd192963d39e",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/ready.json": "a4dd5577a77c9f914770dc9b0cb40beed1dfe0beeef31432b52442741d5824e8"
  },
  "exact_AST_reverse_to_baseline": true,
  "only_evaluator_change": "suite choices add500; fixed questions500 maps existing same questions-{suite} mechanism; no generation/scorer/runtime change"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
  "mode": "native",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/trained-structured-128/manifest.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/trained-structured-128/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
  "mode": "structured",
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "fixed_questions": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/questions-128.jsonl",
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
  "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
  "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
  "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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

- [work/experiments/instruct-token-warmup-20261010/math-system.txt](../artifacts/work/experiments/instruct-token-warmup-20261010/math-system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/plan.json](../artifacts/work/experiments/instruct-token-warmup-20261010/plan.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "created_at": "2026-10-10T07:46:48.912719+00:00",
  "authorization": "User explicitly requests Qwen3-4B instruct six-tag mean-subpiece ONLY-token warmup on newfiltered3000 with Unseen; supersedes oldno-newtraining ONLYthisSirius experiment.",
  "model": "work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
  "data": "exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think",
  "split": {
    "train": 2700,
    "val": 300
  },
  "trainable": "only6tiedembeddingrows;15360parameters;alloldrowsandtransformerfrozen",
  "init": "mean_original_tokenizer_tag_subpiece_embeddings_FP32",
  "epochs": 3,
  "global_batch": 64,
  "micro_batch_per_gpu": 1,
  "learning_rate": 0.0005,
  "weight_decay": 0,
  "warmup_steps": 5,
  "seed": 20261010,
  "max_length": 8192,
  "gpus": "Sirius0..7 only; existingnightCloudcleanup09UTC unchanged",
  "safety": [
    "CPUdata and independentcodeaudit beforeactual8GPU2stepsmoke",
    "finite2steps/updateonly6rows/UnseenCPU+GPUisolation gate beforeproduction",
    "originalmodel/tokenizer/data frozen;allwritesnewfolder",
    "noMATH500selection;validationgenerationbeforeafter",
    "NO LoRA/fullweight/RL updates"
  ],
  "status": "production_running_actual_steps_verified",
  "production_controller_pid": 1249140,
  "actual_smoke_passed": true,
  "smoke_weights_reused": false,
  "root_launch_proof": "root-production-launch-proof.json",
  "approx_training_eta_UTC": "08:22–08:27",
  "full_evaluation_follows_training": true
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/system.txt](../artifacts/work/experiments/instruct-token-warmup-20261010/system.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Метрики и полнота результатов

- [work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/smoke-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/smoke-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "smoke",
  "started_at": "2026-10-10T07:54:13.135103+00:00",
  "command": [
    "${PROJECT_ROOT}/.venv/bin/python",
    "-m",
    "torch.distributed.run",
    "--standalone",
    "--nnodes=1",
    "--nproc_per_node=8",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/train.py",
    "--stage",
    "smoke"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/smoke.log",
  "owned_process_group": 1246663,
  "heartbeat_at": "2026-10-10T07:54:43.149885+00:00",
  "returncode": 1,
  "finished_at": "2026-10-10T07:54:53.153384+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "at": "2026-10-10T07:54:53.156649+00:00",
  "error": "AssertionError(('smoke', 1))"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 106,
  "pass_at_1_completed_only": 0.828125,
  "format_valid": 103,
  "format_fraction_completed_only": 0.8046875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 18,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 85,
  "legacy_format_fraction_completed_only": 0.6640625,
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
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 106
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 100,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 264254.0,
      "mean": 2064.484375,
      "median": 1815.0,
      "p95": 4094.0,
      "min": 291.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 264254.0,
      "mean": 2064.484375,
      "median": 1815.0,
      "p95": 4094.0,
      "min": 291.0,
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
      "sum": 264510.0,
      "mean": 2066.484375,
      "median": 1817.0,
      "p95": 4096.0,
      "min": 293.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 264254.0,
      "mean": 2064.484375,
      "median": 1815.0,
      "p95": 4094.0,
      "min": 291.0,
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
      "sum": 10105.542692899704,
      "mean": 78.94955228827894,
      "median": 68.33069813251495,
      "p95": 158.24643697738648,
      "min": 10.876765966415405,
      "max": 162.50066232681274
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
      "sum": 264254.0,
      "mean": 2064.484375,
      "median": 1815.0,
      "p95": 4094.0,
      "min": 291.0,
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
      "sum": 264126.0,
      "mean": 2063.484375,
      "median": 1814.0,
      "p95": 4093.0,
      "min": 290.0,
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
      "n": 106,
      "sum": 180696.0,
      "mean": 1704.6792452830189,
      "median": 1413.0,
      "p95": 3984.25,
      "min": 291.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 106,
      "sum": 180696.0,
      "mean": 1704.6792452830189,
      "median": 1413.0,
      "p95": 3984.25,
      "min": 291.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 106,
      "sum": 212.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 106,
      "sum": 180908.0,
      "mean": 1706.6792452830189,
      "median": 1415.0,
      "p95": 3986.25,
      "min": 293.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 106,
      "sum": 180696.0,
      "mean": 1704.6792452830189,
      "median": 1413.0,
      "p95": 3984.25,
      "min": 291.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 106,
      "sum": 106.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 106,
      "sum": 6907.115405082703,
      "mean": 65.16146608568587,
      "median": 55.75517475605011,
      "p95": 151.17279291152954,
      "min": 10.876765966415405,
      "max": 161.97542548179626
    },
    "forks": {
      "n": 106,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 106,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 106,
      "sum": 106.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 106,
      "sum": 180696.0,
      "mean": 1704.6792452830189,
      "median": 1413.0,
      "p95": 3984.25,
      "min": 291.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 106,
      "sum": 106.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 106,
      "sum": 180590.0,
      "mean": 1703.6792452830189,
      "median": 1412.0,
      "p95": 3983.25,
      "min": 290.0,
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
    "truncated_samples": 5,
    "truncated_fraction": 0.04716981132075472,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 102,
  "historical_pass_at_1_completed_only": 0.796875,
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
      "correct": 54,
      "pass_at_1": 0.84375,
      "basic_valid": 56,
      "basic_valid_fraction": 0.875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 54,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 128137.0,
          "mean": 2002.140625,
          "median": 1701.5,
          "p95": 4094.0,
          "min": 450.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 128137.0,
          "mean": 2002.140625,
          "median": 1701.5,
          "p95": 4094.0,
          "min": 450.0,
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
          "sum": 128265.0,
          "mean": 2004.140625,
          "median": 1703.5,
          "p95": 4096.0,
          "min": 452.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 128137.0,
          "mean": 2002.140625,
          "median": 1701.5,
          "p95": 4094.0,
          "min": 450.0,
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
          "sum": 4924.50187253952,
          "mean": 76.94534175843,
          "median": 65.33642423152924,
          "p95": 159.08066147565842,
          "min": 17.588464975357056,
          "max": 162.09074449539185
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
          "sum": 128137.0,
          "mean": 2002.140625,
          "median": 1701.5,
          "p95": 4094.0,
          "min": 450.0,
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
          "sum": 128073.0,
          "mean": 2001.140625,
          "median": 1700.5,
          "p95": 4093.0,
          "min": 449.0,
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
        "truncated_samples": 9,
        "truncated_fraction": 0.140625,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 54,
          "sum": 92427.0,
          "mean": 1711.611111111111,
          "median": 1514.5,
          "p95": 3544.349999999997,
          "min": 450.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 54,
          "sum": 92427.0,
          "mean": 1711.611111111111,
          "median": 1514.5,
          "p95": 3544.349999999997,
          "min": 450.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 54,
          "sum": 108.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 54,
          "sum": 92535.0,
          "mean": 1713.611111111111,
          "median": 1516.5,
          "p95": 3546.349999999997,
          "min": 452.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 54,
          "sum": 92427.0,
          "mean": 1711.611111111111,
          "median": 1514.5,
          "p95": 3544.349999999997,
          "min": 450.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 54,
          "sum": 54.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 54,
          "sum": 3553.0777299404144,
          "mean": 65.7977357396373,
          "median": 58.53240990638733,
          "p95": 140.9235657930373,
          "min": 17.588464975357056,
          "max": 161.97542548179626
        },
        "forks": {
          "n": 54,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 54,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 54,
          "sum": 54.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 54,
          "sum": 92427.0,
          "mean": 1711.611111111111,
          "median": 1514.5,
          "p95": 3544.349999999997,
          "min": 450.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 54,
          "sum": 54.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 54,
          "sum": 92373.0,
          "mean": 1710.611111111111,
          "median": 1513.5,
          "p95": 3543.349999999997,
          "min": 449.0,
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
        "truncated_fraction": 0.018518518518518517,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 54,
      "historical_pass_at_1": 0.84375
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 52,
      "pass_at_1": 0.8125,
      "basic_valid": 47,
      "basic_valid_fraction": 0.734375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 136117.0,
          "mean": 2126.828125,
          "median": 1899.0,
          "p95": 4094.0,
          "min": 291.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 136117.0,
          "mean": 2126.828125,
          "median": 1899.0,
          "p95": 4094.0,
          "min": 291.0,
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
          "sum": 136245.0,
          "mean": 2128.828125,
          "median": 1901.0,
          "p95": 4096.0,
          "min": 293.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 136117.0,
          "mean": 2126.828125,
          "median": 1899.0,
          "p95": 4094.0,
          "min": 291.0,
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
          "sum": 5181.040820360184,
          "mean": 80.95376281812787,
          "median": 72.0155565738678,
          "p95": 157.8868256688118,
          "min": 10.876765966415405,
          "max": 162.50066232681274
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
          "sum": 136117.0,
          "mean": 2126.828125,
          "median": 1899.0,
          "p95": 4094.0,
          "min": 291.0,
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
          "sum": 136053.0,
          "mean": 2125.828125,
          "median": 1898.0,
          "p95": 4093.0,
          "min": 290.0,
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
        "truncated_samples": 15,
        "truncated_fraction": 0.234375,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 52,
          "sum": 88269.0,
          "mean": 1697.4807692307693,
          "median": 1231.0,
          "p95": 4094.0,
          "min": 291.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 52,
          "sum": 88269.0,
          "mean": 1697.4807692307693,
          "median": 1231.0,
          "p95": 4094.0,
          "min": 291.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 52,
          "sum": 104.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 52,
          "sum": 88373.0,
          "mean": 1699.4807692307693,
          "median": 1233.0,
          "p95": 4096.0,
          "min": 293.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 52,
          "sum": 88269.0,
          "mean": 1697.4807692307693,
          "median": 1231.0,
          "p95": 4094.0,
          "min": 291.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 52,
          "sum": 52.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 52,
          "sum": 3354.037675142288,
          "mean": 64.50072452196709,
          "median": 45.53436636924744,
          "p95": 151.39224545955656,
          "min": 10.876765966415405,
          "max": 157.88806223869324
        },
        "forks": {
          "n": 52,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 52,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 52,
          "sum": 52.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 52,
          "sum": 88269.0,
          "mean": 1697.4807692307693,
          "median": 1231.0,
          "p95": 4094.0,
          "min": 291.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 52,
          "sum": 52.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 52,
          "sum": 88217.0,
          "mean": 1696.4807692307693,
          "median": 1230.0,
          "p95": 4093.0,
          "min": 290.0,
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
        "truncated_samples": 4,
        "truncated_fraction": 0.07692307692307693,
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/initial-structured-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 98,
  "pass_at_1_completed_only": 0.765625,
  "format_valid": 55,
  "format_fraction_completed_only": 0.4296875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 25,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 7,
  "legacy_format_fraction_completed_only": 0.0546875,
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
    "basic_valid": 55,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 98
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 53,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 357577.0,
      "mean": 2793.5703125,
      "median": 2755.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 8309.062408447266,
      "mean": 64.91455006599426,
      "median": 63.99682855606079,
      "p95": 96.44358860254287,
      "min": 11.262817859649658,
      "max": 97.842360496521
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 33,
    "truncated_fraction": 0.2578125,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 237783.0,
      "mean": 2426.3571428571427,
      "median": 2287.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 5541.742632389069,
      "mean": 56.54839420805172,
      "median": 53.92203164100647,
      "p95": 93.84375003576278,
      "min": 11.262817859649658,
      "max": 97.42130255699158
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 6,
    "truncated_fraction": 0.061224489795918366,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 92,
  "historical_pass_at_1_completed_only": 0.71875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 53,
      "pass_at_1": 0.828125,
      "basic_valid": 48,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 165383.0,
          "mean": 2584.109375,
          "median": 2484.0,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 3870.1240785121918,
          "mean": 60.470688726752996,
          "median": 57.2359139919281,
          "p95": 95.86901619434357,
          "min": 11.262817859649658,
          "max": 97.842360496521
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 122831.0,
          "mean": 2317.566037735849,
          "median": 2289.0,
          "p95": 3829.3999999999996,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 2878.6099936962128,
          "mean": 54.31339610747571,
          "median": 54.06875681877136,
          "p95": 90.72830996513366,
          "min": 11.262817859649658,
          "max": 93.69397974014282
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_fraction": 0.018867924528301886,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 52,
      "historical_pass_at_1": 0.8125
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 45,
      "pass_at_1": 0.703125,
      "basic_valid": 7,
      "basic_valid_fraction": 0.109375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 7,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 192194.0,
          "mean": 3003.03125,
          "median": 3329.5,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 4438.938329935074,
          "mean": 69.35841140523553,
          "median": 76.58371460437775,
          "p95": 96.64395034313202,
          "min": 28.71153163909912,
          "max": 97.42130255699158
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 23,
        "truncated_fraction": 0.359375,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 45,
          "sum": 90.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 45,
          "sum": 114952.0,
          "mean": 2554.488888888889,
          "median": 2226.0,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 45,
          "sum": 2663.132638692856,
          "mean": 59.18072530428569,
          "median": 53.31890535354614,
          "p95": 95.88220701217651,
          "min": 28.71153163909912,
          "max": 97.42130255699158
        },
        "forks": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 5,
        "truncated_fraction": 0.1111111111111111,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 40,
      "historical_pass_at_1": 0.625
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 24,
  "completed": 24,
  "missing": 0,
  "correct": 18,
  "pass_at_1_completed_only": 0.75,
  "format_valid": 13,
  "format_fraction_completed_only": 0.5416666666666666,
  "executed_fork_samples": 0,
  "unfinished_thinking": 4,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 24,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 1,
  "legacy_format_fraction_completed_only": 0.041666666666666664,
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
    "completed": 24,
    "basic_valid": 13,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 18
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 13,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 24,
      "sum": 48.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 24,
      "sum": 63330.0,
      "mean": 2638.75,
      "median": 2795.5,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 24,
      "sum": 1447.9214973449707,
      "mean": 60.33006238937378,
      "median": 65.06705737113953,
      "p95": 94.03679386377334,
      "min": 11.417489290237427,
      "max": 95.7468273639679
    },
    "forks": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 5,
    "truncated_fraction": 0.20833333333333334,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "T_sampled": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "T_forced": {
      "n": 18,
      "sum": 36.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 18,
      "sum": 39619.0,
      "mean": 2201.0555555555557,
      "median": 1760.0,
      "p95": 3799.1499999999996,
      "min": 487.0,
      "max": 3902.0
    },
    "actual_generated_tokens": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "generation_calls": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 18,
      "sum": 912.5134189128876,
      "mean": 50.695189939604866,
      "median": 39.89489018917084,
      "p95": 89.33311570882798,
      "min": 11.417489290237427,
      "max": 89.58707118034363
    },
    "forks": {
      "n": 18,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 18,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
  "historical_correct": 18,
  "historical_pass_at_1_completed_only": 0.75,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 12,
      "completed": 12,
      "correct": 9,
      "pass_at_1": 0.75,
      "basic_valid": 8,
      "basic_valid_fraction": 0.6666666666666666,
      "parallel_valid": 0,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 8,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 34111.0,
          "mean": 2842.5833333333335,
          "median": 3231.5,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 790.0861840248108,
          "mean": 65.8405153354009,
          "median": 75.52647662162781,
          "p95": 95.0505464911461,
          "min": 11.417489290237427,
          "max": 95.7468273639679
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 3,
        "truncated_fraction": 0.25,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "T_sampled": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "T_forced": {
          "n": 9,
          "sum": 18.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 9,
          "sum": 21823.0,
          "mean": 2424.777777777778,
          "median": 2761.0,
          "p95": 3853.6,
          "min": 487.0,
          "max": 3902.0
        },
        "actual_generated_tokens": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "generation_calls": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 9,
          "sum": 508.4642598628998,
          "mean": 56.49602887365553,
          "median": 64.81307911872864,
          "p95": 89.46756272315979,
          "min": 11.417489290237427,
          "max": 89.58707118034363
        },
        "forks": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
      "historical_correct": 9,
      "historical_pass_at_1": 0.75
    },
    "math": {
      "planned": 12,
      "completed": 12,
      "correct": 9,
      "pass_at_1": 0.75,
      "basic_valid": 5,
      "basic_valid_fraction": 0.4166666666666667,
      "parallel_valid": 0,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 5,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 29219.0,
          "mean": 2434.9166666666665,
          "median": 1760.0,
          "p95": 4096.0,
          "min": 1268.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 657.8353133201599,
          "mean": 54.81960944334666,
          "median": 39.89489018917084,
          "p95": 90.63378480672836,
          "min": 29.584301471710205,
          "max": 91.52040696144104
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 2,
        "truncated_fraction": 0.16666666666666666,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "T_sampled": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "T_forced": {
          "n": 9,
          "sum": 18.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 9,
          "sum": 17796.0,
          "mean": 1977.3333333333333,
          "median": 1738.0,
          "p95": 3247.0,
          "min": 1268.0,
          "max": 3249.0
        },
        "actual_generated_tokens": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "generation_calls": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 9,
          "sum": 404.0491590499878,
          "mean": 44.8943510055542,
          "median": 39.545300006866455,
          "p95": 72.15226783752442,
          "min": 29.584301471710205,
          "max": 72.2122974395752
        },
        "forks": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
      "historical_correct": 9,
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "24",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-native-24/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 90,
  "pass_at_1_completed_only": 0.703125,
  "format_valid": 90,
  "format_fraction_completed_only": 0.703125,
  "executed_fork_samples": 5,
  "unfinished_thinking": 17,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 104,
  "parallel_execution_mismatch_samples": 23,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 91,
  "legacy_format_fraction_completed_only": 0.7109375,
  "legacy_parallel_protocol_valid": 1,
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
    "completed": 128,
    "basic_valid": 90,
    "executed_fork_samples": 5,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 23,
    "correct": 90
  },
  "fork_coverage": 0.0390625,
  "valid_parallel_among_executed_forks": 0.0,
  "invalid_width_fraction": 0.1796875,
  "correct_and_basic_valid": 85,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 180129.0,
      "mean": 1407.2578125,
      "median": 946.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 182426.0,
      "mean": 1425.203125,
      "median": 946.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 128,
      "sum": 334.0,
      "mean": 2.609375,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 27.0
    },
    "T_assembled": {
      "n": 128,
      "sum": 182760.0,
      "mean": 1427.8125,
      "median": 948.5,
      "p95": 4096.0,
      "min": 105.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 182426.0,
      "mean": 1425.203125,
      "median": 946.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 185.0,
      "mean": 1.4453125,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 11.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 6774.089711904526,
      "mean": 52.92257587425411,
      "median": 35.54568946361542,
      "p95": 152.82640157938002,
      "min": 3.4975600242614746,
      "max": 156.2981312274933
    },
    "forks": {
      "n": 128,
      "sum": 5.0,
      "mean": 0.0390625,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 128,
      "sum": 5.0,
      "mean": 0.0390625,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 128,
      "sum": 133.0,
      "mean": 1.0390625,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 128,
      "sum": 182426.0,
      "mean": 1425.203125,
      "median": 946.5,
      "p95": 4094.0,
      "min": 103.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 185.0,
      "mean": 1.4453125,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 11.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 182241.0,
      "mean": 1423.7578125,
      "median": 945.5,
      "p95": 4093.0,
      "min": 101.0,
      "max": 4093.0
    },
    "widths": {
      "n": 28,
      "sum": 106.0,
      "mean": 3.7857142857142856,
      "median": 3.0,
      "p95": 6.0,
      "min": 2.0,
      "max": 7.0
    },
    "width_histogram": {
      "2": 5,
      "3": 10,
      "4": 6,
      "5": 1,
      "6": 5,
      "7": 1
    },
    "truncated_samples": 12,
    "truncated_fraction": 0.09375,
    "invalid_width_samples": 23,
    "forked_samples": 5
  },
  "metrics_correct": {
    "F": {
      "n": 90,
      "sum": 100359.0,
      "mean": 1115.1,
      "median": 878.0,
      "p95": 3109.799999999999,
      "min": 139.0,
      "max": 4067.0
    },
    "T_sampled": {
      "n": 90,
      "sum": 101258.0,
      "mean": 1125.088888888889,
      "median": 878.0,
      "p95": 3119.699999999999,
      "min": 139.0,
      "max": 4069.0
    },
    "T_forced": {
      "n": 90,
      "sum": 226.0,
      "mean": 2.511111111111111,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 27.0
    },
    "T_assembled": {
      "n": 90,
      "sum": 101484.0,
      "mean": 1127.6,
      "median": 885.5,
      "p95": 3121.699999999999,
      "min": 141.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 90,
      "sum": 101258.0,
      "mean": 1125.088888888889,
      "median": 878.0,
      "p95": 3119.699999999999,
      "min": 139.0,
      "max": 4069.0
    },
    "generation_calls": {
      "n": 90,
      "sum": 113.0,
      "mean": 1.2555555555555555,
      "median": 1.0,
      "p95": 1.5499999999999972,
      "min": 1.0,
      "max": 11.0
    },
    "wall_seconds": {
      "n": 90,
      "sum": 3748.3497426509857,
      "mean": 41.64833047389984,
      "median": 32.509279012680054,
      "p95": 120.11268726587294,
      "min": 5.403902769088745,
      "max": 153.10989212989807
    },
    "forks": {
      "n": 90,
      "sum": 3.0,
      "mean": 0.03333333333333333,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 90,
      "sum": 3.0,
      "mean": 0.03333333333333333,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 90,
      "sum": 93.0,
      "mean": 1.0333333333333334,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 90,
      "sum": 101258.0,
      "mean": 1125.088888888889,
      "median": 878.0,
      "p95": 3119.699999999999,
      "min": 139.0,
      "max": 4069.0
    },
    "prefill_calls_inferred": {
      "n": 90,
      "sum": 113.0,
      "mean": 1.2555555555555555,
      "median": 1.0,
      "p95": 1.5499999999999972,
      "min": 1.0,
      "max": 11.0
    },
    "decode_calls_inferred": {
      "n": 90,
      "sum": 101145.0,
      "mean": 1123.8333333333333,
      "median": 877.0,
      "p95": 3118.699999999999,
      "min": 138.0,
      "max": 4066.0
    },
    "widths": {
      "n": 5,
      "sum": 18.0,
      "mean": 3.6,
      "median": 3.0,
      "p95": 6.199999999999999,
      "min": 2.0,
      "max": 7.0
    },
    "width_histogram": {
      "2": 1,
      "3": 3,
      "7": 1
    },
    "truncated_samples": 1,
    "truncated_fraction": 0.011111111111111112,
    "invalid_width_samples": 2,
    "forked_samples": 3
  },
  "historical_correct": 86,
  "historical_pass_at_1_completed_only": 0.671875,
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
      "basic_valid": 48,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 56,
      "parallel_execution_mismatch_samples": 7,
      "correct_and_basic_valid": 47,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 91710.0,
          "mean": 1432.96875,
          "median": 1014.0,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 93927.0,
          "mean": 1467.609375,
          "median": 1014.0,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 194.0,
          "mean": 3.03125,
          "median": 2.0,
          "p95": 9.649999999999949,
          "min": 2.0,
          "max": 27.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 94121.0,
          "mean": 1470.640625,
          "median": 1016.0,
          "p95": 4096.0,
          "min": 105.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 93927.0,
          "mean": 1467.609375,
          "median": 1014.0,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 99.0,
          "mean": 1.546875,
          "median": 1.0,
          "p95": 5.399999999999977,
          "min": 1.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 3511.317611217499,
          "mean": 54.86433767527342,
          "median": 37.36943185329437,
          "p95": 153.65263887643815,
          "min": 3.4975600242614746,
          "max": 156.2981312274933
        },
        "forks": {
          "n": 64,
          "sum": 4.0,
          "mean": 0.0625,
          "median": 0.0,
          "p95": 0.8499999999999943,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 64,
          "sum": 4.0,
          "mean": 0.0625,
          "median": 0.0,
          "p95": 0.8499999999999943,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 64,
          "sum": 68.0,
          "mean": 1.0625,
          "median": 1.0,
          "p95": 1.8499999999999943,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 64,
          "sum": 93927.0,
          "mean": 1467.609375,
          "median": 1014.0,
          "p95": 4094.0,
          "min": 103.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 99.0,
          "mean": 1.546875,
          "median": 1.0,
          "p95": 5.399999999999977,
          "min": 1.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 93828.0,
          "mean": 1466.0625,
          "median": 1013.0,
          "p95": 4093.0,
          "min": 101.0,
          "max": 4093.0
        },
        "widths": {
          "n": 11,
          "sum": 44.0,
          "mean": 4.0,
          "median": 4.0,
          "p95": 6.5,
          "min": 2.0,
          "max": 7.0
        },
        "width_histogram": {
          "2": 2,
          "3": 2,
          "4": 4,
          "5": 1,
          "6": 1,
          "7": 1
        },
        "truncated_samples": 7,
        "truncated_fraction": 0.109375,
        "invalid_width_samples": 7,
        "forked_samples": 4
      },
      "metrics_correct": {
        "F": {
          "n": 49,
          "sum": 57191.0,
          "mean": 1167.1632653061224,
          "median": 946.0,
          "p95": 3289.7999999999997,
          "min": 139.0,
          "max": 4067.0
        },
        "T_sampled": {
          "n": 49,
          "sum": 58010.0,
          "mean": 1183.8775510204082,
          "median": 946.0,
          "p95": 3402.599999999999,
          "min": 139.0,
          "max": 4069.0
        },
        "T_forced": {
          "n": 49,
          "sum": 132.0,
          "mean": 2.693877551020408,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 27.0
        },
        "T_assembled": {
          "n": 49,
          "sum": 58142.0,
          "mean": 1186.5714285714287,
          "median": 948.0,
          "p95": 3404.599999999999,
          "min": 141.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 49,
          "sum": 58010.0,
          "mean": 1183.8775510204082,
          "median": 946.0,
          "p95": 3402.599999999999,
          "min": 139.0,
          "max": 4069.0
        },
        "generation_calls": {
          "n": 49,
          "sum": 64.0,
          "mean": 1.3061224489795917,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 11.0
        },
        "wall_seconds": {
          "n": 49,
          "sum": 2168.502247571945,
          "mean": 44.25514790963153,
          "median": 35.665197134017944,
          "p95": 126.54754762649533,
          "min": 5.403902769088745,
          "max": 153.10989212989807
        },
        "forks": {
          "n": 49,
          "sum": 2.0,
          "mean": 0.04081632653061224,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 49,
          "sum": 2.0,
          "mean": 0.04081632653061224,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 49,
          "sum": 51.0,
          "mean": 1.0408163265306123,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 49,
          "sum": 58010.0,
          "mean": 1183.8775510204082,
          "median": 946.0,
          "p95": 3402.599999999999,
          "min": 139.0,
          "max": 4069.0
        },
        "prefill_calls_inferred": {
          "n": 49,
          "sum": 64.0,
          "mean": 1.3061224489795917,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 11.0
        },
        "decode_calls_inferred": {
          "n": 49,
          "sum": 57946.0,
          "mean": 1182.5714285714287,
          "median": 945.0,
          "p95": 3401.599999999999,
          "min": 138.0,
          "max": 4066.0
        },
        "widths": {
          "n": 2,
          "sum": 9.0,
          "mean": 4.5,
          "median": 4.5,
          "p95": 6.75,
          "min": 2.0,
          "max": 7.0
        },
        "width_histogram": {
          "2": 1,
          "7": 1
        },
        "truncated_samples": 1,
        "truncated_fraction": 0.02040816326530612,
        "invalid_width_samples": 0,
        "forked_samples": 2
      },
      "historical_correct": 47,
      "historical_pass_at_1": 0.734375
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 41,
      "pass_at_1": 0.640625,
      "basic_valid": 42,
      "basic_valid_fraction": 0.65625,
      "parallel_valid": 0,
      "parallel_syntax_valid": 48,
      "parallel_execution_mismatch_samples": 16,
      "correct_and_basic_valid": 38,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 88419.0,
          "mean": 1381.546875,
          "median": 856.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 88499.0,
          "mean": 1382.796875,
          "median": 868.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 64,
          "sum": 140.0,
          "mean": 2.1875,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 14.0
        },
        "T_assembled": {
          "n": 64,
          "sum": 88639.0,
          "mean": 1384.984375,
          "median": 876.0,
          "p95": 4096.0,
          "min": 112.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 88499.0,
          "mean": 1382.796875,
          "median": 868.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 86.0,
          "mean": 1.34375,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 7.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 3262.772100687027,
          "mean": 50.9808140732348,
          "median": 32.33584225177765,
          "p95": 148.72440518140792,
          "min": 4.206994295120239,
          "max": 154.6365933418274
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
          "sum": 88499.0,
          "mean": 1382.796875,
          "median": 868.0,
          "p95": 4094.0,
          "min": 110.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 86.0,
          "mean": 1.34375,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 7.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 88413.0,
          "mean": 1381.453125,
          "median": 863.5,
          "p95": 4093.0,
          "min": 108.0,
          "max": 4093.0
        },
        "widths": {
          "n": 17,
          "sum": 62.0,
          "mean": 3.6470588235294117,
          "median": 3.0,
          "p95": 6.0,
          "min": 2.0,
          "max": 6.0
        },
        "width_histogram": {
          "2": 3,
          "3": 8,
          "4": 2,
          "6": 4
        },
        "truncated_samples": 5,
        "truncated_fraction": 0.078125,
        "invalid_width_samples": 16,
        "forked_samples": 1
      },
      "metrics_correct": {
        "F": {
          "n": 41,
          "sum": 43168.0,
          "mean": 1052.878048780488,
          "median": 740.0,
          "p95": 2527.0,
          "min": 226.0,
          "max": 3979.0
        },
        "T_sampled": {
          "n": 41,
          "sum": 43248.0,
          "mean": 1054.8292682926829,
          "median": 740.0,
          "p95": 2527.0,
          "min": 226.0,
          "max": 3979.0
        },
        "T_forced": {
          "n": 41,
          "sum": 94.0,
          "mean": 2.292682926829268,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 14.0
        },
        "T_assembled": {
          "n": 41,
          "sum": 43342.0,
          "mean": 1057.121951219512,
          "median": 742.0,
          "p95": 2529.0,
          "min": 228.0,
          "max": 3981.0
        },
        "actual_generated_tokens": {
          "n": 41,
          "sum": 43248.0,
          "mean": 1054.8292682926829,
          "median": 740.0,
          "p95": 2527.0,
          "min": 226.0,
          "max": 3979.0
        },
        "generation_calls": {
          "n": 41,
          "sum": 49.0,
          "mean": 1.1951219512195121,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 7.0
        },
        "wall_seconds": {
          "n": 41,
          "sum": 1579.8474950790405,
          "mean": 38.532865733635134,
          "median": 27.755918741226196,
          "p95": 86.87146854400635,
          "min": 8.220338582992554,
          "max": 141.00138783454895
        },
        "forks": {
          "n": 41,
          "sum": 1.0,
          "mean": 0.024390243902439025,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 41,
          "sum": 1.0,
          "mean": 0.024390243902439025,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 41,
          "sum": 42.0,
          "mean": 1.024390243902439,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 41,
          "sum": 43248.0,
          "mean": 1054.8292682926829,
          "median": 740.0,
          "p95": 2527.0,
          "min": 226.0,
          "max": 3979.0
        },
        "prefill_calls_inferred": {
          "n": 41,
          "sum": 49.0,
          "mean": 1.1951219512195121,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 7.0
        },
        "decode_calls_inferred": {
          "n": 41,
          "sum": 43199.0,
          "mean": 1053.6341463414635,
          "median": 739.0,
          "p95": 2525.0,
          "min": 225.0,
          "max": 3977.0
        },
        "widths": {
          "n": 3,
          "sum": 9.0,
          "mean": 3.0,
          "median": 3.0,
          "p95": 3.0,
          "min": 3.0,
          "max": 3.0
        },
        "width_histogram": {
          "3": 3
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 2,
        "forked_samples": 1
      },
      "historical_correct": 39,
      "historical_pass_at_1": 0.609375
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
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 24,
  "completed": 24,
  "missing": 0,
  "correct": 15,
  "pass_at_1_completed_only": 0.625,
  "format_valid": 16,
  "format_fraction_completed_only": 0.6666666666666666,
  "executed_fork_samples": 1,
  "unfinished_thinking": 2,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
  "parallel_syntax_valid": 17,
  "parallel_execution_mismatch_samples": 7,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 16,
  "legacy_format_fraction_completed_only": 0.6666666666666666,
  "legacy_parallel_protocol_valid": 0,
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
    "completed": 24,
    "basic_valid": 16,
    "executed_fork_samples": 1,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 7,
    "correct": 15
  },
  "fork_coverage": 0.041666666666666664,
  "valid_parallel_among_executed_forks": 0.0,
  "invalid_width_fraction": 0.2916666666666667,
  "correct_and_basic_valid": 15,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 24,
      "sum": 22827.0,
      "mean": 951.125,
      "median": 619.5,
      "p95": 2400.7999999999993,
      "min": 165.0,
      "max": 3473.0
    },
    "T_sampled": {
      "n": 24,
      "sum": 23334.0,
      "mean": 972.25,
      "median": 619.5,
      "p95": 2400.7999999999993,
      "min": 165.0,
      "max": 3473.0
    },
    "T_forced": {
      "n": 24,
      "sum": 63.0,
      "mean": 2.625,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 17.0
    },
    "T_assembled": {
      "n": 24,
      "sum": 23397.0,
      "mean": 974.875,
      "median": 621.5,
      "p95": 2402.7999999999993,
      "min": 167.0,
      "max": 3475.0
    },
    "actual_generated_tokens": {
      "n": 24,
      "sum": 23334.0,
      "mean": 972.25,
      "median": 619.5,
      "p95": 2400.7999999999993,
      "min": 165.0,
      "max": 3473.0
    },
    "generation_calls": {
      "n": 24,
      "sum": 38.0,
      "mean": 1.5833333333333333,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 8.0
    },
    "wall_seconds": {
      "n": 24,
      "sum": 861.5787353515625,
      "mean": 35.89911397298177,
      "median": 23.217636108398438,
      "p95": 88.32820879220961,
      "min": 7.052232503890991,
      "max": 123.14075946807861
    },
    "forks": {
      "n": 24,
      "sum": 1.0,
      "mean": 0.041666666666666664,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "rounds": {
      "n": 24,
      "sum": 1.0,
      "mean": 0.041666666666666664,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "generation_turns": {
      "n": 24,
      "sum": 25.0,
      "mean": 1.0416666666666667,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "model_forward_calls_inferred": {
      "n": 24,
      "sum": 23334.0,
      "mean": 972.25,
      "median": 619.5,
      "p95": 2400.7999999999993,
      "min": 165.0,
      "max": 3473.0
    },
    "prefill_calls_inferred": {
      "n": 24,
      "sum": 38.0,
      "mean": 1.5833333333333333,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 8.0
    },
    "decode_calls_inferred": {
      "n": 24,
      "sum": 23296.0,
      "mean": 970.6666666666666,
      "median": 618.0,
      "p95": 2398.9499999999994,
      "min": 163.0,
      "max": 3472.0
    },
    "widths": {
      "n": 8,
      "sum": 30.0,
      "mean": 3.75,
      "median": 3.0,
      "p95": 6.599999999999998,
      "min": 3.0,
      "max": 8.0
    },
    "width_histogram": {
      "3": 6,
      "4": 1,
      "8": 1
    },
    "truncated_samples": 0,
    "truncated_fraction": 0.0,
    "invalid_width_samples": 7,
    "forked_samples": 1
  },
  "metrics_correct": {
    "F": {
      "n": 15,
      "sum": 15170.0,
      "mean": 1011.3333333333334,
      "median": 742.0,
      "p95": 2586.799999999999,
      "min": 193.0,
      "max": 3473.0
    },
    "T_sampled": {
      "n": 15,
      "sum": 15170.0,
      "mean": 1011.3333333333334,
      "median": 742.0,
      "p95": 2586.799999999999,
      "min": 193.0,
      "max": 3473.0
    },
    "T_forced": {
      "n": 15,
      "sum": 30.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 15,
      "sum": 15200.0,
      "mean": 1013.3333333333334,
      "median": 744.0,
      "p95": 2588.799999999999,
      "min": 195.0,
      "max": 3475.0
    },
    "actual_generated_tokens": {
      "n": 15,
      "sum": 15170.0,
      "mean": 1011.3333333333334,
      "median": 742.0,
      "p95": 2586.799999999999,
      "min": 193.0,
      "max": 3473.0
    },
    "generation_calls": {
      "n": 15,
      "sum": 15.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 15,
      "sum": 561.2690153121948,
      "mean": 37.41793435414632,
      "median": 25.958603143692017,
      "p95": 94.43875057697292,
      "min": 7.052232503890991,
      "max": 123.14075946807861
    },
    "forks": {
      "n": 15,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 15,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 15,
      "sum": 15.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 15,
      "sum": 15170.0,
      "mean": 1011.3333333333334,
      "median": 742.0,
      "p95": 2586.799999999999,
      "min": 193.0,
      "max": 3473.0
    },
    "prefill_calls_inferred": {
      "n": 15,
      "sum": 15.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 15,
      "sum": 15155.0,
      "mean": 1010.3333333333334,
      "median": 741.0,
      "p95": 2585.799999999999,
      "min": 192.0,
      "max": 3472.0
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
  "historical_correct": 15,
  "historical_pass_at_1_completed_only": 0.625,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 24,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 12,
      "completed": 12,
      "correct": 10,
      "pass_at_1": 0.8333333333333334,
      "basic_valid": 10,
      "basic_valid_fraction": 0.8333333333333334,
      "parallel_valid": 0,
      "parallel_syntax_valid": 10,
      "parallel_execution_mismatch_samples": 2,
      "correct_and_basic_valid": 10,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 12871.0,
          "mean": 1072.5833333333333,
          "median": 784.5,
          "p95": 2776.699999999999,
          "min": 165.0,
          "max": 3473.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 12871.0,
          "mean": 1072.5833333333333,
          "median": 784.5,
          "p95": 2776.699999999999,
          "min": 165.0,
          "max": 3473.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 12895.0,
          "mean": 1074.5833333333333,
          "median": 786.5,
          "p95": 2778.699999999999,
          "min": 167.0,
          "max": 3475.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 12871.0,
          "mean": 1072.5833333333333,
          "median": 784.5,
          "p95": 2776.699999999999,
          "min": 165.0,
          "max": 3473.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 14.0,
          "mean": 1.1666666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 479.3197572231293,
          "mean": 39.94331310192744,
          "median": 29.018447399139404,
          "p95": 100.58918105363843,
          "min": 7.052232503890991,
          "max": 123.14075946807861
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 12871.0,
          "mean": 1072.5833333333333,
          "median": 784.5,
          "p95": 2776.699999999999,
          "min": 165.0,
          "max": 3473.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 14.0,
          "mean": 1.1666666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 12857.0,
          "mean": 1071.4166666666667,
          "median": 783.5,
          "p95": 2775.699999999999,
          "min": 163.0,
          "max": 3472.0
        },
        "widths": {
          "n": 2,
          "sum": 6.0,
          "mean": 3.0,
          "median": 3.0,
          "p95": 3.0,
          "min": 3.0,
          "max": 3.0
        },
        "width_histogram": {
          "3": 2
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 2,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 10,
          "sum": 12335.0,
          "mean": 1233.5,
          "median": 1062.5,
          "p95": 2903.299999999999,
          "min": 193.0,
          "max": 3473.0
        },
        "T_sampled": {
          "n": 10,
          "sum": 12335.0,
          "mean": 1233.5,
          "median": 1062.5,
          "p95": 2903.299999999999,
          "min": 193.0,
          "max": 3473.0
        },
        "T_forced": {
          "n": 10,
          "sum": 20.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 10,
          "sum": 12355.0,
          "mean": 1235.5,
          "median": 1064.5,
          "p95": 2905.299999999999,
          "min": 195.0,
          "max": 3475.0
        },
        "actual_generated_tokens": {
          "n": 10,
          "sum": 12335.0,
          "mean": 1233.5,
          "median": 1062.5,
          "p95": 2903.299999999999,
          "min": 193.0,
          "max": 3473.0
        },
        "generation_calls": {
          "n": 10,
          "sum": 10.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 10,
          "sum": 458.00949883461,
          "mean": 45.800949883461,
          "median": 39.18920373916626,
          "p95": 104.68946803808208,
          "min": 7.052232503890991,
          "max": 123.14075946807861
        },
        "forks": {
          "n": 10,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 10,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 10,
          "sum": 10.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 10,
          "sum": 12335.0,
          "mean": 1233.5,
          "median": 1062.5,
          "p95": 2903.299999999999,
          "min": 193.0,
          "max": 3473.0
        },
        "prefill_calls_inferred": {
          "n": 10,
          "sum": 10.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 10,
          "sum": 12325.0,
          "mean": 1232.5,
          "median": 1061.5,
          "p95": 2902.299999999999,
          "min": 192.0,
          "max": 3472.0
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
      "historical_correct": 10,
      "historical_pass_at_1": 0.8333333333333334
    },
    "math": {
      "planned": 12,
      "completed": 12,
      "correct": 5,
      "pass_at_1": 0.4166666666666667,
      "basic_valid": 6,
      "basic_valid_fraction": 0.5,
      "parallel_valid": 0,
      "parallel_syntax_valid": 7,
      "parallel_execution_mismatch_samples": 5,
      "correct_and_basic_valid": 5,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 9956.0,
          "mean": 829.6666666666666,
          "median": 592.5,
          "p95": 2203.45,
          "min": 278.0,
          "max": 2435.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 10463.0,
          "mean": 871.9166666666666,
          "median": 592.5,
          "p95": 2203.45,
          "min": 278.0,
          "max": 2435.0
        },
        "T_forced": {
          "n": 12,
          "sum": 39.0,
          "mean": 3.25,
          "median": 2.0,
          "p95": 8.74999999999999,
          "min": 2.0,
          "max": 17.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 10502.0,
          "mean": 875.1666666666666,
          "median": 594.5,
          "p95": 2205.45,
          "min": 280.0,
          "max": 2437.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 10463.0,
          "mean": 871.9166666666666,
          "median": 592.5,
          "p95": 2203.45,
          "min": 278.0,
          "max": 2435.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 1.5,
          "p95": 4.699999999999996,
          "min": 1.0,
          "max": 8.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 382.2589781284332,
          "mean": 31.854914844036102,
          "median": 22.323156118392944,
          "p95": 80.17918915748595,
          "min": 9.816729545593262,
          "max": 89.42061805725098
        },
        "forks": {
          "n": 12,
          "sum": 1.0,
          "mean": 0.08333333333333333,
          "median": 0.0,
          "p95": 0.4499999999999993,
          "min": 0.0,
          "max": 1.0
        },
        "rounds": {
          "n": 12,
          "sum": 1.0,
          "mean": 0.08333333333333333,
          "median": 0.0,
          "p95": 0.4499999999999993,
          "min": 0.0,
          "max": 1.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 13.0,
          "mean": 1.0833333333333333,
          "median": 1.0,
          "p95": 1.4499999999999993,
          "min": 1.0,
          "max": 2.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 10463.0,
          "mean": 871.9166666666666,
          "median": 592.5,
          "p95": 2203.45,
          "min": 278.0,
          "max": 2435.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 1.5,
          "p95": 4.699999999999996,
          "min": 1.0,
          "max": 8.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 10439.0,
          "mean": 869.9166666666666,
          "median": 591.0,
          "p95": 2201.9999999999995,
          "min": 276.0,
          "max": 2433.0
        },
        "widths": {
          "n": 6,
          "sum": 24.0,
          "mean": 4.0,
          "median": 3.0,
          "p95": 7.0,
          "min": 3.0,
          "max": 8.0
        },
        "width_histogram": {
          "3": 4,
          "4": 1,
          "8": 1
        },
        "truncated_samples": 0,
        "truncated_fraction": 0.0,
        "invalid_width_samples": 5,
        "forked_samples": 1
      },
      "metrics_correct": {
        "F": {
          "n": 5,
          "sum": 2835.0,
          "mean": 567.0,
          "median": 591.0,
          "p95": 722.6,
          "min": 398.0,
          "max": 742.0
        },
        "T_sampled": {
          "n": 5,
          "sum": 2835.0,
          "mean": 567.0,
          "median": 591.0,
          "p95": 722.6,
          "min": 398.0,
          "max": 742.0
        },
        "T_forced": {
          "n": 5,
          "sum": 10.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 5,
          "sum": 2845.0,
          "mean": 569.0,
          "median": 593.0,
          "p95": 724.6,
          "min": 400.0,
          "max": 744.0
        },
        "actual_generated_tokens": {
          "n": 5,
          "sum": 2835.0,
          "mean": 567.0,
          "median": 591.0,
          "p95": 722.6,
          "min": 398.0,
          "max": 742.0
        },
        "generation_calls": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 5,
          "sum": 103.25951647758484,
          "mean": 20.651903295516966,
          "median": 22.47240114212036,
          "p95": 25.559456729888915,
          "min": 14.04002332687378,
          "max": 25.958603143692017
        },
        "forks": {
          "n": 5,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 5,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 5,
          "sum": 2835.0,
          "mean": 567.0,
          "median": 591.0,
          "p95": 722.6,
          "min": 398.0,
          "max": 742.0
        },
        "prefill_calls_inferred": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 5,
          "sum": 2830.0,
          "mean": 566.0,
          "median": 590.0,
          "p95": 721.6,
          "min": 397.0,
          "max": 741.0
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
      "historical_correct": 5,
      "historical_pass_at_1": 0.4166666666666667
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
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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
  "suite": "24",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-1e-3-trained-structured-24/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 98,
  "pass_at_1_completed_only": 0.765625,
  "format_valid": 55,
  "format_fraction_completed_only": 0.4296875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 25,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 7,
  "legacy_format_fraction_completed_only": 0.0546875,
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
    "basic_valid": 55,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 98
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 53,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 357577.0,
      "mean": 2793.5703125,
      "median": 2755.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 8447.327067613602,
      "mean": 65.99474271573126,
      "median": 64.78199708461761,
      "p95": 99.59882279634475,
      "min": 11.340869665145874,
      "max": 102.1218581199646
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 33,
    "truncated_fraction": 0.2578125,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 237783.0,
      "mean": 2426.3571428571427,
      "median": 2287.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 5626.0571546554565,
      "mean": 57.40874647607609,
      "median": 53.93285691738129,
      "p95": 97.7583480000496,
      "min": 11.340869665145874,
      "max": 102.1218581199646
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 6,
    "truncated_fraction": 0.061224489795918366,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 92,
  "historical_pass_at_1_completed_only": 0.71875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 53,
      "pass_at_1": 0.828125,
      "basic_valid": 48,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 165383.0,
          "mean": 2584.109375,
          "median": 2484.0,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 3914.8035531044006,
          "mean": 61.16880551725626,
          "median": 60.069340229034424,
          "p95": 99.47327344417572,
          "min": 11.340869665145874,
          "max": 100.91785669326782
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 122831.0,
          "mean": 2317.566037735849,
          "median": 2289.0,
          "p95": 3829.3999999999996,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 2906.8700828552246,
          "mean": 54.84660533689103,
          "median": 55.380449295043945,
          "p95": 91.19474811553955,
          "min": 11.340869665145874,
          "max": 98.06270360946655
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_fraction": 0.018867924528301886,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 52,
      "historical_pass_at_1": 0.8125
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 45,
      "pass_at_1": 0.703125,
      "basic_valid": 7,
      "basic_valid_fraction": 0.109375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 7,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 192194.0,
          "mean": 3003.03125,
          "median": 3329.5,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 4532.523514509201,
          "mean": 70.82067991420627,
          "median": 79.49807071685791,
          "p95": 99.34512535333633,
          "min": 29.694364309310913,
          "max": 102.1218581199646
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 23,
        "truncated_fraction": 0.359375,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 45,
          "sum": 90.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 45,
          "sum": 114952.0,
          "mean": 2554.488888888889,
          "median": 2226.0,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 45,
          "sum": 2719.187071800232,
          "mean": 60.426379373338484,
          "median": 53.60948133468628,
          "p95": 98.33456449508667,
          "min": 29.694364309310913,
          "max": 102.1218581199646
        },
        "forks": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 5,
        "truncated_fraction": 0.1111111111111111,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 40,
      "historical_pass_at_1": 0.625
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 24,
  "completed": 24,
  "missing": 0,
  "correct": 18,
  "pass_at_1_completed_only": 0.75,
  "format_valid": 13,
  "format_fraction_completed_only": 0.5416666666666666,
  "executed_fork_samples": 0,
  "unfinished_thinking": 4,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "parallel_syntax_valid": 24,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 1,
  "legacy_format_fraction_completed_only": 0.041666666666666664,
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
    "completed": 24,
    "basic_valid": 13,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 18
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 13,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 24,
      "sum": 48.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 24,
      "sum": 63330.0,
      "mean": 2638.75,
      "median": 2795.5,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 24,
      "sum": 63282.0,
      "mean": 2636.75,
      "median": 2793.5,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 24,
      "sum": 1493.3470289707184,
      "mean": 62.22279287377993,
      "median": 68.71044099330902,
      "p95": 96.94601719379425,
      "min": 11.939513683319092,
      "max": 97.53874516487122
    },
    "forks": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 5,
    "truncated_fraction": 0.20833333333333334,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "T_sampled": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "T_forced": {
      "n": 18,
      "sum": 36.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 18,
      "sum": 39619.0,
      "mean": 2201.0555555555557,
      "median": 1760.0,
      "p95": 3799.1499999999996,
      "min": 487.0,
      "max": 3902.0
    },
    "actual_generated_tokens": {
      "n": 18,
      "sum": 39583.0,
      "mean": 2199.0555555555557,
      "median": 1758.0,
      "p95": 3797.1499999999996,
      "min": 485.0,
      "max": 3900.0
    },
    "generation_calls": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 18,
      "sum": 938.2873129844666,
      "mean": 52.127072943581474,
      "median": 41.8072395324707,
      "p95": 90.81489341259002,
      "min": 11.939513683319092,
      "max": 91.38632559776306
    },
    "forks": {
      "n": 18,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 18,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 18,
      "sum": 18.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
  "historical_correct": 18,
  "historical_pass_at_1_completed_only": 0.75,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 12,
      "completed": 12,
      "correct": 9,
      "pass_at_1": 0.75,
      "basic_valid": 8,
      "basic_valid_fraction": 0.6666666666666666,
      "parallel_valid": 0,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 8,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 34111.0,
          "mean": 2842.5833333333335,
          "median": 3231.5,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 34087.0,
          "mean": 2840.5833333333335,
          "median": 3229.5,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 807.7237164974213,
          "mean": 67.31030970811844,
          "median": 77.58206129074097,
          "p95": 96.38220155239105,
          "min": 11.939513683319092,
          "max": 97.53874516487122
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 3,
        "truncated_fraction": 0.25,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "T_sampled": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "T_forced": {
          "n": 9,
          "sum": 18.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 9,
          "sum": 21823.0,
          "mean": 2424.777777777778,
          "median": 2761.0,
          "p95": 3853.6,
          "min": 487.0,
          "max": 3902.0
        },
        "actual_generated_tokens": {
          "n": 9,
          "sum": 21805.0,
          "mean": 2422.777777777778,
          "median": 2759.0,
          "p95": 3851.6,
          "min": 485.0,
          "max": 3900.0
        },
        "generation_calls": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 9,
          "sum": 520.9933335781097,
          "mean": 57.88814817534553,
          "median": 67.13429355621338,
          "p95": 91.11741633415222,
          "min": 11.939513683319092,
          "max": 91.38632559776306
        },
        "forks": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
      "historical_correct": 9,
      "historical_pass_at_1": 0.75
    },
    "math": {
      "planned": 12,
      "completed": 12,
      "correct": 9,
      "pass_at_1": 0.75,
      "basic_valid": 5,
      "basic_valid_fraction": 0.4166666666666667,
      "parallel_valid": 0,
      "parallel_syntax_valid": 12,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 5,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 29219.0,
          "mean": 2434.9166666666665,
          "median": 1760.0,
          "p95": 4096.0,
          "min": 1268.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 29195.0,
          "mean": 2432.9166666666665,
          "median": 1758.0,
          "p95": 4094.0,
          "min": 1266.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 685.6233124732971,
          "mean": 57.13527603944143,
          "median": 41.8072395324707,
          "p95": 96.81600830554962,
          "min": 29.957270860671997,
          "max": 96.99477052688599
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 2,
        "truncated_fraction": 0.16666666666666666,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "T_sampled": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "T_forced": {
          "n": 9,
          "sum": 18.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 9,
          "sum": 17796.0,
          "mean": 1977.3333333333333,
          "median": 1738.0,
          "p95": 3247.0,
          "min": 1268.0,
          "max": 3249.0
        },
        "actual_generated_tokens": {
          "n": 9,
          "sum": 17778.0,
          "mean": 1975.3333333333333,
          "median": 1736.0,
          "p95": 3245.0,
          "min": 1266.0,
          "max": 3247.0
        },
        "generation_calls": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 9,
          "sum": 417.2939794063568,
          "mean": 46.36599771181742,
          "median": 40.78084921836853,
          "p95": 74.94817242622375,
          "min": 29.957270860671997,
          "max": 75.0762231349945
        },
        "forks": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
      "historical_correct": 9,
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "24",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-native-24/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 81,
  "pass_at_1_completed_only": 0.6328125,
  "format_valid": 73,
  "format_fraction_completed_only": 0.5703125,
  "executed_fork_samples": 0,
  "unfinished_thinking": 16,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "parallel_syntax_valid": 98,
  "parallel_execution_mismatch_samples": 27,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 67,
  "legacy_format_fraction_completed_only": 0.5234375,
  "legacy_parallel_protocol_valid": 0,
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
    "completed": 128,
    "basic_valid": 73,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 27,
    "correct": 81
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.2109375,
  "correct_and_basic_valid": 71,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 248626.0,
      "mean": 1942.390625,
      "median": 1489.5,
      "p95": 4094.0,
      "min": 400.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 248626.0,
      "mean": 1942.390625,
      "median": 1489.5,
      "p95": 4094.0,
      "min": 400.0,
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
      "sum": 248882.0,
      "mean": 1944.390625,
      "median": 1491.5,
      "p95": 4096.0,
      "min": 402.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 248626.0,
      "mean": 1942.390625,
      "median": 1489.5,
      "p95": 4094.0,
      "min": 400.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 128,
      "sum": 155.0,
      "mean": 1.2109375,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 2.0
    },
    "wall_seconds": {
      "n": 128,
      "sum": 9581.892207145691,
      "mean": 74.85853286832571,
      "median": 58.98131513595581,
      "p95": 159.29628727436065,
      "min": 15.297545433044434,
      "max": 171.85179948806763
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
      "sum": 248626.0,
      "mean": 1942.390625,
      "median": 1489.5,
      "p95": 4094.0,
      "min": 400.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 128,
      "sum": 155.0,
      "mean": 1.2109375,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 2.0
    },
    "decode_calls_inferred": {
      "n": 128,
      "sum": 248471.0,
      "mean": 1941.1796875,
      "median": 1488.0,
      "p95": 4093.0,
      "min": 399.0,
      "max": 4093.0
    },
    "widths": {
      "n": 24,
      "sum": 60.0,
      "mean": 2.5,
      "median": 2.0,
      "p95": 4.849999999999998,
      "min": 2.0,
      "max": 6.0
    },
    "width_histogram": {
      "2": 18,
      "3": 3,
      "4": 1,
      "5": 1,
      "6": 1
    },
    "truncated_samples": 22,
    "truncated_fraction": 0.171875,
    "invalid_width_samples": 27,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 81,
      "sum": 118924.0,
      "mean": 1468.1975308641975,
      "median": 1228.0,
      "p95": 3559.0,
      "min": 400.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 81,
      "sum": 118924.0,
      "mean": 1468.1975308641975,
      "median": 1228.0,
      "p95": 3559.0,
      "min": 400.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 81,
      "sum": 162.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 81,
      "sum": 119086.0,
      "mean": 1470.1975308641975,
      "median": 1230.0,
      "p95": 3561.0,
      "min": 402.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 81,
      "sum": 118924.0,
      "mean": 1468.1975308641975,
      "median": 1228.0,
      "p95": 3559.0,
      "min": 400.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 81,
      "sum": 82.0,
      "mean": 1.0123456790123457,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "wall_seconds": {
      "n": 81,
      "sum": 4598.31344628334,
      "mean": 56.76930180596717,
      "median": 47.03874611854553,
      "p95": 136.42615056037903,
      "min": 15.297545433044434,
      "max": 162.43017101287842
    },
    "forks": {
      "n": 81,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 81,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 81,
      "sum": 81.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 81,
      "sum": 118924.0,
      "mean": 1468.1975308641975,
      "median": 1228.0,
      "p95": 3559.0,
      "min": 400.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 81,
      "sum": 82.0,
      "mean": 1.0123456790123457,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 2.0
    },
    "decode_calls_inferred": {
      "n": 81,
      "sum": 118842.0,
      "mean": 1467.1851851851852,
      "median": 1227.0,
      "p95": 3558.0,
      "min": 399.0,
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
    "truncated_samples": 3,
    "truncated_fraction": 0.037037037037037035,
    "invalid_width_samples": 1,
    "forked_samples": 0
  },
  "historical_correct": 77,
  "historical_pass_at_1_completed_only": 0.6015625,
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
      "basic_valid": 43,
      "basic_valid_fraction": 0.671875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 49,
      "parallel_execution_mismatch_samples": 14,
      "correct_and_basic_valid": 43,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 117105.0,
          "mean": 1829.765625,
          "median": 1597.0,
          "p95": 4094.0,
          "min": 449.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 117105.0,
          "mean": 1829.765625,
          "median": 1597.0,
          "p95": 4094.0,
          "min": 449.0,
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
          "sum": 117233.0,
          "mean": 1831.765625,
          "median": 1599.0,
          "p95": 4096.0,
          "min": 451.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 117105.0,
          "mean": 1829.765625,
          "median": 1597.0,
          "p95": 4094.0,
          "min": 449.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 78.0,
          "mean": 1.21875,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 4551.291536092758,
          "mean": 71.11393025144935,
          "median": 62.392449617385864,
          "p95": 158.06855471134182,
          "min": 16.94235610961914,
          "max": 165.20670294761658
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
          "sum": 117105.0,
          "mean": 1829.765625,
          "median": 1597.0,
          "p95": 4094.0,
          "min": 449.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 78.0,
          "mean": 1.21875,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 117027.0,
          "mean": 1828.546875,
          "median": 1596.0,
          "p95": 4093.0,
          "min": 448.0,
          "max": 4093.0
        },
        "widths": {
          "n": 13,
          "sum": 28.0,
          "mean": 2.1538461538461537,
          "median": 2.0,
          "p95": 3.0,
          "min": 2.0,
          "max": 3.0
        },
        "width_histogram": {
          "2": 11,
          "3": 2
        },
        "truncated_samples": 6,
        "truncated_fraction": 0.09375,
        "invalid_width_samples": 14,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 44,
          "sum": 59795.0,
          "mean": 1358.9772727272727,
          "median": 1238.5,
          "p95": 2767.7000000000007,
          "min": 449.0,
          "max": 3216.0
        },
        "T_sampled": {
          "n": 44,
          "sum": 59795.0,
          "mean": 1358.9772727272727,
          "median": 1238.5,
          "p95": 2767.7000000000007,
          "min": 449.0,
          "max": 3216.0
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
          "sum": 59883.0,
          "mean": 1360.9772727272727,
          "median": 1240.5,
          "p95": 2769.7000000000007,
          "min": 451.0,
          "max": 3218.0
        },
        "actual_generated_tokens": {
          "n": 44,
          "sum": 59795.0,
          "mean": 1358.9772727272727,
          "median": 1238.5,
          "p95": 2767.7000000000007,
          "min": 449.0,
          "max": 3216.0
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
          "sum": 2321.591050863266,
          "mean": 52.763432974165134,
          "median": 49.06055772304535,
          "p95": 107.93976104259494,
          "min": 16.94235610961914,
          "max": 126.48726844787598
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
          "sum": 59795.0,
          "mean": 1358.9772727272727,
          "median": 1238.5,
          "p95": 2767.7000000000007,
          "min": 449.0,
          "max": 3216.0
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
          "sum": 59751.0,
          "mean": 1357.9772727272727,
          "median": 1237.5,
          "p95": 2766.7000000000007,
          "min": 448.0,
          "max": 3215.0
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
      "correct": 37,
      "pass_at_1": 0.578125,
      "basic_valid": 30,
      "basic_valid_fraction": 0.46875,
      "parallel_valid": 0,
      "parallel_syntax_valid": 49,
      "parallel_execution_mismatch_samples": 13,
      "correct_and_basic_valid": 28,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 131521.0,
          "mean": 2055.015625,
          "median": 1420.5,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 131521.0,
          "mean": 2055.015625,
          "median": 1420.5,
          "p95": 4094.0,
          "min": 400.0,
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
          "sum": 131649.0,
          "mean": 2057.015625,
          "median": 1422.5,
          "p95": 4096.0,
          "min": 402.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 131521.0,
          "mean": 2055.015625,
          "median": 1420.5,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 64,
          "sum": 77.0,
          "mean": 1.203125,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 64,
          "sum": 5030.600671052933,
          "mean": 78.60313548520207,
          "median": 54.24246573448181,
          "p95": 158.97100912332536,
          "min": 15.297545433044434,
          "max": 171.85179948806763
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
          "sum": 131521.0,
          "mean": 2055.015625,
          "median": 1420.5,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 64,
          "sum": 77.0,
          "mean": 1.203125,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 64,
          "sum": 131444.0,
          "mean": 2053.8125,
          "median": 1419.5,
          "p95": 4093.0,
          "min": 399.0,
          "max": 4093.0
        },
        "widths": {
          "n": 11,
          "sum": 32.0,
          "mean": 2.909090909090909,
          "median": 2.0,
          "p95": 5.5,
          "min": 2.0,
          "max": 6.0
        },
        "width_histogram": {
          "2": 7,
          "3": 1,
          "4": 1,
          "5": 1,
          "6": 1
        },
        "truncated_samples": 16,
        "truncated_fraction": 0.25,
        "invalid_width_samples": 13,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 37,
          "sum": 59129.0,
          "mean": 1598.081081081081,
          "median": 1200.0,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 37,
          "sum": 59129.0,
          "mean": 1598.081081081081,
          "median": 1200.0,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 37,
          "sum": 74.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 37,
          "sum": 59203.0,
          "mean": 1600.081081081081,
          "median": 1202.0,
          "p95": 4096.0,
          "min": 402.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 37,
          "sum": 59129.0,
          "mean": 1598.081081081081,
          "median": 1200.0,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 37,
          "sum": 38.0,
          "mean": 1.027027027027027,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 37,
          "sum": 2276.7223954200745,
          "mean": 61.533037714056064,
          "median": 43.87299966812134,
          "p95": 149.55613331794734,
          "min": 15.297545433044434,
          "max": 162.43017101287842
        },
        "forks": {
          "n": 37,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 37,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 37,
          "sum": 37.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 37,
          "sum": 59129.0,
          "mean": 1598.081081081081,
          "median": 1200.0,
          "p95": 4094.0,
          "min": 400.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 37,
          "sum": 38.0,
          "mean": 1.027027027027027,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 37,
          "sum": 59091.0,
          "mean": 1597.054054054054,
          "median": 1199.0,
          "p95": 4093.0,
          "min": 399.0,
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
        "truncated_samples": 3,
        "truncated_fraction": 0.08108108108108109,
        "invalid_width_samples": 1,
        "forked_samples": 0
      },
      "historical_correct": 33,
      "historical_pass_at_1": 0.515625
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
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
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
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 24,
  "completed": 24,
  "missing": 0,
  "correct": 14,
  "pass_at_1_completed_only": 0.5833333333333334,
  "format_valid": 14,
  "format_fraction_completed_only": 0.5833333333333334,
  "executed_fork_samples": 0,
  "unfinished_thinking": 2,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
  "parallel_syntax_valid": 17,
  "parallel_execution_mismatch_samples": 7,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 13,
  "legacy_format_fraction_completed_only": 0.5416666666666666,
  "legacy_parallel_protocol_valid": 0,
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
    "completed": 24,
    "basic_valid": 14,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 7,
    "correct": 14
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.2916666666666667,
  "correct_and_basic_valid": 14,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 24,
      "sum": 40217.0,
      "mean": 1675.7083333333333,
      "median": 1286.0,
      "p95": 4094.0,
      "min": 374.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 24,
      "sum": 40217.0,
      "mean": 1675.7083333333333,
      "median": 1286.0,
      "p95": 4094.0,
      "min": 374.0,
      "max": 4094.0
    },
    "T_forced": {
      "n": 24,
      "sum": 48.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 24,
      "sum": 40265.0,
      "mean": 1677.7083333333333,
      "median": 1288.0,
      "p95": 4096.0,
      "min": 376.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 24,
      "sum": 40217.0,
      "mean": 1675.7083333333333,
      "median": 1286.0,
      "p95": 4094.0,
      "min": 374.0,
      "max": 4094.0
    },
    "generation_calls": {
      "n": 24,
      "sum": 31.0,
      "mean": 1.2916666666666667,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 2.0
    },
    "wall_seconds": {
      "n": 24,
      "sum": 1522.5200390815735,
      "mean": 63.43833496173223,
      "median": 49.87659692764282,
      "p95": 148.96543167829515,
      "min": 13.900334596633911,
      "max": 151.7487964630127
    },
    "forks": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 24,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 24,
      "sum": 24.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 24,
      "sum": 40217.0,
      "mean": 1675.7083333333333,
      "median": 1286.0,
      "p95": 4094.0,
      "min": 374.0,
      "max": 4094.0
    },
    "prefill_calls_inferred": {
      "n": 24,
      "sum": 31.0,
      "mean": 1.2916666666666667,
      "median": 1.0,
      "p95": 2.0,
      "min": 1.0,
      "max": 2.0
    },
    "decode_calls_inferred": {
      "n": 24,
      "sum": 40186.0,
      "mean": 1674.4166666666667,
      "median": 1284.5,
      "p95": 4093.0,
      "min": 373.0,
      "max": 4093.0
    },
    "widths": {
      "n": 7,
      "sum": 17.0,
      "mean": 2.4285714285714284,
      "median": 2.0,
      "p95": 3.6999999999999993,
      "min": 2.0,
      "max": 4.0
    },
    "width_histogram": {
      "2": 5,
      "3": 1,
      "4": 1
    },
    "truncated_samples": 3,
    "truncated_fraction": 0.125,
    "invalid_width_samples": 7,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 14,
      "sum": 18805.0,
      "mean": 1343.2142857142858,
      "median": 849.0,
      "p95": 2979.3999999999996,
      "min": 374.0,
      "max": 3216.0
    },
    "T_sampled": {
      "n": 14,
      "sum": 18805.0,
      "mean": 1343.2142857142858,
      "median": 849.0,
      "p95": 2979.3999999999996,
      "min": 374.0,
      "max": 3216.0
    },
    "T_forced": {
      "n": 14,
      "sum": 28.0,
      "mean": 2.0,
      "median": 2.0,
      "p95": 2.0,
      "min": 2.0,
      "max": 2.0
    },
    "T_assembled": {
      "n": 14,
      "sum": 18833.0,
      "mean": 1345.2142857142858,
      "median": 851.0,
      "p95": 2981.3999999999996,
      "min": 376.0,
      "max": 3218.0
    },
    "actual_generated_tokens": {
      "n": 14,
      "sum": 18805.0,
      "mean": 1343.2142857142858,
      "median": 849.0,
      "p95": 2979.3999999999996,
      "min": 374.0,
      "max": 3216.0
    },
    "generation_calls": {
      "n": 14,
      "sum": 14.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "wall_seconds": {
      "n": 14,
      "sum": 723.3735077381134,
      "mean": 51.6695362670081,
      "median": 32.8834308385849,
      "p95": 115.29524034261703,
      "min": 13.900334596633911,
      "max": 125.43480682373047
    },
    "forks": {
      "n": 14,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "rounds": {
      "n": 14,
      "sum": 0.0,
      "mean": 0.0,
      "median": 0.0,
      "p95": 0.0,
      "min": 0.0,
      "max": 0.0
    },
    "generation_turns": {
      "n": 14,
      "sum": 14.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "model_forward_calls_inferred": {
      "n": 14,
      "sum": 18805.0,
      "mean": 1343.2142857142858,
      "median": 849.0,
      "p95": 2979.3999999999996,
      "min": 374.0,
      "max": 3216.0
    },
    "prefill_calls_inferred": {
      "n": 14,
      "sum": 14.0,
      "mean": 1.0,
      "median": 1.0,
      "p95": 1.0,
      "min": 1.0,
      "max": 1.0
    },
    "decode_calls_inferred": {
      "n": 14,
      "sum": 18791.0,
      "mean": 1342.2142857142858,
      "median": 848.0,
      "p95": 2978.3999999999996,
      "min": 373.0,
      "max": 3215.0
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
  "historical_correct": 14,
  "historical_pass_at_1_completed_only": 0.5833333333333334,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 24,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 12,
      "completed": 12,
      "correct": 9,
      "pass_at_1": 0.75,
      "basic_valid": 9,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 10,
      "parallel_execution_mismatch_samples": 2,
      "correct_and_basic_valid": 9,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 22526.0,
          "mean": 1877.1666666666667,
          "median": 1972.5,
          "p95": 3611.0999999999995,
          "min": 449.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 22526.0,
          "mean": 1877.1666666666667,
          "median": 1972.5,
          "p95": 3611.0999999999995,
          "min": 449.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 22550.0,
          "mean": 1879.1666666666667,
          "median": 1974.5,
          "p95": 3613.0999999999995,
          "min": 451.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 22526.0,
          "mean": 1877.1666666666667,
          "median": 1972.5,
          "p95": 3611.0999999999995,
          "min": 449.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 14.0,
          "mean": 1.1666666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 868.8444089889526,
          "mean": 72.40370074907939,
          "median": 77.14445614814758,
          "p95": 137.27610216140747,
          "min": 17.065657377243042,
          "max": 151.7487964630127
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 22526.0,
          "mean": 1877.1666666666667,
          "median": 1972.5,
          "p95": 3611.0999999999995,
          "min": 449.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 14.0,
          "mean": 1.1666666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 22512.0,
          "mean": 1876.0,
          "median": 1971.0,
          "p95": 3610.0999999999995,
          "min": 448.0,
          "max": 4093.0
        },
        "widths": {
          "n": 2,
          "sum": 4.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "width_histogram": {
          "2": 2
        },
        "truncated_samples": 1,
        "truncated_fraction": 0.08333333333333333,
        "invalid_width_samples": 2,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 9,
          "sum": 13726.0,
          "mean": 1525.111111111111,
          "median": 1222.0,
          "p95": 3070.3999999999996,
          "min": 449.0,
          "max": 3216.0
        },
        "T_sampled": {
          "n": 9,
          "sum": 13726.0,
          "mean": 1525.111111111111,
          "median": 1222.0,
          "p95": 3070.3999999999996,
          "min": 449.0,
          "max": 3216.0
        },
        "T_forced": {
          "n": 9,
          "sum": 18.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 9,
          "sum": 13744.0,
          "mean": 1527.111111111111,
          "median": 1224.0,
          "p95": 3072.3999999999996,
          "min": 451.0,
          "max": 3218.0
        },
        "actual_generated_tokens": {
          "n": 9,
          "sum": 13726.0,
          "mean": 1525.111111111111,
          "median": 1222.0,
          "p95": 3070.3999999999996,
          "min": 449.0,
          "max": 3216.0
        },
        "generation_calls": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 9,
          "sum": 533.6518559455872,
          "mean": 59.294650660620796,
          "median": 47.082268953323364,
          "p95": 119.19507360458374,
          "min": 17.065657377243042,
          "max": 125.43480682373047
        },
        "forks": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 9,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 9,
          "sum": 13726.0,
          "mean": 1525.111111111111,
          "median": 1222.0,
          "p95": 3070.3999999999996,
          "min": 449.0,
          "max": 3216.0
        },
        "prefill_calls_inferred": {
          "n": 9,
          "sum": 9.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 9,
          "sum": 13717.0,
          "mean": 1524.111111111111,
          "median": 1221.0,
          "p95": 3069.3999999999996,
          "min": 448.0,
          "max": 3215.0
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
      "historical_correct": 9,
      "historical_pass_at_1": 0.75
    },
    "math": {
      "planned": 12,
      "completed": 12,
      "correct": 5,
      "pass_at_1": 0.4166666666666667,
      "basic_valid": 5,
      "basic_valid_fraction": 0.4166666666666667,
      "parallel_valid": 0,
      "parallel_syntax_valid": 7,
      "parallel_execution_mismatch_samples": 5,
      "correct_and_basic_valid": 5,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 12,
          "sum": 17691.0,
          "mean": 1474.25,
          "median": 844.0,
          "p95": 4094.0,
          "min": 374.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 12,
          "sum": 17691.0,
          "mean": 1474.25,
          "median": 844.0,
          "p95": 4094.0,
          "min": 374.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 12,
          "sum": 24.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 12,
          "sum": 17715.0,
          "mean": 1476.25,
          "median": 846.0,
          "p95": 4096.0,
          "min": 376.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 12,
          "sum": 17691.0,
          "mean": 1474.25,
          "median": 844.0,
          "p95": 4094.0,
          "min": 374.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 12,
          "sum": 17.0,
          "mean": 1.4166666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "wall_seconds": {
          "n": 12,
          "sum": 653.6756300926208,
          "mean": 54.47296917438507,
          "median": 32.18819582462311,
          "p95": 148.90204790830612,
          "min": 13.900334596633911,
          "max": 148.98920059204102
        },
        "forks": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 12,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 12,
          "sum": 12.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 12,
          "sum": 17691.0,
          "mean": 1474.25,
          "median": 844.0,
          "p95": 4094.0,
          "min": 374.0,
          "max": 4094.0
        },
        "prefill_calls_inferred": {
          "n": 12,
          "sum": 17.0,
          "mean": 1.4166666666666667,
          "median": 1.0,
          "p95": 2.0,
          "min": 1.0,
          "max": 2.0
        },
        "decode_calls_inferred": {
          "n": 12,
          "sum": 17674.0,
          "mean": 1472.8333333333333,
          "median": 843.0,
          "p95": 4093.0,
          "min": 373.0,
          "max": 4093.0
        },
        "widths": {
          "n": 5,
          "sum": 13.0,
          "mean": 2.6,
          "median": 2.0,
          "p95": 3.8,
          "min": 2.0,
          "max": 4.0
        },
        "width_histogram": {
          "2": 3,
          "3": 1,
          "4": 1
        },
        "truncated_samples": 2,
        "truncated_fraction": 0.16666666666666666,
        "invalid_width_samples": 5,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 5,
          "sum": 5079.0,
          "mean": 1015.8,
          "median": 798.0,
          "p95": 2081.2,
          "min": 374.0,
          "max": 2379.0
        },
        "T_sampled": {
          "n": 5,
          "sum": 5079.0,
          "mean": 1015.8,
          "median": 798.0,
          "p95": 2081.2,
          "min": 374.0,
          "max": 2379.0
        },
        "T_forced": {
          "n": 5,
          "sum": 10.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 5,
          "sum": 5089.0,
          "mean": 1017.8,
          "median": 800.0,
          "p95": 2083.2,
          "min": 376.0,
          "max": 2381.0
        },
        "actual_generated_tokens": {
          "n": 5,
          "sum": 5079.0,
          "mean": 1015.8,
          "median": 798.0,
          "p95": 2081.2,
          "min": 374.0,
          "max": 2379.0
        },
        "generation_calls": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 5,
          "sum": 189.72165179252625,
          "mean": 37.94433035850525,
          "median": 30.908689498901367,
          "p95": 76.4570261478424,
          "min": 13.900334596633911,
          "max": 87.2043571472168
        },
        "forks": {
          "n": 5,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 5,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 5,
          "sum": 5079.0,
          "mean": 1015.8,
          "median": 798.0,
          "p95": 2081.2,
          "min": 374.0,
          "max": 2379.0
        },
        "prefill_calls_inferred": {
          "n": 5,
          "sum": 5.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "decode_calls_inferred": {
          "n": 5,
          "sum": 5074.0,
          "mean": 1014.8,
          "median": 797.0,
          "p95": 2080.2,
          "min": 373.0,
          "max": 2378.0
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
      "historical_correct": 5,
      "historical_pass_at_1": 0.4166666666666667
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
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "questions_sha256": "0d925cc42ba83f2063c4691036cd2d88bca431882d92440bf4a1d43ffee9b35e",
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
  "suite": "24",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/lr-2e-4-trained-structured-24/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 98,
  "pass_at_1_completed_only": 0.765625,
  "format_valid": 55,
  "format_fraction_completed_only": 0.4296875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 25,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
  "gate_passed": false,
  "response_cap": 4096,
  "path_cap": 2048,
  "accuracy_gate": "at least one correct; no stronger accuracy threshold",
  "model": "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
  "parallel_syntax_valid": 128,
  "parallel_execution_mismatch_samples": 0,
  "parallel_valid_definition": "Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control",
  "format_schema_version": 2,
  "accuracy_schema_version": 2,
  "legacy_format_valid": 7,
  "legacy_format_fraction_completed_only": 0.0546875,
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
    "basic_valid": 55,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 98
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 53,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 357577.0,
      "mean": 2793.5703125,
      "median": 2755.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 8660.699485778809,
      "mean": 67.66171473264694,
      "median": 65.87486445903778,
      "p95": 101.0175164580345,
      "min": 11.80995774269104,
      "max": 104.2663037776947
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 33,
    "truncated_fraction": 0.2578125,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 237783.0,
      "mean": 2426.3571428571427,
      "median": 2287.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 5757.977805137634,
      "mean": 58.75487556262892,
      "median": 54.78069293498993,
      "p95": 97.86540901660918,
      "min": 11.80995774269104,
      "max": 104.20655298233032
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 6,
    "truncated_fraction": 0.061224489795918366,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 92,
  "historical_pass_at_1_completed_only": 0.71875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 53,
      "pass_at_1": 0.828125,
      "basic_valid": 48,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 165383.0,
          "mean": 2584.109375,
          "median": 2484.0,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 4025.7042763233185,
          "mean": 62.90162931755185,
          "median": 62.02750611305237,
          "p95": 100.48131618499755,
          "min": 11.80995774269104,
          "max": 103.48198652267456
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 122831.0,
          "mean": 2317.566037735849,
          "median": 2289.0,
          "p95": 3829.3999999999996,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 2986.7858057022095,
          "mean": 56.35444916419263,
          "median": 56.69348454475403,
          "p95": 93.92767610549926,
          "min": 11.80995774269104,
          "max": 100.35823440551758
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_fraction": 0.018867924528301886,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 52,
      "historical_pass_at_1": 0.8125
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 45,
      "pass_at_1": 0.703125,
      "basic_valid": 7,
      "basic_valid_fraction": 0.109375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 7,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 192194.0,
          "mean": 3003.03125,
          "median": 3329.5,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 4634.99520945549,
          "mean": 72.42180014774203,
          "median": 79.89138352870941,
          "p95": 101.24992128610612,
          "min": 30.205644607543945,
          "max": 104.2663037776947
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 23,
        "truncated_fraction": 0.359375,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 45,
          "sum": 90.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 45,
          "sum": 114952.0,
          "mean": 2554.488888888889,
          "median": 2226.0,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 45,
          "sum": 2771.191999435425,
          "mean": 61.58204443189833,
          "median": 53.02387237548828,
          "p95": 99.34497866630554,
          "min": 30.205644607543945,
          "max": 104.20655298233032
        },
        "forks": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 5,
        "truncated_fraction": 0.1111111111111111,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 40,
      "historical_pass_at_1": 0.625
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/summary.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "planned": 128,
  "completed": 128,
  "missing": 0,
  "correct": 98,
  "pass_at_1_completed_only": 0.765625,
  "format_valid": 55,
  "format_fraction_completed_only": 0.4296875,
  "executed_fork_samples": 0,
  "unfinished_thinking": 25,
  "gate_format_threshold": 0.8,
  "parallel_protocol_valid": 0,
  "parallel_protocol_fraction_completed_only": 0.0,
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
  "legacy_format_valid": 7,
  "legacy_format_fraction_completed_only": 0.0546875,
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
    "basic_valid": 55,
    "executed_fork_samples": 0,
    "valid_parallel_among_fork_samples": 0,
    "invalid_width_samples": 0,
    "correct": 98
  },
  "fork_coverage": 0.0,
  "valid_parallel_among_executed_forks": null,
  "invalid_width_fraction": 0.0,
  "correct_and_basic_valid": 53,
  "correct_and_parallel_valid": 0,
  "metrics_all": {
    "F": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 357577.0,
      "mean": 2793.5703125,
      "median": 2755.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 128,
      "sum": 357321.0,
      "mean": 2791.5703125,
      "median": 2753.0,
      "p95": 4094.0,
      "min": 485.0,
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
      "sum": 8670.530199289322,
      "mean": 67.73851718194783,
      "median": 67.27637326717377,
      "p95": 101.2674719929695,
      "min": 11.821501731872559,
      "max": 103.72609281539917
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 33,
    "truncated_fraction": 0.2578125,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "metrics_correct": {
    "F": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
    },
    "T_sampled": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 237783.0,
      "mean": 2426.3571428571427,
      "median": 2287.0,
      "p95": 4096.0,
      "min": 487.0,
      "max": 4096.0
    },
    "actual_generated_tokens": {
      "n": 98,
      "sum": 237587.0,
      "mean": 2424.3571428571427,
      "median": 2285.0,
      "p95": 4094.0,
      "min": 485.0,
      "max": 4094.0
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
      "sum": 5786.678912401199,
      "mean": 59.04774400409387,
      "median": 54.37870216369629,
      "p95": 97.6802416563034,
      "min": 11.821501731872559,
      "max": 101.63769960403442
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
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "prefill_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
    },
    "decode_calls_inferred": {
      "n": 0,
      "sum": 0.0,
      "mean": null,
      "median": null,
      "p95": null,
      "min": null,
      "max": null
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
    "truncated_samples": 6,
    "truncated_fraction": 0.061224489795918366,
    "invalid_width_samples": 0,
    "forked_samples": 0
  },
  "historical_correct": 92,
  "historical_pass_at_1_completed_only": 0.71875,
  "primary_metric": "Math-Verify final answer equivalence after removing only think markup; independent of think-format validity",
  "work_inference": {
    "measurement_status": "INFERRED from structured serial HF source; not measured GPU telemetry",
    "structured_trace_verified_samples": 0,
    "structured_trace_stat_mismatch_samples": 0,
    "native_forward_counts_available": false
  },
  "by_dataset": {
    "gsm": {
      "planned": 64,
      "completed": 64,
      "correct": 53,
      "pass_at_1": 0.828125,
      "basic_valid": 48,
      "basic_valid_fraction": 0.75,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 46,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 165383.0,
          "mean": 2584.109375,
          "median": 2484.0,
          "p95": 4096.0,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 165255.0,
          "mean": 2582.109375,
          "median": 2482.0,
          "p95": 4094.0,
          "min": 485.0,
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
          "sum": 4031.9193670749664,
          "mean": 62.99874011054635,
          "median": 62.15397250652313,
          "p95": 99.57860629558563,
          "min": 11.821501731872559,
          "max": 103.72609281539917
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 122831.0,
          "mean": 2317.566037735849,
          "median": 2289.0,
          "p95": 3829.3999999999996,
          "min": 487.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 53,
          "sum": 122725.0,
          "mean": 2315.566037735849,
          "median": 2287.0,
          "p95": 3827.3999999999996,
          "min": 485.0,
          "max": 4094.0
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
          "sum": 2998.4826543331146,
          "mean": 56.57514442137952,
          "median": 58.04424571990967,
          "p95": 94.60174126625061,
          "min": 11.821501731872559,
          "max": 100.9320170879364
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_fraction": 0.018867924528301886,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 52,
      "historical_pass_at_1": 0.8125
    },
    "math": {
      "planned": 64,
      "completed": 64,
      "correct": 45,
      "pass_at_1": 0.703125,
      "basic_valid": 7,
      "basic_valid_fraction": 0.109375,
      "parallel_valid": 0,
      "parallel_syntax_valid": 64,
      "parallel_execution_mismatch_samples": 0,
      "correct_and_basic_valid": 7,
      "correct_and_parallel_valid": 0,
      "metrics_all": {
        "F": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 192194.0,
          "mean": 3003.03125,
          "median": 3329.5,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 64,
          "sum": 192066.0,
          "mean": 3001.03125,
          "median": 3327.5,
          "p95": 4094.0,
          "min": 1274.0,
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
          "sum": 4638.6108322143555,
          "mean": 72.4782942533493,
          "median": 81.88068211078644,
          "p95": 101.50575227737427,
          "min": 30.713853120803833,
          "max": 102.92368364334106
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
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 23,
        "truncated_fraction": 0.359375,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "metrics_correct": {
        "F": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_sampled": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "T_forced": {
          "n": 45,
          "sum": 90.0,
          "mean": 2.0,
          "median": 2.0,
          "p95": 2.0,
          "min": 2.0,
          "max": 2.0
        },
        "T_assembled": {
          "n": 45,
          "sum": 114952.0,
          "mean": 2554.488888888889,
          "median": 2226.0,
          "p95": 4096.0,
          "min": 1276.0,
          "max": 4096.0
        },
        "actual_generated_tokens": {
          "n": 45,
          "sum": 114862.0,
          "mean": 2552.488888888889,
          "median": 2224.0,
          "p95": 4094.0,
          "min": 1274.0,
          "max": 4094.0
        },
        "generation_calls": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "wall_seconds": {
          "n": 45,
          "sum": 2788.1962580680847,
          "mean": 61.95991684595744,
          "median": 54.1926372051239,
          "p95": 100.30331106185912,
          "min": 30.713853120803833,
          "max": 101.63769960403442
        },
        "forks": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "rounds": {
          "n": 45,
          "sum": 0.0,
          "mean": 0.0,
          "median": 0.0,
          "p95": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "generation_turns": {
          "n": 45,
          "sum": 45.0,
          "mean": 1.0,
          "median": 1.0,
          "p95": 1.0,
          "min": 1.0,
          "max": 1.0
        },
        "model_forward_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "prefill_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
        },
        "decode_calls_inferred": {
          "n": 0,
          "sum": 0.0,
          "mean": null,
          "median": null,
          "p95": null,
          "min": null,
          "max": null
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
        "truncated_samples": 5,
        "truncated_fraction": 0.1111111111111111,
        "invalid_width_samples": 0,
        "forked_samples": 0
      },
      "historical_correct": 40,
      "historical_pass_at_1": 0.625
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
    "native_vllm_fast"
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
  "system_file": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
  "provenance": {
    "evaluator_sha256": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
    "questions_sha256": "f40af1afc5073be8e41e691f04f701a57dbd2c07ff5fa9a9256e675220674b5d",
    "generation_config_sha256": "2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2",
    "runtime_sha256": {
      "native_eos.py": "e8ff0eaa8f50e35e9db75c8f848da538f3615a69adc208a205589f06277d3ae3",
      "summary_metrics.py": "3eab70d837c464d490886866afc32cb965f4546d8a43a2daf8b1cbcef064f4c7",
      "runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
      "runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
      "runtime/verl/utils/parallel_structure.py": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    }
  },
  "system_sha256": "eff263864e35545cc737445e2dfd1053104a12689514315f16c1e210b952f802",
  "suite": "128",
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

- [work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/worker-exits.json](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/trained-native-128/worker-exits.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

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

- [work/experiments/instruct-token-warmup-20261010/export-audit-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/export-audit-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "export-audit",
  "started_at": "2026-10-10T08:19:25.084005+00:00",
  "command": [
    "${PROJECT_ROOT}/.venv/bin/python",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/audit_export.py"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/export-audit.log",
  "owned_process_group": 1250391,
  "heartbeat_at": "2026-10-10T08:19:35.107330+00:00",
  "returncode": 1,
  "finished_at": "2026-10-10T08:19:45.110961+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/format-loss-research-20261010/independent-diagnosis.json](../artifacts/work/experiments/instruct-token-warmup-20261010/format-loss-research-20261010/independent-diagnosis.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "stage": "independent_format_loss_diagnosis",
  "at": "2026-10-10T09:25:47.522053+00:00",
  "read_only_audit_no_GPU_or_approvals": true,
  "source_sha256": {
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/data.py": "7a9415bc70d8c237452a47dadb0c1b8ca5e9bbd8f4d877f3c1c599cc47315919",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/train.py": "bdeabce08d10423708fb0b21a2319b755616df34e5c8070145815b9d6ba0b28d",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/evaluate.py": "ce546b0bc74945b17f99cbd93fb3be1d3d54b4ed737445e15ac80157d8a9d6e8",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "e2d36f53ddd2157d1cc22beb167bad82f337f2d4ff560cda066712bb0fd0d14e",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/runtime/verl/workers/rollout/vllm_rollout/structured_worker.py": "18a98bf021b8907167d3188c84274e71e18d7699d76693bb21e6ad2bcf763e21",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/structured-runtime-smoke24/scores.jsonl": "9a266e35d08ed2358d2f1e1ee5bafce8cec9a872ee511a456945f28c3f3f2d77",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/structured-runtime-smoke24/manifest.json": "a84b19555e07245d38f59440b80910d1a4cea6b919ee6f1a51b3b8c39c3bca09",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/native-runtime-smoke24/scores.jsonl": "0d58f09bb4500a85fef022451a8ee5d714091e05e1044834a29ff6c7c3fc4bee"
  },
  "actual24": {
    "model": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
    "correct": 12,
    "format_valid_current_scorer": 11,
    "parallel_protocol_valid": 0,
    "executed_forks_samples": 3,
    "invalid_width_samples": [
      0,
      8,
      4,
      12,
      1,
      2,
      10,
      18,
      15,
      23
    ],
    "parallel_after_think_close_samples": [
      0,
      8,
      16,
      4,
      12,
      1,
      17,
      2,
      10,
      18,
      15,
      23
    ],
    "fork_samples_after_think_close": [
      16,
      17
    ],
    "raw_vs_assembled_terminal_mismatches": [
      {
        "sample_index": 16,
        "phase": "summary",
        "raw_terminal_id": 151645,
        "assembled_terminal_id": 151674
      },
      {
        "sample_index": 21,
        "phase": "path",
        "raw_terminal_id": 151671,
        "assembled_terminal_id": 151670
      },
      {
        "sample_index": 21,
        "phase": "summary",
        "raw_terminal_id": 151671,
        "assembled_terminal_id": 151674
      },
      {
        "sample_index": 21,
        "phase": "summary",
        "raw_terminal_id": 151645,
        "assembled_terminal_id": 151674
      },
      {
        "sample_index": 17,
        "phase": "summary",
        "raw_terminal_id": 151645,
        "assembled_terminal_id": 151674
      }
    ]
  },
  "diagnosis": [
    "Actual24 forced think opener is present once and promptthink false: no observed duplicated/missing opener explains failures.",
    "Model samples native reasoning then think-close, then protocol in answer phase. Runtime main does not track think state and accepts any Parallel opener even after think-close. This is permissive protocol enforcement, not runtime movement of sampled think-close.",
    "Width decoder requires exact digit2..8+newline within4 tokens. Leading spaces/newlines terminate or exhaust header: observed10 failures.",
    "strict_format checks balanced counts and final-after-think but fails to require all XML controls inside think or Plan-ID/width consistency; use stronger diagnostic validator without changing historical metrics.",
    "Path/summary stop normalization substitutes wrong sampled controls/EOS to expected closing tags while marking them sampled. Actual24 contains5 mismatching terminal tokens; forced-tag zero mask policy must not count normalization as observed correct policy prediction."
  ],
  "structural_target_policy": {
    "predicted_parallel_open": "include single token Parallel opener",
    "predicted_width": "include entire exact [2-8]+newline after Parallel, all BPE slots by offsets",
    "plan": "include Plan: syntax, linebreaks, numbered ID+colon prefixes; specify separately whether assignment prose is included",
    "predicted_path_close": "include Path-close token when teacher target, despite runtime fallback injection",
    "predicted_summary_close": "include Summary-close token when teacher target, despite runtime fallback injection",
    "native_think_close": "include native think-close; train correct placement after final Summary and before Final Answer",
    "final_boundary": "optionally explicit Final Answer prefix plus native im_end as separate class; otherwise onlyparallel cannot teach final layout",
    "always_zero": "prompt/forced think opener, Path+ID+newline headers, Parallel-close+newline+Summary-open compiler bridge, masked forced whitespace spills; final weight must be target_mask multiplied by structural-or-semantic factor",
    "shift": "weights index TARGET slots and shift exactly once weights[1:] alongside logits[:-1] and ids[1:]"
  },
  "weighted_loss_pitfalls": [
    "Onlyparallel needs precise public definition: XML-token-only loses width, Plan and think-close supervision; broad structural schema is a different objective and must be named.",
    "Fivefold structural weights with sum(weight) denominator changes every semantic gradient scale relative to baseline; define whether weighted mean normalization or baseline token denominator is intended and record both normalized objectives.",
    "Per-example weighted mean then batch mean differs from global weighted token mean; retain existing sample averaging unless change intentional.",
    "Forced boundary BPE whitespace spill must remain0 even if newline is structural.",
    "Keep loss finite and positive denominator; report count/mass by target class, structuralCE and semanticCE independently.",
    "Plan/think-close/native digits remain frozen output rows under six-row training. Trainable new-tag embeddings in system and prior protocol context can steer hidden states, and new-tag logits compete in softmax, but six rows do not provide full model capacity; format-only convergence cannot be promised.",
    "Six-row tied model applies gradients through forced tag input embeddings despite forced TARGET loss0; this is expected and needed.",
    "Do not silently fix runtime normalization or constrain decode while comparing loss ablations; treat runtime enforcement change as separate arm/protocol."
  ],
  "recommended_cpu_tests": [
    "forced slots always0 under all modes, weights exactly1 baseline and5 structural for weighted mode",
    "target shift proof on known token/offset boundaries and whitespace spill",
    "Plan-width IDs and all controls inside think in strict diagnostic parser",
    "all targets finite and no semantic tokens accidentally weighted via BPE boundary",
    "sequential samples without parallel have explicit nonempty structural fallback or consciously rejected zero-denominator",
    "source-reversal and frozen-pins unaffected by isolated research code"
  ]
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/initial-structured-128-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/initial-structured-128-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "initial-structured-128",
  "started_at": "2026-10-10T09:22:45.765849+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/init-model",
    "--name",
    "initial-structured-128",
    "--suite",
    "128",
    "--mode",
    "structured",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/initial-structured-128.log",
  "owned_process_group": 1258165,
  "heartbeat_at": "2026-10-10T09:49:36.496917+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T09:49:46.500174+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/native-runtime-smoke24-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/native-runtime-smoke24-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "native-runtime-smoke24",
  "started_at": "2026-10-10T08:25:13.382350+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
    "--name",
    "native-runtime-smoke24",
    "--suite",
    "24",
    "--mode",
    "native",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/native-runtime-smoke24.log",
  "owned_process_group": 1250944,
  "heartbeat_at": "2026-10-10T08:30:33.531578+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T08:30:43.535688+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/original-native-128-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/original-native-128-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "original-native-128",
  "started_at": "2026-10-10T08:40:34.148442+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model",
    "--name",
    "original-native-128",
    "--suite",
    "128",
    "--mode",
    "native",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/original-native-128.log",
  "owned_process_group": 1253883,
  "heartbeat_at": "2026-10-10T09:01:24.699063+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T09:01:34.703637+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/prior-postexport-controller-status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/prior-postexport-controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "failed",
  "at": "2026-10-10T08:19:45.114699+00:00",
  "error": "AssertionError(('export-audit', 1))"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/prior-waiting-controller-status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/prior-waiting-controller-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "awaiting_root_smoke_review",
  "at": "2026-10-10T07:59:14.836465+00:00",
  "smoke_gate": "smoke-gate.json"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/production-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/production-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "production",
  "started_at": "2026-10-10T08:05:34.599574+00:00",
  "command": [
    "${PROJECT_ROOT}/.venv/bin/python",
    "-m",
    "torch.distributed.run",
    "--standalone",
    "--nnodes=1",
    "--nproc_per_node=8",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/train.py",
    "--stage",
    "production"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/production.log",
  "owned_process_group": 1249143,
  "heartbeat_at": "2026-10-10T08:19:15.062587+00:00",
  "training_progress": {
    "state": "running",
    "at": "2026-10-10T08:18:54.336074+00:00",
    "step": 129,
    "target_steps": 129,
    "epoch": 3,
    "loss": 0.8920596912503242,
    "row_grad_norm": 2.0427489280700684,
    "lr": 5e-05,
    "mean_input_tokens": 4104.5,
    "mean_supervised_tokens": 1430.5,
    "row_update_l2": 1.223875880241394,
    "elapsed_seconds": 779.9456103732809,
    "estimated_remaining_seconds": 0.0,
    "trainable_parameters": 15360,
    "frozen_parameter_versions_unchanged": true
  },
  "returncode": 0,
  "finished_at": "2026-10-10T08:19:25.067600+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/runs/production/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/runs/production/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:19:18.480519+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 804.090093947947,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/runs/production/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:19:18.480519+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 804.090093947947,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/runs/smoke/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/runs/smoke/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T07:59:08.696888+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 44.27634390164167,
  "final": null
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/runs/smoke/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/runs/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T07:59:08.696888+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 44.27634390164167,
  "final": null
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/smoke-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/smoke-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "smoke",
  "started_at": "2026-10-10T07:58:04.797610+00:00",
  "command": [
    "${PROJECT_ROOT}/.venv/bin/python",
    "-m",
    "torch.distributed.run",
    "--standalone",
    "--nnodes=1",
    "--nproc_per_node=8",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/train.py",
    "--stage",
    "smoke"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/smoke.log",
  "owned_process_group": 1248046,
  "heartbeat_at": "2026-10-10T07:59:04.821632+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T07:59:14.825628+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "interrupted_for_weighted_sft",
  "stage": "trained-structured-128",
  "started_at": "2026-10-10T09:49:46.714164+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
    "--name",
    "trained-structured-128",
    "--suite",
    "128",
    "--mode",
    "structured",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/trained-structured-128.log",
  "owned_process_group": 1264150,
  "heartbeat_at": "2026-10-10T09:55:06.845465+00:00",
  "interrupted_at": "2026-10-10T09:55:13.536552+00:00",
  "handoff_receipt": "${PROJECT_ROOT}/work/experiments/format-loss-20261010/owned-eval-handoff.json"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/structured-runtime-smoke24-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/structured-runtime-smoke24-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "structured-runtime-smoke24",
  "started_at": "2026-10-10T08:30:43.757656+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
    "--name",
    "structured-runtime-smoke24",
    "--suite",
    "24",
    "--mode",
    "structured",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/structured-runtime-smoke24.log",
  "owned_process_group": 1251888,
  "heartbeat_at": "2026-10-10T08:35:03.883090+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T08:35:13.886675+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/trained-native-128-process-result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/trained-native-128-process-result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "running",
  "stage": "trained-native-128",
  "started_at": "2026-10-10T09:01:34.914008+00:00",
  "command": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/runs/production/final",
    "--name",
    "trained-native-128",
    "--suite",
    "128",
    "--mode",
    "native",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt"
  ],
  "log": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/trained-native-128.log",
  "owned_process_group": 1256297,
  "heartbeat_at": "2026-10-10T09:22:35.557794+00:00",
  "returncode": 0,
  "finished_at": "2026-10-10T09:22:45.560887+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/pipeline-status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/pipeline-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "started_at": "2026-10-10T08:44:34.453431+00:00",
  "variant": "lr-1e-3",
  "ready_sha256": "2e3ecb8ec26d9d54f329132b959b9a7b683e207b4863fe790d460b480c63ed29",
  "pipeline_sha256": "d4a951c40b48b9419eac521c026e123d7a27b72b7b7c62365fc0738a6417603d",
  "state": "completed",
  "completed": [
    {
      "label": "training-smoke",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/run_train.sh",
        "smoke"
      ],
      "finished_at": "2026-10-10T08:46:00.404700+00:00"
    },
    {
      "label": "production",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/run_train.sh",
        "production"
      ],
      "finished_at": "2026-10-10T09:21:29.369311+00:00"
    },
    {
      "label": "export-audit",
      "returncode": 0,
      "argv": [
        "${PROJECT_ROOT}/work/experiments/night-20261010/cloud/tmp2/runtime/bin/python",
        "-B",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/audit_export.py"
      ],
      "finished_at": "2026-10-10T09:21:52.065486+00:00"
    },
    {
      "label": "lr-1e-3-trained-native-24",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
        "--name",
        "lr-1e-3-trained-native-24",
        "--suite",
        "24",
        "--mode",
        "native"
      ],
      "finished_at": "2026-10-10T09:27:00.687189+00:00"
    },
    {
      "label": "lr-1e-3-trained-structured-24",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--name",
        "lr-1e-3-trained-structured-24",
        "--suite",
        "24",
        "--mode",
        "structured"
      ],
      "finished_at": "2026-10-10T09:30:48.113552+00:00"
    },
    {
      "label": "lr-1e-3-trained-native-128",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
        "--name",
        "lr-1e-3-trained-native-128",
        "--suite",
        "128",
        "--mode",
        "native"
      ],
      "finished_at": "2026-10-10T09:56:56.390003+00:00"
    },
    {
      "label": "lr-1e-3-trained-structured-128",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--name",
        "lr-1e-3-trained-structured-128",
        "--suite",
        "128",
        "--mode",
        "structured"
      ],
      "finished_at": "2026-10-10T10:17:58.203410+00:00"
    }
  ],
  "production_from_canonical_mean_init": true,
  "only_six_rows": true,
  "base_learning_rate": 0.001,
  "commands": {
    "smoke": [
      "bash",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/run_train.sh",
      "smoke"
    ],
    "production_AFTER_ROOT_SMOKE_REVIEW": [
      "bash",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/run_train.sh",
      "production"
    ],
    "export_audit": [
      "${PROJECT_ROOT}/work/experiments/night-20261010/cloud/tmp2/runtime/bin/python",
      "-B",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/audit_export.py"
    ]
  },
  "at": "2026-10-10T10:17:58.534826+00:00",
  "active": null,
  "argv": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
    "--name",
    "lr-1e-3-trained-structured-128",
    "--suite",
    "128",
    "--mode",
    "structured"
  ],
  "active_pid": null,
  "approval_request": null,
  "approvals": {
    "training_smoke": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/root-smoke-approved.json",
      "sha256": "df506f84b2e87d0d12f178112e3887c60100ec45acd82748a7018b5d8cb78f39",
      "independent_review_path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/independent-actual-smokes-review-mac-20261010.json",
      "independent_review_sha256": "ad00811c852cfd1e57787666990b9aa27693168918e150982ceddd2272d8ace9"
    },
    "inference_smoke": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/root-inference-approved.json",
      "sha256": "c8de8da613235308d78ffa97e1f745cf4d1f7adf8b25ff55808113215c472b18",
      "independent_review_path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/independent-actual-inference-review-lr-1e-3-mac-20261010.json",
      "independent_review_sha256": "6eaabbbc3c09693cdd9f2b3012928acdd1ca2f06056af9b5dea2f8ef29bb1aee"
    }
  },
  "finished_at": "2026-10-10T10:17:58.534813+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:21:24.590155+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 806.5598135981709,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:21:24.590155+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 806.5598135981709,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:45:55.744408+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 60.42666188068688,
  "final": null
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:45:55.744408+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 60.42666188068688,
  "final": null
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/pipeline-status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/pipeline-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "started_at": "2026-10-10T08:44:32.718378+00:00",
  "variant": "lr-2e-4",
  "ready_sha256": "8431d950fdc4682ddac20ce5a1f180d281f5bceb0e743aeee5c86efadc090fd6",
  "pipeline_sha256": "d4a951c40b48b9419eac521c026e123d7a27b72b7b7c62365fc0738a6417603d",
  "state": "completed",
  "completed": [
    {
      "label": "training-smoke",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/run_train.sh",
        "smoke"
      ],
      "finished_at": "2026-10-10T08:45:45.693033+00:00"
    },
    {
      "label": "production",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/run_train.sh",
        "production"
      ],
      "finished_at": "2026-10-10T09:21:41.990914+00:00"
    },
    {
      "label": "export-audit",
      "returncode": 0,
      "argv": [
        "${PROJECT_ROOT}/work/experiments/night-20261010/cloud/tmp3/runtime/bin/python",
        "-B",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/audit_export.py"
      ],
      "finished_at": "2026-10-10T09:22:02.915189+00:00"
    },
    {
      "label": "lr-2e-4-trained-native-24",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
        "--name",
        "lr-2e-4-trained-native-24",
        "--suite",
        "24",
        "--mode",
        "native"
      ],
      "finished_at": "2026-10-10T09:27:21.573340+00:00"
    },
    {
      "label": "lr-2e-4-trained-structured-24",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--name",
        "lr-2e-4-trained-structured-24",
        "--suite",
        "24",
        "--mode",
        "structured"
      ],
      "finished_at": "2026-10-10T09:34:23.418368+00:00"
    },
    {
      "label": "lr-2e-4-trained-native-128",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/math-system.txt",
        "--name",
        "lr-2e-4-trained-native-128",
        "--suite",
        "128",
        "--mode",
        "native"
      ],
      "finished_at": "2026-10-10T09:59:06.736451+00:00"
    },
    {
      "label": "lr-2e-4-trained-structured-128",
      "returncode": 0,
      "argv": [
        "bash",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
        "--model",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
        "--system-file",
        "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
        "--name",
        "lr-2e-4-trained-structured-128",
        "--suite",
        "128",
        "--mode",
        "structured"
      ],
      "finished_at": "2026-10-10T10:24:38.956798+00:00"
    }
  ],
  "production_from_canonical_mean_init": true,
  "only_six_rows": true,
  "base_learning_rate": 0.0002,
  "commands": {
    "smoke": [
      "bash",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/run_train.sh",
      "smoke"
    ],
    "production_AFTER_ROOT_SMOKE_REVIEW": [
      "bash",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/run_train.sh",
      "production"
    ],
    "export_audit": [
      "${PROJECT_ROOT}/work/experiments/night-20261010/cloud/tmp3/runtime/bin/python",
      "-B",
      "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/audit_export.py"
    ]
  },
  "at": "2026-10-10T10:24:40.891892+00:00",
  "active": null,
  "argv": [
    "bash",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh",
    "--model",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final",
    "--system-file",
    "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt",
    "--name",
    "lr-2e-4-trained-structured-128",
    "--suite",
    "128",
    "--mode",
    "structured"
  ],
  "active_pid": null,
  "approval_request": null,
  "approvals": {
    "training_smoke": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/root-smoke-approved.json",
      "sha256": "08bd219f4942421b8127876fb81b5d10b3d5125d39869a18cef3dbf6b4dcad10",
      "independent_review_path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/independent-actual-smokes-review-mac-20261010.json",
      "independent_review_sha256": "ad00811c852cfd1e57787666990b9aa27693168918e150982ceddd2272d8ace9"
    },
    "inference_smoke": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/root-inference-approved.json",
      "sha256": "624d407bcb5b6c3d93a6f4a9bf8656a40a963622f9e9b8046a50229da1146351",
      "independent_review_path": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/independent-actual-inference-review-lr-2e-4-mac-20261010.json",
      "independent_review_sha256": "6be480c93ebdc9ada630212de3e3b408ab9b696dc0ce464ddd5873afea5c2b0c"
    }
  },
  "finished_at": "2026-10-10T10:24:40.891876+00:00"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:21:37.253636+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 811.315627200529,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T09:21:37.253636+00:00",
  "steps": 129,
  "epochs": 3,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 811.315627200529,
  "final": "${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/production/final"
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/metrics.jsonl](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/metrics.jsonl) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/result.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/result.json) — remote_nfs, снимок 2026-10-12T17:50:26.429011+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:45:41.261029+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 47.59587815217674,
  "final": null
}
```

</details>

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/status.json](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/runs/smoke/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "complete",
  "at": "2026-10-10T08:45:41.261029+00:00",
  "steps": 2,
  "epochs": 1,
  "trainable_parameters": 15360,
  "only_six_rows_updated": true,
  "all_other_parameters_frozen_version_checks_passed": true,
  "elapsed_seconds": 47.59587815217674,
  "final": null
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/controller.py](../artifacts/work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/train.py](../artifacts/work/experiments/instruct-token-warmup-20261010/attempts/01-ddp-version-counter/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/controller.py](../artifacts/work/experiments/instruct-token-warmup-20261010/controller.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/data.py](../artifacts/work/experiments/instruct-token-warmup-20261010/data.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh](../artifacts/work/experiments/instruct-token-warmup-20261010/evaluations/run_eval.sh) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/train.py](../artifacts/work/experiments/instruct-token-warmup-20261010/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/data.py](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/data.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/train.py](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/data.py](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/data.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/train.py](../artifacts/work/experiments/instruct-token-warmup-20261010/variants/lr-2e-4/train.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
