"""Paired dev and IFEval intervals for the 19-example Sol reserve variant."""
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
TOOL = Path(__file__).resolve().parents[1] / "instruct4b_eval/paired_compare.py"
SUFFIXES = ("dev-mvth", "dev-th", "dev-nt", "ifeval-th", "ifeval-nt")


def main():
    runs, out = ROOT / "eval_runs", ROOT / "sol_compare"
    out.mkdir(exist_ok=True)
    for suffix in SUFFIXES:
        for base, cand in (("c0", "reserve-r3"), ("reserve-r3-control", "reserve-r3"),
                           ("deep75-bal", "reserve-r3"), ("c0", "reserve-r3-control")):
            a, b = runs / f"{base}-{suffix}", runs / f"{cand}-{suffix}"
            assert (a / "meta.json").exists() and (b / "meta.json").exists(), (a, b)
            name = f"{cand}_vs_{base}_{suffix}"
            cmd = [sys.executable, str(TOOL), "--base", str(a), "--cand", str(b),
                   "--out", str(out / f"{name}.json")]
            result = subprocess.run(cmd, capture_output=True, text=True)
            (out / f"{name}.txt").write_text(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(f"{name}: {(result.stderr or result.stdout)[-1000:]}")
            print(name, flush=True)


if __name__ == "__main__":
    main()
