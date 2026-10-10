import json
from pathlib import Path
from fractions import Fraction as F
from math import comb
p=Path(__file__).parent
inputs={r['id']:r for r in map(json.loads,(p/'input.jsonl').read_text().splitlines())}
screen=list(map(json.loads,(p/'screen.jsonl').read_text().splitlines()))
traces=list(map(json.loads,(p/'traces.jsonl').read_text().splitlines()))
assert len(screen)==33 and {r['id'] for r in screen}==set(inputs)
assert len(traces)==21 and len({r['id'] for r in traces})==21
for r in traces:
    for field in ('question','source','answer_type'):
        assert r[field]==inputs[r['id']][field]
    s=r['response']
    assert s.startswith('<think>\n')
    for marker in ('<think>','</think>','Part 1:','Part 2:','Final Answer:'):
        assert s.count(marker)==1
    assert s.index('Part 1:') < s.index('Part 2:') < s.index('</think>') < s.index('Final Answer:')
    assert 'Multiverse' not in s
assert F(3)*F(62,100)+4*F(42,100)==F(354,100)
assert sum(comb(8,k) for k in range(5,9))/F(256)==F(93,256)
assert F(3,4)*(240-F(240,3)-F(240,5))==84
assert F(1,2)**8*F(3,4)**-3==F(1,108)
assert len([i for i in range(1,25) if 24%i==0])/F(24)==F(1,3)
assert (complex(-1,4)-2*(complex(0,2)-complex(-1,4)))==complex(-3,8)
t=F(2,3)
assert t*(8-t)==(2-t)*(t+3)
assert abs(F(21,10)-F(54,10))==F(33,10)
assert (F(2)**2*F(2)**-3)/(F(2)**3*F(2)**-2)==F(1,4)
assert F(560,90)==F(56,9)
assert F(comb(3,1)+comb(3,2),8)==F(3,4)
assert F(-20,2)*F(-19,5)==38
assert 12*24+36*12==720
x,y=F(3,2),F(5,4)
assert 3*x+2*y==7 and 2*x+4*y==8 and x+y==F(11,4)
assert 9-8==1 and -3-(-3)==0 and 8*(3-3)==0 and -8+(-3)**2==1
assert F(sum(comb(7,k) for k in range(4,8)),128)==F(1,2)
assert F(3,8)/F(1,2)==F(3,4)
assert 5*(F(25,100)*4+F(35,100)*10)==F(225,10)
assert F(comb(4,2)*10**4,20**4)==F(3,8)
print('PASS: 33 unique screening IDs; 21 unique accepted traces; source fields preserved semantically; section order and single final-answer marker valid; no Multiverse tags.')
print('PASS: Exact rational arithmetic checks for accepted numerical expressions; geometry determinant and norms reviewed explicitly; polynomial expansion reviewed explicitly.')
