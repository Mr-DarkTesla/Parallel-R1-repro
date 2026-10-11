#!/usr/bin/env python3
"""Release cached pages of completed /tmp exp21 weight files without deleting them."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def memory_bytes() -> int:
    return int(Path("/sys/fs/cgroup/memory.current").read_text())


def main() -> None:
    roots = [Path(arg).resolve() for arg in sys.argv[1:]]
    if not roots or any(not str(root).startswith("/tmp/exp21-") for root in roots):
        raise SystemExit("only explicit /tmp/exp21-* roots are accepted")
    before = memory_bytes()
    count = size = 0
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.safetensors"):
            if path.is_symlink() or not path.is_file():
                continue
            fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC)
            try:
                os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
            finally:
                os.close(fd)
            count += 1
            size += path.stat().st_size
    print(json.dumps({"roots": [str(root) for root in roots], "files": count,
                      "advised_gb": round(size / 1e9, 3),
                      "memory_gb_before": round(before / 1e9, 3),
                      "memory_gb_after": round(memory_bytes() / 1e9, 3)}))


if __name__ == "__main__":
    main()
