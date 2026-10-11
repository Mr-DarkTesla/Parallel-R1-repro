#!/usr/bin/env python3
"""Select a leak-clean, unused four-stratum pool for a Qwen3-4B teacher pilot."""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
SOURCES = (
    "pair_final_m1.jsonl",
    "more_m1_matched180.jsonl",
    "teacher_trajectory_candidates.jsonl",
    "onpolicy_agent_authored_accepted78.jsonl",
)
OUT = DATA / "qwen4b_teacher_pool320.jsonl"


def read(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def rank(row):
    return hashlib.sha256(("qwen4b-teacher-20261011\0" + row["id"]).encode()).hexdigest()


def main():
    excluded = {row["id"] for name in SOURCES for row in read(DATA / name)}
    pool = read(DATA / "pool.jsonl")
    assert len(pool) == len({row["id"] for row in pool})
    groups = collections.defaultdict(list)
    for row in pool:
        if row["id"] in excluded or row["source"] not in ("gsm8k", "math"):
            continue
        key = (row["source"], row["answer_type"])
        if key in (("gsm8k", "integer"), ("math", "integer"), ("math", "fraction"), ("math", "expression")):
            groups[key].append(row)
    chosen = []
    for key in (("gsm8k", "integer"), ("math", "integer"), ("math", "fraction"), ("math", "expression")):
        rows = groups[key]
        if key[0] == "math":
            easy = sorted((r for r in rows if r.get("level") in ("Level 1", "Level 2", "Level 3")), key=rank)
            hard = sorted((r for r in rows if r.get("level") not in ("Level 1", "Level 2", "Level 3")), key=rank)
            selected = easy[:60] + hard[:20]
        else:
            selected = sorted(rows, key=rank)[:80]
        assert len(selected) == 80, key
        chosen += selected
    assert len(chosen) == len({r["id"] for r in chosen}) == 320
    assert not ({r["id"] for r in chosen} & excluded)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in chosen))
    print(json.dumps({"out": str(OUT), "rows": len(chosen), "excluded_prior_ids": len(excluded),
                      "strata": {str(k): v for k, v in collections.Counter((r["source"], r["answer_type"]) for r in chosen).items()}}, indent=2))


if __name__ == "__main__":
    main()
