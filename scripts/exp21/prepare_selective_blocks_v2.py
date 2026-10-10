"""Build the second selective-block SFT dataset from selective-blocks v1.

Atomic, independently reviewed Qwen traces teach the Multiverse prompt to omit
parallel markup.  Replacement is by complete three-copy positive groups, with
source and answer-type counts held fixed.
"""
import collections
import json
import random
from pathlib import Path

import pandas as pd

from build_sft import row


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
BASE = DATA / "sft_selective_blocks_m1_text1"
OUTPUT = DATA / "sft_selective_blocks_v2"

MATH_V1_IDS = [
    "5901", "6060", "5361", "7243", "6356", "1214", "3269", "6198",
    "1000", "2808", "6038", "370",
]
MATH_NEW_IDS = ["2023", "6378"]
GSM_IDS = ["2098", "2221", "2334", "2587", "2793", "3663", "4765",
           "4952", "6932", "7415"]
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


def load_jsonl(path):
    return {record["id"]: record for record in map(json.loads, path.open())}


def kind(record):
    return record["extra_info"]["kind"]


def answer_types(frame, pool):
    return collections.Counter(pool[id_]["answer_type"] for id_ in frame.id)


def select_groups(frame, pool, source, groups_needed, forced=(), excluded=(), seed=0):
    """Select exact three-copy positive IDs, stratified by answer type."""
    positives = frame[(frame.source == source) & frame.extra_info.map(lambda x: x["kind"] == "parallel_th")]
    counts = collections.Counter(positives.id)
    assert set(counts.values()) == {3}, (source, counts)
    forced, excluded = set(forced), set(excluded)
    assert forced <= set(counts)
    selected = set(forced)
    rng = random.Random(seed)
    for answer_type, need in sorted(groups_needed.items()):
        already = sum(pool[id_]["answer_type"] == answer_type for id_ in selected)
        candidates = sorted(id_ for id_ in counts
                            if pool[id_]["answer_type"] == answer_type
                            and id_ not in selected and id_ not in excluded)
        rng.shuffle(candidates)
        assert len(candidates) >= need - already, (source, answer_type, len(candidates), need - already)
        selected.update(candidates[:need - already])
    assert collections.Counter(pool[id_]["answer_type"] for id_ in selected) == groups_needed
    return selected


