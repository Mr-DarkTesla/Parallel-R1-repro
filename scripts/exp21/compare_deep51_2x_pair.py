"""Paired fixed-40 comparison for the Deep51 2x tagged/plain experiment.

By default the script may write a clearly marked preliminary result using raw
``acc_robust`` and null useful IDs.  ``--final`` requires evidence-backed
manual reviews for every 2x archive and reviewed Deep51-1x comparison data.
"""

import argparse
import json
import os
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_deep51_pair import (
    ComparisonError, apply_review, require, verify_same_pilot,
)
from compare_masked_pilot_archives import compare, load
from compare_v4_recovery8 import corrected


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
OUTPUT = AUDIT / "deep51_2x_pair_paired.json"
ONE_X_AUDIT = AUDIT / "deep51_pair_paired.json"
TWO_X = {
    "tagged_step4": "deep51_2x_tagged_p8_step4_masked_pilot.tgz",
    "tagged_step8": "deep51_2x_tagged_p8_step8_masked_pilot.tgz",
    "plain_step4": "deep51_2x_plain_p8_step4_masked_pilot.tgz",
    "plain_step8": "deep51_2x_plain_p8_step8_masked_pilot.tgz",
}
ONE_X = {
    "tagged_step4": "deep51_tagged_p8_step4_masked_pilot.tgz",
    "tagged_step8": "deep51_tagged_p8_step8_masked_pilot.tgz",
    "plain_step4": "deep51_plain_p8_step4_masked_pilot.tgz",
    "plain_step8": "deep51_plain_p8_step8_masked_pilot.tgz",
}
BASELINES = {
    "corrected_c0": "c0-greedy-pilot40.tgz",
    "recovery8_step8": "v4_recovery8_step8_masked_pilot.tgz",
}
METRICS = {
    "external_accuracy": "acc_robust",
    "response_level_numbered": "think_numbered_block",
    "truncation": "truncated",
    "tokens": "tokens",
    "forward_passes": "forward_passes",
}


def read_reviews(path):
    if path is None:
        return {}
    require(path.is_file(), f"review manifest missing: {path}")
    data = json.loads(path.read_text())
    require(data.get("schema_version") == 1, "review schema_version must be 1")
    archives = data.get("archives")
    require(isinstance(archives, dict), "review manifest must contain object archives")
    unknown = sorted(set(archives) - set(TWO_X.values()))
    require(not unknown, "review manifest contains unknown archives: " + ", ".join(unknown))
    return archives


def reviewed_one_x(raw_rows):
    if not ONE_X_AUDIT.is_file():
        summary = {
            label: {
                "manual_review_complete": False,
                "external_accuracy_source": "archive_acc_robust_unreviewed",
                "external_overrides": [],
                "strict_useful_ids": None,
            }
            for label in ONE_X
        }
        return raw_rows, summary, False
    report = json.loads(ONE_X_AUDIT.read_text())
    manifest_value = report.get("review_manifest")
    require(isinstance(manifest_value, str) and manifest_value,
            "deep51_pair_paired.json has no review_manifest")
    manifest_path = Path(manifest_value)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest_path = manifest_path.resolve()
    require(manifest_path.is_relative_to(ROOT.resolve()) and manifest_path.is_file(),
            "Deep51-1x review manifest is missing or outside the result directory")
    manifest = json.loads(manifest_path.read_text())
    require(manifest.get("schema_version") == 1,
            "Deep51-1x review manifest schema_version must be 1")
    reviews = manifest.get("archives")
    require(isinstance(reviews, dict),
            "Deep51-1x review manifest must contain object archives")
    variants = report.get("variants", {})
    require(isinstance(variants, dict), "deep51_pair_paired.json has no variants object")
    corrected_rows, summary, complete = {}, {}, True
    for label, filename in ONE_X.items():
        entry = variants.get(label)
        review = reviews.get(filename)
        if (not isinstance(entry, dict) or entry.get("manual_review_complete") is not True
                or not isinstance(review, dict) or review.get("review_complete") is not True):
            corrected_rows[label], complete = raw_rows[label], False
            summary[label] = {
                "manual_review_complete": False,
                "external_accuracy_source": "archive_acc_robust_unreviewed",
                "external_overrides": [],
                "strict_useful_ids": None,
            }
            continue
        require(entry.get("archive") == filename, f"1x audit archive mismatch for {label}")
        rows, useful_ids, overrides, accuracy_source = apply_review(
            raw_rows[label], filename, review)
        require(sum(row["acc_robust"] for row in rows.values()) == entry.get("external_correct"),
                f"1x reviewed external count mismatch for {label}")
        require(overrides == entry.get("external_overrides"),
                f"1x reviewed external corrections differ for {label}")
        require(useful_ids == entry.get("strict_useful_ids"),
                f"1x strict useful IDs differ for {label}")
        corrected_rows[label] = rows
        summary[label] = {
            "manual_review_complete": True,
            "external_accuracy_source": accuracy_source,
            "external_overrides": overrides,
            "strict_useful_ids": useful_ids,
        }
    return corrected_rows, summary, complete


