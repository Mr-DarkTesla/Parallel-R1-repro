# Independent review: FINDING-parallel-dump-check.md

Reviewer: Claude (read-only). Code: worktree parallel-r1-instruct4b-filtered @ baad652. The 15r log header shows commit dbe704b.
`git diff baad652 dbe704b -- scripts verl` is empty, so both runs used the same eval code.
Pod evidence: B, files read only.

VERDICT: ACCEPT-WITH-CHANGES

The diagnosis is correct: the assertion fails on a correct rollout. Skipping the dump-input check for parallel is correct, but on its own it
leaves parallel runs with only a log grep. Replace the check with a parallel-specific output check (diff below) and plan the
meta.json/commit handling for reruns (section 2).

## 1. Is it a false failure? Yes.

- What the dump `input` is: `verl/verl/trainer/ppo/ray_trainer.py:703-705` (`_validate`) decodes
  `test_batch.batch["input_ids"]` with `skip_special_tokens=True`. That happens before the rollout, and those ids are popped and never
  replaced. They come from `verl/verl/utils/dataset/rl_dataset.py:261`:
  `apply_chat_template(messages, add_generation_prompt=True, tokenize=False)`, with no `enable_thinking`, so the default template.
  The agent loop's own prompt is returned as `batch["prompts"]` (`parallel_thinking_generation_v3/agent_loop.py:393`), but it is never dumped.
- What the rollout actually generated from:
  - The manager passes the parquet messages to the loop: `rl_dataset.py:311-312` (`raw_prompt = messages`, because
    `data.return_raw_chat=True` in `eval_rollout.sh:21`), then `parallel_thinking_generation_v3/agent_loop.py:290,300-302`.
  - The agent defaults to `parallel_thinking_agent_v3` (`agent_loop.py:284-285`).
  - The loop renders the prompt once, at `parallel_thinking_loop_v3.py:102-107`, with `**self.template_kwargs`.
  - Those kwargs are a class attribute set from the environment variable (`:90-92`). `run_eval.sh:51` exports
    `PARALLEL_ROLLOUT_ENABLE_THINKING=false`.
- Do the kwargs reach every generation call? Yes. No later call re-templates:
  - main continuation: `:262-266`, using `prompt_ids`
  - each path: `:346-350`, using `prompt_ids + [<Path>]`
  - summary: `:410-414`, using `prompt_ids + parallel_ids`

  All of them extend the same initial token list, so the empty think block, once in that list, is in every call.
- Log: 14f `gsm8k_dev.log:411` and `:452` (`... {'enable_thinking': False} [repeated 31x across cluster]`), so all 32 workers.
  15r: `:420`, `:462`, same. Neither log has a line with other kwargs.
- Symptom check on the dumps (1184 rows per arm):

  | | 14f | 15r |
  |---|---|---|
  | outputs containing `<think>` | 0 | 0 |
  | outputs containing `</think>` | 0 | 0 |
  | inputs ending `assistant\n`, no `<think>` | 1184 | 1184 |
  | outputs with `<Parallel>` | 1068 | 1090 |
  | outputs with `<Summary>` | 1172 | 1175 |
  | outputs ending `<|im_end|>` | 1183 | 1183 |

  Example ending: `...</Summary>\n\nJames pays $75.\n\nFinal Answer: 75<|im_end|>`.
  A Qwen3 hybrid model prompted without the empty think block normally starts with `<think>`. `<think>` is not a special token, and outputs
  are decoded with `skip_special_tokens=False` (`ray_trainer.py:754`), so it would show up in the dump. Nothing points to a thinking-mode prompt.
- Same template for both arms: `/work/runs/14-filtered/model` and `/work/runs/15-random-control/model` have the same `chat_template`.

## 2. Is the proposed change correct and sufficient? Correct; better with an output check.

- **score.py:** reads `input` only for row alignment (`scripts/bench/score.py:33-34`: the last 200 characters of the parquet prompt, tags removed, must
  appear in `input`). The dataset rendering contains the problem text, so this is unaffected. score.py strips `<|endoftext|>`/`<|im_end|>`
  and splits on `</think>` (`:36-37`), which is fine.
- **paired_compare.py, parallel vs parallel:** `check_aligned` compares `problem` and `input` (`paired_compare.py:74`). These are the dataset's
  default-template text from the same parquet with the same template, so they are equal across arms. Verified: 14f inputs == 15r inputs
  (True, 1184 rows).
- **paired_compare.py --cross-prompt:** skips `input` and `problem` and compares headers and problem text (`:57-66,74`). Unaffected.
- **Gap:** with the check skipped, parallel mode is gated only by "the expected line exists". The repo's verl stays unchanged, so the actual
  agent-loop prompt cannot be checked from the dump. Two cheap guards close most of the gap:
  1. Fail if any worker logged other kwargs (`{}` = unset, or `True`).
  2. Fail if any parallel output contains `<think>`. This is a symptom check, not proof, but it passes on both existing dumps.
