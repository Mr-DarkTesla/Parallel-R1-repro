"""Build a test parquet from GAIR/LIMO (817 problems, integer answers) in the format of the authors' test set.

The prompt is the authors' instruction prompt taken from their test set, with the LIMO problem instead.
data_source "APO_LIMO" routes the answer check to the same math_dapo accuracy reward as AIME/AMC/MATH.
Usage (from verl/): python ../scripts/make_limo_test.py <limo.jsonl> <repeats> <output.parquet>
"""
import sys

import pandas as pd

limo_path, repeats, output_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]

authors_test = pd.read_parquet("data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet")
instruction = authors_test.iloc[0]["prompt"][0]["content"].split("Problem:")[0]

limo = pd.read_json(limo_path, lines=True)
test = pd.DataFrame({
    "data_source": "APO_LIMO",
    "prompt": [[{"role": "user", "content": f"{instruction}Problem: {question}"}] for question in limo["question"]],
    "ability": "math",
    "reward_model": [{"ground_truth": str(answer), "style": "rule-lighteval/MATH_v2"} for answer in limo["answer"]],
    "extra_info": [{"reward_method": "accuracy_reward"}] * len(limo),
})
test.loc[test.index.repeat(repeats)].reset_index(drop=True).to_parquet(output_path)
