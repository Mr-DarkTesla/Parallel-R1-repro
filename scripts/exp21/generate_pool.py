"""Qwen3-0.6B answers for pool problems (vLLM, one GPU): the source of M2 texts and of the replay rows of exp 21.

Prompt = the plain eval prompt (scripts/bench/make_bench_data.py PLAIN_HEADER + "Problem: "), so SFT rows look like evaluation rows.
Sampling = Qwen3's recommended settings: non-thinking T 0.7 / top_p 0.8 / top_k 20, thinking T 0.6 / top_p 0.95 / top_k 20.
Sample k of a problem uses vLLM seed k. skip_special_tokens=False keeps <think>/</think> as generated.
Usage: python generate_pool.py <model> <pool.jsonl> <out.jsonl> <thinking|no-thinking> <samples> <max_tokens>
Output rows: id, sample, mode, prompt (user text), output, tokens, truncated.
"""
import json
import os
import sys

from vllm import LLM, SamplingParams

HEADER = ("Solve the following problem step by step.\n"
          "End your response with a line starting with Final Answer: followed by the final result.\n\nProblem: ")
model, pool_path, out, mode, samples, max_tokens = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
assert mode in ("thinking", "no-thinking")
sampling = dict(temperature=0.6, top_p=0.95, top_k=20) if mode == "thinking" else dict(temperature=0.7, top_p=0.8, top_k=20)

pool = [json.loads(line) for line in open(pool_path)]
llm = LLM(model, dtype="bfloat16", max_model_len=max_tokens + 1024, gpu_memory_utilization=0.85, seed=0)
tok = llm.get_tokenizer()
prompts, params, keys = [], [], []
for r in pool:
    text = HEADER + r["question"]
    rendered = tok.apply_chat_template([{"role": "user", "content": text}], add_generation_prompt=True, tokenize=False,
                                       enable_thinking=mode == "thinking")
    for k in range(samples):
        prompts.append(rendered)
        params.append(SamplingParams(**sampling, max_tokens=max_tokens, skip_special_tokens=False, seed=k))
        keys.append((r["id"], k, text))
outputs = llm.generate(prompts, params)
with open(out + ".tmp", "w") as f:
    for (idx, k, text), o in zip(keys, outputs):
        c = o.outputs[0]
        f.write(json.dumps({"id": idx, "sample": k, "mode": mode, "prompt": text, "output": c.text, "tokens": len(c.token_ids),
                            "truncated": c.finish_reason == "length"}, ensure_ascii=False) + "\n")
os.replace(out + ".tmp", out)
