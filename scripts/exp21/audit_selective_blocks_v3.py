"""Audit v3 frontblock replacement against v2 and audited M1 source."""

import collections
import json
import re
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
V2 = DATA / "sft_selective_blocks_v2"
V3 = DATA / "sft_selective_blocks_v3"
FRONTBLOCK = DATA / "pair_expanded_m1_frontblock.jsonl"
POOL = DATA / "pool.jsonl"
FRONTBLOCK_TARGET_AUDIT = DATA / "m1_frontblock_target_audit.json"
OUTPUT = DATA / "sft_selective_blocks_v3_quality.json"
NUMBERS = re.compile(r"(?<!\w)\d+(?:\.\d+)?(?:/\d+)?")


def load_jsonl(path, expected=None):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    if expected is not None:
        assert len(rows) == expected
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def signature(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True)


def block(answer):
    start = answer.index("<Parallel>")
    end = answer.index("</Parallel>") + len("</Parallel>")
    return answer[start:end]


def final_suffix(answer):
    return answer[answer.index("</think>"):]


def audit_split(split, old, new, frontblock, pool):
    assert len(old) == len(new)
    assert old.id.tolist() == new.id.tolist()
    assert old.source.tolist() == new.source.tolist()
    assert [kind(row) for row in old.to_dict("records")] == [kind(row) for row in new.to_dict("records")]
    changed = unchanged = grammar_ok = 0
    transformed = unchanged_frontblock = 0
    ids = set()
    for previous, current in zip(old.to_dict("records"), new.to_dict("records")):
        assert previous["id"] == current["id"] and previous["source"] == current["source"]
        if kind(previous) != "parallel_th":
            assert signature(previous) == signature(current), (split, previous["id"])
            unchanged += 1
            continue
        source = frontblock[previous["id"]]
        old_answer = previous["extra_info"]["answer"]
        new_answer = current["extra_info"]["answer"]
        assert current["extra_info"]["question"] == previous["extra_info"]["question"]
        assert current["extra_info"]["question"] == mv_prompt(HEADER + source["question"])
        assert new_answer == source["response"]
        assert block(old_answer) == block(new_answer), previous["id"]
        assert final_suffix(old_answer) == final_suffix(new_answer), previous["id"]
        assert set(NUMBERS.findall(old_answer)) == set(NUMBERS.findall(new_answer)), previous["id"]
        assert (old_answer == new_answer) == (not source["frontblock_transformed"]), previous["id"]
        assert new_answer.startswith("<think>") and new_answer.count("</think>") == 1
        inside, outside = new_answer.split("</think>", 1)
        parsed = parse(inside)
        assert parsed["valid"] and len(parsed["blocks"]) == 1, previous["id"]
        assert parsed["blocks"][0]["numbered"] and len(parsed["blocks"][0]["paths"]) == 2, previous["id"]
        assert parse(outside)["tags"] == 0 and all(tag not in outside for tag in TAGS), previous["id"]
        changed += 1
        grammar_ok += 1
        transformed += source["frontblock_transformed"]
        unchanged_frontblock += not source["frontblock_transformed"]
        ids.add(previous["id"])
    rows = new.to_dict("records")
    positives = [row for row in rows if kind(row) == "parallel_th"]
    controls = [row for row in rows if kind(row) == "control_th"]
    return {
        "rows": len(new), "parallel_rows_transformed": changed,
        "non_parallel_rows_unchanged": unchanged,
        "parallel_distinct_ids": len(ids),
        "frontblock_moved_rows": transformed,
        "frontblock_retained_rows": unchanged_frontblock,
        "valid_two_path_blocks_inside_think": grammar_ok,
        "tags_outside_think": 0,
        "source_counts": dict(collections.Counter(row["source"] for row in rows)),
        "answer_type_counts": dict(collections.Counter(pool[row["id"]]["answer_type"] for row in rows)),
        "kind_counts": dict(collections.Counter(kind(row) for row in rows)),
        "parallel_rows_by_source": dict(collections.Counter(row["source"] for row in positives)),
        "control_rows_by_source": dict(collections.Counter(row["source"] for row in controls)),
    }


def main():
    frontblock = load_jsonl(FRONTBLOCK, expected=337)
    pool = load_jsonl(POOL)
    old = {split: pd.read_parquet(f"{V2}_{split}.parquet") for split in ("train", "val")}
    new = {split: pd.read_parquet(f"{V3}_{split}.parquet") for split in ("train", "val")}
    assert len(new["train"]) == 2748 and len(new["val"]) == 63
    assert not set(new["train"].id) & set(new["val"].id)
    report = {"base": V2.name, "candidate": V3.name,
              "frontblock_source": FRONTBLOCK.name,
              "splits": {split: audit_split(split, old[split], new[split], frontblock, pool)
                         for split in ("train", "val")}}
    train, val = report["splits"]["train"], report["splits"]["val"]
    assert train["parallel_rows_transformed"] == 555 and val["parallel_rows_transformed"] == 24
    assert train["kind_counts"] == {"replay_nt": 879, "replay_th": 804, "parallel_th": 555, "control_th": 510}
    assert val["kind_counts"] == {"parallel_th": 24, "replay_nt": 21, "replay_th": 18}
    assert train["control_rows_by_source"] == {"math": 252, "gsm8k": 180, "arc": 78}
    assert train["parallel_rows_by_source"] == {"math": 372, "gsm8k": 183}
    token_audit = json.loads(FRONTBLOCK_TARGET_AUDIT.read_text())["files"]
    source_train = next(value for key, value in token_audit.items() if key.endswith("_train.parquet"))
    source_val = next(value for key, value in token_audit.items() if key.endswith("_val.parquet"))
    assert source_train["max_tokens"] == 3838 and source_train["over_4096"] == 0
    assert source_val["max_tokens"] == 3513 and source_val["over_4096"] == 0
    report["token_limit"] = {
        "evidence": FRONTBLOCK_TARGET_AUDIT.name,
        "same_frontblock_answers_and_prompts_as_audited_source": True,
        "train_max_tokens": source_train["max_tokens"], "val_max_tokens": source_val["max_tokens"],
        "over_4096": 0,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
