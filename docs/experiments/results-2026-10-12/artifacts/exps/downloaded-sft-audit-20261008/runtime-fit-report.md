# Runtime and training fit audit, 2026-10-08

Scope: read-only inspection of six Downloads files, the checked-out Qwen3 SFT loaders/config/trainer, and v3 inference loop. Full structural scan covers 5,000 rows in each GSM JSONL and the mixed 4,500 train / 500 validation rows in both JSONL and Parquet representations. No input edits, network requests, training, or production code changes. `runtime-fit-stats.json` contains file SHA-256 identities and complete counts; `runtime-fit-scan.py` reproduces them with local pyarrow.

## Schema and role compatibility

The current launch script `verl/training_scripts/sft_qwen3_06b.sh` selects `sft_qwen3_06b_seen` by default; the Unseen variant selects `sft_qwen3_06b`. Both inherit a 3072-token maximum and `truncation: error`. The Qwen3 base config expects `extra_info.question` and `extra_info.answer` (`verl/verl/trainer/config/sft_qwen3_06b.yaml:8`). Those columns do not exist in downloaded mixed Parquet.

For the existing mixed Parquet, direct schema compatibility requires these overrides, as well as the actual train/validation paths:

```yaml
data:
  prompt_key: problem
  response_key: response
  prompt_dict_keys: []
  response_dict_keys: []
```

`answer` is a short scalar reference, while `response` is the demonstration. Using `response_key: answer` would train only the final scalar. Metadata, `branch_count`, and `id` are not consumed by either single-turn loader. JSONL is not accepted directly: every built-in SFT loader calls `pandas.read_parquet`.

Both GSM datasets have one system/user/assistant triple in every row, with one shared system instruction per file. Mixed JSONL has user/assistant pairs, and its Parquet contains the same text columns without messages. The single-turn loaders construct exactly `[{role: user, content: prompt}]` and then append the response plus tokenizer EOS (`parallel_thinking_sft_dataset.py:379`, `sft_dataset.py:124`). Selecting only the GSM user content therefore discards its system instruction. Do not select real-GSM top-level `question` alone: its `problem` contains the long facts, while the messages user content is the full model input.

The built-in multiturn loader accepts system first and masks system/user loss. Converting GSM messages to a Parquet messages column and setting `data.multiturn.enable=true` preserves the role sequence. However, `create_sft_dataset` checks multiturn before `parallel_attention` (`fsdp_parallel_sft_trainer.py:607`), so this chooses `MultiTurnSFTDataset` with ordinary one-dimensional causal attention and sequential positions (`multiturn_sft_dataset.py:330`). Setting both options does not produce role-preserving Unseen training. Unseen needs a role-aware parallel loader/custom class, or a deliberately documented single-user serialization with matching inference input. `data.chat_template` cannot solve this because the trainer explicitly rejects a non-null override (`fsdp_parallel_sft_trainer.py:95`).

The tokenizer adds only the six exact tags `<Path>`, `</Path>`, `<Parallel>`, `</Parallel>`, `<Summary>`, `</Summary>` (`prepare_qwen3_parallel.py:23`). IDs such as `1:` are ordinary text. The v3 runtime validates six distinct single-token encodings (`parallel_thinking_loop_v3.py:72`); the SFT loader assumes them by taking `encode(tag)[0]` without equivalent validation.

## Whole-sequence length and truncation

Exact Qwen3 student token counts were not obtainable offline: no Qwen3 tokenizer was found in the repo/checkpoints, Downloads, the local caches, projects, Application Support, or temporary paths inspected. The tokenizers located were unrelated (GigaChat/BERT/test fixtures). No tokenizer was downloaded or substituted. Therefore counts over 3072, chat-template overhead, EOS identity, and the exact smallest fitting context remain unknown. Character counts below are descriptive and are not token estimates.

| Input | user + response characters, median | p95 | max |
|---|---:|---:|---:|
| real GSM | 6305 | 18145 | 139742 |
| realistic GSM | 5480 | 10308 | 16207 |
| mixed train | 614 | 889 | 1719 |
| mixed validation | 610 | 858 | 1648 |

