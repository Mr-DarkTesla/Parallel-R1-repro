"""Dev parquets for setting selection and slice metadata for the frozen benchmark parquets (exp 13).

dev (selection only, never the frozen tests):
  gsm8k_dev  GSM8K train problems held out of every SFT arm (filter worker's dev split), x4 samples
  math_dev   MATH test without the frozen MATH300 / AIME / AMC / LIMO texts, 500 stratified by subject (seed 1), x2
  arc_dev    ARC-Challenge validation, x4
  mmlu_pro_dev  MMLU-Pro test questions outside the frozen 2000 (by id and text), 1000 stratified by category (seed 1), x1
Prompts as in scripts/bench/make_bench_data.py: plain = the authors' header without the parallel paragraph, parallel = the authors' header.
extra_info keeps reward_method (the rollout needs it), a stable id and the slice fields.
meta/<suite>/<bench>.jsonl: per parquet row the problem id that score.py writes and the slice fields; for the frozen parquets they are
rebuilt from the sources and checked against the prompts. manifest.json: sizes, ids and exact-text overlap checks.

Usage (from verl/): python ../scripts/instruct4b_eval/make_eval_data.py <bench_dir> <filter_dev.parquet> <sft_train.parquet> <frozen_dir> <output_dir>
"""
import difflib
import json
import os
import re
import sys

import pandas as pd

bench_dir, filter_dev_path, sft_path, frozen_dir, output_dir = sys.argv[1:6]
DATA = "data_preprocess_scripts/data"
authors = pd.read_parquet(f"{DATA}/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet")
PARALLEL_HEADER = authors.iloc[0]["prompt"][0]["content"].split("Problem:")[0]
start, end = PARALLEL_HEADER.index("During the reasoning process"), PARALLEL_HEADER.index("End your response")
PLAIN_HEADER = PARALLEL_HEADER[:start] + PARALLEL_HEADER[end:]
LETTERS = "ABCDEFGHIJ"


