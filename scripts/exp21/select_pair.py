"""Select M1/M2 examples on identical problems after all quality and tokenizer-length checks.

Run on pod B, where the Qwen3-0.6B tokenizer already exists. Inputs are the pool, M1 and M2 output JSONL files and the graded
non-thinking generations (for M2's original text). Output <prefix>_{m1,m2}.jsonl and <prefix>_stats.json. A problem can appear
only once in each method. Selection uses no eval data or scores.
"""
import argparse
import collections
import json
import random

from transformers import AutoTokenizer

from build_sft import row
from checks import check
from mv_format import forward_passes


def read(path):
    return [json.loads(line) for line in open(path)]


def token_lengths(tok, candidate, kind="parallel"):
    prepared = row(kind, candidate)["extra_info"]
    prompt = tok.apply_chat_template([{"role": "user", "content": prepared["question"]}],
                                     add_generation_prompt=True, tokenize=False,
                                     enable_thinking=prepared["enable_thinking"])
    response = prepared["answer"] + tok.eos_token
    return len(tok.encode(prompt, add_special_tokens=False)), len(tok.encode(response, add_special_tokens=False))


def main():
    ap = argparse.ArgumentParser()
    for name in ("pool", "m1", "m2", "graded_nt", "tokenizer", "out_prefix"):
        ap.add_argument(name)
    ap.add_argument("--exclude", help="one problem id per line")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--seed", type=int, default=21)
    ap.add_argument("--max-response", type=int, default=2048)
    ap.add_argument("--max-total", type=int, default=4096)
    args = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    pool = {r["id"]: r for r in read(args.pool)}
    original = {(r["id"], r["sample"]): r["output"] for r in read(args.graded_nt) if r["correct"]}
    excluded = set(open(args.exclude).read().splitlines()) if args.exclude else set()
    counters = {method: collections.Counter() for method in ("m1", "m2")}
    choices = {method: {} for method in ("m1", "m2")}

    for method in ("m1", "m2"):
        for r in read(getattr(args, method)):
            key = r["id"]
            if key in excluded:
                counters[method]["manual_exclusion"] += 1
                continue
            if not r.get("response") or not (r.get("check") or {}).get("ok"):
                counters[method]["author_or_first_check"] += 1
                continue
            source = pool[key]
            before = original.get((key, r.get("sample"))) if method == "m2" else None
            if method == "m2" and before is None:
                counters[method]["missing_original"] += 1
                continue
            result = check(r["response"], source["answer"], source["source"], original=before)
            if not result["ok"]:
                counters[method].update(result["issues"])
                continue
            candidate = {**source, "response": r["response"], "method": method}
            prompt_len, response_len = token_lengths(tok, candidate)
            if response_len > args.max_response or prompt_len + response_len > args.max_total:
                counters[method]["length"] += 1
                continue
            candidate.update(prompt_tokens=prompt_len, response_tokens=response_len,
                             forward_passes=forward_passes(r["response"], lambda s: len(tok.encode(s, add_special_tokens=False))))
            candidate["saved_passes"] = response_len - candidate["forward_passes"]
            old = choices[method].get(key)
            if old is None or candidate["saved_passes"] > old["saved_passes"]:
                choices[method][key] = candidate
            counters[method]["accepted_samples"] += 1

    common = sorted(choices["m1"].keys() & choices["m2"].keys())
    if args.limit and len(common) > args.limit:
        rng = random.Random(args.seed)
        groups = collections.defaultdict(list)
        for key in common:
            groups[pool[key]["answer_type"]].append(key)
        chosen = []
        for answer_type in ("fraction", "expression"):
            rng.shuffle(groups[answer_type])
            chosen.extend(groups[answer_type][:min(len(groups[answer_type]), args.limit // 5)])
        remaining = list(set(common) - set(chosen))
        rng.shuffle(remaining)
        common = sorted(chosen + remaining[:args.limit - len(chosen)])
    for method in ("m1", "m2"):
        with open(f"{args.out_prefix}_{method}.jsonl", "w") as f:
            for key in common:
                f.write(json.dumps(choices[method][key], ensure_ascii=False) + "\n")
    stats = {"selected": len(common), "answer_types": dict(collections.Counter(pool[k]["answer_type"] for k in common)),
             "sources": dict(collections.Counter(pool[k]["source"] for k in common)),
             "max_response": args.max_response, "max_total": args.max_total, "exclude": sorted(excluded),
             "method": {m: {"distinct_eligible": len(choices[m]), **dict(counters[m])} for m in choices}}
    with open(f"{args.out_prefix}_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
