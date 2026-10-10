"""Record the independent manual audit and verbatim wrapping of reserve A traces."""
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit/sol_reserve_round3"
PLANS = {
    "math-train/1544": ("Determine the enchilada price by eliminating tacos.", "Determine the taco price by eliminating enchiladas."),
    "math-train/6751": ("Count divisors with no factor of three.", "Count divisors with one factor of three."),
    "math-train/7220": ("Transform the real coordinate.", "Transform the imaginary coordinate."),
    "math-train/1250": ("Compute Monday's utility expression.", "Compute Tuesday's utility expression."),
    "math-train/3992": ("Determine the first integer and opposite fractional component.", "Determine the second integer and opposite fractional component."),
    "math-train/7203": ("Compute the determinant of the two rays.", "Compute the product of the ray lengths."),
    "math-train/421": ("Determine the inverse-proportion constant from the first exam.", "Determine the score needed on the second exam."),
    "math-train/4536": ("Compute the product of roots of the first cubic.", "Compute the product of roots of the second cubic."),
    "math-train/4436": ("Derive an upper bound for the target expression.", "Find a feasible point attaining the bound."),
    "math-train/1938": ("Compute expected rainfall from the four-inch outcome.", "Compute expected rainfall from the ten-inch outcome."),
    "math-train/1976": ("Count placements of the two even dice.", "Count face assignments for one placement."),
}
REJECT = {
    "math-train/1975": "Fair independent coin flips are assumed but not stated; branches are also short.",
    "gsm8k-train/4150": "Each path is a single trivial multiplication; most work is after the block.",
    "math-train/6643": "Both paths are single trivial factor evaluations.",
    "math-train/5879": "Both paths are single trivial exponent reductions.",
    "math-train/2448": "Independent births are assumed but not stated, and both paths are short counts.",
    "math-train/694": "Each path is one elementary multiplication; no substantive reasoning split.",
    "math-train/6945": "Each path reads one matrix entry directly; verification carries the reasoning.",
    "math-train/2513": "Independent game outcomes are assumed but not stated.",
    "math-train/1983": "Independent uniform arrivals are assumed without being specified, and the diagonal orientation is imprecise.",
    "math-train/253": "Two very short expansions; most reasoning is in the combination.",
}


def wrap(response, plan):
    think, tail = response.split("</think>", 1)
    first = think.index("\n\nPart 1:\n") + 2
    second = think.index("\n\nPart 2:\n") + 2
    synthesis = think.index("\n\n", second + len("Part 2:\n")) + 2
    prefix, path1, path2, conclusion = think[:first], think[first:second], think[second:synthesis], think[synthesis:]
    assert prefix.startswith("<think>") and conclusion.strip() and not re.match(r"(?i)^combine\s+the\s+independent", conclusion.strip())
    goal = ("<Goal><Outline>1: " + plan[0] + "</Outline>"
            "<Outline>2: " + plan[1] + "</Outline></Goal>")
    tagged = (prefix + "<Parallel>" + goal + "<Path>1: " + path1 + "</Path>"
              + "<Path>2: " + path2 + "</Path><Conclusion>" + conclusion
              + "</Conclusion></Parallel></think>" + tail)
    stripped = re.sub(r"<Goal>.*?</Goal>", "", tagged, flags=re.S)
    stripped = re.sub(r"<Path>\s*[12]:\s*", "", stripped)
    stripped = re.sub(r"</?(?:Parallel|Path|Conclusion)>", "", stripped)
    assert re.sub(r"\s+", "", stripped) == re.sub(r"\s+", "", response)
    return tagged


def main():
    rows = [json.loads(line) for line in (ROOT / "agent_a/traces.jsonl").open()]
    assert len(rows) == len(PLANS) + len(REJECT) == 21
    assert {r["id"] for r in rows} == set(PLANS) | set(REJECT)
    review = []
    tagged = []
    for row in rows:
        id_ = row["id"]
        reason = "Mathematical steps and final answer checked; substantive independent calculations and synthesis." if id_ in PLANS else REJECT[id_]
        review.append({"id": id_, "verdict": "accept" if id_ in PLANS else "reject", "reason": reason,
                       "reviewer": "root_manual_independent_of_author"})
        if id_ in PLANS:
            tagged.append({**row, "response": wrap(row["response"], PLANS[id_])})
    for name, items in (("review_a_root.jsonl", review), ("tagged_a_root.jsonl", tagged)):
        (ROOT / name).write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items))
    print("reviewed", len(review), "tagged", len(tagged))


if __name__ == "__main__":
    main()
