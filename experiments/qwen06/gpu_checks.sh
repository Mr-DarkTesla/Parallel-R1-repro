#!/usr/bin/env bash
# GPU checks of the qwen3-0.6b-rl branch in one run, on a fresh vast.ai instance or on the GCP VM.
#   setup         bootstrap_vm.sh (uv environment, checkout); an existing clean checkout of the branch is fast-forwarded
#   prepare       prepare_think.py --smoke-model: think data (Hugging Face fallback) and Qwen3-0.6B with the tags
#   unit_tests    pytest tests experiments, test_vllm_graph.py included (the real vLLM 0.8.5 scheduler)
#   graph_forced  check_graph_rollout.py, forced blocks: every token vLLM samples vs. the HF graph forward
#   graph_evict   the same with --blocks 160: held branch KV fills the cache, trajectories are evicted and rebuilt
#   smoke_flat    SMOKE=1 run_rl.sh think: one update, flat_packed log-probs
#   smoke_graph   the same with GRAPH_ROLLOUT=true (tree log-probs)
# A failed step does not stop the next ones, except setup. The block between the GPU CHECK SUMMARY lines at the
# end is what to send back; logs and JSON stay in $PARALLEL_R1_ROOT/runs/gpu-checks/<time> (and .../latest).
#
#   curl -fsSL https://raw.githubusercontent.com/Mr-DarkTesla/Parallel-R1-repro/qwen3-0.6b-rl/experiments/qwen06/gpu_checks.sh -o ~/gpu_checks.sh
#   nohup bash ~/gpu_checks.sh > ~/gpu-checks.log 2>&1 < /dev/null &    # the log ends with GPU_CHECKS_DONE
#   STEPS="graph_forced graph_evict" bash ~/gpu_checks.sh                 # only these steps (setup always runs)
set -uo pipefail

main() {
  export PATH="$HOME/.local/bin:$PATH"
  ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
  BRANCH=${PARALLEL_R1_BRANCH:-qwen3-0.6b-rl}
  export PARALLEL_R1_ROOT=$ROOT PARALLEL_R1_BRANCH=$BRANCH
  REPO=$ROOT/repo
  PY=$ROOT/.venv/bin/python
  SMOKE_MODEL=$ROOT/models/smoke-qwen3-0.6b-think
  STAMP=$(date -u +%Y%m%d-%H%M%S)
  OUT=$ROOT/runs/gpu-checks/$STAMP
  mkdir -p "$OUT" && ln -sfn "$OUT" "$ROOT/runs/gpu-checks/latest"
  : > "$OUT/steps.tsv"

  if ! step preflight 60 preflight || ! step setup 0 setup; then
    summary
    return 1
  fi
  cd "$REPO" || return 1
  if [ -f "$SMOKE_MODEL/SMOKE_ONLY" ] && [ -f "$ROOT/data/think_smoke_train.parquet" ] && [ "${REPREPARE:-0}" != 1 ]; then
    step prepare 60 echo "Reusing $SMOKE_MODEL and $ROOT/data (REPREPARE=1 rebuilds them)"
  else
    step prepare 3600 "$PY" experiments/qwen06/prepare_think.py --root "$ROOT" --smoke-model
  fi
  step unit_tests 3600 env PYTHONPATH="$REPO/verl:$REPO/experiments/qwen06" \
    "$PY" -m pytest tests experiments -q -p no:cacheprovider
  step graph_forced 1800 "$PY" experiments/qwen06/check_graph_rollout.py "$SMOKE_MODEL" --out "$OUT/graph_forced.json"
  step graph_evict 1800 "$PY" experiments/qwen06/check_graph_rollout.py "$SMOKE_MODEL" --blocks 160 \
    --out "$OUT/graph_evict.json"
  # One update each; no checkpoint (it would write the optimizer state of 0.6B parameters for nothing).
  step smoke_flat 2700 env -u LOGPROB_CONTEXT SMOKE=1 GRAPH_ROLLOUT=false RUN_NAME="gpu-check-$STAMP-flat" \
    bash experiments/qwen06/run_rl.sh think "$SMOKE_MODEL" trainer.save_freq=-1
  stop_ray
  step smoke_graph 2700 env -u LOGPROB_CONTEXT SMOKE=1 GRAPH_ROLLOUT=true RUN_NAME="gpu-check-$STAMP-graph" \
    bash experiments/qwen06/run_rl.sh think "$SMOKE_MODEL" trainer.save_freq=-1
  stop_ray
  summary
}

