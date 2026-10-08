"""Check paired exp21 SFT arms before starting a GPU job.

Usage: python audit_sft_parity.py M1_PREFIX M2_PREFIX [CONTROL_PREFIX] [m1|m2] [OUT.json]
All prefixes name the train/val parquet pair produced by build_sft.py.
"""
import collections
import json
import sys

import pandas as pd

from mv_format import strip_tags


def read(prefix):
    result = {}
    for split in ("train", "val"):
        frame = pd.read_parquet(f"{prefix}_{split}.parquet")
        result[split] = frame.to_dict("records")
    return result


def grouped(rows):
    output = collections.defaultdict(list)
    for r in rows:
        e = r["extra_info"]
        output[(e["kind"], e["id"])].append(e)
    return output


def signature(data):
    return {split: {
        "distinct_problems": len({r["id"] for r in rows}),
        "kinds": dict(collections.Counter(r["extra_info"]["kind"] for r in rows)),
        "rows": len(rows),
    } for split, rows in data.items()}


def check(first, second, control=None, control_source=None):
    arms = {"m1": first, "m2": second}
    if control is not None:
        arms["control"] = control
    assert all(not ({r["id"] for r in arm["train"]} & {r["id"] for r in arm["val"]}) for arm in arms.values())
    for split in ("train", "val"):
        groups = {name: grouped(arm[split]) for name, arm in arms.items()}
        replay = {name: {key: sorted((e["question"], e["answer"], e["enable_thinking"]) for e in values)
                         for key, values in group.items() if key[0].startswith("replay_")}
                  for name, group in groups.items()}
        assert all(rows == replay["m1"] for rows in replay.values()), (split, "replay mismatch")
        primary = {name: {(key[1], len(values)) for key, values in group.items()
                          if key[0] in ("parallel", "control")}
                   for name, group in groups.items()}
        assert all(rows == primary["m1"] for rows in primary.values()), (split, "primary IDs or repetitions differ")
        for name, group in groups.items():
            assert set(group) == set(groups["m1"]) or name == "control", (split, name, "kind mismatch")
            for key, values in group.items():
                assert len({e["question"] for e in values}) == 1, (split, name, key, "prompt mismatch within arm")
                assert len({e["answer"] for e in values}) == 1, (split, name, key, "answer mismatch within arm")
                assert len({e["enable_thinking"] for e in values}) == 1, (split, name, key, "mode mismatch")
        for (kind, key), values in groups["m1"].items():
            if kind == "parallel":
                assert values[0]["question"] == groups["m2"][(kind, key)][0]["question"], (split, key, "prompt mismatch")
                if control is not None:
                    c = groups["control"][("control", key)][0]
                    source = groups[control_source][(kind, key)][0]
                    assert c["answer"] == strip_tags(source["answer"]).strip(), (split, key, "control text mismatch")
                    assert not c["enable_thinking"]
        assert {r["id"] for r in first[split]} == {r["id"] for r in second[split]}
        if control is not None:
            assert {r["id"] for r in first[split]} == {r["id"] for r in control[split]}
    return {name: signature(data) for name, data in arms.items()}


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args.pop() if args and args[-1].endswith(".json") else None
    assert len(args) in (2, 4), "expected M1 M2 [CONTROL m1|m2] [OUT.json]"
    assert len(args) == 2 or args[3] in ("m1", "m2")
    report = check(read(args[0]), read(args[1]), read(args[2]) if len(args) == 4 else None,
                   args[3] if len(args) == 4 else None)
    encoded = json.dumps(report, indent=2, ensure_ascii=False)
    if out:
        open(out, "w").write(encoded + "\n")
    print(encoded)
