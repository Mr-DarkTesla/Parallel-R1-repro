"""Move an audited two-Path M1 block to the start of <think> when no numbers are lost."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

from mv_format import parse

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
SOURCE = DATA / "pair_expanded_m1_two_paths.jsonl"
OUTPUT = DATA / "pair_expanded_m1_frontblock.jsonl"
PREFIX = DATA / "sft_expanded_th_m1_frontblock_replay3_tagged"
REPORT = DATA / "m1_frontblock_audit.json"
NUMBERS = re.compile(r"(?<!\w)\d+(?:\.\d+)?(?:/\d+)?")
KEEP_PREAMBLE = {"math-train/3081"}  # symmetry/point definitions used by both Paths


def move_block(row):
    original = row["response"]
    assert original.startswith("<think>") and original.count("<Parallel>") == 1
    block = original.index("<Parallel>")
    close = original.index("</think>")
    prefix = original[len("<think>"):block]
    suffix = original[block:]
    numbers_before = set(NUMBERS.findall(original))
    numbers_after = set(NUMBERS.findall(suffix))
    numbers_preserved_without_prefix = numbers_before <= numbers_after
    transformed = numbers_preserved_without_prefix and row["id"] not in KEEP_PREAMBLE
    changed = "<think>\n" + suffix if transformed else original
    assert set(NUMBERS.findall(changed)) == numbers_before if transformed else changed == original
    assert changed[changed.index("<Parallel>"):] == suffix
    assert changed[changed.index("</think>"):] == original[close:]
    assert (parsed := parse(changed))["valid"] and len(parsed["blocks"]) == 1
    assert parsed["blocks"][0]["numbered"] and changed.count("<Path>") == 2
    result = dict(row)
    result["response"] = changed
    result["frontblock_transformed"] = transformed
    result["frontblock_number_safe"] = numbers_preserved_without_prefix
    result["removed_preamble_chars"] = len(prefix) if transformed else 0
    return result


def main():
    source = [json.loads(line) for line in SOURCE.open()]
    assert len(source) == 337 and len({r["id"] for r in source}) == 337
    rows = [move_block(row) for row in source]
    assert len(rows) == len(source)
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    val_ids = DATA / "sft_expanded_val_ids"
    specs = ([f"parallel_th:{OUTPUT}"] * 3
             + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * 3
             + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 3)
    subprocess.run([sys.executable, str(Path(__file__).with_name("build_sft.py")),
                    str(PREFIX), "--rows", *specs,
                    "--val-ids-from", str(val_ids), "--seed", "21"], check=True)
    train = pd.read_parquet(f"{PREFIX}_train.parquet")
    val = pd.read_parquet(f"{PREFIX}_val.parquet")
    old_train = pd.read_parquet(DATA / "sft_expanded_th_m1_twopath_replay3_tagged_train.parquet")
    old_val = pd.read_parquet(DATA / "sft_expanded_th_m1_twopath_replay3_tagged_val.parquet")
    assert train.id.tolist() == old_train.id.tolist()
    assert val.id.tolist() == old_val.id.tolist()
    assert len(train) == 2748 and len(val) == 63
    for new, old in ((train, old_train), (val, old_val)):
        for a, b in zip(new.extra_info, old.extra_info):
            assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
            if a["kind"] != "parallel_th":
                assert a == b
    report = {"source_rows": len(source),
              "frontblock_transformed": sum(r["frontblock_transformed"] for r in rows),
              "unchanged_for_number_preservation": sum(not r["frontblock_number_safe"] for r in rows),
              "unchanged_for_context": sum(r["id"] in KEEP_PREAMBLE for r in rows),
              "removed_preamble_chars_total": sum(r["removed_preamble_chars"] for r in rows),
              "train_rows": len(train), "val_rows": len(val),
              "same_ids_order_split_replay": True, "same_block_and_final_suffix": True,
              "source_card": "DATASET_M1_TWOPATH_TAGWEIGHTED.md"}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
