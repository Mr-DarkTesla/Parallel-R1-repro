"""Make a paired dev prompt that reserves combination of Paths for Conclusion."""

import sys
from pathlib import Path

import pandas as pd

SOURCE = Path(sys.argv[1])
DEST = Path(sys.argv[2])
ANCHOR = "End your response with a line starting with Final Answer: followed by the final result."
EXTRA = ("Plan the split before writing it. Each Path solves only its own Outline. "
         "Do not make the final sum, difference, comparison, or choice inside a Path. "
         "Perform the combining step in Conclusion after seeing both Paths. "
         "Do not state a proposed final answer before Conclusion.\n\n")

DEST.mkdir(parents=True, exist_ok=True)
for name in ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10"):
    frame = pd.read_parquet(SOURCE / f"{name}.parquet")
    changed = frame.copy(deep=True)
    prompts = []
    for prompt in frame.prompt:
        assert len(prompt) == 1 and prompt[0]["role"] == "user"
        text = prompt[0]["content"]
        assert text.count(ANCHOR) == 1
        prompts.append([{"role": "user", "content": text.replace(ANCHOR, EXTRA + ANCHOR)}])
    changed["prompt"] = prompts
    assert changed.extra_info.tolist() == frame.extra_info.tolist()
    assert changed.reward_model.tolist() == frame.reward_model.tolist()
    changed.to_parquet(DEST / f"{name}.parquet", index=False)
print("prepared 40 paired questions with explicit Conclusion instruction")
