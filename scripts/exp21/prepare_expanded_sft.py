"""Combine audited 187-row and new 180-row M1/M2 data; fix a shared SFT validation split.

Usage: python prepare_expanded_sft.py RESULTS_DIR
Writes combined JSONL, validation IDs, and a one-column parquet for build_sft.py.
"""
import collections
import json
import random
import sys
from pathlib import Path

import pandas as pd


PRIMARY_VAL = {"gsm8k": 3, "math": 5}
REPLAY_VAL_NT = {"gsm8k": 2, "math": 4, "arc": 1}
REPLAY_VAL_TH = {"gsm8k": 2, "math": 3, "arc": 1}


def read(path):
    return [json.loads(line) for line in path.open()]


def choose(rows, quota, seed):
    rng = random.Random(seed)
    out = []
    for source, n in quota.items():
        candidates = sorted((r for r in rows if r["source"] == source), key=lambda x: x["id"])
        rng.shuffle(candidates)
        assert len(candidates) >= n, (source, len(candidates), n)
        out.extend(candidates[:n])
    return out


def main(root):
    data = root / "data"
    old_m1, old_m2 = (read(data / name) for name in ("pair_final_m1.jsonl", "pair_audited_m2.jsonl"))
    new_m1, new_m2 = (read(data / name) for name in ("more_m1_matched180.jsonl", "more_m2_matched180.jsonl"))
    replay_nt, replay_th = (read(data / name) for name in ("replay_nt.jsonl", "replay_th.jsonl"))
    assert (len(old_m1), len(old_m2), len(new_m1), len(new_m2)) == (187, 187, 180, 180)
    m1, m2 = old_m1 + new_m1, old_m2 + new_m2
    assert len({r["id"] for r in m1}) == len({r["id"] for r in m2}) == 367
    assert collections.Counter((r["source"], r["answer_type"]) for r in m1) == collections.Counter(
        (r["source"], r["answer_type"]) for r in m2)
    for name, rows in (("m1", m1), ("m2", m2)):
        (data / f"pair_expanded_{name}.jsonl").write_text("".join(
            json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(rows, key=lambda x: x["id"])))

    primary_ids = {r["id"] for r in m1 + m2}
    new_ids = {r["id"] for r in new_m1 + new_m2}
    nt_ids, th_ids = ({r["id"] for r in rows} for rows in (replay_nt, replay_th))
    old_shared = {r["id"] for r in old_m1} & {r["id"] for r in old_m2}
    primary_val = choose([r for r in old_m1 if r["id"] in old_shared - nt_ids - th_ids - new_ids],
                         PRIMARY_VAL, 21065)
    nt_val = choose([r for r in replay_nt if r["id"] not in primary_ids | th_ids], REPLAY_VAL_NT, 21066)
    th_val = choose([r for r in replay_th if r["id"] not in primary_ids | nt_ids], REPLAY_VAL_TH, 21067)
    val_ids = {r["id"] for r in primary_val + nt_val + th_val}
    assert len(val_ids) == 21 and not val_ids & new_ids
    assert len(primary_val) * 3 + (len(nt_val) + len(th_val)) * 2 == 50
    selection = {"primary": [r["id"] for r in primary_val], "replay_nt": [r["id"] for r in nt_val],
                 "replay_th": [r["id"] for r in th_val], "val_rows_each_arm": 50,
                 "new_primary_in_val": 0, "primary_rows_each_arm": 367 * 3,
                 "replay_rows_each_arm": (len(replay_nt) + len(replay_th)) * 2,
                 "total_rows_each_arm": 367 * 3 + (len(replay_nt) + len(replay_th)) * 2,
                 "replay_fraction": 1200 / 2301}
    (root / "audit/expanded_sft_split.json").write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n")
    pd.DataFrame({"id": sorted(val_ids)}).to_parquet(data / "sft_expanded_val_ids_val.parquet", index=False)
    print(json.dumps(selection, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
