#!/usr/bin/env python3
"""Collect bounded, raw DeepSeek reasoning traces through VK AI Proxy.

CPU-only.  Calls are sequential.  This program never retries an API request,
never reconstructs reasoning, and stops before the $20 conservative bound can
be exceeded.  It needs ``math_verify`` through ``scripts/exp21/checks.py``.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from checks import candidate, correct


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
POOL = DATA / "pool.jsonl"
DEFAULT_PREFIX = "deepseek_traces"

ENDPOINT = "https://ai-proxy.vk.team/v1/chat/completions"
MODEL = "deepseek-v4-pro"
HARD_CAP_USD = 20.0
MAX_TASKS = 400
# Explicit ceilings, deliberately higher than an unverified price list.  They
# are used for safety accounting, not reported as an invoice amount.
INPUT_PRICE_CEILING_PER_MTOK = 10.0
OUTPUT_PRICE_CEILING_PER_MTOK = 30.0
MAX_INPUT_BYTES = 1024
MAX_OUTPUT_TOKENS = 1024
GROUPS = (("gsm8k", "integer"), ("math", "integer"),
          ("math", "fraction"), ("math", "expression"))
PROMPT_PREFIX = (
    "Solve this math problem carefully. Give a concise final answer on a line "
    "starting exactly with `Final Answer:`.\n\nProblem: "
)


class StopCollection(RuntimeError):
    pass


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().casefold()


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(value, ensure_ascii=False) + "\n")
        file.flush()
        os.fsync(file.fileno())


def output_paths(prefix: str) -> tuple[Path, Path, Path, Path]:
    if not re.fullmatch(r"[a-z0-9_]+_traces", prefix):
        raise StopCollection("output prefix must be lowercase and end in _traces")
    if prefix == DEFAULT_PREFIX:
        return DATA / f"{prefix}_raw.jsonl", AUDIT / f"{prefix}_accounting.jsonl", \
            AUDIT / f"{prefix}_state.json", RUN / "DATASET_DEEPSEEK_TRACES.md"
    return DATA / f"{prefix}_raw.jsonl", AUDIT / f"{prefix}_accounting.jsonl", \
        AUDIT / f"{prefix}_state.json", AUDIT / f"{prefix}_pilot.md"


def api_key() -> str:
    value = os.environ.get("AI_PROXY_API_KEY")
    if value:
        return value
    config = Path("/Users/v.charkin/.config/opencode/opencode.json")
    try:
        value = json.loads(config.read_text())["provider"]["llm-proxy"]["options"]["apiKey"]
    except (FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise StopCollection("AI Proxy API key unavailable; set AI_PROXY_API_KEY") from error
    if not isinstance(value, str) or not value:
        raise StopCollection("AI Proxy API key unavailable; set AI_PROXY_API_KEY")
    return value


def question_from_row(row: dict[str, Any]) -> str | None:
    for key in ("question", "problem"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value
    info = row.get("extra_info")
    if isinstance(info, dict):
        value = info.get("question")
        if isinstance(value, str) and value.strip():
            marker = "\n\nProblem: "
            return value.rsplit(marker, 1)[-1] if marker in value else value
    return None


def collect_exclusions(raw: Path, output_prefix: str) -> tuple[set[str], set[str], dict[str, int]]:
    """Read prior data, audit and eval artifacts without treating pool as used."""
    ids, questions = set(), set()
    scanned = 0
    skip_exact = {POOL.resolve(), raw.resolve()}
    for root in (DATA, AUDIT, RUN / "eval_runs", RUN / "eval_archives", RUN / "masked_pilot", RUN / "sol_compare"):
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            if path.resolve() in skip_exact or path.name.startswith(f"{output_prefix}_"):
                continue
            try:
                rows = jsonl(path)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            scanned += 1
            for row in rows:
                for key in ("id", "problem_id", "source_id"):
                    value = row.get(key)
                    if isinstance(value, str):
                        ids.add(value)
                question = question_from_row(row)
                if question:
                    questions.add(normalized(question))
    parquet_files = 0
    for path in DATA.glob("*val*.parquet"):
        try:
            rows = pd.read_parquet(path).to_dict("records")
        except Exception:
            continue
        parquet_files += 1
        for row in rows:
            value = row.get("id")
            if isinstance(value, str):
                ids.add(value)
            question = question_from_row(row)
            if question:
                questions.add(normalized(question))
    return ids, questions, {"jsonl_files": scanned, "validation_parquets": parquet_files,
                             "ids": len(ids), "normalized_questions": len(questions)}


def build_selection(limit: int, raw: Path, output_prefix: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pool = jsonl(POOL)
    by_id = {row["id"]: row for row in pool}
    if len(pool) != len(by_id):
        raise StopCollection("clean pool has duplicate IDs")
    excluded_ids, excluded_questions, scan = collect_exclusions(raw, output_prefix)
    groups: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in pool:
        key = (row.get("source"), row.get("answer_type"))
        if key not in GROUPS or row["id"] in excluded_ids or normalized(row["question"]) in excluded_questions:
            continue
        prompt = PROMPT_PREFIX + row["question"]
        if len(prompt.encode("utf-8")) > MAX_INPUT_BYTES:
            continue
        groups[key].append(row)
    quota = limit // len(GROUPS)
    if limit != MAX_TASKS or quota != 100:
        raise StopCollection(f"limit must remain {MAX_TASKS} for fixed balance")
    for key in GROUPS:
        groups[key].sort(key=lambda row: hashlib.sha256(
            ("deepseek-traces-20261011\\0" + row["id"]).encode()).hexdigest())
        if len(groups[key]) < quota:
            raise StopCollection(f"not enough clean unused {key}: {len(groups[key])} < {quota}")
    selected = {key: groups[key][:quota] for key in GROUPS}
    # Five request pilot: two GSM8K and one row from every MATH answer type.
    sequence = [selected[("gsm8k", "integer")][0], selected[("math", "integer")][0],
                selected[("math", "fraction")][0], selected[("math", "expression")][0],
                selected[("gsm8k", "integer")][1]]
    positions = {key: 0 for key in GROUPS}
    positions[("gsm8k", "integer")] = 2
    positions[("math", "integer")] = positions[("math", "fraction")] = positions[("math", "expression")] = 1
    while len(sequence) < limit:
        for key in GROUPS:
            if positions[key] < quota and len(sequence) < limit:
                sequence.append(selected[key][positions[key]])
                positions[key] += 1
    assert len(sequence) == limit == len({row["id"] for row in sequence})
    return sequence, {"pool_rows": len(pool), "excluded": scan,
                      "eligible_after_exclusions_and_input_bound": {"/".join(key): len(groups[key]) for key in GROUPS},
                      "selected": {"/".join(key): quota for key in GROUPS}}


def response_cost(usage: Any, input_price: float, output_price: float) -> tuple[float, dict[str, int], float | None]:
    if not isinstance(usage, dict):
        raise StopCollection("response usage unavailable")
    prompt, completion = usage.get("prompt_tokens"), usage.get("completion_tokens")
    if not isinstance(prompt, int) or not isinstance(completion, int) or prompt < 0 or completion < 0:
        raise StopCollection("response usage lacks nonnegative prompt_tokens and completion_tokens")
    ceiling = prompt * input_price / 1_000_000 + completion * output_price / 1_000_000
    billed = usage.get("cost_usd")
    if not isinstance(billed, (int, float)):
        billed = None
    return ceiling, {"prompt_tokens": prompt, "completion_tokens": completion,
                     "total_tokens": int(usage.get("total_tokens", prompt + completion))}, billed


def call(session: requests.Session, key: str, row: dict[str, Any], args: argparse.Namespace) -> tuple[dict[str, Any], float]:
    prompt = PROMPT_PREFIX + row["question"]
    prebound = MAX_INPUT_BYTES * args.input_price_ceiling / 1_000_000 + args.max_tokens * args.output_price_ceiling / 1_000_000
    request = {"model": args.model, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0, "max_tokens": args.max_tokens, "stream": False}
    started = time.monotonic()
    try:
        response = session.post(ENDPOINT, headers={"Authorization": f"Bearer {key}"}, json=request, timeout=args.timeout)
    except requests.RequestException as error:
        return {"status": "transport_error", "error": type(error).__name__, "request_params": request,
                "duration_ms": round((time.monotonic() - started) * 1000)}, prebound
    duration_ms = round((time.monotonic() - started) * 1000)
    if response.status_code >= 400:
        return {"status": "http_error", "http_status": response.status_code,
                "error": "HTTP response body omitted", "request_params": request, "duration_ms": duration_ms}, prebound
    try:
        payload = response.json()
        choice = payload["choices"][0]
        message = choice["message"]
    except (ValueError, KeyError, IndexError, TypeError) as error:
        return {"status": "invalid_response", "error": type(error).__name__, "request_params": request,
                "duration_ms": duration_ms}, prebound
    content = message.get("content")
    reasoning = message.get("reasoning_content")
    return {"status": "received", "request_params": request, "duration_ms": duration_ms,
            "response_id": payload.get("id"), "response_model": payload.get("model"),
            "finish_reason": choice.get("finish_reason"), "raw_content": content,
            "raw_reasoning_content": reasoning, "usage": payload.get("usage")}, prebound


def write_card(state: dict[str, Any], card: Path) -> None:
    stats = state["stats"]
    prefix = state["config"].get("output_prefix", DEFAULT_PREFIX)
    title = "DeepSeek reasoning traces" if prefix == DEFAULT_PREFIX else "Qwen3-32B reasoning trace pilot"
    last = state["records"][-1] if state["records"] else {}
    pilot_detail = ""
    if prefix != DEFAULT_PREFIX and last:
        pilot_detail = (f"\n## Pilot request\n\nHTTP status: `{last.get('http_status', 'not returned')}`. "
                        f"Usage present: `{isinstance(last.get('usage'), dict)}`. "
                        f"Content present: `{last.get('content_present', False)}`. "
                        f"reasoning_content present: `{last.get('reasoning_content_present', False)}`.\n")
    text = f"""# {title}

