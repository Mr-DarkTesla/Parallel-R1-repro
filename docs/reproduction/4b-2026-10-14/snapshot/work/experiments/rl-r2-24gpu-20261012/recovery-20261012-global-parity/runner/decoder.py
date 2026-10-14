"""Independent structured Path rows, decoded together through one KV-cache batch.

Each real row retains the exact unpadded per-call positions and 4D mask. Padding
and finished-row dummy slots never become visible to a live row. Physical batch
forward counts live in last_batch_stats; per-call returns count logical row work.
"""
import math
import torch


class BatchedHFDecoder:
    def __init__(self, model, replay, device=None):
        self.model, self.replay = model, replay
        self.device = str(next(model.parameters()).device if device is None else device)
        self.last_batch_stats = {}

    def __call__(self, call, budget, stops):
        return self.decode_many([call], budget, stops)[0]

    @torch.inference_mode()
    def decode_many(self, calls, budget, stops, *, target_sequences=None):
        """Return one (raw sampled IDs, logps, active row forwards) per call.

        budget may be an integer or per-row list. stops is a shared iterable.
        target_sequences is a proof-only teacher-forcing option; production uses
        independent seeded multinomial draws from each row's full distribution.
        """
        budgets = [int(budget)] * len(calls) if isinstance(budget, int) else list(map(int, budget))
        if len(budgets) != len(calls) or any(n < 0 for n in budgets):
            raise ValueError('Invalid batch budgets')
        if target_sequences is not None:
            if len(target_sequences) != len(calls) or any(len(x) > n for x, n in zip(target_sequences, budgets)):
                raise ValueError('Invalid proof targets')
            budgets = [len(x) for x in target_sequences]
        selected = [i for i, n in enumerate(budgets) if n]
        result = [([], [], 0) for _ in calls]
        if not selected:
            self.last_batch_stats = dict(physical_forward_calls=0, prefill_forward_calls=0,
                                        decode_forward_calls=0, active_row_forward_work=0)
            return result
        parameter = next(self.model.parameters())
        dtype, device = parameter.dtype, parameter.device
        parts = []
        for index in selected:
            call = calls[index]
            temp = float(call.get('temperature', 1.))
            if not math.isfinite(temp) or temp <= 0:
                raise ValueError('Finite positive sampling temperature required')
            parts.append(self.replay.call_inputs(dict(call, generated_ids=[0]), device, dtype))
        size, length = len(selected), max(x[0].shape[1] for x in parts)
        ids = torch.empty((size, length), dtype=torch.long, device=device)
        positions = torch.zeros_like(ids)
        mask = torch.full((size, 1, length, length), -torch.inf, dtype=dtype, device=device)
        valid = torch.zeros((size, length), dtype=torch.bool, device=device)
        next_positions = []
        for row, (index, (input_ids, pos, allowed)) in enumerate(zip(selected, parts)):
            pad = int(calls[index]['pad_id'])
            ids[row].fill_(pad)
            width = input_ids.shape[1]
            offset = length - width
            ids[row, offset:] = input_ids[0]
            positions[row, offset:] = pos[0]
            mask[row, :, offset:, offset:] = allowed[0]
            # Pad query self-visibility prevents NaNs, while live queries cannot
            # read these keys. Their hidden values therefore have no influence.
            if offset:
                diagonal = torch.arange(offset, device=device)
                mask[row, 0, diagonal, diagonal] = 0
            valid[row, offset:] = True
            next_positions.append(int(pos[0, -1]))
        output = self.model(input_ids=ids, position_ids=positions, attention_mask=mask,
                            use_cache=True, logits_to_keep=1)
        physical = 1
        generators = [torch.Generator(device=self.device).manual_seed(int(calls[i].get('seed', 0)))
                      for i in selected]
        raw = [[] for _ in selected]
        logps = [[] for _ in selected]
        active = [True] * size
        stops = set(stops)
        active_sizes = []
        while any(active):
            active_sizes.append(sum(active))
            last_tokens = [int(calls[i]['pad_id']) for i in selected]
            for row, index in enumerate(selected):
                if not active[row]:
                    continue
                logits = output.logits[row, -1].float() / float(calls[index].get('temperature', 1.))
                logits = self.replay.mask_logits(logits, calls[index])
                if target_sequences is None:
                    target = int(torch.multinomial(logits.softmax(-1), 1, generator=generators[row]))
                else:
                    target = int(target_sequences[index][len(raw[row])])
                raw[row].append(target)
                logps[row].append(float(logits[target] - logits.logsumexp(-1)))
                last_tokens[row] = target
                if target in stops or len(raw[row]) >= budgets[index]:
                    active[row] = False
            if not any(active):
                break
            live = torch.tensor(active, dtype=torch.bool, device=device)
            # Only continuation rows append a semantic cache token. Inactive
            # rows append masked dummy slots with an isolated self-only query.
            valid = torch.cat([valid, live[:, None]], dim=1)
            mask = torch.full((size, 1, 1, valid.shape[1]), -torch.inf, dtype=dtype, device=device)
            mask[:, 0, 0].masked_fill_(valid, 0)
            mask[~live] = -torch.inf
            mask[~live, 0, 0, -1] = 0
            for row in range(size):
                if active[row]:
                    next_positions[row] += 1
            pos = torch.tensor([[p if a else 0] for p, a in zip(next_positions, active)],
                               dtype=torch.long, device=device)
            input_ids = torch.tensor([[token if a else int(calls[i]['pad_id'])]
                                      for token, a, i in zip(last_tokens, active, selected)],
                                     dtype=torch.long, device=device)
            output = self.model(input_ids=input_ids, position_ids=pos, attention_mask=mask,
                                past_key_values=output.past_key_values, use_cache=True,
                                logits_to_keep=1)
            physical += 1
        for row, index in enumerate(selected):
            result[index] = (raw[row], logps[row], len(raw[row]))
        self.last_batch_stats = dict(physical_forward_calls=physical, prefill_forward_calls=1,
                                    decode_forward_calls=physical-1,
                                    active_row_forward_work=sum(map(len, raw)),
                                    active_rows_per_sampling_step=active_sizes,
                                    prefill_rows=size, padded_prefill_length=length,
                                    real_prefill_tokens=sum(x[0].shape[1] for x in parts),
                                    generated_lengths=list(map(len, raw)),
                                    kernel_batch_rows=size,
                                    padding_side='left', finished_rows_semantically_masked=True)
        return result
