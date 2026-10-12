from pathlib import Path
import json,shutil,hashlib,torch
from huggingface_hub import snapshot_download,HfApi
from transformers import AutoTokenizer,AutoModelForCausalLM
R=Path(__file__).resolve().parent; torch.set_num_threads(4)
revision=HfApi().model_info('Qwen/Qwen3-0.6B').sha
cached=Path('${USER_HOME}/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots')/revision
raw=R/'raw';raw.mkdir(exist_ok=True)
if cached.exists():
 for p in cached.iterdir():
  if p.is_file():shutil.copyfile(p,raw/p.name)
snapshot_download('Qwen/Qwen3-0.6B',revision=revision,local_dir=raw,cache_dir=R/'cache',allow_patterns=['*.json','*.safetensors','*.txt','*.jinja'])
tok=AutoTokenizer.from_pretrained(raw,local_files_only=True);model=AutoModelForCausalLM.from_pretrained(raw,local_files_only=True,torch_dtype=torch.bfloat16)
old=model.get_input_embeddings().weight.detach().clone();before_template=tok.chat_template;tokens=['<Path>','</Path>','<Parallel>','</Parallel>','<Summary>','</Summary>']; n=tok.add_special_tokens({'additional_special_tokens':tokens},replace_additional_special_tokens=False)
assert n==6;model.resize_token_embeddings(max(len(tok),old.shape[0]),mean_resizing=False); torch.manual_seed(1)
with torch.no_grad():
 for emb in [model.get_input_embeddings(),model.get_output_embeddings()]:
  if emb is None:continue
  for t in tokens:emb.weight[tok.convert_tokens_to_ids(t)].normal_(mean=0,std=model.config.initializer_range)
keep=torch.ones(old.shape[0],dtype=torch.bool);keep[[tok.convert_tokens_to_ids(t) for t in tokens]]=False
assert torch.equal(model.get_input_embeddings().weight[:old.shape[0]][keep],old[keep])
assert tok.chat_template==before_template
out=R/'model';model.save_pretrained(out);tok.save_pretrained(out)
report={'model':'Qwen/Qwen3-0.6B','revision':revision,'source':'official HF','six_added_tokens':{t:tok.convert_tokens_to_ids(t) for t in tokens},'seed':1,'std':model.config.initializer_range,'all_pretrained_rows_except_six_protocol_rows_exactly_preserved':True,'native_chat_template_preserved':True,'template_sha256':hashlib.sha256(before_template.encode()).hexdigest()}
(R/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
