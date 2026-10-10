#!/usr/bin/env bash
# Fixed 100-question sample per dev benchmark with autonomous greedy masked decoding.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
model=/tmp/exp21-expanded-th-runs/exp21-expanded-th-m1-twopath-tagweighted/model
data=/tmp/exp21-masked-dev100-unique
out=/work/exp21/masked_dev100/m1-twopath-tagweighted-unique
test -e "$model/config.json"
export EXP21_TOKENIZER="$model"
mkdir -p "$data" "$out"
python - "$data" <<'PY'
import json
import sys
from pathlib import Path

import pandas as pd

dest = Path(sys.argv[1])
source = Path("/work/bench_data/instruct4b/eval/dev/multiverse")
selected = {}
for bench in ("gsm8k_dev", "math_dev", "arc_dev", "mmlu_pro_dev"):
    frame = pd.read_parquet(source / f"{bench}.parquet")
    questions = [list(prompt)[0]["content"] for prompt in frame["prompt"]]
    unique = frame.assign(question_key=questions).drop_duplicates("question_key")
    indices = sorted(unique.sample(n=100, random_state=0).index.tolist())
    selected[bench] = indices
    frame.iloc[indices].reset_index(drop=True).to_parquet(dest / f"{bench}.parquet")
(dest / "selection.json").write_text(json.dumps(selected, indent=2) + "\n")
PY

cd /work/parallel-r1/verl
run_one() {
    local bench=$1 budget=$2
    local test=$data/$bench.parquet dump=$out/$bench.jsonl
    if [ -e "$out/$bench-blocks.json" ]; then return; fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$dump" 100 "$budget" thinking greedy > "$out/$bench.log" 2>&1
    python ../scripts/bench/score.py "$dump" "$test" \
        "$out/$bench-score.json" "$out/$bench-rows.jsonl" >> "$out/$bench.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$dump" "$out/$bench-rows.jsonl" "$out/$bench-blocks.json" \
        "$out/$bench-block-rows.jsonl" masked >> "$out/$bench.log" 2>&1
}

run_one gsm8k_dev 2048
run_one math_dev 4096
run_one arc_dev 2048
run_one mmlu_pro_dev 2048
date -Is > "$out/DONE"
