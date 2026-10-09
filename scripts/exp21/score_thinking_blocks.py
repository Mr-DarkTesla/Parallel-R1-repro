"""Score Multiverse blocks inside the generated Qwen3 <think> span.

Run scripts/bench/score.py first for answer accuracy and tokenizer-based forwards.
Usage: python score_thinking_blocks.py DUMP_JSONL SCORE_ROWS_JSONL OUT_JSON OUT_ROWS_JSONL DECODER
DECODER is sequential, masked, or branch; branch inserts some Path tags.
"""
import json
import sys

from mv_format import parse


def read_rows(path):
    with open(path) as file:
        return [json.loads(line) for line in file]


def thought_span(prompt, output):
    prefix_opens = prompt.rfind("<think>") > prompt.rfind("</think>")
    start = output.find("<think>")
    if prefix_opens:
        body_start = 0
        opened = start < 0
    else:
        body_start = start + len("<think>") if start >= 0 else 0
        opened = start >= 0
    close = output.find("</think>", body_start)
    closed = opened and close >= 0
    thought = output[body_start:close if closed else len(output)]
    outside = output[close + len("</think>"):] if closed else ""
    wellformed = closed and output.count("<think>") + int(prefix_opens) == 1 and output.count("</think>") == 1
    return thought, outside, wellformed


def main():
    dump_path, score_path, out_path, rows_path, decoder = sys.argv[1:6]
    assert decoder in ("sequential", "masked", "branch")
    generations, scored = read_rows(dump_path), read_rows(score_path)
    assert len(generations) == len(scored)
    results = []
    for generated, row in zip(generations, scored):
        assert generated["input"] == row["input"]
        thought, final, wellformed = thought_span(generated["input"], generated["output"])
        inside, outside = parse(thought), parse(final)
        numbered = inside["valid"] and all(block["numbered"] for block in inside["blocks"])
        results.append({
            "problem_id": row["problem_id"], "problem": row["problem"], "source": row["source"],
            "input": row["input"], "sample": row["sample"], "decoder": decoder,
            "acc_robust": bool(row["acc_robust"]), "think_wellformed": wellformed,
            "think_has_parallel": "<Parallel>" in thought,
            "think_full_block": bool(wellformed and inside["valid"] and inside["blocks"]),
            "think_numbered_block": bool(wellformed and numbered and inside["blocks"]),
            "think_started_blocks": max(thought.count("<Parallel>"), thought.count("</Parallel>")),
            "think_valid_blocks": sum(block["numbered"] for block in inside["blocks"]),
            "outside_think_tags": outside["tags"],
            "tokens": int(row["tokens"]), "forward_passes": int(row["forward_passes"]),
            "truncated": bool(row["truncated"]),
        })
    with open(rows_path, "w") as file:
        for row in results:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {}
    for source in sorted(set(row["source"] for row in results)):
        group = [row for row in results if row["source"] == source]
        share = lambda field: round(100 * sum(bool(row[field]) for row in group) / len(group), 2)  # noqa: E731
        summary[source] = {
            "responses": len(group), "problems": len(set(row["problem_id"] for row in group)),
            "accuracy_robust": share("acc_robust"), "think_wellformed": share("think_wellformed"),
            "think_has_parallel": share("think_has_parallel"),
            "think_full_block": share("think_full_block"),
            "think_numbered_block": share("think_numbered_block"),
            "outside_think_tags_responses": round(100 * sum(row["outside_think_tags"] > 0 for row in group) / len(group), 2),
            "truncated": share("truncated"),
            "mean_tokens": round(sum(row["tokens"] for row in group) / len(group), 1),
            "mean_forward_passes": round(sum(row["forward_passes"] for row in group) / len(group), 1),
        }
    with open(out_path, "w") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
