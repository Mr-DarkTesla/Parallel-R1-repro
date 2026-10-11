#!/usr/bin/env python3
"""CPU-only matched 4B SFT pair from independently accepted agent solutions.

Example: uv run --offline --no-project --with math-verify --with transformers \
  --with jinja2 --with pandas --with pyarrow python scripts/exp21/build_agent_parallel_pair.py \
  --accepted accepted.jsonl --out-prefix /tmp/agent-parallel/sft

The accepted JSONL needs id, source, question, answer, answer_type, output,
provenance. A production build also needs --review-report JSON with at least
30 independently read examples, >=90% useful blocks and zero wrong finals.
Without it, or with fewer than 46 positive tasks, the output is pilot_only and
the GPU runner refuses it.
"""

from __future__ import annotations

import argparse
import collections
import copy
import importlib.util
import json
import random
import re
import tarfile
import unicodedata
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse, strip_tags
from filter_onpolicy_rollouts import lone_number, normalize_superscripts


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"
REPLAY_KINDS = {"replay_th": 55, "replay_nt": 54}
REQUIRED = ("id", "source", "question", "answer", "answer_type", "output", "provenance")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def answer_checker():
    """Use the unchanged on-policy math rule without importing verl's Ray runtime."""
    from math_verify import parse as parse_math, verify

    path = ROOT / "verl/verl/utils/reward_score/math_dapo.py"
    spec = importlib.util.spec_from_file_location("exp21_math_dapo", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def correct(source, answer, truth):
        if source.upper() in ("ARC", "MMLUPRO"):
            choices = re.findall(r"(?i)(?:final answer|correct answer|answer is|answer)\s*:?\s*\**\(?([A-J]|10|[1-9])\b", answer)
            return bool(choices) and (choices[-1].upper() if choices[-1].isalpha()
                                      else "ABCDEFGHIJ"[int(choices[-1]) - 1]) == truth
        boxed = module.last_boxed_only_string(answer)
        if boxed:
            candidate = module.remove_boxed(boxed)
        else:
            parts = re.split(r"(?i)final answer\s*:", answer)
            lines = [line for line in parts[-1].splitlines() if line.strip()] if len(parts) > 1 else []
            candidate = lines[0] if lines else ""
        candidate = candidate.strip().strip("$").strip().rstrip(".")
        if not candidate:
            return False
        candidate = normalize_superscripts(candidate)
        if r"\approx" in truth:
            truth = truth.rsplit(r"\approx", 1)[-1].replace(r"\$", "").strip()
        target = parse_math(f"${truth}$")
        if verify(target, parse_math(f"${candidate}$")) or module.compute_score(f"Final Answer: {candidate}", truth)["acc"]:
            return True
        number = lone_number(candidate) if re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:/\d+)?%?", truth.strip()) else None
        return bool(number) and verify(target, parse_math(f"${number}$"))

    return correct


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).split()).casefold()


def jsonl(path):
    require(path.is_file(), f"missing JSONL: {path}")
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        require(bool(line.strip()), f"blank line: {path}:{line_number}")
        row = json.loads(line)
        require(isinstance(row, dict), f"object required: {path}:{line_number}")
        rows.append(row)
    require(bool(rows), f"empty JSONL: {path}")
    return rows


def question_from_prompt(prompt):
    marker = "\n\nProblem: "
    require(isinstance(prompt, str) and marker in prompt, "replay/val prompt lacks Problem marker")
    return norm(prompt.rsplit(marker, 1)[1].split("<|im_end|>", 1)[0])


def fixed40_questions(path):
    require(path.is_file(), f"missing fixed40 archive: {path}")
    questions = set()
    with tarfile.open(path) as archive:
        names = [name for name in archive.getnames() if name.endswith("-block-rows.jsonl")]
        require(len(names) == 4, "fixed40 needs four block-row files")
        for name in names:
            for line in archive.extractfile(name):
                questions.add(norm(json.loads(line)["problem"]))
    require(len(questions) == 40, "fixed40 needs 40 distinct questions")
    return questions


def holdout_questions(path):
    manifest = json.loads((path / "manifest.json").read_text())
    questions, identifiers = set(), set()
    for source in ("gsm8k", "math"):
        ids = manifest["sources"][source]["selected_ids"]
        frame = pd.read_parquet(path / f"{source}_holdout20.parquet")
        require(len(ids) == len(frame) == 20, f"bad {source} holdout")
        identifiers.update(ids)
        questions.update(question_from_prompt(row["prompt"][0]["content"]) for _, row in frame.iterrows())
    require(len(questions) == len(identifiers) == 40, "holdout IDs/questions are not distinct")
    return identifiers, questions


