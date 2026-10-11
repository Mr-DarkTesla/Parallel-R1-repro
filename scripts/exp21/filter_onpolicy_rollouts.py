"""Fail-closed CPU prefilter for fresh exp-21 on-policy rollouts.

Usage:
  python3 scripts/exp21/filter_onpolicy_rollouts.py ROLLOUTS.jsonl OUTPUT_DIR

Writes provisional_candidates.jsonl for blind semantic-path review,
rejected_rollouts.jsonl with all structural reasons, and summary.json.  The
script intentionally does not decide whether Paths are semantically independent.
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATES = ROOT / "results/21-qwen3-0.6b-multiverse/data/onpolicy46_candidates.jsonl"
REQUIRED_ROLLOUT = ("id", "source", "answer_type", "seed", "output", "tokens", "truncated")

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "verl"))
from bench.answer_normalization import lone_number, normalize_superscripts  # noqa: E402
from exp21.mv_format import TAGS, parse as parse_multiverse  # noqa: E402


def answer_checker():
    """Load the exact robust math path used by scripts/bench/score.py."""
    try:
        from math_verify import parse, verify
        from verl.utils.reward_score.math_dapo import compute_score, last_boxed_only_string, remove_boxed
    except ImportError as error:
        raise RuntimeError("math_verify and verl math_dapo are required; refusing to weaken answer checking") from error

    def correct_robust(source, answer, truth):
        if source.upper() in ("ARC", "MMLUPRO"):
            choices = re.findall(r"(?i)(?:final answer|correct answer|answer is|answer)\s*:?\s*\**\(?([A-J]|10|[1-9])\b", answer)
            return bool(choices) and (choices[-1].upper() if choices[-1].isalpha() else "ABCDEFGHIJ"[int(choices[-1]) - 1]) == truth
        boxed = last_boxed_only_string(answer)
        if boxed:
            candidate = remove_boxed(boxed)
        else:
            parts = re.split(r"(?i)final answer\s*:", answer)
            lines = [line for line in parts[-1].splitlines() if line.strip()] if len(parts) > 1 else []
            candidate = lines[0] if lines else ""
        candidate = candidate.strip().strip("$").strip().rstrip(".")
        if not candidate:
            return False
        candidate = normalize_superscripts(candidate)
        target = parse(f"${truth}$")
        if verify(target, parse(f"${candidate}$")) or compute_score(f"Final Answer: {candidate}", truth)["acc"]:
            return True
        number = lone_number(candidate) if re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:/\d+)?%?", truth.strip()) else None
        return bool(number) and verify(target, parse(f"${number}$"))

    return correct_robust


def read_jsonl(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    records = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank JSONL line: {path}:{line_number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON: {path}:{line_number}") from error
            if not isinstance(record, dict):
                raise ValueError(f"JSON object required: {path}:{line_number}")
            records.append((line_number, record))
    if not records:
        raise ValueError(f"empty JSONL: {path}")
    return records


def read_candidates(path):
    candidates = {}
    for line_number, record in read_jsonl(path):
        if not all(isinstance(record.get(field), str) and record[field].strip()
                   for field in ("id", "source", "question", "answer", "answer_type")):
            raise ValueError(f"malformed candidate: {path}:{line_number}")
        if record["id"] in candidates:
            raise ValueError(f"duplicate candidate id: {record['id']}")
        candidates[record["id"]] = (line_number, record)
    return candidates


def validate_rollouts(records, candidates, rollout_path):
    seen = set()
    for line_number, record in records:
        if any(field not in record for field in REQUIRED_ROLLOUT):
            raise ValueError(f"missing required rollout field: {rollout_path}:{line_number}")
        if (not isinstance(record["id"], str) or not record["id"] or
                not isinstance(record["seed"], int) or isinstance(record["seed"], bool) or
                not isinstance(record["output"], str) or
                not isinstance(record["tokens"], int) or isinstance(record["tokens"], bool) or
                not isinstance(record["truncated"], bool)):
            raise ValueError(f"malformed rollout identity or generation: {rollout_path}:{line_number}")
        key = (record["id"], record["seed"])
        if key in seen:
            raise ValueError(f"duplicate rollout id/seed: {key}")
        if record["id"] not in candidates:
            raise ValueError(f"missing candidate for rollout id: {record['id']}")
        if "sample_seed" in record and record["sample_seed"] != record["seed"]:
            raise ValueError(f"sample_seed differs from seed: {rollout_path}:{line_number}")
        seen.add(key)


def reasons_for(record, candidate, correct_robust):
    reasons = []
    if record["source"] != candidate["source"] or record["answer_type"] != candidate["answer_type"]:
        reasons.append("candidate_metadata_mismatch")
    if record["tokens"] < 0:
        reasons.append("invalid_token_count")
    elif record["tokens"] > 4096:
        reasons.append("too_long")
    if record["truncated"]:
        reasons.append("truncated")

    output = record["output"].replace("<|endoftext|>", "").replace("<|im_end|>", "")
    if not output.startswith("<think>"):
        reasons.append("think_not_at_start")
    if output.count("<think>") != 1 or output.count("</think>") != 1:
        reasons.append("think_not_closed_once")
        return sorted(set(reasons))

    thought, final = output.split("</think>", 1)
    if any(tag in final for tag in TAGS):
        reasons.append("multiverse_tag_outside_think")
    structure = parse_multiverse(thought)
    if not structure["valid"] or len(structure["blocks"]) != 1:
        reasons.append("not_exactly_one_complete_parallel_block")
    elif not structure["blocks"][0]["numbered"]:
        reasons.append("parallel_block_not_numbered")
    if not final.strip():
        reasons.append("missing_external_final")
    elif not correct_robust(candidate["source"], final, candidate["answer"]):
        reasons.append("wrong_external_final")
    return sorted(set(reasons))


def review_record(line_number, record, candidate_line, candidate, rollout_path, candidates_path, reasons):
    return {
        "id": record["id"],
        "source": candidate["source"],
        "answer_type": candidate["answer_type"],
        "seed": record["seed"],
        "tokens": record["tokens"],
        "truncated": record["truncated"],
        "question": candidate["question"],
        "output": record["output"],
        "rollout_reference": {"path": str(rollout_path.resolve()), "line": line_number},
        "candidate_reference": {"path": str(candidates_path.resolve()), "line": candidate_line},
        "rejection_reasons": reasons,
        "manual_audit": {"semantic_path_independence": "unreviewed", "blind": True},
    }


def write_jsonl(path, records):
    with path.open("x") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rollouts", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    return parser.parse_args()


def main():
    args = parse_args()
    candidates = read_candidates(args.candidates)
    rollouts = read_jsonl(args.rollouts)
    validate_rollouts(rollouts, candidates, args.rollouts)
    correct_robust = answer_checker()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = {name: args.output_dir / name for name in
             ("provisional_candidates.jsonl", "rejected_rollouts.jsonl", "summary.json")}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError("output directory already contains prefilter results")

    provisional, rejected, reason_counts = [], [], collections.Counter()
    by_source = collections.defaultdict(collections.Counter)
    for line_number, record in rollouts:
        candidate_line, candidate = candidates[record["id"]]
        reasons = reasons_for(record, candidate, correct_robust)
        review = review_record(line_number, record, candidate_line, candidate, args.rollouts, args.candidates, reasons)
        bucket = "rejected" if reasons else "provisional"
        by_source[candidate["source"]][bucket] += 1
        if reasons:
            rejected.append(review)
            reason_counts.update(reasons)
        else:
            provisional.append(review)

    write_jsonl(paths["provisional_candidates.jsonl"], provisional)
    write_jsonl(paths["rejected_rollouts.jsonl"], rejected)
    summary = {
        "rollouts": len(rollouts),
        "provisional": len(provisional),
        "rejected": len(rejected),
        "rejection_reasons": dict(sorted(reason_counts.items())),
        "by_source": {source: dict(sorted(counts.items())) for source, counts in sorted(by_source.items())},
        "rollouts_path": str(args.rollouts.resolve()),
        "candidates_path": str(args.candidates.resolve()),
        "semantic_path_independence": "unreviewed; blind manual audit required",
    }
    with paths["summary.json"].open("x") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
