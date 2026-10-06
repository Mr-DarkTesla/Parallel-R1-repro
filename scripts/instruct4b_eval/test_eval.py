"""CPU checks of the exp 13 evaluation code on tiny synthetic inputs (code behaviour, not benchmark evidence).

1. score.py: the summary JSON is the same with and without the optional rows file; repeated answers of one problem get one
   problem id and sample indices 0..k-1; per-row strict/robust results, tags, tokens and truncation are written;
   SCORE_IFEVAL_SEED changes nothing outside IFEval.
2. SCORE_IFEVAL_SEED on two real IFEval rows whose installed-checker result depends on the random state (needs the pod's /work,
   otherwise reported as skipped): repeated scorings and another row order/cohort give the same per-prompt outcomes; output
   schema without the option is the same.
3. paired_compare.py: known per-problem outcomes give the expected delta; reordered rows, another cohort of problems, a missing
   benchmark, unequal samples per problem within a source (different counts across sources are allowed), a different budget and
   a different or absent IFEval scorer seed, equal candidate names, a --meta-dir without the benchmark and an unversioned test-only run
   are rejected; seeds are reported separately and pooled; sources are printed. --cross-prompt (plain vs parallel prompts) accepts the
   same problems under the two headers, also with "Problem:" inside the problem text, and rejects (2026-10-07 review probes) thinking vs
   no-thinking or parallel, parallel vs parallel, another data directory, other problems at the same ids, another header, no common benchmark.

Usage (from verl/, PYTHONPATH and NLTK_DATA as in run_eval.sh): python ../scripts/instruct4b_eval/test_eval.py
"""
import json
import os
import subprocess
import sys
import tempfile

import pandas as pd

IFEVAL = ("/work/bench_data/plain/ifeval.parquet", "/work/bench/qwen3-4b-nothinking-16k/ifeval.jsonl")  # frozen prompts, C0 dump
FLAKY = (22, 511)  # 2026-10-06 rescoring flips: letter_frequency with letter "!" (random letter), response_language (langdetect)

HERE = os.path.dirname(os.path.abspath(__file__))
SCORE = os.path.join(HERE, "../bench/score.py")
COMPARE = os.path.join(HERE, "paired_compare.py")
HEADER = "Solve the following problem step by step.\nEnd your response with a line starting with Final Answer: followed by the final result.\n\n"
PARALLEL_HEADER = HEADER.replace("End your", "During the reasoning process, insert <Parallel> blocks of <Path>s.\n\nEnd your")


def run(*args, seed=None, env=None):
    env = ({k: v for k, v in os.environ.items() if k not in ("SCORE_IFEVAL_SEED", "EVAL_ALLOW_UNVERSIONED")}
           | ({"SCORE_IFEVAL_SEED": str(seed)} if seed is not None else {}) | (env or {}))
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, env=env)


def math_case(tmp):
    """2 problems x 3 samples, consecutive rows as in the dev parquets."""
    problems = [("What is 2+3?", "5"), ("What is 7*6?", "42")]
    outputs = ["2+3=5\nFinal Answer: 5", "The sum is \\boxed{5}.", "Final Answer: 6",
               "<Parallel><Path>7*6=42</Path><Path>6*7=42</Path></Parallel><Summary>42</Summary>\nFinal Answer: 42", "Final Answer: 41", "I think 42"]
    test = pd.DataFrame({
        "data_source": "APO_MATH_DEV",
        "prompt": [[{"role": "user", "content": f"{HEADER}Problem: {q}"}] for q, _ in problems for _ in range(3)],
        "ability": "math",
        "reward_model": [{"ground_truth": a, "style": "rule"} for _, a in problems for _ in range(3)],
        "extra_info": [{"reward_method": "accuracy_reward", "doc": "{}", "id": f"toy/{n}"} for n in range(2) for _ in range(3)],
    })
    test.to_parquet(f"{tmp}/test.parquet")
    with open(f"{tmp}/gen.jsonl", "w") as f:
        for prompt, output, n in zip(test["prompt"], outputs, range(6)):
            f.write(json.dumps({"input": f"<|im_start|>user\n{prompt[0]['content']}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n",
                                "output": output + "<|im_end|>", "tokens": 10 + n, "truncated": n == 5}) + "\n")


