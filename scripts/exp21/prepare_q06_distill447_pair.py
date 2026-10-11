#!/usr/bin/env python3
"""Add fully reviewed 4B reasoning to the paired 0.6B replay mixture."""
import json
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd

from mv_format import ANY_TAG, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
OUT = DATA / "q06_distill447"
SOURCE = "qwen4b_onpolicy189_clean46"
SEED = 210447
PILOT = RUN / "masked_pilot/masked_pilot"
PILOT_PARTS = ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")


def normalized(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().casefold()


def raw_question(prompt):
    return prompt.rsplit("\n\nProblem: ", 1)[1]


def fixed40_questions():
    rows = [row for part in PILOT_PARTS
            for row in pd.read_parquet(PILOT / f"{part}.parquet").to_dict("records")]
    assert len(rows) == 40
    return {normalized(raw_question(row["prompt"][0]["content"])) for row in rows}


def rows(stem, arm, split):
    return pd.read_parquet(DATA / f"{stem}_{arm}_{split}.parquet").to_dict("records")


def paired(tagged, plain):
    assert len(tagged) == len(plain)
    for a, b in zip(tagged, plain):
        ai, bi = a["extra_info"], b["extra_info"]
        assert a["id"] == b["id"] == ai["id"] == bi["id"]
        assert a["source"] == b["source"]
        assert ai["question"] == bi["question"]
        assert ai["enable_thinking"] == bi["enable_thinking"]
        assert ANY_TAG.sub("", ai["answer"]) == bi["answer"]
        if ai["kind"] == "parallel_th":
            assert bi["kind"] == "control_th"
            answer = ai["answer"]
            structure = parse(answer)
            assert answer.startswith("<think>") and answer.count("</think>") == 1
            assert structure["valid"] and len(structure["blocks"]) == 1
            assert structure["blocks"][0]["numbered"]
            assert structure["blocks"][0]["end"] < answer.index("</think>")
            assert answer.count("Final Answer:") == 1
        else:
            assert ai == bi and not ANY_TAG.search(ai["answer"])
        assert not ANY_TAG.search(bi["answer"])


def main():
    old = json.loads((AUDIT / "qwen4b_mixed401_report.json").read_text())
    new = json.loads((AUDIT / "qwen4b_onpolicy189_clean46_pair_report.json").read_text())
    assert old["status"] == "ready_for_paired_sft" and old["distinct_positive"] == 401
    assert old["plain_only_removes_tags"] and old["fixed40_question_overlap"] == 0
    assert old["rows_per_arm"] == {"train": 2383, "val": 50}
    assert new["accepted"]["count"] == 46
    assert new["accepted"]["semantic_path_independence"] == "reviewed"
    assert new["checks"]["plain_equals_tagged_after_removing_only_tags"]
    assert new["checks"]["candidate_eval_leakcheck"] == "passed"
    assert new["checks"]["train_validation_question_overlap"] == 0
    assert new["checks"]["train_fixed40_question_overlap"] == 0

    original = {arm: rows("qwen4b_mixed401", arm, "train") for arm in ("tagged", "plain")}
    recent = {arm: rows(SOURCE, arm, "train") for arm in ("tagged", "plain")}
    validation = {arm: rows("qwen4b_mixed401", arm, "val") for arm in ("tagged", "plain")}
    for arm in ("tagged", "plain"):
        assert validation[arm] == rows(SOURCE, arm, "val")
    for group in (original, recent, validation):
        paired(group["tagged"], group["plain"])

    new_positive = {arm: [r for r in recent[arm]
                          if r["extra_info"]["kind"] == ("parallel_th" if arm == "tagged" else "control_th")]
                    for arm in ("tagged", "plain")}
    paired(new_positive["tagged"], new_positive["plain"])
    assert len(new_positive["tagged"]) == len(new_positive["plain"]) == 138
    assert len({r["id"] for r in new_positive["tagged"]}) == 46
    assert set(new["accepted"]["ids"]) == {r["id"] for r in new_positive["tagged"]}
    old_ids = {r["id"] for r in original["tagged"]}
    val_ids = {r["id"] for r in validation["tagged"]}
    assert not old_ids & {r["id"] for r in new_positive["tagged"]}
    assert not val_ids & (old_ids | {r["id"] for r in new_positive["tagged"]})
    old_questions = {normalized(raw_question(r["extra_info"]["question"])) for r in original["tagged"]}
    new_questions = {normalized(raw_question(r["extra_info"]["question"])) for r in new_positive["tagged"]}
    val_questions = {normalized(raw_question(r["extra_info"]["question"])) for r in validation["tagged"]}
    fixed_questions = fixed40_questions()
    assert len(new_questions) == 46
    assert not new_questions & (old_questions | val_questions | fixed_questions)
    assert not old_questions & (val_questions | fixed_questions)

    # Three source copies become six: stronger exposure to the 46 reviewed 4B paths.
    combined = {arm: original[arm] + new_positive[arm] * 2 for arm in ("tagged", "plain")}
    order = list(range(len(combined["tagged"])))
    random.Random(SEED).shuffle(order)
    for arm in combined:
        combined[arm] = [{**{k: v for k, v in combined[arm][i].items() if k != "copy_index"},
                          "index": j} for j, i in enumerate(order)]
    paired(combined["tagged"], combined["plain"])
    assert len(combined["tagged"]) == len(combined["plain"]) == 2659
    kinds = Counter(r["extra_info"]["kind"] for r in combined["tagged"])
    assert kinds == {"parallel_th": 1489, "replay_th": 588, "replay_nt": 582}
    train_positive_ids = {r["id"] for r in combined["tagged"]
                          if r["extra_info"]["kind"] == "parallel_th"}
    val_positive_ids = {r["id"] for r in validation["tagged"]
                        if r["extra_info"]["kind"] == "parallel_th"}
    assert len(train_positive_ids) == 439 and len(val_positive_ids) == 8
    assert len(train_positive_ids | val_positive_ids) == 447

    # Every rendered prompt and answer is an unchanged source row. Both sources
    # measured lengths with the same 0.6B Multiverse tokenizer and chat template.
    lengths = {arm: {"train": max(old["max_total_tokens"][arm],
                                  new["checks"]["max_total_tokens"][arm]["train"]),
                     "val": new["checks"]["max_total_tokens"][arm]["val"]}
               for arm in ("tagged", "plain")}
    assert max(size for splits in lengths.values() for size in splits.values()) <= 4096
    for arm in ("tagged", "plain"):
        for split, records in (("train", combined[arm]), ("val", validation[arm])):
            pd.DataFrame(records).to_parquet(f"{OUT}_{arm}_{split}.parquet", index=False)
    report = {"status": "ready_for_paired_sft", "target": "Qwen/Qwen3-0.6B",
              "distinct_positive": 447, "train_distinct_positive": 439,
              "val_distinct_positive": 8,
              "sources": {"m1": 367, "qwen4b_reviewed": 34,
                                                     "qwen4b_clean46": 46},
              "copies": {"m1": 3, "qwen4b_reviewed": 4, "qwen4b_clean46": 6,
                         "q06_replay_thinking": 2, "q06_replay_no_thinking": 2},
              "rows_per_arm": {"train": 2659, "val": 50},
              "train_kind_counts": dict(kinds), "max_total_tokens": lengths,
              "train_val_question_overlap": 0, "fixed40_question_overlap": 0,
              "old_new_question_overlap": 0, "plain_only_removes_tags": True,
              "lengths_reused_from_unchanged_source_rows": True,
              "seed": SEED, "command": "python scripts/exp21/prepare_q06_distill447_pair.py"}
    (AUDIT / "q06_distill447_pair_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
