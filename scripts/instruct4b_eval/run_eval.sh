#!/usr/bin/env bash
# One model, one mode, dev or frozen suite, with per-row outcomes for paired comparisons (exp 13). One GPU.
#   no-thinking | thinking: native Qwen3 chat template with enable_thinking off | on; plain prompts (IFEval: the original prompt)
#   parallel: the authors' parallel prompt and the genuine parallel rollout (scripts/bench/eval_rollout.sh) in the non-thinking
#             template (PARALLEL_ROLLOUT_ENABLE_THINKING=false); math benchmarks only
#   multiverse (exp 21): sequential no-thinking diagnostic on the Multiverse prompt.
#   multiverse-branch (exp 21): independently generate sibling paths from the shared Goal prefix, then join and continue.
# dev: scripts/instruct4b_eval/generate.py (seed = sample index). frozen: scripts/bench/generate_plain.py, the protocol of the finished
# baseline runs. REUSE=<old run dir> scores that run's dumps instead of generating; allowed only for the two finished C0 16k runs below.
# Usage on the pod (venv active): CUDA_VISIBLE_DEVICES=<g> bash scripts/instruct4b_eval/run_eval.sh <name> <model> <dev|frozen> <mode> <budget>
# Env: EVAL_DATA (default /work/bench_data/instruct4b/eval, output of make_eval_data.py), EVAL_OUT (default /work/bench/instruct4b),
# BENCHES (subset, e.g. to split a suite over GPUs; one process per benchmark), REUSE,
# EVAL_ALLOW_UNVERSIONED=1 (CPU tests of a copied checkout without git, REUSE only; meta.json gets commit null, unversioned_test_only).
# Output $EVAL_OUT/<name>/: meta.json, dumps, <bench>.log, results/<bench>.json (score.py summary), rows/<bench>.jsonl.
# Code: tracked files under scripts/ and verl/ must be committed; meta.json records the commit, a rerun at another commit or with
# other settings fails. meta.json is created and checked under a lock (BENCHES splits of one name may start together).
# Resume: a benchmark with rows/<bench>.jsonl is skipped after its rows are checked against the current test parquet. Summary and rows are
# written to *.tmp and renamed after scoring succeeded. Dumps and logs of an unfinished attempt are renamed to *.incomplete-<time>.
# Scoring: SCORE_IFEVAL_SEED=0 for every run (C0 rescored from REUSE dumps and candidates alike), recorded in meta.json and required
# equal by paired_compare.py; summaries of the old unseeded scoring (IFEval one prompt flips between rescorings) are not comparable.
set -euo pipefail
name=$1 model=$2 suite=$3 mode=$4 budget=$5
repo=$(cd "$(dirname "$0")/../.." && pwd)
data=${EVAL_DATA:-/work/bench_data/instruct4b/eval}
run=${EVAL_OUT:-/work/bench/instruct4b}/$name
case $suite in
    dev) dir=$data/dev all="gsm8k_dev math_dev arc_dev mmlu_pro_dev" math="gsm8k_dev math_dev" generator=scripts/instruct4b_eval/generate.py ;;
    frozen) dir=/work/bench_data all="apo arc ifeval mmlu_pro limo" math="apo limo" generator=scripts/bench/generate_plain.py ;;
    *) echo "suite: dev | frozen"; exit 1 ;;
esac
case $mode in
    no-thinking | thinking) benches=${BENCHES:-$all} prompts=$dir/plain ;;
    multiverse) benches=${BENCHES:-$all} prompts=$dir/multiverse ;;
    multiverse-branch) benches=${BENCHES:-$all} prompts=$dir/multiverse generator=scripts/exp21/generate_multiverse.py ;;
    parallel) benches=${BENCHES:-$math} prompts=$dir/parallel generator=scripts/bench/eval_rollout.sh ;;
    *) echo "mode: no-thinking | thinking | parallel | multiverse"; exit 1 ;;
