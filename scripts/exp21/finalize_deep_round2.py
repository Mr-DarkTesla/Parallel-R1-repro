"""Finalize the independently reviewed Sol 6.1 inside-thinking dataset.

Usage: python -B scripts/exp21/finalize_deep_round2.py
All inputs and outputs live under results/21-qwen3-0.6b-multiverse/audit/deep_trace_round2.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checks import check  # noqa: E402
from mv_format import parse  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/audit/deep_trace_round2"
EXCLUDED = {"math-train/6780"}  # source solution is valid, pool gold omits k=12


def read(name):
    return [json.loads(line) for line in (DATA / name).open()]


def write(name, rows):
    (DATA / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def main():
    gold = {r["id"]: r for r in read("selected52_with_gold.jsonl")}
    source = {r["id"]: r for batch in "abc" for r in read(f"traces52_{batch}.jsonl")}
    tagged = [r for batch in "abc" for r in read(f"tagged52_{batch}.jsonl")]
    reviews = {r["id"]: r for batch in "abc" for r in read(f"tagged52_{batch}_review.jsonl")}
    assert len(gold) == len(source) == 52
    assert len(tagged) == len(reviews) == 51
    assert set(gold) - {r["id"] for r in tagged} == EXCLUDED
    assert set(reviews) == {r["id"] for r in tagged}

    audit = []
    accepted = []
    with_gold = []
    for row in tagged:
        id_ = row["id"]
        original = source[id_]["response"]
        assert row["question"] == source[id_]["question"] == gold[id_]["question"]
        review = reviews[id_]
        assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
        assert review["independent_paths"] and review["source_preserved"]
        result = check(row["response"], gold[id_]["answer"], "math", original)
        assert result["ok"], (id_, result["issues"])
        structure = parse(row["response"])
        assert len(structure["blocks"]) == 1
        block = structure["blocks"][0]
        think_end = row["response"].index("</think>")
        assert 0 < block["start"] < block["end"] < think_end
        assert min(len(re.sub(r"^\s*\d+\s*:", "", p).strip()) for p in block["paths"]) >= 80
        assert all(len(re.sub(r"^\s*\d+\s*:", "", o).strip()) >= 10 for o in block["outlines"])
        audit.append({"id": id_, "checks": result, "review": review})
        accepted.append({"id": id_, "question": row["question"], "response": row["response"],
                         "source": "sol6.1_deep_round2", "gold_answer": gold[id_]["answer"]})
        with_gold.append({"id": id_, "question": row["question"], "answer": gold[id_]["answer"]})

    write("accepted51.jsonl", accepted)
    write("accepted51_with_gold.jsonl", with_gold)
    write("accepted51_audit.jsonl", audit)
    summary = {"selected": 52, "excluded_bad_pool_gold": sorted(EXCLUDED), "accepted": len(accepted),
               "independent_review_useful": len(accepted), "wrong_answers": 0,
               "grammar_check_pass": len(accepted), "verbatim_check_pass": len(accepted),
               "inside_think": len(accepted)}
    summary["path_count"] = {str(n): sum(len(parse(r["response"])["blocks"][0]["paths"]) == n for r in accepted)
                             for n in (2, 3)}
    (DATA / "accepted51_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
