"""Find new, verified M1 tasks that also have a correct Qwen answer for M2.

Usage: python prepare_more_m1.py POOL M1 GRADED_NT OLD_M1 OLD_M2 TOKENIZER OUT_JSONL
Only training data and the local tokenizer are used; no proxy calls or eval scores.
"""
import collections
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

from checks import check
from m2_convert import split_units
from mv_format import forward_passes
from select_pair import token_lengths


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    pool_path, m1_path, graded_path, old_m1, old_m2, tokenizer_path, output = sys.argv[1:8]
    pool = {row["id"]: row for row in read(pool_path)}
    excluded = {row["id"] for path in (old_m1, old_m2) for row in read(path)}
    qwen = collections.defaultdict(list)
    for row in read(graded_path):
        if (row["id"] in excluded or not row["correct"] or row["tokens"] > 2048
                or len(row["output"]) < 250 or len(split_units(row["output"])[0]) < 4):
            continue
        qwen[row["id"]].append(row["sample"])
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    candidates, counts = [], collections.Counter()
    for row in read(m1_path):
        problem_id = row["id"]
        if problem_id not in qwen or not row.get("response") or not (row.get("check") or {}).get("ok"):
            continue
        source = pool[problem_id]
        result = check(row["response"], source["answer"], source["source"])
        if not result["ok"]:
            counts["failed_recheck"] += 1
            continue
        candidate = {**source, "response": row["response"], "method": "m1"}
        prompt_len, response_len = token_lengths(tokenizer, candidate)
        if response_len > 2048 or prompt_len + response_len > 4096:
            counts["too_long"] += 1
            continue
        passes = forward_passes(row["response"], lambda s: len(tokenizer.encode(s, add_special_tokens=False)))
        candidate.update(prompt_tokens=prompt_len, response_tokens=response_len,
                         forward_passes=passes, saved_passes=response_len - passes,
                         qwen_samples=sorted(qwen[problem_id]))
        candidates.append(candidate)
        counts[f"{source['source']}/{source['answer_type']}"] += 1
    assert len(candidates) == len({r["id"] for r in candidates})
    out = Path(output)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(candidates, key=lambda x: x["id"])))
    out.with_name(out.stem + "_stats.json").write_text(json.dumps({"candidates": len(candidates),
        "old_ids_excluded": len(excluded), "counts": dict(counts)}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"candidates": len(candidates), "counts": dict(counts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
