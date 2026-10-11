#!/usr/bin/env python3
"""Validate v2 Sol-authored examples and prepare a blinded final 30-row review."""
from __future__ import annotations

import collections
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_more_4b_teacher_parallel import TOKENIZER, load_tokenizer, validate
from mv_format import ANY_TAG


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
CANDIDATES = DATA / "qwen4b_extra_v2_candidates.jsonl"
AUTHOR = AUDIT / "qwen4b_extra_v2_sol_author.jsonl"
V1_STRICT = DATA / "qwen4b_teacher_extra_tagged.jsonl"
OUT_TAGGED = DATA / "qwen4b_extra_v2_tagged.jsonl"
OUT_PLAIN = DATA / "qwen4b_extra_v2_plain.jsonl"
OUT_REJECTED = AUDIT / "qwen4b_extra_v2_rejected.jsonl"
OUT_REPORT = AUDIT / "qwen4b_extra_v2_report.json"
REVIEW_IN = AUDIT / "qwen4b_extra_v2_final_review_input.jsonl"
REVIEW = AUDIT / "qwen4b_extra_v2_final_review.jsonl"
LEAKCHECK = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py"
CORPUS = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus"


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    os.replace(temporary, path)


def leakcheck(rows: list[dict]) -> dict:
    input_path, prefix = AUDIT / "qwen4b_extra_v2_leakcheck_input.jsonl", AUDIT / "qwen4b_extra_v2_leakcheck"
    write(input_path, [{key: row[key] for key in ("id", "question", "answer")} for row in rows])
    done = subprocess.run([sys.executable, "-B", str(LEAKCHECK), str(input_path), str(prefix), "--corpus", str(CORPUS)],
                          cwd=ROOT, capture_output=True, text=True, check=False)
    if done.returncode:
        raise SystemExit(f"leakcheck failed: {done.stderr[-300:]}")
    result = json.loads(prefix.with_suffix(".summary.json").read_text())
    if result["n_leaky_vs_our_evals"]:
        raise SystemExit("leakcheck found eval leak")
    return result


def main() -> None:
    candidates = {row["id"]: row for row in read(CANDIDATES)}
    authored = read(AUTHOR)
    if len({row["id"] for row in authored}) != len(authored) or not set(row["id"] for row in authored) <= set(candidates):
        raise SystemExit("author IDs duplicate or are outside v2 candidate manifest")
    tokenizer = load_tokenizer()
    tagged, rejected = [], []
    for authored_row in authored:
        source = candidates[authored_row["id"]]
        ok, issues, facts = validate(authored_row["response"], source, tokenizer)
        if not ok:
            rejected.append({"id": source["id"], "reason": issues, **facts})
            continue
        tagged.append({"id": source["id"], "source": source["source"], "question": source["question"],
                       "answer": source["gold"], "answer_type": source["answer_type"], "response": authored_row["response"],
                       "teacher": "fresh_sol61_authoring_v2", "question_and_gold_source": "qwen4b_teacher_graded320.jsonl",
                       "status": "auto_checked_pending_final_review", **facts})
    ids = {row["id"] for row in tagged}
    if len(ids) != len(tagged):
        raise SystemExit("validated v2 IDs duplicate")
    plain = [{**row, "response": ANY_TAG.sub("", row["response"])} for row in tagged]
    if not all(ANY_TAG.sub("", left["response"]) == right["response"] for left, right in zip(tagged, plain)):
        raise SystemExit("plain arm differs beyond tags")
    manual_screen = read(OUT_REJECTED) if OUT_REJECTED.exists() else []
    if not authored:
        if ({row.get("id") for row in manual_screen} != set(candidates) or
                any(set(row) != {"id", "structure_type", "reason"} for row in manual_screen)):
            raise SystemExit("empty author run requires one concrete manual verdict per candidate")
    leak = leakcheck(tagged)
    write(OUT_TAGGED, tagged)
    write(OUT_PLAIN, plain)
    if authored:
        write(OUT_REJECTED, rejected)

    v1 = read(V1_STRICT)
    if len(v1) != 19 or ids & {row["id"] for row in v1}:
        raise SystemExit("unexpected v1 strict pair or overlap")
    review_pool = v1 + tagged
    if not REVIEW.exists() and len(review_pool) >= 30:
        write(REVIEW_IN, review_pool[:30])
    review_rows = read(REVIEW) if REVIEW.exists() else []
    review_ok = sum(row.get("useful") is True and row.get("answer_correct") is True and
                    row.get("block_grammar_inside_think") is True and row.get("paths_independent") is True and
                    row.get("conclusion_correct") is True for row in review_rows)
    ready = len(review_rows) >= 30 and review_ok / len(review_rows) >= .9 and all(row.get("answer_correct") is True for row in review_rows)
    report = {"status": "ready_for_sft_but_not_staged" if ready else "pending_or_failed_final_review",
              "ready_for_sft": ready, "author_rows": len(authored), "auto_accepted": len(tagged),
              "auto_rejected": len(rejected), "manual_screen": {"rows": len(manual_screen),
                  "unique_ids": len({row.get("id") for row in manual_screen}),
                  "by_structure": dict(collections.Counter(row.get("structure_type") for row in manual_screen))},
              "by_source": dict(collections.Counter(row["source"] for row in tagged)),
              "checks": {"grammar_inside_think": len(tagged), "math_verify": len(tagged),
                         "independence_heuristic": len(tagged), "numeric_invariants": len(tagged),
                         "under_4096": len(tagged), "max_tokens": max((row["tokens"] for row in tagged), default=0),
                         "plain_only_removes_tags": len(tagged), "leakcheck": leak},
              "final_review": {"pool_v1_strict": len(v1), "pool_v2_auto": len(tagged), "input_rows": min(30, len(review_pool)),
                               "review_rows": len(review_rows), "strictly_useful": review_ok,
                               "useful_fraction": review_ok / len(review_rows) if review_rows else None},
              "outputs": {"tagged": str(OUT_TAGGED.relative_to(ROOT)), "plain": str(OUT_PLAIN.relative_to(ROOT)),
                          "review_input": str(REVIEW_IN.relative_to(ROOT)) if REVIEW_IN.exists() else None},
              "command": "uv run --offline --no-project --with tokenizers==0.23.2 --with math-verify==0.9.0 python scripts/exp21/finalize_qwen4b_extra_v2.py"}
    OUT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"auto_accepted": len(tagged), "review_pool": len(review_pool), "ready_for_sft": ready}, ensure_ascii=False))


if __name__ == "__main__":
    main()
