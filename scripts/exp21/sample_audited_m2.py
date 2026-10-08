"""Draw fresh disjoint stratified review samples from audited M2 examples."""
import argparse
import collections
import json
import random
from pathlib import Path


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("selected")
    ap.add_argument("out_prefix")
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--seed", type=int, default=2109)
    args = ap.parse_args()
    excluded = {r["id"] for path in args.exclude for r in read(path)}
    groups = collections.defaultdict(list)
    for r in read(args.selected):
        if r["id"] not in excluded:
            groups[(r["source"], r["answer_type"])].append(r)
    rng = random.Random(args.seed)
    for values in groups.values():
        rng.shuffle(values)
    quotas = [("gsm8k", "integer", 7, 4), ("math", "integer", 11, 5),
              ("math", "fraction", 11, 5), ("math", "expression", 11, 6)]
    independent, self_review = [], []
    for source, kind, n_independent, n_self in quotas:
        rows = groups[source, kind]
        assert len(rows) >= n_independent + n_self, (source, kind, len(rows))
        independent += rows[:n_independent]
        self_review += rows[n_independent:n_independent + n_self]
    for suffix, rows in (("independent40", independent), ("self20", self_review)):
        with open(f"{args.out_prefix}_{suffix}.jsonl", "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {"selected": args.selected, "seed": args.seed, "exclude_files": args.exclude,
                "excluded_prior_ids": sorted(excluded),
                "quotas": [{"source": s, "answer_type": k, "independent": ni, "self": ns}
                           for s, k, ni, ns in quotas],
                "independent40_ids": [r["id"] for r in independent],
                "self20_ids": [r["id"] for r in self_review]}
    Path(f"{args.out_prefix}_sampling.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"independent40": len(independent), "self20": len(self_review), "excluded_prior_ids": len(excluded)}))


if __name__ == "__main__":
    main()
