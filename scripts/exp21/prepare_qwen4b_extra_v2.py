#!/usr/bin/env python3
"""Prepare new, disjoint questions for a second CPU-only 4B-task-pool authoring pass."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
SOURCE = DATA / "qwen4b_teacher_graded320.jsonl"
EXISTING = DATA / "qwen4b_mixed401_positive.jsonl"
FROZEN = DATA / "sft_v4_recovery8_val.parquet"
V1_AUTHORED = AUDIT / "qwen4b_teacher_extra_sol_author.jsonl"
V1_REVISIONS = AUDIT / "qwen4b_teacher_extra_sol_author_revision.jsonl"
OUT = DATA / "qwen4b_extra_v2_candidates.jsonl"
REPORT = AUDIT / "qwen4b_extra_v2_selection_report.json"
NUMBER = re.compile(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?")


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def score(row: dict) -> tuple[int, int, str]:
    question = row["question"].lower()
    cues = ("sum", "total", "difference", "both", "each", "respectively", "area", "volume", "coordinates",
            "matrix", "polynomial", "factor", "ratio", "probability", "ways", "choose", "perimeter")
    return (sum(cue in question for cue in cues) + min(5, len(NUMBER.findall(question))), -len(question), row["id"])


def main() -> None:
    source = rows(SOURCE)
    mixed = rows(EXISTING)
    old_ids = {row["id"] for row in mixed}
    old_questions = {norm(row["question"]) for row in mixed}
    frozen = pd.read_parquet(FROZEN).to_dict("records")
    old_ids |= {row["id"] for row in frozen}
    old_questions |= {norm(row["extra_info"]["question"].rsplit("\n\nProblem: ", 1)[1]) for row in frozen}
    attempted = {row["id"] for path in (V1_AUTHORED, V1_REVISIONS) for row in rows(path)}
    kept = [row for row in source if row.get("clean") and row.get("correct") and not row.get("truncated")
            and row["id"] not in old_ids | attempted and norm(row["question"]) not in old_questions]
    kept.sort(key=score, reverse=True)
    assert kept and len({row["id"] for row in kept}) == len(kept)
    payload = [{key: row[key] for key in ("id", "source", "question", "gold", "answer_type")} for row in kept]
    OUT.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in payload))
    REPORT.write_text(json.dumps({"status": "authoring_candidates_only", "eligible_after_v1_attempts": len(payload),
                                  "v1_attempted_ids_excluded": len(attempted), "existing_train_or_frozen_ids_excluded": len(old_ids),
                                  "selection": "all remaining clean correct nontruncated tasks, sorted only for author triage",
                                  "output": str(OUT.relative_to(ROOT))}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"candidates": len(payload), "first_ids": [row["id"] for row in payload[:10]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
