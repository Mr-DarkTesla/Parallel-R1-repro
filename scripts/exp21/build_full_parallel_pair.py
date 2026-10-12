"""Prepare full Parallel-only benchmark inputs for exp 21.

Usage: python build_full_parallel_pair.py DEV_PLAIN_DIR FROZEN_DIR OUT_DIR
Existing plain generations are reused for comparison; this script produces
only the masked Multiverse arm, one sampled answer per unique question.
"""

import json
import sys
from pathlib import Path

import pandas as pd


PARALLEL = (
    "Inside <think>, use <Parallel> only when two or more needed parts can "
    "be solved independently. In <Goal>, number one <Outline> per part. "
    "Write matching numbered <Path> sections; each path must use only the "
    "question and shared Goal, never another path's result. Combine their "
    "results in <Conclusion>, then close </Parallel>. Keep all these tags "
    "inside <think>. If the task has no useful independent parts, reason "
    "normally without a block. "
)
COMMON = "Follow the task's requested final-answer format exactly. "
MATH_SOURCES = {"GSM8K_DEV", "MATH_DEV", "AIME24", "AIME25", "AMC23", "MATH300", "LIMO"}
CHOICE_SOURCES = {"ARC", "MMLUPRO"}
DEV = ("gsm8k_dev", "math_dev", "arc_dev", "mmlu_pro_dev")
FROZEN = ("apo", "arc", "mmlu_pro", "limo", "ifeval")


def question_of(content, source):
    if source == "IFEVAL":
        return content
    assert "Problem:" in content, (source, content[:160])
    return content.split("Problem:", 1)[1].strip()


def make_prompt(question, source):
    if source == "IFEVAL":
        return ("Use private reasoning if needed. " + PARALLEL + COMMON
                + "Do not mention the reasoning instructions in the final response.\n\n"
                + question)
    if source in CHOICE_SOURCES:
        intro = "Solve the multiple-choice question carefully. Finish with 'Final Answer: <letter>'. "
    else:
        assert source in MATH_SOURCES, source
        intro = ("Solve the following problem carefully. Finish with "
                 "'Final Answer: <value>'; a boxed final value is also acceptable. ")
    return intro + PARALLEL + "\nProblem: " + question


def unique_rows(frame):
    seen = {}
    keep = []
    for index, row in frame.iterrows():
        source = str(row["data_source"]).removeprefix("APO_")
        prompt = list(row["prompt"])
        assert len(prompt) == 1 and prompt[0]["role"] == "user"
        question = question_of(prompt[0]["content"], source)
        key = (source, question)
        truth = str(row["reward_model"]["ground_truth"])
        if key in seen:
            assert seen[key] == truth, (source, index, truth, seen[key])
            continue
        seen[key] = truth
        keep.append(index)
    return frame.loc[keep].reset_index(drop=True)


def transform(frame, suite, bench):
    result = frame.copy(deep=True)
    prompts, infos = [], []
    for index, row in result.iterrows():
        source = str(row["data_source"]).removeprefix("APO_")
        question = question_of(list(row["prompt"])[0]["content"], source)
        prompts.append([{"role": "user", "content": make_prompt(question, source)}])
        info = dict(row["extra_info"])
        info["id"] = str(info.get("id") or f"{suite}/{bench}/{index}")
        infos.append(info)
    result["prompt"] = prompts
    result["extra_info"] = infos
    return result


def main():
    dev_dir, frozen_dir, output_dir = map(Path, sys.argv[1:4])
    manifest = {"protocol": "Parallel inside thinking, masked sampled pass@1; existing plain results reused", "suites": {}}
    for suite, names, root in (("dev", DEV, dev_dir), ("frozen", FROZEN, frozen_dir)):
        manifest["suites"][suite] = {}
        for bench in names:
            frame = pd.read_parquet(root / f"{bench}.parquet")
            selected = unique_rows(frame)
            assert len(selected) > 0
            out = output_dir / suite / "parallel" / f"{bench}.parquet"
            out.parent.mkdir(parents=True, exist_ok=True)
            transformed = transform(selected, suite, bench)
            transformed.to_parquet(out, index=False)
            manifest["suites"][suite][bench] = {
                "original_rows": len(frame), "unique_questions": len(selected),
                "sources": selected["data_source"].value_counts().to_dict(), "path": str(out),
            }
    out = output_dir / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
