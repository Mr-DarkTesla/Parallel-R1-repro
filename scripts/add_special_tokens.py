"""Add the six parallel-thinking tokens to a Qwen3 base model, as in Parallel-R1/Qwen3-4B-Base-add-special-token."""
import sys

from transformers import AutoModelForCausalLM, AutoTokenizer

TOKENS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]

base_model, output_dir = sys.argv[1], sys.argv[2]
tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.add_special_tokens({"additional_special_tokens": TOKENS})
model = AutoModelForCausalLM.from_pretrained(base_model)
model.resize_token_embeddings(len(tokenizer))

assert tokenizer.convert_tokens_to_ids(TOKENS) == list(range(151669, 151675))
assert model.config.vocab_size == len(tokenizer) == 151675

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
