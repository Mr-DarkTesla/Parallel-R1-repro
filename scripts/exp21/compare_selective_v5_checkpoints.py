"""Compare all eight v5 checkpoints after complete row-level manual review.

The script is intentionally fail-closed.  It writes no output until all eight
archives exist and every step has a complete review entry.  Manual overrides
must name an archive row and a local review file.

Usage:
  python3 scripts/exp21/compare_selective_v5_checkpoints.py \
    --reviews results/21-qwen3-0.6b-multiverse/audit/selective_v5_checkpoint_reviews.json
"""

import argparse
import json
import os
from pathlib import Path

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import compare, load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
STEPS = (8, 16, 24, 32, 40, 48, 56, 64)
DEFAULT_REVIEWS = AUDIT / "selective_v5_checkpoint_reviews.json"
DEFAULT_OUTPUT = AUDIT / "selective_v5_checkpoint_paired.json"
TEMPLATE = AUDIT / "selective_v5_checkpoint_reviews.template.json"
REFERENCE_ARCHIVES = {
    "c0_corrected": "c0-greedy-pilot40.tgz",
    "selective_v2": "selective_v2_masked_pilot.tgz",
}


class ReviewError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewError(message)


def parse_key(value, context):
    require(isinstance(value, list) and len(value) == 3,
            f"{context}: key must be [source, problem_id, sample]")
    source, problem_id, sample = value
    require(source in {"GSM8K_DEV", "MATH_DEV"}, f"{context}: bad source {source!r}")
    require(isinstance(problem_id, str) and problem_id, f"{context}: bad problem_id")
    require(isinstance(sample, int), f"{context}: sample must be an integer")
    return source, problem_id, sample


def evidence_path(value, context):
    require(isinstance(value, str) and value.startswith("audit/"),
            f"{context}: evidence_file must be relative to the result directory and start with audit/")
    path = (ROOT / value).resolve()
    require(path.is_relative_to(ROOT.resolve()), f"{context}: evidence_file escapes result directory")
    require(path.is_file(), f"{context}: missing evidence file {value}")
    return path


def validate_evidence(item, context):
    evidence_path(item.get("evidence_file"), context)
    note = item.get("evidence_note")
    require(isinstance(note, str) and note.strip(), f"{context}: non-empty evidence_note is required")


def corrected_c0(rows):
    result = {key: row.copy() for key, row in rows.items()}
    for key in FIXES:
        require(key in result, f"C0 correction key absent from archive: {key}")
        require(result[key]["acc_robust"] is False, f"C0 correction no longer changes value: {key}")
        result[key]["acc_robust"] = True
    return result


def validate_review_manifest(path):
    if not path.is_file():
        raise ReviewError(
            f"review manifest is missing: {path}. Fill {TEMPLATE.name} and pass it with --reviews"
        )
    data = json.loads(path.read_text())
    require(data.get("schema_version") == 1, "review manifest schema_version must be 1")
    steps = data.get("steps")
    require(isinstance(steps, dict), "review manifest must contain object steps")
    missing = [str(step) for step in STEPS if not isinstance(steps.get(str(step)), dict)
               or steps[str(step)].get("review_complete") is not True]
    extra = sorted(set(steps) - {str(step) for step in STEPS})
    require(not extra, "unexpected steps in review manifest: " + ", ".join(extra))
    return data, missing


def missing_archives():
    missing = [f"selective_v5_step{step}_masked_pilot.tgz" for step in STEPS
               if not (ARCHIVES / f"selective_v5_step{step}_masked_pilot.tgz").is_file()]
    missing += [name for name in REFERENCE_ARCHIVES.values() if not (ARCHIVES / name).is_file()]
    return missing


