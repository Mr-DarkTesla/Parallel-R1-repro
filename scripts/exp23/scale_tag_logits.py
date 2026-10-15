"""Exp 23 variant: the prepared model with the output rows of the six tags scaled by c; everything else unchanged.

In the prepared model (scripts/instruct4b/prepare_model.py) embeddings are tied and a tag row is the mean of its pieces' rows, so
logit(tag) = mean of the pieces' logits and never beats the best piece: the model writes ">" where the prompt's format has a tag
(scripts/exp23/tag_logits.py: p(tag) 0.0000 at the first answer position). Here lm_head is untied: input embeddings stay the mean
(the prompt's tags read as before), lm_head = the old matrix with the six tag rows times c (logit = c * mean of the pieces' logits).
Usage: python scripts/exp23/scale_tag_logits.py <prepared model> <output dir> <c>
"""
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

IDS = list(range(151669, 151675))
source, output_dir, scale = sys.argv[1], sys.argv[2], float(sys.argv[3])
model = AutoModelForCausalLM.from_pretrained(source, torch_dtype=torch.bfloat16)
embeddings = model.get_input_embeddings().weight.data
assert model.config.tie_word_embeddings and model.get_output_embeddings().weight.data_ptr() == embeddings.data_ptr()
head = embeddings.clone()
head[IDS] = (head[IDS].float() * scale).to(head.dtype)
model.config.tie_word_embeddings = False
model.lm_head.weight = torch.nn.Parameter(head)
model.save_pretrained(output_dir)
AutoTokenizer.from_pretrained(source).save_pretrained(output_dir)

saved = AutoModelForCausalLM.from_pretrained(output_dir, torch_dtype="auto")
original = AutoModelForCausalLM.from_pretrained(source, torch_dtype="auto").get_input_embeddings().weight
out, inp = saved.get_output_embeddings().weight, saved.get_input_embeddings().weight
assert not saved.config.tie_word_embeddings and out.data_ptr() != inp.data_ptr() and torch.equal(inp, original)
changed = (out != original).any(dim=1).nonzero().flatten().tolist()
assert changed == IDS and torch.equal(out[IDS], (original[IDS].float() * scale).to(out.dtype)), changed
print(f"saved {output_dir}: untied, input rows unchanged, lm_head rows {IDS} x {scale}")
