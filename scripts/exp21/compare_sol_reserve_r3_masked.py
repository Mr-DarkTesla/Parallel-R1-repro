"""Compare the fixed R3 masked pilot with its sequential run and prior masked SFT."""
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
TOOL = Path(__file__).with_name("compare_thinking_blocks.py")


def read(path):
    return [json.loads(line) for line in path.open()]


def save(path, rows):
    with path.open("w") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    out = ROOT / "sol_compare"
    for short, source in (("gsm", "gsm8k_dev"), ("math", "math_dev")):
        pilot = ROOT / "masked_pilot/sol_r3"
        balanced = ROOT / "masked_pilot/balanced/masked_pilot"
        masked = read(pilot / f"r3-{short}10-block-rows.jsonl") + read(pilot / f"r3-{short}next10-block-rows.jsonl")
        prior = read(balanced / f"bal-{short}10-block-rows.jsonl") + read(balanced / f"bal-{short}next10-block-rows.jsonl")
        seq_all = read(out / f"reserve-r3_dev-mvth_{source}_thinking_blocks_rows.jsonl")
        seq_by_id = {r["problem_id"]: r for r in seq_all if r["sample"] == 0}
        assert len(masked) == len(prior) == 20
        seq = [seq_by_id[r["problem_id"]] for r in masked]
        for b, c, d in zip(seq, masked, prior):
            for key in ("problem_id", "problem", "input", "sample"):
                assert b[key] == c[key] == d[key], key
        paths = {}
        for name, rows in (("seq", seq), ("masked", masked), ("balanced", prior)):
            paths[name] = out / f"reserve-r3_{short}20_{name}_block_rows.jsonl"
            save(paths[name], rows)
        for base in ("seq", "balanced"):
            result = out / f"reserve-r3_masked_vs_{base}_{short}20.json"
            subprocess.run([sys.executable, str(TOOL), str(paths[base]),
                            str(paths["masked"]), str(result)], check=True)


if __name__ == "__main__":
    main()
