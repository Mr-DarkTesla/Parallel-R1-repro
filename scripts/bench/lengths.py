"""Answer lengths and decode steps per benchmark source for one generation dump.

length: all answer tokens (both paths of every block included).
decode steps: tokens the model decodes one after another. Plain generation: equal to the length (exact token counts from vLLM).
Parallel rollout (paths decoded at the same time): main-chain tokens + per block the longest path + the summary; tokens the rollout
inserts itself (<Path>, </Parallel>, the newline and <Summary>) are not decoded. The rollout dump keeps text only, so it is re-tokenized.

Usage (from verl/): python ../scripts/bench/lengths.py <generations.jsonl> <tokenizer_dir> <test.parquet> <output.json>
"""
import json
import sys

import numpy as np
import pandas as pd
from transformers import AutoTokenizer

generations_path, tokenizer_dir, test_path, output_path = sys.argv[1:5]
generations = pd.read_json(generations_path, lines=True)
sources = pd.read_parquet(test_path)["data_source"].str.removeprefix("APO_").to_numpy()
tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
tag = {name: tokenizer.convert_tokens_to_ids(name) for name in ("<Parallel>", "<Path>", "</Path>", "</Parallel>", "<Summary>", "</Summary>")}


def rollout_steps(ids):
    """Decode steps of one parallel-rollout answer: <Parallel> stops the main chain, then 2 paths, then the summary."""
    steps, i = 0, 0
    while i < len(ids):
        steps += 1
        if ids[i] != tag["<Parallel>"]:
            i += 1
            continue
        i += 1
        paths = []
        while i < len(ids) and ids[i] == tag["<Path>"]:  # inserted by the rollout
            end = ids.index(tag["</Path>"], i) + 1 if tag["</Path>"] in ids[i:] else len(ids)
            paths.append(end - i - 1)
            i = end
        steps += max(paths, default=0)
        while i < len(ids) and ids[i] != tag["<Summary>"] and ids[i] in (tag["</Parallel>"], *tokenizer.encode("\n")):  # inserted
            i += 1
        if i < len(ids) and ids[i] == tag["<Summary>"]:  # inserted, then the summary is decoded up to </Summary>
            i += 1
            end = ids.index(tag["</Summary>"], i) + 1 if tag["</Summary>"] in ids[i:] else len(ids)
            steps += end - i
            i = end
    return steps


if "tokens" in generations:  # plain generation
    lengths = steps = generations["tokens"].to_numpy()
else:
    texts = generations["output"].str.replace(tokenizer.eos_token, "", regex=False)
    encoded = [tokenizer.encode(text, add_special_tokens=False) for text in texts]
    lengths = np.array([len(ids) for ids in encoded])
    steps = np.array([rollout_steps(ids) for ids in encoded])


def stats(values):
    return {"mean": round(float(values.mean()), 1), "median": float(np.median(values)), "p95": float(np.percentile(values, 95))}


summary = {}
for source in pd.unique(sources):
    mask = sources == source
    summary[source] = {"answers": int(mask.sum()), "decode_steps_total": int(steps[mask].sum()),
                       "decode_steps": stats(steps[mask]), "length_tokens": stats(lengths[mask])}
json.dump(summary, open(output_path, "w"), indent=1)
print(json.dumps(summary))
