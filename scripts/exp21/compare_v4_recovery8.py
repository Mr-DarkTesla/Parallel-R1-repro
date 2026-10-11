"""Paired fixed-40 comparison of v4 recovery8 steps 4 and 8."""

import json
import os
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import compare, load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
OUTPUT = AUDIT / "v4_recovery8_paired.json"
STEPS = (4, 8)
EXPECTED = {
    4: {"external": 27, "numbered": 14, "truncated": 4,
        "useful": ["math-test/9"]},
    8: {"external": 29, "numbered": 12, "truncated": 2,
        "useful": ["math-test/9", "math-test/36"]},
}
REVIEW_FILES = {
    4: AUDIT / "v4_recovery8_step4_answer_review.md",
    8: AUDIT / "v4_recovery8_step8_answer_review.md",
}
V4_STEP56_FIXES = (("GSM8K_DEV", "gsm8k-train/279", 0),)
REFERENCE_FILES = {
    "c0_corrected": "c0-greedy-pilot40.tgz",
    "v4_step56": "selective_v4_step56_masked_pilot.tgz",
    "selective_v2": "selective_v2_masked_pilot.tgz",
}


def corrected(rows, keys):
    result = {key: row.copy() for key, row in rows.items()}
    for key in keys:
        assert key in result, key
        assert result[key]["acc_robust"] is False, key
        result[key]["acc_robust"] = True
    return result


def verify_same_pilot(reference, candidate, label, step):
    assert reference.keys() == candidate.keys(), (step, label, "different rows")
    for key in sorted(candidate):
        assert reference[key]["input"] == candidate[key]["input"], (step, label, key)
        assert reference[key]["decoder"] == candidate[key]["decoder"] == "masked", (step, label, key)


def main():
    required = [ARCHIVES / name for name in REFERENCE_FILES.values()]
    required += [ARCHIVES / f"v4_recovery8_step{step}_masked_pilot.tgz" for step in STEPS]
    required += list(REVIEW_FILES.values())
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    assert not missing, "missing evidence: " + ", ".join(missing)

    c0_raw = load(ARCHIVES / REFERENCE_FILES["c0_corrected"])
    v4_raw = load(ARCHIVES / REFERENCE_FILES["v4_step56"])
    v2_raw = load(ARCHIVES / REFERENCE_FILES["selective_v2"])
    references = {
        "c0_corrected": corrected(c0_raw, FIXES),
        "v4_step56": corrected(v4_raw, V4_STEP56_FIXES),
        "selective_v2": v2_raw,
    }
    assert {name: sum(row["acc_robust"] for row in rows.values())
            for name, rows in references.items()} == {
                "c0_corrected": 34, "v4_step56": 27, "selective_v2": 30}

    output = {
        "protocol": {
            "pilot": "same 40 masked greedy prompts",
            "accuracy": "reviewed correct external answer after closed </think>",
            "ci": "10,000 paired bootstrap samples from compare_masked_pilot_archives.py",
        },
        "references": {
            "c0_corrected": {"archive": REFERENCE_FILES["c0_corrected"],
                             "external_corrections": [list(key) for key in FIXES],
                             "external_correct": 34},
            "v4_step56": {"archive": REFERENCE_FILES["v4_step56"],
                          "external_corrections": [list(key) for key in V4_STEP56_FIXES],
                          "external_correct": 27},
            "selective_v2": {"archive": REFERENCE_FILES["selective_v2"],
                             "external_corrections": [], "external_correct": 30},
        },
        "steps": {},
    }
    metrics = ("acc_robust", "think_numbered_block", "truncated", "tokens", "forward_passes")
    metric_names = {
        "acc_robust": "external_accuracy",
        "think_numbered_block": "response_level_numbered",
        "truncated": "truncation",
        "tokens": "tokens",
        "forward_passes": "forward_passes",
    }
    for step in STEPS:
        filename = f"v4_recovery8_step{step}_masked_pilot.tgz"
        review = REVIEW_FILES[step]
        assert filename in review.read_text(), (step, review)
        rows = load(ARCHIVES / filename)
        assert len(rows) == 40
        for label, reference in references.items():
            verify_same_pilot(reference, rows, label, step)
        expected = EXPECTED[step]
        external = sum(row["acc_robust"] for row in rows.values())
        numbered = sum(row["think_numbered_block"] for row in rows.values())
        truncated = sum(row["truncated"] for row in rows.values())
        assert (external, numbered, truncated) == (
            expected["external"], expected["numbered"], expected["truncated"])
        keys = sorted(rows)
        paired = {
            metric_names[metric]: {
                label: compare(reference, rows, keys, metric)
                for label, reference in references.items()
            }
            for metric in metrics
        }
        output["steps"][str(step)] = {
            "archive": filename,
            "review_file": str(review.relative_to(ROOT)),
            "external_correct": external,
            "response_level_numbered": numbered,
            "strict_useful_ids": expected["useful"],
            "truncated": truncated,
            "outside_think": sum(row["outside_think_tags"] > 0 for row in rows.values()),
            "mean_tokens": round(sum(row["tokens"] for row in rows.values()) / 40, 2),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in rows.values()) / 40, 2),
            "paired": paired,
        }

    temporary = OUTPUT.with_suffix(".tmp.json")
    try:
        temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, OUTPUT)
    finally:
        temporary.unlink(missing_ok=True)
    for step, row in output["steps"].items():
        print(step, row["external_correct"], row["response_level_numbered"],
              len(row["strict_useful_ids"]), row["truncated"],
              row["paired"]["external_accuracy"]["c0_corrected"])


if __name__ == "__main__":
    main()
