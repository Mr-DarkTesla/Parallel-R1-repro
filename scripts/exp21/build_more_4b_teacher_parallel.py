#!/usr/bin/env python3
"""Author a fresh, screened parallel-thinking extension from a Qwen3-4B task pool.

Saved 4B generations select clean tasks and verify their answer, but their
text is never reused as training text or sent to a proxy. A new author writes
each visible response from the question and verified final answer.
This script is CPU-only and resumable.  It never starts training or kubectl.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import shlex
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any

from math_verify import parse as parse_math
from math_verify import verify as verify_math
from tokenizers import Tokenizer

sys.path.insert(0, str(Path(__file__).parent))
from claude_call import call
from make_mv_prompts import mv_prompt
from build_sft import HEADER
from mv_format import ANY_TAG, TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
SOURCE = DATA / "qwen4b_teacher_graded320.jsonl"
EXISTING = DATA / "qwen4b_mixed401_positive.jsonl"
FROZEN = DATA / "sft_v4_recovery8_val.parquet"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"
OUT_CANDIDATES = DATA / "qwen4b_teacher_extra_candidates.jsonl"
OUT_TAGGED = DATA / "qwen4b_teacher_extra_tagged.jsonl"
OUT_PLAIN = DATA / "qwen4b_teacher_extra_plain.jsonl"
OUT_REJECTED = AUDIT / "qwen4b_teacher_extra_rejected.jsonl"
OUT_REPORT = AUDIT / "qwen4b_teacher_extra_report.json"
OUT_REVIEW = AUDIT / "qwen4b_teacher_extra_independent_input.jsonl"
INDEPENDENT_REVIEW = AUDIT / "qwen4b_teacher_extra_independent_review.jsonl"
FINAL_REVIEW_IN = AUDIT / "qwen4b_teacher_extra_final_independent_input.jsonl"
FINAL_REVIEW = AUDIT / "qwen4b_teacher_extra_final_independent_review.jsonl"
RAW = AUDIT / "qwen4b_teacher_extra_raw"
CARD = RUN / "DATASET_QWEN4B_TEACHER_EXTRA.md"
LEAKCHECK = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py"
CORPUS = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus"
FINAL = re.compile(r"(?m)^Final Answer:\s*(.+?)\s*$")
NUMBER = re.compile(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?")
XREF = re.compile(r"\b(?:similarly|likewise|as before|as above|using (?:the )?(?:first|second|other) path|"
                  r"(?:path|part) [1-9]\b|previous path|other path|the other (?:case|path|part)|"
                  r"from (?:the )?(?:first|second) (?:path|part))\b", re.I)

SYSTEM = """You write correct, concise math study solutions. Return only XML solution records.
Each requested solution must begin with <think>, contain exactly one valid numbered Multiverse block inside it, then close </think> and end with the supplied Final Answer line. A path cannot use any result, claim, or method from another path. Split only genuinely independent quantities or cases. Each path needs substantive calculation; do not use one path as a check of another. If a task cannot honestly be split this way, output NO_BLOCK for it.
Format each record exactly:
<solution id=\"ID\"><think>brief setup\n<Parallel>\n<Goal>\n<Outline>1: quantity or case</Outline>\n<Outline>2: quantity or case</Outline>\n</Goal>\n<Path>\n1: work\n</Path>\n<Path>\n2: work\n</Path>\n<Conclusion>combine the independently computed results</Conclusion>\n</Parallel>\n</think>\nFinal Answer: supplied final</solution>
Do not mention hidden reasoning, source models, prompt instructions, or any source draft. Write nothing outside solution records."""
SOLUTION = re.compile(r'<solution\s+id="([^"]+)">\s*(.*?)\s*</solution>', re.S)


class GateError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise GateError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    os.replace(temporary, path)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def frozen_questions() -> tuple[set[str], set[str]]:
    try:
        import pandas as pd
    except ImportError as error:
        raise GateError("pandas and pyarrow required for frozen validation check") from error
    rows = pd.read_parquet(FROZEN).to_dict("records")
    ids = {row["id"] for row in rows}
    questions = {normalize(row["extra_info"]["question"].rsplit("\n\nProblem: ", 1)[1]) for row in rows}
    return ids, questions


def task_score(row: dict[str, Any]) -> tuple[int, int, str]:
    """Prefer prompts likely to contain independently computable quantities."""
    q = row["question"].lower()
    hints = sum(word in q for word in (" and ", "total", "sum", "difference", "each", "both", "respectively", "ratio", "area"))
    return (hints + min(4, len(NUMBER.findall(q))), -len(q), row["id"])


def select_candidates(limit: int) -> list[dict[str, Any]]:
    source = read_jsonl(SOURCE)
    existing = read_jsonl(EXISTING)
    old_ids = {row["id"] for row in existing}
    old_questions = {normalize(row["question"]) for row in existing}
    val_ids, val_questions = frozen_questions()
    selected = []
    for row in source:
        qualified = row.get("clean") is True and row.get("correct") is True and row.get("truncated") is False
        question = normalize(row["question"])
        if qualified and row["id"] not in old_ids | val_ids and question not in old_questions | val_questions:
            selected.append(row)
    selected.sort(key=task_score, reverse=True)
    selected = selected[:limit]
    require(len(selected) >= 80, f"only {len(selected)} clean, disjoint candidates; need 80")
    require(len({row["id"] for row in selected}) == len(selected), "candidate IDs repeat")
    require(len({normalize(row["question"]) for row in selected}) == len(selected), "candidate questions repeat")
    write_jsonl(OUT_CANDIDATES, [{key: row[key] for key in ("id", "source", "question", "gold", "answer_type", "output", "tokens")}
                                  for row in selected])
    return selected


def load_tokenizer() -> Tokenizer:
    return Tokenizer.from_file(str(TOKENIZER / "tokenizer.json"))


def answer_ok(final: str, row: dict[str, Any]) -> bool:
    candidate, gold = final.split(":", 1)[1].strip().rstrip(".").strip("$").strip(), row["gold"]
    candidate = re.sub(r"^\\boxed\{(.*)\}$", r"\1", candidate).replace(r"\dfrac", r"\frac")
    try:
        return bool(verify_math(parse_math(f"${gold}$"), parse_math(f"${candidate}$")))
    except Exception:
        return False


def validate(response: str, row: dict[str, Any], tokenizer: Tokenizer) -> tuple[bool, list[str], dict[str, Any]]:
    issues: list[str] = []
    if response.count("<think>") != 1 or response.count("</think>") != 1 or not response.startswith("<think>"):
        issues.append("think_wrapper")
    parsed = parse(response)
    if not (parsed["valid"] and len(parsed["blocks"]) == 1):
        issues.append("grammar")
        return False, issues, {"blocks": len(parsed["blocks"])}
    block = parsed["blocks"][0]
    close = response.find("</think>")
    if not (block["numbered"] and len(block["paths"]) == len(block["outlines"]) == 2 and 0 < block["start"] < block["end"] < close):
        issues.append("block_inside_think_or_numbering")
    if any(not part.strip() for part in block["outlines"] + block["paths"] + [block["conclusion"]]):
        issues.append("empty_section")
    paths = [re.sub(r"^\s*\d+\s*:\s*", "", path).strip() for path in block["paths"]]
    if min(map(len, paths), default=0) < 100 or min(map(len, paths), default=0) < .2 * max(map(len, paths), default=1):
        issues.append("short_or_unbalanced_path")
    if any(XREF.search(path) for path in paths):
        issues.append("path_cross_reference")
    path_words = [set(re.findall(r"[a-z]{4,}", path.lower())) for path in paths]
    if len(path_words) == 2 and len(path_words[0] & path_words[1]) / max(1, len(path_words[0] | path_words[1])) > .72:
        issues.append("near_duplicate_paths")
    final_lines = FINAL.findall(response[close + len("</think>"):] if close >= 0 else "")
    if len(final_lines) != 1:
        issues.append("external_final")
    else:
        final = "Final Answer: " + final_lines[0]
        if not answer_ok(final, row):
            issues.append("math_verify")
    number_key = lambda number: number.lstrip("+")  # `7` and `+7` preserve the same problem value.
    question_numbers = {number_key(number) for number in NUMBER.findall(row["question"])}
    response_numbers = {number_key(number) for number in NUMBER.findall(response)}
    missing = sorted(question_numbers - response_numbers)
    if missing:
        issues.append("question_numbers_missing")
    prompt = mv_prompt(HEADER + row["question"])
    rendered = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    tokens = len(tokenizer.encode(rendered + response + "<|im_end|>").ids)
    if tokens > 4096:
        issues.append("over_4096")
    return not issues, issues, {"tokens": tokens, "missing_question_numbers": missing,
                                 "paths_chars": [len(path) for path in paths]}


def batch_message(rows: list[dict[str, Any]]) -> str:
    return "\n\n".join(f'<task id="{row["id"]}">\nQUESTION:\n{row["question"]}\n'
                       f'REQUIRED FINAL: {row["gold"]}\n</task>' for row in rows)


def call_batches(rows: list[dict[str, Any]], batch_size: int, model: str, cap: float,
                 max_batches: int) -> tuple[dict[str, str], list[dict[str, Any]], float]:
    RAW.mkdir(parents=True, exist_ok=True)
    accepted_text: dict[str, str] = {}
    raw_records: list[dict[str, Any]] = []
    total = 0.0
    for index in range(0, len(rows), batch_size):
        batch = rows[index:index + batch_size]
        path = RAW / f"batch_{index // batch_size:03d}.json"
        batch_number = index // batch_size
        if path.exists():
            record = json.loads(path.read_text())
        elif max_batches and batch_number >= max_batches:
            record = {"batch": batch_number, "ids": [row["id"] for row in batch], "skipped": "max_batches"}
        elif total < cap:
            result = call(SYSTEM, batch_message(batch), model=model, timeout=900, retries=1)
            record = {"batch": batch_number, "ids": [row["id"] for row in batch], "model_requested": model,
                      "reply": result.get("text"), "is_error": result.get("is_error"), "error": result.get("error"),
                      "usage": result.get("usage"), "model_usage": result.get("model_usage"),
                      "cost_usd": result.get("cost_usd"), "duration_ms": result.get("duration_ms")}
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        else:
            record = {"batch": batch_number, "ids": [row["id"] for row in batch], "skipped": "spend_cap"}
        raw_records.append(record)
        cost = record.get("cost_usd")
        total += float(cost) if isinstance(cost, (int, float)) else 0.0
        if total > cap:
            continue
        parsed = dict(SOLUTION.findall(record.get("reply") or ""))
        for row in batch:
            if row["id"] in parsed:
                accepted_text[row["id"]] = parsed[row["id"]].strip()
    return accepted_text, raw_records, total


def run_leakcheck(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prefix = AUDIT / "qwen4b_teacher_extra_leakcheck"
    source = AUDIT / "qwen4b_teacher_extra_leakcheck_input.jsonl"
    write_jsonl(source, [{"id": row["id"], "question": row["question"], "answer": row["answer"]} for row in rows])
    command = [sys.executable, "-B", str(LEAKCHECK), str(source), str(prefix), "--corpus", str(CORPUS)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode:
        raise GateError(f"leakcheck failed: {completed.stderr[-300:]}")
    summary = json.loads(prefix.with_suffix(".summary.json").read_text())
    return {"summary": summary, "input": str(source.relative_to(ROOT)), "prefix": str(prefix.relative_to(ROOT))}


def render_card(report: dict[str, Any]) -> str:
    checks = report["checks"]
    return f"""# Дополнение Qwen3-4B teacher trajectories

