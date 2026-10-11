"""Prepare leak-free, unseen MATH/GSM8K candidates for an on-policy rollout.

The selector is CPU-only.  It never calls a model: it only reads the canonical
pool, all current SFT parquet variants, the fixed pilot40 archive, and the
existing leakcheck corpus.  Usage is intentionally fail-closed; provide the
checked-in leakcheck script and its corpus explicitly.
"""

import argparse
import collections
import hashlib
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
POOL = DATA / "pool.jsonl"
PILOT = RUN / "eval_archives/c0-greedy-pilot40.tgz"
OUT = DATA / "onpolicy46_candidates.jsonl"
SEED = "onpolicy46-candidates-v1-20261011"
EXPECTED_SFT_FILES = 78
MATH_QUOTAS = {"integer": 64, "expression": 40, "fraction": 24}
PILOT_MEMBER_RE = re.compile(r"/(?:gsm10|gsmnext10|math10|mathnext10)-rows\.jsonl$")
PROBLEM_MARKER = "\n\nProblem: "


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split())


def rank(problem_id):
    return hashlib.sha256(f"{SEED}\0{problem_id}".encode()).hexdigest()


def read_jsonl(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = [json.loads(line) for line in path.open()]
    if not rows:
        raise ValueError(f"empty JSONL: {path}")
    return rows


def raw_problem(prompt):
    if PROBLEM_MARKER not in prompt:
        raise ValueError("SFT or pilot prompt has no final Problem: marker")
    return prompt.rsplit(PROBLEM_MARKER, 1)[1]


def pilot_questions(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    rows, ids = [], []
    with tarfile.open(path) as archive:
        names = sorted(name for name in archive.getnames() if PILOT_MEMBER_RE.search(name))
        if len(names) != 4:
            raise ValueError(f"expected four pilot40 row files, got {names}")
        for name in names:
            handle = archive.extractfile(name)
            if handle is None:
                raise ValueError(f"cannot read {name} from {path}")
            for line in handle:
                row = json.loads(line)
                rows.append(normalize(raw_problem(row["problem"])))
                ids.append(row["problem_id"])
    if len(rows) != 40 or len(set(rows)) != 40 or len(set(ids)) != 40:
        raise ValueError("pilot archive is not exactly 40 unique questions and IDs")
    return set(rows), sorted(ids)


def sft_questions(files, pool_by_id):
    questions = set()
    rows_by_file = {}
    for path in files:
        frame = pd.read_parquet(path)
        rows_by_file[str(path)] = len(frame)
        if "extra_info" not in frame:
            if set(frame.columns) != {"id"}:
                raise ValueError(f"cannot recover question from {path}: {list(frame.columns)}")
            for problem_id in frame["id"]:
                row = pool_by_id.get(problem_id)
                if row is None:
                    raise ValueError(f"ID-only SFT row absent from pool: {problem_id}")
                questions.add(normalize(row["question"]))
            continue
        for info in frame["extra_info"]:
            if not isinstance(info, dict) or not isinstance(info.get("question"), str):
                raise ValueError(f"invalid extra_info.question in {path}")
            prompt = info["question"]
            questions.add(normalize(prompt))
            questions.add(normalize(raw_problem(prompt)))
    if not questions:
        raise ValueError("no questions recovered from SFT parquet files")
    return questions, rows_by_file


def load_leakcheck(path, corpus_dir):
    if not path.is_file() or not corpus_dir.is_dir():
        raise FileNotFoundError(f"leakcheck={path}, corpus={corpus_dir}")
    spec = importlib.util.spec_from_file_location("onpolicy46_leakcheck", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Corpus(str(corpus_dir))


def eval_collision(corpus, row):
    """Match the canonical pool's leak policy, including full MATH-test info."""
    hits = corpus.check(row["question"], row["answer"])
    return any(
        ("(info)" not in hit["eval_set"] and hit.get("leak"))
        or (hit["eval_set"] == "math_test_full(info)" and hit.get("tier") in ("dup", "variant"))
        for hit in hits
    )


def choose(rows, count, corpus, rejected, allow_shortfall=False):
    chosen = []
    for row in sorted(rows, key=lambda item: (rank(item["id"]), item["id"])):
        if eval_collision(corpus, row):
            rejected["eval_leak"].add(row["id"])
            continue
        chosen.append(row)
        if len(chosen) == count:
            return chosen
    if allow_shortfall:
        return chosen
    raise ValueError(f"only {len(chosen)} clean candidates; need {count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, default=POOL)
    parser.add_argument("--pilot", type=Path, default=PILOT)
    parser.add_argument("--sft-dir", type=Path, default=DATA)
    parser.add_argument("--expected-sft-files", type=int, default=EXPECTED_SFT_FILES)
    parser.add_argument("--leakcheck", type=Path, required=True)
    parser.add_argument("--eval-corpus", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    pool = read_jsonl(args.pool)
    if any(not isinstance(row.get("id"), str) or not row["id"] for row in pool):
        raise ValueError("pool row misses ID")
    if len(pool) != len({row["id"] for row in pool}):
        raise ValueError("pool has duplicate or missing IDs")
    if any(not isinstance(row.get("question"), str) or not row.get("answer") for row in pool):
        raise ValueError("pool row misses question or answer")
    if len({normalize(row["question"]) for row in pool}) != len(pool):
        raise ValueError("pool has duplicate normalized question text")

    sft_files = sorted(args.sft_dir.glob("sft_*_*.parquet"))
    if len(sft_files) != args.expected_sft_files:
        raise ValueError(f"expected {args.expected_sft_files} SFT variants, found {len(sft_files)}")
    if any(not re.fullmatch(r"sft_.+_(?:train|val)\.parquet", path.name) for path in sft_files):
        raise ValueError("SFT glob included a non train/val variant")

    trained_questions, sft_rows = sft_questions(sft_files, {row["id"]: row for row in pool})
    pilot, pilot_ids = pilot_questions(args.pilot)
    corpus = load_leakcheck(args.leakcheck, args.eval_corpus)
    rejected = collections.defaultdict(set)

    eligible = []
    for row in pool:
        if row.get("source") not in ("math", "gsm8k"):
            continue
        text = normalize(row["question"])
        if re.search(r"\[asy\]", row["question"], re.IGNORECASE):
            rejected["asy_question"].add(row["id"])
        elif text in trained_questions:
            rejected["sft_question"].add(row["id"])
        elif text in pilot:
            rejected["pilot40_question"].add(row["id"])
        else:
            eligible.append(row)

    math = [row for row in eligible if row["source"] == "math"]
    gsm = [row for row in eligible if row["source"] == "gsm8k"]
    math_selected = []
    selected_ids = set()
    quota_shortfall = {}
    for answer_type, count in MATH_QUOTAS.items():
        picked = choose(
            [row for row in math if row.get("answer_type") == answer_type],
            count, corpus, rejected, allow_shortfall=True,
        )
        math_selected.extend(picked)
        selected_ids.update(row["id"] for row in picked)
        quota_shortfall[answer_type] = count - len(picked)
    if len(math_selected) < 128:
        fill = choose(
            [row for row in math if row["id"] not in selected_ids],
            128 - len(math_selected), corpus, rejected,
        )
        math_selected.extend(fill)
        selected_ids.update(row["id"] for row in fill)
    gsm_selected = choose(gsm, 128, corpus, rejected)
    selected = math_selected + gsm_selected

    questions = [normalize(row["question"]) for row in selected]
    if len(selected) != 256 or len(selected_ids) != 128 or len({row["id"] for row in selected}) != 256:
        raise AssertionError("selected ID cardinality mismatch")
    if len(questions) != len(set(questions)):
        raise AssertionError("selected normalized question collision")
    if set(questions) & trained_questions or set(questions) & pilot:
        raise AssertionError("selected text collision")
    if collections.Counter(row["source"] for row in selected) != {"math": 128, "gsm8k": 128}:
        raise AssertionError("source quota mismatch")
    if sum(quota_shortfall.values()) == 0 and collections.Counter(row["answer_type"] for row in math_selected) != MATH_QUOTAS:
        raise AssertionError("MATH answer-type quota mismatch")

    selected.sort(key=lambda row: (rank(row["id"]), row["id"]))
    audit = {
        "status": "prepared",
        "seed": SEED,
        "inputs": {
            "pool": str(args.pool), "pilot40": str(args.pilot), "leakcheck": str(args.leakcheck),
            "eval_corpus": str(args.eval_corpus), "sft_files": [str(path) for path in sft_files],
            "sft_rows_by_file": sft_rows,
        },
        "counts": {
            "pool_rows": len(pool), "sft_files": len(sft_files), "sft_normalized_questions": len(trained_questions),
            "pilot40_questions": len(pilot), "eligible_before_eval": len(eligible), "selected": len(selected),
            "by_source": dict(sorted(collections.Counter(row["source"] for row in selected).items())),
            "math_by_answer_type": dict(sorted(collections.Counter(row["answer_type"] for row in math_selected).items())),
            "math_quota_shortfall": quota_shortfall,
            "rejected": {key: len(value) for key, value in sorted(rejected.items())},
        },
        "ids": {
            "selected": [row["id"] for row in selected],
            "selected_by_source": {source: [row["id"] for row in selected if row["source"] == source]
                                   for source in ("math", "gsm8k")},
            "selected_math_by_answer_type": {
                answer_type: [row["id"] for row in selected if row["source"] == "math" and row["answer_type"] == answer_type]
                for answer_type in MATH_QUOTAS
            },
            "pilot40": pilot_ids,
            "rejected": {key: sorted(value) for key, value in sorted(rejected.items())},
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    audit_path = args.out.with_suffix(".audit.json")
    tmp_out, tmp_audit = args.out.with_suffix(".tmp.jsonl"), audit_path.with_suffix(".tmp.json")
    try:
        with tmp_out.open("w") as handle:
            for row in selected:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        tmp_audit.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
        os.replace(tmp_out, args.out)
        os.replace(tmp_audit, audit_path)
    finally:
        tmp_out.unlink(missing_ok=True)
        tmp_audit.unlink(missing_ok=True)
    print(json.dumps(audit["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
