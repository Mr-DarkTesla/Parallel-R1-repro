"""Summarize which parts of a Multiverse evaluation were supplied by the branch decoder.

Usage: python audit_branch_rollout.py <run_dir> <out.json>
"""
import json
import sys
from pathlib import Path


def main():
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    report = {}
    for file in sorted(run.glob("*.jsonl")):
        rows = [json.loads(line) for line in file.open()]
        if not rows or "rollout" not in rows[0]:
            continue
        counts = [r["rollout"]["independent_paths"] for r in rows]
        attempted = [r for r in rows if r["rollout"]["path_closed"]]
        report[file.stem] = {
            "responses": len(rows),
            "joined_branch_responses": sum(n > 0 for n in counts),
            "joined_paths": sum(counts),
            "path_close_rate": (sum(sum(x["rollout"]["path_closed"]) for x in attempted) /
                                sum(len(x["rollout"]["path_closed"]) for x in attempted) if attempted else None),
            "decoder_supplies": ["<Path> openers", "</Path> closers after model stop", "path numbers"],
            "model_supplies": ["<Parallel>", "<Goal>", "<Outline>", "path text", "<Conclusion>", "</Parallel>"],
        }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(out)


if __name__ == "__main__":
    main()
