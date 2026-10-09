"""Incremental Multiverse attention for one flat block, without inserting tokens.

The caller supplies the number of outlines from the model's Goal before the first
Path closes. Every emitted token is then fed back with the same sibling visibility
and position as `multiverse_structure.py` uses for SFT.
"""


class MaskedDecodeState:
    def __init__(self, path_open, path_close, expected_paths=None):
        self.path_open = path_open
        self.path_close = path_close
        self.expected_paths = expected_paths
        self.tokens = []
        self.positions = []
        self.phase = "pre"
        self.base = None
        self.current_start = None
        self.suffix_start = None
        self.suffix_base = None
        self.path_spans = []
        self.path_lengths = []

    def append(self, token):
        i = len(self.tokens)
        phase = self.phase
        if phase == "pre" and token == self.path_open:
            self.base = self.current_start = i
            self.phase = phase = "path"
        if phase == "pre":
            position = i
        elif phase in ("path", "gap"):
            position = self.base + i - self.current_start
        else:
            position = self.suffix_base + i - self.suffix_start
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
                self.suffix_start = end
                self.suffix_base = self.base + max(self.path_lengths)
                self.phase = "suffix"
        elif phase == "gap" and token == self.path_open:
            self.phase = "path"
        return position, visible
