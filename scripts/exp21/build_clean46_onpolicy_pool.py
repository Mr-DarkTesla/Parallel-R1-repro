"""Select new on-policy questions without reusing clean46 positives or masked holdout.

Usage: python scripts/exp21/build_clean46_onpolicy_pool.py CANDIDATES MANIFEST HOLDOUT_DIR OUT_JSONL AUDIT_JSON
The input 189 candidates have a prior leakcheck; this is a verified subset.
"""

import argparse
import json
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    parser.add_argument("clean46_manifest", type=Path)
    parser.add_argument("holdout", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("audit", type=Path)
    args = parser.parse_args()

    rows = [json.loads(line) for line in args.candidates.read_text().splitlines() if line.strip()]
    if len(rows) != 189 or len({row["id"] for row in rows}) != 189:
        raise ValueError("expected 189 distinct audited candidates")
    parent_audit_path = args.candidates.with_suffix(".audit.json")
    parent_audit = json.loads(parent_audit_path.read_text())
    checks = parent_audit["checks"]
    if (checks["leakcheck"]["checked_candidates"] != 189 or
            checks["leakcheck"]["blocking_hits"] != 0 or
            not checks["distinct_ids"] or
            not checks["distinct_normalized_questions"] or
            checks["selected_overlap_each_exclusion"] != 0 or
            set(parent_audit["ids"]["selected"]) != {row["id"] for row in rows}):
        raise ValueError("parent candidate audit failed")
    clean_ids = set(json.loads(args.clean46_manifest.read_text())["accepted_ids"])
    if len(clean_ids) != 46:
        raise ValueError("expected 46 clean46 positive IDs")

    holdout_ids, holdout_questions = set(), set()
    for source in ("gsm8k", "math"):
        frame = pd.read_parquet(args.holdout / f"{source}_holdout20.parquet")
        if len(frame) != 20:
            raise ValueError(f"{source}: expected 20 holdout questions")
        for info, prompt in zip(frame["extra_info"], frame["prompt"]):
            holdout_ids.add(info["id"])
            holdout_questions.add(normalize(prompt[0]["content"].split("Problem: ", 1)[1]))

    kept, reasons = [], Counter()
    for row in rows:
        if row["id"] in clean_ids:
            reasons["clean46_positive_id"] += 1
        elif row["id"] in holdout_ids or normalize(row["question"]) in holdout_questions:
            reasons["fresh_holdout_id_or_question"] += 1
        else:
            kept.append(row)
    if len(kept) + sum(reasons.values()) != len(rows) or len({r["id"] for r in kept}) != len(kept):
        raise ValueError("selection accounting or duplicate IDs failed")
    if any(r["id"] in holdout_ids or normalize(r["question"]) in holdout_questions for r in kept):
        raise ValueError("selected question overlaps masked holdout")
    if len(kept) < 100:
        raise ValueError(f"too few distinct unseen questions: {len(kept)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists() or args.audit.exists():
        raise FileExistsError("refusing to overwrite the on-policy pool or its audit")
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept))
    result = {
        "parent_candidates": str(args.candidates),
        "parent_audit": str(parent_audit_path),
        "parent_leakcheck": "189 checked, zero blocking hits",
        "clean46_manifest": str(args.clean46_manifest),
        "fresh_holdout": str(args.holdout),
        "source_count": len(rows),
        "excluded": dict(reasons),
        "selected_count": len(kept),
        "selected_by_source": dict(Counter(row["source"] for row in kept)),
        "selected_ids": [row["id"] for row in kept],
        "gold_answers_in_prompt": False,
    }
    args.audit.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("source_count", "excluded", "selected_count", "selected_by_source")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
