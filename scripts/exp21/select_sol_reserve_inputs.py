"""Choose unused, previously verified parallel problems for blind Sol traces."""
import collections
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
DATA = ROOT / "data"
OUT = ROOT / "audit/sol_reserve_round3"
SEED = 20261010
RESERVES = ("more_m1_180_reserve.jsonl", "more_m1_matched180_reserve.jsonl",
            "more_m2_matched180_reserve.jsonl")
USED = ("pair_final_m1.jsonl", "pair_final_m2.jsonl", "more_m1_matched180.jsonl",
        "more_m2_matched180.jsonl", "replay_nt.jsonl", "replay_th.jsonl",
        "sol_deep75.jsonl")


def read(path):
    return (json.loads(line) for line in path.open())


def write(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    used = {row["id"] for name in USED for row in read(DATA / name)}
    used |= {row["id"] for row in read(ROOT / "audit/deep_trace_round2/accepted51.jsonl")}
    used |= {row["id"] for row in read(ROOT / "audit/qwen_structured_thinking/inputs_clean_with_gold.jsonl")}
    available = {}
    for name in RESERVES:
        for row in read(DATA / name):
            if row["id"] not in used and "[asy]" not in row["question"]:
                available.setdefault(row["id"], row)
    items = list(available.values())
    rng = random.Random(SEED)
    rng.shuffle(items)
    gold = [{k: row[k] for k in ("id", "source", "question", "answer", "answer_type")}
            for row in items]
    blind = [{k: row[k] for k in ("id", "source", "question", "answer_type")}
             for row in items]
    write(OUT / "candidates_with_gold.jsonl", gold)
    write(OUT / "candidates_blind.jsonl", blind)
    (OUT / "selection.json").write_text(json.dumps({"seed": SEED, "count": len(gold),
        "by_type": dict(collections.Counter(f"{r['source']}/{r['answer_type']}" for r in gold)),
        "excluded_prior_ids": len(used), "sources": RESERVES}, indent=2) + "\n")
    print(len(gold))


def make_clean_batches():
    """Run only after leakcheck_candidates; hide gold and reserve answers."""
    hits = read(OUT / "leakcheck_candidates.hits.jsonl")
    bad = {row["id"] for row in hits if any(
        hit["eval_set"] == "math_test_full(info)" and
        (hit["leak"] or hit.get("strong") or hit.get("jac", 0) >= 0.6)
        for hit in row["hits"])}
    gold = [row for row in read(OUT / "candidates_with_gold.jsonl") if row["id"] not in bad]
    blind = [{k: row[k] for k in ("id", "source", "question", "answer_type")} for row in gold]
    write(OUT / "clean_with_gold.jsonl", gold)
    write(OUT / "clean_blind.jsonl", blind)
    for index, name in enumerate("abc"):
        folder = OUT / f"agent_{name}"
        folder.mkdir(exist_ok=True)
        write(folder / "input.jsonl", blind[index::3])
    (OUT / "clean_selection.json").write_text(json.dumps({"excluded_math_test": sorted(bad),
        "count": len(gold), "batches": {name: len(blind[index::3]) for index, name in enumerate("abc")}},
        indent=2) + "\n")
    print("clean", len(gold), "excluded", len(bad))


if __name__ == "__main__":
    import sys
    make_clean_batches() if sys.argv[1:] == ["--clean"] else main()
