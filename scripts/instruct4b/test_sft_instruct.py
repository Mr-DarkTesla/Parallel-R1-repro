"""CPU checks of the SFT inputs for Qwen3-4B (hybrid instruct) and of the gradient accumulation.

Run on the pod from verl/ of this checkout (the venv has an editable verl from /work/setup-src, PYTHONPATH must win):
  cd verl && CUDA_VISIBLE_DEVICES= PYTHONPATH=$PWD python ../scripts/instruct4b/test_sft_instruct.py
MODEL (default /work/assets/models/Qwen3-4B) only needs the tokenizer; the six tags are added in memory.
"""
import os
import tempfile
import traceback
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import torch
import verl
from omegaconf import OmegaConf
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

from verl.trainer.fsdp_parallel_sft_trainer import FSDPParallelThinkingSFTTrainer
from verl.utils.dataset.parallel_thinking_sft_dataset import ParallelThinkingSFTDataset, collate_cropped

TAGS = ["<Path>", "</Path>", "<Parallel>", "</Parallel>", "<Summary>", "</Summary>"]
PROMPT = ("Insert a parallel block: begin with <Parallel>, each path within <Path> and </Path>, close with </Parallel>, "
          "then <Summary> and </Summary>.\n\nProblem: 2 + 3?")
# A user instruction with two literal paths: text, not structure
TWO_PATHS_PROMPT = "Reply in the format <Parallel><Path>first</Path><Path>second</Path></Parallel><Summary>...</Summary>.\n\nProblem: 2 + 3?"
RESPONSE = "We add.\n\n<Parallel><Path>2 + 3 = 5</Path><Path>3 + 2 = 5</Path></Parallel>\n<Summary>Both give 5.</Summary>\n\nFinal Answer: 5"


def test_checkout_is_used():
    assert os.path.dirname(verl.__file__).startswith(os.getcwd()), f"verl imported from {verl.__file__}"


def make_dataset(tokenizer, tmp_path, prompt=PROMPT, **config):
    path = str(tmp_path / "d.parquet")
    pd.DataFrame({"prompt": [prompt] * 2, "response": [RESPONSE] * 2}).to_parquet(path)
    return ParallelThinkingSFTDataset(path, tokenizer, {"max_length": 256, **config})


def make_sample(tokenizer, tmp_path, prompt=PROMPT, **config):
    return make_dataset(tokenizer, tmp_path, prompt, **config)[0]


def test_tags_are_single_new_tokens(tokenizer):
    assert [tokenizer.encode(tag) for tag in TAGS] == [[i] for i in range(151669, 151675)]


def test_native_non_thinking_template(tokenizer, tmp_path):
    """The training sequence is the native render of the conversation: empty <think></think>, response, <|im_end|>."""
    sample = make_sample(tokenizer, tmp_path, enable_thinking=False)
    messages = [{"role": "user", "content": PROMPT}, {"role": "assistant", "content": RESPONSE}]
    native = tokenizer.apply_chat_template(messages, tokenize=False)
    assert native.endswith("<|im_end|>\n")
    length = int(sample["length"])
    assert tokenizer.decode(sample["input_ids"][:length]) == native[: -len("\n")]
    targets = sample["input_ids"][1:][sample["loss_mask"][:-1].bool()]
    assert tokenizer.decode(targets) == RESPONSE + "<|im_end|>"


def test_default_template_unchanged(tokenizer, tmp_path):
    sample = make_sample(tokenizer, tmp_path)
    assert "<think>" not in tokenizer.decode(sample["input_ids"][: int(sample["length"])])


def check_structure_only_in_response(tokenizer, sample):
    """Tags in the instruction are not structure: causal prompt, consecutive prompt positions; paths do not see each other."""
    ids, mask, pos = sample["input_ids"], sample["bool_attention_mask"][0], sample["position_ids"]
    length = int(sample["length"])
    prompt_length = int(sample["loss_mask"].nonzero()[0]) + 1
    assert torch.equal(mask[:prompt_length, :prompt_length], torch.ones(prompt_length, prompt_length).tril().bool())
    assert torch.equal(pos[:prompt_length], torch.arange(prompt_length))
    starts = (ids == tokenizer.convert_tokens_to_ids("<Path>")).nonzero().flatten()
    ends = (ids == tokenizer.convert_tokens_to_ids("</Path>")).nonzero().flatten()
    starts, ends = starts[starts >= prompt_length], ends[ends >= prompt_length]
    (s1, s2), (e1, e2) = starts.tolist(), ends.tolist()
    assert not mask[s2:e2 + 1, s1:e1 + 1].any()
    assert pos[s1] == pos[s2] and pos[e2 + 1] == pos[s1] + max(e1 - s1, e2 - s2) + 1  # </Parallel> after the longest path
    summary = int((ids == tokenizer.convert_tokens_to_ids("<Summary>")).nonzero()[-1])
    assert mask[summary, s1:e2 + 1].all() and not mask[:length, length:].any()