def validate_response(row, checker):
    identifier, response = row["id"], row["output"]
    require(response.startswith("<think>") and response.count("<think>") == 1
            and response.count("</think>") == 1, f"{identifier}: invalid thinking envelope")
    thought, final = response.split("</think>", 1)
    require(not any(tag in final for tag in TAGS), f"{identifier}: tag outside thinking")
    require(re.fullmatch(r"Final Answer: [^\n]+", final.strip()) is not None,
            f"{identifier}: external final must be one complete Final Answer line")
    parsed = parse(thought)
    require(parsed["valid"] and len(parsed["blocks"]) == 1, f"{identifier}: need one grammatical block")
    block = parsed["blocks"][0]
    require(block["numbered"] and len(block["paths"]) == len(block["outlines"]) == 2,
            f"{identifier}: need two numbered independent paths/outlines")
    require(all(item.strip() for item in block["outlines"] + block["paths"] + [block["conclusion"]]),
            f"{identifier}: empty block section")
    require(checker(row["source"], final, row["answer"]), f"{identifier}: wrong external answer")
    plain = strip_tags(response)
    require(not any(tag in plain for tag in TAGS), f"{identifier}: tag remains in plain control")
    # strip_tags is the sole transformation; it removes markup and normalizes
    # whitespace, but must preserve every non-tag word and number in order.
    stripped_words = norm(re.sub(r"</?(?:Parallel|Goal|Outline|Path|Conclusion)>", "", response))
    require(stripped_words == norm(plain), f"{identifier}: plain control changed non-tag text")
    return plain


def load_val(tagged_path, plain_path):
    frames = {arm: pd.read_parquet(path).to_dict("records") for arm, path in
              (("tagged", tagged_path), ("plain", plain_path))}
    require(all(len(rows) == 50 for rows in frames.values()), "paired validation needs 50 rows/arm")
    for left, right in zip(frames["tagged"], frames["plain"]):
        require(left["id"] == right["id"] and left["extra_info"]["question"] == right["extra_info"]["question"],
                "paired validation rows differ in ID or prompt")
        require(norm(strip_tags(left["extra_info"]["answer"])) == norm(right["extra_info"]["answer"]),
                "paired validation differs beyond structural tags")
    return frames


def review_gate(path, selected_ids):
    if path is None:
        return {"status": "absent", "reviewed": 0, "useful": 0, "wrong_final": 0}
    report = json.loads(path.read_text())
    reviewed = report.get("reviewed_ids")
    useful = report.get("useful_ids")
    wrong = report.get("wrong_final_ids")
    require(all(isinstance(items, list) and all(isinstance(value, str) for value in items)
                for items in (reviewed, useful, wrong)), "review report needs three ID lists")
    require(all(len(items) == len(set(items)) for items in (reviewed, useful, wrong)), "duplicate review ID")
    require(set(useful) <= set(reviewed) and set(wrong) <= set(reviewed), "review IDs inconsistent")
    require(set(reviewed) <= selected_ids, "reviewed ID absent from selected positives")
    require(len(reviewed) >= 30 and len(useful) * 10 >= len(reviewed) * 9 and not wrong,
            "independent review gate failed (<30, <90% useful, or wrong final)")
    require(isinstance(report.get("reviewer"), str) and report["reviewer"].strip()
            and isinstance(report.get("method"), str) and report["method"].strip(),
            "review report needs reviewer and sampling method")
    return {"status": "passed", "path": str(path), "reviewed": len(reviewed),
            "useful": len(useful), "wrong_final": 0, "method": report["method"]}


