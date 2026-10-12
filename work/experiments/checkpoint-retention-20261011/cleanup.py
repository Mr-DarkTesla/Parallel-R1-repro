import hashlib,json,os,pathlib,shutil,subprocess,time
R=pathlib.Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1');B=R/'work/experiments/rl-instruct-20261011/direct-full500';O=R/'work/experiments/checkpoint-retention-20261011/reports'
audit=json.loads((O/'audit.json').read_text());selected=[x for x in audit['candidates'] if x['complete']['step'] in [4,8,16]]
assert len(selected)==6
runs=[B/'runs/strong_width',B/'r1-repair/run']
def du():return {str(p.relative_to(R)):int(subprocess.check_output(['du','-s','-B1',str(p)]).split()[0]) for p in runs}
def df():return subprocess.check_output(['df','-B1',str(R)],text=True)
before=du();dfbefore=df();manifest=dict(state='prepared',before=before,df_before=dfbefore,dependency_audit=str(O/'audit.json'),scanned_small_text_files=audit['scanned_small_text_files'],preserved=['both checkpoint32 benchmark anchors','both checkpoint64 full Adam+RNG resume pins','future128/256/500 anchors','all initial/final models','all legacy technical smoke proofs','all validation scores/traces/logs'],deleted=[])
M=O/'deletion-manifest.json'
def write():
 t=M.with_suffix('.tmp');t.write_text(json.dumps(manifest,indent=2)+'\n');os.replace(t,M)
for x in selected:
 p=R/x['path'];assert p.resolve().is_relative_to(B.resolve()) and not p.is_symlink() and not x['references'] and not x['symlinks']
 assert json.loads((p/'complete.json').read_text())==x['complete']
 assert all((p.parent/f'checkpoint-{step:04}'/'complete.json').is_file() for step in [32,64])
 for f in x['files']:
  q=p/f['path'];s=q.stat();assert (s.st_ino,s.st_dev,s.st_nlink,s.st_size,s.st_blocks*512)==(f['inode'],f['dev'],f['nlink'],f['bytes'],f['allocated'])
  assert s.st_nlink==1 and not q.is_symlink() # no claimed hardlink savings
 # Refuse unexpected newly added files or nested mounts.
 assert {str(q.relative_to(p)) for q in p.rglob('*') if q.is_file()}=={f['path'] for f in x['files']}
 assert all(q.stat().st_dev==p.stat().st_dev for q in p.rglob('*'))
write()
for x in selected:
 p=R/x['path'];archive=O/'deleted-checkpoint-metadata'/p.parent.relative_to(R)/p.name;archive.mkdir(parents=True,exist_ok=False)
 saved=[]
 for q in p.rglob('*'):
  if q.is_file() and q.suffix in ['.json','.txt']:
   target=archive/q.relative_to(p);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,target);saved.append(dict(path=str(q.relative_to(p)),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),bytes=q.stat().st_size))
 row=dict(path=x['path'],reason='obsolete early checkpoint; no configuration/queue/plan/source-seal reference in audit; later32benchmark and64resumable complete; steps4/8/16 metrics+traces retained',logical_bytes=x['logical_bytes'],exclusively_linked_allocated_bytes=x['allocated_unique_link_bytes'],nlink=1,metadata_archive=str(archive.relative_to(R)),metadata_files=saved,state='deleting')
 manifest['deleted'].append(row);write();shutil.rmtree(p);row.update(state='deleted',removed_at=time.time());write()
manifest.update(state='completed',after=du(),df_after=df(),completed_at=time.time(),gross_exclusively_linked_allocated_bytes=sum(x['allocated_unique_link_bytes'] for x in selected))
manifest['targeted_run_allocated_bytes_reduction']=sum(manifest['before'].values())-sum(manifest['after'].values());manifest['retained_archive_allocated_bytes']=int(subprocess.check_output(['du','-s','-B1',str(O/'deleted-checkpoint-metadata')]).split()[0]);manifest['net_project_allocated_bytes_reduction_estimate']=manifest['targeted_run_allocated_bytes_reduction']-manifest['retained_archive_allocated_bytes'];write()
print(json.dumps({k:v for k,v in manifest.items() if k!='deleted'},indent=2))
