"""Prepare the small, matched Deep51 tagged/plain SFT pair.

The two training files have the same 256 IDs and order.  They differ only in
the 51 accepted Deep51 responses: the tagged arm is copied verbatim, while the
plain arm removes the Multiverse container, Goal/Outline/Conclusion plan text,
and Path tags.  The substantive text of both Paths remains in order.
"""

import collections
import hashlib
import json
import os
import re
import tarfile
import unicodedata
from copy import deepcopy
from pathlib import Path

import pandas as pd

from build_sft import HEADER
from make_mv_prompts import mv_prompt
from mv_format import TAGS, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
DEEP = RUN / "audit/deep_trace_round2/accepted51.jsonl"
DEEP_AUDIT = RUN / "audit/deep_trace_round2/accepted51_audit.jsonl"
DEEP_LEAK = RUN / "audit/deep_trace_round2/leakcheck_accepted51.summary.json"
RECOVERY_TRAIN = DATA / "sft_v4_recovery8_train.parquet"
RECOVERY_VAL = DATA / "sft_v4_recovery8_val.parquet"
POOL = DATA / "pool.jsonl"
GLOBAL_LEAK = RUN / "audit/leak_clean_recheck.json"
PILOT_ARCHIVE = RUN / "eval_archives/selective_v4_step56_masked_pilot.tgz"

TAGGED_TRAIN = DATA / "sft_deep51_tagged_train.parquet"
PLAIN_TRAIN = DATA / "sft_deep51_plain_train.parquet"
# Validation has no held-out Deep51 rows.  It is deliberately shared so its
# loss is comparable between arms and cannot change either training target.
SHARED_VAL = DATA / "sft_deep51_pair_val.parquet"
PLAN = DATA / "sft_deep51_pair_audit.json"

CONTROL_COUNT = 45
REPLAY_COUNT = 160
CONTROL_SEED = "deep51-pair-control-20261012"
ORDER_SEED = "deep51-pair-order-20261012"

BLOCK_RE = re.compile(
    r"<Parallel>\s*<Goal>.*?</Goal>\s*(?P<paths>(?:<Path>.*?</Path>\s*)+)"
    r"<Conclusion>.*?</Conclusion>\s*</Parallel>",
    re.DOTALL,
)
PATH_RE = re.compile(r"<Path>(?P<text>.*?)</Path>", re.DOTALL)


def load_jsonl(path):
    rows = [json.loads(line) for line in path.open()]
    assert len(rows) == len({row["id"] for row in rows}), path
    return rows


def stable_rank(seed, problem_id):
    return hashlib.sha256(f"{seed}\0{problem_id}".encode()).hexdigest()


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def raw_problem(prompt):
    marker = "\n\nProblem: "
    assert marker in prompt
    return prompt.rsplit(marker, 1)[1]


def pilot_questions():
    rows = []
    with tarfile.open(PILOT_ARCHIVE) as archive:
        for name in sorted(name for name in archive.getnames() if name.endswith("-block-rows.jsonl")):
            handle = archive.extractfile(name)
            assert handle is not None
            rows.extend(json.loads(line) for line in handle)
    assert len(rows) == 40
    return {normalize(raw_problem(row["problem"])) for row in rows}


def underlying_solution(response):
    """Drop exactly the block's plan scaffolding, retaining both path texts."""
    match = BLOCK_RE.search(response)
    assert match and response.count("<Parallel>") == response.count("</Parallel>") == 1
    paths = [item.group("text").strip() for item in PATH_RE.finditer(match.group("paths"))]
    assert len(paths) == 2
    return normalize(response[:match.start()] + "\n\n" + "\n\n".join(paths) + "\n\n" + response[match.end():])


def plain_response(response):
    match = BLOCK_RE.search(response)
    assert match
    paths = [item.group("text").strip() for item in PATH_RE.finditer(match.group("paths"))]
    plain = response[:match.start()] + "\n\n" + "\n\n".join(paths) + "\n\n" + response[match.end():]
    assert all(tag not in plain for tag in TAGS)
    assert underlying_solution(response) == normalize(plain)
    return plain


def recovery_rows():
    frame = pd.read_parquet(RECOVERY_TRAIN)
    assert len(frame) == len(set(frame.id)) == 256
    controls = [row for row in frame.to_dict("records") if row["extra_info"]["kind"] == "control_th"]
    replay = [row for row in frame.to_dict("records") if row["extra_info"]["kind"] == "replay_th"]
    assert len(controls) == 50 and len(replay) == REPLAY_COUNT
    return controls, replay


