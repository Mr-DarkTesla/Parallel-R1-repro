from pathlib import Path
import os,json,hashlib,datetime as dt
D=Path(__file__).resolve().parent
os.environ.update(HF_HOME=str(D/'cache'),HF_HUB_CACHE=str(D/'cache/hub'),XDG_CACHE_HOME=str(D/'cache'),TMPDIR=str(D/'tmp'),HF_HUB_DISABLE_XET='1',PYTHONDONTWRITEBYTECODE='1')
for k in ['HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE']:os.environ.pop(k,None)
(D/'tmp').mkdir(exist_ok=True)
from huggingface_hub import HfApi,snapshot_download
repo='Qwen/Qwen3-4B';info=HfApi().model_info(repo);rev=info.sha
snapshot_download(repo,revision=rev,local_dir=D/'model',cache_dir=D/'cache/hub',allow_patterns=['*.json','*.safetensors','*.jinja','*.txt'],max_workers=4)
from transformers import AutoTokenizer
model=D/'model';tok=AutoTokenizer.from_pretrained(model,local_files_only=True)
assert (model/'model.safetensors.index.json').exists() or (model/'model.safetensors').exists()
q=json.loads((D.parent/'rl-eval/questions-24.jsonl').read_text().splitlines()[0])
ids=tok.apply_chat_template([{'role':'system','content':'Solve carefully.'},{'role':'user','content':q['problem']}],tokenize=True,add_generation_prompt=True,enable_thinking=True)
assert tok.decode(ids[-5:]).endswith('<|im_start|>assistant\n')
ids += tok.encode('<think>\n',add_special_tokens=False)
assert tok.decode(ids[-2:])=='<think>\n'
proof={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'repo':repo,'revision':rev,'original_weights_tokenizer':True,'added_tokens':False,'enable_thinking':True,'force_initial_native_think_prefix':True,'template_suffix':tok.decode(ids[-5:]),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in model.iterdir() if p.is_file()}}
(D/'model-proof.json').write_text(json.dumps(proof,indent=2)+'\n');(D/'READY').write_text('ready\n');print(json.dumps({k:v for k,v in proof.items() if k!='files'}))
