#!/usr/bin/env python3
"""Add canonical final-answer lines to accepted native Qwen3-4B no-thinking rows.

Usage: python scripts/exp21/normalize_qwen4b_native_no_thinking.py INPUT.jsonl OUTPUT.jsonl
"""

import argparse
import json
import re
from pathlib import Path


FINAL_LINE = re.compile(r"(?m)^Final Answer:\s*\S.*$")
THINK_TAG = re.compile(r"</?think\s*>", re.I)
REQUIRED = ("id", "mode", "output", "candidate", "truncated", "clean", "correct")


def parsed_candidate(text: str) -> str:
    """Match the candidate extraction used by grade_gen.py."""
    boxed = re.findall(r"\\boxed\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", text)
    parts = re.split(r"(?i)final answer\s*:", text)
    if len(parts) > 1:
        lines = [line for line in parts[-1].splitlines() if line.strip()]
        value = lines[0] if lines else ""
    elif boxed:
        value = boxed[-1]
    else:
        return ""
    value = value.strip().strip("$").strip().rstrip(".").strip("*").strip()
    match = re.fullmatch(r"\\boxed\{(.*)\}", value)
    return match.group(1) if match else value


def fail(line_number: int, message: str) -> ValueError:
    return ValueError(f"line {line_number}: {message}")


def validate(row: object, line_number: int, seen: set[str]) -> None:
    if not isinstance(row, dict):
        raise fail(line_number, "JSON object required")
    if any(key not in row for key in REQUIRED):
        raise fail(line_number, "graded row misses required fields")
    identifier = row["id"]
    if not isinstance(identifier, str) or not identifier:
        raise fail(line_number, "malformed ID")
    if identifier in seen:
        raise fail(line_number, f"duplicate ID: {identifier}")
    seen.add(identifier)
    if row["mode"] != "no-thinking":
        raise fail(line_number, "mode must be no-thinking")
    if not isinstance(row["output"], str):
        raise fail(line_number, "output must be a string")
    if THINK_TAG.search(row["output"]):
        raise fail(line_number, "no-thinking output contains think tags")
    if any(type(row[key]) is not bool for key in ("truncated", "clean", "correct")):
        raise fail(line_number, "graded flags must be booleans")
    if "final_answer_line_added" in row and type(row["final_answer_line_added"]) is not bool:
        raise fail(line_number, "final_answer_line_added must be a boolean")


def appendable(row: dict) -> bool:
    return row["correct"] and row["clean"] and not row["truncated"] and not FINAL_LINE.search(row["output"])


def validate_candidate(row: dict, line_number: int) -> None:
    value = row["candidate"]
    if (not isinstance(value, str) or not value or value != value.strip() or "\n" in value or "\r" in value or
            "Final Answer:" in value or THINK_TAG.search(value) or value != parsed_candidate(row["output"])):
        raise fail(line_number, "malformed parsed candidate")


def normalize(rows: list[dict]) -> tuple[list[dict], int]:
    result, added = [], 0
    seen: set[str] = set()
    for line_number, row in enumerate(rows, 1):
        validate(row, line_number, seen)
        add_line = appendable(row)
        if add_line:
            validate_candidate(row, line_number)
            row = {**row, "output": row["output"] + "\n\nFinal Answer: " + row["candidate"]}
            added += 1
        row["final_answer_line_added"] = row.get("final_answer_line_added", False) or add_line
        result.append(row)
    return result, added


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise fail(line_number, "blank JSONL line")
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise fail(line_number, "invalid JSON") from error
    if not rows:
        raise ValueError(f"empty JSONL: {path}")
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must differ")
    return args


def main() -> None:
    args = parse_args()
    rows, added = normalize(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"rows": len(rows), "final_answer_line_added": added}, ensure_ascii=False))


if __name__ == "__main__":
    main()
