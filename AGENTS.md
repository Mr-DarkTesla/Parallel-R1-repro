# Parallel-R1 reproduction

Fork of https://github.com/zhengkid/Parallel-R1 (remote `upstream`, base commit `f1c6389`).
Goal: reproduce Parallel-R1 and test the mid-training exploration scaffold hypothesis.

## Code rules

- Code must be short and readable. Never add code that can be removed.
- Keep changes to the authors' code minimal; every deviation is listed in `docs/changes.md` with the reason and how it was verified.
- Our scripts live in `scripts/`; the authors' code stays in `verl/`.

## Runs

- GPU: pod `vcharkin-shared-vm-0`, namespace `shared-dzen-ml`, 1x H100. The pod has no internet and no PyPI mirror: install from the offline wheelhouse.
- Pod paths (ephemeral disk, lost on pod restart): repo `/home/jovyan/parallel-r1`, venv `/home/jovyan/venv`, models and wheels `/home/jovyan/assets`, runs `/home/jovyan/runs`.
- `/shared-storage` (PVC) is almost full; do not put checkpoints there.
- Copy logs and metrics of every run back into `results/<run_name>/` in this repo.
