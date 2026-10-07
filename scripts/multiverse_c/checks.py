"""Variant C: automatic checks of a converted trace (pure Python; token length and the verl mask are checked in check_mask.py).

check_sample(original, response, units, blocks) -> {"ok", "issues", "stats", ...}
- grammar: <Parallel><Goal><Outline>i: ..</Outline>{2,}</Goal><Path>i: ..</Path>{same count}<Conclusion>..</Conclusion></Parallel>,
  only whitespace between structural elements, nested <Parallel> only inside a <Path>, depth <= 2, numbering 1..k / k.1..k.m,
  all tags inside <think>, nothing tagged after </think>;
- answer after </think> byte-identical to the original; text outside blocks identical (by construction, verified);
- faithfulness per block: word-level similarity of original units vs paths+sequential text (tags, outlines, conclusion, "k:" removed),
  share of original lines kept verbatim, numbers/formulas kept;
- independence heuristics: sibling references at a path start or inside ("similarly", "as in path 1", ...).
"""
import collections
import difflib
import re

TAG = re.compile(r"<(/?)(Parallel|Goal|Outline|Path|Conclusion)>")
SIBLING = re.compile(r"(?i)\b(similarly|likewise|alternatively|as before|as above|as in (?:case|path|part) \d|"
                     r"(?:the )?(?:previous|other|first|second|earlier) (?:path|case|branch)|path \d)\b")
START_CONNECTIVE = re.compile(r"(?i)^\s*(?:\d+(?:\.\d+)?:\s*)(similarly|now|next|then|also|alternatively|again|finally|moving on)\b")
MIN_SIMILARITY = 0.8  # Multiverse content check: edit-distance ratio <= 0.2


class GrammarError(Exception):
    pass


def parse_blocks(text):
    """Parse all top-level parallel blocks of a thinking text; returns list of block dicts (nested in paths)."""
    toks = [(m.start(), m.end(), m.group(1) == "/", m.group(2)) for m in TAG.finditer(text)]
    pos = [0]

    def expect(close, name):
        if pos[0] >= len(toks):
            raise GrammarError(f"expected {'</' if close else '<'}{name}>, got end")
        t = toks[pos[0]]
        if (t[2], t[3]) != (close, name):
            raise GrammarError(f"expected {'</' if close else '<'}{name}> at {t[0]}, got {'</' if t[2] else '<'}{t[3]}>")
        pos[0] += 1
        return t

    def between(a, b):
        if text[a:b].strip():
            raise GrammarError(f"text between structural tags at {a}: {text[a:b].strip()[:60]!r}")

    def block(depth, prefix):
        if depth > 2:
            raise GrammarError("nesting deeper than 2")
        p0 = expect(False, "Parallel")
        g0 = expect(False, "Goal")
        between(p0[1], g0[0])
        outlines, last = [], g0[1]
        while pos[0] < len(toks) and toks[pos[0]][2:] == (False, "Outline"):
            o0 = expect(False, "Outline")
            between(last, o0[0])
            o1 = expect(True, "Outline")
            outlines.append(text[o0[1]:o1[0]])
            last = o1[1]
        g1 = expect(True, "Goal")
        between(last, g1[0])
        paths, last = [], g1[1]
        while pos[0] < len(toks) and toks[pos[0]][2:] == (False, "Path"):
            a0 = expect(False, "Path")
            between(last, a0[0])
            children = []
            k = len(paths) + 1
            while pos[0] < len(toks) and toks[pos[0]][2:] == (False, "Parallel"):
                children.append(block(depth + 1, f"{prefix}{k}."))
            a1 = expect(True, "Path")
            paths.append({"text": text[a0[1]:a1[0]], "span": (a0[0], a1[1]), "children": children})
            last = a1[1]
        c0 = expect(False, "Conclusion")
        between(last, c0[0])
        c1 = expect(True, "Conclusion")
        p1 = expect(True, "Parallel")
        between(c1[1], p1[0])
        if len(outlines) < 2 or len(outlines) != len(paths):
            raise GrammarError(f"{len(outlines)} outlines, {len(paths)} paths (need equal and >= 2)")
        for i, (o, p) in enumerate(zip(outlines, paths), 1):
            want = f"{prefix}{i}:"
            if not o.strip().startswith(want) or not p["text"].strip().startswith(want):
                raise GrammarError(f"outline/path {want} numbering mismatch")
        return {"outlines": outlines, "paths": paths, "conclusion": text[c0[1]:c1[0]], "span": (p0[0], p1[1]),
                "depth": depth}

    blocks = []
    while pos[0] < len(toks):
        if toks[pos[0]][2:] != (False, "Parallel"):
            t = toks[pos[0]]
            raise GrammarError(f"stray {'</' if t[2] else '<'}{t[3]}> at {t[0]}")
        blocks.append(block(1, ""))
    return blocks


