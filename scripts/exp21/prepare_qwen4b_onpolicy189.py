#!/usr/bin/env python3
"""Select fresh 189-task Qwen4B masked on-policy candidates on CPU only."""

import argparse
import collections
import importlib.util
import json
import os
import re
import tarfile
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
OUT = DATA / "qwen4b_onpolicy189_candidates.jsonl"
PILOT = RUN / "eval_archives/onpolicy46_pilot128/rollouts.jsonl"
FIXED40 = RUN / "eval_archives/qwen4b_init_fixed40.tgz"
SOURCE_AUDIT = DATA / "onpolicy46_candidates.audit.json"
MARKER = "\n\nProblem: "
SOURCES = ("math", "gsm8k")
TARGET = {"math": 94, "gsm8k": 95}
QWEN_PAIRS = {
    "focus34": (DATA / "qwen4b_focus34_tagged_train.parquet",
                DATA / "qwen4b_focus34_tagged_val.parquet",
                DATA / "qwen4b_focus34_plain_train.parquet",
                DATA / "qwen4b_focus34_plain_val.parquet"),
    "mixed401": (DATA / "qwen4b_mixed401_tagged_train.parquet",
                 DATA / "qwen4b_mixed401_tagged_val.parquet",
                 DATA / "qwen4b_mixed401_plain_train.parquet",
                 DATA / "qwen4b_mixed401_plain_val.parquet"),
}


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split()).casefold()


