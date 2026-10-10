"""Read-only check of rendered SFT lengths and supervision of structure tokens."""

import json
import sys
from collections import Counter

import pandas as pd
from transformers import AutoTokenizer


TAGS = ["<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>",
        "</Outline>", "<Path>", "</Path>", "<Conclusion>", "</Conclusion>"]


def audit(model, paths):
    tok = AutoTokenizer.from_pretrained(model)
    tags = {t: tok.convert_tokens_to_ids(t) for t in TAGS}
    assert all(tok.encode(t, add_special_tokens=False) == [i] for t, i in tags.items())
    out = {"model": model, "tag_ids": tags, "files": {}}
    for path in paths:
        data = pd.read_parquet(path)
        lengths = []
        kinds = Counter()
        tag_targets = Counter()
        masked_targets = Counter()
        think_prompt_suffixes = Counter()
        for row in data.extra_info:
            mode = bool(row["enable_thinking"])
            kinds[row.get("kind", "unknown")] += 1
            prompt = tok.apply_chat_template([{"role": "user", "content": row["question"]}],
                                             add_generation_prompt=True, tokenize=False,
                                             enable_thinking=mode)
            think_prompt_suffixes["thinking" if mode else "no_thinking"] = prompt[-50:]
            pids = tok.encode(prompt, add_special_tokens=False)
            rids = tok.encode(row["answer"] + tok.eos_token, add_special_tokens=False)
            lengths.append(len(pids) + len(rids))
            # The actual trainer predicts target input_ids[j] from logits[j-1] and
            # uses loss_mask[j-1]. The prompt before its last token is masked.
            for tag, tid in tags.items():
                for r in (i for i, token in enumerate(rids) if token == tid):
                    tag_targets[tag] += 1
                    target_mask_index = len(pids) + r - 1
                    if target_mask_index < len(pids) - 1:
                        masked_targets[tag] += 1
            if rids[-1] != tok.eos_token_id:
                raise AssertionError("response must end with EOS")
        out["files"][path] = {
            "rows": len(data), "kinds": kinds, "max_tokens": max(lengths),
            "over_4096": sum(n > 4096 for n in lengths),
            "token_length_p50": int(pd.Series(lengths).median()),
            "tag_target_counts": tag_targets, "masked_tag_target_counts": masked_targets,
            "prompt_suffixes": think_prompt_suffixes,
        }
    return out


if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1], sys.argv[2:]), ensure_ascii=False, indent=2))
