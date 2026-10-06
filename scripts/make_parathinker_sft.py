"""ParaThinker SFT data (Leslie04/parathinker-math-6K) as Parallel-R1 SFT examples, mixed with the GSM8K SFT set (exp12).

ParaThinker examples are pre-tokenized: N independent full solutions <thinkK>...</thinkK>, then a template <summary> with the answer.
We keep the two shortest finished solutions whose \\boxed answer equals the summary answer and write one parallel block:
<Parallel><Path>a</Path><Path>b</Path></Parallel>\\n<Summary>Both paths give X.</Summary>\\n\\nFinal Answer: X
Dropped: problems sharing a 13-word span with an eval problem, examples longer than MAX_LENGTH with our chat template.
Usage (from verl/): python ../scripts/make_parathinker_sft.py <parathinker_dir> <our_model_dir> <output.parquet>
  <parathinker_dir> holds train/data-*.arrow of the dataset and the tokenizer files of Leslie04/ParaThinker-1.5B.
"""
import collections
import glob
import re
import sys

import pandas as pd
import pyarrow as pa
from transformers import AutoTokenizer

from tag_validator import validate

DATA = "data_preprocess_scripts/data"
PROMPT_V3 = "adaptive_parallel_thinking_final_with_prompt_v3"
GSM8K_SFT = f"{DATA}/gsm8k/{PROMPT_V3}/sft_all_accuracy_times_parallel_reward/train.parquet"
EVAL = [
    f"{DATA}/APO_combine/{PROMPT_V3}/rl_all_accuracy_reward/test.parquet",
    f"{DATA}/APO_combine/{PROMPT_V3}/rl_all_accuracy_reward/math300_x8.parquet",
    f"{DATA}/limo/test.parquet",
    f"{DATA}/gsm8k/{PROMPT_V3}/rl_all_accuracy_times_parallel_reward/test.parquet",
]
MAX_LENGTH = 8192
SPAN = 13


def last_boxed(text):
    start = text.rfind("\\boxed{")
    if start < 0:
        return None
    end, depth = start + len("\\boxed{"), 1
    while end < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[end], 0)
        end += 1
    return text[start + len("\\boxed{"):end - 1].strip() if depth == 0 else None


def spans(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + SPAN]) for i in range(max(len(words) - SPAN + 1, 1))}


parathinker_dir, model_dir, output = sys.argv[1:]
theirs = AutoTokenizer.from_pretrained(parathinker_dir)
ours = AutoTokenizer.from_pretrained(model_dir)
gsm8k = pd.read_parquet(GSM8K_SFT)
template = gsm8k.extra_info[0]["question"].split("Problem: ")[0] + "Problem: "
eval_spans = set().union(*(spans(p[0]["content"].split("Problem: ", 1)[1]) for f in EVAL for p in pd.read_parquet(f).prompt))

rows, stats = [], collections.Counter()
for shard in sorted(glob.glob(f"{parathinker_dir}/train/data-*.arrow")):
    with pa.memory_map(shard) as source:
        examples = pa.ipc.open_stream(source).read_all().column("input_ids").to_pylist()
    for ids in examples:
        stats["total"] += 1
        text = theirs.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False).replace("<vllm_pad>", "")
        problem = re.search(r"<｜User｜>(.*?) You FIRST think", text, re.S).group(1).strip()
        if spans(problem) & eval_spans:
            stats["eval overlap"] += 1
            continue
        answer = last_boxed(re.findall(r"<summary>(.*?)</summary>", text, re.S)[-1])
        paths = sorted((p.strip() for _, p in re.findall(r"<think(\d)>(.*?)</think\1>", text, re.S)
                        if answer and last_boxed(p) == answer), key=len)
        if len(paths) < 2:
            stats["< 2 finished paths with the summary answer"] += 1
            continue
        question = template + problem
        response = (f"<Parallel><Path>{paths[0]}</Path><Path>{paths[1]}</Path></Parallel>\n"
                    f"<Summary>Both paths give {answer}.</Summary>\n\nFinal Answer: {answer}")
        prompt_ids = ours.apply_chat_template([{"role": "user", "content": question}], add_generation_prompt=True, tokenize=True)
        if len(prompt_ids) + len(ours(response + ours.eos_token, add_special_tokens=False)["input_ids"]) > MAX_LENGTH:
            stats[f"> {MAX_LENGTH} tokens"] += 1
            continue
        tags, correct = validate(response)
        assert tags == correct == 8, response[:200]
        rows.append({
            "index": len(rows), "output": response, "data_source": "Leslie04/parathinker-math-6K",
            "prompt": [{"content": question, "role": "user"}], "ability": "math",
            "reward_model": {"ground_truth": answer, "style": "rule"},
            "extra_info": {"answer": response, "index": len(rows), "question": question},
        })
stats["kept"] = len(rows)
print(dict(stats))
mix = pd.concat([gsm8k, pd.DataFrame(rows)], ignore_index=True)
mix.to_parquet(output)
print(f"{len(gsm8k)} GSM8K + {len(rows)} ParaThinker -> {output}")
