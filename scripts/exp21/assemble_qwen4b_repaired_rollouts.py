#!/usr/bin/env python3
"""Assemble 189 Qwen4B rollouts, replacing only manifest-approved repair drafts.

Candidates use ``answer`` as gold; repair drafts must repeat it as ``gold``.
The output adds ``output_provenance`` so approved edits are never presented as
raw model generations.  Math correctness is intentionally out of scope here.
"""
import argparse
import json
import re
from pathlib import Path

from tokenizers import Tokenizer

from mv_format import ANY_TAG, parse


FINAL_ANSWER = re.compile(r"(?m)^Final Answer:\s*\S.*$")
PROBLEM_MARKER = "\n\nProblem: "


def fail(message):
    raise ValueError(message)


def read_jsonl(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                fail(f"blank JSONL line: {path}:{line_number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON: {path}:{line_number}") from error
            if not isinstance(row, dict):
                fail(f"JSON object required: {path}:{line_number}")
            rows.append((row, line_number))
    if not rows:
        fail(f"empty JSONL: {path}")
    return rows


def require_unique(rows, name):
    ids = [row.get("id") for row, _ in rows]
    if any(not isinstance(identifier, str) or not identifier for identifier in ids):
        fail(f"{name} has missing ID")
    if len(ids) != len(set(ids)):
        fail(f"duplicate {name} ID")


def candidate_gold(row):
    answer, gold = row.get("answer"), row.get("gold")
    if not isinstance(answer, str) or not answer:
        fail(f"candidate lacks answer: {row.get('id')}")
    if gold is not None and gold != answer:
        fail(f"candidate answer/gold differ: {row.get('id')}")
    return answer


def load_candidates(path, expected_count):
    rows = read_jsonl(path)
    require_unique(rows, "candidate")
    if len(rows) != expected_count:
        fail(f"need exactly {expected_count} candidates, got {len(rows)}")
    required = ("id", "source", "answer_type", "question")
    candidates = {}
    for row, _ in rows:
        if any(not isinstance(row.get(key), str) or not row[key] for key in required):
            fail(f"malformed candidate: {row.get('id')}")
        candidate_gold(row)
        candidates[row["id"]] = row
    return candidates


def question_from_prompt(prompt, identifier):
    if not isinstance(prompt, str) or PROBLEM_MARKER not in prompt:
        fail(f"missing Problem marker in rollout prompt: {identifier}")
    question = prompt.rsplit(PROBLEM_MARKER, 1)[1]
    for marker in ("<|im_end|>", "<|endoftext|>"):
        question = question.split(marker, 1)[0]
    if not question:
        fail(f"empty rollout prompt question: {identifier}")
    return question


def validate_response(response, identifier, tokenizer):
    if not isinstance(response, str) or not response.startswith("<think>"):
        fail(f"response must start with <think>: {identifier}")
    if response.count("<think>") != 1 or response.count("</think>") != 1:
        fail(f"response has invalid think envelope: {identifier}")
    thought, final = response.split("</think>", 1)
    structure = parse(thought)
    if not structure["valid"] or len(structure["blocks"]) != 1 or not structure["blocks"][0]["numbered"]:
        fail(f"response lacks one completed numbered Multiverse block: {identifier}")
    if ANY_TAG.search(final):
        fail(f"response has Multiverse tags outside <think>: {identifier}")
    final_lines = FINAL_ANSWER.findall(response)
    if len(final_lines) != 1 or not response.rstrip().endswith(final_lines[0]):
        fail(f"response needs one final Final Answer line: {identifier}")
    length = len(tokenizer.encode(response).ids)
    if length > 4096:
        fail(f"response exceeds 4096 tokens: {identifier} ({length})")
    return length


def load_rollouts(path, candidates, expected_count):
    rows = read_jsonl(path)
    require_unique(rows, "rollout")
    if len(rows) != expected_count:
        fail(f"need exactly {expected_count} rollouts, got {len(rows)}")
    if {row["id"] for row, _ in rows} != set(candidates):
        fail("rollout IDs differ from candidates")
    required = ("id", "source", "answer_type", "input", "output")
    for row, _ in rows:
        if any(key not in row for key in required):
            fail(f"rollout misses required field: {row.get('id')}")
        candidate = candidates[row["id"]]
        if (row["source"] != candidate["source"] or row["answer_type"] != candidate["answer_type"] or
                question_from_prompt(row["input"], row["id"]) != candidate["question"]):
            fail(f"rollout differs from candidate: {row['id']}")
    return rows


def load_drafts(paths, candidates):
    drafts = {}
    for path in paths:
        rows = read_jsonl(path)
        require_unique(rows, f"draft ({path})")
        for row, line_number in rows:
            identifier = row["id"]
            if identifier in drafts:
                fail(f"duplicate draft ID: {identifier}")
            if identifier not in candidates:
                fail(f"draft ID absent from candidates: {identifier}")
            candidate = candidates[identifier]
            required = ("id", "source", "answer_type", "question", "gold", "response")
            if any(key not in row for key in required):
                fail(f"draft misses required field: {identifier}")
            if any(row[key] != candidate[key] for key in ("id", "source", "answer_type", "question")):
                fail(f"draft metadata differs from candidate: {identifier}")
            if row["gold"] != candidate_gold(candidate):
                fail(f"draft gold differs from candidate: {identifier}")
            drafts[identifier] = {"response": row["response"], "path": path, "line": line_number}
    return drafts


def approved_ids(path, drafts):
    if not path.is_file():
        raise FileNotFoundError(path)
    manifest = json.loads(path.read_text())
    identifiers = manifest.get("approved_repair_ids")
    if not isinstance(identifiers, list) or any(not isinstance(item, str) or not item for item in identifiers):
        fail("manifest needs approved_repair_ids list")
    if len(identifiers) != len(set(identifiers)):
        fail("duplicate approved repair ID")
    missing = set(identifiers) - set(drafts)
    if missing:
        fail(f"approved IDs absent from drafts: {sorted(missing)}")
    return set(identifiers)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollouts", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--drafts", type=Path, nargs="+", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=189)
    args = parser.parse_args()
    if args.expected_count < 1:
        fail("expected count must be positive")
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")

    tokenizer = Tokenizer.from_file(str(args.tokenizer))
    candidates = load_candidates(args.candidates, args.expected_count)
    rollouts = load_rollouts(args.rollouts, candidates, args.expected_count)
    drafts = load_drafts(args.drafts, candidates)
    approved = approved_ids(args.manifest, drafts)

    assembled, repaired, maximum = [], 0, 0
    for rollout, line_number in rollouts:
        identifier = rollout["id"]
        row = dict(rollout)
        if identifier in approved:
            draft = drafts[identifier]
            row["output"] = draft["response"]
            response_tokens = validate_response(row["output"], identifier, tokenizer)
            maximum = max(maximum, response_tokens)
            row["output_provenance"] = {"kind": "approved_repair_draft", "raw_model_generation": False,
                                        "draft_file": str(draft["path"]), "draft_line": draft["line"],
                                        "approval_manifest": str(args.manifest),
                                        "raw_generation_tokens": row.get("tokens"),
                                        "raw_generation_forward_calls": row.get("forward_calls")}
            row["tokens"] = response_tokens
            repaired += 1
        else:
            row["output_provenance"] = {"kind": "raw_model_rollout", "raw_model_generation": True,
                                        "rollout_file": str(args.rollouts), "rollout_line": line_number}
        assembled.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        for row in assembled:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"rows": len(assembled), "repaired": repaired, "raw": len(assembled) - repaired,
                      "max_repaired_response_tokens": maximum}, ensure_ascii=False))


if __name__ == "__main__":
    main()
