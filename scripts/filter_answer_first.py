"""Answer-first filter for the Parallel-R1 SFT parquet, plus a dev split and structure/length matched random controls.

A well-formed row is `answer_first` when, before some <Parallel> block, the sequential text (prefix spans and earlier
Summaries, never Paths) explicitly states the final value for the asked quantity, nothing new is derived in sequential
text after that statement, and the block only repeats: a Path contains the final value, or every Path ends at a value
that was already known. A number merely appearing earlier is not enough; such rows are `ambiguous`: kept by the
`filtered` arm, dropped by `filtered_broad` (which keeps only `clean`). Malformed rows are dropped from every arm.
Retained rows are written unchanged, in the input schema. The dev split is assigned by problem group before filtering;
`dev_untouched` also drops the problem groups of dev rows inspected during filter tuning.
Each random control keeps, label-blind, as many control_full rows as its filtered arm in every (length decile,
blocks, Paths) stratum.

Usage: python scripts/filter_answer_first.py <sft train.parquet> <tokenizer.json> <out_dir> [--dev-percent 5] [--seed 0]
Writes <out_dir>/{dev,dev_untouched,control_full,filtered,random_control,filtered_broad,random_control_broad}.parquet,
rows.csv (one line per input row: split, label, reason, evidence, arm membership) and summary.json.
"""
import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter
from decimal import Decimal
from pathlib import Path

from tag_validator import BLOCK, TAG

FINAL = re.compile(r"Final Answer:\s*([0-9][0-9,]*(?:\.[0-9]+)?)\.?\s*$")
NUM = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?!\w|[.,]\d)")
PATH = re.compile(r"<Path>(.*?)</Path>", re.S)
SUMMARY = re.compile(r"<Summary>(.*?)</Summary>", re.S)
SENTENCE = re.compile(r"\n|(?<=[.!?])\s+")
STATES = re.compile(r"(?:=|\b(?:is|are|was|were|be|equals?|totals?|makes?|gives?|gets?|get|has|have|had|needs?|takes?|of|to|"
                    r"costs?|spends?|spent|earns?|earned|sells?|sold|pays?|paid|saves?|saved|weighs?)|(?<!\d):)"
                    r"\s*(?:about |approximately |only |exactly |a total of |still )?\$?\s*$", re.I)
OPERAND = re.compile(r"\s*(?:[-+*/×÷x=]\s*[\d$(\\]|%|\\(?:times|cdot|div)\b)")
RATE = re.compile(r"\s*(?:[a-z]+\s+)?per\b", re.I)
DEFINITION = re.compile(r"\b[Ll]et\s+([A-Za-z])\s+(?:be|=|represents?|denotes?)\s+([^.\n]*)")
HYPOTHETICAL = re.compile(r"\?|\b(?:if|suppose|assum\w*|guess\w*|try|trying|maybe|perhaps|might)\b", re.I)
WORD_NUMBERS = dict(zip("""one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen
sixteen seventeen eighteen nineteen twenty""".split(), range(1, 21))) | {"thirty": 30, "forty": 40, "fifty": 50,
                                                                          "hundred": 100, "dozen": 12}
STOP = set("""a an the of to in on at for by with from and or but if then than that this these those it its he she they
him her them his their we you i do does did is are was were be been will would can could should must has have had
how many much what which who whom whose when where why there here each per all any some more most total""".split())
REQUIRED = {"index", "output", "data_source", "prompt", "ability", "reward_model", "extra_info"}
EXTRA = {"answer", "index", "question", "reward_method", "split"}
TAGS = ["<Parallel>", "</Parallel>", "<Path>", "</Path>", "<Summary>", "</Summary>"]
INSPECTED_DEV_ROWS = {179}  # extra_info.index of the dev row read in the 2026-10-05 audit, before the split existed


def value(text):
    return Decimal(text.replace(",", "")).normalize()


def numbers(text):
    return {value(m.group()) for m in NUM.finditer(text)}


def stem(word):
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith(("ches", "shes", "sses", "xes")):
        return word[:-2]
    return word[:-1] if len(word) > 3 and word.endswith("s") and not word.endswith("ss") else word


