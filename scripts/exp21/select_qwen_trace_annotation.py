"""Select new, correct Qwen thinking traces for independent tag-only annotation."""
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
SOURCE = ROOT / "audit/qwen_structured_thinking"
OUT = SOURCE / "annotation_round2"
COUNTS = {("gsm8k", "integer"): 90, ("math", "integer"): 54,
          ("math", "expression"): 24, ("math", "fraction"): 12}


def read(path):
    return [json.loads(line) for line in path.open()]


def main():
    old = {row["id"] for row in read(SOURCE / "candidates149_blind.jsonl")}
    selected = []
    rng = random.Random(20261010)
    graded = read(SOURCE / "graded.jsonl")
    for key, count in COUNTS.items():
        pool = [row for row in graded if row["correct"] and row["clean"]
                and row["id"] not in old and row["tokens"] <= 1400
                and (row["source"], row["answer_type"]) == key]
        rng.shuffle(pool)
        if len(pool) < count:
            raise ValueError((key, len(pool), count))
        selected.extend(pool[:count])
    rng.shuffle(selected)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for index, row in enumerate(selected):
        batch = index % 3
        manifest.append({"id": row["id"], "batch": batch,
                         "source": row["source"], "answer_type": row["answer_type"],
                         "gold": row["gold"]})
    for batch in range(3):
        with (OUT / f"inputs_{batch}.jsonl").open("w") as file:
            for index, row in enumerate(selected):
                if index % 3 == batch:
                    data = {"id": row["id"], "question": row["question"],
                            "response": row["output"], "source": row["source"],
                            "answer_type": row["answer_type"]}
                    file.write(json.dumps(data, ensure_ascii=False) + "\n")
    with (OUT / "manifest.jsonl").open("w") as file:
        for row in manifest:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    print({"selected": len(selected), "per_batch": 60, "seed": 20261010})


if __name__ == "__main__":
    main()
