"""Pilot autonomous Multiverse decoding with the same path mask and positions as SFT.

No structural tokens or path numbers are inserted. Supports one flat block per
answer. Output columns match the existing generation dumps.

Usage: python generate_masked_multiverse.py MODEL DEV_PARQUET OUT_JSONL COUNT MAX_TOKENS
"""
import json
import re
import sys

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from masked_decode_state import MaskedDecodeState


def path_count(prefix):
    goal = re.search(r"<Goal>(.*?)</Goal>\s*$", prefix, re.S)
    if not goal:
        return 0
    outlines = re.findall(r"<Outline>\s*(\d+)\s*:(.*?)</Outline>", goal.group(1), re.S)
    if len(outlines) not in (2, 3, 4):
        return 0
    return len(outlines) if [int(x[0]) for x in outlines] == list(range(1, len(outlines) + 1)) else 0


def generate(model, tok, prompt, max_tokens, seed, path_open, path_close):
    prompt_ids = tok.encode(prompt, add_special_tokens=False)
    ids = torch.tensor([prompt_ids], device="cuda")
    state = MaskedDecodeState(path_open, path_close)
    generator = torch.Generator(device="cuda").manual_seed(seed)
    response = []
    with torch.inference_mode():
        out = model(input_ids=ids, use_cache=True)
        past, logits = out.past_key_values, out.logits[0, -1].float()
        for step in range(max_tokens):
            token = torch.multinomial(torch.softmax(logits, -1), 1, generator=generator).item()
            if token == tok.eos_token_id:
                break
            if token == path_open and state.base is None:
                state.expected_paths = path_count(tok.decode(response, skip_special_tokens=False)) or 1
            position, visible = state.append(token)
            response.append(token)
            rowmask = torch.zeros(1, 1, 1, len(prompt_ids) + len(response),
                                  dtype=torch.bfloat16, device="cuda")
            rowmask[..., len(prompt_ids):].masked_fill_(
                ~torch.tensor(visible, device="cuda"), torch.finfo(torch.bfloat16).min)
            out = model(input_ids=torch.tensor([[token]], device="cuda"), past_key_values=past,
                        attention_mask=rowmask,
                        position_ids=torch.tensor([[len(prompt_ids) + position]], device="cuda"),
                        cache_position=torch.tensor([len(prompt_ids) + step], device="cuda"),
                        use_cache=True)
            past, logits = out.past_key_values, out.logits[0, -1].float()
    return tok.decode(response, skip_special_tokens=False), len(response), len(response) == max_tokens


def main():
    model_path, data_path, output_path, count, budget = sys.argv[1:6]
    count, budget = int(count), int(budget)
    tok = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    path_open = tok.convert_tokens_to_ids("<Path>")
    path_close = tok.convert_tokens_to_ids("</Path>")
    assert tok.encode("<Path>", add_special_tokens=False) == [path_open]
    assert tok.encode("</Path>", add_special_tokens=False) == [path_close]
    seen = set()
    with open(output_path, "w") as file:
        for _, row in pd.read_parquet(data_path).iterrows():
            question = list(row["prompt"])[0]["content"]
            if question in seen:
                continue
            seen.add(question)
            prompt = tok.apply_chat_template(list(row["prompt"]), add_generation_prompt=True,
                                             tokenize=False, enable_thinking=False)
            answer, length, truncated = generate(model, tok, prompt, budget, 0,
                                                 path_open, path_close)
            file.write(json.dumps({"input": prompt, "output": answer, "tokens": length,
                                   "truncated": truncated, "seed": 0,
                                   "rollout": {"decoder": "masked-autonomous"}}, ensure_ascii=False) + "\n")
            file.flush()
            print(len(seen), length, truncated, answer.count("<Path>"), flush=True)
            if len(seen) >= count:
                break


if __name__ == "__main__":
    main()