def strip_structure(text):
    """Sequential text + path texts of a replacement, without tags, outlines, conclusions, numbering prefixes."""
    text = re.sub(r"<Goal>.*?</Goal>", "", text, flags=re.S)
    text = re.sub(r"<Conclusion>.*?</Conclusion>", "", text, flags=re.S)
    text = re.sub(r"<Path>\s*\d+(?:\.\d+)*:\s*", " ", text)
    return TAG.sub(" ", text)


def words(text):
    return re.findall(r"\S+", text)


def math_atoms(text):
    """Numbers and compact formula pieces; a multiset to compare original and rewrite."""
    return collections.Counter(re.findall(r"\d+(?:\.\d+)?|[=<>≤≥±√]", text))


def walk(blocks):
    for b in blocks:
        yield b
        for p in b["paths"]:
            yield from walk(p["children"])


def check_sample(original, response, units, blocks):
    issues, stats = [], {}
    orig = original.replace("<|im_end|>", "").replace("<|endoftext|>", "")
    if orig.split("</think>", 1)[1] != response.split("</think>", 1)[1]:
        issues.append("answer_changed")
    if response.count("</think>") != 1:
        issues.append("think_tags")
    think = response.split("</think>", 1)[0]
    if TAG.search(response.split("</think>", 1)[1]):
        issues.append("tags_after_think")
    try:
        parsed = parse_blocks(think)
    except GrammarError as e:
        issues.append(f"grammar: {e}")
        parsed = []
    if not blocks:
        issues.append("no_blocks")
    # faithfulness per replaced range
    sims, kept_lines, atoms_lost = [], [], 0
    for a, b, text in blocks:
        src = "\n\n".join(units[a - 1:b])
        dst = strip_structure(text)
        sm = difflib.SequenceMatcher(None, words(src), words(dst), autojunk=False)
        sims.append(round(sm.ratio(), 3))
        lines = [ln.strip() for ln in src.splitlines() if len(ln.strip()) > 20]
        kept_lines.append(round(sum(ln in text for ln in lines) / max(len(lines), 1), 3))
        lost = math_atoms(src) - math_atoms(dst)
        atoms_lost += sum(lost.values())
        if "<Parallel>" not in text:
            issues.append(f"block {a}-{b} without <Parallel>")
    if sims and min(sims) < MIN_SIMILARITY:
        issues.append(f"low_similarity {min(sims)}")
    if atoms_lost:
        issues.append(f"math_atoms_lost {atoms_lost}")
    # independence heuristics
    flags = []
    for blk in walk(parsed):
        for p in blk["paths"]:
            t = p["text"]
            if START_CONNECTIVE.search(t):
                flags.append(f"path starts with connective: {t.strip()[:50]!r}")
            for m in SIBLING.finditer(t):
                flags.append(f"sibling word {m.group(0)!r}")
    if flags:
        issues.append(f"independence_flags {len(flags)}")
    allb = list(walk(parsed))
    path_chars = sum(len(p["text"]) for b in parsed for p in b["paths"])
    saved = sum(sum(len(p["text"]) for p in b["paths"]) - max(len(p["text"]) for p in b["paths"]) for b in allb)
    stats = {"blocks_top": len(parsed), "blocks_all": len(allb), "max_depth": max((b["depth"] for b in allb), default=0),
             "paths_per_block": [len(b["paths"]) for b in allb], "similarity": sims, "lines_kept": kept_lines,
             "math_atoms_lost": atoms_lost, "share_chars_in_paths": round(path_chars / max(len(think), 1), 3),
             "share_chars_saved_by_parallel(approx)": round(saved / max(len(think), 1), 3),
             "path_chars": [len(p["text"]) for b in allb for p in b["paths"]], "independence_flags": flags[:10]}
    hard = [i for i in issues if not i.startswith("independence_flags")]
    return {"ok": not hard, "issues": issues, "stats": stats}
