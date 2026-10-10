"""Select unused, previously solved pool tasks for new Qwen thinking traces.

The source contains correct Qwen no-thinking answers, but their text is not
used: only the questions and pool references go to the thinking generator.
"""
import collections
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
DATA = ROOT / "data"
AUDIT = ROOT / "audit"
OUT = AUDIT / "qwen_structured_thinking"
SEED = 20261010
QUOTAS = {("gsm8k", "integer"): 550, ("math", "integer"): 600,
          ("math", "expression"): 230, ("math", "fraction"): 120}
USED = [DATA / name for name in (
    "pair_final_m1.jsonl", "pair_final_m2.jsonl", "more_m1_matched180.jsonl",
    "more_m2_matched180.jsonl", "replay_nt.jsonl", "replay_th.jsonl", "sol_deep75.jsonl",
)] + [AUDIT / "qwen_trace_screen/accepted13.jsonl",
      AUDIT / "think_trace_sol/accepted_all_reviewed.jsonl"]


def rows(path):
    return (json.loads(line) for line in path.open())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    used = {r["id"] for path in USED for r in rows(path)}
    choices = collections.defaultdict(list)
    for r in rows(DATA / "more_m2_new_inputs.jsonl"):
        key = (r["source"], r["answer_type"])
        if r["id"] not in used and key in QUOTAS and "[asy]" not in r["question"]:
            choices[key].append({k: r[k] for k in ("id", "source", "question", "answer", "answer_type")})
    rng = random.Random(SEED)
    selected = []
    counts = {}
    for key, quota in QUOTAS.items():
        group = choices[key]
        rng.shuffle(group)
        if len(group) < quota:
            raise ValueError(f"not enough {key}: {len(group)} < {quota}")
        selected += group[:quota]
        counts["/".join(key)] = {"eligible": len(group), "selected": quota}
    rng.shuffle(selected)
    assert len({r["id"] for r in selected}) == len(selected)
    with (OUT / "inputs1500_with_gold.jsonl").open("w") as f:
        for r in selected:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (OUT / "selection.json").write_text(json.dumps({"seed": SEED, "source": "more_m2_new_inputs.jsonl",
                                                     "excluded_used_ids": len(used), "counts": counts}, indent=2) + "\n")
    print(len(selected), counts)


if __name__ == "__main__":
    main()
