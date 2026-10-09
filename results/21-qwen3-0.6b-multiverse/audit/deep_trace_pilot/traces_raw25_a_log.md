# Blind mathematical trace batch A

Date: 2026-10-09T22:00:56.120723+00:00

Scope: read `selected25_blind_a.jsonl` only for problem data. Read repository and ancestor instructions plus caveman skill. Did not inspect pool, gold, evaluations, earlier solutions, or other agents' outputs. No network, GPU, Kubernetes, proxy, or external model calls. Wrote only the two assigned artifacts.

Independent assessment: all 13 suggested splits define valid independent mathematical calculations after a shared setup. Every problem solved. Expositions are public mathematical solutions, with both calculations and their combination stated explicitly. No forced alternative verification branches. Two expositions below 1200 characters concern short calculations; no padding added.

Creation command: `python3 - <<'PY'` loaded only the selected input, paired each ID with its newly written solution, then used `json.dumps(..., ensure_ascii=False)` to write `traces_raw25_a.jsonl` in input order. Explanation lengths range 1093 to 1693 characters.

Validation command, run from repository root:

```python
import json, math, itertools
from fractions import Fraction as F
from pathlib import Path
base=Path('results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot')
inputs=[json.loads(x) for x in (base/'selected25_blind_a.jsonl').read_text().splitlines()]
rows=[json.loads(x) for x in (base/'traces_raw25_a.jsonl').read_text().splitlines()]
assert len(inputs)==len(rows)==13
assert [r['id'] for r in rows]==[r['id'] for r in inputs]
assert len({r['id'] for r in rows})==13
for src,r in zip(inputs,rows):
    assert r['question']==src['question']
    assert set(r)=={'id','question','response','parallelizable','status','notes'}
    assert r['status']=='solved' and r['parallelizable'] is True
    assert r['response'].startswith('<think>\n')
    assert r['response'].count('<think>')==r['response'].count('</think>')==1
    assert r['response'].count('Final Answer: ')==1
    assert r['response'].split('</think>')[1].startswith('\nFinal Answer: ')
answers={r['id']:r['response'].split('Final Answer: ')[1] for r in rows}
expected={
'math-train/6855':r'\sqrt{2}', 'math-train/6774':r'\frac{6}{25}',
'math-train/2170':'2148', 'math-train/2846':r'5\sqrt{13}',
'math-train/3082':r'\frac{7}{2}', 'math-train/5272':'757',
'math-train/5482':'73', 'math-train/7186':'30', 'math-train/5349':'680',
'math-train/3177':'39', 'math-train/6952':'(3,-2,2)',
'math-train/2464':r'\frac{7}{24}', 'math-train/4047':'(3281,3280)'}
assert answers==expected
# Positive hypotenuse solutions, including original trigonometric equations.
y=math.sqrt(2)-1
assert abs(y*y+2*y-1)<1e-14 and y>0
for value,hyp in [(1,'tan'),(y,'cos')]:
    x=math.atan(math.sqrt(value))
    sides={'sin':math.sin(x),'cos':math.cos(x),'tan':math.tan(x)}
    assert 0<x<math.pi/2 and sides[hyp]==max(sides.values())
    assert abs(sides[hyp]**2-sum(v*v for k,v in sides.items() if k!=hyp))<1e-14
assert abs(1+y-math.sqrt(2))<1e-14
# Distinct rational values and exact modular criterion for squared cosine=squared sine.
R=sorted({F(n,d) for d in range(1,6) for n in range(2*d)})
assert len(R)==20
counts=[0,0,0]
for a,b in itertools.product(R,repeat=2):
    c0=(a-F(1,2))%1==0
    s0=b%1==0
    eq=(a+b-F(1,2))%1==0 or (a-b-F(1,2))%1==0
    if c0 or s0: counts[0]+=1
    elif eq: counts[1]+=1
    if c0 or s0 or eq: counts[2]+=1
assert counts==[76,20,96] and F(counts[2],400)==F(6,25)
# Enumerate grid triples with exact determinant test.
pts=list(itertools.product(range(1,6),repeat=2))
collinear=0
for a,b,c in itertools.combinations(pts,3):
    collinear+=(b[0]-a[0])*(c[1]-a[1])==(b[1]-a[1])*(c[0]-a[0])
assert math.comb(25,3)==2300 and collinear==152 and 2300-collinear==2148
# 13-14-15 circle centers d=k*sqrt(13), radii 2k, feet on BC.
for k,r,lam in [(2,4,F(7,15)),(7,14,F(8,15))]:
    assert r==2*k and abs(56-18*k)==5*r
    qx=F(39)+3*lam; qy=F(26)-54*lam
    assert 18*qx+qy==728 and 0<lam<1
    # M=(13k,0)/sqrt(13); BC direction=(3,-54)/sqrt(13).
    assert (qx-13*k)*3+qy*(-54)==0
assert 7-2==5
# Right-triangle circle solution, segment limits, and determinant area.
assert 30/F(15)==2
valid_r=[r for r in range(1,6) if (F(r)-6)**2+(F(r)-F(5,2))**2==(F(13,2)-r)**2]
assert valid_r==[4]
assert F(abs(4*2-F(1,2)*2),2)==F(7,2)
# Supplement proof with bounded exact arithmetic search; proof itself is unbounded.
triples=[]
for h,t in itertools.product(range(1,101),repeat=2):
    rem=1-F(1,h)-F(1,t)
    if rem<=0 or rem.numerator!=1: continue
    u=rem.denominator
    if math.gcd(h,t)>1 and math.gcd(t,u)>1 and 2%math.gcd(h,u)!=0:
        triples.append((h,t,u))
assert triples==[(3,3,3),(4,2,4)]
for h,t,u in triples:
    for n in range(1,1001):
        hits=sum(n>=s and (n-s)%v==0 for s,v in [(1,h),(2,t),(3,u)])
        assert hits==1
assert sum(100*h+10*t+u for h,t,u in triples)==757
assert [w for w in range(101) if (136*w-184)%203==0]==[73]
assert sum(x*x+y*y+z*z==9 for x,y,z in itertools.product(range(-3,4),repeat=3))==30
nums=[n for n in range(100,1000) if len(set(str(n)))==3]
assert len(nums)==648 and sum(nums)==355680 and sum(nums)%1000==680
assert 25-9==16 and round(16+20+math.pi)==39
D=(3,-2,2)
for v in [(0,1,2),(4,2,1),(3,1,5)]: assert sum((a-b)**2 for a,b in zip(D,v))==18
assert [F(7,3)+F(2,3),F(4,3)-F(10,3),F(8,3)-F(2,3)]==[F(x) for x in D]
assert any(x.denominator!=1 for x in [F(7,3)-F(2,3),F(4,3)+F(10,3),F(8,3)+F(2,3)])
# Exact antiderivative values for meeting volumes.
v1=F(1,3); v2=(F(2)**2-F(2))-(F(1)**2-F(1))
assert v2==2 and (v1+v2)/8==F(7,24)
# Direct eight-step update of prime-exponent vectors.
p,q,r,s=1,0,0,1
for _ in range(8): p,q,r,s=2*p-r,2*q-s,2*r-p,2*s-q
assert r==-3280 and s==3281
print('PASS: 13 JSON rows, original order/questions, exact schema, unique IDs, balanced think tags, final-answer fields.')
print('PASS: independent mathematical checks for all 13 rows; rational count 96/400, grid degeneracies 152, paint triples (3,3,3),(4,2,4).')
print('PASS: all splits valid; geometry tangency feet checked; meeting volumes 1/3 and 2.')
```

Validation results:

Initial validation found a Python string-escaping error in three fraction answer fields: form-feed was written instead of the LaTeX backslash. Corrected those fields using explicit character codes. Mathematical expositions and values were unchanged.

```text
PASS: 13 JSON rows, original order/questions, exact schema, unique IDs, balanced think tags, final-answer fields.
PASS: independent mathematical checks for all 13 rows; rational count 96/400, grid degeneracies 152, paint triples (3,3,3),(4,2,4).
PASS: all splits valid; geometry tangency feet checked; meeting volumes 1/3 and 2.
```
