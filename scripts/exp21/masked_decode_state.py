"""Incremental Multiverse attention for flat blocks, without inserting tokens.

The caller supplies the number of outlines from the model's Goal before the first
Path closes. Every emitted token is then fed back with the same sibling visibility
and position as `multiverse_structure.py` uses for SFT. After each block's last
path, plain text and later blocks continue from that block's longest path.
"""
import re


def path_count(prefix):
    """Count numbered outlines in the most recent complete Goal."""
    start = prefix.rfind("<Goal>")
    if start < 0:
        return 0
    goal = re.fullmatch(r"<Goal>(.*?)</Goal>\s*", prefix[start:], re.S)
    if not goal:
        return 0
    outlines = re.findall(r"<Outline>\s*(\d+)\s*:(.*?)</Outline>", goal.group(1), re.S)
    if len(outlines) not in (2, 3, 4):
        return 0
    return len(outlines) if [int(x[0]) for x in outlines] == list(range(1, len(outlines) + 1)) else 0


class MaskedDecodeState:
    def __init__(self, path_open, path_close, expected_paths=None):
        self.path_open = path_open
        self.path_close = path_close
        self.expected_paths = expected_paths
        self.tokens = []
        self.positions = []
        self.phase = "plain"
        self.next_plain_position = 0
        self.base = None
        self.current_start = None
        self.path_spans = []
        self.path_lengths = []

    def append(self, token):
        i = len(self.tokens)
        phase = self.phase
        if phase == "plain" and token == self.path_open:
            if self.expected_paths is None:
                raise ValueError("set expected_paths from the Goal before the first <Path>")
            self.base = self.next_plain_position
            self.current_start = i
            self.path_spans = []
            self.path_lengths = []
            self.phase = phase = "path"
        if phase == "plain":
            position = self.next_plain_position
            self.next_plain_position += 1
        else:
            position = self.base + i - self.current_start
        visible = [True] * (i + 1)
        if phase in ("path", "gap"):
            for start, end in self.path_spans:
                visible[start:end] = [False] * (end - start)
        self.tokens.append(token)
        self.positions.append(position)
        if phase == "path" and token == self.path_close:
            end = i + 1
            self.path_spans.append((self.current_start, end))
            self.path_lengths.append(position - self.base + 1)
            if self.expected_paths is None:
                raise ValueError("set expected_paths from the Goal before the first </Path>")
            if len(self.path_spans) < self.expected_paths:
                self.current_start = end
                self.phase = "gap"
            else:
                self.next_plain_position = self.base + max(self.path_lengths)
                self.base = self.current_start = self.expected_paths = None
                self.path_spans = []
                self.path_lengths = []
                self.phase = "plain"
        elif phase == "gap" and token == self.path_open:
            self.phase = "path"
        return position, visible
