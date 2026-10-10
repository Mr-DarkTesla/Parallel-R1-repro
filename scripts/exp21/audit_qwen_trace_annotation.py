"""Audit tag-only edits of correct Qwen thinking traces."""
import json
import re
from pathlib import Path

from mv_format import parse


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
BASE = ROOT / "audit/qwen_structured_thinking"
OUT = BASE / "annotation_round2"


def read(path):
    return [json.loads(line) for line in path.open()]


def restore(response):
    response = re.sub(r"<Goal>.*?</Goal>", "", response, flags=re.S)
    response = re.sub(r"<Path>\s*[1-9]\d*:\s*", "", response)
    response = re.sub(r"</?(?:Parallel|Path|Conclusion)>", "", response)
    return "".join(response.split())


def main():
    source = {row["id"]: row for row in read(BASE / "graded.jsonl")}
    inputs = {row["id"] for batch in range(3) for row in read(OUT / f"inputs_{batch}.jsonl")}
    records = []
    fixed = BASE / "fix_conclusion/tagged_fixed.jsonl"
    paths = [fixed] + [OUT / f"agent_{batch}/tagged.jsonl" for batch in range(3)]
    for path in paths:
        for row in read(path):
            original = source[row["id"]]
            assert original["correct"] and original["clean"], row["id"]
            if path != fixed:
                assert row["id"] in inputs, row["id"]
            answer = row["response"]
            assert answer.count("<think>") == answer.count("</think>") == 1, row["id"]
            inside, outside = answer.split("</think>", 1)
            parsed = parse(inside)
            assert parsed["valid"] and len(parsed["blocks"]) == 1, row["id"]
            assert parsed["blocks"][0]["numbered"], row["id"]
            assert parse(outside)["tags"] == 0, row["id"]
            assert restore(answer) == "".join(original["output"].split()), row["id"]
            records.append({"id": row["id"], "question": original["question"],
                            "response": answer, "source": original["source"],
                            "answer_type": original["answer_type"], "answer": original["gold"],
                            "method": "qwen_thinking_tag_only"})
    assert len(records) == len({row["id"] for row in records})
    with (OUT / "accepted_audited.jsonl").open("w") as file:
        for row in records:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {"audited_accepted": len(records), "old_fixed": len(read(fixed)),
               "new": len(records) - len(read(fixed)),
               "source_restored": len(records), "correct_original_final": len(records),
               "valid_numbered_block_inside_think": len(records), "tags_outside_think": 0}
    (OUT / "audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    verdict_path = OUT / "independent_review/verdicts.jsonl"
    if verdict_path.exists():
        verdicts = read(verdict_path)
        assert len(verdicts) == len(records)
        by_id = {row["id"]: row for row in verdicts}
        assert set(by_id) == {row["id"] for row in records}
        reviewed = [row for row in records if by_id[row["id"]]["accept"]]
        with (OUT / "accepted_reviewed.jsonl").open("w") as file:
            for row in reviewed:
                file.write(json.dumps(row, ensure_ascii=False) + "\n")
        summary["independent_review_accepted"] = len(reviewed)
        summary["independent_review_rejected"] = len(records) - len(reviewed)
        (OUT / "audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(summary)


if __name__ == "__main__":
    main()
