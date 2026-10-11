"""Fail-closed paired fixed-40 comparison for the Deep69 recovery-recipe arm.

The required manifest uses schema version 1 from ``compare_deep69_pair.py``
and must cover both new step archives exactly.  Manual review, not tag syntax,
supplies reviewed external answers and strict-useful blocks.  The optional
``--include-lr10`` reference is admitted only with its complete manifest.
"""

import argparse
import json
import os
from pathlib import Path

from compare_deep69_lr10_pair import (
    BASE_ARCHIVES,
    CANDIDATES as LR10,
    DEEP69_LR100,
    DEEP69_REVIEWS,
    LR10_REVIEWS,
    corrected_c0,
    reviewed_recovery8,
)
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
from compare_masked_pilot_archives import load


OUTPUT = AUDIT / "deep69_recovery_recipe_paired.json"
REVIEWS = AUDIT / "deep69_recovery_recipe_manual_reviews.json"
CANDIDATES = {
    "recovery_recipe_tagged_step4": "deep69_recovery_recipe_tagged_p8_step4_masked_pilot.tgz",
    "recovery_recipe_tagged_step8": "deep69_recovery_recipe_tagged_p8_step8_masked_pilot.tgz",
}
LR10_TAGGED = {"tagged_lr10_step8": LR10["tagged_lr10_step8"]}


def reviewed_with_external(rows, archive, entry):
    """A gate-useful block must also have a reviewed correct external answer."""
    reviewed, metadata = reviewed_rows(rows, archive, entry)
    invalid = [key for key, row in reviewed.items()
               if row["strict_useful"] and not row["acc_robust"]]
    require(not invalid,
            f"{archive}: strict useful blocks require a correct external answer: {invalid}")
    return reviewed, metadata


def paired(reference, candidate, reference_raw, candidate_raw):
    result = {}
    for source in SOURCES:
        keys = [key for key in sorted(candidate) if source == "all" or key[0] == source]
        result[source] = {
            "external_accuracy": ci_compare(reference, candidate, keys, "acc_robust", percent=True),
            "strict_useful_blocks": ci_compare(reference, candidate, keys, "strict_useful", percent=True),
            "response_level_numbered": ci_compare(
                reference_raw, candidate_raw, keys, "think_numbered_block", percent=True),
            "truncation": ci_compare(reference_raw, candidate_raw, keys, "truncated", percent=True),
            "tokens": ci_compare(reference_raw, candidate_raw, keys, "tokens", percent=False),
            "forward_passes": ci_compare(reference_raw, candidate_raw, keys, "forward_passes", percent=False),
        }
    return result


def load_reviewed(archives, entries):
    raw = {label: load(ARCHIVES / archive) for label, archive in archives.items()}
    reviewed, metadata = {}, {}
    for label, archive in archives.items():
        reviewed[label], metadata[label] = reviewed_with_external(raw[label], archive, entries[archive])
    return raw, reviewed, metadata


def main(manifest, output, include_lr10):
    entries = read_manifest(manifest, CANDIDATES.values(), "Deep69 recovery recipe")
    lr100_entries = read_manifest(DEEP69_REVIEWS, DEEP69_ALL.values(), "Deep69 LR100")
    required = [ARCHIVES / name for name in (*CANDIDATES.values(), *DEEP69_LR100.values(),
                                             *BASE_ARCHIVES.values())]
    lr10_entries = None
    if include_lr10:
        lr10_entries = read_manifest(LR10_REVIEWS, LR10.values(), "Deep69 LR10")
        required += [ARCHIVES / name for name in LR10_TAGGED.values()]
    missing = [path.name for path in required if not path.is_file()]
    require(not missing, "missing pilot archives: " + ", ".join(missing))

    c0_raw, c0 = corrected_c0()
    recovery_raw, recovery, recovery_useful = reviewed_recovery8()
    lr100_raw, lr100, lr100_meta = load_reviewed(DEEP69_LR100, lr100_entries)
    candidate_raw, candidates, candidate_meta = load_reviewed(CANDIDATES, entries)

    all_rows = {"corrected_c0": c0, "recovery8_step8": recovery, **lr100, **candidates}
    raw_rows = {"corrected_c0": c0_raw, "recovery8_step8": recovery_raw,
                **lr100_raw, **candidate_raw}
    lr10_meta = None
    if include_lr10:
        lr10_raw, lr10, lr10_meta = load_reviewed(LR10_TAGGED, lr10_entries)
        all_rows.update(lr10)
        raw_rows.update(lr10_raw)
    for label, rows in all_rows.items():
        same_pilot(c0, rows, label)

    references = ("corrected_c0", "recovery8_step8", *DEEP69_LR100)
    if include_lr10:
        references += ("tagged_lr10_step8",)
    output_json = {
        "status": "final_reviewed",
        "protocol": {
            "pilot": "same 40 masked greedy prompts; 20 GSM8K_DEV and 20 MATH_DEV",
            "external_accuracy": "reviewed correct standalone answer after closed </think>",
            "strict_useful": "manifest-reviewed useful block with reviewed correct external answer",
            "ci": "10,000 paired bootstrap samples; binary deltas in percentage points",
        },
        "review_manifests": {
            "recovery_recipe": str(manifest.relative_to(ROOT)),
            "deep69_lr100": str(DEEP69_REVIEWS.relative_to(ROOT)),
            "recovery8": "audit/v4_recovery8_paired.json",
            "c0_corrections": "scripts/exp21/audit_c0_pilot_scoring.py",
            "lr10": str(LR10_REVIEWS.relative_to(ROOT)) if include_lr10 else None,
        },
        "baselines": {
            "corrected_c0": {"archive": BASE_ARCHIVES["corrected_c0"], **source_summary(c0, c0_raw)},
            "recovery8_step8": {
                "archive": BASE_ARCHIVES["recovery8_step8"],
                "strict_useful_ids": list(recovery_useful),
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
    if include_lr10:
        output_json["baselines"]["deep69_lr10"] = {
            label: {"archive": LR10_TAGGED[label], **lr10_meta[label],
                    **source_summary(all_rows[label], raw_rows[label])}
            for label in LR10_TAGGED
        }
    for label, rows in candidates.items():
        output_json["variants"][label] = {
            "archive": CANDIDATES[label], **candidate_meta[label],
            **source_summary(rows, candidate_raw[label]),
            "paired": {
                reference: paired(all_rows[reference], rows, raw_rows[reference], candidate_raw[label])
                for reference in references
            },
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, default=REVIEWS,
                        help="complete manual-review manifest for new recovery-recipe step-4 and step-8 archives")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--include-lr10", action="store_true",
                        help="also compare each new step with reviewed Deep69 LR10 tagged step 8")
    args = parser.parse_args()
    try:
        manifest, output_path = args.reviews.resolve(), args.output.resolve()
        require(manifest.is_relative_to(ROOT.resolve()), "review manifest must be under result root")
        require(output_path.is_relative_to(ROOT.resolve()), "output must be under result root")
        main(manifest, output_path, args.include_lr10)
    except (AssertionError, ValueError, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
