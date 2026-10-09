"""Pilot autonomous Multiverse decoding with the same path mask and positions as SFT.

No structural tokens or path numbers are inserted. Supports multiple flat blocks
per answer. Output columns match the existing generation dumps.

Usage: python generate_masked_multiverse.py MODEL DEV_PARQUET OUT_JSONL COUNT MAX_TOKENS [thinking|no-thinking]
"""
import json
import os
import sys
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from masked_decode_state import MaskedDecodeState, path_count


def generate(model, tok, prompt, max_tokens, seed, path_open, path_close):
    prompt_ids = tok.encode(prompt, add_special_tokens=False)
    ids = torch.tensor([prompt_ids], device="cuda")
    state = MaskedDecodeState(path_open, path_close)
    generator = torch.Generator(device="cuda").manual_seed(seed)
    response = []
    ended_with_eos = False
    with torch.inference_mode():
        out = model(input_ids=ids, use_cache=True)
        past, logits = out.past_key_values, out.logits[0, -1].float()
        for step in range(max_tokens):
            token = torch.multinomial(torch.softmax(logits, -1), 1, generator=generator).item()
            if token == tok.eos_token_id:
                ended_with_eos = True
                break
            if token == path_open and state.phase == "plain":
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
    # Token decisions include EOS; physical calls also include prompt prefill and
    # execute every path serially. Scoring separately reports ideal parallel depth.
    return (tok.decode(response, skip_special_tokens=False), len(response) + int(ended_with_eos),
            not ended_with_eos, 1 + len(response))


def main():
    model_path, data_path, output_path, count, budget = sys.argv[1:6]
    count, budget = int(count), int(budget)
    mode = sys.argv[6] if len(sys.argv) > 6 else "no-thinking"
    assert mode in ("thinking", "no-thinking")
    output = Path(output_path)
    meta = {"model": model_path, "data": data_path, "count": count, "max_tokens": budget,
            "seed": 0, "mode": mode, "decoder": "masked-autonomous-v2", "commit": os.environ.get("EXP21_COMMIT")}
    meta_path = output.with_suffix(output.suffix + ".meta.json")
    if meta_path.exists():
        assert json.loads(meta_path.read_text()) == meta, "run settings changed during resume"
    else:
        assert not output.exists() or output.stat().st_size == 0, "output exists without run settings"
        meta_path.write_text(json.dumps(meta, indent=2))
    with open(output) if output.exists() else open(os.devnull) as previous_file:
        previous = [json.loads(line) for line in previous_file]
    assert len(previous) <= count
    tok = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    path_open = tok.convert_tokens_to_ids("<Path>")
    path_close = tok.convert_tokens_to_ids("</Path>")
    assert tok.encode("<Path>", add_special_tokens=False) == [path_open]
    assert tok.encode("</Path>", add_special_tokens=False) == [path_close]
    seen = set()
    with open(output, "a") as file:
        for _, row in pd.read_parquet(data_path).iterrows():
            question = list(row["prompt"])[0]["content"]
            if question in seen:
                continue
            seen.add(question)
            prompt = tok.apply_chat_template(list(row["prompt"]), add_generation_prompt=True,
                                             tokenize=False, enable_thinking=mode == "thinking")
            if len(seen) <= len(previous):
                assert previous[len(seen) - 1]["input"] == prompt, "resume order or prompt changed"
                continue
            answer, length, truncated, model_calls = generate(model, tok, prompt, budget, 0,
                                                              path_open, path_close)
            file.write(json.dumps({"input": prompt, "output": answer, "tokens": length,
                                   "truncated": truncated, "seed": 0,
                                   "model_forward_calls": model_calls,
                                   "rollout": {"decoder": "masked-autonomous-v2", "mode": mode}}, ensure_ascii=False) + "\n")
            file.flush()
            print(len(seen), length, truncated, answer.count("<Path>"), flush=True)
            if len(seen) >= count:
                break


if __name__ == "__main__":
    main()
