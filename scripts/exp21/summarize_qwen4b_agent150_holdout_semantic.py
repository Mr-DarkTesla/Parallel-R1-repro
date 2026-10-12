#!/usr/bin/env python3
"""Paired blinded semantic review for the authored150 fresh masked dev40."""

import argparse
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
AUDIT = ROOT / "audit"
ARMS = {
    "parent": {"gsm8k": "parent_gsm8k20", "math": "parent_math20"},
    "plain16": {"gsm8k": "plain16_gsm20", "math": "plain16_math20"},
    "tagged32": {"gsm8k": "tagged32_gsm8k20", "math": "tagged32_math20"},
}
BLIND_FIELDS = {"id", "cohort", "input", "output"}
REVIEW_FIELDS = {
    "id", "cohort", "correct_final", "strict_final", "full_block_inside_think",
    "independent_useful", "pass", "reason",
}


def read_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_arm(audit, arm):
    result = {}
    for source, suffix in ARMS[arm].items():
        stem = f"agent_parallel150_holdout_{suffix}"
        blind = read_jsonl(audit / f"{stem}_blind.jsonl")
        review = read_jsonl(audit / f"{stem}_review.jsonl")
        if len(blind) != 20 or len(review) != 20:
            raise ValueError(f"{stem}: expected 20 blind and reviewed rows")
        pairs = []
        for left, right in zip(blind, review):
            identifier = left.get("id")
            if set(left) != BLIND_FIELDS or set(right) != REVIEW_FIELDS:
                raise ValueError(f"{stem}/{identifier}: schema mismatch")
            if left["id"] != right["id"] or left["cohort"] != right["cohort"]:
                raise ValueError(f"{stem}/{identifier}: review/order mismatch")
            if left["cohort"] != f"{source}_holdout20":
                raise ValueError(f"{stem}/{identifier}: wrong source")
            for field in ("correct_final", "strict_final", "full_block_inside_think", "independent_useful", "pass"):
                if type(right[field]) is not bool:
                    raise ValueError(f"{stem}/{identifier}: invalid {field}")
            if right["pass"] != (right["correct_final"] and right["full_block_inside_think"]
                                  and right["independent_useful"]):
                raise ValueError(f"{stem}/{identifier}: inconsistent pass")
            if not isinstance(right["reason"], str) or not right["reason"].strip():
                raise ValueError(f"{stem}/{identifier}: missing reason")
            pairs.append({"id": identifier, "input": left["input"], "useful": right["pass"],
                          "correct_final_manual": right["correct_final"],
                          "strict_final_manual": right["strict_final"],
                          "full_block_manual": right["full_block_inside_think"]})
        if len({row["id"] for row in pairs}) != 20:
            raise ValueError(f"{stem}: duplicate ID")
        result[source] = pairs
    return result


def validate_same_questions(arms):
    parent = arms["parent"]
    for arm in ("plain16", "tagged32"):
        for source in ("gsm8k", "math"):
            for a, b in zip(parent[source], arms[arm][source]):
                if a["id"] != b["id"] or a["input"] != b["input"]:
                    raise ValueError(f"{arm}/{source}: question, prompt, or order mismatch")


def counts(by_source):
    return {
        source: {field: sum(row[field] for row in rows)
                 for field in ("useful", "correct_final_manual", "strict_final_manual", "full_block_manual")}
        for source, rows in by_source.items()
    }


def paired(reference, candidate, field):
    changes = {
        source: [int(right[field]) - int(left[field])
                 for left, right in zip(reference[source], candidate[source])]
        for source in ("gsm8k", "math")
    }
    values = changes["gsm8k"] + changes["math"]
    rng = random.Random(0)
    draws = sorted(sum(sum(part[rng.randrange(20)] for _ in range(20))
                       for part in changes.values()) / 40 for _ in range(10_000))
    return {"delta_pp": round(100 * sum(values) / 40, 2),
            "ci95_pp": [round(100 * draws[index], 2) for index in (249, 9749)],
            "n": 40, "bootstrap": "10,000 paired draws, stratified 20 GSM8K + 20 MATH"}


def build(audit):
    arms = {arm: load_arm(audit, arm) for arm in ARMS}
    validate_same_questions(arms)
    pairs = (("parent", "plain16"), ("parent", "tagged32"), ("plain16", "tagged32"))
    return {
        "protocol": "same fresh masked greedy dev40; two blind readers per arm, 20 rows each",
        "criterion": "correct final plus complete block inside think with independent distinct necessary correct paths and valid conclusion",
        "counts": {arm: counts(rows) for arm, rows in arms.items()},
        "paired": {f"{candidate}_minus_{reference}": {
            field: paired(arms[reference], arms[candidate], field)
            for field in ("useful", "correct_final_manual", "strict_final_manual", "full_block_manual")
        } for reference, candidate in pairs},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT)
    parser.add_argument("--output", type=Path, default=ROOT / "audit/agent_parallel150_holdout_semantic_paired.json")
    args = parser.parse_args()
    result = build(args.audit_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
