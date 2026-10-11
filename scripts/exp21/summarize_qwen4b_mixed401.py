#!/usr/bin/env python3
"""Summarize paired 4B mixed401 fixed40 archives without re-scoring outputs.

Expected archive directories below ``eval_archives``:
``qwen4b_mixed401_{tagged,plain}_step128``.  Each is compared with the
prepared 4B initial model, its matching Sol196 step-16 parent, and its paired
mixed401 arm.  All comparisons require identical fixed40 keys and prompts.
"""

import argparse
import json
import math
import random
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVE_NAMES = {
    "initial": "qwen4b_init_fixed40",
    "sol196_tagged_step16": "qwen4b_sol61_tagged_step16",
    "sol196_plain_step16": "qwen4b_sol61_plain_step16",
    "mixed401_tagged_step128": "qwen4b_mixed401_tagged_step128",
    "mixed401_plain_step128": "qwen4b_mixed401_plain_step128",
}
STEMS = (
    ("gsm8k_dev10", "GSM8K_DEV", 2048),
    ("gsm8k_devnext10", "GSM8K_DEV", 2048),
    ("math_dev10", "MATH_DEV", 4096),
    ("math_devnext10", "MATH_DEV", 4096),
)
METRICS = ("strict", "robust", "block", "truncated", "tokens", "forward_passes")
PROTOCOL = {"count": 10, "seed": 0, "mode": "thinking",
            "decoder": "masked-autonomous-v2", "policy": "greedy"}


class SummaryError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise SummaryError(message)


def read_jsonl(path):
    try:
        # ``splitlines`` would split valid U+2028 text inside a JSON string.
        return [json.loads(line) for line in path.read_text().split("\n") if line]
    except json.JSONDecodeError as error:
        raise SummaryError(f"invalid JSONL {path}: {error}") from error


def read_json(path):
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise SummaryError(f"invalid JSON {path}: {error}") from error


def row_key(row):
    return row["source"], row["problem_id"], row["sample"]


def expected_model(label):
    if label == "initial":
        return "/tmp/exp21-qwen3-4b-mv10"
    if label.startswith("sol196_"):
        arm = label.split("_")[1]
        return f"/tmp/exp21-selective-runs/exp21-4b-sol61-{arm}-p16/step_models/step_16/model"
    arm = label.split("_")[1]
    return f"/tmp/exp21-selective-runs/exp21-4b-mixed401-{arm}-p128/step_models/step_128/model"


def load_archive(archives, label):
    path = archives / ARCHIVE_NAMES[label]
    require((path / "DONE").is_file(), f"{label}: unfinished or missing archive {path}")
    rows = {}
    for stem, expected_source, budget in STEMS:
        meta_path = path / f"{stem}.jsonl.meta.json"
        score_path = path / f"{stem}-rows.jsonl"
        block_path = path / f"{stem}-block-rows.jsonl"
        require(meta_path.is_file() and score_path.is_file() and block_path.is_file(),
                f"{label}/{stem}: missing metadata, score rows, or block rows")
        metadata = read_json(meta_path)
        require(metadata.get("model") == expected_model(label),
                f"{label}/{stem}: wrong model {metadata.get('model')!r}")
        require(str(metadata.get("data", "")).endswith(f"/masked_pilot/{stem}.parquet"),
                f"{label}/{stem}: wrong data {metadata.get('data')!r}")
        for field, value in PROTOCOL.items():
            require(metadata.get(field) == value,
                    f"{label}/{stem}: {field}={metadata.get(field)!r}, expected {value!r}")
        require(metadata.get("max_tokens") == budget,
                f"{label}/{stem}: max_tokens={metadata.get('max_tokens')!r}, expected {budget}")

        score_rows, block_rows = read_jsonl(score_path), read_jsonl(block_path)
        require(len(score_rows) == len(block_rows) == 10, f"{label}/{stem}: expected ten rows")
        blocks = {row_key(row): row for row in block_rows}
        require(len(blocks) == 10, f"{label}/{stem}: duplicate block key")
        for score in score_rows:
            key = row_key(score)
            require(key not in rows and key in blocks, f"{label}/{stem}: unmatched or duplicate score key {key}")
            block = blocks[key]
            require(score["source"] == expected_source and score["input"] == block["input"],
                    f"{label}/{stem}: source or prompt mismatch at {key}")
            require(block.get("decoder") == "masked", f"{label}/{stem}: non-masked block row at {key}")
            for field in ("acc_robust", "truncated", "tokens", "forward_passes"):
                if field in score:
                    require(score[field] == block[field],
                            f"{label}/{stem}: score/block {field} mismatch at {key}")
            rows[key] = {
                "input": score["input"],
                "strict": bool(score["acc"]),
                "robust": bool(block["acc_robust"]),
                "block": bool(block["think_numbered_block"]),
                "truncated": bool(block["truncated"]),
                "tokens": int(block["tokens"]),
                "forward_passes": int(block["forward_passes"]),
            }
    require(len(rows) == 40, f"{label}: expected fixed40, got {len(rows)} rows")
    require(sum(key[0] == "GSM8K_DEV" for key in rows) == 20, f"{label}: wrong GSM8K count")
    require(sum(key[0] == "MATH_DEV" for key in rows) == 20, f"{label}: wrong MATH count")
    return rows