def apply_overrides(rows, items, step, metric):
    require(isinstance(items, list), f"step {step} {metric}: overrides must be a list")
    values = {key: bool(row["acc_robust"]) for key, row in rows.items()}
    seen = set()
    serialized = []
    for index, item in enumerate(items):
        context = f"step {step} {metric} override {index}"
        require(isinstance(item, dict), f"{context}: override must be an object")
        key = parse_key(item.get("key"), context)
        require(key in rows, f"{context}: archive row does not exist: {key}")
        require(key not in seen, f"{context}: duplicate archive row: {key}")
        require(type(item.get("value")) is bool, f"{context}: value must be true or false")
        validate_evidence(item, context)
        require(values[key] != item["value"],
                f"{context}: override does not change strict parser value for {key}")
        seen.add(key)
        values[key] = item["value"]
        serialized.append({"key": list(key), "value": item["value"],
                           "evidence_file": item["evidence_file"],
                           "evidence_note": item["evidence_note"]})
    return values, serialized


def validate_useful(rows, items, step):
    require(isinstance(items, list), f"step {step}: strict_useful must be a list")
    keys, serialized = [], []
    for index, item in enumerate(items):
        context = f"step {step} strict_useful item {index}"
        require(isinstance(item, dict), f"{context}: item must be an object")
        key = parse_key(item.get("key"), context)
        require(key in rows, f"{context}: archive row does not exist: {key}")
        require(key not in keys, f"{context}: duplicate archive row: {key}")
        validate_evidence(item, context)
        require(bool(rows[key]["think_numbered_block"]),
                f"{context}: strictly useful row is not response-level numbered: {key}")
        keys.append(key)
        serialized.append({"key": list(key), "evidence_file": item["evidence_file"],
                           "evidence_note": item["evidence_note"]})
    return keys, serialized


def rows_with_accuracy(rows, values):
    result = {key: row.copy() for key, row in rows.items()}
    for key, value in values.items():
        result[key]["acc_robust"] = value
    return result


