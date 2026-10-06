"""Regression tests for scripts/filter_answer_first.py.  Run: python -m pytest scripts/tests -q"""
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from filter_answer_first import (answer_first, check_schema, group_key, matched_random_keep, parse,  # noqa: E402
                                 stratifier, untouched)

PROMPT = "Solve the following problem step by step.\n\nProblem: "


def block(*paths, summary="Both paths agree."):
    return "<Parallel>" + "".join(f"<Path>{p}</Path>" for p in paths) + f"</Parallel>\n<Summary>{summary}</Summary>\n\n"


def label(problem, answer):
    parts, malformed = parse(answer)
    return ("malformed", malformed, 0) if malformed else answer_first(PROMPT + problem, parts)[:3]


BEANS = "Susie has 572 beans. One-fourth are red, a third of the rest are white, half of the rest are green. How many green beans are there?"


def test_solution_before_first_block_is_answer_first():
    answer = ("The red beans are 572 / 4 = 143, the rest is 429, the white are 143, the rest is 286.\n\n"
              "So the number of green beans is 286 / 2 = 143.\n\n"
              + block("286 / 2 = 143", "572 / 8 = 143") + "Final Answer: 143")
    assert label(BEANS, answer) == ("answer_first", "block1", 1)


def test_coincidental_intermediate_value_is_not_answer_first():
    answer = ("Susie has 572 beans.\n\nOne-fourth of them are red, so red beans = (1/4) * 572 = 143.\n\n"
              + block("572 - 143 = 429", "572 * (3/4) = 429")
              + "White beans = (1/3) * 429 = 143, so 286 remain.\n\n"
              + block("429 - 143 = 286", "572 / 2 = 286")
              + "Then green beans = (1/2) * 286 = 143.\n\nFinal Answer: 143")
    assert label(BEANS, answer)[0] != "answer_first"


def test_value_given_in_question_is_not_evidence():
    problem = "Tom has 30 apples and buys none. How many apples does Tom have?"
    answer = "Tom has 30 apples.\n\n" + block("Nothing is added, so 30.", "0 bought, 30 + 0 = 30") + "Final Answer: 30"
    assert label(problem, answer) == ("clean", "", 0)


def test_answer_only_after_block_is_clean():
    problem = "Ann has 3 boxes with 4 pens each. How many pens does Ann have?"
    answer = "Ann has 3 boxes with 4 pens each.\n\n" + block("3 * 4 = 12", "4 + 4 + 4 = 12") + "Final Answer: 12"
    assert label(problem, answer) == ("clean", "", 0)


def test_answer_before_second_block_is_later_block():
    problem = "Ann has 3 boxes with 4 pens each and gives away 2 pens. How many pens does Ann have left?"
    answer = ("Ann has 3 boxes with 4 pens each.\n\n" + block("3 * 4 = 12", "4 + 4 + 4 = 12")
              + "She gives away 2, so Ann has 12 - 2 = 10 pens left.\n\n"
              + block("12 - 2 = 10", "Count down from 12 twice: 10.") + "Final Answer: 10")
    assert label(problem, answer) == ("answer_first", "later_block", 2)


def test_answer_stated_in_summary_then_repeated():
    problem = "Ann has 3 boxes with 4 pens each. How many pens does Ann have?"
    answer = (block("3 * 4 = 12", "4 + 4 + 4 = 12", summary="Both paths show that Ann has 12 pens.")
              + block("12 / 3 = 4 pens per box, consistent: 12", "3 + 3 + 3 + 3 = 12") + "Final Answer: 12")
    assert label(problem, answer) == ("answer_first", "later_block", 2)


def test_multi_paragraph_prefix_superseded_statement_is_not_answer_first():
    problem = "Ann has 3 boxes with 4 pens each and buys 2 more pens. How many pens does Ann have?"
    answer = ("First paragraph: Ann has 3 * 4 = 12 pens.\n\n"  # 12 is an intermediate, not the final 14
              "Second paragraph: she buys 2 more.\n\n" + block("12 + 2 = 14", "3 * 4 + 2 = 14") + "Final Answer: 14")
    assert label(problem, answer)[0] == "clean"
    answer = ("Ann has 3 * 4 = 12 pens, so Ann has 12 pens.\n\n"
              "Wait, she also buys 2, so 12 + 2 = 15.\n\n"  # a new value after the statement: not the final answer yet
              + block("12 + 3 = 15", "15") + "Final Answer: 12")
    assert label(problem, answer)[0] != "answer_first"


