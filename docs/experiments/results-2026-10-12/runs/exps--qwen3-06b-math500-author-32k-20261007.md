# exps/qwen3-06b-math500-author-32k-20261007

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [exps/qwen3-06b-math500-author-32k-20261007/manifest-single-gpu.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/manifest-single-gpu.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "created": "2026-10-07T11:37:19.776796+00:00",
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "weights_sha256": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b",
  "source_dataset": "HuggingFaceH4/MATH-500",
  "questions": 500,
  "profiles": {
    "instant": {
      "temperature": 0.7,
      "top_p": 0.8,
      "top_k": 20,
      "min_p": 0.0,
      "presence_penalty": 1.5
    },
    "reasoning": {
      "temperature": 0.6,
      "top_p": 0.95,
      "top_k": 20,
      "min_p": 0.0,
      "presence_penalty": 0.0
    }
  },
  "samples_per_question": 1,
  "max_output_tokens": 32768,
  "max_model_len": 40960,
  "prompt_instruction": "Please reason step by step, and put your final answer within \\boxed{}.",
  "native_chat_template": true,
  "parallel_r1": false,
  "seed": 42,
  "dtype": "bfloat16",
  "tensor_parallel_size": 1,
  "gpus_per_run": 1,
  "sequential_modes": true,
  "engine": {
    "max_num_seqs": 32,
    "max_num_batched_tokens": 8192,
    "enable_chunked_prefill": true,
    "gpu_memory_utilization": 0.85
  },
  "scoring": "Math-Verify 0.8.0 symbolic equivalence, reference-blind final answer extraction",
  "source_sha256": "32317851fa9be3c3d949c4709c18ec3b40c0efbe79b5bdef72a0addad1446658",
  "dataset_sha256": "fbb1fc6a839247042311f7695a40dc963631ba01885a665f3725b2f6acbe2b96",
  "versions": {
    "vllm": "0.8.5.post1",
    "transformers": "4.53.2"
  },
  "references": [
    "https://arxiv.org/html/2505.09388v1#S4.SS4",
    "https://huggingface.co/Qwen/Qwen3-0.6B#best-practices"
  ],
  "note": "Reproduces published decoding settings and recommended prompt. The technical report does not specify its complete MATH-500 grading implementation; Math-Verify is explicitly identified here."
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/manifest.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "created": "2026-10-07T11:37:19.776796+00:00",
  "model": "Qwen/Qwen3-0.6B",
  "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
  "weights_sha256": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b",
  "source_dataset": "HuggingFaceH4/MATH-500",
  "questions": 500,
  "profiles": {
    "instant": {
      "temperature": 0.7,
      "top_p": 0.8,
      "top_k": 20,
      "min_p": 0.0,
      "presence_penalty": 1.5
    },
    "reasoning": {
      "temperature": 0.6,
      "top_p": 0.95,
      "top_k": 20,
      "min_p": 0.0,
      "presence_penalty": 0.0
    }
  },
  "samples_per_question": 1,
  "max_output_tokens": 32768,
  "max_model_len": 40960,
  "prompt_instruction": "Please reason step by step, and put your final answer within \\boxed{}.",
  "native_chat_template": true,
  "parallel_r1": false,
  "seed": 42,
  "dtype": "bfloat16",
  "tensor_parallel_size": 1,
  "gpus_per_run": 1,
  "sequential_modes": true,
  "engine": {
    "max_num_seqs": 32,
    "max_num_batched_tokens": 8192,
    "enable_chunked_prefill": true,
    "gpu_memory_utilization": 0.85
  },
  "scoring": "Math-Verify 0.8.0 symbolic equivalence, reference-blind final answer extraction",
  "source_sha256": "32317851fa9be3c3d949c4709c18ec3b40c0efbe79b5bdef72a0addad1446658",
  "dataset_sha256": "fbb1fc6a839247042311f7695a40dc963631ba01885a665f3725b2f6acbe2b96",
  "versions": {
    "vllm": "0.8.5.post1",
    "transformers": "4.53.2"
  },
  "references": [
    "https://arxiv.org/html/2505.09388v1#S4.SS4",
    "https://huggingface.co/Qwen/Qwen3-0.6B#best-practices"
  ],
  "note": "Reproduces published decoding settings and recommended prompt. The technical report does not specify its complete MATH-500 grading implementation; Math-Verify is explicitly identified here.",
  "execution_revision": "2026-10-07T11:57:22.981111+00:00",
  "total_gpus": 8,
  "worker_gpus": 1,
  "replicas_per_unfinished_mode": 8,
  "preserve_completed_modes": true,
  "scheduler": "Eight disjoint task shards, ordinary inference",
  "max_num_seqs_per_replica": 16,
  "streaming_completed_answers": true
}
```

</details>

## Метрики и полнота результатов

- [exps/qwen3-06b-math500-author-32k-20261007/instant/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/instant/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T11:50:04.930846+00:00",
  "answers": 500,
  "expected": 500
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/instant/summary.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/instant/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "mode": "instant",
  "questions": 500,
  "answers": 500,
  "samples_per_question": 1,
  "accuracy": 0.51,
  "correct": 255,
  "ci95": [
    0.4662736879310782,
    0.5535738252596908
  ],
  "ci_method": "Wilson two-sided 95%",
  "invalid_answers": 0,
  "scorer_errors": [],
  "finish_reasons": {
    "stop": 500,
    "length": 0,
    "abort": 0
  },
  "output_tokens": 310036,
  "scoring": "Final-answer extraction independent of gold, Math-Verify 0.8.0 symbolic equivalence",
  "traces_sha256": "0d8846cb8704ae36c21b33f662d5faa7aa690ca491b696f6ddb8d190662bdad9",
  "extraction_tests": 10
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/0/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/0/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:07:33.764476+00:00",
  "engine_ready": "2026-10-07T11:58:48.757363+00:00",
  "answers": 63,
  "expected": 63,
  "pending": 0,
  "elapsed_generation_seconds": 525.0070984447375,
  "generated_tokens": 446390,
  "finished_tokens": 446390,
  "mean_finished_tokens": 7085.555555555556,
  "max_finished_tokens": 32768,
  "active_lengths": [],
  "output_tokens_per_second": 850.2551704964942
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/1/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/1/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:06:11.428649+00:00",
  "engine_ready": "2026-10-07T11:58:48.839260+00:00",
  "answers": 63,
  "expected": 63,
  "pending": 0,
  "elapsed_generation_seconds": 442.5893783485517,
  "generated_tokens": 361765,
  "finished_tokens": 361765,
  "mean_finished_tokens": 5742.3015873015875,
  "max_finished_tokens": 31306,
  "active_lengths": [],
  "output_tokens_per_second": 817.3829235348251
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/2/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/2/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:05:50.133650+00:00",
  "engine_ready": "2026-10-07T11:58:48.526873+00:00",
  "answers": 63,
  "expected": 63,
  "pending": 0,
  "elapsed_generation_seconds": 421.60677912831306,
  "generated_tokens": 331168,
  "finished_tokens": 331168,
  "mean_finished_tokens": 5256.6349206349205,
  "max_finished_tokens": 32768,
  "active_lengths": [],
  "output_tokens_per_second": 785.4902159891773
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/3/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/3/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:05:28.423956+00:00",
  "engine_ready": "2026-10-07T11:58:48.499460+00:00",
  "answers": 63,
  "expected": 63,
  "pending": 0,
  "elapsed_generation_seconds": 399.9244940262288,
  "generated_tokens": 348763,
  "finished_tokens": 348763,
  "mean_finished_tokens": 5535.920634920635,
  "max_finished_tokens": 27848,
  "active_lengths": [],
  "output_tokens_per_second": 872.0721166359133
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/4/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/4/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:05:15.031180+00:00",
  "engine_ready": "2026-10-07T11:58:51.705765+00:00",
  "answers": 62,
  "expected": 62,
  "pending": 0,
  "elapsed_generation_seconds": 383.32539833150804,
  "generated_tokens": 362506,
  "finished_tokens": 362506,
  "mean_finished_tokens": 5846.870967741936,
  "max_finished_tokens": 22495,
  "active_lengths": [],
  "output_tokens_per_second": 945.6874018206772
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/5/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/5/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:05:47.513147+00:00",
  "engine_ready": "2026-10-07T11:58:51.716872+00:00",
  "answers": 62,
  "expected": 62,
  "pending": 0,
  "elapsed_generation_seconds": 415.796261748299,
  "generated_tokens": 345899,
  "finished_tokens": 345899,
  "mean_finished_tokens": 5579.0161290322585,
  "max_finished_tokens": 32768,
  "active_lengths": [],
  "output_tokens_per_second": 831.8954060471782
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/6/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/6/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:06:47.151572+00:00",
  "engine_ready": "2026-10-07T11:58:52.329771+00:00",
  "answers": 62,
  "expected": 62,
  "pending": 0,
  "elapsed_generation_seconds": 474.8217814248055,
  "generated_tokens": 427422,
  "finished_tokens": 427422,
  "mean_finished_tokens": 6893.903225806452,
  "max_finished_tokens": 32768,
  "active_lengths": [],
  "output_tokens_per_second": 900.1735318826945
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/7/progress.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/shards/7/progress.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T12:06:02.201213+00:00",
  "engine_ready": "2026-10-07T11:58:51.605975+00:00",
  "answers": 62,
  "expected": 62,
  "pending": 0,
  "elapsed_generation_seconds": 430.59523843508214,
  "generated_tokens": 370351,
  "finished_tokens": 370351,
  "mean_finished_tokens": 5973.403225806452,
  "max_finished_tokens": 32768,
  "active_lengths": [],
  "output_tokens_per_second": 860.0907927964356
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/reasoning/summary.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/reasoning/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "mode": "reasoning",
  "questions": 500,
  "answers": 500,
  "samples_per_question": 1,
  "accuracy": 0.742,
  "correct": 371,
  "ci95": [
    0.7019060194394218,
    0.7784037997771869
  ],
  "ci_method": "Wilson two-sided 95%",
  "invalid_answers": 5,
  "scorer_errors": [],
  "finish_reasons": {
    "stop": 495,
    "length": 5,
    "abort": 0
  },
  "output_tokens": 2994264,
  "scoring": "Final-answer extraction independent of gold, Math-Verify 0.8.0 symbolic equivalence",
  "traces_sha256": "4822c125c260021f9fbe7da3ecd5f3545dd499c2adda137831c1d13f346e10d2",
  "extraction_tests": 10
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/status.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "status": "complete",
  "updated": "2026-10-07T12:07:49.958943+00:00",
  "summary": "${PROJECT_ROOT}/exps/qwen3-06b-math500-author-32k-20261007/summary.json"
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/summary.json](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "finished": "2026-10-07T12:07:49.954911+00:00",
  "profiles": {
    "instant": {
      "complete": true,
      "mode": "instant",
      "questions": 500,
      "answers": 500,
      "samples_per_question": 1,
      "accuracy": 0.51,
      "correct": 255,
      "ci95": [
        0.4662736879310782,
        0.5535738252596908
      ],
      "ci_method": "Wilson two-sided 95%",
      "invalid_answers": 0,
      "scorer_errors": [],
      "finish_reasons": {
        "stop": 500,
        "length": 0,
        "abort": 0
      },
      "output_tokens": 310036,
      "scoring": "Final-answer extraction independent of gold, Math-Verify 0.8.0 symbolic equivalence",
      "traces_sha256": "0d8846cb8704ae36c21b33f662d5faa7aa690ca491b696f6ddb8d190662bdad9",
      "extraction_tests": 10
    },
    "reasoning": {
      "complete": true,
      "mode": "reasoning",
      "questions": 500,
      "answers": 500,
      "samples_per_question": 1,
      "accuracy": 0.742,
      "correct": 371,
      "ci95": [
        0.7019060194394218,
        0.7784037997771869
      ],
      "ci_method": "Wilson two-sided 95%",
      "invalid_answers": 5,
      "scorer_errors": [],
      "finish_reasons": {
        "stop": 495,
        "length": 5,
        "abort": 0
      },
      "output_tokens": 2994264,
      "scoring": "Final-answer extraction independent of gold, Math-Verify 0.8.0 symbolic equivalence",
      "traces_sha256": "4822c125c260021f9fbe7da3ecd5f3545dd499c2adda137831c1d13f346e10d2",
      "extraction_tests": 10
    }
  }
}
```

</details>

- [exps/qwen3-06b-math500-author-32k-20261007/instant/progress.json](../history/local_saved/5fba2cdc4cc1/exps/qwen3-06b-math500-author-32k-20261007/instant/progress.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "updated": "2026-10-07T11:45:52.348199+00:00",
  "answers": 96,
  "expected": 500
}
```

</details>

## Графики

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_and.png](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_and.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_not.png](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_not.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_or.png](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_or.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_xor.png](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/tests/test_region_xor.png) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

## Исходники рецепта и награды

- [exps/qwen3-06b-math500-author-32k-20261007/run.py](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/plot.py](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/plot.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/pygletplot/plot.py](../artifacts/exps/qwen3-06b-math500-author-32k-20261007/scorer-deps/sympy/plotting/pygletplot/plot.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
