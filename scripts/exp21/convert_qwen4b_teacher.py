#!/usr/bin/env python3
"""Convert screened Qwen 4B headed or inside-think work to two-path blocks.

CPU only. The per-ID split is intentionally explicit: a newly screened row has
no conversion plan until its independent/dependent Part boundary is reviewed.
This creates review data, not an SFT mixture.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from math_verify import parse as parse_math
from math_verify import verify as verify_math
from transformers import AutoTokenizer

from mv_format import ANY_TAG, parse


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "results/21-qwen3-0.6b-multiverse"
SOURCE = RUN / "data/qwen4b_teacher_graded320.jsonl"
SCREEN = RUN / "audit/qwen4b_teacher_part_screen.jsonl"
UNHEADED_SCREEN = RUN / "audit/qwen4b_teacher_unheaded_screen.jsonl"
ACCEPTED = RUN / "audit/qwen4b_teacher_conversion_accepted.jsonl"
REJECTED = RUN / "audit/qwen4b_teacher_conversion_rejected.jsonl"
REPORT = RUN / "audit/qwen4b_teacher_conversion_report.json"
TOKENIZER = ROOT.parents[2] / "ChatGPT/R1/outputs/instruct4b-2026-10-06/exp21_06b/data/q06_mv_tokenizer"

# First text that belongs to Conclusion, after exactly two independent Parts.
# Later independent Parts belong there too; their mathematics stays verbatim.
MERGE_START = {
    "gsm8k-train/532": "Part 3: Calculate the number of golf balls Chris buys",
    "gsm8k-train/3572": "Combining the results:",
    "gsm8k-train/5956": "Part 3: Compute the savings",
    "gsm8k-train/3099": "Combined total minutes:",
    "gsm8k-train/3381": "Combine the parts:",
    "gsm8k-train/7034": "Part 3: Calculate the total weight of bluegills",
    "gsm8k-train/3238": "Total time is the sum",
    "gsm8k-train/6283": "Part 3: Limo Charter",
    "gsm8k-train/3526": "Part 3: Identify the cheaper fruit",
    "math-train/150": "Part 3: Multiply the results",
    "math-train/164": "**Final Calculation:**",
    "math-train/1491": "Part 3: Simplify the fraction",
    "math-train/2299": "**Combining the Results**",
    "math-train/285": "Now that we have the two solutions",
    "math-train/2240": "**Final Calculation:**",
    "math-train/6376": "### Part 3: Evaluate the third term",
    "math-train/737": "**Part 3:** Multiply the inner terms",
    "math-train/7138": "**Part 3:** Compute $z$",
}

# Exact, inclusive source-text span boundaries: Path 1, Path 2, Conclusion.
# The source thought has much repeated checking; select only the first useful
# computation of each independent quantity and a source-written combination.
UNHEADED_SPANS = {
    "gsm8k-train/2788": (
        ("For the electric and water bill:", "So that's $1,200."),
        ("Starting with house rental and food:", "so total is 1020."),
        ("Total expenses: 640 + 380 = 1020.", "6000 - 3720 = 2280. Yes, that seems correct.")),
    "gsm8k-train/7121": (
        ("First, I need to figure out her total revenue", "So, her total revenue is $500."),
        ("Next, I need to calculate her total expenses.", "So, her total expenses are $200."),
        ("Now, to find out how much she makes after expenses,", "Therefore, Jenny makes $300 after factoring in her expenses.")),
    "gsm8k-train/6393": (
        ("So, 18 shirts plus 12 pants is 30.", "So, 18 shirts plus 12 pants is 30."),
        ("Then 17 sweaters and 13 jeans make 30 more.", "Then 17 sweaters and 13 jeans make 30 more."),
        ("So total clothes are 30 + 30 = 60 items.", "So the answer should be 3 hours.")),
    "gsm8k-train/3242": (
        ("First, I need to calculate the total cost for the ice cream.", "So the ice cream cost $75 total."),
        ("Next, the pudding.", "So the pudding cost $10 total."),
        ("Now, to find out how much more", "So the answer should be $65.")),
    "math-train/252": (
        ("Calculating 8 squared is 64.", "Calculating 8 squared is 64."),
        ("Then (-15) squared is 225.", "Then (-15) squared is 225."),
        ("Adding those together: 64 + 225 equals 289.", "So the distance between the two points should be 17 units.")),
    "math-train/3495": (
        ("So, let's compute the left-hand limit as x approaches n.", "Plugging n into x² + 2 gives n² + 2."),
        ("Now the right-hand limit as x approaches n.", "So the right-hand limit is 2n + 5."),
        ("Since the function is continuous at x = n,", "So adding them together: 3 + (-1) = 2.")),
    "math-train/3186": (
        ("Original pyramid: base edge is 12 cm,", "So original volume is 384."),
        ("Then the smaller pyramid has base edges of 6 cm.", "times 4 is 48 cm³."),
        ("Therefore, subtracting 48 from 384 gives 336 cm³ for the frustum.",
         "Therefore, subtracting 48 from 384 gives 336 cm³ for the frustum.")),
    "math-train/7356": (
        ("First, multiply the elements on the main diagonal:", "So -5 times -4 is 20."),
        ("Then, the other product is the off-diagonal elements:", "Multiplying those gives 12."),
        ("Now subtract the second product from the first.", "Therefore, the determinant should be 8.")),
    "math-train/6059": (
        ("First, let me handle the numerator.", "So the numerator simplifies to 13."),
        ("Now the denominator is the square root of (16 + 9).", "So the denominator simplifies to 5."),
        ("So putting it all together, r is 13 divided by 5.", "13/5 is already in its simplest form.")),
    "math-train/4349": (
        ("So the real part squared is (-4)² which is 16.", "So the real part squared is (-4)² which is 16."),
        ("Then the imaginary part is 7/6,", "so that's 49/36."),
        ("Original complex number: -4 + (7/6)i.", "So the modulus is 25/6.")),
    "math-train/1245": (
        ("First, I'll distribute each term in the first polynomial", "That would give me x⁴, 2x³, and 2x²."),
        ("Next, I'll move to the second term in the first polynomial,", "2 * 2 is 4."),
        ("So, putting all those terms together, I have:", "which simplifies to x⁴ + 4.")),
    "math-train/4083": (
        ("Since the coefficient of x² is negative, the parabola opens downward.",
         "Since the coefficient of x² is negative, the parabola opens downward."),
        ("Original quadratic: -12x² + 3x -5.", "Therefore, no real roots."),
        ("Since it opens downward and has no real roots,", "true for all real numbers.")),
    "math-train/958": (
        ("Starting with the constants: 2 + 8 -14.", "So the constant term is -4."),
        ("Next, the x terms: -4x +10x +16x.", "So the x squared terms add up to zero?"),
        ("So putting it all together, the simplified expression is -4 +22x +0x².",
         "So that would be 22x -4.")),
    "math-train/424": (
        ("First, I'll take the 2x from the first binomial", "2x times 5 is 10x."),
        ("Then, I need to do the same with the 3", "3 times 5 is 15."),
        ("Now, let me write down all those terms:", "2x² + 13x + 15.")),
    "math-train/3292": (
        ("6 squared is 36", "6 squared is 36"),
        ("8 squared is 64.", "8 squared is 64."),
        ("Adding them together, 36 + 64 equals 100.", "So, the circumference should be 10π cm.")),
    "math-train/212": (
        ("First, I'll take the x from the first parenthesis", "Okay, that part seems straightforward."),
        ("Next, I need to multiply the 2 from the first parenthesis", "Got that."),
        ("Now, let me write down all those terms:", "x squared plus 7x plus 10.")),
    "math-train/4465": (
        ("the x-coordinate is (14)/2 = 7", "the x-coordinate is (14)/2 = 7"),
        ("the y-coordinate is 4/2 = 2.", "the y-coordinate is 4/2 = 2."),
        ("Therefore, the center should be at (7, 2).", "Therefore, the center should be at (7, 2).")),
    "math-train/1514": (
        ("Starting with the x-coordinate equation:", "x = 5"),
        ("Now for the y-coordinate:", "y = 7"),
        ("So the other endpoint should be (5,7).", "So the other endpoint should be (5,7).")),
}

# A few calculations have their input substitution and result in separate
# sentences. Keep both exact source fragments in the corresponding Path.
UNHEADED_INPUT_SPANS = {
    "math-train/252": (
        ("the difference in x-coordinates is 8 - 0, which is 8.",
         "the difference in x-coordinates is 8 - 0, which is 8."),
        ("The difference in y-coordinates is 0 - 15, which is -15.",
         "The difference in y-coordinates is 0 - 15, which is -15.")),
    "math-train/4465": (
        ("the x-coordinate of the center would be (5 + 9)/2",
         "the x-coordinate of the center would be (5 + 9)/2"),
        ("the y-coordinate would be (0 + 4)/2.",
         "the y-coordinate would be (0 + 4)/2.")),
}

PART = re.compile(r"(?m)^(?:#{1,6}\s*)?(?:\*\*)?Part\s+(\d+)\s*:\s*([^\n]*)")
FINAL = re.compile(r"(?m)^Final Answer:\s*.+$")


def read_jsonl(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ids = [row.get("id") for row in rows]
    if not rows or any(not isinstance(key, str) for key in ids) or len(set(ids)) != len(ids):
        raise ValueError(f"empty, invalid, or duplicate IDs: {path}")
    return rows


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def title(match: re.Match[str], segment: str) -> str:
    heading = match.group(2).strip().strip("*").strip()
    if heading:
        return heading
    lines = [line.strip().strip("*# ") for line in segment[match.end() - match.start():].splitlines()]
    return next((line for line in lines if line and line != "---"), "")


def checked_final(final: str, row: dict) -> None:
    line = FINAL.match(final)
    require(line is not None and line.start() == 0, "missing external Final Answer")
    observed = line.group(0).split(":", 1)[1].strip().rstrip(".").strip("$").strip()
    expected = row["gold"]
    if row["id"] == "gsm8k-train/7034":
        match = re.search(r"=\s*([-+]?\d+(?:\.\d+)?)\s+pounds$", observed)
        require(match is not None, "cannot read weight from external answer")
        observed = match.group(1)
    observed = re.sub(r"^\\boxed\{(.*)\}$", r"\1", observed)
    observed = observed.replace(r"\dfrac", r"\frac")
    if row["id"] in {"math-train/7138", "math-train/4465", "math-train/1514"}:
        left = [part.strip() for part in observed[1:-1].split(",")]
        right = [part.strip() for part in expected[1:-1].split(",")]
        require(len(left) == len(right) == (3 if row["id"] == "math-train/7138" else 2),
                "coordinate answer has wrong arity")
        pairs = zip(right, left)
    else:
        pairs = [(expected, observed)]
    for gold, candidate in pairs:
        require(bool(verify_math(parse_math(f"${gold}$"), parse_math(f"${candidate}$"))),
                f"math_verify rejected external answer: {candidate!r} vs {gold!r}")


def convert(row: dict, screen: dict, tokenizer: AutoTokenizer) -> tuple[dict, int]:
    problem_id = row["id"]
    require(screen.get("part_screen") == "accepted" and screen.get("independent_parts") is True
            and screen.get("final_answer_correct") is True
            and screen.get("part_heading_placement") == "outside_think", "screen did not accept independent Parts")
    require(row.get("clean") is True and row.get("correct") is True and row.get("truncated") is False,
            "source grade is not clean, correct, and complete")
    raw = row["output"]
    require(raw.count("<think>") == raw.count("</think>") == 1, "source think wrapper is malformed")
    before, external = raw.split("</think>", 1)
    require(before.startswith("<think>") and not ANY_TAG.search(raw), "source contains unexpected tags")
    answers = list(FINAL.finditer(external))
    require(len(answers) == 1, "source needs exactly one external Final Answer")
    body, final = external[:answers[0].start()], external[answers[0].start():]
    checked_final(final, row)
    headings = list(PART.finditer(body))
    require(len(headings) >= 2 and [headings[0].group(1), headings[1].group(1)] == ["1", "2"],
            "missing first two numbered Parts")
    marker = MERGE_START.get(problem_id)
    require(marker is not None and body.count(marker) == 1, "missing unique reviewed merge boundary")
    split = body.index(marker)
    require(headings[1].start() < split, "merge boundary precedes second Part")
    preamble = body[:headings[0].start()]
    first = body[headings[0].start():headings[1].start()]
    second = body[headings[1].start():split]
    conclusion = body[split:]
    require(preamble + first + second + conclusion == body, "source Part text reconstruction changed")
    require(first.strip() and second.strip() and conclusion.strip(), "empty Path or Conclusion")
    require(not PART.search(second[headings[1].end() - headings[1].start():]), "second Path contains another Part")
    outlines = [title(headings[0], first), title(headings[1], second)]
    require(all(outlines), "cannot derive both outlines from source Parts")
    if problem_id == "gsm8k-train/7034":
        # Its original conclusion exists only in Final Answer; copy that math.
        conclusion += "\n" + final.split(":", 1)[1].strip() + "\n"
    block = ("<Parallel>\n<Goal>\n"
             + "".join(f"<Outline>{index}: {outline}</Outline>\n" for index, outline in enumerate(outlines, 1))
             + "</Goal>\n"
             + f"<Path>\n1: {first.strip()}\n</Path>\n"
             + f"<Path>\n2: {second.strip()}\n</Path>\n"
             + f"<Conclusion>\n{conclusion.strip()}\n</Conclusion>\n</Parallel>")
    response = "<think>\n" + preamble.strip() + ("\n\n" if preamble.strip() else "") + block + "\n</think>\n" + final
    parsed = parse(response)
    require(parsed["valid"] and len(parsed["blocks"]) == 1 and parsed["blocks"][0]["numbered"],
            "invalid numbered Parallel grammar")
    close = response.index("</think>")
    require(parsed["blocks"][0]["end"] < close and not ANY_TAG.search(response[close:]),
            "Parallel tag outside think")
    require(response[close + len("</think>\n"):] == final and response.count("Final Answer:") == 1,
            "external Final Answer changed")
    require(final.startswith("Final Answer:") and not PART.search(final), "Part text remains outside think")
    require(problem_id == screen["id"] and problem_id.startswith(row["source"] + "-train/"),
            "source ID mismatch")
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": row["prompt"]}],
                                           add_generation_prompt=True, tokenize=False, enable_thinking=True)
    length = len(tokenizer.encode(prompt + response + tokenizer.eos_token, add_special_tokens=False))
    require(length <= 4096, f"4096-token limit exceeded: {length}")
    return ({"id": problem_id, "source": row["source"], "question": row["question"],
             "answer": row["gold"], "answer_type": row["answer_type"],
             "teacher": "qwen3_4b", "status": "converted_for_review_not_sft",
             "screen_reason": screen["reason"], "source_raw_response": raw, "response": response,
             "source_id": problem_id, "source_work_placement": "outside_think",
             "total_tokens_with_source_prompt": length,
             "answer_verification": "verified_math_verify"}, length)


def source_span(thought: str, boundaries: tuple[str, str]) -> tuple[str, int, int]:
    start, finish = boundaries
    require(thought.count(start) == 1, f"nonunique source span start: {start!r}")
    first = thought.index(start)
    last = thought.find(finish, first)
    require(last >= first, f"missing source span end: {finish!r}")
    result = thought[first:last + len(finish)]
    require(result.strip() and "Final Answer:" not in result, "empty span or internal Final Answer")
    return result, first, last + len(finish)


def convert_unheaded(row: dict, screen: dict, tokenizer: AutoTokenizer) -> tuple[dict, int]:
    problem_id = row["id"]
    require(screen.get("decision") == "accept" and screen.get("independent_paths") is True
            and screen.get("candidate_work_placement") == "inside_think"
            and screen.get("think_closed") is True, "screen did not accept inside-think paths")
    require(row.get("clean") is True and row.get("correct") is True and row.get("truncated") is False,
            "source grade is not clean, correct, and complete")
    raw = row["output"]
    require(raw.count("<think>") == raw.count("</think>") == 1 and not ANY_TAG.search(raw),
            "source think wrapper or tags are malformed")
    before, external = raw.split("</think>", 1)
    require(before.startswith("<think>"), "source think opening is malformed")
    answers = list(FINAL.finditer(external))
    require(len(answers) == 1, "source needs exactly one external Final Answer")
    checked_final(external[answers[0].start():], row)
    plan = UNHEADED_SPANS.get(problem_id)
    require(plan is not None, "no reviewed inside-think span plan")
    thought = before[len("<think>"):]
    spans = [source_span(thought, pair) for pair in plan]
    inputs = [source_span(thought, pair) for pair in UNHEADED_INPUT_SPANS.get(problem_id, ())]
    selected = spans + inputs
    require(all(a[2] <= b[1] or b[2] <= a[1]
                for index, a in enumerate(selected) for b in selected[index + 1:]),
            "selected source spans overlap")
    first, second, conclusion = [span[0] for span in spans]
    if inputs:
        first, second = inputs[0][0] + "\n" + first, inputs[1][0] + "\n" + second
    outlines = screen.get("proposed_split", "").split(" | ")
    require(len(outlines) == 2 and all(outlines), "screen has no two-part outline")
    if problem_id == "gsm8k-train/2788":
        outlines.reverse()  # Source computes proportional bills before fixed bills.
    block = ("<Parallel>\n<Goal>\n"
             + f"<Outline>1: {outlines[0]}</Outline>\n<Outline>2: {outlines[1]}</Outline>\n"
             + "</Goal>\n"
             + f"<Path>\n1: {first}\n</Path>\n"
             + f"<Path>\n2: {second}\n</Path>\n"
             + f"<Conclusion>\n{conclusion}\n</Conclusion>\n</Parallel>")
    response = "<think>\n" + block + "\n</think>" + external
    parsed = parse(response)
    require(parsed["valid"] and len(parsed["blocks"]) == 1 and parsed["blocks"][0]["numbered"],
            "invalid numbered Parallel grammar")
    close = response.index("</think>")
    require(parsed["blocks"][0]["end"] < close and not ANY_TAG.search(response[close:]),
            "Parallel tag outside think")
    require(response[close + len("</think>"):] == external and problem_id == screen["id"]
            and problem_id.startswith(row["source"] + "-train/"),
            "external response or source ID changed")
    prompt = tokenizer.apply_chat_template([{"role": "user", "content": row["prompt"]}],
                                           add_generation_prompt=True, tokenize=False, enable_thinking=True)
    length = len(tokenizer.encode(prompt + response + tokenizer.eos_token, add_special_tokens=False))
    require(length <= 4096, f"4096-token limit exceeded: {length}")
    return ({"id": problem_id, "source": row["source"], "question": row["question"],
             "answer": row["gold"], "answer_type": row["answer_type"],
             "teacher": "qwen3_4b", "status": "converted_for_review_not_sft",
             "screen_reason": screen["reason"], "source_raw_response": raw, "response": response,
             "source_id": problem_id, "source_work_placement": "inside_think",
             "total_tokens_with_source_prompt": length,
             "answer_verification": "verified_math_verify"}, length)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, default=TOKENIZER)
    args = parser.parse_args()
    require(args.tokenizer.is_dir(), f"missing tokenizer: {args.tokenizer}")
    rows, screens, unheaded = read_jsonl(SOURCE), read_jsonl(SCREEN), read_jsonl(UNHEADED_SCREEN)
    require((len(rows), len(screens), len(unheaded)) == (320, 57, 106), "source or screen row count changed")
    by_id = {row["id"]: row for row in screens}
    unheaded_by_id = {row["id"]: row for row in unheaded}
    source_ids = {row["id"] for row in rows}
    require(not set(by_id) & set(unheaded_by_id), "headed/unheaded screens overlap")
    require(set(by_id) | set(unheaded_by_id) <= source_ids, "screen ID absent from graded source")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    accepted, rejected, lengths = [], [], []
    for row in rows:
        headed_screen = by_id.get(row["id"])
        unheaded_screen = unheaded_by_id.get(row["id"])
        screen = headed_screen or unheaded_screen
        if headed_screen and headed_screen.get("part_screen") == "accepted":
            converter, screen_kind = convert, "headed"
        elif unheaded_screen and unheaded_screen.get("decision") == "accept":
            converter, screen_kind = convert_unheaded, "unheaded"
        else:
            rejected.append({"id": row["id"], "reason": "not accepted by either independent-path screen",
                             "screen_status": (headed_screen.get("part_screen") if headed_screen else
                                               unheaded_screen.get("decision") if unheaded_screen else "not_screened"),
                             "screen_reason": screen.get("reason") if screen else None})
            continue
        try:
            converted, length = converter(row, screen, tokenizer)
        except (ValueError, KeyError, TypeError) as error:
            rejected.append({"id": row["id"], "reason": str(error), "screen_status": "accepted",
                             "screen_kind": screen_kind, "screen_reason": screen.get("reason")})
            continue
        accepted.append(converted)
        lengths.append(length)
    for path, records in ((ACCEPTED, accepted), (REJECTED, rejected)):
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records))
    report = {"status": "converted_for_review_not_sft", "graded_rows": len(rows),
              "headed_screen_rows": len(screens), "unheaded_screen_rows": len(unheaded),
              "headed_screen_accepted": sum(s.get("part_screen") == "accepted" for s in screens),
              "unheaded_screen_accepted": sum(s.get("decision") == "accept" for s in unheaded),
              "converted": len(accepted), "rejected": len(rejected),
              "converted_by_source_placement": dict(collections.Counter(row["source_work_placement"] for row in accepted)),
              "rejected_by_screen_status": dict(collections.Counter(row["screen_status"] for row in rejected)),
              "converted_ids": [row["id"] for row in accepted],
              "max_total_tokens_with_source_prompt": max(lengths, default=None),
              "verification": "one numbered two-path block inside think; exact external Final Answer; verbatim source computations; math_verify; Qwen tokenizer <=4096",
              "command": "uv run --no-project --with 'transformers>=4.50,<5' --with 'math-verify>=0.8,<1' --with jinja2 python scripts/exp21/convert_qwen4b_teacher.py",
              "conclusion": "Only screen-accepted independent headed or inside-think rows were converted; data remains outside SFT.",
              "source": str(SOURCE.relative_to(ROOT)), "headed_screen": str(SCREEN.relative_to(ROOT)),
              "unheaded_screen": str(UNHEADED_SCREEN.relative_to(ROOT)),
              "tokenizer": str(args.tokenizer)}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("headed_screen_accepted", "unheaded_screen_accepted", "converted", "rejected", "max_total_tokens_with_source_prompt")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