- **Rerun consequences (not in the finding):**
  - Committing the fix changes HEAD. `run_eval.sh:79-81` then rejects every existing `$EVAL_OUT/<name>/meta.json` that has the old commit,
    including the finished `14f-dev-nothink`, `14f-dev-think`, `15r-dev-nothink` and `15r-dev-think`, if they are ever resumed under the new commit.
  - The `*-dev-par` dirs have no rows. Move each whole dir aside (`mv <dir> <dir>.stale-<date>`), then regenerate (~4 min per bench).
  - Finished runs stay comparable: `PROTOCOL` in `paired_compare.py:36` does not include `commit`.
  - All three arms (13-control, 14f, 15r) need the same fix commit, as the finding says.

### Recommended diff (scripts/instruct4b_eval/run_eval.sh)

```diff
@@ -122,2 +122,4 @@
         bash ../scripts/bench/eval_rollout.sh "$model" "$run/$bench" "$test" "$budget" >> "$log" 2>&1
-        grep -q "Parallel rollout chat template kwargs: {'enable_thinking': False}" "$log" || { echo "rollout template not non-thinking: $log"; exit 1; }
+        # every AgentLoopWorker must log the non-thinking kwargs; none may log others ({} = env unset)
+        grep -q "Parallel rollout chat template kwargs: {'enable_thinking': False}" "$log" \
+            && ! grep "Parallel rollout chat template kwargs:" "$log" | grep -vqF "{'enable_thinking': False}" \
+            || { echo "rollout template not non-thinking: $log"; exit 1; }
@@ -128,8 +130,15 @@
-    # the dumped prompts must be rendered in the requested mode (empty think block = non-thinking template)
+    # the dumped prompts must be rendered in the requested mode (empty think block = non-thinking template).
+    # parallel: the dump's input is RLHFDataset's default-template prompt (ray_trainer._validate decodes the dataset input_ids
+    # before the rollout), not the agent-loop prompt; that one is gated by the Ray-log check above. Here: no output opens a think block.
     python - "$generations" "$mode" <<'EOF'
 import sys
 import pandas as pd
-inputs, mode = pd.read_json(sys.argv[1], lines=True)["input"], sys.argv[2]
-empty_think = inputs.str.contains("<think>\n\n</think>", regex=False)
-assert (empty_think if mode != "thinking" else ~empty_think).all(), f"{(~empty_think).sum()} prompts without an empty think block ({mode})"
+dump, mode = pd.read_json(sys.argv[1], lines=True), sys.argv[2]
+if mode == "parallel":
+    thinking = dump["output"].str.contains("<think>", regex=False)
+    assert not thinking.any(), f"{thinking.sum()} parallel outputs with a think block"
+else:
+    empty_think = dump["input"].str.contains("<think>\n\n</think>", regex=False)
+    assert (empty_think if mode != "thinking" else ~empty_think).all(), f"{(~empty_think).sum()} prompts without an empty think block ({mode})"
 EOF
```

How the grep line works: if the first grep fails, the script stops. If it passes, `! grep ... | grep -vqF` fails when any kwargs line lacks
`{'enable_thinking': False}`, and the script stops. The "[repeated 31x]" line contains that text, so it passes.

Optional: a CPU test in `test_eval.py` that a parallel-mode dump whose `input` has no empty think block passes the check, and that an output
with `<think>` fails it.

## 3. Other blockers in the same logs: none

- **Configuration** (14f log :94-95, :136, :221, :233): `num_paths=2`, `max_path_response_length=16384`, `response_length=16384`,
  `truncation='left'`, `max_iterations_for_parallel_thinking=4` (eval_rollout.sh:35).
- **Errors:** `grep -ci 'traceback|error|warning: prompt length'` gives 0 in both logs.
- **Prompt length:** left_pad_lens are about 1757-1760 of 2000, so prompts are about 240 tokens. Nothing is truncated.
- **Budget:** the longest output after removing padding is 8101 characters (14f) and 5116 (15r), far below 16384 tokens. No output was cut by the budget.
- **One unterminated row per arm** (14f row 913, 15r row 834): output stops at `</Summary>` after the 4th parallel block. That is the
  `should_stop` iteration cap (`parallel_thinking_loop_v3.py:252-256`), the authors' setting and the same for both arms. It is scored as having
  no final answer. 1/1184 is not a blocker, but it should be counted (`no_final_answer`) when reading the results.
- **Answers use `Final Answer: N`, no `\boxed`.** score.py handles this. verl's own acc is 0.825 (14f) and 0.829 (15r), so scoring will work.
- **Dump size:** about 249 MB per bench, because responses are padded to 16384 with `<|endoftext|>`. score.py strips it. This is not a
  problem, but frozen-suite parallel runs will be similarly large.
