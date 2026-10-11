#!/usr/bin/env python3
"""Rank eight reviewed selective checkpoints for the Multiverse objective."""

import argparse
import json
from pathlib import Path


STEPS = {8, 16, 24, 32, 40, 48, 56, 64}


def rank(row: dict, step: int) -> tuple[int, int, int, int, int, int]:
    useful = row.get("strict_useful_count")
    if useful is None:
        useful = row.get("strictly_useful_count")
    if useful is None:
        useful = len(row["strict_useful_ids"])
    numbered = row.get("numbered_blocks")
    if numbered is None:
        numbered = row["response_level_numbered"]
    return (
        int(numbered > 0),
        int(useful),
        int(row["external_final_correct"]),
        -int(row["truncated"]),
        -int(row["outside_think"]),
        step,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="reviewed JSON with eight step summaries")
    args = parser.parse_args()
    data = json.loads(args.summary.read_text())
    steps = {int(key): value for key, value in data["steps"].items()}
    if set(steps) != STEPS:
        parser.error("summary must contain exactly steps 8,16,...,64")
    ordered = sorted(steps, key=lambda step: rank(steps[step], step), reverse=True)
    for index, step in enumerate(ordered, 1):
        row = steps[step]
        print(index, step, rank(row, step)[:5], "KEEP" if index <= 5 else "DROP")
    print("TOP5_STEPS=", ",".join(map(str, sorted(ordered[:5]))), sep="")


if __name__ == "__main__":
    main()
