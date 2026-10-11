#!/usr/bin/env python3
"""Summarize completed M1-367 fixed40 sweeps with paired intervals.

Only syntactic numbered blocks are counted. Semantic usefulness and any
candidate answer-parser corrections require separate manual review.
"""

import json
import math
import random
import re
import tarfile
from pathlib import Path

from audit_c0_pilot_scoring import FIXES


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
PATTERN = re.compile(r"m1_rewrapped_(tagged|plain)_step(16|35|70)$")
METRICS = ("strict", "robust", "block", "truncated", "tokens", "forward_passes")
STEMS = ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")
STEM_ALIASES = ("gsm10", "gsmnext10", "math10", "mathnext10")
CANONICAL = dict(zip(STEM_ALIASES, STEMS))
PROTOCOL = {"count": 10, "seed": 0, "mode": "thinking",
            "decoder": "masked-autonomous-v2", "policy": "greedy"}


def key(row):
    return row["source"], row["problem_id"], row["sample"]


def decode_jsonl(data):
    # splitlines() also splits valid U+2028 characters inside JSON strings.
    return [json.loads(line) for line in data.decode().split("\n") if line]


def load(path, stems, expected_model=None):
    if path.is_dir():
        if not (path / "DONE").is_file():
            raise ValueError(f"unfinished archive: {path}")

        def read(suffix):
            return (path / suffix).read_bytes()
    else:
        archive = tarfile.open(path)
        names = archive.getnames()

        def read(suffix):
            matches = [name for name in names if name.endswith("/" + suffix)]
            if len(matches) != 1:
                raise ValueError(f"expected one {suffix} in {path}, got {matches}")
            return archive.extractfile(matches[0]).read()

    output = {}
    for stem in stems:
        metadata = json.loads(read(f"{stem}.jsonl.meta.json"))
        if expected_model is not None and metadata.get("model") != expected_model:
            raise ValueError(f"{path}/{stem}: wrong model {metadata.get('model')!r}")
        if not str(metadata.get("data", "")).endswith("/" + CANONICAL.get(stem, stem) + ".parquet"):
            raise ValueError(f"{path}/{stem}: wrong data {metadata.get('data')!r}")
        for field, expected in PROTOCOL.items():
            if metadata.get(field) != expected:
                raise ValueError(f"{path}/{stem}: {field}={metadata.get(field)!r}, expected {expected!r}")
        budget = 4096 if stem.startswith("math") else 2048
        if metadata.get("max_tokens") != budget:
            raise ValueError(f"{path}/{stem}: max_tokens={metadata.get('max_tokens')!r}, expected {budget}")
        scores = decode_jsonl(read(f"{stem}-rows.jsonl"))
        blocks = decode_jsonl(read(f"{stem}-block-rows.jsonl"))
        if len(scores) != 10 or len(blocks) != 10:
            raise ValueError(f"{path}/{stem}: expected ten score and block rows")
        block_by_key = {key(row): row for row in blocks}
        if len(block_by_key) != 10:
            raise ValueError(f"{path}/{stem}: duplicate block key")
        for score in scores:
            k = key(score)
            if k in output or k not in block_by_key:
                raise ValueError(f"{path}/{stem}: duplicate or unmatched score {k}")
            block = block_by_key[k]
            if score["input"] != block["input"] or block["decoder"] != "masked":
                raise ValueError(f"{path}/{stem}: prompt or decoder mismatch at {k}")
            output[k] = {"input": score["input"], "strict": bool(score["acc"]),
                         "robust": bool(block["acc_robust"]),
                         "block": bool(block["think_numbered_block"]),
                         "truncated": bool(block["truncated"]),
                         "tokens": int(block["tokens"]),
                         "forward_passes": int(block["forward_passes"])}
    if len(output) != 40:
        raise ValueError(f"{path}: expected 40 unique rows, got {len(output)}")
    if not path.is_dir():
        archive.close()
    return output


def summary(rows):
    result = {}
    for metric in METRICS:
        values = [row[metric] for row in rows.values()]
        result[metric] = round(sum(values) / len(values), 2) if metric in ("tokens", "forward_passes") else sum(values)
    return result


def interval(base, candidate, keys, metric):
    changes = [float(candidate[k][metric]) - float(base[k][metric]) for k in keys]
    rng = random.Random(0)
    n = len(changes)
    draws = sorted(sum(changes[rng.randrange(n)] for _ in range(n)) / n for _ in range(10_000))
    scale = 1 if metric in ("tokens", "forward_passes") else 100
    result = {"delta": round(scale * sum(changes) / n, 2),
              "ci95": [round(scale * draws[i], 2) for i in (249, 9749)]}
    if metric in ("strict", "robust"):
        lost = sum(base[k][metric] and not candidate[k][metric] for k in keys)
        gained = sum(candidate[k][metric] and not base[k][metric] for k in keys)
        discordant = lost + gained
        result["discordant"] = {"lost": lost, "gained": gained}
        result["mcnemar_exact_p"] = (min(1.0, 2 * sum(math.comb(discordant, j)
                                                         for j in range(min(lost, gained) + 1)) / 2**discordant)
                                     if discordant else 1.0)
    return result


def compare(base, candidate):
    keys = sorted(base)
    if keys != sorted(candidate) or any(base[k]["input"] != candidate[k]["input"] for k in keys):
        raise ValueError("fixed40 keys or prompts differ")
    return {metric: interval(base, candidate, keys, metric) for metric in METRICS}


def main():
    original_raw = load(ARCHIVES / "c0-greedy-pilot40.tgz", STEM_ALIASES)
    original = {k: row.copy() for k, row in original_raw.items()}
    for k in FIXES:
        if k not in original or original[k]["robust"]:
            raise ValueError(f"C0 correction drift at {k}")
        original[k]["robust"] = True
    parent = load(ARCHIVES / "v4_recovery8_step8_masked_pilot.tgz", STEMS)
    compare(original, parent)
    result = {"protocol": "same fixed40 prompts, thinking, masked greedy, 2048 GSM8K / 4096 MATH tokens",
              "notes": ["C0 robust answer has two documented manual parser corrections.",
                        "Other robust answers are automatic parser output pending manual review.",
                        "block counts complete numbered syntax only, not semantic usefulness."],
              "original": summary(original), "parent_v4_recovery8_step8": summary(parent),
              "runs": {}, "tagged_vs_plain": {}}
    runs = {}
    for path in sorted(ARCHIVES.iterdir()):
        match = PATTERN.fullmatch(path.name)
        if match and (path / "DONE").is_file():
            name = f"{match[1]}_step{match[2]}"
            expected_model = (f"/tmp/exp21-selective-runs/exp21-m1-rewrapped-{match[1]}-p70"
                              f"/step_models/step_{match[2]}/model")
            rows = load(path, STEMS, expected_model)
            runs[name] = rows
            result["runs"][name] = {"metrics": summary(rows),
                                    "vs_original": compare(original, rows),
                                    "vs_parent": compare(parent, rows)}
    if not runs:
        raise ValueError("no completed M1-367 fixed40 archives")
    for step in (16, 35, 70):
        tagged, plain = runs.get(f"tagged_step{step}"), runs.get(f"plain_step{step}")
        if tagged is not None and plain is not None:
            result["tagged_vs_plain"][f"step{step}"] = compare(plain, tagged)
    output = ROOT / "audit/m1_rewrapped_sweep_auto.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for name, row in result["runs"].items():
        print(name, row["metrics"], row["vs_original"]["robust"])


if __name__ == "__main__":
    main()
