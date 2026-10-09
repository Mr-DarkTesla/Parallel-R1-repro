"""Audit expanded 0.6B SFT arms and both possible tag-free controls.

Usage: python audit_expanded_sft.py RESULTS_DIR TOKENIZER_DIR
The new M1/M2 task IDs differ, so compare their source/answer-type distribution,
replay rows, validation IDs, repetitions, and the tag-free M1 control text.
"""
import collections
import datetime
import json
import re
import sys
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from mv_format import strip_tags
from build_sft import row


ARMS = {"m1": "sft_m1_expanded", "m2": "sft_m2_expanded",
        "control_m1": "sft_control_m1_expanded", "control_m2": "sft_control_m2_expanded"}


def read(path):
    return [json.loads(line) for line in path.open()]


def grouped(rows):
    groups = collections.defaultdict(list)
    for r in rows:
        e = r["extra_info"]
        groups[(e["kind"], e["id"])].append(e)
    return groups


def main(root, tokenizer_dir):
    if not __debug__:
        raise RuntimeError("Run the audit without python -O")
    data, audit = root / "data", root / "audit"
    split = json.loads((audit / "expanded_sft_split.json").read_text())
    val_ids = set(split["primary"] + split["replay_nt"] + split["replay_th"])
    pairs = {name: read(data / f"pair_expanded_{name}.jsonl") for name in ("m1", "m2")}
    replays = {kind: read(data / f"{kind}.jsonl") for kind in ("replay_nt", "replay_th")}
    new_ids = {r["id"] for method in ("m1", "m2")
               for r in read(data / f"more_{method}_matched180.jsonl")}
    assert len(pairs["m1"]) == len(pairs["m2"]) == 367
    assert not new_ids & val_ids
    assert len(val_ids) == 21 and split["val_rows_each_arm"] == 50
    assert split["new_primary_in_val"] == len(new_ids & val_ids)
    assert split["primary_rows_each_arm"] == 1101
    assert split["replay_rows_each_arm"] == 1200
    assert split["total_rows_each_arm"] == 2301
    distributions = {name: collections.Counter((r["source"], r["answer_type"]) for r in rows)
                     for name, rows in pairs.items()}
    assert distributions["m1"] == distributions["m2"]
    frames = {name: {part: pd.read_parquet(data / f"{prefix}_{part}.parquet").to_dict("records")
                     for part in ("train", "val")} for name, prefix in ARMS.items()}
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    max_total = max_response = 0
    report = {"arms": {}, "primary_distribution": {f"{a}/{b}": n for (a, b), n in distributions["m1"].items()},
              "audit_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "tokenizer_path": str(tokenizer_dir.resolve()),
              "inputs": {"parquet_prefixes": ARMS, "pair_files": [f"pair_expanded_{m}.jsonl" for m in ("m1", "m2")],
                         "replay_files": ["replay_nt.jsonl", "replay_th.jsonl"],
                         "new_files": [f"more_{m}_matched180.jsonl" for m in ("m1", "m2")]}}
    for name, parts in frames.items():
        train, val = parts["train"], parts["val"]
        assert (len(train), len(val)) == (2251, 50), name
        assert {r["id"] for r in val} == val_ids, name
        assert not {r["id"] for r in train} & val_ids, name
        groups = grouped(train + val)
        primary_kind = "control" if name.startswith("control_") else "parallel"
        sources = [(primary_kind, r) for r in pairs[name.removeprefix("control_")]] + [
            (kind, r) for kind, examples in replays.items() for r in examples]
        expected = {(kind, r["id"]): row(kind, r) for kind, r in sources}
        assert len(expected) == 967, name
        assert set(groups) == set(expected), name
        for actual in train + val:
            source = expected[(actual["extra_info"]["kind"], actual["id"])]
            assert all(actual[field] == source[field] for field in ("id", "source", "data_source", "extra_info")), (
                name, actual["id"])
        raw_questions = {(kind, r["id"]): re.sub(r"\s+", " ", r["question"]).strip().casefold()
                         for kind, r in sources}
        train_questions = {raw_questions[(r["extra_info"]["kind"], r["id"])] for r in train}
        val_questions = {raw_questions[(r["extra_info"]["kind"], r["id"])] for r in val}
        assert not train_questions & val_questions, name
        assert {key[1] for key in groups if key[0] == primary_kind} == {
            r["id"] for r in pairs[name.removeprefix("control_")]}
        assert collections.Counter(key[0] for key in groups) == {
            primary_kind: 367, "replay_nt": 300, "replay_th": 300}
        for (kind, _), values in groups.items():
            assert len(values) == (3 if kind == primary_kind else 2)
            assert all(v == values[0] for v in values)
            e = values[0]
            prompt = tokenizer.apply_chat_template([{"role": "user", "content": e["question"]}],
                                                   add_generation_prompt=True, tokenize=False,
                                                   enable_thinking=e["enable_thinking"])
            prompt_len = len(tokenizer.encode(prompt, add_special_tokens=False))
            response_len = len(tokenizer.encode(e["answer"] + tokenizer.eos_token, add_special_tokens=False))
            assert prompt_len + response_len <= 4096, (name, kind, e["id"])
            max_total = max(max_total, prompt_len + response_len)
            max_response = max(max_response, response_len)
        report["arms"][name] = {"train": len(train), "val": len(val),
                                "train_kinds": dict(collections.Counter(r["extra_info"]["kind"] for r in train)),
                                "val_kinds": dict(collections.Counter(r["extra_info"]["kind"] for r in val))}
    for part in ("train", "val"):
        groups = {name: grouped(frames[name][part]) for name in ARMS}
        for kind in ("replay_nt", "replay_th"):
            baseline = {key: values for key, values in groups["m1"].items() if key[0] == kind}
            assert all({key: values for key, values in arm.items() if key[0] == kind} == baseline
                       for arm in groups.values()), (part, kind)
        m1 = {key[1]: values[0] for key, values in groups["m1"].items() if key[0] == "parallel"}
        m2 = {key[1]: values[0] for key, values in groups["m2"].items() if key[0] == "parallel"}
        for name, source_rows in (("control_m1", m1), ("control_m2", m2)):
            control = {key[1]: values[0] for key, values in groups[name].items() if key[0] == "control"}
            assert source_rows.keys() == control.keys()
            for problem_id, source in source_rows.items():
                target = control[problem_id]
                assert target["question"] == source["question"] and not target["enable_thinking"]
                assert target["answer"] == strip_tags(source["answer"]).strip()
        for problem_id in m1.keys() & m2.keys():
            assert m1[problem_id]["question"] == m2[problem_id]["question"]
    report["max_tokens"] = {"response": max_response, "total": max_total}
    report["new_primary_in_val"] = len(new_ids & val_ids)
    report["shared_primary_ids"] = len({r["id"] for r in pairs["m1"]} & {r["id"] for r in pairs["m2"]})
    report["tag_free_control_exact_text"] = True
    report["replay_identical_all_arms"] = True
    report["source_text_matches_parquet"] = True
    report["normalized_question_train_val_overlap"] = 0
    (audit / "expanded_sft_parity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main(*(Path(arg) for arg in sys.argv[1:3]))
