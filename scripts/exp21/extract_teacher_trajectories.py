#!/usr/bin/env python3
"""Extract audited, tag-free teacher trajectories as candidates for later review.

CPU-only.  The output is deliberately a *candidate* manifest, never an SFT
input: it copies raw pre-annotation reasoning and does not add Parallel tags.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
SOL = AUDIT / "think_trace_sol"

SOURCES = (
    {
        "name": "sol61_next80",
        "raw": SOL / "next80_traces_checked.jsonl",
        "final": SOL / "next80_final.jsonl",
        "precheck": SOL / "next80_trace_answer_precheck.jsonl",
        "leakcheck": SOL / "leakcheck80_next.summary.json",
        "correct_key": "strict_correct",
    },
    {
        "name": "sol61_next120",
        "raw": SOL / "next120_traces_checked.jsonl",
        "final": SOL / "next120_final.jsonl",
        "precheck": SOL / "next120_trace_answer_precheck.jsonl",
        "leakcheck": SOL / "leakcheck120_next.summary.json",
        "correct_key": "strict_correct",
    },
    {
        "name": "sol61_noninteger60",
        "raw": SOL / "noninteger60_traces_checked.jsonl",
        "final": SOL / "noninteger60_final.jsonl",
        "precheck": SOL / "noninteger60_trace_answer_precheck.jsonl",
        "leakcheck": SOL / "leakcheck_noninteger60.summary.json",
        "correct_key": "correct",
    },
)

DEFAULT_OUT = DATA / "teacher_trajectory_candidates.jsonl"
DEFAULT_AUDIT = AUDIT / "teacher_trajectory_candidates.md"
DEFAULT_POOL = DATA / "pool.jsonl"
DEFAULT_ACCEPTED = DATA / "onpolicy_agent_authored_accepted78.jsonl"
GLOBAL_LEAK = AUDIT / "leak_clean_recheck.json"


class ExtractionError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ExtractionError(message)


def jsonl(path: Path) -> list[dict[str, Any]]:
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
        row = dict(row)
        row["_line"] = lineno
        rows.append(row)
    if len(rows) != len({row["id"] for row in rows}):
        fail(f"duplicate IDs in {path}")
    return rows


def require_tag_free_thinking(response: str, problem_id: str) -> tuple[str, str]:
    if response.count("<think>") != 1 or response.count("</think>") != 1 or not response.startswith("<think>"):
        fail(f"{problem_id}: expected exactly one leading <think> section")
    think, external = response.split("</think>", 1)
    if "<Parallel>" in response or "</Parallel>" in response:
        fail(f"{problem_id}: raw trajectory already contains Parallel markup")
    if "<think>" in external or not external.strip().startswith("Final Answer:"):
        fail(f"{problem_id}: missing external Final Answer after </think>")
    reasoning = think[len("<think>"):].strip()
    if len(reasoning) < 200:
        fail(f"{problem_id}: reasoning is too short ({len(reasoning)} chars)")
    return reasoning, external.strip()


def assert_leak_provenance(path: Path) -> None:
    summary = json.loads(path.read_text())
    required_zero = ("n_leaky_vs_our_evals", "n_dup_vs_our_evals", "n_dup_or_variant_vs_our_evals")
    if any(summary.get(key) != 0 for key in required_zero):
        fail(f"source leakcheck is not clean: {path}")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.jsonl")
    try:
        temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_audit(path: Path, report: dict[str, Any]) -> None:
    source_rows = "\n".join(
        f"| `{source}` | {counts['final_ids']} | {counts['candidates']} |"
        for source, counts in report["by_source_file"].items()
    )
    answer_rows = "\n".join(
        f"| `{kind}` | {count} |" for kind, count in sorted(report["by_answer_type"].items())
    )
    text = f"""# Teacher trajectory candidates

Статус: **{report['status']}**. Это {report['rows']} кандидатов для
последующей разметки. Они не приняты в SFT, не содержат `<Parallel>` и не
должны попадать в обучение без отдельной проверки качества и разметки путей.

## Источник

Из трёх сохранённых партий Sol 6.1 взяты только raw thinking-трейсы, чьи ID
вошли в final full-review списка соответствующей партии. Для каждого ID
проверены answer-precheck, принадлежность очищенному `pool.jsonl`, один
`<think>`, внешний `Final Answer:`, отсутствие Parallel-тегов и минимум 200
символов reasoning.

| Партия | Full-review ID | Raw candidates |
| --- | ---: | ---: |
{source_rows}

Текущий `onpolicy_agent_authored_accepted78.jsonl` исключён полностью:
{report['checks']['current_accepted_overlap']} пересечений. Это защищает новую
очередь от повторного использования current accepted78.

## Leakage provenance

Все три исходные партии имеют `leakcheck.py` summary с нулём для наших eval,
точных дублей и вариантов eval. Глобальная повторная проверка очищенного pool
также сообщает 0 eval leak pairs, 0 MATH-test dup/variant и 0 exact prompt
duplicates. Final full-review списки применяют уже принятые ручные исключения
слабых MATH-test сигналов; extractor не использует более широкие raw партии.

## Состав

