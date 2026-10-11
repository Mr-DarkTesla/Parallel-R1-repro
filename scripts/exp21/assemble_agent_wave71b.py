"""Assemble independently reviewed wave71b labels without disputed paths."""

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
sys.path.insert(0, str(ROOT / "scripts"))
from exp21.mv_format import TAGS, parse  # noqa: E402

REJECTED = {
    "gsm8k-train/5968", "math-train/6173", "math-train/5579",
    "math-train/2556", "math-train/3251", "math-train/5184",
    "math-train/6734",
}
REVIEWS = [
    "agent_parallel_wave71b_review_1_by_4.md",
    "agent_parallel_wave71b_review_2_by_3.md",
    "agent_parallel_wave71b_review_3_by_1.md",
    "agent_parallel_wave71b_review_4_by_1.md",
]


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split()).casefold()


def main():
    pool = {row["id"]: row for row in rows(DATA / "pool.jsonl")}
    prior = rows(DATA / "agent_parallel_91_accepted.jsonl")
    if len(prior) != 91:
        raise ValueError("expected 91 previously accepted examples")
    prior_gate = json.loads((RUN / "audit/agent_parallel_91_review_gate.json").read_text())
    if (set(prior_gate["reviewed_ids"]) != {row["id"] for row in prior}
            or set(prior_gate["useful_ids"]) != {row["id"] for row in prior}
            or prior_gate["wrong_final_ids"]):
        raise ValueError("previous 91-example review gate is not complete")
    for name in REVIEWS:
        if not (RUN / "audit" / name).is_file():
            raise ValueError(f"missing independent review: {name}")
    accepted, seen, skips = [], set(), set()
    for batch in range(1, 5):
        inputs = rows(DATA / f"agent_parallel_wave71b_input_{batch}.jsonl")
        finals = rows(DATA / f"agent_parallel_wave71b_final_{batch}.jsonl")
        source = {row["id"]: row for row in inputs}
        reviewed_text = (RUN / "audit" / REVIEWS[batch - 1]).read_text()
        mentioned = set(re.findall(r"(?:gsm8k|math)-train/\d+", reviewed_text))
        if not set(source) <= mentioned:
            raise ValueError(f"batch {batch}: independent report omits IDs: {sorted(set(source) - mentioned)}")
        if len(inputs) != len(finals) or len(source) != len(inputs):
            raise ValueError(f"batch {batch}: input/final count or IDs differ")
        if {row["id"] for row in finals} != set(source):
            raise ValueError(f"batch {batch}: final IDs differ from input")
        for row in finals:
            id_ = row["id"]
            if id_ in seen or id_ not in pool:
                raise ValueError(f"duplicate or unknown ID: {id_}")
            seen.add(id_)
            if row["status"] == "skip":
                skips.add(id_)
                continue
            if row["status"] != "ready":
                raise ValueError(f"unknown status: {id_}")
            if id_ in REJECTED:
                continue
            question = source[id_]
            truth = pool[id_]
            if question["question"] != truth["question"] or question["source"] != truth["source"]:
                raise ValueError(f"question differs from pool: {id_}")
            output = row["output"]
            if not output.startswith("<think>") or output.count("</think>") != 1:
                raise ValueError(f"invalid think block: {id_}")
            thought, final = output.split("</think>", 1)
            parsed = parse(thought)
            if not parsed["valid"] or len(parsed["blocks"]) != 1 or not parsed["blocks"][0]["numbered"]:
                raise ValueError(f"invalid Parallel block: {id_}")
            if thought.count("<Parallel>") != 1 or thought.count("<Path>") != 2 or thought.count("<Outline>") != 2:
                raise ValueError(f"wrong number of block paths: {id_}")
            if any(tag in final for tag in TAGS) or not final.strip().startswith("Final Answer:"):
                raise ValueError(f"invalid external final: {id_}")
            accepted.append({
                "id": id_, "source": question["source"], "question": question["question"],
                "answer": truth["answer"], "answer_type": question["answer_type"],
                "output": output, "provenance": f"agent_parallel_wave71b_batch{batch}",
            })
    if len(seen) != 71 or len(skips) != 5 or len(REJECTED & skips) or len(accepted) != 59:
        raise ValueError(f"unexpected gate counts: seen={len(seen)}, skip={len(skips)}, accepted={len(accepted)}")
    combined = prior + accepted
    if len({row["id"] for row in combined}) != 150 or len({normalize(row["question"]) for row in combined}) != 150:
        raise ValueError("duplicate ID or question in combined 150")
    (DATA / "agent_parallel_wave71b_accepted.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in accepted)
    )
    (DATA / "agent_parallel_150_accepted.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in combined)
    )
    gate = {
        "reviewer": "independent_cross_review_four_wave71b_batches_plus_previous_91",
        "method": "all_150_accepted_full_conditions_and_outputs_reviewed_in_cross_batch_reports; root_read_batch1_and_spot_checked_8_other_outputs",
        "reviewed_ids": sorted(row["id"] for row in combined),
        "useful_ids": sorted(row["id"] for row in combined),
        "wrong_final_ids": [],
        "evidence": prior_gate["evidence"] + [f"audit/{name}" for name in REVIEWS],
        "excluded_ids": sorted(set(prior_gate["excluded_ids"]) | skips | REJECTED),
    }
    (RUN / "audit/agent_parallel_150_review_gate.json").write_text(
        json.dumps(gate, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"inputs": len(seen), "accepted_new": len(accepted),
                      "rejected_semantics": sorted(REJECTED), "skips": sorted(skips),
                      "combined": len(combined), "review_reports": REVIEWS}, ensure_ascii=False))


if __name__ == "__main__":
    main()
