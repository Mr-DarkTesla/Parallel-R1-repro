"""Add the six parallel-thinking tokens to a Qwen3 base model, as in Parallel-R1/Qwen3-4B-Base-add-special-token.

Each new token embedding starts as the mean embedding of the pieces its text splits into ("<", "Path", ">").
Without this, in Qwen3-0.6B-Base all six tokens get the same unused embedding row and the model cannot tell them apart.
"""
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

TOKENS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]

base_model, output_dir = sys.argv[1], sys.argv[2]
tokenizer = AutoTokenizer.from_pretrained(base_model)
pieces = [tokenizer(token, add_special_tokens=False)["input_ids"] for token in TOKENS]
tokenizer.add_special_tokens({"additional_special_tokens": TOKENS})
model = AutoModelForCausalLM.from_pretrained(base_model)
model.resize_token_embeddings(len(tokenizer))

token_ids = tokenizer.convert_tokens_to_ids(TOKENS)
embeddings = model.get_input_embeddings().weight.data
for token_id, piece_ids in zip(token_ids, pieces):
    embeddings[token_id] = embeddings[piece_ids].mean(dim=0)

assert token_ids == list(range(151669, 151675))
assert model.config.vocab_size == len(tokenizer) == 151675
new = torch.nn.functional.normalize(embeddings[token_ids], dim=1)
assert (new @ new.T).fill_diagonal_(0).max() < 0.99, "new token embeddings must differ"

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
