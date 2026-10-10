"""Audit selective-blocks v4 against v2 and audited merge-inside M1 answers."""

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
V4 = DATA / "sft_selective_blocks_v4"
MERGE_INSIDE = DATA / "pair_expanded_m1_merge_inside.jsonl"
TWO_PATHS = DATA / "pair_expanded_m1_two_paths.jsonl"
POOL = DATA / "pool.jsonl"
MERGE_TARGET_AUDIT = DATA / "m1_merge_inside_target_audit.json"
OUTPUT = DATA / "sft_selective_blocks_v4_quality.json"
NUMBERS = re.compile(r"(?<!\w)\d+(?:\.\d+)?(?:/\d+)?")


def load_jsonl(path, expected=None):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    if expected is not None:
        assert len(rows) == expected
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def move_merge(response):
    conclusion_end = response.index("</Conclusion>")
    parallel_end = response.index("</Parallel>") + len("</Parallel>")
    think_end = response.index("</think>")
    post = response[parallel_end:think_end].strip()
    assert post
    return (response[:conclusion_end].rstrip() + "\n" + post + "\n"
            + response[conclusion_end:parallel_end] + "\n" + response[think_end:])


def signature(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True)


def audit_split(split, old, new, merge_inside, two_paths, pool):
    assert len(old) == len(new)
    assert old.id.tolist() == new.id.tolist()
    assert old.source.tolist() == new.source.tolist()
    replaced = unchanged = grammar_ok = answer_fields_match_pool = tagged_rows = 0
    paths_preserved = finals_preserved = number_multisets_preserved = 0
    ids, moved_chars = set(), 0
    for previous, current in zip(old.to_dict("records"), new.to_dict("records")):
        assert previous["id"] == current["id"] and previous["source"] == current["source"]
        answer = current["extra_info"]["answer"]
        if any(tag in answer for tag in TAGS):
            assert answer.startswith("<think>") and answer.count("</think>") == 1, (split, current["id"])
            assert not any(tag in answer.split("</think>", 1)[1] for tag in TAGS), (split, current["id"])
            tagged_rows += 1
        if kind(previous) != "parallel_th":
            assert signature(previous) == signature(current), (split, previous["id"])
            unchanged += 1
            continue
        assert kind(current) == "parallel_th"
        source = merge_inside[previous["id"]]
        original = two_paths[previous["id"]]
        old_info, new_info = previous["extra_info"], current["extra_info"]
        assert {key: value for key, value in old_info.items() if key != "answer"} == {
            key: value for key, value in new_info.items() if key != "answer"}
        assert new_info["question"] == mv_prompt(HEADER + source["question"])
        assert new_info["answer"] == source["response"] == move_merge(original["response"])
        assert source["question"] == original["question"]
        assert source["answer"] == original["answer"]
        assert source["moved_into_conclusion_chars"] > 0
        assert set(NUMBERS.findall(source["response"])) == set(NUMBERS.findall(original["response"]))
        assert collections.Counter(NUMBERS.findall(source["response"])) == collections.Counter(NUMBERS.findall(original["response"]))
        old_parsed, merged_parsed = parse(original["response"]), parse(source["response"])
        assert old_parsed["valid"] and merged_parsed["valid"]
        assert len(old_parsed["blocks"]) == len(merged_parsed["blocks"]) == 1
        assert old_parsed["blocks"][0]["paths"] == merged_parsed["blocks"][0]["paths"]
        assert original["response"][original["response"].index("</think>"):] == source["response"][source["response"].index("</think>"):]
        inside, outside = new_info["answer"].split("</think>", 1)
        parsed = parse(inside)
        assert parsed["valid"] and len(parsed["blocks"]) == 1
        assert parsed["blocks"][0]["numbered"] and len(parsed["blocks"][0]["paths"]) == 2
        assert parse(outside)["tags"] == 0 and all(tag not in outside for tag in TAGS)
        assert source["answer"] == pool[previous["id"]]["answer"], previous["id"]
        replaced += 1
        grammar_ok += 1
        answer_fields_match_pool += 1
        paths_preserved += 1
        finals_preserved += 1
        number_multisets_preserved += 1
        moved_chars += source["moved_into_conclusion_chars"]
        ids.add(previous["id"])
    rows = new.to_dict("records")
    positives = [row for row in rows if kind(row) == "parallel_th"]
    controls = [row for row in rows if kind(row) == "control_th"]
    return {
        "rows": len(new), "parallel_th_replaced": replaced,
        "non_parallel_rows_unchanged": unchanged,
        "parallel_distinct_ids": len(ids), "moved_into_conclusion_chars": moved_chars,
        "original_paths_preserved": paths_preserved,
        "final_answer_suffix_preserved": finals_preserved,
        "number_multiset_preserved": number_multisets_preserved,
        "answer_fields_match_pool": answer_fields_match_pool,
        "valid_two_path_blocks_inside_think": grammar_ok,
        "all_tagged_rows_inside_think": tagged_rows, "tags_outside_think": 0,
        "source_counts": dict(collections.Counter(row["source"] for row in rows)),
        "kind_counts": dict(collections.Counter(kind(row) for row in rows)),
        "parallel_rows_by_source": dict(collections.Counter(row["source"] for row in positives)),
        "control_rows_by_source": dict(collections.Counter(row["source"] for row in controls)),
    }


def main():
    merge_inside = load_jsonl(MERGE_INSIDE, expected=337)
    two_paths = load_jsonl(TWO_PATHS, expected=337)
    pool = load_jsonl(POOL)
    old = {split: pd.read_parquet(f"{V2}_{split}.parquet") for split in ("train", "val")}
    new = {split: pd.read_parquet(f"{V4}_{split}.parquet") for split in ("train", "val")}
    assert len(new["train"]) == 2748 and len(new["val"]) == 63
    assert not set(new["train"].id) & set(new["val"].id)
    report = {"base": V2.name, "candidate": V4.name, "positive_source": MERGE_INSIDE.name,
              "source_before_merge": TWO_PATHS.name,
              "splits": {split: audit_split(split, old[split], new[split], merge_inside, two_paths, pool)
                         for split in ("train", "val")}}
    train, val = report["splits"]["train"], report["splits"]["val"]
    assert train["parallel_th_replaced"] == 555 and val["parallel_th_replaced"] == 24
    assert train["kind_counts"] == {"replay_nt": 879, "replay_th": 804, "parallel_th": 555, "control_th": 510}
    assert val["kind_counts"] == {"parallel_th": 24, "replay_nt": 21, "replay_th": 18}
    assert train["control_rows_by_source"] == {"math": 252, "gsm8k": 180, "arc": 78}
    assert train["parallel_rows_by_source"] == {"math": 372, "gsm8k": 183}
    token_audit = json.loads(MERGE_TARGET_AUDIT.read_text())["files"]
    source_train = next(value for key, value in token_audit.items() if key.endswith("_train.parquet"))
    source_val = next(value for key, value in token_audit.items() if key.endswith("_val.parquet"))
    assert source_train["max_tokens"] == 3838 and source_train["over_4096"] == 0
    assert source_val["max_tokens"] == 3513 and source_val["over_4096"] == 0
    report["token_limit"] = {
        "evidence": MERGE_TARGET_AUDIT.name,
        "same_positive_prompts_and_answers_as_audited_source": True,
        "train_max_tokens": source_train["max_tokens"], "val_max_tokens": source_val["max_tokens"],
        "over_4096": 0,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
