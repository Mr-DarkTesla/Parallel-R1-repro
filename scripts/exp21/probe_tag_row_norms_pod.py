#!/usr/bin/env python3
"""CPU-only safetensors check for 4B structural-tag embedding drift."""
import json
import sys
from pathlib import Path

import torch
from safetensors import safe_open
from transformers import AutoTokenizer


TAGS = ("<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>",
        "</Outline>", "<Path>", "</Path>", "<Conclusion>", "</Conclusion>")
KEY = "model.embed_tokens.weight"


def read(root, low, high):
    root = Path(root)
    shard = json.loads((root / "model.safetensors.index.json").read_text())["weight_map"][KEY]
    with safe_open(root / shard, framework="pt", device="cpu") as handle:
        tensor = handle.get_slice(KEY)
        tags = tensor[low:high].float()
        reference = torch.cat([tensor[i:i + 1024].float().norm(dim=1)
                               for i in (0, 32000, 64000, 96000, 128000)])
    return tags, round(float(reference.median()), 6)


def main():
    base, tagged, plain, output = sys.argv[1:5]
    tok = AutoTokenizer.from_pretrained(base)
    ids = {tag: tok.convert_tokens_to_ids(tag) for tag in TAGS}
    assert len(set(ids.values())) == len(TAGS)
    assert all(tok.encode(tag, add_special_tokens=False) == [idx] for tag, idx in ids.items())
    low, high = min(ids.values()), max(ids.values()) + 1
    weights, medians = {}, {}
    for name, root in (("base", base), ("tagged16", tagged), ("plain16", plain)):
        weights[name], medians[name] = read(root, low, high)
    result = {"models": {"base": base, "tagged16": tagged, "plain16": plain},
              "method": "CPU safetensors slices; existing-row median samples five disjoint 1024-row bands",
              "tag_ids": ids, "sampled_existing_norm_median": medians, "tags": {}}
    for tag, index in ids.items():
        j = index - low
        result["tags"][tag] = {
            "base_norm": round(float(weights["base"][j].norm()), 6),
            "tagged16_norm": round(float(weights["tagged16"][j].norm()), 6),
            "plain16_norm": round(float(weights["plain16"][j].norm()), 6),
            "tagged16_delta_l2": round(float((weights["tagged16"][j] - weights["base"][j]).norm()), 6),
            "plain16_delta_l2": round(float((weights["plain16"][j] - weights["base"][j]).norm()), 6),
            "tagged_plain_delta_l2": round(float((weights["tagged16"][j] - weights["plain16"][j]).norm()), 6),
        }
    Path(output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"median": medians, "root": result["tags"]["<Parallel>"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
