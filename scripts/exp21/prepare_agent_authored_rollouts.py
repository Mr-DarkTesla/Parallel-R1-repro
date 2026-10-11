"""Convert question-only authored solutions into the standard quality-filter schema."""

import argparse
import json
from pathlib import Path


def read(path):
    rows = [json.loads(line) for line in path.open() if line.strip()]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate IDs: {path}")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path)
    parser.add_argument("math", type=Path)
    parser.add_argument("gsm", type=Path)
    parser.add_argument("tokenizer")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    candidates = read(args.candidates)
    authored = read(args.math) + read(args.gsm)
    solutions = {row["id"]: row for row in authored}
    if len(solutions) != len(authored) or set(solutions) != {row["id"] for row in candidates}:
        raise ValueError("authored IDs must exactly match selected candidate IDs")

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    with args.output.open("x") as handle:
        for candidate in candidates:
            row = solutions[candidate["id"]]
            if row.get("source") != candidate["source"] or not isinstance(row.get("output"), str):
                raise ValueError(f"bad source or output for {candidate['id']}")
            record = {
                "id": candidate["id"], "source": candidate["source"],
                "answer_type": candidate["answer_type"], "seed": 0,
                "output": row["output"],
                "tokens": len(tokenizer.encode(row["output"], add_special_tokens=False)),
                "truncated": False,
                "origin": "agent-authored-question-only",
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"prepared {len(candidates)} authored rows")


if __name__ == "__main__":
    main()
