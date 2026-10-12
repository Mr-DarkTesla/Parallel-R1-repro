"""Create a fresh immutable two-run snapshot; never modify old experiments."""
import hashlib,json,shutil,ast
from pathlib import Path
RUN=Path(__file__).resolve().parent;OLD=RUN.parent/'gsm-unseen-two-rewards-20261008';CODE=RUN/'code'
assert not CODE.exists(),'Snapshot already exists'
shutil.copytree(OLD/'code',CODE,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for name in ['train.parquet','validation.parquet','smoke-validation.parquet','data-audit.json']:
    shutil.copy2(OLD/name,RUN/name)
shutil.copy2(RUN/'reward.py',CODE/'verl/verl/utils/reward_score/gsm_depth.py')
shutil.copy2(RUN/'split_grpo.py',CODE/'verl/verl/trainer/ppo/split_grpo.py')
p=CODE/'verl/verl/trainer/ppo/ray_trainer.py';s=p.read_text()
old='''        advantages, returns = core_algos.compute_grpo_outcome_advantage(
            token_level_rewards=data.batch["token_level_rewards"],
            response_mask=grpo_calculation_mask,
            index=data.non_tensor_batch["uid"],
            norm_adv_by_std_in_grpo=norm_adv_by_std_in_grpo,
        )'''
new='''        if config.get("split_accuracy_aux", False):
            assert not config.get("use_kl_in_reward", False)
            from verl.trainer.ppo.split_grpo import compute_split_advantage
            advantages, returns, split_metrics = compute_split_advantage(
                data.non_tensor_batch["accuracy_reward"], data.non_tensor_batch["aux_reward"],
                data.non_tensor_batch["uid"], grpo_calculation_mask)
            data.meta_info["split_reward_metrics"] = split_metrics
        else:
'''+''.join('    '+line+'\n' for line in old.splitlines()).rstrip()
assert s.count(old)==1;s=s.replace(old,new)
marker="                        if self.config.algorithm.adv_estimator == 'grpo':"
assert s.count(marker)==1
s=s.replace(marker,"                        metrics.update(batch.meta_info.pop('split_reward_metrics', {}))\n"+marker)
p.write_text(s);ast.parse(s)
m=json.loads((OLD/'manifest.json').read_text())
m.update(run=RUN.name,steps=400,stages=['gated_depth','parallel_gain'],parent_run=str(OLD),
    hypothesis='Correctness-gated auxiliaries with accuracy-only standardization preserve coefficient scale and avoid all-wrong shortening gradients.',
    advantage_formula='standardize_group(accuracy) + aux_reward - group_mean(aux_reward)',
    reward_formulas={'gated_depth':'c - 0.0001*c*D','parallel_gain':'c + 0.2*c*valid_parallel*(1-D/T)'},
    bonus_alpha=0.2,lambda_per_decode_depth=0.0001,
    caveats=['Gated depth cost can still favor short correct answers.',
             'Relative efficiency may reward extra tokens in parallel paths; audit total length and validation.',
             'Both are separate independent runs from original Unseen-SFT; not continuation of old RL.'])
m['overrides']=[x.replace(str(OLD),str(RUN)).replace('trainer.total_training_steps=800','trainer.total_training_steps=400') for x in m['overrides']]
m['overrides']+=['+algorithm.split_accuracy_aux=true','+custom_reward_function.reward_kwargs.bonus_alpha=0.2']
m['code_sha256']={str(p.relative_to(CODE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in CODE.rglob('*') if p.is_file() and p.suffix in ['.py','.yaml','.sh']}
m['data_sha256']={name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in m['data_sha256']}
m['script_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in RUN.glob('*.py')}
(RUN/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'run':RUN.name,'steps_each':400,'stages':m['stages'],'code_files':len(m['code_sha256'])}))
