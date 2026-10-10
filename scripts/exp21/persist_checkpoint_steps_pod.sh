#!/usr/bin/env bash
# Stage all BF16 step exports on the dedicated PVC before ranking and pruning to five.
set -euo pipefail
run=${EXP21_RUN:?set EXP21_RUN}
dest=${EXP21_CHECKPOINT_DIR:-/checkpoints/exp21-m1-selective-v4}
steps=${EXP21_STEPS:-8,16,24,32,40,48,56,64}
test -s "$run/DONE"
mkdir -p "$dest"
IFS=, read -r -a checkpoint_steps <<< "$steps"
for step in "${checkpoint_steps[@]}"; do
    source=$run/step_models/step_$step/model
    target=$dest/step_$step/model
    test -s "$source/config.json"
    if [ ! -d "$target" ]; then
        mkdir -p "$dest/step_$step"
        rm -rf "$target.tmp"
        cp -a "$source" "$target.tmp"
        test -s "$target.tmp/config.json"
        test -s "$target.tmp/tokenizer_config.json"
        find "$target.tmp" -maxdepth 1 -type f \( -name '*.safetensors' -o -name '*.bin' \) -size +0c | grep -q .
        mv "$target.tmp" "$target"
    fi
    test -s "$target/config.json"
    test -s "$target/tokenizer_config.json"
    find "$target" -maxdepth 1 -type f \( -name '*.safetensors' -o -name '*.bin' \) -size +0c | grep -q .
    echo "persisted step $step: $target"
done
date -Is > "$dest/ALL_EIGHT_STAGED"
