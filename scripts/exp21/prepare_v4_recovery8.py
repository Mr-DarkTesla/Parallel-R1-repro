"""Build the small, deterministic v4-step56 recovery8 SFT dataset.

The train split contains one existing v4 row per problem: 46 manually reviewed
parallel_th rows, all 50 reviewed control_th rows, and 160 replay_th rows.  No
answer or prompt is regenerated.  The v4 validation split is copied verbatim.
"""

import collections
import hashlib
import json
import os
import re
import tarfile
import unicodedata
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
SOURCE_TRAIN = DATA / "sft_selective_blocks_v4_train.parquet"
SOURCE_VAL = DATA / "sft_selective_blocks_v4_val.parquet"
TRAIN_OUT = DATA / "sft_v4_recovery8_train.parquet"
VAL_OUT = DATA / "sft_v4_recovery8_val.parquet"
AUDIT_OUT = DATA / "sft_v4_recovery8_audit.json"
POOL = DATA / "pool.jsonl"
LEAK_AUDIT = RUN / "audit/leak_clean_recheck.json"
PILOT_ARCHIVE = RUN / "eval_archives/selective_v4_step56_masked_pilot.tgz"

REPLAY_SEED = "v4-recovery8-replay-20261012"
ORDER_SEED = "v4-recovery8-order-20261012"
REPLAY_QUOTAS = {"math": 80, "gsm8k": 50, "arc": 30}

# DATASET_SELECTIVE_BLOCKS_V4.md, section "Ручное чтение".
REVIEWED_20 = [
    "gsm8k-train/2761", "gsm8k-train/508", "gsm8k-train/2838",
    "gsm8k-train/4779", "gsm8k-train/6652", "gsm8k-train/3947",
    "gsm8k-train/5854", "gsm8k-train/619", "gsm8k-train/369",
    "gsm8k-train/5185", "math-train/1667", "math-train/4311",
    "math-train/6987", "math-train/2909", "math-train/6008",
    "math-train/4831", "math-train/5565", "math-train/6286",
    "math-train/1164", "math-train/3081",
]

# DATASET_SELECTIVE_BLOCKS_V4.md, section "Независимое ревью".
REVIEWED_30 = [
    "gsm8k-train/1481", "gsm8k-train/1779", "gsm8k-train/2802",
    "gsm8k-train/3026", "gsm8k-train/4309", "gsm8k-train/5185",
    "gsm8k-train/5854", "gsm8k-train/6952", "gsm8k-train/697",
    "gsm8k-train/716", "math-train/1171", "math-train/141",
    "math-train/1552", "math-train/1767", "math-train/1978",
    "math-train/1997", "math-train/2028", "math-train/2341",
    "math-train/2493", "math-train/2709", "math-train/271",
    "math-train/3762", "math-train/4209", "math-train/452",
    "math-train/4669", "math-train/4831", "math-train/4854",
    "math-train/5803", "math-train/6615", "math-train/965",
]
EXCLUDED_REVIEW_ID = "math-train/4669"


def load_jsonl(path):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows}), path
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def signature(row):
    return json.dumps({key: value for key, value in row.items() if key != "index"},
                      ensure_ascii=False, sort_keys=True)


def stable_rank(seed, problem_id):
    return hashlib.sha256(f"{seed}\0{problem_id}".encode()).hexdigest()


