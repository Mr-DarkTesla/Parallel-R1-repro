# Changes to the authors' code

Base: upstream commit `f1c6389`.

## SFT speedups (`verl/verl/trainer/fsdp_parallel_sft_trainer.py`, `verl/verl/utils/dataset/parallel_thinking_sft_dataset.py`)

1. Padding is cropped to the longest sample instead of `max_length=4096`.
   The dataset still builds the same masks and position ids; it also returns the real `length`.
   `collate_cropped` crops each batch on CPU, `crop_padding` crops each micro batch before the forward.
   Cropping on CPU is needed on 1 GPU: a batch of 128 uncropped 4096x4096 float masks is ~10 GB of host memory per batch.
2. Micro batch 8 instead of 1 (`scripts/sft_qwen3_0.6b.sh`). The loss is the token mean within each sample,
   then the mean over samples, which is exactly the objective of the authors' micro batch 1.
   `data.balance_dp_token` is no longer used.
3. Gradient checkpointing is off (`scripts/sft_qwen3_0.6b.sh`).

Verification:
- CPU, tiny random Qwen3, authors' dataset class, 4 samples: same loss, max gradient difference 1.2e-7.
  A token mean over the micro batch (verl default) gives a gradient difference of 1.7e-2, so the per-sample mean is required.
- GPU: `scripts/check_sft_parity.sh` runs 10 steps of the authors' code and of ours on the same data order and init.

## Pod

- StatefulSet `vcharkin-shared-vm`: `/dev/shm` is an in-memory `emptyDir` of 32Gi (was 64M), needed by the DataLoader workers.
