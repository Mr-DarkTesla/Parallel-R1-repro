"""Audit diverse selective-blocks v5 against v1 targets and v2 fixed rows."""

import collections
import json
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
V1 = DATA / "sft_selective_blocks_m1_text1"
V2 = DATA / "sft_selective_blocks_v2"
V5 = DATA / "sft_selective_blocks_v5"
TWO_PATHS = DATA / "pair_expanded_m1_two_paths.jsonl"
POOL = DATA / "pool.jsonl"
TARGET_AUDIT = DATA / "m1_twopath_target_audit.json"
PLAN = DATA / "sft_selective_blocks_v5_audit.json"
OUTPUT = DATA / "sft_selective_blocks_v5_quality.json"


def load_jsonl(path, expected=None):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    if expected is not None:
        assert len(rows) == expected
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def signature(row):
    return json.dumps({key: value for key, value in row.items() if key != "index"}, ensure_ascii=False, sort_keys=True)


def main():
    plan = json.loads(PLAN.read_text())
    source = load_jsonl(TWO_PATHS, expected=337)
    pool = load_jsonl(POOL)
    v1_train = pd.read_parquet(f"{V1}_train.parquet")
    v2_train = pd.read_parquet(f"{V2}_train.parquet")
    v2_val = pd.read_parquet(f"{V2}_val.parquet")
    train = pd.read_parquet(f"{V5}_train.parquet")
    val = pd.read_parquet(f"{V5}_val.parquet")
    assert len(train) == 2748 and len(val) == 63 and val.equals(v2_val)
    assert not set(train.id) & set(val.id)
    fixed_v2 = collections.Counter(signature(row) for row in v2_train.to_dict("records") if kind(row) != "parallel_th")
    fixed_v5 = collections.Counter(signature(row) for row in train.to_dict("records") if kind(row) != "parallel_th")
    assert fixed_v5 == fixed_v2
    v1_positive = v1_train[v1_train.extra_info.map(lambda info: info["kind"] == "parallel_th")]
    expected_ids = set(v1_positive.id)
    positives = train[train.extra_info.map(lambda info: info["kind"] == "parallel_th")]
    assert len(expected_ids) == 305 and set(positives.id) == expected_ids
    copies = collections.Counter(positives.id)
    math_ids = {id_ for id_ in expected_ids if id_.startswith("math-")}
    gsm_ids = {id_ for id_ in expected_ids if id_.startswith("gsm8k-")}
    assert len(math_ids) == 184 and len(gsm_ids) == 121
    assert collections.Counter(copies[id_] for id_ in math_ids) == {2: 180, 3: 4}
    assert collections.Counter(copies[id_] for id_ in gsm_ids) == {1: 59, 2: 62}
    assert {id_ for id_ in math_ids if copies[id_] == 3} == set(plan["third_math_ids"])
    assert {id_ for id_ in gsm_ids if copies[id_] == 2} == set(plan["second_gsm_ids"])
    grammar_ok = answer_fields_match_pool = tagged_rows = post_parallel_merge_rows = 0
    for row in train.to_dict("records") + val.to_dict("records"):
        answer = row["extra_info"]["answer"]
        if any(tag in answer for tag in TAGS):
            assert answer.startswith("<think>") and answer.count("</think>") == 1, row["id"]
            assert not any(tag in answer.split("</think>", 1)[1] for tag in TAGS), row["id"]
            tagged_rows += 1
        if kind(row) != "parallel_th":
            continue
        record = source[row["id"]]
        assert row["extra_info"]["question"] == mv_prompt(HEADER + record["question"])
        assert row["extra_info"]["answer"] == record["response"]
        assert record["answer"] == pool[row["id"]]["answer"]
        inside, outside = answer.split("</think>", 1)
        parsed = parse(inside)
        assert parsed["valid"] and len(parsed["blocks"]) == 1
        assert parsed["blocks"][0]["numbered"] and len(parsed["blocks"][0]["paths"]) == 2
        assert parse(outside)["tags"] == 0
        post = answer[answer.index("</Parallel>") + len("</Parallel>"):answer.index("</think>")].strip()
        assert post
        grammar_ok += 1
        answer_fields_match_pool += 1
        post_parallel_merge_rows += 1
    assert len(positives) == 555 and grammar_ok == 579
    assert collections.Counter(kind(row) for row in train.to_dict("records")) == {
        "replay_nt": 879, "replay_th": 804, "control_th": 510, "parallel_th": 555,
    }
    assert collections.Counter(positives.source) == {"math": 372, "gsm8k": 183}
    token_audit = json.loads(TARGET_AUDIT.read_text())["files"]
    source_train = next(value for key, value in token_audit.items() if key.endswith("_train.parquet"))
    source_val = next(value for key, value in token_audit.items() if key.endswith("_val.parquet"))
    assert source_train["max_tokens"] == 3838 and source_train["over_4096"] == 0
    assert source_val["max_tokens"] == 3513 and source_val["over_4096"] == 0
    report = {
        "train_rows": len(train), "val_rows": len(val), "val_identical_to_v2": True,
        "train_val_problem_ids_disjoint": True,
        "v2_non_positive_rows_identical": True,
        "positive_distinct_ids": len(expected_ids),
        "positive_copies_by_source": {"math": 372, "gsm8k": 183},
        "math_copy_distribution": {"two": 180, "three": 4},
        "gsm8k_copy_distribution": {"one": 59, "two": 62},
        "all_positive_answers_match_original_two_path_source": grammar_ok,
        "answer_fields_match_pool": answer_fields_match_pool,
        "post_parallel_merge_rows": post_parallel_merge_rows,
        "valid_two_path_blocks_inside_think": grammar_ok,
        "all_tagged_rows_inside_think": tagged_rows, "tags_outside_think": 0,
        "train_kind_counts": dict(collections.Counter(kind(row) for row in train.to_dict("records"))),
        "token_limit": {"evidence": TARGET_AUDIT.name,
                        "same_positive_prompts_and_answers_as_audited_source": True,
                        "train_max_tokens": source_train["max_tokens"],
                        "val_max_tokens": source_val["max_tokens"], "over_4096": 0},
        "leakcheck": "All v5 positive questions are v1 target questions from the prior leakchecked cleaned pool; see DATASET_POOL.md.",
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
