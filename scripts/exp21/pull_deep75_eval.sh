#!/usr/bin/env bash
# Copy one completed exp21 evaluation from the owner's pod for local analysis.
set -euo pipefail
name=${1:?pass run name, e.g. deep75-dev-th}
case "$name" in
    deep75-* | deep75-control-*) ;;
    *) echo "unexpected run name: $name" >&2; exit 2 ;;
esac
repo=$(cd "$(dirname "$0")/../.." && pwd)
dest="$repo/results/21-qwen3-0.6b-multiverse"
context=tele.corp.mail.ru-k8s_ml_MNTINFRA_3322
namespace=shared-dzen-ml
pod=vcharkin-exp-vm-0
kubectl --context "$context" -n "$namespace" exec "$pod" -- bash -lc \
    "test \"\$(cat /work/exp21/logs/eval-$name.exit)\" = 0 && tar -czf /tmp/$name.tgz -C /work/exp21/eval $name"
kubectl --context "$context" -n "$namespace" cp "$pod:/tmp/$name.tgz" "$dest/eval_archives/$name.tgz"
tar -tzf "$dest/eval_archives/$name.tgz" >/dev/null
tar -xzf "$dest/eval_archives/$name.tgz" -C "$dest/eval_runs"
echo "$name archived and extracted"
