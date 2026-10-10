"""Keep the audited M1 examples with exactly two independent Paths.

Later siblings are intentionally invisible and share positions; a third Path cannot
infer whether it is second or third without an added branch index. Two Paths avoid
that numbering ambiguity while preserving the required parallel structure.
"""

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

from mv_format import parse, strip_tags


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
SOURCE = DATA / "pair_expanded_m1_thinking.jsonl"
FILTERED = DATA / "pair_expanded_m1_two_paths.jsonl"
PREFIX = DATA / "sft_expanded_th_m1_twopath_replay3_tagged"
CONTROL = DATA / "sft_expanded_th_m1_twopath_replay3_control"


def main():
    source = [json.loads(line) for line in SOURCE.open()]
    kept = [row for row in source if row["response"].count("<Path>") == 2]
    assert len(source) == 367 and len(kept) == 337
    assert all((parsed := parse(row["response"]))["valid"]
               and len(parsed["blocks"]) == 1
               and parsed["blocks"][0]["numbered"]
               for row in kept)
    FILTERED.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept))
    val_prefix = DATA / "sft_expanded_val_ids"
    for prefix, kind in ((PREFIX, "parallel_th"), (CONTROL, "control_th")):
        specs = ([f"{kind}:{FILTERED}"] * 3
                 + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * 3
                 + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 3)
        subprocess.run([sys.executable, str(Path(__file__).with_name("build_sft.py")),
                        str(prefix), "--rows", *specs,
                        "--val-ids-from", str(val_prefix), "--seed", "21"], check=True)
    train = pd.read_parquet(f"{PREFIX}_train.parquet")
    val = pd.read_parquet(f"{PREFIX}_val.parquet")
    fixed_ids = set(pd.read_parquet(f"{val_prefix}_val.parquet").id)
    assert not set(train.id) & fixed_ids and set(val.id) == fixed_ids
    assert all(info["answer"].count("<Path>") == 2
               for frame in (train, val) for info in frame.extra_info
               if info["kind"] == "parallel_th")
    for split, tagged in (("train", train), ("val", val)):
        control = pd.read_parquet(f"{CONTROL}_{split}.parquet")
        assert tagged.id.tolist() == control.id.tolist()
        for a, b in zip(tagged.extra_info, control.extra_info):
            assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
            assert strip_tags(a["answer"]).strip() == b["answer"].strip()
    report = {"source_distinct": len(source), "retained_two_path_distinct": len(kept),
              "removed_three_path_distinct": len(source) - len(kept),
              "primary_copies": 3, "replay_copies_each": 3,
              "train_rows": len(train), "val_rows": len(val),
              "validation_ids_reused": True, "control_text_and_order_matched": True,
              "new_annotations": 0,
              "source_audit": "DATASET_EXPANDED_THINKING.md"}
    (DATA / "sft_expanded_th_m1_twopath_replay3_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
