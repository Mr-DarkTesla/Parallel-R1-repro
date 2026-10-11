#!/usr/bin/env python3
"""Build conservative, non-training Multiverse views of screened Sol 6.1 traces.

This is a CPU-only converter. It reads the two human screens as an exact
allowlist, refuses ambiguous paragraph layouts, and never labels output as
accepted training data.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
from pathlib import Path
from typing import Any

from mv_format import TAGS, parse

try:
    from math_verify import parse as parse_answer
    from math_verify import verify as verify_answer
except ImportError:
    parse_answer = verify_answer = None


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
INPUT = DATA / "teacher_trajectory_candidates.jsonl"
SCREEN_FIRST = AUDIT / "teacher_screen_first102.jsonl"
SCREEN_LAST = AUDIT / "teacher_screen_last101.jsonl"
DEFAULT_OUT = DATA / "teacher_parallel_screened_sol61.jsonl"
DEFAULT_AUDIT = AUDIT / "teacher_parallel_screened_sol61.md"

DENY_IDS = {"math-train/92", "math-train/1553", "gsm8k-train/1358"}
STANDARD_THREE = {
    "P1: абзац 1; P2: абзац 2; merge: абзац 3",
    "P1 | P2 -> P3 (combine)",
}
THREE_PATH_FOURTH = "P1 | P2 | P3 -> P4 (combine)"
TWO_PATH_MIDDLE_PAIR = "P1: абзац 1; P2: абзацы 2-3; merge: абзац 4"
SPECIAL_2180 = "setup: остаток $1200; P1: абзац 1 после setup; P2: абзац 2; merge: абзац 3"
SPECIAL_1071 = "P1: абзац 1; P2: абзацы 2-3 до финального предложения; merge: финальное предложение абзаца 3"
SPECIAL_1655 = "setup: абзац 1; P1: абзац 2; P2: абзац 3 до последней фразы; merge: последняя фраза абзаца 3 и внешний ответ"
SPECIAL_98 = "P1 | P2 | P3 (constant term, then assemble)"


class GateError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise GateError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        fail(f"missing JSONL: {path}")
    rows: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            fail(f"invalid JSON at {path}:{lineno}: {error}")
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            fail(f"missing string ID at {path}:{lineno}")
        rows.append(row)
    if not rows or len(rows) != len({row["id"] for row in rows}):
        fail(f"empty or duplicate IDs: {path}")
    return rows


def load_screens(candidates: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    first, last = read_jsonl(SCREEN_FIRST), read_jsonl(SCREEN_LAST)
    if len(first) != 102 or len(last) != 101:
        fail(f"screen sizes must be 102 and 101, got {len(first)} and {len(last)}")
    candidate_ids = [row["id"] for row in candidates]
    if [row.get("source_index") for row in first] != list(range(1, 103)):
        fail("first screen source_index must be exactly 1..102")
    if [row["id"] for row in first] != candidate_ids[:102]:
        fail("first screen IDs do not exactly match first 102 candidates")
    if [row["id"] for row in last] != candidate_ids[102:]:
        fail("last screen IDs do not exactly match last 101 candidates")

    decisions: dict[str, dict[str, str]] = {}
    for screen, grouping_key in ((first, "proposed_paragraph_grouping"), (last, "paragraph_grouping")):
        for row in screen:
            verdict, grouping = row.get("verdict"), row.get(grouping_key)
            if verdict not in {"accept", "reject"} or not isinstance(grouping, str) or not grouping:
                fail(f"malformed screen decision for {row['id']}")
            if row["id"] in decisions:
                fail(f"duplicate screen decision: {row['id']}")
            decisions[row["id"]] = {"verdict": verdict, "grouping": grouping, "reason": str(row.get("reason", ""))}
    if set(decisions) != set(candidate_ids):
        fail("screens do not cover candidate set exactly")
    return decisions


def split_response(response: str, problem_id: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"(<think>\n)(.*)\n</think>\n(Final Answer:\s*.+)", response, re.S)
    if not match:
        fail(f"{problem_id}: expected one leading think section and external Final Answer")
    if any(tag in response for tag in TAGS):
        fail(f"{problem_id}: source already contains Multiverse tags")
    return match.group(1), match.group(2), match.group(3)


def unit_ranges(reasoning: str, problem_id: str) -> list[tuple[int, int]]:
    """Return source-preserving paragraph ranges.

    Some saved traces use one newline for a paragraph break. Accept one
    separator convention per trace; mixed or empty units are ambiguous.
    """
    separator = "\n\n" if "\n\n" in reasoning else "\n"
    parts = reasoning.split(separator)
    if not all(parts):
        fail(f"{problem_id}: empty or mixed reasoning paragraphs")
    ranges, start = [], 0
    for part in parts:
        end = start + len(part)
        ranges.append((start, end))
        start = end + len(separator)
    if start - len(separator) != len(reasoning):
        fail(f"{problem_id}: paragraph reconstruction failed")
    return ranges


def section(reasoning: str, start: int, end: int, problem_id: str) -> str:
    if not (0 <= start < end <= len(reasoning)):
        fail(f"{problem_id}: empty or invalid approved paragraph range")
    return reasoning[start:end]


def split_at(text: str, needle: str, problem_id: str) -> int:
    if text.count(needle) != 1:
        fail(f"{problem_id}: approved split marker is ambiguous or absent")
    return text.index(needle)


def layout(reasoning: str, grouping: str, problem_id: str) -> tuple[str, list[str], str]:
    """Apply only an exact screen grouping and retain every source character."""
    ranges = unit_ranges(reasoning, problem_id)
    starts = [start for start, _ in ranges]
    if grouping in STANDARD_THREE:
        if len(ranges) != 3:
            fail(f"{problem_id}: approved three-part grouping has {len(ranges)} paragraphs")
        return "", [section(reasoning, 0, starts[1], problem_id), section(reasoning, starts[1], starts[2], problem_id)], section(reasoning, starts[2], len(reasoning), problem_id)
    if grouping == TWO_PATH_MIDDLE_PAIR:
        if len(ranges) != 4:
            fail(f"{problem_id}: approved 1|2-3|4 grouping has {len(ranges)} paragraphs")
        return "", [section(reasoning, 0, starts[1], problem_id), section(reasoning, starts[1], starts[3], problem_id)], section(reasoning, starts[3], len(reasoning), problem_id)
    if grouping == THREE_PATH_FOURTH:
        if len(ranges) != 4:
            fail(f"{problem_id}: approved 1|2|3|4 grouping has {len(ranges)} paragraphs")
        return "", [section(reasoning, starts[i], starts[i + 1], problem_id) for i in range(3)], section(reasoning, starts[3], len(reasoning), problem_id)
    if grouping == SPECIAL_2180 and problem_id == "gsm8k-train/2180":
        if len(ranges) != 3:
            fail(f"{problem_id}: setup grouping has {len(ranges)} paragraphs")
        boundary = split_at(reasoning[:starts[1]], "With all six friends participating", problem_id)
        return section(reasoning, 0, boundary, problem_id), [section(reasoning, boundary, starts[1], problem_id), section(reasoning, starts[1], starts[2], problem_id)], section(reasoning, starts[2], len(reasoning), problem_id)
    if grouping == SPECIAL_1071 and problem_id == "math-train/1071":
        if len(ranges) != 3:
            fail(f"{problem_id}: partial-product grouping has {len(ranges)} paragraphs")
        boundary = starts[2] + split_at(reasoning[starts[2]:], "Adding these three partial products", problem_id)
        return "", [section(reasoning, 0, starts[1], problem_id), section(reasoning, starts[1], boundary, problem_id)], section(reasoning, boundary, len(reasoning), problem_id)
    if grouping == SPECIAL_1655 and problem_id == "math-train/1655":
        if len(ranges) != 3:
            fail(f"{problem_id}: complex-number grouping has {len(ranges)} paragraphs")
        boundary = starts[2] + split_at(reasoning[starts[2]:], "Dividing both independent components", problem_id)
        return section(reasoning, 0, starts[1], problem_id), [section(reasoning, starts[1], starts[2], problem_id), section(reasoning, starts[2], boundary, problem_id)], section(reasoning, boundary, len(reasoning), problem_id)
    if grouping == SPECIAL_98 and problem_id == "math-train/98":
        if len(ranges) != 3:
            fail(f"{problem_id}: coefficient grouping has {len(ranges)} paragraphs")
        boundary = starts[2] + split_at(reasoning[starts[2]:], "Their sum is 5, so assembling", problem_id)
        return "", [section(reasoning, starts[0], starts[1], problem_id), section(reasoning, starts[1], starts[2], problem_id), section(reasoning, starts[2], boundary, problem_id)], section(reasoning, boundary, len(reasoning), problem_id)
    fail(f"{problem_id}: screen grouping is not in exact convertible allowlist")


def external_candidate(external: str, problem_id: str) -> str:
    match = re.fullmatch(r"Final Answer:\s*(.+)", external.strip(), re.S)
    if not match:
        fail(f"{problem_id}: malformed external Final Answer")
    answer = match.group(1).strip().splitlines()[0].strip().rstrip(".")
    return answer.strip("$").strip()


def verify_final(external: str, gold: str, problem_id: str) -> tuple[str, bool | None]:
    if parse_answer is None or verify_answer is None:
        return "unverified_math_verify_unavailable", None
    candidate = external_candidate(external, problem_id)
    try:
        verified = bool(verify_answer(parse_answer(f"${gold}$"), parse_answer(f"${candidate}$")))
    except Exception as error:
        return f"unverified_math_verify_error:{type(error).__name__}", None
    return ("verified_math_verify" if verified else "failed_math_verify"), verified


def build_response(prefix: str, setup: str, paths: list[str], conclusion: str, external: str) -> str:
    outlines = "".join(f"<Outline>{index}: independent computation {index}</Outline>" for index in range(1, len(paths) + 1))
    path_text = "".join(f"<Path>{index}: {text}</Path>" for index, text in enumerate(paths, 1))
    return f"{prefix}{setup}<Parallel><Goal>{outlines}</Goal>{path_text}<Conclusion>{conclusion}</Conclusion></Parallel>\n</think>\n{external}"


def reconstruct(response: str) -> str:
    """Remove converter-only wrappers and recover original response byte-for-byte."""
    response = re.sub(r"<Goal><Outline>.*?</Outline>(?:<Outline>.*?</Outline>)*</Goal>", "", response, flags=re.S)
    response = re.sub(r"<Path>(\d+): ", "", response)
    return re.sub(r"</?(?:Parallel|Path|Conclusion)>", "", response)


def validate_response(response: str, original: str, problem_id: str) -> None:
    if reconstruct(response) != original:
        fail(f"{problem_id}: exact source reconstruction failed")
    structure = parse(response)
    if not structure["valid"] or len(structure["blocks"]) != 1:
        fail(f"{problem_id}: generated invalid Multiverse grammar")
    block = structure["blocks"][0]
    if not block["numbered"] or len(block["paths"]) != len(block["outlines"]):
        fail(f"{problem_id}: generated unnumbered or mismatched block")
    think_end = response.index("</think>")
    if not (response.index("<think>") < block["start"] < block["end"] < think_end):
        fail(f"{problem_id}: block escapes think")
    if any(tag in response[think_end:] for tag in TAGS):
        fail(f"{problem_id}: tag outside think")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.jsonl")
    try:
        temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_audit(path: Path, report: dict[str, Any]) -> None:
    reason_rows = "\n".join(f"| `{row['id']}` | {row['reason']} |" for row in report["skipped"])
    verifier = "available" if parse_answer is not None else "unavailable"
    text = f"""# Screened Sol 6.1 teacher trajectories

