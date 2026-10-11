#!/usr/bin/env python3
"""Build CPU-only matched tagged/plain SFT data from screened Sol 6.1 traces."""
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
DEFAULT_REPLAY = DATA / "sft_selective_blocks_v4_train.parquet"
DEFAULT_RECOVERY_TRAIN = DATA / "sft_v4_recovery8_train.parquet"
DEFAULT_RECOVERY_VAL = DATA / "sft_v4_recovery8_val.parquet"
DEFAULT_PREFIX = DATA / "sft_teacher"
CONTROL_COUNT = 45
QUOTAS = {"replay_th": {"math": 36, "gsm8k": 22, "arc": 13},
          "replay_nt": {"math": 36, "gsm8k": 22, "arc": 13}}
SEEDS = {"control": "teacher-sol61-control-20261012",
         "replay_th": "teacher-sol61-replay-th-20261012",
         "replay_nt": "teacher-sol61-replay-nt-20261012",
         "order": "teacher-sol61-order-20261012"}
YES = {"accept", "accepted", "accepted_for_sft", "screened_accepted"}
NO = {"reject", "rejected", "proposal_not_accepted", "candidate_not_accepted"}


class GateError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise GateError(message)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def rank(seed: str, item: str) -> str:
    return hashlib.sha256(f"{seed}\0{item}".encode()).hexdigest()


def read_rows(path: Path, label: str) -> list[dict[str, Any]]:
    """Accept JSONL, a JSON list, or a JSON object containing rows/records."""
    if not path.is_file():
        fail(f"missing {label}: {path}")
    text = path.read_text().strip()
    if not text:
        fail(f"empty {label}: {path}")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, list):
        rows = parsed
    elif isinstance(parsed, dict):
        rows = next((parsed[key] for key in ("rows", "records", "accepted", "items") if isinstance(parsed.get(key), list)), None)
        if rows is None:
            fail(f"JSON {label} needs rows, records, accepted, or items: {path}")
    elif parsed is None:
        rows = []
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                fail(f"invalid JSON in {label} at {path}:{lineno}: {error}")
    else:
        fail(f"unsupported {label} format: {path}")
    if not rows or any(not isinstance(row, dict) or not isinstance(row.get("id"), str) for row in rows):
        fail(f"{label} needs nonempty object rows with string id: {path}")
    if len(rows) != len({row["id"] for row in rows}):
        fail(f"duplicate IDs in {label}: {path}")
    return [dict(row) for row in rows]


def review_decision(row: dict[str, Any], context: str) -> bool:
    votes: list[bool] = []
    if "accepted" in row:
        if type(row["accepted"]) is not bool:
            fail(f"{context} {row['id']}: accepted must be boolean")
        votes.append(row["accepted"])
    for field in ("verdict", "status"):
        value = row.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            fail(f"{context} {row['id']}: {field} must be a string")
        value = value.strip().lower()
        if value in YES:
            votes.append(True)
        elif value in NO:
            votes.append(False)
        else:
            fail(f"{context} {row['id']}: unsupported {field}={value!r}")
    if not votes:
        fail(f"{context} {row['id']}: missing explicit accept/reject decision")
    if len(set(votes)) != 1:
        fail(f"{context} {row['id']}: conflicting acceptance fields")
    return votes[0]


