"""Point for the "accuracy vs forwards" slide: MATH500 and AIME 2024/2025/2026, each benchmark weighs 1/4 (as plot.py of the RL branches).
accuracy: accuracy_robust; forwards: mean decode steps per answer (scripts/bench/lengths.py); forks: mean <Parallel> blocks per answer.

Usage: python scripts/bench/slide_summary.py <output.json> <run_dir> [<run_dir> ...]   (run dirs with results/ and lengths/)
"""
import glob
import json
import sys

output, runs = sys.argv[1], sys.argv[2:]
benchmarks = {}
for run in runs:
    for path in glob.glob(f"{run}/results/*.json"):
        results, lengths = json.load(open(path)), json.load(open(path.replace("/results/", "/lengths/")))
        for name, r in results.items():
            benchmarks[name] = {**r, "accuracy": r["accuracy_robust"], "accuracy_authors_grader": r["accuracy"],
                                "forwards": lengths[name]["decode_steps"]["mean"], "forks": lengths[name]["forks"], "answers": lengths[name]["answers"]}
assert sorted(benchmarks) == ["AIME24", "AIME25", "AIME26", "MATH500"], sorted(benchmarks)
macro = {key: round(sum(b[key] for b in benchmarks.values()) / 4, 3) for key in ("accuracy", "forwards", "forks")}
json.dump({"macro": macro, "benchmarks": benchmarks}, open(output, "w"), indent=1)
print(json.dumps(macro))
for name, b in sorted(benchmarks.items()):
    print(f"{name}: accuracy {b['accuracy']}, forwards {b['forwards']}, forks {b['forks']}, answers {b['answers']}")
