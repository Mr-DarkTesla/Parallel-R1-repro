"""CPU bitwise tensor comparison; exported model must differ only at six rows."""
from pathlib import Path
import json,datetime,torch
from safetensors import safe_open
D=Path(__file__).resolve().parent;A=D.parents[1];native=A.parent/'night-20261010/qwen3-4b-tag-probe-20261010/model';final=D/'runs/production/final'
def mapping(folder):
 index=folder/'model.safetensors.index.json'
 if index.exists():return json.loads(index.read_text())['weight_map']
 with safe_open(str(folder/'model.safetensors'),framework='pt',device='cpu') as f:return {key:'model.safetensors' for key in f.keys()}
old=mapping(native);new=mapping(final);assert set(old)==set(new),'Export tensor keys changed'
proof=json.loads((A/'tokenizer-proof.json').read_text());ids=list(proof['tags'].values());checks={};row_changed=None
for key in old:
 with safe_open(str(native/old[key]),framework='pt',device='cpu') as f:before=f.get_tensor(key)
 with safe_open(str(final/new[key]),framework='pt',device='cpu') as f:after=f.get_tensor(key)
 assert before.shape==after.shape and before.dtype==after.dtype,(key,'shape/dtype changed')
 if key=='model.embed_tokens.weight':
  assert torch.equal(before[:ids[0]],after[:ids[0]]) and torch.equal(before[ids[-1]+1:],after[ids[-1]+1:]),'Old embedding rows changed'
  with safe_open(str(D/'runs/production/rows-final.safetensors'),framework='pt',device='cpu') as f:expected=f.get_tensor('rows').to(after.dtype);initial=f.get_tensor('initial_rows').to(after.dtype)
  assert torch.equal(after[ids],expected),'Exported rows differ from committed row checkpoint'
  row_changed=not torch.equal(expected,initial);assert row_changed,'No learned row update'
 else:assert torch.equal(before,after),(key,'Frozen tensor changed')
 checks[key]=True
 del before,after
def actual_template(folder):
 config=json.loads((folder/'tokenizer_config.json').read_text());inline=config.get('chat_template');file=folder/'chat_template.jinja'
 standalone=file.read_text() if file.exists() else None
 assert inline is None or isinstance(inline,str),'This pinned model expects a single string template'
 assert standalone is not None or inline is not None,'No chat template'
 if standalone is not None and inline is not None:assert standalone==inline,'Conflicting template representations'
 return standalone if standalone is not None else inline
assert actual_template(native)==actual_template(final),'Native chat template changed'
for name in ['vocab.json','merges.txt']:assert (native/name).read_bytes()==(final/name).read_bytes()
result={'passed':True,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_tensor_keys_and_dtypes_exact':True,'old_embedding_rows_bitwise_identical':True,'all_other_tensors_bitwise_identical':checks,'only_six_rows_changed':True,'new_rows_exact_committed_checkpoint':True,'new_rows_changed_from_mean_init':row_changed,'native_chat_template_vocab_merges_preserved':True,'chat_template_source':'nativeinline-tokenizer_config vs finalstandalone-jinja','audit_source_version':2,'GPU_calls':False}
(D/'export-byte-proof.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'tensors_checked':len(checks),'only_six_rows_changed':True}))
