"""Variant C: token-level checks of converted samples with the real Qwen3 tokenizer (run where torch/transformers exist, e.g. pod B).

For every sample: the 6 Multiverse tags + 6 Parallel-R1 tags are single tokens; the nested structure parses
(multiverse_structure.py, the same code the SFT dataset uses with structure=multiverse); the dense mask builds; sibling paths are
mutually invisible in it; prompt+response length <= max length. Also reports the same for Multiverse-1K traces if given.
Usage: python check_mask.py <tokenizer_dir> <converted.jsonl> <out.json> [--multiverse1k path] [--max-len 16384]
converted.jsonl rows: key, prompt (user text), response (full assistant text with <think>..</think>answer).
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../verl/verl/utils/dataset"))
from multiverse_structure import StructureError, dense_mask, multiverse_structure  # noqa: E402

NEW_TAGS = ["<Goal>", "</Goal>", "<Outline>", "</Outline>", "<Conclusion>", "</Conclusion>"]
OLD_TAGS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]


def load_tokenizer(path):
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(path)
    missing = [t for t in OLD_TAGS + NEW_TAGS if t not in tok.get_vocab()]
    if missing:
        tok.add_special_tokens({"additional_special_tokens": tok.additional_special_tokens + missing})
    ids = {t: tok.convert_tokens_to_ids(t) for t in OLD_TAGS + NEW_TAGS}
    for t in OLD_TAGS + NEW_TAGS:
        assert tok.encode(t, add_special_tokens=False) == [ids[t]], t
    return tok, ids, missing


def check(tok, ids, prompt, response, max_len, mask_check=True):
    tags = {"Parallel": ids["<Parallel>"], "/Parallel": ids["</Parallel>"], "Path": ids["<Path>"], "/Path": ids["</Path>"]}
    p = tok.apply_chat_template([{"role": "user", "content": prompt}], add_generation_prompt=True, tokenize=False,
                                enable_thinking=True)
    p_ids = tok(p, add_special_tokens=False)["input_ids"]
    r_ids = tok(response + tok.eos_token, add_special_tokens=False)["input_ids"]
    out = {"prompt_tokens": len(p_ids), "response_tokens": len(r_ids), "fits": len(p_ids) + len(r_ids) <= max_len}
    try:
        pos, groups = multiverse_structure(r_ids, tags)
    except StructureError as e:
        return {**out, "ok": False, "error": str(e)}
    out.update({"blocks": len(groups), "paths": [len(g) for g in groups],
                "parallel_saving": round(1 - (pos[-1] + 1) / len(r_ids), 3) if r_ids else 0})
    if mask_check:
        m = dense_mask(len(r_ids), groups)
        bad = 0
        for spans in groups:
            for a, (s1, e1) in enumerate(spans):
                for s2, e2 in spans[a + 1:]:
                    bad += int(m[s2:e2, s1:e1].any())
        out["mask_leaks"] = bad
    out["ok"] = out.get("mask_leaks", 0) == 0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tokenizer")
    ap.add_argument("converted")
    ap.add_argument("out")
    ap.add_argument("--multiverse1k", default="")
    ap.add_argument("--max-len", type=int, default=16384)
    args = ap.parse_args()
    tok, ids, missing = load_tokenizer(args.tokenizer)
    res = {"tag_ids": ids, "added_in_memory": missing, "samples": {}}
    for line in open(args.converted):
        r = json.loads(line)
        res["samples"][r["key"]] = check(tok, ids, r["prompt"], r["response"], args.max_len)
    if args.multiverse1k:
        stats, lens = collections.Counter(), []
        for r in json.load(open(args.multiverse1k)):
            resp = "<think>\n" + r["deepseek_thinking_trajectory_parallel"] + "\n</think>\n\n" + r["deepseek_attempt"]
            c = check(tok, ids, r["question"], resp, args.max_len, mask_check=False)
            stats["ok" if c["ok"] else "structure_error"] += 1
            stats["fits_16k"] += c["fits"]
            lens.append(c["prompt_tokens"] + c["response_tokens"])
        lens.sort()
        res["multiverse1k"] = {**stats, "tokens_p50_p90_max": [lens[len(lens) // 2], lens[int(.9 * len(lens))], lens[-1]]}
    json.dump(res, open(args.out, "w"), indent=1)
    s = res["samples"]
    print(json.dumps({"samples": len(s), "ok": sum(v["ok"] for v in s.values()), "fits": sum(v["fits"] for v in s.values()),
                      "multiverse1k": res.get("multiverse1k"), "added_in_memory": missing}, indent=1))


if __name__ == "__main__":
    main()
