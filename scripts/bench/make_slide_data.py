"""MATH500 and AIME 2024/2025/2026 in the authors' parallel prompt: the problems of the "accuracy vs forwards" slide
(docs/reproduction/benchmark-trajectories-2026-10-14 in the RL branches). Each problem is repeated to lower the noise of the mean.
AIME24/25: the authors' test set; MATH500: HuggingFaceH4/MATH-500; AIME26: MathArena/aime_2026 (revision d2de22f3, as on the slide).

Usage (from verl/, HF_ENDPOINT=http://huggingface.proxy): python ../scripts/bench/make_slide_data.py <output_dir> <math_repeats> <aime_repeats>
-> <output_dir>/parallel/{math500,aime}.parquet
"""
import os
import sys

import pandas as pd
from datasets import load_dataset

output_dir, math_repeats, aime_repeats = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
authors = pd.read_parquet("data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet")
HEADER = authors.iloc[0]["prompt"][0]["content"].split("Problem:")[0]


def rows(source, problems, answers, repeats):
    return pd.DataFrame({
        "data_source": f"APO_{source}",
        "prompt": [[{"role": "user", "content": f"{HEADER}Problem: {p}"}] for p in problems for _ in range(repeats)],
        "ability": "math",
        "reward_model": [{"ground_truth": str(a), "style": "rule-lighteval/MATH_v2"} for a in answers for _ in range(repeats)],
        "extra_info": [{"reward_method": "accuracy_reward"}] * (len(problems) * repeats),
    })


aime = []
for source in ("AIME24", "AIME25"):
    frame = authors[authors["data_source"] == f"APO_{source}"]  # repeated x16 in the authors' set
    problems = list(dict.fromkeys(row[0]["content"].split("Problem:", 1)[1].strip() for row in frame["prompt"]))
    truth = {row[0]["content"].split("Problem:", 1)[1].strip(): r["ground_truth"] for row, r in zip(frame["prompt"], frame["reward_model"])}
    assert len(problems) == 30, (source, len(problems))
    aime.append(rows(source, problems, [truth[p] for p in problems], aime_repeats))
aime26 = load_dataset("MathArena/aime_2026", revision="d2de22f3", split="train")
assert len(aime26) == 30
aime.append(rows("AIME26", aime26["problem"], aime26["answer"], aime_repeats))
math500 = load_dataset("HuggingFaceH4/MATH-500", split="test")
assert len(math500) == 500

os.makedirs(f"{output_dir}/parallel", exist_ok=True)
for name, frame in (("math500", rows("MATH500", math500["problem"], math500["answer"], math_repeats)), ("aime", pd.concat(aime, ignore_index=True))):
    frame.to_parquet(f"{output_dir}/parallel/{name}.parquet")
    print(name, len(frame), frame["data_source"].value_counts().to_dict())
