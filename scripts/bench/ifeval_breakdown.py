"""IFEval diagnostics for plain-mode runs: pipeline checks (truncation, special-token leftovers, empty answers) and
instruction-level strict accuracy per instruction group.

Usage (on the pod, PYTHONPATH/NLTK_DATA as in run_bench.sh): python scripts/bench/ifeval_breakdown.py <run>...
"""
import collections
import json
import sys

import numpy as np
import pandas as pd
from lm_eval.tasks.ifeval import utils

test = pd.read_parquet("/work/bench_data/plain/ifeval.parquet")
docs = [json.loads(info["doc"]) for info in test["extra_info"]]
groups = {}
for run in sys.argv[1:]:
    generations = pd.read_json(f"/work/bench/{run}/ifeval.jsonl", lines=True)
    answers = generations["output"].str.replace("<|endoftext|>", "", regex=False).str.replace("<|im_end|>", "", regex=False)
    answers = answers.map(lambda text: text.split("</think>")[-1])
    results = [utils.process_results(doc, [answer]) for doc, answer in zip(docs, answers)]
    print(f"{run}: strict {100 * np.mean([r['prompt_level_strict_acc'] for r in results]):.1f}"
          f" | truncated {100 * generations['truncated'].mean():.1f}% | mean tokens {generations['tokens'].mean():.0f}"
          f" | special-token leftovers {100 * answers.str.contains(r'<[|]im_start[|]>|<[|]endoftext[|]>').mean():.1f}%"
          f" | empty {100 * (answers.str.strip() == '').mean():.1f}%")
    by_group = collections.defaultdict(list)
    for doc, result in zip(docs, results):
        for instruction, ok in zip(doc["instruction_id_list"], result["inst_level_strict_acc"]):
            by_group[instruction.split(":")[0]].append(ok)
    groups[run] = {group: round(100 * np.mean(oks)) for group, oks in by_group.items()}
    groups[run]["n"] = None
counts = collections.Counter(i.split(":")[0] for doc in docs for i in doc["instruction_id_list"])
table = pd.DataFrame(groups).drop(index="n")
table["instructions"] = pd.Series(counts)
print(table.sort_values(table.columns[1]).to_string())
