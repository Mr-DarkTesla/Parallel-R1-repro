from pathlib import Path
import json,hashlib,datetime
P=Path.cwd();D=P/'work/experiments/instruct-token-warmup-20261010';C=P/'work/experiments/format-loss-20261010';F=P/'work/experiments/format-diagnosis-20261010';N=P/'work/experiments/night-20261010'
s=(D/'system.txt').read_text()
lead='''Organize the reasoning itself into useful independent calculations. Start inside <think> with a short decomposition and a multiline Plan:, before doing the complete calculation. Execute the planned calculations using <Parallel>N and its paths while still inside think. Do not solve the whole problem sequentially and then restate the work as a plan in the final answer. Keep the final answer outside think. If only one meaningful calculation exists, reason sequentially; never make duplicate or empty branches just to increase the count.

Here is a complete example of the required placement and exact syntax. The example is separate from the actual user problem and its numbers must not be reused:
Problem: A shop has 3 packs containing 5 red pens each and 4 packs containing 3 blue pens each. How many pens are there in total?
Assistant response:
<think>
The red and blue counts can be computed independently, then added.
Plan:
1: Calculate the number of red pens.
2: Calculate the number of blue pens.
<Parallel>2
<Path>1
Red pens = 3 * 5 = 15.
</Path>
<Path>2
Blue pens = 4 * 3 = 12.
</Path>
</Parallel>
<Summary>
The paths give 15 red and 12 blue pens. Total = 15 + 12 = 27.
</Summary>
</think>
Final Answer: \\boxed{27}

Apply this placement to the actual user problem, with its own plan, useful calculations and answer. Never include a parallel block or a Plan after </think>.

'''
prompt=F/'parallel-inside-think-example-system.txt';prompt.write_text(lead+s)
name='weighted-format-fewshot-128';w=N/'cloud-continued/tmp2';q=dict(argv=['bash',str(C/'evaluations/run_eval.sh'),'--model',str(C/'runs/production/final'),'--mode','structured','--name',name,'--suite','128','--system-file',str(prompt)],cwd=str(P),timeout_seconds=21600,wait_for=[str(w/'results/110-original-instruct-thinking-hf-128.json')],scope='Prompt-only diagnostic ablation: same weighted checkpoint, constrained decoder, budgets, scorer, 128questions. One synthetic worked example and early Plan instruction; no forced Plan or fork. Original98/128 baseline unchanged.',prompt_sha256=hashlib.sha256(prompt.read_bytes()).hexdigest())
path=w/'queue/120-weighted-format-fewshot-128.json'
with path.open('x') as f:json.dump(q,f,indent=2)
(F/'prompt-ablation-queued.json').write_text(json.dumps(q,indent=2)+'\n')
print('QUEUED',name,'on existingtmp2; baseline unchanged; no forced fork')
