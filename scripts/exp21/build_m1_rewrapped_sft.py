#!/usr/bin/env python3
"""Build a matched M1 Multiverse-inside-``<think>`` SFT/control pair.

The 367 positives are the already vetted 187-row M1 set plus the vetted,
matched 180-row addition.  This is a CPU-only data build: it neither starts a
pod nor launches training.  The tagged response changes only where the think
wrapper is inserted.  The plain response removes only Multiverse XML tags and
keeps every other character of the reasoning and external final answer.
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from math_verify import parse as math_parse
from math_verify import verify as math_verify
from transformers import AutoTokenizer

from build_sft import HEADER
from checks import candidate
from make_mv_prompts import mv_prompt
from mv_format import ANY_TAG, TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
SOURCES = (DATA / "pair_final_m1.jsonl", DATA / "more_m1_matched180.jsonl")
TAGGED_SOURCE = DATA / "m1_rewrapped_tagged.jsonl"
PLAIN_SOURCE = DATA / "m1_rewrapped_plain.jsonl"
TAGGED_PREFIX = DATA / "sft_m1_rewrapped_tagged"
PLAIN_PREFIX = DATA / "sft_m1_rewrapped_plain"
REPORT = AUDIT / "m1_rewrapped_report.json"
BUILDER = Path(__file__).with_name("build_sft.py")
VAL_PREFIX = DATA / "sft_expanded_val_ids"
PRIOR_TAGGED_PREFIX = DATA / "sft_expanded_th_m1_tagged"
DEFAULT_TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"

PRIMARY_COPIES = 3
REPLAY_COPIES = 2
SEED = 21


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"missing input: {path}")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    require(rows and len(rows) == len({row.get("id") for row in rows}), f"duplicate or empty IDs: {path}")
    return rows


def final_offset(response: str, problem_id: str) -> int:
    require(response.count("Final Answer:") == 1, f"{problem_id}: exactly one Final Answer required")
    offset = response.index("Final Answer:")
    require(offset > 0 and response[offset:].strip() != "Final Answer:", f"{problem_id}: empty final answer")
    return offset


def wrap(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = row["response"]
    problem_id = row["id"]
    require(isinstance(raw, str) and "<think>" not in raw and "</think>" not in raw,
            f"{problem_id}: source must be no-think")
    require(all(tag in raw for tag in ("<Parallel>", "</Parallel>", "<Path>", "</Path>")),
            f"{problem_id}: missing Multiverse block")
    split = final_offset(raw, problem_id)
    reasoning, final = raw[:split], raw[split:]
    tagged_response = "<think>\n" + reasoning + "</think>\n" + final
    plain_response = ANY_TAG.sub("", tagged_response)

    parsed = parse(tagged_response)
    require(parsed["valid"] and len(parsed["blocks"]) == 1 and parsed["blocks"][0]["numbered"],
            f"{problem_id}: invalid numbered Multiverse grammar")
    block = parsed["blocks"][0]
    close = tagged_response.index("</think>")
    require(tagged_response.startswith("<think>\n") and block["start"] < block["end"] < close,
            f"{problem_id}: block outside <think>")
    require(not any(tag in tagged_response[close:] for tag in TAGS), f"{problem_id}: tag outside <think>")
    require(not ANY_TAG.search(plain_response), f"{problem_id}: plain arm retained Multiverse tag")
    require(tagged_response[len("<think>\n"):close] + final == raw,
            f"{problem_id}: raw reconstruction changed")
    require(tagged_response[close + len("</think>\n"):] == final,
            f"{problem_id}: external Final Answer changed")

    tagged, plain = dict(row), dict(row)
    tagged["response"], plain["response"] = tagged_response, plain_response
    tagged["method"] = "m1_rewrapped_tagged"
    plain["method"] = "m1_rewrapped_plain"
    return tagged, plain


def answer_is_math_verified(row: dict[str, Any]) -> bool:
    final = row["response"].split("</think>\n", 1)[1]
    proposed = candidate(final)
    require(proposed, f"{row['id']}: cannot extract external answer")
    try:
        return bool(math_verify(math_parse(f"${row['answer']}$"), math_parse(f"${proposed}$")))
    except Exception as error:
        raise ValueError(f"{row['id']}: math_verify failure: {error}") from error


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def build(prefix: Path, primary: Path) -> None:
    specs = ([f"parallel_th:{primary}"] * PRIMARY_COPIES
             + [f"replay_nt:{DATA / 'replay_nt.jsonl'}"] * REPLAY_COPIES
             + [f"replay_th:{DATA / 'replay_th.jsonl'}"] * REPLAY_COPIES)
    subprocess.run([sys.executable, str(BUILDER), str(prefix), "--rows", *specs,
                    "--val-ids-from", str(VAL_PREFIX), "--seed", str(SEED)], check=True)


def set_plain_arm_metadata(path: Path, primary_ids: set[str]) -> None:
    parts: dict[str, list[dict[str, Any]]] = {}
    for split in ("train", "val"):
        source = path.with_name(f"{path.name}_{split}.parquet")
        frame = pd.read_parquet(source)
        records = frame.to_dict("records")
        for row in records:
            if row["id"] in primary_ids and row["extra_info"]["kind"] == "parallel_th":
                row["data_source"] = "exp21_control_th"
                row["extra_info"] = dict(row["extra_info"], kind="control_th")
        pd.DataFrame(records).to_parquet(source, index=False)
        parts[split] = records
    counts = {
        split: dict(collections.Counter((row["extra_info"]["kind"], row["source"])
                                        for row in rows).most_common())
        for split, rows in parts.items()
    }
    serialized = {split: {f"{kind}/{source}": count for (kind, source), count in values.items()}
                  for split, values in counts.items()}
    serialized["rows_in"] = sum(len(rows) for rows in parts.values())
    path.with_name(f"{path.name}_rows.json").write_text(json.dumps(serialized, indent=1) + "\n")


def validate_pair(tagged: dict[str, list[dict[str, Any]]], plain: dict[str, list[dict[str, Any]]],
                  tagged_by_id: dict[str, dict[str, Any]], plain_by_id: dict[str, dict[str, Any]],
                  tokenizer: AutoTokenizer) -> dict[str, Any]:
    max_tokens = {"tagged": 0, "plain": 0}
    counts: dict[str, Any] = {}
    for split in ("train", "val"):
        left, right = tagged[split], plain[split]
        require([row["id"] for row in left] == [row["id"] for row in right], f"{split}: row order differs")
        require(len(left) == len(right), f"{split}: arm size differs")
        counts[split] = {"rows": len(left), "kinds": dict(collections.Counter(
            row["extra_info"]["kind"] for row in left))}
        for a, b in zip(left, right):
            ai, bi = a["extra_info"], b["extra_info"]
            require(ai["question"] == bi["question"] and ai["enable_thinking"] == bi["enable_thinking"],
                    f"{split}/{a['id']}: prompt or thinking mode differs")
            if ai["kind"] == "parallel_th":
                require(ai["kind"] == "parallel_th" and bi["kind"] == "control_th",
                        f"{split}/{a['id']}: primary kind differs")
                require(ai["answer"] == tagged_by_id[a["id"]]["response"], f"{a['id']}: tagged source differs")
                require(bi["answer"] == plain_by_id[b["id"]]["response"], f"{b['id']}: plain source differs")
            else:
                require(ai == bi, f"{split}/{a['id']}: replay differs between arms")
            for label, info in (("tagged", ai), ("plain", bi)):
                prompt = tokenizer.apply_chat_template(
                    [{"role": "user", "content": info["question"]}], add_generation_prompt=True,
                    tokenize=False, enable_thinking=info["enable_thinking"])
                length = len(tokenizer.encode(prompt, add_special_tokens=False))
                length += len(tokenizer.encode(info["answer"] + tokenizer.eos_token, add_special_tokens=False))
                require(length <= 4096, f"{split}/{a['id']}: {label} length {length} exceeds 4096")
                max_tokens[label] = max(max_tokens[label], length)
    train_questions = {row["extra_info"]["question"] for row in tagged["train"]}
    val_questions = {row["extra_info"]["question"] for row in tagged["val"]}
    require(not train_questions & val_questions, "train/validation prompt overlap")
    return {"splits": counts, "max_total_tokens": max_tokens}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    args = parser.parse_args()
    require(args.tokenizer.is_dir(), f"missing tokenizer: {args.tokenizer}")

    old, added = (read_jsonl(path) for path in SOURCES)
    require((len(old), len(added)) == (187, 180), "expected 187 + 180 M1 sources")
    source_rows = sorted(old + added, key=lambda row: row["id"])
    primary_ids = {row["id"] for row in source_rows}
    require(len(source_rows) == len(primary_ids) == 367, "expected 367 unique positives")
    replays = {name: read_jsonl(DATA / f"{name}.jsonl") for name in ("replay_nt", "replay_th")}
    require(all(len(rows) == 300 for rows in replays.values()), "expected two 300-row replays")
    replay_ids = {row["id"] for rows in replays.values() for row in rows}

    tagged_rows, plain_rows = zip(*(wrap(row) for row in source_rows))
    tagged_rows, plain_rows = list(tagged_rows), list(plain_rows)
    require(all(answer_is_math_verified(row) for row in tagged_rows), "math_verify rejected a final answer")
    write_jsonl(TAGGED_SOURCE, tagged_rows)
    write_jsonl(PLAIN_SOURCE, plain_rows)

    build(TAGGED_PREFIX, TAGGED_SOURCE)
    build(PLAIN_PREFIX, PLAIN_SOURCE)
    set_plain_arm_metadata(PLAIN_PREFIX, primary_ids)

    tagged = {split: pd.read_parquet(f"{TAGGED_PREFIX}_{split}.parquet").to_dict("records")
              for split in ("train", "val")}
    plain = {split: pd.read_parquet(f"{PLAIN_PREFIX}_{split}.parquet").to_dict("records")
             for split in ("train", "val")}
    val_ids = set(pd.read_parquet(f"{VAL_PREFIX}_val.parquet")["id"])
    require({row["id"] for row in tagged["val"]} == val_ids, "validation IDs differ from prior builder")
    require(not {row["id"] for row in tagged["train"]} & val_ids, "train/validation leak")
    require((len(tagged["train"]), len(tagged["val"])) == (2251, 50), "unexpected tagged split size")
    require((len(plain["train"]), len(plain["val"])) == (2251, 50), "unexpected plain split size")
    for split in ("train", "val"):
        prior = pd.read_parquet(f"{PRIOR_TAGGED_PREFIX}_{split}.parquet").to_dict("records")
        require([row["id"] for row in prior] == [row["id"] for row in tagged[split]],
                f"{split}: prior-builder row order differs")
        require(all(a["extra_info"]["question"] == b["extra_info"]["question"]
                    and a["extra_info"]["enable_thinking"] == b["extra_info"]["enable_thinking"]
                    for a, b in zip(prior, tagged[split])), f"{split}: prior-builder prompt differs")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    pair_report = validate_pair(tagged, plain, {row["id"]: row for row in tagged_rows},
                                {row["id"]: row for row in plain_rows}, tokenizer)

    review_self = read_jsonl(AUDIT / "more_m1_matched180_self20.jsonl")
    review_independent = read_jsonl(AUDIT / "more_m1_matched180_review30.jsonl")
    require(len(review_self) == 20 and len(review_independent) == 30, "20+30 review evidence missing")
    require({row["id"] for row in review_self}.isdisjoint({row["id"] for row in review_independent}),
            "20+30 review samples overlap")
    require({row["id"] for row in review_self + review_independent} <= {row["id"] for row in added},
            "review evidence IDs absent from matched180 source")

    report = {
        "status": "validated_cpu_only",
        "sources": {str(path.relative_to(RUN)): len(rows) for path, rows in zip(SOURCES, (old, added))},
        "positive_distinct": 367,
        "primary_copies": PRIMARY_COPIES,
        "replay": {name: {"distinct": len(rows), "copies": REPLAY_COPIES} for name, rows in replays.items()},
        "rows_each_arm": {"total": 2301, "train": 2251, "val": 50},
        "validation": {"reused_prefix": str(VAL_PREFIX.relative_to(RUN)), "new_primary_in_val": 0,
                       "train_val_id_overlap": 0},
        "transform": {"tagged": "<think> wraps exact raw pre-Final Answer text",
                      "plain": "removes only Multiverse XML tags; keeps think wrapper, paths, outlines, conclusion and all other text",
                      "raw_reconstruction": "367/367", "external_final_answer_byte_exact": "367/367",
                      "grammar_and_placement": "367/367 numbered one-block answers inside <think>",
                      "math_verify": "367/367"},
        "pairing": {"same_ids_order_prompts_thinking_mode": True,
                    "same_ids_order_prompts_as_prior_expanded_builder": True, "replay_identical": True,
                    "plain_primary_kind": "control_th"},
        "lengths": pair_report["max_total_tokens"],
        "split_counts": pair_report["splits"],
        "leakage_provenance": {"187_source_card": "DATASET_M1.md; cleaned pool and leak_clean_recheck.json",
                                "180_source_card": "DATASET_M1_MORE.md; more_matched180_verify.json",
                                "cross_source_id_overlap": 0,
                                "positive_replay_id_overlap": len(primary_ids & replay_ids),
                                "positive/replay_prompt_policy": "same prior builder: Multiverse and ordinary prompts may share an ID; validation holds all rows for each held-out ID"},
        "review_evidence": {"matched180_self_review": {"rows": 20,
                             "file": "audit/more_m1_matched180_self20.jsonl"},
                            "matched180_independent_review": {"rows": 30,
                             "file": "audit/more_m1_matched180_review30.jsonl"},
                            "disjoint": True},
        "training_recommendation": {"candidate_and_plain_control": "paired 16-step run",
                                    "batch_size": 32, "learning_rate": "3e-6",
                                    "save_steps": [4, 8, 12, 16], "launch_status": "not launched"},
        "commands": {"build": f"{sys.executable} {Path(__file__).relative_to(ROOT)} --tokenizer {args.tokenizer}",
                     "validate": f"{sys.executable} {Path(__file__).relative_to(ROOT)} --tokenizer {args.tokenizer}"},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
