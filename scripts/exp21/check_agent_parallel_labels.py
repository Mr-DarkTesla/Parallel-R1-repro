"""Check accepted Parallel labels with the exact on-policy answer rule on CPU."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "verl"))
from exp21.filter_onpolicy_rollouts import answer_checker  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", type=Path)
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    records = [json.loads(line) for line in args.labels.read_text().splitlines() if line.strip()]
    checker = answer_checker()
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    lengths, failures = [], []
    for row in records:
        final = row["output"].split("</think>", 1)[1]
        if not checker(row["source"], final, row["answer"]):
            failures.append(row["id"])
        lengths.append(len(tokenizer.encode(row["output"], add_special_tokens=False)))
    print(json.dumps({
        "rows": len(records), "accepted_by_math_verify": len(records) - len(failures),
        "failure_ids": failures, "output_tokens_min": min(lengths),
        "output_tokens_max": max(lengths),
        "output_tokens_mean": round(sum(lengths) / len(lengths), 1),
        "over_4096": sum(length > 4096 for length in lengths),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
