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

- GPU: pod `vcharkin-exp-vm-0` (3x H100, `infra/exp-vm.yaml`), namespace `shared-dzen-ml`. One experiment per GPU via `CUDA_VISIBLE_DEVICES`.
  Pods have no internet and no PyPI mirror: install from the offline wheelhouse (`env/`).
- Persistent paths on PVC `vcharkin-parallel-r1-pvc` (`infra/parallel-r1-pvc.yaml`) mounted at `/work`: repo `/work/parallel-r1`,
  venv `/work/venv`, models and wheels `/work/assets`, runs `/work/runs`. Everything outside `/work` is lost when the pod is evicted
  (node802 was evicted by a node taint on 2026-10-05 and the ephemeral data was lost).
- Copy logs and metrics of every run back into `results/<run_name>/` in this repo.
