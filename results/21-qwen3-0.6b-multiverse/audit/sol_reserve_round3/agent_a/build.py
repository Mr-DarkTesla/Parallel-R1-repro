import json
from pathlib import Path
p = Path(__file__).parent
rows = [json.loads(s) for s in (p/'input.jsonl').read_text().splitlines()]
accepted = {}
def add(n, setup, one, two, combine, final, reason):
    accepted[n] = (f'<think>\n{setup}\n\nPart 1:\n{one}\n\nPart 2:\n{two}\n\n{combine}\n</think>\nFinal Answer: {final}', reason)
add('1544', 'Let e and t be the prices of one enchilada and one taco. The given equations are 2e+3t=2.50 and 3e+2t=2.70.',
'Eliminate t to compute the enchilada price. Twice the first equation gives 4e+6t=5.00; three times the second gives 9e+6t=8.10. Subtraction gives 5e=3.10, so e=0.62.',
'Independently eliminate e to compute the taco price. Three times the first equation gives 6e+9t=7.50; twice the second gives 6e+4t=5.40. Subtraction gives 5t=2.10, so t=0.42.',
'The requested cost is 3e+4t=3(0.62)+4(0.42)=1.86+1.68=3.54.', '3.54', 'Independent elimination solves each item price from original equations.')
add('1975', 'Treat each coin as fair and independent, so the 8 flips have 2^8 equally likely outcomes. More heads than tails means 5, 6, 7, or 8 heads.',
'Count outcomes with 5 or 6 heads: C(8,5)+C(8,6)=56+28=84.',
'Count outcomes with 7 or 8 heads: C(8,7)+C(8,8)=8+1=9.',
'These cases are disjoint, so the probability is (84+9)/256=93/256.', '93/256', 'Independent disjoint binomial counts combine into requested probability.')
add('4150', 'All spending fractions refer to the original $240 incentive. The saved amount is three quarters of the money left after both purchases.',
'Food costs (1/3)(240)=$80.',
'Clothes cost (1/5)(240)=$48.',
'The remaining amount is 240-80-48=112 dollars. Savings are (3/4)(112)=84 dollars.', '$84', 'Independent expenditures feed remaining balance and savings.')
add('6643', 'Evaluate each factor before multiplying.',
'The first factor is (1/2)^8=1/256.',
'The second factor is (3/4)^(-3)=(4/3)^3=64/27.',
'The product is (1/256)(64/27)=1/108.', '1/108', 'Separate exponent computations are independent factors.')
add('6751', 'Since 4!=24=2^3 times 3, each positive divisor has the form 2^u 3^v with 0<=u<=3 and v either 0 or 1. All positive divisors lie between 1 and 24.',
'For v=0 the divisors are 1, 2, 4, and 8: four choices.',
'For v=1 the divisors are 3, 6, 12, and 24: four choices.',
'The groups are disjoint, giving 8 favorable numbers among 24 equally likely numbers. The probability is 8/24=1/3.', '1/3', 'Independent divisor groups yield favorable count.')
add('7220', 'A dilation with center c and factor s sends z to c+s(z-c). Here c=-1+4i, s=-2, and z=0+2i. Real and imaginary coordinates transform separately.',
'The real coordinate becomes -1+(-2)(0-(-1))=-1-2=-3.',
'The imaginary coordinate becomes 4+(-2)(2-4)=4+4=8.',
'Combining the transformed coordinates gives -3+8i.', '-3+8i', 'Independent coordinate transformations.')
add('1250', 'Equal utility requires the two daily products to agree.',
'Using only Monday\'s hours, utility is t(8-t)=8t-t^2.',
'Using only Tuesday\'s hours, utility is (2-t)(t+3)=2t+6-t^2-3t=6-t-t^2.',
'Equating the independently computed products gives 8t-t^2=6-t-t^2, hence 9t=6 and t=2/3. This value makes every stated duration nonnegative.', '2/3', 'Independent expansions of daily utilities precede equality solve.')
add('3992', 'For any real number u, its fractional part {u} lies in [0,1), and u=floor(u)+{u}.',
'From floor(x)+{y}=2.4, the only possible integer floor(x) is 2. Thus {y}=0.4.',
'From {x}+floor(y)=5.1, the only possible integer floor(y) is 5. Thus {x}=0.1.',
'Combine these components: x=2+0.1=2.1 and y=5+0.4=5.4. Therefore |x-y|=3.3=33/10.', '33/10', 'Each original equation independently determines separate integer and fractional components.')
add('5879', 'Simplify numerator and denominator separately using exponent addition.',
'The numerator is 2^2 times 2^(-3)=2^(-1)=1/2.',
'The denominator is 2^3 times 2^(-2)=2^1=2.',
'The quotient is (1/2)/2=1/4.', '1/4', 'Independent numerator and denominator computations.')
add('7203', 'Scale the equilateral triangle to side length 6: B=(0,0), C=(6,0), A=(3,3sqrt(3)), D=(2,0), E=(4,0). Thus AD and AE have vectors u=(-1,-3sqrt(3)) and v=(1,-3sqrt(3)). The sine between two planar vectors equals their absolute determinant divided by the product of their lengths.',
'Compute the determinant directly from the coordinates: det(u,v)=(-1)(-3sqrt(3))-(-3sqrt(3))(1)=6sqrt(3). Its absolute value is 6sqrt(3).',
'Compute the length product directly from the coordinates: |u|=sqrt(1+27)=sqrt(28) and |v|=sqrt(1+27)=sqrt(28), so |u||v|=28.',
'Therefore sin(angle DAE)=6sqrt(3)/28=3sqrt(3)/14.', '3sqrt(3)/14', 'Independent determinant and norm computations from common coordinate setup.')
add('421', 'Interpret inverse relation as score times sleep hours being constant. Let the second score be s and the required hours be h.',
'The first exam fixes the inverse-proportion constant: 8 times 70=560.',
'The desired average independently fixes the second score: (70+s)/2=80, so s=160-70=90.',
'Then 90h=560, giving h=56/9=6.222... hours. Rounded to the nearest tenth, this is 6.2 hours.', '6.2', 'Independent inverse constant and target-score computations.')
add('2448', 'Three independent equally likely births give 2^3=8 equally likely ordered outcomes. A mixed family has exactly one boy or exactly two boys.',
'Exactly one boy can occupy any of three positions, giving C(3,1)=3 outcomes.',
'Exactly two boys can occupy any pair of positions, giving C(3,2)=3 outcomes.',
'The disjoint groups contain 3+3=6 outcomes, so the probability is 6/8=3/4.', '3/4', 'Independent disjoint family-composition counts.')
add('4536', 'The roots of the product polynomial are the roots of the two cubic factors, counted with multiplicity. A cubic with leading coefficient A and constant term D has root product -D/A.',
'For 2x^3+x^2-8x+20, the root product is -20/2=-10.',
'For 5x^3-25x^2+19, the root product is -19/5.',
'The product of all six roots is (-10)(-19/5)=38.', '38', 'Independent Vieta products for original cubic factors.')
add('694', 'Compute the two summands separately.',
'12 times 24=288.',
'36 times 12=432.',
'Adding the two results gives 288+432=720.', '720', 'Independent arithmetic products combine by addition.')
add('4436', 'To establish a maximum, derive an upper bound and separately find an admissible point attaining it.',
'Multiply 3x+2y<=7 by 1/4 and 2x+4y<=8 by 1/8. Both multipliers are positive. Adding gives x+y<=7/4+1=11/4.',
'Solve the boundary equations directly. Twice 3x+2y=7 is 6x+4y=14; subtracting 2x+4y=8 gives 4x=6, hence x=3/2. Substitution gives y=5/4. This point satisfies both inequalities with equality.',
'The admissible point has x+y=3/2+5/4=11/4, which attains the independently derived upper bound. Therefore the largest value is 11/4.', '11/4', 'Independent dual upper bound and primal attaining-point calculation.')
add('6945', 'A matrix is its own inverse exactly when its square is the identity. For M=[[3,-1],[c,d]], M^2=[[9-c,-3-d],[c(3+d),-c+d^2]].',
'The upper-left identity condition gives 9-c=1, so c=8.',
'The upper-right identity condition gives -3-d=0, so d=-3.',
'Combining these values, the lower-left entry is 8(3-3)=0 and the lower-right entry is -8+9=1. Thus the full square is the identity and (c,d)=(8,-3).', '(8,-3)', 'Independent identity-entry equations determine different parameters.')
add('2513', 'Assume games are independent. Seven equally likely binary game results give 2^7=128 outcomes. Winning at least four games means 4, 5, 6, or 7 wins.',
'Count sequences with 4 or 5 Badgers wins: C(7,4)+C(7,5)=35+21=56.',
'Count sequences with 6 or 7 Badgers wins: C(7,6)+C(7,7)=7+1=8.',
'The groups are disjoint, so the probability is (56+8)/128=64/128=1/2.', '1/2', 'Independent disjoint binomial counts.')
add('1983', 'Measure arrival times as fractions of the hour after 1:00. Let A and B be independent uniform points in [0,1]. Conditioning on A>B restricts the unit square to the region above the diagonal.',
'The conditioning region A>B is a triangle with area 1/2, so P(A>B)=1/2.',
'The joint event B<1/2 and A>B has area integral from 0 to 1/2 of (1-b) db. This equals [b-b^2/2] from 0 to 1/2, or 1/2-1/8=3/8.',
'The conditional probability is (3/8)/(1/2)=3/4.', '3/4', 'Independent conditioning-region and joint-event area computations.')
add('1938', 'Sun contributes zero rain. Linearity of expectation lets us sum rainfall contributions across all five days without assuming independence between days.',
'The 4-inch outcome contributes 0.25 times 4=1 expected inch per day, hence 5 expected inches over five days.',
'The 10-inch outcome contributes 0.35 times 10=3.5 expected inches per day, hence 17.5 expected inches over five days.',
'Total expected rainfall is 5+17.5=22.5 inches, already rounded to the nearest tenth.', '22.5', 'Independent rainfall-outcome contributions to expectation.')
add('253', 'Expand each original product separately, then collect equal powers of x.',
'The first product is x(3x^2-2)=3x^3-2x.',
'The second product, including its minus sign, is -5(x^2-2x+7)=-5x^2+10x-35.',
'Adding gives 3x^3-5x^2+(-2+10)x-35=3x^3-5x^2+8x-35.', '3x^3-5x^2+8x-35', 'Independent original polynomial-product expansions.')
add('1976', 'Four labeled dice have 20^4 equally likely ordered face outcomes. Each die has 10 even faces and 10 odd faces.',
'Choose which two dice are even: C(4,2)=4 times 3 / 2=6 position patterns.',
'For any fixed pattern with two even and two odd positions, each position has 10 allowed faces. Thus each pattern has 10^4=10000 face assignments.',
'The patterns are disjoint, so favorable outcomes number 6 times 10000=60000. The probability is 60000/20^4=60000/160000=3/8.', '3/8', 'Independent position-pattern and within-pattern face counts.')
rejected = {
'4411':'Coefficient integrality is unstated; rational-root theorem would require an extra assumption. Reject uncertain problem.',
'7194':'Natural multiple-angle evaluation is one sequential computation; splitting it would require artificial intermediate checks.',
'4192':'Natural square-root solve uses coupled real and imaginary constraints; insufficient substantive independent branches.',
'7256':'Equality condition drives a sequential substitution into target; denominators and a+b also require unstated nonzero conditions.',
'982':'Single monomial simplification; artificial division of tiny factor arithmetic would add no substantive branches.',
'3086':'Natural coordinate or similarity solution determines intersection first, then area; no clear independent substantive split.',
'3299':'Single angle-bisector ratio computation; preliminary side scaling is dependent setup rather than a substantive independent branch.',
'533':'Single geometric-series identification and sum; ratio and first term do not support two substantive computations.',
'4241':'Root geometry and shortest polygon ordering require a rigorous independent optimization argument; not confident enough to supply a trace.',
'4042':'Second geometric-series evaluation depends directly on relation obtained from first; no independent original-fact branches.',
'2883':'Base and height are immediate coordinate differences; splitting them would not be substantive.',
'6839':'Elimination plus triangle inequalities is sequential; no confidently identified independent two-branch solution.'}
assert len(rows)==33
assert len(accepted)+len(rejected)==33
screen=[]
traces=[]
for row in rows:
    n=row['id'].split('/')[-1]
    if n in accepted:
        response,reason=accepted[n]
        screen.append({'id':row['id'],'verdict':'accept','reason':reason})
        traces.append({**row,'response':response})
    else:
        screen.append({'id':row['id'],'verdict':'reject','reason':rejected[n]})
