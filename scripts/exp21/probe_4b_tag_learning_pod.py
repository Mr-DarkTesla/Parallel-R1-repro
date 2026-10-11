#!/usr/bin/env python3
"""Teacher-forced tag NLL and root-tag rank on held-out Qwen4B-34 traces."""
import json
import sys
from collections import defaultdict
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from verl.utils.dataset.multiverse_structure import dense_mask, multiverse_structure


TAGS = ("<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>",
        "</Outline>", "<Path>", "</Path>", "<Conclusion>", "</Conclusion>")


@torch.inference_mode()
def main():
    model_path, data_path, output_path = sys.argv[1:4]
    rows = [json.loads(s) for s in Path(data_path).read_text().splitlines() if s.strip()]
    assert len(rows) == 34
    tok = AutoTokenizer.from_pretrained(model_path)
    token_ids = {tag: tok.convert_tokens_to_ids(tag) for tag in TAGS}
    assert all(tok.encode(tag, add_special_tokens=False) == [idx]
               for tag, idx in token_ids.items())
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda").eval()
    embeddings = model.get_input_embeddings().weight
    norms = torch.linalg.vector_norm(embeddings.float(), dim=1)
    result = {"model": model_path, "data": data_path, "count": len(rows),
              "tag_norms": {tag: round(float(norms[idx]), 6) for tag, idx in token_ids.items()},
              "vocabulary_norm_median": round(float(norms.median()), 6), "rows": []}
    per_tag = defaultdict(list)
    other_losses = []
    structures = {"Parallel": token_ids["<Parallel>"], "/Parallel": token_ids["</Parallel>"],
                  "Path": token_ids["<Path>"], "/Path": token_ids["</Path>"]}
    tag_by_id = {value: key for key, value in token_ids.items()}
    for row in rows:
        prompt = tok.apply_chat_template([{"role": "user", "content": row["prompt"]}],
                                         add_generation_prompt=True, tokenize=False, enable_thinking=True)
        pids = tok.encode(prompt, add_special_tokens=False)
        rids = tok.encode(row["response"] + tok.eos_token, add_special_tokens=False)
        positions, groups = multiverse_structure(rids, structures)
        assert len(groups) == 1 and len(groups[0]) == 2
        P, R, total = len(pids), len(rids), len(pids) + len(rids)
        ids = torch.tensor([pids + rids], device="cuda")
        pos = torch.tensor([list(range(P)) + [P + p for p in positions]], device="cuda")
        visible = torch.ones(total, total, dtype=torch.bool).tril_()
        visible[P:, P:] = dense_mask(R, groups, device="cpu")
        mask = torch.zeros(1, 1, total, total, dtype=model.dtype, device="cuda")
        mask.masked_fill_(~visible.to("cuda")[None, None], torch.finfo(model.dtype).min)
        logits = model(input_ids=ids, attention_mask=mask, position_ids=pos,
                       use_cache=False).logits[0, P - 1:total - 1].float()
        target = torch.tensor(rids, device="cuda")
        logp = logits.gather(1, target[:, None]).flatten() - torch.logsumexp(logits, dim=1)
        root = rids.index(token_ids["<Parallel>"])
        root_rank = int((logits[root] > logits[root, token_ids["<Parallel>"]]).sum()) + 1
        root_p = float(logp[root].exp())
        for index, token in enumerate(rids):
            if token in tag_by_id:
                per_tag[tag_by_id[token]].append(-float(logp[index]))
            else:
                other_losses.append(-float(logp[index]))
        result["rows"].append({"id": row["id"], "root_probability": root_p,
                               "root_rank": root_rank, "root_top5": root_rank <= 5,
                               "root_top1": root_rank == 1})
        del logits, logp, ids, pos, mask
    result["summary"] = {
        "root_probability_mean": sum(r["root_probability"] for r in result["rows"]) / len(rows),
        "root_top1": sum(r["root_top1"] for r in result["rows"]),
        "root_top5": sum(r["root_top5"] for r in result["rows"]),
        "tag_nll": {tag: {"count": len(values), "mean": sum(values) / len(values)}
                    for tag, values in per_tag.items()},
        "other_text_nll_mean": sum(other_losses) / len(other_losses),
    }
    Path(output_path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
