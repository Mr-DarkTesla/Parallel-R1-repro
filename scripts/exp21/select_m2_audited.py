"""Select equal-volume M2 data after full-step audit, retaining old task IDs first.

All candidates must have passed the original deterministic checks. A separate
on-pod recheck is required before SFT. Rows marked incomplete or uncertain by
the auditor are excluded conservatively.
"""
import argparse
import collections
import json
from pathlib import Path


MANUAL_EXCLUDE = {
    "math-train/2909", "math-train/3684", "math-train/7261", "math-train/2242",
    "math-train/2219", "math-train/6635", "math-train/2904",
}


def read(path):
    return [json.loads(line) for line in open(path)]


def main():
    ap = argparse.ArgumentParser()
    for name in ("original", "extra", "original_audit", "extra_audit", "out_prefix"):
        ap.add_argument(name)
    args = ap.parse_args()
    original, extra = read(args.original), read(args.extra)
    audits = {r["id"]: r for path in (args.original_audit, args.extra_audit) for r in read(path)}
    assert len(audits) == len(original) + len(extra)
    assert len({r["id"] for r in original + extra}) == len(original) + len(extra)
    desired = collections.Counter((r["source"], r["answer_type"]) for r in original)
    eligible = lambda r: audits[r["id"]]["status"] == "clean" and r["id"] not in MANUAL_EXCLUDE
    selected = [r for r in original if eligible(r)]
    retained = {r["id"] for r in selected}
    chosen_counts = collections.Counter((r["source"], r["answer_type"]) for r in selected)
    extras = [r for r in extra if eligible(r)]
    for group in sorted(desired):
        for r in extras:
            if (r["source"], r["answer_type"]) != group or r["id"] in retained:
                continue
            if chosen_counts[group] >= desired[group]:
                break
            selected.append(r)
            retained.add(r["id"])
            chosen_counts[group] += 1
    if len(selected) < len(original):
        for r in extras:
            if r["id"] in retained:
                continue
            selected.append(r)
            retained.add(r["id"])
            chosen_counts[(r["source"], r["answer_type"])] += 1
            if len(selected) == len(original):
                break
    assert len(selected) == len(original), f"Only {len(selected)} clean candidates; need {len(original)}"
    prefix = Path(args.out_prefix)
    with prefix.with_suffix(".jsonl").open("w") as f:
        for r in sorted(selected, key=lambda x: x["id"]):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    stats = {"selected": len(selected), "retained_original_ids": len([r for r in selected if r["id"] in {x["id"] for x in original}]),
             "joint_distribution": {f"{source}/{kind}": n for (source, kind), n in sorted(chosen_counts.items())},
             "original_joint_distribution": {f"{source}/{kind}": n for (source, kind), n in sorted(desired.items())},
             "audit_status_original": dict(collections.Counter(audits[r["id"]]["status"] for r in original)),
             "audit_status_extra": dict(collections.Counter(audits[r["id"]]["status"] for r in extra)),
             "manual_exclude": sorted(MANUAL_EXCLUDE),
             "auditor_cost_usd": sum(r.get("cost_usd") or 0 for r in audits.values()),
             "selected_ids": sorted(retained)}
    prefix.with_name(prefix.name + "_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in stats.items() if k != "selected_ids"}, indent=2))


if __name__ == "__main__":
    main()
