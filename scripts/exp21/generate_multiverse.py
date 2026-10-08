"""Evaluate Multiverse with independently generated sibling paths.

The SFT mask hides earlier sibling paths from later ones. Ordinary left-to-right
generation therefore gives the second <Path> opener a context that it never had
during training. This rollout stops at the first <Path>, generates each numbered
path from the same Goal prefix, then resumes after joining the paths. Its saved
dump has the same columns as scripts/instruct4b_eval/generate.py.

Usage: python generate_multiverse.py <model> <test.parquet> <output.jsonl> <max_tokens>
"""
import json
import re
import sys

import pandas as pd
from vllm import LLM, SamplingParams


def path_count(prefix):
    goal = re.search(r"<Goal>(.*?)</Goal>\s*$", prefix, re.S)
    if not goal:
        return 0
    outlines = re.findall(r"<Outline>\s*(\d+)\s*:(.*?)</Outline>", goal.group(1), re.S)
    if len(outlines) < 2 or len(outlines) > 4:
        return 0
    if [int(x[0]) for x in outlines] != list(range(1, len(outlines) + 1)):
        return 0
    return len(outlines)


def params(max_tokens, seed, stop=None):
    return SamplingParams(temperature=1.0, top_p=1.0, max_tokens=max(1, max_tokens),
                          skip_special_tokens=False, seed=int(seed), stop_token_ids=stop or [])


def main():
    model, test_path, output_path, budget = sys.argv[1:5]
    budget = int(budget)
    test = pd.read_parquet(test_path)
    llm = LLM(model, dtype="bfloat16", max_model_len=budget + 2048, gpu_memory_utilization=0.85, seed=0)
    tok = llm.get_tokenizer()
    ids = {tag: tok.convert_tokens_to_ids(tag) for tag in ("<Path>", "</Path>")}
    assert all(tok.encode(tag, add_special_tokens=False) == [idx] for tag, idx in ids.items()), ids
    prompts = [tok.apply_chat_template(list(p), add_generation_prompt=True, tokenize=False, enable_thinking=False)
               for p in test["prompt"]]
    seeds = pd.Series(prompts).groupby(prompts).cumcount()
    first = llm.generate(prompts, [params(budget, s, [ids["<Path>"]]) for s in seeds])
    records = []
    branches = []
    for i, (prompt, output, seed) in enumerate(zip(prompts, first, seeds)):
        item = output.outputs[0]
        prefix = item.text
        stopped = item.stop_reason == ids["<Path>"]
        count = path_count(prefix) if stopped else 0
        records.append({"input": prompt, "prefix": prefix, "prefix_tokens": len(item.token_ids),
                        "seed": int(seed), "count": count, "first_stopped": stopped,
                        "first_finish": item.finish_reason})
        if count:
            for k in range(1, count + 1):
                start = prefix + "<Path>\n" + f"{k}: "
                branches.append((i, k, prompt + start, start))
    if branches:
        generated = llm.generate([x[2] for x in branches],
                                 [params(budget, int(seeds[i]) * 100 + k, [ids["</Path>"]])
                                  for i, k, _, _ in branches])
        for (i, k, _, start), output in zip(branches, generated):
            item = output.outputs[0]
            stopped = item.stop_reason == ids["</Path>"]
            segment = "<Path>\n" + f"{k}: " + item.text + ("</Path>\n" if stopped else "")
            records[i].setdefault("paths", []).append(segment)
            records[i].setdefault("path_tokens", []).append(len(item.token_ids) + len(tok.encode(segment, add_special_tokens=False))
                                                             - len(tok.encode(item.text, add_special_tokens=False)))
            records[i].setdefault("path_closed", []).append(stopped)
    suffix_jobs = []
    for i, rec in enumerate(records):
        if rec["count"] and all(rec.get("path_closed", [])):
            joined = rec["prefix"] + "".join(rec["paths"])
            remaining = budget - len(tok.encode(joined, add_special_tokens=False))
            if remaining > 0:
                suffix_jobs.append((i, rec["input"] + joined, remaining))
    if suffix_jobs:
        generated = llm.generate([x[1] for x in suffix_jobs],
                                 [params(n, int(seeds[i]) * 100 + 99) for i, _, n in suffix_jobs])
        for (i, _, _), output in zip(suffix_jobs, generated):
            item = output.outputs[0]
            records[i]["suffix"] = item.text
            records[i]["suffix_tokens"] = len(item.token_ids)
            records[i]["suffix_finish"] = item.finish_reason
    fallback_jobs = []
    for i, rec in enumerate(records):
        if rec["first_stopped"] and not rec["count"]:
            partial = rec["prefix"] + "<Path>"
            remaining = budget - len(tok.encode(partial, add_special_tokens=False))
            if remaining > 0:
                fallback_jobs.append((i, rec["input"] + partial, remaining))
    if fallback_jobs:
        generated = llm.generate([x[1] for x in fallback_jobs],
                                 [params(n, int(seeds[i]) * 100 + 99) for i, _, n in fallback_jobs])
        for (i, _, _), output in zip(fallback_jobs, generated):
            item = output.outputs[0]
            records[i]["fallback"] = item.text
            records[i]["fallback_tokens"] = len(item.token_ids)
            records[i]["fallback_finish"] = item.finish_reason
    with open(output_path, "w") as f:
        for rec in records:
            complete = rec["count"] and all(rec.get("path_closed", [])) and "suffix" in rec
            if complete:
                response = rec["prefix"] + "".join(rec["paths"]) + rec["suffix"]
                tokens = rec["prefix_tokens"] + sum(rec["path_tokens"]) + rec["suffix_tokens"]
            elif rec["count"]:
                response = rec["prefix"] + "".join(rec.get("paths", []))
                tokens = rec["prefix_tokens"] + sum(rec.get("path_tokens", []))
            elif "fallback" in rec:
                response = rec["prefix"] + "<Path>" + rec["fallback"]
                tokens = rec["prefix_tokens"] + 1 + rec["fallback_tokens"]
            else:
                response, tokens = rec["prefix"], rec["prefix_tokens"]
            truncated = (rec["first_finish"] == "length" or
                         any(not closed for closed in rec.get("path_closed", [])) or
                         (rec["count"] > 0 and not complete) or
                         (rec["first_stopped"] and rec["count"] == 0 and "fallback" not in rec) or
                         (complete and rec["suffix_finish"] == "length") or
                         rec.get("fallback_finish") == "length")
            f.write(json.dumps({"input": rec["input"], "output": response, "tokens": tokens,
                                "truncated": bool(truncated), "seed": rec["seed"],
                                "rollout": {"independent_paths": rec["count"] if complete else 0,
                                            "path_closed": rec.get("path_closed", []),
                                            "first_finish": rec["first_finish"],
                                            "suffix_finish": rec.get("suffix_finish")}}) + "\n")


if __name__ == "__main__":
    main()
