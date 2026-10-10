"""Replace matched M1 examples with audited no-block thinking examples.

Keeps the previous text-loss=1 training size, validation rows, replay mixture,
source counts, and answer-type counts. ARC replay text is unchanged; only its
prompt teaches that an atomic task needs no parallel block.
"""
import collections
import json
import random
from pathlib import Path

import pandas as pd

from build_sft import row


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
PREFIX = DATA / "sft_expanded_th_m1_twopath_replay3_tagged"
OUTPUT = DATA / "sft_selective_blocks_m1_text1"
MATH_IDS = [
    "5901", "6060", "5361", "7243", "6356", "1214", "3269", "6198",
    "1000", "2808", "6038", "370",
]
ARC_IDS = [
    "MCAS_2005_5_36", "Mercury_401315", "Mercury_7228498", "MDSA_2009_5_46",
    "NYSEDREGENTS_2009_4_4", "Mercury_SC_401156", "Mercury_7163293",
    "Mercury_7283815", "NYSEDREGENTS_2011_4_25", "ACTAAP_2013_5_2",
    "Mercury_175070", "Mercury_7071593", "Mercury_7245805", "NCEOGA_2013_8_1",
    "MSA_2013_8_7", "NYSEDREGENTS_2007_8_9", "TIMSS_2007_4_pg48",
    "CSZ_2008_5_CSZ20111", "ACTAAP_2015_7_2", "AIMS_2009_4_6",
    "Mercury_7058048", "Mercury_7094430", "NAEP_2005_4_S10+1",
    "Mercury_7205958", "Mercury_7216685", "Mercury_7222478",
]


def read_jsonl(path):
    return {r["id"]: r for r in map(json.loads, path.open())}


def count(frame):
    return collections.Counter((r["extra_info"]["kind"], r["source"])
                               for r in frame.to_dict("records"))


def main():
    old = pd.read_parquet(f"{PREFIX}_train.parquet")
    val = pd.read_parquet(f"{PREFIX}_val.parquet")
    pool = read_jsonl(DATA / "pool.jsonl")
    replay = read_jsonl(DATA / "replay_th.jsonl")
    math = [f"math-train/{id_}" for id_ in MATH_IDS]
    arc = [f"arc-train/{id_}" for id_ in ARC_IDS]
    selected = math + arc
    assert len(selected) == len(set(selected)) == 38
    assert not set(selected) & set(val.id)
    assert set(selected) <= set(replay) & set(pool)
    for id_ in selected:
        sample = replay[id_]
        assert sample["question"] == pool[id_]["question"]
        assert sample["response"].count("<think>") == sample["response"].count("</think>") == 1
        assert sample["response"].lstrip().startswith("<think>")
        assert "Final Answer:" in sample["response"].split("</think>", 1)[1]
        assert not any(tag in sample["response"] for tag in ("<Parallel>", "<Path>", "<Goal>"))

    # For each MATH no-block problem, remove two positive problems of the same
    # answer type. Three positive copies become six no-block copies.
    desired = collections.Counter(pool[id_]["answer_type"] for id_ in math)
    desired = {kind: n * 2 for kind, n in desired.items()}
    candidates = sorted({r.id for r in old.itertuples()
                         if r.source == "math" and r.extra_info["kind"] == "parallel_th"})
    assert not set(candidates) & set(selected)
    by_type = {kind: [id_ for id_ in candidates if pool[id_]["answer_type"] == kind]
               for kind in desired}
    rng = random.Random(21064)
    remove = []
    for kind, n in sorted(desired.items()):
        rng.shuffle(by_type[kind])
        assert len(by_type[kind]) >= n
        remove += by_type[kind][:n]
    remove = set(remove)
    assert len(remove) == 24

    kept = []
    replaced_arc = collections.Counter()
    removed_math = collections.Counter()
    for old_row in old.to_dict("records"):
        id_ = old_row["id"]
        if id_ in remove and old_row["extra_info"]["kind"] == "parallel_th":
            removed_math[id_] += 1
            continue
        if id_ in arc and old_row["extra_info"]["kind"] == "replay_th":
            replacement = row("control_th", replay[id_])
            assert old_row["extra_info"]["answer"] == replacement["extra_info"]["answer"]
            kept.append(replacement)
            replaced_arc[id_] += 1
        else:
            kept.append({k: v for k, v in old_row.items() if k != "index"})
    assert set(removed_math) == remove and set(removed_math.values()) == {3}
    assert set(replaced_arc) == set(arc) and set(replaced_arc.values()) == {3}
    for id_ in math:
        kept.extend(row("control_th", replay[id_]) for _ in range(6))

    rng.shuffle(kept)
    new = pd.DataFrame(kept)
    new["index"] = range(len(new))
    assert len(new) == len(old) == 2748 and len(val) == 63
    assert not set(new.id) & set(val.id)
    assert collections.Counter(new.source) == collections.Counter(old.source)
    assert all(r["extra_info"]["enable_thinking"] for r in kept
               if r["extra_info"]["kind"] == "control_th")
    assert all(r["extra_info"]["question"] == row("control_th", replay[r["id"]])["extra_info"]["question"]
               for r in kept if r["extra_info"]["kind"] == "control_th")
    for id_ in math:
        assert sum(r["id"] == id_ and r["extra_info"]["kind"] == "control_th" for r in kept) == 6

    new.to_parquet(f"{OUTPUT}_train.parquet")
    val.to_parquet(f"{OUTPUT}_val.parquet")
    report = {
        "base": PREFIX.name, "train_rows": len(new), "val_rows": len(val),
        "removed_positive_ids": sorted(remove), "removed_positive_copies": 72,
        "new_math_no_block_ids": math, "new_math_no_block_copies": 72,
        "converted_arc_replay_ids": arc, "converted_arc_copies": 78,
        "answer_types_removed_positive": dict(desired),
        "answer_types_added_math": {kind: n * 6 for kind, n in collections.Counter(
            pool[id_]["answer_type"] for id_ in math).items()},
        "train_kind_source_before": {f"{a}/{b}": n for (a, b), n in count(old).items()},
        "train_kind_source_after": {f"{a}/{b}": n for (a, b), n in count(new).items()},
        "val_rows_unchanged": True, "seed": 21064,
        "independent_manual_review": "MATH 29 checked, 12 selected; ARC 30 checked, 26 selected",
    }
    (DATA / "sft_selective_blocks_m1_text1_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"train": len(new), "val": len(val), "no_block_ids": 38}))


if __name__ == "__main__":
    main()
