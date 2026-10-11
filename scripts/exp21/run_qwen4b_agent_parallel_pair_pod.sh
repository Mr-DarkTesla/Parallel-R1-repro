#!/usr/bin/env bash
# Explicit one-GPU launch on owned vcharkin-exp-vm-0 only. Never run as a watcher.
set -euo pipefail

test "$(hostname)" = vcharkin-exp-vm-0
repo=${EXP21_REPO:-/work/parallel-r1}
data=${EXP21_PAIR_DATA:-/checkpoints/exp21-agent-parallel}
sampler=${EXP21_SAMPLER_ROOT:-/checkpoints/exp21-clean46-onpolicy143}
parent=${EXP21_PARENT_MODEL:-/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model}
runroot=${EXP21_RUN_ROOT:-/tmp/exp21-selective-runs}
name=${EXP21_RUN_PREFIX:-exp21-4b-agent-parallel}
[[ "$name" =~ ^exp21-4b-[a-z0-9-]+$ ]] || { echo 'unsafe run name' >&2; exit 1; }
case "$runroot" in /tmp/*) ;; *) echo 'model exports must stay ephemeral under /tmp' >&2; exit 1 ;; esac
mkdir -p "$runroot"
runroot=$(realpath "$runroot")
case "$runroot" in /tmp/*) ;; *) echo 'runroot resolves outside /tmp' >&2; exit 1 ;; esac
mkdir -p "$data"
case "$(realpath "$data")" in
    /work/*|/checkpoints/*) ;;
    *) echo 'pair data and archives must live on persistent /work or /checkpoints' >&2; exit 1 ;;
esac
test -s "$sampler/FILTER_DONE" || { echo 'on-policy sampler filter is unfinished' >&2; exit 1; }
grep -q ' status=0$' "$sampler/ATTEMPT_DONE" || { echo 'sampler failed' >&2; exit 1; }
test -s "$parent/config.json"
test -s "$data/sft_build_report.json"
for arm in tagged plain; do
    test -s "$data/sft_${arm}_train.parquet"
    test -s "$data/sft_${arm}_val.parquet"
done

exec 9>"$data/runner.lock"
flock -n 9 || { echo 'paired runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$data/ATTEMPT_DONE"' EXIT

source /work/venv/bin/activate
python - "$data/sft_build_report.json" "$data" "$repo/scripts/exp21" "$parent" <<'PY'
import json, pathlib, sys, unicodedata
import pandas as pd
from transformers import AutoTokenizer

sys.path.insert(0, sys.argv[3])
from mv_format import TAGS, strip_tags
from reconcile_global_top5_pod import build_plan

def norm(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split()).casefold()

report = json.load(open(sys.argv[1]))
root = pathlib.Path(sys.argv[2])
parent = pathlib.Path(sys.argv[4]).resolve(strict=True)
checkpoint_root = pathlib.Path('/checkpoints').resolve(strict=True)
manifest = checkpoint_root / 'exp21-global-top5/GLOBAL_TOP5.json'
plan = build_plan(checkpoint_root, manifest)
assert len(plan['kept']) == len(plan['all_models']) == 5 and not plan['remove_models']
assert parent in plan['kept'], 'parent must be a model in the validated global TOP-5'
tokenizer = AutoTokenizer.from_pretrained(parent, local_files_only=True)
added = tokenizer.get_added_vocab()
tag_ids = {tag: tokenizer.encode(tag, add_special_tokens=False) for tag in TAGS}
assert len(TAGS) == 10 and all(len(ids) == 1 and tag in added and tag in tokenizer.all_special_tokens
                               and ids[0] == added[tag] for tag, ids in tag_ids.items())
assert len({ids[0] for ids in tag_ids.values()}) == 10, 'Multiverse tags must have distinct special token IDs'
assert report['status'] == 'ready_for_paired_sft'
assert report['accepted']['count'] >= 46
review = report['accepted']['review']
assert review['status'] == 'passed' and review['reviewed'] >= 30
assert review['useful'] * 10 >= review['reviewed'] * 9 and review['wrong_final'] == 0
assert report['checks']['train_val_fixed40_holdout_overlap'] == 0
assert report['checks']['plain_transform'] == 'mv_format.strip_tags'
assert report['checks']['same_prompts_and_order']
assert report['checks']['length_method'] == 'ParallelThinkingSFTDataset chat template and separate prompt/response tokenization'
assert all(value <= 4096 for sizes in report['checks']['max_total_tokens'].values() for value in sizes.values())
maxima = {}
for split in ('train', 'val'):
    tagged = pd.read_parquet(root / f'sft_tagged_{split}.parquet').to_dict('records')
    plain = pd.read_parquet(root / f'sft_plain_{split}.parquet').to_dict('records')
    assert len(tagged) == len(plain) == report['rows_per_arm'][split]
    maxima[split] = {'tagged': 0, 'plain': 0}
    for left, right in zip(tagged, plain):
        assert left['id'] == right['id']
        assert left['extra_info']['question'] == right['extra_info']['question']
        assert norm(strip_tags(left['extra_info']['answer'])) == norm(right['extra_info']['answer'])
    for arm, rows in (('tagged', tagged), ('plain', plain)):
        for row in rows:
            info = row['extra_info']
            prompt = tokenizer.apply_chat_template(
                [{'role': 'user', 'content': info['question']}],
                add_generation_prompt=True, tokenize=False,
                enable_thinking=bool(info['enable_thinking']))
            length = len(tokenizer(prompt, add_special_tokens=False)['input_ids'])
            length += len(tokenizer(info['answer'] + tokenizer.eos_token,
                                    add_special_tokens=False)['input_ids'])
            assert length <= 4096, (arm, split, row['id'], length)
            maxima[split][arm] = max(maxima[split][arm], length)
(root / 'preflight_parent.json').write_text(json.dumps({
    'parent': str(parent), 'global_top5_manifest': str(manifest),
    'tag_ids': {tag: ids[0] for tag, ids in tag_ids.items()},
    'trainer_exact_max_total_tokens': maxima}, indent=2) + '\n')
PY

busy_gpu() {
    if pgrep -f '[t]orchrun.*fsdp_parallel_sft_trainer|[g]enerate_masked_multiverse.py|[g]enerate_onpolicy_masked.py|[s]cripts/instruct4b_eval/generate.py|[s]cripts/bench/generate_plain.py|[v]llm.entrypoints' >/dev/null; then
        return 0
    fi
    if command -v nvidia-smi >/dev/null && [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d '[:space:]')" ]; then
        return 0
    fi
    return 1
}

cd "$repo"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
archive_root="$data/archives"
mkdir -p "$archive_root"
# Model exports stay on /tmp for manual semantic/accuracy ranking. Only raw
# outputs and train metadata go to the persistent data root; promotion is manual.
archive_training() {
    local arm=$1 run="${name}-$1-p32" target="$archive_root/${name}-$1-training.tgz"
    test -s "$runroot/$run/DONE"
    if test -e "$target"; then
        tar -tzf "$target" >/dev/null || { echo "invalid existing archive: $target" >&2; exit 1; }
        return 0
    fi
    tar -czf "$target.tmp" -C "$runroot" \
        "$run/train.log" "$run/results" "$run/DONE" "$run/TRAINED"
    mv "$target.tmp" "$target"
    test -s "$target"
}
archive_fixed40() {
    local arm=$1 evalroot="/tmp/${name}-$1-fixed40" target="$archive_root/${name}-$1-fixed40.tgz"
    test -s "$evalroot/DONE"
    if test -e "$target"; then
        tar -tzf "$target" >/dev/null || { echo "invalid existing archive: $target" >&2; exit 1; }
        return 0
    fi
    if find "$evalroot" -type f \( -name '*.safetensors' -o -name '*.bin' \) -print -quit | grep -q .; then
        echo 'refusing to archive model weights with raw evaluation' >&2; exit 1
    fi
    tar -czf "$target.tmp" -C /tmp "$(basename "$evalroot")"
    mv "$target.tmp" "$target"
    test -s "$target"
}
for arm in tagged plain; do
    busy_gpu && { echo 'another GPU process is active on owned pod' >&2; exit 1; }
    overrides=(optim.tag_lr_mult=100)
    if [ "$arm" = tagged ]; then
        overrides+=(+data.structure=multiverse +data.parallel_text_loss_weight=1.0)
    else
        overrides+=(+data.structure=parallel_r1)
    fi
    RUN_ROOT="$runroot" RUN_NAME="${name}-${arm}-p32" \
    MODEL="$parent" DATA_PATH="$data/sft_${arm}_train.parquet" VAL_PATH="$data/sft_${arm}_val.parquet" \
    NGPUS=1 STEPS=32 SAVE_STEPS=8,16,32 LR=5e-7 BATCH=16 MICRO_BATCH=1 \
    MAX_LENGTH=4096 MIN_FREE_GB=30 \
    bash scripts/instruct4b/sft.sh "${overrides[@]}"
    archive_training "$arm"
done
date -Is > "$data/TRAIN_PAIR_DONE"

for arm in tagged plain; do
    busy_gpu && { echo 'another GPU process is active before evaluation' >&2; exit 1; }
    run="$runroot/${name}-${arm}-p32"
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/${name}-${arm}-fixed40" \
        EXP21_STEPS=8,16,32 bash scripts/exp21/eval_checkpoint_steps_pod.sh
    archive_fixed40 "$arm"
done
for arm in tagged plain; do
    test -s "$archive_root/${name}-${arm}-training.tgz"
    test -s "$archive_root/${name}-${arm}-fixed40.tgz"
done
test -s "$data/preflight_parent.json"
date -Is > "$data/EVAL_DONE"
echo 'Raw results archived. Rank semantic blocks and accuracy, then promote at most one model manually into global TOP-5.'
