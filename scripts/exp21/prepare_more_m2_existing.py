"""Recover unused, automatically valid M2 plans from already paid proxy calls.

Usage: python prepare_more_m2_existing.py POOL M2 GRADED_NT OLD_M1 OLD_M2 TOKENIZER OUT_JSONL
Rechecks the verbatim Qwen text, answer and token lengths; one sample per new task.
"""
import collections
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

from checks import candidate, check, correct
from mv_format import forward_passes, parse
from select_pair import token_lengths


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    pool_path, m2_path, graded_path, old_m1, old_m2, tokenizer_path, output = sys.argv[1:8]
    pool = {r["id"]: r for r in read(pool_path)}
    excluded = {r["id"] for path in (old_m1, old_m2) for r in read(path)}
    original = {(r["id"], r["sample"]): r["output"] for r in read(graded_path) if r["correct"]}
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    choices, counts = {}, collections.Counter()
    for row in read(m2_path):
        problem_id = row["id"]
        if problem_id in excluded or row["status"] != "ok":
            continue
        source = pool[problem_id]
        before = original.get((problem_id, row["sample"]))
        if before is None:
            counts["missing_correct_qwen_original"] += 1
            continue
        checked = check(row["response"], source["answer"], source["source"], original=before)
        if checked["issues"] == ["wrong_answer"] and "percent" in source["question"].lower():
            after = row["response"][parse(row["response"])["blocks"][-1]["end"]:]
            answer = candidate(after)
            if answer.endswith("%") and correct(source["answer"], answer[:-1], source["source"]):
                checked["issues"], checked["ok"] = [], True
                counts["percent_notation_accepted"] += 1
        if not checked["ok"]:
            counts["failed_recheck"] += 1
            continue
        selected = {**source, "response": row["response"], "method": "m2", "sample": row["sample"]}
        prompt_len, response_len = token_lengths(tokenizer, selected)
        if response_len > 2048 or prompt_len + response_len > 4096:
            counts["too_long"] += 1
            continue
        passes = forward_passes(row["response"], lambda s: len(tokenizer.encode(s, add_special_tokens=False)))
        selected.update(prompt_tokens=prompt_len, response_tokens=response_len,
                        forward_passes=passes, saved_passes=response_len - passes)
        previous = choices.get(problem_id)
        if previous is None or selected["saved_passes"] > previous["saved_passes"]:
            choices[problem_id] = selected
        counts["accepted_samples"] += 1
    out = Path(output)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(choices.values(), key=lambda x: x["id"])))
    out.with_name(out.stem + "_stats.json").write_text(json.dumps({"candidates": len(choices),
        "counts": dict(counts)}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"candidates": len(choices), "counts": dict(counts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
