# Changes to the authors' code

Base: upstream commit `f1c6389`.

## SFT speedups (`verl/verl/trainer/fsdp_parallel_sft_trainer.py`, `verl/verl/utils/dataset/parallel_thinking_sft_dataset.py`)

1. Padding is cropped to the longest sample instead of `max_length=4096`.
   The dataset still builds the same masks and position ids; it also returns the real `length`.
   `collate_cropped` crops each batch on CPU, `crop_padding` crops each micro batch before the forward.
   Cropping on CPU is needed on 1 GPU: a batch of 128 uncropped 4096x4096 float masks is ~10 GB of host memory per batch.
2. Micro batch 4 instead of 1 (`scripts/sft_qwen3_0.6b.sh`); micro batch 8 ran out of GPU memory on the longest batches (fp32 cross entropy over the 151k vocabulary). The loss is the token mean within each sample,
   then the mean over samples, which is exactly the objective of the authors' micro batch 1.
   `data.balance_dp_token` is no longer used.
3. Gradient checkpointing is off (`scripts/sft_qwen3_0.6b.sh`).
4. DataLoader `num_workers=2` instead of 8. With 8 workers the prefetched batches of float masks (up to ~3 GB per 128-sample batch)
   plus their pinned copies hit the pod memory limit of 122 GiB at the first epoch boundary (process killed with SIGKILL).
   Two workers are enough: a sample takes 0.04 s to build, a 128-sample batch ~5 s per worker, a training step ~6 s.

Verification:
- CPU, tiny random Qwen3, authors' dataset class, 4 samples: same loss, max gradient difference 1.2e-7.
  A token mean over the micro batch (verl default) gives a gradient difference of 1.7e-2, so the per-sample mean is required.
- GPU: `scripts/check_sft_parity.sh` runs 10 steps of the authors' code and of ours on the same data order and init.

## Special tokens (`scripts/add_special_tokens.py`)

The authors add the six tags with `add_special_tokens` + `resize_token_embeddings(151675)`, which gives the tags
the existing unused embedding rows 151669-151674. In Qwen3-4B-Base those rows differ; in Qwen3-0.6B-Base all of them
are the same vector (norm 0.35). With tied embeddings the 0.6B model then cannot tell the tags apart: after SFT the tags
were still nearly identical (cosine 0.999) and only 0.2% of parallel answers had a valid tag structure
(`results/eval_sft_identical_tags`). We initialise each tag with the mean embedding of the pieces of its text
(`<`, `Path`, `>`). The authors' 4B rows match neither this init (cosine 0.40-0.56) nor the unused rows, so their exact
init is unknown; what matters is that their tags are distinct.

## Pod

- StatefulSet `vcharkin-shared-vm`: `/dev/shm` is an in-memory `emptyDir` of 32Gi (was 64M), needed by the DataLoader workers.
