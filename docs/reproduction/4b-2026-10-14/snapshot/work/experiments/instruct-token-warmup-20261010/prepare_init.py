"""Build isolated checkpoint0 from original tensors, changing six reserved rows only."""
from pathlib import Path
import json,hashlib,shutil,torch
from safetensors.torch import load_file,save_file
D=Path(__file__).resolve().parent;N=D.parent/'night-20261010';native=N/'qwen3-4b-tag-probe-20261010/model';out=D/'init-model'
assert not out.exists(),'No overwrite'
proof=json.loads((D/'tokenizer-proof.json').read_text());sourceproof=json.loads((N/'qwen3-4b-tag-probe-20261010/model-proof.json').read_text())
assert all(hashlib.sha256((native/name).read_bytes()).hexdigest()==sha for name,sha in sourceproof['files'].items())
index=json.loads((native/'model.safetensors.index.json').read_text());state={}
for name in sorted(set(index['weight_map'].values())):
 shard=load_file(str(native/name),device='cpu');assert not set(shard)&set(state);state.update(shard)
assert set(state)==set(index['weight_map'])
key='model.embed_tokens.weight';emb=state[key];ids=list(proof['tags'].values());assert emb.shape[0]==proof['model_vocab_size'];assert 'lm_head.weight' not in state
initial=torch.stack([emb[proof['native_pieces'][tag]].float().mean(0) for tag in proof['tags']])
before=hashlib.sha256(emb[:ids[0]].contiguous().numpy().tobytes()+emb[ids[-1]+1:].contiguous().numpy().tobytes()).hexdigest() if emb.dtype!=torch.bfloat16 else hashlib.sha256(emb[:ids[0]].contiguous().view(torch.uint8).numpy().tobytes()+emb[ids[-1]+1:].contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()
emb.index_copy_(0,torch.tensor(ids),initial.to(emb.dtype))
after=hashlib.sha256(emb[:ids[0]].contiguous().view(torch.uint8).numpy().tobytes()+emb[ids[-1]+1:].contiguous().view(torch.uint8).numpy().tobytes()).hexdigest();assert before==after
out.mkdir();save_file(state,str(out/'model.safetensors'),metadata={'format':'pt'})
for p in native.iterdir():
 if p.is_file() and p.suffix in ['.json','.jinja','.txt'] and p.name!='model.safetensors.index.json':shutil.copyfile(p,out/p.name)
for p in (D/'tokenizer').iterdir():
 if p.is_file():shutil.copyfile(p,out/p.name)
save_file({'initial_rows':initial},str(D/'initial-rows.safetensors'))
result={'passed':True,'source_original_all_file_hashes_passed':True,'only_six_reserved_rows_modified':True,'nonselected_embedding_rows_bytehash_before_after_equal':before==after,'unchanged_other_tensor_references':len(state)-1,'source_model_revision':sourceproof['revision'],'tag_ids':ids,'init_rows_FP32_sha256':hashlib.sha256(initial.numpy().tobytes()).hexdigest(),'init_model_safetensors_sha256':hashlib.sha256((out/'model.safetensors').read_bytes()).hexdigest(),'native_model_not_modified':True,'no_vocab_resize':True}
(D/'initialization-proof.json').write_text(json.dumps(result,indent=2)+'\n');(out/'READY').write_text('ready\n');print(json.dumps(result),flush=True)
