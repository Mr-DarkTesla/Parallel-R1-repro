"""Second bounded Opus consultation: review exact mask/decode code, no data annotation."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from claude_call import call


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/21-qwen3-0.6b-multiverse/opus_consultation"
SYSTEM = """You are a careful code reviewer for LLM structured SFT. Review exact code before advising. Do not annotate or write reasoning traces, do not invent benchmark results, distinguish verified code facts from hypotheses. Respond in Russian. Prioritize correctness of train/inference match and cheap diagnostics."""


def excerpt(path, first, last):
    lines = (ROOT / path).read_text().splitlines()
    return f"{path}:{first}-{last}\n" + "\n".join(f"{i}: {lines[i-1]}" for i in range(first, last+1))


PARTS = [
    excerpt("verl/verl/utils/dataset/multiverse_structure.py", 1, 93),
    excerpt("scripts/exp21/masked_decode_state.py", 1, 78),
    excerpt("scripts/exp21/generate_masked_multiverse.py", 19, 54),
    excerpt("verl/verl/utils/dataset/parallel_thinking_sft_dataset.py", 393, 484),
    excerpt("verl/verl/trainer/fsdp_parallel_sft_trainer.py", 314, 332),
    excerpt("verl/verl/trainer/fsdp_parallel_sft_trainer.py", 348, 382),
    excerpt("verl/verl/trainer/fsdp_parallel_sft_trainer.py", 480, 501),
]
USER = """Follow-up on your prior consultation. We verified: (1) vLLM sequential generator uses skip_special_tokens=False, raw dumps visibly contain tags; (2) gold validator accepts 1077/1077 M1 and M2 training blocks and 1062/1062 M3, including numbering; (3) tokenizer maps all 10 tags to one token each; (4) every tag in rendered SFT targets is supervised, none masked; (5) rendered full lengths max 3838, none >4096; (6) actual train prompt with enable_thinking=True ends at '<|im_start|>assistant\\n' and response starts '<think>', so no doubled prefix. Model is constructed with default attention backend, not explicit flash_attention_2; dense 4D mask is passed. (7) Separate per-row LR implementation updates only 10 tag rows. BF16 export weight norms M1/M2/M3: tag rows 0.95-1.00, preexisting row p50/p99 0.936/1.158, old-row drift p50 <0.001, p99 <0.006. Thus large-norm/whole-matrix hypotheses do not fit. Tags drift ~0.2-0.3 in norm from initialization. (8) Training with 64*32=2048 presentations over 2251 rows containing 1077 primary tagged rows, which represent ~360 unique problems repeated ~3 times. (9) Masked pilot has no forced tag insertion; only sampled tokens are fed back.

Please review exact code below for a specific train/inference inconsistency. In particular inspect off-by-one behavior at Path boundaries, goal/path visibility, duplicated cache positions, attention mask row shape, and what happens if predicted number of paths is wrong. If no clear bug, say so. Then specify a minimal reproducible test comparing per-token logprobs of one gold val sample in full forward versus stepwise cached decoder, with numerical tolerance and code changes needed. Finally, rank the next 2 GPU experiments after the current 32-step matched M1/M2 pilots and untagged M2 control finish. Focus on accuracy and valid blocks jointly. Do not propose creating new annotations."""
USER += "\n\n" + "\n\n".join(PARTS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "code_prompt.json").write_text(json.dumps({"system": SYSTEM, "user": USER, "requested_model": "opus[1m]"}, ensure_ascii=False, indent=2) + "\n")
    result = call(SYSTEM, USER, timeout=900, model="opus[1m]", retries=1)
    result["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "code_response.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (OUT / "code_response.md").write_text(result.get("text", "") + "\n")
    print(json.dumps({"is_error": result.get("is_error"), "cost_usd": result.get("cost_usd"), "duration_ms": result.get("duration_ms"), "response_chars": len(result.get("text", "")), "output": str(OUT)}, ensure_ascii=False))
    if result.get("is_error") or not result.get("text"):
        print("Claude follow-up failed; see code_response.json", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
