"""Compare SFT full forward with the autonomous cached masked decoder on gold val rows."""

import json
import sys
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from masked_decode_state import MaskedDecodeState, path_count
from verl.utils.dataset.multiverse_structure import dense_mask, multiverse_structure


TAGS = ("<Parallel>", "</Parallel>", "<Path>", "</Path>")


@torch.inference_mode()
def check_row(model, tok, row):
    prompt = tok.apply_chat_template([{"role": "user", "content": row["question"]}],
                                     add_generation_prompt=True, tokenize=False,
                                     enable_thinking=True)
    pids = tok.encode(prompt, add_special_tokens=False)
    rids = tok.encode(row["answer"] + tok.eos_token, add_special_tokens=False)
    tags = dict(zip(("Parallel", "/Parallel", "Path", "/Path"),
                    (tok.convert_tokens_to_ids(t) for t in TAGS)))
    positions, groups = multiverse_structure(rids, tags)
    rmask = dense_mask(len(rids), groups, device="cpu")
    state = MaskedDecodeState(tags["Path"], tags["/Path"])
    for i, token in enumerate(rids[:-1]):
        if token == tags["Path"] and state.phase == "plain":
            n = path_count(tok.decode(rids[:i], skip_special_tokens=False))
            assert n >= 2, (row["id"], i, "bad path count")
            state.expected_paths = n
        pos, visible = state.append(token)
        assert pos == positions[i], (row["id"], i, pos, positions[i])
        assert visible == rmask[i, :i + 1].tolist(), (row["id"], i, "mask mismatch")
    assert state.phase == "plain", (row["id"], state.phase)

    P, R, T = len(pids), len(rids), len(pids) + len(rids)
    ids = torch.tensor([pids + rids], device="cuda")
    pos = torch.tensor([list(range(P)) + [P + p for p in positions]], device="cuda")
    bmask = torch.ones(T, T, dtype=torch.bool).tril_()
    bmask[P:, P:] = rmask
    bmask = bmask.to("cuda")
    add = torch.zeros(1, 1, T, T, dtype=model.dtype, device="cuda")
    add.masked_fill_(~bmask[None, None], torch.finfo(model.dtype).min)
    out = model(input_ids=ids, attention_mask=add, position_ids=pos, use_cache=False)
    target = ids[0, P:]
    full = out.logits[0, P - 1:T - 1].float().log_softmax(-1).gather(-1, target[:, None]).flatten()
    causal = torch.zeros_like(add).masked_fill_(~torch.ones(T, T, dtype=torch.bool, device="cuda").tril_()[None, None],
                                                  torch.finfo(model.dtype).min)
    out_causal = model(input_ids=ids, attention_mask=causal, position_ids=pos, use_cache=False)
    causal_lp = out_causal.logits[0, P - 1:T - 1].float().log_softmax(-1).gather(-1, target[:, None]).flatten()
    ordinary_pos = torch.arange(T, device="cuda")[None]
    out_ordinary = model(input_ids=ids, attention_mask=causal, position_ids=ordinary_pos, use_cache=False)
    ordinary_full = out_ordinary.logits[0, P - 1:T - 1].float().log_softmax(-1).gather(-1, target[:, None]).flatten()

    pre = model(input_ids=ids[:, :P], use_cache=True)
    past, logits = pre.past_key_values, pre.logits[0, -1].float()
    step_lps = []
    state = MaskedDecodeState(tags["Path"], tags["/Path"])
    for i, token in enumerate(rids):
        step_lps.append(logits.log_softmax(-1)[token])
        if token == tok.eos_token_id:
            break
        if token == tags["Path"] and state.phase == "plain":
            state.expected_paths = path_count(tok.decode(rids[:i], skip_special_tokens=False))
        step_pos, visible = state.append(token)
        rowmask = torch.zeros(1, 1, 1, P + i + 1, dtype=model.dtype, device="cuda")
        rowmask[..., P:].masked_fill_(~torch.tensor(visible, device="cuda"), torch.finfo(model.dtype).min)
        nxt = model(input_ids=torch.tensor([[token]], device="cuda"), past_key_values=past,
                    attention_mask=rowmask,
                    position_ids=torch.tensor([[P + step_pos]], device="cuda"),
                    cache_position=torch.tensor([P + i], device="cuda"), use_cache=True)
        past, logits = nxt.past_key_values, nxt.logits[0, -1].float()
    step = torch.stack(step_lps)
    assert len(step) == R
    ordinary = model(input_ids=ids[:, :P], use_cache=True)
    ordinary_past, ordinary_logits = ordinary.past_key_values, ordinary.logits[0, -1].float()
    ordinary_lps = []
    for i, token in enumerate(rids):
        ordinary_lps.append(ordinary_logits.log_softmax(-1)[token])
        if token == tok.eos_token_id:
            break
        nxt = model(input_ids=torch.tensor([[token]], device="cuda"), past_key_values=ordinary_past,
                    position_ids=torch.tensor([[P + i]], device="cuda"),
                    cache_position=torch.tensor([P + i], device="cuda"), use_cache=True)
        ordinary_past, ordinary_logits = nxt.past_key_values, nxt.logits[0, -1].float()
    ordinary_step = torch.stack(ordinary_lps)
    diff = (full - step).abs()
    ordinary_diff = (ordinary_full - ordinary_step).abs()
    effect = (full - causal_lp).abs()
    second = groups[0][1]
    s2, e2 = second
    return {
        "id": row["id"], "prompt_tokens": P, "response_tokens": R,
        "paths": len(groups[0]), "max_logprob_delta": float(diff.max()),
        "p99_logprob_delta": float(torch.quantile(diff, .99)),
        "path2_max_delta": float(diff[s2:e2].max()),
        "ordinary_causal_max_delta": float(ordinary_diff.max()),
        "ordinary_causal_p99_delta": float(torch.quantile(ordinary_diff, .99)),
        "mask_effect_path2_max": float(effect[s2:e2].max()),
        "mask_effect_path2_mean": float(effect[s2:e2].mean()),
        "largest_deltas": [
            {"response_token_index": i, "token": tok.decode([rids[i]], skip_special_tokens=False),
             "delta": round(float(diff[i]), 6)}
            for i in torch.topk(diff, min(8, R)).indices.tolist()
        ],
    }


def main():
    model_path, val_path, output_path = sys.argv[1:4]
    dtype_name = sys.argv[4] if len(sys.argv) > 4 else "bfloat16"
    assert dtype_name in ("bfloat16", "float32")
    dtype = torch.bfloat16 if dtype_name == "bfloat16" else torch.float32
    tok = AutoTokenizer.from_pretrained(model_path)
    df = pd.read_parquet(val_path)
    candidates = [x for x in df.extra_info if x.get("kind") == "parallel_th"]
    candidates.sort(key=lambda x: len(tok.encode(x["answer"], add_special_tokens=False)))
    by_paths = {}
    for row in candidates:
        n = row["answer"].count("<Path>")
        by_paths.setdefault(n, row)
    chosen = [by_paths[n] for n in (2, 3, 4) if n in by_paths]
    assert chosen
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=dtype, attn_implementation="sdpa").to("cuda").eval()
    result = {"model": model_path, "validation": val_path,
              "backend": "sdpa", "dtype": dtype_name, "rows": []}
    for row in chosen:
        result["rows"].append(check_row(model, tok, row))
    Path(output_path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
