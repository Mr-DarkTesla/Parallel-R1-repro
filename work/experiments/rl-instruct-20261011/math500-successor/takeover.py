from pathlib import Path
import json,os,time,signal,subprocess,hashlib,sys
R=Path.cwd();B=R/'work/experiments/rl-instruct-20261011/math500-successor';old=R/'work/experiments/rl-instruct-20261011/math500-sparse'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(x):
 p=B/'handoff-status.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(x,pid=os.getpid(),updated=time.time()),indent=2)+'\n');t.replace(p)
fd=os.open(B/'handoff.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
assert all(sha(k)==v for k,v in read(B/'seal.json')['sha256'].items())
required=['001-fullSFT-baseline','R1-checkpoint-0032','R2-checkpoint-0032']
while True:
 s=read(old/'status.json');ready=all((old/'results'/f'{j}.json').exists() and read(old/'results'/f'{j}.json')['passed'] for j in required)
 if ready and s['state'] in ['waiting_standalone_checkpoints','completed']:
  pid=s['pid'];proc=Path('/proc')/str(pid)
  if proc.exists():
   assert str(old/'controller.py') in (proc/'cmdline').read_bytes().decode().replace('\x00',' ')
   if subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():time.sleep(5);continue
   os.kill(pid,signal.SIGSTOP)
   # Freeze only the idle queue owner, then recheck no worker raced into a job.
   if read(old/'status.json')['state'] not in ['waiting_standalone_checkpoints','completed'] or subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():os.kill(pid,signal.SIGCONT);time.sleep(5);continue
   os.kill(pid,signal.SIGTERM);os.kill(pid,signal.SIGCONT)
  write(dict(state='handoff_released',original_controller_pid=pid,original_source_preserved=True,active_workers_killed=False))
  log=(B/'controller.log').open('a');child=subprocess.Popen([sys.executable,str(B/'controller.py')],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);write(dict(state='successor_running',successor_pid=child.pid,original_controller_pid=pid));break
 write(dict(state='waiting_first_three_terminal_and_idle_original',original_state=s['state'],first_three_ready=ready));time.sleep(30)
