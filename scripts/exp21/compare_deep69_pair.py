"""Fail-closed paired comparison for Deep69 tagged/plain fixed-40 pilots.

Expected archives are the four masked greedy pilots named in ``CANDIDATES``.
The command requires a completed Deep69 review manifest and the already
completed Deep51-1x manifest.  It never infers useful blocks from syntax:
``strict_useful`` is populated only from a reviewed manifest.

Deep69 manifest schema (all four archive names are required)::

  {"schema_version": 1, "archives": {
    "deep69_tagged_p8_step4_masked_pilot.tgz": {
      "review_complete": true,
      "expected_external_correct": 0,
      "external_overrides": [
        {"key": ["GSM8K_DEV", "gsm8k-train/1", 0], "value": true,
         "evidence_file": "audit/review.md", "evidence_note": "..."}
      ],
      "strict_useful": [
        {"key": ["MATH_DEV", "math-test/1", 0],
         "evidence_file": "audit/review.md", "evidence_note": "..."}
      ]
    }
  }}

``review_complete`` means that every response containing a candidate block was
reviewed.  The script refuses a partial, unknown, or unsubstantiated manifest.
Output contains global, GSM8K and MATH counts plus paired bootstrap CIs against
C0, recovery8, the matching Deep51-1x arm, and the same-step matched arm.
"""

import argparse
import json
import os
from pathlib import Path

import numpy as np

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
OUTPUT = AUDIT / "deep69_pair_paired.json"
DEEP69_REVIEWS = AUDIT / "deep69_pair_manual_reviews.json"
DEEP51_REVIEWS = AUDIT / "deep51_pair_manual_reviews.json"
RECOVERY_REVIEW = AUDIT / "v4_recovery8_paired.json"

CANDIDATES = {
    "tagged_step4": "deep69_tagged_p8_step4_masked_pilot.tgz",
    "tagged_step8": "deep69_tagged_p8_step8_masked_pilot.tgz",
    "plain_step4": "deep69_plain_p8_step4_masked_pilot.tgz",
    "plain_step8": "deep69_plain_p8_step8_masked_pilot.tgz",
}
DEEP51 = {
    "deep51_tagged_step4": "deep51_tagged_p8_step4_masked_pilot.tgz",
    "deep51_tagged_step8": "deep51_tagged_p8_step8_masked_pilot.tgz",
    "deep51_plain_step4": "deep51_plain_p8_step4_masked_pilot.tgz",
    "deep51_plain_step8": "deep51_plain_p8_step8_masked_pilot.tgz",
}
BASE_ARCHIVES = {
    "corrected_c0": "c0-greedy-pilot40.tgz",
    "recovery8_step8": "v4_recovery8_step8_masked_pilot.tgz",
}
SOURCES = ("all", "GSM8K_DEV", "MATH_DEV")
BOOTSTRAP_INDICES = {}


class ComparisonError(ValueError):
    """Input evidence is incomplete, mismatched, or internally inconsistent."""


def require(condition, message):
    if not condition:
        raise ComparisonError(message)


def parse_key(value, context):
    require(isinstance(value, list) and len(value) == 3,
            f"{context}: key must be [source, problem_id, sample]")
    source, problem_id, sample = value
    require(source in SOURCES[1:], f"{context}: invalid source")
    require(isinstance(problem_id, str) and problem_id, f"{context}: invalid problem_id")
    require(isinstance(sample, int), f"{context}: sample must be integer")
    return source, problem_id, sample


def evidence_path(item, context):
    relative = item.get("evidence_file")
    require(isinstance(relative, str) and relative.startswith("audit/"),
            f"{context}: evidence_file must be below audit/")
    path = (ROOT / relative).resolve()
    require(path.is_relative_to(ROOT.resolve()) and path.is_file(),
            f"{context}: missing evidence_file {relative!r}")
    note = item.get("evidence_note")
    require(isinstance(note, str) and note.strip(), f"{context}: evidence_note is required")
    return relative


