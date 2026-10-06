"""Scores a generation dump (authors' rollout dump or scripts/bench/generate_plain.py) against its benchmark parquet; rows are in parquet order.

Math (authors' set, LIMO): the authors' math_dapo check of "Final Answer:". ARC / MMLU-Pro: the letter after the last "Final Answer:".
accuracy_robust also accepts other answer layouts: math from the last \\boxed{} or the line after the last "Final Answer:", checked with
math_verify; options also as "answer is X" / "Correct Answer: X" or as the option number (1 = A).
IFEval: the official lm-eval checker on the answer with any <think> block removed (prompt- and instruction-level, strict and loose).
Also: share of answers with <Parallel>, tag validity (scripts/tag_validator.py), answers without "Final Answer", mean length in characters.

Usage (from verl/, PYTHONPATH with the IFEval checker): python ../scripts/bench/score.py <generations.jsonl> <test.parquet> <output.json> [<rows.jsonl>]
The optional rows.jsonl gets one outcome per answer for paired comparisons; the summary JSON does not depend on it.
Optional env SCORE_IFEVAL_SEED=<int> (set by scripts/instruct4b_eval/run_eval.sh): the IFEval checker's random fallbacks (e.g. a random
letter when the doc's letter is "!") are seeded per prompt from "<seed>/<doc key>", langdetect with <seed>. Unset: unseeded, as before.
"""
import json
import os
import random
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, __file__.rsplit("/", 2)[0])
from tag_validator import validate  # noqa: E402
from math_verify import parse, verify  # noqa: E402
from verl.utils.reward_score.math_dapo import compute_score, last_boxed_only_string, remove_boxed  # noqa: E402

generations_path, test_path, output_path, *rows_path = sys.argv[1:]
generations = pd.read_json(generations_path, lines=True)
test = pd.read_parquet(test_path)
assert len(generations) == len(test), (len(generations), len(test))
tags = re.compile(r"</?(?:Parallel|Path|Summary)>")
for row, (prompt, generated) in enumerate(zip(test["prompt"], generations["input"])):  # rows must line up
    assert tags.sub("", prompt[0]["content"])[-200:] in tags.sub("", generated), f"row {row} does not match its prompt"

answers = generations["output"].str.replace("<|endoftext|>", "", regex=False).str.replace("<|im_end|>", "", regex=False)
final = answers.map(lambda text: text.split("</think>")[-1])  # the answer after any thinking block
sources = test["data_source"].str.removeprefix("APO_")
truths = [reward["ground_truth"] for reward in test["reward_model"]]


def correct(source, answer, truth, info):
    if source == "IFEVAL":
        from lm_eval.tasks.ifeval import utils
        doc, seed = json.loads(info["doc"]), os.environ.get("SCORE_IFEVAL_SEED")
        if seed is not None:
            from langdetect import DetectorFactory
            random.seed(f"{int(seed)}/{doc['key']}")
            DetectorFactory.seed = int(seed)
        return utils.process_results(doc, [answer])
    if source in ("ARC", "MMLUPRO"):
        letters = re.findall(r"(?i)Final Answer\s*:\s*\**\(?([A-J])\b", answer)
        return bool(letters) and letters[-1].upper() == truth
    return compute_score(answer, truth)["acc"]


def correct_robust(source, answer, truth):
    if source in ("ARC", "MMLUPRO"):
        choices = re.findall(r"(?i)(?:final answer|correct answer|answer is|answer)\s*:?\s*\**\(?([A-J]|10|[1-9])\b", answer)
        return bool(choices) and (choices[-1].upper() if choices[-1].isalpha() else "ABCDEFGHIJ"[int(choices[-1]) - 1]) == truth
    boxed = last_boxed_only_string(answer)
    if boxed:
        candidate = remove_boxed(boxed)
    else:
        parts = re.split(r"(?i)final answer\s*:", answer)
        lines = [line for line in parts[-1].splitlines() if line.strip()] if len(parts) > 1 else []
        candidate = lines[0] if lines else ""
    candidate = candidate.strip().strip("$").strip().rstrip(".")
    return bool(candidate) and (verify(parse(f"${truth}$"), parse(f"${candidate}$")) or compute_score(f"Final Answer: {candidate}", truth)["acc"])


