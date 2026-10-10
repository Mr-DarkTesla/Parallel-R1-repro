"""Add held-out gold answers to the existing Qwen thinking annotation batches."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/annotation_round2"


def read(path):
    return [json.loads(line) for line in path.open()]


def main():
    gold = {row["id"]: row["gold"] for row in read(ROOT / "manifest.jsonl")}
    for batch in range(3):
        rows = read(ROOT / f"inputs_{batch}.jsonl")
        assert len(rows) == 60
        with (ROOT / f"rewrite_inputs_{batch}.jsonl").open("w") as file:
            for row in rows:
                row["gold_answer"] = gold[row["id"]]
                file.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("rewrite batches: 3 x 60")


if __name__ == "__main__":
    main()
