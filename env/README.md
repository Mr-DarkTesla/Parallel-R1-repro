# Pod environment

The pod has no internet, so packages are installed from an offline wheelhouse.

- `requirements.in`: steps 1-2 of `verl/scripts/install_vllm_sglang_mcore.sh` without sglang and megatron; `transformers` pinned to the vllm 0.8.5 era.
- `requirements.lock`: `uv pip compile requirements.in --python-version 3.10 --python-platform x86_64-manylinux_2_28 --exclude-newer 2025-10-01`.
- Wheels are downloaded on a machine with internet with `pip download --no-deps` for linux / cp310, plus `flash_attn-2.7.4.post1+cu12torch2.6cxx11abiFALSE-cp310-cp310-linux_x86_64.whl` from the flash-attention GitHub release.
- Install on the pod: `bash env/install_pod.sh <wheelhouse_dir>...`.