esac
# REUSE: only the finished C0 frozen 16k runs of 2026-10-06 (queue logs gpu3.log / gpu0.log, exit 0):
#   cd /work/bench-src && bash scripts/bench/run_bench.sh qwen3-4b-<nothinking|thinking>-16k /work/assets/models/Qwen3-4B <mode> 16384
# Each benchmark's own log there must also show this model and max_seq_len = budget + 2048 (generate_plain.py), checked before scoring.
reuse_provenance=
if [ -n "${REUSE:-}" ]; then
    case "$mode:$REUSE" in
        no-thinking:/work/bench/qwen3-4b-nothinking-16k) reuse_provenance="queue gpu3 2026-10-06 15:01:10-15:38:17 exit=0" ;;
        thinking:/work/bench/qwen3-4b-thinking-16k) reuse_provenance="queue gpu0 2026-10-06 15:54:08-22:04:09 exit=0" ;;
        *) echo "REUSE only /work/bench/qwen3-4b-nothinking-16k (no-thinking) or /work/bench/qwen3-4b-thinking-16k (thinking)"; exit 1 ;;
    esac
    [ "$suite $model $budget" = "frozen /work/assets/models/Qwen3-4B 16384" ] || { echo "REUSE only for frozen /work/assets/models/Qwen3-4B 16384"; exit 1; }
    reuse_provenance="$reuse_provenance: cd /work/bench-src && bash scripts/bench/run_bench.sh ${REUSE##*/} $model $mode $budget"
