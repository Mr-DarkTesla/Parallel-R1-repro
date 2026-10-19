"""Read-only token composition extraction for new-reward SFT -> RL150."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path("${PROJECT_ROOT}")
TRAIN = ROOT / "work/experiments/rl-r4-dapo2k-sft-16gpu-20261013"
EVAL = ROOT / "work/experiments/rl-r4-posteval-20261013/sft/checkpoint-0150"
OLD = ROOT / "work/experiments/eval-rl300-vllm-rolling-32k-20261013"
EXPECTED_REWARD = "C*(1-.9*(1-exp(-ln(9)*F/10000)))"
CATEGORIES = ["plan", "branches", "summary", "answer", "other_thought", "service"]

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

config = read(TRAIN / "production-config.json")
job = read(EVAL / "job.json")
checkpoint = TRAIN / "production/checkpoint-0150"
complete = read(checkpoint / "complete.json")
proof = read(EVAL.parent / "training-completed-proof.json")
summary = read(EVAL / "runs/MATH500/summary.json")
assert config["initial_step"] == 0 and config["initial_checkpoint"] is None
assert config["model"] == str(ROOT / "work/experiments/instruct-full-20261011/runs/epoch1/final")
assert config["experiment"]["reward"] == EXPECTED_REWARD
assert config["reward_mode"] == "forward_only"
assert config["experiment"]["width_bonus"] == config["experiment"]["round_bonus"] == 0
assert config["std_normalization"] is False
assert job["checkpoint"] == complete["step"] == proof["completed_step"] == 150
assert job["model"] == str(checkpoint / "hf")
assert complete["files"]["hf/model.safetensors"]["sha256"] == job["model_sha256"]
assert summary["passed"] and summary["completed"] == 500 and summary["technical_unknown"] == 0
assert summary["model_sha256"] == job["model_sha256"]

def extract(root):
    eval_job = read(root / "job.json")
    tokenizer_config = read(Path(eval_job["model"]) / "tokenizer_config.json")
    decoder = tokenizer_config["added_tokens_decoder"]
    token_ids = {v["content"]: int(k) for k, v in decoder.items()}
    tags = {token_ids[t] for t in ["<Parallel>", "</Parallel>", "<Path>", "</Path>",
                                   "<Summary>", "</Summary>", "<think>", "</think>"]}
    # These terminate model calls and are service tokens rather than prose.
    model_config = read(Path(eval_job["model"]) / "config.json")
    eos = model_config["eos_token_id"]
    tags.update(eos if isinstance(eos, list) else [eos])
    tags.update(token_ids[t] for t in ["<|im_end|>", "<|endoftext|>"] if t in token_ids)
    tc = token_ids["</think>"]
    po = token_ids["<Parallel>"]
    records = []
    files = []
    for path in sorted((root / "runs/MATH500").glob("rank-*.jsonl")):
        h = hashlib.sha256()
        rows = 0
        with path.open("rb") as stream:
            for line in stream:
                h.update(line)
                if not line.strip():
                    continue
                row = json.loads(line)
                rows += 1
                assert row["dataset"] == "MATH500" and not row["technical_unknown"]
                assert row["model_identity"]["sha256"] == eval_job["model_sha256"]
                ids = row["response_ids"]
                mask = row["response_mask"]
                assert len(ids) == len(mask)
                counts = Counter({c: 0 for c in CATEGORIES})
                counts["service"] = sum(m == 0 for m in mask)
                occupied = set()
                thinking = True
                seen_parallel = False
                for call in row["policy_calls"]:
                    start = call["response_start"]
                    stop = start + len(call["generated_ids"])
                    assert 0 <= start <= stop <= len(ids)
                    phase = call["phase"]
                    assert phase in ["main", "width", "path", "summary"]
                    for index in range(start, stop):
                        assert index not in occupied and mask[index] == 1
                        occupied.add(index)
                        token = ids[index]
                        if phase == "width" or token in tags:
                            category = "service"
                        elif phase == "path":
                            category = "branches"
                        elif phase == "summary":
                            category = "summary"
                        elif not thinking:
                            category = "answer"
                        elif seen_parallel:
                            category = "other_thought"
                        else:
                            category = "plan"
                        counts[category] += 1
                        if phase == "main" and token == tc:
                            thinking = False
                        if phase == "main" and token == po:
                            seen_parallel = True
                assert occupied == {i for i, m in enumerate(mask) if m == 1}
                assert sum(counts.values()) == len(ids)
                assert sum(mask) == row["stats"]["sampled_tokens"]
                records.append(dict(id=row["id"], valid=row["format_valid"],
                                    correct=row["grade"]["correct"], total=len(ids),
                                    sampled=sum(mask), counts=dict(counts)))
        files.append(dict(path=str(path.relative_to(ROOT)), sha256=h.hexdigest(), rows=rows))
    assert len(records) == len({r["id"] for r in records}) == 500
    return records, files

records, files = extract(EVAL)
reference_records, reference_files = extract(OLD)
assert sum(r["correct"] for r in records) == summary["correct"]
assert sum(r["valid"] for r in records) == summary["format_valid"]
assert sum(r["sampled"] for r in records) / 500 == summary["sampled_tokens_all"]
metadata = dict(
    checkpoint=150, dataset="MATH500", reward=EXPECTED_REWARD,
    initial_model=config["model"], training_root=str(TRAIN), evaluation_root=str(EVAL),
    model_sha256=job["model_sha256"], summary=summary,
    reward_source_sha256=digest(Path(config["reward"])),
    training_config_sha256=digest(TRAIN / "production-config.json"),
    job_sha256=digest(EVAL / "job.json"), complete_sha256=digest(checkpoint / "complete.json"),
    extracted_at=datetime.now(timezone.utc).isoformat(), source_files=files,
    protocol=dict(precision=job["precision"], response_budget=job["response_budget"],
                  path_budget=job["path_budget"], samples_per_question=1),
)
print(json.dumps(dict(metadata=metadata, records=records,
                      reference_records=reference_records, reference_sources=reference_files),
                 separators=(",", ":")))
