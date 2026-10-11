#!/usr/bin/env python3
"""Build CPU-only paired JSONL for 25 strict Qwen4B rows plus reviewed rewrites.

This script only prepares an SFT candidate pair.  It never starts training,
GPU work, kubectl, or proxy calls.
"""
from __future__ import annotations

import collections
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd
from math_verify import parse as parse_math
from math_verify import verify as verify_math
from tokenizers import Tokenizer

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import ANY_TAG, TAGS, parse

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
BASE_TAGGED = DATA / "qwen4b_teacher_final_tagged.jsonl"
BASE_PLAIN = DATA / "qwen4b_teacher_final_plain.jsonl"
BASE_REVIEW = AUDIT / "qwen4b_teacher_conversion_independent_review.jsonl"
BASE_REPORT = AUDIT / "qwen4b_teacher_final_report.json"
GSM = AUDIT / "qwen4b_rewrite_gsm_proposals.jsonl"
MATH = AUDIT / "qwen4b_rewrite_math_proposals.jsonl"
PRIMARY = AUDIT / "qwen4b_rewrite_primary33.md"
INDEPENDENT = AUDIT / "qwen4b_rewrite_independent_review.jsonl"
POOL = DATA / "qwen4b_teacher_pool320.jsonl"
FROZEN_VAL = DATA / "sft_v4_recovery8_val.parquet"
CONVERTED = AUDIT / "qwen4b_teacher_conversion_accepted.jsonl"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"
OUT_TAGGED = DATA / "qwen4b_rewrite_reviewed_tagged.jsonl"
OUT_PLAIN = DATA / "qwen4b_rewrite_reviewed_plain.jsonl"
OUT_EXCLUDED = AUDIT / "qwen4b_rewrite_pair_excluded.jsonl"
OUT_REPORT = AUDIT / "qwen4b_rewrite_pair_report.json"
FINAL = re.compile(r"(?m)^Final Answer:[^\n]*$")
PRIMARY_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.M)
LEGACY_REPLAY_NT_IDS = {"math-train/1514", "math-train/424"}


class GateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"missing input: {path}")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ids = [row.get("id") for row in rows]
    require(rows and all(isinstance(item, str) for item in ids) and len(ids) == len(set(ids)),
            f"empty, invalid, or duplicate IDs: {path}")
    return rows


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def final_line(response: str, problem_id: str) -> str:
    require(response.count("<think>") == response.count("</think>") == 1 and response.startswith("<think>"),
            f"{problem_id}: malformed think wrapper")
    outside = response.split("</think>", 1)[1]
    matches = list(FINAL.finditer(outside))
    require(len(matches) == 1 and outside.strip() == matches[0].group(0),
            f"{problem_id}: need exactly one external Final Answer line")
    line = matches[0].group(0)
    require(line != "Final Answer:", f"{problem_id}: empty final answer")
    return line


def source_final_line(response: str, problem_id: str) -> str:
    require(response.count("<think>") == response.count("</think>") == 1 and response.startswith("<think>"),
            f"{problem_id}: malformed source think wrapper")
    matches = list(FINAL.finditer(response.split("</think>", 1)[1]))
    require(len(matches) == 1 and matches[0].group(0) != "Final Answer:",
            f"{problem_id}: source needs exactly one Final Answer line")
    return matches[0].group(0)


def check_block(response: str, problem_id: str) -> None:
    parsed = parse(response)
    require(parsed["valid"] and len(parsed["blocks"]) == 1, f"{problem_id}: invalid Parallel grammar")
    block = parsed["blocks"][0]
    close = response.index("</think>")
    require(block["numbered"] and len(block["paths"]) == len(block["outlines"]) == 2
            and response.index("<think>") < block["start"] < block["end"] < close,
            f"{problem_id}: block must have two numbered paths inside think")
    require(all(part.strip() for part in block["paths"] + block["outlines"] + [block["conclusion"]]),
            f"{problem_id}: empty Parallel section")
    require(not ANY_TAG.search(response[close:]), f"{problem_id}: tag outside think")


