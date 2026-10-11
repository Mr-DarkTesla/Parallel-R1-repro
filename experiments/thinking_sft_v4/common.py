"""Shared helpers for thinking-SFT v4: the format contract loaded by file path, and the eight plan tags.

The contract (verl/verl/parallel_thinking_generation_v3/contract.py) is owned by the RL side; importing the
verl package pulls ray/vllm, so it is loaded from its file. Override with THINK_CONTRACT_PATH.
"""
import hashlib
import importlib.util
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT_PATH = Path(os.environ.get(
    'THINK_CONTRACT_PATH', REPO / 'verl/verl/parallel_thinking_generation_v3/contract.py'))
# Revision agreed with the RL thread (qwen3-0.6b-rl 6f87cf0). Set THINK_CONTRACT_SHA256='' to skip the check.
EXPECTED_SHA256 = os.environ.get(
    'THINK_CONTRACT_SHA256', '2503e4a330752554464cceab138b9b65057ef2e64939c8632b9a4fe91d6e346e')

# Hugging Face snapshots the VM self-test and the trainer use by default (thinking mode, post-trained). The 4B
# model is the current target; the 0.6B one stays usable with --model Qwen/Qwen3-0.6B (its revision is filled in).
BASE_MODEL = 'Qwen/Qwen3-4B'
BASE_REVISION = '1cfa9a7208912126459214e8b04321603b3df60c'
SMALL_MODEL = 'Qwen/Qwen3-0.6B'
SMALL_REVISION = 'c1899de289a04d12100db370d81485cdf75e47ca'
KNOWN_REVISIONS = {BASE_MODEL: BASE_REVISION, SMALL_MODEL: SMALL_REVISION}


def default_revision(model):
    """Pinned revision for a known HF id, None otherwise (local paths, other models)."""
    return KNOWN_REVISIONS.get(str(model))

def load_contract(path=CONTRACT_PATH):
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and digest != EXPECTED_SHA256:
        raise RuntimeError(f'contract {path} sha256 {digest} != expected {EXPECTED_SHA256}')
    spec = importlib.util.spec_from_file_location('thinking_contract', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.SHA256 = digest
    return module


contract = load_contract()