Статус: **screened_not_accepted**. Ноль строк объявлены принятыми в SFT.
Скрипт сохраняет только строки с `verdict=accept` в обеих точных screen
частях, с распознанной allowlist-группировкой и с подтверждённым `math_verify`
внешним ответом. Он не запускает GPU, proxy или сеть.

## Результат

- candidates: {report['input_rows']}
- first102: {report['screen_first']}; last101: {report['screen_last']}
- screen accept: {report['screen_accept']}; screen reject: {report['screen_reject']}
- explicit denylist: {report['denylist']}
- screened rows: {report['screened']}
- math_verify: {verifier}; verified rows: {report['verified']}
- output rows: {report['output_rows']}

Каждый output row имеет `status=screened_not_accepted` и
`answer_verification=verified_math_verify`. Неудачная или недоступная проверка
ответа остаётся причиной пропуска, а не основанием объявить строку принятой.

## Exact reconstruction

Для каждой output строки проверено байтовое равенство исходного `raw_response`
и результата после удаления только добавленных `Goal`/`Outline`, тегов и
обязательных `N:` в `Path`. Исходные символы, формулы, переносы и внешний
`Final Answer:` сохранены; Parallel block целиком находится в `<think>`.

## Пропуски

| ID | Причина |
| --- | --- |
{reason_rows if reason_rows else '| — | — |'}

