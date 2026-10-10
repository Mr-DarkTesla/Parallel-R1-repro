"""Make blind review batches from correct Qwen thinking outputs with Part headings."""
import collections
import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking"
P1 = re.compile(r"\bPart\s*1\s*[:.]", re.I)
P2 = re.compile(r"\bPart\s*2\s*[:.]", re.I)
SEED = 20261010


def write(path, rows):
    with path.open("w") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    groups = collections.defaultdict(list)
    counts = collections.Counter()
    for row in (json.loads(line) for line in (ROOT / "graded.jsonl").open()):
        key = (row["source"], row["answer_type"])
        counts[(key, "generated")] += 1
        if not row["correct"]:
            continue
        counts[(key, "correct")] += 1
        thought = row["output"].split("</think>", 1)[0]
        first, second = P1.search(thought), P2.search(thought)
        if first and second and first.start() < second.start() and "<Parallel>" not in row["output"]:
            groups[key].append(row)
    rng = random.Random(SEED)
    blind, gold = [], []
    for key in sorted(groups):
        rng.shuffle(groups[key])
        for row in groups[key]:
            blind.append({"id": row["id"], "question": row["question"], "response": row["output"],
                          "source": row["source"], "answer_type": row["answer_type"], "tokens": row["tokens"]})
            gold.append({"id": row["id"], "question": row["question"], "answer": row["gold"]})
    assert len(blind) == len(gold) == len({r["id"] for r in blind}) == 149
    write(ROOT / "candidates149_blind.jsonl", blind)
    write(ROOT / "candidates149_with_gold.jsonl", gold)
    batches = {name: [] for name in "abc"}
    for i, row in enumerate(blind):
        batches["abc"[i % 3]].append(row)
    for name, rows in batches.items():
        directory = ROOT / f"agent_{name}"
        directory.mkdir(exist_ok=True)
        write(directory / "input.jsonl", rows)
    summary = {"seed": SEED, "generated": 1484, "correct": sum(v for (key, stage), v in counts.items() if stage == "correct"),
               "part_candidates": len(blind), "batches": {name: len(rows) for name, rows in batches.items()},
               "by_type": {"/".join(key): len(rows) for key, rows in groups.items()}}
    (ROOT / "candidate_screen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
