"""Prepare matched Deep51 2x tagged/plain SFT datasets without training."""

import collections
import hashlib
import json
import os
from copy import deepcopy
from pathlib import Path

import pandas as pd

from prepare_deep51_pair import (
    CONTROL_COUNT, CONTROL_SEED, DEEP, DEEP_AUDIT, DEEP_LEAK, GLOBAL_LEAK,
    ORDER_SEED, POOL, RECOVERY_TRAIN, RECOVERY_VAL, SHARED_VAL, load_jsonl,
    normalize, pilot_questions, plain_response, stable_rank,
)
from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
TAGGED_TRAIN = DATA / "sft_deep51_2x_tagged_train.parquet"
PLAIN_TRAIN = DATA / "sft_deep51_2x_plain_train.parquet"
PLAN = DATA / "sft_deep51_2x_pair_quality.json"

POSITIVE_COPIES = 2
REPLAY_COUNT = 109
REPLAY_SEED = "deep51-2x-replay-20261012"
ORDER_SEED_2X = "deep51-2x-order-20261012"
# 109 rows proportional to recovery8's 80/50/30 replay split, with the
# largest remainder assigned to MATH: 55 + 34 + 20 = 109.
REPLAY_BY_SOURCE = {"math": 55, "gsm8k": 34, "arc": 20}


def recovery_rows():
    frame = pd.read_parquet(RECOVERY_TRAIN)
    assert len(frame) == len(set(frame.id)) == 256
    rows = frame.to_dict("records")
    controls = [row for row in rows if row["extra_info"]["kind"] == "control_th"]
    replay = [row for row in rows if row["extra_info"]["kind"] == "replay_th"]
    assert len(controls) == 50 and len(replay) == 160
    return controls, replay


def select_replay(replay, deep_ids):
    eligible = [row for row in replay if row["id"] not in deep_ids]
    selected = []
    for source, count in REPLAY_BY_SOURCE.items():
        group = [row for row in eligible if row["source"] == source]
        ranked = sorted(group, key=lambda row: (stable_rank(REPLAY_SEED, row["id"]), row["id"]))
        assert len(group) >= count
        selected.extend(ranked[:count])
    assert len(selected) == REPLAY_COUNT
    assert len({row["id"] for row in selected}) == REPLAY_COUNT
    return selected


def add_positive_rows(deep, tagged, plain):
    for source in deep:
        structure = parse(source["response"])
        assert structure["valid"] and len(structure["blocks"]) == 1
        for copy_index in range(POSITIVE_COPIES):
            prompt = mv_prompt(HEADER + source["question"])
            tagged.append({
                "data_source": f"exp21_deep51_2x_tagged_copy{copy_index + 1}",
                "id": source["id"], "source": "math", "copy_index": copy_index,
                "extra_info": {"question": prompt, "answer": source["response"],
                               "enable_thinking": True, "kind": "parallel_th", "id": source["id"]},
            })
            plain.append({
                "data_source": f"exp21_deep51_2x_plain_copy{copy_index + 1}",
                "id": source["id"], "source": "math", "copy_index": copy_index,
                "extra_info": {"question": prompt, "answer": plain_response(source["response"]),
                               "enable_thinking": True, "kind": "control_th", "id": source["id"]},
            })


