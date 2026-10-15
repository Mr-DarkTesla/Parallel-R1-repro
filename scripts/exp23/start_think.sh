#!/usr/bin/env bash
# Exp 23, thinking placement: the original Qwen3-4B (tags as text) with header_think.txt (blocks inside <think>), thinking mode,
# the 150+150 subset of make_subset.py (the rows of exp23sub-c0-think), budget 16384. GPU0 gsm8k_dev, GPU1 math_dev.
# Copied to /work/exp23/start.sh (infra/exp23-vm.yaml, 2 GPUs). Rerun = resume. Results /work/bench/exp23/exp23sub-c0-thinkprompt.
set -uo pipefail
source /work/venv/bin/activate
repo=/work/exps/23-instruct4b-prompt-zeroshot
export EVAL_DATA=/work/bench_data/exp23thinksub EVAL_OUT=/work/bench/exp23 PYTHONDONTWRITEBYTECODE=1
logs=/work/exp23/logs
mkdir -p "$logs"
cd "$repo"
echo "start_think $(date) commit $(git rev-parse HEAD)" >> "$logs/start.log"
if [ ! -d "$EVAL_DATA/dev" ]; then
    python scripts/exp23/make_data.py /work/bench_data/instruct4b/eval /work/bench_data/exp23think scripts/exp23/header_think.txt
    python scripts/exp23/make_subset.py /work/bench_data/exp23think "$EVAL_DATA" 150
fi > "$logs/make_think_data.log" 2>&1
for job in 0:gsm8k_dev 1:math_dev; do
    gpu=${job%%:*} bench=${job#*:}
    (CUDA_VISIBLE_DEVICES=$gpu BENCHES=$bench bash scripts/instruct4b_eval/run_eval.sh exp23sub-c0-thinkprompt /work/assets/models/Qwen3-4B dev thinking 16384
     echo "exit $? $(date)") >> "$logs/thinkprompt-gpu$gpu.log" 2>&1 &
done
wait
python scripts/exp23/think_where.py /work/bench/exp23/exp23sub-c0-think /work/bench/exp23/exp23sub-c0-thinkprompt > "$logs/think_where.log" 2>&1
echo "done_think $(date)" >> "$logs/start.log"
exec sleep infinity  # keep the pod quiet until it is scaled to 0
