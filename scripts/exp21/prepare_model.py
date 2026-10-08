"""Add the ten Multiverse tags (scripts/exp21/mv_format.py TAGS) to the hybrid Qwen3-0.6B without resizing it, with distinct rows.

Usage: python scripts/exp21/prepare_model.py /work/assets/models/Qwen3-0.6B /work/assets/models/Qwen3-0.6B-mv
IDs 151669..151678 lie inside the 151936 embedding rows (unused), so the shape stays. The tied embedding / lm_head is the only change.
Init (FINDING-root-tag-embeddings: mean-of-pieces rows of exp 13-15 were close to each other and to their text pieces, and the model
wrote closing tags as text): row = mean of the pieces of the tag's word ("Parallel") + a shared open or close direction + a random
direction of its own, scaled to the mean norm of ordinary rows. Checked: pairwise cosine of the ten rows <= 0.5, open != close.
"""
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from mv_format import TAGS  # noqa: E402

FIRST_ID = 151669
source, output_dir = sys.argv[1], sys.argv[2]
tokenizer = AutoTokenizer.from_pretrained(source)
assert len(tokenizer) == FIRST_ID, len(tokenizer)
words = [tokenizer(" " + tag.strip("</>"), add_special_tokens=False)["input_ids"] for tag in TAGS]
tokenizer.add_special_tokens({"additional_special_tokens": TAGS})
ids = tokenizer.convert_tokens_to_ids(TAGS)
assert ids == list(range(FIRST_ID, FIRST_ID + len(TAGS))), ids

model = AutoModelForCausalLM.from_pretrained(source, torch_dtype=torch.bfloat16)
embeddings = model.get_input_embeddings().weight.data
assert model.config.vocab_size == embeddings.shape[0] == 151936 and model.config.tie_word_embeddings
assert model.get_output_embeddings().weight.data_ptr() == embeddings.data_ptr()
original = embeddings.clone()
ordinary = original[:FIRST_ID].float()
norm = ordinary.norm(dim=1).mean()
unit = lambda v: v / v.norm()  # noqa: E731
generator = torch.Generator().manual_seed(0)
random = [unit(torch.randn(embeddings.shape[1], generator=generator)) for _ in range(len(TAGS) + 2)]
open_dir, close_dir = random[-2], random[-1]
for k, (token_id, tag, pieces) in enumerate(zip(ids, TAGS, words)):
    word = unit(ordinary[pieces].mean(dim=0))
    row = word + 0.5 * (close_dir if tag.startswith("</") else open_dir) + random[k]
    embeddings[token_id] = (norm * unit(row)).to(embeddings.dtype)

changed = (embeddings != original).any(dim=1).nonzero().flatten().tolist()
assert changed == ids, changed
new = torch.nn.functional.normalize(embeddings[ids].float(), dim=1)
cos = (new @ new.T).fill_diagonal_(0)
assert cos.max() <= 0.5, cos.max()
print(f"tag rows: norm {embeddings[ids].float().norm(dim=1).mean():.3f} (ordinary {norm:.3f}), pairwise cos max {cos.max():.3f}")

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
saved = AutoModelForCausalLM.from_pretrained(output_dir, torch_dtype="auto")
saved_tokenizer = AutoTokenizer.from_pretrained(output_dir)
assert saved.dtype == torch.bfloat16 and saved.config.vocab_size == 151936 and saved.config.tie_word_embeddings
assert torch.equal(saved.get_input_embeddings().weight[ids], embeddings[ids])
assert saved_tokenizer.chat_template == AutoTokenizer.from_pretrained(source).chat_template
assert [saved_tokenizer.encode(tag) for tag in TAGS] == [[i] for i in ids]
print(f"saved {output_dir}: vocab_size 151936, changed rows {changed}, bf16, tied, native chat template")
