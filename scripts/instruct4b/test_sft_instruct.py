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


TAG_IDS = list(range(151669, 151675))


def tag_lr_steps(model, mult, grads, full=lambda p: p.detach(), shard=lambda g, p: g):
    """AdamW steps of the trainer (tag-row multiplier `mult`) with given full gradients; returns full weights after each step."""
    trainer = SimpleNamespace(model=model, tag_lr_mult=mult, tag_ids=TAG_IDS)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, betas=(0.9, 0.95), weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / 3)  # changing lr, like the warmup
    history = []
    for step_grads in grads:
        for p, g in zip(model.parameters(), step_grads):
            p.grad = shard(g.clone(), p)
        saved = FSDPParallelThinkingSFTTrainer._tag_rows_before_step(trainer)
        opt.step()
        FSDPParallelThinkingSFTTrainer._scale_tag_rows_update(trainer, saved)
        sched.step()
        history.append([full(p).clone() for p in model.parameters()])
    return history


def check_tag_lr(make_model, mult=50.0, steps=3, **sharding):
    """Only the tag rows get lr*mult (equal to a separate AdamW with lr*mult); every other element follows the old recipe."""
    params = list(tiny_tied_model().parameters())  # same init as make_model(), unsharded
    torch.manual_seed(1)
    grads = [[torch.randn_like(p) for p in params] for _ in range(steps)]
    old = tag_lr_steps(tiny_tied_model(), 1.0, grads)  # old recipe, unsharded
    new = tag_lr_steps(make_model(), mult, grads, **sharding)
    emb = [i for i, p in enumerate(params) if p.shape[0] >= 151675]
    assert len(emb) == 1, "tied embedding is a single parameter"
    e = emb[0]
    rows = torch.nn.Parameter(params[e].detach()[TAG_IDS].clone())
    ref = torch.optim.AdamW([rows], lr=1e-3 * mult, betas=(0.9, 0.95), weight_decay=0.01)
    ref_sched = torch.optim.lr_scheduler.LambdaLR(ref, lambda s: (s + 1) / 3)
    others = torch.ones(params[e].shape[0], dtype=torch.bool)
    others[TAG_IDS] = False
    for step, (a, b) in enumerate(zip(old, new)):
        rows.grad = grads[step][e][TAG_IDS].clone()
        ref.step()
        ref_sched.step()
        for i, (x, y) in enumerate(zip(a, b)):
            if i == e:
                torch.testing.assert_close(y[others], x[others], rtol=0, atol=0)
                torch.testing.assert_close(y[TAG_IDS], rows.detach(), rtol=1e-5, atol=1e-6)
                assert (y[TAG_IDS] - x[TAG_IDS]).abs().max() > 1e-2  # the rows really moved further
            else:
                torch.testing.assert_close(y, x, rtol=0, atol=0)


def tiny_tied_model(vocab=151936):  # the real embedding has 151936 rows, tags at 151669..151674
    torch.manual_seed(0)
    return Qwen3ForCausalLM(Qwen3Config(vocab_size=vocab, hidden_size=16, intermediate_size=32, num_hidden_layers=1,
                                        num_attention_heads=2, num_key_value_heads=1, head_dim=8, tie_word_embeddings=True))


def test_tag_lr_mult_only_tag_rows():
    check_tag_lr(tiny_tied_model)


def test_tag_lr_mult_default_is_old_step():
    trainer = SimpleNamespace(model=tiny_tied_model(), tag_lr_mult=1.0, tag_ids=TAG_IDS)
    assert FSDPParallelThinkingSFTTrainer._tag_rows_before_step(trainer) is None


def _fsdp2_worker(rank, port, errors):
    import torch.distributed as dist
    from torch.distributed.device_mesh import init_device_mesh
    from torch.distributed.fsdp import fully_shard
    from torch.distributed.tensor import distribute_tensor

    os.environ.update(MASTER_ADDR="127.0.0.1", MASTER_PORT=str(port))
    dist.init_process_group("gloo", rank=rank, world_size=2)
    try:
        mesh = init_device_mesh("cpu", (2,))

        def sharded_model():  # wrapped as in verl apply_fsdp2: layers, then the root (holds the tied embedding)
            model = tiny_tied_model()
            for layer in model.model.layers:
                fully_shard(layer, mesh=mesh)
            fully_shard(model, mesh=mesh)
            assert model.get_output_embeddings().weight is model.get_input_embeddings().weight
            return model

        check_tag_lr(sharded_model, full=lambda p: p.full_tensor(),
                     shard=lambda g, p: distribute_tensor(g, mesh, p.placements))
    except Exception:
        errors.put(f"rank {rank}: {traceback.format_exc()}")
    finally:
        dist.destroy_process_group()


def test_tag_lr_mult_fsdp2_shards():
    """The same check on 2 CPU ranks with the real FSDP2 layout (all tag rows on rank 1). Synthetic gradients:
    FSDP2 forward/backward needs CUDA streams."""
    import torch.multiprocessing as mp

    errors = mp.get_context("spawn").SimpleQueue()
    mp.spawn(_fsdp2_worker, args=(29500 + os.getpid() % 1000, errors), nprocs=2)
    assert errors.empty(), errors.get()


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
