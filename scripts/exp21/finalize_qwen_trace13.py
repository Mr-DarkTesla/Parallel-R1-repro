"""Finalize strict plan-only tags on Qwen3-0.6B's own correct thinking traces."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checks import check  # noqa: E402
from mv_format import parse  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/21-qwen3-0.6b-multiverse"
AUDIT = BASE / "audit/qwen_trace_screen"
WEAK_MATH_TEST_OVERLAP = {"math-train/840"}


def read(path):
    return [json.loads(line) for line in path.open()]


def write(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def main():
    pool = {r["id"]: r for r in read(BASE / "data/pool.jsonl")}
    original = {r["id"]: r for batch in "abc" for r in read(AUDIT / f"batch_{batch}.jsonl")}
    tagged = [r for batch in "abc" for r in read(AUDIT / f"tagged_{batch}.jsonl") if r["status"] == "tagged"]
    review = {r["id"]: r for batch in "abc" for r in read(AUDIT / f"tagged_{batch}_review.jsonl")}
    assert len(original) == 213 and len(tagged) == len(review) == 14
    assert len({r["id"] for r in tagged}) == 14 and set(review) == {r["id"] for r in tagged}
    results = []
    accepted = []
    with_gold = []
    for r in tagged:
        id_, source = r["id"], r["id"].split("-")[0]
        assert r["question"] == original[id_]["question"] == pool[id_]["question"]
        audit = review[id_]
        assert audit["verdict"] == "useful"
        assert all(audit[k] for k in ("answer_correct", "reasoning_correct", "independent_paths", "source_preserved"))
        checked = check(r["response"], pool[id_]["answer"], source, original[id_]["response"])
        assert checked["ok"], (id_, checked["issues"])
        block = parse(r["response"])["blocks"][0]
        assert len(parse(r["response"])["blocks"]) == 1
        assert 0 < block["start"] < block["end"] < r["response"].index("</think>")
        results.append({"id": id_, "checks": checked, "review": audit})
        if id_ not in WEAK_MATH_TEST_OVERLAP:
            accepted.append({"id": id_, "question": r["question"], "response": r["response"],
                             "source": source, "answer": pool[id_]["answer"]})
            with_gold.append({"id": id_, "question": r["question"], "answer": pool[id_]["answer"]})
    assert len(accepted) == 13
    write(AUDIT / "accepted13.jsonl", accepted)
    write(AUDIT / "accepted13_with_gold.jsonl", with_gold)
    write(AUDIT / "reviewed14_audit.jsonl", results)
    summary = {"screened": len(original), "structurally_suitable": 16, "tagged_and_independently_reviewed": 14,
               "weak_math_test_overlap_excluded": sorted(WEAK_MATH_TEST_OVERLAP), "accepted_for_dataset": 13,
               "screening_false_positives": ["math-train/1283", "math-train/4511"],
               "answer_and_reasoning_correct": 14, "checks_pass": 14}
    (AUDIT / "accepted13_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
