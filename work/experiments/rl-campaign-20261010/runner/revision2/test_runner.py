"""Meaningful executor regression tests; no GPU or ML dependency needed."""
import unittest
from rollout import TAGS, execute
from train import centered, format_flags


class Tokenizer:
    pad_token_id = 0
    def __init__(self):
        self.tags = {x:1000+i for i,x in enumerate(TAGS)}
    def encode(self, text, add_special_tokens=False):
        return [self.tags[text]] if text in self.tags else [ord(x)+1 for x in text]
    def decode(self, ids, skip_special_tokens=False):
        inverse = {v:k for k,v in self.tags.items()}
        return ''.join(inverse[x] if x in inverse else chr(x-1) for x in ids)


class RunnerTests(unittest.TestCase):
    def scripted(self, widths, stop='</Path>', batched=False):
        tok = Tokenizer()
        script = []
        for width in widths:
            plan = 'Plan:\n'+''.join(f'{i}: compute useful value\n' for i in range(1,width+1))
            script.append(('main',tok.encode(plan)+tok.encode('<Parallel>')))
            script.append(('width',tok.encode(str(width)+'\n')))
            for i in range(width):
                script.append(('path',tok.encode('X'+str(len(script)))+tok.encode(stop)))
            script.append(('summary',tok.encode('Merged.\n')+tok.encode('</Summary>')))
        script.append(('main',tok.encode('\nFinal Answer: 2')+[999]))
        calls = []
        def decoder(call, budget, stops):
            phase, raw = script.pop(0)
            self.assertEqual(call['phase'], phase)
            self.assertLessEqual(len(raw),budget)
            if phase=='path':
                siblings = [c for c in calls if c['phase']=='path']
                previous_merge = next((j for j,c in reversed(list(enumerate(calls))) if c['phase']=='summary'),-1)
                # A branch prefix contains the common fork prefix plus only its own header.
                for sibling in calls[previous_merge+1:]:
                    if sibling['phase']=='path':
                        self.assertNotIn(tok.decode(sibling['generated_ids'][:-1]),tok.decode(call['prompt_ids']))
            result = dict(call,generated_ids=raw)
            calls.append(result)
            return raw,[-1.]*len(raw),len(raw)
        if batched:
            class BatchDecoder:
                last_batch_stats={}
                def __call__(self,*args):
                    return decoder(*args)
                def decode_many(self,calls,budgets,stops):
                    outputs=[decoder(c,b,stops) for c,b in zip(calls,budgets)]
                    groups=[outputs[i:i+2] for i in range(0,len(outputs),2)]
                    self.last_batch_stats=dict(physical_forward_calls=sum(max(len(x[0]) for x in g) for g in groups),
                                               prefill_forward_calls=len(groups),microbatch_max_paths=2)
                    return outputs
            decode=BatchDecoder()
        else:
            decode=decoder
        trace = execute(tok,tok.encode('Problem:\n'),decode,[999],response_budget=4096)
        self.assertFalse(script)
        return tok,trace

    def test_four_rounds_many_widths_and_isolated_siblings(self):
        tok,trace = self.scripted([2,3,4,8])
        self.assertEqual(trace['widths'],[2,3,4,8])
        self.assertEqual(trace['stats']['forks'],4)
        self.assertEqual(len([c for c in trace['policy_calls'] if c['phase']=='path']),17)
        self.assertTrue(format_flags(trace['output'],trace['stats'])[1])
        coverage = [0]*len(trace['response_mask'])
        for c in trace['policy_calls']:
            a=c['response_start']; b=a+len(c['generated_ids'])
            self.assertFalse(any(coverage[a:b]))
            coverage[a:b]=[1]*(b-a)
        self.assertEqual(coverage,trace['response_mask'])
        self.assertGreater(trace['stats']['forced_tokens'],0)
        self.assertGreater(trace['stats']['actual_model_forward_calls'],trace['stats']['critical_depth'])

    def test_replaced_stop_is_raw_policy_target(self):
        tok,trace = self.scripted([4],stop='<Parallel>')
        for c in trace['policy_calls']:
            if c['phase']=='path':
                self.assertEqual(c['generated_ids'][-1],tok.tags['<Parallel>'])
                self.assertEqual(trace['response_ids'][c['response_start']+len(c['generated_ids'])-1],tok.tags['</Path>'])
                self.assertEqual(trace['response_mask'][c['response_start']+len(c['generated_ids'])-1],1)

    def test_unknown_or_malformed_width_never_forks(self):
        tok=Tokenizer(); script=[tok.encode('<Parallel>'),tok.encode('9\n')]
        trace=execute(tok,tok.encode('Q'),lambda call,budget,stops:(script.pop(0),[-1.] if call['phase']=='main' else [-1.,-1.],1),[999])
        self.assertTrue(trace['stats']['invalid_width'])
        self.assertEqual(trace['widths'],[])
        self.assertFalse(format_flags(trace['output'],trace['stats'])[0])

    def test_reward_scale_is_preserved_without_std(self):
        self.assertEqual(centered([1.,0.,1.,0.]),[.5,-.5,.5,-.5])
        self.assertEqual(centered([.1,0.,.1,0.]),[.05,-.05,.05,-.05])
        self.assertEqual(centered([0.,0.,0.,0.]),[0.,0.,0.,0.])

    def test_batched_physical_work_charged_once_with_identical_seed_protocol(self):
        _,serial=self.scripted([2,3,4,8])
        _,batch=self.scripted([2,3,4,8],batched=True)
        self.assertEqual(serial['response_ids'],batch['response_ids'])
        self.assertEqual([c['seed'] for c in serial['policy_calls']],[c['seed'] for c in batch['policy_calls']])
        self.assertEqual(batch['stats']['sampled_tokens'],batch['stats']['serial_equivalent_forward_calls'])
        self.assertLess(batch['stats']['actual_model_forward_calls'],batch['stats']['sampled_tokens'])
        expected=sum(len(c['generated_ids']) for c in batch['policy_calls'] if c['phase']!='path')
        expected+=sum(g['physical_forward_calls'] for g in batch['fork_batch_ledger'])
        self.assertEqual(expected,batch['stats']['actual_model_forward_calls'])


if __name__=='__main__':
    unittest.main()
