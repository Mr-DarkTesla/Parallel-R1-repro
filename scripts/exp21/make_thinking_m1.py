"""Move reviewed M1 or M2 blocks inside Qwen3's thinking span without changing solution text.

Usage: python make_thinking_m1.py PAIRS_JSONL OUT_JSONL
The last Final Answer section moves after </think>; all words and tags stay in order.
"""
import json
import re
import sys

from mv_format import parse


def convert(row):
    response = row["response"]
    finals = list(re.finditer(r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?Final Answer[ \t]*:", response))
    if not finals:
        # One audited M2 trace puts the final answer in a Step heading and a boxed line.
        finals = list(re.finditer(r"(?im)^#{1,6}[ \t]*Step[ \t]+\d+[ \t]*:[ \t]*Final Answer[ \t]*$", response))
    assert finals, row["id"]
    reasoning = response[:finals[-1].start()].rstrip()
    final = response[finals[-1].start():].strip()
    assert reasoning and final, row["id"]
    assert "<think>" not in response and "</think>" not in response, row["id"]
    structure = parse(reasoning)
    assert structure["valid"] and all(b["numbered"] for b in structure["blocks"]), row["id"]
    transformed = f"<think>\n{reasoning}\n</think>\n{final}"
    assert re.sub(r"\s+", "", reasoning + final) == re.sub(r"\s+", "", response), row["id"]
    return {**row, "response": transformed, "method": f"{row.get('method', 'm2')}_th_wrap"}


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