def total_tokens(tokenizer, row):
    info = row["extra_info"]
    # Exactly ParallelThinkingSFTDataset.__getitem__: render each row's
    # thinking mode, then tokenize prompt and response separately with no
    # implicit special tokens. The GPU runner repeats this with its parent.
    rendered = tokenizer.apply_chat_template(
        [{"role": "user", "content": info["question"]}],
        add_generation_prompt=True, tokenize=False,
        enable_thinking=bool(info["enable_thinking"]),
    )
    prompt_ids = tokenizer(rendered, add_special_tokens=False)["input_ids"]
    response_ids = tokenizer(info["answer"] + tokenizer.eos_token,
                             add_special_tokens=False)["input_ids"]
    return len(prompt_ids) + len(response_ids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted", type=Path, required=True)
    parser.add_argument("--out-prefix", type=Path, required=True)
    parser.add_argument("--positive-count", type=int, default=46)
    parser.add_argument("--positive-copies", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261012)
    parser.add_argument("--review-report", type=Path)
    parser.add_argument("--pool", type=Path, default=DATA / "pool.jsonl")
    parser.add_argument("--replay-train", type=Path, default=DATA / "qwen4b_onpolicy189_clean46_tagged_train.parquet")
    parser.add_argument("--tagged-val", type=Path, default=DATA / "qwen4b_onpolicy189_clean46_tagged_val.parquet")
    parser.add_argument("--plain-val", type=Path, default=DATA / "qwen4b_onpolicy189_clean46_plain_val.parquet")
    parser.add_argument("--fixed40", type=Path, default=RUN / "eval_archives/qwen4b_init_fixed40.tgz")
    parser.add_argument("--holdout40", type=Path, default=RUN / "holdout40")
    parser.add_argument("--tokenizer", type=Path, default=TOKENIZER)
    args = parser.parse_args()
    require(args.positive_count > 0 and args.positive_copies > 0, "positive count/copies must be positive")

    accepted = jsonl(args.accepted)
    require(all(all(isinstance(row.get(key), str) and row[key].strip() for key in REQUIRED)
                for row in accepted), "accepted row lacks required nonempty string field")
    require(all(row["source"] in ("gsm8k", "math") for row in accepted), "unknown accepted source")
    require(len({row["id"] for row in accepted}) == len(accepted), "duplicate accepted ID")
    require(len({norm(row["question"]) for row in accepted}) == len(accepted), "duplicate accepted question")
    require(len(accepted) >= args.positive_count, "too few accepted rows")

    pool_rows = jsonl(args.pool)
    pool = {row["id"]: row for row in pool_rows}
    require(len(pool_rows) == len(pool) == 16547, "wrong/duplicate leakchecked pool")
    for row in accepted:
        source = pool.get(row["id"])
        require(source is not None and all(source[key] == row[key] for key in
                                       ("source", "question", "answer", "answer_type")),
                f"{row['id']}: accepted metadata differs from leakchecked pool")

    checker = answer_checker()
    plain_text = {row["id"]: validate_response(row, checker) for row in accepted}

    randomizer = random.Random(args.seed)
    candidates = sorted(accepted, key=lambda row: row["id"])
    randomizer.shuffle(candidates)
    selected = []
    if args.positive_count >= 46:
        quotas = {("gsm8k", "integer"): 18, ("math", "integer"): 6,
                  ("math", "fraction"): 6, ("math", "expression"): 6}
        for (source, answer_type), count in quotas.items():
            matches = [row for row in candidates if row["source"] == source and row["answer_type"] == answer_type]
            require(len(matches) >= count, f"too few accepted {source}/{answer_type}: {len(matches)} < {count}")
            selected.extend(matches[:count])
    selected_ids = {row["id"] for row in selected}
    selected.extend(row for row in candidates if row["id"] not in selected_ids)  # stable seeded fill
    selected = selected[:args.positive_count]
    selected_ids = {row["id"] for row in selected}
    reviewed = review_gate(args.review_report, selected_ids)

    val = load_val(args.tagged_val, args.plain_val)
    val_ids = {row["id"] for row in val["tagged"]}
    val_questions = {question_from_prompt(row["extra_info"]["question"]) for row in val["tagged"]}
    holdout_ids, holdout_text = holdout_questions(args.holdout40)
    fixed_text = fixed40_questions(args.fixed40)
    accepted_questions = {norm(row["question"]) for row in accepted}
    require(not {row["id"] for row in accepted} & (val_ids | holdout_ids), "accepted ID overlaps val or holdout")
    require(not accepted_questions & (val_questions | fixed_text | holdout_text),
            "positive text overlaps val or masked holdout")
    selected_questions = {norm(row["question"]) for row in selected}

    old_train = pd.read_parquet(args.replay_train).to_dict("records")
    replay = [copy.deepcopy(row) for row in old_train if row["extra_info"]["kind"] in REPLAY_KINDS]
    kinds = collections.Counter(row["extra_info"]["kind"] for row in replay)
    require(kinds == REPLAY_KINDS, f"wrong replay composition: {kinds}")
    replay_ids = {row["id"] for row in replay}
    replay_questions = {question_from_prompt(row["extra_info"]["question"]) for row in replay}
    require(len(replay_ids) == len(replay_questions) == len(replay), "replay has duplicate IDs/questions")
    require(not replay_ids & (selected_ids | val_ids | holdout_ids), "replay ID overlaps positive/val/holdout")
    require(not replay_questions & (selected_questions | val_questions | fixed_text | holdout_text),
            "replay text overlaps positive/val/masked holdout")
    require(all(not any(tag in row["extra_info"]["answer"] for tag in TAGS) for row in replay),
            "replay contains Multiverse tag")

    train = {"tagged": [], "plain": []}
    for copy_index in range(args.positive_copies):
        for row in selected:
            common = {"id": row["id"], "source": row["source"], "copy_index": copy_index,
                      "provenance": row["provenance"]}
            prompt = mv_prompt(HEADER + row["question"])
            for arm, answer, kind in (("tagged", row["output"], "parallel_th"),
                                      ("plain", plain_text[row["id"]], "control_th")):
                train[arm].append({**common, "data_source": f"exp21_agent_parallel_{arm}",
                                   "extra_info": {"question": prompt, "answer": answer,
                                                  "enable_thinking": True, "kind": kind, "id": row["id"]}})
    for row in replay:
        for arm in train:
            train[arm].append(copy.deepcopy(row))
    order = list(range(len(train["tagged"])))
    randomizer.shuffle(order)
    train = {arm: [rows[index] for index in order] for arm, rows in train.items()}
    for index, (left, right) in enumerate(zip(train["tagged"], train["plain"])):
        left["index"] = right["index"] = index
        require(left["id"] == right["id"] and left["extra_info"]["question"] == right["extra_info"]["question"],
                "train pair drifted in ID/order/prompt")
        require(norm(strip_tags(left["extra_info"]["answer"])) == norm(right["extra_info"]["answer"]),
                "train pair differs beyond structural tags")

    require(args.tokenizer.is_dir(), f"missing tokenizer directory: {args.tokenizer}")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    maxima = {arm: {split: max(total_tokens(tokenizer, row) for row in rows)
                    for split, rows in (("train", train[arm]), ("val", val[arm]))} for arm in train}
    require(all(size <= 4096 for sizes in maxima.values() for size in sizes.values()),
            f"row exceeds 4096 tokens: {maxima}")
    ready = args.positive_count >= 46 and reviewed["status"] == "passed"
    report = {
        "status": "ready_for_paired_sft" if ready else "pilot_only",
        "inputs": {"accepted": str(args.accepted), "pool": str(args.pool),
                   "replay_train": str(args.replay_train), "tagged_val": str(args.tagged_val),
                   "plain_val": str(args.plain_val), "fixed40": str(args.fixed40),
                   "holdout40": str(args.holdout40), "tokenizer": str(args.tokenizer)},
        "seed": args.seed,
        "accepted": {"count": len(selected), "available": len(accepted), "selected_ids": sorted(selected_ids),
                     "by_source_type": dict(collections.Counter(f"{row['source']}/{row['answer_type']}" for row in selected)),
                     "review": reviewed},
        "rows_per_arm": {"train": len(train["tagged"]), "val": len(val["tagged"])},
        "train": {"positive_copies": args.positive_copies, "positive_rows": len(selected) * args.positive_copies,
                  "replay_thinking": kinds["replay_th"], "replay_no_thinking": kinds["replay_nt"]},
        "checks": {"pool_metadata_match": True, "math_verify_final": len(accepted),
                   "one_block_inside_think": len(accepted), "plain_transform": "mv_format.strip_tags",
                   "same_prompts_and_order": True, "train_val_fixed40_holdout_overlap": 0,
                   "max_total_tokens": maxima,
                   "length_method": "ParallelThinkingSFTDataset chat template and separate prompt/response tokenization"},
    }
    targets = {f"{arm}_{split}": args.out_prefix.with_name(args.out_prefix.name + f"_{arm}_{split}.parquet")
               for arm in train for split in ("train", "val")}
    report_path = args.out_prefix.with_name(args.out_prefix.name + "_build_report.json")
    require(not any(path.exists() for path in [*targets.values(), report_path]), "refusing to overwrite output")
    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for key, path in targets.items():
        arm, split = key.split("_")
        pd.DataFrame(train[arm] if split == "train" else val[arm]).to_parquet(path, index=False)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "rows_per_arm": report["rows_per_arm"],
                      "report": str(report_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
