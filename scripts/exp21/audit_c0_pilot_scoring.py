"""Document two verified false negatives in the fixed 40-question C0 pilot.

Usage: python scripts/exp21/audit_c0_pilot_scoring.py OUTPUT_JSON
This audit changes no generation dump or historical score file.
"""
import json
import sys
import tarfile
from pathlib import Path

from compare_masked_pilot_archives import compare, load


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
BASE = ARCHIVES / "c0-greedy-pilot40.tgz"
FIXES = {
    ("GSM8K_DEV", "gsm8k-train/235", 0): ("gsm10", "Each of them will get 9 apples."),
    ("MATH_DEV", "math-test/103", 0): ("mathnext10", "2x(15x² - 4x + 10)"),
}
CANDIDATES = {
    "m1_tagweighted": "m1-tagweighted-greedy-pilot40.tgz",
    "m1_control": "m1-tagweighted-control-greedy-pilot40.tgz",
    "alpha_090": "interp_a090_masked_pilot.tgz",
    "text1": "text1_masked_pilot.tgz",
    "frontblock": "m1_frontblock_masked_pilot.tgz",
    "merge_inside": "m1_merge_inside_masked_pilot.tgz",
}


def main(output):
    original = load(BASE)
    corrected = {key: row.copy() for key, row in original.items()}
    evidence = []
    with tarfile.open(BASE) as archive:
        for key, (stem, final) in FIXES.items():
            row = corrected[key]
            assert row["acc_robust"] is False and row["truncated"] is False
            name = f"c0_greedy_pilot/{stem}.jsonl"
            raw = [json.loads(line) for line in archive.extractfile(name)]
            matching = [(i, entry) for i, entry in enumerate(raw) if entry["input"] == row["input"]]
            assert len(matching) == 1, key
            index, entry = matching[0]
            answer = entry["output"].split("</think>")[-1]
            assert final in answer, (key, answer)
            row["acc_robust"] = True
            evidence.append({"key": key, "raw_file": name, "row": index,
                             "final": answer.strip(), "manual_verdict": "correct"})
    result = {"base_archive": BASE.name, "original_correct": sum(r["acc_robust"] for r in original.values()),
              "corrected_correct": sum(r["acc_robust"] for r in corrected.values()),
              "evidence": evidence, "comparisons": {}}
    for label, filename in CANDIDATES.items():
        candidate = load(ARCHIVES / filename)
        assert corrected.keys() == candidate.keys(), label
        for key in corrected:
            assert corrected[key]["input"] == candidate[key]["input"], (label, key)
        keys = sorted(corrected)
        result["comparisons"][label] = {
            "archive": filename, "original": compare(original, candidate, keys, "acc_robust"),
            "corrected": compare(corrected, candidate, keys, "acc_robust")}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["comparisons"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
