#!/usr/bin/env python3
"""Prepare, but do not mix, reviewed Qwen 4B tagged/plain SFT candidates.

The two JSONL arms contain only the 25 independently reviewed useful rows.
Plain response equals tagged response with the ten Multiverse tag types removed;
all other characters, including the external final line, are identical.
"""
from __future__ import annotations

import collections
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from build_sft import HEADER
from convert_qwen4b_teacher import TOKENIZER, checked_final
from make_mv_prompts import mv_prompt
from mv_format import ANY_TAG, TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
CONVERTED = AUDIT / "qwen4b_teacher_conversion_accepted.jsonl"
REVIEW = AUDIT / "qwen4b_teacher_conversion_independent_review.jsonl"
POOL = DATA / "qwen4b_teacher_pool320.jsonl"
POOL_ALL = DATA / "pool.jsonl"
TAGGED = DATA / "qwen4b_teacher_final_tagged.jsonl"
PLAIN = DATA / "qwen4b_teacher_final_plain.jsonl"
EXCLUDED = AUDIT / "qwen4b_teacher_final_excluded.jsonl"
REPORT = AUDIT / "qwen4b_teacher_final_report.json"
PRIOR_POSITIVES = (
    DATA / "pair_final_m1.jsonl",
    DATA / "more_m1_matched180.jsonl",
    DATA / "teacher_trajectory_candidates.jsonl",
    DATA / "onpolicy_agent_authored_accepted78.jsonl",
)
FROZEN_VAL = DATA / "sft_v4_recovery8_val.parquet"
HISTORICAL_TRAIN = (
    DATA / "sft_selective_blocks_v4_train.parquet",
    DATA / "sft_agent_authored_tagged_train.parquet",
)
FINAL_LINE = re.compile(r"(?m)^Final Answer:[^\n]*$")


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def read_jsonl(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ids = [row.get("id") for row in rows]
    require(rows and all(isinstance(key, str) for key in ids) and len(ids) == len(set(ids)),
            f"empty, invalid, or duplicate IDs: {path}")
    return rows


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def question_from_prompt(prompt: str) -> str:
    marker = "\n\nProblem: "
    require(marker in prompt, "validation prompt lacks Problem marker")
    return normalize(prompt.rsplit(marker, 1)[1])


def exact_final(response: str, row: dict) -> tuple[str, str]:
    require(response.count("<think>") == response.count("</think>") == 1,
            f"{row['id']}: malformed think wrapper")
    thought, outside = response.split("</think>", 1)
    require(thought.startswith("<think>"), f"{row['id']}: missing think opening")
    lines = list(FINAL_LINE.finditer(outside))
    require(len(lines) == 1, f"{row['id']}: need one external Final Answer line")
    final_line = lines[0].group(0)
    require(final_line.strip() == final_line and final_line != "Final Answer:",
            f"{row['id']}: malformed final line")
    checked_final(final_line, {"id": row["id"], "gold": row["answer"],
                               "answer_type": row["answer_type"]})
    return thought + "</think>\n" + final_line, final_line


def check_block(response: str, problem_id: str) -> None:
    parsed = parse(response)
    require(parsed["valid"] and len(parsed["blocks"]) == 1, f"{problem_id}: invalid Parallel grammar")
    block = parsed["blocks"][0]
    close = response.index("</think>")
    require(block["numbered"] and len(block["paths"]) == len(block["outlines"]) == 2
            and block["start"] > response.index("<think>") and block["end"] < close,
            f"{problem_id}: two numbered Paths must be inside think")
    require(all(part.strip() for part in block["paths"] + block["outlines"] + [block["conclusion"]]),
            f"{problem_id}: empty Parallel section")
    require(not ANY_TAG.search(response[close:]), f"{problem_id}: tag outside think")


def main() -> None:
    converted, review, pool = read_jsonl(CONVERTED), read_jsonl(REVIEW), read_jsonl(POOL)
    require((len(converted), len(review), len(pool)) == (36, 36, 320), "input row count changed")
    require([row["id"] for row in review] == [row["id"] for row in converted],
            "independent review order/IDs do not match conversion source")
    require(all(row.get("source_line") == index for index, row in enumerate(review, 1)),
            "review line provenance changed")
    reviewed = {row["id"]: row for row in review}
    pool_by_id = {row["id"]: row for row in pool}
    selected = [row for row in converted if reviewed[row["id"]].get("strictly_useful") is True]
    excluded = [{"id": row["id"], "review_class": reviewed[row["id"]]["review_class"],
                 "reason": reviewed[row["id"]]["reason"]} for row in converted if row not in selected]
    require(len(selected) == 25 and len(excluded) == 11, "strict review count changed")
    require(all(reviewed[row["id"]].get(key) is True
                for row in selected for key in ("external_answer_correct", "block_grammar_inside_think",
                                                  "path_1_substantive", "path_2_substantive",
                                                  "paths_independent", "conclusion_correct")),
            "strictly useful row has a negative quality flag")
    require(all(reviewed[row["id"]].get("review_class") == "useful" for row in selected),
            "strict review class mismatch")

    selected_ids = {row["id"] for row in selected}
    questions = [normalize(row["question"]) for row in selected]
    require(len(selected_ids) == len(questions) == len(set(questions)), "duplicate selected ID or question")
    require(selected_ids <= set(pool_by_id), "selected ID absent from leak-clean Qwen pool")
    for row in selected:
        source = pool_by_id[row["id"]]
        require(all(row[key] == source[key] for key in ("source", "question", "answer", "answer_type")),
                f"{row['id']}: converted metadata differs from leak-clean pool")
        require(row.get("source_id") == row["id"] and row.get("teacher") == "qwen3_4b"
                and row.get("answer_verification") == "verified_math_verify",
                f"{row['id']}: conversion provenance mismatch")

    prior = [row for path in PRIOR_POSITIVES for row in read_jsonl(path)]
    prior_ids = {row["id"] for row in prior}
    all_pool = {row["id"]: row for row in read_jsonl(POOL_ALL)}
    require(all(row.get("question") or row["id"] in all_pool for row in prior),
            "prior positive lacks a resolvable source question")
    prior_questions = {normalize(row.get("question") or all_pool[row["id"]]["question"]) for row in prior}
    require(not selected_ids & prior_ids and not set(questions) & prior_questions,
            "selected row duplicates an earlier positive by ID or question")
    frozen = pd.read_parquet(FROZEN_VAL).to_dict("records")
    val_ids = {row["id"] for row in frozen}
    val_questions = {question_from_prompt(row["extra_info"]["question"]) for row in frozen}
    require(not selected_ids & val_ids and not set(questions) & val_questions,
            "selected row leaks into frozen validation")

    # Historical replay overlap is reported for future mixture design. These
    # 25 candidates are not merged into any existing train parquet here.
    historical_overlap = {}
    for path in HISTORICAL_TRAIN:
        frame = pd.read_parquet(path)
        overlaps = frame[frame["id"].isin(selected_ids)]
        historical_overlap[path.name] = sorted({row["id"] for _, row in overlaps.iterrows()})

    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)
    tagged_rows, plain_rows = [], []
    max_lengths = {"tagged": 0, "plain": 0}
    for row in selected:
        problem_id = row["id"]
        tagged_response, final_line = exact_final(row["response"], row)
        check_block(tagged_response, problem_id)
        plain_response = ANY_TAG.sub("", tagged_response)
        require(len(TAGS) == 10 and not ANY_TAG.search(plain_response)
                and plain_response.count("<think>") == plain_response.count("</think>") == 1,
                f"{problem_id}: plain response retained markup or lost think wrapper")
        require(ANY_TAG.sub("", tagged_response) == plain_response,
                f"{problem_id}: plain arm differs beyond Multiverse tags")
        require(tagged_response.split("</think>\n", 1)[1] == final_line
                and plain_response.split("</think>\n", 1)[1] == final_line,
                f"{problem_id}: external response is not exact final line")
        prompt = mv_prompt(HEADER + row["question"])
        common = {"id": problem_id, "source": row["source"], "question": row["question"],
                  "answer": row["answer"], "answer_type": row["answer_type"],
                  "prompt": prompt, "enable_thinking": True, "teacher": "qwen3_4b",
                  "source_id": row["source_id"], "source_work_placement": row["source_work_placement"],
                  "review_reason": reviewed[problem_id]["reason"],
                  "status": "candidate_pair_not_mixed"}
        tagged_rows.append({**common, "response": tagged_response})
        plain_rows.append({**common, "response": plain_response})
        rendered = tokenizer.apply_chat_template([{"role": "user", "content": prompt}],
                                                 add_generation_prompt=True, tokenize=False,
                                                 enable_thinking=True)
        for arm, response in (("tagged", tagged_response), ("plain", plain_response)):
            length = len(tokenizer.encode(rendered + response + tokenizer.eos_token,
                                          add_special_tokens=False))
            require(length <= 4096, f"{problem_id}: {arm} length {length} exceeds 4096")
            max_lengths[arm] = max(max_lengths[arm], length)

    require(all({k: v for k, v in left.items() if k != "response"} ==
                {k: v for k, v in right.items() if k != "response"}
                for left, right in zip(tagged_rows, plain_rows)), "paired metadata differs")
    for path, rows in ((TAGGED, tagged_rows), (PLAIN, plain_rows), (EXCLUDED, excluded)):
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    report = {
        "status": "candidate_pair_not_mixed", "ready_for_sft": False,
        "reason_not_mixed": "25 strictly useful independent rows; gate requires at least 30",
        "strictly_useful": len(selected), "excluded_by_review": len(excluded),
        "selected_ids": [row["id"] for row in selected],
        "by_source": dict(collections.Counter(row["source"] for row in selected)),
        "math_by_answer_type": dict(collections.Counter(row["answer_type"] for row in selected if row["source"] == "math")),
        "checks": {"grammar_inside_think": len(selected), "external_exact_final_line": len(selected),
                   "math_verify": len(selected), "same_row_order_and_metadata": True,
                   "plain_equals_tagged_without_10_multiverse_tag_types": True,
                   "unique_ids": len(selected_ids), "unique_normalized_questions": len(set(questions)),
                   "prior_positive_id_overlap": 0, "prior_positive_question_overlap": 0,
                   "frozen_validation_id_overlap": 0, "frozen_validation_question_overlap": 0,
                   "max_total_tokens": max_lengths},
        "historical_replay_overlap": historical_overlap,
        "inputs": {"converted": str(CONVERTED.relative_to(ROOT)), "independent_review": str(REVIEW.relative_to(ROOT)),
                   "leak_clean_pool": str(POOL.relative_to(ROOT)), "full_pool_for_prior_questions": str(POOL_ALL.relative_to(ROOT)),
                   "prior_positives": [str(path.relative_to(ROOT)) for path in PRIOR_POSITIVES],
                   "frozen_validation": str(FROZEN_VAL.relative_to(ROOT)), "tokenizer": str(TOKENIZER)},
        "outputs": {"tagged": str(TAGGED.relative_to(ROOT)), "plain": str(PLAIN.relative_to(ROOT)),
                    "excluded": str(EXCLUDED.relative_to(ROOT))},
        "command": "uv run --offline --no-project --with pandas --with pyarrow --with 'transformers>=4.50,<5' --with 'math-verify>=0.8,<1' --with jinja2 python scripts/exp21/build_qwen4b_teacher_sft.py",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"tagged": len(tagged_rows), "plain": len(plain_rows),
                      "max_total_tokens": max_lengths, "ready_for_sft": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
