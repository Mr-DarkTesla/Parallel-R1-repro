"""Blend non-tag weights with the base model while keeping learned Multiverse tag rows."""

import argparse
import json
import shutil
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file
from transformers import AutoTokenizer

TAGS = ("<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>",
        "</Outline>", "<Path>", "</Path>", "<Conclusion>", "</Conclusion>")
EMBEDDING = "model.embed_tokens.weight"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("trained", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--alpha", type=float, required=True)
    args = parser.parse_args()
    assert 0 <= args.alpha <= 1
    assert not args.output.exists(), args.output

    tokenizer = AutoTokenizer.from_pretrained(args.trained)
    tag_ids = [tokenizer.convert_tokens_to_ids(tag) for tag in TAGS]
    assert all(tokenizer.encode(tag, add_special_tokens=False) == [tag_id]
               for tag, tag_id in zip(TAGS, tag_ids))

    base_file = args.base / "model.safetensors"
    trained_file = args.trained / "model.safetensors"
    tensors = {}
    with safe_open(base_file, framework="pt", device="cpu") as base, \
            safe_open(trained_file, framework="pt", device="cpu") as trained:
        assert base.keys() == trained.keys()
        assert EMBEDDING in base.keys()
        for key in base.keys():
            original, adapted = base.get_tensor(key), trained.get_tensor(key)
            assert original.shape == adapted.shape and original.dtype == adapted.dtype, key
            blended = torch.lerp(original.float(), adapted.float(), args.alpha).to(original.dtype)
            if key == EMBEDDING:
                blended[tag_ids] = adapted[tag_ids]
            tensors[key] = blended.contiguous()

    args.output.mkdir(parents=True)
    for source in args.trained.iterdir():
        if source.is_file() and source.name != "model.safetensors":
            shutil.copy2(source, args.output / source.name)
    save_file(tensors, args.output / "model.safetensors", metadata={"format": "pt"})
    (args.output / "interpolation.json").write_text(json.dumps({
        "base": str(args.base), "trained": str(args.trained), "alpha": args.alpha,
        "tags": dict(zip(TAGS, tag_ids)),
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
