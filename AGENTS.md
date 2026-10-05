# Parallel-R1 reproduction

Fork of https://github.com/zhengkid/Parallel-R1 (remote `upstream`, base commit `f1c6389`).
Goal: reproduce Parallel-R1 and test the mid-training exploration scaffold hypothesis.

## Code rules

- Code must be short and readable. Never add code that can be removed.
- Keep changes to the authors' code minimal; every deviation is listed in `docs/changes.md` with the reason and how it was verified.
- Our scripts live in `scripts/`; the authors' code stays in `verl/`.

## Experiments and git

- Remote `origin`: https://github.com/Mr-DarkTesla/Parallel-R1-repro (push over SSH, port 443). Never push to `upstream`.
- One branch per experiment: `exp/NN-short-name`, branched from the experiment it changes. Only that experiment's change goes into the branch.
- The branch stores the experiment's code, metrics and report in `results/<NN-short-name>/`. Commit and push when the experiment finishes.
- Run an SFT experiment on the pod with `bash scripts/run_experiment.sh <name>`.

## Runs

- GPU: pod `vcharkin-shared-vm-0`, namespace `shared-dzen-ml`, 1x H100. The pod has no internet and no PyPI mirror: install from the offline wheelhouse.
- Pod paths (ephemeral disk, lost on pod restart): repo `/home/jovyan/parallel-r1`, venv `/home/jovyan/venv`, models and wheels `/home/jovyan/assets`, runs `/home/jovyan/runs`.
- `/shared-storage` (PVC) is almost full; do not put checkpoints there.
- Copy logs and metrics of every run back into `results/<run_name>/` in this repo.
