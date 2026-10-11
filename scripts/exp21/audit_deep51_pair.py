"""Fail-closed audit for the matched Deep51 tagged/plain datasets."""

import collections
import json
import os
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from checks import candidate, correct
from mv_format import TAGS, parse
from prepare_deep51_pair import (
    CONTROL_COUNT, DEEP, DEEP_AUDIT, DEEP_LEAK, GLOBAL_LEAK, ORDER_SEED,
    PLAN, PLAIN_TRAIN, POOL, RECOVERY_VAL, REPLAY_COUNT, SHARED_VAL,
    TAGGED_TRAIN, load_jsonl, normalize, pilot_questions, plain_response,
    stable_rank, underlying_solution,
)


ROOT = Path(__file__).resolve().parents[2]
TOKENIZER = Path(os.environ.get(
    "EXP21_TOKENIZER",
    "/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer",
))
OUTPUT = ROOT / "results/21-qwen3-0.6b-multiverse/data/sft_deep51_pair_quality.json"


def exact_tokens(tokenizer, info):
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": info["question"]}], add_generation_prompt=True, tokenize=False,
    )
    return len(tokenizer(prompt, add_special_tokens=False).input_ids) + len(
        tokenizer(info["answer"] + tokenizer.eos_token, add_special_tokens=False).input_ids
    )


def external_answer_ok(response, gold):
    assert response.count("</think>") == 1
    return correct(gold, candidate(response.split("</think>", 1)[1]), "math")


def row_answer_ok(row, pool):
    answer = row["extra_info"]["answer"]
    assert answer.count("</think>") == 1
    proposed = candidate(answer.split("</think>", 1)[1])
    source = row["source"]
    gold = pool[row["id"]]["answer"]
    if correct(gold, proposed, source):
        return True
    # Existing recovery8 audit accepts the conventional omission of '%' only
    # for a question explicitly asking for a percent.
    return ("percent" in pool[row["id"]]["question"].lower()
            and gold.rstrip("%") == proposed.rstrip("%"))


def main():
    assert TOKENIZER.is_dir(), TOKENIZER
    tagged = pd.read_parquet(TAGGED_TRAIN)
    plain = pd.read_parquet(PLAIN_TRAIN)
    val = pd.read_parquet(SHARED_VAL)
    recovery_val = pd.read_parquet(RECOVERY_VAL)
    plan = json.loads(PLAN.read_text())
    deep = {row["id"]: row for row in load_jsonl(DEEP)}
    deep_audit = {row["id"]: row for row in load_jsonl(DEEP_AUDIT)}
    pool = {row["id"]: row for row in load_jsonl(POOL)}
    deep_ids = set(deep)
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)

    assert len(tagged) == len(plain) == len(set(tagged.id)) == 256
    assert tagged.id.tolist() == plain.id.tolist() == plan["train"]["row_order_ids"]
    assert tagged["index"].tolist() == plain["index"].tolist() == list(range(256))
    assert val.equals(recovery_val)
    assert not set(tagged.id) & set(val.id)
    assert set(plan["train"]["deep51_ids"]) == deep_ids and len(deep_ids) == 51
    assert collections.Counter(row["extra_info"]["kind"] for row in tagged.to_dict("records")) == {
        "parallel_th": 51, "control_th": CONTROL_COUNT, "replay_th": REPLAY_COUNT,
    }
    assert collections.Counter(row["extra_info"]["kind"] for row in plain.to_dict("records")) == {
        "control_th": 51 + CONTROL_COUNT, "replay_th": REPLAY_COUNT,
    }

    tagged_lengths, plain_lengths = {}, {}
    for left, right in zip(tagged.to_dict("records"), plain.to_dict("records")):
        problem_id = left["id"]
        assert problem_id == right["id"]
        assert left["extra_info"]["question"] == right["extra_info"]["question"]
        assert left["extra_info"]["enable_thinking"] == right["extra_info"]["enable_thinking"] is True
        if problem_id not in deep_ids:
            assert left == right
            assert row_answer_ok(left, pool)
        else:
            source = deep[problem_id]
            review = deep_audit[problem_id]["review"]
            assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
            assert review["independent_paths"] and review["source_preserved"]
            assert left["extra_info"]["answer"] == source["response"]
            structure = parse(left["extra_info"]["answer"])
            assert structure["valid"] and len(structure["blocks"]) == 1
            assert structure["blocks"][0]["numbered"] and len(structure["blocks"][0]["paths"]) == 2
            assert left["extra_info"]["answer"].startswith("<think>")
            assert all(tag not in left["extra_info"]["answer"].split("</think>", 1)[1] for tag in TAGS)
            assert right["extra_info"]["answer"] == plain_response(source["response"])
            assert all(tag not in right["extra_info"]["answer"] for tag in TAGS)
            assert underlying_solution(left["extra_info"]["answer"]) == normalize(right["extra_info"]["answer"])
            assert external_answer_ok(left["extra_info"]["answer"], source["gold_answer"])
            assert external_answer_ok(right["extra_info"]["answer"], source["gold_answer"])
        tagged_lengths[problem_id] = exact_tokens(tokenizer, left["extra_info"])
        plain_lengths[problem_id] = exact_tokens(tokenizer, right["extra_info"])

    # The source rows already passed full-pool answer and leak audits; retain
    # their existing answers byte-for-byte and prove no new question overlap.
    leak = json.loads(GLOBAL_LEAK.read_text())
    deep_leak = json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0
    train_questions = {normalize(pool[problem_id]["question"]) for problem_id in tagged.id}
    val_questions = {normalize(pool[problem_id]["question"]) for problem_id in val.id}
    pilot = pilot_questions()
    assert not train_questions & val_questions and not train_questions & pilot and not val_questions & pilot
    assert max(tagged_lengths.values()) <= 4096 and max(plain_lengths.values()) <= 4096

    report = {
        "status": "audited",
        "checks": {
            "tagged_train_rows": len(tagged), "plain_train_rows": len(plain), "unique_train_ids": len(set(tagged.id)),
            "same_ids_and_order": True, "other_205_rows_identical": True,
            "tagged_deep51_verbatim": len(deep_ids), "plain_underlying_solution_equivalent": len(deep_ids),
            "deep51_independence_evidence": len(deep_ids), "deep51_answers_match_pool": len(deep_ids),
            "tagged_grammar_inside_think": len(deep_ids), "plain_tags": 0, "tagged_tags_outside_think": 0,
            "train_val_normalized_question_overlap": 0, "train_pilot40_normalized_question_overlap": 0,
            "val_pilot40_normalized_question_overlap": 0, "deep51_eval_leaks": 0, "over_4096": 0,
        },
        "lengths": {
            "tagged_min": min(tagged_lengths.values()), "tagged_max": max(tagged_lengths.values()),
            "plain_min": min(plain_lengths.values()), "plain_max": max(plain_lengths.values()),
            "tagged": tagged_lengths, "plain": plain_lengths,
        },
        "shared_validation": {"path": SHARED_VAL.name, "rows": len(val), "equals_recovery8_validation": True},
    }
    temporary = OUTPUT.with_suffix(".tmp.json")
    try:
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, OUTPUT)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps(report["checks"], ensure_ascii=False))


if __name__ == "__main__":
    main()
