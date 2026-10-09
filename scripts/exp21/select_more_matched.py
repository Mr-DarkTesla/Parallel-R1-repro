"""Select equal 180-row M1/M2 additions after full automatic and human review.

Usage: python select_more_matched.py RESULTS_DIR
The two sets have identical source/answer-type quotas and disjoint task IDs.
"""
import collections
import json
import random
import sys
from pathlib import Path


QUOTAS = {("gsm8k", "integer"): 85, ("math", "integer"): 62,
          ("math", "expression"): 25, ("math", "fraction"): 8}


def read(path):
    return [json.loads(line) for line in path.open()]


def write(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n"
                            for row in sorted(rows, key=lambda x: x["id"])))


def select(groups, quotas, rng):
    chosen, reserve = [], []
    for group, size in quotas.items():
        rows = sorted(groups[group], key=lambda r: r["id"])
        rng.shuffle(rows)
        assert len(rows) >= size, (group, len(rows), size)
        chosen.extend(rows[:size])
        reserve.extend(rows[size:])
    return chosen, reserve


def main(root):
    data, audit = root / "data", root / "audit"
    m1_candidates = read(data / "more_m1_candidates.jsonl")
    m1_verdicts = {r["id"]: r for r in read(audit / "more_m1_reasoning_judge.jsonl")}
    assert len(m1_candidates) == len(m1_verdicts)
    m1 = []
    for row in m1_candidates:
        verdict = m1_verdicts[row["id"]]
        assert all(verdict[k] == row[k] for k in ("question", "answer", "response")), row["id"]
        if verdict["status"] == "clean":
            m1.append(row)

    existing = read(data / "more_m2_existing_reviewed27.jsonl")
    new = read(data / "more_m2_new_2000_candidates.jsonl")
    new_verdicts = {r["id"]: r for r in read(audit / "more_m2_new_2000_reasoning_judge.jsonl")}
    excluded = json.loads((audit / "more_m2_new_human_exclusions.json").read_text())
    assert len(new) == len(new_verdicts)
    assert all(new_verdicts[k]["status"] == "clean" for k in excluded)
    m2 = existing[:]
    for row in new:
        verdict = new_verdicts[row["id"]]
        assert all(verdict[k] == row[k] for k in ("question", "answer", "response")), row["id"]
        if verdict["status"] == "clean" and row["id"] not in excluded:
            m2.append(row)

    assert len(m1) == len({r["id"] for r in m1}) == 309
    assert len(m2) == len({r["id"] for r in m2}) == 201
    m2_groups = collections.defaultdict(list)
    for row in m2:
        m2_groups[(row["source"], row["answer_type"])].append(row)
    selected_m2, reserve_m2 = select(m2_groups, QUOTAS, random.Random(21062))
    # Freeze M1 before later manual M2 substitutions; preserve its 20+30 review samples.
    selected_m2_ids = {r["id"] for r in selected_m2}
    m1_groups = collections.defaultdict(list)
    for row in m1:
        if row["id"] not in selected_m2_ids:
            m1_groups[(row["source"], row["answer_type"])].append(row)
    selected_m1, reserve_m1 = select(m1_groups, QUOTAS, random.Random(21061))
    m1_excluded = json.loads((audit / "more_m1_matched_human_exclusions.json").read_text())
    m1_replacements = {}
    for problem_id in m1_excluded:
        match = next((r for r in selected_m1 if r["id"] == problem_id), None)
        assert match is not None, problem_id
        group = (match["source"], match["answer_type"])
        replacement = next((r for r in reserve_m1 if (r["source"], r["answer_type"]) == group), None)
        assert replacement is not None, group
        selected_m1.remove(match)
        selected_m1.append(replacement)
        reserve_m1.remove(replacement)
        m1_replacements[problem_id] = replacement["id"]
    m2_self_excluded = json.loads((audit / "more_m2_matched_self_exclusions.json").read_text())
    m2_replacements = {}
    selected_m1_ids = {r["id"] for r in selected_m1}
    for problem_id in m2_self_excluded:
        match = next((r for r in selected_m2 if r["id"] == problem_id), None)
        assert match is not None, problem_id
        group = (match["source"], match["answer_type"])
        replacement = next((r for r in reserve_m2 if (r["source"], r["answer_type"]) == group
                            and r["id"] not in selected_m1_ids), None)
        assert replacement is not None, group
        selected_m2.remove(match)
        selected_m2.append(replacement)
        reserve_m2.remove(replacement)
        m2_replacements[problem_id] = replacement["id"]
    selected_m2_ids = {r["id"] for r in selected_m2}
    assert len(selected_m1) == len(selected_m2) == 180
    assert not {r["id"] for r in selected_m1} & selected_m2_ids
    for name, selected, reserve in (("m1", selected_m1, reserve_m1), ("m2", selected_m2, reserve_m2)):
        write(data / f"more_{name}_matched180.jsonl", selected)
        write(data / f"more_{name}_matched180_reserve.jsonl", reserve)
    stats = {"quotas": {"/".join(k): n for k, n in QUOTAS.items()},
             "m1_clean": len(m1), "m2_existing_reviewed": len(existing),
             "m2_new_auto_clean": sum(v["status"] == "clean" for v in new_verdicts.values()),
             "m2_new_human_excluded": len(excluded), "m2_reviewed_available": len(m2),
             "selected_each": 180, "m1_reserve": len(reserve_m1), "m2_reserve": len(reserve_m2),
             "m1_m2_selected_id_overlap": 0,
             "m1_human_excluded": sorted(m1_excluded), "m1_replacements": m1_replacements,
             "m2_self_excluded": sorted(m2_self_excluded), "m2_replacements": m2_replacements}
    (audit / "more_matched180_selection.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
