"""Prepare the matched Deep69 tagged/plain dataset without launching SFT.

The only tagged/plain difference is the structural Multiverse markup on the
69 independently reviewed positive traces.  Every other response, prompt and
row position is copied identically from an existing audited source.
"""

import collections
import hashlib
import json
import os
from copy import deepcopy
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import parse
from prepare_deep51_pair import (
    DEEP,
    DEEP_AUDIT,
    DEEP_LEAK,
    GLOBAL_LEAK,
    POOL,
    RECOVERY_TRAIN,
    RECOVERY_VAL,
    load_jsonl,
    normalize,
    pilot_questions,
    plain_response,
    stable_rank,
)


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
V4_TRAIN = DATA / "sft_selective_blocks_v4_train.parquet"
V4_RECOVERY_AUDIT = DATA / "sft_v4_recovery8_audit.json"
TAGGED_TRAIN = DATA / "sft_deep69_tagged_train.parquet"
PLAIN_TRAIN = DATA / "sft_deep69_plain_train.parquet"
PLAN = DATA / "sft_deep69_pair_quality.json"

CONTROL_COUNT = 45
REPLAY_BY_KIND_AND_SOURCE = {
    "replay_th": {"math": 36, "gsm8k": 22, "arc": 13},
    "replay_nt": {"math": 36, "gsm8k": 22, "arc": 13},
}
CONTROL_SEED = "deep69-control-20261012"
REPLAY_SEEDS = {
    "replay_th": "deep69-replay-th-20261012",
    "replay_nt": "deep69-replay-nt-20261012",
}
ORDER_SEED = "deep69-order-20261012"

# These are the GSM8K members of v4's two accepted positive review lists.
# The two overlaps have both kinds of review; every other item has one.
V4_MANUAL_GSM = {
    "gsm8k-train/2761", "gsm8k-train/508", "gsm8k-train/2838",
    "gsm8k-train/4779", "gsm8k-train/6652", "gsm8k-train/3947",
    "gsm8k-train/5854", "gsm8k-train/619", "gsm8k-train/369",
    "gsm8k-train/5185",
}
V4_INDEPENDENT_GSM = {
    "gsm8k-train/1481", "gsm8k-train/1779", "gsm8k-train/2802",
    "gsm8k-train/3026", "gsm8k-train/4309", "gsm8k-train/5185",
    "gsm8k-train/5854", "gsm8k-train/6952", "gsm8k-train/697",
    "gsm8k-train/716",
}
GSM_POSITIVE_IDS = V4_MANUAL_GSM | V4_INDEPENDENT_GSM


def question_of(row, pool):
    return normalize(pool[row["id"]]["question"])


def recovery_rows():
    frame = pd.read_parquet(RECOVERY_TRAIN)
    assert len(frame) == len(set(frame.id)) == 256
    rows = frame.to_dict("records")
    controls = [row for row in rows if row["extra_info"]["kind"] == "control_th"]
    positives = [row for row in rows if row["extra_info"]["kind"] == "parallel_th"]
    assert len(controls) == 50 and len(positives) == 46
    return controls, positives


def select_controls(controls, positive_ids):
    eligible = [row for row in controls if row["id"] not in positive_ids]
    chosen = sorted(
        eligible, key=lambda row: (stable_rank(CONTROL_SEED, row["id"]), row["id"])
    )[:CONTROL_COUNT]
    assert len(chosen) == CONTROL_COUNT
    return chosen


def select_replay(v4_rows, excluded_ids, excluded_questions, pool):
    selected = []
    used_ids, used_questions = set(excluded_ids), set(excluded_questions)
    for kind, quotas in REPLAY_BY_KIND_AND_SOURCE.items():
        for source, count in quotas.items():
            eligible = [
                row for row in v4_rows
                if row["extra_info"]["kind"] == kind and row["source"] == source
                and row["id"] not in used_ids and question_of(row, pool) not in used_questions
            ]
            # v4 contains repeated source rows for some replay IDs.  This
            # pair intentionally has 256 distinct questions, so rank ID
            # groups and retain one deterministic source row per group.
            by_id = {}
            for row in eligible:
                old = by_id.get(row["id"])
                if old is None or row["extra_info"]["answer"] < old["extra_info"]["answer"]:
                    by_id[row["id"]] = row
            chosen = sorted(
                by_id.values(),
                key=lambda row: (stable_rank(REPLAY_SEEDS[kind], row["id"]), row["id"]),
            )[:count]
            assert len(chosen) == count, (kind, source, len(chosen), count)
            selected.extend(chosen)
            used_ids.update(row["id"] for row in chosen)
            used_questions.update(question_of(row, pool) for row in chosen)
    assert len(selected) == 142 and len({row["id"] for row in selected}) == 142
    assert len({question_of(row, pool) for row in selected}) == 142
    return selected


def review_provenance(problem_id):
    kinds = []
    if problem_id in V4_MANUAL_GSM:
        kinds.append("v4_manual_read")
    if problem_id in V4_INDEPENDENT_GSM:
        kinds.append("v4_independent_review")
    assert kinds
    return kinds