def test_score(tmp):
    math_case(tmp)
    plain = run(SCORE, f"{tmp}/gen.jsonl", f"{tmp}/test.parquet", f"{tmp}/a.json")
    assert plain.returncode == 0, plain.stderr[-2000:]
    with_rows = run(SCORE, f"{tmp}/gen.jsonl", f"{tmp}/test.parquet", f"{tmp}/b.json", f"{tmp}/rows.jsonl")
    assert with_rows.returncode == 0, with_rows.stderr[-2000:]
    assert json.load(open(f"{tmp}/a.json")) == json.load(open(f"{tmp}/b.json")), "summary changed by the rows option"
    rows = pd.read_json(f"{tmp}/rows.jsonl", lines=True)
    assert rows["problem_id"].tolist() == ["toy/0"] * 3 + ["toy/1"] * 3
    assert rows["sample"].tolist() == [0, 1, 2] * 2
    assert rows["acc"].tolist() == [True, False, False, True, False, False], rows["acc"].tolist()  # strict: "Final Answer:" only
    assert rows["acc_robust"].tolist() == [True, True, False, True, False, False], rows["acc_robust"].tolist()  # robust: also \boxed
    assert rows["parallel"].tolist() == [False, False, False, True, False, False]
    assert rows["valid_tags"].tolist() == [False, False, False, True, False, False]
    assert rows["tokens"].tolist() == list(range(10, 16)) and rows["truncated"].tolist() == [False] * 5 + [True]
    summary = json.load(open(f"{tmp}/a.json"))["MATH_DEV"]
    assert summary["accuracy_robust"] == 50.0 and summary["problems"] == 2
    seeded = run(SCORE, f"{tmp}/gen.jsonl", f"{tmp}/test.parquet", f"{tmp}/c.json", f"{tmp}/rows_seeded.jsonl", seed=0)
    assert seeded.returncode == 0, seeded.stderr[-2000:]
    assert json.load(open(f"{tmp}/c.json")) == json.load(open(f"{tmp}/a.json"))
    assert pd.read_json(f"{tmp}/rows_seeded.jsonl", lines=True).equals(rows), "the IFEval seed changed math scoring"


def test_ifeval_seed(tmp):
    if not all(map(os.path.exists, IFEVAL)):
        return False
    import random
    from langdetect import DetectorFactory
    from lm_eval.tasks.ifeval import utils
    test, dump = pd.read_parquet(IFEVAL[0]), pd.read_json(IFEVAL[1], lines=True)
    for row in FLAKY:  # the installed checker on the real answer: the result depends on the random state
        doc, answer = json.loads(test["extra_info"][row]["doc"]), dump["output"][row].replace("<|im_end|>", "").split("</think>")[-1]
        outcomes = set()
        for state in range(40):
            random.seed(state)
            DetectorFactory.seed = state
            result = utils.process_results(doc, [answer])
            outcomes.add((result["prompt_level_strict_acc"], result["prompt_level_loose_acc"]))
        assert len(outcomes) > 1, f"row {row} is not random-state dependent: {outcomes}"

    def score(name, picked, seed):
        test.iloc[picked].reset_index(drop=True).to_parquet(f"{tmp}/{name}.parquet")
        dump.iloc[picked].to_json(f"{tmp}/{name}.jsonl", orient="records", lines=True)
        done = run(SCORE, f"{tmp}/{name}.jsonl", f"{tmp}/{name}.parquet", f"{tmp}/{name}.json", f"{tmp}/{name}_rows.jsonl", seed=seed)
        assert done.returncode == 0, done.stderr[-2000:]
        rows = pd.read_json(f"{tmp}/{name}_rows.jsonl", lines=True)
        keys = ["prompt_level_strict_acc", "prompt_level_loose_acc", "inst_level_strict_acc", "inst_level_loose_acc"]
        return json.load(open(f"{tmp}/{name}.json")), rows, {p: tuple(map(str, r)) for p, r in zip(rows["problem"], rows[keys].to_numpy())}

    flaky, other = [*FLAKY, 0], [5, 511, 0, 22, 7]  # other: another order and two more prompts in the cohort
    runs = [score(f"seeded{n}", flaky, 0) for n in range(3)] + [score("other", other, 0)]
    for _, _, outcomes in runs[1:]:
        assert all(runs[0][2][p] == outcomes[p] for p in runs[0][2]), "seeded per-prompt outcomes differ between scorings"
    summary, rows, _ = score("unseeded", flaky, None)
    assert summary.keys() == runs[0][0].keys() and summary["IFEVAL"].keys() == runs[0][0]["IFEVAL"].keys()
    assert list(rows.columns) == list(runs[0][1].columns), "rows schema depends on the seed option"
    print(f"seeded outcomes of rows {FLAKY}: {[runs[0][2][test['prompt'][r][0]['content']][:2] for r in FLAKY]}")
    return True


