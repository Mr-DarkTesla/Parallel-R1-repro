"""Fail-closed fixed-40 comparison for the conditional Deep69 LR10 pair.

Requires two complete, archived manual-review manifests:

* ``audit/deep69_lr10_pair_manual_reviews.json`` for LR10 tagged/plain;
* ``audit/deep69_pair_manual_reviews.json`` for the same-arm Deep69 LR100
  step-8 reference.

Each manifest uses schema version 1 from ``compare_deep69_pair.py`` and must
contain all and only the archive entries requested below.  A review is not
accepted unless it marks ``review_complete=true``, gives the reviewed external
total, and attaches a local audit evidence file to every override/useful row.
The script only reads archives and manifests; it does not generate outputs.
"""

import argparse
import json
import os
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import load
from compare_deep69_pair import (
    ARCHIVES,
    AUDIT,
    CANDIDATES as DEEP69_ALL,
    ROOT,
    SOURCES,
    ci_compare,
    read_manifest,
    require,
    reviewed_rows,
    same_pilot,
    source_summary,
)


OUTPUT = AUDIT / "deep69_lr10_pair_paired.json"
LR10_REVIEWS = AUDIT / "deep69_lr10_pair_manual_reviews.json"
DEEP69_REVIEWS = AUDIT / "deep69_pair_manual_reviews.json"
RECOVERY_REVIEW = AUDIT / "v4_recovery8_paired.json"

CANDIDATES = {
    "tagged_lr10_step8": "deep69_lr10_tagged_p8_step8_masked_pilot.tgz",
    "plain_lr10_step8": "deep69_lr10_plain_p8_step8_masked_pilot.tgz",
}
DEEP69_LR100 = {
    "deep69_tagged_lr100_step8": "deep69_tagged_p8_step8_masked_pilot.tgz",
    "deep69_plain_lr100_step8": "deep69_plain_p8_step8_masked_pilot.tgz",
}
BASE_ARCHIVES = {
    "corrected_c0": "c0-greedy-pilot40.tgz",
    "recovery8_step8": "v4_recovery8_step8_masked_pilot.tgz",
}


def corrected_c0():
    raw = load(ARCHIVES / BASE_ARCHIVES["corrected_c0"])
    rows = {key: row.copy() for key, row in raw.items()}
    for key in FIXES:
        require(key in rows and not rows[key]["acc_robust"],
                f"C0 correction no longer applies: {key}")
        rows[key]["acc_robust"] = True
    for row in rows.values():
        row["strict_useful"] = False
    require(sum(bool(row["acc_robust"]) for row in rows.values()) == 34,
            "corrected C0 must contain 34 external-correct rows")
    return raw, rows


def reviewed_recovery8():
    raw = load(ARCHIVES / BASE_ARCHIVES["recovery8_step8"])
    require(RECOVERY_REVIEW.is_file(), f"recovery8 review missing: {RECOVERY_REVIEW}")
    report = json.loads(RECOVERY_REVIEW.read_text())
    step8 = report.get("steps", {}).get("8")
    require(isinstance(step8, dict) and step8.get("external_correct") == 29,
            "recovery8 reviewed external count must be 29")
    useful_ids = step8.get("strict_useful_ids")
    require(isinstance(useful_ids, list) and len(useful_ids) == 2,
            "recovery8 reviewed useful ID list must contain two rows")
    rows = {key: row.copy() for key, row in raw.items()}
    for row in rows.values():
        row["strict_useful"] = False
    for problem_id in useful_ids:
        matching = [key for key in rows if key[1] == problem_id]
        require(len(matching) == 1 and bool(rows[matching[0]]["think_numbered_block"]),
                f"invalid recovery8 useful ID: {problem_id}")
        rows[matching[0]]["strict_useful"] = True
    require(sum(bool(row["acc_robust"]) for row in rows.values()) == 29,
            "recovery8 raw score drifted from reviewed total")
    return raw, rows, useful_ids


def compare_to_references(label, rows, raw_rows, all_rows, raw_lookup):
    references = {
        "tagged_lr10_step8": (
            "corrected_c0", "recovery8_step8", "deep69_tagged_lr100_step8", "plain_lr10_step8"
        ),
        "plain_lr10_step8": (
            "corrected_c0", "recovery8_step8", "deep69_plain_lr100_step8", "tagged_lr10_step8"
        ),
    }[label]
    result = {}
    for reference_label in references:
        reference = all_rows[reference_label]
        by_source = {}
        for source in SOURCES:
            keys = [key for key in sorted(rows) if source == "all" or key[0] == source]
            by_source[source] = {
                "external_accuracy": ci_compare(reference, rows, keys, "acc_robust", percent=True),
                "strict_useful_blocks": ci_compare(reference, rows, keys, "strict_useful", percent=True),
                "response_level_numbered": ci_compare(raw_lookup[reference_label], raw_rows, keys,
                                                       "think_numbered_block", percent=True),
                "truncation": ci_compare(raw_lookup[reference_label], raw_rows, keys,
                                          "truncated", percent=True),
                "tokens": ci_compare(raw_lookup[reference_label], raw_rows, keys, "tokens", percent=False),
                "forward_passes": ci_compare(raw_lookup[reference_label], raw_rows, keys,
                                             "forward_passes", percent=False),
            }
        result[reference_label] = by_source
    return result


