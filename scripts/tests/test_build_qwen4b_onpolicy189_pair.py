"""Focused CPU tests for paired Qwen4B on-policy SFT packing."""
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pandas as pd
import pytest
from tokenizers import Tokenizer, models, pre_tokenizers


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "scripts/exp21/build_qwen4b_onpolicy189_pair.py"
HEADER = "Solve the following problem step by step.\nEnd your response with a line starting with Final Answer: followed by the final result.\n\nProblem: "
sys.path.insert(0, str(ROOT / "scripts/exp21"))
from build_qwen4b_onpolicy189_pair import replay_rows  # noqa: E402


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def tagged_answer():
    return ("<think><Parallel><Goal><Outline>1: first part</Outline><Outline>2: second part</Outline></Goal>"
            "<Path>1: First result.</Path><Path>2: Second result.</Path>"
            "<Conclusion>Combine them.</Conclusion></Parallel></think>\nFinal Answer: 1")


def candidates():
    rows = []
    for source, count in (("math", 94), ("gsm8k", 95)):
        for number in range(count):
            identifier = f"{source}-train/{number}"
            rows.append({"id": identifier, "source": source, "question": f"{source} question {number}?",
                         "answer": "1", "answer_type": "number"})
    return rows


def make_fixed40(path, directory):
    for part in range(4):
        member = directory / f"part{part}-block-rows.jsonl"
        write_jsonl(member, [{"problem_id": f"fixed/{part}/{number}",
                              "problem": HEADER + f"fixed question {part}-{number}?"} for number in range(10)])
    with tarfile.open(path, "w:gz") as archive:
        for member in sorted(directory.glob("*.jsonl")):
            archive.add(member, arcname=member.name)


def make_validation(path, arm):
    rows = []
    for number in range(50):
        answer = tagged_answer() if arm == "tagged" else tagged_answer().replace("<Parallel>", "").replace("</Parallel>", "").replace("<Goal>", "").replace("</Goal>", "").replace("<Outline>", "").replace("</Outline>", "").replace("<Path>", "").replace("</Path>", "").replace("<Conclusion>", "").replace("</Conclusion>", "")
        rows.append({"data_source": "fixture", "id": f"val/{number}", "source": "math",
                     "extra_info": {"question": HEADER + f"validation question {number}?", "answer": answer,
                                    "enable_thinking": True, "kind": "parallel_th", "id": f"val/{number}"},
                     "index": number})
    pd.DataFrame(rows).to_parquet(path, index=False)


def make_replay(path, kind):
    rows = []
    for number in range(100):
        response = (f"<think>Reason {number}.</think>\nFinal Answer: {number}" if kind == "replay_th"
                    else f"Final Answer: {number}")
        row = {"id": f"{kind}-train/{number}", "source": "math", "question": f"{kind} question {number}?",
               "answer_type": "number", "correct": True, "clean": True, "truncated": False}
        if kind == "replay_th":
            row.update({"output": response, "sample": 0, "mode": "thinking", "prompt_variant": "structured"})
        else:
            row["response"] = response
        rows.append(row)
    write_jsonl(path, rows)


