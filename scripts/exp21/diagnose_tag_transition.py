"""Teacher-forced Path-tag probabilities with the SFT mask versus causal decoding.

Usage: PYTHONPATH=<repo>/verl/verl/utils/dataset python diagnose_tag_transition.py MODEL VAL_PARQUET OUT_JSON [LIMIT]
The exact M1 val rows are used; this does not generate or score benchmark answers.
"""
import json
import statistics
import sys

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from multiverse_structure import dense_mask, multiverse_structure


def main():
    model_path, val_path, output_path = sys.argv[1:4]
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else None
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    tags = {key: tokenizer.convert_tokens_to_ids(f"<{key}>") for key in ("Parallel", "Path")}
    tags["/Parallel"] = tokenizer.convert_tokens_to_ids("</Parallel>")
    tags["/Path"] = tokenizer.convert_tokens_to_ids("</Path>")
    conclusion = tokenizer.convert_tokens_to_ids("<Conclusion>")
    assert all(isinstance(v, int) and v >= 0 for v in (*tags.values(), conclusion))
    rows = pd.read_parquet(val_path)
    rows = rows[rows["extra_info"].map(lambda x: x["kind"] == "parallel")]
    rows = rows.drop_duplicates(subset=["id"])
    if limit is not None:
        rows = rows.head(limit)
    results = []
    for _, row in rows.iterrows():
        info = row["extra_info"]
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": info["question"]}], add_generation_prompt=True,
            tokenize=False, enable_thinking=False)
        prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
        response_ids = tokenizer.encode(info["answer"] + tokenizer.eos_token, add_special_tokens=False)
        positions, groups = multiverse_structure(response_ids, tags)
        path_indices = [i for i, token in enumerate(response_ids) if token == tags["Path"]]
        assert len(path_indices) >= 2 and groups, info["id"]
        targets = [("path_first", path_indices[0]), ("path_second", path_indices[1])]
        target_conclusion = next((i for i, token in enumerate(response_ids) if token == conclusion), None)
        if target_conclusion is not None:
            targets.append(("conclusion", target_conclusion))

        ids = torch.tensor([prompt_ids + response_ids], device="cuda")
        n, p = ids.shape[1], len(prompt_ids)
        mask = torch.ones(n, n, dtype=torch.bool, device="cuda").tril_()
        mask[p:, p:] = dense_mask(len(response_ids), groups, device="cuda")
        additive = torch.zeros(1, 1, n, n, dtype=torch.bfloat16, device="cuda")
        additive.masked_fill_(~mask[None, None], torch.finfo(torch.bfloat16).min)
        pos = torch.tensor([list(range(p)) + [p + x for x in positions]], device="cuda")
        with torch.inference_mode():
            structured = model(input_ids=ids, attention_mask=additive, position_ids=pos, use_cache=False).logits[0]
            causal = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False).logits[0]
        scores = {}
        for name, response_index in targets:
            index = p + response_index
            token = ids[0, index].item()
            scores[name] = {}
            for label, logits in (("structured", structured), ("causal", causal)):
                vector = logits[index - 1].float()
                score = vector[token]
                scores[name][label] = {
                    "prob": round(torch.softmax(vector, -1)[token].item(), 6),
                    "rank": int((vector > score).sum().item() + 1),
                    "top1": tokenizer.decode([int(vector.argmax().item())]),
                }
        results.append({"id": info["id"], "path_count": len(path_indices), "tokens": n, "scores": scores})
        print(info["id"], len(results), "/", len(rows), scores["path_second"], flush=True)
        del structured, causal, additive, mask, ids
    summary = {}
    for target in ("path_first", "path_second", "conclusion"):
        pairs = [r["scores"][target] for r in results if target in r["scores"]]
        summary[target] = {mode: {"n": len(pairs),
                                  "median_prob": round(statistics.median(p[mode]["prob"] for p in pairs), 6),
                                  "top1_rate": round(sum(p[mode]["rank"] == 1 for p in pairs) / len(pairs), 4)}
                           for mode in ("structured", "causal")}
    with open(output_path, "w") as file:
        json.dump({"summary": summary, "rows": results}, file, ensure_ascii=False, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
