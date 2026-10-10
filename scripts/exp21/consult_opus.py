"""One bounded technical consultation through the existing VK AI Proxy route."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from claude_call import call


OUT = Path("results/21-qwen3-0.6b-multiverse/opus_consultation")
SYSTEM = """You are an independent expert in LLM post-training, structured generation, and custom attention masks. Give critical, concrete advice. Separate observations from hypotheses. Do not assume the current experiment is valid merely because training ran. Prioritize minimal GPU-hours and matched dev comparisons. Do not propose using frozen test sets for model selection. Reply in Russian, concise but technical."""
USER = """Goal: fine-tune post-trained Qwen3-0.6B to produce a grammatically correct Multiverse block inside <think> with minimal accuracy loss. Format: <Parallel><Goal><Outline>...</Outline>...</Goal><Path>...</Path><Path>...</Path><Conclusion>...</Conclusion></Parallel>. New tag tokens have distinct initialization and embedding-row LR multiplier. During training, sibling Paths have independent attention/positions; at inference we tested both ordinary sequential and a custom sibling-masked generator. Budget and GPU time are constrained.

Measured results on dev, same prompts/tasks for matched models:
- C0 base Qwen, normal thinking: GSM8K 73.65%, MATH 69.09%, ARC 68.65%, MMLU-Pro 32.73%; special Multiverse prompt: 67.06, 68.26, 64.80, 32.83%; IFEval thinking 55.27%.
- M1: 367 Claude-written tagged tasks inside <think>, 2251 train/50 val including same own-Qwen correct thinking/no-thinking replay; 64 SFT steps, base lr 1e-5, tag multiplier 100. Normal thinking: 75.42/47.72/64.55/27.43; IFEval thinking 33.83. Special prompt accuracy: 29.39/13.38/54.10/19.72; full numbered valid block inside <think> only 0.17-1.69%. Sibling-masked same40 dev pilot: 27/40 valid, 12/40 correct.
- M2: same 367 tasks, Qwen's own correct no-thinking solution copied into <think> and Claude supplies only structure, exactly same steps/mix. Normal thinking: 74.83/62.03/68.73/36.04; IFEval thinking 40.67. Special prompt: 46.20/36.83/53.76/23.02; 0% valid blocks. Sibling-masked same40: 20/40 valid, 20/40 correct.
- M3: 180 Qwen-generated genuine correct thinking traces, rewritten/corrected to two independent tagged Paths inside <think>, human reviewed 30/30 after fixes, zero final-answer errors. 2232 train/48 val with same Qwen replay. 64 steps lr1e-5 tag multiplier100: normal thinking 48.82/34.75/60.79/36.24, IFEval 45.66; special prompt 19.51/9.34/49.67/19.32, valid inside-think 2.5-8.9%. Masked same40: 6/40 valid+correct. A lighter 16 steps lr3e-6 mult100: 0/40 valid, 28/40 correct, 4/40 truncated, ~1305 tokens average. A 64-step lr3e-6 mult300 masked pilot: 2/40 valid and 4/40 correct.
- Repeated failure: models often open <Parallel> but misnest/omit closing tags, collapse to very short wrong calculation or on light SFT ramble until truncation. Evaluation has same task prompts across variants; ordinary generator does not apply sibling masking, custom pilot does. Data are verified leak-free against our eval and full MATH test. All experiments use post-trained Qwen, BF16, max train len4096, batch32/micro4; answer types vary. The special evaluation prompt requests a Parallel block inside <think>; ordinary thinking eval uses standard prompting. IFEval has no imposed Final Answer marker.
- At this moment two matched M1/M2 32-step lr5e-6 mult100 jobs are running, each followed by same40 masked pilot. M2 control on exactly same texts without structural tags is being evaluated separately. Please do not assume their results.

Questions:
1. What are the 2-3 most likely root causes, ranked by evidence? In particular, how would you distinguish data/teacher-forcing issues, the custom attention/position implementation, loss masking, token initialization/tied embeddings, and decoding/prompt mismatch?
2. Give a concrete cheap diagnostic sequence (file-level/inference-level tests and at most 2 new GPU ablations) with pass/fail criteria. Include one test that catches train-inference mismatch on the same example, and one test that determines whether grammar loss or answer accuracy is the binding failure.
3. Recommend a revised training/inference recipe to target >=90% valid blocks inside <think> while retaining accuracy. State which changes are speculative. Should we use canonical short blocks, constrained tag decoding, staged training, higher proportion of tag supervision, masking at inference, or a separate planner? Consider fair comparison to untagged control.
4. Point out any methodological mistake in interpreting these metrics, especially the apparent masked 40 improvement versus full sequential dev.

Please be specific about what to inspect in code and what result would change your recommendation. Do not suggest spending more proxy budget on large data generation until diagnostics justify it."""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prompt.json").write_text(json.dumps({"system": SYSTEM, "user": USER, "requested_model": "opus[1m]"}, ensure_ascii=False, indent=2) + "\n")
    result = call(SYSTEM, USER, timeout=900, model="opus[1m]", retries=1)
    result["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "response.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (OUT / "response.md").write_text(result.get("text", "") + "\n")
    print(json.dumps({"is_error": result.get("is_error"), "cost_usd": result.get("cost_usd"), "duration_ms": result.get("duration_ms"), "response_chars": len(result.get("text", "")), "output": str(OUT)}, ensure_ascii=False))
    if result.get("is_error") or not result.get("text"):
        print("Claude consultation failed; see response.json", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
