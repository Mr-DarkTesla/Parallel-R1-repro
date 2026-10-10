"""Paired bootstrap for one model on two prompts with identical questions."""

import json
import sys
from pathlib import Path

from compare_masked_pilot_archives import compare, load

base, candidate = map(load, sys.argv[1:3])
assert base.keys() == candidate.keys()
for key in base:
    assert base[key]["input"].split("Problem:", 1)[1] == candidate[key]["input"].split("Problem:", 1)[1]
    assert base[key]["decoder"] == candidate[key]["decoder"] == "masked"
out = {"base_archive": Path(sys.argv[1]).name,
       "candidate_archive": Path(sys.argv[2]).name,
       "prompt_changed": True}
for source in ("all", *sorted({key[0] for key in base})):
    keys = [key for key in sorted(base) if source == "all" or key[0] == source]
    out[source] = {metric: compare(base, candidate, keys, metric)
                   for metric in ("acc_robust", "think_numbered_block", "truncated",
                                  "tokens", "forward_passes")}
Path(sys.argv[3]).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out["all"], ensure_ascii=False, indent=2))