def main():
    deep = load_jsonl(DEEP)
    deep_audit = {row["id"]: row for row in load_jsonl(DEEP_AUDIT)}
    pool = {row["id"]: row for row in load_jsonl(POOL)}
    deep_ids = {row["id"] for row in deep}
    assert len(deep) == len(deep_ids) == 51
    for row in deep:
        review = deep_audit[row["id"]]["review"]
        assert row["gold_answer"] == pool[row["id"]]["answer"]
        assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
        assert review["independent_paths"] and review["source_preserved"]

    controls, replay = recovery_rows()
    controls = [row for row in controls if row["id"] not in deep_ids]
    controls = sorted(controls, key=lambda row: (stable_rank(CONTROL_SEED, row["id"]), row["id"]))[:CONTROL_COUNT]
    replay = select_replay(replay, deep_ids)
    assert len(controls) == CONTROL_COUNT
    assert not ({row["id"] for row in controls} & {row["id"] for row in replay})

    tagged, plain = [], []
    add_positive_rows(deep, tagged, plain)
    other = controls + replay
    for row in other:
        row["copy_index"] = 0
    tagged.extend(deepcopy(other))
    plain.extend(deepcopy(other))
    assert len(tagged) == len(plain) == 102 + CONTROL_COUNT + REPLAY_COUNT == 256

    def order_key(row):
        return (stable_rank(ORDER_SEED_2X, f"{row['id']}\0{row.get('copy_index', 0)}"),
                row["id"], row.get("copy_index", 0))

    tagged.sort(key=order_key)
    plain.sort(key=order_key)
    for index, (left, right) in enumerate(zip(tagged, plain)):
        left["index"] = right["index"] = index
        assert left["id"] == right["id"] and left.get("copy_index") == right.get("copy_index")
        if left["id"] not in deep_ids:
            assert left == right

    val = pd.read_parquet(RECOVERY_VAL)
    train_questions = {normalize(pool[row["id"]]["question"]) for row in tagged}
    val_questions = {normalize(pool[row_id]["question"]) for row_id in val.id}
    pilot = pilot_questions()
    assert not train_questions & val_questions and not train_questions & pilot and not val_questions & pilot
    leak = json.loads(GLOBAL_LEAK.read_text())
    deep_leak = json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0

    report = {
        "status": "prepared",
        "candidate": "deep51-2x-paired",
        "seeds": {"control": CONTROL_SEED, "replay": REPLAY_SEED, "order": ORDER_SEED_2X},
        "train": {
            "rows": 256, "unique_ids": len({row["id"] for row in tagged}),
            "positive_rows": len(deep) * POSITIVE_COPIES, "unique_positive_ids": len(deep_ids),
            "positive_copies_per_id": POSITIVE_COPIES,
            "control_rows": len(controls), "replay_rows": len(replay),
            "replay_by_source": dict(collections.Counter(row["source"] for row in replay)),
            "deep51_ids": sorted(deep_ids), "control_th_ids": [row["id"] for row in controls],
            "replay_th_ids": [row["id"] for row in replay],
            "row_order": [{"id": row["id"], "copy_index": row.get("copy_index", 0)} for row in tagged],
            "tagged_kind_counts": dict(collections.Counter(row["extra_info"]["kind"] for row in tagged)),
            "plain_kind_counts": dict(collections.Counter(row["extra_info"]["kind"] for row in plain)),
        },
        "transform": {"tagged": "accepted51 copied verbatim twice", "plain": "same paths with only structural Multiverse scaffolding removed", "underlying_solution_equivalence": 102},
        "overlap": {"train_val_normalized_question": 0, "train_pilot40_normalized_question": 0, "val_pilot40_normalized_question": 0},
        "leakcheck": {"deep51_eval_leaks": 0, "deep51_eval_dup_or_variant": 0, "global_pool": GLOBAL_LEAK.name, "deep51": DEEP_LEAK.name},
    }
    outputs = [(TAGGED_TRAIN, pd.DataFrame(tagged)), (PLAIN_TRAIN, pd.DataFrame(plain))]
    temporary = []
    try:
        for path, frame in outputs:
            temp = path.with_suffix(".tmp.parquet")
            frame.to_parquet(temp, index=False)
            temporary.append((path, temp))
        report_temp = PLAN.with_suffix(".tmp.json")
        report_temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        temporary.append((PLAN, report_temp))
        for path, temp in temporary:
            os.replace(temp, path)
    finally:
        for _, temp in temporary:
            temp.unlink(missing_ok=True)
    print(json.dumps(report["train"], ensure_ascii=False))


if __name__ == "__main__":
    main()
