"""Check shifted tag loss weights without changing tokens, attention or positions."""

import json
import sys

import torch
from transformers import AutoTokenizer

from verl.utils.dataset.parallel_thinking_sft_dataset import (
    ParallelThinkingSFTDataset, collate_cropped,
)


def main():
    model_path, parquet_path = sys.argv[1:3]
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    config = {"prompt_key": "extra_info", "response_key": "extra_info",
              "prompt_dict_keys": ["question"], "response_dict_keys": ["answer"],
              "max_length": 4096, "truncation": "error", "structure": "multiverse",
              "enable_thinking": False}
    ordinary = ParallelThinkingSFTDataset(parquet_path, tokenizer, config)
    weighted = ParallelThinkingSFTDataset(
        parquet_path, tokenizer, config | {"parallel_text_loss_weight": 0.1})
    tag_index = weighted.row_kind.index("parallel_th")
    replay_index = weighted.row_kind.index("replay_th")
    tag_row, replay_row = weighted[tag_index], weighted[replay_index]
    for index, row in ((tag_index, tag_row), (replay_index, replay_row)):
        baseline = ordinary[index]
        for key in ("input_ids", "attention_mask", "position_ids"):
            assert torch.equal(row[key], baseline[key]), (index, key)
    target_ids = tag_row["input_ids"][1:]
    weights = tag_row["loss_mask"][:-1]
    selected = weights > 0
    tags = torch.isin(target_ids, torch.tensor(sorted(weighted.loss_tag_ids))) & selected
    text = selected & ~tags
    assert int(tags.sum()) == 14 and int(text.sum()) > 20
    assert torch.all(weights[tags] == 1) and torch.all(weights[text] == 0.1)
    assert torch.all(replay_row["loss_mask"][replay_row["loss_mask"] > 0] == 1)
    for samples in ([tag_row, replay_row], [replay_row, tag_row]):
        batch = collate_cropped(samples)
        assert batch["loss_mask"].dtype == torch.float32 and batch["loss_mask"].shape[0] == 2
    report = {"tag_targets": int(tags.sum()), "text_targets": int(text.sum()),
              "replay_targets": int((replay_row["loss_mask"] > 0).sum()),
              "batch_dtype": str(batch["loss_mask"].dtype)}
    if len(sys.argv) > 3:
        control = ParallelThinkingSFTDataset(
            sys.argv[3], tokenizer, config | {"parallel_text_loss_weight": 0.1})
        row = control[control.row_kind.index("control_th")]
        weights = row["loss_mask"][:-1]
        selected = weights > 0
        assert selected.sum() > 20 and torch.all(weights[selected] == 0.1)
        report["control_text_targets"] = int(selected.sum())
    print(json.dumps(report))


if __name__ == "__main__":
    main()
