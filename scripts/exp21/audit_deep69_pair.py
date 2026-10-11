"""Fail-closed CPU audit for the matched Deep69 tagged/plain pair."""

import collections
import json
import os
import tarfile
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from checks import candidate, correct
from mv_format import TAGS, parse
from prepare_deep51_pair import (
    DEEP,
    DEEP_AUDIT,
    DEEP_LEAK,
    GLOBAL_LEAK,
    PILOT_ARCHIVE,
    POOL,
    load_jsonl,
    normalize,
    plain_response,
    raw_problem,
    underlying_solution,
)
from prepare_deep69_pair import (
    CONTROL_COUNT,
    GSM_POSITIVE_IDS,
    PLAIN_TRAIN,
    REPLAY_BY_KIND_AND_SOURCE,
    TAGGED_TRAIN,
    V4_INDEPENDENT_GSM,
    V4_MANUAL_GSM,
    V4_RECOVERY_AUDIT,
    V4_TRAIN,
    question_of,
    review_provenance,
)
from prepare_deep51_pair import RECOVERY_TRAIN


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
OUTPUT = RUN / "data/sft_deep69_pair_quality.json"
TOKENIZER = Path(os.environ.get(
    "EXP21_TOKENIZER",
    "/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer",
))


def exact_tokens(tokenizer, info):
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": info["question"]}],
        add_generation_prompt=True,
        tokenize=False,
        enable_thinking=info["enable_thinking"],
    )
    return len(tokenizer(prompt + info["answer"] + tokenizer.eos_token,
                         add_special_tokens=False).input_ids)


def answer_ok(row, pool):
    answer = row["extra_info"]["answer"]
    if row["extra_info"]["enable_thinking"]:
        assert answer.count("</think>") == 1
        answer = answer.split("</think>", 1)[1]
    gold, proposed = pool[row["id"]]["answer"], candidate(answer)
    if correct(gold, proposed, row["source"]):
        return True
    return "percent" in pool[row["id"]]["question"].lower() and gold.rstrip("%") == proposed.rstrip("%")


def pilot_raw_rows():
    rows = []
    with tarfile.open(PILOT_ARCHIVE) as archive:
        for name in sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl")):
            handle = archive.extractfile(name)
            assert handle is not None
            rows.extend(json.loads(line) for line in handle)
    assert len(rows) == 40
    return rows


def v4_review_evidence(problem_id):
    evidence = review_provenance(problem_id)
    assert (problem_id in V4_MANUAL_GSM) == ("v4_manual_read" in evidence)
    assert (problem_id in V4_INDEPENDENT_GSM) == ("v4_independent_review" in evidence)
    return evidence


