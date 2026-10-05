"""Use the original answer verifiers without a parallel-format reward multiplier."""

from verl.utils.reward_score import default_compute_score
from verl.utils.reward_score.gsm8k_add_special_token_reward import check_parallel_thinking_format


def compute_score(data_source, solution_str, solution_str_with_special_tokens, ground_truth, extra_info=None):
    result = default_compute_score(
        data_source, solution_str, solution_str_with_special_tokens, ground_truth,
        extra_info={**(extra_info or {}), "reward_method": "accuracy_reward"},
    )
    if not isinstance(result, dict):
        result = {"score": result, "acc": result}
    return {
        **result,
        "data_source": data_source,
        "parallel": float("<Parallel>" in solution_str_with_special_tokens),
        "format": float(not check_parallel_thinking_format(solution_str_with_special_tokens)),
    }
