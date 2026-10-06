"""Opt-in full decode graphs for Qwen3 on vLLM 0.8.5.post1 / FlashAttention.

Keep prefill and unsupported attention modes on vLLM's existing path. Capture
exact batch shapes: adding padding changes BF16 GEMMs and can change outputs.
"""
import copy
import os


def enable_decode_graph(runner, check_replays=False):
    import torch
    from vllm.compilation.backends import PiecewiseBackend
    from vllm.forward_context import get_forward_context
    from vllm.v1.attention.backends.flash_attn import FlashAttentionMetadata

    original = runner.model.forward
    graphs = {}
    pool = torch.cuda.graph_pool_handle()
    stats = {"captures": 0, "replays": 0}
    runner._decode_graph_stats = stats
    runner._decode_graph_check = check_replays

    def forward(*args, **kwargs):
        context = get_forward_context()
        metadata = context.attn_metadata
        if (not isinstance(metadata, FlashAttentionMetadata) or metadata.max_query_len != 1
                or metadata.use_cascade or metadata.local_attn_metadata is not None
                or kwargs.get("inputs_embeds") is not None
                or kwargs.get("intermediate_tensors") is not None):
            return original(*args, **kwargs)
        ids, positions = kwargs["input_ids"], kwargs["positions"]
        count, size = metadata.num_actual_tokens, ids.shape[0]
        # Preserve FlashAttention's KV block count and split-reduction order.
        # A model-wide upper bound changes BF16 results on long contexts.
        context_bound = min(((int(metadata.max_seq_len) + 63) // 64) * 64, runner.max_model_len)
        key = (count, size, context_bound)
        if key not in graphs:
            static = copy.copy(metadata)
            static.max_seq_len = context_bound
            static.query_start_loc = metadata.query_start_loc.clone()
            static.seq_lens = metadata.seq_lens.clone()
            static.slot_mapping = metadata.slot_mapping.clone()
            static.block_table = metadata.block_table.clone()
            graphs[key] = {"metadata": static, "ids": ids.clone(), "positions": positions.clone()}
        entry = graphs[key]
        static = entry["metadata"]
        entry["ids"].copy_(ids)
        entry["positions"].copy_(positions)
        static.seq_lens.copy_(metadata.seq_lens)
        static.slot_mapping.copy_(metadata.slot_mapping)
        static.block_table.copy_(metadata.block_table)
        if "graph" not in entry:
            reference = original(*args, **kwargs).clone()
            graph_kwargs = {**kwargs, "input_ids": entry["ids"], "positions": entry["positions"]}
            piece_call = PiecewiseBackend.__call__

            def compiled_piece(piece, *inputs):
                shape = inputs[piece.sym_shape_indices[0]]
                concrete = piece.concrete_size_entries.get(shape)
                function = (concrete.runnable if concrete and concrete.runnable
                            else piece.compiled_graph_for_general_shape)
                return function(*inputs)

            context.attn_metadata = static
            try:
                stream = torch.cuda.Stream()
                stream.wait_stream(torch.cuda.current_stream())
                with torch.cuda.stream(stream):
                    for _ in range(3):
                        original(**graph_kwargs)
                torch.cuda.current_stream().wait_stream(stream)
                graph = torch.cuda.CUDAGraph()
                # PyTorch disallows nested replay. Capture the same compiled
                # kernels directly, including attention, in one outer graph.
                PiecewiseBackend.__call__ = compiled_piece
                # Replays are serial; share scratch allocations across shapes.
                with torch.cuda.graph(graph, pool=pool):
                    output = original(**graph_kwargs)
                PiecewiseBackend.__call__ = piece_call
                graph.replay()
                torch.testing.assert_close(output[:count], reference[:count], atol=0, rtol=0)
                entry.update(graph=graph, output=output)
                stats["captures"] += 1
            finally:
                context.attn_metadata = metadata
                PiecewiseBackend.__call__ = piece_call
        else:
            entry["graph"].replay()
            if runner._decode_graph_check:
                reference = original(*args, **kwargs)
                torch.testing.assert_close(entry["output"][:count], reference[:count], atol=0, rtol=0)
        stats["replays"] += 1
        return entry["output"][:count]

    runner.model.forward = forward
    return original


def install_decode_graph():
    if os.getenv("PARALLEL_R1_FULL_DECODE_GRAPH") != "1":
        return
    import vllm
    from vllm.v1.worker.gpu_model_runner import GPUModelRunner

    if vllm.__version__ != "0.8.5.post1":
        raise RuntimeError("Full decode graphs require the validated vLLM 0.8.5.post1 runtime")
    if getattr(GPUModelRunner, "_parallel_r1_decode_graph", False):
        return
    original = GPUModelRunner.load_model

    def load_model(runner, *args, **kwargs):
        result = original(runner, *args, **kwargs)
        if runner.model_config.hf_config.model_type != "qwen3" or runner.parallel_config.tensor_parallel_size != 1:
            raise RuntimeError("Full decode graphs require Qwen3 with rollout tensor parallel size 1")
        enable_decode_graph(runner)
        return result

    GPUModelRunner.load_model = load_model
    GPUModelRunner._parallel_r1_decode_graph = True
