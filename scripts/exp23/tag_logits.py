"""Exp 23 diagnosis: can the model emit a tag token at all? Teacher forcing over plain-generation dumps (prompt + its own answer).

With tied embeddings and a tag row equal to the mean of its pieces' rows, logit(tag) = mean of the pieces' logits <= the best piece's
logit, so the tag never beats its best piece. Here the output rows of the six tags are scaled by c (logit c * mean), the input rows
stay; c = 1 is the model as is. Per c: at the first answer position (where the prompt's format puts <Parallel>) the probability of
<Parallel> and of any tag; at every other answer position the mean tag probability and the share of positions where a tag is argmax
(tags where the answer had none). Usage: python scripts/exp23/tag_logits.py <model> <dump.jsonl> [rows]
"""
import json
import sys

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

IDS = list(range(151669, 151675))
PARALLEL = 151671
model_path, dump_path = sys.argv[1], sys.argv[2]
rows = int(sys.argv[3]) if len(sys.argv) > 3 else 64
tok = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16).cuda().eval()
W = model.get_output_embeddings().weight
dump = pd.read_json(dump_path, lines=True).iloc[:rows]
scales = (1, 2, 3, 4, 6)
first = {c: [] for c in scales}
rest = {c: [] for c in scales}
with torch.no_grad():
    for text, answer in zip(dump["input"], dump["token_ids"]):
        prompt = tok.encode(text)
        ids = torch.tensor([prompt + answer[:-1]]).cuda()
        h = model.model(ids).last_hidden_state[0, len(prompt) - 1:].float()  # predicts answer[0], answer[1], ...
        base = h @ W.float().T
        for c in scales:
            logits = base.clone()
            logits[:, IDS] *= c
            p = logits.softmax(-1)
            first[c].append((p[0, PARALLEL].item(), p[0, IDS].sum().item()))
            rest[c].append((p[1:, IDS].sum(-1).mean().item(), (logits[1:].argmax(-1).unsqueeze(-1) == torch.tensor(IDS).cuda()).any(-1).float().mean().item()))
for c in scales:
    f, r = torch.tensor(first[c]).mean(0), torch.tensor(rest[c]).mean(0)
    print(json.dumps({"scale": c, "first_pos_p_<Parallel>": round(f[0].item(), 4), "first_pos_p_any_tag": round(f[1].item(), 4),
                      "other_pos_mean_p_tags": round(r[0].item(), 5), "other_pos_tag_argmax_share": round(r[1].item(), 5)}))
