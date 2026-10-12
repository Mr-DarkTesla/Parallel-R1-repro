#!/usr/bin/env python3
"""Strict paired fixed40 summary for the authored150 4B SFT pair.

This reads completed local evaluations only.  It refuses to write a partial
report until both tagged and plain full-evaluation ``DONE`` markers exist.
"""

import argparse
import json
import math
import os
import random
import tempfile
from pathlib import Path

from summarize_qwen4b_mixed401 import (
    PROTOCOL, ROOT, STEMS, SummaryError, read_json, read_jsonl, require, row_key,
)


ARMS = ("tagged", "plain")
STEPS = (8, 16, 32)
METRICS = ("strict", "robust", "full_numbered_block", "truncated", "tokens", "forward_passes")
NUMERIC_METRICS = {"tokens", "forward_passes"}
INITIAL_MODEL = "/tmp/exp21-qwen3-4b-mv10"
PARENT_MODEL = "/tmp/exp21-selective-runs/exp21-4b-clean46-tagged-p32/step_models/step_32/model"
DEFAULT_ROOTS = {
    arm: Path(f"/tmp/exp21-4b-agent-parallel150-{arm}-fixed40") for arm in ARMS
}
DEFAULT_ARCHIVES = ROOT / "eval_archives"
DEFAULT_OUTPUT = ROOT / "audit/qwen4b_agent_parallel150_auto_paired.json"


def expected_model(arm, step):
    return (f"/tmp/exp21-selective-runs/exp21-4b-agent-parallel150-{arm}-p32/"
            f"step_models/step_{step}/model")


def bool_value(row, field, context):
    value = row.get(field)
    require(type(value) is bool, f"{context}: {field} must be boolean")
    return value


def integer_value(row, field, context):
    value = row.get(field)
    require(type(value) is int, f"{context}: {field} must be integer")
    return value


def load_archive(path, label, model):
    require((path / "DONE").is_file(), f"{label}: unfinished or missing archive {path}")
    rows = {}
    for stem, source, budget in STEMS:
        metadata_path = path / f"{stem}.jsonl.meta.json"
        score_path = path / f"{stem}-rows.jsonl"
        block_path = path / f"{stem}-block-rows.jsonl"
        require(metadata_path.is_file() and score_path.is_file() and block_path.is_file(),
                f"{label}/{stem}: missing metadata, score rows, or block rows")
        metadata = read_json(metadata_path)
        require(metadata.get("model") == model, f"{label}/{stem}: wrong model {metadata.get('model')!r}")
        require(str(metadata.get("data", "")).endswith(f"/masked_pilot/{stem}.parquet"),
                f"{label}/{stem}: wrong data {metadata.get('data')!r}")
        require(metadata.get("max_tokens") == budget,
                f"{label}/{stem}: max_tokens={metadata.get('max_tokens')!r}, expected {budget}")
        for field, expected in PROTOCOL.items():
            require(metadata.get(field) == expected,
                    f"{label}/{stem}: {field}={metadata.get(field)!r}, expected {expected!r}")

        scores, block_rows = read_jsonl(score_path), read_jsonl(block_path)
        require(len(scores) == len(block_rows) == 10, f"{label}/{stem}: expected ten rows")
        blocks = {row_key(row): row for row in block_rows}
        require(len(blocks) == 10, f"{label}/{stem}: duplicate block key")
        for score in scores:
            key = row_key(score)
            require(key not in rows and key in blocks, f"{label}/{stem}: unmatched or duplicate score key {key}")
            block = blocks[key]
            context = f"{label}/{stem} {key}"
            require(score.get("source") == source, f"{context}: wrong source")
            require(score.get("problem") == block.get("problem"), f"{context}: question mismatch")
            require(score.get("input") == block.get("input"), f"{context}: prompt mismatch")
            require(block.get("decoder") == "masked", f"{context}: non-masked block row")
            for field in ("acc_robust", "truncated", "tokens", "forward_passes"):
                if field in score:
                    require(score[field] == block.get(field), f"{context}: score/block {field} mismatch")
            strict = bool_value(score, "acc", context)
            robust = bool_value(block, "acc_robust", context)
            full = bool_value(block, "think_full_block", context)
            numbered = bool_value(block, "think_numbered_block", context)
            truncated = bool_value(block, "truncated", context)
            tokens = integer_value(block, "tokens", context)
            passes = integer_value(block, "forward_passes", context)
            require(0 <= passes <= tokens <= budget, f"{context}: invalid token/forward-pass limits")
            rows[key] = {
                "question": score["problem"], "input": score["input"], "strict": strict,
                "robust": robust, "full_numbered_block": full and numbered,
                "truncated": truncated, "tokens": tokens, "forward_passes": passes,
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
    randomizer, size = random.Random(0), len(changes)
    draws = sorted(sum(changes[randomizer.randrange(size)] for _ in range(size)) / size
                   for _ in range(10_000))
    scale = 1 if metric in NUMERIC_METRICS else 100
    result = {
        "reference": round(scale * sum(float(reference[key][metric]) for key in keys) / size, 2),
        "candidate": round(scale * sum(float(candidate[key][metric]) for key in keys) / size, 2),
        "delta": round(scale * sum(changes) / size, 2),
        "ci95": [round(scale * draws[index], 2) for index in (249, 9749)],
        "unit": "ideal_forward_passes" if metric == "forward_passes"
        else "tokens" if metric == "tokens" else "percentage_points",
        "n": size,
    }
    if metric in {"strict", "robust"}:
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


def build_result(tagged_root, plain_root, initial_archive, parent_archive):
    initial = load_archive(initial_archive, "initial", INITIAL_MODEL)
    parent = load_archive(parent_archive, "clean46 tagged step32 parent", PARENT_MODEL)
    roots = {"tagged": tagged_root, "plain": plain_root}
    candidates = {(arm, step): load_archive(roots[arm] / f"step_{step}",
                                             f"agent_parallel150 {arm} step{step}",
                                             expected_model(arm, step))
                  for arm in ARMS for step in STEPS}
    same_fixed40(initial, parent, "initial vs clean46 tagged step32 parent")
    for arm, step in candidates:
        rows = candidates[arm, step]
        same_fixed40(initial, rows, f"initial vs agent_parallel150 {arm} step{step}")
        same_fixed40(parent, rows, f"parent vs agent_parallel150 {arm} step{step}")

    variants, tagged_vs_plain = {}, {}
    for step in STEPS:
        tagged, plain = candidates["tagged", step], candidates["plain", step]
        tagged_vs_plain[f"step{step}"] = compare(plain, tagged, f"tagged vs plain step{step}")
        for arm, rows in (("tagged", tagged), ("plain", plain)):
            label = f"agent_parallel150_{arm}_step{step}"
            variants[label] = {
                "archive": str(roots[arm] / f"step_{step}"),
                "model": expected_model(arm, step),
                "metrics": summarize(rows),
                "vs_initial_4b": compare(initial, rows, f"initial vs {label}"),
                "vs_clean46_tagged_step32_parent": compare(parent, rows, f"parent vs {label}"),
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
            "strict": "automatic archive acc; strict external final-answer accuracy",
            "robust": "automatic archive acc_robust",
            "full_numbered_block": "think_full_block and think_numbered_block inside <think>; structural only",
            "truncated": "archive truncation flag",
            "tokens": "mean generated tokens",
            "forward_passes": "mean ideal sequential decoding passes",
        },
        "provenance": {
            "initial_4b": {"archive": str(initial_archive), "model": INITIAL_MODEL},
            "clean46_tagged_step32_parent": {"archive": str(parent_archive), "model": PARENT_MODEL},
            "agent_parallel150_roots": {arm: str(roots[arm]) for arm in ARMS},
        },
        "initial_4b": {"metrics": summarize(initial)},
        "clean46_tagged_step32_parent": {"metrics": summarize(parent)},
        "variants": variants,
        "tagged_vs_matched_plain_by_step": tagged_vs_plain,
    }