# step NAME LIMIT COMMAND...: runs COMMAND (a function here, or a program under `timeout LIMIT`) with its output
# in $OUT/NAME.log and records the exit code. STEPS limits which steps run; preflight and setup always do.
step() {
  local name=$1 limit=$2 start code
  shift 2
  if [ -n "${STEPS:-}" ] && [[ " preflight setup $STEPS " != *" $name "* ]]; then return 0; fi
  start=$(date +%s)
  echo "== $(date -u +%H:%M:%S) $name: started, log $OUT/$name.log"
  if declare -F "$1" > /dev/null; then
    ("$@") > "$OUT/$name.log" 2>&1 < /dev/null
  else
    timeout --kill-after=60 "$limit" "$@" > "$OUT/$name.log" 2>&1 < /dev/null
  fi
  code=$?
  printf '%s\t%s\t%s\n' "$name" "$code" "$(($(date +%s) - start))" >> "$OUT/steps.tsv"
  echo "== $(date -u +%H:%M:%S) $name: exit $code"
  return "$code"
}

preflight() {
  command -v nvidia-smi > /dev/null || { echo 'nvidia-smi not found: no NVIDIA driver here'; return 1; }
  nvidia-smi
  echo "gpu: $(nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader | head -1)"
  echo "disk: $(df -Ph "$HOME" | awk 'NR == 2 {print $4 " free of " $2}') on $HOME"
  local used free need=25
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | sort -n | tail -1)
  if [ "${used:-0}" -gt 2048 ] && [ "${FORCE:-0}" != 1 ]; then
    echo "The GPU already has $used MiB in use: stop the other job first (FORCE=1 skips this check)"
    return 1
  fi
  [ -x "$PY" ] && need=8
  free=$(df -Pk "$HOME" | awk 'NR == 2 {print int($4 / 1048576)}')
  if [ "$free" -lt "$need" ]; then
    echo "Only $free GB free on $HOME; the environment, models and data need about $need GB"
    return 1
  fi
}

setup() {
  if [ -d "$REPO/.git" ]; then
    local current
    git -C "$REPO" fetch -q origin "$BRANCH" || return 1
    current=$(git -C "$REPO" rev-parse --abbrev-ref HEAD)
    if [ "$current" != "$BRANCH" ]; then
      echo "$REPO is on $current, not $BRANCH; switch it yourself, the checks do not"
      return 1
    fi
    if [ -n "$(git -C "$REPO" status --porcelain --untracked-files=no)" ]; then
      echo "$REPO has local changes; testing them as they are"
    else
      git -C "$REPO" merge -q --ff-only "origin/$BRANCH" || return 1
    fi
    bash "$REPO/experiments/qwen06/bootstrap_vm.sh" || return 1
  else
    curl -fsSL "https://raw.githubusercontent.com/Mr-DarkTesla/Parallel-R1-repro/$BRANCH/experiments/qwen06/bootstrap_vm.sh" \
      -o "$OUT/bootstrap_vm.sh" && bash "$OUT/bootstrap_vm.sh" || return 1
  fi
  echo "commit: $(git -C "$REPO" log -1 --format='%h %s')"
  "$PY" -c 'import torch, vllm, transformers, flash_attn
props = torch.cuda.get_device_properties(0)
print(f"versions: torch {torch.__version__} (CUDA {torch.version.cuda}) vllm {vllm.__version__} transformers"
      f" {transformers.__version__} flash_attn {flash_attn.__version__} | {props.name} {props.total_memory / 2**30:.0f} GiB")'
}

stop_ray() {
  [ -x "$ROOT/.venv/bin/ray" ] && "$ROOT/.venv/bin/ray" stop --force > /dev/null 2>&1
  return 0
}