Статус: **{state['status']}**. Сборщик запросил {stats['requests']} из 400 задач;
{stats['received']} ответов содержат `reasoning_content`, {stats['correct_nontruncated']} имеют
верный неусечённый final-ответ. Цель: минимум 200 таких сырых трейсов.

## Ограничения

- Модель: `{state['config']['model']}`. Запросы последовательные, без повторов.
- Сохраняются исходные `content` и `reasoning_content`. Текст рассуждений не создаётся и не исправляется локально.
- Только GSM8K integer и MATH integer/fraction/expression. Выбор равный: 100 задач каждого типа.
- До выбора исключаются все найденные ранее positive, replay, validation и eval ID, а также нормализованные тексты вопросов. Источник `data/pool.jsonl` ранее прошёл leakcheck.
- Любой пустой/отсутствующий `reasoning_content`, ответ без безопасного `usage` или транспортная ошибка останавливает сбор.

## Расходы

В API не обнаружен текущий тариф или invoice-поле. Поэтому это не заявленная фактическая стоимость: перед каждым запросом применяется явный верхний тариф `{state['config']['input_price_ceiling']}` USD/M input и `{state['config']['output_price_ceiling']}` USD/M output, максимум `{state['config']['input_bytes_ceiling']}` input bytes и `{state['config']['max_tokens']}` output tokens. Верхняя граница на 400 запросов: `{state['config']['max_program_cost_usd']:.6f}` USD, меньше жёстких $20. Накопленная граница по фактическому `usage`: `{stats['usage_cost_ceiling_usd']:.6f}` USD. Proxy invoice: `{stats['proxy_billed_cost_usd'] if stats['proxy_billed_cost_usd'] is not None else 'unavailable'}`.

