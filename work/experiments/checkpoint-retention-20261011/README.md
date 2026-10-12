Checkpoint retention, 2026-10-11

This isolated runner does not change any currently running or source-sealed arm.
Adopt its train.py changes only in a new namespace and re-seal the runnable inputs.
The rollout/replay/optimizer semantics are unchanged here.

Configuration defaults:
  eval_steps: legacy checkpoint_steps if present, otherwise eval_every=16
  keep_steps: [32, 128, 256, 500]
  resume_checkpoint_every: 16
  keep_count: 1

Evaluation writes traces and scores directly from resident weights. Steps 4/8
can therefore be evaluated without saving a full model + Adam + RNG export.
Each resume save writes every optimizer shard and RNG state before complete.json.
The completed final step is always saved; keep_steps must include final if training
is continued in the same output namespace (new output namespaces are recommended).
Old managed resumes are removed only after the next complete checkpoint exists.
All JSON/TXT checkpoint metadata is archived under checkpoint-history/ before
weights/Adam/RNG are removed. Scores and trajectory logs live outside checkpoints
and are untouched. Legacy artifacts lacking retention_managed=true are untouched.

Scheduled evaluation and resume consumers must acquire a lease before publishing
queue/config references, including references to a checkpoint that does not exist
yet. Example:

  from checkpoint_retention import pin, release
  pin(run_output, 64, 'corrected-width8-resume')
  pin(run_output, 128, 'MATH500-run128')
  # Publish consumer only AFTER pin succeeds.
  # Release only after all workers/readers have exited and results are sealed:
  release(run_output, 128, 'MATH500-run128')

Leases do not expire automatically. Incomplete checkpoints, symlinked trees,
unknown lease states, and unowned legacy artifacts are not deleted. Atomic registry
updates and a shared flock serialize lease creation against pruning. Consumers
must use this API instead of editing artifact-leases.json without the lock.
New runners that require published checkpoints beyond the anchor list must pin
them before the next checkpoint completes.

Tests:
  python3 work/experiments/checkpoint-retention-20261011/test_retention.py
  python3 -m py_compile work/experiments/checkpoint-retention-20261011/runner/*.py
