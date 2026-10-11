#!/usr/bin/env python3
"""Compare the matched 4B focus34 fixed40 pilot with its mixed401 parents."""

import json
from pathlib import Path

from summarize_qwen4b_mixed401 import (
    ROOT, STEMS, PROTOCOL, compare, load_archive, read_json, read_jsonl,
    require, row_key, same_fixed40, summarize,
)


ARCHIVES = ROOT / "eval_archives"
OUTPUT = ROOT / "audit/qwen4b_focus34_paired.json"


def focus_rows(arm):
    path = ARCHIVES / f"qwen4b_focus34_{arm}_step32"
    model = f"/tmp/exp21-selective-runs/exp21-4b-focus34-{arm}-p32/step_models/step_32/model"
    require((path / "DONE").is_file(), f"unfinished {path}")
    result = {}
    for stem, source, budget in STEMS:
        meta = read_json(path / f"{stem}.jsonl.meta.json")
        require(meta.get("model") == model, f"{stem}: unexpected checkpoint")
        require(str(meta.get("data", "")).endswith(f"/masked_pilot/{stem}.parquet"),
                f"{stem}: unexpected dataset")
        require(meta.get("max_tokens") == budget, f"{stem}: unexpected budget")
        for key, expected in PROTOCOL.items():
            require(meta.get(key) == expected, f"{stem}: {key} mismatch")
        scores = read_jsonl(path / f"{stem}-rows.jsonl")
        blocks = read_jsonl(path / f"{stem}-block-rows.jsonl")
        require(len(scores) == len(blocks) == 10, f"{stem}: not 10 rows")
        by_key = {row_key(row): row for row in blocks}
        require(len(by_key) == 10, f"{stem}: duplicate key")
        for score in scores:
            key = row_key(score)
            require(key not in result and key in by_key, f"{stem}: unmatched {key}")
            block = by_key[key]
            require(score["source"] == source and score["input"] == block["input"],
                    f"{stem}: source or prompt mismatch {key}")
            require(block.get("decoder") == "masked", f"{stem}: decoder mismatch")
            result[key] = {
                "input": score["input"], "strict": bool(score["acc"]),
                "robust": bool(block["acc_robust"]),
                "block": bool(block["think_numbered_block"]),
                "truncated": bool(block["truncated"]),
                "tokens": int(block["tokens"]),
                "forward_passes": int(block["forward_passes"]),
            }
    require(len(result) == 40, f"expected fixed40, got {len(result)}")
    return result


def main():
    initial = load_archive(ARCHIVES, "initial")
    parents = {arm: load_archive(ARCHIVES, f"mixed401_{arm}_step128")
               for arm in ("tagged", "plain")}
    focus = {arm: focus_rows(arm) for arm in ("tagged", "plain")}
    for arm in focus:
        same_fixed40(initial, focus[arm], f"focus34 {arm}")
        same_fixed40(parents[arm], focus[arm], f"focus34 {arm} vs parent")
    report = {
        "protocol": "same fixed40 prompts, thinking, masked-autonomous-v2, greedy seed 0",
        "focus34": {arm: {"metrics": summarize(focus[arm]),
                          "vs_initial": compare(initial, focus[arm]),
                          "vs_parent": compare(parents[arm], focus[arm])}
                    for arm in focus},
        "tagged_vs_plain": compare(focus["plain"], focus["tagged"]),
        "parents": {arm: summarize(parents[arm]) for arm in parents},
        "initial": summarize(initial),
        "semantic_review": "audit/qwen4b_focus34_tagged_step32_semantic_review.md",
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({arm: item["metrics"] for arm, item in report["focus34"].items()},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
