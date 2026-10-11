"""Sample fresh on-policy Multiverse answers with SFT-matched sibling masking.

The candidate JSONL may retain gold answers for later grading, but this script
never reads them into a prompt or an output row.  Each response token is fed
back through ``MaskedDecodeState`` so later sibling Paths cannot attend to
earlier ones and use the same RoPE positions as SFT.

Example (run on the prepared GPU pod, not locally):
  python scripts/exp21/generate_onpolicy_masked.py \
    /checkpoints/exp21-v4-recovery8/step_8/model \
    results/21-qwen3-0.6b-multiverse/data/onpolicy46_candidates.jsonl \
    /work/exp21/onpolicy46/recovery8_step8.jsonl \
    --math-count 23 --gsm-count 23 --seeds 0
"""

import argparse
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_mv_prompts import mv_prompt
from masked_decode_state import MaskedDecodeState, path_count


HEADER = ("Solve the following problem step by step.\n"
          "End your response with a line starting with Final Answer: followed by the final result.\n\nProblem: ")
MAX_NEW_TOKENS = {"math": 4096, "gsm8k": 2048}
REQUIRED_FIELDS = ("id", "source", "question", "answer", "answer_type")


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).split())


def read_candidates(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    rows, ids, questions = [], set(), set()
    with path.open() as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"blank candidate line {number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid candidate JSON at line {number}") from error
            if not isinstance(row, dict) or any(field not in row for field in REQUIRED_FIELDS):
                raise ValueError(f"candidate line {number} misses required fields")
            if (not isinstance(row["id"], str) or not row["id"] or
                    row["source"] not in MAX_NEW_TOKENS or
                    not isinstance(row["question"], str) or not normalize(row["question"]) or
                    not isinstance(row["answer"], str) or not row["answer"].strip() or
                    not isinstance(row["answer_type"], str) or not row["answer_type"]):
                raise ValueError(f"malformed candidate line {number}")
            question = normalize(row["question"])
            if row["id"] in ids:
                raise ValueError(f"duplicate candidate ID: {row['id']}")
            if question in questions:
                raise ValueError(f"duplicate normalized candidate question at line {number}")
            ids.add(row["id"])
            questions.add(question)
            rows.append(row)
    if not rows:
        raise ValueError(f"empty candidate JSONL: {path}")
    return rows


def select_candidates(rows, math_count, gsm_count):
    counts = {"math": math_count, "gsm8k": gsm_count}
    selected = {source: [] for source in counts}
    for row in rows:  # Candidate-file order is the deterministic source order.
        source = row["source"]
        if len(selected[source]) < counts[source]:
            selected[source].append(row)
    if any(len(selected[source]) != count for source, count in counts.items()):
        have = {source: len(selected[source]) for source in counts}
        raise ValueError(f"candidate file cannot satisfy requested source counts: {have}")
    return [row for row in rows if row in selected[row["source"]]]


def parse_seeds(values):
    try:
        seeds = [int(item) for value in values for item in value.split(",") if item]
    except ValueError as error:
        raise argparse.ArgumentTypeError("--seeds values must be integers") from error
    if not seeds or len(set(seeds)) != len(seeds):
        raise argparse.ArgumentTypeError("--seeds must be a nonempty list without duplicates")
    return seeds


def sampled_token(logits, generator, temperature, top_p, top_k):
    import torch

    logits = logits / temperature
    if top_k:
        cutoff = torch.topk(logits, top_k).values[-1]
        logits = logits.masked_fill(logits < cutoff, -torch.inf)
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative = torch.softmax(sorted_logits, dim=-1).cumsum(dim=-1)
    remove = cumulative > top_p
    remove[1:] = remove[:-1].clone()
    remove[0] = False
    logits = logits.scatter(0, sorted_indices, sorted_logits.masked_fill(remove, -torch.inf))
    return torch.multinomial(torch.softmax(logits, dim=-1), 1, generator=generator).item()


def generate(model, tokenizer, prompt, max_new_tokens, seed, path_open, path_close, settings):
    import torch

    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if not prompt_ids:
        raise ValueError("empty rendered prompt")
    state = MaskedDecodeState(path_open, path_close)
    generator = torch.Generator(device="cuda").manual_seed(seed)
    response, eos = [], False
    with torch.inference_mode():
        output = model(input_ids=torch.tensor([prompt_ids], device="cuda"), use_cache=True)
        past, logits = output.past_key_values, output.logits[0, -1].float()
        for step in range(max_new_tokens):
            token = sampled_token(logits, generator, settings["temperature"], settings["top_p"], settings["top_k"])
            if token == tokenizer.eos_token_id:
                eos = True
                break
            if token == path_open and state.phase == "plain":
                # A malformed Goal remains sequential; valid sibling blocks use their
                # actual outline count and therefore the exact SFT visibility rule.
                state.expected_paths = path_count(tokenizer.decode(response, skip_special_tokens=False)) or 1
            position, visible = state.append(token)
            response.append(token)
            rowmask = torch.zeros(1, 1, 1, len(prompt_ids) + len(response),
                                  dtype=torch.bfloat16, device="cuda")
            rowmask[..., len(prompt_ids):].masked_fill_(
                ~torch.tensor(visible, device="cuda"), torch.finfo(torch.bfloat16).min)
            output = model(
                input_ids=torch.tensor([[token]], device="cuda"),
                past_key_values=past,
                attention_mask=rowmask,
                position_ids=torch.tensor([[len(prompt_ids) + position]], device="cuda"),
                cache_position=torch.tensor([len(prompt_ids) + step], device="cuda"),
                use_cache=True,
            )
            past, logits = output.past_key_values, output.logits[0, -1].float()
    # Token decisions include EOS. Forward passes are prompt prefill plus one
    # continuation forward pass per non-EOS emitted token.
    return {
        "output": tokenizer.decode(response, skip_special_tokens=False),
        "tokens": len(response) + int(eos),
        "forward_calls": 1 + len(response),
        "truncated": not eos,
    }


