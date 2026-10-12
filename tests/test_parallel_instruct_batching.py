import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).parents[1]/'experiments/parallel_instruct/batching.py'
s=importlib.util.spec_from_file_location('batching',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class BatchTests(unittest.TestCase):
    def records(self,world,prompts=8,group=4):
        return [[dict(prompt_index=p,sample_index=s,id=f'q{p}',reward=[1.,.6,0.,0.][s%4] if p%2==0 else 0.)
                 for p,s in m.assignments(rank,world,prompts,group)] for rank in range(world)]

    def test_effective_batch_and_sampler_seeds_are_gpu_independent(self):
        expected={(p,s) for p in range(8) for s in range(4)}
        for world in [1,2,4,8,12,16,24,32]:
            with self.subTest(world=world):
                pairs=[(r['prompt_index'],r['sample_index']) for rank in self.records(world) for r in rank]
                self.assertEqual(set(pairs),expected);self.assertEqual(len(pairs),32)
                self.assertTrue(all(m.assignments(r,world,8,4) for r in range(world)))
                seeds={m.rollout_seed(3,51,p,s) for p,s in pairs}
                self.assertEqual(len(seeds),32)

    def test_eight_gpu_preserves_four_local_responses(self):
        for rank in range(8):
            self.assertEqual(m.assignments(rank,8,8,4),[(rank,s) for s in range(4)])
        self.assertEqual([len(m.assignments(r,24,8,4)) for r in range(3)],[2,1,1])
        self.assertTrue(all(len(m.assignments(r,32,8,4))==1 for r in range(32)))

    def test_group_advantages_and_ddp_gradient_match_old_batch32(self):
        reference=None
        for world in [1,4,8,12,16,24,32]:
            records=self.records(world);adv=m.prompt_advantages(records,8,4)
            if reference is None:reference=adv
            self.assertEqual(adv,reference)
            for prompt in range(8):self.assertAlmostEqual(sum(adv[prompt,s] for s in range(4)),0.)
            # Analytic derivative of independent per-response losses. DDP must
            # give global response mean even with uneven local episode counts.
            per_rank=[]
            for rank in records:
                per_rank.append(sum(adv[r['prompt_index'],r['sample_index']]*(r['prompt_index']*4+r['sample_index']+1) for r in rank)*m.ddp_loss_scale(world,8,4)/4096)
            observed=sum(per_rank)/world
            expected=sum(reference[p,s]*(p*4+s+1) for p in range(8) for s in range(4))/(32*4096)
            self.assertAlmostEqual(observed,expected,places=15)
            self.assertEqual([adv[1,s] for s in range(4)],[0.]*4)

    def test_bad_coverage_and_mixed_questions_fail(self):
        for mode in ['missing','duplicate','mixed','nan']:
            records=self.records(24)
            if mode=='missing':records[0].pop()
            if mode=='duplicate':records[0][1]['sample_index']=0
            if mode=='mixed':records[0][0]['id']='other'
            if mode=='nan':records[0][0]['reward']=float('nan')
            with self.assertRaises(ValueError):m.prompt_advantages(records,8,4)
        for args in [(0,0,8,4),(0,33,8,4),(-1,8,8,4),(0,8,8,1)]:
            with self.assertRaises(ValueError):m.assignments(*args)

    def test_all_gpu_presets_keep_batch32_and_fit_one_or_more_nodes(self):
        import json
        root=Path(__file__).parents[1]/'experiments/parallel_instruct/configs'
        for world in [1,2,4,8,16,24,32]:
            cfg=json.loads((root/f'r2-{world}gpu.json').read_text())
            self.assertEqual(cfg['expected_world_size'],world)
            self.assertEqual(cfg['processes_per_node'],min(world,8))
            self.assertEqual(world%cfg['processes_per_node'],0)
            self.assertEqual(cfg['global_batch'],dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32))

    def test_prepare_run_supports_every_preset(self):
        import json,subprocess,sys,tempfile
        root=Path(__file__).parents[1]
        with tempfile.TemporaryDirectory(dir=root/'work') as directory:
            d=Path(directory);model=d/'model';model.mkdir()
            for name in ['train','val','scorer','system']:(d/name).write_text('fixture')
            for world in [1,2,4,8,16,24,32]:
                cfg=json.loads((root/f'experiments/parallel_instruct/configs/r2-{world}gpu.json').read_text())
                cfg.update(model=str(model),**{name:str(d/name) for name in ['train','val','scorer','system']})
                source=d/f'config-{world}.json';source.write_text(json.dumps(cfg))
                output=d/f'run-{world}'
                subprocess.run([sys.executable,str(root/'experiments/parallel_instruct/prepare_run.py'),'--config',str(source),'--run-root',str(output)],check=True,capture_output=True)
                generated=json.loads((output/'production-config-v2.json').read_text())
                self.assertEqual(generated['expected_world_size'],world)
                self.assertEqual(generated['global_batch']['responses_per_step'],32)
                self.assertFalse((output/'control/production-approved.json').exists())

    def test_batch_changes_are_explicit(self):
        for prompts,group,world in [(16,4,8),(32,8,64),(3,4,10)]:
            pairs=[pair for r in range(world) for pair in m.assignments(r,world,prompts,group)]
            self.assertEqual(len(set(pairs)),prompts*group)
            self.assertEqual(len(pairs),prompts*group)

if __name__=='__main__':unittest.main()
