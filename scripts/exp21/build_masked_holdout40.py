"""Make a fresh 20 GSM8K + 20 MATH masked-decoding holdout from dev.

The output uses the exact Multiverse prompt of fixed40, but excludes its
problems and every supplied SFT training parquet by ID and problem text.
Only prepares CPU data; it never starts an evaluation.

Usage: python build_masked_holdout40.py DEV_PLAIN_DIR FIXED40_DIR OUT_DIR
       --train /path/to/tagged_train.parquet [--train ...] [--seed 21]
"""

import argparse
import json
import random
import re
from pathlib import Path

import pandas as pd

from make_mv_prompts import mv_prompt


SOURCES = {
    "gsm8k": ("gsm8k_dev.parquet", ("gsm8k_dev10", "gsm8k_devnext10")),
    "math": ("math_dev.parquet", ("math_dev10", "math_devnext10")),
}


def identity(row):
    return str(row["extra_info"]["id"])


def problem(text):
    assert "Problem:" in text, "question has no Problem: delimiter"
    return re.sub(r"\s+", " ", text.split("Problem:", 1)[1]).strip().casefold()


def question(row):
    prompt = list(row["prompt"])
    assert len(prompt) == 1 and prompt[0]["role"] == "user"
    return prompt[0]["content"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dev_plain_dir", type=Path)
    parser.add_argument("fixed40_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--train", action="append", type=Path, default=[])
    parser.add_argument("--seed", type=int, default=21)
    args = parser.parse_args()

    excluded_ids, excluded_texts = set(), set()
    for _, stems in SOURCES.values():
        for stem in stems:
            frame = pd.read_parquet(args.fixed40_dir / f"{stem}.parquet")
            assert len(frame) == 10, (stem, len(frame))
            for _, row in frame.iterrows():
                excluded_ids.add(identity(row))
                excluded_texts.add(problem(question(row)))
    fixed_ids = set(excluded_ids)
    train_ids, train_texts = set(), set()
    for path in args.train:
        frame = pd.read_parquet(path)
        assert {"id", "extra_info"}.issubset(frame.columns), path
        for _, row in frame.iterrows():
            train_ids.add(str(row["id"]))
            train_texts.add(problem(row["extra_info"]["question"]))
    excluded_ids |= train_ids
    excluded_texts |= train_texts

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "seed": args.seed,
        "selection": "20 unique problems per source after fixed40 and training exclusions",
        "dev_plain_dir": str(args.dev_plain_dir),
        "fixed40_dir": str(args.fixed40_dir),
        "train_parquets": [str(path) for path in args.train],
        "fixed40_ids": len(fixed_ids),
        "train_ids": len(train_ids),
        "sources": {},
    }
    for offset, (source, (filename, _)) in enumerate(SOURCES.items()):
        frame = pd.read_parquet(args.dev_plain_dir / filename)
        first_index = {}
        source_texts = {}
        for index, row in frame.iterrows():
            item_id, text = identity(row), problem(question(row))
            if item_id in first_index:
                assert source_texts[item_id] == text, (source, item_id)
            else:
                first_index[item_id] = index
                source_texts[item_id] = text
        eligible = sorted(item_id for item_id in first_index
                          if item_id not in excluded_ids
                          and source_texts[item_id] not in excluded_texts)
        assert len(eligible) >= 20, (source, len(eligible))
        chosen = random.Random(args.seed + offset).sample(eligible, 20)
        selected = frame.loc[[first_index[item_id] for item_id in chosen]].copy()
        selected["prompt"] = [[{"role": "user", "content": mv_prompt(question(row))}]
                              for _, row in selected.iterrows()]
        assert len(set(identity(row) for _, row in selected.iterrows())) == 20
        assert not set(chosen).intersection(fixed_ids | train_ids)
        assert not set(source_texts[item_id] for item_id in chosen).intersection(excluded_texts)
        output = args.out_dir / f"{source}_holdout20.parquet"
        selected.to_parquet(output, index=False)
        manifest["sources"][source] = {
            "dev_rows": len(frame), "unique_problems": len(first_index),
            "eligible_problems": len(eligible), "selected_ids": chosen,
            "output": str(output),
        }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({source: len(entry["selected_ids"])
                      for source, entry in manifest["sources"].items()}))


if __name__ == "__main__":
    main()
