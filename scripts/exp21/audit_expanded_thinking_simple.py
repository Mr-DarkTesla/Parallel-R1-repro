"""Required simple format gate for wrapped M1/M2 before training."""
import json
from pathlib import Path

from mv_format import parse


DATA = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/data"
report = {}
for method in ("m1", "m2"):
    path = DATA / f"pair_expanded_{method}_thinking.jsonl"
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({r["id"] for r in rows}) == 367
    for row in rows:
        response = row["response"]
        assert response.startswith("<think>\n") and response.count("</think>") == 1, row["id"]
        inside, outside = response.split("</think>", 1)
        block = parse(inside)
        assert block["valid"] and len(block["blocks"]) == 1, row["id"]
        assert block["blocks"][0]["numbered"], row["id"]
        assert parse(outside)["tags"] == 0 and outside.strip(), row["id"]
    report[method] = {"rows": len(rows), "valid_numbered_inside_think": len(rows),
                      "tags_outside_think": 0}
(DATA / "pair_expanded_thinking_simple_audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
