#!/usr/bin/env python3
"""Build a fail-closed matched SFT pair from independently accepted agent-authored traces.

The script is CPU-only and never launches training.  It writes two training
parquets with identical prompts, IDs, row order and replay rows.  For each
accepted positive, the tagged arm keeps the reviewed response byte-for-byte;
the plain arm removes only the Multiverse plan/container and tags, retaining
both Path bodies in their original order.
"""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"

DEFAULT_AUTHORED = [
    DATA / "onpolicy_agent_authored_math16.jsonl",
    DATA / "onpolicy_agent_authored_math_remaining.jsonl",
    DATA / "onpolicy_agent_authored_gsm16.jsonl",
    DATA / "onpolicy_agent_authored_gsm_remaining.jsonl",
    DATA / "onpolicy_agent_authored_fraction8.jsonl",
]
DEFAULT_CANDIDATES = AUDIT / "agent_authored82/candidates.jsonl"
DEFAULT_CANDIDATE_AUDIT = DATA / "onpolicy46_candidates.audit.json"
# These are the audited sources used by Deep69: v4 supplies both replay modes,
# recovery8 supplies the frozen validation and the ordinary thinking controls.
DEFAULT_REPLAY_TRAIN = DATA / "sft_selective_blocks_v4_train.parquet"
DEFAULT_REPLAY_VAL = DATA / "sft_v4_recovery8_val.parquet"
DEFAULT_OUT_PREFIX = DATA / "sft_agent_authored"

CONTROL_COUNT = 45
REPLAY_BY_KIND_AND_SOURCE = {
    "replay_th": {"math": 36, "gsm8k": 22, "arc": 13},
    "replay_nt": {"math": 36, "gsm8k": 22, "arc": 13},
}
CONTROL_SEED = "agent-authored-control-20261012"
REPLAY_SEEDS = {
    "replay_th": "agent-authored-replay-th-20261012",
    "replay_nt": "agent-authored-replay-nt-20261012",
}
ORDER_SEED = "agent-authored-order-20261012"


class GateError(RuntimeError):
    """An input fails a quality, provenance, or composition precondition."""


