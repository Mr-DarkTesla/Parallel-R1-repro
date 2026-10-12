# work/experiments/hf-instruct-sft-20261012

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/hf-instruct-sft-20261012/bundle/system_prompt.txt](../artifacts/work/experiments/hf-instruct-sft-20261012/bundle/system_prompt.txt) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

- [work/experiments/hf-instruct-sft-20261012/bundle/upload-manifest.json](../artifacts/work/experiments/hf-instruct-sft-20261012/bundle/upload-manifest.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "repo_id": "sirius-parallel-r1/Parallel-R1-Qwen3-4B-Instruct-SFT",
  "source": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final",
  "full_sft": true,
  "rl_updates": 0,
  "training_steps": 42,
  "files": {
    "config.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/config.json",
      "bytes": 1542,
      "sha256": "938d961211217b1b58af4c9dc7c52a34f86c9ca8cace368475161cbd063a93d5"
    },
    "generation_config.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/generation_config.json",
      "bytes": 214,
      "sha256": "475b038504e6cd813ed0a80c3b01200a5fdbd2e3679c2354c01371e83c50a7cc"
    },
    "model.safetensors.index.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model.safetensors.index.json",
      "bytes": 32854,
      "sha256": "a4552ba4015e525d61298de02b8b586eaab32ff08b6eac266303c9306edf5392"
    },
    "model-00001-of-00002.safetensors": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00001-of-00002.safetensors",
      "bytes": 4967215360,
      "sha256": "6912a3e099474bb2e3476dfdc864e813852b86d30de62d3fe365b271792b9339"
    },
    "model-00002-of-00002.safetensors": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/model-00002-of-00002.safetensors",
      "bytes": 3077766632,
      "sha256": "0339d59522bda178993f328c35a2b9dea9b043b30d526b48655874af167cb438"
    },
    "chat_template.jinja": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/chat_template.jinja",
      "bytes": 4168,
      "sha256": "a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8"
    },
    "tokenizer_config.json": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/tokenizer_config.json",
      "bytes": 6560,
      "sha256": "26c6acc08d99bb84c75646e977bd35c69a2b4795bbebfe96fcd28b7eefdf21ba"
    },
    "special_tokens_map.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/special_tokens_map.json",
      "bytes": 714,
      "sha256": "288dab326a769b9ccb4f558eab94e753a6a73424445528364da1953a09e7bc7c"
    },
    "added_tokens.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/added_tokens.json",
      "bytes": 844,
      "sha256": "7850ed5df9923a253976020596c17700d5dd552db3686ec96cf5621ac05c0569"
    },
    "vocab.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/vocab.json",
      "bytes": 2776833,
      "sha256": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910"
    },
    "merges.txt": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/merges.txt",
      "bytes": 1671853,
      "sha256": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5"
    },
    "tokenizer.json": {
      "path": "${PROJECT_ROOT}/work/experiments/instruct-full-20261011/runs/epoch1/final/tokenizer.json",
      "bytes": 11423769,
      "sha256": "473316a0fd7d9b756447419d97489c5e6ee3fe4ffceb25392011edfe68bca4f7"
    },
    "system_prompt.txt": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/system_prompt.txt",
      "bytes": 1725,
      "sha256": "82fb35db3d24b2865b9ac195943d93803a9404b2936fc8e83c996169486af59e"
    },
    "prompt.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/prompt.py",
      "bytes": 324,
      "sha256": "b99401297e1fa73515fe5b0ee7227467e1427cc31f0b6e38b72e2a876447ca8d"
    },
    "parallel_generate.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/parallel_generate.py",
      "bytes": 1969,
      "sha256": "87ce34fc6e53ac52877bb6737efad458d7d3789d90c82feacc613918f27c29e9"
    },
    "requirements.txt": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/requirements.txt",
      "bytes": 60,
      "sha256": "002e11ebc4fb0155e6ad6b2d72d5887299b7104cf919aca02f72a58629ac7ad2"
    },
    "README.md": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/README.md",
      "bytes": 3742,
      "sha256": "e9ac1bdb5aa0bc1a1d3e67ae3d196ffd9acd31490aa9fe8aac8cf597a18efc8e"
    },
    "runtime/decoder.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/decoder.py",
      "bytes": 7234,
      "sha256": "11efd325c9862b87a1a3451c1860dbec69ae46bf18df3b4df15898e2ef1c84c6"
    },
    "runtime/microbatch_decoder.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/microbatch_decoder.py",
      "bytes": 2377,
      "sha256": "985d3bad47eb3ac77d8c3ef613416925d9b35b2ebcbd503c84718b0e41d93701"
    },
    "runtime/structured_replay.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/structured_replay.py",
      "bytes": 5300,
      "sha256": "e37502b5a200534963905bc1891dcf5164c0c4c97bfff973d681f4667cf1cc59"
    },
    "runtime/rollout.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/rollout.py",
      "bytes": 10078,
      "sha256": "e0d496fa47d359be27cc1493a7c9e481fd3f33ffd7933215d22f175b9ba1d411"
    },
    "runtime/source/parallel_structure.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/source/parallel_structure.py",
      "bytes": 2773,
      "sha256": "f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f"
    },
    "runtime/source/__init__.py": {
      "path": "${PROJECT_ROOT}/work/experiments/hf-instruct-sft-20261012/bundle/runtime/source/__init__.py",
      "bytes": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  },
  "auth": "Ephemeral stdin token only; no huggingface login or credential persistence",
  "trace_always_saved": true
}
```

</details>

## Метрики и полнота результатов

- [work/experiments/hf-instruct-sft-20261012/bridge-status.json](../artifacts/work/experiments/hf-instruct-sft-20261012/bridge-status.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "url": "${LOCAL_ENDPOINT}",
  "credentials_persisted": false
}
```

</details>

- [work/experiments/hf-instruct-sft-20261012/status.json](../artifacts/work/experiments/hf-instruct-sft-20261012/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "state": "completed",
  "repo_id": "sirius-parallel-r1/Parallel-R1-Qwen3-4B-Instruct-SFT",
  "time": 1791801449.4646049,
  "commit": "7c7efe1a50a189eee0323003386ba379b4477be6",
  "credentials_persisted": false
}
```

</details>
