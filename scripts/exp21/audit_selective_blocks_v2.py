"""Audit selective-blocks v2 for data integrity and SFT compatibility."""
import collections
import json
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from build_sft import HEADER, row
from checks import candidate, correct
from make_mv_prompts import mv_prompt
from mv_format import TAGS


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
BASE = DATA / "sft_selective_blocks_m1_text1"
SELECTIVE = DATA / "sft_selective_blocks_v2"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"


def load_jsonl(path):
    return {record["id"]: record for record in map(json.loads, path.open())}


def kind(record):
    return record["extra_info"]["kind"]


def signature(record):
    return json.dumps({key: value for key, value in record.items() if key != "index"}, sort_keys=True)


def answer_types(frame, pool):
    return collections.Counter(pool[id_]["answer_type"] for id_ in frame.id)


def main():
    base = pd.read_parquet(f"{BASE}_train.parquet")
    train = pd.read_parquet(f"{SELECTIVE}_train.parquet")
    base_val = pd.read_parquet(f"{BASE}_val.parquet")
    val = pd.read_parquet(f"{SELECTIVE}_val.parquet")
    plan = json.loads((DATA / "sft_selective_blocks_v2_audit.json").read_text())
    pool = load_jsonl(DATA / "pool.jsonl")
    replay = load_jsonl(DATA / "replay_th.jsonl")
    selected = plan["math_v1_reviewed_ids"] + plan["math_new_audit_ids"] + plan["gsm_new_screened_ids"] + plan["arc_v1_reviewed_ids"]
    new_selected = plan["math_new_audit_ids"] + plan["gsm_new_screened_ids"]
    assert len(selected) == len(set(selected)) == 50
    assert len(new_selected) == 12
    assert len(base) == len(train) == 2748 and len(val) == 63 and base_val.equals(val)
    assert not set(train.id) & set(val.id)
    assert collections.Counter(base.source) == collections.Counter(train.source)
    assert answer_types(base, pool) == answer_types(train, pool)

    removed = set(plan["removed_positive_ids"]["math"] + plan["removed_positive_ids"]["gsm8k"])
    base_remaining = [record for record in base.to_dict("records")
                      if not (record["id"] in removed and kind(record) == "parallel_th")]
    base_remaining_signatures = collections.Counter(map(signature, base_remaining))
    train_signatures = collections.Counter(map(signature, train.to_dict("records")))
    assert base_remaining_signatures <= train_signatures
    added_signatures = train_signatures - base_remaining_signatures
    assert sum(added_signatures.values()) == 360
    added_rows = [json.loads(value) for value, count in added_signatures.items() for _ in range(count)]
    assert all(kind(record) == "control_th" and record["id"] in set(plan["math_v1_reviewed_ids"] + new_selected)
               for record in added_rows)

    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
    lengths, correct_count, exact_text_count = {}, 0, 0
    per_id_controls = {}
    for id_ in selected:
        reference, trace = pool[id_], replay[id_]
        assert trace["question"] == reference["question"]
        assert trace["response"].startswith("<think>")
        assert trace["response"].count("<think>") == trace["response"].count("</think>") == 1
        assert not any(tag in trace["response"] for tag in TAGS)
        rows = [record["extra_info"] for record in train.to_dict("records")
                if record["id"] == id_ and kind(record) == "control_th"]
        expected = 3 if id_.startswith("arc-") else 18
        assert len(rows) == expected, (id_, len(rows))
        assert all(info["question"] == mv_prompt(HEADER + reference["question"]) for info in rows)
        assert all(info["answer"] == trace["response"] and info["enable_thinking"] for info in rows)
        answer = rows[0]["answer"]
        assert answer.count("<think>") == answer.count("</think>") == 1
        assert not any(tag in answer for tag in TAGS)
        assert correct(reference["answer"], candidate(answer.split("</think>", 1)[1]), reference["source"]), id_
        length = len(tokenizer.encode(rows[0]["question"] + answer + tokenizer.eos_token, add_special_tokens=False))
        assert length <= 4096, (id_, length)
        lengths[id_] = length
        per_id_controls[id_] = expected
        correct_count += 1
        exact_text_count += 1

    controls = train[train.extra_info.map(lambda x: x["kind"] == "control_th")]
    positives = train[train.extra_info.map(lambda x: x["kind"] == "parallel_th")]
    assert len(controls) == 510 and len(positives) == 555
    assert collections.Counter(controls.source) == {"math": 252, "gsm8k": 180, "arc": 78}
    assert collections.Counter(positives.source) == {"math": 372, "gsm8k": 183}
    result = {
        "selected_distinct": len(selected), "new_audit_selected_distinct": len(new_selected),
        "previously_independently_reviewed_distinct": 38,
        "answers_correct": correct_count, "exact_qwen_trace_text": exact_text_count,
        "one_think_pair_and_no_multiverse_tags": len(selected),
        "max_training_tokens": max(lengths.values()), "over_4096": 0,
        "train_rows": len(train), "val_rows": len(val), "val_identical_to_v1": True,
        "train_val_problem_ids_disjoint": True,
        "source_counts_preserved": True, "answer_type_counts_preserved": True,
        "unchanged_rows_preserved": True,
        "removed_positive_copies": plan["removed_positive_copies"],
        "no_block_multiverse_rows": len(controls), "positive_parallel_rows": len(positives),
        "control_rows_by_source": dict(collections.Counter(controls.source)),
        "parallel_rows_by_source": dict(collections.Counter(positives.source)),
        "per_id_control_copies": per_id_controls, "lengths": lengths,
        "leakcheck": "Every selected question exactly matches data/pool.jsonl, the prior leakchecked cleaned pool; see DATASET_POOL.md.",
    }
    (DATA / "sft_selective_blocks_v2_quality.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in {"lengths", "per_id_control_copies"}}))


if __name__ == "__main__":
    main()
