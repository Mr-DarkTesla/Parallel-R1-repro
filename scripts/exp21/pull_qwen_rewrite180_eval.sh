#!/usr/bin/env bash
set -euo pipefail

name=${1:?pass qwen-rewrite180-* eval name}
case "$name" in
    qwen-rewrite180-dev-mvth | qwen-rewrite180-dev-th | qwen-rewrite180-dev-nt | \
    qwen-rewrite180-ifeval-th | qwen-rewrite180-ifeval-nt | \
    qwen-rewrite180-control-dev-mvth | qwen-rewrite180-control-dev-th | \
    qwen-rewrite180-control-dev-nt | qwen-rewrite180-control-ifeval-th | \
    qwen-rewrite180-control-ifeval-nt) ;;
    *) echo "unexpected run name: $name" >&2; exit 2 ;;
esac
repo=$(cd "$(dirname "$0")/../.." && pwd)
dest="$repo/results/21-qwen3-0.6b-multiverse"
context=tele.corp.mail.ru-k8s_ml_MNTINFRA_3322
namespace=shared-dzen-ml
pod=vcharkin-exp-vm-0
kubectl --context "$context" -n "$namespace" exec "$pod" -- bash -lc \
    "test \"\$(cat /work/exp21/logs/eval-$name.exit)\" = 0 && tar -czf /tmp/$name.tgz -C /work/exp21/eval $name"
mkdir -p "$dest/eval_archives" "$dest/eval_runs"
kubectl --context "$context" -n "$namespace" cp --retries=3 "$pod:/tmp/$name.tgz" "$dest/eval_archives/$name.tgz"
tar -tzf "$dest/eval_archives/$name.tgz" >/dev/null
tar -xzf "$dest/eval_archives/$name.tgz" -C "$dest/eval_runs"
echo "$name archived and extracted"