def candidate_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_settings(args, candidates, seeds):
    return {
        "decoder": "masked-autonomous-v2",
        "model": args.model,
        "candidates": str(args.candidates.resolve()),
        "candidate_sha256": candidate_digest(args.candidates),
        "selection": [{key: row[key] for key in ("id", "source", "answer_type")} for row in candidates],
        "math_count": args.math_count,
        "gsm_count": args.gsm_count,
        "seeds": seeds,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "max_new_tokens": {"math": args.math_max_new_tokens, "gsm8k": args.gsm_max_new_tokens},
        "thinking": True,
    }


def row_settings(settings, source):
    return {
        "decoder": settings["decoder"],
        "thinking": True,
        "temperature": settings["temperature"],
        "top_p": settings["top_p"],
        "top_k": settings["top_k"],
        "max_new_tokens": settings["max_new_tokens"][source],
    }


def prepare_resume(output_path, meta_path, settings):
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
        meta_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n")

    selected = {(row["id"], row["source"], row["answer_type"]) for row in settings["selection"]}
    requested = {(row["id"], seed) for row in settings["selection"] for seed in settings["seeds"]}
    done = set()
    if output_path.exists():
        with output_path.open() as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    raise ValueError(f"blank output line {number}")
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"invalid output JSON at line {number}") from error
                key = (row.get("id"), row.get("seed"))
                if ((row.get("id"), row.get("source"), row.get("answer_type")) not in selected or
                        key not in requested or key in done):
                    raise ValueError(f"inconsistent resumed output at line {number}")
                required = ("output", "tokens", "forward_calls", "truncated", "settings")
                if (any(field not in row for field in required) or
                        not isinstance(row["output"], str) or
                        not isinstance(row["tokens"], int) or
                        not isinstance(row["forward_calls"], int) or
                        not isinstance(row["truncated"], bool) or
                        row["settings"] != row_settings(settings, row["source"])):
                    raise ValueError(f"malformed resumed output at line {number}")
                done.add(key)
    return done


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model")
    parser.add_argument("candidates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--math-count", type=int, default=128)
    parser.add_argument("--gsm-count", type=int, default=128)
    parser.add_argument("--seeds", nargs="+", default=["0"])
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--math-max-new-tokens", type=int, default=MAX_NEW_TOKENS["math"])
    parser.add_argument("--gsm-max-new-tokens", type=int, default=MAX_NEW_TOKENS["gsm8k"])
    parser.add_argument("--thinking", action="store_true", default=True,
                        help="kept for explicit CLI readability; thinking is always enabled")
    args = parser.parse_args()
    if args.math_count < 0 or args.gsm_count < 0 or not (args.math_count + args.gsm_count):
        parser.error("source counts must be nonnegative and total at least one")
    if args.temperature <= 0 or not 0 < args.top_p <= 1 or args.top_k < 0:
        parser.error("require temperature > 0, 0 < top-p <= 1, and top-k >= 0")
    if args.math_max_new_tokens < 1 or args.gsm_max_new_tokens < 1:
        parser.error("max_new_tokens must be positive")
    return args, parse_seeds(args.seeds)


def main():
    args, seeds = parse_args()
    selected = select_candidates(read_candidates(args.candidates), args.math_count, args.gsm_count)
    settings = run_settings(args, selected, seeds)
    meta_path = args.output.with_suffix(args.output.suffix + ".meta.json")
    done = prepare_resume(args.output, meta_path, settings)
    jobs = [(row, seed) for row in selected for seed in seeds if (row["id"], seed) not in done]
    if not jobs:
        print("all requested (id, seed) results already present")
        return

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for masked on-policy rollout")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    path_open, path_close = (tokenizer.convert_tokens_to_ids(tag) for tag in ("<Path>", "</Path>"))
    if (tokenizer.encode("<Path>", add_special_tokens=False) != [path_open] or
            tokenizer.encode("</Path>", add_special_tokens=False) != [path_close]):
        raise ValueError("model tokenizer lacks single-token Path tags")
    if tokenizer.eos_token_id is None:
        raise ValueError("model tokenizer lacks eos_token_id")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a") as handle:
        for row, seed in jobs:
            prompt = mv_prompt(HEADER + row["question"])
            rendered = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}], add_generation_prompt=True,
                tokenize=False, enable_thinking=True)
            result = generate(model, tokenizer, rendered, settings["max_new_tokens"][row["source"]],
                              seed, path_open, path_close, sampling)
            record = {
                "id": row["id"], "source": row["source"], "answer_type": row["answer_type"],
                "seed": seed, "input": rendered, **result,
                "settings": row_settings(settings, row["source"]),
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            print(json.dumps({key: record[key] for key in ("id", "seed", "tokens", "truncated")}), flush=True)


if __name__ == "__main__":
    main()
