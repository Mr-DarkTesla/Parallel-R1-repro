#!/usr/bin/env python3
"""Summarize paired Qwen3-4B fixed40 checkpoint archives.

The script is deliberately limited to automatic fixed40 measurements.  A
well-formed numbered block is a structural property, not evidence that its
paths are semantically useful; that verdict remains a separate human review.
"""

import argparse
import json
import math
import random
import tempfile
from pathlib import Path

from summarize_qwen4b_mixed401 import (
    ARCHIVE_NAMES as PARENT_ARCHIVES,
    PROTOCOL,
    ROOT,
    STEMS,
    SummaryError,
    load_archive,
    read_json,
    read_jsonl,
    require,
    row_key,
)


ARCHIVES = ROOT / "eval_archives"
OUTPUT = ROOT / "audit/qwen4b_onpolicy189_paired.json"
ARMS = ("tagged", "plain")
STEPS = (8, 16, 32)
METRICS = ("strict", "robust", "full_numbered_block", "truncated", "tokens", "forward_passes")
NUMERIC_METRICS = {"tokens", "forward_passes"}
BASE_LABEL = "initial"
VARIANT = "onpolicy189"


def candidate_label(arm, step):
    return f"{VARIANT}_{arm}_step{step}"


def archive_name(arm, step):
    return f"qwen4b_{VARIANT}_{arm}_step{step}"


def expected_model(arm, step):
    return (f"/tmp/exp21-selective-runs/exp21-4b-{VARIANT}-{arm}-p32/"
            f"step_models/step_{step}/model")


def row_truth(row, field, context):
    value = row.get(field)
    require(type(value) is bool, f"{context}: {field} must be boolean")
    return value


def load_onpolicy_archive(archives, arm, step):
    label = candidate_label(arm, step)
    path = archives / archive_name(arm, step)
    require((path / "DONE").is_file(), f"{label}: unfinished or missing archive {path}")
    rows = {}
    for stem, expected_source, budget in STEMS:
        meta_path = path / f"{stem}.jsonl.meta.json"
        score_path = path / f"{stem}-rows.jsonl"
        block_path = path / f"{stem}-block-rows.jsonl"
        require(meta_path.is_file() and score_path.is_file() and block_path.is_file(),
                f"{label}/{stem}: missing metadata, score rows, or block rows")
        metadata = read_json(meta_path)
        require(metadata.get("model") == expected_model(arm, step),
                f"{label}/{stem}: wrong model {metadata.get('model')!r}")
        require(str(metadata.get("data", "")).endswith(f"/masked_pilot/{stem}.parquet"),
                f"{label}/{stem}: wrong data {metadata.get('data')!r}")
        for field, value in PROTOCOL.items():
            require(metadata.get(field) == value,
                    f"{label}/{stem}: {field}={metadata.get(field)!r}, expected {value!r}")
        require(metadata.get("max_tokens") == budget,
                f"{label}/{stem}: max_tokens={metadata.get('max_tokens')!r}, expected {budget}")

        scores, block_rows = read_jsonl(score_path), read_jsonl(block_path)
        require(len(scores) == len(block_rows) == 10, f"{label}/{stem}: expected ten rows")
        blocks = {row_key(row): row for row in block_rows}
        require(len(blocks) == 10, f"{label}/{stem}: duplicate block key")
        for score in scores:
            key = row_key(score)
            require(key not in rows and key in blocks,
                    f"{label}/{stem}: unmatched or duplicate score key {key}")
            block = blocks[key]
            require(score["source"] == expected_source,
                    f"{label}/{stem}: wrong source at {key}")
            require(score.get("problem") == block.get("problem"),
                    f"{label}/{stem}: question mismatch at {key}")
            require(score.get("input") == block.get("input"),
                    f"{label}/{stem}: prompt mismatch at {key}")
            require(block.get("decoder") == "masked",
                    f"{label}/{stem}: non-masked block row at {key}")
            for field in ("acc_robust", "truncated", "tokens", "forward_passes"):
                if field in score:
                    require(score[field] == block.get(field),
                            f"{label}/{stem}: score/block {field} mismatch at {key}")
            robust = row_truth(block, "acc_robust", f"{label}/{stem} {key}")
            strict = row_truth(score, "acc", f"{label}/{stem} {key}")
            full = row_truth(block, "think_full_block", f"{label}/{stem} {key}")
            numbered = row_truth(block, "think_numbered_block", f"{label}/{stem} {key}")
            truncated = row_truth(block, "truncated", f"{label}/{stem} {key}")
            tokens, passes = int(block["tokens"]), int(block["forward_passes"])
            require(0 <= passes <= tokens <= budget,
                    f"{label}/{stem}: invalid token/ideal-forward limits at {key}")
            rows[key] = {
                "question": score["problem"],
                "input": score["input"],
                "strict": strict,
                "robust": robust,
                "full_numbered_block": full and numbered,
                "truncated": truncated,
                "tokens": tokens,
                "forward_passes": passes,
            }
    require(len(rows) == 40, f"{label}: expected fixed40, got {len(rows)} rows")
    require(sum(key[0] == "GSM8K_DEV" for key in rows) == 20, f"{label}: wrong GSM8K count")
    require(sum(key[0] == "MATH_DEV" for key in rows) == 20, f"{label}: wrong MATH count")
    return rows