summary() {
  local python=python3
  [ -x "$PY" ] && python=$PY
  "$python" - "$OUT" << 'PY' | tee "$OUT/summary.txt"
import json
import re
import sys
from pathlib import Path

out = Path(sys.argv[1])
SEGMENTS = ('main_before_fork', 'path_block1', 'path_later', 'summary_block1', 'summary_later', 'main_after_fork',
            'plan_block1', 'plan_later')
METRIC = re.compile(r'([A-Za-z0-9_@./+-]+):(-?(?:[0-9.]+(?:e[+-]?[0-9]+)?|nan|inf))')


def lines_with(text, *prefixes):
    return [line for line in text.splitlines() if line.startswith(prefixes)]


def graph(name):
    path = out / f'{name}.json'
    if not path.exists():
        return []
    result = json.loads(path.read_text())
    rows = [f"  {result['trajectories']} trajectories, {result['blocks']} blocks, statuses {result['statuses']}, "
            f"evicted requests {result['evicted_requests']}, kv_blocks {result['kv_blocks']}, "
            f"rollout {result['rollout_seconds']}s, checks {result['checks']}",
            f"  {'segment':<17}{'tokens':>7}   mean/max |vLLM - HF| (nats): graph | graph@physical | causal"]
    for segment, entry in result['segments'].items():
        cells = ' | '.join(f"{entry[k]['mean']:.4f}/{entry[k]['max']:.3f}"
                           for k in ('graph', 'graph_mask_physical_positions', 'causal'))
        rows.append(f"  {segment:<17}{entry['tokens']:>7}   {cells}   {'ok' if entry['ok'] else 'FAIL'}")
    return rows


def smoke(text):
    steps = [dict(METRIC.findall(line)) for line in text.splitlines() if 'training/global_step:' in line]
    if not steps:
        return []
    metrics = {key: float(value) for key, value in steps[-1].items()}
    rows = ['  ' + ', '.join(f'{key} {metrics[key]:.4g}' for key in (
        'response_length/mean', 'actor/pg_loss', 'actor/grad_norm', 'actor/entropy', 'timing_s/gen', 'timing_s/step')
        if key in metrics)]
    gaps = [f"{segment} {metrics[f'rollout_gap/{segment}_abs_mean']:.4f}/{metrics[f'rollout_gap/{segment}_abs_max']:.3f}"
            f" n={metrics[f'rollout_gap/{segment}_tokens']:.0f}" for segment in SEGMENTS + ('all',)
            if metrics.get(f'rollout_gap/{segment}_tokens', 0) > 0 and f'rollout_gap/{segment}_abs_mean' in metrics]
    rows.append('  rollout_gap mean/max: ' + ('; '.join(gaps) if gaps else 'not logged'))
    parallel = [f"{key.split('/', 1)[1]} {value:.3g}" for key, value in metrics.items() if key.startswith('parallel/')]
    if parallel:
        rows.append('  parallel: ' + ', '.join(parallel))
    validation = [f'{key} {value:.3g}' for key, value in metrics.items() if key.startswith('val')]
    if validation:
        rows.append('  ' + ', '.join(validation[:4]))
    return rows


print(f'===== GPU CHECK SUMMARY {out.name} =====')
failed = 0
records = [line.split('\t') for line in (out / 'steps.tsv').read_text().splitlines() if line]
for name, code, seconds in records:
    code = int(code)
    failed += code != 0
    log = out / f'{name}.log'
    text = log.read_text(errors='replace') if log.exists() else ''
    status = 'ok' if code == 0 else 'TIMEOUT' if code in (124, 137) else f'FAIL({code})'
    print(f'{name:<13}{status:<10}{seconds:>6}s')
    details = []
    if name == 'preflight':
        details = ['  ' + line for line in lines_with(text, 'gpu:', 'disk:')]
    elif name == 'setup':
        details = ['  ' + line for line in lines_with(text, 'commit:', 'versions:')]
    elif name == 'unit_tests':
        details = ['  ' + line for line in text.splitlines() if re.search(r'\d+ (passed|failed|error)', line)][-1:]
        details += ['  ' + line[:200] for line in lines_with(text, 'FAILED', 'ERROR')][:12]
    elif name.startswith('graph_'):
        details = graph(name)
    elif name.startswith('smoke_'):
        details = smoke(text)
    if details:
        print('\n'.join(details))
    if code:
        # Ray and vLLM keep logging after the exception, so name the last errors before the tail of the log.
        errors = list(dict.fromkeys(line.strip()[:240] for line in text.splitlines()
                                    if re.search(r'\b\w*(Error|Exception)\b: ', line)))[-3:]
        if errors:
            print('\n'.join('  error: ' + line for line in errors))
        tail = [line[:240] for line in text.splitlines() if line.strip()][-15:]
        print('  last lines of ' + str(log) + ':\n' + '\n'.join('    ' + line for line in tail))
print(f'===== END GPU CHECK SUMMARY: {failed} of {len(records)} steps failed; logs in {out} =====')
sys.exit(1 if failed else 0)
PY
  local code=$?
  echo "GPU_CHECKS_DONE exit=$code"
  return "$code"
}

main "$@"
exit $?