def make_tokenizer(path):
    tokenizer = Tokenizer(models.WordLevel({"<unk>": 0}, unk_token="<unk>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    tokenizer.save(str(path))


def command(paths, accepted_ids, manifest=True):
    if manifest:
        paths["manifest"].write_text(json.dumps({"semantic_path_independence": "reviewed",
                                                   "accepted_ids": accepted_ids}))
    return [sys.executable, str(BUILDER), "--candidates", str(paths["candidates"]), "--candidate-audit", str(paths["audit"]),
            "--rollouts", str(paths["rollouts"]), "--accepted-manifest", str(paths["manifest"]),
            "--provisional", str(paths["provisional"]), "--focus-tagged-val", str(paths["tagged_val"]),
            "--focus-plain-val", str(paths["plain_val"]), "--fixed40", str(paths["fixed"]),
            "--replay-thinking", str(paths["replay_th"]), "--replay-no-thinking", str(paths["replay_nt"]),
            "--replay-thinking-provenance", "fixture-qwen4b-thinking", "--replay-no-thinking-provenance",
            "fixture-qwen4b-no-thinking",
            "--tokenizer", str(paths["tokenizer"]),
            "--replay-thinking-count", "4", "--replay-no-thinking-count", "5", "--out-prefix", str(paths["out"]),
            "--report", str(paths["report"])]


@pytest.fixture
def pack_inputs(tmp_path):
    rows = candidates()
    paths = {name: tmp_path / name for name in
             ("candidates", "audit", "rollouts", "manifest", "provisional", "tagged_val", "plain_val", "fixed",
              "replay_th", "replay_nt", "report", "tokenizer")}
    paths["out"] = tmp_path / "onpolicy"
    write_jsonl(paths["candidates"], rows)
    paths["audit"].write_text(json.dumps({"checks": {"selected_overlap_each_exclusion": 0,
                                                        "leakcheck": {"blocking_hits": 0}},
                                            "ids": {"selected": [row["id"] for row in rows]}}))
    generated = [{"id": row["id"], "source": row["source"], "answer_type": row["answer_type"], "seed": 0,
                  "input": "chat" + HEADER + row["question"], "output": tagged_answer(), "tokens": 42,
                  "forward_calls": 43, "truncated": False, "settings": {}} for row in rows]
    write_jsonl(paths["rollouts"], generated)
    write_jsonl(paths["provisional"], [{"id": row["id"], "output": row["output"], "rejection_reasons": []}
                                         for row in generated[:30]])
    make_validation(paths["tagged_val"], "tagged")
    make_validation(paths["plain_val"], "plain")
    make_fixed40(paths["fixed"], tmp_path)
    make_replay(paths["replay_th"], "replay_th")
    make_replay(paths["replay_nt"], "replay_nt")
    make_tokenizer(paths["tokenizer"])
    return paths, generated


def test_builds_exact_paired_counts_and_preserves_text(pack_inputs):
    paths, generated = pack_inputs
    accepted = [row["id"] for row in generated[:30]]
    result = subprocess.run(command(paths, accepted), capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    tagged = pd.read_parquet(f"{paths['out']}_tagged_train.parquet").to_dict("records")
    plain = pd.read_parquet(f"{paths['out']}_plain_train.parquet").to_dict("records")
    assert len(tagged) == len(plain) == 99
    for left, right in zip(tagged, plain):
        assert left["id"] == right["id"]
        assert left["extra_info"]["question"] == right["extra_info"]["question"]
        stripped = left["extra_info"]["answer"]
        for tag in ("<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>", "</Outline>",
                    "<Path>", "</Path>", "<Conclusion>", "</Conclusion>"):
            stripped = stripped.replace(tag, "")
        assert stripped == right["extra_info"]["answer"]
    report = json.loads(paths["report"].read_text())
    assert report["train"]["kind_counts"] == {"parallel_th": 90, "replay_th": 4, "replay_nt": 5}


def test_rejects_manifest_ids_without_filter_evidence(pack_inputs):
    paths, generated = pack_inputs
    accepted = [row["id"] for row in generated[:29]] + [generated[30]["id"]]
    result = subprocess.run(command(paths, accepted), capture_output=True, text=True)
    assert result.returncode != 0
    assert "correct structural-filter evidence" in result.stderr


def test_rejects_missing_semantic_manifest(pack_inputs):
    paths, generated = pack_inputs
    accepted = [row["id"] for row in generated[:30]]
    paths["manifest"].write_text(json.dumps({"semantic_path_independence": "unreviewed", "accepted_ids": accepted}))
    result = subprocess.run(command(paths, accepted, manifest=False),
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert "not reviewed" in result.stderr


def test_real_replay_schemas_smoke_without_rollout():
    data = ROOT / "results/21-qwen3-0.6b-multiverse/data"
    thinking, thinking_stats = replay_rows(data / "qwen4b_teacher_graded320.jsonl", "replay_th")
    no_thinking, no_thinking_stats = replay_rows(data / "replay_nt.jsonl", "replay_nt")
    assert thinking_stats["source_rows"] == 320
    assert len(thinking) == thinking_stats["usable_rows"] == 146
    assert thinking_stats["excluded_rows"] == 174
    assert thinking_stats["excluded_grade_rows"] == 157
    assert thinking_stats["excluded_structural_rows"] == 17
    assert no_thinking_stats["source_rows"] == 300
    assert len(no_thinking) == no_thinking_stats["usable_rows"] == 271
    assert no_thinking_stats["excluded_grade_rows"] == 0
    assert no_thinking_stats["excluded_structural_rows"] == 29
