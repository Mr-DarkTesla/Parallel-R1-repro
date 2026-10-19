"""Verify immutable inputs, then restore to a NEW portable project directory."""
import argparse,hashlib,json,os,shutil,sys,tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
# Absolute project root of the original runs; location references under it are rewritten to --target.
HISTORICAL_ROOT=os.environ.get('PARALLEL_R1_HISTORICAL_ROOT','${PROJECT_ROOT}')
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--download-models',action='store_true');a=p.parse_args()
 lock=json.loads((HERE/'bundle.json').read_text());assert digest(a.bundle)==lock['sha256'],'Bundle SHA256 mismatch'
 target=a.target.resolve();assert not target.exists(),'Use a new directory; historical/live runs must not be overwritten'
 target.mkdir(parents=True)
 with tarfile.open(a.bundle) as t:t.extractall(target,filter='data')
 manifest=json.loads((target/'input-manifest.json').read_text())
 for rel,expected in manifest.items():
  path=target/rel;assert path.is_file() and path.stat().st_size==expected['bytes'] and digest(path)==expected['sha256'],rel
 # Verify original bytes first. Only location references are rewritten afterward.
 relocated=[]
 for rel,expected in manifest.items():
  path=target/rel
  if expected['kind']!='data' and path.suffix in {'.py','.json','.yaml','.txt','.sh','.jinja'}:
   raw=path.read_text();new=raw.replace(HISTORICAL_ROOT,str(target))
   if raw!=new:path.write_text(new);relocated.append(rel)
 # Archived results are evidence, not an existing training run. Preserve them elsewhere.
 for rel in ['work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production','work/experiments/instruct-full-20261011/runs/epoch1']:
  source=target/rel
  if source.exists():
   evidence=target/'historical-results'/rel;evidence.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(source),str(evidence))
 (target/'verl').mkdir(exist_ok=True);(target/'README.md').write_text('Frozen 4B reproduction workspace\n')
 # Legacy shell entrypoints use this conventional interpreter location.
 (target/'.venv').symlink_to(Path(sys.prefix),target_is_directory=True)
 if a.download_models:
  from huggingface_hub import snapshot_download
  native=target/'work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model'
  snapshot_download('Qwen/Qwen3-4B',revision='1cfa9a7208912126459214e8b04321603b3df60c',local_dir=native)
  sft=json.loads((HERE/'sft-remote.json').read_text());destination=target/'work/experiments/instruct-full-20261011/runs/epoch1/final'
  snapshot_download(sft['repo'],revision=sft['revision'],local_dir=destination)
  for weight in sft['weights']:assert digest(destination/weight['name'])==weight['sha256'],weight['name']
 (target/'restoration-receipt.json').write_text(json.dumps(dict(passed=True,bundle_sha256=lock['sha256'],verified_original_files=len(manifest),relocated_files=relocated,models_downloaded=a.download_models,new_GPU_run_performed=False),indent=2)+'\n')
 print(json.dumps(dict(passed=True,target=str(target),verified_files=len(manifest),models_downloaded=a.download_models)))
if __name__=='__main__':main()