def add_deep_rows(deep, tagged, plain):
    for source in deep:
        assert parse(source["response"])["valid"]
        prompt = mv_prompt(HEADER + source["question"])
        tagged.append({
            "data_source": "exp21_deep69_tagged_deep51",
            "id": source["id"], "source": "math", "copy_index": 0,
            "extra_info": {"question": prompt, "answer": source["response"],
                           "enable_thinking": True, "kind": "parallel_th", "id": source["id"]},
        })
        plain.append({
            "data_source": "exp21_deep69_plain_deep51",
            "id": source["id"], "source": "math", "copy_index": 0,
            "extra_info": {"question": prompt, "answer": plain_response(source["response"]),
                           "enable_thinking": True, "kind": "control_th", "id": source["id"]},
        })


def add_gsm_rows(gsm_rows, tagged, plain):
    for source in gsm_rows:
        assert parse(source["extra_info"]["answer"])["valid"]
        for target, data_source, answer, kind in (
            (tagged, "exp21_deep69_tagged_gsm", source["extra_info"]["answer"], "parallel_th"),
            (plain, "exp21_deep69_plain_gsm", plain_response(source["extra_info"]["answer"]), "control_th"),
        ):
            item = deepcopy(source)
            item["source_origin"] = "recovery8"
            item["source_index"] = item["index"]
            item["data_source"] = data_source
            item["copy_index"] = 0
            item["extra_info"]["answer"] = answer
            item["extra_info"]["kind"] = kind
            target.append(item)


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

    controls, recovery_positive = recovery_rows()
    recovery_positive_by_id = {row["id"]: row for row in recovery_positive}
    assert set(recovery_positive_by_id) >= GSM_POSITIVE_IDS
    gsm = [recovery_positive_by_id[problem_id] for problem_id in sorted(GSM_POSITIVE_IDS)]
    assert len(gsm) == 18 and all(row["source"] == "gsm8k" for row in gsm)
    assert not (deep_ids & GSM_POSITIVE_IDS)
    positive_ids = deep_ids | GSM_POSITIVE_IDS
    assert len(positive_ids) == 69

    controls = select_controls(controls, positive_ids)
    candidate_questions = {normalize(pool[problem_id]["question"]) for problem_id in positive_ids}
    candidate_questions.update(question_of(row, pool) for row in controls)
    v4_rows = pd.read_parquet(V4_TRAIN).to_dict("records")
    replay = select_replay(v4_rows, positive_ids | {row["id"] for row in controls}, candidate_questions, pool)
    other = []
    for row in controls:
        item = deepcopy(row)
        item["source_origin"] = "recovery8"
        item["source_index"] = item["index"]
        other.append(item)
    for row in replay:
        item = deepcopy(row)
        item["source_origin"] = "v4"
        item["source_index"] = item["index"]
        other.append(item)
    assert not (set(row["id"] for row in controls) & set(row["id"] for row in replay))

    tagged, plain = [], []
    add_deep_rows(deep, tagged, plain)
    add_gsm_rows(gsm, tagged, plain)
    for row in other:
        item = deepcopy(row)
        item["copy_index"] = 0
        tagged.append(item)
        plain.append(deepcopy(item))
    assert len(tagged) == len(plain) == 69 + 45 + 142 == 256

    tagged.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    plain.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    for index, (left, right) in enumerate(zip(tagged, plain)):
        left["index"] = right["index"] = index
        assert left["id"] == right["id"] and left["copy_index"] == right["copy_index"]
        if left["id"] not in positive_ids:
            assert left == right

    val = pd.read_parquet(RECOVERY_VAL)
    train_questions = {question_of(row, pool) for row in tagged}
    val_questions = {normalize(pool[row_id]["question"]) for row_id in val.id}
    assert len(train_questions) == len(tagged)
    assert not train_questions & val_questions and not train_questions & pilot_questions()
    leak = json.loads(GLOBAL_LEAK.read_text())
    deep_leak = json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0
    recovery_audit = json.loads(V4_RECOVERY_AUDIT.read_text())
    assert recovery_audit["checks"]["train_eval_normalized_question_overlap"] == 0

    report = {
        "status": "prepared",
        "candidate": "deep69-paired-math-gsm-and-mixed-replay",
        "seeds": {"control": CONTROL_SEED, "replay": REPLAY_SEEDS, "order": ORDER_SEED},
        "train": {
            "rows": 256, "unique_ids": len({row["id"] for row in tagged}),
            "positive_rows": 69, "unique_positive_ids": 69,
            "deep51_math_ids": sorted(deep_ids), "recovery8_gsm_ids": sorted(GSM_POSITIVE_IDS),
            "gsm_review_provenance": {problem_id: review_provenance(problem_id) for problem_id in sorted(GSM_POSITIVE_IDS)},
            "control_th_ids": [row["id"] for row in controls],
            "replay_ids": {kind: [row["id"] for row in replay if row["extra_info"]["kind"] == kind]
                           for kind in REPLAY_BY_KIND_AND_SOURCE},
            "replay_counts": {kind: dict(collections.Counter(row["source"] for row in replay if row["extra_info"]["kind"] == kind))
                              for kind in REPLAY_BY_KIND_AND_SOURCE},
            "row_order": [row["id"] for row in tagged],
        },
        "transform": {
            "tagged": "all 69 source positive answers copied verbatim",
            "plain": "only Multiverse tags and Goal/Outline/Conclusion scaffolding removed; Path text retained in order",
            "positive_domain_and_replay_mode_changed_vs_deep51_1x": True,
        },
        "overlap": {"train_val_normalized_question": 0, "train_pilot40_normalized_question": 0},
        "leakcheck": {"global_pool": GLOBAL_LEAK.name, "deep51": DEEP_LEAK.name},
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
    print(json.dumps(report["train"]["replay_counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
