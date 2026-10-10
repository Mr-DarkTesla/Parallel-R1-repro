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
