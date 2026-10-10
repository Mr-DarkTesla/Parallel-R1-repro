"""Recheck selected no-block examples, answers, split and SFT length."""
import collections
import json
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

from checks import candidate, correct


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results/21-qwen3-0.6b-multiverse/data"
BASE = DATA / "sft_expanded_th_m1_twopath_replay3_tagged"
SELECTIVE = DATA / "sft_selective_blocks_m1_text1"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"


def load(path):
    return {r["id"]: r for r in map(json.loads, path.open())}


def main():
    base = pd.read_parquet(f"{BASE}_train.parquet")
    train = pd.read_parquet(f"{SELECTIVE}_train.parquet")
    old_val = pd.read_parquet(f"{BASE}_val.parquet")
    val = pd.read_parquet(f"{SELECTIVE}_val.parquet")
    plan = json.loads((DATA / "sft_selective_blocks_m1_text1_audit.json").read_text())
    pool, replay = load(DATA / "pool.jsonl"), load(DATA / "replay_th.jsonl")
    selected = set(plan["new_math_no_block_ids"] + plan["converted_arc_replay_ids"])
    assert len(base) == len(train) == 2748 and len(val) == 63 and old_val.equals(val)
    assert not selected & set(val.id)
    assert collections.Counter(base.source) == collections.Counter(train.source)
    assert len(selected) == 38
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
    lengths = {}
    for id_ in selected:
        reference = pool[id_]
        own = replay[id_]
        assert own["question"] == reference["question"]
        assert own["response"].count("<think>") == own["response"].count("</think>") == 1
        assert own["response"].startswith("<think>")
        assert all(tag not in own["response"] for tag in ("<Parallel>", "<Goal>", "<Path>"))
        final = own["response"].split("</think>", 1)[1]
        assert correct(reference["answer"], candidate(final), reference["source"]), id_
        rows = [r["extra_info"] for r in train.to_dict("records")
                if r["id"] == id_ and r["extra_info"]["kind"] == "control_th"]
        assert len(rows) == (6 if id_.startswith("math-") else 3), id_
        assert all(info["answer"] == own["response"] for info in rows), id_
        info = rows[0]
        assert all(info["question"] == other["question"] and other["enable_thinking"] for other in rows)
        prompt = tokenizer.apply_chat_template([{"role": "user", "content": info["question"]}],
                                               add_generation_prompt=True, tokenize=False,
                                               enable_thinking=True)
        length = len(tokenizer.encode(prompt + info["answer"] + tokenizer.eos_token,
                                      add_special_tokens=False))
        assert length <= 4096, (id_, length)
        lengths[id_] = length
    result = {"selected_distinct": len(selected), "answers_correct": len(selected),
              "max_training_tokens": max(lengths.values()), "over_limit": 0,
              "train_rows": len(train), "val_rows": len(val), "val_identical": True,
              "leakcheck": "All 38 questions exactly match the previously leakchecked pool; DATASET_POOL.md.",
              "lengths": lengths}
    (DATA / "sft_selective_blocks_m1_text1_quality.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "lengths"}))


if __name__ == "__main__":
    main()