def main(lr10_manifest, output):
    lr10_entries = read_manifest(lr10_manifest, CANDIDATES.values(), "Deep69 LR10")
    # The Deep69 source manifest covers both steps 4 and 8; this comparison
    # reads its complete reviewed manifest and selects the step-8 entries.
    lr100_entries = read_manifest(DEEP69_REVIEWS, DEEP69_ALL.values(), "Deep69 LR100")
    required = [ARCHIVES / name for name in (*CANDIDATES.values(), *DEEP69_LR100.values(),
                                             *BASE_ARCHIVES.values())]
    missing = [path.name for path in required if not path.is_file()]
    require(not missing, "missing pilot archives: " + ", ".join(missing))

    c0_raw, c0 = corrected_c0()
    recovery_raw, recovery, recovery_useful = reviewed_recovery8()
    lr100_raw = {label: load(ARCHIVES / name) for label, name in DEEP69_LR100.items()}
    lr100, lr100_meta = {}, {}
    for label, archive in DEEP69_LR100.items():
        lr100[label], lr100_meta[label] = reviewed_rows(lr100_raw[label], archive, lr100_entries[archive])
    candidate_raw = {label: load(ARCHIVES / name) for label, name in CANDIDATES.items()}
    candidates, candidate_meta = {}, {}
    for label, archive in CANDIDATES.items():
        candidates[label], candidate_meta[label] = reviewed_rows(candidate_raw[label], archive, lr10_entries[archive])

    anchor = c0
    all_rows = {"corrected_c0": c0, "recovery8_step8": recovery, **lr100, **candidates}
    raw_lookup = {"corrected_c0": c0_raw, "recovery8_step8": recovery_raw, **lr100_raw, **candidate_raw}
    for label, rows in all_rows.items():
        same_pilot(anchor, rows, label)

    output_json = {
        "status": "final_reviewed",
        "protocol": {
            "pilot": "same 40 masked greedy prompts; 20 GSM8K_DEV and 20 MATH_DEV",
            "external_accuracy": "reviewed correct standalone answer after closed </think>",
            "strict_useful": "reviewed independent substantive paths with correct combination",
            "ci": "10,000 paired bootstrap samples; binary deltas in percentage points",
        },
        "review_manifests": {
            "lr10": str(lr10_manifest.relative_to(ROOT)),
            "deep69_lr100": str(DEEP69_REVIEWS.relative_to(ROOT)),
            "recovery8": str(RECOVERY_REVIEW.relative_to(ROOT)),
            "c0_corrections": "scripts/exp21/audit_c0_pilot_scoring.py",
        },
        "baselines": {
            "corrected_c0": {"archive": BASE_ARCHIVES["corrected_c0"], **source_summary(c0, c0_raw)},
            "recovery8_step8": {
                "archive": BASE_ARCHIVES["recovery8_step8"], "strict_useful_ids": useful_ids_to_list(recovery_useful),
                **source_summary(recovery, recovery_raw),
            },
            "deep69_lr100": {
                label: {"archive": DEEP69_LR100[label], **lr100_meta[label],
                        **source_summary(lr100[label], lr100_raw[label])}
                for label in DEEP69_LR100
            },
        },
        "variants": {},
    }
    for label, rows in candidates.items():
        output_json["variants"][label] = {
            "archive": CANDIDATES[label], **candidate_meta[label],
            **source_summary(rows, candidate_raw[label]),
            "paired": compare_to_references(label, rows, candidate_raw[label], all_rows, raw_lookup),
        }

    temporary = output.with_suffix(output.suffix + ".tmp")
    try:
        temporary.write_text(json.dumps(output_json, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    for label, item in output_json["variants"].items():
        print(label, item["all"]["external_correct"], item["all"]["strict_useful"],
              item["GSM8K_DEV"]["external_correct"], item["GSM8K_DEV"]["strict_useful"],
              item["MATH_DEV"]["external_correct"], item["MATH_DEV"]["strict_useful"])


def useful_ids_to_list(values):
    """Keep the static reviewed recovery IDs visibly distinct from a manifest."""
    return list(values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, default=LR10_REVIEWS,
                        help="complete archived manual-review manifest for the two LR10 archives")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        reviews, output_path = args.reviews.resolve(), args.output.resolve()
        require(reviews.is_relative_to(ROOT.resolve()), "LR10 review manifest must be under result root")
        require(output_path.is_relative_to(ROOT.resolve()), "output must be under result root")
        main(reviews, output_path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
