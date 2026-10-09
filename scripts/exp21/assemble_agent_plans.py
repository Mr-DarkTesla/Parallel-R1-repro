"""Check and assemble human/agent plans inside saved reasoning traces; no model calls.

Usage: python assemble_agent_plans.py TRACES PLANS POOL TOKENIZER OUT_DIR
TRACES rows need id and response (question defaults to POOL); PLANS rows need id and plan.
"""
import argparse
import collections
import json
import re
from pathlib import Path

from transformers import AutoTokenizer

from build_sft import row as sft_row
from checks import candidate, check, correct
from m2_convert import PLAN, PlanError, assemble, parse_plan, split_units
from mv_format import parse

THINK = re.compile(r"\A<think>(.*?)</think>(.*)\Z", re.S)


def read(path):
    return [json.loads(line) for line in Path(path).open()]


def convert(trace, plan, gold, tokenizer):
    match = THINK.fullmatch(trace["response"].strip())
    if not match:
        return {"status": "bad_think"}
    if not correct(gold["answer"], candidate(match.group(2)), gold["source"]):
        return {"status": "wrong_original_answer"}
    wrapper = PLAN.fullmatch(plan.strip())
    if not wrapper or wrapper.group(1) != trace["id"] + "#0":
        return {"status": "bad_plan_wrapper"}
    units, seps = split_units(match.group(1))
    try:
        blocks, edits = parse_plan(wrapper.group(2), len(units))
    except PlanError as exc:
        return {"status": "plan_error", "error": str(exc)}
    if not blocks:
        return {"status": "no_block"}
    inner, decisions = assemble(units, seps, blocks, edits)
    if inner is None:
        return {"status": "filtered", "decisions": decisions}
    response = "<think>\n" + inner.strip() + "\n</think>" + match.group(2)
    audit = check(response, gold["answer"], gold["source"], original=trace["response"])
    parsed = parse(response)
    if not parsed["blocks"] or any(b["end"] > response.index("</think>") for b in parsed["blocks"]):
        audit["issues"].append("block_outside_think")
    e = sft_row("parallel_th", {"id": trace["id"], "question": trace["question"], "response": response})["extra_info"]
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": e["question"]}],
                                           add_generation_prompt=True, tokenize=False, enable_thinking=True)
    tokens = len(tokenizer.encode(prompt, add_special_tokens=False))
    tokens += len(tokenizer.encode(e["answer"] + tokenizer.eos_token, add_special_tokens=False))
    if tokens > 4096:
        audit["issues"].append("length")
    audit["issues"] = sorted(set(audit["issues"]))
    audit["ok"] = not audit["issues"]
    return {"status": "ok" if audit["ok"] else "rejected", "response": response,
            "check": audit, "tokens": tokens, "decisions": decisions}


def main():
    ap = argparse.ArgumentParser()
    for name in ("traces", "plans", "pool", "tokenizer", "out_dir"):
        ap.add_argument(name)
    args = ap.parse_args()
    traces = read(args.traces)
    plans = {r["id"]: r for r in read(args.plans)}
    gold = {r["id"]: r for r in read(args.pool)}
    assert len(plans) == len(traces) == len({r["id"] for r in traces})
    assert set(plans) == {r["id"] for r in traces} <= set(gold)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for trace in traces:
        trace = {"question": gold[trace["id"]]["question"], **trace}
        record = {"id": trace["id"], "source": gold[trace["id"]]["source"],
                  "question": trace["question"], "original_response": trace["response"],
                  "plan": plans[trace["id"]]["plan"], "rationale": plans[trace["id"]].get("rationale", "")}
        record.update(convert(trace, record["plan"], gold[trace["id"]], tokenizer))
        results.append(record)
    (out / "assembled.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results))
    summary = {"traces": len(results), "status": dict(collections.Counter(r["status"] for r in results)),
               "issues": dict(collections.Counter(issue for r in results for issue in r.get("check", {}).get("issues", [])))}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
