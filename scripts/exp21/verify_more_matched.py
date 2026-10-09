"""Recheck matched M1/M2 additions against pool, original Qwen text, and SFT limits.

Usage: python verify_more_matched.py RESULTS_DIR LOCAL_DATA_DIR TOKENIZER_DIR
"""
import collections
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

from checks import candidate, check, correct
from mv_format import parse
from select_pair import token_lengths


def read(path):
    return [json.loads(line) for line in path.open()]


def checked_response(row, original=None):
    result = check(row["response"], row["answer"], row["source"], original=original)
    if result["issues"] == ["wrong_answer"] and "percent" in row["question"].lower():
        after = row["response"][parse(row["response"])["blocks"][-1]["end"]:]
        answer = candidate(after)
        if answer.endswith("%") and correct(row["answer"], answer[:-1], row["source"]):
            result["issues"], result["ok"] = [], True
    return result


def main(root, local, tokenizer_dir):
    data, audit = root / "data", root / "audit"
    m1, m2 = (read(data / f"more_{name}_matched180.jsonl") for name in ("m1", "m2"))
    assert len(m1) == len(m2) == 180
    assert len({r["id"] for r in m1 + m2}) == 360
    pool = {r["id"]: r for r in read(local / "pool.jsonl")}
    old = {r["id"] for name in ("pair_final_m1.jsonl", "pair_audited_m2.jsonl")
           for r in read(local / name)}
    assert not old & {r["id"] for r in m1 + m2}
    originals = {(r["id"], r["sample"]): r["output"] for r in read(local / "graded_nt.jsonl") if r["correct"]}
    m1_audit = {r["id"]: r for r in read(audit / "more_m1_reasoning_judge.jsonl")}
    m2_audit = {r["id"]: r for r in read(audit / "more_m2_new_2000_reasoning_judge.jsonl")}
    existing = {r["id"] for r in read(data / "more_m2_existing_reviewed27.jsonl")}
    excluded = set(json.loads((audit / "more_m2_new_human_exclusions.json").read_text()))
    excluded |= set(json.loads((audit / "more_m1_matched_human_exclusions.json").read_text()))
    excluded |= set(json.loads((audit / "more_m2_matched_self_exclusions.json").read_text()))
    assert not excluded & {r["id"] for r in m1 + m2}
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    report = {}
    for name, rows in (("m1", m1), ("m2", m2)):
        groups = collections.Counter()
        max_prompt = max_response = max_total = 0
        for row in rows:
            source = pool[row["id"]]
            assert all(source[k] == row[k] for k in ("question", "answer", "source", "answer_type")), row["id"]
            verdict = (m1_audit if name == "m1" else m2_audit).get(row["id"])
            if name == "m1" or row["id"] not in existing:
                assert verdict and verdict["status"] == "clean", row["id"]
                assert all(verdict[k] == row[k] for k in ("question", "answer", "response")), row["id"]
            original = originals.get((row["id"], row["sample"])) if name == "m2" else None
            if name == "m2":
                assert original is not None, row["id"]
            checked = checked_response(row, original)
            assert checked["ok"] and checked["blocks"] >= 1, (row["id"], checked["issues"])
            prompt_len, response_len = token_lengths(tokenizer, row)
            assert response_len <= 2048 and prompt_len + response_len <= 4096, row["id"]
            assert (prompt_len, response_len) == (row["prompt_tokens"], row["response_tokens"]), row["id"]
            max_prompt = max(max_prompt, prompt_len)
            max_response = max(max_response, response_len)
            max_total = max(max_total, prompt_len + response_len)
            groups[f"{row['source']}/{row['answer_type']}"] += 1
        report[name] = {"selected": len(rows), "distribution": dict(groups),
                        "max_tokens": {"prompt": max_prompt, "response": max_response, "total": max_total},
                        "verbatim_qwen_checked": len(rows) if name == "m2" else 0}
    assert report["m1"]["distribution"] == report["m2"]["distribution"]
    self_ids = {r["id"] for r in read(audit / "more_m1_matched180_self20.jsonl")}
    reviewer_ids = {r["id"] for r in read(audit / "more_m1_matched180_review30.jsonl")}
    assert len(self_ids) == 20 and len(reviewer_ids) == 30 and not self_ids & reviewer_ids
    assert self_ids | reviewer_ids <= {r["id"] for r in m1}
    m2_self_ids = {r["id"] for r in read(audit / "more_m2_matched180_self20.jsonl")}
    assert len(m2_self_ids) == 20 and m2_self_ids <= {r["id"] for r in m2}
    report["checks"] = {"pool_membership": 360, "no_old_or_cross_method_id": True,
                        "grammar_answer_independence_length": 360, "m1_self_review": 20,
                        "m1_independent_review": 30, "m2_self_review": 20,
                        "m2_human_reviewed": 180}
    (audit / "more_matched180_verify.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main(*(Path(arg) for arg in sys.argv[1:4]))
