"""Plain generation (no parallel rollout) on a benchmark parquet, in the same JSONL format as the authors' validation dump.

Usage (from verl/): python ../scripts/bench/generate_plain.py <model> <test.parquet> <output.jsonl> <max_tokens> [thinking|no-thinking|default] [temperature]
Sampling as in the authors' validation by default: temperature 1.0, top_p 1.0; temperature 0 is greedy.
"""
import json
import sys

import pandas as pd
from vllm import LLM, SamplingParams

model, test_path, output_path, max_tokens = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
thinking = sys.argv[5] if len(sys.argv) > 5 else "default"
temperature = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0

test = pd.read_parquet(test_path)
llm = LLM(model, dtype="bfloat16", max_model_len=max_tokens + 2048, gpu_memory_utilization=0.85, seed=0)
tokenizer = llm.get_tokenizer()
template_kwargs = {} if thinking == "default" else {"enable_thinking": thinking == "thinking"}
prompts = [tokenizer.apply_chat_template(list(prompt), add_generation_prompt=True, tokenize=False, **template_kwargs) for prompt in test["prompt"]]
outputs = llm.generate(prompts, SamplingParams(temperature=temperature, top_p=1.0, max_tokens=max_tokens, skip_special_tokens=False, seed=0))
with open(output_path, "w") as f:
    for prompt, output in zip(prompts, outputs):
        completion = output.outputs[0]
        f.write(json.dumps({"input": prompt, "output": completion.text, "tokens": len(completion.token_ids),
                            "truncated": completion.finish_reason == "length"}) + "\n")
