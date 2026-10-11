#!/usr/bin/env python3
"""Checked paired fixed40 summary for Qwen3-0.6B distill447 checkpoints."""

import argparse
import json
import re
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from summarize_m1_rewrapped_sweep import (ARCHIVES, ROOT, STEMS, STEM_ALIASES,
                                           compare, decode_jsonl, key, load, summary)


STEPS = (16, 32, 64, 96, 128)
PATTERN = re.compile(r"q06_distill447_(tagged|plain)_step(16|32|64|96|128)$")
OUTPUT = ROOT / "audit/q06_distill447_sweep_auto.json"


def original_rows():
    rows = load(ARCHIVES / "c0-greedy-pilot40.tgz", STEM_ALIASES)
    for row_key in FIXES:
        if row_key not in rows or rows[row_key]["robust"]:
            raise ValueError(f"C0 correction drift at {row_key}")
        rows[row_key]["robust"] = True
    return rows


def candidate_rows(path, arm, step):
    model = (f"/tmp/exp21-selective-runs/exp21-q06-distill447-{arm}-p128/"
             f"step_models/step_{step}/model")
    rows = load(path, STEMS, model)
    block_keys = set()
    for stem in STEMS:
        for block in decode_jsonl((path / f"{stem}-block-rows.jsonl").read_bytes()):
            row_key = key(block)
            if row_key not in rows or row_key in block_keys:
                raise ValueError(f"{path}/{stem}: duplicate or unexpected block {row_key}")
            if type(block.get("think_full_block")) is not bool or type(block.get("think_numbered_block")) is not bool:
                raise ValueError(f"{path}/{stem}: missing boolean block fields at {row_key}")
            rows[row_key]["block"] = block["think_full_block"] and block["think_numbered_block"]
            block_keys.add(row_key)
    if block_keys != set(rows):
        raise ValueError(f"{path}: incomplete block coverage")
    return rows, model


def build_result(expect_complete=False):
    original = original_rows()
    candidates = {}
    result = {
        "protocol": "same fixed40 prompts, thinking, masked greedy, 2048 GSM8K / 4096 MATH tokens",
        "metrics": "strict external answer, robust answer with two documented C0 parser fixes, complete numbered block inside think, truncation, generated tokens, ideal sequential forward passes",
        "intervals": "10,000 paired bootstrap samples, seed 0; binary deltas in percentage points",
        "semantic_review": "pending human judgment; complete grammar is not usefulness",
        "original": summary(original), "runs": {}, "tagged_vs_plain": {},
    }
    for path in sorted(ARCHIVES.iterdir()):
        match = PATTERN.fullmatch(path.name)
        if not match or not (path / "DONE").is_file():
            continue
        arm, step = match[1], int(match[2])
        rows, model = candidate_rows(path, arm, step)
        candidates[arm, step] = rows
        result["runs"][f"{arm}_step{step}"] = {
            "archive": path.name, "model": model,
            "metrics": summary(rows), "vs_original": compare(original, rows),
        }
    if not candidates:
        raise ValueError("no completed distill447 fixed40 archives")
    if expect_complete and set(candidates) != {(arm, step) for arm in ("tagged", "plain") for step in STEPS}:
        raise ValueError(f"incomplete distill447 sweep: {sorted(candidates)}")
    for step in STEPS:
        if ("tagged", step) in candidates and ("plain", step) in candidates:
            result["tagged_vs_plain"][f"step{step}"] = compare(candidates["plain", step],
                                                                 candidates["tagged", step])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-complete", action="store_true")
    args = parser.parse_args()
    result = build_result(args.expect_complete)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for name, run in result["runs"].items():
        print(name, run["metrics"], run["vs_original"]["robust"])


if __name__ == "__main__":
    main()
