"""Select candidate records and merge question-only authored solution batches."""

import argparse
import json
from pathlib import Path


def read(path):
    rows = [json.loads(line) for line in path.open() if line.strip()]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate IDs in {path}")
    return rows


def write(path, rows):
    if path.exists():
        raise FileExistsError(path)
    with path.open("x") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("authored", nargs="+", type=Path)
    args = parser.parse_args()

    candidates = {row["id"]: row for row in read(args.candidates)}
    authored = [row for path in args.authored for row in read(path)]
    ids = [row["id"] for row in authored]
    if len(ids) != len(set(ids)) or set(ids) - candidates.keys():
        raise ValueError("authored IDs duplicate or absent from candidate pool")
    by_source = {"math": [], "gsm8k": []}
    for row in authored:
        source = candidates[row["id"]]["source"]
        if row.get("source") != source or not isinstance(row.get("output"), str):
            raise ValueError(f"bad authored source/output for {row['id']}")
        by_source[source].append(row)
    selected = [row for row in read(args.candidates) if row["id"] in set(ids)]
    if len(selected) != len(authored):
        raise AssertionError("selected count differs from authored count")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write(args.output_dir / "candidates.jsonl", selected)
    write(args.output_dir / "math.jsonl", by_source["math"])
    write(args.output_dir / "gsm.jsonl", by_source["gsm8k"])
    print(f"selected={len(selected)} math={len(by_source['math'])} gsm8k={len(by_source['gsm8k'])}")


if __name__ == "__main__":
    main()
