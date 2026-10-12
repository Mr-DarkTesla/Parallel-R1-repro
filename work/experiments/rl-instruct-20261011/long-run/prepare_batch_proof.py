"""Stage isolated true32-prompt two-step proof configs; never launches a worker."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--stage-config',required=True);p.add_argument('--predecessor-result',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;base=here.parent
cfg=json.loads(Path(a.stage_config).read_text());cfg.update(smoke=True,group=4,prompts_per_rank=4,lane='tmp2',steps=1,checkpoint_steps=[1],checkpoint_every=1,output=str(here/'batch-proof/step1'),resume=None,global_batch=dict(prompts_per_step=32,rollouts_per_prompt=4,responses_per_step=128),engineering_only=True,curriculum_selection=False)
# Engineering probes retain varied reward groups; clean curriculum is independently sealed later.
cfg['train']=str(base/'runner/technical-probes.jsonl');cfg['val']=cfg['train'];cfg['val_count']=16
cfg['replay']=str(here/'runner/structured_replay.py');cfg['batch_decoder']=str(here/'runner/microbatch_decoder.py')
cfg.update(dataset='engineering_probes_only',validation_label='engineering_probes16_not_selection',selection_allowed=False,curriculum_revision=None,curriculum='engineering probes16 repeated across32 prompt slots; not admitted training curriculum',validation_protocol='FP32 engineering probes16 only, not cleanval32 and not selection',unique_prompt_ids=16,prompt_slots=32,probe_repetition_disclosed=True)
out=here/'batch-proof-configs';out.mkdir(exist_ok=True)
for name in ['step1','resume-step2']:
 if name=='resume-step2':cfg.update(steps=2,resume=str(here/'batch-proof/step1/checkpoint-0001'),output=str(here/'batch-proof/resume-step2'),checkpoint_steps=[2])
 (out/(name+'.json')).write_text(json.dumps(cfg,indent=2)+'\n')
files=[x for x in (here/'runner').rglob('*.py') if '__pycache__' not in str(x)]+list(out.glob('*.json'))+[Path(__file__),here/'proof_accumulation.py',here/'launch_batch_proof.py',here/'root_batch_gate.py',here/'batch-proof-wrapper.sh',Path(cfg['train']),Path(cfg['val']),base/'reward.py',Path(cfg['system']),Path(cfg['scorer'])]
seal=dict(state='staged_not_launched',lane='tmp2',predecessor_result=a.predecessor_result,global_prompts=32,rollouts_per_prompt=4,global_responses=128,model=cfg['model'],sha256={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},full_sft_export_audit=str(base.parent/'instruct-full-20261011/epoch1-export-proof.json'),requires_root_receipt=True,requires_eight_gpu_empty=True,requires_fresh_independent_source_review=True)
(here/'batch-proof-source-seal.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal))
