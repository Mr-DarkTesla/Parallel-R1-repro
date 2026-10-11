"""Assemble independently reviewed wave-76 labels, excluding disputed gold."""

import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
sys.path.insert(0, str(ROOT / "scripts"))
from exp21.mv_format import TAGS, parse  # noqa: E402

EXCLUDED = {"gsm8k-train/7364", "gsm8k-train/3715", "math-train/2326"}


def rows(path):
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    pool = {row["id"]: row for row in rows(DATA / "pool.jsonl")}
    accepted = []
    seen = set()
    statuses = {}
    for batch in (1, 2, 3):
        inputs = {row["id"]: row for row in rows(DATA / f"agent_parallel_wave76_input_{batch}.jsonl")}
        finals = rows(DATA / f"agent_parallel_wave76_final_{batch}.jsonl")
        if len(inputs) != len(finals):
            raise ValueError(f"batch {batch}: input/final count differs")
        for row in finals:
            id_ = row["id"]
            if id_ in seen or id_ not in inputs or id_ not in pool:
                raise ValueError(f"duplicate or unknown id: {id_}")
            seen.add(id_)
            status = row["status"]
            statuses[status] = statuses.get(status, 0) + 1
            if status != "ready" or id_ in EXCLUDED:
                continue
            source = inputs[id_]
            truth = pool[id_]
            if source["question"] != truth["question"] or source["source"] != truth["source"]:
                raise ValueError(f"candidate differs from pool: {id_}")
            output = row["output"]
            if not output.startswith("<think>") or output.count("</think>") != 1:
                raise ValueError(f"invalid think block: {id_}")
            thought, final = output.split("</think>", 1)
            parsed = parse(thought)
            if not parsed["valid"] or len(parsed["blocks"]) != 1 or not parsed["blocks"][0]["numbered"]:
                raise ValueError(f"invalid Parallel block: {id_}")
            if any(tag in final for tag in TAGS) or not final.strip().startswith("Final Answer:"):
                raise ValueError(f"invalid external final: {id_}")
            accepted.append({
                "id": id_, "source": source["source"], "question": source["question"],
                "answer": truth["answer"], "answer_type": source["answer_type"],
                "output": output, "provenance": f"agent_parallel_wave76_batch{batch}",
            })
    if len(seen) != 76 or len(accepted) != 71 or statuses != {"ready": 73, "gold_conflict": 1, "skip": 2}:
        raise ValueError(f"unexpected counts: seen={len(seen)}, accepted={len(accepted)}, statuses={statuses}")
    path = DATA / "agent_parallel_wave76_accepted.jsonl"
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in accepted))
    pilot = rows(DATA / "agent_parallel_pilot20_accepted.jsonl")
    combined = pilot + accepted
    normalized = [" ".join(unicodedata.normalize("NFKC", row["question"]).split()).casefold()
                  for row in combined]
    if len(pilot) != 20 or len({row["id"] for row in combined}) != 91 or len(set(normalized)) != 91:
        raise ValueError("pilot plus wave has duplicate or missing questions")
    combined_path = DATA / "agent_parallel_91_accepted.jsonl"
    combined_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in combined))
    print(json.dumps({"accepted": len(accepted), "statuses": statuses,
                      "combined": len(combined), "excluded": sorted(EXCLUDED)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
