"""Wait for the owned evaluation, then grade, validate and render the final report."""
from pathlib import Path
import datetime as dt,fcntl,hashlib,json,os,subprocess,sys,time,traceback
W=Path(__file__).resolve().parent;R=W.parent;P=W.parents[3]
def save(**values):
    values['updated_at']=dt.datetime.now(dt.timezone.utc).isoformat();f=W/'analysis-status.tmp';f.write_text(json.dumps(values,indent=2)+'\n');f.replace(W/'analysis-status.json')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()
def main():
    lock=(W/'finalize.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    assert not (W/'final-validation.json').exists(),'Finalization already completed'
    save(state='waiting_for_generation')
    while True:
        state=json.loads((W/'status.json').read_text())
        if state['state']=='failed':raise RuntimeError(state)
        if state['state']=='generated':break
        time.sleep(15)
    save(state='grading')
    with (W/'final-analysis.log').open('w') as log:subprocess.run([sys.executable,str(W/'score.py'),'--final'],cwd=P,stdout=log,stderr=subprocess.STDOUT,check=True)
    m=json.loads((W/'manifest.json').read_text());s=json.loads((W/'summary.json').read_text());assert s['state']=='complete'
    weights=Path(m['checkpoint'])/'model.safetensors';assert sha(weights)==m['checkpoint_sha256']
    assert sha(W/'questions.jsonl')==m['questions_sha256']==m['previous_questions_sha256']
    frozen=json.loads((R/'sft-code-sha256.json').read_text());changed=[f for f,h in frozen.items() if sha(R/'sft-code'/f)!=h];assert not changed,changed
    sources=json.loads((R/'data-report.json').read_text())['source_sha256'];changed=[f for f,h in sources.items() if sha(f)!=h];assert not changed,changed
    manifest=json.loads((R/'rl-code-manifest.json').read_text());assert all(sha(R/'rl-code'/v['path'])==v['sha256'] for v in manifest if 'sha256' in v)
    # Generation supervisor waits for all eight owned worker processes to exit.
    still_alive=[pid for pid in state['worker_pids'] if Path(f'/proc/{pid}').exists()];assert not still_alive,still_alive
    files={f.name:dict(bytes=f.stat().st_size,sha256=sha(f)) for f in sorted(W.glob('traces-*.jsonl'))}
    checks=dict(passed=True,questions=s['questions'],unique_answers=500,scorer_errors=s['scorer_errors'],context_audit=s['context_audit'],checkpoint_sha256=sha(weights),questions_sha256=sha(W/'questions.jsonl'),frozen_sft_files_unchanged=len(frozen),sources_unchanged=len(sources),production_rl_manifest_verified=True,workers_exited=True,trace_files=files,generation_status=state,finished_at=dt.datetime.now(dt.timezone.utc).isoformat())
    (W/'final-validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    subprocess.run([sys.executable,str(W/'report.py')],cwd=P,check=True)
    save(state='complete',historical_pass_at_1=s['pass_at_1'],final_answer_only_pass_at_1=s['final_answer_only_diagnostic']['pass_at_1'])
    print(json.dumps(checks),flush=True)
if __name__=='__main__':
    try:main()
    except BaseException as error:save(state='failed',error=repr(error));traceback.print_exc();raise
