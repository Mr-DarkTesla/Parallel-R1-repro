"""Summarize matched M2 masked fixed40 steps and paired old/new intervals."""

import json
import random
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVE = ROOT / "eval_archives/expanded-th-masked-pilot40.tgz"
FIELDS = ("acc_robust", "think_numbered_block", "truncated", "tokens", "forward_passes")


def rows_from_dir(path):
    if not (path / "DONE").is_file():
        raise ValueError(f"incomplete fixed40: {path}")
    rows = [json.loads(line) for file in path.glob("*block-rows.jsonl") for line in file.open()]
    if len(rows) != 40 or len({row["problem_id"] for row in rows}) != 40:
        raise ValueError(f"expected 40 distinct rows: {path}")
    return {row["problem_id"]: row for row in rows}


def old_rows():
    rows = []
    with tarfile.open(ARCHIVE) as archive:
        for member in archive.getmembers():
            if member.name.startswith("masked_pilot/m2-") and member.name.endswith("-block-rows.jsonl"):
                rows.extend(json.loads(line) for line in archive.extractfile(member))
    if len(rows) != 40 or len({row["problem_id"] for row in rows}) != 40:
        raise ValueError("old M2 archive lacks 40 distinct rows")
    return {row["problem_id"]: row for row in rows}


def summary(rows):
    return {"n": len(rows), **{field: sum(float(row[field]) for row in rows.values()) for field in FIELDS}}


def paired(old, new):
    if old.keys() != new.keys() or any(old[key]["input"] != new[key]["input"] for key in old):
        raise ValueError("old/new problem IDs or exact prompts differ")
    ids = sorted(old)
    result = {}
    for field in FIELDS:
        deltas = [float(new[key][field]) - float(old[key][field]) for key in ids]
        randomizer = random.Random(20261011)
        draws = sorted(sum(deltas[randomizer.randrange(40)] for _ in ids) / 40 for _ in range(10000))
        result[field] = {"mean_delta": sum(deltas) / 40, "ci95": [draws[249], draws[9749]]}
    return result


def main():
    old = old_rows()
    steps = {step: rows_from_dir(ROOT / f"eval_archives/m2_spanfocus_tagged_step{step}")
             for step in (16, 32, 64)}
    report = {"protocol": "matched-masked-greedy-fixed40", "old_M2_full_CE": summary(old),
              "span_focused_steps": {str(step): summary(rows) for step, rows in steps.items()},
              "paired_step64_minus_old_M2": paired(old, steps[64]),
              "bootstrap": {"resamples": 10000, "seed": 20261011, "sample_unit": "problem_id"}}
    output = ROOT / "audit/m2_spanfocus_paired.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(output)


if __name__ == "__main__":
    main()
