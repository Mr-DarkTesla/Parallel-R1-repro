import json
from pathlib import Path
root=Path(__file__).parent
rows=[json.loads(s) for s in (root/'input.jsonl').read_text().splitlines()]
solutions={
'816':('The denominator factors as (x-10)(x+3). Multiplying by that denominator gives 5x+2=A(x+3)+B(x-10).','Set x=10 to isolate A. Then 52=13A, so A=4.','Set x=-3 to isolate B. Then -13=-13B, so B=1.','The independently isolated coefficients give the required ordered pair.','(4,1)'),
'620':('Divide the equation by 9. It becomes x^2-2x+y^2+4y+44/9=0. Complete the two coordinate squares separately.','For the x terms, x^2-2x=(x-1)^2-1. Thus the horizontal center coordinate is 1.','For the y terms, y^2+4y=(y+2)^2-4. Thus the vertical center coordinate is -2.','Together the equation is (x-1)^2+(y+2)^2=1/9, identifying the center.','(1,-2)'),
'1985':('There are 2^6=64 equally likely gender sequences. More sons and more daughters are disjoint events.','More sons means 4, 5, or 6 sons. Their counts are C(6,4)=15, C(6,5)=6, and C(6,6)=1, giving 22 sequences.','More daughters means 4, 5, or 6 daughters. Choosing their positions gives C(6,4)+C(6,5)+C(6,6)=15+6+1=22 sequences.','Add the disjoint counts: the probability is (22+22)/64=44/64=11/16.','11/16'),
'3483':('Real coefficients require the conjugate root -2+i sqrt(5). For a monic quadratic, use the roots’ sum and product.','The sum of the two roots is (-2-i sqrt(5))+(-2+i sqrt(5))=-4. Therefore the coefficient of x is 4.','Their product is (-2)^2-(i sqrt(5))^2=4-(-5)=9. Therefore the constant coefficient is 9.','Combining the two coefficients gives the monic quadratic.','x^2+4x+9'),
'1877':('The 7 independent fair flips produce 2^7=128 equally likely sequences. Partition the requested event into exactly five heads and six or seven heads.','Exactly five heads has C(7,5)=7!/(5!2!)=21 sequences.','Exactly six heads has C(7,6)=7 sequences, and exactly seven heads has C(7,7)=1 sequence. This branch contributes 8 sequences.','The disjoint branches contribute 21+8=29 sequences out of 128.','29/128'),
'4424':('Count rabbit-ear wearers separately among women and men, then add the two groups.','There are 200*0.40=80 women. Rabbit-ear wearers among them number 80*0.80=64.','There are 200*(1-0.40)=120 men. Rabbit-ear wearers among them number 120*0.60=72.','The two groups give 64+72=136 people wearing rabbit ears.','136'),
'685':('Expand each side of the given equation independently before equating the resulting polynomials.','The left side is (w+13)^2=w^2+26w+169.','The right side is (3w+7)(2w+4)=6w^2+12w+14w+28=6w^2+26w+28.','Equating the expansions cancels 26w and gives 169-28=6w^2-w^2, so 5w^2=141. Thus w^2=141/5=28.2.','28.2'),
'1145':('Use separate eliminations on the original system 3x-5y=-11 and 7x+2y=-12 to determine each variable independently.','Multiply the first equation by 2 and the second by 5: 6x-10y=-22 and 35x+10y=-60. Adding gives 41x=-82, hence x=-2.','Multiply the first equation by 7 and the second by 3: 21x-35y=-77 and 21x+6y=-36. Subtracting the first from the second gives 41y=41, hence y=1.','Combine the independently computed coordinates.','(-2,1)'),
'2415':('Expected value is the sum of each face value multiplied by its probability. Separate face 6 from faces 1 through 5.','Face 6 contributes 6*(1/2)=3 to the expectation.','The other faces contribute (1+2+3+4+5)*(1/10)=15/10=1.5.','Adding the contributions gives 3+1.5=4.5.','4.5'),
'5755':('Let L be the shared square perimeter and circle circumference. Compute each area from L independently.','The square side is L/4. Its area is (L/4)^2=L^2/16.','The circle radius is L/(2*pi). Its area is pi*(L/(2*pi))^2=L^2/(4*pi).','The square-to-circle area ratio is (L^2/16)/(L^2/(4*pi))=pi/4.','pi/4'),
'2035':('With replacement, each draw independently has green probability 7/10 and purple probability 3/10. Count valid color arrangements and compute each arrangement’s probability separately.','Choose the three green positions among six draws. There are C(6,3)=6!/(3!3!)=20 valid arrangements.','Any specified arrangement of three greens and three purples has probability (7/10)^3*(3/10)^3=(343*27)/1000000=9261/1000000.','The arrangements are disjoint, giving 20*9261/1000000=0.18522. Rounded to the nearest thousandth, this is 0.185.','0.185'),
'164':('Compute the numerator and denominator independently using x=3/5 and y=7/9.','The numerator is 5x+9y=5*(3/5)+9*(7/9)=3+7=10.','The denominator is 45xy=45*(3/5)*(7/9)=45*(21/45)=21.','Divide the two computed values: 10/21 is already in lowest terms.','10/21'),
'2003':('There are 15 marbles, so each unordered three-marble subset is equally likely. Separate favorable monochromatic subsets from all possible subsets.','The favorable count is C(4,3)+C(5,3)+C(6,3)=4+10+20=34, corresponding to red, white, and blue subsets.','The total number of possible subsets is C(15,3)=15*14*13/(3*2*1)=455.','The requested probability is favorable count divided by total count, 34/455. Their greatest common divisor is 1.','34/455'),
'5816':('Jar A starts with 12 buttons and keeps (2/3)*12=8. Thus four buttons are transferred, equally split as two red and two blue. Compute each jar’s red probability independently.','Jar A retains 4-2=2 red buttons and 8-2=6 blue buttons. Its red probability is 2/(2+6)=1/4.','Jar B contains 2 red and 2 blue buttons. Its red probability is 2/(2+2)=1/2.','Selections from the separate jars are independent, so both-red probability is (1/4)*(1/2)=1/8.','1/8'),
'4353':('Let N=2000^6. The reciprocal-log identity 1/log_b(N)=log_N(b) converts each summand independently.','The first summand is 2/log_4(N)=2*log_N(4)=log_N(4^2)=log_N(16).','The second summand is 3/log_5(N)=3*log_N(5)=log_N(5^3)=log_N(125).','Add the logarithms: log_N(16)+log_N(125)=log_N(2000). Since N=2000^6, this equals 1/6.','1/6'),
'1179':('Rewrite the given equations as 5u+2v=-7 and 3u-4v=-25. Use independent eliminations for the two variables.','Double the first equation: 10u+4v=-14. Add the second equation to get 13u=-39, so u=-3.','Multiply the first equation by 3 and the second by 5: 15u+6v=-21 and 15u-20v=-125. Subtracting the second from the first gives 26v=104, so v=4.','Together these coordinates form the required ordered pair.','(-3,4)'),
'2353':('The 12 die faces are equally likely. Compute the contributions from one-digit and two-digit outcomes separately.','Faces 1 through 9 give nine one-digit outcomes. Their contribution to the expected digit count is 1*(9/12)=3/4.','Faces 10 through 12 give three two-digit outcomes. Their contribution is 2*(3/12)=1/2.','The expected digit count is 3/4+1/2=5/4=1.25.','1.25')
}
reasons={
'4324':'Single telescoping product; splitting numerator and denominator would create artificial arithmetic branches.',
'7041':'Single normal-distance computation; no second substantive independent quantity is needed.',
'3594':'Unknown quadratic coefficients are coupled through shared equations; straightforward coefficient solution is sequential.',
'2792':'Reflection and translation are elementary coordinate updates; neither offers substantial independent work.',
'669':'Degree-four cancellation determines c; degree-three verification depends on that result.',
'513':'Single linear equation after direct substitution; no substantive independent branches.',
'5661':'Single rational product; arbitrary factor grouping would not provide meaningful independent work.',
'1498':'Shared segment fraction immediately yields both coordinates; two coordinate substitutions are too slight.',
'7093':'Trigonometric identity reduction has no clear independent two-part decomposition with confidently verified solution.',
'5887':'Two one-step repeating-decimal conversions are too slight to count as substantive computations.',
'1784':'Independence of daily snow events is unstated; probability of at least one snowy day is not determined by marginals alone.',
'6827':'Quadrilateral ordering is not explicit; given A,B,C,D order crosses, while convex-hull interpretation differs. Reject ambiguity.',
'3278':'Corey’s gift depends directly on Mike’s stated gift; computation is short and sequential.',
'995':'Collinearity yields one determinant equation; no substantive independent branch structure.',
'970':'Cubing and solving one linear equation is sequential; no substantive independent branches.'
}
screen=[];traces=[]
for r in rows:
    k=r['id'].split('/')[-1]
    if k in solutions:
        setup,p1,p2,combine,answer=solutions[k]
        response=f'<think>\n{setup}\n\nPart 1:\n{p1}\n\nPart 2:\n{p2}\n\n{combine}\n</think>\nFinal Answer: {answer}'
        traces.append({**r,'response':response})
        screen.append({'id':r['id'],'verdict':'accept','reason':'Two independent computations from shared problem facts: '+p1.split('.')[0]+'; '+p2.split('.')[0]+'.'})
    else:
        screen.append({'id':r['id'],'verdict':'reject','reason':reasons[k]})
