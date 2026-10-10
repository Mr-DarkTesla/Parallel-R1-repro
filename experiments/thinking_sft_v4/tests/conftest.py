"""Shared pytest setup: the package directory and tests/ on sys.path, tiny tokenizer/model fixtures."""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
for path in (HERE.parent, HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from tiny import build_tiny_model, build_tiny_tokenizer  # noqa: E402


@pytest.fixture
def tiny_tokenizer():
    """Fresh tiny tokenizer, contract tags NOT added."""
    return build_tiny_tokenizer()


@pytest.fixture
def tiny_model(tiny_tokenizer):
    """Fresh tiny fp32 Qwen3 (sdpa) sized for tiny_tokenizer plus the tags."""
    return build_tiny_model(tiny_tokenizer)
