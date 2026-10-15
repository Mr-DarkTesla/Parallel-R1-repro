"""Exp 23 thinking runs: are the parallel blocks inside the <think> reasoning or in the answer after </think>?
Per run and benchmark (%): answers with a tag <Parallel> inside think / after think, with a complete block
(<Parallel><Path>..</Path><Path>..</Path></Parallel><Summary>..</Summary>, whitespace allowed) inside / after, with ">"-lines (the tag substitute of the
c=1 model) inside / after, think closed; accuracy is in results/<bench>.json.
Usage: python scripts/exp23/think_where.py <run dir>...
"""
import json
import os
import re
import sys

import pandas as pd

BLOCK = re.compile(r"<Parallel>\s*<Path>(?:(?!</?Parallel>).)+?</Path>\s*<Path>(?:(?!</?Parallel>).)+?</Path>\s*</Parallel>\s*<Summary>.+?</Summary>", re.S)

for run in sys.argv[1:]:
    for bench in ("gsm8k_dev", "math_dev"):
        if not os.path.exists(f"{run}/{bench}.jsonl"):
            continue
        text = pd.read_json(f"{run}/{bench}.jsonl", lines=True)["output"]
        closed = text.str.contains("</think>", regex=False)
        think = text.where(closed, text + "</think>").str.split("</think>", n=1).str[0]
        answer = text.str.split("</think>", n=1).str[1].fillna("")
        share = lambda mask: round(100 * mask.mean(), 1)  # noqa: E731
        full = lambda part: part.str.contains(BLOCK)  # noqa: E731
        print(json.dumps({"run": os.path.basename(run), "bench": bench, "rows": len(text), "think_closed": share(closed),
                          "block_in_think": share(think.str.contains("<Parallel>", regex=False)),
                          "block_after_think": share(answer.str.contains("<Parallel>", regex=False)),
                          "full_block_in_think": share(full(think)), "full_block_after_think": share(full(answer)),
                          "full_blocks_in_think_mean": round(think.map(lambda t: len(BLOCK.findall(t))).mean(), 2),
                          "gt_lines_in_think": share(think.str.contains(r"(?m)^>\s*$")),
                          "gt_lines_after_think": share(answer.str.contains(r"(?m)^>\s*$")),
                          "think_mentions_paths": share(think.str.contains("path", case=False))}))