def read_manifest(path, expected_archives, label):
    require(path.is_file(), f"{label} review manifest missing: {path}")
    data = json.loads(path.read_text())
    require(data.get("schema_version") == 1, f"{label}: schema_version must be 1")
    entries = data.get("archives")
    require(isinstance(entries, dict), f"{label}: archives must be object")
    require(set(entries) == set(expected_archives),
            f"{label}: archive names differ; expected all and only {sorted(expected_archives)}")
    return entries


def reviewed_rows(raw_rows, archive_name, entry):
    """Apply reviewed answer overrides and add a manifest-only useful label."""
    require(isinstance(entry, dict) and entry.get("review_complete") is True,
            f"{archive_name}: review_complete=true required")
    rows = {key: row.copy() for key, row in raw_rows.items()}
    for row in rows.values():
        row["strict_useful"] = False
    overrides = entry.get("external_overrides")
    require(isinstance(overrides, list), f"{archive_name}: external_overrides must be list")
    seen = set()
    serialized_overrides = []
    for index, item in enumerate(overrides):
        context = f"{archive_name}: external override {index}"
        require(isinstance(item, dict), f"{context}: must be object")
        key = parse_key(item.get("key"), context)
        require(key in rows and key not in seen, f"{context}: missing or duplicate row")
        require(type(item.get("value")) is bool and item["value"] != bool(rows[key]["acc_robust"]),
                f"{context}: value must change raw acc_robust")
        relative = evidence_path(item, context)
        rows[key]["acc_robust"] = item["value"]
        seen.add(key)
        serialized_overrides.append({
            "key": list(key), "value": item["value"], "evidence_file": relative,
            "evidence_note": item["evidence_note"],
        })
    expected = entry.get("expected_external_correct")
    require(type(expected) is int and expected == sum(bool(row["acc_robust"]) for row in rows.values()),
            f"{archive_name}: expected_external_correct disagrees with reviewed rows")

    useful = entry.get("strict_useful")
    require(isinstance(useful, list), f"{archive_name}: strict_useful must be list")
    useful_ids, useful_seen, serialized_useful = [], set(), []
    for index, item in enumerate(useful):
        context = f"{archive_name}: strict useful {index}"
        require(isinstance(item, dict), f"{context}: must be object")
        key = parse_key(item.get("key"), context)
        require(key in rows and key not in useful_seen, f"{context}: missing or duplicate row")
        require(bool(raw_rows[key]["think_numbered_block"]),
                f"{context}: strict useful row lacks a complete numbered block")
        relative = evidence_path(item, context)
        rows[key]["strict_useful"] = True
        useful_seen.add(key)
        useful_ids.append(key[1])
        serialized_useful.append({
            "key": list(key), "evidence_file": relative, "evidence_note": item["evidence_note"],
        })
    return rows, {
        "external_correct": expected,
        "external_overrides": serialized_overrides,
        "strict_useful_ids": useful_ids,
        "strict_useful_evidence": serialized_useful,
        "manual_review_complete": True,
    }


def same_pilot(anchor, rows, label):
    require(anchor.keys() == rows.keys(), f"{label}: pilot keys differ")
    require(len(rows) == 40, f"{label}: expected 40 rows, got {len(rows)}")
    for key in sorted(rows):
        require(anchor[key]["input"] == rows[key]["input"], f"{label}: different input at {key}")
        require(anchor[key]["decoder"] == rows[key]["decoder"] == "masked",
                f"{label}: non-masked or mismatched decoder at {key}")


def ci_compare(base, candidate, keys, metric, percent):
    deltas = np.asarray([float(candidate[key][metric]) - float(base[key][metric]) for key in keys])
    require(len(deltas), "cannot compare empty domain")
    n = len(deltas)
    if n not in BOOTSTRAP_INDICES:
        BOOTSTRAP_INDICES[n] = np.random.default_rng(0).integers(0, n, size=(10_000, n))
    bootstrap = np.sort(deltas[BOOTSTRAP_INDICES[n]].mean(axis=1))
    scale = 100 if percent else 1
    return {
        "base": round(scale * np.mean([float(base[key][metric]) for key in keys]), 2),
        "candidate": round(scale * np.mean([float(candidate[key][metric]) for key in keys]), 2),
        "delta": round(scale * deltas.mean(), 2),
        "ci95": [round(scale * bootstrap[index], 2) for index in (249, 9749)],
        "n": n,
    }


