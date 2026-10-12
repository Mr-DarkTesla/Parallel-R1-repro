import json, os, pathlib, time, subprocess
R=pathlib.Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1')
B=R/'work/experiments/rl-instruct-20261011/direct-full500'
candidates=[p for run in [B/'runs/strong_width', B/'r1-repair/run'] for p in sorted(run.glob('checkpoint-*'))]
refs={str(p.relative_to(R)):[] for p in candidates}
texts=0
for base in [R/'work',R/'exps',R/'docs',R/'scripts']:
 for directory, dirs, files in os.walk(base,followlinks=False):
  dirs[:]=[d for d in dirs if d not in {'__pycache__','.git','cache','teacher-cache','teacher-runtime'} and not d.startswith('checkpoint-')]
  for name in files:
   f=pathlib.Path(directory)/name
   if f.suffix not in {'.json','.jsonl','.py','.sh','.md','.yaml','.yml','.txt'} or f.is_symlink(): continue
   try:
    if f.stat().st_size>2_000_000: continue
    text=f.read_text(); texts+=1
   except (OSError,UnicodeError): continue
   for key in refs:
    # Full or project-relative references. Parent run references alone are tracked separately below.
    if key in text or str(R/key) in text:
     refs[key].append(dict(file=str(f.relative_to(R)),lines=[i+1 for i,l in enumerate(text.splitlines()) if key in l][:12]))
rows=[]
for p in candidates:
 files=[];symlinks=[];mounts=[]
 for f in p.rglob('*'):
  if f.is_symlink(): symlinks.append(str(f))
  elif f.is_file():
   s=f.stat();files.append(dict(path=str(f.relative_to(p)),bytes=s.st_size,allocated=s.st_blocks*512,dev=s.st_dev,inode=s.st_ino,nlink=s.st_nlink))
 key=str(p.relative_to(R))
 rows.append(dict(path=key,references=refs[key],files=files,symlinks=symlinks,logical_bytes=sum(x['bytes'] for x in files),allocated_unique_link_bytes=sum(x['allocated'] for x in files if x['nlink']==1),complete=json.loads((p/'complete.json').read_text())))
report=dict(timestamp=time.time(),scanned_small_text_files=texts,candidates=rows,active_status={str(run.relative_to(R)):json.loads((run/'status.json').read_text()) for run in [B/'runs/strong_width',B/'r1-repair/run']},findmnt=subprocess.run(['findmnt','-T',str(B),'-J'],capture_output=True,text=True).stdout,df=subprocess.run(['df','-B1',str(R)],capture_output=True,text=True).stdout)
out=R/'work/experiments/checkpoint-retention-20261011/reports';out.mkdir(parents=True,exist_ok=True)
(out/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(scanned_small_text_files=texts,candidates=[{k:v for k,v in x.items() if k not in ['files']} for x in rows]),indent=2))
