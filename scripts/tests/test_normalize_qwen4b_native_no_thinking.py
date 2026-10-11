"""Focused tests for native Qwen3-4B no-thinking final-line normalization."""
import copy
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/exp21"))
from normalize_qwen4b_native_no_thinking import normalize  # noqa: E402


def row(**changes):
    value = {
        "id": "gsm8k-train/1", "mode": "no-thinking", "output": "2 + 3 = 5\n\n### Final Answer: 5",
        "candidate": "5", "truncated": False, "clean": True, "correct": True,
        "source": "gsm8k", "metadata": {"keep": "verbatim"},
    }
    value.update(changes)
    return value


def test_appends_only_missing_canonical_final_line_and_preserves_metadata():
    original = row()
    unchanged = row(id="gsm8k-train/2", output="reasoning\nFinal Answer: 8", candidate="8")
    incorrect = row(id="gsm8k-train/3", correct=False, candidate="wrong")
    result, added = normalize([copy.deepcopy(original), copy.deepcopy(unchanged), copy.deepcopy(incorrect)])

    assert added == 1
    assert result[0]["output"] == original["output"] + "\n\nFinal Answer: 5"
    assert result[0]["final_answer_line_added"] is True
    assert result[0]["metadata"] == original["metadata"]
    assert result[1]["output"] == unchanged["output"]
    assert result[1]["final_answer_line_added"] is False
    assert result[2]["output"] == incorrect["output"]
    assert result[2]["final_answer_line_added"] is False


def test_accepts_boxed_candidate_and_keeps_provenance_on_rerun():
    original = row(candidate="$ \\boxed{115}", output="work\n\n**Final Answer:** $ \\boxed{115} $")
    normalized, added = normalize([original])
    rerun, rerun_added = normalize(normalized)

    assert added == 1
    assert normalized[0]["output"].endswith("Final Answer: $ \\boxed{115}")
    assert rerun_added == 0
    assert rerun == normalized


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"mode": "thinking"}, "mode must be no-thinking"),
        ({"output": "<think>reasoning</think>\nFinal Answer: 5"}, "think tags"),
        ({"candidate": "different"}, "malformed parsed candidate"),
        ({"candidate": "5\nextra"}, "malformed parsed candidate"),
    ],
)
def test_rejects_unsafe_rows(changes, message):
    with pytest.raises(ValueError, match=message):
        normalize([row(**changes)])


def test_rejects_duplicate_ids():
    with pytest.raises(ValueError, match="duplicate ID"):
        normalize([row(), row()])
