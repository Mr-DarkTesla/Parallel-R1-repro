"""Compare a 20-task plain thinking pilot with saved full-dev sample-0 rows.

Usage: python compare_plain_pilot.py PILOT_ROWS EVAL_EFF_DIR OUT_JSON
The saved dev runs used a 16k budget; report token and truncation differences.
"""
import json
import sys
from pathlib import Path

import numpy as np


def read(path):
    return [json.loads(line) for line in open(path)]


if __name__ == "__main__":
    pilot = read(sys.argv[1])
    assert pilot and all(row["sample"] == 0 for row in pilot)
    assert len(pilot) == len({row["problem_id"] for row in pilot})
    base = Path(sys.argv[2])
    runs = {"pilot": pilot}
    for name in ("c0", "m1", "m2a", "control-m1"):
        saved = {(row["problem_id"], row["sample"]): row for row in
                 read(base / f"{name}-dev-th/rows/gsm8k_dev.jsonl")}
        runs[name] = [saved[(row["problem_id"], 0)] for row in pilot]
        assert all(a["problem"] == b["problem"] for a, b in zip(pilot, runs[name]))
    rng = np.random.default_rng(0)
    indices = rng.integers(0, len(pilot), size=(10000, len(pilot)))
    result = {"problems": len(pilot), "budget_pilot": 4096, "budget_saved": 16384, "runs": {}, "paired": {}}
    for name, rows in runs.items():
        result["runs"][name] = {
            "correct": sum(bool(row["acc_robust"]) for row in rows),
            "truncated": sum(bool(row["truncated"]) for row in rows),
            "over_4096_tokens": sum(row["tokens"] > 4096 for row in rows),
            "mean_tokens": round(sum(row["tokens"] for row in rows) / len(rows), 1),
        }
        if name == "pilot":
            continue
        delta = np.array([int(a["acc_robust"]) - int(b["acc_robust"])
                          for a, b in zip(pilot, rows)])
        result["paired"][name] = {"accuracy_delta_pp": round(100 * delta.mean(), 1),
                                    "ci95": [round(float(x), 1) for x in
                                             np.percentile(100 * delta[indices].mean(1), [2.5, 97.5])]}
    Path(sys.argv[3]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