def same_fixed40(reference, candidate, label):
    require(set(reference) == set(candidate), f"{label}: fixed40 keys differ")
    for key in sorted(reference):
        require(reference[key]["question"] == candidate[key]["question"],
                f"{label}: question drift at {key}")
        require(reference[key]["input"] == candidate[key]["input"],
                f"{label}: prompt drift at {key}")


def complete_reference_rows(rows, archives, label):
    """Restore checked question and full-block fields omitted by the shared loader."""
    path = archives / PARENT_ARCHIVES[label]
    seen = set()
    for stem, source, budget in STEMS:
        scores = read_jsonl(path / f"{stem}-rows.jsonl")
        blocks = {row_key(block): block for block in read_jsonl(path / f"{stem}-block-rows.jsonl")}
        require(len(blocks) == len(scores), f"{label}/{stem}: duplicate or missing block key")
        for score in scores:
            key = row_key(score)
            block = blocks[key]
            require(score.get("source") == source, f"{label}/{stem}: wrong source at {key}")
            require(score.get("problem") == block.get("problem"),
                    f"{label}/{stem}: question mismatch at {key}")
            require(score.get("input") == block.get("input"),
                    f"{label}/{stem}: prompt mismatch at {key}")
            require(block.get("decoder") == "masked",
                    f"{label}/{stem}: non-masked block row at {key}")
            robust = row_truth(block, "acc_robust", f"{label}/{stem} {key}")
            strict = row_truth(score, "acc", f"{label}/{stem} {key}")
            full = row_truth(block, "think_full_block", f"{label}/{stem} {key}")
            numbered = row_truth(block, "think_numbered_block", f"{label}/{stem} {key}")
            truncated = row_truth(block, "truncated", f"{label}/{stem} {key}")
            tokens, passes = int(block["tokens"]), int(block["forward_passes"])
            require(0 <= passes <= tokens <= budget,
                    f"{label}/{stem}: invalid token/ideal-forward limits at {key}")
            require(rows[key]["input"] == score["input"] and rows[key]["robust"] == robust
                    and rows[key]["truncated"] == truncated and rows[key]["tokens"] == tokens
                    and rows[key]["forward_passes"] == passes,
                    f"{label}/{stem}: shared-loader row mismatch at {key}")
            rows[key]["question"] = score["problem"]
            rows[key]["strict"] = strict
            rows[key]["full_numbered_block"] = full and numbered
            seen.add(key)
    require(seen == set(rows), f"{label}: question rows differ")
    return rows


def load_reference_archive(archives, label):
    loaded = load_archive(archives, label)
    rows = {key: {
        "question": row["input"],
        "input": row["input"],
        "strict": False,
        "robust": row["robust"],
        "full_numbered_block": row["block"],
        "truncated": row["truncated"],
        "tokens": row["tokens"],
        "forward_passes": row["forward_passes"],
    } for key, row in loaded.items()}
    return complete_reference_rows(rows, archives, label)


def summarize(rows):
    result = {}
    for metric in METRICS:
        values = [float(row[metric]) for row in rows.values()]
        if metric in NUMERIC_METRICS:
            result[metric] = {"mean": round(sum(values) / len(values), 2)}
        else:
            count = int(sum(values))
            result[metric] = {"count": count, "percent": round(100 * count / len(values), 2)}
    return result