results = [correct(s, a, t, i) for s, a, t, i in zip(sources, final, truths, test["extra_info"])]
frame = pd.DataFrame({"source": sources, "problem": [p[0]["content"] for p in test["prompt"]], "answer": answers})
if (sources == "IFEVAL").all():
    for key in ("prompt_level_strict_acc", "prompt_level_loose_acc"):
        frame[key] = [r[key] for r in results]
    frame["inst_level_strict_acc"] = [np.mean(r["inst_level_strict_acc"]) for r in results]
    frame["acc"] = frame["prompt_level_strict_acc"]
else:
    frame["acc"] = results
    frame["acc_robust"] = [correct_robust(s, a, t) for s, a, t in zip(sources, final, truths)]
frame["parallel"] = answers.str.contains("<Parallel>")
frame[["tags", "correct_tags"]] = answers.map(validate).tolist()
frame["no_final_answer"] = ~final.str.contains(r"(?i)Final Answer\s*:")
frame["chars"] = answers.str.len()
if "truncated" in generations:
    frame["truncated"] = generations["truncated"]

summary = {}
for source, group in frame.groupby("source"):
    per_problem = group.groupby("problem")["acc"]
    tagged = group[group["tags"] > 0]
    summary[source] = {
        "accuracy": round(100 * group["acc"].mean(), 2),
        **({"accuracy_robust": round(100 * group["acc_robust"].mean(), 2)} if "acc_robust" in group else {}),
        f"pass@{per_problem.size().iloc[0]}": round(100 * per_problem.max().mean(), 2),
        **({f"pass_robust@{per_problem.size().iloc[0]}": round(100 * group.groupby("problem")["acc_robust"].max().mean(), 2)} if "acc_robust" in group else {}),
        "problems": int(per_problem.ngroups),
        "with_parallel": round(100 * group["parallel"].mean(), 1),
        "valid_tagged_responses": round(100 * (tagged["tags"] == tagged["correct_tags"]).mean(), 1) if len(tagged) else None,
        "no_final_answer": round(100 * group["no_final_answer"].mean(), 1),
        "mean_chars": int(group["chars"].mean()),
        **({"truncated": round(100 * group["truncated"].mean(), 1)} if "truncated" in group else {}),
        **({key: round(100 * group[key].mean(), 2) for key in ("prompt_level_loose_acc", "inst_level_strict_acc")} if source == "IFEVAL" else {}),
    }
json.dump(summary, open(output_path, "w"), indent=1)
print(json.dumps(summary))

if rows_path:  # problem_id: extra_info "id" if the parquet has it, else source/<order of first appearance of the prompt>
    order = {problem: n for n, problem in enumerate(dict.fromkeys(frame["problem"]))}
    rows = frame.drop(columns=["answer"]).assign(
        row=range(len(frame)), input=generations["input"],
        problem_id=[info.get("id") or f"{s}/{order[p]}" for info, s, p in zip(test["extra_info"], sources, frame["problem"])],
        sample=frame.groupby("problem").cumcount(),
        valid_tags=(frame["tags"] > 0) & (frame["tags"] == frame["correct_tags"]),
        tokens=generations["tokens"] if "tokens" in generations else None,
        truncated=frame["truncated"] if "truncated" in frame else None)
    if (sources == "IFEVAL").all():
        rows["instruction_id_list"] = [json.loads(info["doc"])["instruction_id_list"] for info in test["extra_info"]]
        for key in ("inst_level_strict_acc", "inst_level_loose_acc"):
            rows[key] = [r[key] for r in results]
    rows.to_json(rows_path[0], orient="records", lines=True)
