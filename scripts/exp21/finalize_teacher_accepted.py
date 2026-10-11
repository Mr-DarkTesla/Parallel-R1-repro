#!/usr/bin/env python3
"""Promote screened Sol6.1 examples only after the two recorded quality gates."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
SCREENED = RUN / "data/teacher_parallel_screened_sol61.jsonl"
REVIEW = RUN / "audit/teacher_screened_independent30.jsonl"
PRIMARY = RUN / "audit/teacher_screened_primary20.md"
OUT = RUN / "data/teacher_parallel_accepted196.jsonl"

PRIMARY_IDS = {
    "gsm8k-train/908", "gsm8k-train/1231", "gsm8k-train/1182", "gsm8k-train/616", "gsm8k-train/1938",
    "math-train/2371", "math-train/3054", "math-train/2364", "math-train/2386", "math-train/2899",
    "math-train/1760", "math-train/2457", "math-train/2273", "math-train/1916", "math-train/175",
    "math-train/2804", "math-train/1400", "math-train/219", "math-train/5660", "math-train/1494",
}


def rows(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main():
    screened, review = rows(SCREENED), rows(REVIEW)
    ids = {r["id"] for r in screened}
    assert len(screened) == len(ids) == 196
    assert len(PRIMARY_IDS) == 20 and PRIMARY_IDS <= ids
    primary_text = PRIMARY.read_text()
    assert "20/20 полезных" in primary_text and "0 неверных" in primary_text
    assert all(f"`{problem_id}`" in primary_text for problem_id in PRIMARY_IDS)
    assert len(review) >= 30 and len({r["id"] for r in review}) == len(review)
    assert {r["id"] for r in review} <= ids
    assert sum(bool(r.get("useful")) for r in review) / len(review) >= .9
    assert all(r.get("answer_correct") is True and r.get("placement_inside_think") is True for r in review)
    assert all(r.get("answer_verification") == "verified_math_verify" and r.get("status") == "screened_not_accepted" for r in screened)
    accepted = []
    for row in screened:
        item = dict(row)
        item["status"] = "accepted_for_sft"
        item["acceptance_audits"] = [
            str(PRIMARY.relative_to(ROOT)),
            str(REVIEW.relative_to(ROOT)),
        ]
        accepted.append(item)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in accepted))
    print(json.dumps({"accepted": len(accepted), "primary_full_read": len(PRIMARY_IDS),
                      "independent_full_read": len(review), "out": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
