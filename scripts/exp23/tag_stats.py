"""Exp 23: does the model write the tags as the special tokens or as text pieces ("<", "Parallel", ">")?

Plain generation dumps (scripts/instruct4b_eval/generate.py, with token_ids): tag ids in the prompt vLLM received; per tag, occurrences in the decoded text vs occurrences
of its id; text minus ids = tags written as pieces. Rollout dumps (text only): a block opened by the <Parallel> id is assembled by the
rollout as "<Parallel><Path>" (forced <Path> right after the id) and logged as "Conducting parallel thinking..." (RAY_DEDUP_LOGS=0);
a <Parallel> without that log line was typed as pieces and never branched.
Usage: python scripts/exp23/tag_stats.py <run dir>...   (run dirs of scripts/instruct4b_eval/run_eval.sh)
"""
import json
import os
import re
import sys

import pandas as pd

TAGS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]
IDS = dict(zip(TAGS, range(151669, 151675)))

for run in sys.argv[1:]:
    for bench in ("gsm8k_dev", "math_dev"):
        plain, rollout = f"{run}/{bench}.jsonl", f"{run}/{bench}/generations/0.jsonl"
        if not os.path.exists(plain) and not os.path.exists(rollout):
            continue
        dump = pd.read_json(plain if os.path.exists(plain) else rollout, lines=True)
        text = dump["output"]
        stats = {"rows": len(dump), "rows_with_<Parallel>_text_%": round(100 * text.str.contains("<Parallel>", regex=False).mean(), 1)}
        if "token_ids" in dump:
            for tag, i in IDS.items():
                n_text, n_ids = int(text.str.count(re.escape(tag)).sum()), int(dump["token_ids"].map(lambda ids: ids.count(i)).sum())
                stats[tag] = {"text": n_text, "id": n_ids, "pieces": n_text - n_ids}
            has_id = dump["token_ids"].map(lambda ids: IDS["<Parallel>"] in ids)
            stats["rows_with_<Parallel>_id_%"] = round(100 * has_id.mean(), 1)
            stats["prompt_tag_ids_min_max"] = [int(dump["prompt_tag_ids"].min()), int(dump["prompt_tag_ids"].max())]  # 16 in the exp-23 prompt
        else:
            log = open(f"{run}/{bench}.log").read()
            stats["blocks_<Parallel>_text"] = int(text.str.count("<Parallel>").sum())
            stats["blocks_branched_by_rollout"] = log.count("Conducting parallel thinking...")
            stats["blocks_assembled_<Parallel><Path>"] = int(text.str.count("<Parallel><Path>").sum())
            stats["rows_with_assembled_block_%"] = round(100 * text.str.contains("<Parallel><Path>", regex=False).mean(), 1)
        print(json.dumps({"run": os.path.basename(run), "bench": bench, **stats}))
