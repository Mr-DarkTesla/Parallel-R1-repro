"""Rescore response spans in another context within the same forward (flat_packed logprob_context).

vLLM samples path k of a block from prompt + response[:block_start] + <Path>, so in the
flat response it is preceded by sibling paths it never saw. Each such span is copied after
the sequence; the copy attends to the context the vLLM call had and to itself, at the
positions that call used. Its logits replace the in-place log-probs of the span's tokens.
"""
import torch


def append_replay_segments(input_ids, position_ids, bool_mask, segments, offset):
    """Append span copies to one microbatch.

    Args:
        input_ids, position_ids: (B, T).
        bool_mask: (B, T, T), True where attention is allowed.
        segments: per row, (start, end, ctx_end) in response coordinates. The copy of
            response[start:end] sees what the token at ctx_end - 1 sees plus that token.
        offset: column of response index 0.

    Returns:
        input_ids, position_ids, bool_mask extended by D columns, and targets (B, D):
        the response index predicted by the logit at each appended column, or -1.
    """
    batch_size, length = input_ids.shape
    width = max((sum(end - start for start, end, _ in row) for row in segments), default=0)
    targets = torch.full((batch_size, width), -1, dtype=torch.long, device=input_ids.device)
    if width == 0:
        return input_ids, position_ids, bool_mask, targets
    total = length + width
    input_ids = torch.cat([input_ids, input_ids.new_zeros(batch_size, width)], dim=1)
    position_ids = torch.cat([position_ids, position_ids.new_zeros(batch_size, width)], dim=1)
    mask = bool_mask.new_zeros(batch_size, total, total)
    mask[:, :length, :length] = bool_mask
    # Unused appended rows attend to themselves: a fully masked row would give NaN gradients.
    mask[:, length:, length:] = torch.eye(width, dtype=torch.bool, device=mask.device)
    for row, spans in enumerate(segments):
        column = length
        for start, end, ctx_end in spans:
            size = end - start
            assert 0 < ctx_end <= start < end and offset + end <= length, (start, end, ctx_end)
            copy = slice(column, column + size)
            last_context = offset + ctx_end - 1
            input_ids[row, copy] = input_ids[row, offset + start:offset + end]
            position_ids[row, copy] = position_ids[row, last_context] + 1 + torch.arange(
                size, dtype=position_ids.dtype, device=position_ids.device)
            mask[row, copy, :length] = bool_mask[row, last_context]
            mask[row, copy, copy] = torch.ones(size, size, dtype=torch.bool, device=mask.device).tril()
            # Column j predicts copy token j + 1; the last copy token predicts nothing.
            targets[row, column - length:column - length + size - 1] = torch.arange(
                start + 1, end, dtype=torch.long, device=targets.device)
            column += size
    return input_ids, position_ids, mask, targets
