"""Unseen structure == independent path KV caches concatenated at </Parallel> (tiny Qwen3, CPU, fp64).

The SFT/actor objective (path-isolating mask + multiverse positions, taken verbatim from
parallel_thinking_sft_dataset.py) must equal decoding each path from its own copy of the
prefix cache and physically concatenating the per-path caches, as Multiverse Engine does.
This is the correctness premise of a KV-merging rollout; no RoPE re-rotation is needed.

python -m unittest tests.test_unseen_kv_reference
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch
from transformers import DynamicCache, Qwen3Config, Qwen3ForCausalLM

SOURCE = Path(__file__).resolve().parents[1] / 'verl/verl/utils/dataset/parallel_thinking_sft_dataset.py'
ns = dict(torch=torch)
for node in ast.walk(ast.parse(SOURCE.read_text())):
    if isinstance(node, ast.FunctionDef) and node.name in (
            'generate_parallel_thinking_reasponse_mask', 'compute_structured_position_ids'):
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), ns)
PARALLEL, END_PARALLEL, PATH, END_PATH, SUMMARY, END_SUMMARY, NEWLINE = range(50, 57)


class UnseenKVReferenceTest(unittest.TestCase):
    def test_mask_and_positions_equal_concatenated_path_caches(self):
        torch.manual_seed(0)
        dtype = torch.get_default_dtype()
        torch.set_default_dtype(torch.float64)
        self.addCleanup(torch.set_default_dtype, dtype)
        config = Qwen3Config(vocab_size=64, hidden_size=64, intermediate_size=128, num_hidden_layers=3,
                             num_attention_heads=4, num_key_value_heads=2, head_dim=16)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).eval()
        text = lambda n: torch.randint(1, 40, (n,)).tolist()

        prefix = text(7) + [PARALLEL]
        blocks = [[text(5), text(9), text(3)], [text(6), text(4)]]
        tails = [[END_PARALLEL, NEWLINE, SUMMARY] + text(4) + [END_SUMMARY] + text(5) + [PARALLEL],
                 [END_PARALLEL, NEWLINE, SUMMARY] + text(3) + [END_SUMMARY] + text(4)]
        sequence = list(prefix)
        for paths, tail in zip(blocks, tails):
            for path in paths:
                sequence += [PATH] + path + [END_PATH]
            sequence += tail
        ids = torch.tensor(sequence)

        tags = SimpleNamespace(start_parallel_token=PARALLEL, end_parallel_token=END_PARALLEL, start_path_token=PATH,
                               end_path_token=END_PATH, tokenizer=SimpleNamespace(pad_token_id=0))
        allowed = ns['generate_parallel_thinking_reasponse_mask'](tags, ids)
        positions = ns['compute_structured_position_ids'](tags, ids)
        mask = torch.zeros(allowed.shape).masked_fill(~allowed, float('-inf'))[None, None]
        with torch.no_grad():
            structured = model(ids[None], attention_mask=mask, position_ids=positions[None]).logits[0]

            def run(tokens, start, cache):
                past = cache.get_seq_length()
                out = model(torch.tensor([tokens]), position_ids=torch.arange(start, start + len(tokens))[None],
                            past_key_values=cache, cache_position=torch.arange(past, past + len(tokens)), use_cache=True)
                return out.logits[0], out.past_key_values

            reference = []
            logits, cache = run(prefix, 0, DynamicCache())
            reference.append(logits)
            next_position = len(prefix)
            for paths, tail in zip(blocks, tails):
                base, layers, longest = next_position, cache.to_legacy_cache(), 0
                path_caches = []
                for path in paths:
                    tokens = [PATH] + path + [END_PATH]
                    copy = DynamicCache.from_legacy_cache(tuple((k.clone(), v.clone()) for k, v in layers))
                    logits, copy = run(tokens, base, copy)
                    reference.append(logits)
                    path_caches.append([(k[:, :, -len(tokens):], v[:, :, -len(tokens):]) for k, v in copy.to_legacy_cache()])
                    longest = max(longest, len(tokens))
                # Merge: physical concatenation; keys keep the rotation of their own positions.
                cache = DynamicCache.from_legacy_cache(tuple(
                    (torch.cat([layers[l][0]] + [c[l][0] for c in path_caches], 2),
                     torch.cat([layers[l][1]] + [c[l][1] for c in path_caches], 2)) for l in range(len(layers))))
                next_position = base + longest  # </Parallel> sits right after the longest path
                logits, cache = run(tail, next_position, cache)
                reference.append(logits)
                next_position += len(tail)
            reference = torch.cat(reference)
            flat = model(ids[None]).logits[0]
        torch.testing.assert_close(structured, reference, atol=1e-10, rtol=0)
        self.assertGreater((flat - reference).abs().max().item(), 1e-2)  # the check is not vacuous


if __name__ == '__main__':
    unittest.main()