| Answer type | Кандидатов |
| --- | ---: |
{answer_rows}

- MATH: {report['by_dataset'].get('math', 0)}
- GSM8K: {report['by_dataset'].get('gsm8k', 0)}
- Thinking chars: min {report['reasoning_chars']['min']}, median {report['reasoning_chars']['median']}, max {report['reasoning_chars']['max']}
- Correct-answer provenance: {report['checks']['answer_precheck_true']}/{report['rows']}
- Raw tag-free thinking: {report['checks']['raw_tag_free_thinking']}/{report['rows']}

## Reproduction

```bash
python3 -B scripts/exp21/extract_teacher_trajectories.py
```

Скрипт CPU-only и не выполняет GPU, прокси, сетевые или платные вызовы.
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
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--pool", type=Path, default=DEFAULT_POOL)
    parser.add_argument("--current-accepted", type=Path, default=DEFAULT_ACCEPTED)
    args = parser.parse_args()

    pool_rows = jsonl(args.pool)
    pool = {row["id"]: row for row in pool_rows}
    current_accepted = {row["id"] for row in jsonl(args.current_accepted)}
    global_leak = json.loads(GLOBAL_LEAK.read_text())
    if any(global_leak.get(key) != 0 for key in ("eval_leak_pairs", "math_test_dup_variant", "exact_prompt_duplicates")):
        fail("global cleaned-pool leakcheck is not clean")

    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    source_counts: dict[str, dict[str, int]] = {}
    for source in SOURCES:
        assert_leak_provenance(source["leakcheck"])
        raw_rows = {row["id"]: row for row in jsonl(source["raw"])}
        final_rows = jsonl(source["final"])
        prechecks = {row["id"]: row for row in jsonl(source["precheck"])}
        final_ids = {row["id"] for row in final_rows}
        if not final_ids <= set(raw_rows) or not final_ids <= set(prechecks):
            fail(f"{source['name']}: final IDs are missing raw traces or answer prechecks")
        added = 0
        for problem_id in sorted(final_ids):
            if problem_id in current_accepted:
                continue
            if problem_id in seen:
                fail(f"duplicate candidate across teacher sources: {problem_id}")
            trace, precheck, pool_row = raw_rows[problem_id], prechecks[problem_id], pool.get(problem_id)
            if pool_row is None:
                fail(f"{problem_id}: absent from cleaned pool")
            if precheck.get(source["correct_key"]) is not True:
                fail(f"{problem_id}: source answer precheck failed")
            if precheck.get("source") != pool_row.get("source"):
                fail(f"{problem_id}: precheck/pool source mismatch")
            reasoning, external = require_tag_free_thinking(trace.get("response", ""), problem_id)
            if pool_row.get("source") not in {"math", "gsm8k"}:
                fail(f"{problem_id}: unsupported pool source {pool_row.get('source')!r}")
            candidates.append({
                "id": problem_id,
                "source": pool_row["source"],
                "question": pool_row["question"],
                "answer": pool_row["answer"],
                "answer_type": pool_row.get("answer_type"),
                "level": pool_row.get("level"),
                "type": pool_row.get("type"),
                "teacher": "sol61",
                "status": "candidate_not_accepted",
                "reasoning": reasoning,
                "external_answer": external,
                "raw_response": trace["response"],
                "teacher_source": {
                    "raw_file": str(source["raw"].relative_to(ROOT)),
                    "raw_line": trace["_line"],
                    "final_review_file": str(source["final"].relative_to(ROOT)),
                    "answer_precheck_file": str(source["precheck"].relative_to(ROOT)),
                    "leakcheck_summary": str(source["leakcheck"].relative_to(ROOT)),
                    "precheck_candidate": precheck.get("candidate"),
                    "precheck_correct_field": source["correct_key"],
                },
            })
            seen.add(problem_id)
            added += 1
        source_counts[source["name"]] = {"final_ids": len(final_ids), "candidates": added}

    if len(candidates) < 180:
        fail(f"only {len(candidates)} candidates; target is at least 180")
    candidates.sort(key=lambda row: row["id"])
    reasoning_lengths = sorted(len(row["reasoning"]) for row in candidates)
    answer_types = collections.Counter(row["answer_type"] or "unknown" for row in candidates)
    datasets = collections.Counter(row["source"] for row in candidates)
    report = {
        "status": "candidate_manifest_only",
        "rows": len(candidates),
        "by_source_file": source_counts,
        "by_dataset": dict(datasets),
        "by_answer_type": dict(answer_types),
        "reasoning_chars": {
            "min": reasoning_lengths[0],
            "median": reasoning_lengths[len(reasoning_lengths) // 2],
            "max": reasoning_lengths[-1],
        },
        "checks": {
            "answer_precheck_true": len(candidates),
            "raw_tag_free_thinking": len(candidates),
            "current_accepted_overlap": len(set(row["id"] for row in candidates) & current_accepted),
            "parallel_tags": 0,
            "global_pool_eval_leaks": 0,
        },
    }
    write_jsonl(args.out, candidates)
    write_audit(args.audit, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except ExtractionError as error:
        raise SystemExit(f"EXTRACTION GATE FAILED: {error}") from error
