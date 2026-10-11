"""CPU check for ``data.parallel_text_loss_scope=parallel_block``.

Run from the repository root with CPU PyTorch, pandas, transformers and matplotlib:
    python scripts/exp21/check_span_focused_mask.py
"""

import importlib.util
import re
import sys
import types
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]


def load_dataset_class():
    """Load the real dataset module without initializing the unrelated Ray trainer."""
    for name in ("verl", "verl.utils", "verl.utils.dataset"):
        module = types.ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module
    sys.modules["verl.utils"].hf_tokenizer = lambda value: value
    fs = types.ModuleType("verl.utils.fs")
    fs.copy_to_local = lambda value, **kwargs: value
    sys.modules["verl.utils.fs"] = fs
    model = types.ModuleType("verl.utils.model")
    model.compute_position_id_with_mask = lambda value: value
    sys.modules["verl.utils.model"] = model
    for name, path in (
        ("verl.utils.dataset.multiverse_structure", ROOT / "verl/verl/utils/dataset/multiverse_structure.py"),
        ("verl.utils.dataset.parallel_thinking_sft_dataset", ROOT / "verl/verl/utils/dataset/parallel_thinking_sft_dataset.py"),
    ):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules["verl.utils.dataset.parallel_thinking_sft_dataset"].ParallelThinkingSFTDataset


ParallelThinkingSFTDataset = load_dataset_class()


class ToyTokenizer:
    """Small single-token-tag tokenizer sufficient to exercise dataset indexing."""

    eos_token = "<eos>"
    pad_token_id = 0

    def __init__(self):
        self.ids = {"<pad>": 0, "<eos>": 1}

    def _id(self, token):
        if token not in self.ids:
            self.ids[token] = len(self.ids)
        return self.ids[token]

    def encode(self, text, add_special_tokens=False):
        tokens = re.findall(r"<[^>]+>|[^<]", text)
        return [self._id(token) for token in tokens]

    def convert_tokens_to_ids(self, token):
        return self._id(token)

    def apply_chat_template(self, messages, add_generation_prompt, tokenize, **kwargs):
        assert not tokenize and add_generation_prompt
        return "user:" + messages[0]["content"] + "\nassistant:"

    def __call__(self, text, return_tensors, add_special_tokens=False):
        ids = torch.tensor([self.encode(text, add_special_tokens=add_special_tokens)], dtype=torch.long)
        return {"input_ids": ids, "attention_mask": torch.ones_like(ids)}


def make_dataset(response, kind="parallel_th", max_length=512, scope="parallel_block"):
    tokenizer = ToyTokenizer()
    dataset = ParallelThinkingSFTDataset.__new__(ParallelThinkingSFTDataset)
    dataset.tokenizer = tokenizer
    dataset.prompts = ["What is the answer?"]
    dataset.responses = [response]
    dataset.row_thinking = [True]
    dataset.row_kind = [kind]
    dataset.template_kwargs = {}
    dataset.structure = "multiverse"
    dataset.parallel_text_loss_weight = 0.1
    dataset.parallel_text_loss_scope = scope
    dataset.truncation = "error"
    dataset.max_length = max_length
    dataset.start_parallel_token = tokenizer.encode("<Parallel>")[0]
    dataset.end_parallel_token = tokenizer.encode("</Parallel>")[0]
    dataset.start_path_token = tokenizer.encode("<Path>")[0]
    dataset.end_path_token = tokenizer.encode("</Path>")[0]
    dataset.structure_tags = {
        "Parallel": dataset.start_parallel_token,
        "/Parallel": dataset.end_parallel_token,
        "Path": dataset.start_path_token,
        "/Path": dataset.end_path_token,
    }
    dataset.think_start_ids = tokenizer.encode("<think>", add_special_tokens=False)
    dataset.think_end_ids = tokenizer.encode("</think>", add_special_tokens=False)
    names = ("Parallel", "/Parallel", "Goal", "/Goal", "Outline", "/Outline",
             "Path", "/Path", "Conclusion", "/Conclusion")
    dataset.loss_tag_ids = {tokenizer.convert_tokens_to_ids(f"<{name}>") for name in names}
    return dataset


def main():
    response = (
        "<think>before "
        "<Parallel><Goal><Outline>first</Outline><Outline>second</Outline></Goal>"
        "<Path>one</Path><Path>two</Path><Conclusion>done</Conclusion></Parallel>"
        " after</think>Final Answer: done"
    )
    dataset = make_dataset(response)
    response_ids = torch.tensor(dataset.tokenizer.encode(response + dataset.tokenizer.eos_token))
    span = dataset._validated_parallel_block_span(response_ids)
    assert span is not None

    sample = dataset[0]
    prompt = dataset.tokenizer.apply_chat_template(
        [{"role": "user", "content": dataset.prompts[0]}], add_generation_prompt=True,
        tokenize=False, enable_thinking=True,
    )
    first = len(dataset.tokenizer.encode(prompt)) - 1
    weights = sample["loss_mask"][:-1]
    block_start, block_end = span
    assert torch.all(weights[first + block_start:first + block_end + 1] == 1)
    outside = torch.cat((weights[first:first + block_start],
                         weights[first + block_end + 1:first + len(response_ids)]))
    assert outside.numel() and torch.all(outside == 0.1)
    assert weights.sum() > 0

    historical = make_dataset(response, scope="all")[0]
    historical_weights = historical["loss_mask"][:-1]
    for offset, token in enumerate(response_ids.tolist()):
        expected = 1 if token in dataset.loss_tag_ids else 0.1
        assert historical_weights[first + offset] == expected

    replay = make_dataset(response, kind="replay_th")[0]
    replay_weights = replay["loss_mask"][:-1]
    replay_targets = replay_weights[replay_weights > 0]
    assert replay_targets.numel() and torch.all(replay_targets == 1)

    plain_control = make_dataset(response, kind="control_th")[0]
    plain_targets = plain_control["loss_mask"][:-1]
    plain_targets = plain_targets[plain_targets > 0]
    assert plain_targets.numel() and torch.all(plain_targets == 1)

    repeated = torch.tensor(dataset.tokenizer.encode(
        "<think><Parallel><Path>a</Path><Path>b</Path></Parallel>"
        "<Parallel><Path>c</Path><Path>d</Path></Parallel></think>"
    ))
    assert dataset._validated_parallel_block_span(repeated) is None

    too_short = make_dataset(response, max_length=4)
    try:
        too_short[0]
    except NotImplementedError:
        pass
    else:
        raise AssertionError("truncation=error must reject a partial focused block")

    print({"block_token_targets": block_end - block_start + 1,
           "outside_token_targets": int(outside.numel()),
           "replay_targets": int(replay_targets.numel())})


if __name__ == "__main__":
    main()