These exclude system content, the chat template, and EOS. The real-GSM prompt alone reaches 136141 characters. The large tail requires an actual student-token preflight before claiming 3072 compatibility.

The maximum applies to the concatenated prompt and *entire* response, summing all paths, summaries, and rounds (`parallel_thinking_sft_dataset.py:401-422`). Repeated branch position IDs do not reduce stored input length or the 3072 limit. With current settings an oversized row raises; there is no automatic filtering or silent truncation. Changing to right truncation can drop a path closure, summary, later rounds, or final answer. The active mask finalizes sibling exclusion only when it encounters `</Parallel>` (`parallel_thinking_sft_dataset.py:164`), so cutting before this closure leaves the unfinished block causal. The position parser also indexes a path end after scanning to sequence end, which can raise on an unfinished path (`parallel_thinking_sft_dataset.py:349`). Left truncation keeps original `prompt_length` and can apply prompt-loss masking and structure parsing to wrong offsets. Neither mode is a safe whole-chain conversion.

Required future preflight: tokenize the role-preserving prefix with the exact saved student tokenizer/template; tokenize the full response and EOS using the selected loader contract; report per-file and per-round total/assistant lengths and count every row above the chosen maximum. Retain `truncation:error`. Filter whole examples or regenerate shorter verified chains if a context cap remains; do not present a clipped chain as a valid demonstration. Raising context is an implementation/resource choice requiring actual model and memory validation.

## Mask and position fit

Unseen chooses `ParallelThinkingSFTDataset`; Seen chooses `SFTDataset`. The Unseen loader applies the active `generate_parallel_thinking_reasponse_mask`, excludes direct attention between sibling `<Path>...</Path>` spans, and repeats positions for paths within each block. Summaries and later sequential reasoning can attend all completed paths; following rounds can use earlier shared summaries (`parallel_thinking_sft_dataset.py:124-174`, `:297-368`). Sequential multi-round blocks are supported; nested blocks are not established as supported by this scanner.

Every parallel block in the two GSM inputs has whitespace between sibling paths: 8524/8524 real-GSM and 8250/8250 realistic-GSM blocks. All characters outside paths within these blocks are whitespace. Mixed input uses contiguous path spans and has no such separators.

This layout exposes two current Unseen defects. Sibling path spans are mutually masked, but inter-path newline tokens are outside both spans. Such a newline can attend a preceding sibling, and the later sibling can attend the newline. Thus direct masking does not guarantee indirect branch isolation. Also, `compute_structured_position_ids` initializes all nonpad positions to the prompt length and only assigns path spans inside `<Parallel>`; it skips these separator tokens, leaving them at that initial position (`parallel_thinking_sft_dataset.py:309-311`, `:333-356`).

Executed reproduction: `runtime-fit-mask-witness.py` AST-loads these two **unchanged actual methods** from the checked-out source and executes them with cached local Torch 2.6.0 and Python 3.12 on synthetic single-token IDs. In its two-path example, direct B-to-A attention is false, separator-to-A attention is true, and B-to-separator attention is true. The inter-path separator position is 2 (prompt length), while both path openers correctly receive 4 (fork-local start). The compact example has no such separator. The JSON witness records the actual source hash, method lines, inputs, and outputs. This proves the parser/mask behavior and the allowed two-layer information route; it does not measure learned model leakage or use the missing Qwen3 tokenizer.

These are the active functions: `__getitem__` calls them at lines 426 and 439, translates the boolean mask to 0/-infinity `attention_mask` at lines 435-437, and returns that float mask. The trainer passes `attention_mask` and `position_ids` into the model at line 334. `bool_attention_mask` is a diagnostic duplicate and is removed before forward at lines 464/553. The defect therefore applies to selected Unseen data processing; Seen already uses ordinary causal attention.

Mechanical conversion can compact internal block separators to `<Parallel><Path>...` and `</Path><Path>...` and `</Path></Parallel>`, preserving all path and summary text. Alternatively, fix the parser/mask to assign and isolate every separator with a defined branch or fork context. Current runtime already concatenates path spans without inter-path whitespace (`parallel_thinking_loop_v3.py:405-421`), so compaction also aligns this part of serialization. Confirm exact mask/position parity on the future student-tokenized sample before Unseen training.

