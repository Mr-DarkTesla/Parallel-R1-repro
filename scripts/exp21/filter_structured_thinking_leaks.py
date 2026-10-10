"""Exclude every full-MATH-test leak, strong hit, and close stem match."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking"


def rows(name):
    return (json.loads(line) for line in (ROOT / name).open())


bad = {r["id"] for r in rows("leakcheck_inputs1500.hits.jsonl")
       if any(h["eval_set"] == "math_test_full(info)" and
              (h["leak"] or h.get("strong") or h.get("jac", 0) >= 0.6) for h in r["hits"])}
all_rows = list(rows("inputs1500_with_gold.jsonl"))
with (ROOT / "inputs_clean_with_gold.jsonl").open("w") as file:
    for row in all_rows:
        if row["id"] not in bad:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
(ROOT / "excluded_math_test.json").write_text(json.dumps({"count": len(bad), "ids": sorted(bad)}, indent=2) + "\n")
assert len(all_rows) == 1500 and len(bad) == 16
print(f"selected {len(all_rows) - len(bad)}; excluded {len(bad)}")
