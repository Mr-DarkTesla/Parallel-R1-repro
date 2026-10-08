"""Collect exp21 per-benchmark summaries from corrected run directories into one CSV.

Usage: python collect_eval.py <eval_eff_dir> <output.csv>
"""
import csv
import json
import sys
from pathlib import Path


FIELDS = ("run", "suite", "mode", "bench", "problems", "accuracy", "mv_with_tags",
          "mv_valid_tagged", "mv_numbered_tagged", "mv_valid_blocks_percent",
          "mean_tokens", "mean_forward_passes", "truncated", "commit")


def main():
    root, output = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    for run in sorted(root.iterdir()):
        if not (run / "meta.json").exists():
            continue
        meta = json.loads((run / "meta.json").read_text())
        for path in sorted((run / "results").glob("*.json")):
            score = next(iter(json.loads(path.read_text()).values()))
            row = {"run": run.name, "suite": meta["suite"], "mode": meta["mode"],
                   "bench": path.stem, "problems": score.get("problems"),
                   "accuracy": score.get("accuracy_robust", score.get("accuracy")),
                   "commit": meta.get("commit")}
            row.update({key: score.get(key) for key in FIELDS if key not in row})
            rows.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} benchmark summaries -> {output}")


if __name__ == "__main__":
    main()