def write_fixture_archive(path, model, offset):
    path.mkdir(parents=True)
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
            tokens, passes = 100 + index + offset, 99 + index + offset
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
        root = Path(directory)
        initial, parent = root / "initial", root / "parent"
        write_fixture_archive(initial, INITIAL_MODEL, 0)
        write_fixture_archive(parent, PARENT_MODEL, 1)
        roots = {arm: root / arm for arm in ARMS}
        for offset, (arm, step) in enumerate(((arm, step) for arm in ARMS for step in STEPS), 2):
            write_fixture_archive(roots[arm] / f"step_{step}", expected_model(arm, step), offset)
        for path in roots.values():
            (path / "DONE").write_text("fixture\n")
        result = build_result(roots["tagged"], roots["plain"], initial, parent)
        require(len(result["variants"]) == 6, "fixture variants missing")
        require(result["tagged_vs_matched_plain_by_step"]["step32"]["robust"]["n"] == 40,
                "fixture paired interval n drift")
        score_path = roots["tagged"] / "step_8/gsm8k_dev10-rows.jsonl"
        scores = read_jsonl(score_path)
        scores[0]["acc"] = 1
        score_path.write_text("".join(json.dumps(row) + "\n" for row in scores))
        try:
            load_archive(roots["tagged"] / "step_8", "fixture", expected_model("tagged", 8))
        except SummaryError as error:
            require("acc must be boolean" in str(error), "fixture strict accuracy rejection drift")
        else:
            raise SummaryError("fixture accepted non-boolean strict accuracy")
        scores[0]["acc"] = True
        score_path.write_text("".join(json.dumps(row) + "\n" for row in scores))
        metadata_path = roots["tagged"] / "step_8/gsm8k_dev10.jsonl.meta.json"
        metadata = read_json(metadata_path)
        metadata["model"] = "wrong-model"
        metadata_path.write_text(json.dumps(metadata))
        try:
            load_archive(roots["tagged"] / "step_8", "fixture", expected_model("tagged", 8))
        except SummaryError as error:
            require("wrong model" in str(error), "fixture provenance rejection drift")
        else:
            raise SummaryError("fixture accepted wrong model provenance")
    print("self-test passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tagged-root", type=Path, default=DEFAULT_ROOTS["tagged"])
    parser.add_argument("--plain-root", type=Path, default=DEFAULT_ROOTS["plain"])
    parser.add_argument("--initial-archive", type=Path, default=DEFAULT_ARCHIVES / "qwen4b_init_fixed40")
    parser.add_argument("--parent-archive", type=Path, default=DEFAULT_ARCHIVES / "qwen4b_clean46_tagged_step32")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    roots = {"tagged": args.tagged_root.resolve(), "plain": args.plain_root.resolve()}
    for arm, root in roots.items():
        require((root / "DONE").is_file(), f"{arm}: full fixed40 evaluation unfinished or missing {root / 'DONE'}")
    result = build_result(roots["tagged"], roots["plain"], args.initial_archive.resolve(),
                          args.parent_archive.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output.parent,
                                     prefix=args.output.name + ".", suffix=".tmp", delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary, args.output)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({label: item["metrics"] for label, item in result["variants"].items()}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (SummaryError, FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