def checked_final(final: str, row: dict[str, Any]) -> None:
    observed = final.split(":", 1)[1].strip().rstrip(".").strip("$").strip()
    expected = row["answer"]
    if row["id"] == "gsm8k-train/7034":
        match = re.search(r"=\s*([-+]?\d+(?:\.\d+)?)\s+pounds$", observed)
        require(match is not None, "cannot read weight from external answer")
        observed = match.group(1)
    observed = re.sub(r"^\\boxed\\{(.*)\\}$", r"\1", observed).replace(r"\dfrac", r"\frac")
    if row["id"] in {"math-train/7138", "math-train/4465", "math-train/1514"}:
        observed_parts = [part.strip() for part in observed[1:-1].split(",")]
        expected_parts = [part.strip() for part in expected[1:-1].split(",")]
        expected_arity = 3 if row["id"] == "math-train/7138" else 2
        require(len(observed_parts) == len(expected_parts) == expected_arity,
                f"{row['id']}: coordinate answer has wrong arity")
        pairs = zip(expected_parts, observed_parts)
    else:
        pairs = [(expected, observed)]
    for gold, candidate in pairs:
        verified = bool(verify_math(parse_math(f"${gold}$"), parse_math(f"${candidate}$")))
        if not verified:
            trailing_number = re.search(r"(?:^|[\s$])([-+]?\d+(?:\.\d+)?)$", candidate)
            if trailing_number is not None:
                verified = bool(verify_math(parse_math(f"${gold}$"), parse_math(f"${trailing_number.group(1)}$")))
        require(verified, f"{row['id']}: math_verify rejected {candidate!r} vs {gold!r}")


def math_check(response: str, row: dict[str, Any]) -> None:
    line = final_line(response, row["id"])
    checked_final(line, row)


def primary_accepts(path: Path) -> tuple[set[str], dict[str, str]]:
    decisions: dict[str, str] = {}
    for problem_id, decision in PRIMARY_ROW.findall(path.read_text()):
        problem_id, decision = problem_id.strip(), decision.strip().lower()
        if problem_id in {"ID", "---"}:
            continue
        require(problem_id not in decisions, f"primary review duplicates ID: {problem_id}")
        require(decision in {"принять", "пограничный", "отклонить"},
                f"primary review has unknown decision for {problem_id}: {decision}")
        decisions[problem_id] = decision
    require(len(decisions) >= 20, f"only {len(decisions)} personally read rows; need at least 20")
    return {problem_id for problem_id, decision in decisions.items() if decision == "принять"}, decisions


def checked_rewrite_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    proposals = read_jsonl(GSM) + read_jsonl(MATH)
    require(len(proposals) == 33 and len({row["id"] for row in proposals}) == 33,
            "rewrite proposal source must contain 33 unique rows")
    primary, primary_all = primary_accepts(PRIMARY)
    review_rows = read_jsonl(INDEPENDENT)
    require(len(review_rows) == len(proposals), "independent review/proposal count differs")
    reviews = {row["id"]: row for row in review_rows}
    require(set(reviews) == {row["id"] for row in proposals}, "independent review IDs differ")
    useful = {
        problem_id for problem_id, row in reviews.items()
        if row.get("verdict") == "useful" or row.get("strictly_useful") is True
    }
    selected, excluded = [], []
    for row in proposals:
        problem_id, review = row["id"], reviews[row["id"]]
        strict_flags = (review.get("external_answer_status") == "correct",
                        review.get("block_grammar_inside_think") is True,
                        review.get("paths_independent") is True,
                        review.get("conclusion_arithmetic_correct") is True,
                        review.get("confirmed_arithmetic_error") is False)
        accepted = problem_id in primary and problem_id in useful and all(strict_flags)
        record = {"id": problem_id, "primary": primary_all[problem_id],
                  "independent_verdict": review.get("verdict"), "strict_flags": all(strict_flags),
                  "selected": accepted}
        (selected if accepted else excluded).append((row, record))
    require(len(selected) == 9, f"expected 9 doubly reviewed rewrites, got {len(selected)}")
    expected = {"gsm8k-train/4051", "gsm8k-train/5845", "gsm8k-train/144", "gsm8k-train/1093",
                "gsm8k-train/61", "gsm8k-train/1046", "math-train/2318", "math-train/684", "math-train/6693"}
    require({row["id"] for row, _ in selected} == expected, "strict intersection differs from reviewed nine IDs")
    require(all(row["id"] not in LEGACY_REPLAY_NT_IDS for row, _ in selected), "legacy replay_nt ID selected as rewrite")
    return [row for row, _ in selected], [record for _, record in excluded], {
        "personally_read_rows": len(primary_all), "primary_accepted": len(primary),
        "independent_useful": len(useful), "intersection": len(selected),
    }


