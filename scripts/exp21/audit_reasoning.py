"""Independent, resumable audit of every displayed step in a paired response.

Claude only flags possible errors. A human must review flagged rows and a fresh
random sample of retained rows before using the filter for training.
"""
import argparse
import concurrent.futures
import json
import sys
from pathlib import Path

from claude_call import call


SYSTEM = """You audit mathematical training data. Check the entire response, both inside and after <Parallel>, against the problem. Check EVERY displayed equation, enumeration, premise, and claim. The final answer may be right by coincidence, so do not use it as a shortcut. Flag a substantive false statement, wrong arithmetic, invalid case enumeration, or unsupported geometric premise. An incomplete but non-false proof is a separate issue. Do not flag harmless notation or style. Return ONLY JSON with keys: status (clean, error, incomplete, uncertain), issue (specific short explanation), quote (short exact fragment of response proving the issue). If clean, issue and quote are empty strings. Be especially alert to using diameter as radius, swapping symbols, misreading cos(angle) as angle, and wrong listed outcomes."""


def audit(row):
    user = f"Problem:\n{row['question']}\n\nReference answer:\n{row['answer']}\n\nResponse to audit:\n{row['response']}"
    result = call(SYSTEM, user, timeout=600)
    try:
        raw = result["text"].strip().removeprefix("```json").removesuffix("```").strip()
        verdict = json.loads(raw)
        assert verdict["status"] in {"clean", "error", "incomplete", "uncertain"}
    except (ValueError, KeyError, AssertionError):
        verdict = {"status": "uncertain", "issue": "Could not parse auditor reply", "quote": ""}
    return {"id": row["id"], "question": row["question"], "answer": row["answer"],
            "response": row["response"], "status": verdict["status"], "issue": verdict.get("issue", ""),
            "quote": verdict.get("quote", ""), "cost_usd": result.get("cost_usd"),
            "is_error": result.get("is_error", False)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    rows = [json.loads(s) for s in open(args.input)]
    out = Path(args.output)
    previous = [json.loads(s) for s in out.read_text().splitlines()] if out.exists() else []
    done = {r["id"]: r for r in previous}
    assert len(done) == len(previous)
    assert len(rows) == len({r["id"] for r in rows})
    for row in rows:
        if row["id"] in done:
            assert all(done[row["id"]].get(k) == row[k] for k in ("question", "answer", "response")), row["id"]
    todo = [r for r in rows if r["id"] not in done]
    print(f"Auditing {len(todo)} of {len(rows)} rows", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool, out.open("a") as f:
        futures = {pool.submit(audit, row): row for row in todo}
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                result = future.result()
            except Exception as e:
                row = futures[future]
                result = {"id": row["id"], "question": row["question"], "answer": row["answer"],
                          "response": row["response"], "status": "uncertain", "issue": str(e),
                          "quote": "", "cost_usd": None, "is_error": True}
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
            f.flush()
            if i % 10 == 0 or result["status"] != "clean":
                print(f"{i}/{len(todo)} {result['id']} {result['status']}", flush=True)


if __name__ == "__main__":
    main()
