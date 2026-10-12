"""Full frozen execute() with real tiny-Qwen likelihoods and proof-only actions.

Targets force two forks, stop-ID replacement, injected bridges and final text.
No targets or sampling overrides are proposed for training.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent/'long-run/runner'
sys.path.insert(0, str(RUNNER))
import structured_replay as replay
from source.parallel_structure import attention, layout
from rollout import execute
from decoder import BatchedHFDecoder
from microbatch_decoder import MicrobatchedHFDecoder
from cohort_decoder import CohortDecoder
from execute_candidate import execute_cohort

spec = importlib.util.spec_from_file_location('episode_reward', HERE.parent/'reward.py')
reward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reward)


class Tokenizer:
    pad_token_id = 0
    eos_token_id = 16
    strings = {10:'<Parallel>',11:'</Parallel>',12:'<Path>',13:'</Path>',
               14:'<Summary>',15:'</Summary>',16:'<eos>',17:'</think>',18:'\n',
               21:'x',22:'y',31:'1',32:'2',33:'3'}
    def encode(self, text, add_special_tokens=False):
        inverse = {v:k for k,v in self.strings.items()}
        if text in inverse:
            return [inverse[text]]
        if text.endswith('\n') and text[:-1].isdigit():
            return [30+int(text[:-1]),18]
        raise ValueError(text)
    def decode(self, ids, skip_special_tokens=False):
        return ''.join(self.strings.get(i, 'p') for i in ids)


class ProofTargets:
    def __init__(self, decoder, episode):
        self.decoder, self.episode = decoder, episode
        self.main_index = 0
        self.width_index = 0
        self.last_batch_stats = {}
    def targets(self, call):
        phase = call['phase']
        if phase == 'main':
            self.main_index += 1
            return [21,10] if self.main_index <= 2 else ([17] if self.main_index == 3 else [21,16])
        if phase == 'width':
            self.width_index += 1
            return [33 if self.width_index == 1 else 32,18]
        if phase == 'summary':
            # EOS is replaced only in visible assembly; raw action stays EOS.
            return [21,16]
        row = call['prompt_ids'][-2]-30
        return [21]*(45+row*10+self.episode) + [13 if row%2 else 16]
    def __call__(self, call, budget, stops):
        return self.decode_many([call], budget, stops)[0]
    def decode_many(self, calls, budgets, stops):
        targets = [self.targets(c) for c in calls]
        result = self.decoder.decode_many(calls,budgets,stops,target_sequences=targets)
        self.last_batch_stats = copy.deepcopy(self.decoder.last_batch_stats)
        return result


def main():
    torch.set_num_threads(2)
    torch.manual_seed(103)
    cfg = Qwen3Config(vocab_size=128, hidden_size=64, intermediate_size=128,
                      num_hidden_layers=3, num_attention_heads=4, num_key_value_heads=2,
                      head_dim=16, attention_dropout=0., pad_token_id=0)
    cfg._attn_implementation = 'sdpa'
    model = Qwen3ForCausalLM(cfg).eval()
    original_forward = model.forward
    forward_counter = [0]
    def counted_forward(*args,**kwargs):
        forward_counter[0] += 1
        return original_forward(*args,**kwargs)
    model.forward = counted_forward
    tok = Tokenizer()
    serial = MicrobatchedHFDecoder(model,replay,max_paths=2)
    prompts = [[23+i]*(4+i*3) for i in range(4)]
    def run_one(decoder, episode, prompt):
        return execute(tok,prompt,ProofTargets(decoder,episode),[16],1024,128,2048,2100+episode*100)
    baseline = [run_one(serial,i,p) for i,p in enumerate(prompts)]
    def proof_execute(tokenizer,prompt,decoder,eos,rb,pb,mc,seed):
        return execute(tokenizer,prompt,ProofTargets(decoder,(seed-2100)//100),eos,rb,pb,mc,seed)
    def run_candidate(collection):
        return execute_cohort(proof_execute,tok,BatchedHFDecoder(model,replay),collection,
                              [2100+i*100 for i in range(4)],[16],1024,128,2048,max_rows=8)
    forward_counter[0] = 0
    outputs,telemetry = run_candidate(prompts)
    observed_server_calls = forward_counter[0]
    assert observed_server_calls == telemetry['cross_episode_server_forward_calls']
    server_stats = copy.deepcopy(telemetry['server_batches'])
    old_deltas, replay_deltas = [], []
    origins_checked = replacements = isolation_queries = 0
    rewards = []
    for episode,(old,new) in enumerate(zip(baseline,outputs)):
        for key in ['prompt_ids','response_ids','response_mask','output','widths','path_lengths','stats']:
            assert old[key] == new[key], (episode,key)
        assert new['widths'] == [3,2] and not new['stats']['invalid_width']
        covered = [0]*len(new['response_mask'])
        for a,b in zip(old['policy_calls'],new['policy_calls']):
            assert {k:v for k,v in a.items() if k != 'old_logprobs'} == {k:v for k,v in b.items() if k != 'old_logprobs'}
            old_deltas.extend(abs(x-y) for x,y in zip(a['old_logprobs'],b['old_logprobs']))
            full,_ = replay.score_call(model,b)
            replay_deltas.extend((full.detach().cpu()-torch.tensor(b['old_logprobs'])).abs().tolist())
            start = b['response_start']
            for offset,raw in enumerate(b['generated_ids']):
                at = start+offset
                assert new['response_mask'][at] == 1 and covered[at] == 0
                covered[at] = 1
                visible = new['response_ids'][at]
                if raw != visible:
                    assert raw == 16 and visible in [13,15]
                    replacements += 1
                origins_checked += 1
        assert covered == new['response_mask'] and 0 in covered
        ids = torch.tensor(new['prompt_ids']+new['response_ids'])
        positions,spans = layout(ids,len(new['prompt_ids']),[10,11,12,13],0)
        allowed = attention(ids,len(new['prompt_ids']),[10,11,12,13],0)
        assert len(spans) == 2
        for ranges in spans:
            assert len({int(positions[s]) for s,e in ranges}) == 1
            first = ranges[0][0]
            for s,e in ranges[1:]:
                assert not allowed[s:e,first:s].any()
                isolation_queries += e-s
        with torch.inference_mode():
            additive = torch.zeros_like(allowed,dtype=torch.float32).masked_fill_(~allowed,-torch.inf)
            before = model(input_ids=ids[None],position_ids=positions[None],attention_mask=additive[None,None],use_cache=False).logits
            changed = ids.clone()
            changed[spans[0][0][0]+3] = 22
            after = model(input_ids=changed[None],position_ids=positions[None],attention_mask=additive[None,None],use_cache=False).logits
            for s,e in spans[0][1:]:
                assert (before[:,s:e]-after[:,s:e]).abs().max() < 1e-5
        def grade(t):
            s=t['stats']
            return reward.score(True,True,s['critical_depth'],s['sampled_tokens'],t['widths'],
                                forward_calls=s['actual_model_forward_calls'])
        assert grade(old) == grade(new)
        rewards.append(grade(new))
    assert max(old_deltas) < 1e-5 and max(replay_deltas) < 1e-5
    # Another episode's content cannot affect this episode's likelihood.
    changed_prompts = copy.deepcopy(prompts)
    changed_prompts[0][-1] = 28
    altered,_ = run_candidate(changed_prompts)
    perturb_delta = max(abs(a-b) for old,new in zip(outputs[1:],altered[1:])
                        for x,y in zip(old['policy_calls'],new['policy_calls'])
                        for a,b in zip(x['old_logprobs'],y['old_logprobs']))
    assert perturb_delta < 1e-5
    result = dict(passed=True,proof_only_forced_actions=True,model='tiny-Qwen3-CPU-FP32',
                  full_execute_trace_parity=True,action_origins_checked=origins_checked,
                  raw_stop_visible_replacements_checked=replacements,sibling_mask_queries_checked=isolation_queries,
                  repeated_positions_checked=True,max_old_logp_delta=max(old_deltas),
                  max_replay_logp_delta=max(replay_deltas),cross_episode_perturbation_delta=perturb_delta,
                  episode_forward_calls=[t['stats']['actual_model_forward_calls'] for t in outputs],
                  server_forward_calls=sum(s['physical_forward_calls'] for s in server_stats),
                  instrumented_actual_model_forward_calls=observed_server_calls,
                  server_prefill_calls=sum(s['prefill_forward_calls'] for s in server_stats),
                  server_decode_calls=sum(s['decode_forward_calls'] for s in server_stats),
                  episode_rewards=rewards,gpu4b_proof_not_complete=True,
                  source_sha256={n:hashlib.sha256((RUNNER/n).read_bytes()).hexdigest()
                                 for n in ['rollout.py','structured_replay.py','decoder.py','microbatch_decoder.py']})
    (HERE/'cpu-execute-proof.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['episode_rewards','source_sha256']}))


if __name__ == '__main__':
    main()
