"""MathVerify correctness via a persistent isolated CPU oracle process."""
import atexit, json, os, re, select, subprocess, sys, threading
from pathlib import Path
from verl.utils.reward_score.counted_parallel import check_format

_lock=threading.Lock()
_worker=None
_owner=None


def close():
    global _worker
    if _worker is not None:
        _worker.terminate()
        try: _worker.wait(timeout=2)
        except subprocess.TimeoutExpired: _worker.kill();_worker.wait()
        _worker.stdin.close()
        _worker.stdout.close()
        _worker=None
atexit.register(close)


def grade(output,gold):
    global _worker,_owner
    with _lock:
        if _worker is None or _worker.poll() is not None or _owner != os.getpid():
            env=dict(os.environ,CUDA_VISIBLE_DEVICES="")
            # Never inherit RL imports into the symbolic parser process.
            env.pop("PYTHONPATH",None)
            _worker=subprocess.Popen([sys.executable,"-u",str(Path(__file__).with_name("night_oracle.py"))],
                                     stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1,env=env)
            _owner=os.getpid()
        _worker.stdin.write(json.dumps(dict(output=output,gold=gold))+"\n");_worker.stdin.flush()
        if not select.select([_worker.stdout],[],[],30)[0]:
            close();raise TimeoutError("MathVerify CPU oracle timed out")
        line=_worker.stdout.readline()
        if not line:
            close();raise RuntimeError("MathVerify CPU oracle exited")
        result=json.loads(line)
        if "error" in result: raise RuntimeError("MathVerify scoring failed: "+result["error"])
        return result


def format_flags(text):
    errors,widths=check_format(text)
    parallel_valid=not errors
    think_valid=text.count("<think>")==1 and text.count("</think>")==1 and text.find("<think>")<text.find("</think>")
    strict=False
    if think_valid:
        opening=text.index("<think>")+len("<think>");closing=text.index("</think>")
        inside=all(opening<=m.start()<closing for m in re.finditer(r"</?(?:Parallel|Path|Summary)>",text))
        final_pattern=r"(?i)(?:\*\*)?Final\s+Answer(?:\*\*)?\s*:"
        final_outside=bool(re.search(final_pattern,text[closing+len("</think>"):]))
        final_in_path=any(re.search(final_pattern,m.group()) for m in re.finditer(r"<Path>.*?</Path>",text,re.DOTALL))
        strict=parallel_valid and inside and final_outside and not final_in_path
    return dict(format=float(strict),parallel_format_valid=float(parallel_valid),think_valid=float(think_valid),
                format_schema_version=2,max_width=max(widths,default=0))


def compute_score(data_source,solution_str,solution_str_with_special_tokens,ground_truth,extra_info=None,**kwargs):
    result=grade(solution_str_with_special_tokens,str(ground_truth))
    correct=result["correct"]
    text=solution_str_with_special_tokens;flags=format_flags(text)
    return dict(score=float(correct),acc=float(correct),pred=result["pred"],valid_answer=float(result["valid_answer"]),
                historical_acc=float(result["historical_correct"]),accuracy_schema_version=result["accuracy_schema_version"],
                correct_and_valid=float(correct and flags["format"]),
                correct_and_parallel_valid=float(correct and flags["parallel_format_valid"]),
                forks=text.count("<Parallel>"),**flags)
