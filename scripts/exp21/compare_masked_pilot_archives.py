"""Paired 95% bootstrap comparison of identical masked pilot questions."""
import json
import random
import sys
import tarfile
from pathlib import Path


def load(path):
    with tarfile.open(path) as archive:
        names = sorted(n for n in archive.getnames() if n.endswith("-block-rows.jsonl"))
        rows = [json.loads(line) for name in names for line in archive.extractfile(name)]
    key = lambda row: (row["source"], row["problem_id"], row["sample"])
    assert len({key(row) for row in rows}) == len(rows)
    return {key(row): row for row in rows}


def compare(base, candidate, keys, metric):
    deltas = [float(candidate[key][metric]) - float(base[key][metric]) for key in keys]
    rng = random.Random(0)
    n = len(deltas)
    samples = sorted(sum(deltas[rng.randrange(n)] for _ in range(n)) / n for _ in range(10000))
    scale = 100 if metric in ("acc_robust", "think_numbered_block", "truncated") else 1
    return {"base": round(scale * sum(float(base[k][metric]) for k in keys) / n, 2),
            "candidate": round(scale * sum(float(candidate[k][metric]) for k in keys) / n, 2),
            "delta": round(scale * sum(deltas) / n, 2),
            "ci95": [round(scale * samples[i], 2) for i in (249, 9749)], "n": n}


def main():
    base, candidate = map(load, sys.argv[1:3])
    assert base.keys() == candidate.keys(), "different questions"
    for key in base:
        assert base[key]["input"] == candidate[key]["input"], f"different prompt: {key}"
        assert base[key]["decoder"] == candidate[key]["decoder"] == "masked"
    output = {"base_archive": Path(sys.argv[1]).name, "candidate_archive": Path(sys.argv[2]).name}
    for source in ("all", *sorted({key[0] for key in base})):
        keys = [key for key in sorted(base) if source == "all" or key[0] == source]
        output[source] = {metric: compare(base, candidate, keys, metric)
                          for metric in ("acc_robust", "think_numbered_block", "truncated", "tokens", "forward_passes")}
    Path(sys.argv[3]).write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output["all"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
