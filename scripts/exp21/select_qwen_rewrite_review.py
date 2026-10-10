"""Fixed independent semantic-review sample: ten rows from each annotation worker."""
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/annotation_round2"


def main():
    rng = random.Random(20261011)
    rows = []
    for batch in range(3):
        group = [json.loads(line) for line in (ROOT / f"rewrite_agent_{batch}/tagged.jsonl").open()]
        assert len(group) == 60
        rng.shuffle(group)
        rows += group[:10]
    rng.shuffle(rows)
    for label, subset in (("a", rows[:15]), ("b", rows[15:])):
        with (ROOT / f"rewrite_review30_{label}.jsonl").open("w") as file:
            for row in subset:
                file.write(json.dumps(row, ensure_ascii=False) + "\n")
    print({"sample": len(rows), "per_worker": 10,
           "ids": [row["id"] for row in rows]})


if __name__ == "__main__":
    main()
