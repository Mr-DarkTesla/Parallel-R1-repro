"""Count exact SFT prompt+response lengths before applying max_length truncation.

Usage: python count_sft_tokens.py ROWS_JSONL TOKENIZER OUT_JSON
"""
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_sft import row  # noqa: E402


def main():
    rows = [json.loads(line) for line in open(sys.argv[1])]
    tok = AutoTokenizer.from_pretrained(sys.argv[2], local_files_only=True)
    result = []
    for r in rows:
        example = row("parallel_th", r)
        info = example["extra_info"]
        prompt = tok.apply_chat_template([{"role": "user", "content": info["question"]}],
                                         add_generation_prompt=True, tokenize=False)
        length = len(tok(prompt, add_special_tokens=False).input_ids)
        length += len(tok(info["answer"] + tok.eos_token, add_special_tokens=False).input_ids)
        result.append({"id": r["id"], "tokens": length})
    counts = [r["tokens"] for r in result]
    summary = {"count": len(result), "min_tokens": min(counts), "mean_tokens": round(sum(counts) / len(counts), 1),
               "max_tokens": max(counts), "over_4096": [r["id"] for r in result if r["tokens"] > 4096],
               "rows": result}
    Path(sys.argv[3]).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print({k: v for k, v in summary.items() if k != "rows"})


if __name__ == "__main__":
    main()
