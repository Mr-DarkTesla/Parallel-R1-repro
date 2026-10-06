"""Score sampled actions in the exact causal contexts used by the rollout calls."""
import torch

from verl.utils.torch_functional import entropy_from_logits, logprobs_from_logits


def forward_rollout_calls(model, calls_by_response, responses, temperature, calculate_entropy=False):
    """One model forward per microbatch, including on ranks with no sampled actions.

    Prompt left-padding aligns the generated spans. Labels come from the original
    calls, not the assembled response: the runtime may replace EOS with a tag.
    Keeping separate contexts also recomputes prefix KV as the summary server did.
    """
    batch_size, response_length = responses.shape
    calls = [(owner, call) for owner, row in enumerate(calls_by_response)
             for call in row if call['generated_ids']]
    device = responses.device
    if not calls:
        # FSDP collectives must still be entered on every rank. Connect a zero
        # loss to all model parameters through its ordinary causal forward.
        ids = torch.zeros((1, 2), dtype=torch.long, device=device)
        logits = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                       position_ids=torch.arange(2, device=device)[None],
                       use_cache=False, logits_to_keep=1).logits
        zeros = torch.zeros_like(responses, dtype=logits.dtype) + logits.sum() * 0
        return zeros if calculate_entropy else None, zeros

    prompt_length = max(len(c['prompt_ids']) for _, c in calls)
    generated_length = max(len(c['generated_ids']) for _, c in calls)
    assert prompt_length > 0 and temperature > 0
    ids = torch.zeros((len(calls), prompt_length + generated_length), dtype=torch.long, device=device)
    attention = torch.zeros_like(ids)
    selected = torch.zeros((len(calls), generated_length), dtype=torch.bool, device=device)
    destinations = []
    for row, (owner, call) in enumerate(calls):
        prompt, generated = call['prompt_ids'], call['generated_ids']
        start = call['response_start']
        assert prompt and 0 <= start and start + len(generated) <= response_length
        left = prompt_length - len(prompt)
        ids[row, left:prompt_length] = torch.as_tensor(prompt, device=device)
        ids[row, prompt_length:prompt_length + len(generated)] = torch.as_tensor(generated, device=device)
        attention[row, left:prompt_length + len(generated)] = 1
        selected[row, :len(generated)] = True
        destinations.extend(owner * response_length + start + i for i in range(len(generated)))
    assert len(set(destinations)) == len(destinations), 'Overlapping sampled-action slots'
    positions = (attention.cumsum(-1) - 1).clamp_min(0)
    output = model(input_ids=ids, attention_mask=attention, position_ids=positions,
                   use_cache=False, logits_to_keep=generated_length + 1)
    temperatures = torch.as_tensor([c.get('temperature', temperature) for _, c in calls], device=device)
    assert (temperatures > 0).all(), 'PPO requires stochastic sampling with positive temperature'
    scales = temperatures[:, None].expand_as(selected)[selected].unsqueeze(-1)
    logits = output.logits[:, :-1][selected] / scales
    labels = ids[:, prompt_length:][selected]
    scores = logprobs_from_logits(logits, labels, inplace_backward=False)
    dest = torch.as_tensor(destinations, dtype=torch.long, device=device)

    def scatter(values):
        return values.new_zeros(batch_size * response_length).scatter(0, dest, values).view_as(responses)

    entropy = scatter(entropy_from_logits(logits)) if calculate_entropy else None
    return entropy, scatter(scores)