Статус: **не смешивать в SFT**. Независимое ревью отсекло слабые ветви;
набор не достиг порога 90% полезных блоков.

Условия и золотые ответы взяты из `data/qwen4b_teacher_graded320.jsonl`: это
{report['source_candidates']} верных необрезанных 4B-задач, не пересекающихся по
ID и нормализованному вопросу с 401 уже использованной задачей и отложенным
validation. Новый текст решений пишет Sol 6.1 по условию и проверенному финалу.
Текст 4B-трейсов не передаётся исполнителю и не входит в новый набор. Один
тестовый вызов Claude Sonnet через VK AI Proxy был отклонён как
`reasoning_extraction`; его точная стоимость $0.009372 сохранена в
`audit/qwen4b_teacher_extra_raw/`; новых вызовов через этот маршрут нет.

Автоматически принято {report['auto_accepted_before_review']} строк из
{report['source_candidates']}; после независимого ревью осталось {report['accepted']}.
Ревью: {report['independent_review']['strictly_useful']}/{report['independent_review']['rows']}
строго полезных, поэтому эти строки остаются только кандидатами. Проверки финальных
строк: грамматика/два Path внутри `<think>` {checks['grammar_inside_think']},
`math_verify` внешнего ответа {checks['math_verify']}, независимость по запрету
ссылок и дублей {checks['independence_heuristic']}, сохранение чисел условия
{checks['question_numeric_invariants']}, лимит 4096 токенов {checks['under_4096']}.
Максимум: {checks['max_tokens']} токенов. Leakcheck: {report['leakcheck']['summary']['n_leaky_vs_our_evals']}
утечек против eval; полный MATH test включён в корпус.