def paired_interval(reference, candidate, metric):
    keys = sorted(reference)
    changes = [float(candidate[key][metric]) - float(reference[key][metric]) for key in keys]
    rng = random.Random(0)
    size = len(changes)
    draws = sorted(sum(changes[rng.randrange(size)] for _ in range(size)) / size
                   for _ in range(10_000))
    numeric = metric in NUMERIC_METRICS
    scale = 1 if numeric else 100
    result = {
        "reference": round(scale * sum(float(reference[key][metric]) for key in keys) / size, 2),
        "candidate": round(scale * sum(float(candidate[key][metric]) for key in keys) / size, 2),
        "delta": round(scale * sum(changes) / size, 2),
        "ci95": [round(scale * draws[index], 2) for index in (249, 9749)],
        "unit": "ideal_forward_passes" if metric == "forward_passes"
        else "tokens" if metric == "tokens" else "percentage_points",
        "n": size,
    }
    if metric == "robust":
        lost = sum(reference[key][metric] and not candidate[key][metric] for key in keys)
        gained = sum(candidate[key][metric] and not reference[key][metric] for key in keys)
        discordant = lost + gained
        result["discordant"] = {"lost": lost, "gained": gained}
        result["mcnemar_exact_p"] = (
            min(1.0, 2 * sum(math.comb(discordant, index)
                             for index in range(min(lost, gained) + 1)) / 2 ** discordant)
            if discordant else 1.0
        )
    return result


def compare(reference, candidate, label):
    same_fixed40(reference, candidate, label)
    return {metric: paired_interval(reference, candidate, metric) for metric in METRICS}


def build_result(archives):
    initial = load_reference_archive(archives, BASE_LABEL)
    parents = {arm: load_reference_archive(archives, f"mixed401_{arm}_step128") for arm in ARMS}
    candidates = {(arm, step): load_onpolicy_archive(archives, arm, step)
                  for step in STEPS for arm in ARMS}
    for arm in ARMS:
        same_fixed40(initial, parents[arm], f"base4b vs mixed401 {arm}")
        for step in STEPS:
            same_fixed40(initial, candidates[arm, step], f"base4b vs {arm} step{step}")
            same_fixed40(parents[arm], candidates[arm, step], f"parent vs {arm} step{step}")

    variants = {}
    tagged_vs_plain = {}
    for step in STEPS:
        tagged, plain = candidates["tagged", step], candidates["plain", step]
        tagged_vs_plain[f"step{step}"] = compare(plain, tagged, f"tagged vs plain step{step}")
        for arm, rows in (("tagged", tagged), ("plain", plain)):
            label = candidate_label(arm, step)
            variants[label] = {
                "archive": archive_name(arm, step),
                "model": expected_model(arm, step),
                "metrics": summarize(rows),
                "vs_base4b": compare(initial, rows, f"base4b vs {label}"),
                "vs_parent_mixed401_step128": compare(parents[arm], rows,
                                                        f"parent vs {label}"),
            }
    return {
        "schema_version": 1,
        "protocol": {
            "fixed40": "same 20 GSM8K_DEV and 20 MATH_DEV questions, prompts, IDs, and samples",
            "generation": "thinking, masked-autonomous-v2, masked decoder, greedy, seed 0",
            "limits": "2048 GSM8K and 4096 MATH max_tokens; 0 <= ideal forward passes <= tokens <= max_tokens",
            "intervals": "10,000 deterministic paired bootstrap resamples; binary deltas in percentage points",
        },
        "metric_definitions": {
            "strict": "automatic archive acc; exact final-answer format and correctness",
            "robust": "automatic archive acc_robust; no human semantic conclusion",
            "full_numbered_block": "think_full_block and think_numbered_block inside <think>; structural only",
            "truncated": "archive truncation flag",
            "tokens": "mean generated tokens",
            "forward_passes": "mean ideal sequential decoding passes under grammatical parallel paths; not measured hardware runtime",
        },
        "semantic_review": {
            "status": "pending_human_review",
            "rule": "Do not infer semantic usefulness or path independence from parser fields.",
        },
        "provenance": {
            "base4b": {"archive": PARENT_ARCHIVES[BASE_LABEL], "model": "/tmp/exp21-qwen3-4b-mv10"},
            "mixed401_parents": {
                arm: {"archive": PARENT_ARCHIVES[f"mixed401_{arm}_step128"],
                      "model": f"/tmp/exp21-selective-runs/exp21-4b-mixed401-{arm}-p128/step_models/step_128/model"}
                for arm in ARMS
            },
        },
        "base4b": {"metrics": summarize(initial)},
        "parents": {arm: {"metrics": summarize(parents[arm])} for arm in ARMS},
        "variants": variants,
        "tagged_vs_plain_by_step": tagged_vs_plain,
    }


