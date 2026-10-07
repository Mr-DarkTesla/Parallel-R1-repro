"""Variant C, step 3 (v3, plan-only): Claude returns a structure plan, this script assembles the Multiverse text from Qwen's paragraphs.

Claude (convert_plan_system.md) sees the problem and the thinking text split into numbered paragraphs and returns, per block: paragraph
ranges of lead / paths / tail, one outline per path, a short conclusion, and optional connective edits. Path text is therefore Qwen's
text byte for byte (except listed connective edits); the answer after </think> and text outside blocks are copied unchanged.
Usage: python convert_plan.py <traces.jsonl> <pool.jsonl|-> <out_dir> [--ids mv:sample,...] [--limit N] [--workers 4] [--model M]
Writes out_dir/<mv_index>_<sample>.json (reply, plan, usage, attempts, response, checks) and summary.jsonl.
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
from convert import refused, splice, split_trace  # noqa: E402

SYSTEM = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "convert_plan_system.md")).read()
R = r'units="(\d+)(?:-(\d+))?"'
TOK = re.compile(rf'<block {R}>|</block>|<(lead|tail) {R}\s*/>|<path {R}>|</path>|<outline>(.*?)</outline>|'
                 r'<conclusion>(.*?)</conclusion>|<edit unit="(\d+)">\s*<old>(.*?)</old>\s*<new>(.*?)</new>\s*</edit>', re.S)


class PlanError(ValueError):
    pass


def tokens(text):
    text = re.sub(r"<analysis>.*?</analysis>", "", text, flags=re.S)
    out = []
    for m in TOK.finditer(text):
        g = m.groups()
        rng = lambda a, b: (int(a), int(b or a))  # noqa: E731
        if g[0]:
            out.append(("block", rng(g[0], g[1])))
        elif m.group(0) == "</block>":
            out.append(("/block", None))
        elif g[2]:
            out.append((g[2], rng(g[3], g[4])))
        elif g[5]:
            out.append(("path", rng(g[5], g[6])))
        elif m.group(0) == "</path>":
            out.append(("/path", None))
        elif g[7] is not None:
            out.append(("outline", g[7].strip()))
        elif g[8] is not None:
            out.append(("conclusion", g[8].strip()))
        elif g[9]:
            out.append(("edit", (int(g[9]), g[10], g[11])))
    return out


def parse_plan(text, n_units):
    """-> list of top-level blocks: {"range", "lead", "paths": [{"range", "outline", "inner"}], "conclusion", "tail"}, edits."""
    toks, pos, edits = tokens(text), [0], []

    def take(kind):
        if pos[0] >= len(toks) or toks[pos[0]][0] != kind:
            got = toks[pos[0]][0] if pos[0] < len(toks) else "end"
            raise PlanError(f"expected {kind}, got {got}")
        pos[0] += 1
        return toks[pos[0] - 1][1]

    def peek():
        return toks[pos[0]][0] if pos[0] < len(toks) else None

    def block(depth, lo, hi):
        a, b = take("block")
        if depth > 2:
            raise PlanError("nesting deeper than 2")
        if not (lo <= a <= b <= hi):
            raise PlanError(f"block {a}-{b} outside {lo}-{hi}")
        blk = {"range": (a, b), "lead": None, "paths": [], "conclusion": "", "tail": None}
        if peek() == "lead":
            blk["lead"] = take("lead")
        while peek() == "path":
            x, y = take("path")
            path = {"range": (x, y), "outline": take("outline"), "inner": None}
            if peek() == "block":
                path["inner"] = block(depth + 1, x, y)
            take("/path")
            blk["paths"].append(path)
        blk["conclusion"] = take("conclusion")
        if peek() == "tail":
            blk["tail"] = take("tail")
        while peek() == "edit":
            edits.append(take("edit"))
        take("/block")
        parts = ([blk["lead"]] if blk["lead"] else []) + [p["range"] for p in blk["paths"]] + ([blk["tail"]] if blk["tail"] else [])
        nxt = a
        for s, e in parts:
            if s != nxt or e < s:
                raise PlanError(f"block {a}-{b}: parts do not tile the range at {s}-{e}")
            nxt = e + 1
        if nxt != b + 1:
            raise PlanError(f"block {a}-{b}: parts end at {nxt - 1}")
        if not 2 <= len(blk["paths"]) <= 6:
            raise PlanError(f"block {a}-{b}: {len(blk['paths'])} paths")
        if not blk["conclusion"] or any(not p["outline"] for p in blk["paths"]):
            raise PlanError(f"block {a}-{b}: empty outline or conclusion")
        return blk

    blocks, last = [], 0
    while peek() == "block":
        blk = block(1, last + 1, n_units)
        blocks.append(blk)
        last = blk["range"][1]
    if pos[0] != len(toks):
        raise PlanError(f"unexpected {toks[pos[0]][0]} after blocks")
    return blocks, edits


def path_units(blocks):
    for blk in blocks:
        for p in blk["paths"]:
            yield from range(p["range"][0], p["range"][1] + 1)


def apply_edits(units, edits, allowed):
    """Apply connective edits; an edit that is not a pure connective change (math removed or added, outside a path, not found
    exactly once, too long) is skipped and reported, so the original wording stays."""
    units, skipped = list(units), []
    for k, old, new in edits:
        bad = (k not in allowed or not old or units[k - 1].count(old) != 1 or len(old) > 200 or len(new) > len(old) + 40
               or checks.math_atoms(old) != checks.math_atoms(new))
        if bad:
            skipped.append([k, old[:80]])
            continue
        units[k - 1] = units[k - 1].replace(old, new, 1)
    return units, skipped


def render(units, seps, blk, prefix=""):
    def text(a, b):
        return "".join(units[i] + (seps[i] if i < b - 1 else "") for i in range(a - 1, b))

    def sep(i):  # separator after paragraph i (1-based)
        return seps[i - 1] if i - 1 < len(seps) else "\n\n"

    out = ""
    if blk["lead"]:
        out += text(*blk["lead"]) + sep(blk["lead"][1])
    out += "<Parallel>\n<Goal>\n"
    out += "".join(f"<Outline>\n{prefix}{i}: {p['outline']}\n</Outline>\n" for i, p in enumerate(blk["paths"], 1))
    out += "</Goal>\n"
    for i, p in enumerate(blk["paths"], 1):
        x, y = p["range"]
        inner = p["inner"]
        if inner:
            p0, q0 = inner["range"]
            body = (text(x, p0 - 1) + sep(p0 - 1) if p0 > x else "") + render(units, seps, inner, f"{prefix}{i}.") + \
                   (sep(q0) + text(q0 + 1, y) if q0 < y else "")
        else:
            body = text(x, y)
        out += f"<Path>\n{prefix}{i}: {body}\n</Path>\n"
    out += f"<Conclusion>\n{blk['conclusion']}\n</Conclusion>\n</Parallel>"
    if blk["tail"]:
        out += sep(blk["tail"][0] - 1) + text(*blk["tail"])
    return out


def convert_one(row, problem, out_dir, model=None, fallback="claude-sonnet-5-5"):
    key = f"{row['mv_index']}_{row['sample']}"
    path = os.path.join(out_dir, key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    head, units, seps, tail = split_trace(row["output"])
    numbered = "\n\n".join(f"[U{i + 1}] {u}" for i, u in enumerate(units))
    msg = f"PROBLEM\n{problem}\n\nSOLUTION DRAFT by Qwen3-4B ({len(units)} paragraphs), to be restructured\n{numbered}\n"
    reply = call(SYSTEM, msg, model=model)
    attempts = [{"model": model or "default", "is_error": reply["is_error"], "refused": refused(reply)}]
    if refused(reply) and fallback:  # safeguard false positive: one retry with another model through the same proxy
        reply = call(SYSTEM, msg, model=fallback)
        attempts.append({"model": fallback, "is_error": reply["is_error"], "refused": refused(reply)})
    rec = {"key": key, "mv_index": row["mv_index"], "sample": row["sample"], "prompt": row["prompt"], "n_units": len(units),
           "reply": reply["text"], "usage": reply.get("usage"), "cost_usd": reply.get("cost_usd"),
           "duration_ms": reply.get("duration_ms"), "is_error": reply["is_error"], "attempts": attempts,
           "plan_error": None, "blocks": [], "original": row["output"], "response": None}
    if not reply["is_error"]:
        try:
            blocks, edits = parse_plan(reply["text"], len(units))
            edited, skipped = apply_edits(units, edits, set(path_units(blocks)))
            spliced = [(b["range"][0], b["range"][1], render(edited, seps, b)) for b in blocks]
            rec.update({"blocks": [list(b["range"]) for b in blocks], "edits": len(edits), "edits_skipped": skipped,
                        "response": head + splice(units, seps, spliced) + tail})
            if blocks:
                rec["checks"] = checks.check_sample(row["output"], rec["response"], units, spliced)
        except PlanError as e:
            rec["plan_error"] = str(e)
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
    ap.add_argument("--model", default=None)
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
        futs = [ex.submit(convert_one, r, problems.get(r["mv_index"], r["prompt"]), args.out_dir, args.model) for r in rows]
        for f in cf.as_completed(futs):
            rec = f.result()
            c = rec.get("checks", {})
            print(rec["key"], "attempts", [a["refused"] for a in rec["attempts"]], "blocks", len(rec["blocks"]),
                  "plan_error", rec["plan_error"], "ok", c.get("ok"), "issues", c.get("issues"),
                  "out_tokens", (rec["usage"] or {}).get("output_tokens"), "cost", rec["cost_usd"], flush=True)
    with open(os.path.join(args.out_dir, "summary.jsonl"), "w") as f:
        for name in sorted(os.listdir(args.out_dir)):
            if name.endswith(".json"):
                r = json.load(open(os.path.join(args.out_dir, name)))
                f.write(json.dumps({k: r.get(k) for k in ("key", "n_units", "blocks", "usage", "cost_usd", "attempts",
                                                          "plan_error", "checks")}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
