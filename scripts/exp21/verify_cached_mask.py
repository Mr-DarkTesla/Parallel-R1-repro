"""Check cached one-token Multiverse decoding against a full SFT forward pass."""
import json
import sys

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from masked_decode_state import MaskedDecodeState
from multiverse_structure import dense_mask, multiverse_structure


def main():
    model_path, val_path = sys.argv[1:3]
    tok = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    row = next(x for x in pd.read_parquet(val_path)["extra_info"] if x["kind"] == "parallel")
    prompt = tok.apply_chat_template(
        [{"role": "user", "content": row["question"]}], add_generation_prompt=True,
        tokenize=False, enable_thinking=False)
    prompt_ids = tok.encode(prompt, add_special_tokens=False)
    response_ids = tok.encode(row["answer"] + tok.eos_token, add_special_tokens=False)
    tags = {key: tok.convert_tokens_to_ids(value) for key, value in {
        "Parallel": "<Parallel>", "/Parallel": "</Parallel>",
        "Path": "<Path>", "/Path": "</Path>"}.items()}
    positions, groups = multiverse_structure(response_ids, tags)
    targets = [i for i, token in enumerate(response_ids) if token == tags["Path"]]
    assert len(targets) >= 2
    p, n = len(prompt_ids), len(response_ids)
    ids = torch.tensor([prompt_ids + response_ids], device="cuda")
    attention = torch.ones(p + n, p + n, dtype=torch.bool, device="cuda").tril_()
    attention[p:, p:] = dense_mask(n, groups, device="cuda")
    mask = torch.zeros(1, 1, p + n, p + n, dtype=torch.bfloat16, device="cuda")
    mask.masked_fill_(~attention[None, None], torch.finfo(torch.bfloat16).min)
    pos = torch.tensor([list(range(p)) + [p + x for x in positions]], device="cuda")
    with torch.inference_mode():
        reference = model(input_ids=ids, attention_mask=mask, position_ids=pos, use_cache=False).logits[0]
        out = model(input_ids=ids[:, :p], use_cache=True)
        past = out.past_key_values
        cached = {}
        state = MaskedDecodeState(tags["Path"], tags["/Path"], len(targets))
        for j, token in enumerate(response_ids[:targets[1]]):
            position, visible = state.append(token)
            rowmask = torch.zeros(1, 1, 1, p + j + 1, dtype=torch.bfloat16, device="cuda")
            rowmask[..., p:].masked_fill_(~torch.tensor(visible, device="cuda"),
                                          torch.finfo(torch.bfloat16).min)
            out = model(input_ids=ids[:, p + j:p + j + 1], past_key_values=past,
                        attention_mask=rowmask, position_ids=torch.tensor([[p + position]], device="cuda"),
                        cache_position=torch.tensor([p + j], device="cuda"), use_cache=True)
            past = out.past_key_values
            if j + 1 == targets[0]:
                cached["first"] = out.logits[0, -1].float()
            if j + 1 == targets[1]:
                cached["second"] = out.logits[0, -1].float()
    result = {}
    for label, j in (("first", targets[0]), ("second", targets[1])):
        full, inc = reference[p + j - 1].float(), cached[label]
        result[label] = {"full_top": tok.decode([full.argmax().item()]),
                         "cached_top": tok.decode([inc.argmax().item()]),
                         "full_path_prob": torch.softmax(full, -1)[tags["Path"]].item(),
                         "cached_path_prob": torch.softmax(inc, -1)[tags["Path"]].item(),
                         "max_logit_delta": (full - inc).abs().max().item()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