def fake_run(path, outcomes, budget=16384, reorder=False, mode="no-thinking", scorer_seed=0, prompts=None, header=None, texts=None, meta=None):
    """outcomes: {bench: [(problem_id, [robust results of its samples])]} -> run directory as written by run_eval.sh.
    problem_id "AIME/x" gets source AIME, others MATH_DEV; scorer_seed None = meta.json without the key (unseeded scoring).
    Problem "<header>Problem: <texts[id] or 'q <id>'>", header by mode; prompts /x/plain or /x/parallel; meta: extra meta.json keys."""
    os.makedirs(f"{path}/rows", exist_ok=True)
    parallel = mode == "parallel"
    json.dump({"suite": "dev", "mode": mode, "budget": budget, "temperature": 1.0, "top_p": 1.0,
               "generator": "scripts/bench/eval_rollout.sh" if parallel else "scripts/instruct4b_eval/generate.py",
               "prompts": prompts or ("/x/parallel" if parallel else "/x/plain"),
               **({"ifeval_scorer_seed": scorer_seed} if scorer_seed is not None else {}), **(meta or {})}, open(f"{path}/meta.json", "w"))
    header = header or (PARALLEL_HEADER if parallel else HEADER)
    for bench, problems in outcomes.items():
        text = {pid: f"{header}Problem: {(texts or {}).get(pid, f'q {pid}')}" for pid, _ in problems}
        rows = pd.DataFrame([{"source": pid.split("/")[0] if "/" in pid else "MATH_DEV", "problem_id": pid, "problem": text[pid], "input": f"<user>{mode} {text[pid]}", "sample": s, "acc": ok, "acc_robust": ok,
                              "parallel": False, "valid_tags": False, "no_final_answer": False, "truncated": False, "tokens": 5}
                             for pid, oks in problems for s, ok in enumerate(oks)])
        if reorder:
            rows = rows.iloc[::-1]
        rows.to_json(f"{path}/rows/{bench}.jsonl", orient="records", lines=True)


