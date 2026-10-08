"""Multiverse-style parallel format of exp 21 (no nesting): grammar validator, block parser and forward-pass count.

A block, as written in a sequential answer:
    <Parallel>
    <Goal>
    <Outline>1: what part 1 determines</Outline>
    <Outline>2: ...</Outline>
    </Goal>
    <Path>
    1: text of part 1
    </Path>
    <Path>
    2: ...
    </Path>
    <Conclusion>
    combined results
    </Conclusion>
    </Parallel>
Rules: >= 2 outlines, as many paths as outlines, outline k and path k start with "k:", only whitespace between the tagged parts,
no tag inside any text part, no tag outside blocks. Paths of a block are generated independently (they see the text before the
block and the Goal), so a block costs as many sequential forward passes as its longest path (Multiverse paper indexing).
"""
import re

TAGS = ["<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>", "</Outline>", "<Path>", "</Path>",
        "<Conclusion>", "</Conclusion>"]
ANY_TAG = re.compile(r"</?(?:Parallel|Goal|Outline|Path|Conclusion)>")
TEXT = r"((?:(?!</?(?:Parallel|Goal|Outline|Path|Conclusion)>).)*?)"
OUTLINE = re.compile(rf"<Outline>{TEXT}</Outline>", re.S)
PATH = re.compile(rf"<Path>{TEXT}</Path>", re.S)
BLOCK = re.compile(
    rf"<Parallel>\s*<Goal>((?:\s*<Outline>{TEXT[1:-1]}</Outline>)+)\s*</Goal>((?:\s*<Path>{TEXT[1:-1]}</Path>)+)"
    rf"\s*<Conclusion>{TEXT}</Conclusion>\s*</Parallel>", re.S)
NUMBER = re.compile(r"\s*(\d+)\s*:")


def parse(text):
    """-> dict(tags, valid_tags, blocks=[{start, end, outlines, paths, conclusion, numbered}], valid) for one answer.
    valid: at least one tag and every tag belongs to a grammatical block (numbering is reported separately)."""
    blocks = []
    for m in BLOCK.finditer(text):
        outlines, paths = OUTLINE.findall(m.group(1)), PATH.findall(m.group(2))
        if len(outlines) < 2 or len(paths) != len(outlines):
            continue
        numbers = lambda parts: [int(n.group(1)) if (n := NUMBER.match(p)) else None for p in parts]  # noqa: E731
        expected = list(range(1, len(paths) + 1))
        blocks.append({"start": m.start(), "end": m.end(), "outlines": outlines, "paths": paths, "conclusion": m.group(3),
                       "numbered": numbers(outlines) == expected and numbers(paths) == expected})
    tags = len(ANY_TAG.findall(text))
    valid_tags = sum(len(ANY_TAG.findall(text[b["start"]:b["end"]])) for b in blocks)
    return {"tags": tags, "valid_tags": valid_tags, "blocks": blocks, "valid": tags > 0 and tags == valid_tags}


def forward_passes(text, count_tokens):
    """Sequential decoding steps of an answer when the paths of each grammatical block run in parallel: text outside paths
    counts fully, each block's paths count as the longest one. count_tokens(str) -> int (the model's tokenizer)."""
    blocks = parse(text)["blocks"]
    total, saved = count_tokens(text), 0
    for b in blocks:
        segment = text[b["start"]:b["end"]]
        lengths = [count_tokens(m.group(0)) for m in PATH.finditer(segment)]
        saved += sum(lengths) - max(lengths)
    return total - saved


def strip_tags(text):
    """The same answer as sequential text: tags removed, outlines and conclusion kept as plain lines (tag-free control)."""
    text = re.sub(r"<Outline>\s*", "", text)
    text = ANY_TAG.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n" if text.strip() else text
