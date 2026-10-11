#!/usr/bin/env python3
"""Build CPU-only paired SFT data from semantically accepted 4B on-policy rollouts.

The semantic manifest is deliberately separate from the automatic structural
filter.  A row enters this pack only when it occurs in both: the filter proves
the generated final answer and grammar passed, and the manifest records manual
semantic-path review.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import tarfile
import unicodedata
from pathlib import Path

import pandas as pd
from tokenizers import Tokenizer

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import ANY_TAG, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer/tokenizer.json"
MARKER = "\n\nProblem: "
FINAL = re.compile(r"(?m)^Final Answer:\s*\S.*$")
MIN_ACCEPTED = 30


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split()).casefold()


def read_jsonl(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    result = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank JSONL line: {path}:{line_number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON: {path}:{line_number}") from error
            if not isinstance(row, dict):
                raise ValueError(f"JSON object required: {path}:{line_number}")
            result.append(row)
    if not result:
        raise ValueError(f"empty JSONL: {path}")
    return result


def unique(name, values):
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {name}")


def problem_from_prompt(prompt, origin):
    if not isinstance(prompt, str) or MARKER not in prompt:
        raise ValueError(f"missing final Problem marker: {origin}")
    problem = prompt.rsplit(MARKER, 1)[1].split("<|im_end|>", 1)[0].split("<|endoftext|>", 1)[0]
    if not problem.strip():
        raise ValueError(f"empty Problem: {origin}")
    return normalize(problem)


def candidate_rows(path):
    rows = read_jsonl(path)
    required = ("id", "source", "question", "answer", "answer_type")
    for row in rows:
        if any(not isinstance(row.get(key), str) or not row[key].strip() for key in required):
            raise ValueError("malformed on-policy candidate")
        if row["source"] not in {"math", "gsm8k"}:
            raise ValueError("on-policy source must be math or gsm8k")
    unique("candidate IDs", [row["id"] for row in rows])
    unique("candidate normalized questions", [normalize(row["question"]) for row in rows])
    if len(rows) != 189 or collections.Counter(row["source"] for row in rows) != {"math": 94, "gsm8k": 95}:
        raise ValueError("on-policy candidate pool must be exactly 94 MATH plus 95 GSM8K")
    return {row["id"]: row for row in rows}


def verify_candidate_audit(path, candidates):
    if not path.is_file():
        raise FileNotFoundError(path)
    audit = json.loads(path.read_text())
    checks, ids = audit.get("checks"), audit.get("ids", {})
    if not isinstance(checks, dict) or checks.get("selected_overlap_each_exclusion") != 0:
        raise ValueError("candidate audit lacks clean exclusion check")
    leak = checks.get("leakcheck")
    if not isinstance(leak, dict) or leak.get("blocking_hits") != 0:
        raise ValueError("candidate audit lacks passing evaluation leak check")
    selected = ids.get("selected")
    if not isinstance(selected, list) or set(selected) != set(candidates) or len(selected) != len(candidates):
        raise ValueError("candidate audit selected IDs differ from candidate pool")


def rollout_rows(path, candidates):
    rows = read_jsonl(path)
    required = ("id", "source", "answer_type", "seed", "input", "output", "tokens", "forward_calls", "truncated", "settings")
    seen, output = set(), {}
    for row in rows:
        if any(key not in row for key in required):
            raise ValueError("generated rollout misses required field")
        identifier = row["id"]
        if (not isinstance(identifier, str) or identifier not in candidates or row["seed"] != 0 or
                not isinstance(row["output"], str) or not isinstance(row["input"], str) or
                not isinstance(row["tokens"], int) or not isinstance(row["forward_calls"], int) or
                not isinstance(row["truncated"], bool) or not isinstance(row["settings"], dict)):
            raise ValueError("malformed generated rollout")
        candidate = candidates[identifier]
        if row["source"] != candidate["source"] or row["answer_type"] != candidate["answer_type"]:
            raise ValueError(f"generated rollout metadata differs: {identifier}")
        if problem_from_prompt(row["input"], identifier) != normalize(candidate["question"]):
            raise ValueError(f"generated rollout question differs: {identifier}")
        if identifier in seen:
            raise ValueError(f"duplicate generated rollout ID: {identifier}")
        seen.add(identifier)
        output[identifier] = row
    if set(output) != set(candidates):
        raise ValueError("generated rollouts must contain every selected candidate exactly once")
    return output


def accepted_ids(path, rollouts, provisional):
    if not path.is_file():
        raise FileNotFoundError(path)
    manifest = json.loads(path.read_text())
    if manifest.get("semantic_path_independence") != "reviewed":
        raise ValueError("semantic manifest is absent or not reviewed")
    identifiers = manifest.get("accepted_ids")
    if not isinstance(identifiers, list) or any(not isinstance(item, str) for item in identifiers):
        raise ValueError("semantic manifest lacks accepted_ids")
    unique("accepted semantic IDs", identifiers)
    if len(identifiers) < MIN_ACCEPTED:
        raise ValueError(f"need at least {MIN_ACCEPTED} semantically accepted rows")
    if not set(identifiers) <= set(rollouts):
        raise ValueError("semantic manifest accepts IDs absent from generated rollouts")
    provisional_by_id = {row.get("id"): row for row in read_jsonl(provisional)}
    if len(provisional_by_id) != len(read_jsonl(provisional)):
        raise ValueError("duplicate provisional filter ID")
    missing = set(identifiers) - set(provisional_by_id)
    if missing:
        raise ValueError(f"accepted IDs lack correct structural-filter evidence: {sorted(missing)[:5]}")
    for identifier in identifiers:
        evidence = provisional_by_id[identifier]
        if evidence.get("output") != rollouts[identifier]["output"] or evidence.get("rejection_reasons") != []:
            raise ValueError(f"provisional correctness evidence differs: {identifier}")
    return identifiers


def fixed40_questions(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    questions = []
    with tarfile.open(path) as archive:
        names = sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl"))
        if len(names) != 4:
            raise ValueError("fixed40 archive must have four block-row files")
        for name in names:
            handle = archive.extractfile(name)
            if handle is None:
                raise ValueError(f"cannot read fixed40 member: {name}")
            for line in handle:
                row = json.loads(line)
                questions.append(problem_from_prompt(row.get("problem"), f"{path}:{name}"))
    if len(questions) != 40:
        raise ValueError("fixed40 must have 40 questions")
    unique("fixed40 normalized questions", questions)
    return set(questions)


def paired_rows(path):
    rows = pd.read_parquet(path).to_dict("records")
    if len(rows) != 50:
        raise ValueError(f"paired validation must have 50 rows: {path}")
    return rows


def assert_pair(tagged, plain):
    if len(tagged) != len(plain):
        raise ValueError("paired arms have different row counts")
    for tagged_row, plain_row in zip(tagged, plain):
        if tagged_row["id"] != plain_row["id"]:
            raise ValueError("paired arms have different ID order")
        left, right = tagged_row["extra_info"], plain_row["extra_info"]
        if left["question"] != right["question"] or left["enable_thinking"] != right["enable_thinking"]:
            raise ValueError(f"paired prompt mismatch: {tagged_row['id']}")
        if ANY_TAG.sub("", left["answer"]) != right["answer"] or ANY_TAG.search(right["answer"]):
            raise ValueError(f"paired text differs beyond Multiverse tags: {tagged_row['id']}")


def valid_onpolicy_answer(answer, identifier):
    if not answer.startswith("<think>") or answer.count("<think>") != 1 or answer.count("</think>") != 1:
        raise ValueError(f"on-policy thinking envelope invalid: {identifier}")
    thought, final = answer.split("</think>", 1)
    parsed = parse(thought)
    if not parsed["valid"] or len(parsed["blocks"]) != 1 or not parsed["blocks"][0]["numbered"]:
        raise ValueError(f"on-policy Multiverse block invalid: {identifier}")
    if ANY_TAG.search(final) or len(FINAL.findall(final)) != 1:
        raise ValueError(f"on-policy final answer invalid: {identifier}")


def stable_rank(seed, identifier):
    return hashlib.sha256(f"{seed}\0{identifier}".encode()).hexdigest()


def replay_rows(path, kind):
    pool = read_jsonl(path)
    normalized, excluded = [], collections.Counter()
    grade_excluded, structural_excluded = 0, 0
    for row in pool:
        required = ("id", "source", "question", "answer_type")
        if any(not isinstance(row.get(key), str) or not row[key].strip() for key in required):
            raise ValueError(f"malformed {kind} replay")
        response = row.get("response", row.get("output"))
        if not isinstance(response, str) or not response.strip():
            raise ValueError(f"missing {kind} replay response: {row['id']}")
        has_grade = any(field in row for field in ("correct", "clean", "truncated"))
        if has_grade:
            if not all(isinstance(row.get(field), bool) for field in ("correct", "clean", "truncated")):
                raise ValueError(f"malformed grade fields in {kind} replay: {row['id']}")
            reasons = []
            if row["correct"] is not True:
                reasons.append("not_correct")
            if row["clean"] is not True:
                reasons.append("not_clean")
            if row["truncated"] is not False:
                reasons.append("truncated")
            if reasons:
                excluded.update(reasons)
                excluded["rows"] += 1
                grade_excluded += 1
                continue
        elif (not isinstance(row.get("prompt_tokens"), int) or not isinstance(row.get("response_tokens"), int)):
            raise ValueError(f"{kind} replay needs correctness fields or supported replay schema: {row['id']}")
        identifier = row["id"]
        structural_reason = None
        if ANY_TAG.search(response) or len(FINAL.findall(response)) != 1:
            structural_reason = "tagged_or_final_invalid"
        elif kind == "replay_th":
            if not response.startswith("<think>") or response.count("<think>") != 1 or response.count("</think>") != 1:
                structural_reason = "thinking_envelope_invalid"
        elif response.startswith("<think>") or "</think>" in response:
            structural_reason = "unexpected_thinking_envelope"
        if structural_reason:
            excluded.update((structural_reason,))
            excluded["rows"] += 1
            structural_excluded += 1
            continue
        normalized.append(dict(row, response=response, _graded=has_grade))
    unique(f"{kind} source IDs", [row["id"] for row in normalized])
    unique(f"{kind} source questions", [normalize(row["question"]) for row in normalized])
    return normalized, {"source_rows": len(pool), "usable_rows": len(normalized),
                        "excluded_rows": excluded.pop("rows", 0), "excluded_grade_rows": grade_excluded,
                        "excluded_structural_rows": structural_excluded, "excluded_reasons": dict(excluded)}


def select_replay(path, kind, count, excluded_ids, excluded_questions, seed):
    candidates = []
    rows, source_stats = replay_rows(path, kind)
    for row in rows:
        identifier, question = row["id"], normalize(row["question"])
        if identifier not in excluded_ids and question not in excluded_questions:
            candidates.append(row)
    unique(f"eligible {kind} IDs", [row["id"] for row in candidates])
    unique(f"eligible {kind} questions", [normalize(row["question"]) for row in candidates])
    chosen = sorted(candidates, key=lambda row: (stable_rank(seed, row["id"]), row["id"]))[:count]
    if len(chosen) != count:
        raise ValueError(f"need {count} non-overlapping {kind} replay rows, got {len(chosen)}")
    source_stats["excluded_overlap_rows"] = len(rows) - len(candidates)
    source_stats["selected_rows"] = len(chosen)
    return chosen, source_stats


def output_row(kind, source, response, copy_index=0):
    prompt = mv_prompt(HEADER + source["question"]) if kind in {"parallel_th", "control_th"} else HEADER + source["question"]
    return {
        "data_source": f"exp21_qwen4b_onpolicy189_{kind}",
        "id": source["id"], "source": source["source"], "copy_index": copy_index,
        "extra_info": {"question": prompt, "answer": response, "enable_thinking": kind != "replay_nt",
                       "kind": kind, "id": source["id"]},
    }


def write_parquet(path, rows):
    frame = pd.DataFrame(rows)
    frame["index"] = range(len(frame))
    temporary = path.with_suffix(path.suffix + ".tmp")
    frame.to_parquet(temporary, index=False)
    os.replace(temporary, path)


def total_tokens(tokenizer, row):
    info = row["extra_info"]
    rendered = f"<|im_start|>user\n{info['question']}<|im_end|>\n<|im_start|>assistant\n"
    return len(tokenizer.encode(rendered + info["answer"] + "<|im_end|>").ids)


def check_lengths(tokenizer_path, train, val):
    if not tokenizer_path.is_file():
        raise FileNotFoundError(tokenizer_path)
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    maxima = {}
    for arm in ("tagged", "plain"):
        maxima[arm] = {}
        for split, rows in (("train", train[arm]), ("val", val[arm])):
            sizes = [(row["id"], total_tokens(tokenizer, row)) for row in rows]
            overlong = [(identifier, size) for identifier, size in sizes if size > 4096]
            if overlong:
                raise ValueError(f"{arm} {split} row exceeds 4096 tokens: {overlong[0]}")
            maxima[arm][split] = max(size for _, size in sizes)
    return maxima


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DATA / "qwen4b_onpolicy189_candidates.jsonl")
    parser.add_argument("--candidate-audit", type=Path, default=DATA / "qwen4b_onpolicy189_candidates.audit.json")
    parser.add_argument("--rollouts", type=Path, required=True)
    parser.add_argument("--accepted-manifest", type=Path, required=True)
    parser.add_argument("--provisional", type=Path, required=True,
                        help="filter/provisional_candidates.jsonl proving generated answer correctness")
    parser.add_argument("--focus-tagged-val", type=Path, default=DATA / "qwen4b_focus34_tagged_val.parquet")
    parser.add_argument("--focus-plain-val", type=Path, default=DATA / "qwen4b_focus34_plain_val.parquet")
    parser.add_argument("--fixed40", type=Path, default=RUN / "eval_archives/qwen4b_init_fixed40.tgz")
    parser.add_argument("--replay-thinking", type=Path, required=True,
                        help="correct native thinking replay JSONL")
    parser.add_argument("--replay-no-thinking", type=Path, required=True,
                        help="correct native no-thinking replay JSONL")
    parser.add_argument("--replay-thinking-provenance", required=True,
                        help="exact model/run provenance for thinking replay")
    parser.add_argument("--replay-no-thinking-provenance", required=True,
                        help="exact model/run provenance for no-thinking replay")
    parser.add_argument("--tokenizer", type=Path, default=TOKENIZER,
                        help="tokenizer.json used for full rendered row length gating")
    parser.add_argument("--positive-copies", type=int, default=3)
    parser.add_argument("--replay-thinking-count", type=int, default=64)
    parser.add_argument("--replay-no-thinking-count", type=int, default=65)
    parser.add_argument("--seed", default="qwen4b-onpolicy189-pair-20261011")
    parser.add_argument("--out-prefix", type=Path, default=DATA / "qwen4b_onpolicy189")
    parser.add_argument("--report", type=Path,
                        help="defaults to audit/<out-prefix-name>_report.json")
    args = parser.parse_args(argv)
    if args.positive_copies < 1 or args.replay_thinking_count < 0 or args.replay_no_thinking_count < 0:
        parser.error("counts must be nonnegative; positive copies must be positive")
    return args


def main(argv=None):
    args = parse_args(argv)
    targets = [Path(f"{args.out_prefix}_{arm}_{split}.parquet")
               for arm in ("tagged", "plain") for split in ("train", "val")]
    report_path = args.report or AUDIT / f"{args.out_prefix.name}_report.json"
    if any(path.exists() for path in [*targets, report_path]):
        raise FileExistsError("refusing to overwrite paired dataset or report")

    candidates = candidate_rows(args.candidates)
    verify_candidate_audit(args.candidate_audit, candidates)
    rollouts = rollout_rows(args.rollouts, candidates)
    accepted = accepted_ids(args.accepted_manifest, rollouts, args.provisional)
    accepted_rows = [candidates[identifier] | {"output": rollouts[identifier]["output"]} for identifier in accepted]
    for row in accepted_rows:
        valid_onpolicy_answer(row["output"], row["id"])

    val = {"tagged": paired_rows(args.focus_tagged_val), "plain": paired_rows(args.focus_plain_val)}
    assert_pair(val["tagged"], val["plain"])
    val_questions = {problem_from_prompt(row["extra_info"]["question"], row["id"]) for row in val["tagged"]}
    fixed_questions = fixed40_questions(args.fixed40)
    accepted_questions = {normalize(row["question"]) for row in accepted_rows}
    if len(accepted_questions) != len(accepted_rows) or accepted_questions & (val_questions | fixed_questions):
        raise ValueError("accepted on-policy questions overlap validation or fixed40")

    excluded_ids = set(accepted) | {row["id"] for row in val["tagged"]}
    excluded_questions = accepted_questions | val_questions | fixed_questions
    replay_th, replay_th_stats = select_replay(args.replay_thinking, "replay_th", args.replay_thinking_count,
                                                excluded_ids, excluded_questions, args.seed + "-thinking")
    excluded_ids.update(row["id"] for row in replay_th)
    excluded_questions.update(normalize(row["question"]) for row in replay_th)
    replay_nt, replay_nt_stats = select_replay(args.replay_no_thinking, "replay_nt", args.replay_no_thinking_count,
                                                excluded_ids, excluded_questions, args.seed + "-no-thinking")

    train = {"tagged": [], "plain": []}
    for copy_index in range(args.positive_copies):
        for row in accepted_rows:
            train["tagged"].append(output_row("parallel_th", row, row["output"], copy_index))
            train["plain"].append(output_row("control_th", row, ANY_TAG.sub("", row["output"]), copy_index))
    for row in replay_th:
        item = output_row("replay_th", row, row["response"])
        train["tagged"].append(item)
        train["plain"].append(dict(item, extra_info=dict(item["extra_info"])))
    for row in replay_nt:
        item = output_row("replay_nt", row, row["response"])
        train["tagged"].append(item)
        train["plain"].append(dict(item, extra_info=dict(item["extra_info"])))
    assert_pair(train["tagged"], train["plain"])

    train_questions = {problem_from_prompt(row["extra_info"]["question"], row["id"]) for row in train["tagged"]}
    if train_questions & (val_questions | fixed_questions):
        raise ValueError("train question overlaps validation or fixed40")
    expected = len(accepted) * args.positive_copies + args.replay_thinking_count + args.replay_no_thinking_count
    if len(train["tagged"]) != expected:
        raise AssertionError("unexpected training row count")
    maxima = check_lengths(args.tokenizer, train, val)

    for arm in ("tagged", "plain"):
        write_parquet(Path(f"{args.out_prefix}_{arm}_train.parquet"), train[arm])
        write_parquet(Path(f"{args.out_prefix}_{arm}_val.parquet"), val[arm])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "ready_for_paired_onpolicy_sft",
        "inputs": {key: str(getattr(args, key).resolve()) for key in
                   ("candidates", "candidate_audit", "rollouts", "accepted_manifest", "provisional", "fixed40",
                    "replay_thinking", "replay_no_thinking", "tokenizer")},
        "accepted": {"count": len(accepted), "ids": accepted, "semantic_path_independence": "reviewed"},
        "rows_per_arm": {"train": expected, "val": 50},
        "train": {"positive_copies": args.positive_copies, "positive_rows": len(accepted) * args.positive_copies,
                  "replay_thinking": len(replay_th), "replay_no_thinking": len(replay_nt),
                  "replay_provenance": {
                      "thinking": {"declared": args.replay_thinking_provenance,
                                   "record_status": "correct_clean_untruncated" if all(row["_graded"] for row in replay_th)
                                   else "supported_replay_schema", "filter": replay_th_stats},
                      "no_thinking": {"declared": args.replay_no_thinking_provenance,
                                       "record_status": "correct_clean_untruncated" if all(row["_graded"] for row in replay_nt)
                                       else "supported_replay_schema", "filter": replay_nt_stats},
                  },
                  "kind_counts": dict(collections.Counter(row["extra_info"]["kind"] for row in train["tagged"]))},
        "checks": {"same_order": True, "plain_equals_tagged_after_removing_only_tags": True,
                   "accepted_structural_filter_evidence": len(accepted), "candidate_eval_leakcheck": "passed",
                   "train_validation_question_overlap": 0, "train_fixed40_question_overlap": 0,
                   "max_total_tokens": maxima},
        "seed": args.seed,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
