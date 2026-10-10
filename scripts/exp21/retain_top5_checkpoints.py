#!/usr/bin/env python3
"""Prune one experiment's staged BF16 exports after its pilot is reviewed."""

import argparse
from pathlib import Path
import shutil


STEPS = {8, 16, 24, 32, 40, 48, 56, 64}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="experiment directory on owned checkpoint PVC")
    parser.add_argument("--keep", required=True, help="five comma-separated step numbers")
    parser.add_argument("--apply", action="store_true", help="delete three exports after validation")
    args = parser.parse_args()

    keep = [int(value) for value in args.keep.split(",")]
    if len(keep) != 5 or len(set(keep)) != 5 or not set(keep) <= STEPS:
        parser.error("--keep must contain exactly five distinct steps from 8,16,...,64")
    root = args.root.resolve(strict=True)
    if root.parent != Path("/checkpoints").resolve() or root.name not in {
        "exp21-m1-selective-v4", "exp21-m1-selective-v5"
    }:
        parser.error("refusing to touch directories outside owned selective checkpoint PVC")
    if not (root / "ALL_EIGHT_STAGED").is_file():
        parser.error("all-eight staging marker is missing")
    for step in STEPS:
        model = root / f"step_{step}" / "model"
        if not (model / "config.json").is_file() or not (model / "tokenizer_config.json").is_file():
            parser.error(f"incomplete model at step {step}")
        if not any(model.glob("*.safetensors")) and not any(model.glob("*.bin")):
            parser.error(f"missing weights at step {step}")

    remove = sorted(STEPS - set(keep))
    print("keep:", ", ".join(map(str, sorted(keep))))
    print("remove:", ", ".join(map(str, remove)))
    if not args.apply:
        print("dry run; pass --apply after archiving all eight evaluations")
        return
    for step in remove:
        shutil.rmtree(root / f"step_{step}")
    (root / "TOP5_STEPS.txt").write_text(",".join(map(str, sorted(keep))) + "\n")


if __name__ == "__main__":
    main()
