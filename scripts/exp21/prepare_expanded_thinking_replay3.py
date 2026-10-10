"""M1 dev tuning: lower backbone LR with more Qwen replay and unchanged tag LR."""

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
PRIMARY = DATA / "pair_expanded_m1_thinking.jsonl"
PREFIX = DATA / "sft_expanded_th_m1_replay3_tagged"


def main():
    val_prefix = DATA / "sft_expanded_val_ids"
    specs = ([f"parallel_th:{PRIMARY}"] * 3
             + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * 3
             + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 3)
    subprocess.run([sys.executable, str(Path(__file__).with_name("build_sft.py")),
                    str(PREFIX), "--rows", *specs,
                    "--val-ids-from", str(val_prefix), "--seed", "21"], check=True)
    train = pd.read_parquet(f"{PREFIX}_train.parquet")
    val = pd.read_parquet(f"{PREFIX}_val.parquet")
    fixed_ids = set(pd.read_parquet(f"{val_prefix}_val.parquet")["id"])
    assert not set(train.id) & fixed_ids
    assert set(val.id) == fixed_ids
    counts = {
        split: {kind: int((frame.data_source == f"exp21_{kind}").sum())
                for kind in ("parallel_th", "replay_nt", "replay_th")}
        for split, frame in (("train", train), ("val", val))
    }
    assert len(train) + len(val) == 3 * (367 + 300 + 300)
    assert all(row["answer"].startswith("<think>") and row["answer"].count("<Parallel>") == 1
               for row in train.extra_info if row["kind"] == "parallel_th")
    report = {"primary_distinct": 367, "primary_copies": 3,
              "replay_nt_distinct": 300, "replay_th_distinct": 300,
              "replay_copies_each": 3, "total_rows": len(train) + len(val),
              "train_rows": len(train), "val_rows": len(val),
              "validation_ids_reused": str(val_prefix), "counts": counts,
              "base_lr": 3e-6, "tag_lr_mult": 300,
              "effective_tag_lr": 9e-4, "steps": 64}
    (DATA / "sft_expanded_th_m1_replay3_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
