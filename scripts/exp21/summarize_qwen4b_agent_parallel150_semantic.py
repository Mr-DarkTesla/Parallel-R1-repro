#!/usr/bin/env python3
"""Rebuild strict paired semantic audit for the authored150 tagged checkpoints."""

import argparse
import json
import os
import tempfile
from pathlib import Path

from summarize_qwen4b_agent_parallel150 import paired_interval
from summarize_qwen4b_mixed401 import ROOT, SummaryError, read_jsonl, require


AUDIT = ROOT / "audit"
OUTPUT = AUDIT / "agent_parallel150_semantic_paired.json"
COHORTS = ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")
BLIND_FIELDS = {"cohort", "id", "input", "output"}
REVIEW_FIELDS = {
    "id", "cohort", "correct_final", "strict_final", "full_block_inside_think",
    "independent_useful", "pass", "reason",
}
VARIANTS = {
    "clean46_parent_step32": "rereview",
    "agent_parallel150_tagged_step8": "review",
    "agent_parallel150_tagged_step16": "review",
    "agent_parallel150_tagged_step32": "review",
}


def require_schema(row, fields, context):
    require(set(row) == fields, f"{context}: schema mismatch")


def load_variant(audit, label, review_kind):
    blind_parts = [read_jsonl(audit / f"{label}_blind_{part}.jsonl") for part in ("a", "b")]
    full = read_jsonl(audit / f"{label}_blind_full.jsonl")
    review_parts = [read_jsonl(audit / f"{label}_{review_kind}_{part}.jsonl") for part in ("a", "b")]
    require(all(len(rows) == 20 for rows in blind_parts + review_parts),
            f"{label}: each blind/review part must contain 20 rows")
    require(len(full) == 40, f"{label}: blind full must contain 40 rows")
    require(full == blind_parts[0] + blind_parts[1], f"{label}: blind full differs from ordered parts")

    reviewed = {}
    for part, blind_rows, review_rows in zip(("a", "b"), blind_parts, review_parts):
        for index, (blind, review) in enumerate(zip(blind_rows, review_rows), 1):
            context = f"{label}/{part}[{index}]"
            require_schema(blind, BLIND_FIELDS, context)
            require_schema(review, REVIEW_FIELDS, context)
            require(all(isinstance(blind[field], str) and blind[field] for field in ("cohort", "id", "input", "output")),
                    f"{context}: invalid blind value")
            require(blind["id"] == review["id"] and blind["cohort"] == review["cohort"],
                    f"{context}: review key/cohort mismatch")
            for field in ("correct_final", "strict_final", "full_block_inside_think", "independent_useful", "pass"):
                require(type(review[field]) is bool, f"{context}: {field} must be boolean")
            require(isinstance(review["reason"], str) and review["reason"].strip(),
                    f"{context}: missing review reason")
            require(review["strict_final"] == review["correct_final"],
                    f"{context}: strict/correct final mismatch")
            require(review["pass"] == (review["correct_final"] and review["full_block_inside_think"]
                                        and review["independent_useful"]),
                    f"{context}: pass does not match rubric fields")
            require(blind["id"] not in reviewed, f"{context}: duplicate ID")
            reviewed[blind["id"]] = {
                "cohort": blind["cohort"], "input": blind["input"], "useful": review["pass"],
                "correct_final": review["correct_final"],
                "full_block_inside_think": review["full_block_inside_think"],
            }
    require(len(reviewed) == 40, f"{label}: expected 40 distinct IDs")
    cohort_counts = {cohort: sum(row["cohort"] == cohort for row in reviewed.values()) for cohort in COHORTS}
    require(cohort_counts == {cohort: 10 for cohort in COHORTS},
            f"{label}: wrong cohort counts {cohort_counts}")
    return {"rows": reviewed, "order": [row["id"] for row in full]}


def same_fixed40(reference, candidate, label):
    require(reference["order"] == candidate["order"], f"{label}: fixed40 order differs")
    reference_rows, candidate_rows = reference["rows"], candidate["rows"]
    require(set(reference_rows) == set(candidate_rows), f"{label}: fixed40 IDs differ")
    for identifier in reference["order"]:
        require(reference_rows[identifier]["cohort"] == candidate_rows[identifier]["cohort"],
                f"{label}: cohort drift at {identifier}")
        require(reference_rows[identifier]["input"] == candidate_rows[identifier]["input"],
                f"{label}: prompt drift at {identifier}")


def counts(rows):
    return {
        "useful": sum(row["useful"] for row in rows.values()),
        "correct_final_manual": sum(row["correct_final"] for row in rows.values()),
        "full_block_inside_think_manual": sum(row["full_block_inside_think"] for row in rows.values()),
        "gsm8k_useful": sum(row["useful"] for row in rows.values() if row["cohort"].startswith("gsm8k_")),
        "math_useful": sum(row["useful"] for row in rows.values() if row["cohort"].startswith("math_")),
    }


def build_result(audit):
    rows = {label: load_variant(audit, label, review_kind) for label, review_kind in VARIANTS.items()}
    parent = rows["clean46_parent_step32"]
    for label, candidate in rows.items():
        same_fixed40(parent, candidate, f"parent vs {label}")
    return {
        "criterion": "independent distinct necessary intermediate facts and conclusion combining them; correct final",
        "review": "two readers each reviewed 20 disjoint rows blind to gold/scorer; same rubric for all four variants",
        "fixed40": 40,
        "variants": {label: counts(rows[label]["rows"]) for label in VARIANTS},
        "paired_vs_parent": {
            label: paired_interval(parent["rows"], rows[label]["rows"], "useful")
            for label in VARIANTS if label != "clean46_parent_step32"
        },
    }


def write_atomic(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(result, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def self_test(audit):
    result = build_result(audit)
    require(result["variants"]["clean46_parent_step32"]["useful"] == 13,
            "real-data parent useful count drift")
    require(result["variants"]["agent_parallel150_tagged_step32"]["correct_final_manual"] == 35,
            "real-data step32 final count drift")
    require(result["paired_vs_parent"]["agent_parallel150_tagged_step8"]["n"] == 40,
            "real-data paired sample size drift")
    print("self-test passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    audit = args.audit_dir.resolve()
    if args.self_test:
        self_test(audit)
        return
    write_atomic(args.output, build_result(audit))


if __name__ == "__main__":
    try:
        main()
    except (SummaryError, FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