def main():
    deep = load_jsonl(DEEP)
    deep_audit = {row["id"]: row for row in load_jsonl(DEEP_AUDIT)}
    pool = {row["id"]: row for row in load_jsonl(POOL)}
    assert len(deep) == len(deep_audit) == 51
    deep_ids = {row["id"] for row in deep}
    assert all(row["id"] in pool and row["gold_answer"] == pool[row["id"]]["answer"] for row in deep)
    for row in deep:
        review = deep_audit[row["id"]]["review"]
        assert review["verdict"] == "useful" and review["answer_verdict"] == "correct"
        assert review["independent_paths"] and review["source_preserved"]
        structure = parse(row["response"])
        assert structure["valid"] and len(structure["blocks"]) == 1
        assert structure["blocks"][0]["numbered"] and len(structure["blocks"][0]["paths"]) == 2
        assert row["response"].startswith("<think>") and row["response"].count("</think>") == 1

    controls, replay = recovery_rows()
    controls = [row for row in controls if row["id"] not in deep_ids]
    replay = [row for row in replay if row["id"] not in deep_ids]
    controls = sorted(controls, key=lambda row: (stable_rank(CONTROL_SEED, row["id"]), row["id"]))[:CONTROL_COUNT]
    assert len(controls) == CONTROL_COUNT and len(replay) == REPLAY_COUNT
    assert len({row["id"] for row in controls}) == CONTROL_COUNT
    assert not deep_ids & {row["id"] for row in controls + replay}
    assert not {row["id"] for row in controls} & {row["id"] for row in replay}

    tagged, plain = [], []
    for source in deep:
        prompt = mv_prompt(HEADER + source["question"])
        tagged_info = {"question": prompt, "answer": source["response"], "enable_thinking": True,
                       "kind": "parallel_th", "id": source["id"]}
        plain_info = {"question": prompt, "answer": plain_response(source["response"]), "enable_thinking": True,
                      "kind": "control_th", "id": source["id"]}
        tagged.append({"data_source": "exp21_deep51_tagged", "id": source["id"], "source": "math",
                       "extra_info": tagged_info})
        plain.append({"data_source": "exp21_deep51_plain", "id": source["id"], "source": "math",
                      "extra_info": plain_info})

    other = controls + replay
    tagged.extend(deepcopy(other))
    plain.extend(deepcopy(other))
    assert len(tagged) == len(plain) == 51 + CONTROL_COUNT + REPLAY_COUNT == 256
    assert {row["id"] for row in tagged} == {row["id"] for row in plain}
    assert len({row["id"] for row in tagged}) == 256

    tagged.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    plain.sort(key=lambda row: (stable_rank(ORDER_SEED, row["id"]), row["id"]))
    for index, (left, right) in enumerate(zip(tagged, plain)):
        left["index"] = right["index"] = index
        assert left["id"] == right["id"]
        if left["id"] not in deep_ids:
            assert left == right

    val = pd.read_parquet(RECOVERY_VAL)
    train_questions = {normalize(pool[row["id"]]["question"]) for row in tagged}
    val_questions = {normalize(pool[row_id]["question"]) for row_id in val.id}
    pilot = pilot_questions()
    assert not train_questions & val_questions and not train_questions & pilot and not val_questions & pilot

    leak = json.loads(GLOBAL_LEAK.read_text())
    deep_leak = json.loads(DEEP_LEAK.read_text())
    assert leak["eval_leak_pairs"] == leak["math_test_dup_variant"] == leak["exact_prompt_duplicates"] == 0
    assert deep_leak["n_leaky_vs_our_evals"] == deep_leak["n_dup_or_variant_vs_our_evals"] == 0

    report = {
        "status": "prepared", "candidate": "deep51-paired-small", "seeds": {"control": CONTROL_SEED, "order": ORDER_SEED},
        "train": {"rows": 256, "unique_ids": 256, "deep51_ids": sorted(deep_ids),
                  "control_th_ids": [row["id"] for row in controls], "replay_th_ids": [row["id"] for row in replay],
                  "row_order_ids": [row["id"] for row in tagged],
                  "tagged_kind_counts": dict(collections.Counter(row["extra_info"]["kind"] for row in tagged)),
                  "plain_kind_counts": dict(collections.Counter(row["extra_info"]["kind"] for row in plain))},
        "validation": {"path": SHARED_VAL.name, "rows": len(val), "shared_verbatim_recovery8_validation": True,
                       "reason": "no held-out Deep51 IDs; validation must not create a train/val leak"},
        "transform": {"tagged": "accepted51 response copied verbatim", "plain": "remove Parallel container, Goal/Outline/Conclusion text, and Path tags; concatenate the two original Path texts in order", "underlying_solution_equivalence": 51},
        "overlap": {"train_val_normalized_question": 0, "train_pilot40_normalized_question": 0, "val_pilot40_normalized_question": 0},
        "leakcheck": {"deep51": DEEP_LEAK.name, "global_pool": GLOBAL_LEAK.name,
                      "deep51_eval_leaks": 0, "deep51_eval_dup_or_variant": 0},
    }
    outputs = [(TAGGED_TRAIN, pd.DataFrame(tagged)), (PLAIN_TRAIN, pd.DataFrame(plain)), (SHARED_VAL, val)]
    temporary = []
    try:
        for path, frame in outputs:
            temp = path.with_suffix(".tmp.parquet")
            frame.to_parquet(temp, index=False)
            temporary.append((path, temp))
        report_temp = PLAN.with_suffix(".tmp.json")
        report_temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        temporary.append((PLAN, report_temp))
        for path, temp in temporary:
            os.replace(temp, path)
    finally:
        for _, temp in temporary:
            temp.unlink(missing_ok=True)
    print(json.dumps(report["train"], ensure_ascii=False))


if __name__ == "__main__":
    main()
