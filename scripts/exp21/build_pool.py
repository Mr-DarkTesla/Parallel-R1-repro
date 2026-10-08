"""Problem pool of exp 21: MATH train, GSM8K train, ARC train (Easy + Challenge), cleaned with the shared leak checker v2.

Inputs: the dataset survey folder (../dataset_survey: data/norm/*.jsonl, leak/*.hits.jsonl, leak/*.residual_pairs.md, raw MATH/ARC
parquets under /tmp/ds_survey_dl). A row is dropped if the checker reports ANY tier (dup, variant or weak) against one of our eval
sets, or dup/variant against the full MATH test (source of MATH dev and MATH300), or it is on the residual answer-rule lists (remove
and review), or its text names AIME/AMC/HMMT. GSM8K dev is a subset of GSM8K train: those rows are dup hits and are dropped too.
Output rows: id, source (math|gsm8k|arc), question (as the eval prompt shows it), answer, answer_type (integer|fraction|expression|letter),
level/type (MATH). Usage: python build_pool.py <survey_dir> <raw_dir> <out.jsonl>
"""
import json
import re
import sys

import pandas as pd

survey, raw, out = sys.argv[1:4]
ORIGIN = re.compile(r"\b(AIME|Invitational|AMC|American Mathematics Competition|HMMT)\b", re.I)
LETTERS = "ABCDEFGHIJ"


def leaky(name):
    bad = set()
    for line in open(f"{survey}/leak/{name}.hits.jsonl"):
        h = json.loads(line)
        for x in h["hits"]:
            ours = "(info)" not in x["eval_set"] and (x.get("leak") or x.get("tier"))
            math_test = x["eval_set"] == "math_test_full(info)" and x.get("tier") in ("dup", "variant")
            if ours or math_test:
                bad.add(str(h["id"]))
    try:
        bad |= set(re.findall(r"^- (?:remove|review) jac=\S+ `([^`]+)`", open(f"{survey}/leak/{name}.residual_pairs.md").read(), re.M))
    except FileNotFoundError:
        pass
    return bad


def answer_type(answer):
    a = answer.replace(" ", "").replace("$", "")
    if re.fullmatch(r"-?\d+", a.replace(",", "")):
        return "integer"
    if re.fullmatch(r"-?(\\[dt]?frac\{-?\d+\}\{\d+\}|\d+/\d+|-?\d*\.\d+)", a):
        return "fraction"
    return "expression"


def norm_rows(name):
    return [json.loads(line) for line in open(f"{survey}/data/norm/{name}.jsonl")]


rows, stats = [], {}
math_raw = pd.read_parquet(f"{raw}/math/default-train-0000.parquet")
for name, source in (("src_math_train", "math"), ("src_gsm8k_train", "gsm8k")):
    bad, kept = leaky(name), 0
    seen = set()
    for r in norm_rows(name):
        key = re.sub(r"\s+", " ", r["question"].strip().lower())
        if str(r["id"]) in bad or ORIGIN.search(r["question"]) or not r["ref"] or key in seen:
            continue
        seen.add(key)
        row = {"id": f"{source}-train/{r['id']}", "source": source, "question": r["question"].strip(), "answer": r["ref"].strip(),
               "answer_type": answer_type(r["ref"])}
        if source == "math":
            raw_row = math_raw.iloc[int(r["id"])]
            assert raw_row["problem"].strip() == r["question"].strip()
            row.update(level=raw_row["level"], type=raw_row["type"])
            if "\\text" in r["ref"] or len(r["ref"]) > 40:  # word answers and long multi-part answers: unreliable checking
                continue
        rows.append(row)
        kept += 1
    stats[source] = {"rows": len(norm_rows(name)), "leaky_or_flagged": len(bad), "kept": kept}

bad = leaky("rep_arc_train")
arc = pd.concat([pd.read_parquet(f"{raw}/arc/{f}.parquet") for f in ("easy", "challenge")])
kept = 0
for _, r in arc.iterrows():
    if r["id"] in bad:
        continue
    labels = list(r["choices"]["label"])
    if r["answerKey"] not in labels:
        continue
    lines = "\n".join(f"{LETTERS[i]}. {t}" for i, t in enumerate(r["choices"]["text"]))
    question = f"{r['question']}\n\n{lines}\n\nThe final result is the letter of the correct option."
    rows.append({"id": f"arc-train/{r['id']}", "source": "arc", "question": question, "answer": LETTERS[labels.index(r["answerKey"])],
                 "answer_type": "letter"})
    kept += 1
stats["arc"] = {"rows": len(arc), "leaky_or_flagged": len(bad), "kept": kept}

with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
frame = pd.DataFrame(rows)
stats["answer_types"] = frame.groupby(["source", "answer_type"]).size().unstack(fill_value=0).to_dict("index")
json.dump(stats, open(out + ".stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))
