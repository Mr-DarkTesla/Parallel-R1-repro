"""Keep new M2 examples that passed automatic and human review."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "results/21-qwen3-0.6b-multiverse/data"
EXCLUDED = {
    "gsm8k-train/6086": "first path is irrelevant to the requested result",
    "math-train/7045": "invalid intermediate vector expression",
    "math-train/1905": "final fraction is not reduced",
    "math-train/2079": "final fraction is not reduced",
    "math-train/2513": "final fraction is not reduced",
}


def main() -> None:
    source = DIR / "more_m2_existing_clean32.jsonl"
    rows = [json.loads(line) for line in source.read_text().splitlines() if line]
    ids = [row["id"] for row in rows]
    assert len(rows) == 32 and len(set(ids)) == 32
    assert set(EXCLUDED) <= set(ids)
    selected = [row for row in rows if row["id"] not in EXCLUDED]
    assert len(selected) == 27
    output = DIR / "more_m2_existing_reviewed27.jsonl"
    output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in selected))
    stats = {
        "source_automatic_clean": len(rows),
        "reviewed_all_independently": len(rows),
        "retained": len(selected),
        "excluded": EXCLUDED,
        "distribution": dict(sorted(Counter(f"{r['source']}/{r['answer_type']}" for r in selected).items())),
    }
    (DIR / "more_m2_existing_reviewed27_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
