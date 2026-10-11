"""Paired fixed-40 analysis for the agent-authored tagged/plain SFT sweep.

The script discovers archives named
``agent_authored_{tagged,plain}_p8_step{N}_masked_pilot.tgz`` and compares every
completed same-step pair.  It always reports raw parser accuracy separately
from manual semantic correctness.  ``strict_useful`` is never inferred from
syntax: it requires a complete review manifest with evidence for every block.

Usage:
  python3 -B scripts/exp21/compare_agent_authored_sweep.py
  python3 -B scripts/exp21/compare_agent_authored_sweep.py \
    --reviews results/21-qwen3-0.6b-multiverse/audit/agent_authored_sweep_manual_reviews.json

Outputs are limited to audit/agent_authored_sweep_*.
"""

import argparse
import json
import os
import re
from pathlib import Path

import numpy as np

from audit_c0_pilot_scoring import FIXES
from compare_masked_pilot_archives import load

ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
DEFAULT_REVIEWS = AUDIT / "agent_authored_sweep_manual_reviews.json"
DEFAULT_JSON = AUDIT / "agent_authored_sweep_paired.json"
DEFAULT_MD = AUDIT / "agent_authored_sweep_table.md"
BASELINE = "c0-greedy-pilot40.tgz"
PATTERN = re.compile(r"^agent_authored_(tagged|plain)_p8_step([1-8])_masked_pilot\.tgz$")
SOURCES = ("all", "GSM8K_DEV", "MATH_DEV")
BOOTSTRAP = {}


class AnalysisError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AnalysisError(message)


def key_from_json(value, context):
    require(isinstance(value, list) and len(value) == 3, f"{context}: key must be [source,id,sample]")
    source, problem_id, sample = value
    require(source in SOURCES[1:] and isinstance(problem_id, str) and isinstance(sample, int),
            f"{context}: invalid key")
    return source, problem_id, sample


def ci(reference, candidate, keys, metric, percent):
    deltas = np.asarray([float(candidate[k][metric]) - float(reference[k][metric]) for k in keys])
    n = len(deltas)
    require(n > 0, f"no rows for {metric}")
    if n not in BOOTSTRAP:
        BOOTSTRAP[n] = np.random.default_rng(0).integers(0, n, size=(10_000, n))
    distribution = np.sort(deltas[BOOTSTRAP[n]].mean(axis=1))
    scale = 100 if percent else 1
    return {
        "baseline": round(scale * np.mean([float(reference[k][metric]) for k in keys]), 2),
        "candidate": round(scale * np.mean([float(candidate[k][metric]) for k in keys]), 2),
        "delta": round(scale * deltas.mean(), 2),
        "ci95": [round(scale * distribution[i], 2) for i in (249, 9749)],
        "n": n,
    }


def corrected_c0():
    raw = load(ARCHIVES / BASELINE)
    rows = {key: row.copy() for key, row in raw.items()}
    for key in FIXES:
        require(key in rows and not rows[key]["acc_robust"], f"C0 fix drift: {key}")
        rows[key]["acc_robust"] = True
    require(sum(bool(row["acc_robust"]) for row in rows.values()) == 34,
            "expected 34 corrected C0 answers")
    return raw, rows


def discover():
    found = {}
    for path in ARCHIVES.glob("agent_authored_*_p8_step*_masked_pilot.tgz"):
        match = PATTERN.fullmatch(path.name)
        if match:
            arm, step = match.groups()
            found[(arm, int(step))] = path
    return found


def validate_same40(anchor, candidate, label):
    require(set(anchor) == set(candidate), f"{label}: row keys differ from C0")
    require(len(candidate) == 40, f"{label}: expected fixed40, got {len(candidate)}")
    for key in anchor:
        require(anchor[key]["input"] == candidate[key]["input"], f"{label}: prompt drift at {key}")
        require(anchor[key]["decoder"] == candidate[key]["decoder"] == "masked",
                f"{label}: decoder mismatch at {key}")


def read_reviews(path, expected_names):
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    require(data.get("schema_version") == 1, "review manifest schema_version must be 1")
    entries = data.get("archives")
    require(isinstance(entries, dict), "review manifest archives must be an object")
    unknown = set(entries) - expected_names
    require(not unknown, f"review manifest references unknown archives: {sorted(unknown)}")
    return entries


