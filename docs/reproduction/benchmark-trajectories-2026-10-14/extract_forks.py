"""Read-only remote extraction. Run on the shared NFS; compact JSON to stdout."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import os
import json
import sys

ROOT = Path(os.environ["PROJECT_ROOT"])
ROOTS = {
    "SFT": ROOT / "work/experiments/eval-baselines-32k-20261013/full-sft",
    **{f"RL{step}": ROOT / f"work/experiments/eval-intermediates-vllm-rolling-32k-20261013/checkpoint-{step:04d}"
       for step in [50, 100, 150, 200, 250]},
    "RL300": ROOT / "work/experiments/eval-rl300-vllm-rolling-32k-20261013",
}
DATASETS = {"MATH500": 500, "AIME2024": 30, "AIME2025": 30, "AIME2026": 30}
report = dict(extracted_at=datetime.now(timezone.utc).isoformat(), models={}, sources={})
for model, root in ROOTS.items():
    print(f"Extracting {model}", file=sys.stderr, flush=True)
    report["models"][model] = {}
    source_files = []
    for dataset, count in DATASETS.items():
        records = []
        for path in sorted((root / "runs" / dataset).glob("rank-*.jsonl")):
            digest = hashlib.sha256()
            physical_rows = 0
            with path.open("rb") as stream:
                for line in stream:
                    digest.update(line)
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    physical_rows += 1
                    stats = row["stats"]
                    widths = row["widths"]
                    assert len(widths) == stats["forks"]
                    assert all(isinstance(w, int) and 1 <= w <= 8 for w in widths)
                    assert not row["technical_unknown"]
                    assert row["dataset"] == dataset
                    assert stats["actual_model_forward_calls"] == row["instrumented_forward_calls"]
                    records.append(dict(
                        id=row["id"], correct=int(row["grade"]["correct"]),
                        F=row["instrumented_forward_calls"], tokens=stats["sampled_tokens"],
                        precision=row["precision"], forks=stats["forks"], widths=widths,
                        format_valid=row["format_valid"], truncated=stats["truncated"],
                        critical_depth=stats["critical_depth"],
                        model_sha256=row["model_identity"]["sha256"],
                    ))
            source_files.append(dict(path=str(path.relative_to(ROOT)),
                                     sha256=digest.hexdigest(), rows=physical_rows))
        assert len(records) == count and len({r["id"] for r in records}) == count, (model, dataset, len(records))
        report["models"][model][dataset] = records
    report["sources"][model] = source_files
print(json.dumps(report, separators=(",", ":")))
