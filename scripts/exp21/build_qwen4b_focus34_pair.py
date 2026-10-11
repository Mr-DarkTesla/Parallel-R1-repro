#!/usr/bin/env python3
"""CPU-only paired continuation data: reviewed Qwen4B blocks plus Qwen4B replay."""
import json
import os
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd
from tokenizers import Tokenizer

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import ANY_TAG, TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA, AUDIT = RUN / "data", RUN / "audit"
PREFIX = DATA / "qwen4b_focus34"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer/tokenizer.json"
PILOT = RUN / "masked_pilot/masked_pilot"
FIXED40 = ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")
FINAL = re.compile(r"(?m)^Final Answer:[^\n]+$")


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def norm(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().casefold()


def question(prompt):
    marker = "\n\nProblem: "
    assert marker in prompt
    return norm(prompt.rsplit(marker, 1)[1])


def fixed40():
    return [(row["extra_info"]["id"], question(row["prompt"][0]["content"]))
            for part in FIXED40 for row in pd.read_parquet(PILOT / f"{part}.parquet").to_dict("records")]


def output_row(kind, source, response):
    prompt = mv_prompt(HEADER + source["question"]) if kind in {"parallel_th", "control_th"} else HEADER + source["question"]
    return {"data_source": f"exp21_{kind}", "id": source["id"], "source": source["source"],
            "extra_info": {"question": prompt, "answer": response, "enable_thinking": True,
                           "kind": kind, "id": source["id"]}}


def paired(left, right):
    assert len(left) == len(right) and [row["id"] for row in left] == [row["id"] for row in right]
    for tagged, plain in zip(left, right):
        a, b = tagged["extra_info"], plain["extra_info"]
        assert a["question"] == b["question"] and a["enable_thinking"] == b["enable_thinking"]
        assert ANY_TAG.sub("", a["answer"]) == b["answer"], tagged["id"]
        assert not ANY_TAG.search(b["answer"]), tagged["id"]


def tags_inside_think(response, problem_id):
    assert response.startswith("<think>") and response.count("<think>") == response.count("</think>") == 1
    close = response.index("</think>")
    assert not ANY_TAG.search(response[close:]), problem_id
    parsed = parse(response)
    assert parsed["valid"] and len(parsed["blocks"]) == 1, problem_id
    assert all(match.start() < close for match in ANY_TAG.finditer(response)), problem_id
    assert len(FINAL.findall(response[close:])) == 1, problem_id


def length(tokenizer, row):
    info = row["extra_info"]
    rendered = f"<|im_start|>user\n{info['question']}<|im_end|>\n<|im_start|>assistant\n"
    return len(tokenizer.encode(rendered + info["answer"] + "<|im_end|>").ids)


def write_parquet(path, data):
    frame = pd.DataFrame(data)
    frame["index"] = range(len(frame))
    temporary = path.with_suffix(path.suffix + ".tmp")
    frame.to_parquet(temporary, index=False)
    os.replace(temporary, path)


def main():
    tagged = rows(DATA / "qwen4b_rewrite_reviewed_tagged.jsonl")
    plain = rows(DATA / "qwen4b_rewrite_reviewed_plain.jsonl")
    graded = rows(DATA / "qwen4b_teacher_graded320.jsonl")
    review = json.loads((AUDIT / "qwen4b_rewrite_pair_report.json").read_text())
    assert review["ready_for_sft"] and review["checks"]["math_verify"] == 34
    assert len(TAGS) == 10 and len(tagged) == len(plain) == 34
    assert [row["id"] for row in tagged] == [row["id"] for row in plain]
    assert len({row["id"] for row in tagged}) == len({norm(row["question"]) for row in tagged}) == 34
    for left, right in zip(tagged, plain):
        assert {key: value for key, value in left.items() if key not in {"response", "prompt"}} == \
            {key: value for key, value in right.items() if key not in {"response", "prompt"}}
        assert ANY_TAG.sub("", left["response"]) == right["response"]
        assert all(tag in left["response"] for tag in TAGS)
        tags_inside_think(left["response"], left["id"])

    val = {arm: pd.read_parquet(DATA / f"qwen4b_mixed401_{arm}_val.parquet").to_dict("records")
           for arm in ("tagged", "plain")}
    assert len(val["tagged"]) == len(val["plain"]) == 50
    paired(val["tagged"], val["plain"])
    val_questions = {question(row["extra_info"]["question"]) for row in val["tagged"]}
    fixed = fixed40()
    assert len(fixed) == 40
    fixed_questions = {value for _, value in fixed}

    positive_ids = {row["id"] for row in tagged}
    positive_questions = {norm(row["question"]) for row in tagged}
    replay = [row for row in graded if row.get("correct") is True and row.get("clean") is True and
              row.get("truncated") is False and row["id"] not in positive_ids and
              norm(row["question"]) not in positive_questions]
    assert len(graded) == 320 and len(replay) == 129
    assert len({row["id"] for row in replay}) == len({norm(row["question"]) for row in replay}) == len(replay)
    for row in replay:
        assert row["output"].startswith("<think>") and row["output"].count("<think>") == row["output"].count("</think>") == 1
        assert FINAL.search(row["output"].split("</think>", 1)[1]) and not ANY_TAG.search(row["output"])
    train_questions = positive_questions | {norm(row["question"]) for row in replay}
    assert not train_questions & fixed_questions and not train_questions & val_questions

    train = {"tagged": [], "plain": []}
    for _ in range(3):
        train["tagged"] += [output_row("parallel_th", row, row["response"]) for row in tagged]
        train["plain"] += [output_row("control_th", row, row["response"]) for row in plain]
    for row in replay:
        replay_row = output_row("replay_th", row, row["output"])
        train["tagged"].append(replay_row)
        train["plain"].append(replay_row)
    paired(train["tagged"], train["plain"])
    assert len(train["tagged"]) == len(train["plain"]) == 231

    tokenizer = Tokenizer.from_file(str(TOKENIZER))
    limits = {arm: {split: max(length(tokenizer, row) for row in part)
                    for split, part in (("train", train[arm]), ("val", val[arm]))}
              for arm in ("tagged", "plain")}
    assert max(value for arm in limits.values() for value in arm.values()) <= 4096
    for arm in ("tagged", "plain"):
        write_parquet(DATA / f"qwen4b_focus34_{arm}_train.parquet", train[arm])
        write_parquet(DATA / f"qwen4b_focus34_{arm}_val.parquet", val[arm])

    report = {"status": "ready_for_paired_continuation", "parent": "qwen4b_mixed401_{tagged,plain}_step128",
              "rows_per_arm": {"train": 231, "val": 50},
              "train": {"reviewed_positive_unique": 34, "positive_copies_each": 3,
                        "positive_rows": 102, "qwen4b_replay_unique": 129, "replay_rows": 129,
                        "kind_counts": dict(Counter(row["extra_info"]["kind"] for row in train["tagged"]))},
              "validation": {"source": "qwen4b_mixed401_{tagged,plain}_val.parquet", "rows_copied": 50},
              "checks": {"reviewed_math_verify_provenance": "34/34", "replay_grade_gen_math_verify_provenance": "129/129",
                         "same_row_order": True, "plain_equals_tagged_after_removing_only_10_tag_types": True,
                         "tagged_blocks_inside_think": 34, "replay_untagged": 129,
                         "fixed40_normalized_question_overlap": 0, "validation_normalized_question_overlap": 0,
                         "fixed40_raw_id_collisions_different_questions": sorted({row["id"] for row in train["tagged"]} & {key for key, _ in fixed}),
                         "max_total_tokens": limits},
              "command": "uv run --offline --no-project --with pandas --with pyarrow --with tokenizers==0.23.2 python scripts/exp21/build_qwen4b_focus34_pair.py"}
    target = AUDIT / "qwen4b_focus34_report.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
