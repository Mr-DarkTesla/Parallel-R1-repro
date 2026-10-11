#!/usr/bin/env python3
"""Pair M1-367 and reviewed Qwen4B-34 with exact-text plain control."""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from mv_format import ANY_TAG, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = RUN / "data"
AUDIT = RUN / "audit"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"
OUT = DATA / "qwen4b_mixed401"
VAL = DATA / "sft_expanded_val_ids"
FORBIDDEN_REPLAY = {"math-train/1514", "math-train/424"}


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main():
    m1 = read(DATA / "m1_rewrapped_tagged.jsonl")
    m1_plain = read(DATA / "m1_rewrapped_plain.jsonl")
    q4 = read(DATA / "qwen4b_rewrite_reviewed_tagged.jsonl")
    q4_plain = read(DATA / "qwen4b_rewrite_reviewed_plain.jsonl")
    report = json.loads((AUDIT / "qwen4b_rewrite_pair_report.json").read_text())
    assert len(m1) == 367 and len(q4) == len(q4_plain) == 34
    assert [r["id"] for r in m1] == [r["id"] for r in m1_plain]
    assert all(ANY_TAG.sub("", a["response"]) == b["response"] for a, b in zip(m1, m1_plain))
    assert report["ready_for_sft"] and report["checks"]["math_verify"] == 34
    assert [r["id"] for r in q4] == [r["id"] for r in q4_plain]
    assert all(ANY_TAG.sub("", a["response"]) == b["response"] for a, b in zip(q4, q4_plain))
    positive = sorted(m1 + q4, key=lambda row: row["id"])
    plain_positive = sorted(m1_plain + q4_plain, key=lambda row: row["id"])
    assert len(positive) == len({r["id"] for r in positive}) == 401
    assert len({r["question"].strip() for r in positive}) == 401
    assert [r["id"] for r in positive] == [r["id"] for r in plain_positive]
    assert all(ANY_TAG.sub("", a["response"]) == b["response"]
               for a, b in zip(positive, plain_positive))
    assert all(r["response"].startswith("<think>") and
               r["response"].count("</think>") == 1 and
               parse(r["response"])["valid"] and
               len(parse(r["response"])["blocks"]) == 1 and
               r["response"].count("Final Answer:") == 1 for r in positive)
    replay_nt = [r for r in read(DATA / "replay_nt.jsonl") if r["id"] not in FORBIDDEN_REPLAY]
    replay_th = read(DATA / "replay_th.jsonl")
    assert len(replay_nt) == 298 and len(replay_th) == 300
    assert not {r["id"] for r in replay_nt} & {r["id"] for r in q4}
    write(OUT.with_name(OUT.name + "_positive.jsonl"), positive)
    write(OUT.with_name(OUT.name + "_positive_plain.jsonl"), plain_positive)
    write(OUT.with_name(OUT.name + "_replay_nt.jsonl"), replay_nt)
    # Three positive copies plus one additional 4B copy: every 4B row appears four times.
    # build_sft's control_th compresses whitespace, so both arms use parallel_th
    # on paired source text; only plain metadata is relabelled after building.
    for arm in ("tagged", "plain"):
        primary = f"{OUT}_positive{'_plain' if arm == 'plain' else ''}.jsonl"
        qwen = DATA / f"qwen4b_rewrite_reviewed_{arm}.jsonl"
        arm_specs = ([f"parallel_th:{primary}"] * 3 + [f"parallel_th:{qwen}"] +
                     [f"replay_nt:{OUT}_replay_nt.jsonl"] * 2 +
                     [f"replay_th:{DATA / 'replay_th.jsonl'}"] * 2)
        subprocess.run([sys.executable, str(Path(__file__).with_name("build_sft.py")),
                        f"{OUT}_{arm}", "--rows", *arm_specs,
                        "--val-ids-from", str(VAL), "--seed", "21"], check=True)
    for split in ("train", "val"):
        path = Path(f"{OUT}_plain_{split}.parquet")
        rows = pd.read_parquet(path).to_dict("records")
        for row in rows:
            if row["extra_info"]["kind"] == "parallel_th":
                row["extra_info"] = dict(row["extra_info"], kind="control_th")
                row["data_source"] = "exp21_control_th"
        pd.DataFrame(rows).to_parquet(path, index=False)
    left = {split: pd.read_parquet(f"{OUT}_tagged_{split}.parquet").to_dict("records")
            for split in ("train", "val")}
    right = {split: pd.read_parquet(f"{OUT}_plain_{split}.parquet").to_dict("records")
             for split in ("train", "val")}
    tok = AutoTokenizer.from_pretrained(TOKENIZER)
    lengths = {"tagged": 0, "plain": 0}
    for split in ("train", "val"):
        assert [r["id"] for r in left[split]] == [r["id"] for r in right[split]]
        for a, b in zip(left[split], right[split]):
            ai, bi = a["extra_info"], b["extra_info"]
            assert ai["question"] == bi["question"] and ai["enable_thinking"] == bi["enable_thinking"]
            assert ANY_TAG.sub("", ai["answer"]) == bi["answer"]
            if ai["kind"] == "parallel_th":
                assert bi["kind"] == "control_th"
            else:
                assert ai == bi
            for arm, info in (("tagged", ai), ("plain", bi)):
                prompt = tok.apply_chat_template([{"role": "user", "content": info["question"]}],
                                                 add_generation_prompt=True, tokenize=False,
                                                 enable_thinking=info["enable_thinking"])
                size = len(tok.encode(prompt + info["answer"] + tok.eos_token, add_special_tokens=False))
                lengths[arm] = max(lengths[arm], size)
                assert size <= 4096, (a["id"], arm, size)
    assert not {r["id"] for r in left["train"]} & {r["id"] for r in left["val"]}
    assert not {r["extra_info"]["question"] for r in left["train"]} & \
        {r["extra_info"]["question"] for r in left["val"]}
    assert {r["id"] for r in left["val"]} == set(pd.read_parquet(f"{VAL}_val.parquet")["id"])
    result = {"status": "ready_for_paired_sft", "sources": {"m1": 367, "qwen4b": 34},
              "distinct_positive": 401, "reviewed_qwen4b": 34,
              "copies": {"m1": 3, "qwen4b": 4, "replay_nt": 2, "replay_th": 2},
              "replay_nt_filtered_ids": sorted(FORBIDDEN_REPLAY),
              "rows_per_arm": {split: len(left[split]) for split in left},
              "max_total_tokens": lengths, "val_overlap": 0,
              "plain_only_removes_tags": True,
              "command": "python scripts/exp21/build_qwen4b_mixed_pair.py"}
    (AUDIT / "qwen4b_mixed401_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
