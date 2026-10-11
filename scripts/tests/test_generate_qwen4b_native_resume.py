"""Focused CPU tests for native Qwen4B resume generation."""
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/exp21"))
from generate_qwen4b_native_resume import (  # noqa: E402
    HEADER, prepare_resume, prompt_for, prompt_provenance, read_candidates, run_settings, write_record,
)


class Tokenizer:
    def apply_chat_template(self, messages, **kwargs):
        assert kwargs == {"add_generation_prompt": True, "tokenize": False, "enable_thinking": True}
        return "rendered: " + messages[0]["content"]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def candidate(answer="GOLD-ANSWER-MUST-NOT-LEAK"):
    return {"id": "math/train-1", "source": "math", "question": "What is one plus one?",
            "answer": answer, "answer_type": "integer"}


def record(settings, row, prompt):
    return {
        "id": row["id"], "source": row["source"], "answer_type": row["answer_type"],
        "seed": settings["seed"], "model_path": settings["model_path"], "mode": settings["mode"],
        "prompt": prompt, "prompt_provenance": prompt_provenance(settings, row),
        "output": "<think>one plus one is two</think>\nFinal Answer: 2", "tokens": 12,
        "truncated": False, "generation": settings["generation"],
    }


def test_candidate_gold_is_not_retained_or_persisted(tmp_path):
    input_path = tmp_path / "candidates.jsonl"
    output_path = tmp_path / "out.jsonl"
    secret = "GOLD-ANSWER-MUST-NOT-LEAK"
    write_jsonl(input_path, [candidate(secret)])
    rows = read_candidates(input_path)
    assert rows == [{"id": "math/train-1", "source": "math", "question": "What is one plus one?",
                     "answer_type": "integer", "line": 1}]
    settings = run_settings("/model", input_path, "thinking", 99, 7, rows)
    prompt = prompt_for(Tokenizer(), rows[0]["question"], True)
    assert prompt == "rendered: " + HEADER + rows[0]["question"]
    assert prepare_resume(output_path, settings) == set()
    with output_path.open("a") as handle:
        write_record(handle, record(settings, rows[0], prompt))
    assert prepare_resume(output_path, settings) == {"math/train-1"}
    assert secret not in output_path.read_text()
    assert secret not in output_path.with_suffix(".jsonl.meta.json").read_text()


def test_resume_rejects_changed_settings_and_duplicate_record(tmp_path):
    input_path = tmp_path / "candidates.jsonl"
    output_path = tmp_path / "out.jsonl"
    write_jsonl(input_path, [candidate()])
    rows = read_candidates(input_path)
    settings = run_settings("/model", input_path, "no-thinking", 23, 0, rows)
    prepare_resume(output_path, settings)
    one = record(settings, rows[0], "rendered prompt")
    with output_path.open("a") as handle:
        write_record(handle, one)
        write_record(handle, one)
    with pytest.raises(ValueError, match="inconsistent resumed output"):
        prepare_resume(output_path, settings)
    changed = run_settings("/model", input_path, "thinking", 23, 0, rows)
    with pytest.raises(ValueError, match="run settings changed"):
        prepare_resume(output_path, changed)


def test_read_candidates_rejects_bad_schema(tmp_path):
    path = tmp_path / "bad.jsonl"
    write_jsonl(path, [{"id": "x"}])
    with pytest.raises(ValueError, match="misses required fields"):
        read_candidates(path)
