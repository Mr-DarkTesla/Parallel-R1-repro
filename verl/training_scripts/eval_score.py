"""Use the original answer verifiers without a parallel-format reward multiplier."""

import re

from verl.utils.reward_score import default_compute_score
from verl.utils.reward_score.gsm8k_add_special_token_reward import check_parallel_thinking_format


def compute_score(data_source, solution_str, solution_str_with_special_tokens, ground_truth, extra_info=None):
    result = default_compute_score(
        data_source, solution_str, solution_str_with_special_tokens, ground_truth,
        extra_info={**(extra_info or {}), "reward_method": "accuracy_reward"},
    )
    if not isinstance(result, dict):
        result = {"score": result, "acc": result}
    tags = re.findall(r"</?(?:Parallel|Path|Summary)>", solution_str_with_special_tokens)
    stack = []
    format_ok = True
    for tag in tags:
        if not tag.startswith("</"):
            stack.append(tag[1:-1])
        elif not stack or stack.pop() != tag[2:-1]:
            format_ok = False
            break
    format_ok = format_ok and not stack
    return {
        **result,
        "data_source": data_source,
        "parallel": float("<Parallel>" in solution_str_with_special_tokens),
        "format": float(not check_parallel_thinking_format(solution_str_with_special_tokens)),
        "parallel_format": float(bool(tags) and format_ok),
        "format_error": float(bool(tags) and not format_ok),
        "no_tags": float(not tags),
    }