fi
mkdir -p "$run/results" "$run/rows"
export PYTHONPATH=$repo/verl:/work/assets/ifeval/pkg NLTK_DATA=/work/assets/ifeval/nltk_data RAY_TMPDIR=/tmp/ray_${name}_$$
# private Ray dir per process; Ray's socket <dir>/session_<date>_<pid>/sockets/plasma_store must stay within the 107-byte AF_UNIX limit
if [ "$mode" = parallel ] && [ ${#RAY_TMPDIR} -gt 45 ]; then echo "RAY_TMPDIR $RAY_TMPDIR too long for Ray sockets: use a shorter name"; exit 1; fi
export PARALLEL_ROLLOUT_ENABLE_THINKING=false  # read by the rollout only
export EXP21_TOKENIZER=$model  # score.py: forward passes of Multiverse answers in this model's tokens
export SCORE_IFEVAL_SEED=0  # deterministic IFEval checker in score.py (per prompt key); fixed protocol, not a tuning knob
# the verl that score.py and the rollout import (outside the repo, the cwd is not on the path): this checkout, not /work/setup-src
(cd / && python -c "import sys, verl; assert verl.__file__ == sys.argv[1], verl.__file__" "$repo/verl/verl/__init__.py")
cd "$repo/verl"

# protocol record, created or checked under a lock; prints the commit
commit=$(python - "$run/meta.json" <<EOF
import fcntl, json, os, subprocess, sys
path = sys.argv[1]
git = lambda *args: subprocess.run(["git", "-C", "$repo", *args], capture_output=True, text=True)  # noqa: E731
head, status = git("rev-parse", "HEAD"), git("status", "--porcelain", "--untracked-files=no", "--", "scripts", "verl")
commit = head.stdout.strip() if head.returncode == 0 and status.returncode == 0 else None
if commit is None and not (os.environ.get("EVAL_ALLOW_UNVERSIONED") == "1" and "${REUSE:-}"):
    sys.exit("$repo: no git commit; EVAL_ALLOW_UNVERSIONED=1 is only for CPU tests with REUSE")
if commit and status.stdout.strip():
    sys.exit(f"uncommitted code changes, commit them first:\n{status.stdout}")
meta = {"model": "$model", "suite": "$suite", "mode": "$mode", "budget": $budget, "temperature": 1.0, "top_p": 1.0,
        "generator": "$generator", "prompts": "$prompts", "reused_from": "${REUSE:-}" or None,
        **({"reuse_provenance": "$reuse_provenance", "reuse_source_logs": "${REUSE:-}/<bench>.log"} if "${REUSE:-}" else {}),
        "ifeval_scorer_seed": int(os.environ["SCORE_IFEVAL_SEED"]),
    "seeds": {"scripts/instruct4b_eval/generate.py": "sample index", "scripts/bench/generate_plain.py": "0 for every row",
                  "scripts/bench/eval_rollout.sh": "unseeded",
                  "scripts/exp21/generate_multiverse.py": "sample index for Goal; 100*sample+path for paths; 100*sample+99 for suffix"}["$generator"],
        "commit": commit, **({} if commit else {"unversioned_test_only": True})}
with open(path + ".lock", "w") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    if os.path.exists(path):
        old = json.load(open(path))
        differs = {k: (old.get(k), meta.get(k)) for k in old.keys() | meta.keys() if old.get(k) != meta.get(k)}
        if differs:
            sys.exit(f"{path} has other settings or code (old, now): {differs}")
    else:
        json.dump(meta, open(path + ".tmp", "w"), indent=1)
        os.replace(path + ".tmp", path)
print(commit)
EOF
)

for bench in $benches; do
    test=$prompts/$bench.parquet
    log=$run/$bench.log
    if [ -e "$run/rows/$bench.jsonl" ]; then  # finished earlier: the rows must be this test's rows, else stop
        python - "$run/rows/$bench.jsonl" "$test" "$run/results/$bench.json" <<'EOF'
import os, sys
import pandas as pd
rows, test = pd.read_json(sys.argv[1], lines=True), pd.read_parquet(sys.argv[2])
problems = pd.Series([p[0]["content"] for p in test["prompt"]])
sources = test["data_source"].str.removeprefix("APO_")
order = {p: n for n, p in enumerate(dict.fromkeys(problems))}
expected = {"source": sources, "problem": problems, "sample": problems.groupby(problems).cumcount(),
            "problem_id": [i.get("id") or f"{s}/{order[p]}" for i, s, p in zip(test["extra_info"], sources, problems)]}
ok = os.path.exists(sys.argv[3]) and len(rows) == len(test) and all(
    c in rows and (rows[c].astype(str).to_numpy() == pd.Series(v).astype(str).to_numpy()).all() for c, v in expected.items())
if not ok:
    sys.exit(f"{sys.argv[1]} is not a finished scoring of {sys.argv[2]}. Recover: move it and {sys.argv[3]} aside "
             f"(mv <file> <file>.stale-<date>), then rerun; other files of the run are kept")
EOF
        continue
    fi
    stamp=$(date +%Y%m%d-%H%M%S)
    for old in "$log" "$run/$bench.jsonl" "$run/$bench"; do  # an unfinished attempt: keep its dumps and log under another name
        if [ -e "$old" ]; then mv "$old" "$old.incomplete-$stamp"; fi
    done
    echo "commit $commit, $name $model $suite $mode $budget $bench" > "$log"
    if [ -n "${REUSE:-}" ]; then
        generations=$REUSE/$bench.jsonl
        grep -qF "model='$model'" "$REUSE/$bench.log" && grep -qF "max_seq_len=$((budget + 2048))" "$REUSE/$bench.log" \
            || { echo "$REUSE/$bench.log does not show model='$model' and max_seq_len=$((budget + 2048))"; exit 1; }
        echo "reused $generations; $reuse_provenance; source log $REUSE/$bench.log" >> "$log"
    elif [ "$mode" = parallel ]; then
        generations=$run/$bench/generations/0.jsonl
        bash ../scripts/bench/eval_rollout.sh "$model" "$run/$bench" "$test" "$budget" >> "$log" 2>&1
        # every AgentLoopWorker must log the non-thinking kwargs; none may log others ({} = env unset). The mismatches are collected
        # first: a negated `grep | grep -q` pipeline can pass under pipefail when the first grep gets SIGPIPE.
        other=$(grep "Parallel rollout chat template kwargs:" "$log" | grep -vF "{'enable_thinking': False}" || true)
        grep -q "Parallel rollout chat template kwargs: {'enable_thinking': False}" "$log" && [ -z "$other" ] \
            || { echo "rollout template not non-thinking: $log"; exit 1; }
    else
        generations=$run/$bench.jsonl
        if [ "$mode" = multiverse-branch ]; then
            python "../$generator" "$model" "$test" "$generations" "$budget" >> "$log" 2>&1
        else
            python "../$generator" "$model" "$test" "$generations" "$budget" "${mode/multiverse/no-thinking}" >> "$log" 2>&1
        fi
    fi
    # the dumped prompts must be rendered in the requested mode (empty think block = non-thinking template).
    # parallel: the dump's input is RLHFDataset's default-template prompt (ray_trainer._validate decodes the dataset input_ids
    # before the rollout), not the agent-loop prompt; that one is gated by the Ray-log check above. Here: no output opens a think block.
    python - "$generations" "$mode" <<'EOF'
import sys
import pandas as pd
dump, mode = pd.read_json(sys.argv[1], lines=True), sys.argv[2]
if mode == "parallel":
    thinking = dump["output"].str.contains("<think>", regex=False)
    assert not thinking.any(), f"{thinking.sum()} parallel outputs with a think block"
else:
    empty_think = dump["input"].str.contains("<think>\n\n</think>", regex=False)
    assert (empty_think if mode != "thinking" else ~empty_think).all(), f"{(~empty_think).sum()} prompts without an empty think block ({mode})"
EOF
    python ../scripts/bench/score.py "$generations" "$test" "$run/results/$bench.json.tmp" "$run/rows/$bench.jsonl.tmp" >> "$log" 2>&1
    mv "$run/results/$bench.json.tmp" "$run/results/$bench.json"
    mv "$run/rows/$bench.jsonl.tmp" "$run/rows/$bench.jsonl"  # last: the rows file marks the benchmark finished
done
