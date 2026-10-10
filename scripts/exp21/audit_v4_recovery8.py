"""Fail-closed audit of the v4-step56 recovery8 SFT dataset."""

import collections
import json
import os
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from build_sft import HEADER
from checks import candidate, correct, norm
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse
from prepare_v4_recovery8 import (
    AUDIT_OUT, DATA, EXCLUDED_REVIEW_ID, LEAK_AUDIT, ORDER_SEED,
    POOL, REPLAY_QUOTAS, REPLAY_SEED, SOURCE_TRAIN, SOURCE_VAL, TRAIN_OUT,
    VAL_OUT, kind, load_jsonl, normalize_question, pilot_rows,
    raw_problem, reviewed_positive_ids, select_ids, signature, stable_rank,
)


ROOT = Path(__file__).resolve().parents[2]
TOKENIZER = Path(os.environ.get(
    "EXP21_TOKENIZER",
    ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer",
))
MERGE_INSIDE = DATA / "pair_expanded_m1_merge_inside.jsonl"
REPLAY_SOURCE = DATA / "replay_th.jsonl"
V2_PLAN = DATA / "sft_selective_blocks_v2_audit.json"
V2_QUALITY = DATA / "sft_selective_blocks_v2_quality.json"
V4_QUALITY = DATA / "sft_selective_blocks_v4_quality.json"


def contextual_answer_ok(reference, answer):
    direct = correct(reference["answer"], answer, reference["source"])
    gold = norm(reference["answer"]).replace(r"\%", "%")
    proposed = norm(answer).replace(r"\%", "%")
    contextual_percent = ("percent" in reference["question"].lower()
                          and gold.endswith("%") != proposed.endswith("%")
                          and gold.rstrip("%") == proposed.rstrip("%"))
    return direct or contextual_percent, contextual_percent and not direct


def check_answer(row, reference):
    answer = row["extra_info"]["answer"]
    if "</think>" in answer:
        answer = answer.split("</think>", 1)[1]
    return contextual_answer_ok(reference, candidate(answer))


def check_grammar(row):
    info = row["extra_info"]
    answer = info["answer"]
    if info["kind"] == "parallel_th":
        assert answer.startswith("<think>") and answer.count("<think>") == answer.count("</think>") == 1
        inside, outside = answer.split("</think>", 1)
        structure = parse(inside)
        assert structure["valid"] and len(structure["blocks"]) == 1
        block = structure["blocks"][0]
        assert block["numbered"] and len(block["paths"]) == 2
        assert parse(outside)["tags"] == 0 and all(tag not in outside for tag in TAGS)
        return 1
    if info["kind"] in {"control_th", "replay_th"}:
        assert answer.startswith("<think>") and answer.count("<think>") == answer.count("</think>") == 1
        assert all(tag not in answer for tag in TAGS)
    elif any(tag in answer for tag in TAGS):
        raise AssertionError((row["id"], info["kind"], "tags in non-parallel answer"))
    return 0


