"""Select 180 new M1 examples after a full-step audit, keeping source/answer diversity.

Usage: python select_more_m1.py CANDIDATES AUDIT PRIOR_M2_OK OUT_PREFIX [EXCLUDE_IDS]
Only clean audited rows qualify. Known working M2 plans get priority for paired data.
"""
import collections
import json
import random
import sys
from pathlib import Path


QUOTA = {("gsm8k", "integer"): 53, ("math", "integer"): 30,
         ("math", "fraction"): 61, ("math", "expression"): 36}


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    candidate_path, audit_path, m2_path, output = sys.argv[1:5]
    exclude = set(Path(sys.argv[5]).read_text().splitlines()) if len(sys.argv) > 5 else set()
    candidates = read(candidate_path)
    verdicts = {r["id"]: r for r in read(audit_path)}
    assert len(verdicts) == len(candidates)
    assert len({r["id"] for r in candidates}) == len(candidates)
    m2_ok = {r["id"] for r in read(m2_path) if r["status"] == "ok"}
    clean = []
    for row in candidates:
        verdict = verdicts[row["id"]]
        assert all(verdict[k] == row[k] for k in ("question", "answer", "response")), row["id"]
        if verdict["status"] == "clean" and row["id"] not in exclude:
            clean.append(row)
    groups = collections.defaultdict(list)
    for row in clean:
        groups[(row["source"], row["answer_type"])].append(row)
    rng = random.Random(21)
    chosen, reserve = [], []
    for group, n in QUOTA.items():
        preferred = sorted((r for r in groups[group] if r["id"] in m2_ok), key=lambda r: r["id"])
        others = sorted((r for r in groups[group] if r["id"] not in m2_ok), key=lambda r: r["id"])
        rng.shuffle(others)
        ordered = preferred + others
        assert len(ordered) >= n, (group, len(ordered), n)
        chosen.extend(ordered[:n])
        reserve.extend(ordered[n:])
    prefix = Path(output)
    for suffix, rows in ((".jsonl", chosen), ("_reserve.jsonl", reserve)):
        prefix.with_name(prefix.name + suffix).write_text("".join(
            json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(rows, key=lambda x: x["id"])))
    stats = {"selected": len(chosen), "reserve": len(reserve), "excluded_after_review": sorted(exclude),
             "audit_status": dict(collections.Counter(r["status"] for r in verdicts.values())),
             "selected_distribution": {f"{a}/{b}": sum((r["source"], r["answer_type"]) == (a, b) for r in chosen)
                                       for a, b in QUOTA},
             "selected_with_prior_m2_plan": sum(r["id"] in m2_ok for r in chosen),
             "auditor_known_cost_usd": sum(r.get("cost_usd") or 0 for r in verdicts.values()),
             "auditor_unpriced_calls": sum(r.get("cost_usd") is None for r in verdicts.values())}
    prefix.with_name(prefix.name + "_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
