"""Release both authorized RL arms from actual, independently reviewed proof."""
from pathlib import Path
import fcntl, hashlib, json, math, os, time

P=Path.cwd(); B=P/'work/experiments/rl-instruct-20261011'
S=P/'work/experiments/instruct-full-20261011'
lock=(B/'root-production-gate.lock').open('w')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,data):
    q=path.with_suffix('.tmp');q.write_text(json.dumps(data,indent=2)+'\n');q.replace(path)
status_path=B/'root-production-gate-status.json'
state=dict(state='waiting_for_actual_technical_pass',pid=os.getpid(),started_at=time.time())
save(status_path,state)
try:
    result_path=P/'work/experiments/night-20261010/cloud-continued/tmp2/results/305-instruct-rl-technical-step-resume.json'
    review_path=S/'independent-rl-technical-runtime-review.json'
    while not result_path.exists() or not review_path.exists():
        if result_path.exists():
            assert json.loads(result_path.read_text())['returncode']==0
        state['updated_at']=time.time();save(status_path,state);time.sleep(5)
    assert json.loads(result_path.read_text())['returncode']==0
    proof_path=B/'technical-launch.json'; proof=json.loads(proof_path.read_text())
    assert proof['passed'] and proof['state']=='passed' and proof['lane']=='tmp2'
    runtime=json.loads(review_path.read_text())
    assert runtime['passed'] and runtime['technical_proof_sha256']==sha(proof_path)
    source_path=S/'independent-rl-production-source-review.json'
    assert sha(source_path)=='c04e5d2019b38977a70c1e1239f6ee67c29257d3372b74c1579e0209be80ecfd'
    assert json.loads(source_path.read_text())['passed']
    seal_path=B/'production-seal.json'
    assert sha(seal_path)=='94cb83ff0271a12a4c07a91b6b96dce181dbbcb0349f1a1a11ee87c37494c17d'
    seal=json.loads(seal_path.read_text())
    for name,expected in seal['sha256'].items(): assert sha(P/name)==expected,name
    for name in ['step1','resume-step2']:
        cfg=json.loads((B/'technical-configs'/f'{name}.json').read_text())
        run=Path(cfg['output'])
        assert json.loads((run/'result.json').read_text())['completed']
        ranks=[m for line in (run/'metrics.jsonl').read_text().splitlines()
               for m in json.loads(line)['ranks']]
        assert len(ranks)==8 and {m['rank'] for m in ranks}==set(range(8))
        for m in ranks:
            assert m['trainable']>=4_000_000_000 and m['optimizer_step']
            assert all(math.isfinite(m[k]) for k in ['loss','grad_norm','backbone_update_l2'])
            assert m['backbone_update_l2']>0
            assert m['max_replay_logp_drift']<=.01 and m['mean_replay_logp_drift']<=.002 and m['p95_replay_logp_drift']<=.005
            if name=='resume-step2':
                assert all(m['resume_proof'].get(k) for k in
                    ['exact_local_adam_state','exact_cpu_rng','exact_cuda_rng','exact_python_rng'])
    configs={}
    for mode in ['strong_width','forward_only']:
        path=B/'production-configs'/f'{mode}-stage16.json'
        assert sha(path)==seal['configs'][f'{mode}-stage16']
        configs[mode]=json.loads(path.read_text())
    left={k:v for k,v in configs['strong_width'].items() if k not in ['reward_mode','lane','output']}
    right={k:v for k,v in configs['forward_only'].items() if k not in ['reward_mode','lane','output']}
    assert left==right and left['bonus_schedule']=='constant_no_annealing'
    assert not left['std_normalization']
    released=[]
    for mode,task in [('strong_width','306-instruct-rl-strong-width-stage16'),
                      ('forward_only','232-instruct-rl-forward-only-stage16')]:
        config=B/'production-configs'/f'{mode}-stage16.json'
        receipt=B/f'{mode}-production-root-approved.json'
        assert not receipt.exists()
        save(receipt,dict(approved=True,approved_at=time.time(),
            production_seal_sha256=sha(seal_path),config_sha256=sha(config),
            technical_proof_sha256=sha(proof_path),technical_result_sha256=sha(result_path),
            independent_runtime_review_sha256=sha(review_path),
            independent_source_review_sha256=sha(source_path)))
        draft=B/'production-queue-drafts'/f'{task}.json'
        job=json.loads(draft.read_text())
        assert job['cwd']==str(P)
        lane=configs[mode]['lane']
        destination=P/f'work/experiments/night-20261010/cloud-continued/{lane}/queue/{task}.json'
        assert not destination.exists()
        save(destination,job)
        released.append(dict(mode=mode,lane=lane,task=task,receipt_sha256=sha(receipt)))
    state.update(state='released',finished_at=time.time(),arms=released)
except BaseException as error:
    state.update(state='failed',error=repr(error),finished_at=time.time());raise
finally:save(status_path,state)
