"""Focused CPU tests for approved Qwen4B on-policy rollout repairs."""
import json
import subprocess
import sys
from pathlib import Path

import pytest
from tokenizers import Tokenizer, models, pre_tokenizers


ROOT = Path(__file__).resolve().parents[2]
ASSEMBLER = ROOT / "scripts/exp21/assemble_qwen4b_repaired_rollouts.py"


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def response(answer="1"):
    return ("<think>\n"
            "<Parallel><Goal><Outline>1: first value</Outline><Outline>2: second value</Outline></Goal>"
            "<Path>1: Find first value.</Path><Path>2: Find second value.</Path>"
            "<Conclusion>Combine values.</Conclusion></Parallel>\n"
            "</think>\n"
            f"Final Answer: {answer}")


def make_tokenizer(path):
    tokenizer = Tokenizer(models.WordLevel({"<unk>": 0}, unk_token="<unk>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    tokenizer.save(str(path))


@pytest.fixture
def inputs(tmp_path):
    candidates = []
    rollouts = []
    for number in range(3):
        identifier = f"gsm8k-train/{number}"
        question = f"What is fixture {number}?"
        candidates.append({"id": identifier, "source": "gsm8k", "answer_type": "integer",
                           "question": question, "answer": str(number + 1)})
        rollouts.append({"id": identifier, "source": "gsm8k", "answer_type": "integer", "seed": 0,
                         "input": f"header\n\nProblem: {question}<|im_end|>\nassistant\n",
                         "output": response(str(number + 1)), "tokens": 1, "forward_calls": 1,
                         "truncated": False, "settings": {"decoder": "fixture"}})
    draft = {"id": "gsm8k-train/1", "source": "gsm8k", "answer_type": "integer",
             "question": candidates[1]["question"], "gold": "2", "response": response("2")}
    rollouts[0]["output"] = "<think>malformed original rollout"
    paths = {name: tmp_path / name for name in ("rollouts.jsonl", "candidates.jsonl", "drafts.jsonl",
                                                 "manifest.json", "tokenizer.json", "assembled.jsonl")}
    write_jsonl(paths["rollouts.jsonl"], rollouts)
    write_jsonl(paths["candidates.jsonl"], candidates)
    write_jsonl(paths["drafts.jsonl"], [draft])
    paths["manifest.json"].write_text(json.dumps({"approved_repair_ids": [draft["id"]]}))
    make_tokenizer(paths["tokenizer.json"])
    return paths, rollouts, draft


def command(paths):
    return [sys.executable, str(ASSEMBLER), "--rollouts", str(paths["rollouts.jsonl"]),
            "--candidates", str(paths["candidates.jsonl"]), "--drafts", str(paths["drafts.jsonl"]),
            "--manifest", str(paths["manifest.json"]), "--tokenizer", str(paths["tokenizer.json"]),
            "--output", str(paths["assembled.jsonl"]), "--expected-count", "3"]


def test_replaces_only_approved_draft_and_refuses_overwrite(inputs):
    paths, rollouts, draft = inputs
    result = subprocess.run(command(paths), capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    rows = [json.loads(line) for line in paths["assembled.jsonl"].read_text().splitlines()]
    assert [row["id"] for row in rows] == [row["id"] for row in rollouts]
    assert rows[0]["output"] == rollouts[0]["output"]
    assert rows[1]["output"] == draft["response"]
    assert rows[1]["tokens"] > 1
    assert rows[1]["input"] == rollouts[1]["input"]
    assert rows[0]["output_provenance"]["kind"] == "raw_model_rollout"
    assert rows[1]["output_provenance"] == {
        "kind": "approved_repair_draft", "raw_model_generation": False,
        "draft_file": str(paths["drafts.jsonl"]), "draft_line": 1,
        "approval_manifest": str(paths["manifest.json"]),
        "raw_generation_tokens": 1, "raw_generation_forward_calls": 1,
    }
    rerun = subprocess.run(command(paths), capture_output=True, text=True)
    assert rerun.returncode != 0
    assert "refusing to overwrite" in rerun.stderr


def test_rejects_approved_draft_without_numbered_multiverse_block(inputs):
    paths, _, draft = inputs
    draft["response"] = "<think><Parallel><Goal><Outline>first</Outline><Outline>second</Outline></Goal><Path>first</Path><Path>second</Path><Conclusion>done</Conclusion></Parallel></think>\nFinal Answer: 2"
    write_jsonl(paths["drafts.jsonl"], [draft])
    result = subprocess.run(command(paths), capture_output=True, text=True)
    assert result.returncode != 0
    assert "Multiverse block" in result.stderr
    assert not paths["assembled.jsonl"].exists()
