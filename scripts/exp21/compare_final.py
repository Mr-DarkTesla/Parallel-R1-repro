"""Paired confidence intervals for the final exp21 dev, IFEval and matched-prompt comparisons.

Usage: python scripts/exp21/compare_final.py EVAL_EFF_DIR OUT_DIR
All referenced runs must have finished. Frozen runs are deliberately excluded.
"""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tool = Path(__file__).resolve().parents[1] / "instruct4b_eval/paired_compare.py"
    comparisons = []
    for suffix in ("dev-nt", "dev-th", "ifeval-nt", "ifeval-th"):
        for base, candidate in (("c0", "control-m1"), ("control-m1", "m1"),
                                ("c0", "m2a"), ("m1", "m2a"), ("control-m1", "m2a")):
            comparisons.append((base, candidate, suffix))
    for base, candidate in (("control-m1", "m1"), ("p06", "m2a"),
                            ("m1", "m2a"), ("control-m1", "m2a")):
        comparisons.append((base, candidate, "dev-mvb"))
    matched = args.runs / "m1-dev-mvb-match" / "meta.json"
    if matched.exists():
        comparisons.append(("m1", "m2a", "dev-mv-match"))
        for base, candidate in (("control-m1", "m1"), ("control-m1", "m2a"),
                                ("p06", "m1"), ("p06", "m2a"), ("m1", "m2a")):
            comparisons.append((base, candidate, "dev-mvb-match"))
    for base, candidate, suffix in comparisons:
        base_run = args.runs / f"{base}-{suffix}"
        candidate_run = args.runs / f"{candidate}-{suffix}"
        assert (base_run / "meta.json").exists() and (candidate_run / "meta.json").exists(), (base_run, candidate_run)
        name = f"{candidate}_vs_{base}_{suffix}"
        result = subprocess.run([sys.executable, str(tool), "--base", str(base_run),
                                 "--cand", str(candidate_run), "--out", str(args.out / f"{name}.json")],
                                capture_output=True, text=True)
        (args.out / f"{name}.txt").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f"{name}: {result.stderr[-1000:]}")
        print(name, flush=True)


if __name__ == "__main__":
    main()
