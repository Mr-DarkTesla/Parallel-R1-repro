"""Multiverse prompt variant of the evaluation parquets (and of the exp 21 SFT rows): the plain eval prompt with one paragraph
about the format inserted after its first line. The model is asked for blocks only where parts are independent.

Usage (pod): python make_mv_prompts.py <plain_dir> <out_dir>   e.g. /work/bench_data/instruct4b/eval/dev/plain -> .../dev/multiverse
"""
import os
import sys

FIRST_LINE = "Solve the following problem step by step.\n"
MV_PARAGRAPH = (
    "When the work splits into parts that do not depend on each other (separate cases or separate quantities), "
    "solve those parts in a parallel block.\n\n"
    "Within each parallel block:\n"
    "Begin the block with <Parallel>, then list the parts inside <Goal> and </Goal>, one per <Outline> and </Outline>, numbered 1:, 2:, ...\n"
    "Write one path per outline with the same number, enclosed in <Path> and </Path>. A path must not use results of other paths, "
    "as the paths are generated simultaneously and independently.\n"
    "After the last path, combine the results of the paths in <Conclusion> and </Conclusion>, close the block with </Parallel> "
    "and continue the solution.\n\n")


def mv_prompt(plain):
    assert plain.startswith(FIRST_LINE), plain[:80]
    return FIRST_LINE + MV_PARAGRAPH + plain[len(FIRST_LINE):]


if __name__ == "__main__":
    import pandas as pd

    plain_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(plain_dir)):
        frame = pd.read_parquet(f"{plain_dir}/{name}")
        if not all(p[0]["content"].startswith(FIRST_LINE) for p in frame["prompt"]):
            print("skip (other prompt layout)", name)
            continue
        frame["prompt"] = [[{"role": "user", "content": mv_prompt(p[0]["content"])}] for p in frame["prompt"]]
        frame.to_parquet(f"{out_dir}/{name}")
        print(name, len(frame))
