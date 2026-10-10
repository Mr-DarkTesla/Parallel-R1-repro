"""Count final-answer lines in paired archived IFEval generations."""

import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
OUT = ROOT / "audit/ifeval_final_answer_line_audit.json"
names = [f"{model}-ifeval-{mode}" for model in ("c0", "m1-twopath-tagweighted",
                                               "m1-twopath-control") for mode in ("th", "nt")]
report = {}
for name in names:
    with tarfile.open(ARCHIVES / f"{name}.tgz") as archive:
        member = next(n for n in archive.getnames()
                      if n.endswith("/rows/ifeval.jsonl") and "/._" not in n)
        rows = [json.loads(line) for line in archive.extractfile(member)]
    with_line = [r for r in rows if not r["no_final_answer"]]
    report[name] = {"rows": len(rows),
                    "strict_correct": sum(r["prompt_level_strict_acc"] for r in rows),
                    "with_final_answer_line": len(with_line),
                    "strict_correct_among_with_line": sum(r["prompt_level_strict_acc"]
                                                          for r in with_line)}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(OUT)
