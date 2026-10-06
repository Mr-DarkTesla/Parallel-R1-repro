"""Add the Parallel-R1 control tokens to a Qwen3 base model."""

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B-Base")
    parser.add_argument("--revision", default="main")
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    set_seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision, torch_dtype=torch.bfloat16)
    original_vocab_size = len(tokenizer)
    tokens = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]
    tokenizer.add_special_tokens({"additional_special_tokens": tokens}, replace_additional_special_tokens=False)
    model.resize_token_embeddings(len(tokenizer))
    # Qwen's padded embedding rows are reused by resize, so initialize the new tokens explicitly.
    with torch.no_grad():
        model.get_input_embeddings().weight[original_vocab_size:].normal_(std=model.config.initializer_range)
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)
    (args.output / "source.json").write_text(json.dumps({
        "model": args.model,
        "revision": model.config._commit_hash,
        "seed": args.seed,
        "token_initialization": "normal",
        "tokens": {token: tokenizer.convert_tokens_to_ids(token) for token in tokens},
    }, indent=2) + "\n")
    print(f"Prepared {args.output}")


if __name__ == "__main__":
    main()
