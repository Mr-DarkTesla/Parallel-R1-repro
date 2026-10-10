"""Summarize the eight identical v4 pilots with reviewed answer corrections."""

import json
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import compare, load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
STEPS = (8, 16, 24, 32, 40, 48, 56, 64)
GSM = "GSM8K_DEV"
MATH = "MATH_DEV"
CORRECTIONS = {
    8: [(GSM, name, 0) for name in (
        "gsm8k-train/132", "gsm8k-train/228", "gsm8k-train/288", "gsm8k-train/653"
    )] + [(MATH, name, 0) for name in (
        "math-test/45", "math-test/51", "math-test/65", "math-test/93",
        "math-test/98", "math-test/108"
    )],
    16: [(GSM, "gsm8k-train/279", 0)],
    24: [],
    32: [],
    40: [(MATH, "math-test/36", 0)],
    48: [],
    56: [(GSM, "gsm8k-train/279", 0)],
    64: [],
}
USEFUL = {
    8: [], 16: [], 24: [], 32: [],
    40: ["math-test/9"], 48: ["math-test/9"],
    56: ["math-test/9", "math-test/36"],
    64: ["math-test/9", "math-test/36"],
}


def corrected(rows, keys):
    result = {key: row.copy() for key, row in rows.items()}
    for key in keys:
        assert result[key]["acc_robust"] is False, key
        result[key]["acc_robust"] = True
    return result


def main():
    references = {
        "c0_corrected": corrected(load(ARCHIVES / "c0-greedy-pilot40.tgz"), FIXES),
        "selective_v2": load(ARCHIVES / "selective_v2_masked_pilot.tgz"),
    }
    output = {"protocol": "same 40 masked greedy prompts; semantic answer review", "steps": {}}
    for step in STEPS:
        filename = f"selective_v4_step{step}_masked_pilot.tgz"
        raw = load(ARCHIVES / filename)
        rows = corrected(raw, CORRECTIONS[step])
        assert len(rows) == 40
        keys = sorted(rows)
        for name, base in references.items():
            assert base.keys() == rows.keys(), name
            for key in keys:
                assert base[key]["input"] == rows[key]["input"], (step, key)
                assert base[key]["decoder"] == rows[key]["decoder"] == "masked"
        output["steps"][str(step)] = {
            "archive": filename,
            "manual_corrections": [list(key) for key in CORRECTIONS[step]],
            "robust_correct": sum(row["acc_robust"] for row in raw.values()),
            "manual_correct": sum(row["acc_robust"] for row in rows.values()),
            "numbered_blocks": sum(row["think_numbered_block"] for row in rows.values()),
            "strict_useful_ids": USEFUL[step],
            "outside_think": sum(row["outside_think_tags"] > 0 for row in rows.values()),
            "truncated": sum(row["truncated"] for row in rows.values()),
            "mean_tokens": round(sum(row["tokens"] for row in rows.values()) / 40, 2),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in rows.values()) / 40, 2),
            "paired_accuracy": {name: compare(base, rows, keys, "acc_robust")
                                for name, base in references.items()},
        }
    path = ROOT / "audit/selective_v4_checkpoint_paired.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    for step, row in output["steps"].items():
        print(step, row["manual_correct"], len(row["strict_useful_ids"]),
              row["paired_accuracy"]["c0_corrected"]["delta"])


if __name__ == "__main__":
    main()
