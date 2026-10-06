"""Plain generation for the dev suite: scripts/bench/generate_plain.py with one change, the vLLM seed of a row is its sample index
(the number of earlier rows with the same prompt). generate_plain.py seeds every row with 0, so repeated rows of one prompt differ only
by batch nondeterminism (Qwen3-4B no-thinking 16k AMC23: 8.5 distinct answers per 16 rows); here repeats are separate samples.
Sample 0 keeps seed 0. Same output format as generate_plain.py.

Usage (from verl/): python ../scripts/instruct4b_eval/generate.py <model> <test.parquet> <output.jsonl> <max_tokens> <thinking|no-thinking> [temperature]
"""
import json
import sys

import pandas as pd
from vllm import LLM, SamplingParams

model, test_path, output_path, max_tokens, thinking = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
temperature = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
assert thinking in ("thinking", "no-thinking"), thinking

test = pd.read_parquet(test_path)
llm = LLM(model, dtype="bfloat16", max_model_len=max_tokens + 2048, gpu_memory_utilization=0.85, seed=0)
tokenizer = llm.get_tokenizer()
prompts = [tokenizer.apply_chat_template(list(prompt), add_generation_prompt=True, tokenize=False, enable_thinking=thinking == "thinking")
           for prompt in test["prompt"]]
samples = pd.Series(prompts).groupby(prompts).cumcount()
params = [SamplingParams(temperature=temperature, top_p=1.0, max_tokens=max_tokens, skip_special_tokens=False, seed=int(s)) for s in samples]
outputs = llm.generate(prompts, params)
with open(output_path, "w") as f:
    for prompt, output, sample in zip(prompts, outputs, samples):
        completion = output.outputs[0]
        f.write(json.dumps({"input": prompt, "output": completion.text, "tokens": len(completion.token_ids),
                            "truncated": completion.finish_reason == "length", "seed": int(sample)}) + "\n")