def main():
    assert TOKENIZER.is_dir(), TOKENIZER
    tagged, plain = pd.read_parquet(TAGGED_TRAIN), pd.read_parquet(PLAIN_TRAIN)
    pool = {row["id"]: row for row in load_jsonl(POOL)}
    deep = {row["id"]: row for row in load_jsonl(DEEP)}
    deep_audit = {row["id"]: row for row in load_jsonl(DEEP_AUDIT)}
    deep_ids, positive_ids = set(deep), set(deep) | GSM_POSITIVE_IDS
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)

    assert len(tagged) == len(plain) == 256
    assert tagged[["id", "copy_index", "index"]].equals(plain[["id", "copy_index", "index"]])
    assert tagged["index"].tolist() == list(range(256))
    assert len(set(tagged.id)) == len(tagged) == 256
    assert set(tagged[tagged.extra_info.map(lambda info: info["kind"] == "parallel_th")].id) == positive_ids
    assert len(positive_ids) == 69 and len(deep_ids) == 51 and len(GSM_POSITIVE_IDS) == 18
    assert collections.Counter(info["kind"] for info in tagged.extra_info) == {
        "parallel_th": 69, "control_th": CONTROL_COUNT, "replay_th": 71, "replay_nt": 71,
    }
    assert collections.Counter(info["kind"] for info in plain.extra_info) == {
        "control_th": 69 + CONTROL_COUNT, "replay_th": 71, "replay_nt": 71,
    }

    source_v4 = {row["index"]: row for row in pd.read_parquet(V4_TRAIN).to_dict("records")}
    source_recovery = {row["index"]: row for row in pd.read_parquet(RECOVERY_TRAIN).to_dict("records")}
    tagged_lengths, plain_lengths = {}, {}
    source_preserved = {"deep51": 0, "recovery8_gsm": 0, "nonpositive": 0}
    independence_evidence = {"deep51": 0, "recovery8_gsm": 0}
    for left, right in zip(tagged.to_dict("records"), plain.to_dict("records")):
        key = f"{left['index']}:{left['id']}"
        assert left["id"] == right["id"] and left["copy_index"] == right["copy_index"] == 0
        assert left["extra_info"]["question"] == right["extra_info"]["question"]
        if left["id"] not in positive_ids:
            assert left == right
            assert all(tag not in left["extra_info"]["answer"] for tag in TAGS)
            source_map = source_recovery if left["source_origin"] == "recovery8" else source_v4
            source = source_map[left["source_index"]].copy()
            source.pop("index", None)
            actual = left.copy()
            for key in ("index", "copy_index", "source_origin", "source_index"):
                actual.pop(key, None)
            assert actual == source
            source_preserved["nonpositive"] += 1
        elif left["id"] in deep_ids:
            source, review = deep[left["id"]], deep_audit[left["id"]]["review"]
            assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
            assert review["independent_paths"] and review["source_preserved"]
            assert left["extra_info"]["answer"] == source["response"]
            assert right["extra_info"]["answer"] == plain_response(source["response"])
            source_preserved["deep51"] += 1
            independence_evidence["deep51"] += 1
        else:
            assert left["source_origin"] == "recovery8"
            source = source_recovery[left["source_index"]]
            assert source["extra_info"]["kind"] == "parallel_th" and source["source"] == "gsm8k"
            assert left["extra_info"]["question"] == source["extra_info"]["question"]
            assert left["extra_info"]["answer"] == source["extra_info"]["answer"]
            assert right["extra_info"]["answer"] == plain_response(source["extra_info"]["answer"])
            assert v4_review_evidence(left["id"])
            source_preserved["recovery8_gsm"] += 1
            independence_evidence["recovery8_gsm"] += 1

        if left["id"] in positive_ids:
            structure = parse(left["extra_info"]["answer"])
            assert structure["valid"] and len(structure["blocks"]) == 1
            assert structure["blocks"][0]["numbered"] and len(structure["blocks"][0]["paths"]) == 2
            assert all(tag not in left["extra_info"]["answer"].split("</think>", 1)[1] for tag in TAGS)
            assert all(tag not in right["extra_info"]["answer"] for tag in TAGS)
            assert underlying_solution(left["extra_info"]["answer"]) == normalize(right["extra_info"]["answer"])
        assert answer_ok(left, pool) and answer_ok(right, pool)
        tagged_lengths[key] = exact_tokens(tokenizer, left["extra_info"])
        plain_lengths[key] = exact_tokens(tokenizer, right["extra_info"])

    assert source_preserved == {"deep51": 51, "recovery8_gsm": 18, "nonpositive": 187}
    assert independence_evidence == {"deep51": 51, "recovery8_gsm": 18}
    val = pd.read_parquet(RUN / "data/sft_v4_recovery8_val.parquet")
    train_questions = {question_of(row, pool) for row in tagged.to_dict("records")}
    val_questions = {normalize(pool[row_id]["question"]) for row_id in val.id}
    pilot = pilot_raw_rows()
    pilot_questions = {normalize(raw_problem(row["problem"])) for row in pilot}
    assert len(train_questions) == 256 and not train_questions & val_questions and not train_questions & pilot_questions
    raw_369 = [row for row in pilot if row["problem_id"] == "gsm8k-train/369"]
    assert len(raw_369) == 1 and normalize(pool["gsm8k-train/369"]["question"]) != normalize(raw_problem(raw_369[0]["problem"]))
    leak, deep_leak = json.loads(GLOBAL_LEAK.read_text()), json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0
    assert json.loads(V4_RECOVERY_AUDIT.read_text())["checks"]["train_eval_normalized_question_overlap"] == 0
    assert max(tagged_lengths.values()) <= 4096 and max(plain_lengths.values()) <= 4096

    report = {
        "status": "audited",
        "checks": {
            "tagged_train_rows": 256, "plain_train_rows": 256, "unique_train_ids": 256,
            "positive_rows": 69, "unique_positive_ids": 69,
            "deep51_math_positive_rows": 51, "recovery8_gsm_positive_rows": 18,
            "same_row_order": True, "nonpositive_rows_identical": True,
            "source_answers_verbatim": source_preserved,
            "plain_underlying_solution_equivalent": 69,
            "independence_evidence": independence_evidence,
            "tagged_grammar_inside_think": 69, "plain_tags": 0, "tagged_tags_outside_think": 0,
            "nonpositive_tags": 0,
            "answers_match_pool": 512,
            "replay_th_rows": 71, "replay_nt_rows": 71,
            "replay_by_kind_and_source": REPLAY_BY_KIND_AND_SOURCE,
            "train_val_normalized_question_overlap": 0,
            "train_pilot40_normalized_question_overlap": 0,
            "raw_id369_pilot_collision_is_different_question": True,
            "global_eval_leaks": 0, "deep51_eval_leaks": 0, "over_4096": 0,
        },
        "lengths": {
            "tagged_min": min(tagged_lengths.values()), "tagged_max": max(tagged_lengths.values()),
            "plain_min": min(plain_lengths.values()), "plain_max": max(plain_lengths.values()),
            "tagged": tagged_lengths, "plain": plain_lengths,
        },
        "limitations": [
            "Compared with Deep51-1x, both the positive domain mix and replay thinking-mode mix change.",
            "Therefore this candidate can test practical GSM block recovery but cannot isolate either change causally.",
        ],
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