def shown_path(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_expected_counts(review, counts, step):
    expected = review.get("expected_counts")
    require(isinstance(expected, dict), f"step {step}: expected_counts is required")
    require(set(expected) == set(counts),
            f"step {step}: expected_counts keys must be {sorted(counts)}")
    for name, actual in counts.items():
        require(type(expected[name]) is int and expected[name] == actual,
                f"step {step}: reviewed {name}={expected.get(name)!r}, computed {actual}")


def main(reviews_path, output_path):
    manifest, missing_reviews = validate_review_manifest(reviews_path)
    absent_archives = missing_archives()
    readiness_errors = []
    if missing_reviews:
        readiness_errors.append("manual review incomplete for steps: " + ", ".join(missing_reviews))
    if absent_archives:
        readiness_errors.append("missing pilot archives: " + ", ".join(absent_archives))
    require(not readiness_errors, "; ".join(readiness_errors))
    references = {
        "c0_corrected": corrected_c0(load(ARCHIVES / REFERENCE_ARCHIVES["c0_corrected"])),
        "selective_v2": load(ARCHIVES / REFERENCE_ARCHIVES["selective_v2"]),
    }
    output = {
        "protocol": {
            "pilot": "same 40 masked greedy prompts at all eight checkpoints",
            "strict_parser_correct": "archive acc_robust without candidate correction",
            "external_final_correct": "retention metric: closed think and mathematically correct standalone external answer, even if reasoning markup is damaged",
            "clean_external_final_correct": "conservative diagnostic: closed think and unambiguous standalone correct external answer; damaged reasoning markup and ambiguous notation are excluded",
            "answer_anywhere_correct": "reviewed correct value anywhere, including truncated reasoning",
            "response_level_numbered": "archive think_numbered_block; the whole response must pass the structural parser",
            "strictly_useful": "reviewed correct, substantive independent paths with a correct combination",
            "paired_ci": "10,000 paired bootstrap samples from compare_masked_pilot_archives.py",
        },
        "review_manifest": shown_path(reviews_path),
        "references": {
            "c0_corrected": {"archive": REFERENCE_ARCHIVES["c0_corrected"],
                             "manual_corrections": [list(key) for key in FIXES]},
            "selective_v2": {"archive": REFERENCE_ARCHIVES["selective_v2"],
                             "manual_corrections": []},
        },
        "steps": {},
    }

    for step in STEPS:
        review = manifest["steps"][str(step)]
        filename = f"selective_v5_step{step}_masked_pilot.tgz"
        require(review.get("archive") == filename,
                f"step {step}: reviewed archive must be {filename}")
        review_file = evidence_path(review.get("review_file"), f"step {step}")
        review_text = review_file.read_text()
        require(filename in review_text, f"step {step}: review file does not name {filename}")

        raw = load(ARCHIVES / filename)
        require(len(raw) == 40, f"step {step}: archive has {len(raw)} rows, expected 40")
        keys = sorted(raw)
        for reference_name, base in references.items():
            require(base.keys() == raw.keys(), f"step {step}: rows differ from {reference_name}")
            for key in keys:
                require(base[key]["input"] == raw[key]["input"],
                        f"step {step}: prompt differs from {reference_name} at {key}")
                require(base[key]["decoder"] == raw[key]["decoder"] == "masked",
                        f"step {step}: decoder differs at {key}")

        external_values, external_overrides = apply_overrides(
            raw, review.get("external_final_overrides"), step,
            "external_final")
        clean_external_values, clean_external_overrides = apply_overrides(
            raw, review.get("clean_external_final_overrides"), step,
            "clean_external_final")
        anywhere_values, anywhere_overrides = apply_overrides(
            raw, review.get("answer_anywhere_overrides"), step,
            "answer_anywhere")
        useful_keys, useful_items = validate_useful(
            raw, review.get("strict_useful"), step)
        external_rows = rows_with_accuracy(raw, external_values)
        clean_external_rows = rows_with_accuracy(raw, clean_external_values)
        anywhere_rows = rows_with_accuracy(raw, anywhere_values)
        counts = {
            "strict_parser_correct": sum(bool(row["acc_robust"]) for row in raw.values()),
            "external_final_correct": sum(external_values.values()),
            "clean_external_final_correct": sum(clean_external_values.values()),
            "answer_anywhere_correct": sum(anywhere_values.values()),
            "response_level_numbered": sum(bool(row["think_numbered_block"]) for row in raw.values()),
            "strictly_useful": len(useful_keys),
        }
        validate_expected_counts(review, counts, step)

        output["steps"][str(step)] = {
            "archive": filename,
            "review_file": review["review_file"],
            "strict_parser_correct": counts["strict_parser_correct"],
            "external_final_correct": counts["external_final_correct"],
            "clean_external_final_correct": counts["clean_external_final_correct"],
            "answer_anywhere_correct": counts["answer_anywhere_correct"],
            "response_level_numbered": counts["response_level_numbered"],
            "strictly_useful_count": counts["strictly_useful"],
            "strict_useful_ids": [key[1] for key in useful_keys],
            "strict_useful_rows": useful_items,
            "external_final_overrides": external_overrides,
            "clean_external_final_overrides": clean_external_overrides,
            "answer_anywhere_overrides": anywhere_overrides,
            "outside_think": sum(row["outside_think_tags"] > 0 for row in raw.values()),
            "truncated": sum(bool(row["truncated"]) for row in raw.values()),
            "mean_tokens": round(sum(row["tokens"] for row in raw.values()) / 40, 2),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in raw.values()) / 40, 2),
            "paired_strict_parser_accuracy": {
                name: compare(base, raw, keys, "acc_robust") for name, base in references.items()},
            "paired_external_final_accuracy": {
                name: compare(base, external_rows, keys, "acc_robust") for name, base in references.items()},
            "paired_clean_external_final_accuracy": {
                name: compare(base, clean_external_rows, keys, "acc_robust") for name, base in references.items()},
            "paired_answer_anywhere_accuracy": {
                name: compare(base, anywhere_rows, keys, "acc_robust") for name, base in references.items()},
            "paired_response_level_numbered": {
                name: compare(base, raw, keys, "think_numbered_block") for name, base in references.items()},
        }

    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)
    for step, row in output["steps"].items():
        print(step, row["strict_parser_correct"], row["external_final_correct"],
              row["clean_external_final_correct"],
              row["answer_anywhere_correct"], row["response_level_numbered"],
              row["strictly_useful_count"],
              row["paired_external_final_accuracy"]["c0_corrected"]["delta"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, default=DEFAULT_REVIEWS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        main(args.reviews.resolve(), args.output.resolve())
    except (ReviewError, FileNotFoundError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
