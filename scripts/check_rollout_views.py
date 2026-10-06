"""Checks exp10 rollout views on a tiny random Qwen3: the copy of a later path must get the same logits as a plain causal
forward over (prefix up to its <Parallel>) + path, and the main sequence the same logits as a plain causal forward.

Usage (from verl/): python ../scripts/check_rollout_views.py <tokenizer_dir> <train.parquet>
"""
import contextlib
import io
import sys

import torch
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

from verl.utils.dataset.parallel_thinking_sft_dataset import ParallelThinkingSFTDataset

tokenizer = AutoTokenizer.from_pretrained(sys.argv[1])
config = {"prompt_key": "extra_info", "prompt_dict_keys": ["question"], "response_key": "extra_info", "response_dict_keys": ["answer"],
          "max_length": 4096, "parallel_structure": False, "rollout_path_views": True}
with contextlib.redirect_stdout(io.StringIO()):
    dataset = ParallelThinkingSFTDataset(sys.argv[2], tokenizer, config)
torch.manual_seed(0)
model = Qwen3ForCausalLM(Qwen3Config(vocab_size=len(tokenizer), hidden_size=64, intermediate_size=128, num_hidden_layers=2, num_attention_heads=4,
                                     num_key_value_heads=2, head_dim=16, max_position_embeddings=4096, attn_implementation="sdpa")).eval()


def logits(ids, **kwargs):
    with torch.no_grad():
        return model(input_ids=ids[None], **kwargs).logits[0]


worst = 0.0
for index in range(8):
    sample = dataset[index]
    total = int(sample["length"])
    ids = sample["input_ids"][:total]
    views = logits(ids, attention_mask=sample["attention_mask"][None, :, :total, :total], position_ids=sample["position_ids"][None, :total])
    positions = sample["position_ids"][:total]
    drops = (positions[1:] <= positions[:-1]).nonzero()
    main_length = int(drops[0]) + 1 if len(drops) else total
    worst = max(worst, (views[:main_length] - logits(ids[:main_length])).abs().max().item())
    cursor = main_length
    while cursor < total:
        start_position = int(positions[cursor])
        end = cursor + 1
        while end < total and sample["attention_mask"][0, end, end - 1] == 0:  # next token of the same copy
            end += 1
        rollout_ids = torch.cat((ids[:start_position], ids[cursor:end]))
        worst = max(worst, (views[cursor:end] - logits(rollout_ids)[start_position:]).abs().max().item())
        assert ids[start_position - 1] == dataset.start_parallel_token
        cursor = end
    loss_targets = ids[1:total][sample["loss_mask"][: total - 1].bool()]
    print(index, "tokens", total, "copies", total - main_length, "trained targets", len(loss_targets))
print("max logit difference vs rollout views:", worst)
