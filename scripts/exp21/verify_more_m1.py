"""Final automatic gate for 180 new M1 examples and disjoint manual reviews.

Usage: python verify_more_m1.py SELECTED AUDIT POOL OLD_M1 OLD_M2 SELF20 INDEP30 TOKENIZER OUT
"""
import collections
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

from checks import check
from select_pair import token_lengths


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    selected_path, audit_path, pool_path, old_m1, old_m2, self20, independent30, tokenizer_path, output = sys.argv[1:10]
    rows = read(selected_path)
    assert len(rows) == 180 and len({r["id"] for r in rows}) == len(rows)
    selected = {r["id"] for r in rows}
    old = {r["id"] for path in (old_m1, old_m2) for r in read(path)}
    assert not selected & old
    pool = {r["id"]: r for r in read(pool_path)}
    audits = {r["id"]: r for r in read(audit_path)}
    samples = [{r["id"] for r in read(path)} for path in (self20, independent30)]
    assert len(samples[0]) == 20 and len(samples[1]) == 30
    assert samples[0] <= selected and samples[1] <= selected and not samples[0] & samples[1]
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    max_prompt, max_response, max_total = 0, 0, 0
    groups = collections.Counter()
    for row in rows:
        source = pool[row["id"]]
        assert all(source[k] == row[k] for k in ("source", "question", "answer", "answer_type")), row["id"]
        verdict = audits[row["id"]]
        assert verdict["status"] == "clean" and all(verdict[k] == row[k]
            for k in ("question", "answer", "response")), row["id"]
        result = check(row["response"], row["answer"], row["source"])
        assert result["ok"] and result["blocks"] >= 1, row["id"]
        prompt_len, response_len = token_lengths(tokenizer, row)
        assert response_len <= 2048 and prompt_len + response_len <= 4096, row["id"]
        max_prompt, max_response, max_total = max(max_prompt, prompt_len), max(max_response, response_len), max(max_total, prompt_len + response_len)
        groups[f"{row['source']}/{row['answer_type']}"] += 1
    report = {"selected": len(rows), "from_leak_checked_pool": True,
              "disjoint_from_original_M1_and_M2": True, "automatic_check_passed": len(rows),
              "auditor_clean": len(rows), "review_self": len(samples[0]), "review_independent": len(samples[1]),
              "distribution": dict(groups), "max_tokens": {"prompt": max_prompt,
              "response": max_response, "total": max_total}}
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
