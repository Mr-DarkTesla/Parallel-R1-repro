# Qwen3-4B: full matched dev and IFEval after focus34

## Decision and scope

The runner evaluates the selected focus34 tagged checkpoint and its focus34
plain control at configurable exported steps. Both arms originate from equal
text and ordering: plain removes only the ten Multiverse tags. The default is
the focus34 final step 32 for both arms.

Ordinary model quality uses the same `plain` prompt parquet for each arm:

- dev: GSM8K, MATH, ARC and MMLU-Pro;
- IFEval only from the frozen suite;
- native Qwen `thinking` and `no-thinking` generation in both suites;
- one answer per existing protocol, budget 16,384 and deterministic IFEval
  scorer seed 0.

This opens no frozen benchmark other than IFEval. The base Qwen3-4B comparison
is optional through `INCLUDE_BASE=1`; it uses the same four ordinary modes.
Existing frozen base IFEval dumps are not silently reused, so all selected
comparisons have current metadata and row-level outputs.

Block formation is a different measurement. The focus34 run already scores
its fixed40. If `RUN_MASKED_BLOCKS=1` is explicitly set, tagged and plain
run on the same four ten-question fixed40 splits
with `generate_masked_multiverse.py`, greedy decoding, the Multiverse mask and
the learned positions. `score_thinking_blocks.py` records decoder `masked`.
Those outputs measure model generation under the trained decoder conditions;
they must not be compared as ordinary sequential dev behavior or merged with
the ordinary dev/IFEval summary.

## Preconditions and ownership

Run only on the personal pod after focus34 writes:

```text
/work/exp21/qwen4b_focus34/EVAL_DONE
```

The runner waits for that nonempty marker, locks
`/checkpoints/exp21-qwen4b-full-dev/runner.lock`, requires the owned GPU index
`EXP21_GPU=0`, and refuses to start if an SFT, masked decoder, or ordinary
evaluator is already running. It also requires a clean committed `scripts/`
and `verl/` checkout, as the underlying evaluator records the Git commit.
The training checkout on `/work` currently has local tracked edits; prepare a
clean worktree under `/tmp` and set `EXP21_REPO` to it before launching.
It sets `CUDA_VISIBLE_DEVICES=0`. It does not
scale pods, change PVCs, use a proxy, or invoke another GPU queue.

It writes these owned artifacts under `QWEN4B_FULL_DEV_ROOT`, default
`/checkpoints/exp21-qwen4b-full-dev`. The `/work` PVC has only about
1.5 GiB free, whereas the owned checkpoint PVC has about 26 GiB free;
full dev output must not be sent to `/work`:

- `runner_meta.json`: immutable models, steps, protocol, commit and output
  paths for safe resume;
- `eval/<run>/meta.json`, generation dumps, scores and per-row outcomes from
  the established evaluator;
- `masked_fixed40/{selected,plain}/step_<step>/` only for the separate block
  protocol;
- `ATTEMPT_DONE`: timestamp and status for every exit;
- `EVAL_DONE`: only after all requested ordinary suites and masked runs pass.

The runner does not overwrite incomplete or incompatible suite outputs. It
only skips a suite after checking its metadata, current prompt parquet,
per-row IDs/order/sample values and nonempty summary. A mismatch stops for
manual inspection rather than mixing protocols.

Before `EVAL_DONE`, it also compares tagged and plain row files for every
ordinary suite and mode. `source`, problem ID, problem text, rendered input
and sample index must match exactly.

## Invocation

Default selected focus34 pair:

```bash
bash scripts/exp21/run_qwen4b_selected_full_dev_pod.sh
```

Select an exported checkpoint, include base, or separate model paths:

```bash
SELECTED_STEP=16 PLAIN_STEP=16 INCLUDE_BASE=1 \
SELECTED_MODEL=/path/to/tagged/model PLAIN_MODEL=/path/to/plain/model \
bash scripts/exp21/run_qwen4b_selected_full_dev_pod.sh
```

`SELECTED_MODEL` and `PLAIN_MODEL` change only ordinary evaluation. For the
masked fixed40 protocol, `SELECTED_RUN`/`PLAIN_RUN` and their selected steps
must still name SFT run directories with `step_models/step_<step>/model`.
Use `RUN_MASKED_BLOCKS=0` (the default) when using already completed
fixed40 results or a model outside that layout. `EVAL_BUDGET`,
`QWEN4B_FULL_DEV_ROOT` and `FOCUS34_WAIT_SECONDS` are
configurable as well. The masked evaluator supplied by exp21 is fixed to the
owned GPU index 0, so this runner requires `EXP21_GPU=0`.

## Report interpretation

Compare tagged with plain on each ordinary suite and mode using the stored
row-level outputs. They share the exact problem text and prompt parquet. Base
is a second reference when enabled. Treat block frequency, well-formedness and
external-answer accuracy from the masked fixed40 as distinct figures: the
decoder applies visibility and position rules, while the normal suites do not.
