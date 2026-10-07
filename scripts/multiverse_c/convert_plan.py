"""Variant C, step 3 (plan-only converter, v4 with the review block filter): Claude returns a structure plan, this script assembles the Multiverse text from Qwen's paragraphs.

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


# Block filter (independent review multiverse_c2_review): drop blocks with skipped edits, trivial or unbalanced paths, small
# saving, or a path 2..k that opens like a continuation of its sibling; at most one re-check block after the answer appears.
MIN_PATH_CHARS = 200  # ~60 Qwen3 tokens: no one-line paths (calibrated on the 10 reviewed samples)
MIN_RATIO = 0.1  # shortest / longest path
MIN_SAVED_CHARS = 200  # sum of paths minus the longest; good reviewed blocks saved 256-2800 chars
SIBLING_START = re.compile(r"^\s*(?:\d+(?:\.\d+)*:\s*)?(?:similarly|again|as before|as above|therefore|thus|hence|likewise|but|"
                           r"however|alternatively|also|next|then|in the same way|the other)\b", re.I)
SIBLING_NEAR = re.compile(r"\b(?:the other (?:case|path|one|method|approach)|as before|as above|earlier|previous(?:ly)?)\b", re.I)


def answer_unit(units, cand):
    """1-based index of the first paragraph that states the final candidate as a result (e.g. "= 59", "is 59"), else None."""
    cand = (cand or "").strip()
    if not cand or len(cand) > 30:
        return None
    pat = re.compile(r"(?:=|\bis\b|\bbe\b|\bget\b|\bgives?\b|\bequals?\b|boxed\{)\s*\$?\s*" + re.escape(cand) + r"(?!\d|\.\d)")
    for i, u in enumerate(units, 1):
        if pat.search(u):
            return i
    return None


def block_defects(blk, units, seps, skipped_units, top):
    def text(a, b):
        return "".join(units[i] + (seps[i] if i < b - 1 else "") for i in range(a - 1, b))

    texts = [text(*p["range"]) for p in blk["paths"]]
    lens = [len(t) for t in texts]
    out = []
    if any(skipped_units & set(range(p["range"][0], p["range"][1] + 1)) for p in blk["paths"]):
        out.append("edit_skipped")
    if min(lens) < MIN_PATH_CHARS:
        out.append("short_path")
    if min(lens) < MIN_RATIO * max(lens):
        out.append("unbalanced")
    if top and sum(lens) - max(lens) < MIN_SAVED_CHARS:
        out.append("small_saving")
    if any(SIBLING_START.search(t) or SIBLING_NEAR.search(t[:200]) for t in texts[1:]):
        out.append("sibling_start")
    return out


def select_blocks(blocks, units, seps, skipped, ans_unit):
    """-> (kept top-level blocks, per-block decisions). Inner blocks with defects are unwrapped (path stays sequential)."""
    skipped_units = {k for k, _ in skipped}
    decisions, good, checks_ok = [], [], []
    for blk in blocks:
        for p in blk["paths"]:
            if p["inner"]:
                d = block_defects(p["inner"], units, seps, skipped_units, top=False)
                if d:
                    decisions.append({"range": p["inner"]["range"], "inner": True, "dropped": d})
                    p["inner"] = None
        d = block_defects(blk, units, seps, skipped_units, top=True)
        is_check = ans_unit is not None and blk["range"][0] > ans_unit
        decisions.append({"range": blk["range"], "check": is_check, "dropped": d})
        if not d:
            (checks_ok if is_check else good).append(blk)
    if checks_ok:  # at most one re-check block: the one with the most text in paths
        best = max(checks_ok, key=lambda b: sum(p["range"][1] - p["range"][0] + 1 for p in b["paths"]))
        for dcs in decisions:
            if dcs.get("check") and not dcs["dropped"] and dcs["range"] != best["range"]:
                dcs["dropped"] = ["extra_check_block"]
        good.append(best)
    return sorted(good, key=lambda b: b["range"][0]), decisions


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


def assemble(rec, row, head, units, seps, tail):
    """Parse the plan in rec["reply"], filter blocks, render; fills rec (blocks, decisions, response, checks)."""
    blocks, edits = parse_plan(rec["reply"], len(units))
    plan_ranges = [list(b["range"]) for b in blocks]
    edited, skipped = apply_edits(units, edits, set(path_units(blocks)))
    ans = answer_unit(units, row.get("candidate"))
    kept, decisions = select_blocks(blocks, edited, seps, skipped, ans)
    keep_units = set(path_units(kept))
    for b in kept:  # edits only inside kept parallel paths; unwrapped inner blocks keep the original wording
        for p in b["paths"]:
            if p["inner"]:
                keep_units |= set(path_units([p["inner"]]))
    final = [edited[i] if (i + 1) in keep_units and not _in_unwrapped(i + 1, decisions) else units[i] for i in range(len(units))]
    spliced = [(b["range"][0], b["range"][1], render(final, seps, b)) for b in kept]
    rec.update({"plan_blocks": plan_ranges, "blocks": [list(b["range"]) for b in kept], "decisions": decisions,
                "answer_unit": ans, "edits": len(edits), "edits_skipped": skipped,
                "response": head + splice(units, seps, spliced) + tail})
    rec.pop("checks", None)
    if kept:
        rec["checks"] = checks.check_sample(row["output"], rec["response"], units, spliced)


def _in_unwrapped(u, decisions):
    return any(d.get("inner") and d["range"][0] <= u <= d["range"][1] for d in decisions)


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
           "call_error": reply.get("error"), "plan_error": None, "blocks": [], "original": row["output"], "response": None}
    if not reply["is_error"]:
        try:
            assemble(rec, row, head, units, seps, tail)
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
