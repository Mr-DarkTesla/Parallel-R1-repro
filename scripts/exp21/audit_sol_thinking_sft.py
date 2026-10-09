"""Check actual tagged/control parquets for the fully reviewed Sol thinking SFT.

Usage: python -B scripts/exp21/audit_sol_thinking_sft.py TOKENIZER
Reads the fixed exp21 paths below and writes an audit JSON. No model or GPU needed.
"""
import collections
import json
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from mv_format import ANY_TAG, strip_tags


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = BASE / "data"
AUDIT = BASE / "audit/think_trace_sol"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_jsonl(path):
    return [json.loads(line) for line in path.open() if line.strip()]


def load(prefix, split):
    return pd.read_parquet(DATA / f"{prefix}_{split}.parquet").to_dict("records")


def main(tokenizer_path):
    selected = read_jsonl(AUDIT / "selected187.jsonl")
    primary_ids = {r["id"] for r in selected}
    replay = {name: read_jsonl(DATA / f"{name}.jsonl") for name in ("replay_nt", "replay_th")}
    replay_ids = {r["id"] for rows in replay.values() for r in rows}
    require(len(selected) == len(primary_ids) == 187, "187 unique primary rows required")
    require(not primary_ids & replay_ids, "primary and replay question overlap")
    require(all(len(rows) == 300 for rows in replay.values()), "expected 300 rows in each replay set")

    tagged = {split: load("sft_sol_th_187", split) for split in ("train", "val")}
    control = {split: load("sft_control_sol_th_187", split) for split in ("train", "val")}
    require({split: len(rows) for split, rows in tagged.items()} == {"train": 1111, "val": 50},
            "tagged split sizes differ")
    require({split: len(rows) for split, rows in control.items()} == {"train": 1111, "val": 50},
            "control split sizes differ")
    for arm in (tagged, control):
        require(not ({r["id"] for r in arm["train"]} & {r["id"] for r in arm["val"]}),
                "same ID in train and val")
        require(not ({r["extra_info"]["question"] for r in arm["train"]} &
                     {r["extra_info"]["question"] for r in arm["val"]}),
                "same prompt in train and val")

    counts = {}
    for split in ("train", "val"):
        left, right = tagged[split], control[split]
        require([r["id"] for r in left] == [r["id"] for r in right], "row order or split changed")
        counts[split] = dict(collections.Counter(r["extra_info"]["kind"] for r in left))
        for t, c in zip(left, right):
            ti, ci = t["extra_info"], c["extra_info"]
            require(ti["question"] == ci["question"], f"prompt differs: {t['id']}")
            require(ti["enable_thinking"] == ci["enable_thinking"], f"thinking mode differs: {t['id']}")
            if t["id"] in primary_ids:
                require(ti["kind"] == "parallel_th" and ci["kind"] == "control_th", f"kind differs: {t['id']}")
                require(ti["answer"].startswith("<think>") and ti["answer"].count("</think>") == 1,
                        f"invalid thinking answer: {t['id']}")
                require(ci["answer"] == strip_tags(ti["answer"]).strip(), f"control text differs: {t['id']}")
                require(not ANY_TAG.search(ci["answer"]), f"tag in control: {t['id']}")
                require(ti["enable_thinking"], f"thinking disabled for primary: {t['id']}")
            else:
                require(t["id"] in replay_ids, f"unknown row: {t['id']}")
                require(ti["kind"] == ci["kind"] in replay, f"replay kind differs: {t['id']}")
                require(ti["answer"] == ci["answer"], f"replay text differs: {t['id']}")
                require(ti["enable_thinking"] == (ti["kind"] == "replay_th"), f"replay mode differs: {t['id']}")

    all_tagged = tagged["train"] + tagged["val"]
    all_control = control["train"] + control["val"]
    require(collections.Counter(r["id"] for r in all_tagged if r["id"] in primary_ids) ==
            collections.Counter({id: 3 for id in primary_ids}), "primary repeat count differs")
    for name, rows in replay.items():
        source_ids = collections.Counter(r["id"] for r in rows)
        actual_ids = collections.Counter(r["id"] for r in all_tagged if r["extra_info"]["kind"] == name)
        require(actual_ids == source_ids, f"{name} replay rows differ")

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    max_tokens = {}
    for name, rows in (("tagged", all_tagged), ("control", all_control)):
        maximum = 0
        for row in rows:
            info = row["extra_info"]
            prompt = tokenizer.apply_chat_template([{"role": "user", "content": info["question"]}],
                                                   add_generation_prompt=True, tokenize=False,
                                                   enable_thinking=info["enable_thinking"])
            n = len(tokenizer.encode(prompt, add_special_tokens=False))
            n += len(tokenizer.encode(info["answer"] + tokenizer.eos_token, add_special_tokens=False))
            maximum = max(maximum, n)
        require(maximum <= 4096, f"{name} max tokens {maximum} exceeds 4096")
        max_tokens[name] = maximum

    summary = {"tagged_train": len(tagged["train"]), "tagged_val": len(tagged["val"]),
               "control_train": len(control["train"]), "control_val": len(control["val"]),
               "unique_primary": len(primary_ids), "primary_repeats": 3,
               "replay_nt": len(replay["replay_nt"]), "replay_th": len(replay["replay_th"]),
               "primary_replay_overlap": 0, "matched_order_prompt_split": True,
               "control_exact_tag_stripping": True, "thinking_mode_matched": True,
               "kinds_in_tagged": counts, "max_tokens": max_tokens,
               "tokenizer_path": str(tokenizer_path),
               "tagged_prefix": str(DATA / "sft_sol_th_187"),
               "control_prefix": str(DATA / "sft_control_sol_th_187")}
    (DATA / "sft_sol_th_187_audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: audit_sol_thinking_sft.py TOKENIZER")
    main(sys.argv[1])
