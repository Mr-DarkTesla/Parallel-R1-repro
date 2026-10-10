"""Simple automatic gate for the corrected Qwen thinking annotation batches."""
import collections
import json
from pathlib import Path

from checks import candidate, correct
from mv_format import parse


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/annotation_round2"


def read(path):
    return [json.loads(line) for line in path.open()]


def main():
    manifest = {row["id"]: row for row in read(ROOT / "manifest.jsonl")}
    rows = []
    for batch in range(3):
        inp = {row["id"]: row for row in read(ROOT / f"rewrite_inputs_{batch}.jsonl")}
        decisions = read(ROOT / f"rewrite_agent_{batch}/decisions.jsonl")
        tagged = read(ROOT / f"rewrite_agent_{batch}/tagged.jsonl")
        assert len(inp) == len(decisions) == 60
        assert len({row["id"] for row in decisions}) == 60
        assert {row["id"] for row in decisions} == set(inp)
        assert {row["id"] for row in tagged} == {row["id"] for row in decisions if row["accept"]}
        for row in tagged:
            original = inp[row["id"]]
            assert row["question"] == original["question"], row["id"]
            assert row["source"] == original["source"], row["id"]
            assert row["answer_type"] == original["answer_type"], row["id"]
            assert row["gold_answer"] == original["gold_answer"] == manifest[row["id"]]["gold"], row["id"]
            response = row["response"]
            assert len(response) <= 8000, row["id"]
            assert response.startswith("<think>") and response.count("<think>") == response.count("</think>") == 1, row["id"]
            inside, outside = response.split("</think>", 1)
            block = parse(inside)
            assert block["valid"] and len(block["blocks"]) == 1 and block["blocks"][0]["numbered"], row["id"]
            assert len(block["blocks"][0]["paths"]) >= 2 and parse(outside)["tags"] == 0, row["id"]
            assert correct(row["gold_answer"], candidate(outside), row["source"]), row["id"]
            rows.append({"id": row["id"], "question": row["question"], "response": response,
                         "source": row["source"], "answer_type": row["answer_type"],
                         "answer": row["gold_answer"], "method": "qwen_thinking_rewrite"})
    assert len(rows) == len({row["id"] for row in rows})
    with (ROOT / "rewrite_audited.jsonl").open("w") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    report = {"inputs": 180, "accepted": len(rows), "rejected": 180 - len(rows),
              "valid_numbered_inside_think": len(rows), "correct_final_answer": len(rows),
              "tags_outside_think": 0,
              "source_answer_type": {f"{source}/{answer_type}": n for (source, answer_type), n
                                     in sorted(collections.Counter((r["source"], r["answer_type"]) for r in rows).items())}}
    (ROOT / "rewrite_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(report)


if __name__ == "__main__":
    main()
