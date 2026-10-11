#!/usr/bin/env python3
"""Paired bootstrap interval for manually reviewed external answers."""
import json
import random
import sys
from pathlib import Path


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text())["archives"]
    base_name, candidate_name, out = sys.argv[2:5]
    def rows(name):
        return {tuple(row["key"]): row for row in manifest[name]["rows"]}
    base, candidate = rows(base_name), rows(candidate_name)
    assert len(base) == len(candidate) == 40 and base.keys() == candidate.keys()
    keys = sorted(base)
    deltas = [int(candidate[k]["external_correct"]) - int(base[k]["external_correct"]) for k in keys]
    rng = random.Random(0)
    samples = sorted(100 * sum(deltas[rng.randrange(40)] for _ in range(40)) / 40
                     for _ in range(10000))
    result = {"base": base_name, "candidate": candidate_name, "n": 40,
              "base_correct": sum(int(base[k]["external_correct"]) for k in keys),
              "candidate_correct": sum(int(candidate[k]["external_correct"]) for k in keys),
              "paired_delta_pp": round(100 * sum(deltas) / 40, 2),
              "ci95_pp": [round(samples[i], 2) for i in (249, 9749)],
              "method": "10000 paired percentile bootstrap resamples, seed 0"}
    Path(out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
