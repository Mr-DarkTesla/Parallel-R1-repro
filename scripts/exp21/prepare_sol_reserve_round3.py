"""Assemble the reviewed plan-only Sol traces; no training starts here."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checks import XREF, candidate, correct, stated_before  # noqa: E402
from mv_format import ANY_TAG, parse  # noqa: E402

ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/sol_reserve_round3"
EXCLUDE_CONCLUSION = {"math-train/1145", "math-train/1179", "math-train/3483", "math-train/816"}


def read(path):
    return [json.loads(line) for line in path.open()]


def write(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def source_text(tagged):
    result = re.sub(r"<Goal>.*?</Goal>", "", tagged, flags=re.S)
    result = re.sub(r"<Path>\s*\d+\s*:\s*", "", result)
    return ANY_TAG.sub("", result)


def main():
    gold = {r["id"]: r for r in read(ROOT / "clean_with_gold.jsonl")}
    originals = {r["id"]: r for name in "abc" for r in read(ROOT / f"agent_{name}/traces.jsonl")}
    reviews = {r["id"]: r for path in (ROOT / "review_a_root.jsonl",
                 ROOT / "agent_c/review_b.jsonl", ROOT / "agent_b/review_c.jsonl") for r in read(path)}
    tagged = {r["id"]: r for path in (ROOT / "tagged_a_root.jsonl",
                ROOT / "agent_a/tagged_bc.jsonl") for r in read(path)}
    assert len(gold) == 97 and len(originals) == len(reviews) == 52 and len(tagged) == 41
    selected, audit, with_gold = [], [], []
    for id_, review in reviews.items():
        if review["verdict"] != "accept" or id_ in EXCLUDE_CONCLUSION:
            continue
        row, orig, g = tagged[id_], originals[id_], gold[id_]
        assert row["question"] == orig["question"] == g["question"]
        t = row["response"]
        structure = parse(t)
        assert structure["valid"] and len(structure["blocks"]) == 1, id_
        block = structure["blocks"][0]
        assert block["numbered"] and len(block["paths"]) == len(block["outlines"]) == 2, id_
        assert t.startswith("<think>") and block["end"] <= t.index("</think>"), id_
        assert "Final Answer:" in t[block["end"]:], id_
        assert not stated_before(t[:block["start"]], g["answer"]), id_
        recovered = source_text(t)
        assert re.sub(r"\s+", "", recovered) == re.sub(r"\s+", "", orig["response"]), id_
        numbers = lambda s: sorted(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", s))  # noqa: E731
        assert numbers(recovered) == numbers(orig["response"]), id_
        assert all(len(re.sub(r"^\s*\d+\s*:", "", p).strip()) >= 40 for p in block["paths"]), id_
        assert all(len(re.sub(r"^\s*\d+\s*:", "", o).strip()) >= 10 for o in block["outlines"]), id_
        assert all(not XREF.search(re.sub(r"^\s*\d+\s*:\s*Part\s+\d+\s*:\s*", "", p))
                   for p in block["paths"]), id_
        assert re.search(r"\d|\\(?:frac|sqrt|pi)", block["conclusion"]), id_
        answer = candidate(t.split("</think>", 1)[1])
        answer_ok = correct(g["answer"], answer, g["source"])
        if id_ == "math-train/5755":
            answer_ok = answer == "pi/4" and g["answer"] == r"\frac{\pi}{4}"  # independent review confirmed equivalence
        assert answer_ok, (id_, g["answer"], answer)
        selected.append({"id": id_, "question": row["question"], "response": t,
                         "source": g["source"], "answer_type": g["answer_type"], "gold_answer": g["answer"]})
        with_gold.append({"id": id_, "question": row["question"], "answer": g["answer"]})
        audit.append({"id": id_, "author_batch": id_ in {x["id"] for x in read(ROOT / "agent_a/traces.jsonl")} and "a" or "b_or_c",
                      "review": review, "paths_chars": [len(p.strip()) for p in block["paths"]],
                      "conclusion": block["conclusion"].strip(), "answer_correct": True,
                      "grammar": True, "inside_think": True, "source_preserved": True})
    assert len(selected) == 30 and len({r["id"] for r in selected}) == 30
    write(ROOT / "candidate30.jsonl", selected)
    write(ROOT / "candidate30_with_gold.jsonl", with_gold)
    write(ROOT / "candidate30_audit.jsonl", audit)
    independently_tag_reviewed = {r["id"] for path in (ROOT / "agent_c/review_b.jsonl",
                                  ROOT / "agent_b/review_c.jsonl") for r in read(path) if r["verdict"] == "accept"}
    accepted = [r for r in selected if r["id"] in independently_tag_reviewed]
    assert len(accepted) == 19
    write(ROOT / "accepted19.jsonl", accepted)
    write(ROOT / "accepted19_with_gold.jsonl", [r for r in with_gold if r["id"] in independently_tag_reviewed])
    write(ROOT / "accepted19_audit.jsonl", [r for r in audit if r["id"] in independently_tag_reviewed])
    (ROOT / "candidate30_summary.json").write_text(json.dumps({"reviewed_source_traces": 52,
        "independent_review_accepted_before_semantic_conclusion_gate": 34,
        "excluded_procedural_or_vague_conclusion": sorted(EXCLUDE_CONCLUSION),
        "candidate": len(selected), "independently_tag_reviewed_for_sft": len(accepted),
        "root_tagged_a_pending_external_review": 11, "wrong_final_answers": 0,
        "grammar_valid": len(selected), "inside_think": len(selected), "source_preserved": len(selected)}, indent=2) + "\n")
    print(len(selected))


if __name__ == "__main__":
    main()
