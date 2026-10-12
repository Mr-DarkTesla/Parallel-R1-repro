# work/experiments/rl-readiness-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-readiness-20261010/base-final-sealed-manifest.json](../artifacts/work/experiments/rl-readiness-20261010/base-final-sealed-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "passed": true,
  "model": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
  "created_at": "2026-10-11T00:10:36.174961+00:00",
  "actual_weight_shards": [
    "model-00001-of-00002.safetensors",
    "model-00002-of-00002.safetensors"
  ],
  "tensor_keys": 398,
  "total_weight_file_bytes": 8044981992,
  "files": {
    "added_tokens.json": {
      "sha256": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569",
      "bytes": 844
    },
    "chat_template.jinja": {
      "sha256": "5104cde78ab23e430f35fc626ae3e547504644a371dfa9ef6b8ce7bb40e7d30a",
      "bytes": 249
    },
    "config.json": {
      "sha256": "8b21d7e0d9e60e6ffa78001206a049ebc665c49fa6d4a158b91d176b834263f3",
      "bytes": 1542
    },
    "generation_config.json": {
      "sha256": "8a47fb71ce00121a7bb199fd65ec641b15518d902d8a868f693ae86f0aa81984",
      "bytes": 117
    },
    "model-00001-of-00002.safetensors": {
      "sha256": "7f6c3614e019aad7b7d55dcdc81ff89b80be637191930423c8e24ed02d8e779a",
      "bytes": 4967215360
    },
    "model-00002-of-00002.safetensors": {
      "sha256": "a4c4921e71a1bdcd220e424758383435848eb88d715e5e279b0db00f27dfaffd",
      "bytes": 3077766632
    },
    "model.safetensors.index.json": {
      "sha256": "a4552ba4015e525d61298de02b8b586eaab32ff08b6eac266303c9306edf5392",
      "bytes": 32854
    },
    "special_tokens_map.json": {
      "sha256": "94c1690bfeeb9d6c26e2fda1fb655a843dbc2f0fca442f8154413138292502e1",
      "bytes": 433
    },
    "tokenizer.json": {
      "sha256": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7",
      "bytes": 11423769
    },
    "tokenizer_config.json": {
      "sha256": "f34e5f6291309b8a663fb4a7cf48a8f748766fa5e3aeeaf8efeded3f56e17b1e",
      "bytes": 6279
    },
    "vocab.json": {
      "sha256": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
      "bytes": 2776833
    }
  },
  "manifest_scope": "Exact original fullBasefinal weights/config/tokenizer/template; verifybeforeeachproductionlaunch"
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/rl-readiness-20261010/readiness-status.json](../artifacts/work/experiments/rl-readiness-20261010/readiness-status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "base_sft_training_attention": "structured 4D additive mask with isolated same-round siblings, shared count header, merged suffix",
  "base_sft_positions": "repeated per sibling, continuation at longest sibling end+1",
  "prompt_template": "Instruction/Problem/Solution, no think",
  "response_mask_policy": "Sampled raw actions1; forcedheaders,synchronizationbridges,padding0; prompt excluded by response scope",
  "checkpoint": "${PROJECT_ROOT}/work/experiments/base-format-20261010/runs/production/final",
  "hashes": {
    "work/experiments/base-format-20261010/code/verl/trainer/fsdp_parallel_sft_trainer.py": "4ae8a56333a41d0bb9fd5f8b9f08b611abe48489390ecbb2b94140eb435bd4e2",
    "work/experiments/base-format-20261010/code/verl/utils/dataset/parallel_thinking_sft_dataset.py": "862ce8ba02023eca6eb69cd9726f4dc18b65a24f66cea5935de463bee5800d35",
    "work/experiments/base-format-20261010/code/verl/utils/parallel_structure.py": "f183fe9189592c99862bfbb6260737fe86fd1907c0cb80b7eb03dc416af0dedf",
    "work/experiments/base-format-20261010/runs/production/final/config.json": "8b21d7e0d9e60e6ffa78001206a049ebc665c49fa6d4a158b91d176b834263f3",
    "work/experiments/base-format-20261010/runs/production/final/chat_template.jinja": "5104cde78ab23e430f35fc626ae3e547504644a371dfa9ef6b8ce7bb40e7d30a",
    "verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py": "2e63fe62b7ff6c5f1e16424fc6d4987727fed98cb57899bacbdf9370812e4ca9",
    "verl/verl/workers/actor/dp_actor.py": "3ae20e77fe5395e11229962ffdbeab7a544fd089f2427289b295211db05900b4"
  },
  "legacy_blockers": [
    "Runtime injectedtags response_mask1",
    "Fixedwidth+chat template incompatible adaptiveBase",
    "Causal rollout vs structured actor probabilities",
    "Recomputed old_logprobs cannot prove decoder parity"
  ],
  "selected_fix": "Standalone HF structured rollout and exact per-call replay, no legacy trainer dependencies",
  "cpu_pass": true,
  "loop_pass": true,
  "bf16_gpu_pass": false,
  "fp32_gpu_pending": false,
  "launch_readiness": false,
  "fp32_gpu_pass": true,
  "fp32_precision": "highest,TF32disabled,FULLFP32 decoder andactor",
  "gpu_max_abs_logp_delta": 0.00011444091796875,
  "gpu_mean_abs_logp_delta": 5.646211775456322e-06,
  "gpu_p95_abs_logp_delta": 3.0517578125e-05,
  "gpu_call_pairs": 105,
  "remaining": "Actual8GPUdistributedoptimizer/actor-sampling smoke and proof; no automaticproductionrelease"
}
```

</details>
