#!/usr/bin/env python3
"""Preview unseen questions with two plausible independent solution parts.

CPU only. This is a question shortlist, not a source of solutions or labels.
Run from any directory: python scripts/exp21/build_structurally_parallel_pool.py
"""

import json
import re
import tarfile
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
POOL = DATA / "pool.jsonl"
OUT = DATA / "structurally_parallel_pool_preview.jsonl"
FULL_TRAIN = DATA / "qwen4b_onpolicy189_clean46_tagged_train.parquet"
SOURCES = {
    "clean46_positive": RUN / "audit/qwen4b_onpolicy189_clean46_manifest.json",
    "onpolicy143": DATA / "clean46_onpolicy_nonpositive_candidates.jsonl",
    "fixed40": RUN / "eval_archives/qwen4b_init_fixed40.tgz",
    "fresh_holdout40": RUN / "holdout40",
    "clean46_val": DATA / "qwen4b_onpolicy189_clean46_tagged_val.parquet",
}
MANUAL_REJECT = {
    # Read without gold answers; these have one sequential target or a duplicate structure.
    "gsm8k-train/2496", "gsm8k-train/4423", "gsm8k-train/6261",
    "gsm8k-train/1997", "gsm8k-train/3299", "gsm8k-train/4556",
    "gsm8k-train/4815", "gsm8k-train/5614", "gsm8k-train/1889",
    "gsm8k-train/3501", "gsm8k-train/4895", "gsm8k-train/7371",
    "gsm8k-train/6024", "gsm8k-train/2014",
    "math-train/1017", "math-train/6345", "math-train/2082",
    "math-train/1339", "math-train/2719", "math-train/1937",
    "math-train/2685",
}


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split()).casefold()


def bare_question(text):
    text = str(text).rsplit("Problem:", 1)[-1]
    return text.split("<|im_end|>", 1)[0].split("<|endoftext|>", 1)[0]


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def add(group, identifier, question):
    group["ids"].add(str(identifier))
    group["texts"].add(normalize(bare_question(question)))


def exclusions():
    groups = {name: {"ids": set(), "texts": set()} for name in SOURCES}
    positives = json.loads(SOURCES["clean46_positive"].read_text())["accepted_ids"]
    if len(positives) != 46 or len(set(positives)) != 46:
        raise ValueError("clean46 positive manifest must contain 46 distinct IDs")
    pool_by_id = {row["id"]: row for row in load_jsonl(POOL)}
    for identifier in positives:
        add(groups["clean46_positive"], identifier, pool_by_id[identifier]["question"])

    onpolicy = load_jsonl(SOURCES["onpolicy143"])
    if len(onpolicy) != 143 or len({row["id"] for row in onpolicy}) != 143:
        raise ValueError("onpolicy143 file must contain 143 distinct IDs")
    for row in onpolicy:
        add(groups["onpolicy143"], row["id"], row["question"])

    with tarfile.open(SOURCES["fixed40"]) as archive:
        members = sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl"))
        if len(members) != 4:
            raise ValueError("fixed40 archive must have four block-row files")
        for name in members:
            for line in archive.extractfile(name):
                row = json.loads(line)
                add(groups["fixed40"], row["problem_id"], row["problem"])

    holdout = SOURCES["fresh_holdout40"]
    manifest = json.loads((holdout / "manifest.json").read_text())
    for source in ("gsm8k", "math"):
        selected = manifest["sources"][source]["selected_ids"]
        frame = pd.read_parquet(holdout / f"{source}_holdout20.parquet")
        if len(selected) != 20 or len(frame) != 20:
            raise ValueError(f"{source} fresh holdout must have 20 rows")
        for identifier in selected:
            groups["fresh_holdout40"]["ids"].add(identifier)
        for row in frame.itertuples():
            add(groups["fresh_holdout40"], row.extra_info["id"], row.prompt[0]["content"])

    val = pd.read_parquet(SOURCES["clean46_val"])
    if len(val) != 50:
        raise ValueError("clean46 val must have 50 rows")
    for row in val.itertuples():
        add(groups["clean46_val"], row.id, row.extra_info["question"])
    return groups