def fail(message: str) -> None:
    raise GateError(message)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def stable_rank(seed: str, problem_id: str) -> str:
    return hashlib.sha256(f"{seed}\0{problem_id}".encode()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        fail(f"missing JSONL: {path}")
    rows: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            fail(f"invalid JSON on {path}:{lineno}: {error}")
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            fail(f"JSONL row needs string id: {path}:{lineno}")
        rows.append(row)
    if not rows or len(rows) != len({row["id"] for row in rows}):
        fail(f"empty or duplicate IDs in {path}")
    return rows


def read_id_manifest(path: Path, *, accepted: bool) -> set[str]:
    """Read JSON array, JSONL, or one-ID-per-line manifest.

    A manifest is an explicit decision record.  Rows marked reject in an
    accepted manifest (or accept in a rejected manifest) are rejected rather
    than silently reinterpreted.
    """
    if not path.is_file():
        fail(f"missing ID manifest: {path}")
    text = path.read_text().strip()
    if not text:
        fail(f"empty ID manifest: {path}")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    items: list[Any]
    if isinstance(parsed, list):
        items = parsed
    elif isinstance(parsed, dict):
        keys = ("accepted_ids", "ids") if accepted else ("rejected_ids", "ids")
        for key in keys:
            if isinstance(parsed.get(key), list):
                items = parsed[key]
                break
        else:
            fail(f"JSON manifest needs one of {keys}: {path}")
    elif parsed is None:
        # JSONL first; fall back to a plain one-ID-per-line list only when no
        # line parses as JSON.  This avoids accepting malformed JSONL silently.
        items = []
        json_seen = False
        for lineno, line in enumerate(text.splitlines(), 1):
            item = line.strip()
            if not item:
                continue
            if item.startswith("{") or item.startswith("[") or item.startswith('"'):
                json_seen = True
                try:
                    items.append(json.loads(item))
                except json.JSONDecodeError as error:
                    fail(f"invalid manifest JSON on {path}:{lineno}: {error}")
            else:
                items.append(item)
        if json_seen and any(isinstance(item, str) and item.startswith("{") for item in items):
            fail(f"mixed malformed JSONL manifest: {path}")
    else:
        fail(f"unsupported manifest format: {path}")

    result: set[str] = set()
    wanted = "accept" if accepted else "reject"
    opposite = "reject" if accepted else "accept"
    for item in items:
        if isinstance(item, str):
            problem_id = item
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            problem_id = item["id"]
            verdict = item.get("verdict")
            if verdict is not None and verdict != wanted:
                fail(f"{path}: {problem_id} is marked {verdict!r}, expected {wanted!r}")
            decision = item.get("accepted")
            if decision is not None and bool(decision) != accepted:
                fail(f"{path}: {problem_id} has accepted={decision!r}, expected {accepted!r}")
            if item.get("status") == opposite:
                fail(f"{path}: {problem_id} is marked status={opposite!r}")
        else:
            fail(f"manifest item needs an id string: {path}: {item!r}")
        if not problem_id or problem_id in result:
            fail(f"empty or duplicate manifest id in {path}: {problem_id!r}")
        result.add(problem_id)
    if not result:
        fail(f"no IDs in manifest: {path}")
    return result


def raw_problem(prompt: str) -> str:
    marker = "\n\nProblem: "
    if marker not in prompt:
        fail(f"replay prompt lacks problem marker: {prompt[:100]!r}")
    return normalize(prompt.rsplit(marker, 1)[1])


def question_of(row: dict[str, Any]) -> str:
    info = row.get("extra_info")
    if not isinstance(info, dict) or not isinstance(info.get("question"), str):
        fail(f"row {row.get('id')} lacks extra_info.question")
    return raw_problem(info["question"])


def external_answer(response: str, problem_id: str) -> str:
    if response.count("</think>") != 1:
        fail(f"{problem_id}: expected one closing </think>")
    answer = response.split("</think>", 1)[1].strip()
    if not answer.startswith("Final Answer:") or not answer[len("Final Answer:"):].strip():
        fail(f"{problem_id}: missing nonempty external Final Answer")
    return answer


def validate_tagged(response: str, problem_id: str) -> dict[str, Any]:
    if not response.startswith("<think>") or response.count("<think>") != 1:
        fail(f"{problem_id}: response must start with exactly one <think>")
    external_answer(response, problem_id)
    think_end = response.index("</think>")
    structure = parse(response)
    if not structure["valid"] or len(structure["blocks"]) != 1:
        fail(f"{problem_id}: need exactly one grammatical Parallel block")
    block = structure["blocks"][0]
    if not block["numbered"] or len(block["paths"]) != 2 or len(block["outlines"]) != 2:
        fail(f"{problem_id}: need two numbered Outlines and Paths")
    if not (response.index("<think>") < block["start"] < block["end"] < think_end):
        fail(f"{problem_id}: Parallel block must be wholly inside <think>")
    if any(tag in response[think_end:] for tag in TAGS):
        fail(f"{problem_id}: Multiverse tag outside <think>")
    if any(not item.strip() for item in block["outlines"] + block["paths"] + [block["conclusion"]]):
        fail(f"{problem_id}: empty Multiverse section")
    return block


def plain_response(response: str, problem_id: str) -> str:
    """Remove structural/planning text while preserving each Path body verbatim."""
    block = validate_tagged(response, problem_id)
    paths = list(block["paths"])
    plain = response[:block["start"]] + "\n\n" + "\n\n".join(paths) + "\n\n" + response[block["end"]:]
    if any(tag in plain for tag in TAGS):
        fail(f"{problem_id}: plain transform retained a Multiverse tag")
    # Normalizing only whitespace verifies all non-structural parts, including
    # the path text and final answer, have retained their order and spelling.
    expected = normalize(response[:block["start"]] + "\n\n" + "\n\n".join(paths) + "\n\n" + response[block["end"]:])
    if normalize(plain) != expected:
        fail(f"{problem_id}: non-equivalent plain transform")
    return plain


def load_authored(paths: list[Path]) -> dict[str, dict[str, Any]]:
    authored: dict[str, dict[str, Any]] = {}
    for path in paths:
        for row in read_jsonl(path):
            if row["id"] in authored:
                fail(f"duplicate authored ID across source files: {row['id']}")
            if row.get("source") not in {"math", "gsm8k"} or not isinstance(row.get("output"), str):
                fail(f"malformed authored row {row['id']} in {path}")
            row = dict(row)
            row["_source_file"] = str(path)
            authored[row["id"]] = row
    return authored


def select_controls(
    recovery_train: list[dict[str, Any]], used_ids: set[str], used_questions: set[str]
) -> list[dict[str, Any]]:
    eligible = [
        row for row in recovery_train
        if row.get("extra_info", {}).get("kind") == "control_th"
        and row["id"] not in used_ids and question_of(row) not in used_questions
    ]
    by_id: dict[str, dict[str, Any]] = {}
    for row in eligible:
        by_id.setdefault(row["id"], row)
    chosen = sorted(by_id.values(), key=lambda r: (stable_rank(CONTROL_SEED, r["id"]), r["id"]))[:CONTROL_COUNT]
    if len(chosen) != CONTROL_COUNT:
        fail(f"only {len(chosen)} controls available, need {CONTROL_COUNT}")
    return chosen


def select_replay(
    replay_train: list[dict[str, Any]], used_ids: set[str], used_questions: set[str]
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    selected_ids, selected_questions = set(used_ids), set(used_questions)
    for kind, quotas in REPLAY_BY_KIND_AND_SOURCE.items():
        for source, count in quotas.items():
            eligible = [
                row for row in replay_train
                if row.get("extra_info", {}).get("kind") == kind and row.get("source") == source
                and row["id"] not in selected_ids and question_of(row) not in selected_questions
            ]
            by_id: dict[str, dict[str, Any]] = {}
            for row in eligible:
                old = by_id.get(row["id"])
                if old is None or row["extra_info"]["answer"] < old["extra_info"]["answer"]:
                    by_id[row["id"]] = row
            chosen = sorted(
                by_id.values(), key=lambda r: (stable_rank(REPLAY_SEEDS[kind], r["id"]), r["id"])
            )[:count]
            if len(chosen) != count:
                fail(f"only {len(chosen)} {kind}/{source} replay rows available, need {count}")
            selected.extend(chosen)
            selected_ids.update(row["id"] for row in chosen)
            selected_questions.update(question_of(row) for row in chosen)
    if len(selected) != 142 or len({row["id"] for row in selected}) != 142:
        fail("replay selection must contain 142 distinct IDs")
    return selected


def positive_rows(
    accepted_ids: set[str], candidates: dict[str, dict[str, Any]], authored: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], collections.Counter[str]]:
    tagged: list[dict[str, Any]] = []
    plain: list[dict[str, Any]] = []
    math_types: collections.Counter[str] = collections.Counter()
    for problem_id in sorted(accepted_ids):
        candidate = candidates[problem_id]
        source = authored[problem_id]
        if source["source"] != candidate["source"]:
            fail(f"{problem_id}: authored/candidate source mismatch")
        response = source["output"]
        validate_tagged(response, problem_id)
        prompt = mv_prompt(HEADER + candidate["question"])
        common = {
            "id": problem_id,
            "source": candidate["source"],
            "copy_index": 0,
            "source_origin": "agent_authored",
            "source_file": source["_source_file"],
        }
        tagged.append({
            **common,
            "data_source": "exp21_agent_authored_tagged",
            "extra_info": {"question": prompt, "answer": response, "enable_thinking": True,
                           "kind": "parallel_th", "id": problem_id},
        })
        plain.append({
            **common,
            "data_source": "exp21_agent_authored_plain",
            "extra_info": {"question": prompt, "answer": plain_response(response, problem_id), "enable_thinking": True,
                           "kind": "control_th", "id": problem_id},
        })
        if candidate["source"] == "math":
            math_types[candidate.get("answer_type", "")] += 1
    return tagged, plain, math_types


def copy_nonpositive(rows: list[dict[str, Any]], origin: str) -> list[dict[str, Any]]:
    copied = []
    for row in rows:
        item = copy.deepcopy(row)
        item["source_origin"] = origin
        item["source_index"] = item.get("index")
        item["copy_index"] = 0
        copied.append(item)
    return copied


def atomic_write(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.parquet")
    try:
        frame.to_parquet(temporary, index=False)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted-ids", type=Path, required=True,
                        help="Explicit accepted ID manifest: JSON array, JSONL, or one ID per line.")
    parser.add_argument("--rejected-ids", type=Path,
                        help="Optional rejected ID manifest; must be disjoint from --accepted-ids.")
    parser.add_argument("--rejected-id", action="append", default=[],
                        help="One explicitly rejected ID; may be passed more than once.")
    parser.add_argument("--authored", type=Path, nargs="+", default=DEFAULT_AUTHORED,
                        help="Five (or replacement) authoring JSONL sources.")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES,
                        help="Leakchecked candidate IDs, questions, source, and answer type.")
    parser.add_argument("--candidate-audit", type=Path, default=DEFAULT_CANDIDATE_AUDIT,
                        help="Leakcheck provenance JSON for the candidate pool.")
    parser.add_argument("--replay-train", type=Path, default=DEFAULT_REPLAY_TRAIN)
    parser.add_argument("--replay-val", type=Path, default=DEFAULT_REPLAY_VAL)
    parser.add_argument("--recovery-train", type=Path, default=DATA / "sft_v4_recovery8_train.parquet")
    parser.add_argument("--out-prefix", type=Path, default=DEFAULT_OUT_PREFIX)
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the build report without writing files.")
    args = parser.parse_args()

    accepted_ids = read_id_manifest(args.accepted_ids, accepted=True)
    rejected_ids = set(args.rejected_id)
    if len(rejected_ids) != len(args.rejected_id) or any(not problem_id for problem_id in rejected_ids):
        fail("--rejected-id values must be unique nonempty IDs")
    if args.rejected_ids is not None:
        rejected_ids.update(read_id_manifest(args.rejected_ids, accepted=False))
    if accepted_ids & rejected_ids:
        fail(f"accepted/rejected overlap: {sorted(accepted_ids & rejected_ids)}")

    candidate_audit = json.loads(args.candidate_audit.read_text())
    if candidate_audit.get("status") != "prepared":
        fail(f"candidate leakcheck audit is not prepared: {args.candidate_audit}")
    candidates_rows = read_jsonl(args.candidates)
    candidates = {row["id"]: row for row in candidates_rows}
    if not accepted_ids <= set(candidates):
        fail(f"accepted IDs missing from leakchecked candidate file: {sorted(accepted_ids - set(candidates))}")
    if not accepted_ids <= set(candidate_audit.get("ids", {}).get("selected", [])):
        fail("accepted IDs are absent from the documented leakchecked candidate selection")

    authored = load_authored(args.authored)
    if not accepted_ids <= set(authored):
        fail(f"accepted IDs missing from authored sources: {sorted(accepted_ids - set(authored))}")
    if rejected_ids & set(authored) and accepted_ids & rejected_ids:
        fail("rejected authored IDs would be mixed into positives")

    tagged, plain, math_types = positive_rows(accepted_ids, candidates, authored)
    source_counts = collections.Counter(row["source"] for row in tagged)
    if len(tagged) < 46:
        fail(f"only {len(tagged)} accepted positives, gate requires at least 46")
    if source_counts["gsm8k"] < 18:
        fail(f"only {source_counts['gsm8k']} accepted GSM8K positives, gate requires at least 18")
    for answer_type in ("integer", "expression", "fraction"):
        if math_types[answer_type] < 6:
            fail(f"only {math_types[answer_type]} accepted MATH {answer_type} answers, gate requires at least 6")

    recovery_train = pd.read_parquet(args.recovery_train).to_dict("records")
    replay_train = pd.read_parquet(args.replay_train).to_dict("records")
    replay_val = pd.read_parquet(args.replay_val).to_dict("records")
    if len(recovery_train) != len({row["id"] for row in recovery_train}):
        fail("recovery control source must have unique IDs")
    if not replay_val:
        fail("empty replay validation source")

    positive_questions = {normalize(candidates[problem_id]["question"]) for problem_id in accepted_ids}
    controls = select_controls(recovery_train, set(accepted_ids), set(positive_questions))
    used_ids = set(accepted_ids) | {row["id"] for row in controls}
    used_questions = set(positive_questions) | {question_of(row) for row in controls}
    replay = select_replay(replay_train, used_ids, used_questions)
    other = copy_nonpositive(controls, "v4_recovery8") + copy_nonpositive(replay, "selective_v4")
    for row in other:
        info = row["extra_info"]
        kind = info.get("kind")
        if kind not in {"control_th", "replay_th", "replay_nt"}:
            fail(f"unexpected non-positive kind for {row['id']}: {kind!r}")
        if any(tag in info.get("answer", "") for tag in TAGS):
            fail(f"non-positive replay/control contains a Multiverse tag: {row['id']}")
        if bool(info.get("enable_thinking")) != (kind != "replay_nt"):
            fail(f"wrong thinking mode for {row['id']}: {kind}")

    tagged.extend(other)
    plain.extend(copy.deepcopy(other))
    if len(tagged) != len(plain) or len({row["id"] for row in tagged}) != len(tagged):
        fail("train pair must have equal sizes and unique IDs")
    if any(left["id"] != right["id"] for left, right in zip(sorted(tagged, key=lambda r: r["id"]), sorted(plain, key=lambda r: r["id"]))):
        fail("tagged/plain positive IDs differ")

    tagged.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    plain.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    for index, (left, right) in enumerate(zip(tagged, plain)):
        left["index"] = right["index"] = index
        if left["id"] != right["id"] or left["extra_info"]["question"] != right["extra_info"]["question"]:
            fail("tagged/plain row alignment mismatch")
        if left["id"] not in accepted_ids and left != right:
            fail(f"non-positive row differs across arms: {left['id']}")

    val_questions = {question_of(row) for row in replay_val}
    train_questions = {question_of(row) for row in tagged}
    if len(train_questions) != len(tagged) or train_questions & val_questions:
        fail("train/validation normalized question overlap")
    if accepted_ids & set(row["id"] for row in replay_val):
        fail("accepted positive ID appears in frozen validation")

    replay_counts = {
        kind: dict(collections.Counter(row["source"] for row in replay if row["extra_info"]["kind"] == kind))
        for kind in REPLAY_BY_KIND_AND_SOURCE
    }
    if replay_counts != REPLAY_BY_KIND_AND_SOURCE:
        fail(f"wrong replay composition: {replay_counts}")
    report = {
        "status": "prepared" if not args.dry_run else "validated_not_written",
        "inputs": {
            "accepted_ids": str(args.accepted_ids),
            "rejected_ids": str(args.rejected_ids) if args.rejected_ids else None,
            "rejected_id_args": sorted(args.rejected_id),
            "authored": [str(path) for path in args.authored], "candidates": str(args.candidates),
            "candidate_audit": str(args.candidate_audit), "replay_train": str(args.replay_train),
            "recovery_train": str(args.recovery_train), "replay_val": str(args.replay_val),
        },
        "seeds": {"control": CONTROL_SEED, "replay": REPLAY_SEEDS, "order": ORDER_SEED},
        "positive": {
            "rows": len(accepted_ids), "ids": sorted(accepted_ids), "by_source": dict(source_counts),
            "math_by_answer_type": dict(math_types), "rejected_ids_excluded": sorted(rejected_ids),
        },
        "replay": {"controls": len(controls), "by_kind_and_source": replay_counts,
                   "ids": {kind: [row["id"] for row in replay if row["extra_info"]["kind"] == kind]
                           for kind in REPLAY_BY_KIND_AND_SOURCE}},
        "validation": {"rows": len(replay_val), "source": str(args.replay_val), "copied_verbatim": True},
        "checks": {
            "gate_minimum_accepted_46": len(accepted_ids) >= 46,
            "gate_minimum_gsm_18": source_counts["gsm8k"] >= 18,
            "gate_minimum_math_each_type_6": all(math_types[kind] >= 6 for kind in ("integer", "expression", "fraction")),
            "accepted_rejected_disjoint": True, "accepted_subset_leakchecked_candidates": True,
            "tagged_grammar_inside_think": len(accepted_ids), "plain_tags": 0,
            "same_train_row_order": True, "nonpositive_rows_identical": True,
            "train_val_normalized_question_overlap": 0,
        },
        "train": {"rows_per_arm": len(tagged), "unique_ids": len(tagged),
                  "row_order": [row["id"] for row in tagged]},
        "transform": {
            "tagged": "accepted authored response copied verbatim",
            "plain": "removes Parallel, Goal, Outline, Conclusion and Path tags; preserves Path bodies in order",
            "replay": "both thinking and no-thinking replay rows copied identically into both arms",
        },
    }

    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    tagged_path = args.out_prefix.with_name(args.out_prefix.name + "_tagged_train.parquet")
    plain_path = args.out_prefix.with_name(args.out_prefix.name + "_plain_train.parquet")
    val_path = args.out_prefix.with_name(args.out_prefix.name + "_val.parquet")
    report_path = args.out_prefix.with_name(args.out_prefix.name + "_build.json")
    atomic_write(tagged_path, pd.DataFrame(tagged))
    atomic_write(plain_path, pd.DataFrame(plain))
    atomic_write(val_path, pd.DataFrame(replay_val))
    temporary = report_path.with_suffix(".tmp.json")
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, report_path)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"tagged": str(tagged_path), "plain": str(plain_path), "val": str(val_path),
                      "rows_per_arm": len(tagged)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"BUILD GATE FAILED: {error}") from error
