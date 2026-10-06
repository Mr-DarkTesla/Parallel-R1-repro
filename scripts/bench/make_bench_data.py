"""Benchmark parquets in the authors' format, in two prompt variants:
parallel = the authors' instruction prompt (with the <Parallel> block instructions), plain = the same prompt without that paragraph.
Benchmarks: the authors' test set (AIME24/25, AMC23, MATH300), LIMO x4, ARC-Challenge, MMLU-Pro (2000 stratified), IFEval.
data_source "APO_*" routes the authors' reward to math_dapo (the rollout needs a reward); real scoring is scripts/bench/score.py.

Usage (from verl/): python ../scripts/bench/make_bench_data.py <bench_dir> <output_dir>
"""
import json
import os
import sys

import pandas as pd

bench_dir, output_dir = sys.argv[1], sys.argv[2]
DATA = "data_preprocess_scripts/data"
authors = pd.read_parquet(f"{DATA}/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet")
PARALLEL_HEADER = authors.iloc[0]["prompt"][0]["content"].split("Problem:")[0]
start, end = PARALLEL_HEADER.index("During the reasoning process"), PARALLEL_HEADER.index("End your response")
PLAIN_HEADER = PARALLEL_HEADER[:start] + PARALLEL_HEADER[end:]
LETTERS = "ABCDEFGHIJ"


def multiple_choice(question, options):
    lines = "\n".join(f"{LETTERS[i]}. {option}" for i, option in enumerate(options))
    return f"{question}\n\n{lines}\n\nThe final result is the letter of the correct option."


def rows(source, problems, answers, extra=None):
    """problems: problem texts; returns (parallel, plain) frames."""
    frames = []
    for header in (PARALLEL_HEADER, PLAIN_HEADER):
        frames.append(pd.DataFrame({
            "data_source": f"APO_{source}",
            "prompt": [[{"role": "user", "content": f"{header}Problem: {problem}"}] for problem in problems],
            "ability": "math",
            "reward_model": [{"ground_truth": str(answer), "style": "rule-lighteval/MATH_v2"} for answer in answers],
            "extra_info": [{"reward_method": "accuracy_reward", "doc": json.dumps(doc)} for doc in (extra or [{}] * len(problems))],
        }))
    return frames


def problems_of(frame):
    return [row[0]["content"].split("Problem:", 1)[1].strip() for row in frame["prompt"]], [r["ground_truth"] for r in frame["reward_model"]]


benchmarks = {}
# the authors' math test set and LIMO keep their sources and repeats
for name, path in {"apo": f"{DATA}/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet", "limo": f"{DATA}/limo/test.parquet"}.items():
    frame = pd.read_parquet(path)
    problems, answers = problems_of(frame)
    parallel, plain = rows("x", problems, answers)
    parallel["data_source"] = plain["data_source"] = frame["data_source"].to_numpy()
    benchmarks[name] = (parallel, plain)

arc = pd.read_parquet(next(f"{bench_dir}/ai2_arc/ARC-Challenge/{f}" for f in os.listdir(f"{bench_dir}/ai2_arc/ARC-Challenge") if f.startswith("test")))
benchmarks["arc"] = rows("ARC", [multiple_choice(q, c["text"]) for q, c in zip(arc["question"], arc["choices"])],
                         [LETTERS[list(c["label"]).index(key)] for c, key in zip(arc["choices"], arc["answerKey"])])

mmlu = pd.read_parquet(next(f"{bench_dir}/MMLU-Pro/data/{f}" for f in os.listdir(f"{bench_dir}/MMLU-Pro/data") if f.startswith("test")))
subset = mmlu.groupby("category", group_keys=False).apply(lambda g: g.sample(frac=2000 / len(mmlu), random_state=0)).sort_values("question_id")
benchmarks["mmlu_pro"] = rows("MMLUPRO", [multiple_choice(q, list(o)) for q, o in zip(subset["question"], subset["options"])], subset["answer"])

ifeval = pd.read_json(f"{bench_dir}/IFEval/ifeval_input_data.jsonl", lines=True)
docs = [{"key": int(k), "instruction_id_list": list(i), "prompt": p, "kwargs": [{a: b for a, b in kw.items() if b is not None} for kw in kws]}
        for k, i, p, kws in zip(ifeval["key"], ifeval["instruction_id_list"], ifeval["prompt"], ifeval["kwargs"])]
parallel, plain = rows("IFEVAL", ifeval["prompt"], [""] * len(ifeval), docs)
plain["prompt"] = [[{"role": "user", "content": p}] for p in ifeval["prompt"]]  # plain IFEval is the original prompt
benchmarks["ifeval"] = (parallel, plain)

for name, (parallel, plain) in benchmarks.items():
    for mode, frame in (("parallel", parallel), ("plain", plain)):
        os.makedirs(f"{output_dir}/{mode}", exist_ok=True)
        frame.to_parquet(f"{output_dir}/{mode}/{name}.parquet")
        print(mode, name, len(frame), frame["data_source"].unique()[:4])
