import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import pandas as pd
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
TRAIN = PROJECT/'exps/sft-unseen-three-datasets-20261008'
SOURCE = PROJECT/'exps/branch-diversity-20261006/math500-source.jsonl'
OLD = PROJECT/'exps/qwen3-06b-math500-author-32k-20261007'

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    if not (ROOT/'scorer-deps').exists():
        shutil.copytree(OLD/'scorer-deps',ROOT/'scorer-deps')
    from score import check, parsed
    assert importlib.metadata.version('math-verify') == '0.8.0'
    data = [json.loads(line) for line in SOURCE.read_text().splitlines()]
    assert len(data)==500 and len({r['unique_id'] for r in data})==500
    system = ("Solve the problem step by step. Use <Parallel> only for genuinely independent required subcomputations "
              "that can be carried out simultaneously from the information already known at that point; write one "
              "<Path> per independent subcomputation, and follow the block with a short <Summary> of the branch "
              "results. Otherwise reason sequentially. End with 'Final Answer: <answer>'.")
    questions, records = [], []
    for i,r in enumerate(data):
        assert parsed(str(r['answer'])), r['unique_id']
        questions.append(dict(index=i,id=r['unique_id'],problem=r['problem'],answer=str(r['answer']),subject=r['subject'],level=r['level']))
        records.append(dict(data_source='APO_MATH300',prompt=[dict(role='system',content=system),dict(role='user',content=r['problem'])],
            ability='MATH',reward_model=dict(ground_truth=str(r['answer']),style='rule'),
            extra_info=dict(index=i,unique_id=r['unique_id'],subject=r['subject'],level=r['level'])))
    (ROOT/'questions.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in questions))
    pd.DataFrame(records).to_parquet(ROOT/'math500.parquet',index=False)
    models = []
    for name,rel,epoch in [('gsm_infinite_ep5','01_gsm_infinite/final',5),('sft_messages_ep5','02_sft_messages/final',5),('mixed_ep1','03_mixed/checkpoints/global_step_35',1)]:
        path=TRAIN/'runs'/rel
        tok=AutoTokenizer.from_pretrained(path,local_files_only=True)
        lengths=[len(tok.apply_chat_template(r['prompt'],tokenize=True,add_generation_prompt=True)) for r in records]
        assert max(lengths)<=2048
        assert all(len(tok.encode(t,add_special_tokens=False))==1 for t in ('<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>'))
        models.append(dict(name=name,path=str(path),epoch=epoch,weights_sha256=sha(path/'model.safetensors'),max_prompt_tokens=max(lengths)))
    # Snapshot-only fixes: respect the requested sampling parameters at every call.
    patches = []
    for rel,old,new in [
        ('verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py','"temperature": 1.0, "max_tokens": max_len','"temperature": sampling_params["temperature"], "max_tokens": max_len'),
        ('verl/parallel_thinking_generation_v3/agent_loop.py','            top_p=config.top_p,','            top_p=config.top_p,\n            top_k=config.top_k,'),
        ('verl/parallel_thinking_generation_v3/agent_loop.py','            sampling_params["top_p"] = config.val_kwargs.top_p','            sampling_params["top_k"] = config.val_kwargs.top_k\n            sampling_params["top_p"] = config.val_kwargs.top_p'),
        ('verl/parallel_thinking_generation_v3/repro_trace.py',"generated_tokens=len(ids), generated_ids=list(ids),","generated_tokens=len(ids), generated_ids=list(ids), sampling_params=dict(sampling_params),")]:
        p=ROOT/'code'/rel
        s=p.read_text()
        assert s.count(old)==1,(rel,old)
        before=sha(p)
        p.write_text(s.replace(old,new))
        patches.append(dict(file=rel,before=before,after=sha(p),old=old,new=new))
    protocol=dict(dataset='HuggingFaceH4/MATH-500',source_sha256=sha(SOURCE),dataset_sha256=sha(ROOT/'math500.parquet'),
        questions=500,samples_per_question=1,models=models,system_prompt=system,
        max_prompt_tokens=2048,max_response_tokens=30720,max_model_len=32768,
        temperature=0.6,top_p=0.95,top_k=20,repetition_penalty=1.0,engine_seed=42,
        branch_seed_policy='Runtime random seeds saved per call; asynchronous scheduling is not bitwise deterministic.',
        runtime='existing async Parallel-R1 v3 fork/join, snapshot sampling fixes only',
        fixed_num_paths=2,max_forks=0,max_forks_meaning='No fixed round cap; bounded by total response token budget',
        max_path_response_tokens=8192,gpus=list(range(8)),models_sequential=True,
        scorer='Math-Verify 0.8.0; reference-blind final answer extraction',scorer_tests=check(),reference_tests=500,
        limitations=['Width is fixed by runtime, not selected by model.','vLLM summary/main continuation does not apply Unseen custom positions/mask.',
                     'One stochastic sample per problem.','Tag validity includes manually inserted tags; raw generation calls are saved separately.'],
        snapshot_patches=patches,code_sha256={str(p.relative_to(ROOT/'code')):sha(p) for p in (ROOT/'code').rglob('*') if p.is_file() and '__pycache__' not in str(p)})
    (ROOT/'manifest.json').write_text(json.dumps(protocol,indent=2)+'\n')
    print(json.dumps({k:v for k,v in protocol.items() if k not in ('code_sha256','snapshot_patches')},indent=2))

if __name__=='__main__':main()
