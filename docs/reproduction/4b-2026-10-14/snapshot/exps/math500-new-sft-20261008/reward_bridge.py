"""Keep Math-Verify's ANTLR dependencies out of verl's legacy reward imports."""
import json
from pathlib import Path
import select
import subprocess
import sys
import threading

_process=None
_lock=threading.Lock()

def compute_score(data_source,solution_str,solution_str_with_special_tokens,ground_truth,extra_info=None):
    global _process
    with _lock:
        if _process is None:
            _process=subprocess.Popen([sys.executable,str(Path(__file__).with_name('score.py')),'--worker'],
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
        if _process.poll() is not None:
            raise RuntimeError(f'Isolated Math-Verify worker exited: {_process.returncode}')
        _process.stdin.write(json.dumps(dict(output=solution_str_with_special_tokens,gold=str(ground_truth)))+'\n')
        _process.stdin.flush()
        if not select.select([_process.stdout],[],[],30)[0]:
            _process.kill()
            raise TimeoutError('Isolated scorer did not return within 30 seconds')
        line=_process.stdout.readline()
        if not line:raise RuntimeError('Isolated scorer closed its output')
        value=json.loads(line)
    return dict(score=float(value['correct']),acc=float(value['correct']),valid_answer=float(value['valid']),
                scorer_error=float(value['error'] is not None),sample_index=int((extra_info or {}).get('index',-1)))
