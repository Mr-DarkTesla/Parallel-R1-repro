"""Build selective-blocks v4 from v2 with audited merge-inside positives."""

import collections
import json
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
V2 = DATA / "sft_selective_blocks_v2"
V4 = DATA / "sft_selective_blocks_v4"
MERGE_INSIDE = DATA / "pair_expanded_m1_merge_inside.jsonl"
REPORT = DATA / "sft_selective_blocks_v4_audit.json"


def load_jsonl(path):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def replace(frame, merge_inside):
    replaced = 0
    rows = []
    for row in frame.to_dict("records"):
        copied = dict(row)
        copied["extra_info"] = dict(row["extra_info"])
        if kind(row) == "parallel_th":
            source = merge_inside[row["id"]]
            assert copied["extra_info"]["question"] == mv_prompt(HEADER + source["question"])
            copied["extra_info"]["answer"] = source["response"]
            replaced += 1
        rows.append(copied)
    return pd.DataFrame(rows), replaced


def main():
    merge_inside = load_jsonl(MERGE_INSIDE)
    before = {split: pd.read_parquet(f"{V2}_{split}.parquet") for split in ("train", "val")}
    after = {}
    report = {"base": V2.name, "positive_source": MERGE_INSIDE.name, "splits": {}}
    for split in ("train", "val"):
        after[split], replaced = replace(before[split], merge_inside)
        assert len(after[split]) == len(before[split])
        assert after[split].id.tolist() == before[split].id.tolist()
        assert after[split].source.tolist() == before[split].source.tolist()
        assert [kind(row) for row in after[split].to_dict("records")] == [kind(row) for row in before[split].to_dict("records")]
        after[split].to_parquet(f"{V4}_{split}.parquet")
        report["splits"][split] = {
            "rows": len(after[split]),
            "parallel_th_replaced": replaced,
            "non_parallel_rows_unchanged": len(after[split]) - replaced,
            "parallel_distinct_ids": len(set(after[split][after[split].extra_info.map(
                lambda info: info["kind"] == "parallel_th")].id)),
            "source_counts": dict(collections.Counter(after[split].source)),
            "kind_counts": dict(collections.Counter(info["kind"] for info in after[split].extra_info)),
        }
    assert len(after["train"]) == 2748 and len(after["val"]) == 63
    assert not set(after["train"].id) & set(after["val"].id)
    assert report["splits"]["train"]["parallel_th_replaced"] == 555
    assert report["splits"]["val"]["parallel_th_replaced"] == 24
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
