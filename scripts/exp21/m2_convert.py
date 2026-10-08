"""M2 of exp 21: Qwen3-0.6B's own correct non-thinking answers + a block plan from Claude; path text stays Qwen's text.

Claude (m2_system.md, through the VK AI Proxy) sees answers split into numbered units and returns, per answer, unit ranges of
lead / paths / tail, one outline per path and a short conclusion (plan-only converter of variant C, v3,
0/28 refusals, here without nesting and batched). This script assembles the block from the units verbatim. Blocks with defects are dropped
(short or unbalanced paths, small saving, a path 2..k that opens like a continuation of its sibling);
the result must pass checks.check (grammar, verified answer after the block, no answer before it, numbers kept, no re-check).
Usage: python m2_convert.py <answers.jsonl> <out_dir> [--batch 4] [--workers 8] [--limit N] [--model M]
answers.jsonl rows: id, sample, question, answer (gold), source, output (Qwen's answer text).
Writes out_dir/batch_<k>.json (reply, usage) and out_dir/m2.jsonl (id, sample, response or null, decisions, check).
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checks import XREF, check  # noqa: E402
from claude_call import call  # noqa: E402

SYSTEM = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "m2_system.md")).read()
PLAN = re.compile(r'<plan id="([^"]+)">(.*?)</plan>', re.S)
R = r'units="(\d+)(?:-(\d+))?"'
TOK = re.compile(rf'<block {R}>|</block>|<(lead|tail) {R}\s*/>|<path {R}>|</path>|<outline>(.*?)</outline>|'
                 r'<conclusion>(.*?)</conclusion>|<edit unit="(\d+)">\s*<old>(.*?)</old>\s*<new>(.*?)</new>\s*</edit>', re.S)
SIBLING_START = re.compile(r"^\s*(?:similarly|again|as before|as above|therefore|thus|hence|likewise|but|however|alternatively|also|"
                           r"next|then|now|finally|in the same way|the other)\b", re.I)
MIN_PATH, MIN_RATIO, MIN_SAVED = 80, 0.15, 80  # characters


class PlanError(ValueError):
    pass


def split_units(text):
    """-> (units, seps): text == units[0] + seps[0] + ... + units[-1]; lines, display math kept in one unit."""
    parts = re.split(r"(\n+)", text.strip())
    units, seps = [parts[0]], []
    for sep, line in zip(parts[1::2], parts[2::2]):
        open_math = units[-1].count("$$") % 2 == 1 or units[-1].count("\\[") > units[-1].count("\\]")
        if open_math or re.fullmatch(r"\s*(\\\]|\$\$)\s*", line):
            units[-1] += sep + line
        else:
            units.append(line)
            seps.append(sep)
    return units, seps


def parse_plan(text, n):
    toks = []
    for m in TOK.finditer(text):
        g = m.groups()
        rng = (lambda a, b: (int(a), int(b or a)))  # noqa: E731
        if g[0]:
            toks.append(("block", rng(g[0], g[1])))
        elif m.group(0) == "</block>":
            toks.append(("/block", None))
        elif g[2]:
            toks.append((g[2], rng(g[3], g[4])))
        elif g[5]:
            toks.append(("path", rng(g[5], g[6])))
        elif m.group(0) == "</path>":
            toks.append(("/path", None))
        elif g[7] is not None:
            toks.append(("outline", g[7].strip()))
        elif g[8] is not None:
            toks.append(("conclusion", g[8].strip()))
        elif g[9]:
            toks.append(("edit", (int(g[9]), g[10], g[11])))
    pos, blocks, edits, last = [0], [], [], 0

    def take(kind):
        if pos[0] >= len(toks) or toks[pos[0]][0] != kind:
            raise PlanError(f"expected {kind}, got {toks[pos[0]][0] if pos[0] < len(toks) else 'end'}")
        pos[0] += 1
        return toks[pos[0] - 1][1]

    peek = lambda: toks[pos[0]][0] if pos[0] < len(toks) else None  # noqa: E731
    while peek() == "block":
        a, b = take("block")
        if not last < a <= b <= n:
            raise PlanError(f"block {a}-{b} outside {last + 1}-{n}")
        blk = {"range": (a, b), "lead": take("lead") if peek() == "lead" else None, "paths": []}
        while peek() == "path":
            rng = take("path")
            blk["paths"].append({"range": rng, "outline": take("outline")})
            take("/path")
        blk["conclusion"] = take("conclusion")
        blk["tail"] = take("tail") if peek() == "tail" else None
        while peek() == "edit":
            edits.append(take("edit"))
        take("/block")
        parts = ([blk["lead"]] if blk["lead"] else []) + [p["range"] for p in blk["paths"]] + ([blk["tail"]] if blk["tail"] else [])
        nxt = a
        for s, e in parts:
            if s != nxt or e < s:
                raise PlanError(f"block {a}-{b}: parts do not tile the range at {s}-{e}")
            nxt = e + 1
        if nxt != b + 1 or not 2 <= len(blk["paths"]) <= 4 or not blk["conclusion"] or not all(p["outline"] for p in blk["paths"]):
            raise PlanError(f"block {a}-{b}: tiling, path count, outline or conclusion")
        blocks.append(blk)
        last = b
    if pos[0] != len(toks):
        raise PlanError(f"unexpected {toks[pos[0]][0]}")
    return blocks, edits


def assemble(units, seps, blocks, edits):
    """-> (response or None, decisions)."""
    # A plan may suggest edits, but M2 keeps the model's words unchanged.
    edited = {k for k, _, _ in edits}
    text = lambda a, b: "".join(units[i] + (seps[i] if i < b - 1 else "") for i in range(a - 1, b))  # noqa: E731
    sep = lambda i: seps[i - 1] if i - 1 < len(seps) else "\n"  # noqa: E731
    pieces, decisions, i = [], [], 1
    for blk in blocks:
        paths = [text(*p["range"]).strip() for p in blk["paths"]]
        lens = [len(t) for t in paths]
        why = [w for w, bad in (("edit_required", any(edited & set(range(p["range"][0], p["range"][1] + 1)) for p in blk["paths"])),
                                ("short_path", min(lens) < MIN_PATH), ("unbalanced", min(lens) < MIN_RATIO * max(lens)),
                                ("small_saving", sum(lens) - max(lens) < MIN_SAVED),
                                ("sibling_start", any(SIBLING_START.search(t) for t in paths[1:])),
                                ("xref", any(XREF.search(t) for t in paths))) if bad]
        decisions.append({"range": blk["range"], "dropped": why})
        if why:
            continue
        a, b = blk["range"]
        while i < a:
            pieces.append(units[i - 1] + sep(i))
            i += 1
        out = (text(*blk["lead"]) + sep(blk["lead"][1]) if blk["lead"] else "") + "<Parallel>\n<Goal>\n"
        out += "".join(f"<Outline>{k}: {p['outline']}</Outline>\n" for k, p in enumerate(blk["paths"], 1)) + "</Goal>\n"
        out += "".join(f"<Path>\n{k}: {t}\n</Path>\n" for k, t in enumerate(paths, 1))
        out += f"<Conclusion>\n{blk['conclusion']}\n</Conclusion>\n</Parallel>"
        out += (sep(blk["tail"][0] - 1) + text(*blk["tail"])) if blk["tail"] else ""
        pieces.append(out + (sep(b) if b < len(units) else ""))
        i = b + 1
    if not any(not d["dropped"] for d in decisions):
        return None, decisions
    while i <= len(units):
        pieces.append(units[i - 1] + (sep(i) if i < len(units) else ""))
        i += 1
    return "".join(pieces), decisions


def run_batch(k, rows, out_dir, model):
    path = os.path.join(out_dir, f"batch_{k:05d}.json")
    if os.path.exists(path):
        return json.load(open(path))
    msgs = []
    for r in rows:
        units, _ = split_units(r["output"])
        numbered = "\n".join(f"[U{i}] {u}" for i, u in enumerate(units, 1))
        msgs.append(f'SOLUTION id="{r["key"]}" ({len(units)} units)\nPROBLEM: {r["question"]}\n{numbered}')
    reply = call(SYSTEM, "\n\n".join(msgs), model=model)
    rec = {"batch": k, "keys": [r["key"] for r in rows], "reply": reply["text"], "is_error": reply["is_error"],
           "error": reply.get("error"), "usage": reply.get("usage"), "cost_usd": reply.get("cost_usd")}
    if reply["is_error"] and not reply["text"]:  # transport failure (e.g. policyHelper timeout): not saved, a rerun retries it
        return rec
    json.dump(rec, open(path + ".tmp", "w"), ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("answers")
    ap.add_argument("out_dir")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=None)
    args = ap.parse_args()
    rows = [json.loads(line) for line in open(args.answers)]
    for r in rows:
        r["output"] = r["output"].replace("<|im_end|>", "").replace("<|endoftext|>", "").strip()
        r["key"] = f"{r['id']}#{r['sample']}"
    rows = rows[:args.limit] if args.limit else rows
    os.makedirs(args.out_dir, exist_ok=True)
    batches = [rows[i:i + args.batch] for i in range(0, len(rows), args.batch)]
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for n, f in enumerate(cf.as_completed([ex.submit(run_batch, k, b, args.out_dir, args.model) for k, b in enumerate(batches)]), 1):
            rec = f.result()
            if n % 20 == 0 or rec["is_error"]:
                print(n, "/", len(batches), "batch", rec["batch"], "error", rec["is_error"], "cost", rec["cost_usd"], flush=True)
    by_key = {r["key"]: r for r in rows}
    stats, cost = {}, 0.0
    with open(os.path.join(args.out_dir, "m2.jsonl"), "w") as f:
        for name in sorted(os.listdir(args.out_dir)):
            if not (name.startswith("batch_") and name.endswith(".json")):
                continue
            rec = json.load(open(os.path.join(args.out_dir, name)))
            cost += rec["cost_usd"] or 0
            plans = dict(PLAN.findall(rec["reply"] or ""))
            for key in rec["keys"]:
                if key not in by_key:
                    continue
                r = by_key[key]
                units, seps = split_units(r["output"])
                out = {"id": r["id"], "sample": r["sample"], "status": None, "response": None, "decisions": None, "check": None}
                if rec["is_error"] or key not in plans:
                    out["status"] = "call_error" if rec["is_error"] else "missing"
                else:
                    try:
                        blocks, edits = parse_plan(plans[key], len(units))
                        if not blocks:
                            out["status"] = "no_block"
                        else:
                            out["response"], out["decisions"] = assemble(units, seps, blocks, edits)
                            if out["response"] is None:
                                out["status"] = "filtered"
                            else:
                                out["check"] = check(out["response"], r["answer"], r["source"], original=r["output"])
                                out["status"] = "ok" if out["check"]["ok"] else "rejected"
                    except PlanError as e:
                        out["status"], out["error"] = "plan_error", str(e)
                stats[out["status"]] = stats.get(out["status"], 0) + 1
                f.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({"answers": len(rows), **stats, "cost_usd": round(cost, 2)}))


if __name__ == "__main__":
    main()
