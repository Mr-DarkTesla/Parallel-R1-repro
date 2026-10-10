"""Build selective-blocks v3 by front-loading only v2 parallel answers."""

import collections
import json
import re
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
V2 = DATA / "sft_selective_blocks_v2"
V3 = DATA / "sft_selective_blocks_v3"
FRONTBLOCK = DATA / "pair_expanded_m1_frontblock.jsonl"
REPORT = DATA / "sft_selective_blocks_v3_audit.json"
NUMBERS = re.compile(r"(?<!\w)\d+(?:\.\d+)?(?:/\d+)?")


def load_jsonl(path):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def block(answer):
    start = answer.index("<Parallel>")
    end = answer.index("</Parallel>") + len("</Parallel>")
    return answer[start:end]


def final_suffix(answer):
    return answer[answer.index("</think>"):]


def replace(frame, frontblock):
    transformed = 0
    unchanged = 0
    transformed_ids = set()
    rows = []
    for row in frame.to_dict("records"):
        copied = dict(row)
        copied["extra_info"] = dict(row["extra_info"])
        if kind(row) != "parallel_th":
            unchanged += 1
            rows.append(copied)
            continue

        source = frontblock[row["id"]]
        old = row["extra_info"]["answer"]
        new = source["response"]
        assert row["extra_info"]["question"] == mv_prompt(HEADER + source["question"]), row["id"]
        assert old.startswith("<think>") and new.startswith("<think>"), row["id"]
        assert old.count("</think>") == new.count("</think>") == 1, row["id"]
        assert block(old) == block(new), row["id"]
        assert final_suffix(old) == final_suffix(new), row["id"]
        assert set(NUMBERS.findall(old)) == set(NUMBERS.findall(new)), row["id"]
        assert new == source["response"], row["id"]
        copied["extra_info"]["answer"] = new
        transformed += 1
        transformed_ids.add(row["id"])
        rows.append(copied)
    return pd.DataFrame(rows), transformed, unchanged, transformed_ids


def main():
    frontblock = load_jsonl(FRONTBLOCK)
    before = {}
    after = {}
    report = {"base": V2.name, "frontblock_source": FRONTBLOCK.name, "splits": {}}
    for split in ("train", "val"):
        before[split] = pd.read_parquet(f"{V2}_{split}.parquet")
        after[split], changed, unchanged, ids = replace(before[split], frontblock)
        assert len(after[split]) == len(before[split])
        assert after[split].id.tolist() == before[split].id.tolist()
        assert after[split].source.tolist() == before[split].source.tolist()
        after[split].to_parquet(f"{V3}_{split}.parquet")
        report["splits"][split] = {
            "rows": len(after[split]),
            "parallel_rows_replaced": changed,
            "non_parallel_rows_unchanged": unchanged,
            "parallel_distinct_ids": len(ids),
            "frontblock_transformed_rows": sum(frontblock[id_]["frontblock_transformed"]
                                               for id_ in after[split][after[split].extra_info.map(
                                                   lambda info: info["kind"] == "parallel_th")].id),
            "frontblock_unchanged_rows": sum(not frontblock[id_]["frontblock_transformed"]
                                              for id_ in after[split][after[split].extra_info.map(
                                                  lambda info: info["kind"] == "parallel_th")].id),
            "source_counts": dict(collections.Counter(after[split].source)),
            "kind_counts": dict(collections.Counter(info["kind"] for info in after[split].extra_info)),
        }
    assert len(after["train"]) == 2748 and len(after["val"]) == 63
    assert not set(after["train"].id) & set(after["val"].id)
    assert report["splits"]["train"]["parallel_rows_replaced"] == 555
    assert report["splits"]["val"]["parallel_rows_replaced"] == 24
    assert report["splits"]["train"]["kind_counts"]["control_th"] == 510
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
