"""Build diverse selective-blocks v5 from v2 non-positive rows and v1 M1 targets."""

import collections
import json
import random
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
V1 = DATA / "sft_selective_blocks_m1_text1"
V2 = DATA / "sft_selective_blocks_v2"
V5 = DATA / "sft_selective_blocks_v5"
TWO_PATHS = DATA / "pair_expanded_m1_two_paths.jsonl"
REPORT = DATA / "sft_selective_blocks_v5_audit.json"


def load_jsonl(path):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows})
    return {row["id"]: row for row in rows}


def kind(row):
    return row["extra_info"]["kind"]


def signature(row):
    return json.dumps({key: value for key, value in row.items() if key != "index"}, ensure_ascii=False, sort_keys=True)


def main():
    v1 = pd.read_parquet(f"{V1}_train.parquet")
    v2 = pd.read_parquet(f"{V2}_train.parquet")
    val = pd.read_parquet(f"{V2}_val.parquet")
    source = load_jsonl(TWO_PATHS)
    non_positive = [{key: value for key, value in row.items() if key != "index"}
                    for row in v2.to_dict("records") if kind(row) != "parallel_th"]
    positives = v1[v1.extra_info.map(lambda info: info["kind"] == "parallel_th")]
    templates = {}
    for id_, group in positives.groupby("id", sort=False):
        rows = [{key: value for key, value in row.items() if key != "index"} for row in group.to_dict("records")]
        assert len(rows) == 3 and len({signature(row) for row in rows}) == 1, id_
        row = rows[0]
        assert row["extra_info"]["question"] == mv_prompt(HEADER + source[id_]["question"])
        assert row["extra_info"]["answer"] == source[id_]["response"]
        templates[id_] = row
    math_ids = sorted(id_ for id_ in templates if id_.startswith("math-"))
    gsm_ids = sorted(id_ for id_ in templates if id_.startswith("gsm8k-"))
    assert len(math_ids) == 184 and len(gsm_ids) == 121
    third_math = sorted(random.Random(21071).sample(math_ids, 4))
    second_gsm = sorted(random.Random(21072).sample(gsm_ids, 62))
    rows = list(non_positive)
    for id_ in math_ids:
        rows.extend([templates[id_]] * (3 if id_ in third_math else 2))
    for id_ in gsm_ids:
        rows.extend([templates[id_]] * (2 if id_ in second_gsm else 1))
    assert len(rows) == 2748
    assert collections.Counter(kind(row) for row in rows) == {
        "replay_nt": 879, "replay_th": 804, "control_th": 510, "parallel_th": 555,
    }
    rng = random.Random(21073)
    rng.shuffle(rows)
    train = pd.DataFrame(rows)
    train["index"] = range(len(train))
    assert not set(train.id) & set(val.id)
    train.to_parquet(f"{V5}_train.parquet")
    val.to_parquet(f"{V5}_val.parquet")
    report = {
        "base_non_positive_rows": V2.name,
        "positive_templates": V1.name,
        "positive_source": TWO_PATHS.name,
        "val_base": V2.name,
        "train_rows": len(train), "val_rows": len(val), "val_rows_unchanged": True,
        "seeds": {"third_math": 21071, "second_gsm": 21072, "shuffle": 21073},
        "third_math_ids": third_math, "second_gsm_ids": second_gsm,
        "train_kind_counts": dict(collections.Counter(kind(row) for row in train.to_dict("records"))),
        "train_parallel_rows_by_source": dict(collections.Counter(
            row["source"] for row in train.to_dict("records") if kind(row) == "parallel_th")),
        "train_parallel_distinct_ids_by_source": {"math": len(math_ids), "gsm8k": len(gsm_ids)},
        "leakcheck": "All positive questions come from v1's prior leakchecked cleaned pool; see DATASET_POOL.md.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