def tokens(text):
    return {stem(w) for w in re.findall(r"[a-z]+", text.lower())}


def words(text):
    return tokens(text) - STOP


def problem(question):
    return question.split("Problem:", 1)[1].strip()


def given(problem_text):
    """Numbers stated in the problem, digits or number words."""
    spelled = {Decimal(WORD_NUMBERS[w]) for w in re.findall(r"[a-z]+", problem_text.lower()) if w in WORD_NUMBERS}
    return numbers(problem_text) | spelled


def ask(problem_text):
    """Content words of the question sentence and words of the asked quantity after 'how many/much'."""
    sentence = next((s for s in reversed(SENTENCE.split(problem_text)) if "?" in s), problem_text)
    head = re.search(r"\bhow (?:many|much)\s+(?:more |additional |extra )?(?:of (?:the |her |his |their )?)?"
                     r"((?:[a-z-]+\s+){0,3})", sentence, re.I)
    head_words = set()
    for w in (head.group(1).lower().split() if head else []):  # noun phrase: up to a stop word or the first plural
        if w in STOP - {"can"}:
            break
        head_words.add(stem(w))
        if w.endswith("s") and not w.endswith("ss"):
            break
    return words(sentence), head_words


def parse(answer):
    """Split a well-formed answer into [('text', s) | ('block', paths, summary)], or return (None, reject reason)."""
    if "<Parallel>" not in answer:
        return None, "no_parallel"
    blocks = list(BLOCK.finditer(answer))
    if sum(len(TAG.findall(b.group())) for b in blocks) != len(TAG.findall(answer)):
        return None, "malformed_tags"
    if answer.count("Final Answer:") != 1 or not FINAL.search(answer.rstrip().splitlines()[-1]):
        return None, "final_answer_not_last_line"
    parts, end = [], 0
    for b in blocks:
        paths, summary = PATH.findall(b.group()), SUMMARY.search(b.group()).group(1)
        if not all(p.strip() for p in paths) or not summary.strip():
            return None, "empty_path_or_summary"
        parts += [("text", answer[end:b.start()]), ("block", paths, summary)]
        end = b.end()
    if "Final Answer:" not in answer[end:]:
        return None, "final_answer_not_last_line"
    return parts + [("text", answer[end:])], None


class Target:
    """What the problem asks for: the final value and the words/variables that name the asked quantity."""

    def __init__(self, question, answer):
        text = problem(question)
        self.final = value(FINAL.search(answer.rstrip().splitlines()[-1]).group(1))
        self.given = given(text)
        self.ask_words, self.head_words = ask(text)
        self.asks_rate = bool(re.search(r"\bper\b|\beach\b|\brate\b|\baverage\b", text.split(".")[-1], re.I))
        self.variables = {m.group(1) for m in DEFINITION.finditer(answer) if self.grounded(m.group(2))}

    def grounded(self, text):
        return bool(self.head_words and self.head_words <= tokens(text) or len(self.ask_words & words(text)) >= 2)

    def stated_in(self, sentence, previous):
        """`sentence` asserts the final value as the asked quantity, not as an operand, hypothesis, given or other entity."""
        if HYPOTHETICAL.search(sentence):
            return False
        for m in NUM.finditer(sentence):
            before, after = sentence[:m.start()], sentence[m.end():]
            if value(m.group()) != self.final or OPERAND.match(after) or numbers(after) - numbers(before) - self.given:
                continue
            if RATE.match(after) and not self.asks_rate:
                continue
            if self.final in self.given and not re.search(r"=\s*\$?\s*$", before):
                continue
            copula = STATES.search(before) and self.grounded(previous + " " + sentence)
            names_quantity = self.head_words and self.head_words <= tokens(" ".join(after.split()[:4]))
            assigned = self.variables and re.search(rf"\b(?:{'|'.join(self.variables)})\s*=[^=a-zA-Z]*=?\s*\$?\s*$", before)
            if copula or names_quantity or assigned:
                return True
        return False