`trim_padding` removes only batch suffix padding and preserves positions/masks (`fsdp_parallel_sft_trainer.py:308`). The sequence-parallel remove-padding branch forwards `attention_mask=None` (`:372`); it should not be enabled as an assumed-preserving optimization for the special Unseen mask. Current defaults use one sequence-parallel rank and remove-padding false.

## Adaptive rounds, branch count, plans, and injected IDs

Full structural counts (train + val counted once):

| Input | forks per example | paths per fork | numbered paths | explicit Plan rows |
|---|---|---|---:|---:|
| real GSM | 0..6 | 2..5 | 0 / 22091 | 0 |
| realistic GSM | 0..3 | 2..5 | 0 / 29444 | 0 |
| mixed | 0..1 | 2..4 | 10731 / 10731 | 4700 / 5000 |

Real GSM has 1738 rows and realistic GSM has 2747 rows whose number of paths changes across rounds. Mixed has 300 sequential examples and 4700 one-fork examples, with 3580 two-path, 909 three-path, and 211 four-path blocks. No input covers 6, 7, or 8 paths. All counted tags balance, and GSM `branch_schedule` matches the text.

The v3 runtime lets the model choose when to emit `<Parallel>` and can repeat rounds. It stops after the configured iteration cap; current Qwen3 RL/eval configs cap at 4 (`rl_qwen3_06b.yaml:52`, `eval_qwen3_06b.yaml:34`), so the 24 real-GSM rows with 5 or 6 forks exceed that deployed cap. Branch count is nevertheless fixed: every fork uses `self.num_paths` and a loop over that same integer (`parallel_thinking_loop_v3.py:358`, `:390`). RL config sets 2. SFT can consume different counts in text, but its metadata does not make inference choose a count.

Every runtime path call receives the same shared prefix plus only `<Path>`; the index is never included (`parallel_thinking_loop_v3.py:373-397`). `add_diverse_prefix` is assigned at initialization and never used thereafter. Thus the mixed dataset's preplan and `1:`, `2:`, ... content are not paired with injected runtime branch IDs. Sampling independent seeds permits duplicated branch assignments. Unnumbered GSM branches likewise lack deterministic task assignment. A visible global plan alone does not tell each identically prompted path which item it owns.

For the intended 2..8 behavior, define a public plan before `<Parallel>` with a validated count and task for each stable ID; parse it, select the count per round, and inject the corresponding ID/task into each branch request. Preserve that same visible branch prefix and plan contract in SFT. Whether injected prefixes are trainable should be specified consistently for SFT and RL response masks. After each merge, generate a summary and allow another model-selected plan/fork or final answer. Runtime and training need matching serialization, system messages, tokenization, mask, and position semantics. In v3, masks/positions are returned for training, while `server_manager.generate` forwards only prompt IDs and sampling params (`agent_loop.py:81-104`), so ordinary vLLM continuation does not receive the custom mask/positions. This limits claims of Unseen train/inference equivalence.

## Mechanical conversion versus new semantic targets

Mechanical work: select full user prompt and response columns; keep reference answer separate; convert JSONL to the required Parquet schema; preserve system roles in the selected loader; compact only whitespace outside paths inside parallel blocks if keeping the current parser; retain metadata/provenance; validate six student tags; preflight complete sequence lengths; map already-existing mixed plan IDs to an implemented runtime protocol.

New targets or semantic revalidation are required for missing public preplans in GSM, assigning GSM dependency subcalculations to IDs, examples with 6..8 useful branches, mixed examples with multiple dependent rounds, and any shortening/splitting that changes required facts or dependency chains. Adding arbitrary paths, numbering text, or copying an existing solution into a new round does not establish a needed independent calculation. Some plans can be extracted mechanically from authoritative dependency/task metadata, but that requires verifying the extraction and cannot be assumed from schema alone.

No semantic correctness, branch necessity, diversity, contamination, GPU executability, exact token length, or model-quality claim is established by this runtime audit. These remain separate checks.
