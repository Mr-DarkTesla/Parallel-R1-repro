"""Read-only embedding-row audit for the Opus consultation."""

import json
import sys
from pathlib import Path

import torch
from safetensors import safe_open
from transformers import AutoConfig, AutoTokenizer


TAGS = ["<Parallel>", "</Parallel>", "<Goal>", "</Goal>", "<Outline>",
        "</Outline>", "<Path>", "</Path>", "<Conclusion>", "</Conclusion>"]


def embeddings(path):
    with safe_open(str(Path(path) / "model.safetensors"), framework="pt", device="cpu") as f:
        return f.get_tensor("model.embed_tokens.weight").float()


def audit(base_path, model_paths):
    tok = AutoTokenizer.from_pretrained(base_path)
    ids = [tok.convert_tokens_to_ids(t) for t in TAGS]
    assert all(tok.encode(t, add_special_tokens=False) == [i] for t, i in zip(TAGS, ids))
    base = embeddings(base_path)
    old_vocab = min(ids)
    # Sample the pre-existing vocabulary deterministically, omitting padded rows.
    old = torch.linspace(0, old_vocab - 1, steps=min(old_vocab, 10000)).long().unique()
    base_old = base[old]
    out = {"base": base_path, "tag_ids": dict(zip(TAGS, ids)), "models": {}}
    for path in model_paths:
        current = embeddings(path)
        assert current.shape == base.shape
        old_norms = torch.linalg.vector_norm(current[old], dim=1)
        tag_norms = torch.linalg.vector_norm(current[ids], dim=1)
        drift = torch.linalg.vector_norm(current[old] - base_old, dim=1)
        tag_drift = torch.linalg.vector_norm(current[ids] - base[ids], dim=1)
        cfg = AutoConfig.from_pretrained(path)
        out["models"][Path(path).name + ":" + str(Path(path).parent)] = {
            "model": path,
            "tied_config": bool(cfg.tie_word_embeddings),
            "old_norm_p50": round(float(old_norms.median()), 5),
            "old_norm_p99": round(float(torch.quantile(old_norms, 0.99)), 5),
            "old_drift_p50": round(float(drift.median()), 5),
            "old_drift_p99": round(float(torch.quantile(drift, 0.99)), 5),
            "tag_norms": {t: round(float(v), 5) for t, v in zip(TAGS, tag_norms)},
            "tag_drift": {t: round(float(v), 5) for t, v in zip(TAGS, tag_drift)},
            "sampled_old_rows": len(old),
        }
        del current
    return out


if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1], sys.argv[2:]), ensure_ascii=False, indent=2))
