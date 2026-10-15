#!/usr/bin/env bash
# Exp 23 entrypoint on the 4xH100 pod (infra/exp23-vm.yaml runs it as /work/exp23/start.sh under term_forward.sh).
# Prepared Qwen3-4B with the six tag tokens, no training, the exp-23 prompt (header.txt), dev math, budget 16384, one job per GPU:
#   GPU0/1  parallel rollout (authors' rollout, non-thinking template), gsm8k_dev / math_dev
#   GPU2    plain generation, non-thinking, both benchmarks, with token ids
#   GPU3    plain generation, thinking, both benchmarks, with token ids
# Rerun = resume: run_eval.sh skips finished benchmarks. Logs /work/exp23/logs, results /work/bench/exp23/<run>.
set -uo pipefail
source /work/venv/bin/activate
repo=/work/exps/23-instruct4b-prompt-zeroshot
model=/work/assets/models/Qwen3-4B-instruct-add-special-token
export EVAL_DATA=/work/bench_data/exp23 EVAL_OUT=/work/bench/exp23 RAY_DEDUP_LOGS=0
logs=/work/exp23/logs
mkdir -p "$logs"
cd "$repo"
echo "start $(date) commit $(git rev-parse HEAD)" >> "$logs/start.log"
[ -d "$EVAL_DATA/dev" ] || python scripts/exp23/make_data.py /work/bench_data/instruct4b/eval "$EVAL_DATA" > "$logs/make_data.log" 2>&1
if ! python scripts/exp23/check_tokens.py "$model" "$EVAL_DATA" > "$logs/check_tokens.log" 2>&1; then
    echo "check_tokens failed $(date)" >> "$logs/start.log"; exec sleep infinity
fi
run() {  # gpu name mode benches
    CUDA_VISIBLE_DEVICES=$1 BENCHES=$4 bash scripts/instruct4b_eval/run_eval.sh "$2" "$model" dev "$3" 16384 >> "$logs/$2-gpu$1.log" 2>&1
    echo "exit $? $(date)" >> "$logs/$2-gpu$1.log"
}
run 0 exp23-dev-par parallel gsm8k_dev &
run 1 exp23-dev-par parallel math_dev &
run 2 exp23-dev-nothink no-thinking "gsm8k_dev math_dev" &
run 3 exp23-dev-think thinking "gsm8k_dev math_dev" &
wait
echo "done $(date)" >> "$logs/start.log"
touch /work/exp23/DONE
exec sleep infinity  # all finished: keep the pod quiet until it is scaled to 0 (a restart would only skip finished work)
