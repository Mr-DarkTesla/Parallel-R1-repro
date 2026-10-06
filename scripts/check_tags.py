"""Tag validator on free generation of one checkpoint (plain decoding, no parallel rollout loop).

Prompts: first 128 GSM8K test problems and MATH300 from the authors' test set, with the authors' instruction prompt.
Usage (from verl/): python ../scripts/check_tags.py <model_dir> <generations_dir>
"""
import json
import os
import sys

import pandas as pd
from vllm import LLM, SamplingParams

from tag_validator import summarize

DATA = "data_preprocess_scripts/data"
SETS = {
    "gsm8k": pd.read_parquet(f"{DATA}/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet").head(128),
    "math300": pd.read_parquet(f"{DATA}/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet").query("data_source == 'APO_MATH300'"),
}

model, generations_dir = sys.argv[1], sys.argv[2]
os.makedirs(generations_dir, exist_ok=True)
llm = LLM(model, gpu_memory_utilization=0.5, seed=0)
tokenizer = llm.get_tokenizer()
for name, data in SETS.items():
    prompts = [tokenizer.apply_chat_template(list(prompt), add_generation_prompt=True, tokenize=False) for prompt in data["prompt"]]
    for temperature in (0.0, 1.0):
        params = SamplingParams(temperature=temperature, max_tokens=8192, skip_special_tokens=False, seed=0)
        outputs = [output.outputs[0].text for output in llm.generate(prompts, params, use_tqdm=False)]
        with open(f"{generations_dir}/{os.path.basename(model)}_{name}_t{temperature}.jsonl", "w") as f:
            f.writelines(json.dumps({"output": output}) + "\n" for output in outputs)
        stats = {key: round(value, 4) for key, value in summarize(outputs).items()}
        print(json.dumps({"model": model, "set": name, "temperature": temperature, **stats}), flush=True)
