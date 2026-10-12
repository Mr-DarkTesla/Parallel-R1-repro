"""Create an isolated corrected fullwidth8, weights-only training runtime."""
from pathlib import Path
import hashlib
import json
import shutil

R = Path.cwd()
B = R / 'work/experiments/rl-r2-24gpu-20261012'
source = R / 'work/experiments/rl-instruct-20261011/production-runner'
target = B / 'runner'
assert not target.exists()
shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
p = target / 'train.py'
s = p.read_text()
s = s.replace("grade = scorer.grade(trace['output'],str(row['answer']))", "grade = scorer.grade('<think>\\n'+trace['output'],str(row['answer']))")
s = s.replace("grade = scorer.grade(trajectory['output'], str(row['answer']))", "grade = scorer.grade('<think>\\n'+trajectory['output'], str(row['answer']))")
assert "scorer.grade(trace['output']" not in s and "scorer.grade(trajectory['output']" not in s
s = s.replace("world = int(os.environ.get('WORLD_SIZE', '1'))", "world = int(os.environ.get('WORLD_SIZE', '1'))\n    if world != int(cfg.get('expected_world_size', 24)):\n        raise ValueError('Expected exactly 24 distributed training ranks')\n    if cfg.get('resume'):\n        raise ValueError('This run exports weights only and starts fresh')")
s = s.replace("max_paths=int(cfg.get('max_batched_paths',2))", "max_paths=int(cfg.get('max_batched_paths',8))")
s = s.replace("    eos = native_eos_ids(cfg['model'], tok)", "    if int(cfg.get('max_batched_paths',8)) != 8 or not cfg.get('batch_decoder'):\n        raise ValueError('Fullwidth8 runtime required, without subgroup fallback')\n    eos = native_eos_ids(cfg['model'], tok)")
needle = "    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})"
s = s.replace(needle, """    physical_forward_counter = [0]
    original_forward = model.forward
    def counted_forward(*args, **kwargs):
        physical_forward_counter[0] += 1
        return original_forward(*args, **kwargs)
    model.forward = counted_forward
""" + needle)
s = s.replace("                trace = execute(tok,prefix,decoder,eos,budget", "                physical_before = physical_forward_counter[0]\n                trace = execute(tok,prefix,decoder,eos,budget")
s = s.replace("                grade = scorer.grade('<think>\\n'+trace['output']", "                assert physical_forward_counter[0]-physical_before == trace['stats']['actual_model_forward_calls']\n                assert all(x['microbatch_max_paths']==8 and x['sequential_subgroup_count']==1 for x in trace['fork_batch_ledger'])\n                grade = scorer.grade('<think>\\n'+trace['output']")
s = s.replace("            trajectory = execute(tok, prefix, decoder", "            physical_before = physical_forward_counter[0]\n            trajectory = execute(tok, prefix, decoder")
s = s.replace("            grade = scorer.grade('<think>\\n'+trajectory['output']", "            assert physical_forward_counter[0]-physical_before == trajectory['stats']['actual_model_forward_calls']\n            assert all(x['microbatch_max_paths']==8 and x['sequential_subgroup_count']==1 for x in trajectory['fork_batch_ledger'])\n            grade = scorer.grade('<think>\\n'+trajectory['output']")
s = s.replace("    validate(start_step)", "    if not cfg.get('skip_validation', False):\n        validate(start_step)")
s = s.replace("        if step in cfg.get('checkpoint_steps',[]) or (not cfg.get('checkpoint_steps') and step % int(cfg.get('checkpoint_every',16)) == 0) or step == steps:",
              "        if not cfg.get('skip_exports',False) and step in cfg['checkpoint_steps']:")
s = s.replace("        row = train[((step-1)*world+rank) % len(train)]", """        position = (step-1)*world + rank
        epoch, offset = divmod(position, len(train))
        order = list(range(len(train)))
        random.Random(cfg.get('data_seed',20261012)+epoch).shuffle(order)
        row = train[order[offset]]""")
s = s.replace("            validate(step)", "            if not cfg.get('skip_validation', False):\n                validate(step)")
start = s.index("            torch.save(dict(cpu_rng=")
end = s.index("    if rank==0:\n        atomic_json(output/'result.json'", start)
s = s[:start] + """            if rank==0:
                cpu_state = {k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()}
                if not all(torch.isfinite(v).all().item() for v in cpu_state.values()):
                    raise FloatingPointError('Nonfinite exported model weights')
                model.save_pretrained(checkpoint/'hf', state_dict=cpu_state,
                                      safe_serialization=True, max_shard_size='100GB')
                tok.save_pretrained(checkpoint/'hf')
                del cpu_state
                assert (checkpoint/'hf'/'model.safetensors').is_file()
                assert not (checkpoint/'hf'/'model.safetensors.index.json').exists()
                assert not list(checkpoint.glob('optimizer*')) and not list(checkpoint.glob('rng*'))
            if world>1:
                dist.barrier()
            if rank==0:
                atomic_json(checkpoint/'complete.json',dict(step=step,world_size=world,
                            model=True,optimizer=False,rng=False,unsharded=True))
""" + s[end:]
s = s.replace("sampler='Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation'", "sampler='Exact FP32 HF fullwidth8, temperature1 top_p1 nofilter; fixed clean validation seed'")
s = s.replace("            trajectories.append(trajectory)", """            coverage = [0]*len(trajectory['response_mask'])
            for call in trajectory['policy_calls']:
                for at in range(call['response_start'],call['response_start']+len(call['generated_ids'])):
                    assert not coverage[at] and trajectory['response_mask'][at] == 1
                    coverage[at] = 1
            assert coverage == trajectory['response_mask']
            trajectories.append(trajectory)""")