def write_fixture_archive(archives, name, model, offset):
    path = archives / name
    path.mkdir()
    (path / "DONE").write_text("fixture\n")
    for stem, source, budget in STEMS:
        metadata = {"model": model, "data": f"/work/exp21/masked_pilot/{stem}.parquet",
                    "max_tokens": budget, **PROTOCOL}
        (path / f"{stem}.jsonl.meta.json").write_text(json.dumps(metadata))
        scores, blocks = [], []
        for index in range(10):
            row = {"source": source, "problem_id": f"{stem}/{index}", "sample": 0,
                   "problem": f"fixture question {stem} {index}", "input": f"fixture prompt {stem} {index}"}
            robust = (index + offset) % 3 != 0
            full, numbered = index % 2 == 0, (index + offset) % 4 != 1
            tokens = 100 + index + offset
            passes = tokens - int(full and numbered)
            score = {**row, "acc": robust, "acc_robust": robust, "truncated": index == 9,
                     "tokens": tokens, "forward_passes": passes}
            block = {**row, "decoder": "masked", "acc_robust": robust,
                     "think_full_block": full, "think_numbered_block": numbered,
                     "truncated": index == 9, "tokens": tokens, "forward_passes": passes}
            scores.append(score)
            blocks.append(block)
        for suffix, values in (("-rows.jsonl", scores), ("-block-rows.jsonl", blocks)):
            (path / f"{stem}{suffix}").write_text("".join(json.dumps(row) + "\n" for row in values))


def self_test():
    with tempfile.TemporaryDirectory() as directory:
        archives = Path(directory)
        write_fixture_archive(archives, PARENT_ARCHIVES[BASE_LABEL], "/tmp/exp21-qwen3-4b-mv10", 0)
        for arm, offset in zip(ARMS, (1, 2)):
            parent = f"mixed401_{arm}_step128"
            write_fixture_archive(archives, PARENT_ARCHIVES[parent],
                                  f"/tmp/exp21-selective-runs/exp21-4b-mixed401-{arm}-p128/step_models/step_128/model",
                                  offset)
        for offset, (step, arm) in enumerate(((step, arm) for step in STEPS for arm in ARMS), 3):
            write_fixture_archive(archives, archive_name(arm, step), expected_model(arm, step), offset)
        result = build_result(archives)
        require(set(result["variants"]) == {candidate_label(arm, step) for step in STEPS for arm in ARMS},
                "fixture variants missing")
        require(result["variants"][candidate_label("tagged", 8)]["metrics"]["full_numbered_block"]["count"] == 12,
                "fixture full numbered metric drift")
        require(result["tagged_vs_plain_by_step"]["step32"]["robust"]["n"] == 40,
                "fixture paired bootstrap n drift")
        score_path = archives / archive_name("tagged", 8) / "gsm8k_dev10-rows.jsonl"
        block_path = archives / archive_name("tagged", 8) / "gsm8k_dev10-block-rows.jsonl"
        scores, blocks = read_jsonl(score_path), read_jsonl(block_path)
        scores[0]["problem"] = blocks[0]["problem"] = "drifted fixture question"
        score_path.write_text("".join(json.dumps(row) + "\n" for row in scores))
        block_path.write_text("".join(json.dumps(row) + "\n" for row in blocks))
        try:
            build_result(archives)
        except SummaryError as error:
            require("question drift" in str(error), "fixture question-pair rejection drift")
        else:
            raise SummaryError("fixture accepted question drift")
        metadata_path = archives / archive_name("tagged", 8) / "gsm8k_dev10.jsonl.meta.json"
        metadata = read_json(metadata_path)
        metadata["seed"] = 7
        metadata_path.write_text(json.dumps(metadata))
        try:
            load_onpolicy_archive(archives, "tagged", 8)
        except SummaryError as error:
            require("seed" in str(error), "fixture protocol rejection drift")
        else:
            raise SummaryError("fixture accepted wrong seed")
    print("self-test passed")


def main():
    global VARIANT
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("onpolicy189", "clean46"), default="onpolicy189")
    parser.add_argument("--archives", type=Path, default=ARCHIVES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    VARIANT = args.variant
    if args.self_test:
        self_test()
        return
    result = build_result(args.archives.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({label: item["metrics"] for label, item in result["variants"].items()},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (SummaryError, FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