def normalize_question(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def pilot_rows():
    rows = []
    with tarfile.open(PILOT_ARCHIVE) as archive:
        names = sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl"))
        assert len(names) == 4, names
        for name in names:
            handle = archive.extractfile(name)
            assert handle is not None
            rows.extend(json.loads(line) for line in handle)
    assert len(rows) == 40
    assert len({(row["problem_id"], row["problem"]) for row in rows}) == 40
    return rows


def raw_problem(prompt):
    marker = "\n\nProblem: "
    assert marker in prompt
    return prompt.rsplit(marker, 1)[1]


def canonical_rows(frame, wanted_kind):
    result = {}
    subset = frame[frame.extra_info.map(lambda info: info["kind"] == wanted_kind)]
    for problem_id, group in subset.groupby("id", sort=True):
        records = group.sort_values("index").to_dict("records")
        assert len({signature(row) for row in records}) == 1, (wanted_kind, problem_id)
        result[problem_id] = records[0]
    return result


def reviewed_positive_ids():
    assert len(REVIEWED_20) == len(set(REVIEWED_20)) == 20
    assert len(REVIEWED_30) == len(set(REVIEWED_30)) == 30
    assert EXCLUDED_REVIEW_ID in REVIEWED_30 and EXCLUDED_REVIEW_ID not in REVIEWED_20
    reviewed = list(dict.fromkeys(REVIEWED_20 + REVIEWED_30))
    assert len(reviewed) == 47
    selected = [problem_id for problem_id in reviewed if problem_id != EXCLUDED_REVIEW_ID]
    assert len(selected) == len(set(selected)) == 46
    return selected


def select_ids(source_train):
    positive_ids = reviewed_positive_ids()
    positive = canonical_rows(source_train, "parallel_th")
    controls = canonical_rows(source_train, "control_th")
    replay = canonical_rows(source_train, "replay_th")
    assert set(positive_ids) <= set(positive)
    control_ids = sorted(controls)
    assert len(control_ids) == 50

    blocked = set(positive_ids) | set(control_ids)
    replay_ids = {}
    for source, quota in REPLAY_QUOTAS.items():
        available = [problem_id for problem_id, row in replay.items()
                     if row["source"] == source and problem_id not in blocked]
        ordered = sorted(available, key=lambda problem_id: (stable_rank(REPLAY_SEED, problem_id), problem_id))
        assert len(ordered) >= quota, (source, len(ordered), quota)
        replay_ids[source] = ordered[:quota]
    selected_replay = set().union(*map(set, replay_ids.values()))
    assert len(selected_replay) == sum(REPLAY_QUOTAS.values()) == 160
    assert not set(positive_ids) & set(control_ids)
    assert not blocked & selected_replay
    assert len(set(positive_ids) | set(control_ids) | selected_replay) == 256
    return positive_ids, control_ids, replay_ids, positive, controls, replay


def check_source_row(row, pool_row):
    info = row["extra_info"]
    assert row["id"] == info["id"] == pool_row["id"]
    assert row["source"] == pool_row["source"]
    assert info["enable_thinking"] is True
    expected_prompt = HEADER + pool_row["question"]
    if info["kind"] in {"parallel_th", "control_th"}:
        expected_prompt = mv_prompt(expected_prompt)
    assert info["question"] == expected_prompt, row["id"]
    assert info["answer"].startswith("<think>")
    assert info["answer"].count("<think>") == info["answer"].count("</think>") == 1
    inside, outside = info["answer"].split("</think>", 1)
    if info["kind"] == "parallel_th":
        parsed = parse(inside)
        assert parsed["valid"] and len(parsed["blocks"]) == 1
        assert parsed["blocks"][0]["numbered"] and len(parsed["blocks"][0]["paths"]) == 2
        assert all(tag not in outside for tag in TAGS)
    else:
        assert all(tag not in info["answer"] for tag in TAGS)


def main():
    source_train = pd.read_parquet(SOURCE_TRAIN)
    source_val = pd.read_parquet(SOURCE_VAL)
    pool = load_jsonl(POOL)
    positive_ids, control_ids, replay_ids, positive, controls, replay = select_ids(source_train)

    rows = ([positive[problem_id] for problem_id in positive_ids]
            + [controls[problem_id] for problem_id in control_ids]
            + [replay[problem_id] for source in REPLAY_QUOTAS for problem_id in replay_ids[source]])
    assert len(rows) == len({row["id"] for row in rows}) == 256
    for row in rows:
        check_source_row(row, pool[row["id"]])

    train_ids = {row["id"] for row in rows}
    val_ids = set(source_val.id)
    assert not train_ids & val_ids

    leak = json.loads(LEAK_AUDIT.read_text())
    assert leak["rows"] == len(pool) == 16547
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0

    pilot = pilot_rows()
    pilot_questions = {normalize_question(raw_problem(row["problem"])) for row in pilot}
    train_questions = {normalize_question(pool[problem_id]["question"]) for problem_id in train_ids}
    val_questions = {normalize_question(pool[problem_id]["question"]) for problem_id in val_ids}
    assert len(pilot_questions) == 40
    assert len(train_questions) == len(train_ids) == 256
    assert len(val_questions) == len(val_ids)
    assert not train_questions & pilot_questions
    assert not val_questions & pilot_questions
    assert not train_questions & val_questions
    raw_eval_ids = {row["problem_id"] for row in pilot}
    raw_id_collisions = sorted(train_ids & raw_eval_ids)
    assert raw_id_collisions == ["gsm8k-train/369"]
    collision_rows = []
    for problem_id in raw_id_collisions:
        matches = [row for row in pilot if row["problem_id"] == problem_id]
        assert len(matches) == 1
        eval_question = raw_problem(matches[0]["problem"])
        train_question = pool[problem_id]["question"]
        assert normalize_question(eval_question) != normalize_question(train_question)
        collision_rows.append({"id": problem_id, "train_question": train_question,
                               "eval_question": eval_question, "questions_equal": False})

    rows.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    train = pd.DataFrame(rows)
    train["index"] = range(len(train))
    assert collections.Counter(kind(row) for row in train.to_dict("records")) == {
        "replay_th": 160, "control_th": 50, "parallel_th": 46}

    report = {
        "status": "prepared",
        "candidate": "sft_v4_recovery8",
        "source_train": SOURCE_TRAIN.name,
        "source_val": SOURCE_VAL.name,
        "review_evidence": "DATASET_SELECTIVE_BLOCKS_V4.md: Ручное чтение and Независимое ревью",
        "excluded_review_id": EXCLUDED_REVIEW_ID,
        "seeds": {"replay": REPLAY_SEED, "row_order": ORDER_SEED},
        "train": {
            "rows": len(train), "unique_ids": len(train_ids),
            "kind_counts": dict(collections.Counter(kind(row) for row in train.to_dict("records"))),
            "source_counts": dict(collections.Counter(train.source)),
            "parallel_th_ids": positive_ids,
            "control_th_ids": control_ids,
            "replay_th_ids": replay_ids,
            "row_order_ids": train.id.tolist(),
        },
        "val": {"rows": len(source_val), "unique_ids": len(val_ids), "copied_verbatim": True,
                "ids": sorted(val_ids)},
        "overlap": {
            "train_val_id_count": 0,
            "train_eval_normalized_question_count": 0,
            "val_eval_normalized_question_count": 0,
            "train_val_normalized_question_count": 0,
            "eval_questions": len(pilot_questions),
            "raw_id_collisions_with_different_questions": collision_rows,
        },
        "leakcheck": {"evidence": str(LEAK_AUDIT.relative_to(ROOT)), **leak},
    }

    temporary = [TRAIN_OUT.with_suffix(".tmp.parquet"), VAL_OUT.with_suffix(".tmp.parquet"),
                 AUDIT_OUT.with_suffix(".tmp.json")]
    try:
        train.to_parquet(temporary[0], index=False)
        source_val.to_parquet(temporary[1], index=False)
        temporary[2].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        for source, target in zip(temporary, (TRAIN_OUT, VAL_OUT, AUDIT_OUT)):
            os.replace(source, target)
    finally:
        for path in temporary:
            path.unlink(missing_ok=True)
    print(json.dumps({"train_rows": len(train), "val_rows": len(source_val),
                      "unique_train_ids": len(train_ids), "status": "prepared"}))


if __name__ == "__main__":
    main()
