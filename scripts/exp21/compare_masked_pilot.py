"""Compare a masked-decoding pilot with saved runs on the same dev problems."""
import json
import sys


def rows(path):
    return [json.loads(line) for line in open(path)]


def main():
    pilot_path, sequential_path, branch_path, output_path = sys.argv[1:5]
    pilot = rows(pilot_path)
    by_run = {}
    for name, path in (("sequential", sequential_path), ("branch", branch_path)):
        samples = [r for r in rows(path) if r["sample"] == 0]
        by_run[name] = {r["problem"]: r for r in samples}
        assert len(by_run[name]) == len(samples), name
    result = {"n": len(pilot), "same_prompt": True, "runs": {}, "paired": []}
    for name, sample in (("masked", pilot),
                         *((name, [by_run[name][r["problem"]] for r in pilot]) for name in by_run)):
        assert len(sample) == len(pilot)
        result["runs"][name] = {
            "correct": sum(bool(r["acc_robust"]) for r in sample),
            "numbered_block": sum(bool(r["mv_numbered"]) for r in sample),
            "truncated": sum(bool(r["truncated"]) for r in sample),
            "mean_tokens": round(sum(r["tokens"] for r in sample) / len(sample), 1),
            "mean_forward_passes": round(sum(r["forward_passes"] for r in sample) / len(sample), 1),
        }
    for r in pilot:
        entry = {"problem_id": r["problem_id"]}
        for name, item in (("masked", r),
                           *((name, by_run[name][r["problem"]]) for name in by_run)):
            entry[name] = {"correct": bool(item["acc_robust"]),
                           "numbered_block": bool(item["mv_numbered"])}
        result["paired"].append(entry)
    with open(output_path, "w") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps(result["runs"], ensure_ascii=False))


if __name__ == "__main__":
    main()
