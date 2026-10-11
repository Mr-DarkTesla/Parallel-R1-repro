"""Fail-closed audit for the Deep51 2x matched tagged/plain pair."""

import collections
import json
import os
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from checks import candidate, correct
from mv_format import TAGS, parse
from prepare_deep51_2x_pair import (
    CONTROL_COUNT, DEEP, DEEP_AUDIT, DEEP_LEAK, GLOBAL_LEAK, PLAIN_TRAIN,
    POOL, POSITIVE_COPIES, REPLAY_BY_SOURCE, REPLAY_COUNT, TAGGED_TRAIN,
    load_jsonl, normalize, pilot_questions, plain_response,
)
from prepare_deep51_pair import RECOVERY_TRAIN, RECOVERY_VAL, TAGGED_TRAIN as BASE_TAGGED_TRAIN, underlying_solution


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
OUTPUT = RUN / "data/sft_deep51_2x_pair_quality.json"
TOKENIZER = Path(os.environ.get("EXP21_TOKENIZER", "/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"))


def exact_tokens(tokenizer, info):
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": info["question"]}], add_generation_prompt=True, tokenize=False)
    return len(tokenizer(prompt, add_special_tokens=False).input_ids) + len(tokenizer(info["answer"] + tokenizer.eos_token, add_special_tokens=False).input_ids)


def answer_ok(row, pool):
    answer = row["extra_info"]["answer"]
    assert answer.count("</think>") == 1
    gold, proposed = pool[row["id"]]["answer"], candidate(answer.split("</think>", 1)[1])
    if correct(gold, proposed, row["source"]):
        return True
    return "percent" in pool[row["id"]]["question"].lower() and gold.rstrip("%") == proposed.rstrip("%")


def main():
    assert TOKENIZER.is_dir(), TOKENIZER
    tagged, plain = pd.read_parquet(TAGGED_TRAIN), pd.read_parquet(PLAIN_TRAIN)
    deep = {row["id"]: row for row in load_jsonl(DEEP)}
    deep_audit = {row["id"]: row for row in load_jsonl(DEEP_AUDIT)}
    pool = {row["id"]: row for row in load_jsonl(POOL)}
    deep_ids = set(deep)
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)

    assert len(tagged) == len(plain) == 256
    assert tagged[["id", "copy_index", "index"]].equals(plain[["id", "copy_index", "index"]])
    assert tagged["index"].tolist() == list(range(256))
    assert len(set(tagged.id)) == 205
    positive_counts = collections.Counter(tagged[tagged.id.isin(deep_ids)].id)
    assert len(positive_counts) == len(deep_ids) == 51 and set(positive_counts.values()) == {POSITIVE_COPIES}
    assert collections.Counter(row["extra_info"]["kind"] for row in tagged.to_dict("records")) == {"parallel_th": 102, "control_th": CONTROL_COUNT, "replay_th": REPLAY_COUNT}
    assert collections.Counter(row["extra_info"]["kind"] for row in plain.to_dict("records")) == {"control_th": 102 + CONTROL_COUNT, "replay_th": REPLAY_COUNT}
    base = pd.read_parquet(BASE_TAGGED_TRAIN)
    base_controls = {row["id"] for row in base.to_dict("records") if row["extra_info"]["kind"] == "control_th"}
    current_controls = {row["id"] for row in tagged.to_dict("records") if row["extra_info"]["kind"] == "control_th" and row["id"] not in deep_ids}
    assert current_controls == base_controls and len(current_controls) == CONTROL_COUNT
    recovery = {row["id"]: row for row in pd.read_parquet(RECOVERY_TRAIN).to_dict("records")}

    tagged_lengths, plain_lengths = {}, {}
    for left, right in zip(tagged.to_dict("records"), plain.to_dict("records")):
        key = f"{left['index']}:{left['id']}#{left['copy_index']}"
        assert left["id"] == right["id"] and left["copy_index"] == right["copy_index"]
        assert left["extra_info"]["question"] == right["extra_info"]["question"]
        assert left["extra_info"]["enable_thinking"] == right["extra_info"]["enable_thinking"] is True
        if left["id"] not in deep_ids:
            assert left == right and answer_ok(left, pool)
            expected = recovery[left["id"]].copy()
            actual = left.copy()
            expected.pop("index", None)
            actual.pop("index", None)
            actual.pop("copy_index", None)
            assert actual == expected
        else:
            source, review = deep[left["id"]], deep_audit[left["id"]]["review"]
            assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
            assert review["independent_paths"] and review["source_preserved"]
            assert left["extra_info"]["answer"] == source["response"]
            structure = parse(left["extra_info"]["answer"])
            assert structure["valid"] and len(structure["blocks"]) == 1 and structure["blocks"][0]["numbered"] and len(structure["blocks"][0]["paths"]) == 2
            assert all(tag not in left["extra_info"]["answer"].split("</think>", 1)[1] for tag in TAGS)
            assert right["extra_info"]["answer"] == plain_response(source["response"])
            assert all(tag not in right["extra_info"]["answer"] for tag in TAGS)
            assert underlying_solution(left["extra_info"]["answer"]) == normalize(right["extra_info"]["answer"])
            assert answer_ok(left, pool) and answer_ok(right, pool)
        tagged_lengths[key] = exact_tokens(tokenizer, left["extra_info"])
        plain_lengths[key] = exact_tokens(tokenizer, right["extra_info"])

    val = pd.read_parquet(RECOVERY_VAL)
    train_questions = {normalize(pool[problem_id]["question"]) for problem_id in tagged.id}
    val_questions = {normalize(pool[problem_id]["question"]) for problem_id in val.id}
    assert not train_questions & val_questions and not train_questions & pilot_questions()
    leak, deep_leak = json.loads(GLOBAL_LEAK.read_text()), json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0
    assert max(tagged_lengths.values()) <= 4096 and max(plain_lengths.values()) <= 4096

    report = {"status": "audited", "checks": {
        "tagged_train_rows": 256, "plain_train_rows": 256, "unique_train_ids": 205,
        "positive_rows": 102, "unique_positive_ids": 51, "copies_per_positive_id": POSITIVE_COPIES,
        "same_row_order": True, "nonpositive_rows_identical": True,
        "same_45_control_ids_as_deep51_1x": True, "nonpositive_texts_verbatim_recovery8": 154,
        "tagged_deep51_verbatim": 102, "plain_underlying_solution_equivalent": 102,
        "deep51_independence_evidence": 102, "deep51_answers_match_pool": 102,
        "tagged_grammar_inside_think": 102, "plain_tags": 0, "tagged_tags_outside_think": 0,
        "train_val_normalized_question_overlap": 0, "train_pilot40_normalized_question_overlap": 0,
        "deep51_eval_leaks": 0, "over_4096": 0,
    }, "lengths": {"tagged_min": min(tagged_lengths.values()), "tagged_max": max(tagged_lengths.values()),
                    "plain_min": min(plain_lengths.values()), "plain_max": max(plain_lengths.values()),
                    "tagged": tagged_lengths, "plain": plain_lengths},
    "selection": {"control_rows": CONTROL_COUNT, "replay_rows": REPLAY_COUNT, "replay_by_source": REPLAY_BY_SOURCE}}
    temporary = OUTPUT.with_suffix(".tmp.json")
    try:
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, OUTPUT)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps(report["checks"], ensure_ascii=False))


if __name__ == "__main__":
    main()
