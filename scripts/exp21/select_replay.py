"""Select the same clean Qwen3-0.6B replay rows for both M1 and M2, in both chat-template modes.

Run beside the downloaded tokenizer. Input grade_gen.py outputs; write <prefix>_{nt,th}.jsonl and <prefix>_stats.json.
Selection and length checks use no evaluation results.
"""
import argparse
import collections
import json
import random

from transformers import AutoTokenizer

from select_pair import read, token_lengths


def main():
    ap = argparse.ArgumentParser()
    for name in ("pool", "graded_nt", "graded_th", "tokenizer", "out_prefix"):
        ap.add_argument(name)
    ap.add_argument("--exclude", help="one problem id per line")
    ap.add_argument("--limit-nt", type=int, default=0)
    ap.add_argument("--limit-th", type=int, default=0)
    ap.add_argument("--max-total", type=int, default=4096)
    ap.add_argument("--seed", type=int, default=21)
    args = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    allowed = {r["id"] for r in read(args.pool)}
    excluded = set(open(args.exclude).read().splitlines()) if args.exclude else set()
    stats = {}
    for suffix, path, kind, limit in (("nt", args.graded_nt, "replay_nt", args.limit_nt),
                                      ("th", args.graded_th, "replay_th", args.limit_th)):
        choices, rejected = {}, collections.Counter()
        for r in read(path):
            if r["id"] not in allowed:
                rejected["outside_clean_pool"] += 1
                continue
            if r["id"] in excluded:
                rejected["manual_exclusion"] += 1
                continue
            if not r["correct"]:
                rejected["grade"] += 1
                continue
            candidate = {"id": r["id"], "question": r["question"], "response": r["output"],
                         "source": r["source"], "answer_type": r["answer_type"]}
            try:
                prompt_len, response_len = token_lengths(tok, candidate, kind)
            except AssertionError:
                rejected["template"] += 1
                continue
            if prompt_len + response_len > args.max_total:
                rejected["length"] += 1
                continue
            candidate.update(prompt_tokens=prompt_len, response_tokens=response_len)
            old = choices.get(r["id"])
            if old is None or response_len < old["response_tokens"]:
                choices[r["id"]] = candidate
        selected = list(choices.values())
        rng = random.Random(args.seed + (0 if suffix == "nt" else 1))
        rng.shuffle(selected)
        if limit:
            selected = selected[:limit]
        selected.sort(key=lambda x: x["id"])
        with open(f"{args.out_prefix}_{suffix}.jsonl", "w") as f:
            for r in selected:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        stats[suffix] = {"eligible_problems": len(choices), "selected": len(selected), "rejected_samples": dict(rejected),
                         "source": dict(collections.Counter(r["source"] for r in selected)),
                         "answer_type": dict(collections.Counter(r["answer_type"] for r in selected))}
    with open(f"{args.out_prefix}_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
