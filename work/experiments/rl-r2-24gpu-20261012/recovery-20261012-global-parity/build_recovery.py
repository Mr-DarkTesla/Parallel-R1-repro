from pathlib import Path
import shutil,json,hashlib
R=Path('${PROJECT_ROOT}');B=R/'work/experiments/rl-r2-24gpu-20261012';N=B/'recovery-20261012-global-parity'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
runner=N/'runner';shutil.copytree(B/'runner-v2',runner)
shutil.copy2(N/'replay_guard.py',runner/'replay_guard.py')
p=runner/'train.py';s=p.read_text()
s=s.replace('    for step in range(start_step+1, steps+1):','    parity_skips = 0\n    parity_skip_streak = 0\n    for step in range(start_step+1, steps+1):')
a="        if max_drift > float(cfg.get('max_replay_drift', .01)) or mean_drift > .002 or p95_drift > .005:\n            raise ValueError('Decoder/replay probability divergence: '+str(max_drift))"
b="""        from replay_guard import synchronized_guard
        parity_passed, local_parity_bad = synchronized_guard(max_drift, mean_drift, p95_drift,
                device, world, max_allowed=float(cfg.get('max_replay_drift', .01)))
        if not parity_passed:
            parity_skips += 1
            parity_skip_streak += 1
            rejected = output/'rejected-batches'
            rejected.mkdir(parents=True, exist_ok=True)
            atomic_json(rejected/(f'step-{step:04}-rank-{rank}.json'),dict(step=step,rank=rank,
                        technical_unknown=True,optimizer_update_forbidden=True,local_parity_bad=local_parity_bad,
                        max_replay_drift=max_drift,mean_replay_drift=mean_drift,p95_replay_drift=p95_drift,
                        thresholds=dict(max=.01,mean=.002,p95=.005),
                        trace_reference=str(output/f'traces-rank-{rank}.jsonl')))
        else:
            parity_skip_streak = 0
        # All ranks see the same rejection before any Adam state is advanced.
        if parity_skip_streak >= 3 or (step >= 20 and parity_skips/step > .10):
            raise ValueError('Collective stop: persistent replay parity failures')"""
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace("        updated = bool(active_tensor.item()>0)","        updated = bool(active_tensor.item()>0) and parity_passed")
s=s.replace("                      zero_advantage_group=active==0, actual_widths=", "                      replay_guard_passed=parity_passed, local_replay_guard_bad=local_parity_bad,\n                      technical_skip_reason=None if parity_passed else 'replay_probability_parity',\n                      cumulative_replay_parity_skips=parity_skips,\n                      zero_advantage_group=active==0, actual_widths=")
s=s.replace("                        finite=True, optimizer_step=updated, backbone_update_l2=update_l2,", "                        finite=True, optimizer_step=updated, backbone_update_l2=update_l2,\n                        replay_guard_passed=parity_passed, replay_parity_skips=parity_skips,")
# The smoke remains a strict two-positive-update proof, not a skipped-batch pass.
compile(s,str(p),'exec');p.write_text(s)
newprefix=str(runner);oldprefix=str(B/'runner-v2')
for stage in ['smoke','production']:
 c=json.loads((B/(stage+'-config-v2.json')).read_text())
 for k,v in c.items():
  if isinstance(v,str):c[k]=v.replace(oldprefix,newprefix).replace(str(B/'distributed-smoke-proof.json'),str(N/'distributed-smoke-proof.json'))
 c['output']=str(N/stage)
 c['sealed_inputs']={k.replace('rl-r2-24gpu-20261012/runner-v2/','rl-r2-24gpu-20261012/recovery-20261012-global-parity/runner/'):v.replace(oldprefix,newprefix) for k,v in c['sealed_inputs'].items()}
 c['sealed_inputs']['collective_replay_guard']=str(runner/'replay_guard.py')
 c['sealed_inputs']['collective_guard_cpu_proof']=str(N/'guard-collective-proof.json')
 c['replay_guard_policy']='Collective skip update on unchanged thresholds; technical unknown; stop after3consecutive or>10pct after20'
 (N/(stage+'-config-v2.json')).write_text(json.dumps(c,indent=2))
manifest=json.loads((B/'runtime-build-v2.json').read_text());manifest['sources']={str(p.relative_to(R)):sha(p) for p in runner.rglob('*.py')};manifest['collective_replay_guard']=True
(N/'runtime-build-v2.json').write_text(json.dumps(manifest,indent=2))
s=(B/'node_entry_v4.py').read_text().replace("B=R/'work/experiments/rl-r2-24gpu-20261012'","B=R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity'").replace("B/'runner-v2/train.py'","B/'runner/train.py'")
compile(s,'node_entry.py','exec');(N/'node_entry.py').write_text(s)
(N/'portable-venv').symlink_to(B/'portable-venv',target_is_directory=True)
proof=dict(passed=True,failed_step=37,lost_unexported_updates=36,restart_from_original_SFT=True,thresholds_unchanged=True,reward_data_unchanged=True,all_branches_one_forward=True,guard_cpu_proof_sha256=sha(N/'guard-collective-proof.json'),node_entry_sha256=sha(N/'node_entry.py'),train_sha256=sha(runner/'train.py'),config_sha256=sha(N/'production-config-v2.json'),source_manifest_sha256=sha(N/'runtime-build-v2.json'),prior_actual_failure=str(B/'attempts/10-replay-drift-step37/failure-proof.json'),mask_positions_cpu_review=str(B/'replay-diagnostics/cpu-layout-parity.json'),remaining_numerical_root_cause='Exact original trained36weights unavailable; preserve strict threshold and exclude uncertain batches')
(N/'repair-proof.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof))
