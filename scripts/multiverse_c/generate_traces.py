"""Variant C, step 2: Qwen3-4B thinking-mode traces for pool problems (vLLM, one GPU).

Prompt = the plain eval prompt layout (scripts/bench/make_bench_data.py), so the SFT data shows the eval format;
multiple-choice questions get the ARC/MMLU-Pro closing line. Qwen3 recommended thinking sampling: T 0.6, top_p 0.95, top_k 20.
Sample k of a problem uses vLLM seed k. skip_special_tokens=False keeps <think>/</think> as generated.

Usage: python generate_traces.py <model> <pool.jsonl> <out.jsonl> [--limit N] [--samples 4] [--max-tokens 16384] [--seed 0]
--limit takes a seeded random subset (the pilot); the chosen mv_index list is written next to the output.
Output rows: mv_index, sample, prompt (user text), input (rendered), output, tokens, truncated, finish_reason.
"""
import argparse
import json
import random

HEADER = ("Solve the following problem step by step.\n"
          "End your response with a line starting with Final Answer: followed by the final result.\n\nProblem: ")
MC_TAIL = "\n\nThe final result is the letter of the correct option."


def user_prompt(row):
    mc = len(row["answer"]) == 1 and row["answer"].isalpha() and row["answer_source"] == "solution_answer_letter"
    return HEADER + row["question"] + (MC_TAIL if mc else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("pool")
    ap.add_argument("out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--samples", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=16384)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pool = [json.loads(line) for line in open(args.pool)]
    if args.limit:
        pool = sorted(random.Random(args.seed).sample(pool, args.limit), key=lambda r: r["mv_index"])
    json.dump([r["mv_index"] for r in pool], open(args.out + ".problems.json", "w"))

    from vllm import LLM, SamplingParams
    llm = LLM(args.model, dtype="bfloat16", max_model_len=args.max_tokens + 2048, gpu_memory_utilization=0.85, seed=0)
    tok = llm.get_tokenizer()
    prompts, params, keys = [], [], []
    for r in pool:
        text = user_prompt(r)
        rendered = tok.apply_chat_template([{"role": "user", "content": text}], add_generation_prompt=True, tokenize=False,
                                           enable_thinking=True)
        for k in range(args.samples):
            prompts.append(rendered)
            params.append(SamplingParams(temperature=0.6, top_p=0.95, top_k=20, max_tokens=args.max_tokens,
                                         skip_special_tokens=False, seed=k))
            keys.append((r["mv_index"], k, text))
    outputs = llm.generate(prompts, params)
    with open(args.out + ".tmp", "w") as f:
        for (idx, k, text), rendered, o in zip(keys, prompts, outputs):
            c = o.outputs[0]
            f.write(json.dumps({"mv_index": idx, "sample": k, "prompt": text, "input": rendered, "output": c.text,
                                "tokens": len(c.token_ids), "prompt_tokens": len(o.prompt_token_ids),
                                "truncated": c.finish_reason == "length", "finish_reason": c.finish_reason},
                               ensure_ascii=False) + "\n")
    import os
    os.replace(args.out + ".tmp", args.out)


if __name__ == "__main__":
    main()
