"""Deterministic quality checks of exp 21 parallel examples (both methods) and answer verification.

check(response, gold, source, original=None) -> dict(ok, issues, blocks, ...):
  grammar      every tag inside a grammatical block (mv_format.parse), numbering 1:, 2:, ... in outlines and paths, depth 1
  answer       a "Final Answer:" line after the last block, verified against the reference (math_verify, else normalized string)
  answer_first the final answer is not stated before the first block (no Final Answer / \\boxed{} / "answer is <gold>" before it)
  xref         no path points to a sibling ("similarly", "the other case", "path 1", "as above", ...)
  paths        every path >= 80 characters of real text, shortest >= 0.15 of the longest, no near-duplicate paths (3-gram Jaccard >= 0.7)
  outline      outline texts do not contain the final answer; conclusion not empty
  recheck      the conclusion or an outline says the methods agree / verifies (verification, not decomposition)
  verbatim     (M2, original given) removing tags, outlines, conclusion and path numbers recovers the model's answer
               exactly except whitespace; no word, formula or number can change
  length       <= 2048 Qwen3 tokens (counted by the caller) is checked where the tokenizer is available
"""
import re

from math_verify import parse as mv_parse_answer, verify

try:
    from .mv_format import ANY_TAG, PATH, parse  # noqa: F401
except ImportError:
    from mv_format import ANY_TAG, PATH, parse  # noqa: F401

XREF = re.compile(r"\b(?:similarly|likewise|as before|as above|as in (?:the )?(?:other|previous|first|second)|the other (?:case|path|part|one)|"
                  r"(?:path|part) [1-9]\b|previous path|other path|from (?:the )?(?:first|second) (?:path|part)|"
                  r"(?:same|analogous(?:ly)?) (?:as|to) (?:before|above))", re.I)
RECHECK = re.compile(r"\b(?:both|all|the two|each of the) (?:methods|approaches|paths|ways|computations)\b|\b(?:agree|confirms?|consistent|verif(?:y|ies|ication)|check(?:s|ing)? (?:the|that|this))\b", re.I)
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")


def candidate(answer_text):
    from_boxed = re.findall(r"\\boxed\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", answer_text)
    parts = re.split(r"(?i)final answer\s*:", answer_text)
    if len(parts) > 1:
        lines = [ln for ln in parts[-1].splitlines() if ln.strip()]
        cand = lines[0] if lines else ""
    elif from_boxed:
        cand = from_boxed[-1]
    else:
        return ""
    cand = cand.strip().strip("$").strip().rstrip(".").strip("*").strip()
    box = re.fullmatch(r"\\boxed\{(.*)\}", cand)
    return box.group(1) if box else cand


def norm(t):
    t = t.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\left", "").replace("\\right", "").replace("$", "")
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    return re.sub(r"\s+", "", t).rstrip(".").lower()


def correct(gold, cand, source):
    if not cand:
        return False
    if source == "arc":
        m = re.match(r"\(?([A-J])\b", cand.strip())
        return bool(m) and m.group(1) == gold
    if norm(gold) == norm(cand):
        return True
    try:
        return bool(verify(mv_parse_answer(f"${gold}$"), mv_parse_answer(f"${cand}$")))
    except Exception:
        return False


def _ngrams(t, n=3):
    w = re.findall(r"\w+", t.lower())
    return {tuple(w[i:i + n]) for i in range(max(len(w) - n + 1, 0))}


def stated_before(text, gold):
    """The final answer stated as a result in `text` (Final Answer line, boxed, or 'answer is/= gold')."""
    if re.search(r"(?i)final answer\s*:|\\boxed\{", text):
        return True
    g = norm(gold)
    if len(g) < 1:
        return False
    return any(norm(s).endswith(("answer" + "is" + g, "answer=" + g, "answer:" + g)) for s in re.split(r"(?<=[.!?])\s+|\n", text))


def check(response, gold, source, original=None):
    issues = []
    r = parse(response)
    if not r["blocks"]:
        return {"ok": False, "issues": ["no_block"], "blocks": 0}
    if not r["valid"]:
        issues.append("grammar")
    if not all(b["numbered"] for b in r["blocks"]):
        issues.append("numbering")
    first, last = r["blocks"][0]["start"], r["blocks"][-1]["end"]
    after = response[last:]
    cand = candidate(after)
    if not re.search(r"(?i)final answer\s*:", after):
        issues.append("no_final_answer_after_block")
    elif not correct(gold, cand, source):
        issues.append("wrong_answer")
    if stated_before(response[:first], gold):
        issues.append("answer_first")
    for b in r["blocks"]:
        paths = [re.sub(r"^\s*\d+\s*:", "", p).strip() for p in b["paths"]]
        lens = [len(p) for p in paths]
        if min(lens) < 80:
            issues.append("short_path")
        if min(lens) < 0.15 * max(lens):
            issues.append("unbalanced")
        if any(XREF.search(p) for p in paths):
            issues.append("xref")
        grams = [_ngrams(p) for p in paths]
        if any(len(a & c) / max(len(a | c), 1) >= 0.7 for i, a in enumerate(grams) for c in grams[i + 1:]):
            issues.append("near_duplicate_paths")
        if any(norm(gold) and norm(gold) in norm(o) and len(norm(gold)) >= 2 for o in b["outlines"]):
            issues.append("answer_in_outline")
        if not b["conclusion"].strip():
            issues.append("empty_conclusion")
        if RECHECK.search(b["conclusion"]) or any(RECHECK.search(o) for o in b["outlines"]):
            issues.append("recheck")  # the conclusion says the methods agree: a verification, not a decomposition
    if original is not None:
        body = re.sub(r"<Goal>.*?</Goal>|<Conclusion>.*?</Conclusion>", "", response, flags=re.S)
        body = ANY_TAG.sub("", re.sub(r"<Path>\s*\d+\s*:", "", body))
        if re.sub(r"\s+", "", body) != re.sub(r"\s+", "", original):
            issues.append("text_changed")
        nums = lambda t: sorted(NUM.findall(re.sub(r"Step\s*\d+", "Step", t)))  # noqa: E731  "Step k" labels may be dropped in paths
        if nums(body) != nums(original):
            issues.append("numbers_changed")
    issues = sorted(set(issues))
    return {"ok": not issues, "issues": issues, "blocks": len(r["blocks"]), "paths": [len(b["paths"]) for b in r["blocks"]],
            "candidate": cand}
