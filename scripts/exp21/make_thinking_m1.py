"""Move reviewed M1 blocks inside Qwen3's thinking span without changing solution text.

Usage: python make_thinking_m1.py M1_PAIRS_JSONL OUT_JSONL
The sole final answer line moves after </think>; all preceding words and tags stay
in the same order. The original M1 cards and reviews still cover their content.
"""
import json
import re
import sys

from mv_format import parse


def convert(row):
    response = row["response"]
    finals = list(re.finditer(r"(?im)^\s*Final Answer\s*:", response))
    assert len(finals) == 1, row["id"]
    reasoning = response[:finals[0].start()].rstrip()
    final = response[finals[0].start():].strip()
    assert len(final.splitlines()) == 1, row["id"]
    assert "<think>" not in response and "</think>" not in response, row["id"]
    structure = parse(reasoning)
    assert structure["valid"] and all(b["numbered"] for b in structure["blocks"]), row["id"]
    transformed = f"<think>\n{reasoning}\n</think>\n{final}"
    assert re.sub(r"\s+", "", reasoning + final) == re.sub(r"\s+", "", response), row["id"]
    return {**row, "response": transformed, "method": "m1_th_wrap"}


def main():
    source, target = sys.argv[1:3]
    rows = [convert(json.loads(line)) for line in open(source)]
    assert len(rows) == len({row["id"] for row in rows}), "duplicate problems"
    with open(target, "w") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("converted", len(rows))


if __name__ == "__main__":
    main()