s = s.replace("        memory_stages.append(memory_snapshot('after_optimizer'))", """        memory_stages.append(memory_snapshot('after_optimizer'))
        if step == cfg.get('resident_fixture_step'):
            assert updated and optimizer.optim.state
            fixtures = []
            model.eval()
            with torch.no_grad():
                tags = [tok.encode(t,add_special_tokens=False)[0] for t in
                        ['<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>']]
                tc = tok.encode('</think>',add_special_tokens=False)[0]
                body = tok.encode('1+1=2. ',add_special_tokens=False)
                assert not set(body)&set(tags+[tc]+eos)
                fixture_prefix = prefix+tok.encode(' Initial known values. '*512,add_special_tokens=False)
                for width in [2,3,4,6,8]:
                    for round_index in range(4):
                        calls = [dict(phase='path',prompt_ids=fixture_prefix+tok.encode(
                                  'Plan: Check independent parts.\\n<Parallel>'+str(width)+'\\n<Path>'+str(row_index+1)+'\\n',add_special_tokens=False),
                                  structure_start=len(prefix),structure_tags=tags[:4],pad_id=tok.pad_token_id,
                                  blocked_token_ids=[tc],temperature=1.,seed=123400+row_index+round_index*100)
                                 for row_index in range(width)]
                        targets = [(body*16)[:16+row_index*4]+[tags[3]] for row_index in range(width)]
                        observed_before = physical_forward_counter[0]
                        decoded = decoder.decode_many(calls,128,[*tags,*eos],target_sequences=targets)
                        stats = dict(decoder.last_batch_stats)
                        assert stats['sequential_subgroup_count']==1 and stats['requested_rows']==width
                        assert physical_forward_counter[0]-observed_before==stats['physical_forward_calls']==max(map(len,targets))
                        maximum_drift = 0.
                        for call,value in zip(calls,decoded):
                            assert value[0] == targets[calls.index(call)]
                            logp,_ = replay.score_call(model,dict(call,generated_ids=value[0]))
                            maximum_drift=max(maximum_drift,float((logp-torch.tensor(value[1],device=device)).abs().max()))
                            del logp
                        assert maximum_drift<=cfg.get('max_replay_drift',.01)
                        fixtures.append(dict(width=width,round=round_index,physical_forward_calls=stats['physical_forward_calls'],subgroups=1,
                                             max_replay_logp_drift=maximum_drift,optimizer_resident=True))
                        del calls,targets,decoded
            atomic_json(output/('resident-fixtures-rank-'+str(rank)+'.json'),dict(passed=True,rank=rank,world_size=world,
                        cases=fixtures,memory=memory_snapshot('resident_fullwidth8_fixtures')))
            model.train()""")
s = s.replace('del decoder, optimizer, ddp, probe, model',
              'del decoder, optimizer, ddp, probe, model, original_forward, counted_forward')
p.write_text(s)
compile(s,str(p),'exec')
assert 'max_shard_size=\'4GB\'' not in s
assert 'torch.save(' not in s
assert "physical_forward_counter[0]-physical_before" in s
decoder_path=target/'microbatch_decoder.py'
d=decoder_path.read_text().replace('max_paths=2','max_paths=8')
d=d.replace("        budgets = [budget]*len(calls)", "        if self.max_paths != 8 or not 1 <= len(calls) <= 8:\n            raise ValueError('Fullwidth8 requires one complete group of 1..8 branches')\n        budgets = [budget]*len(calls)")
decoder_path.write_text(d)
compile(d,str(decoder_path),'exec')
manifest = {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in target.rglob('*') if p.is_file()}
(B/'runtime-build.json').write_text(json.dumps(dict(passed=True,sources=manifest,
     expected_world_size=24,max_batched_paths=8,checkpoint_steps=[50,100,200,300,400,500],
     weights_only=True,unsharded=True,optimizer_export=False,rng_export=False),indent=2)+'\n')
print(json.dumps(dict(files=len(manifest),train_sha256=manifest[str(p.relative_to(R))] if str(p.relative_to(R)) in manifest else hashlib.sha256((target/'train.py').read_bytes()).hexdigest())))