## Артефакты

- `data/{prefix}_raw.jsonl`: исходные задача, ответ, reasoning, модель, параметры, usage и проверка final-ответа.
- `audit/{prefix}_accounting.jsonl`: один accounting record на запрос.
- `audit/{prefix}_state.json`: прогресс, stop reason и cumulative counts.

    Запуск: `/tmp/exp21-audit-venv/bin/python -B scripts/exp21/collect_deepseek_traces.py --output-prefix {prefix}`.
    {pilot_detail}"""
    card.write_text(text)


def empty_state(args: argparse.Namespace, selection: list[dict[str, Any]], selection_info: dict[str, Any]) -> dict[str, Any]:
    per_call = MAX_INPUT_BYTES * args.input_price_ceiling / 1_000_000 + args.max_tokens * args.output_price_ceiling / 1_000_000
    return {"status": "running", "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "config": {"model": args.model, "endpoint": ENDPOINT, "max_tokens": args.max_tokens,
                       "input_bytes_ceiling": MAX_INPUT_BYTES, "input_price_ceiling": args.input_price_ceiling,
                       "output_price_ceiling": args.output_price_ceiling, "hard_cap_usd": HARD_CAP_USD,
                       "per_call_cost_ceiling_usd": per_call, "max_program_cost_usd": per_call * len(selection)},
            "selection_ids": [row["id"] for row in selection], "selection_info": selection_info,
            "records": [], "stats": {"requests": 0, "received": 0, "correct_nontruncated": 0,
                                          "usage_cost_ceiling_usd": 0.0, "proxy_billed_cost_usd": 0.0}}


def update_stats(state: dict[str, Any]) -> None:
    records = state["records"]
    received = [record for record in records if record["status"] == "received"]
    billed = [record.get("proxy_billed_cost_usd") for record in received]
    state["stats"] = {"requests": len(records), "received": len(received),
                      "correct_nontruncated": sum(record.get("correct_nontruncated") is True for record in received),
                      "usage_cost_ceiling_usd": sum(record.get("usage_cost_ceiling_usd", 0.0) for record in received),
                      "proxy_billed_cost_usd": sum(billed) if billed and all(value is not None for value in billed) else None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--max-tokens", type=int, default=MAX_OUTPUT_TOKENS)
    parser.add_argument("--input-price-ceiling", type=float, default=INPUT_PRICE_CEILING_PER_MTOK)
    parser.add_argument("--output-price-ceiling", type=float, default=OUTPUT_PRICE_CEILING_PER_MTOK)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output-prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--pilot-only", action="store_true",
                        help="make at most one isolated sequential request")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.max_tokens != MAX_OUTPUT_TOKENS or args.input_price_ceiling < INPUT_PRICE_CEILING_PER_MTOK or args.output_price_ceiling < OUTPUT_PRICE_CEILING_PER_MTOK:
        raise StopCollection("fixed conservative token and price ceilings may not be lowered")
    raw, accounting, state_path, card = output_paths(args.output_prefix)
    if state_path.exists():
        state = json.loads(state_path.read_text())
        pool_by_id = {row["id"]: row for row in jsonl(POOL)}
        if len(state.get("selection_ids", [])) != MAX_TASKS or len(set(state["selection_ids"])) != MAX_TASKS or \
                not set(state["selection_ids"]) <= set(pool_by_id):
            raise StopCollection("saved selection is invalid")
        selection = [pool_by_id[problem_id] for problem_id in state["selection_ids"]]
        selection_info = state["selection_info"]
    else:
        selection, selection_info = build_selection(MAX_TASKS, raw, args.output_prefix)
        state = empty_state(args, selection, selection_info)
    state["config"]["output_prefix"] = args.output_prefix
    done = {record["id"] for record in state["records"]}
    if args.dry_run:
        state["status"] = "dry_run_ready"
        update_stats(state)
        atomic_json(state_path, state)
        write_card(state, card)
        print(json.dumps({"status": state["status"], "planned": len(selection), "selection_info": selection_info}, ensure_ascii=False))
        return
    if state["status"].startswith("stopped_") or state["status"] in {"complete", "pilot_complete"}:
        write_card(state, card)
        print(json.dumps({"status": state["status"], "stats": state["stats"]}, ensure_ascii=False))
        return
    key = api_key()
    session = requests.Session()
    for index, row in enumerate(selection):
        if row["id"] in done:
            continue
        prebound = state["config"]["per_call_cost_ceiling_usd"]
        if state["stats"]["usage_cost_ceiling_usd"] + prebound > HARD_CAP_USD:
            state["status"] = "stopped_pre_call_cost_cap"
            state["stop_reason"] = "next worst-case call could exceed $20"
            break
        result, prebound = call(session, key, row, args)
        record: dict[str, Any] = {"sequence": index + 1, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                                  "id": row["id"], "source": row["source"], "answer_type": row["answer_type"],
                                  "question": row["question"], "gold": row["answer"], "model": args.model,
                                  "pre_call_cost_ceiling_usd": prebound, **result}
        if result["status"] != "received":
            record.update(usage_present=False, content_present=False, reasoning_content_present=False,
                          stop_reason="request error has no trustworthy usage accounting")
            state["records"].append(record)
            append_jsonl(accounting, record)
            update_stats(state)
            state["status"] = "stopped_request_error"
            state["stop_reason"] = record["stop_reason"]
            atomic_json(state_path, state)
            write_card(state, card)
            break
        try:
            cost, usage, billed = response_cost(result["usage"], args.input_price_ceiling, args.output_price_ceiling)
        except StopCollection as error:
            record["status"] = "usage_unavailable"
            record["stop_reason"] = str(error)
            state["records"].append(record)
            append_jsonl(accounting, record)
            update_stats(state)
            state["status"] = "stopped_usage_unavailable"
            state["stop_reason"] = str(error)
            atomic_json(state_path, state)
            write_card(state, card)
            break
        record.update(usage=usage, usage_cost_ceiling_usd=cost, proxy_billed_cost_usd=billed,
                      truncated=result.get("finish_reason") == "length",
                      content_present=isinstance(result.get("raw_content"), str) and bool(result.get("raw_content").strip()),
                      reasoning_content_present=isinstance(result.get("raw_reasoning_content"), str) and bool(result.get("raw_reasoning_content").strip()))
        content, reasoning = result.get("raw_content"), result.get("raw_reasoning_content")
        if not isinstance(reasoning, str) or not reasoning.strip():
            record["status"] = "reasoning_unavailable"
            record["stop_reason"] = "reasoning_content is empty or unavailable"
            state["records"].append(record)
            append_jsonl(raw, record)
            append_jsonl(accounting, record)
            update_stats(state)
            state["status"] = "stopped_reasoning_unavailable"
            state["stop_reason"] = record["stop_reason"]
            atomic_json(state_path, state)
            write_card(state, card)
            break
        final = candidate(content) if isinstance(content, str) else ""
        record.update(final_candidate=final, correct_nontruncated=not record["truncated"] and correct(row["answer"], final, row["source"]))
        state["records"].append(record)
        append_jsonl(raw, record)
        append_jsonl(accounting, record)
        update_stats(state)
        if args.pilot_only:
            state["status"] = "pilot_complete"
        atomic_json(state_path, state)
        write_card(state, card)
        print(json.dumps({"sequence": index + 1, "id": row["id"], "correct_nontruncated": record["correct_nontruncated"],
                          "usage_cost_ceiling_usd": round(cost, 6), "cumulative_cost_ceiling_usd": round(state["stats"]["usage_cost_ceiling_usd"], 6)}, ensure_ascii=False), flush=True)
        if args.pilot_only:
            break
    else:
        state["status"] = "complete"
        update_stats(state)
        atomic_json(state_path, state)
        write_card(state, card)
    print(json.dumps({"status": state["status"], "stats": state["stats"]}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except StopCollection as error:
        print(f"collector stopped: {error}", file=sys.stderr)
        raise SystemExit(2)
