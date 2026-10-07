"""Variant C, step 3: convert Qwen3-4B thinking traces into the Multiverse format with Claude (VK AI Proxy), then splice.

Claude sees the thinking split into numbered paragraphs and returns only the replaced unit ranges (convert_system.md);
everything outside the blocks and the answer after </think> are copied byte for byte by this script.
Usage: python convert.py <traces.jsonl> <pool.jsonl|-> <out_dir> [--ids mv_index:sample,...] [--limit N] [--workers 4]
Input rows need: output (raw generation with <think>...</think>), prompt (user text), mv_index, sample.
Writes out_dir/<mv_index>_<sample>.json with the raw Claude reply, usage, spliced response and check results; summary.jsonl.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402
from claude_call import call  # noqa: E402

SYSTEM = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "convert_system.md")).read()
BLOCK = re.compile(r'<block units="(\d+)-(\d+)">\n?(.*?)\n?</block>', re.S)


def split_trace(output):
    """-> (head, units, seps, tail): output == head + units[0] + seps[0] + units[1] + ... + units[-1] + tail."""
    out = output.replace("<|im_end|>", "").replace("<|endoftext|>", "")
    start, end = out.index("<think>") + len("<think>"), out.index("</think>")
    think = out[start:end]
    lead = re.match(r"\s*", think).group(0)
    trail = re.search(r"\s*$", think).group(0)
    body = think[len(lead):len(think) - len(trail)]
    parts = re.split(r"(\n[ \t]*\n\s*)", body)
    units, seps = parts[0::2], parts[1::2]
    return out[:start] + lead, units, seps, trail + out[end:]


def user_message(problem, units):
    numbered = "\n\n".join(f"[U{i + 1}] {u}" for i, u in enumerate(units))
    return (f"PROBLEM\n{problem}\n\nSOLUTION DRAFT by Qwen3-4B ({len(units)} paragraphs), to be restructured\n{numbered}\n")


def splice(units, seps, blocks):
    """Replace unit ranges (1-based, inclusive) with replacement texts; ranges must be ordered and disjoint."""
    pieces, i = [], 0
    for a, b, text in blocks:
        while i < a - 1:
            pieces.append(units[i] + (seps[i] if i < len(seps) else ""))
            i += 1
        pieces.append(text + (seps[b - 1] if b - 1 < len(seps) else ""))
        i = b
    while i < len(units):
        pieces.append(units[i] + (seps[i] if i < len(seps) else ""))
        i += 1
    return "".join(pieces)


def refused(reply):
    return reply.get("stop_reason") == "refusal" or (reply["is_error"] and "safeguards" in (reply.get("text") or ""))


def parse_reply(text, n_units):
    blocks, errors = [], []
    for m in BLOCK.finditer(text):
        a, b, body = int(m.group(1)), int(m.group(2)), m.group(3).strip("\n")
        if not (1 <= a <= b <= n_units):
            errors.append(f"range {a}-{b} out of 1..{n_units}")
        elif blocks and a <= blocks[-1][1]:
            errors.append(f"range {a}-{b} overlaps or is out of order")
        else:
            blocks.append((a, b, body))
    return blocks, errors


def convert_one(row, problem, out_dir, model=None, fallback="claude-sonnet-5-5"):
    key = f"{row['mv_index']}_{row['sample']}"
    path = os.path.join(out_dir, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    head, units, seps, tail = split_trace(row["output"])
    msg = user_message(problem, units)
    reply = call(SYSTEM, msg, model=model)
    attempts = [{"model": model or "default", "is_error": reply["is_error"], "refused": refused(reply)}]
    if refused(reply) and fallback:  # safeguard false positive: one retry with another model through the same proxy
        reply = call(SYSTEM, msg, model=fallback)
        attempts.append({"model": fallback, "is_error": reply["is_error"], "refused": refused(reply)})
    blocks, errors = parse_reply(reply["text"], len(units))
    response = head + splice(units, seps, blocks) + tail if not errors else None
    rec = {"key": key, "mv_index": row["mv_index"], "sample": row["sample"], "prompt": row["prompt"],
           "n_units": len(units), "reply": reply["text"], "usage": reply.get("usage"), "cost_usd": reply.get("cost_usd"),
           "duration_ms": reply.get("duration_ms"), "is_error": reply["is_error"], "attempts": attempts, "parse_errors": errors,
           "blocks": [[a, b] for a, b, _ in blocks], "original": row["output"], "response": response}
    if response is not None:
        rec["checks"] = checks.check_sample(row["output"], response, units, blocks)
    json.dump(rec, open(path + ".tmp", "w"), ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("traces")
    ap.add_argument("pool")
    ap.add_argument("out_dir")
    ap.add_argument("--ids", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    rows = [json.loads(line) for line in open(args.traces)]
    if args.ids:
        want = {tuple(map(int, x.split(":"))) for x in args.ids.split(",")}
        rows = [r for r in rows if (r["mv_index"], r["sample"]) in want]
    if args.limit:
        rows = rows[:args.limit]
    problems = {}
    if args.pool != "-":
        problems = {r["mv_index"]: r["question"] for r in map(json.loads, open(args.pool))}
    os.makedirs(args.out_dir, exist_ok=True)
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(convert_one, r, problems.get(r["mv_index"], r["prompt"]), args.out_dir): r for r in rows}
        for f in cf.as_completed(futs):
            rec = f.result()
            c = rec.get("checks", {})
            print(rec["key"], "blocks", len(rec["blocks"]), "ok", c.get("ok"), "issues", c.get("issues"),
                  "usage in/out", rec["usage"].get("input_tokens"), rec["usage"].get("output_tokens"), flush=True)
    with open(os.path.join(args.out_dir, "summary.jsonl"), "w") as f:
        for name in sorted(os.listdir(args.out_dir)):
            if name.endswith(".json"):
                r = json.load(open(os.path.join(args.out_dir, name)))
                f.write(json.dumps({k: r.get(k) for k in ("key", "n_units", "blocks", "usage", "cost_usd", "parse_errors",
                                                          "checks")}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
