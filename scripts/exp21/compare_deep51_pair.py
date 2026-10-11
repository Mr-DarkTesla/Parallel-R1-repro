"""Paired fixed-40 comparison for the Deep51 tagged/plain 8-step pair.

The four candidate archives must exist before any output is written.  Without
manual review data, external accuracy is the archive's raw ``acc_robust`` and
strict useful IDs are null.  A later review manifest can be supplied with
``--reviews``:

{
  "schema_version": 1,
  "archives": {
    "deep51_tagged_p8_step4_masked_pilot.tgz": {
      "review_complete": true,
      "expected_external_correct": 30,
      "external_overrides": [
        {"key": ["GSM8K_DEV", "gsm8k-train/1", 0], "value": true,
         "evidence_file": "audit/review.md", "evidence_note": "..."}
      ],
      "strict_useful": [
        {"key": ["MATH_DEV", "math-test/1", 0],
         "evidence_file": "audit/review.md", "evidence_note": "..."}
      ]
    }
  }
}
"""

import argparse
import json
import os
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import compare, load
from compare_v4_recovery8 import corrected


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
OUTPUT = ROOT / "audit/deep51_pair_paired.json"
CANDIDATES = {
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


class ComparisonError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ComparisonError(message)


def parse_key(value, context):
    require(isinstance(value, list) and len(value) == 3,
            f"{context}: key must be [source, problem_id, sample]")
    source, problem_id, sample = value
    require(source in {"GSM8K_DEV", "MATH_DEV"}, f"{context}: invalid source")
    require(isinstance(problem_id, str) and problem_id, f"{context}: invalid problem_id")
    require(isinstance(sample, int), f"{context}: sample must be an integer")
    return source, problem_id, sample


def validate_evidence(item, context):
    value = item.get("evidence_file")
    require(isinstance(value, str) and value.startswith("audit/"),
            f"{context}: evidence_file must start with audit/")
    path = (ROOT / value).resolve()
    require(path.is_relative_to(ROOT.resolve()) and path.is_file(),
            f"{context}: missing or invalid evidence_file {value!r}")
    require(isinstance(item.get("evidence_note"), str) and item["evidence_note"].strip(),
            f"{context}: evidence_note is required")


def read_reviews(path):
    if path is None:
        return {}
    require(path.is_file(), f"review manifest missing: {path}")
    data = json.loads(path.read_text())
    require(data.get("schema_version") == 1, "review schema_version must be 1")
    archives = data.get("archives")
    require(isinstance(archives, dict), "review manifest must contain object archives")
    unknown = sorted(set(archives) - set(CANDIDATES.values()))
    require(not unknown, "review manifest contains unknown archives: " + ", ".join(unknown))
    return archives


def apply_review(rows, filename, review):
    if review is None:
        return rows, None, [], "archive_acc_robust_unreviewed"
    require(isinstance(review, dict) and review.get("review_complete") is True,
            f"{filename}: review entry must set review_complete=true")
    values = {key: bool(row["acc_robust"]) for key, row in rows.items()}
    serialized_overrides, seen = [], set()
    overrides = review.get("external_overrides")
    require(isinstance(overrides, list), f"{filename}: external_overrides must be a list")
    for index, item in enumerate(overrides):
        context = f"{filename} external override {index}"
        require(isinstance(item, dict), f"{context}: must be an object")
        key = parse_key(item.get("key"), context)
        require(key in rows and key not in seen, f"{context}: missing or duplicate row {key}")
        require(type(item.get("value")) is bool and item["value"] != values[key],
                f"{context}: value must be boolean and change acc_robust")
        validate_evidence(item, context)
        values[key], seen = item["value"], seen | {key}
        serialized_overrides.append({name: item[name] for name in
                                     ("key", "value", "evidence_file", "evidence_note")})
    corrected_rows = {key: row.copy() for key, row in rows.items()}
    for key, value in values.items():
        corrected_rows[key]["acc_robust"] = value
    expected = review.get("expected_external_correct")
    require(type(expected) is int and expected == sum(values.values()),
            f"{filename}: expected_external_correct does not match reviewed rows")

    useful = review.get("strict_useful")
    require(isinstance(useful, list), f"{filename}: strict_useful must be a list")
    useful_ids, useful_seen = [], set()
    for index, item in enumerate(useful):
        context = f"{filename} strict useful {index}"
        require(isinstance(item, dict), f"{context}: must be an object")
        key = parse_key(item.get("key"), context)
        require(key in rows and key not in useful_seen, f"{context}: missing or duplicate row {key}")
        require(bool(rows[key]["think_numbered_block"]),
                f"{context}: useful row is not response-level numbered")
        validate_evidence(item, context)
        useful_seen.add(key)
        useful_ids.append(key[1])
    return corrected_rows, useful_ids, serialized_overrides, "manual_external_review"


def verify_same_pilot(reference, candidate, reference_name, candidate_name):
    require(reference.keys() == candidate.keys(),
            f"{candidate_name}: rows differ from {reference_name}")
    for key in sorted(candidate):
        require(reference[key]["input"] == candidate[key]["input"],
                f"{candidate_name}: input differs from {reference_name} at {key}")
        require(reference[key]["decoder"] == candidate[key]["decoder"] == "masked",
                f"{candidate_name}: decoder differs at {key}")


def main(reviews_path, output_path):
    needed = [ARCHIVES / name for name in (*CANDIDATES.values(), *BASELINES.values())]
    missing = [path.name for path in needed if not path.is_file()]
    require(not missing, "missing pilot archives: " + ", ".join(missing))
    reviews = read_reviews(reviews_path)

    c0 = corrected(load(ARCHIVES / BASELINES["corrected_c0"]), FIXES)
    recovery = load(ARCHIVES / BASELINES["recovery8_step8"])
    require(sum(row["acc_robust"] for row in c0.values()) == 34,
            "corrected C0 must contain 34 external-correct rows")
    require(sum(row["acc_robust"] for row in recovery.values()) == 29,
            "reviewed recovery8 step8 must contain 29 external-correct rows")
    baselines = {"corrected_c0": c0, "recovery8_step8": recovery}

    raw_candidates = {label: load(ARCHIVES / filename) for label, filename in CANDIDATES.items()}
    candidates, review_summary = {}, {}
    for label, filename in CANDIDATES.items():
        rows = raw_candidates[label]
        require(len(rows) == 40, f"{filename}: expected 40 rows, got {len(rows)}")
        reviewed, useful_ids, overrides, accuracy_source = apply_review(rows, filename, reviews.get(filename))
        candidates[label] = reviewed
        review_summary[label] = {
            "manual_review_complete": useful_ids is not None,
            "external_accuracy_source": accuracy_source,
            "external_overrides": overrides,
            "strict_useful_ids": useful_ids,
        }

    anchor = c0
    for label, rows in {**baselines, **candidates}.items():
        verify_same_pilot(anchor, rows, "corrected_c0", label)

    output = {
        "protocol": {
            "pilot": "same 40 masked greedy prompts",
            "unreviewed_external_accuracy": "archive acc_robust until a manual review manifest is supplied",
            "paired_ci": "10,000 paired bootstrap samples from compare_masked_pilot_archives.py",
        },
        "review_manifest": str(reviews_path) if reviews_path else None,
        "baselines": {
            "corrected_c0": {"archive": BASELINES["corrected_c0"], "external_correct": 34,
                             "external_corrections": [list(key) for key in FIXES]},
            "recovery8_step8": {"archive": BASELINES["recovery8_step8"], "external_correct": 29,
                               "external_corrections": []},
        },
        "variants": {},
    }
    all_rows = {**baselines, **candidates}
    for label, rows in candidates.items():
        raw = raw_candidates[label]
        keys = sorted(rows)
        references = {name: other for name, other in all_rows.items() if name != label}
        output["variants"][label] = {
            "archive": CANDIDATES[label],
            **review_summary[label],
            "external_correct": sum(row["acc_robust"] for row in rows.values()),
            "response_level_numbered": sum(row["think_numbered_block"] for row in raw.values()),
            "truncated": sum(row["truncated"] for row in raw.values()),
            "outside_think": sum(row["outside_think_tags"] > 0 for row in raw.values()),
            "mean_tokens": round(sum(row["tokens"] for row in raw.values()) / 40, 2),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in raw.values()) / 40, 2),
            "paired": {
                output_name: {
                    reference_name: compare(reference, rows if metric == "acc_robust" else raw, keys, metric)
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
    args = parser.parse_args()
    try:
        main(args.reviews.resolve() if args.reviews else None, args.output.resolve())
    except (ComparisonError, FileNotFoundError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