def from_screens(proposals: list[dict[str, Any]], screens: list[Path]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not screens:
        fail("--proposals requires one or more --screens files")
    source = {row["id"]: row for row in proposals}
    decisions: dict[str, tuple[bool, Path]] = {}
    missing_proposals: list[str] = []
    for path in screens:
        for row in read_rows(path, "screen"):
            problem_id = row["id"]
            accepted = review_decision(row, f"screen {path}")
            if problem_id in decisions:
                fail(f"duplicate screen decision for {problem_id}: {decisions[problem_id][1]} and {path}")
            decisions[problem_id] = (accepted, path)
            if problem_id not in source:
                missing_proposals.append(problem_id)
    selected = [source[problem_id] for problem_id, (accepted, _) in sorted(decisions.items()) if accepted and problem_id in source]
    if not selected:
        fail("screen files contain no accepted IDs")
    return selected, {"mode": "converter_proposals_plus_screens", "screen_paths": [str(path) for path in screens],
                      "screened_rows": len(decisions), "rejected_ids": sorted(problem_id for problem_id, (accepted, _) in decisions.items() if not accepted),
                      "screened_ids_without_converter_proposal": sorted(missing_proposals)}


def question_of(row: dict[str, Any]) -> str:
    info = row.get("extra_info")
    if not isinstance(info, dict) or not isinstance(info.get("question"), str):
        fail(f"replay row {row.get('id')}: missing extra_info.question")
    marker = "\n\nProblem: "
    if marker not in info["question"]:
        fail(f"replay row {row['id']}: question lacks Problem marker")
    return norm(info["question"].rsplit(marker, 1)[1])


def tagged_block(response: str, problem_id: str) -> dict[str, Any]:
    if not response.startswith("<think>") or response.count("<think>") != 1 or response.count("</think>") != 1:
        fail(f"{problem_id}: response needs exactly one leading think section")
    external = response.split("</think>", 1)[1].strip()
    if not external.startswith("Final Answer:") or not external[len("Final Answer:"):].strip():
        fail(f"{problem_id}: missing external Final Answer")
    structure = parse(response)
    if not structure["valid"] or len(structure["blocks"]) != 1:
        fail(f"{problem_id}: need one grammatical Parallel block")
    block = structure["blocks"][0]
    if not block["numbered"] or len(block["paths"]) < 2 or len(block["paths"]) != len(block["outlines"]):
        fail(f"{problem_id}: need matching numbered Outlines and at least two Paths")
    think_end = response.index("</think>")
    if not (response.index("<think>") < block["start"] < block["end"] < think_end):
        fail(f"{problem_id}: Parallel block is outside think")
    if any(tag in response[think_end:] for tag in TAGS) or any(not part.strip() for part in block["paths"] + block["outlines"] + [block["conclusion"]]):
        fail(f"{problem_id}: invalid tag placement or empty section")
    return block


def make_plain(response: str, problem_id: str) -> str:
    block = tagged_block(response, problem_id)
    plain = response[:block["start"]] + "\n\n" + "\n\n".join(block["paths"]) + "\n\n" + response[block["end"]:]
    if any(tag in plain for tag in TAGS):
        fail(f"{problem_id}: plain transform retained Multiverse markup")
    return plain


def verify_teacher(row: dict[str, Any]) -> None:
    problem_id = row["id"]
    if row.get("teacher") != "sol61" or row.get("source") not in {"math", "gsm8k"}:
        fail(f"{problem_id}: expected Sol 6.1 math/gsm8k row")
    if any(not isinstance(row.get(field), str) or not row[field].strip() for field in ("question", "answer", "response")):
        fail(f"{problem_id}: missing question, answer, or response")
    source = row.get("teacher_source")
    if not isinstance(source, dict) or not isinstance(source.get("raw_file"), str) or not isinstance(source.get("leakcheck_summary"), str):
        fail(f"{problem_id}: missing teacher source provenance")
    for field in ("raw_file", "leakcheck_summary"):
        relative = Path(source[field])
        path = ROOT / relative
        if relative.is_absolute() or not path.is_file():
            fail(f"{problem_id}: missing provenance file {source[field]!r}")
    try:
        leak = json.loads((ROOT / source["leakcheck_summary"]).read_text())
    except json.JSONDecodeError as error:
        fail(f"{problem_id}: invalid provenance leakcheck: {error}")
    keys = [key for key in ("n_leaky_vs_our_evals", "n_dup_vs_our_evals", "n_dup_or_variant_vs_our_evals") if key in leak]
    if not keys or any(leak[key] != 0 for key in keys):
        fail(f"{problem_id}: source leakcheck is not clean")
    tagged_block(row["response"], problem_id)


def select_controls(rows: list[dict[str, Any]], used_ids: set[str], used_questions: set[str]) -> list[dict[str, Any]]:
    eligible = [row for row in rows if row.get("extra_info", {}).get("kind") == "control_th" and row["id"] not in used_ids and question_of(row) not in used_questions]
    chosen = sorted({row["id"]: row for row in eligible}.values(), key=lambda row: (rank(SEEDS["control"], row["id"]), row["id"]))[:CONTROL_COUNT]
    if len(chosen) != CONTROL_COUNT:
        fail(f"only {len(chosen)} recovery8 controls available, need {CONTROL_COUNT}")
    return chosen


def select_replay(rows: list[dict[str, Any]], used_ids: set[str], used_questions: set[str]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    ids, questions = set(used_ids), set(used_questions)
    for kind, quotas in QUOTAS.items():
        for source, count in quotas.items():
            eligible = [row for row in rows if row.get("extra_info", {}).get("kind") == kind and row.get("source") == source and row["id"] not in ids and question_of(row) not in questions]
            unique: dict[str, dict[str, Any]] = {}
            for row in eligible:
                if row["id"] not in unique or row["extra_info"]["answer"] < unique[row["id"]]["extra_info"]["answer"]:
                    unique[row["id"]] = row
            chosen = sorted(unique.values(), key=lambda row: (rank(SEEDS[kind], row["id"]), row["id"]))[:count]
            if len(chosen) != count:
                fail(f"only {len(chosen)} {kind}/{source} rows available, need {count}")
            selected.extend(chosen)
            ids.update(row["id"] for row in chosen)
            questions.update(question_of(row) for row in chosen)
    if len(selected) != 142 or len({row["id"] for row in selected}) != 142:
        fail("replay selection must contain 142 distinct IDs")
    return selected


def copy_rows(rows: list[dict[str, Any]], origin: str) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        item = copy.deepcopy(row)
        item.update(source_origin=origin, source_index=item.get("index"), copy_index=0)
        result.append(item)
    return result


def write_parquet(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.parquet")
    try:
        pd.DataFrame(rows).to_parquet(temporary, index=False)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--accepted", type=Path, help="Full explicit accepted rows.")
    group.add_argument("--proposals", type=Path, help="Converter proposals requiring --screens.")
    parser.add_argument("--screens", type=Path, nargs="*", default=[])
    parser.add_argument("--min-accepted", type=int, default=150)
    parser.add_argument("--replay-train", type=Path, default=DEFAULT_REPLAY)
    parser.add_argument("--recovery-train", type=Path, default=DEFAULT_RECOVERY_TRAIN)
    parser.add_argument("--recovery-val", type=Path, default=DEFAULT_RECOVERY_VAL)
    parser.add_argument("--out-prefix", type=Path, default=DEFAULT_PREFIX)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.min_accepted < 1:
        fail("--min-accepted must be positive")
    if args.proposals:
        accepted, acceptance = from_screens(read_rows(args.proposals, "converter proposals"), args.screens)
        input_path = args.proposals
    else:
        if args.screens:
            fail("--screens is only valid with --proposals")
        accepted = read_rows(args.accepted, "accepted trajectories")
        rejected = [row["id"] for row in accepted if not review_decision(row, "accepted trajectories")]
        if rejected:
            fail(f"--accepted contains rejected rows: {rejected}")
        acceptance = {"mode": "ready_accepted_rows", "screen_paths": [], "screened_rows": len(accepted), "rejected_ids": []}
        input_path = args.accepted
    if len(accepted) < args.min_accepted:
        fail(f"only {len(accepted)} accepted positives, need at least {args.min_accepted}")
    if len({row["id"] for row in accepted}) != len(accepted):
        fail("duplicate accepted IDs")

    tagged, plain = [], []
    for row in sorted(accepted, key=lambda item: item["id"]):
        verify_teacher(row)
        problem_id = row["id"]
        prompt = mv_prompt(HEADER + row["question"])
        common = {"id": problem_id, "source": row["source"], "copy_index": 0, "source_origin": "teacher_sol61", "source_file": row["teacher_source"]["raw_file"]}
        tagged.append({**common, "data_source": "exp21_teacher_sol61_tagged", "extra_info": {"question": prompt, "answer": row["response"], "enable_thinking": True, "kind": "parallel_th", "id": problem_id}})
        plain.append({**common, "data_source": "exp21_teacher_sol61_plain", "extra_info": {"question": prompt, "answer": make_plain(row["response"], problem_id), "enable_thinking": True, "kind": "control_th", "id": problem_id}})
    accepted_ids = {row["id"] for row in accepted}
    accepted_questions = {norm(row["question"]) for row in accepted}
    if len(accepted_questions) != len(accepted):
        fail("accepted positives have duplicate normalized questions")

    recovery = pd.read_parquet(args.recovery_train).to_dict("records")
    replay_source = pd.read_parquet(args.replay_train).to_dict("records")
    validation = pd.read_parquet(args.recovery_val).to_dict("records")
    if not validation or len(recovery) != len({row["id"] for row in recovery}):
        fail("recovery8 source is empty or has duplicate IDs")
    controls = select_controls(recovery, accepted_ids, accepted_questions)
    replay = select_replay(replay_source, accepted_ids | {row["id"] for row in controls}, accepted_questions | {question_of(row) for row in controls})
    other = copy_rows(controls, "v4_recovery8") + copy_rows(replay, "selective_v4")
    for row in other:
        kind = row.get("extra_info", {}).get("kind")
        if kind not in {"control_th", "replay_th", "replay_nt"} or any(tag in row["extra_info"].get("answer", "") for tag in TAGS):
            fail(f"bad nonpositive row: {row['id']}")
        if bool(row["extra_info"].get("enable_thinking")) != (kind != "replay_nt"):
            fail(f"wrong thinking mode: {row['id']}")
    tagged.extend(other)
    plain.extend(copy.deepcopy(other))
    if len(tagged) != len(plain) or len({row["id"] for row in tagged}) != len(tagged):
        fail("paired train rows must have equal size and unique IDs")
    tagged.sort(key=lambda row: (rank(SEEDS["order"], row["id"]), row["id"]))
    plain.sort(key=lambda row: (rank(SEEDS["order"], row["id"]), row["id"]))
    for index, (left, right) in enumerate(zip(tagged, plain)):
        left["index"] = right["index"] = index
        if left["id"] != right["id"] or left["extra_info"]["question"] != right["extra_info"]["question"]:
            fail("tagged/plain IDs, order, or prompts differ")
        if left["id"] not in accepted_ids and left != right:
            fail(f"nonpositive differs across arms: {left['id']}")
    train_questions, val_questions = {question_of(row) for row in tagged}, {question_of(row) for row in validation}
    if len(train_questions) != len(tagged) or train_questions & val_questions or accepted_ids & {row["id"] for row in validation}:
        fail("train/validation ID or normalized question overlap")
    replay_counts = {kind: dict(collections.Counter(row["source"] for row in replay if row["extra_info"]["kind"] == kind)) for kind in QUOTAS}
    if replay_counts != QUOTAS:
        fail(f"wrong replay composition: {replay_counts}")
    report = {
        "status": "validated_not_written" if args.dry_run else "prepared",
        "inputs": {"accepted_or_proposals": str(input_path), "replay_train": str(args.replay_train),
                   "recovery_train": str(args.recovery_train), "recovery_val": str(args.recovery_val)},
        "acceptance": acceptance, "minimum_accepted": args.min_accepted, "seeds": SEEDS,
        "positive": {"rows": len(accepted), "ids": sorted(accepted_ids),
                     "by_source": dict(collections.Counter(row["source"] for row in accepted))},
        "replay": {"controls": len(controls), "by_kind_and_source": replay_counts,
                   "ids": {kind: [row["id"] for row in replay if row["extra_info"]["kind"] == kind]
                           for kind in QUOTAS}},
        "validation": {"rows": len(validation), "source": str(args.recovery_val), "copied_verbatim": True},
        "train": {"rows_per_arm": len(tagged), "unique_ids": len(tagged),
                  "row_order": [row["id"] for row in tagged]},
        "checks": {"accepted_count_meets_minimum": True, "sol61_provenance_and_clean_leakcheck": len(accepted),
                   "tagged_grammar_inside_think": len(accepted), "plain_tags": 0,
                   "same_train_row_order_and_prompts": True, "nonpositive_rows_identical": True,
                   "train_val_normalized_question_overlap": 0},
        "transform": {"tagged": "accepted converter response copied verbatim",
                      "plain": "removes Parallel plan/container markup and retains Path bodies in order",
                      "replay": "recovery8 controls and v4 replay copied identically into both arms"},
    }
    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    paths = {"tagged": args.out_prefix.with_name(args.out_prefix.name + "_tagged_train.parquet"), "plain": args.out_prefix.with_name(args.out_prefix.name + "_plain_train.parquet"), "val": args.out_prefix.with_name(args.out_prefix.name + "_val.parquet"), "report": args.out_prefix.with_name(args.out_prefix.name + "_build.json")}
    write_parquet(paths["tagged"], tagged)
    write_parquet(paths["plain"], plain)
    write_parquet(paths["val"], validation)
    temporary = paths["report"].with_suffix(".tmp.json")
    try:
        paths["report"].parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, paths["report"])
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"tagged": str(paths["tagged"]), "plain": str(paths["plain"]), "val": str(paths["val"]), "rows_per_arm": len(tagged)}))


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"BUILD GATE FAILED: {error}") from error