def semantic_rows(raw, archive_name, entry):
    """Return reviewed rows or None. Partial review cannot create useful metrics."""
    if not entry or entry.get("review_complete") is not True:
        return None, {"review_complete": False}
    rows = {key: row.copy() for key, row in raw.items()}
    for row in rows.values():
        row["strict_useful"] = False
    overrides = entry.get("external_overrides", [])
    useful = entry.get("strict_useful", [])
    require(isinstance(overrides, list) and isinstance(useful, list),
            f"{archive_name}: overrides/useful must be arrays")
    seen = set()
    for i, item in enumerate(overrides):
        require(isinstance(item, dict), f"{archive_name}: override {i} must be object")
        key = key_from_json(item.get("key"), f"{archive_name}: override {i}")
        require(key in rows and key not in seen, f"{archive_name}: unknown or duplicate override {key}")
        require(type(item.get("value")) is bool and item["value"] != bool(raw[key]["acc_robust"]),
                f"{archive_name}: override must change raw accuracy")
        evidence = item.get("evidence_file")
        require(isinstance(evidence, str) and evidence.startswith("audit/"),
                f"{archive_name}: override needs evidence below audit/")
        require((ROOT / evidence).is_file(), f"{archive_name}: missing evidence {evidence}")
        rows[key]["acc_robust"] = item["value"]
        seen.add(key)
    useful_seen = set()
    for i, item in enumerate(useful):
        require(isinstance(item, dict), f"{archive_name}: useful {i} must be object")
        key = key_from_json(item.get("key"), f"{archive_name}: useful {i}")
        require(key in rows and key not in useful_seen, f"{archive_name}: unknown or duplicate useful {key}")
        require(bool(raw[key]["think_numbered_block"]),
                f"{archive_name}: useful claim needs a complete numbered block")
        evidence = item.get("evidence_file")
        require(isinstance(evidence, str) and evidence.startswith("audit/") and (ROOT / evidence).is_file(),
                f"{archive_name}: useful claim needs existing audit evidence")
        rows[key]["strict_useful"] = True
        useful_seen.add(key)
    expected = entry.get("expected_external_correct")
    require(type(expected) is int and expected == sum(bool(r["acc_robust"]) for r in rows.values()),
            f"{archive_name}: expected_external_correct disagrees with overrides")
    # Every response with a candidate numbered block must have an explicit judgment.
    examined = {key_from_json(k, f"{archive_name}: examined") for k in entry.get("examined_block_keys", [])}
    block_keys = {key for key, row in raw.items() if row["think_numbered_block"]}
    require(examined == block_keys, f"{archive_name}: examined block set must equal actual block set")
    return rows, {
        "review_complete": True,
        "external_correct": expected,
        "strict_useful_ids": [key[1] for key, row in rows.items() if row["strict_useful"]],
        "external_overrides": len(overrides),
        "examined_numbered_blocks": len(examined),
    }


def source_summary(raw, semantic, review):
    result = {}
    for source in SOURCES:
        keys = [key for key in sorted(raw) if source == "all" or key[0] == source]
        required = 40 if source == "all" else 20
        require(len(keys) == required, f"unexpected {source} size {len(keys)}")
        row = {
            "n": required,
            "raw_acc_robust": sum(bool(raw[k]["acc_robust"]) for k in keys),
            "numbered_blocks": sum(bool(raw[k]["think_numbered_block"]) for k in keys),
            "truncated": sum(bool(raw[k]["truncated"]) for k in keys),
            "mean_tokens": round(float(np.mean([raw[k]["tokens"] for k in keys])), 2),
            "mean_forward_passes": round(float(np.mean([raw[k]["forward_passes"] for k in keys])), 2),
        }
        if semantic is None:
            row["manual_external_correct"] = None
            row["strict_useful"] = None
        else:
            row["manual_external_correct"] = sum(bool(semantic[k]["acc_robust"]) for k in keys)
            row["strict_useful"] = sum(bool(semantic[k]["strict_useful"]) for k in keys)
        result[source] = row
    return result


def pair_metrics(reference_raw, candidate_raw, reference_semantic, candidate_semantic):
    output = {}
    for source in SOURCES:
        keys = [key for key in sorted(candidate_raw) if source == "all" or key[0] == source]
        metrics = {
            "raw_acc_robust": ci(reference_raw, candidate_raw, keys, "acc_robust", True),
            "numbered_blocks": ci(reference_raw, candidate_raw, keys, "think_numbered_block", True),
            "truncation": ci(reference_raw, candidate_raw, keys, "truncated", True),
            "tokens": ci(reference_raw, candidate_raw, keys, "tokens", False),
            "forward_passes": ci(reference_raw, candidate_raw, keys, "forward_passes", False),
        }
        if reference_semantic is not None and candidate_semantic is not None:
            metrics["manual_external_accuracy"] = ci(reference_semantic, candidate_semantic, keys, "acc_robust", True)
            metrics["strict_useful"] = ci(reference_semantic, candidate_semantic, keys, "strict_useful", True)
        output[source] = metrics
    return output


