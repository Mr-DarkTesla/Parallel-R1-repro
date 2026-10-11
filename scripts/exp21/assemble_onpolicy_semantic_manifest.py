#!/usr/bin/env python3
"""Fail closed when assembling manual PASS/FAIL review of filtered rollouts."""

import argparse
import json
import re
from pathlib import Path


VERDICT_FIRST = re.compile(r"^\|\s*(PASS|FAIL)\s*\|\s*([^|]+?)\s*\|", re.IGNORECASE)
VERDICT_SECOND = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(PASS|FAIL)\s*\|", re.IGNORECASE)
VERDICT_THIRD = re.compile(r"^\|\s*([^|]+?)\s*\|\s*[^|]+\|\s*(PASS|FAIL)\s*\|", re.IGNORECASE)


def read_provisional(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ids = [row["id"] for row in rows]
    if not rows or len(ids) != len(set(ids)):
        raise ValueError("provisional rows are empty or have duplicate IDs")
    for row in rows:
        if row.get("rejection_reasons") != []:
            raise ValueError(f"row is not provisional: {row['id']}")
    return ids


def read_reviews(paths):
    decisions = {}
    for path in paths:
        found = 0
        for line in path.read_text().splitlines():
            first = VERDICT_FIRST.match(line)
            second = VERDICT_SECOND.match(line) if first is None else None
            third = VERDICT_THIRD.match(line) if first is None and second is None else None
            if first:
                verdict, identifier = first.group(1).upper(), first.group(2).strip()
            elif second:
                verdict, identifier = second.group(2).upper(), second.group(1).strip()
            elif third:
                verdict, identifier = third.group(2).upper(), third.group(1).strip()
            else:
                continue
            if "/" not in identifier:
                continue  # Ignore review tables that summarize by answer type.
            if identifier in decisions:
                raise ValueError(f"empty or duplicate reviewed ID: {identifier!r}")
            decisions[identifier] = {"verdict": verdict, "review": str(path.resolve())}
            found += 1
        if not found:
            raise ValueError(f"no PASS/FAIL review rows: {path}")
    return decisions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provisional", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("reviews", type=Path, nargs="+")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    ids = read_provisional(args.provisional)
    decisions = read_reviews(args.reviews)
    if set(ids) != set(decisions):
        missing = sorted(set(ids) - set(decisions))
        unexpected = sorted(set(decisions) - set(ids))
        raise ValueError(f"review coverage mismatch: missing={missing[:5]}, unexpected={unexpected[:5]}")
    accepted = [identifier for identifier in ids if decisions[identifier]["verdict"] == "PASS"]
    result = {
        "semantic_path_independence": "reviewed",
        "provisional_path": str(args.provisional.resolve()),
        "review_files": [str(path.resolve()) for path in args.reviews],
        "reviewed_count": len(ids),
        "accepted_count": len(accepted),
        "rejected_count": len(ids) - len(accepted),
        "accepted_ids": accepted,
        "decisions": {identifier: decisions[identifier] for identifier in ids},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({key: result[key] for key in ("reviewed_count", "accepted_count", "rejected_count")}))


if __name__ == "__main__":
    main()
