"""Markdown comparison of experiments on every benchmark, from results/<name>/eval_apo.txt, eval_limo.txt, free_generation_tags.jsonl.

Usage: python scripts/compare_runs.py <results_dir>...
"""
import json
import os
import sys

COLUMNS = {"mean_acc": "mean", "pass_at_n": "pass", "parallel_ratio": "with <Parallel>", "valid_responses": "valid responses",
           "correct_tag_share": "correct tags", "no_final_answer": "no final answer"}


def read_table(path):
    """Per-source rows of the text table printed by scripts/summarize_eval.py."""
    lines = [line.split() for line in open(path) if line.strip() and not line.startswith("{")]
    header = lines[0]
    return {row[0]: dict(zip(header, map(float, row[1:]))) for row in lines[2:]}


runs = {os.path.basename(path.rstrip("/")): path for path in sys.argv[1:]}
tables = {name: {**read_table(f"{path}/eval_apo.txt"), **read_table(f"{path}/eval_limo.txt")} for name, path in runs.items()}
for source in ["APO_AIME24", "APO_AIME25", "APO_AMC23", "APO_MATH300", "APO_LIMO"]:
    n = int(next(iter(tables.values()))[source]["n"])
    print(f"\n### {source.removeprefix('APO_')} (x{n})\n")
    print("| run | " + " | ".join(f"{label}@{n}" if key in ("mean_acc", "pass_at_n") else label for key, label in COLUMNS.items()) + " |")
    print("|---" * (len(COLUMNS) + 1) + "|")
    for name, table in tables.items():
        row = table[source]
        print(f"| {name} | " + " | ".join(f"{row[key]:.1f}" if key in row else "—" for key in COLUMNS) + " |")

print("\n### Free generation, final checkpoint: valid responses / correct tags\n")
print("| run | GSM8K T=0 | GSM8K T=1 | MATH300 T=0 | MATH300 T=1 |")
print("|---|---|---|---|---|")
for name, path in runs.items():
    rows = [json.loads(line) for line in open(f"{path}/free_generation_tags.jsonl")]
    last = max(rows, key=lambda row: int(row["model"].rsplit("_", 1)[-1]))["model"]
    cells = {(row["set"], row["temperature"]): f"{100 * row['all_tags_correct']:.0f}% / {100 * row['correct_tag_share']:.0f}%" for row in rows if row["model"] == last}
    print(f"| {name} | " + " | ".join(cells[(s, t)] for s in ("gsm8k", "math300") for t in (0.0, 1.0)) + " |")
