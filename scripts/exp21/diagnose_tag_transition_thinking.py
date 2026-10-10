"""Measure gold tag probabilities under the SFT mask and a causal mask.

Usage: python diagnose_tag_transition_thinking.py MODEL VAL_PARQUET OUT_JSON
"""

import json
import statistics
import sys
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from verl.utils.dataset.multiverse_structure import dense_mask, multiverse_structure


@torch.inference_mode()
def main():
    model_path, val_path, out_path = sys.argv[1:4]
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to("cuda").eval()
    names = ("Parallel", "/Parallel", "Path", "/Path", "Conclusion")
    tags = {name: tokenizer.convert_tokens_to_ids(f"<{name}>") for name in names}
    rows = {info["id"]: info for info in pd.read_parquet(val_path).extra_info
            if info.get("kind") == "parallel_th"}
    results = []
    for info in rows.values():
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": info["question"]}],
            add_generation_prompt=True, tokenize=False, enable_thinking=True)
        prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
        response_ids = tokenizer.encode(info["answer"] + tokenizer.eos_token, add_special_tokens=False)
        positions, groups = multiverse_structure(response_ids, tags)
        p, n = len(prompt_ids), len(response_ids)
        ids = torch.tensor([prompt_ids + response_ids], device="cuda")
        mask = torch.ones(p + n, p + n, dtype=torch.bool, device="cuda").tril_()
        mask[p:, p:] = dense_mask(n, groups, device="cuda")
        additive = torch.zeros(1, 1, p + n, p + n, dtype=model.dtype, device="cuda")
        additive.masked_fill_(~mask[None, None], torch.finfo(model.dtype).min)
        causal = torch.zeros_like(additive).masked_fill_(
            ~torch.ones(p + n, p + n, dtype=torch.bool, device="cuda").tril_()[None, None],
            torch.finfo(model.dtype).min)
        pos = torch.tensor([list(range(p)) + [p + x for x in positions]], device="cuda")
        structured = model(input_ids=ids, attention_mask=additive,
                           position_ids=pos, use_cache=False).logits[0]
        sequential = model(input_ids=ids, attention_mask=causal,
                           position_ids=pos, use_cache=False).logits[0]
        selected = []
        path_open = path_close = 0
        for i, token in enumerate(response_ids):
            if token == tags["Path"]:
                path_open += 1
                label = "path_first" if path_open == 1 else "path_later"
            elif token == tags["/Path"]:
                path_close += 1
                label = "path_close"
            elif token == tags["Conclusion"]:
                label = "conclusion"
            elif token == tags["/Parallel"]:
                label = "parallel_close"
            else:
                continue
            scores = {}
            for mode, logits in (("structured", structured), ("causal", sequential)):
                vector = logits[p + i - 1].float()
                scores[mode] = {
                    "prob": float(vector.softmax(-1)[token]),
                    "rank": int((vector > vector[token]).sum() + 1),
                    "top1": tokenizer.decode([int(vector.argmax())], skip_special_tokens=False),
                }
            selected.append({"label": label, "response_token_index": i, "scores": scores})
        results.append({"id": info["id"], "path_count": path_open,
                        "response_tokens": n, "targets": selected})
        print(info["id"], len(results), "/", len(rows), flush=True)
    summary = {}
    for label in ("path_first", "path_later", "path_close", "conclusion", "parallel_close"):
        for mode in ("structured", "causal"):
            scores = [target["scores"][mode] for row in results for target in row["targets"]
                      if target["label"] == label]
            summary.setdefault(label, {})[mode] = {
                "n": len(scores),
                "median_prob": statistics.median(score["prob"] for score in scores),
                "top1_rate": sum(score["rank"] == 1 for score in scores) / len(scores),
            }
    result = {"model": model_path, "validation": val_path, "summary": summary, "rows": results}
    Path(out_path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