def answer_first(question, parts):
    """Return (label, reason, 1-based block, evidence) for a parsed answer."""
    target = Target(question, "".join(p[1] for p in parts if p[0] == "text"))
    final = target.final
    known, evidence, ambiguous, seen = set(target.given), None, None, {"sequential": False, "path": False}

    def read(text, where):
        nonlocal evidence, known
        previous = ""
        for s in filter(str.strip, SENTENCE.split(text)):
            if target.stated_in(s, previous):
                evidence = f"[{where}] {s.strip()}"
            elif evidence and numbers(s) - known - {final}:
                evidence = None  # something new was derived after the statement: it was not the answer yet
            known |= numbers(s)
            seen["sequential"] |= final in numbers(s)
            previous = s

    block = 0
    for part in parts:
        if part[0] == "text":
            read(part[1], "prefix")
            continue
        block += 1
        paths, summary = part[1], part[2]
        path_results = {value(NUM.findall(p)[-1]) for p in paths if NUM.findall(p)}
        if evidence and (any(final in numbers(p) for p in paths) or path_results <= known):
            return "answer_first", "block1" if block == 1 else "later_block", block, evidence
        if ambiguous is None and final not in target.given:
            if evidence:
                ambiguous = ("stated_then_block_reaches_new_value", block, evidence)
            elif seen["sequential"]:
                ambiguous = ("value_in_sequential_text_not_explicit_answer", block, "")
            elif seen["path"]:
                ambiguous = ("value_only_in_earlier_path", block, "")
        seen["path"] |= any(final in numbers(p) for p in paths)
        known |= {n for p in paths for n in numbers(p)}
        read(summary, "summary")
    return ("ambiguous", *ambiguous) if ambiguous else ("clean", "", 0, "")


def check_schema(rows, columns):
    """Fail closed on anything this filter was not written for."""
    if set(columns) != REQUIRED:
        raise SystemExit(f"unsupported columns: {sorted(columns)}")
    for r in rows:
        info = r["extra_info"]
        if set(info) != EXTRA or info["question"].count("Problem:") != 1:
            raise SystemExit(f"unsupported extra_info in source index {r['index']}")
        if r["prompt"] != [{"content": info["question"], "role": "user"}]:
            raise SystemExit(f"prompt differs from extra_info.question in source index {r['index']}")
    if len({r["index"] for r in rows}) != len(rows):
        raise SystemExit("source index is not unique")


def group_key(question):
    """Problem text with numbers masked: number-variants of one problem land in one split."""
    return re.sub(r"\d[\d,.]*", "#", " ".join(problem(question).lower().split()))