def base_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tagged, plain = read_jsonl(BASE_TAGGED), read_jsonl(BASE_PLAIN)
    require(len(tagged) == len(plain) == 25 and [row["id"] for row in tagged] == [row["id"] for row in plain],
            "strict base pair changed")
    base_review = {row["id"]: row for row in read_jsonl(BASE_REVIEW)}
    strict_review = {problem_id: row for problem_id, row in base_review.items()
                     if row.get("strictly_useful") is True}
    converted = {row["id"]: row for row in read_jsonl(CONVERTED)}
    report = json.loads(BASE_REPORT.read_text())
    require(report.get("strictly_useful") == 25 and set(report.get("selected_ids", [])) == set(strict_review),
            "base strict-review provenance changed")
    for left, right in zip(tagged, plain):
        require({key: value for key, value in left.items() if key != "response"} ==
                {key: value for key, value in right.items() if key != "response"}, f"{left['id']}: base metadata differs")
        require(ANY_TAG.sub("", left["response"]) == right["response"], f"{left['id']}: base plain differs beyond tags")
        review = base_review.get(left["id"], {})
        require(review.get("strictly_useful") is True and review.get("paths_independent") is True,
                f"{left['id']}: base independent review is not strict")
        source = converted.get(left["id"])
        require(source is not None and source.get("source_raw_response"),
                f"{left['id']}: strict source trajectory is unavailable")
        require(final_line(left["response"], left["id"]) == source_final_line(source["source_raw_response"], left["id"]),
                f"{left['id']}: external Final Answer differs from source")
    return tagged, plain


def load_tokenizer() -> Tokenizer:
    config = json.loads((TOKENIZER / "tokenizer_config.json").read_text())
    template = config.get("chat_template", "")
    require(config.get("eos_token") == "<|im_end|>" and "<|im_start|>assistant\\n" in template
            and "enable_thinking is defined and enable_thinking is false" in template,
            "unexpected Qwen chat template")
    return Tokenizer.from_file(str(TOKENIZER / "tokenizer.json"))


def token_count(tokenizer: Tokenizer, prompt: str, response: str) -> int:
    rendered = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    return len(tokenizer.encode(rendered + response + "<|im_end|>").ids)


