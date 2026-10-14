import sys
sys.path.insert(0,'${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations')
import evaluate_math500 as e
e.summarize(e.R/"initial-lr1e-3-structured500")
import json,hashlib,subprocess,datetime
out=e.R/'initial-lr1e-3-structured500'
rows=[json.loads(l) for f in out.glob('traces-*.jsonl') for l in f.read_text().splitlines() if l.strip()]
planned=[json.loads(l) for l in (e.R/'questions-500.jsonl').read_text().splitlines()]
assert len(rows)==len(planned)==500 and len({r['id'] for r in rows})==500
assert {r['id'] for r in rows}=={r['id'] for r in planned}
gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
receipt=dict(passed=not gpu,at=datetime.datetime.now(datetime.timezone.utc).isoformat(),recovered_worker=1,original_worker_exit_failure_preserved=True,repaired_coverage=500,gpu_processes=gpu.splitlines(),repair_evaluator_sha256=hashlib.sha256(Path(e.__file__).read_bytes()).hexdigest(),original_manifest_evaluator_sha256=json.loads((out/'manifest.json').read_text())['evaluator_sha256'],only_evaluator_change='per-worker fixed VLLM_PORT before engine init',trace_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('traces-*.jsonl')})
(out/'recovery-terminal-proof.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['passed'],'GPU processes remain after repaired worker exit'