def source_summary(rows, raw_rows):
    summary = {}
    for source in SOURCES:
        keys = [key for key in sorted(rows) if source == "all" or key[0] == source]
        require(len(keys) == (40 if source == "all" else 20), f"unexpected {source} row count")
        summary[source] = {
            "n": len(keys),
            "external_correct": sum(bool(rows[key]["acc_robust"]) for key in keys),
            "strict_useful": sum(bool(rows[key]["strict_useful"]) for key in keys),
            "response_level_numbered": sum(bool(raw_rows[key]["think_numbered_block"]) for key in keys),
            "truncated": sum(bool(raw_rows[key]["truncated"]) for key in keys),
        }
    return summary


def references_for(label):
    arm, step = label.split("_")
    pair = f"plain_{step}" if arm == "tagged" else f"tagged_{step}"
    return ("corrected_c0", "recovery8_step8", f"deep51_{arm}_{step}", pair)


def main(deep69_reviews, output_path):
    deep69_entries = read_manifest(deep69_reviews, CANDIDATES.values(), "Deep69")
    deep51_entries = read_manifest(DEEP51_REVIEWS, DEEP51.values(), "Deep51-1x")
    required_archives = [ARCHIVES / name for name in (*CANDIDATES.values(), *DEEP51.values(), *BASE_ARCHIVES.values())]
    missing = [path.name for path in required_archives if not path.is_file()]
    require(not missing, "missing pilot archives: " + ", ".join(missing))
    require(RECOVERY_REVIEW.is_file(), f"recovery8 reviewed comparison missing: {RECOVERY_REVIEW}")

    c0_raw = load(ARCHIVES / BASE_ARCHIVES["corrected_c0"])
    c0_entry = {
        "review_complete": True,
        "expected_external_correct": 34,
        "external_overrides": [
            {"key": list(key), "value": True, "evidence_file": "audit_c0_pilot_scoring.py",
             "evidence_note": final}
            for key, (_, final) in FIXES.items()
        ],
        "strict_useful": [],
    }
    # C0's audit evidence is a script under scripts/, not a review file; apply
    # the two reviewed false-negative fixes explicitly after checking raw rows.
    c0 = {key: row.copy() for key, row in c0_raw.items()}
    for key in FIXES:
        require(key in c0 and not c0[key]["acc_robust"], f"C0 correction no longer applies: {key}")
        c0[key]["acc_robust"] = True
    for row in c0.values():
        row["strict_useful"] = False
    require(sum(bool(row["acc_robust"]) for row in c0.values()) == 34,
            "corrected C0 must have 34 external-correct rows")

    recovery_raw = load(ARCHIVES / BASE_ARCHIVES["recovery8_step8"])
    recovery_doc = json.loads(RECOVERY_REVIEW.read_text())
    step8 = recovery_doc.get("steps", {}).get("8")
    require(isinstance(step8, dict) and step8.get("external_correct") == 29,
            "recovery8 reviewed step8 external count must be 29")
    useful_ids = step8.get("strict_useful_ids")
    require(isinstance(useful_ids, list) and len(useful_ids) == 2,
            "recovery8 reviewed step8 useful IDs must contain two rows")
    recovery = {key: row.copy() for key, row in recovery_raw.items()}
    for row in recovery.values():
        row["strict_useful"] = False
    for problem_id in useful_ids:
        matches = [key for key in recovery if key[1] == problem_id]
        require(len(matches) == 1 and recovery[matches[0]]["think_numbered_block"],
                f"recovery8 useful ID invalid: {problem_id}")
        recovery[matches[0]]["strict_useful"] = True
    require(sum(bool(row["acc_robust"]) for row in recovery.values()) == 29,
            "recovery8 raw/manual external count drifted")

    deep51_raw = {label: load(ARCHIVES / filename) for label, filename in DEEP51.items()}
    deep51 = {}
    deep51_meta = {}
    for label, filename in DEEP51.items():
        deep51[label], deep51_meta[label] = reviewed_rows(deep51_raw[label], filename, deep51_entries[filename])
    candidate_raw = {label: load(ARCHIVES / filename) for label, filename in CANDIDATES.items()}
    candidates = {}
    candidate_meta = {}
    for label, filename in CANDIDATES.items():
        candidates[label], candidate_meta[label] = reviewed_rows(candidate_raw[label], filename, deep69_entries[filename])

    anchor = c0
    for label, rows in {"corrected_c0": c0, "recovery8_step8": recovery, **deep51, **candidates}.items():
        same_pilot(anchor, rows, label)

    all_rows = {"corrected_c0": c0, "recovery8_step8": recovery, **deep51, **candidates}
    raw_lookup = {"corrected_c0": c0_raw, "recovery8_step8": recovery_raw, **deep51_raw, **candidate_raw}
    output = {
        "protocol": {
            "pilot": "same 40 masked greedy prompts; 20 GSM8K_DEV and 20 MATH_DEV",
            "manual_external_accuracy": "correct standalone answer after closed </think>, from complete manifest",
            "strict_useful": "manifest-reviewed independent substantive paths and correct combination",
            "ci": "10,000 paired bootstrap samples; deltas in percentage points for binary metrics",
        },
        "review_manifests": {
            "deep69": str(deep69_reviews.relative_to(ROOT)),
            "deep51_1x": str(DEEP51_REVIEWS.relative_to(ROOT)),
            "recovery8": str(RECOVERY_REVIEW.relative_to(ROOT)),
            "c0_corrections": "scripts/exp21/audit_c0_pilot_scoring.py",
        },
        "baselines": {
            "corrected_c0": {"archive": BASE_ARCHIVES["corrected_c0"], **source_summary(c0, c0_raw)},
            "recovery8_step8": {"archive": BASE_ARCHIVES["recovery8_step8"], **source_summary(recovery, recovery_raw)},
            "deep51_1x": {label: {"archive": DEEP51[label], **deep51_meta[label],
                                     **source_summary(deep51[label], deep51_raw[label])}
                           for label in DEEP51},
        },
        "variants": {},
    }
    for label, rows in candidates.items():
        comparisons = {}
        for reference_label in references_for(label):
            reference = all_rows[reference_label]
            by_source = {}
            for source in SOURCES:
                keys = [key for key in sorted(rows) if source == "all" or key[0] == source]
                by_source[source] = {
                    "external_accuracy": ci_compare(reference, rows, keys, "acc_robust", percent=True),
                    "strict_useful_blocks": ci_compare(reference, rows, keys, "strict_useful", percent=True),
                    "response_level_numbered": ci_compare(raw_lookup[reference_label], candidate_raw[label], keys,
                                                           "think_numbered_block", percent=True),
                    "truncation": ci_compare(raw_lookup[reference_label], candidate_raw[label], keys,
                                              "truncated", percent=True),
                    "tokens": ci_compare(raw_lookup[reference_label], candidate_raw[label], keys,
                                         "tokens", percent=False),
                    "forward_passes": ci_compare(raw_lookup[reference_label], candidate_raw[label], keys,
                                                 "forward_passes", percent=False),
                }
            comparisons[reference_label] = by_source
        output["variants"][label] = {
            "archive": CANDIDATES[label], **candidate_meta[label],
            **source_summary(rows, candidate_raw[label]), "paired": comparisons,
        }

    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)
    for label, item in output["variants"].items():
        print(label, item["all"]["external_correct"], item["all"]["strict_useful"],
              item["GSM8K_DEV"]["external_correct"], item["GSM8K_DEV"]["strict_useful"],
              item["MATH_DEV"]["external_correct"], item["MATH_DEV"]["strict_useful"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, default=DEEP69_REVIEWS,
                        help="completed Deep69 manual-review manifest below results/.../")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        reviews = args.reviews.resolve()
        output = args.output.resolve()
        require(reviews.is_relative_to(ROOT.resolve()), "Deep69 review manifest must stay under result root")
        require(output.is_relative_to(ROOT.resolve()), "output must stay under result root")
        main(reviews, output)
    except (ComparisonError, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
