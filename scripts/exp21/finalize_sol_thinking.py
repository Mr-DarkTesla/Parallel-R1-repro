"""Combine fully reviewed Sol thinking blocks and choose 187 primary rows for matched SFT.

Usage: python -B scripts/exp21/finalize_sol_thinking.py
No model, network or GPU calls.
"""
import collections
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/21-qwen3-0.6b-multiverse"
AUDIT = BASE / "audit/think_trace_sol"
SEED = 21
TARGET = 187


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return [json.loads(line) for line in path.open() if line.strip()]


def write(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def finalized_batch(prefix, reviews, gold):
    assembled = read(AUDIT / f"{prefix}_assembled/assembled.jsonl")
    candidates = [row for row in assembled if row["status"] == "ok"]
    by_id = {row["id"]: row for row in candidates}
    require(len(by_id) == len(candidates), f"duplicate assembled ID in {prefix}")
    judgments = [row for name in reviews for row in read(AUDIT / name)]
    verdict = {row["id"]: row for row in judgments}
    require(len(verdict) == len(judgments), f"duplicate review ID in {prefix}")
    require(set(verdict) == set(by_id), f"incomplete review coverage in {prefix}")
    rejected = [row["id"] for row in candidates if not all(verdict[row["id"]][key]
                                                          for key in ("answer_correct", "reasoning_correct", "useful_block"))]
    rows = []
    for row in candidates:
        if row["id"] in rejected:
            continue
        ref = gold[row["id"]]
        rows.append({"id": row["id"], "source": ref["source"], "question": ref["question"],
                     "answer": ref["answer"], "answer_type": ref["answer_type"],
                     "response": row["response"],
                     "provenance": "sol-6.1-public-solution+independent-sol-6.1-plan-only; full-review"})
    write(AUDIT / f"{prefix}_final.jsonl", rows)
    return rows, {"assembled_ok": len(candidates), "fully_reviewed": len(judgments),
                  "rejected_ids": rejected, "accepted": len(rows)}


def main():
    gold = {row["id"]: row for row in read(BASE / "data/pool.jsonl")}
    first = read(AUDIT / "accepted29.jsonl")
    second, second_audit = finalized_batch("next80", ["next80_independent_review30.jsonl",
                                                         "next80_personal_review20.jsonl",
                                                         "next80_review_remaining19_verdict.jsonl"], gold)
    third, third_audit = finalized_batch("next120", ["next120_independent_review30.jsonl",
                                                         "next120_personal_review20.jsonl",
                                                         "next120_review_remaining_a_verdict.jsonl",
                                                         "next120_review_remaining_b_verdict.jsonl"], gold)
    all_rows = first + second + third
    require(len({row["id"] for row in all_rows}) == len(all_rows), "duplicate ID across batches")
    require(len(all_rows) >= TARGET, "not enough reviewed rows")
    write(AUDIT / "accepted_all_reviewed.jsonl", all_rows)

    replay_ids = {row["id"] for name in ("replay_nt", "replay_th")
                  for row in read(BASE / f"data/{name}.jsonl")}
    replay_overlap = sorted({row["id"] for row in all_rows if row["id"] in replay_ids})
    eligible = [row for row in all_rows if row["id"] not in replay_ids]
    noninteger = [row for row in eligible if row["answer_type"] != "integer"]
    integer = [row for row in eligible if row["answer_type"] == "integer"]
    require(len(noninteger) <= TARGET, "too many noninteger rows for target size")
    rng = random.Random(SEED)
    selected_ids = {row["id"] for row in noninteger}
    selected_ids.update(row["id"] for row in rng.sample(integer, TARGET - len(noninteger)))
    selected = [row for row in all_rows if row["id"] in selected_ids]
    require(len(selected) == TARGET, "incorrect selection size")
    write(AUDIT / "selected187.jsonl", selected)

    summary = {"old_pilot": len(first), "next80": second_audit, "next120": third_audit,
               "all_fully_reviewed": len(all_rows), "selected_for_matched_sft": len(selected),
               "selection_seed": SEED,
               "selection_rule": "exclude replay-overlap IDs, retain all fraction/expression rows, seeded sample of integer rows; preserve source order",
               "excluded_due_to_replay_overlap": replay_overlap,
               "all_answer_types": dict(collections.Counter(row["answer_type"] for row in all_rows)),
               "selected_answer_types": dict(collections.Counter(row["answer_type"] for row in selected)),
               "selected_sources": dict(collections.Counter(row["source"] for row in selected)),
               "not_selected_ids": [row["id"] for row in all_rows if row["id"] not in selected_ids]}
    (AUDIT / "final_review_and_selection.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