def read_jsonl(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = []
    with path.open() as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank JSONL line: {path}:{number}")
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSON object required: {path}:{number}")
            rows.append(value)
    if not rows:
        raise ValueError(f"empty JSONL: {path}")
    return rows


def problem_from_prompt(prompt, path):
    if not isinstance(prompt, str) or MARKER not in prompt:
        raise ValueError(f"missing final Problem marker in {path}")
    text = prompt.rsplit(MARKER, 1)[1]
    text = text.split("<|im_end|>", 1)[0]
    text = text.split("<|endoftext|>", 1)[0]
    if not text.strip():
        raise ValueError(f"empty problem after marker in {path}")
    return normalize(text)


def unique(name, values):
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {name}")


def candidate_rows(path):
    rows = read_jsonl(path)
    required = ("id", "source", "question", "answer", "answer_type")
    if any(any(not isinstance(row.get(key), str) or not row[key].strip() for key in required) for row in rows):
        raise ValueError("malformed source candidate")
    if any(row["source"] not in SOURCES for row in rows):
        raise ValueError("candidate source outside MATH/GSM8K")
    unique("candidate IDs", [row["id"] for row in rows])
    unique("candidate normalized questions", [normalize(row["question"]) for row in rows])
    if collections.Counter(row["source"] for row in rows) != {"math": 128, "gsm8k": 128}:
        raise ValueError("source candidate pool is not 128 MATH plus 128 GSM8K")
    return rows


def pilot_rows(path, candidates_by_id):
    rows = read_jsonl(path)
    if len(rows) != 128:
        raise ValueError("onpolicy46 pilot must contain 128 rollouts")
    ids, questions = [], []
    for row in rows:
        if not isinstance(row.get("id"), str) or row["id"] not in candidates_by_id:
            raise ValueError("pilot row lacks a source candidate ID")
        question = problem_from_prompt(row.get("input"), path)
        source = candidates_by_id[row["id"]]
        if question != normalize(source["question"]):
            raise ValueError(f"pilot prompt differs from source candidate: {row['id']}")
        ids.append(row["id"])
        questions.append(question)
    if len(set(ids)) != 64 or len(set(questions)) != 64:
        raise ValueError("pilot must represent exactly 64 unique IDs and questions")
    if collections.Counter(candidates_by_id[identifier]["source"] for identifier in set(ids)) != {"math": 32, "gsm8k": 32}:
        raise ValueError("pilot must have 32 MATH plus 32 GSM8K unique tasks")
    return set(ids), set(questions)


def parquet_questions(path, candidates_by_id):
    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_parquet(path)
    if "id" not in frame:
        raise ValueError(f"missing id column: {path}")
    ids = {str(value) for value in frame["id"]}
    questions = set()
    if "extra_info" not in frame:
        if set(frame.columns) != {"id"}:
            raise ValueError(f"cannot recover question from {path}: {list(frame.columns)}")
        for identifier in ids:
            if identifier not in candidates_by_id:
                continue
            questions.add(normalize(candidates_by_id[identifier]["question"]))
    else:
        for info in frame["extra_info"]:
            if not isinstance(info, dict) or not isinstance(info.get("question"), str):
                raise ValueError(f"invalid extra_info.question: {path}")
            questions.add(normalize(info["question"]))
            questions.add(problem_from_prompt(info["question"], path))
    return ids, questions, len(frame)


def paired_qwen_questions(candidates_by_id):
    groups = {}
    for name, paths in QWEN_PAIRS.items():
        loaded = [parquet_questions(path, candidates_by_id) for path in paths]
        tagged_train, tagged_val, plain_train, plain_val = loaded
        for label, tagged, plain in (("train", tagged_train, plain_train), ("val", tagged_val, plain_val)):
            if tagged[:2] != plain[:2]:
                raise ValueError(f"{name} tagged/plain {label} provenance differs")
        groups[name] = {
            "ids": set().union(*(part[0] for part in loaded)),
            "questions": set().union(*(part[1] for part in loaded)),
            "rows_by_file": {str(path): count for path, (_, _, count) in zip(paths, loaded)},
        }
    return groups


def fixed40_questions(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    ids, questions, members = [], [], []
    with tarfile.open(path) as archive:
        names = sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl"))
        if len(names) != 4:
            raise ValueError(f"fixed40 requires four block-row files, got {names}")
        for name in names:
            handle = archive.extractfile(name)
            if handle is None:
                raise ValueError(f"cannot read {name} from {path}")
            members.append(name)
            for line in handle:
                row = json.loads(line)
                if not isinstance(row.get("problem_id"), str) or not isinstance(row.get("problem"), str):
                    raise ValueError(f"invalid fixed40 row in {name}")
                ids.append(row["problem_id"])
                questions.append(problem_from_prompt(row["problem"], f"{path}:{name}"))
    if len(ids) != 40:
        raise ValueError("fixed40 must contain 40 rows")
    unique("fixed40 IDs", ids)
    unique("fixed40 questions", questions)
    return set(ids), set(questions), members


def recorded_sft_questions(path, candidates_by_id):
    audit = json.loads(path.read_text())
    files = [Path(item) for item in audit.get("inputs", {}).get("sft_files", [])]
    if len(files) != 78:
        raise ValueError("onpolicy46 provenance must list 78 SFT files")
    questions, ids, counts = set(), set(), {}
    for file in files:
        file_ids, file_questions, count = parquet_questions(file, candidates_by_id)
        ids.update(file_ids)
        questions.update(file_questions)
        counts[str(file)] = count
    return ids, questions, counts


def load_leakcheck(path, corpus):
    if not path.is_file() or not corpus.is_dir():
        raise FileNotFoundError(f"leakcheck={path}, eval_corpus={corpus}")
    spec = importlib.util.spec_from_file_location("qwen4b_onpolicy189_leakcheck", path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Corpus(str(corpus))


def leak_summary(corpus, rows):
    blocking, signal_sets = [], collections.Counter()
    for row in rows:
        hits = corpus.check(row["question"], row["answer"])
        for hit in hits:
            signal_sets[hit["eval_set"]] += 1
            blocked = (("(info)" not in hit["eval_set"] and hit.get("leak")) or
                       (hit["eval_set"] == "math_test_full(info)" and hit.get("tier") in ("dup", "variant")))
            if blocked:
                blocking.append({"id": row["id"], "eval_set": hit["eval_set"], "tier": hit.get("tier")})
    if blocking:
        raise ValueError(f"selected candidates leak into eval corpus: {blocking[:5]}")
    return {"checked_candidates": len(rows), "blocking_hits": 0,
            "signals_by_eval_set": dict(sorted(signal_sets.items())),
            "contract": "reject non-info leak and math_test_full(info) dup or variant"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DATA / "onpolicy46_candidates.jsonl")
    parser.add_argument("--pilot", type=Path, default=PILOT)
    parser.add_argument("--fixed40", type=Path, default=FIXED40)
    parser.add_argument("--source-audit", type=Path, default=SOURCE_AUDIT)
    parser.add_argument("--leakcheck", type=Path, required=True)
    parser.add_argument("--eval-corpus", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    audit_path = args.out.with_suffix(".audit.json")
    if args.out.exists() or audit_path.exists():
        raise FileExistsError(f"refusing to overwrite {args.out} or {audit_path}")

    candidates = candidate_rows(args.candidates)
    candidates_by_id = {row["id"]: row for row in candidates}
    candidate_questions = {normalize(row["question"]) for row in candidates}
    pilot_ids, pilot_questions = pilot_rows(args.pilot, candidates_by_id)
    fixed_ids, fixed_questions, fixed_members = fixed40_questions(args.fixed40)
    qwen = paired_qwen_questions(candidates_by_id)
    prior_sft_ids, prior_sft_questions, prior_sft_counts = recorded_sft_questions(args.source_audit, candidates_by_id)

    exclusions = {
        "onpolicy46_pilot128": {"ids": pilot_ids, "questions": pilot_questions},
        "qwen4b_focus34_tagged_plain_train_val": qwen["focus34"],
        "qwen4b_mixed401_tagged_plain_train_val": qwen["mixed401"],
        "qwen4b_init_fixed40": {"ids": fixed_ids, "questions": fixed_questions},
        "onpolicy46_recorded_sft_provenance": {"ids": prior_sft_ids, "questions": prior_sft_questions},
    }
    excluded = collections.defaultdict(set)
    selected = []
    for row in candidates:  # source order is final order
        question = normalize(row["question"])
        reasons = [name for name, values in exclusions.items()
                   if row["id"] in values["ids"] or question in values["questions"]]
        if reasons:
            for reason in reasons:
                excluded[reason].add(row["id"])
        else:
            selected.append(row)

    if len(selected) != sum(TARGET.values()):
        raise ValueError(f"expected {sum(TARGET.values())} selected rows, got {len(selected)}")
    if collections.Counter(row["source"] for row in selected) != TARGET:
        raise ValueError(f"source quotas differ: {collections.Counter(row['source'] for row in selected)}")
    unique("selected IDs", [row["id"] for row in selected])
    unique("selected normalized questions", [normalize(row["question"]) for row in selected])
    for name, values in exclusions.items():
        if ({row["id"] for row in selected} & values["ids"] or
                {normalize(row["question"]) for row in selected} & values["questions"]):
            raise AssertionError(f"selected collision with {name}")
    if not candidate_questions >= {normalize(row["question"]) for row in selected}:
        raise AssertionError("selected question absent from source pool")

    leak = leak_summary(load_leakcheck(args.leakcheck, args.eval_corpus), selected)
    audit = {
        "status": "prepared_cpu_only",
        "selection_order": "original onpolicy46_candidates.jsonl order",
        "inputs": {"candidates": str(args.candidates.resolve()), "pilot": str(args.pilot.resolve()),
                   "fixed40": str(args.fixed40.resolve()), "source_audit": str(args.source_audit.resolve()),
                   "leakcheck": str(args.leakcheck.resolve()), "eval_corpus": str(args.eval_corpus.resolve())},
        "counts": {"source_candidates": len(candidates), "selected": len(selected),
                   "selected_by_source": dict(sorted(collections.Counter(row["source"] for row in selected).items())),
                   "excluded_unique_by_reason": {name: len(excluded[name]) for name in sorted(exclusions)},
                   "excluded_union": len(candidates) - len(selected),
                   "pilot": {"rows": 128, "unique_ids": len(pilot_ids), "unique_questions": len(pilot_questions)},
                   "qwen4b_focus34": {"rows_by_file": qwen["focus34"]["rows_by_file"],
                                       "unique_ids": len(qwen["focus34"]["ids"]), "unique_questions": len(qwen["focus34"]["questions"])},
                   "qwen4b_mixed401": {"rows_by_file": qwen["mixed401"]["rows_by_file"],
                                         "unique_ids": len(qwen["mixed401"]["ids"]), "unique_questions": len(qwen["mixed401"]["questions"])},
                   "fixed40": {"rows": 40, "members": fixed_members},
                   "recorded_sft": {"files": len(prior_sft_counts), "rows_by_file": prior_sft_counts}},
        "checks": {"distinct_ids": True, "distinct_normalized_questions": True,
                   "selected_overlap_each_exclusion": 0, "leakcheck": leak},
        "ids": {"selected": [row["id"] for row in selected],
                "excluded_by_reason": {name: sorted(values) for name, values in sorted(excluded.items())}},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with args.out.open("x") as handle:
            for row in selected:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        with audit_path.open("x") as handle:
            json.dump(audit, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except Exception:
        args.out.unlink(missing_ok=True)
        audit_path.unlink(missing_ok=True)
        raise
    print(json.dumps({"selected": len(selected), "by_source": audit["counts"]["selected_by_source"],
                      "excluded_union": audit["counts"]["excluded_union"], "leakcheck": leak}, ensure_ascii=False))


if __name__ == "__main__":
    main()
