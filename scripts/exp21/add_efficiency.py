"""Add token and sequential-forward counts to completed eval rows without changing their scores.

Use when a run was scored before score.py recorded these fields. The output is a separate derived run with the original
accuracy, truncation and protocol metadata. Row/dump alignment is checked; no scoring is repeated.
Usage: python add_efficiency.py <source_run_dir> <output_run_dir> <tokenizer_dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from mv_format import forward_passes, parse


source, target, tokenizer = map(Path, sys.argv[1:4])
target.mkdir(parents=True, exist_ok=True)
(target / "rows").mkdir(exist_ok=True)
(target / "results").mkdir(exist_ok=True)
tok = AutoTokenizer.from_pretrained(tokenizer)
count = lambda text: len(tok.encode(text, add_special_tokens=False))  # noqa: E731
meta = json.loads((source / "meta.json").read_text())
meta["analysis_efficiency_source"] = str(source)
meta["analysis_efficiency_method"] = "generated tokens minus all but the longest path in each grammatical block"
(target / "meta.json").write_text(json.dumps(meta, indent=1))
for path in sorted((source / "rows").glob("*.jsonl")):
    bench = path.stem
    rows = pd.read_json(path, lines=True)
    dumps = pd.read_json(source / f"{bench}.jsonl", lines=True)
    if len(rows) != len(dumps) or not rows["input"].equals(dumps["input"]):
        raise ValueError(f"{bench}: scored rows do not align with generation dump")
    if dumps["tokens"].isna().any():
        raise ValueError(f"{bench}: generated token counts missing")
    answers = dumps["output"].str.replace("<|endoftext|>", "", regex=False).str.replace("<|im_end|>", "", regex=False)
    structures = [parse(a) for a in answers]
    rows["mv_started_blocks"] = [max(a.count("<Parallel>"), a.count("</Parallel>")) for a in answers]
    rows["mv_valid_blocks"] = [sum(b["numbered"] for b in s["blocks"]) for s in structures]
    saved = [count(a) - forward_passes(a, count) for a in answers]
    rows["tokens"] = dumps["tokens"].astype(int).to_numpy()
    rows["forward_passes"] = rows["tokens"] - saved
    if (rows["forward_passes"] < 0).any() or (rows["forward_passes"] > rows["tokens"]).any():
        raise ValueError(f"{bench}: invalid forward-pass count")
    rows.to_json(target / "rows" / path.name, orient="records", lines=True)
    summary = json.loads((source / "results" / f"{bench}.json").read_text())
    for name, group in rows.groupby("source"):
        summary[name]["mean_tokens"] = round(float(group["tokens"].mean()), 1)
        summary[name]["mean_forward_passes"] = round(float(group["forward_passes"].mean()), 1)
        started = group["mv_started_blocks"].sum()
        summary[name]["mv_valid_blocks_percent"] = round(100 * group["mv_valid_blocks"].sum() / started, 1) if started else None
    (target / "results" / f"{bench}.json").write_text(json.dumps(summary, indent=1))
    print(bench, len(rows), round(float(rows["tokens"].mean()), 1), round(float(rows["forward_passes"].mean()), 1))