def test_structure_only_in_response(tokenizer, tmp_path):
    check_structure_only_in_response(tokenizer, make_sample(tokenizer, tmp_path, enable_thinking=False))


def test_two_literal_paths_in_prompt_are_text(tokenizer, tmp_path):
    """Two literal <Path> blocks in the instruction stay mutually visible (the old full-sequence mask hid them)."""
    sample = make_sample(tokenizer, tmp_path, TWO_PATHS_PROMPT, enable_thinking=False)
    prompt_length = int(sample["loss_mask"].nonzero()[0]) + 1
    assert (sample["input_ids"][:prompt_length] == tokenizer.convert_tokens_to_ids("<Path>")).sum() == 2
    check_structure_only_in_response(tokenizer, sample)


def test_single_path_prompt_mask_unchanged(tokenizer, tmp_path):
    """For the authors' prompt (one literal <Path> pair) the mask equals the old full-sequence mask."""
    dataset = make_dataset(tokenizer, tmp_path)
    sample = dataset[0]
    length = int(sample["length"])
    old = dataset.generate_parallel_thinking_reasponse_mask(sample["input_ids"])[:length, :length]
    assert torch.equal(sample["bool_attention_mask"][0][:length, :length], old)


def test_rollout_prompt_matches_sft(tokenizer, tmp_path):
    """With PARALLEL_ROLLOUT_ENABLE_THINKING=false the parallel rollout starts from the SFT prompt tokens."""
    from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3 as Loop

    agent = {"add_diverse_prefix": False, "max_iterations_for_parallel_thinking": 4, "num_paths": 2, "max_path_response_length": 64}
    config = OmegaConf.create({"actor_rollout_ref": {"rollout": {"agent": agent, "prompt_length": 64, "response_length": 64}}})
    os.environ["PARALLEL_ROLLOUT_ENABLE_THINKING"] = "false"
    Loop._class_initialized = False
    Loop.init_class(config, tokenizer)
    del os.environ["PARALLEL_ROLLOUT_ENABLE_THINKING"]
    rollout = tokenizer.apply_chat_template([{"role": "user", "content": PROMPT}], add_generation_prompt=True, tokenize=True, **Loop.template_kwargs)
    sample = make_sample(tokenizer, tmp_path, enable_thinking=False)
    assert sample["input_ids"][: len(rollout)].tolist() == rollout and sample["loss_mask"][len(rollout) - 1] == 1


def tiny_trainer(tokenizer):
    torch.manual_seed(0)
    config = Qwen3Config(vocab_size=len(tokenizer), hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                         num_attention_heads=4, num_key_value_heads=2, head_dim=8, tie_word_embeddings=True)
    model = Qwen3ForCausalLM(config)
    return SimpleNamespace(fsdp_model=model, model=model, device_name="cpu", use_remove_padding=False,
                           config=OmegaConf.create({"ulysses_sequence_parallel_size": 1}))


def test_gradient_accumulation_divides_before_backward(tokenizer, tmp_path):
    """Two micro batches with loss_scale 1/2 give the gradient of the full batch."""
    sample = make_sample(tokenizer, tmp_path, enable_thinking=False)
    short = make_sample(tokenizer, tmp_path, enable_thinking=False, max_length=int(sample["length"]) + 7)
    batch = collate_cropped([sample, short])
    trainer = tiny_trainer(tokenizer)
    step = FSDPParallelThinkingSFTTrainer._compute_loss_and_backward

    step(trainer, dict(batch))
    full = [p.grad.clone() for p in trainer.model.parameters()]
    trainer.model.zero_grad()
    for i in range(2):
        step(trainer, {key: value[i:i + 1] for key, value in batch.items()}, loss_scale=0.5)
    for a, b in zip(full, (p.grad for p in trainer.model.parameters())):
        torch.testing.assert_close(a, b, rtol=5e-2, atol=1e-5)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(os.environ.get("MODEL", "/work/assets/models/Qwen3-4B"))
    tokenizer.add_special_tokens({"additional_special_tokens": TAGS})
    failed = 0
    for name, test in list(globals().items()):
        if not name.startswith("test_"):
            continue
        args = {"tokenizer": tokenizer, "tmp_path": Path(tempfile.mkdtemp())}
        try:
            test(**{k: v for k, v in args.items() if k in test.__code__.co_varnames[:test.__code__.co_argcount]})
            print("PASS", name)
        except Exception:
            failed += 1
            print("FAIL", name, traceback.format_exc(limit=-2))
    raise SystemExit(failed)