def test_multi_paragraph_prefix_with_answer_in_last_paragraph():
    problem = "Ann has 3 boxes with 4 pens each and buys 2 more pens. How many pens does Ann have?"
    answer = ("Ann has 3 boxes with 4 pens each.\n\nThat is 3 * 4 = 12 pens in boxes.\n\n"
              "Adding the 2 she buys, Ann has 12 + 2 = 14 pens.\n\n" + block("12 + 2 = 14", "3 * 4 + 2 = 14")
              + "Final Answer: 14")
    assert label(problem, answer) == ("answer_first", "block1", 1)


BOXES = "Ann has 20 pens, 4 per box. How many boxes does Ann have?"


def test_hypothesis_is_not_a_statement():
    answer = "Suppose Ann has 5 boxes.\n\n" + block("20 / 4 = 5", "4 + 4 + 4 + 4 + 4 = 20, so 5") + "Final Answer: 5"
    assert label(BOXES, answer)[0] != "answer_first"
    assert label(BOXES, answer.replace("Suppose Ann has", "Ann has"))[0] == "answer_first"


def test_operand_is_not_a_statement():
    answer = "Ann has boxes: 5 × 4 pens make 20 pens.\n\n" + block("20 / 4 = 5", "5") + "Final Answer: 5"
    assert label(BOXES, answer)[0] != "answer_first"
    assert label(BOXES, answer.replace("5 × 4 pens make 20 pens", "5")) == ("answer_first", "block1", 1)


def test_malformed_rows():
    problem = "How many pens?"
    assert label(problem, "No tags. Final Answer: 3") == ("malformed", "no_parallel", 0)
    assert label(problem, "<Parallel><Path>1</Path><Path>2</Path></Parallel>\n<Summary>open\n\nFinal Answer: 3")[1] \
        == "malformed_tags"
    assert label(problem, "<Parallel><Path>a</Path></Parallel>\n<Summary>s</Summary>\nFinal Answer: 3")[1] == "malformed_tags"
    assert label(problem, block("3", " ") + "Final Answer: 3")[1] == "empty_path_or_summary"
    assert label(problem, block("3", "3") + "Final Answer: 3\n\nBut let's confirm.")[1] == "final_answer_not_last_line"


def test_schema_fails_closed():
    question = PROMPT + "How many pens?"
    row = {"index": 0, "output": "", "data_source": "x", "ability": "math", "reward_model": {},
           "prompt": [{"content": question, "role": "user"}],
           "extra_info": {"answer": "", "index": 0, "question": question, "reward_method": "", "split": "train"}}
    check_schema([row], row)
    with pytest.raises(SystemExit):
        check_schema([row], list(row) + ["extra_column"])
    with pytest.raises(SystemExit):
        check_schema([dict(row, prompt=[{"content": "other", "role": "user"}])], row)
    with pytest.raises(SystemExit):
        check_schema([row, row], row)


def test_number_variants_share_a_problem_group():
    assert group_key(PROMPT + "Ann has 3 pens.  How many?") == group_key(PROMPT + "Ann has 1,200 pens. How many?")


def test_random_control_matches_counts_in_every_joint_stratum():
    # Two structures per length range, and `kept` is skewed toward 3 blocks: matching deciles alone would not suffice.
    control = [{"row": i, "target_tokens": 100 + i, "parallel_blocks": 2 + i % 2, "paths": 4 + 2 * (i % 2)}
               for i in range(200)]
    kept = [m for m in control if m["parallel_blocks"] == 3 or m["row"] % 5 == 0]
    keep = matched_random_keep(control, kept, seed=0)
    assert keep == matched_random_keep(control, kept, seed=0)
    assert keep != matched_random_keep(control, kept, seed=1)
    stratum, _ = stratifier(control)
    kept_rows = [m for m in control if m["row"] in set(keep)]
    assert Counter(map(stratum, kept_rows)) == Counter(map(stratum, kept))
    structure = lambda m: (m["parallel_blocks"], m["paths"])  # noqa: E731
    assert Counter(map(structure, kept_rows)) == Counter(map(structure, kept))


def test_block_reaching_a_new_value_is_not_a_repeat():
    answer = "Ann has 20 / 4 = 5 boxes.\n\n" + block("Pens per pair of boxes: 8", "Half the pens: 10") + "Final Answer: 5"
    assert label(BOXES, answer) == ("ambiguous", "stated_then_block_reaches_new_value", 1)


def test_untouched_dev_drops_the_whole_group_of_an_inspected_row():
    dev = [{"row": 1, "group": "a"}, {"row": 2, "group": "b"}, {"row": 3, "group": "a"}, {"row": 4, "group": "c"}]
    assert untouched(dev, {3}) == [2, 4]
    with pytest.raises(SystemExit):
        untouched(dev, {9})  # an inspected row outside dev must not be silently ignored
