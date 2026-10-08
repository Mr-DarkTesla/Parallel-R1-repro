"""M1 of exp 21: Claude (through the VK AI Proxy, claude_call.py) writes concise solutions directly in the Multiverse format.

Problems are sent in batches (m1_system.md); every solution is checked with checks.check against the pool reference; only ok ones are
used later. Resumable: a batch whose file exists is not sent again.
Usage: python m1_author.py <problems.jsonl> <out_dir> [--batch 4] [--workers 8] [--limit N] [--model M]
Writes out_dir/batch_<k>.json (ids, reply, usage, cost) and out_dir/m1.jsonl (one row per problem: id, response, check).
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checks import check  # noqa: E402
from claude_call import call  # noqa: E402

SYSTEM = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "m1_system.md")).read()
SOLUTION = re.compile(r'<solution id="([^"]+)">\s*(.*?)\s*</solution>', re.S)


def run_batch(k, rows, out_dir, model):
    path = os.path.join(out_dir, f"batch_{k:05d}.json")
    if os.path.exists(path):
        return json.load(open(path))
    msg = "\n\n".join(f'PROBLEM id="{r["id"]}"\n{r["question"]}' for r in rows)
    reply = call(SYSTEM, msg, model=model)
    rec = {"batch": k, "ids": [r["id"] for r in rows], "reply": reply["text"], "is_error": reply["is_error"],
           "error": reply.get("error"), "usage": reply.get("usage"), "cost_usd": reply.get("cost_usd")}
    json.dump(rec, open(path + ".tmp", "w"), ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problems")
    ap.add_argument("out_dir")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=None)
    args = ap.parse_args()
    rows = [json.loads(line) for line in open(args.problems)]
    if args.limit:
        rows = rows[:args.limit]
    os.makedirs(args.out_dir, exist_ok=True)
    batches = [rows[i:i + args.batch] for i in range(0, len(rows), args.batch)]
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = [ex.submit(run_batch, k, b, args.out_dir, args.model) for k, b in enumerate(batches)]
        for n, f in enumerate(cf.as_completed(futs), 1):
            rec = f.result()
            if n % 10 == 0 or rec["is_error"]:
                print(n, "/", len(batches), "batch", rec["batch"], "error", rec["is_error"], "cost", rec["cost_usd"], flush=True)
    by_id = {r["id"]: r for r in rows}
    stats, cost = {}, 0.0
    with open(os.path.join(args.out_dir, "m1.jsonl"), "w") as f:
        for b in sorted(os.listdir(args.out_dir)):
            if not (b.startswith("batch_") and b.endswith(".json")):
                continue
            rec = json.load(open(os.path.join(args.out_dir, b)))
            cost += rec["cost_usd"] or 0
            got = dict(SOLUTION.findall(rec["reply"] or ""))
            for i in rec["ids"]:
                if i not in by_id:
                    continue
                text = got.get(i)
                status = "missing" if text is None else "no_block" if text.strip() == "NO_BLOCK" else "written"
                c = check(text, by_id[i]["answer"], by_id[i]["source"]) if status == "written" else None
                key = status if c is None else ("ok" if c["ok"] else "rejected")
                stats[key] = stats.get(key, 0) + 1
                f.write(json.dumps({"id": i, "status": status, "response": text, "check": c}, ensure_ascii=False) + "\n")
    print(json.dumps({"problems": len(rows), **stats, "cost_usd": round(cost, 2)}))


if __name__ == "__main__":
    main()
