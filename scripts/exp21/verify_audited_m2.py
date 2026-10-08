"""Recheck the audited M2 training set on a host with math_verify and the Qwen tokenizer."""
import argparse
import json

from transformers import AutoTokenizer

from checks import candidate, check, correct
from mv_format import parse
from select_pair import token_lengths


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    ap = argparse.ArgumentParser()
    for name in ("selected", "graded_nt", "tokenizer", "output"):
        ap.add_argument(name)
    args = ap.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    # Keep the original even if the grader rejected a percent sign around an
    # otherwise correct answer; the explicit normalization below checks it.
    graded = {(r["id"], r["sample"]): r["output"] for r in read(args.graded_nt)}
    rows = read(args.selected)
    assert len(rows) == len({r["id"] for r in rows})
    issues = []
    length_max = {"response": 0, "total": 0}
    verbatim_checked = 0
    percent_notation_accepted = []
    for row in rows:
        if "sample" not in row:
            issues.append([row["id"], "missing_sample"])
            continue
        original = graded.get((row["id"], row["sample"]))
        verbatim_checked += 1
        if original is None:
            issues.append([row["id"], "missing_original"])
            continue
        checked = check(row["response"], row["answer"], row["source"], original=original)
        if checked["issues"] == ["wrong_answer"] and "percent" in row["question"].lower():
            blocks = parse(row["response"])["blocks"]
            answer = candidate(row["response"][blocks[-1]["end"]:])
            if answer.endswith("%") and correct(row["answer"], answer[:-1], row["source"]):
                checked["issues"] = []
                checked["ok"] = True
                percent_notation_accepted.append(row["id"])
        if not checked["ok"]:
            issues.append([row["id"], checked["issues"]])
        prompt_tokens, response_tokens = token_lengths(tokenizer, row)
        length_max["response"] = max(length_max["response"], response_tokens)
        length_max["total"] = max(length_max["total"], prompt_tokens + response_tokens)
        if response_tokens > 2048 or prompt_tokens + response_tokens > 4096:
            issues.append([row["id"], "length"])
    result = {"rows": len(rows), "verbatim_checked": verbatim_checked,
              "percent_notation_accepted": percent_notation_accepted, "max_tokens": length_max,
              "issues": issues, "ok": not issues}
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    assert not issues


if __name__ == "__main__":
    main()
