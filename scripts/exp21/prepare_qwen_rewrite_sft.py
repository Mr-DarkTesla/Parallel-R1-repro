"""New Qwen-thinking rewrite SFT, with a matched tag-free control."""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

from mv_format import strip_tags


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
DATA = ROOT / "data"
PRIMARY = ROOT / "audit/qwen_structured_thinking/annotation_round2/rewrite_audited.jsonl"
BUILDER = Path(__file__).with_name("build_sft.py")


def main():
    primary = [json.loads(line) for line in PRIMARY.open()]
    assert len(primary) == len({row["id"] for row in primary}) == 180
    results = {}
    for arm, kind in (("tagged", "parallel_th"), ("control", "control_th")):
        prefix = DATA / f"sft_qwen_rewrite180_{arm}"
        specs = ([f"{kind}:{PRIMARY}"] * 6
                 + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * 2
                 + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 2)
        subprocess.run([sys.executable, str(BUILDER), str(prefix), "--rows", *specs,
                        "--val", "48", "--seed", "21"], check=True)
        results[arm] = {split: pd.read_parquet(f"{prefix}_{split}.parquet")
                        for split in ("train", "val")}
    for split in ("train", "val"):
        tagged, control = results["tagged"][split], results["control"][split]
        assert len(tagged) == len(control) and tagged["id"].tolist() == control["id"].tolist()
        for a, b in zip(tagged["extra_info"], control["extra_info"]):
            assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
            assert strip_tags(a["answer"]).strip() == b["answer"]
    report = {"primary_distinct": 180, "primary_copies": 6,
              "replay_nt_distinct": 300, "replay_th_distinct": 300,
              "replay_copies_each": 2, "total_rows_each": 2280,
              "train_rows_each": len(results["tagged"]["train"]),
              "val_rows_each": len(results["tagged"]["val"]),
              "tag_control_order_and_text_matched": True,
              "train_val_ids_disjoint": not set(results["tagged"]["train"]["id"]) &
              set(results["tagged"]["val"]["id"])}
    assert report["train_rows_each"] + report["val_rows_each"] == 2280
    assert report["train_val_ids_disjoint"]
    (DATA / "sft_qwen_rewrite180_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(report)


if __name__ == "__main__":
    main()
