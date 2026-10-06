"""Add the six parallel-thinking tokens to the hybrid Qwen3-4B without resizing it.

Usage: python scripts/instruct4b/prepare_model.py /work/assets/models/Qwen3-4B /work/assets/models/Qwen3-4B-instruct-add-special-token
The ids 151669..151674 already lie inside the 151936 embedding rows (unused, identical rows), so the vocabulary keeps
its 151936 rows. Only these six rows of the tied embedding / lm_head change: each becomes the mean of the pieces its
text splits into ("<", "Path", ">"), as in scripts/add_special_tokens.py. bf16 like the source; native chat template kept.
"""
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

TOKENS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]
IDS = list(range(151669, 151675))

source, output_dir = sys.argv[1], sys.argv[2]
tokenizer = AutoTokenizer.from_pretrained(source)
pieces = [tokenizer(token, add_special_tokens=False)["input_ids"] for token in TOKENS]
tokenizer.add_special_tokens({"additional_special_tokens": TOKENS})
assert tokenizer.convert_tokens_to_ids(TOKENS) == IDS and len(tokenizer) == 151675

model = AutoModelForCausalLM.from_pretrained(source, torch_dtype=torch.bfloat16)
embeddings = model.get_input_embeddings().weight.data
assert model.config.vocab_size == embeddings.shape[0] == 151936 and model.config.tie_word_embeddings
assert model.get_output_embeddings().weight.data_ptr() == embeddings.data_ptr()
original = embeddings.clone()
for token_id, piece_ids in zip(IDS, pieces):
    embeddings[token_id] = original[piece_ids].float().mean(dim=0).to(embeddings.dtype)

changed = (embeddings != original).any(dim=1).nonzero().flatten().tolist()
assert changed == IDS, changed
new = torch.nn.functional.normalize(embeddings[IDS].float(), dim=1)
assert (new @ new.T).fill_diagonal_(0).max() < 0.99, "new token embeddings must differ"

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

# The saved checkpoint loads with the same shape, dtype, tying, template and new rows
saved = AutoModelForCausalLM.from_pretrained(output_dir, torch_dtype="auto")
saved_tokenizer = AutoTokenizer.from_pretrained(output_dir)
assert saved.dtype == torch.bfloat16 and saved.config.vocab_size == 151936 and saved.config.tie_word_embeddings
assert torch.equal(saved.get_input_embeddings().weight[IDS], embeddings[IDS])
assert saved_tokenizer.chat_template == AutoTokenizer.from_pretrained(source).chat_template
assert [saved_tokenizer.encode(token) for token in TOKENS] == [[i] for i in IDS]
print(f"saved {output_dir}: vocab_size 151936, changed rows {changed}, bf16, tied, native chat template")
