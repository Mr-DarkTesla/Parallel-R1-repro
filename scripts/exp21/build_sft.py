"""SFT parquets of exp 21 in the layout of scripts/instruct4b/sft.sh (extra_info.question / extra_info.answer, per-row
extra_info.enable_thinking).

Row kinds:
  parallel  Multiverse prompt (make_mv_prompts.mv_prompt), non-thinking template, response = a checked M1/M2 example
  parallel_th  same prompt and checked M1 solution placed inside <think>; final answer follows </think>
  control   the same examples with tags removed (mv_format.strip_tags), the same Multiverse prompt, non-thinking
  control_th  the same internal-thinking examples with tags removed, thinking enabled
  replay_nt plain prompt, non-thinking, response = Qwen3-0.6B's own correct non-thinking answer (verbatim)
  replay_th plain prompt, thinking, response = Qwen3-0.6B's own correct thinking answer (<think>...</think> + answer, verbatim)
Usage: python build_sft.py <out_prefix> --rows kind:path[:n] ... [--val 48] [--seed 0]
Each input jsonl row: id, question, response. Writes <out_prefix>_train.parquet, <out_prefix>_val.parquet (val rows per kind in
proportion, problems disjoint from train), <out_prefix>_rows.json (counts per kind and source).
"""
import argparse
import collections
import json
import os
import random
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_mv_prompts import mv_prompt  # noqa: E402
from mv_format import strip_tags  # noqa: E402

HEADER = ("Solve the following problem step by step.\n"
          "End your response with a line starting with Final Answer: followed by the final result.\n\nProblem: ")


def row(kind, r):
    plain = HEADER + r["question"]
    response = r["response"].replace("<|im_end|>", "").replace("<|endoftext|>", "").strip()
    if kind == "parallel":
        prompt, thinking = mv_prompt(plain), False
    elif kind == "parallel_th":
        prompt, thinking = mv_prompt(plain), True
        assert response.startswith("<think>") and response.count("</think>") == 1, r["id"]
    elif kind == "control":
        prompt, thinking, response = mv_prompt(plain), False, strip_tags(response).strip()
    elif kind == "control_th":
        assert response.startswith("<think>") and response.count("</think>") == 1, r["id"]
        prompt, thinking, response = mv_prompt(plain), True, strip_tags(response).strip()
    elif kind == "replay_nt":
        prompt, thinking = plain, False
    elif kind == "replay_th":
        prompt, thinking = plain, True
        assert response.startswith("<think>") and response.count("</think>") == 1, r["id"]
    else:
        raise ValueError(kind)
    return {"data_source": f"exp21_{kind}", "id": r["id"], "source": r["id"].split("-")[0],
            "extra_info": {"question": prompt, "answer": response, "enable_thinking": thinking, "kind": kind, "id": r["id"]}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_prefix")
    ap.add_argument("--rows", nargs="+", required=True)
    ap.add_argument("--val", type=int, default=48)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--val-ids-from", help="reuse the held-out problem IDs of an existing SFT prefix")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    rows = []
    for spec in args.rows:
        kind, path, *n = spec.split(":")
        data = [json.loads(line) for line in open(path)]
        rng.shuffle(data)
        rows += [row(kind, r) for r in (data[:int(n[0])] if n else data)]
    problems = sorted({r["id"] for r in rows})
    rng.shuffle(problems)
    total, val_ids = len(rows), set()
    if args.val_ids_from:
        val_ids = set(pd.read_parquet(f"{args.val_ids_from}_val.parquet")["id"])
        assert val_ids <= set(problems)
    else:
        for p in problems:  # whole problems go to val until it has args.val rows
            if sum(r["id"] in val_ids for r in rows) >= args.val:
                break
            val_ids.add(p)
    train = [r for r in rows if r["id"] not in val_ids]
    val = [r for r in rows if r["id"] in val_ids]
    rng.shuffle(train)
    for name, part in (("train", train), ("val", val)):
        frame = pd.DataFrame(part)
        frame["index"] = range(len(frame))
        frame.to_parquet(f"{args.out_prefix}_{name}.parquet")
    counts = {name: dict(collections.Counter((r["extra_info"]["kind"], r["source"]) for r in part).most_common())
              for name, part in (("train", train), ("val", val))}
    json.dump({k: {f"{a}/{b}": c for (a, b), c in v.items()} for k, v in counts.items()} | {"rows_in": total},
              open(f"{args.out_prefix}_rows.json", "w"), indent=1)
    print(json.dumps({"train": len(train), "val": len(val)}))


if __name__ == "__main__":
    main()
