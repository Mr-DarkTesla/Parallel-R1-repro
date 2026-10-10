"""Check Qwen3 tokenizer lengths before the equal-volume inside-thinking SFT."""
import json
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer


DATA = Path("/work/exp21/expanded_th")
tok = AutoTokenizer.from_pretrained("/work/assets/models/Qwen3-0.6B-mv")
report = {}
for method in ("m1", "m2"):
    lengths = []
    for split in ("train", "val"):
        frame = pd.read_parquet(DATA / f"sft_expanded_th_{method}_tagged_{split}.parquet")
        for info in frame["extra_info"]:
            prompt = tok.apply_chat_template([{"role": "user", "content": info["question"]}],
                                             add_generation_prompt=True, tokenize=True,
                                             enable_thinking=info["enable_thinking"])
            answer = tok.encode(info["answer"], add_special_tokens=False)
            lengths.append(len(prompt) + len(answer))
    report[method] = {"rows": len(lengths), "max": max(lengths),
                      "over_4096": sum(length > 4096 for length in lengths)}
assert all(item["rows"] == 2301 and item["over_4096"] == 0 for item in report.values())
(DATA / "lengths.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
