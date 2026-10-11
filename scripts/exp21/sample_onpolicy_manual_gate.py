"""Draw a reproducible blind semantic-review sample from a completed run.

The auto filter establishes answer/format validity only. This script waits for
all 1144 rollouts and samples provisional answers uniformly by row; it never
uses gold or the model's training labels in the review file.
"""

import argparse
import collections
import json
import random
from pathlib import Path


def read_jsonl(path):
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filter_root", type=Path)
    parser.add_argument("sample_path", type=Path)
    parser.add_argument("--seed", type=int, default=20261012)
    args = parser.parse_args()

    summary = json.loads((args.filter_root / "summary.json").read_text())
    if summary["rollouts"] != 1144:
        raise ValueError(f"manual gate requires complete 1144 rollouts, got {summary['rollouts']}")
    provisional = read_jsonl(args.filter_root / "provisional_candidates.jsonl")
    rejected = read_jsonl(args.filter_root / "rejected_rollouts.jsonl")
    if len(provisional) != summary["provisional"] or len(rejected) != summary["rejected"]:
        raise ValueError("filter summary does not match raw rows")
    if len(provisional) + len(rejected) != 1144 or len(provisional) < 40:
        raise ValueError("missing rollout rows or fewer than 40 provisional answers")
    if len({(row["id"], row["seed"]) for row in provisional + rejected}) != 1144:
        raise ValueError("duplicate rollout ID/seed")
    if any(row["rejection_reasons"] or row["truncated"] for row in provisional):
        raise ValueError("provisional sample contains rejected/truncated answer")
    if args.sample_path.exists() or args.sample_path.with_suffix(".manifest.json").exists():
        raise FileExistsError("refusing to redraw an existing manual gate")

    chosen = random.Random(args.seed).sample(provisional, 40)
    blind = [{key: row[key] for key in
              ("id", "source", "answer_type", "seed", "tokens", "question", "output")}
             for row in chosen]
    args.sample_path.parent.mkdir(parents=True, exist_ok=True)
    with args.sample_path.open("x") as handle:
        for row in blind:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    manifest = {
        "method": "uniform_without_replacement_over_automatically_accepted_rollout_rows",
        "seed": args.seed,
        "complete_rollouts": 1144,
        "provisional": len(provisional),
        "sample": len(blind),
        "by_source": dict(sorted(collections.Counter(row["source"] for row in blind).items())),
        "distinct_tasks": len({row["id"] for row in blind}),
        "sample_keys": [[row["id"], row["seed"]] for row in blind],
        "gold_in_sample": False,
        "semantic_review": "pending",
    }
    args.sample_path.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: manifest[key] for key in
                      ("complete_rollouts", "provisional", "sample", "by_source", "distinct_tasks")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
