import hashlib,json,shutil,py_compile
from pathlib import Path
RUN=Path(__file__).resolve().parent
ROOT=RUN.parent.parent
OLD=ROOT/'exps/rl-unseen-s2-bs32-500-20261007/code'
CODE=RUN/'code'
assert not CODE.exists(),'Never modify an existing experiment snapshot'
shutil.copytree(OLD,CODE,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
shutil.copyfile(RUN/'reward.py',CODE/'verl/verl/utils/reward_score/gsm_depth.py')
def patch(file,old,new):
    p=CODE/file;s=p.read_text();assert s.count(old)==1,(file,s.count(old));p.write_text(s.replace(old,new))
patch('verl/verl/parallel_thinking_generation_v3/repro_trace.py',
      "        write_record('traces', self.record)",
      "        from verl.utils.reward_score.gsm_depth import critical_depth\n        self.record['critical_depth'] = critical_depth(self.record['calls'])\n        write_record('traces', self.record)")
patch('verl/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py',
      "                'forks': self.trace.record['executed_fork_count'],",
      "                'critical_depth': self.trace.record['critical_depth'],\n                'forks': self.trace.record['executed_fork_count'],")
patch('verl/verl/workers/reward_manager/naive.py',
      '            extra_info["global_steps"] = global_steps',
      '            extra_info["global_steps"] = global_steps\n            extra_info["validate"] = bool(data.meta_info.get("validate", False))\n            extra_info["parallel_stats"] = data_item.non_tensor_batch["parallel_stats"]')
patch('verl/verl/trainer/ppo/ray_trainer.py',
      "                            metrics['parallel/forks_mean'] = float(np.mean([item['forks'] for item in parallel_stats]))",
      "                            metrics['parallel/forks_mean'] = float(np.mean([item['forks'] for item in parallel_stats]))\n                            metrics['parallel/critical_depth_mean'] = float(np.mean([item['critical_depth'] for item in parallel_stats]))")
manifest=json.loads((ROOT/'exps/rl-unseen-s2-bs32-500-20261007/manifest.json').read_text())
base=[x for x in manifest['overrides'] if not x.startswith(('trainer.resume_','trainer.save_freq=','trainer.test_freq=','trainer.total_training_steps=','actor_rollout_ref.actor.checkpoint.','trainer.max_actor_ckpt_to_keep='))]
base += [f'data.train_files={RUN}/train.parquet',f'data.val_files={RUN}/validation.parquet',
         'data.val_batch_size=256','data.shuffle=true','++data.seed=20261008',
         'trainer.resume_mode=disable','trainer.save_freq=100','trainer.test_freq=50','trainer.total_training_steps=800',
         'trainer.max_actor_ckpt_to_keep=2','trainer.logger=[console]',
         'actor_rollout_ref.actor.checkpoint.save_contents=[model,optimizer,extra,hf_model]',
         'actor_rollout_ref.actor.checkpoint.load_contents=[model,optimizer,extra]',
         f'custom_reward_function.path={CODE}/verl/verl/utils/reward_score/gsm_depth.py',
         'custom_reward_function.name=compute_score','+custom_reward_function.reward_kwargs.depth_lambda=0.0001']
manifest.update(run=RUN.name,checkpoint=manifest['checkpoint'],steps=800,stages=['s2','depth'],overrides=base,
                lambda_per_decode_depth=0.0001,stage_initialization='Each starts independently from original Unseen SFT; retry resumes only its own full checkpoint.',
                depth_definition='Sum of generated main/summary token counts plus maximum generated path token count per fork. Excludes injected tags and prefill compute; not physical batched GPU forwards.',
                checkpoint_policy={'save_every':100,'retain':2,'full_training_state':True,'hf_weights':True},
                max_attempts_per_stage=3,stall_timeout_seconds=2700,stage_attempt_timeout_seconds=86400)
for key in ['changed_file_sha256','resume_checkpoint','resumed_from_step','additional_updates','implementation_changes','validation']:
    manifest.pop(key,None)
manifest['hypothesis']='Matched GSM-Infinite RL: original S2 versus correctness indicator minus critical generation depth; each independently starts from original Unseen SFT.'
manifest['data_sha256']=json.loads((RUN/'data-audit.json').read_text())['data_sha256']
manifest['code_sha256']={str(p.relative_to(CODE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in CODE.rglob('*') if p.is_file() and p.suffix in ['.py','.yaml','.sh']}
manifest['script_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in RUN.glob('*.py')}
for p in CODE.rglob('gsm_depth.py'):py_compile.compile(str(p),doraise=True)
(RUN/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared frozen snapshot',len(manifest['code_sha256']),'files')
