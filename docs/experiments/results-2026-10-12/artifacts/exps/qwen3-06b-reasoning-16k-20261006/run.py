import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from rescore import ROOT, PREVIOUS, WORK, check_extractor, rescore

def now():
    return datetime.now(timezone.utc).isoformat()

def write(name, data):
    (WORK / name).write_text(json.dumps(data, indent=2) + '\n')

if __name__ == '__main__':
    assert check_extractor() == 8
    result = WORK / 'results/eval/reasoning-16k'
    result.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(PATH=str(ROOT / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7', NPROC_PER_NODE='8', OMP_NUM_THREADS='1', RAY_TMPDIR='${TMPDIR}/pr1_reasoning16k', PARALLEL_R1_OUTPUT_ROOT=str(WORK / 'results'), PARALLEL_R1_SCRATCH_ROOT='${SHM_ROOT}/pr1_reasoning16k', HF_HOME='${MODEL_ROOT}/huggingface', PARALLEL_R1_EVAL_NAME='reasoning-16k')
    command = ['bash', 'training_scripts/eval_qwen3_06b.sh', str(PREVIOUS / 'models/reasoning'), 'actor_rollout_ref.rollout.mode=sync', 'actor_rollout_ref.rollout.enforce_eager=true', 'actor_rollout_ref.rollout.val_kwargs.n=1', 'data.max_response_length=16384', 'data.val_batch_size=512', 'actor_rollout_ref.rollout.max_num_batched_tokens=18432', 'actor_rollout_ref.rollout.gpu_memory_utilization=0.8', f'data.val_files={PREVIOUS / "plain.parquet"}', f'data.train_files={PREVIOUS / "plain.parquet"}', 'ray_init.num_cpus=40']
    manifest = json.loads((PREVIOUS / 'manifest.json').read_text())
    manifest.update(started=now(), max_response_tokens=16384, mode='reasoning', gpus=list(range(8)), val_batch_size=512, comparison='Same questions, prompts, weights, temperature=1, top_p=1, top_k=-1 as the 3k run; response budget increased. Legacy metrics and corrected extraction reported separately.', command=command, scorer_sha256=hashlib.sha256((WORK / 'rescore.py').read_bytes()).hexdigest())
    write('manifest.json', manifest)
    write('status.json', dict(status='running', started=now(), pid=os.getpid()))
    (WORK / 'started').write_text(now())
    try:
        with (result / 'driver.log').open('w') as log:
            rc = subprocess.run(command, cwd=PREVIOUS / 'code/verl', env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        (result / 'exit_code').write_text(str(rc))
        if rc:
            raise RuntimeError(f'Inference exited {rc}')
        report = rescore('reasoning-16k', result, 'reasoning')
        write('status.json', dict(status='complete', finished=now(), answers=report['answers']))
        (WORK / 'exit_code').write_text('0')
    except Exception as error:
        write('status.json', dict(status='failed', finished=now(), error=str(error)))
        (WORK / 'exit_code').write_text('1')
        raise
    finally:
        (WORK / 'finished').write_text(now())
