"""Equal-volume M1/M2 inside-thinking SFT and matched tag-free controls."""
import collections
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

from mv_format import strip_tags


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
BUILDER = Path(__file__).with_name("build_sft.py")


def read(path):
    return [json.loads(line) for line in path.open()]


def main():
    val_prefix = DATA / "sft_expanded_val_ids"
    val_ids = set(pd.read_parquet(f"{val_prefix}_val.parquet")["id"])
    arms = {}
    for method in ("m1", "m2"):
        primary = DATA / f"pair_expanded_{method}_thinking.jsonl"
        examples = read(primary)
        assert len(examples) == len({r["id"] for r in examples}) == 367
        new_ids = {r["id"] for r in read(DATA / f"more_{method}_matched180.jsonl")}
        assert len(new_ids) == 180 and not new_ids & val_ids
        arms[method] = collections.Counter((r["source"], r["answer_type"]) for r in examples)
        for arm, kind in (("tagged", "parallel_th"), ("control", "control_th")):
            prefix = DATA / f"sft_expanded_th_{method}_{arm}"
            specs = ([f"{kind}:{primary}"] * 3
                     + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * 2
                     + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 2)
            subprocess.run([sys.executable, str(BUILDER), str(prefix), "--rows", *specs,
                            "--val-ids-from", str(val_prefix), "--seed", "21"], check=True)
            for split, length in (("train", 2251), ("val", 50)):
                frame = pd.read_parquet(f"{prefix}_{split}.parquet")
                assert len(frame) == length
                assert set(frame["id"]).intersection(val_ids) == (val_ids if split == "val" else set())
    assert arms["m1"] == arms["m2"]
    for method in ("m1", "m2"):
        for split in ("train", "val"):
            tagged = pd.read_parquet(DATA / f"sft_expanded_th_{method}_tagged_{split}.parquet")
            control = pd.read_parquet(DATA / f"sft_expanded_th_{method}_control_{split}.parquet")
            assert tagged["id"].tolist() == control["id"].tolist()
            for a, b in zip(tagged["extra_info"], control["extra_info"]):
                assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
                assert strip_tags(a["answer"]).strip() == b["answer"]
    audit = {"primary_distinct_each_method": 367, "primary_copies": 3,
             "replay_nt_distinct": 300, "replay_th_distinct": 300, "replay_copies_each": 2,
             "train_rows_each_arm": 2251, "val_rows_each_arm": 50,
             "validation_ids_reused": str(val_prefix), "same_method_distribution": True,
             "tag_control_text_exact": True, "tag_control_order_exact": True,
             "new_primary_in_val": 0,
             "source_answer_type": {f"{a}/{b}": n for (a, b), n in sorted(arms["m1"].items())}}
    (DATA / "sft_expanded_th_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == "__main__":
    main()
