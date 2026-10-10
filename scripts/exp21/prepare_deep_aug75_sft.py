"""Matched tagged/control SFT for 75 deeply reviewed Sol thinking solutions.

Usage: python -B scripts/exp21/prepare_deep_aug75_sft.py [--new-copies 4] [--name sft_sol_deep75]
The old 187 appear once, the 75 new deeper solutions new-copies times, and
300 correct Qwen responses appear once in each of thinking and no-thinking.
"""
import argparse
import collections
import json
import random
from pathlib import Path

import pandas as pd

from build_sft import row
from mv_format import strip_tags

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/21-qwen3-0.6b-multiverse"
DATA = BASE / "data"
SEED = 21


def read(path):
    return [json.loads(line) for line in path.open()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new-copies", type=int, default=4)
    ap.add_argument("--name", default="sft_sol_deep75")
    ap.add_argument("--extra-file", type=Path, help="independently reviewed additional inside-thinking rows, one copy")
    args = ap.parse_args()
    assert 1 <= args.new_copies <= 4
    assert args.name.startswith("sft_sol_deep75") and "/" not in args.name
    old = read(BASE / "audit/think_trace_sol/selected187.jsonl")
    pilot = read(BASE / "audit/deep_trace_pilot/tagged24.jsonl")
    new = read(BASE / "audit/deep_trace_round2/accepted51.jsonl")
    extra = read(args.extra_file) if args.extra_file else []
    replay_nt, replay_th = read(DATA / "replay_nt.jsonl"), read(DATA / "replay_th.jsonl")
    assert (len(old), len(pilot), len(new), len(replay_nt), len(replay_th)) == (187, 24, 51, 300, 300)
    primary = old + pilot + new + extra
    assert len({r["id"] for r in primary}) == 262 + len(extra)
    replay_ids = {r["id"] for r in replay_nt + replay_th}
    assert not ({r["id"] for r in primary} & replay_ids)
    if not extra:
        (DATA / "sol_deep75.jsonl").write_text("".join(
            json.dumps({"id": r["id"], "question": r["question"], "response": r["response"]}, ensure_ascii=False) + "\n"
            for r in pilot + new))

    specs = [("primary_old", "parallel_th", r) for r in old]
    specs += [("primary_deep", "parallel_th", r) for _ in range(args.new_copies) for r in pilot + new]
    specs += [("replay_nt", "replay_nt", r) for r in replay_nt]
    specs += [("replay_th", "replay_th", r) for r in replay_th]
    specs += [("primary_extra", "parallel_th", r) for r in extra]
    assert len(specs) == 187 + 75 * args.new_copies + 600 + len(extra)
    random.Random(SEED).shuffle(specs)
    val_ids = set(pd.read_parquet(DATA / "sft_sol_th_187_val.parquet")["id"])
    assert val_ids <= {r["id"] for r in old + replay_nt + replay_th}
    assert not val_ids & {r["id"] for r in pilot + new + extra}

    arms = {}
    for arm in ("tagged", "control"):
        rows = []
        for category, kind, source in specs:
            actual = "control_th" if arm == "control" and kind == "parallel_th" else kind
            item = row(actual, source)
            item["category"] = category
            rows.append(item)
        prefix = DATA / f"{args.name}_{arm}"
        arms[arm] = {}
        for split, part in (("train", [r for r in rows if r["id"] not in val_ids]),
                            ("val", [r for r in rows if r["id"] in val_ids])):
            frame = pd.DataFrame(part)
            frame["index"] = range(len(frame))
            frame.to_parquet(f"{prefix}_{split}.parquet")
            arms[arm][split] = frame

    for split in ("train", "val"):
        a, b = arms["tagged"][split], arms["control"][split]
        assert len(a) == len(b) and a["id"].tolist() == b["id"].tolist()
        assert a["category"].tolist() == b["category"].tolist()
        for tagged, control in zip(a.to_dict("records"), b.to_dict("records")):
            t, c = tagged["extra_info"], control["extra_info"]
            assert t["question"] == c["question"]
            assert t["enable_thinking"] == c["enable_thinking"]
            if tagged["category"].startswith("primary"):
                assert strip_tags(t["answer"]).strip() == c["answer"]
            else:
                assert t["answer"] == c["answer"]

    counts = {split: dict(collections.Counter(arms["tagged"][split]["category"])) for split in ("train", "val")}
    report = {"seed": SEED, "primary_distinct": len(primary), "new_deep_distinct": 75,
              "new_extra_distinct": len(extra),
              "old_primary_copies": 1, "new_deep_copies": args.new_copies, "replay_nt": 300, "replay_th": 300,
              "total_rows": len(specs), "split_rows": {s: len(arms["tagged"][s]) for s in ("train", "val")},
              "categories": counts, "new_primary_in_val": 0,
              "tag_free_control_exact_text": True, "questions_and_order_matched": True,
              "validation_ids_reused_from": "data/sft_sol_th_187_val.parquet",
              "input_files": ["audit/think_trace_sol/selected187.jsonl", "audit/deep_trace_pilot/tagged24.jsonl",
                              "audit/deep_trace_round2/accepted51.jsonl", "data/replay_nt.jsonl", "data/replay_th.jsonl"]
              + ([str(args.extra_file)] if args.extra_file else [])}
    (DATA / f"{args.name}_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