def same_fixed40(reference, candidate, label):
    require(set(reference) == set(candidate), f"{label}: fixed40 keys differ")
    for key in reference:
        require(reference[key]["input"] == candidate[key]["input"], f"{label}: prompt drift at {key}")


def summarize(rows):
    output = {}
    for metric in METRICS:
        values = [float(row[metric]) for row in rows.values()]
        if metric in ("tokens", "forward_passes"):
            output[metric] = {"mean": round(sum(values) / len(values), 2)}
        else:
            count = int(sum(values))
            output[metric] = {"count": count, "percent": round(100 * count / len(values), 2)}
    return output


def paired_interval(reference, candidate, metric):
    keys = sorted(reference)
    changes = [float(candidate[key][metric]) - float(reference[key][metric]) for key in keys]
    rng = random.Random(0)
    n = len(changes)
    draws = sorted(sum(changes[rng.randrange(n)] for _ in range(n)) / n for _ in range(10_000))
    binary = metric not in ("tokens", "forward_passes")
    scale = 100 if binary else 1
    result = {
        "reference": round(scale * sum(float(reference[key][metric]) for key in keys) / n, 2),
        "candidate": round(scale * sum(float(candidate[key][metric]) for key in keys) / n, 2),
        "delta": round(scale * sum(changes) / n, 2),
        "ci95": [round(scale * draws[index], 2) for index in (249, 9749)],
        "unit": "percentage_points" if binary else "tokens",
        "n": n,
    }
    if metric in ("strict", "robust"):
        lost = sum(reference[key][metric] and not candidate[key][metric] for key in keys)
        gained = sum(candidate[key][metric] and not reference[key][metric] for key in keys)
        discordant = lost + gained
        result["discordant"] = {"lost": lost, "gained": gained}
        result["mcnemar_exact_p"] = (
            min(1.0, 2 * sum(math.comb(discordant, i) for i in range(min(lost, gained) + 1)) / 2 ** discordant)
            if discordant else 1.0
        )
    return result


def compare(reference, candidate):
    same_fixed40(reference, candidate, "paired comparison")
    return {metric: paired_interval(reference, candidate, metric) for metric in METRICS}