def stratifier(control):
    """Stratum of a row: target-length decile of `control`, number of Parallel blocks (4+ pooled), Paths (6+ pooled)."""
    lengths = sorted(m["target_tokens"] for m in control)
    edges = [lengths[len(lengths) * q // 10] for q in range(1, 10)]
    return lambda m: (sum(m["target_tokens"] >= e for e in edges), min(m["parallel_blocks"], 4), min(m["paths"], 6)), edges


def matched_random_keep(control, kept, seed):
    """Random rows of `control`, as many as `kept` has in every stratum; labels are not used. Feasible: kept ⊆ control."""
    stratum, _ = stratifier(control)
    rng, keep = random.Random(seed), set()
    for s, need in sorted(Counter(map(stratum, kept)).items()):
        keep |= set(rng.sample(sorted(m["row"] for m in control if stratum(m) == s), need))
    return [m["row"] for m in control if m["row"] in keep]


def untouched(dev, inspected):
    """Dev rows outside the problem groups of the `inspected` rows, which were read while tuning the filter."""
    if not inspected <= {m["row"] for m in dev}:
        raise SystemExit("an inspected row is not a well-formed dev row")
    groups = {m["group"] for m in dev if m["row"] in inspected}
    return [m["row"] for m in dev if m["group"] not in groups]


def main():
    import pyarrow.parquet as pq
    from tokenizers import AddedToken, Tokenizer

    parser = argparse.ArgumentParser()
    parser.add_argument("parquet")
    parser.add_argument("tokenizer")
    parser.add_argument("out_dir")
    parser.add_argument("--dev-percent", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    table = pq.read_table(args.parquet)
    rows = table.to_pylist()
    check_schema(rows, table.column_names)
    tokenizer = Tokenizer.from_file(args.tokenizer)
    tokenizer.add_special_tokens([AddedToken(t, special=True, normalized=False) for t in TAGS])

    manifest = []
    for i, r in enumerate(rows):
        info = r["extra_info"]
        key = group_key(info["question"])
        dev = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 100 < args.dev_percent  # split before any filtering
        parts, malformed = parse(info["answer"])
        label, reason, block, evidence = ("malformed", malformed, 0, "") if malformed else answer_first(info["question"], parts)
        manifest.append({"row": i, "source_index": r["index"], "split": "dev" if dev else "train", "label": label,
                         "reason": reason, "block": block, "parallel_blocks": info["answer"].count("<Parallel>"),
                         "paths": info["answer"].count("<Path>"),
                         "target_tokens": len(tokenizer.encode(info["answer"]).ids),
                         "prompt_tokens": len(tokenizer.encode(info["question"]).ids), "evidence": evidence, "group": key})
    splits_of_group = {}
    for m in manifest:
        splits_of_group.setdefault(m["group"], set()).add(m["split"])
    if any(len(s) > 1 for s in splits_of_group.values()):
        raise SystemExit("a problem group is in both splits")

    ok = [m for m in manifest if m["label"] != "malformed"]
    control = [m for m in ok if m["split"] == "train"]
    filtered = [m for m in control if m["label"] != "answer_first"]  # high precision
    filtered_broad = [m for m in control if m["label"] == "clean"]  # also drops `ambiguous`: more recall, less precision
    dev = [m for m in ok if m["split"] == "dev"]
    arms = {"dev": [m["row"] for m in dev],
            "dev_untouched": untouched(dev, INSPECTED_DEV_ROWS),
            "control_full": [m["row"] for m in control],
            "filtered": [m["row"] for m in filtered],
            "random_control": matched_random_keep(control, filtered, args.seed),
            "filtered_broad": [m["row"] for m in filtered_broad],
            "random_control_broad": matched_random_keep(control, filtered_broad, args.seed)}
    stratum, edges = stratifier(control)
    for a, b in [("filtered", "random_control"), ("filtered_broad", "random_control_broad")]:
        if Counter(stratum(manifest[i]) for i in arms[a]) != Counter(stratum(manifest[i]) for i in arms[b]):
            raise SystemExit(f"{b} does not match {a} in every stratum")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, ids in arms.items():
        pq.write_table(table.take(ids), out / f"{name}.parquet")
        members = set(ids)
        for m in manifest:
            m[name] = m["row"] in members
    with open(out / "rows.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    tokens = [m["target_tokens"] for m in manifest]
    summary = {
        "input": str(args.parquet), "rows": len(rows), "dev_percent": args.dev_percent, "seed": args.seed,
        "problem_groups": len(splits_of_group), "rows_in_multi_row_groups": sum(
            Counter(m["group"] for m in manifest)[m["group"]] > 1 for m in manifest),
        "by_split_label_reason": dict(sorted(Counter(f"{m['split']}/{m['label']}/{m['reason']}" for m in manifest).items())),
        "length_decile_edges_target_tokens": edges,
        "dev_untouched_excluded": [{k: manifest[i][k] for k in ("row", "source_index", "label")}
                                   for i in sorted(set(arms["dev"]) - set(arms["dev_untouched"]))],
        "random_control_dropped_by_label": Counter(m["label"] for m in control if not m["random_control"]),
        "random_control_broad_dropped_by_label": Counter(m["label"] for m in control if not m["random_control_broad"]),
        "arms": {name: {"rows": len(ids), "target_tokens": sum(tokens[i] for i in ids),
                        "parallel_blocks": dict(sorted(Counter(manifest[i]["parallel_blocks"] for i in ids).items())),
                        "paths": dict(sorted(Counter(manifest[i]["paths"] for i in ids).items()))}
                 for name, ids in arms.items()},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
