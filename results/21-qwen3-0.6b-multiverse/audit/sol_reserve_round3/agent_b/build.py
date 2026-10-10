import json
from pathlib import Path
p=Path(__file__).parent
rows=[json.loads(s) for s in (p/'input.jsonl').read_text().splitlines()]
sol={
'667':('Split the absolute-value equation into its two signed cases; x must be nonzero.','For 12/x+3=2, subtracting 3 gives 12/x=-1. Thus x=-12.','For 12/x+3=-2, subtracting 3 gives 12/x=-5. Thus x=-12/5.','The two cases exhaust the equation. Their product is (-12)(-12/5)=144/5.','144/5'),
'60':('Since f has positive slope, its fourfold composition is increasing. Compute its values at both domain endpoints independently.','Starting at x=0, the four applications give -2, -8, -26, and -80. Therefore g(0)=-80.','Starting at x=2, the four applications give 4, 10, 28, and 82. Therefore g(2)=82.','An increasing continuous affine function takes every value between its endpoint values. Its range is [-80,82].','[-80,82]'),
'2010':('Use independent daily snow events, as intended by this probability model. Compute the no-snow probabilities for the two groups of days.','For the first three days, each no-snow probability is 2/3. No snow in this group has probability (2/3)^3=8/27.','For the next four days, each no-snow probability is 3/4. No snow in this group has probability (3/4)^4=81/256.','No snow all week has probability (8/27)(81/256)=3/32. Its complement, snow at least once, has probability 1-3/32=29/32.','29/32'),
'2026':('Use the explicitly specified five visits and independent daily outcomes. A successful pattern has four chocolate days and one regular day.','Choose the one regular day among five visits. There are binomial(5,1)=5 mutually exclusive patterns.','For any specified pattern, independence gives probability (2/3)^4(1/3)=16/243.','Summing the equal probabilities of the five patterns gives 5(16/243)=80/243.','80/243'),
'2388':('Treat the five answers as independent. Exactly two positives means two positive answers and three other answers.','The positive answers can occupy any two of five positions. The number of patterns is binomial(5,2)=5*4/2=10.','A specified such pattern has probability (2/5)^2(3/5)^3=(4/25)(27/125)=108/3125.','The ten disjoint patterns give total probability 10(108/3125)=216/625.','216/625'),
'2782':('A uniform point has probability equal to the relevant area divided by the whole area. Horizontal sections permit separate area computations.','The whole parallelogram has horizontal base BC of length 6 and vertical height 6, from y=-3 to y=3. Its area is 6*6=36.','For -3<=y<=0, edge BC/AD gives right boundary x=y, while edge AB/DC gives left boundary x=y-6. More precisely the two slanted sides AB and CD have equations x=y and x=y-6; the section width is 6. Integrating over height 3 gives lower area 6*3=18.','The x-axis itself has zero area. Thus the probability of not being above it is 18/36=1/2.','1/2'),
'2491':('Use equally likely unordered pairs of distinct cards, because the event does not depend on draw order.','There are 26 red cards. Red-only pairs number binomial(26,2)=26*25/2=325.','All pairs from the 52-card deck number binomial(52,2)=52*51/2=1326.','The desired probability is 325/1326=25/102.','25/102'),
'1905':('The product is odd exactly when both selected integers are odd. Count favorable pairs and all possible pairs independently.','The odd integers are 5,7,9,11,13,15,17, seven in total. Favorable distinct pairs number binomial(7,2)=21.','The inclusive interval has 17-5+1=13 integers. All distinct unordered pairs number binomial(13,2)=13*12/2=78.','The probability is 21/78=7/26.','7/26'),
'351':('Let u=1/x and v=1/y. The given equations become u+v=3 and u-v=-7. Solve separately for each reciprocal.','Adding the equations gives 2u=-4, so u=-2. Hence x=-1/2.','Subtracting the second equation from the first gives 2v=10, so v=5. Hence y=1/5.','Therefore x+y=-1/2+1/5=(-5+2)/10=-3/10.','-3/10'),
'1831':('Mary and James occupy distinct seats. Every ordered pair of distinct chairs is equally likely. Count all pairs and adjacent pairs independently.','Mary has 7 choices. For each, James has 6 remaining choices. Thus total ordered seat pairs number 7*6=42.','The seven-chair row has six neighboring chair pairs. Each supports two assignments of Mary and James, so adjacent ordered pairs number 6*2=12.','Nonadjacent pairs number 42-12=30. The desired probability is 30/42=5/7.','5/7'),
'779':('Let p and q be the pencil and pen prices in cents. Then 5p+q=250 and p+2q=185. Eliminate independently to determine each price.','Double the first equation to obtain 10p+2q=500. Subtract the second equation: 9p=315. Thus p=35 cents.','Multiply the second equation by 5: 5p+10q=925. Subtract the first equation: 9q=675. Thus q=75 cents.','Two pencils and one pen cost 2*35+75=145 cents, or 29/20 dollars.','$29/20'),
'6215':('Simplify the two radical ratios independently using positive square roots.','Since 338=169*2 and 288=144*2, the first ratio is (13 sqrt(2))/(12 sqrt(2))=13/12.','Since 150=25*6 and 96=16*6, the second ratio is (5 sqrt(6))/(4 sqrt(6))=5/4.','Their sum is 13/12+5/4=13/12+15/12=28/12=7/3.','7/3'),
'1936':('There are 3^3=27 equally likely ordered meal choices. At least two fruit kinds splits into exactly two kinds and exactly three kinds.','For exactly two kinds, choose the missing fruit in 3 ways. Using the other two kinds over three meals gives 2^3 sequences, but remove the two constant sequences. Thus this case has 3*(8-2)=18 sequences.','For exactly three kinds, every fruit occurs once. Assigning them to breakfast, lunch, and dinner gives 3!=6 sequences.','These cases are disjoint and exhaustive for the target event. Probability is (18+6)/27=24/27=8/9.','8/9'),
'1226':('Multiply both equations by 10: 30x-50y=-15 and 70x+20y=47. Eliminate separately for x and y.','Multiply the first equation by 2 and the second by 5: 60x-100y=-30 and 350x+100y=235. Adding gives 410x=205, hence x=0.5.','Multiply the first equation by 7 and the second by 3: 210x-350y=-105 and 210x+60y=141. Subtract the first from the second: 410y=246, hence y=0.6.','The independently obtained coordinates form (0.5,0.6). Checking gives 1.5-3=-1.5 and 3.5+1.2=4.7.','(0.5,0.6)')}
# Correct the lower-region geometry precisely before emitting.
sol['2782']=(sol['2782'][0],sol['2782'][1],'The slanted sides AB and CD lie on x=y and x=y-6, respectively. At every height -3<=y<=0, the horizontal section has width y-(y-6)=6. Its height is 3, so the portion on or below the x-axis has area 6*3=18.',sol['2782'][3],sol['2782'][4])
reasons={
'3849':'Polynomial expansion has no compelling pair of independently substantive computations; term grouping would be artificial.',
'5137':'Base conversion and subsequent arithmetic form a sequential chain; isolated conversions are too small to be substantive branches.',
'6323':'Removed amount, refill, and final amount are sequentially dependent.',
'6113':'Repeating single-digit decimals require only elementary conversions; no two substantive independent branches.',
'4188':'Single telescoping product; splitting its range would be artificial.',
'1606':'Real and imaginary components are elementary arithmetic, insufficiently substantive.',
'7110':'Coordinate conversions are immediate sine/cosine evaluations, insufficiently substantive.',
'6803':'Reciprocal identity and recovery of sine form one dependent calculation.',
'6373':'Individual rounding checks are trivial, not substantive independent computations.',
'6048':'Collecting linear and constant coefficients is elementary arithmetic.',
'6687':'Single common-denominator addition.',
'701':'Real and imaginary component sums are trivial arithmetic.',
'4168':'Finding positive integer complex root uses coupled real and imaginary constraints; no robust independent split.',
'4484':'Coordinate averaging is trivial arithmetic.',
'6959':'Triple-angle substitution is a single computation; numerator and denominator arithmetic do not form substantive branches.',
'5549':'Prefix count and suffix permutation count are too elementary to form two substantive branches.',
'2218':'Linear expectation of four fair coins needs only trivial per-coin contributions; grouping would be artificial.',
'6918':'Angle-addition evaluation has only elementary standard-angle terms; no substantive independent work.'}
screens=[]; traces=[]
for r in rows:
 k=r['id'].split('/')[-1]
 if k in sol:
  setup,a,b,combine,final=sol[k]
  response=f'<think>\n{setup}\n\nPart 1:\n{a}\n\nPart 2:\n{b}\n\n{combine}\n</think>\nFinal Answer: {final}'
  traces.append({**r,'response':response})
  screens.append({'id':r['id'],'verdict':'accept','reason':'Two independent substantive computations from problem facts; combine only after both parts.'})
 else:
  screens.append({'id':r['id'],'verdict':'reject','reason':reasons[k]})
for name,data in [('screen.jsonl',screens),('traces.jsonl',traces)]:
 (p/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
(p/'review.md').write_text('Reviewed all 32 blind questions. Accepted 14; rejected 18. No gold or source answers read.\n\nAccepted examples: math-train/1226 independently eliminates for each coordinate; math-train/1936 independently counts exactly two and exactly three fruit kinds; math-train/6215 independently simplifies two radical ratios. Every trace combines results after both parts and gives one final answer outside the think block.\n\nRejected examples: math-train/4188 is one telescoping chain; gsm8k-train/6323 is sequential; math-train/4484 has only trivial coordinate averages.\n\nProbability questions use conventional independent-trial interpretations. math-train/2026 explicitly requests five visits despite its introductory week phrasing. Geometry trace uses correct slanted sides AB and CD.\n')
print(len(screens),len(traces))
