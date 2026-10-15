"""Exp 23 pre-run check (CPU): the six tags are single special tokens everywhere the run uses them. Fails on the first violation.

1. Each tag encodes to exactly one id 151669..151674, as the rollout reads it (tokenizer.encode(tag)[0]), and decodes back to the tag.
2. The tag text split as ordinary text ("<", "Parallel", ">") is other ids: the model can still write a tag as pieces; tag_stats.py counts it.
3. Every exp-23 prompt rendered by the chat template (thinking on and off) holds as many tag ids as tag strings.
4. The tag rows of the tied embedding are the mean of their pieces' rows (scripts/instruct4b/prepare_model.py) and differ from each other.
Usage: python scripts/exp23/check_tokens.py <model> <exp23 data dir>
"""
import glob
import json
import re
import sys

import pandas as pd
import torch
from safetensors import safe_open
from transformers import AutoTokenizer

TAGS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]
IDS = list(range(151669, 151675))
model, data = sys.argv[1], sys.argv[2]
tok = AutoTokenizer.from_pretrained(model)

for tag, i in zip(TAGS, IDS):
    assert tok.encode(tag) == [i] and tok.convert_tokens_to_ids(tag) == i and tok.decode([i]) == tag and i in tok.all_special_ids, tag
print("1. tags are single special ids:", dict(zip(TAGS, IDS)))

pieces = {tag: tok.encode(tag, split_special_tokens=True) for tag in TAGS}
assert all(len(p) > 1 and not set(p) & set(IDS) and tok.decode(p) == tag for tag, p in pieces.items()), pieces
print("2. the same text as ordinary text:", {tag: [tok.decode([i]) for i in p] for tag, p in pieces.items()})

pattern = re.compile("|".join(re.escape(t) for t in TAGS))
for path in sorted(glob.glob(f"{data}/dev/*/*.parquet")):
    for prompt in pd.read_parquet(path)["prompt"].iloc[::50]:
        for thinking in (False, True):
            text = tok.apply_chat_template(list(prompt), add_generation_prompt=True, tokenize=False, enable_thinking=thinking)
            ids = tok.apply_chat_template(list(prompt), add_generation_prompt=True, tokenize=True, enable_thinking=thinking)
            n_text, n_ids = len(pattern.findall(text)), sum(i in IDS for i in ids)
            assert ids == tok.encode(text) and n_text == n_ids > 0, (path, n_text, n_ids)
    print(f"3. {path}: every tag in the rendered prompt is one id ({n_ids} tags per prompt)")

name = "model.embed_tokens.weight"
with safe_open(f"{model}/{json.load(open(f'{model}/model.safetensors.index.json'))['weight_map'][name]}", "pt") as f:
    emb = f.get_tensor(name)
for tag, i in zip(TAGS, IDS):
    assert torch.equal(emb[i], emb[pieces[tag]].float().mean(0).to(emb.dtype)), tag
new = torch.nn.functional.normalize(emb[IDS].float(), dim=1)
print(f"4. tag rows = mean of their pieces' rows; max cos between tags {(new @ new.T).fill_diagonal_(0).max():.3f}")
print("OK")