def main():
    old = pd.read_parquet(f"{BASE}_train.parquet")
    val = pd.read_parquet(f"{BASE}_val.parquet")
    pool = load_jsonl(DATA / "pool.jsonl")
    replay = load_jsonl(DATA / "replay_th.jsonl")
    math_v1 = [f"math-train/{id_}" for id_ in MATH_V1_IDS]
    math_new = [f"math-train/{id_}" for id_ in MATH_NEW_IDS]
    math = math_v1 + math_new
    gsm = [f"gsm8k-train/{id_}" for id_ in GSM_IDS]
    arc = [f"arc-train/{id_}" for id_ in ARC_IDS]
    selected = math + gsm + arc
    assert len(selected) == len(set(selected)) == 50
    assert not set(selected) & set(val.id)
    assert set(selected) <= set(pool) & set(replay)
    for id_ in selected:
        assert replay[id_]["question"] == pool[id_]["question"]
        assert replay[id_]["response"].startswith("<think>")
        assert replay[id_]["response"].count("<think>") == replay[id_]["response"].count("</think>") == 1
        assert not any(tag in replay[id_]["response"] for tag in ("<Parallel>", "<Goal>", "<Path>"))

    # Delta from v1 controls: 12 extra copies for each old MATH ID, 18 for
    # each newly selected MATH and GSM8K ID.  The existing 2023 positive group
    # is deliberately one of the expression replacements.
    math_delta = collections.Counter()
    for id_ in math_v1:
        math_delta[pool[id_]["answer_type"]] += 12
    for id_ in math_new:
        math_delta[pool[id_]["answer_type"]] += 18
    gsm_delta = collections.Counter(pool[id_]["answer_type"] for id_ in gsm)
    gsm_delta = collections.Counter({key: value * 18 for key, value in gsm_delta.items()})
    assert math_delta == {"integer": 108, "fraction": 30, "expression": 42}
    assert gsm_delta == {"integer": 180}
    math_groups = collections.Counter({key: value // 3 for key, value in math_delta.items()})
    gsm_groups = collections.Counter({key: value // 3 for key, value in gsm_delta.items()})
    math_remove = select_groups(old, pool, "math", math_groups, forced={"math-train/2023"},
                                excluded=set(math) - {"math-train/2023"}, seed=21065)
    gsm_remove = select_groups(old, pool, "gsm8k", gsm_groups, excluded=set(gsm), seed=21066)
    remove = math_remove | gsm_remove
    assert len(math_remove) == 60 and len(gsm_remove) == 60 and len(remove) == 120

    kept = []
    removed = collections.Counter()
    for old_row in old.to_dict("records"):
        if old_row["id"] in remove and kind(old_row) == "parallel_th":
            removed[old_row["id"]] += 1
        else:
            kept.append({key: value for key, value in old_row.items() if key != "index"})
    assert set(removed) == remove and set(removed.values()) == {3}

    added = collections.Counter()
    for id_ in math + gsm:
        present = sum(record["id"] == id_ and kind(record) == "control_th" for record in kept)
        assert present in (0, 6), (id_, present)
        for _ in range(18 - present):
            control = row("control_th", replay[id_])
            assert control["extra_info"]["answer"] == replay[id_]["response"]
            kept.append(control)
            added[id_] += 1
    assert set(added) == set(math + gsm)
    assert all(added[id_] == 12 for id_ in math_v1)
    assert all(added[id_] == 18 for id_ in math_new + gsm)

    rng = random.Random(21067)
    rng.shuffle(kept)
    new = pd.DataFrame(kept)
    new["index"] = range(len(new))
    assert len(new) == len(old) == 2748 and len(val) == 63
    assert not set(new.id) & set(val.id)
    assert collections.Counter(new.source) == collections.Counter(old.source)
    assert answer_types(new, pool) == answer_types(old, pool)
    controls = new[new.extra_info.map(lambda x: x["kind"] == "control_th")]
    positives = new[new.extra_info.map(lambda x: x["kind"] == "parallel_th")]
    assert len(controls) == 510 and len(positives) == 555
    assert collections.Counter(controls.source) == {"math": 252, "gsm8k": 180, "arc": 78}
    assert collections.Counter(positives.source) == {"math": 372, "gsm8k": 183}
    assert all(record["extra_info"]["enable_thinking"] for record in kept
               if kind(record) == "control_th")

    new.to_parquet(f"{OUTPUT}_train.parquet")
    val.to_parquet(f"{OUTPUT}_val.parquet")
    report = {
        "base": BASE.name,
        "train_rows": len(new), "val_rows": len(val), "val_rows_unchanged": True,
        "seed": {"math_groups": 21065, "gsm_groups": 21066, "shuffle": 21067},
        "target_copies_per_id": {"math": 18, "gsm8k": 18, "arc": 3},
        "math_v1_reviewed_ids": math_v1,
        "math_new_audit_ids": math_new,
        "gsm_new_screened_ids": gsm,
        "arc_v1_reviewed_ids": arc,
        "excluded_gsm_caveat": "gsm8k-train/4824 was marked good in trace quality but is intentionally excluded.",
        "removed_positive_ids": {"math": sorted(math_remove), "gsm8k": sorted(gsm_remove)},
        "removed_positive_copies": {"math": 180, "gsm8k": 180, "total": 360},
        "added_control_copies": {"math": 180, "gsm8k": 180, "total": 360},
        "answer_type_replacement_copies": {"math": dict(math_delta), "gsm8k": dict(gsm_delta)},
        "train_source_before": dict(collections.Counter(old.source)),
        "train_source_after": dict(collections.Counter(new.source)),
        "train_answer_type_before": dict(answer_types(old, pool)),
        "train_answer_type_after": dict(answer_types(new, pool)),
        "train_kind_source_before": {f"{kind_}/{source}": count for (kind_, source), count in collections.Counter(
            (kind(record), record["source"]) for record in old.to_dict("records")).items()},
        "train_kind_source_after": {f"{kind_}/{source}": count for (kind_, source), count in collections.Counter(
            (kind(record), record["source"]) for record in kept).items()},
        "no_block_multiverse_rows": len(controls),
        "positive_parallel_rows": len(positives),
        "manual_review_evidence": {
            "previous_independent_review": "v1 MATH 12 and ARC 26 retained unchanged",
            "new_audit_selected": "MATH 2023, 6378 and GSM8K 10 selected from qwen trace audits/screens",
            "trace_quality": "audit/think_trace_sol/qwen_trace_quality.jsonl",
            "screening": ["audit/qwen_trace_screen/screen_a.jsonl", "audit/qwen_trace_screen/screen_b.jsonl", "audit/qwen_trace_screen/screen_c.jsonl"],
        },
        "leakcheck": "Every selected question exactly matches data/pool.jsonl, the prior leakchecked cleaned pool; see DATASET_POOL.md.",
    }
    (DATA / "sft_selective_blocks_v2_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"train": len(new), "val": len(val), "controls": len(controls), "positives": len(positives)}))


if __name__ == "__main__":
    main()
