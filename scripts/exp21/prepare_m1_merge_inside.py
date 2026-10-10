"""Move final arithmetic into the merge point of audited two-Path M1 answers."""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from mv_format import parse

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
SOURCE = DATA / "pair_expanded_m1_two_paths.jsonl"
OUTPUT = DATA / "pair_expanded_m1_merge_inside.jsonl"
PREFIX = DATA / "sft_expanded_th_m1_merge_inside_replay3_tagged"
REPORT = DATA / "m1_merge_inside_audit.json"
NUMBERS = re.compile(r"(?<!\w)\d+(?:\.\d+)?(?:/\d+)?")


def move_merge(row):
    original = row["response"]
    conclusion_end = original.index("</Conclusion>")
    parallel_end = original.index("</Parallel>") + len("</Parallel>")
    think_end = original.index("</think>")
    post = original[parallel_end:think_end].strip()
    assert post and original.count("<Parallel>") == 1
    changed = (original[:conclusion_end].rstrip() + "\n" + post + "\n"
               + original[conclusion_end:parallel_end] + "\n" + original[think_end:])
    assert Counter(NUMBERS.findall(changed)) == Counter(NUMBERS.findall(original))
    assert original[:original.index("<Conclusion>")] == changed[:changed.index("<Conclusion>")]
    assert changed[changed.index("</think>"):] == original[think_end:]
    parsed = parse(changed)
    assert parsed["valid"] and len(parsed["blocks"]) == 1
    assert parsed["blocks"][0]["numbered"] and changed.count("<Path>") == 2
    result = dict(row)
    result["response"] = changed
    result["moved_into_conclusion_chars"] = len(post)
    return result


def main():
    source = [json.loads(line) for line in SOURCE.open()]
    assert len(source) == 337 and len({r["id"] for r in source}) == 337
    rows = [move_merge(row) for row in source]
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
    assert len(train) == 2748 and len(val) == 63
    for new, old in ((train, old_train), (val, old_val)):
        assert new.id.tolist() == old.id.tolist()
        for a, b in zip(new.extra_info, old.extra_info):
            assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
            if a["kind"] != "parallel_th":
                assert a == b
    report = {"source_rows": len(source), "moved_rows": len(rows),
              "moved_chars_total": sum(r["moved_into_conclusion_chars"] for r in rows),
              "same_ids_order_split_replay": True, "same_paths": True,
              "same_final_answer": True, "same_numeric_multiset": True,
              "train_rows": len(train), "val_rows": len(val)}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