def main():
    assert TOKENIZER.is_dir(), TOKENIZER
    train = pd.read_parquet(TRAIN_OUT)
    val = pd.read_parquet(VAL_OUT)
    source_train = pd.read_parquet(SOURCE_TRAIN)
    source_val = pd.read_parquet(SOURCE_VAL)
    prepared = json.loads(AUDIT_OUT.read_text())
    pool = load_jsonl(POOL)
    merge_inside = load_jsonl(MERGE_INSIDE)
    replay_source = load_jsonl(REPLAY_SOURCE)

    positive_ids, control_ids, replay_ids, positive, controls, replay = select_ids(source_train)
    selected_replay = [problem_id for source in REPLAY_QUOTAS for problem_id in replay_ids[source]]
    expected_ids = set(positive_ids) | set(control_ids) | set(selected_replay)
    assert positive_ids == reviewed_positive_ids() and EXCLUDED_REVIEW_ID not in expected_ids
    assert len(train) == len(set(train.id)) == len(expected_ids) == 256
    assert set(train.id) == expected_ids
    assert train.id.tolist() == sorted(expected_ids,
                                       key=lambda problem_id: (stable_rank(ORDER_SEED, problem_id), problem_id))
    assert train["index"].tolist() == list(range(256))
    assert val.equals(source_val)
    assert not set(train.id) & set(val.id)

    expected_kind_ids = {
        "parallel_th": set(positive_ids),
        "control_th": set(control_ids),
        "replay_th": set(selected_replay),
    }
    actual_kind_ids = {name: set(train[train.extra_info.map(lambda info: info["kind"] == name)].id)
                       for name in expected_kind_ids}
    assert actual_kind_ids == expected_kind_ids
    assert collections.Counter(kind(row) for row in train.to_dict("records")) == {
        "replay_th": 160, "control_th": 50, "parallel_th": 46}
    assert collections.Counter(train[train.extra_info.map(lambda info: info["kind"] == "replay_th")].source) == REPLAY_QUOTAS

    source_by_kind = {"parallel_th": positive, "control_th": controls, "replay_th": replay}
    prompts_preserved = answers_preserved = 0
    for row in train.to_dict("records"):
        original = source_by_kind[kind(row)][row["id"]]
        assert signature(row) == signature(original), row["id"]
        prompts_preserved += row["extra_info"]["question"] == original["extra_info"]["question"]
        answers_preserved += row["extra_info"]["answer"] == original["extra_info"]["answer"]
    assert prompts_preserved == answers_preserved == 256

    # Check the original target files, not only equality with the v4 parquet.
    for problem_id in positive_ids:
        info = positive[problem_id]["extra_info"]
        assert info["question"] == mv_prompt(HEADER + pool[problem_id]["question"])
        assert info["answer"] == merge_inside[problem_id]["response"]
    for problem_id in control_ids:
        info = controls[problem_id]["extra_info"]
        assert info["question"] == mv_prompt(HEADER + pool[problem_id]["question"])
        assert info["answer"] == replay_source[problem_id]["response"]
    for problem_id in selected_replay:
        info = replay[problem_id]["extra_info"]
        assert info["question"] == HEADER + pool[problem_id]["question"]
        assert info["answer"] == replay_source[problem_id]["response"]

    v2_plan = json.loads(V2_PLAN.read_text())
    v2_control_ids = set(v2_plan["math_v1_reviewed_ids"] + v2_plan["math_new_audit_ids"]
                         + v2_plan["gsm_new_screened_ids"] + v2_plan["arc_v1_reviewed_ids"])
    v2_quality = json.loads(V2_QUALITY.read_text())
    v4_quality = json.loads(V4_QUALITY.read_text())
    assert set(control_ids) == v2_control_ids and len(v2_control_ids) == 50
    assert v2_quality["answers_correct"] == v2_quality["selected_distinct"] == 50
    assert v4_quality["splits"]["train"]["valid_two_path_blocks_inside_think"] == 555
    assert v4_quality["splits"]["train"]["answer_fields_match_pool"] == 555

    answer_verified = grammar_parallel = contextual_percent = 0
    for split_name, frame in (("train", train), ("val", val)):
        for row in frame.to_dict("records"):
            grammar_parallel += check_grammar(row)
            ok, contextual = check_answer(row, pool[row["id"]])
            assert ok, (split_name, row["id"], pool[row["id"]]["answer"],
                        candidate(row["extra_info"]["answer"]))
            answer_verified += 1
            contextual_percent += contextual

    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)
    for tag in TAGS:
        assert len(tokenizer.encode(tag, add_special_tokens=False)) == 1, tag
    lengths = {"train": {}, "val": {}}
    for split_name, frame in (("train", train), ("val", val)):
        for row in frame.to_dict("records"):
            info = row["extra_info"]
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": info["question"]}],
                add_generation_prompt=True, tokenize=False,
                enable_thinking=info["enable_thinking"],
            )
            count = len(tokenizer.encode(prompt + info["answer"] + tokenizer.eos_token,
                                         add_special_tokens=False))
            assert count <= 4096, (split_name, row["id"], count)
            lengths[split_name][row["id"]] = count

    leak = json.loads(LEAK_AUDIT.read_text())
    assert leak["rows"] == len(pool) == 16547
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    pilot = pilot_rows()
    pilot_questions = {normalize_question(raw_problem(row["problem"])) for row in pilot}
    train_questions = {normalize_question(pool[problem_id]["question"]) for problem_id in train.id}
    val_questions = {normalize_question(pool[problem_id]["question"]) for problem_id in val.id}
    assert len(pilot_questions) == 40
    assert len(train_questions) == len(train) == 256
    assert len(val_questions) == len(set(val.id))
    assert not train_questions & pilot_questions
    assert not val_questions & pilot_questions
    assert not train_questions & val_questions
    raw_eval_ids = {row["problem_id"] for row in pilot}
    raw_collisions = sorted(set(train.id) & raw_eval_ids)
    assert raw_collisions == ["gsm8k-train/369"]
    collision_evidence = []
    for problem_id in raw_collisions:
        eval_rows = [row for row in pilot if row["problem_id"] == problem_id]
        assert len(eval_rows) == 1
        train_question = pool[problem_id]["question"]
        eval_question = raw_problem(eval_rows[0]["problem"])
        assert normalize_question(train_question) != normalize_question(eval_question)
        collision_evidence.append({"id": problem_id, "train_question": train_question,
                                   "eval_question": eval_question, "questions_equal": False})

    assert prepared["seeds"] == {"replay": REPLAY_SEED, "row_order": ORDER_SEED}
    assert prepared["train"]["parallel_th_ids"] == positive_ids
    assert prepared["train"]["control_th_ids"] == control_ids
    assert prepared["train"]["replay_th_ids"] == replay_ids
    assert prepared["overlap"]["raw_id_collisions_with_different_questions"] == collision_evidence

    report = prepared | {
        "status": "audited",
        "checks": {
            "exact_train_composition": True,
            "deterministic_selection_reproduced": True,
            "unique_train_ids": len(expected_ids),
            "source_rows_preserved": 256,
            "prompts_preserved": prompts_preserved,
            "answers_preserved": answers_preserved,
            "v4_val_copied_verbatim": True,
            "parallel_grammar_rows": grammar_parallel,
            "answers_verified": answer_verified,
            "contextual_percent_answers": contextual_percent,
            "train_max_tokens": max(lengths["train"].values()),
            "val_max_tokens": max(lengths["val"].values()),
            "over_4096": 0,
            "train_val_id_overlap": 0,
            "train_eval_normalized_question_overlap": 0,
            "val_eval_normalized_question_overlap": 0,
            "full_pool_leak_audit": {"eval_leak_pairs": 0, "math_test_dup_variant": 0,
                                     "exact_prompt_duplicates": 0},
        },
        "lengths": lengths,
    }
    temporary = AUDIT_OUT.with_suffix(".tmp.json")
    try:
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, AUDIT_OUT)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps(report["checks"], ensure_ascii=False))


if __name__ == "__main__":
    main()