## Reproduction

```bash
/tmp/exp21-audit-venv/bin/python -B scripts/exp21/convert_teacher_trajectories.py
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.md")
    try:
        temporary.write_text(text)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    args = parser.parse_args()

    candidates = read_jsonl(args.input)
    if len(candidates) != 203:
        fail(f"expected exactly 203 candidates, got {len(candidates)}")
    decisions = load_screens(candidates)
    output: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    counts: collections.Counter[str] = collections.Counter()

    for row in candidates:
        problem_id = row["id"]
        if row.get("status") != "candidate_not_accepted" or row.get("teacher") != "sol61":
            fail(f"{problem_id}: candidate status or teacher provenance changed")
        decision = decisions[problem_id]
        if decision["verdict"] != "accept":
            skipped.append({"id": problem_id, "reason": "screen verdict reject"})
            counts["screen_reject"] += 1
            continue
        counts["screen_accept"] += 1
        if problem_id in DENY_IDS:
            skipped.append({"id": problem_id, "reason": "explicit denylist"})
            counts["denylist"] += 1
            continue
        try:
            prefix, reasoning, external = split_response(row["raw_response"], problem_id)
            setup, paths, conclusion = layout(reasoning, decision["grouping"], problem_id)
            response = build_response(prefix, setup, paths, conclusion, external)
            validate_response(response, row["raw_response"], problem_id)
            verification, verified = verify_final(external, row["answer"], problem_id)
        except GateError as error:
            skipped.append({"id": problem_id, "reason": str(error)})
            counts["layout_or_structure"] += 1
            continue
        if verified is not True:
            skipped.append({"id": problem_id, "reason": verification})
            counts[verification] += 1
            continue
        output.append({
            "id": problem_id,
            "source": row["source"],
            "question": row["question"],
            "answer": row["answer"],
            "answer_type": row["answer_type"],
            "level": row.get("level"),
            "type": row.get("type"),
            "teacher": "sol61",
            "status": "screened_not_accepted",
            "screen_verdict": "accept",
            "screen_reason": decision["reason"],
            "paragraph_grouping": decision["grouping"],
            "answer_verification": verification,
            "source_raw_response": row["raw_response"],
            "response": response,
            "teacher_source": row["teacher_source"],
        })
        counts["verified"] += 1

    output.sort(key=lambda row: row["id"])
    skipped.sort(key=lambda row: row["id"])
    report = {
        "input_rows": len(candidates),
        "screen_first": 102,
        "screen_last": 101,
        "screen_accept": counts["screen_accept"],
        "screen_reject": counts["screen_reject"],
        "denylist": counts["denylist"],
        "screened": len(candidates) - counts["screen_reject"] - counts["denylist"],
        "verified": counts["verified"],
        "output_rows": len(output),
        "skipped": skipped,
    }
    write_jsonl(args.out, output)
    write_audit(args.audit, report)
    print(json.dumps({key: value for key, value in report.items() if key != "skipped"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"CONVERTER GATE FAILED: {error}") from error