def norm(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def multiple_choice(question, options):
    lines = "\n".join(f"{LETTERS[i]}. {option}" for i, option in enumerate(options))
    return f"{question}\n\n{lines}\n\nThe final result is the letter of the correct option."


def near_duplicate(text, pool, threshold=0.8):
    """Some pool text has a difflib ratio above threshold (catches reformatted copies; also catches same-template siblings)."""
    for other in pool:
        m = difflib.SequenceMatcher(None, text, other, autojunk=False)
        if m.real_quick_ratio() > threshold and m.quick_ratio() > threshold and m.ratio() > threshold:
            return True
    return False


def problem_of(content):
    return content.split("Problem:", 1)[1].strip()


def score_ids(frame):
    """The problem ids score.py derives when extra_info has no id."""
    contents = [p[0]["content"] for p in frame["prompt"]]
    order = {c: n for n, c in enumerate(dict.fromkeys(contents))}
    return [f"{s.removeprefix('APO_')}/{order[c]}" for s, c in zip(frame["data_source"], contents)]


def dev_rows(source, table, samples):
    """table: id, problem, answer, slice columns; every problem repeated `samples` times (consecutive rows)."""
    table = table.loc[table.index.repeat(samples)].reset_index(drop=True)
    slices = [c for c in table.columns if c not in ("id", "problem", "answer")]
    frames = {}
    for mode, header in (("parallel", PARALLEL_HEADER), ("plain", PLAIN_HEADER)):
        frames[mode] = pd.DataFrame({
            "data_source": f"APO_{source}",
            "prompt": [[{"role": "user", "content": f"{header}Problem: {p}"}] for p in table["problem"]],
            "ability": "math",
            "reward_model": [{"ground_truth": str(a), "style": "rule-lighteval/MATH_v2"} for a in table["answer"]],
            "extra_info": [{"reward_method": "accuracy_reward", "doc": "{}", "id": str(i), **{c: str(r[c]) for c in slices}}
                           for i, (_, r) in zip(table["id"], table.iterrows())],
        })
    meta = pd.DataFrame({"row": range(len(table)), "problem_id": table["id"].astype(str), **{c: table[c].astype(str) for c in slices}})
    return frames, meta


sft = pd.read_parquet(sft_path)
sft_texts = {norm(problem_of(p[0]["content"])) for p in sft["prompt"]}
frozen = {name: pd.read_parquet(f"{frozen_dir}/{name}.parquet") for name in ("apo", "limo", "arc", "mmlu_pro", "ifeval")}
frozen_math_texts = {norm(problem_of(p[0]["content"])) for name in ("apo", "limo") for p in frozen[name]["prompt"]}
manifest = {"headers": {"plain": PLAIN_HEADER, "parallel": PARALLEL_HEADER}, "dev": {}, "frozen": {}}
dev, meta = {}, {"dev": {}, "frozen": {}}

# GSM8K: the filter worker's dev split (GSM8K train rows held out of all SFT arms, prompt = the authors' parallel header)
gsm = pd.read_parquet(filter_dev_path)
assert all(p[0]["content"].startswith(PARALLEL_HEADER + "Problem:") for p in gsm["prompt"]), "dev prompt header differs from the bench header"
gsm_table = pd.DataFrame({"id": [f"gsm8k-train/{i}" for i in gsm["index"]], "problem": [problem_of(p[0]["content"]) for p in gsm["prompt"]],
                          "answer": [r["ground_truth"] for r in gsm["reward_model"]]})
assert not set(gsm["index"]) & set(sft["index"]), "GSM8K dev rows are in the SFT data"
dev["gsm8k_dev"], meta["dev"]["gsm8k_dev"] = dev_rows("GSM8K_DEV", gsm_table, 4)

# MATH test without any frozen math problem, stratified by subject; sampled problems close to a frozen one (ratio > 0.8) are dropped:
# 2026-10-06 check found 7 reformatted LIMO (old AIME) problems and 14 same-template MATH300 siblings among 501
math = pd.read_parquet(f"{DATA}/math/math_test.parquet")
math_texts = math["question"].map(norm)
pool = math[~math_texts.isin(frozen_math_texts)]
picked = pool.groupby("type", group_keys=False).apply(lambda g: g.sample(frac=500 / len(pool), random_state=1)).sort_values("index")
close = picked["question"].map(lambda q: near_duplicate(norm(q), frozen_math_texts))
manifest["dev"]["math_dev_dropped_near_frozen"] = [f"math-test/{i}" for i in picked["index"][close]]
picked = picked[~close]
math_table = pd.DataFrame({"id": [f"math-test/{i}" for i in picked["index"]], "problem": picked["question"], "answer": picked["reference"],
                           "type": picked["type"], "level": picked["level"]})
dev["math_dev"], meta["dev"]["math_dev"] = dev_rows("MATH_DEV", math_table.reset_index(drop=True), 2)
manifest["dev"]["math_dev_excluded_as_frozen"] = int(math_texts.isin(frozen_math_texts).sum())

# ARC-Challenge validation
arc_val = pd.read_parquet(f"{bench_dir}/ai2_arc/ARC-Challenge/validation-00000-of-00001.parquet")
arc_table = pd.DataFrame({"id": [f"arc-val/{i}" for i in arc_val["id"]],
                          "problem": [multiple_choice(q, c["text"]) for q, c in zip(arc_val["question"], arc_val["choices"])],
                          "answer": [LETTERS[list(c["label"]).index(k)] for c, k in zip(arc_val["choices"], arc_val["answerKey"])]})
dev["arc_dev"], meta["dev"]["arc_dev"] = dev_rows("ARC", arc_table, 4)

# MMLU-Pro: the frozen 2000 rebuilt exactly as make_bench_data.py, dev from the rest (disjoint by id and question text)
mmlu = pd.read_parquet(f"{bench_dir}/MMLU-Pro/data/test-00000-of-00001.parquet")
subset = mmlu.groupby("category", group_keys=False).apply(lambda g: g.sample(frac=2000 / len(mmlu), random_state=0)).sort_values("question_id")
rest = mmlu[~mmlu["question_id"].isin(subset["question_id"]) & ~mmlu["question"].map(norm).isin(set(subset["question"].map(norm)))]
picked = rest.groupby("category", group_keys=False).apply(lambda g: g.sample(frac=1000 / len(rest), random_state=1)).sort_values("question_id")
mmlu_table = pd.DataFrame({"id": [f"mmlu-pro/{i}" for i in picked["question_id"]],
                           "problem": [multiple_choice(q, list(o)) for q, o in zip(picked["question"], picked["options"])],
                           "answer": picked["answer"], "category": picked["category"], "src": picked["src"]})
dev["mmlu_pro_dev"], meta["dev"]["mmlu_pro_dev"] = dev_rows("MMLUPRO", mmlu_table.reset_index(drop=True), 1)

# frozen parquets: ids and slices, checked against the prompts
for name in ("apo", "limo"):
    frame = frozen[name]
    meta["frozen"][name] = pd.DataFrame({"row": range(len(frame)), "problem_id": score_ids(frame),
                                         "source": frame["data_source"].str.removeprefix("APO_")})
by_text = dict(zip(math_texts, zip(math["type"], math["level"])))
apo_texts = [norm(problem_of(p[0]["content"])) for p in frozen["apo"]["prompt"]]
meta["frozen"]["apo"]["type"] = [by_text.get(t, ("", ""))[0] for t in apo_texts]
meta["frozen"]["apo"]["level"] = [by_text.get(t, ("", ""))[1] for t in apo_texts]
math300 = meta["frozen"]["apo"]["source"] == "MATH300"
manifest["frozen"]["math300_matched_to_math_test"] = f"{int((meta['frozen']['apo']['type'][math300] != '').sum())}/{int(math300.sum())}"

arc_test = pd.read_parquet(f"{bench_dir}/ai2_arc/ARC-Challenge/test-00000-of-00001.parquet")
assert [problem_of(p[0]["content"]) for p in frozen["arc"]["prompt"]] == [multiple_choice(q, c["text"]).strip() for q, c in zip(arc_test["question"], arc_test["choices"])]
meta["frozen"]["arc"] = pd.DataFrame({"row": range(len(arc_test)), "problem_id": score_ids(frozen["arc"]), "source_id": arc_test["id"]})
assert [problem_of(p[0]["content"]) for p in frozen["mmlu_pro"]["prompt"]] == [multiple_choice(q, list(o)).strip() for q, o in zip(subset["question"], subset["options"])]
meta["frozen"]["mmlu_pro"] = pd.DataFrame({"row": range(len(subset)), "problem_id": score_ids(frozen["mmlu_pro"]),
                                           "source_id": subset["question_id"].to_numpy(), "category": subset["category"].to_numpy()})
docs = [json.loads(info["doc"]) for info in frozen["ifeval"]["extra_info"]]
assert [p[0]["content"] for p in frozen["ifeval"]["prompt"]] == [d["prompt"] for d in docs]
meta["frozen"]["ifeval"] = pd.DataFrame({"row": range(len(docs)), "problem_id": score_ids(frozen["ifeval"]), "source_id": [d["key"] for d in docs],
                                         "groups": [sorted({i.split(":")[0] for i in d["instruction_id_list"]}) for d in docs]})

# overlaps (exact text after lowercasing and whitespace collapse)
dev_texts = {name: {norm(problem_of(p[0]["content"])) for p in frames["plain"]["prompt"]} for name, frames in dev.items()}
frozen_texts = {name: {norm(problem_of(p[0]["content"])) if "Problem:" in p[0]["content"] else norm(p[0]["content"]) for p in frame["prompt"]}
                for name, frame in frozen.items()}
manifest["overlap"] = {f"{d}~{f}": len(dev_texts[d] & frozen_texts[f]) for d in dev for f in frozen}
manifest["overlap"].update({f"{d}~sft_train": len(dev_texts[d] & sft_texts) for d in dev})
for name, frames in dev.items():
    ids = meta["dev"][name]["problem_id"]
    manifest["dev"][name] = {"rows": len(ids), "problems": ids.nunique(), "samples_per_problem": int(ids.value_counts().iloc[0]),
                             **{c: meta["dev"][name][c].drop_duplicates().size for c in ("category", "type") if c in meta["dev"][name]}}
    for mode, frame in frames.items():
        os.makedirs(f"{output_dir}/dev/{mode}", exist_ok=True)
        frame.to_parquet(f"{output_dir}/dev/{mode}/{name}.parquet")
for suite in meta:
    os.makedirs(f"{output_dir}/meta/{suite}", exist_ok=True)
    for name, table in meta[suite].items():
        table.to_json(f"{output_dir}/meta/{suite}/{name}.jsonl", orient="records", lines=True)
manifest["dev_ids"] = {name: sorted(set(table["problem_id"])) for name, table in meta["dev"].items()}
json.dump(manifest, open(f"{output_dir}/manifest.json", "w"), indent=1, default=int)
print(json.dumps({k: manifest[k] for k in ("dev", "frozen", "overlap")}, indent=1, default=int))