(p/'screen.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in screen))
(p/'traces.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in traces))
(p/'review.md').write_text('''# Blind independent-computation audit\n\n33 questions screened. Accepted: 21. Rejected: 12. No gold labels, model answers, or other agent folders read. Source question strings preserved directly from input objects.\n\nAccepted traces contain common setup, two independent computation sections, and a combination after both sections inside think. Final Answer occurs once outside think. No Multiverse tags added.\n\nStrong examples: math-train/1544 independently eliminates separate prices; math-train/4436 independently derives an upper bound and an attaining feasible point; math-train/7203 independently computes vector determinant and norm product; math-train/1983 independently computes conditioning and joint-event areas.\n\nElementary valid examples: math-train/694 computes two original summands; math-train/253 expands two original products; gsm8k-train/4150 computes food and clothes expenditures independently. Their branches are short but correspond to distinct original problem components.\n\nRejected examples: math-train/4241 requires a confidently proved shortest polygon ordering; math-train/4411 does not explicitly make coefficients integers; math-train/3086 and math-train/4042 naturally form sequential solutions. math-train/2883 has only trivial coordinate differences.\n\nAssumptions: ordinary fair independent flips in math-train/1975; independent games in math-train/2513; independent uniform arrival times in math-train/1983. These are standard interpretations of stated random experiments. No independence between weather days is assumed.\n\nVerification: build.py records generation; validation.txt records structural checks and exact rational arithmetic checks.\n''')
print(f'Screened {len(screen)}; accepted {len(traces)}; rejected {len(rejected)}')