def build_result(archives):
    rows = {label: load_archive(archives, label) for label in ARCHIVE_NAMES}
    initial = rows["initial"]
    for label, candidate in rows.items():
        same_fixed40(initial, candidate, label)
    variants = {}
    for arm in ("tagged", "plain"):
        label = f"mixed401_{arm}_step128"
        parent = f"sol196_{arm}_step16"
        variants[label] = {
            "archive": ARCHIVE_NAMES[label],
            "model": expected_model(label),
            "metrics": summarize(rows[label]),
            "vs_initial": compare(initial, rows[label]),
            "vs_sol196_step16": compare(rows[parent], rows[label]),
        }
    return {
        "protocol": {
            "fixed40": "same 20 GSM8K_DEV and 20 MATH_DEV prompts",
            "generation": "thinking, masked-autonomous-v2, greedy, seed 0",
            "budgets": "2048 GSM8K, 4096 MATH",
            "intervals": "10,000 deterministic paired bootstrap resamples; binary deltas in percentage points",
        },
        "provenance": {label: {"archive": ARCHIVE_NAMES[label], "model": expected_model(label)}
                       for label in ARCHIVE_NAMES},
        "references": {
            "initial": {"archive": ARCHIVE_NAMES["initial"], "metrics": summarize(initial)},
            "sol196_tagged_step16": {"archive": ARCHIVE_NAMES["sol196_tagged_step16"],
                                      "metrics": summarize(rows["sol196_tagged_step16"])},
            "sol196_plain_step16": {"archive": ARCHIVE_NAMES["sol196_plain_step16"],
                                     "metrics": summarize(rows["sol196_plain_step16"])},
        },
        "variants": variants,
        "tagged_vs_plain": compare(rows["mixed401_plain_step128"], rows["mixed401_tagged_step128"]),
    }


def write_fixture_archive(archives, label, offset):
    path = archives / ARCHIVE_NAMES[label]
    path.mkdir()
    (path / "DONE").write_text("fixture\n")
    for stem, source, budget in STEMS:
        metadata = {"model": expected_model(label), "data": f"/work/exp21/masked_pilot/{stem}.parquet",
                    "count": 10, "max_tokens": budget, **PROTOCOL}
        (path / f"{stem}.jsonl.meta.json").write_text(json.dumps(metadata))
        scores, blocks = [], []
        for index in range(10):
            prompt = f"fixture {stem} {index}"
            row = {"source": source, "problem_id": f"{stem}/{index}", "sample": 0, "input": prompt}
            robust = (index + offset) % 3 != 0
            block = (index + offset) % 4 == 0
            truncated = index == 9 and offset % 2 == 1
            tokens = 100 + index + offset
            score = {**row, "acc": robust, "acc_robust": robust, "truncated": truncated,
                     "tokens": tokens, "forward_passes": tokens - int(block)}
            scores.append(score)
            blocks.append({**row, "decoder": "masked", "acc_robust": robust,
                           "think_numbered_block": block, "truncated": truncated,
                           "tokens": tokens, "forward_passes": tokens - int(block)})
        for suffix, values in (("-rows.jsonl", scores), ("-block-rows.jsonl", blocks)):
            (path / f"{stem}{suffix}").write_text("".join(json.dumps(row) + "\n" for row in values))


def self_test():
    with tempfile.TemporaryDirectory() as directory:
        archives = Path(directory)
        for offset, label in enumerate(ARCHIVE_NAMES):
            write_fixture_archive(archives, label, offset)
        result = build_result(archives)
        require(set(result["variants"]) == {"mixed401_tagged_step128", "mixed401_plain_step128"},
                "fixture variants missing")
        require(result["tagged_vs_plain"]["robust"]["n"] == 40, "fixture paired n drift")
        require("mcnemar_exact_p" in result["variants"]["mixed401_tagged_step128"]["vs_initial"]["strict"],
                "fixture strict interval missing McNemar")
        metadata_path = archives / ARCHIVE_NAMES["mixed401_tagged_step128"] / "gsm8k_dev10.jsonl.meta.json"
        metadata = read_json(metadata_path)
        metadata["model"] = "wrong-parent"
        metadata_path.write_text(json.dumps(metadata))
        try:
            load_archive(archives, "mixed401_tagged_step128")
        except SummaryError as error:
            require("wrong model" in str(error), "fixture provenance rejection drift")
        else:
            raise SummaryError("fixture accepted wrong model provenance")
    print("self-test passed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archives", type=Path, default=ROOT / "eval_archives")
    parser.add_argument("--output", type=Path, default=ROOT / "audit/qwen4b_mixed401_paired.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = build_result(args.archives.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({name: item["metrics"] for name, item in result["variants"].items()}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (SummaryError, FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