(root/'screen.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in screen))
(root/'traces.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in traces))
(root/'review.md').write_text('''# Blind reserve review, agent C

32 questions screened. 17 accepted, 15 rejected. Only input.jsonl read for question content. No gold or M1/M2 answers used.

Accepted solutions contain one common setup, Part 1, Part 2, combination inside think, and one Final Answer outside think. No Multiverse tags. Questions copied from parsed input strings without edits.

Strong examples: math-train/1145 and math-train/1179 independently eliminate each variable using the original equations. gsm8k-train/4424 separately counts women and men wearing rabbit ears. math-train/5755 computes square and circle areas independently from shared perimeter. math-train/4353 transforms the two logarithmic terms independently before combining them.

Other accepted decompositions include outcome groups, numerator versus denominator, binomial arrangement count versus fixed-sequence probability, and polynomial sum/product or left/right expansion. Their branches derive from original facts and require no result produced by the other branch.

Rejected uncertain math: math-train/1784 lacks independence, so daily marginals alone do not determine the union probability. math-train/6827 gives an ordering that crosses; interpreting the quadrilateral as a convex hull would require an additional convention. math-train/7093 has no confidently established two-part solution. Remaining rejections are sequential or too slight for substantive independent branches.

Verification: build.py generates artifacts from explicit independently solved text; JSON parsing, complete ID coverage, question-string equality, response structure and absence of Multiverse tags checked locally. No GPU, Kubernetes, proxy or git operations performed.
''')
assert len(screen)==32 and len(traces)==17
for t in traces:
    original=next(r for r in rows if r['id']==t['id'])
    assert t['question']==original['question']
    s=t['response']
    assert s.count('<think>')==s.count('</think>')==s.count('Part 1:')==s.count('Part 2:')==s.count('Final Answer:')==1
    assert s.index('Part 1:')<s.index('Part 2:')<s.index('</think>')<s.index('Final Answer:')
    assert 'Multiverse' not in s
print(f'Validated {len(screen)} screens, {len(traces)} traces.')