def comparison_references(label, baselines, one_x_rows, two_x_rows):
    step = "step4" if label.endswith("step4") else "step8"
    style = "tagged" if label.startswith("tagged_") else "plain"
    other = ("plain_" if label.startswith("tagged_") else "tagged_") + step
    return {
        **baselines,
        f"deep51_1x_{style}_{step}": one_x_rows[f"{style}_{step}"],
        f"deep51_2x_{other}": two_x_rows[other],
    }


def main(reviews_path, output_path, final):
    required = [ARCHIVES / name for name in (
        *TWO_X.values(), *ONE_X.values(), *BASELINES.values())]
    missing = [path.name for path in required if not path.is_file()]
    require(not missing, "missing pilot archives: " + ", ".join(missing))
    reviews = read_reviews(reviews_path)
    if final:
        missing_reviews = [filename for filename in TWO_X.values()
                           if not isinstance(reviews.get(filename), dict)
                           or reviews[filename].get("review_complete") is not True]
        require(not missing_reviews,
                "final comparison requires completed 2x reviews: " + ", ".join(missing_reviews))

    c0 = corrected(load(ARCHIVES / BASELINES["corrected_c0"]), FIXES)
    recovery = load(ARCHIVES / BASELINES["recovery8_step8"])
    require(len(c0) == 40 and len(recovery) == 40,
            "C0 and recovery8 baselines must each contain 40 rows")
    require(sum(row["acc_robust"] for row in c0.values()) == 34,
            "corrected C0 must contain 34 external-correct rows")
    require(sum(row["acc_robust"] for row in recovery.values()) == 29,
            "reviewed recovery8 step8 must contain 29 external-correct rows")
    baselines = {"corrected_c0": c0, "recovery8_step8": recovery}

    raw_one_x = {label: load(ARCHIVES / filename) for label, filename in ONE_X.items()}
    one_x, one_x_review, one_x_complete = reviewed_one_x(raw_one_x)
    require(not final or one_x_complete,
            "final comparison requires manual_review_complete=true for all variants in deep51_pair_paired.json")

    raw_two_x = {label: load(ARCHIVES / filename) for label, filename in TWO_X.items()}
    two_x, review_summary = {}, {}
    for label, filename in TWO_X.items():
        rows = raw_two_x[label]
        require(len(rows) == 40, f"{filename}: expected 40 rows, got {len(rows)}")
        reviewed, useful_ids, overrides, accuracy_source = apply_review(
            rows, filename, reviews.get(filename))
        two_x[label] = reviewed
        review_summary[label] = {
            "manual_review_complete": useful_ids is not None,
            "external_accuracy_source": accuracy_source,
            "external_overrides": overrides,
            "strict_useful_ids": useful_ids,
        }

    anchor = c0
    for label, rows in {**baselines, **one_x, **two_x}.items():
        verify_same_pilot(anchor, rows, "corrected_c0", label)

    output = {
        "status": "final_reviewed" if final else "preliminary",
        "protocol": {
            "pilot": "same 40 masked greedy prompts",
            "unreviewed_external_accuracy": "archive acc_robust",
            "final_requirement": "manual reviews for all 2x and all 1x variants",
            "paired_ci": "10,000 paired bootstrap samples from compare_masked_pilot_archives.py",
        },
        "review_manifest": str(reviews_path) if reviews_path else None,
        "baselines": {
            "corrected_c0": {"archive": BASELINES["corrected_c0"], "external_correct": 34,
                             "external_corrections": [list(key) for key in FIXES]},
            "recovery8_step8": {"archive": BASELINES["recovery8_step8"],
                               "external_correct": 29, "external_corrections": []},
        },
        "deep51_1x": {
            label: {"archive": ONE_X[label],
                    **one_x_review[label],
                    "external_correct": sum(row["acc_robust"] for row in one_x[label].values()),
                    "source_audit": "audit/deep51_pair_paired.json"}
            for label in ONE_X
        },
        "variants": {},
    }
    for label, rows in two_x.items():
        raw = raw_two_x[label]
        keys = sorted(rows)
        references = comparison_references(label, baselines, one_x, two_x)
        output["variants"][label] = {
            "archive": TWO_X[label],
            **review_summary[label],
            "external_correct": sum(row["acc_robust"] for row in rows.values()),
            "response_level_numbered": sum(row["think_numbered_block"] for row in raw.values()),
            "truncated": sum(row["truncated"] for row in raw.values()),
            "outside_think": sum(row["outside_think_tags"] > 0 for row in raw.values()),
            "mean_tokens": round(sum(row["tokens"] for row in raw.values()) / 40, 2),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in raw.values()) / 40, 2),
            "paired": {
                output_name: {
                    reference_name: compare(reference, rows if metric == "acc_robust" else raw,
                                            keys, metric)
                    for reference_name, reference in references.items()
                }
                for output_name, metric in METRICS.items()
            },
        }

    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)
    for label, row in output["variants"].items():
        print(label, row["external_correct"], row["response_level_numbered"],
              row["strict_useful_ids"], row["truncated"], row["external_accuracy_source"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    try:
        main(args.reviews.resolve() if args.reviews else None, args.output.resolve(), args.final)
    except (ComparisonError, FileNotFoundError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
