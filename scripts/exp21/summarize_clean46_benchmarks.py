"""Collect clean46, baseline, and plain-control benchmark metrics."""

import csv
import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/21-qwen3-0.6b-multiverse"
FROZEN = BASE / "eval_archives/qwen4b_clean46_frozen"
OUT = BASE / "qwen4b_clean46_final_benchmarks.csv"


def summarize(model, suite, mode, results, rows):
    groups = {}
    for line in rows.splitlines():
        row = json.loads(line)
        groups.setdefault(row["source"], []).append(row)
    assert set(groups) == set(results), (suite, mode, set(groups), set(results))
    output = []
    for name, result in results.items():
        group = groups[name]
        n = len(group)
        assert n >= result["problems"] and n % result["problems"] == 0
        for key, field in (("mean_tokens", "tokens"), ("mean_forward_passes", "forward_passes")):
            assert abs(sum(r[field] for r in group) / n - result[key]) < 0.11, (suite, mode, name, key)
        valid = sum(bool(r["mv_numbered"]) for r in group)
        output.append({
            "model": model, "suite": suite, "mode": mode, "benchmark": name,
            "problems": result["problems"], "responses": n,
            "strict_percent": result["accuracy"],
            "value_percent": result.get("accuracy_robust", ""),
            "mean_tokens": result["mean_tokens"],
            "mean_forward_passes": result["mean_forward_passes"],
            "complete_numbered_blocks": valid,
            "complete_numbered_blocks_percent": round(100 * valid / n, 2),
            "truncated_percent": result["truncated"],
        })
    return output


def archived(model, suite, mode):
    prefix = f"qwen4b-{model}-dev" if suite == "dev" else f"qwen4b-{model}-frozen"
    name = f"{prefix}-{mode}"
    path = BASE / "full_dev" / f"{name}.tgz"
    with tarfile.open(path, "r:gz") as archive:
        benches = ("gsm8k_dev", "math_dev", "arc_dev", "mmlu_pro_dev") if suite == "dev" else ("ifeval",)
        for bench in benches:
            result = json.load(archive.extractfile(f"{name}/results/{bench}.json"))
            rows = archive.extractfile(f"{name}/rows/{bench}.jsonl").read().decode()
            yield from summarize(model, suite, mode, result, rows)


def frozen(mode):
    for bench in ("apo", "arc", "mmlu_pro", "limo"):
        path = FROZEN / mode / bench
        meta = json.loads((path / "meta.json").read_text())
        assert meta["model"].endswith("/qwen4b-clean46-tagged-step32/model")
        assert meta["suite"] == "frozen" and meta["mode"] == mode
        assert meta["budget"] == 16384 and meta["temperature"] == meta["top_p"] == 1.0
        assert meta["generator"] == "scripts/bench/generate_plain.py"
        assert meta["prompts"] == "/work/bench_data/plain"
        assert meta["commit"] == "14880be3942e861357c55f761354b8f84b4c5520"
        result_path = path / "results" / f"{bench}.json"
        rows_path = path / "rows" / f"{bench}.jsonl"
        if not result_path.exists():
            result_path = path / "results.json"
            rows_path = path / "rows.jsonl"
        yield from summarize("selected", "frozen", mode, json.loads(result_path.read_text()), rows_path.read_text())


def main():
    records = []
    for model in ("base", "plain", "selected"):
        for mode in ("no-thinking", "thinking"):
            records.extend(archived(model, "dev", mode))
            records.extend(archived(model, "ifeval", mode))
    for mode in ("no-thinking", "thinking"):
        records.extend(frozen(mode))
    assert len(records) == 44, len(records)
    with OUT.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    print(OUT)
    for row in records:
        print("\t".join(str(row[k]) for k in ("model", "suite", "mode", "benchmark", "strict_percent", "value_percent", "mean_tokens", "mean_forward_passes", "complete_numbered_blocks_percent", "truncated_percent")))


if __name__ == "__main__":
    main()