def test_compare(tmp):
    base = {"math_dev": [("p0", [1, 1]), ("p1", [0, 0]), ("p2", [1, 0]), ("p3", [1, 1])]}
    seed_a = {"math_dev": [("p0", [1, 1]), ("p1", [1, 0]), ("p2", [1, 0]), ("p3", [0, 0])]}  # per problem 1, .5, .5, 0 -> mean .5
    seed_b = {"math_dev": [("p0", [1, 1]), ("p1", [1, 1]), ("p2", [1, 1]), ("p3", [1, 1])]}  # mean 1
    fake_run(f"{tmp}/base", base)
    fake_run(f"{tmp}/a", seed_a)
    fake_run(f"{tmp}/b", seed_b)
    ok = run(COMPARE, "--base", f"{tmp}/base", "--cand", f"{tmp}/a", "--cand", f"{tmp}/b", "--out", f"{tmp}/cmp.json")
    assert ok.returncode == 0, ok.stderr[-2000:]
    result = json.load(open(f"{tmp}/cmp.json"))["benchmarks"]["math_dev"]
    acc = {name: metrics["acc_robust"] for name, metrics in result["metrics"].items()}
    assert (acc["a"]["base"], acc["a"]["cand"], acc["a"]["delta"]) == (62.5, 50.0, -12.5), acc["a"]
    assert acc["b"]["delta"] == 37.5 and acc["seeds_pooled"]["delta"] == 12.5, acc
    assert acc["a"]["problems"] == 4 and result["samples_per_problem"] == {"MATH_DEV": 2}
    assert acc["a"]["ci95"][0] <= -12.5 <= acc["a"]["ci95"][1]

    mixed = {"math_dev": [("AIME/0", [1, 0, 0, 0]), ("AIME/1", [0, 0, 0, 0]), ("p0", [1]), ("p1", [0])]}  # x4 AIME, x1 MATH: allowed
    fake_run(f"{tmp}/mixed", mixed)
    ok = run(COMPARE, "--base", f"{tmp}/mixed", "--cand", f"{tmp}/mixed", "--out", f"{tmp}/mixed.json")
    assert ok.returncode == 0, ok.stderr[-2000:]
    assert json.load(open(f"{tmp}/mixed.json"))["benchmarks"]["math_dev"]["samples_per_problem"] == {"AIME": 4, "MATH_DEV": 1}
    printed = ok.stdout.splitlines()  # the blend is descriptive, every source gets its own line and label
    assert [line.split()[0] for line in printed] == ["math_dev", "math_dev/AIME", "math_dev/MATH_DEV"], ok.stdout
    assert "blend, descriptive" in printed[0] and all("vs -2 pp (proposed): " in line for line in printed[1:]), ok.stdout

    bad = {"reordered rows": dict(reorder=True), "unequal samples": dict(outcomes={"math_dev": base["math_dev"][:3] + [("p3", [1])]}),
           "unequal samples in one source": dict(outcomes={"math_dev": [("AIME/0", [1, 0, 0, 0]), ("AIME/1", [0, 0, 0]), ("p0", [1]), ("p1", [0])]}),
           "other cohort": dict(outcomes={"math_dev": seed_a["math_dev"][:3] + [("p9", [0, 0])]}),
           "missing benchmark": dict(outcomes={"math_dev": base["math_dev"], "arc_dev": [("q0", [1])]}), "other budget": dict(budget=3000),
           "other scorer seed": dict(scorer_seed=1), "unseeded scorer": dict(scorer_seed=None)}
    for name, kwargs in bad.items():
        fake_run(f"{tmp}/bad_{name}", kwargs.pop("outcomes", seed_a), **kwargs)
        self_compare = ("--base", f"{tmp}/bad_{name}", "--cand", f"{tmp}/bad_{name}")
        target = {"missing benchmark": ("--base", f"{tmp}/bad_{name}", "--cand", f"{tmp}/a"), "unequal samples": self_compare,
                  "unequal samples in one source": self_compare}.get(name, ("--base", f"{tmp}/base", "--cand", f"{tmp}/bad_{name}"))
        failed = run(COMPARE, *target, "--out", f"{tmp}/bad.json")
        assert failed.returncode != 0 and "Error" in failed.stderr, f"{name} was not rejected"
        print(f"rejected {name}: {failed.stderr.strip().splitlines()[-1]}")

    fake_run(f"{tmp}/parallel", seed_a, mode="parallel")  # same problems under the parallel prompt
    fake_run(f"{tmp}/bad_missing benchmark", {"math_dev": base["math_dev"], "arc_dev": [("q0", [1])]})  # plain run with one more benchmark
    wider = run(COMPARE, "--base", f"{tmp}/bad_missing benchmark", "--cand", f"{tmp}/parallel", "--cross-prompt", "--out", f"{tmp}/w.json")
    assert wider.returncode == 0 and json.load(open(f"{tmp}/w.json"))["not_compared"] == ["arc_dev"], wider.stderr[-2000:]
    plain_vs_parallel = ("--base", f"{tmp}/base", "--cand", f"{tmp}/parallel", "--out", f"{tmp}/cross.json")
    assert run(COMPARE, *plain_vs_parallel).returncode != 0, "other prompts accepted without --cross-prompt"
    cross = run(COMPARE, *plain_vs_parallel, "--cross-prompt")
    assert cross.returncode == 0, cross.stderr[-2000:]
    assert json.load(open(f"{tmp}/cross.json"))["benchmarks"]["math_dev"]["metrics"]["parallel"]["acc_robust"]["delta"] == -12.5
    texts = {"p0": "A. Problem: x"}  # "Problem:" inside the problem: the text after the first "Problem:" is compared whole
    fake_run(f"{tmp}/plain_inner", base, texts=texts)
    fake_run(f"{tmp}/par_inner", seed_a, mode="parallel", texts=texts)
    inner = run(COMPARE, "--base", f"{tmp}/plain_inner", "--cand", f"{tmp}/par_inner", "--cross-prompt", "--out", f"{tmp}/inner.json")
    assert inner.returncode == 0 and "vs -2 pp" not in inner.stdout, inner.stderr[-2000:]  # no tolerance label across prompts

    cross_bad = {  # name: (base run, cand run), all with --cross-prompt
        "thinking vs no-thinking": ("base", dict(outcomes=seed_a, mode="thinking")),
        "parallel vs thinking (headers alone would pass)": ("parallel", dict(outcomes=seed_a, mode="thinking")),
        "parallel vs parallel": ("parallel", dict(outcomes=seed_a, mode="parallel", prompts="/y/parallel")),
        "parallel prompts of another data dir": ("base", dict(outcomes=seed_a, mode="parallel", prompts="/y/parallel")),
        "other problems at the same ids": ("base", dict(outcomes=seed_a, mode="parallel", texts={"p2": "another problem"})),
        "other text before an inner Problem:": ("plain_inner", dict(outcomes=seed_a, mode="parallel", texts={"p0": "B. Problem: x"})),
        "another parallel header": ("base", dict(outcomes=seed_a, mode="parallel", header=PARALLEL_HEADER.replace("Solve", "Answer"))),
        "plain header in the parallel run": ("base", dict(outcomes=seed_a, mode="parallel", header=HEADER)),
        "no common benchmark": ("base", dict(outcomes={"gsm8k_dev": base["math_dev"]}, mode="parallel")),
    }
    for name, (base_run, kwargs) in cross_bad.items():
        fake_run(f"{tmp}/cross_{name}", kwargs.pop("outcomes"), **kwargs)
        failed = run(COMPARE, "--base", f"{tmp}/{base_run}", "--cand", f"{tmp}/cross_{name}", "--cross-prompt", "--out", f"{tmp}/bad.json")
        assert failed.returncode != 0 and "Error" in failed.stderr, f"cross-prompt {name} was not rejected: {failed.stdout}"
        print(f"rejected cross-prompt {name}: {failed.stderr.strip().splitlines()[-1][:160]}")

    os.makedirs(f"{tmp}/meta", exist_ok=True)  # slices from --meta-dir; a meta dir without the benchmark is an error
    pd.DataFrame({"problem_id": [p for p, oks in base["math_dev"] for _ in oks], "type": "Algebra"}).to_json(
        f"{tmp}/meta/math_dev.jsonl", orient="records", lines=True)
    sliced = run(COMPARE, "--base", f"{tmp}/base", "--cand", f"{tmp}/a", "--meta-dir", f"{tmp}/meta", "--out", f"{tmp}/sliced.json")
    assert sliced.returncode == 0 and "type=Algebra" in json.load(open(f"{tmp}/sliced.json"))["benchmarks"]["math_dev"]["slices"], sliced.stderr
    os.makedirs(f"{tmp}/s1", exist_ok=True)
    fake_run(f"{tmp}/s1/a", seed_b)  # same basename as {tmp}/a
    fake_run(f"{tmp}/unversioned", seed_a, meta={"commit": None, "unversioned_test_only": True})
    pair = ("--base", f"{tmp}/base", "--cand")
    for name, args in {"equal candidate names": (*pair, f"{tmp}/a", "--cand", f"{tmp}/s1/a"),
                       "meta dir without the benchmark": (*pair, f"{tmp}/a", "--meta-dir", f"{tmp}/s1"),
                       "unversioned test-only run": (*pair, f"{tmp}/unversioned")}.items():
        failed = run(COMPARE, *args, "--out", f"{tmp}/bad.json")
        assert failed.returncode != 0 and "Error" in failed.stderr, f"{name} was not rejected"
        print(f"rejected {name}: {failed.stderr.strip().splitlines()[-1][:160]}")
    allowed = run(COMPARE, *pair, f"{tmp}/unversioned", "--out", f"{tmp}/u.json", env={"EVAL_ALLOW_UNVERSIONED": "1"})
    assert allowed.returncode == 0, allowed.stderr[-2000:]


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        test_score(tmp)
        print("score.py rows: ok")
        print("score.py SCORE_IFEVAL_SEED:", "ok" if test_ifeval_seed(tmp) else f"SKIPPED, {IFEVAL} not found (run on the pod)")
        test_compare(tmp)
        print("paired_compare.py: ok")
