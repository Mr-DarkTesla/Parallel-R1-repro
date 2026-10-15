"""Read-only benchmark extraction for the fresh SFT -> new-reward RL150 run."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path("${PROJECT_ROOT}")
TRAIN = ROOT / "work/experiments/rl-r4-dapo2k-sft-16gpu-20261013"
EVAL = ROOT / "work/experiments/rl-r4-posteval-20261013/sft"
DATASETS = {"MATH500": 500, "AIME2024": 30, "AIME2025": 30, "AIME2026": 30}
config_path = TRAIN / "production-config.json"
config = json.loads(config_path.read_text())
assert config["initial_step"] == 0 and config["initial_checkpoint"] is None
assert config["model"] == str(ROOT / "work/experiments/instruct-full-20261011/runs/epoch1/final")
assert config["experiment"]["reward"] == "C*(1-.9*(1-exp(-ln(9)*F/10000)))"
assert config["reward_mode"] == "forward_only"
report = dict(extracted_at=datetime.now(timezone.utc).isoformat(),
              training_root=str(TRAIN.relative_to(ROOT)),
              initial_model=config["model"], reward=config["experiment"]["reward"],
              config_sha256=hashlib.sha256(config_path.read_bytes()).hexdigest(),
              models={}, sources={}, protocols={})
for step in [50, 100, 150]:
    label = f"NewRL{step}"
    root = EVAL / f"checkpoint-{step:04d}"
    job_path = root / "job.json"
    job = json.loads(job_path.read_text())
    complete_path = TRAIN / f"production/checkpoint-{step:04d}/complete.json"
    complete = json.loads(complete_path.read_text())
    result = json.loads((root / "result.json").read_text())
    assert job["checkpoint"] == complete["step"] == step
    assert job["model"] == str(complete_path.parent / "hf")
    assert job["model_sha256"] == complete["files"]["hf/model.safetensors"]["sha256"]
    assert result["passed"] and result["completed"] == 590
    print(f"Extracting {label}: completed 590/590", file=sys.stderr, flush=True)
    report["protocols"][label] = {
        **{k: job[k] for k in ["response_budget", "path_budget", "max_context", "precision"]},
        "model_sha256": job["model_sha256"],
        "job_sha256": hashlib.sha256(job_path.read_bytes()).hexdigest(),
        "checkpoint_complete_sha256": hashlib.sha256(complete_path.read_bytes()).hexdigest(),
    }
    report["models"][label] = {}
    files = []
    for dataset, total in DATASETS.items():
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
                    assert row["dataset"] == dataset and not row["technical_unknown"]
                    assert row["model_identity"]["sha256"] == job["model_sha256"]
                    assert len(widths) == stats["forks"]
                    assert all(isinstance(w, int) and 1 <= w <= 8 for w in widths)
                    assert row["instrumented_forward_calls"] == stats["actual_model_forward_calls"]
                    records.append(dict(id=row["id"], correct=int(row["grade"]["correct"]),
                                        F=row["instrumented_forward_calls"], tokens=stats["sampled_tokens"],
                                        precision=row["precision"], forks=stats["forks"], widths=widths,
                                        format_valid=row["format_valid"], truncated=stats["truncated"],
                                        model_sha256=row["model_identity"]["sha256"]))
            files.append(dict(path=str(path.relative_to(ROOT)), sha256=digest.hexdigest(),
                              rows=physical_rows))
        assert len(records) == len({r["id"] for r in records}) == total
        report["models"][label][dataset] = records
    report["sources"][label] = files
print(json.dumps(report, separators=(",", ":")))
