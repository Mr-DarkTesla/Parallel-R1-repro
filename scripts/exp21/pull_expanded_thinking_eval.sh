#!/usr/bin/env bash
set -euo pipefail
name=${1:?pass expanded-th-m1-* or expanded-th-m2-* run name}
case "$name" in
    expanded-th-m1-dev-mvth | expanded-th-m1-dev-th | expanded-th-m1-dev-nt | \
    expanded-th-m1-ifeval-th | expanded-th-m1-ifeval-nt | \
    expanded-th-m2-dev-mvth | expanded-th-m2-dev-th | expanded-th-m2-dev-nt | \
    expanded-th-m2-ifeval-th | expanded-th-m2-ifeval-nt) ;;
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
