"""Check incremental positions and visibility against the SFT structure parser."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verl/verl/utils/dataset"))
from multiverse_structure import multiverse_structure  # noqa: E402
from masked_decode_state import MaskedDecodeState  # noqa: E402


TAGS = {"Parallel": 1000, "/Parallel": 1001, "Path": 1002, "/Path": 1003}


def check(count):
    ids = [1000, 1010, 1011, 1012, 10]
    for k in range(count):
        if k:
            ids.append(10)
        ids.extend((1002, 10, 1100 + k, 1200 + k, 1003))
    ids.extend((10, 1030, 1031, 1032, 1001, 1040))
    expected_positions, groups = multiverse_structure(ids, TAGS)
    state = MaskedDecodeState(TAGS["Path"], TAGS["/Path"], count)
    for i, token in enumerate(ids):
        position, visible = state.append(token)
        expected_visible = [j <= i and not any(
            s1 <= j < e1 and s2 <= i < e2
            for spans in groups for a, (s2, e2) in enumerate(spans)
            for s1, e1 in spans[:a]) for j in range(i + 1)]
        assert position == expected_positions[i], (count, i, position, expected_positions[i])
        assert visible == expected_visible, (count, i, visible, expected_visible)
    print(f"{count} paths: {len(ids)} token positions and attention rows match")


if __name__ == "__main__":
    check(2)
    check(3)
    check(4)