def atomic_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.jsonl")
    try:
        temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    tagged, plain = base_rows()
    rewrites, excluded, review_counts = checked_rewrite_rows()
    pool = {row["id"]: row for row in read_jsonl(POOL)}
    source_final_splices: list[str] = []
    for row in rewrites:
        problem_id = row["id"]
        source = pool.get(problem_id)
        require(source is not None and row["question"] == source["question"] and row["gold"] == source["answer"],
                f"{problem_id}: rewrite metadata differs from Qwen4B pool")
        require(row["response"].count("</think>") == 1, f"{problem_id}: malformed rewrite response")
        proposal_final = final_line(row["response"], problem_id)
        source_final = source_final_line(row["source_output"], problem_id)
        response = row["response"]
        if proposal_final != source_final:
            require(response.endswith(proposal_final), f"{problem_id}: rewrite Final Answer is not terminal")
            response = response[:-len(proposal_final)] + source_final
            source_final_splices.append(problem_id)
        require(final_line(response, problem_id) == source_final,
                f"{problem_id}: external Final Answer differs from source")
        prompt = mv_prompt(HEADER + row["question"])
        common = {"id": problem_id, "source": source["source"],
                  "question": row["question"], "answer": row["gold"], "answer_type": source["answer_type"],
                  "prompt": prompt, "enable_thinking": True, "teacher": "qwen3_4b",
                  "source_id": problem_id, "source_work_placement": "inside_think",
                  "review_reason": row["rationale"], "status": "candidate_pair_ready"}
        tagged.append({**common, "response": response, "pair_origin": "rewrite_double_review"})
        plain.append({**common, "response": ANY_TAG.sub("", response), "pair_origin": "rewrite_double_review"})
    require(len(tagged) == len(plain) == 34, "final pair must contain 25+9 rows")

    tokenizer = load_tokenizer()
    max_tokens = {"tagged": 0, "plain": 0}
    for left, right in zip(tagged, plain):
        problem_id = left["id"]
        require({key: value for key, value in left.items() if key != "response"} ==
                {key: value for key, value in right.items() if key != "response"}, f"{problem_id}: pair metadata differs")
        require(ANY_TAG.sub("", left["response"]) == right["response"], f"{problem_id}: plain removed more than ten tags")
        require(len(TAGS) == 10 and not ANY_TAG.search(right["response"]), f"{problem_id}: plain retains tag")
        check_block(left["response"], problem_id)
        math_check(left["response"], left)
        require(final_line(left["response"], problem_id) == final_line(right["response"], problem_id),
                f"{problem_id}: pair external Final Answer differs")
        for arm, row in (("tagged", left), ("plain", right)):
            length = token_count(tokenizer, row["prompt"], row["response"])
            require(length <= 4096, f"{problem_id}: {arm} length {length} exceeds 4096")
            max_tokens[arm] = max(max_tokens[arm], length)

    ids = {row["id"] for row in tagged}
    questions = {normalize(row["question"]) for row in tagged}
    require(len(ids) == len(questions) == len(tagged), "duplicate final ID or normalized question")
    frozen = pd.read_parquet(FROZEN_VAL).to_dict("records")
    val_ids = {row["id"] for row in frozen}
    val_questions = {normalize(row["extra_info"]["question"].rsplit("\n\nProblem: ", 1)[1]) for row in frozen}
    require(not ids & val_ids and not questions & val_questions, "final pair overlaps frozen validation")
    require(sum(row["pair_origin"] == "rewrite_double_review" for row in tagged[25:]) == 9,
            "rewrite provenance drifted")
    require(not any(row.get("kind") == "replay_nt" for row in tagged + plain), "legacy replay_nt was mixed")

    report = {
        "status": "ready_for_sft", "ready_for_sft": True,
        "rows_per_arm": len(tagged), "base_strict_rows": 25, "rewrite_double_review_rows": 9,
        "selected_ids": [row["id"] for row in tagged], "by_source": dict(collections.Counter(row["source"] for row in tagged)),
        "reviews": review_counts,
        "checks": {"math_verify": len(tagged), "grammar_inside_think": len(tagged),
                   "external_final_answer_verbatim_from_source": len(tagged), "same_pair_order_and_metadata": True,
                   "plain_only_removes_10_tags": True, "unique_ids_and_questions": len(tagged),
                   "frozen_validation_id_overlap": 0, "frozen_validation_question_overlap": 0,
                   "personally_read_rows_at_least_20": review_counts["personally_read_rows"],
                   "independently_reviewed_final_rows_at_least_30": len(tagged),
                   "legacy_replay_nt_ids_not_mixed": sorted(LEGACY_REPLAY_NT_IDS), "max_total_tokens": max_tokens},
        "external_final_source_splices": source_final_splices,
        "inputs": {"base_tagged": str(BASE_TAGGED.relative_to(ROOT)), "base_plain": str(BASE_PLAIN.relative_to(ROOT)),
                   "base_independent_review": str(BASE_REVIEW.relative_to(ROOT)), "rewrite_gsm": str(GSM.relative_to(ROOT)),
                   "rewrite_math": str(MATH.relative_to(ROOT)), "primary_review": str(PRIMARY.relative_to(ROOT)),
                   "independent_review": str(INDEPENDENT.relative_to(ROOT)), "pool": str(POOL.relative_to(ROOT)),
                   "frozen_validation": str(FROZEN_VAL.relative_to(ROOT))},
        "outputs": {"tagged": str(OUT_TAGGED.relative_to(ROOT)), "plain": str(OUT_PLAIN.relative_to(ROOT)),
                    "excluded": str(OUT_EXCLUDED.relative_to(ROOT))},
        "command": "uv run --offline --no-project --with pandas --with pyarrow --with 'tokenizers==0.23.2' --with 'math-verify==0.9.0' python scripts/exp21/build_qwen4b_rewrite_pair.py",
    }
    atomic_jsonl(OUT_TAGGED, tagged)
    atomic_jsonl(OUT_PLAIN, plain)
    atomic_jsonl(OUT_EXCLUDED, excluded)
    temporary = OUT_REPORT.with_suffix(".tmp.json")
    try:
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, OUT_REPORT)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"rows_per_arm": len(tagged), "ready_for_sft": True, "max_total_tokens": max_tokens}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"BUILD GATE FAILED: {error}") from error
