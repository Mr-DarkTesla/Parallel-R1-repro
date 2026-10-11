"""Resume-safe one-GPU Qwen3-4B generation through Transformers.

The candidate JSONL is validated against ``id, source, question, answer,
answer_type``. Gold answers are used only to reject malformed input: they are
never put in a prompt, metadata, or generated JSONL record.

Example (on the prepared GPU pod):
  python scripts/exp21/generate_qwen4b_native_resume.py \\
    /work/checkpoints/qwen3-4b-posttrained \\
    results/21-qwen3-0.6b-multiverse/data/candidates_leakchecked.jsonl \\
    /work/exp21/qwen4b_native/thinking.jsonl thinking --max-new-tokens 4096
"""

import argparse
import json
import os
from pathlib import Path


HEADER = ("Solve the following problem step by step.\n"
          "End your response with a line starting with Final Answer: followed by the final result.\n\n"
          "Problem: ")
REQUIRED_FIELDS = ("id", "source", "question", "answer", "answer_type")
SAMPLING = {
    "thinking": {"temperature": 0.6, "top_p": 0.95, "top_k": 20},
    "no-thinking": {"temperature": 0.7, "top_p": 0.8, "top_k": 20},
}
PROMPT_TEMPLATE = "plain_eval_header_v1"


def read_candidates(path: Path) -> list[dict]:
    """Read candidate rows and return only fields safe to persist downstream."""
    if not path.is_file():
        raise FileNotFoundError(path)
    rows, seen = [], set()
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank candidate line {line_number}")
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid candidate JSON at line {line_number}") from error
            if not isinstance(raw, dict) or any(field not in raw for field in REQUIRED_FIELDS):
                raise ValueError(f"candidate line {line_number} misses required fields")
            if (not isinstance(raw["id"], str) or not raw["id"] or
                    not isinstance(raw["source"], str) or not raw["source"] or
                    not isinstance(raw["question"], str) or not raw["question"].strip() or
                    not isinstance(raw["answer"], str) or not raw["answer"].strip() or
                    not isinstance(raw["answer_type"], str) or not raw["answer_type"]):
                raise ValueError(f"malformed candidate line {line_number}")
            if raw["id"] in seen:
                raise ValueError(f"duplicate candidate ID: {raw['id']}")
            seen.add(raw["id"])
            # Do not retain raw["answer"] after schema validation.
            rows.append({"id": raw["id"], "source": raw["source"],
                         "question": raw["question"], "answer_type": raw["answer_type"],
                         "line": line_number})
    if not rows:
        raise ValueError(f"empty candidate JSONL: {path}")
    return rows


def run_settings(model_path: str, candidates_path: Path, mode: str, max_new_tokens: int, seed: int,
                 rows: list[dict]) -> dict:
    return {
        "script": Path(__file__).name,
        "model_path": str(Path(model_path).resolve()),
        "candidates_path": str(candidates_path.resolve()),
        "mode": mode,
        "seed": seed,
        "generation": {**SAMPLING[mode], "max_new_tokens": max_new_tokens},
        # Question is retained to fail closed if a resume points to changed input.
        # Gold answers deliberately never appear in metadata.
        "candidates": [{key: row[key] for key in ("id", "source", "question", "answer_type", "line")}
                       for row in rows],
    }


def prompt_for(tokenizer, question: str, thinking: bool) -> str:
    return tokenizer.apply_chat_template(
        [{"role": "user", "content": HEADER + question}],
        add_generation_prompt=True,
        tokenize=False,
        enable_thinking=thinking,
    )


def prompt_provenance(settings: dict, row: dict) -> dict:
    return {
        "candidate_path": settings["candidates_path"],
        "candidate_line": row["line"],
        "template": PROMPT_TEMPLATE,
        "chat_template": "tokenizer.apply_chat_template",
        "thinking": settings["mode"] == "thinking",
    }


