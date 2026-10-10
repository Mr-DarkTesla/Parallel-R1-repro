"""Compare selective v2 with the fixed 40-question masked pilot archives.

Usage: python scripts/exp21/compare_selective_v2_pilot.py
"""

import json
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import compare, load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
CANDIDATE = "selective_v2_masked_pilot.tgz"
REFERENCES = {
    "c0_corrected": "c0-greedy-pilot40.tgz",
    "selective_v1": "selective_blocks_masked_pilot.tgz",
    "m1_text1": "text1_masked_pilot.tgz",
    "m1_tagweighted": "m1-tagweighted-greedy-pilot40.tgz",
}
METRICS = ("acc_robust", "think_numbered_block", "truncated", "tokens", "forward_passes")


def main():
    candidate = load(ARCHIVES / CANDIDATE)
    assert len(candidate) == 40
    summary = {"archive": CANDIDATE, "by_source": {}}
    for source in ("all", *sorted({key[0] for key in candidate})):
        keys = [key for key in sorted(candidate) if source == "all" or key[0] == source]
        summary["by_source"][source] = {
            "n": len(keys),
            "correct": sum(candidate[key]["acc_robust"] for key in keys),
            "numbered_block": sum(candidate[key]["think_numbered_block"] for key in keys),
            "correct_and_block": sum(candidate[key]["acc_robust"] and candidate[key]["think_numbered_block"] for key in keys),
            "truncated": sum(candidate[key]["truncated"] for key in keys),
            "mean_tokens": round(sum(candidate[key]["tokens"] for key in keys) / len(keys), 2),
            "mean_forward_passes": round(sum(candidate[key]["forward_passes"] for key in keys) / len(keys), 2),
        }
    AUDIT.mkdir(exist_ok=True)
    (AUDIT / "selective_v2_pilot40_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    for label, filename in REFERENCES.items():
        base = load(ARCHIVES / filename)
        assert base.keys() == candidate.keys(), label
        for key in base:
            assert base[key]["input"] == candidate[key]["input"], (label, key)
            assert base[key]["decoder"] == candidate[key]["decoder"] == "masked", (label, key)
        if label == "c0_corrected":
            base = {key: row.copy() for key, row in base.items()}
            for key in FIXES:
                assert base[key]["acc_robust"] is False
                base[key]["acc_robust"] = True
        result = {"base_archive": filename, "candidate_archive": CANDIDATE,
                  "base_manual_corrections": [list(key) for key in FIXES] if label == "c0_corrected" else []}
        for source in summary["by_source"]:
            keys = [key for key in sorted(base) if source == "all" or key[0] == source]
            result[source] = {metric: compare(base, candidate, keys, metric) for metric in METRICS}
        (AUDIT / f"selective_v2_vs_{label}_pilot40.json").write_text(json.dumps(result, indent=2) + "\n")
        print(label, json.dumps(result["all"], ensure_ascii=False))
    print("summary", json.dumps(summary["by_source"], ensure_ascii=False))


if __name__ == "__main__":
    main()
