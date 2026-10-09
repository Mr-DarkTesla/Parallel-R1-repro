"""Audit the mixed M1 thinking SFT against its original rows and verified pairs.

Usage: python audit_thinking_sft.py ORIGINAL_PREFIX MIX_PREFIX M1_PAIRS OUT_JSON [TOKENIZER]
With TOKENIZER on the pod, also check math_verify and the 4096-token SFT limit.
"""
import collections
import json
import re
import sys

import pandas as pd

from make_thinking_m1 import convert
from mv_format import parse


def load(prefix, split):
    return pd.read_parquet(f"{prefix}_{split}.parquet").to_dict("records")


def key(row):
    info = row["extra_info"]
    return info["kind"], info["id"]


def main():
    original, mixed, pairs_path, output = sys.argv[1:5]
    tokenizer_path = sys.argv[5] if len(sys.argv) > 5 else None
    pairs = {row["id"]: row for row in (json.loads(line) for line in open(pairs_path))}
    if tokenizer_path:
        from transformers import AutoTokenizer
        from checks import candidate, correct, norm
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    old_splits = {split: load(original, split) for split in ("train", "val")}
    new_splits = {split: load(mixed, split) for split in ("train", "val")}
    assert not ({r["id"] for r in new_splits["train"]} & {r["id"] for r in new_splits["val"]})
    report = {"splits": {}, "answer_verified": 0 if tokenizer_path else None,
              "percentage_contextual": [], "max_tokens": 0 if tokenizer_path else None}
    checked = set()
    for split in ("train", "val"):
        old, new = old_splits[split], new_splits[split]
        assert len(old) == len(new), split
        assert {r["id"] for r in old} == {r["id"] for r in new}, split
        before = collections.defaultdict(list)
        after = collections.defaultdict(list)
        for row in old:
            before[key(row)].append(row["extra_info"])
        for row in new:
            after[key(row)].append(row["extra_info"])
        for (kind, problem_id), values in before.items():
            if kind == "parallel":
                assert len(values) == 3 and len(after[("parallel", problem_id)]) == 2
                thinking = after[("parallel_th", problem_id)]
                assert len(thinking) == 1 and problem_id in pairs
                reference = values[0]
                assert all(x == reference for x in values)
                assert all(x == reference for x in after[("parallel", problem_id)])
                expected = convert(pairs[problem_id])["response"]
                actual = thinking[0]
                assert actual["question"] == reference["question"] and actual["enable_thinking"] is True
                assert actual["answer"] == expected
                thought, final = actual["answer"].split("</think>\n", 1)
                thought = thought.removeprefix("<think>\n")
                parsed = parse(thought)
                assert parsed["valid"] and all(block["numbered"] for block in parsed["blocks"])
                assert parse(final)["tags"] == 0 and final.startswith("Final Answer:")
                if problem_id not in checked:
                    checked.add(problem_id)
                    if tokenizer_path:
                        answer = candidate(final)
                        gold = pairs[problem_id]["answer"]
                        direct = correct(gold, answer, pairs[problem_id]["source"])
                        contextual_percent = (gold.endswith(r"\%") and norm(gold[:-2]) == norm(answer)
                                              and "percent" in pairs[problem_id]["question"].lower())
                        assert direct or contextual_percent, (problem_id, gold, answer)
                        if contextual_percent and not direct:
                            report["percentage_contextual"].append(problem_id)
                        report["answer_verified"] += 1
            else:
                assert sorted(values, key=str) == sorted(after[(kind, problem_id)], key=str), (split, kind, problem_id)
        expected = set(before) | {("parallel_th", problem_id) for kind, problem_id in before if kind == "parallel"}
        assert set(after) == expected
        if tokenizer_path:
            for row in new:
                info = row["extra_info"]
                prompt = tokenizer.apply_chat_template([{"role": "user", "content": info["question"]}],
                                                       add_generation_prompt=True, tokenize=False,
                                                       enable_thinking=info["enable_thinking"])
                length = len(tokenizer.encode(prompt + info["answer"] + tokenizer.eos_token,
                                              add_special_tokens=False))
                assert length <= 4096, (split, info["id"], length)
                report["max_tokens"] = max(report["max_tokens"], length)
        report["splits"][split] = {"rows": len(new), "problems": len({r["id"] for r in new}),
                                    "kinds": dict(collections.Counter(r["extra_info"]["kind"] for r in new))}
    assert checked == set(pairs)
    with open(output, "w") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