def pattern(row):
    """Conservative structural cues; never inspect gold answer text."""
    question = row["question"]
    q = question.casefold()
    numbers = len(re.findall(r"(?<![a-z])\d+(?:\.\d+)?", q))
    if len(q) < 95 or numbers < 2:
        return None
    combine = bool(re.search(r"\b(total|altogether|combined|in all|difference|more than|less than|how much longer|probability|area|sum|ratio|percent)\b", q))
    if not combine:
        return None
    if row["source"] == "gsm8k":
        if numbers < 4:
            return None
        final = re.split(r"(?<=[.!?])\s+", q.strip())[-1]
        if not re.search(r"\b(total|altogether|combined|in all|difference)\b|\b(more|less)\b.*\bthan\b|how much.*\b(spend|cost|pay)\b|how many.*\b(points|capsules|apples|liters|hours|minutes|towels)\b", final):
            return None
        if re.search(r"\b(first|second|third|fourth) hour\b", q) and "more" in q:
            return None
        if re.search(r"\bwhat price\b|\bhow much[^?]*\beach\b", final):
            return None
        unit_rates = len(re.findall(r"\b(each|per|apiece|every)\b", q))
        money = len(re.findall(r"\$\s*\d|\b(dollars?|cents?|costs?|prices?|spends?)\b", q))
        time = len(re.findall(r"\b(hours?|minutes?|days?|weeks?|months?)\b", q))
        if "respectively" in q and (unit_rates or money or time):
            family, score = "paired_respectively", 9
        elif money >= 3 and unit_rates >= 2:
            family, score = "separate_costs", 8
        elif time >= 3 and unit_rates >= 2:
            family, score = "separate_durations", 8
        elif re.search(r"\b(how many|how much) (more|less)\b", q) and unit_rates >= 1:
            family, score = "compare_quantities", 7
        elif unit_rates >= 2 and numbers >= 5 and re.search(r"\b(two|three|both|different|types|kinds|groups)\b", q):
            family, score = "separate_groups", 6
        else:
            return None
        if re.search(r"\b(after|then|remaining|left over|half as many|twice as many)\b", q):
            score -= 2  # sequential dependence is a common false positive
        return family, score + min(numbers, 8) / 20

    if row["source"] != "math":
        return None
    if re.search(r"(\\begin\{cases\}|\\left\\\{|piecewise)", q) and "continuous" in q and q.count("\\text{if") >= 3:
        family, score = "two_continuity_boundaries", 10
    elif "shaded" in q and ("area" in q or "percent" in q) and "[asy]" in q and len(re.findall(r"\bfill(?:draw)?\s*\(", q)) >= 2:
        family, score = "separate_shaded_regions", 9
    elif re.search(r"(\\left\||\\lvert|absolute value)", q) and re.search(r"\b(solve|solutions|values|integers)\b", q):
        family, score = "absolute_value_cases", 8
    elif "probability" in q and re.search(r"\b(either|or|both|neither)\b", q) and numbers >= 3:
        family, score = "probability_cases", 7
    elif "remainder" in q and re.search(r"x\^2|quadratic", q):
        family, score = "two_remainder_constraints", 7
    elif "perimeter" in q and "area" in q and numbers >= 3:
        family, score = "independent_dimensions", 6
    elif "ratio" in q and "area" in q and "triangle" in q and numbers >= 3:
        family, score = "compare_regions", 6
    else:
        return None
    return family, score + min(numbers, 8) / 20


def main():
    rows = load_jsonl(POOL)
    if len(rows) != 16547 or len({row["id"] for row in rows}) != len(rows):
        raise ValueError("expected 16,547 distinct leakchecked pool IDs")
    blocked = exclusions()
    hits = Counter()
    eligible = []
    for row in rows:
        text = normalize(row["question"])
        reasons = [name for name, group in blocked.items()
                   if row["id"] in group["ids"] or text in group["texts"]]
        hits.update(reasons)
        if not reasons and row["id"] not in MANUAL_REJECT:
            match = pattern(row)
            if match:
                eligible.append((row, *match))
    eligible.sort(key=lambda item: (-item[2], item[0]["id"]))
    chosen = []
    targets = {"gsm8k": {"integer": 66},
               "math": {"integer": 8, "fraction": 13, "expression": 13}}
    for source, kinds in targets.items():
        for answer_type, count in kinds.items():
            candidates = [item for item in eligible if item[0]["source"] == source
                          and item[0]["answer_type"] == answer_type]
            if len(candidates) < count:
                raise ValueError(f"too few {source}/{answer_type} structural candidates: {len(candidates)}")
            chosen.extend(candidates[:count])
    ids = [item[0]["id"] for item in chosen]
    texts = [normalize(item[0]["question"]) for item in chosen]
    if len(ids) != 100 or len(set(ids)) != 100 or len(set(texts)) != 100:
        raise ValueError("selected candidates are not 100 distinct questions")
    if any(row["id"] in group["ids"] or normalize(row["question"]) in group["texts"]
           for row, _, _ in chosen for group in blocked.values()):
        raise ValueError("selected candidate overlaps exclusion source")
    train = pd.read_parquet(FULL_TRAIN)
    train_ids = set(train["id"])
    train_texts = {normalize(info["question"]) for info in train["extra_info"]}
    if any(row["id"] in train_ids or normalize(row["question"]) in train_texts
           for row, _, _ in chosen):
        raise ValueError("selected candidate overlaps complete clean46 train")
    preview = [{key: row[key] for key in ("id", "source", "question", "answer_type")}
               for row, _, _ in chosen]
    OUT.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in preview))
    print(json.dumps({
        "pool": len(rows), "exclusion_sources": {name: len(group["ids"]) for name, group in blocked.items()},
        "pool_hits_by_source": dict(hits),
        "pool_excluded_union": sum(any(row["id"] in group["ids"] or normalize(row["question"]) in group["texts"]
                                       for group in blocked.values()) for row in rows),
        "complete_clean46_train_rows": len(train),
        "complete_clean46_train_unique_ids": len(train_ids),
        "complete_clean46_train_overlap": 0,
        "manual_structural_rejects": len(MANUAL_REJECT),
        "structural_candidates_after_exclusions": len(eligible),
        "preview": len(preview),
        "preview_by_source_type": dict(Counter(f"{row['source']}/{row['answer_type']}" for row in preview)),
        "preview_by_family": dict(Counter(family for _, family, _ in chosen)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
