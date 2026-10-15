#!/usr/bin/env bash
# Exp 23 entrypoint on the 4xH100 pod (infra/exp23-vm.yaml runs it as /work/exp23/start.sh under term_forward.sh).
# No training, the exp-23 prompt (header.txt), dev math, budget 16384. Models: P = prepared Qwen3-4B with the six tag tokens (c=1);
# P2 = P with the tags' output rows x2 (scale_tag_logits.py; in P a tag token is unreachable, tag_logits.py). One job per GPU:
#   GPU0/1  P2 parallel rollout (authors' rollout, non-thinking template), gsm8k_dev / math_dev
#   GPU2    P plain generation non-thinking (token ids), then P2 plain generation thinking
#   GPU3    P2 plain generation non-thinking (token ids)
# P rollout gsm8k_dev (exp23-dev-par) ran in the first launch; P rollout math_dev and P thinking were stopped (tags unreachable).
# Rerun = resume: run_eval.sh skips finished benchmarks. Logs /work/exp23/logs, results /work/bench/exp23/<run>.
set -uo pipefail
source /work/venv/bin/activate
repo=/work/exps/23-instruct4b-prompt-zeroshot
model=/work/assets/models/Qwen3-4B-instruct-add-special-token
model2=/work/assets/models/Qwen3-4B-instruct-tags-out2x
[ -d "$model2" ] || python scripts/exp23/scale_tag_logits.py "$model" "$model2" 2 > /work/exp23/logs/scale.log 2>&1
export EVAL_DATA=/work/bench_data/exp23 EVAL_OUT=/work/bench/exp23 RAY_DEDUP_LOGS=0
export PYTHONDONTWRITEBYTECODE=1  # the repo tracks verl/**/__pycache__; rewritten .pyc would fail run_eval.sh's clean-tree check
logs=/work/exp23/logs
mkdir -p "$logs"
cd "$repo"
echo "start $(date) commit $(git rev-parse HEAD)" >> "$logs/start.log"
[ -d "$EVAL_DATA/dev" ] || python scripts/exp23/make_data.py /work/bench_data/instruct4b/eval "$EVAL_DATA" > "$logs/make_data.log" 2>&1
if ! python scripts/exp23/check_tokens.py "$model" "$EVAL_DATA" > "$logs/check_tokens.log" 2>&1; then
    echo "check_tokens failed $(date)" >> "$logs/start.log"; exec sleep infinity
fi
run() {  # gpu name model mode benches
    CUDA_VISIBLE_DEVICES=$1 BENCHES=$5 bash scripts/instruct4b_eval/run_eval.sh "$2" "$3" dev "$4" 16384 >> "$logs/$2-gpu$1.log" 2>&1
    local code=$?
    echo "exit $code $(date)" >> "$logs/$2-gpu$1.log"
    return $code
}
run 0 exp23x2-dev-par "$model2" parallel gsm8k_dev &
run 1 exp23x2-dev-par "$model2" parallel math_dev &
{ run 2 exp23-dev-nothink "$model" no-thinking "gsm8k_dev math_dev" && run 2 exp23x2-dev-think "$model2" thinking "gsm8k_dev math_dev"; } &
run 3 exp23x2-dev-nothink "$model2" no-thinking "gsm8k_dev math_dev" &
failed=0
for job in $(jobs -p); do wait "$job" || failed=1; done
echo "done $(date) failed=$failed" >> "$logs/start.log"
[ $failed = 0 ] && touch /work/exp23/DONE
exec sleep infinity  # finished or failed: keep the pod quiet until it is scaled to 0; a restart repeats only unfinished benchmarks
