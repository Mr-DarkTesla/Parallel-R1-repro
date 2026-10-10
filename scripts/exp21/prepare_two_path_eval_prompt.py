"""Matched dev pilot prompts that ask for exactly two independent Paths."""

import copy
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
SOURCE = ROOT / "masked_pilot/masked_pilot"
TARGET = ROOT / "masked_pilot/two_path_prompt"
ANCHOR = "When the work splits into parts that do not depend on each other (separate cases or separate quantities), solve those parts in a parallel block."
EXTRA = " Use exactly two independent parts: two Outlines and two Paths, numbered 1 and 2."


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    report = {}
    for name in ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10"):
        frame = pd.read_parquet(SOURCE / f"{name}.parquet")
        prompts = []
        for value in frame.prompt:
            messages = copy.deepcopy(list(value))
            assert len(messages) == 1 and messages[0]["role"] == "user"
            content = messages[0]["content"]
            assert content.count(ANCHOR) == 1
            messages[0]["content"] = content.replace(ANCHOR, ANCHOR + EXTRA)
            prompts.append(messages)
        frame["prompt"] = prompts
        frame.to_parquet(TARGET / f"{name}.parquet")
        report[name] = {"rows": len(frame), "ids": [info["id"] for info in frame.extra_info]}
    (TARGET / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({name: value["rows"] for name, value in report.items()}))


if __name__ == "__main__":
    main()