def prepare_resume(output_path: Path, settings: dict) -> set[str]:
    """Check immutable run metadata and return already completed candidate IDs."""
    meta_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    if meta_path.exists():
        try:
            existing = json.loads(meta_path.read_text())
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid run metadata: {meta_path}") from error
        if existing != settings:
            raise ValueError("run settings changed during resume")
    elif output_path.exists() and output_path.stat().st_size:
        raise ValueError("output exists without run metadata")
    else:
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with meta_path.open("w") as handle:
            json.dump(settings, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

    selected = {row["id"]: row for row in settings["candidates"]}
    done = set()
    if not output_path.exists():
        return done
    with output_path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank output line {line_number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid output JSON at line {line_number}") from error
            identifier = record.get("id")
            candidate = selected.get(identifier)
            required = ("id", "source", "answer_type", "seed", "model_path", "mode", "prompt",
                        "prompt_provenance", "output", "tokens", "truncated", "generation")
            if (candidate is None or identifier in done or any(key not in record for key in required) or
                    record["source"] != candidate["source"] or
                    record["answer_type"] != candidate["answer_type"] or
                    record["seed"] != settings["seed"] or
                    record["model_path"] != settings["model_path"] or
                    record["mode"] != settings["mode"] or
                    record["prompt_provenance"] != prompt_provenance(settings, candidate) or
                    record["generation"] != settings["generation"] or
                    not isinstance(record["prompt"], str) or not isinstance(record["output"], str) or
                    not isinstance(record["tokens"], int) or record["tokens"] < 0 or
                    not isinstance(record["truncated"], bool)):
                raise ValueError(f"inconsistent resumed output at line {line_number}")
            done.add(identifier)
    return done


def write_record(handle, record: dict) -> None:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    handle.flush()
    os.fsync(handle.fileno())


def generate(model, tokenizer, prompt: str, settings: dict) -> tuple[str, int, bool]:
    import torch

    encoded = tokenizer(prompt, return_tensors="pt")
    encoded = {key: value.to("cuda") for key, value in encoded.items()}
    torch.manual_seed(settings["seed"])
    torch.cuda.manual_seed_all(settings["seed"])
    with torch.inference_mode():
        result = model.generate(
            **encoded,
            do_sample=True,
            **settings["generation"],
            pad_token_id=tokenizer.eos_token_id,
        )
    continuation = result[0, encoded["input_ids"].shape[1]:].tolist()
    eos = tokenizer.eos_token_id
    return (tokenizer.decode(continuation, skip_special_tokens=False), len(continuation),
            len(continuation) >= settings["generation"]["max_new_tokens"] and eos not in continuation)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", help="local post-trained Qwen3-4B model directory")
    parser.add_argument("candidates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("mode", choices=tuple(SAMPLING))
    parser.add_argument("--max-new-tokens", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.max_new_tokens < 1:
        parser.error("--max-new-tokens must be positive")
    return args


def main():
    args = parse_args()
    rows = read_candidates(args.candidates)
    settings = run_settings(args.model, args.candidates, args.mode, args.max_new_tokens, args.seed, rows)
    done = prepare_resume(args.output, settings)
    pending = [row for row in rows if row["id"] not in done]
    if not pending:
        print("all requested candidate results already present", flush=True)
        return

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for native Qwen3-4B generation")
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.eos_token_id is None:
        raise ValueError("model tokenizer lacks eos_token_id")
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, attn_implementation="sdpa", local_files_only=True,
    ).to("cuda").eval()
    if getattr(model.config, "model_type", None) != "qwen3":
        raise ValueError(f"expected Qwen3 model, found {getattr(model.config, 'model_type', None)!r}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a") as handle:
        for number, row in enumerate(pending, 1):
            prompt = prompt_for(tokenizer, row["question"], args.mode == "thinking")
            output, tokens, truncated = generate(model, tokenizer, prompt, settings)
            record = {
                "id": row["id"], "source": row["source"], "answer_type": row["answer_type"],
                "seed": args.seed, "model_path": settings["model_path"], "mode": args.mode,
                "prompt": prompt, "prompt_provenance": prompt_provenance(settings, row),
                "output": output, "tokens": tokens, "truncated": truncated,
                "generation": settings["generation"],
            }
            write_record(handle, record)
            print(json.dumps({"completed": number, "total": len(pending), "id": row["id"],
                              "tokens": tokens, "truncated": truncated}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
