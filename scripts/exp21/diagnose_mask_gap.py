"""Show the SFT context of the second Path transition versus causal decoding.

Uses a toy tokenization because the difference follows from the structural mask,
independently of the model tokenizer. No model or GPU is needed.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verl/verl/utils/dataset"))
from multiverse_structure import multiverse_structure  # noqa: E402


def main():
    tags = {"Parallel": 1000, "/Parallel": 1001, "Path": 1002, "/Path": 1003}
    named = [
        ("<Parallel>", 1000), ("<Goal>", 1010), ("outlines", 1011), ("</Goal>", 1012), ("\\n", 10),
        ("<Path> 1", 1002), ("\\n 1", 10), ("1: body", 1020), ("</Path> 1", 1003),
        ("\\n", 10), ("<Path> 2", 1002), ("\\n 2", 10), ("2: body", 1021), ("</Path> 2", 1003),
        ("\\n", 10), ("<Conclusion>", 1030), ("answer", 1031), ("</Conclusion>", 1032), ("</Parallel>", 1001),
    ]
    ids = [token for _, token in named]
    positions, groups = multiverse_structure(ids, tags)
    first, second = groups[0]
    second_gap = second[0]
    first_body = first[0] + 2
    assert first[0] < first_body < first[1] <= second_gap
    blocked = any(s1 <= first_body < e1 and s2 <= second_gap < e2
                  for spans in groups for (s1, e1), (s2, e2) in zip(spans, spans[1:]))
    assert blocked and first_body < second_gap
    assert positions[second_gap] == positions[first[0]]
    print(json.dumps({
        "first_path_span": first, "second_path_span": second,
        "first_path_start_position": positions[first[0]],
        "second_gap_position": positions[second_gap],
        "second_gap_token": named[second_gap][0],
        "first_body_visible_to_second_gap_in_sft": not blocked,
        "first_body_visible_to_second_gap_in_causal_decode": True,
        "shifted_loss_note": "The first token of path 2 is predicted from the last token of path 1; "
                             "the following tokens use the sibling mask.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
