"""Collect exp21 per-benchmark summaries from corrected run directories into one CSV.

Usage: python collect_eval.py <eval_eff_dir> <output.csv>
"""
import csv
import json
import sys
from pathlib import Path


FIELDS = ("run", "suite", "mode", "bench", "source", "problems", "accuracy", "mv_with_tags",
          "mv_valid_tagged", "mv_valid_responses", "mv_numbered_tagged", "mv_valid_blocks_percent",
          "mean_tokens", "mean_forward_passes", "truncated", "commit")


def main():
    root, output = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    for run in sorted(root.iterdir()):
        if not (run / "meta.json").exists():
            continue
        meta = json.loads((run / "meta.json").read_text())
        for path in sorted((run / "results").glob("*.json")):
            scored = run / "rows" / f"{path.stem}.jsonl"
            valid = {}
            if scored.exists():
                for line in scored.open():
                    item = json.loads(line)
                    if item.get("mv_valid") is not None:
                        count, correct = valid.get(item["source"], (0, 0))
                        valid[item["source"]] = (count + 1, correct + bool(item["mv_valid"]))
            for source, score in json.loads(path.read_text()).items():
                row = {"run": run.name, "suite": meta["suite"], "mode": meta["mode"],
                       "bench": path.stem, "source": source, "problems": score.get("problems"),
                       "accuracy": score.get("accuracy_robust", score.get("accuracy")),
                       "commit": meta.get("commit")}
                row.update({key: score.get(key) for key in FIELDS if key not in row})
                if source in valid:
                    count, correct = valid[source]
                    row["mv_valid_responses"] = round(100 * correct / count, 2)
                rows.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} benchmark summaries -> {output}")


if __name__ == "__main__":
    main()
