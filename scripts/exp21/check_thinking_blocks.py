"""Focused checks for locating blocks inside Qwen3's thinking span."""
from mv_format import parse
from score_thinking_blocks import thought_span


BLOCK = ("<Parallel><Goal><Outline>1: a</Outline><Outline>2: b</Outline></Goal>"
         "<Path>1: a</Path><Path>2: b</Path><Conclusion>both</Conclusion></Parallel>")


def check():
    for prompt, output in (
        ("assistant\n", f"<think>{BLOCK}</think>Final Answer: 3"),
        ("assistant\n<think>\n", f"{BLOCK}</think>Final Answer: 3"),
    ):
        thought, final, valid = thought_span(prompt, output)
        assert valid and thought == BLOCK and final == "Final Answer: 3"
        parsed = parse(thought)
        assert parsed["valid"] and parsed["blocks"][0]["numbered"]
    assert not thought_span("assistant\n", f"<think>{BLOCK}")[2]
    assert not thought_span("assistant\n", f"<think><think>{BLOCK}</think>")[2]
    thought, final, valid = thought_span("assistant\n", f"<think>plain</think>{BLOCK}")
    assert valid and not parse(thought)["valid"] and parse(final)["valid"]
    print("thinking span and block placement: pass")


if __name__ == "__main__":
    check()
