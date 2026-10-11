#!/usr/bin/env python3
"""CPU preflight for the real M2 rows and tokenizer before focused CE SFT."""

import json
from collections import Counter
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer

from verl.utils.dataset.parallel_thinking_sft_dataset import ParallelThinkingSFTDataset


ROOT = Path("/work/exp21/expanded_th")
MODEL = Path("/work/assets/models/Qwen3-0.6B-mv")
REPORT = ROOT / "m2_spanfocus_preflight.json"


def audit():
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    dataset = ParallelThinkingSFTDataset.__new__(ParallelThinkingSFTDataset)
    dataset.start_parallel_token = tokenizer.convert_tokens_to_ids("<Parallel>")
    dataset.end_parallel_token = tokenizer.convert_tokens_to_ids("</Parallel>")
    dataset.start_path_token = tokenizer.convert_tokens_to_ids("<Path>")
    dataset.end_path_token = tokenizer.convert_tokens_to_ids("</Path>")
    dataset.structure_tags = {"Parallel": dataset.start_parallel_token,
                              "/Parallel": dataset.end_parallel_token,
                              "Path": dataset.start_path_token,
                              "/Path": dataset.end_path_token}
    dataset.think_start_ids = tokenizer.encode("<think>", add_special_tokens=False)
    dataset.think_end_ids = tokenizer.encode("</think>", add_special_tokens=False)
    for tag in dataset.structure_tags:
        token = f"<{tag}>"
        assert tokenizer.encode(token, add_special_tokens=False) == [tokenizer.convert_tokens_to_ids(token)]

    counts = Counter()
    failures = []
    for split in ("train", "val"):
        frame = pd.read_parquet(ROOT / f"sft_expanded_th_m2_tagged_{split}.parquet")
        for index, extra in enumerate(frame["extra_info"]):
            kind = extra.get("kind")
            counts[f"{split}_{kind}"] += 1
            if kind != "parallel_th":
                continue
            response = extra["answer"]
            token_ids = tokenizer.encode(response + tokenizer.eos_token, add_special_tokens=False)
            span = dataset._validated_parallel_block_span(torch.tensor(token_ids))
            if span is None:
                failures.append({"split": split, "index": index,
                                 "id": extra.get("id"), "reason": "span_not_found"})
                continue
            begin, end = span
            if end - begin < 10:
                failures.append({"split": split, "index": index,
                                 "id": extra.get("id"), "reason": "tiny_block"})
            else:
                counts["positive_spans_valid"] += 1
    positive = counts["train_parallel_th"] + counts["val_parallel_th"]
    result = {"status": "ready" if not failures and counts["positive_spans_valid"] == positive else "reject",
              "model": str(MODEL), "files": [f"sft_expanded_th_m2_tagged_{split}.parquet" for split in ("train", "val")],
              "counts": dict(counts), "positive_expected": positive, "failures": failures}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "positive": positive,
                      "valid": counts["positive_spans_valid"], "failures": len(failures)}))
    if result["status"] != "ready":
        raise SystemExit(1)


if __name__ == "__main__":
    audit()
