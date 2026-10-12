# Frozen experiment sources

This directory preserves source snapshots from the October 10–12 SFT/RL
campaign, including the 8-GPU controls, fullweight Instruct SFT, fullwidth8
inference, collective replay rejection, checkpoint retention, and the pending
24→32-GPU weights-only handoff. Older Base experiments remain historical source;
the active direction is Qwen3-4B Instruct.

Use [`experiments/parallel_instruct`](../experiments/parallel_instruct/README.md)
for the shared configurable runtime. Changing GPU count does not change its
8 prompts × 4 responses effective batch. The dated scripts here retain the
original per-run configurations, hashes, and dependencies; they are not general
launch defaults. In particular, old Cloud allocation IDs and recovered queues
must not be relaunched from archived control scripts.

Git stores code and selected small configuration/proof snapshots. Model weights,
optimizer states, generated datasets, raw traces, logs, caches, live status,
submission receipts, and duplicate review mirrors are ignored. Proof/config
snapshots describe their original execution and are not evidence of current job
state; read the live server receipts when monitoring.
