"""Regex validator of parallel-thinking tags.

A correct block is <Parallel>, at least two <Path>...</Path>, </Parallel>, then <Summary>...</Summary>,
with no other tags inside. A tag is correctly placed if it belongs to a correct block.

Usage: python scripts/tag_validator.py <generations.jsonl>   (field "output", as dumped by the authors' validation)
"""
import json
import re
import sys

TAG = re.compile(r"</?(?:Parallel|Path|Summary)>")
TEXT = r"(?:(?!</?(?:Parallel|Path|Summary)>).)*"
BLOCK = re.compile(rf"<Parallel>(?:\s*<Path>{TEXT}</Path>){{2,}}\s*</Parallel>\s*<Summary>{TEXT}</Summary>", re.S)


def validate(text):
    """Return (number of tags, number of correctly placed tags)."""
    tags = len(TAG.findall(text))
    correct = sum(len(TAG.findall(block)) for block in BLOCK.findall(text))
    return tags, correct


def summarize(texts):
    counts = [validate(text) for text in texts]
    with_tags = [(tags, correct) for tags, correct in counts if tags]
    return {
        "responses": len(texts),
        "with_tags": len(with_tags) / len(texts),
        "correct_tag_share": sum(c for _, c in with_tags) / max(sum(t for t, _ in with_tags), 1),
        "all_tags_correct": sum(t == c for t, c in with_tags) / max(len(with_tags), 1),
    }


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        outputs = [json.loads(line)["output"] for line in f]
    print(json.dumps({key: round(value, 4) for key, value in summarize(outputs).items()}))
