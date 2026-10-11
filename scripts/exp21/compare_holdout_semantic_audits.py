"""Paired intervals from the two 40-row manual holdout audit tables.

Usage: python scripts/exp21/compare_holdout_semantic_audits.py RUN_ROOT AUDIT_CLEAN AUDIT_MIXED OUT_JSON
"""

import argparse
import json
import random
from pathlib import Path


SOURCES = {"GSM8K": "gsm8k", "GSM8K_DEV": "gsm8k", "MATH": "math", "MATH_DEV": "math"}
FIELDS = ("final_correct", "full_agreed_block", "useful_with_correct_final")
YES = {"yes": True, "да": True, "no": False, "нет": False}
REPEATS = 10_000


def parse_audit(path):
    rows = {}
    for line in path.read_text().splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] not in SOURCES or not cells[1].startswith("`"):
            continue
        source, problem_id = SOURCES[cells[0]], cells[1].strip("`")
        flags = tuple(YES.get(value.lower()) for value in cells[2:5])
        if None in flags:
            raise ValueError(f"{path}: invalid verdict for {problem_id}: {cells[2:5]}")
        if flags[2] and not (flags[0] and flags[1]):
            raise ValueError(f"{path}: useful block without correct final or full block: {problem_id}")
        key = (source, problem_id)
        if key in rows:
            raise ValueError(f"{path}: repeated ID: {problem_id}")
        rows[key] = dict(zip(FIELDS, flags))
    if len(rows) != 40 or sum(source == "gsm8k" for source, _ in rows) != 20:
        raise ValueError(f"{path}: expected 20 GSM8K + 20 MATH rows, found {len(rows)}")
    return rows


def scored_accuracy(root, arm):
    result = {}
    for source in ("gsm8k", "math"):
        path = root / arm / f"{source}-block-rows.jsonl"
        for line in path.read_text().splitlines():
            row = json.loads(line)
            result[source, row["problem_id"]] = bool(row["acc_robust"])
    if len(result) != 40:
        raise ValueError(f"{arm}: scored holdout has {len(result)} unique IDs")
    return result


def compare(a, b, metric, seed):
    grouped = {}
    for source in ("gsm8k", "math"):
        keys = sorted(key for key in a if key[0] == source)
        grouped[source] = [int(b[key][metric]) - int(a[key][metric]) for key in keys]
    rng = random.Random(seed)
    samples = []
    for _ in range(REPEATS):
        total = sum(sum(values[rng.randrange(len(values))] for _ in values)
                    for values in grouped.values())
        samples.append(100 * total / 40)
    samples.sort()
    return {
        "clean46": sum(100 * int(row[metric]) for row in a.values()) / 40,
        "mixed401": sum(100 * int(row[metric]) for row in b.values()) / 40,
        "mixed401_minus_clean46": 100 * sum(sum(v) for v in grouped.values()) / 40,
        "ci95": [samples[250], samples[9750]],
        "n": 40,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("audit_clean", type=Path)
    parser.add_argument("audit_mixed", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    a, b = parse_audit(args.audit_clean), parse_audit(args.audit_mixed)
    if set(a) != set(b):
        raise ValueError("audit IDs differ")
    for arm, manual in (("clean46", a), ("mixed401", b)):
        scored = scored_accuracy(args.run_root, arm)
        for key in manual:
            if manual[key]["final_correct"] != scored[key]:
                raise ValueError(f"{arm}: manual/automatic final answer differs for {key}")
    output = {
        "protocol": "same 40 holdout problems; one independent manual reviewer per arm",
        "bootstrap": "10k paired resamples, stratified 20 GSM8K + 20 MATH",
        "metrics": {metric: compare(a, b, metric, seed) for seed, metric in enumerate(FIELDS)},
        "by_source": {
            source: {arm: {metric: sum(int(row[metric]) for key, row in table.items() if key[0] == source)
                           for metric in FIELDS} for arm, table in (("clean46", a), ("mixed401", b))}
            for source in ("gsm8k", "math")
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output["metrics"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
