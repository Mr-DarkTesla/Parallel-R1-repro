#!/usr/bin/env bash
# Serialize 4B SFT after the untouched 4B fixed40 baseline on the same GPU.
set -euo pipefail
for _ in $(seq 1 900); do
    test -s /tmp/exp21-4b-init-fixed40/DONE && break
    sleep 5
done
test -s /tmp/exp21-4b-init-fixed40/DONE
cd /work/parallel-r1
bash scripts/exp21/run_4b_teacher_pair_pod.sh