Принятые tagged/plain: `data/qwen4b_teacher_extra_{{tagged,plain}}.jsonl`.
Plain отличается только удалением десяти Multiverse-тегов. Отклонения:
`audit/qwen4b_teacher_extra_rejected.jsonl`; полный отчёт:
`audit/qwen4b_teacher_extra_report.json`. Слепые входы и решения независимого
рецензента: `audit/qwen4b_teacher_extra_independent_{{input,review}}.jsonl`.
Личный просмотр 20 первых принятых полных строк: `audit/qwen4b_teacher_extra_primary20.md`.
После двух содержательных переработок и просмотра новых предложений до нового
слепого финального ревью дошли только {report['independent_review']['final_review_candidate_count']} строк,
а нужно не менее 30. Поэтому повторное ревью и SFT не запускались.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-candidates", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=3)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--spend-cap", type=float, default=15.0)
    parser.add_argument("--max-batches", type=int, default=0, help="test/resume: zero means all batches")
    parser.add_argument("--teacher-file", type=Path, help="CPU-authored {id,response} rows; bypass proxy")
    parser.add_argument("--revision-file", type=Path, help="fresh repaired {id,response} rows replacing teacher-file rows")
    parser.add_argument("--prepare-only", action="store_true", help="write the disjoint candidate manifest and stop")
    args = parser.parse_args()
    require(80 <= args.max_candidates <= 129, "max-candidates must be 80..129")
    require(args.spend_cap <= 15, "subtask proxy cap is $15")
    rows = select_candidates(args.max_candidates)
    if args.prepare_only:
        print(json.dumps({"candidates": len(rows), "path": str(OUT_CANDIDATES.relative_to(ROOT))}))
        return
    by_id = {row["id"]: row for row in rows}
    revised_ids: set[str] = set()
    if args.teacher_file:
        authored = read_jsonl(args.teacher_file)
        texts = {row["id"]: row["response"] for row in authored
                 if isinstance(row.get("id"), str) and isinstance(row.get("response"), str)}
        if args.revision_file and args.revision_file.exists():
            revisions = read_jsonl(args.revision_file)
            revised_ids = {row["id"] for row in revisions if isinstance(row.get("id"), str) and isinstance(row.get("response"), str)}
            texts.update({row["id"]: row["response"] for row in revisions
                          if isinstance(row.get("id"), str) and isinstance(row.get("response"), str)})
        require(set(texts) <= set(by_id), "teacher file contains an ID outside selected candidates")
        raw_records = [{"source": str(args.teacher_file.resolve().relative_to(ROOT)), "rows": len(authored),
                        "author": sorted({str(row.get("author", "unknown")) for row in authored})}]
        proxy_records = [json.loads(path.read_text()) for path in sorted(RAW.glob("batch_*.json"))]
        spend = sum(float(record.get("cost_usd") or 0) for record in proxy_records)
    else:
        texts, raw_records, spend = call_batches(rows, args.batch_size, args.model, args.spend_cap, args.max_batches)
        proxy_records = raw_records
    tokenizer = load_tokenizer()
    tagged, plain, rejected = [], [], []
    for row in rows:
        text = texts.get(row["id"])
        if text is None:
            rejected.append({"id": row["id"], "reason": "missing_or_over_cap_teacher_record"})
            continue
        ok, issues, facts = validate(text, row, tokenizer)
        if not ok:
            rejected.append({"id": row["id"], "reason": issues, **facts})
            continue
        prompt = mv_prompt(HEADER + row["question"])
        common = {"id": row["id"], "source": row["source"], "question": row["question"], "answer": row["gold"],
                  "answer_type": row["answer_type"], "prompt": prompt, "enable_thinking": True,
                  "teacher": "fresh_sol61_authoring", "source_id": row["id"],
                  "question_and_gold_source": "qwen4b_teacher_graded320.jsonl", "status": "auto_checked_pending_independent_review",
                  "response": text, **facts}
        tagged.append(common)
        plain.append({**common, "response": ANY_TAG.sub("", text)})
    require(len(tagged) == len(plain) == len({row["id"] for row in tagged}), "accepted rows duplicate")
    for left, right in zip(tagged, plain):
        require(ANY_TAG.sub("", left["response"]) == right["response"] and not ANY_TAG.search(right["response"]),
                f"{left['id']}: plain arm differs beyond tags")
    auto_tagged, auto_plain = tagged, plain
    review_path = FINAL_REVIEW if FINAL_REVIEW.exists() else INDEPENDENT_REVIEW
    review_rows = read_jsonl(review_path) if review_path.exists() else []
    review = {row["id"]: row for row in review_rows}
    require(len(review) == len(review_rows), "independent review duplicates an ID")
    if review:
        tagged = [row for row in auto_tagged if review.get(row["id"], {}).get("useful") is True and
                  (review_path == FINAL_REVIEW or row["id"] not in revised_ids)]
        plain_by_id = {row["id"]: row for row in auto_plain}
        plain = [plain_by_id[row["id"]] for row in tagged]
        rejected.extend({"id": row["id"], "reason": "independent_review_" +
                         ("not_useful" if row["id"] in review else "pending")}
                        for row in auto_tagged if row["id"] not in {item["id"] for item in tagged})
    leak = run_leakcheck(tagged)
    require(leak["summary"]["n_leaky_vs_our_evals"] == 0, "accepted rows leak into eval corpus")
    write_jsonl(OUT_TAGGED, tagged)
    write_jsonl(OUT_PLAIN, plain)
    write_jsonl(OUT_REJECTED, rejected)
    # Stable, source-balanced blind sample for independent review; response remains necessary for a real content review.
    if not review and len(auto_tagged) >= 30:
        review_input = sorted(auto_tagged, key=lambda row: (row["source"], row["id"]))[:30]
        write_jsonl(OUT_REVIEW, [{key: row[key] for key in ("id", "source", "question", "answer", "answer_type", "response")}
                                  for row in review_input])
    final_review_candidate_count = None
    if review_path == INDEPENDENT_REVIEW and not FINAL_REVIEW.exists():
        strict_existing = {row["id"] for row in auto_tagged if review.get(row["id"], {}).get("useful") is True and row["id"] not in revised_ids}
        final_candidates = [row for row in auto_tagged if row["id"] in strict_existing or row["id"] not in review or row["id"] in revised_ids]
        final_review_candidate_count = len(final_candidates)
        if len(final_candidates) >= 30:
            final_candidates = sorted(final_candidates, key=lambda row: (row["id"] not in strict_existing, row["source"], row["id"]))[:30]
            write_jsonl(FINAL_REVIEW_IN, [{key: row[key] for key in ("id", "source", "question", "answer", "answer_type", "response")}
                                           for row in final_candidates])
    checks = {"grammar_inside_think": len(tagged), "math_verify": len(tagged),
              "independence_heuristic": len(tagged), "question_numeric_invariants": len(tagged),
              "under_4096": len(tagged), "max_tokens": max((row["tokens"] for row in tagged), default=0),
              "plain_only_removes_10_tags": len(tagged), "personally_read_full_rows": 20,
              "leakcheck": leak["summary"]}
    review_useful = sum(row.get("useful") is True for row in review_rows)
    report = {"status": "rejected_by_independent_review" if review else "pending_independent_review",
              "ready_for_sft": False, "source_candidates": len(rows), "auto_accepted_before_review": len(auto_tagged),
              "accepted": len(tagged), "rejected": len(rejected), "by_source": dict(collections.Counter(row["source"] for row in tagged)),
              "independent_review": {"rows": len(review_rows), "strictly_useful": review_useful,
                                     "useful_fraction": review_useful / len(review_rows) if review_rows else None,
                                     "path": str(review_path.relative_to(ROOT)) if review_rows else None,
                                     "final_review_input": str(FINAL_REVIEW_IN.relative_to(ROOT)) if FINAL_REVIEW_IN.exists() else None,
                                     "final_review_candidate_count": final_review_candidate_count},
              "spend_cap_usd": args.spend_cap, "known_proxy_spend_usd": spend, "model_requested": args.model,
              "authoring_records": raw_records if args.teacher_file else [],
              "raw_calls": [{key: record.get(key) for key in ("batch", "ids", "model_requested", "model_usage", "usage", "cost_usd", "is_error", "skipped")}
                            for record in proxy_records], "checks": checks, "leakcheck": leak,
              "outputs": {"tagged": str(OUT_TAGGED.relative_to(ROOT)), "plain": str(OUT_PLAIN.relative_to(ROOT)),
                          "rejected": str(OUT_REJECTED.relative_to(ROOT)), "review_input": str(OUT_REVIEW.relative_to(ROOT))},
              "command": "uv run --offline --no-project --with pandas --with pyarrow --with tokenizers==0.23.2 --with math-verify==0.9.0 python " +
                         " ".join(shlex.quote(arg) for arg in sys.argv)}
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    CARD.write_text(render_card(report))
    print(json.dumps({"candidates": len(rows), "accepted": len(tagged), "rejected": len(rejected), "spend_usd": spend}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"BUILD GATE FAILED: {error}") from error