def markdown(result):
    lines = ["# Agent-authored tagged/plain fixed40 sweep", "",
             "`raw_acc_robust` is parser output. Manual external accuracy and strictly useful blocks require a complete review manifest; without one they remain null.", "",
             "| Variant | Raw correct /40 | Numbered /40 | Truncated /40 | Manual correct /40 | Strict useful /40 |", "|---|---:|---:|---:|---:|---:|"]
    for label, item in sorted(result["variants"].items()):
        all_ = item["summary"]["all"]
        manual = "pending" if all_["manual_external_correct"] is None else str(all_["manual_external_correct"])
        useful = "pending" if all_["strict_useful"] is None else str(all_["strict_useful"])
        lines.append(f"| {label} | {all_['raw_acc_robust']} | {all_['numbered_blocks']} | {all_['truncated']} | {manual} | {useful} |")
    lines += ["", "## Paired CIs", "", "All reported binary deltas are candidate minus reference in percentage points. CI is a deterministic 10,000-resample paired bootstrap over the identical 40 prompts.", ""]
    for label, item in sorted(result["variants"].items()):
        refs = item["paired"]
        for reference, values in refs.items():
            m = values["all"]
            raw = m["raw_acc_robust"]
            lines.append(f"- `{label}` vs `{reference}` raw accuracy: {raw['delta']:+.2f} pp, 95% CI [{raw['ci95'][0]:.2f}, {raw['ci95'][1]:.2f}].")
            if "manual_external_accuracy" in m:
                sem = m["manual_external_accuracy"]
                useful = m["strict_useful"]
                lines.append(f"  Manual external: {sem['delta']:+.2f} pp [{sem['ci95'][0]:.2f}, {sem['ci95'][1]:.2f}]; strict useful: {useful['delta']:+.2f} pp [{useful['ci95'][0]:.2f}, {useful['ci95'][1]:.2f}].")
    return "\n".join(lines) + "\n"


def main(reviews_path, json_path, markdown_path):
    require((ARCHIVES / BASELINE).is_file(), f"missing baseline {BASELINE}")
    discovered = discover()
    require(discovered, "no agent_authored fixed40 archives found")
    expected_names = {p.name for p in discovered.values()}
    review_entries = read_reviews(reviews_path, expected_names)
    c0_raw, c0_semantic = corrected_c0()
    variants = {}
    raw_by_label = {"c0_corrected": c0_raw}
    semantic_by_label = {"c0_corrected": {k: {**v, "strict_useful": False} for k, v in c0_semantic.items()}
                         }
    for (arm, step), path in sorted(discovered.items(), key=lambda item: (item[0][1], item[0][0])):
        label = f"{arm}_step{step}"
        raw = load(path)
        validate_same40(c0_raw, raw, label)
        entry = None if review_entries is None else review_entries.get(path.name)
        semantic, review = semantic_rows(raw, path.name, entry)
        variants[label] = {"archive": path.name, "summary": source_summary(raw, semantic, review), "review": review}
        raw_by_label[label] = raw
        semantic_by_label[label] = semantic
    for label, item in variants.items():
        refs = {"c0_corrected": raw_by_label["c0_corrected"]}
        arm, step = label.split("_")
        paired_label = f"{'plain' if arm == 'tagged' else 'tagged'}_{step}"
        if paired_label in raw_by_label:
            refs[paired_label] = raw_by_label[paired_label]
        item["paired"] = {name: pair_metrics(reference, raw_by_label[label], semantic_by_label[name], semantic_by_label[label])
                          for name, reference in refs.items()}
    result = {
        "protocol": {
            "fixed40": "same 20 GSM8K_DEV and 20 MATH_DEV prompts, masked decoder",
            "raw_accuracy": "archive acc_robust, not a manual semantic verdict",
            "strict_useful": "only complete manual review manifest can set this metric",
            "ci": "10,000 deterministic paired bootstrap samples; binary deltas in percentage points",
        },
        "archives_discovered": sorted(expected_names),
        "variants": variants,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = json_path.with_suffix(".tmp")
    try:
        temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, json_path)
    finally:
        temporary.unlink(missing_ok=True)
    markdown_path.write_text(markdown(result))
    print(json.dumps({label: item["summary"]["all"] for label, item in variants.items()}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, default=DEFAULT_REVIEWS)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--table", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    try:
        for path in (args.reviews, args.output, args.table):
            require(path.resolve().is_relative_to(ROOT.resolve()), "all paths must remain under result root")
        main(args.reviews.resolve(), args.output.resolve(), args.table.resolve())
    except (AnalysisError, FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: {error}") from error
