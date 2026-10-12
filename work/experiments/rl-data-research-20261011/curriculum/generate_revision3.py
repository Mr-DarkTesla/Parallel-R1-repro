"""Original deterministic math tasks; independent validation required for admission."""
from pathlib import Path
import random,json,hashlib,math,itertools,collections,re,unicodedata
OUT=Path('work/experiments/rl-instruct-20261011/data/revision3');OUT.mkdir(exist_ok=True)
SEED=20261011
def poly_mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def generate(family,i):
 r=random.Random(f'{SEED}:{family}:{i}');p={};oracle={}
 if family=='crt_three':
  mods=r.sample([5,7,11,13,17,19,23,29,31],3); residues=[r.randrange(m) for m in mods];M=math.prod(mods)
  a=sum(v*(M//m)*pow(M//m,-1,m) for v,m in zip(residues,mods))%M
  p={'moduli':mods,'residues':residues};q='Determine the least nonnegative integer n satisfying all three congruences: '+', '.join(f'n ≡ {v} (mod {m})' for v,m in zip(residues,mods))+'.'
 elif family=='polynomial_coefficient':
  factors=[(r.randint(1,6),r.choice([-1,1])*r.randint(1,8)) for _ in range(r.randint(4,7))];degree=r.randint(1,len(factors)-1);c=[1]
  for u,v in factors:c=poly_mul(c,[v,u])
  a=c[degree];p={'factors':factors,'degree':degree};q='Expand the polynomial P(x) = '+''.join(f'({u}x{v:+d})' for u,v in factors)+f'. What is the coefficient of x^{degree}?'
 elif family=='bounded_weighted_count':
  weights=r.sample(range(2,10),3);bounds=[r.randint(5,12) for _ in range(3)];target=r.randint(15,sum(w*b for w,b in zip(weights,bounds))-10)
  a=sum(sum(w*x for w,x in zip(weights,xs))==target for xs in itertools.product(*(range(b+1) for b in bounds)))
  p={'weights':weights,'bounds':bounds,'target':target};q=f'How many ordered triples of integers (u,v,w) satisfy {weights[0]}u+{weights[1]}v+{weights[2]}w={target}, with 0≤u≤{bounds[0]}, 0≤v≤{bounds[1]}, and 0≤w≤{bounds[2]}?'
 elif family=='diophantine_positive_count':
  aa=r.randint(3,18);bb=r.randint(3,18);n=r.randint(80,500);a=sum((n-aa*x)>0 and (n-aa*x)%bb==0 for x in range(1,n//aa+1))
  p={'a':aa,'b':bb,'n':n};q=f'Find the number of ordered pairs of strictly positive integers (x,y) satisfying {aa}x+{bb}y={n}.'
 elif family=='linear_system_three':
  while True:
   matrix=[[r.randint(-5,5) for _ in range(3)] for _ in range(3)]
   det=sum((-1 if sum(perm[j]>perm[k] for j in range(3) for k in range(j+1,3))%2 else 1)*math.prod(matrix[j][perm[j]] for j in range(3)) for perm in itertools.permutations(range(3)))
   if det and all(all(v!=0 for v in row) for row in matrix):break
  hidden=[r.randint(-9,9) for _ in range(3)];rhs=[sum(c*v for c,v in zip(row,hidden)) for row in matrix];a=hidden[0]*hidden[1]+hidden[2]
  p={'matrix':matrix,'rhs':rhs,'target':'x*y+z'};q='The real numbers x, y, and z satisfy the simultaneous equations '+ '; '.join(f'{row[0]}x{row[1]:+d}y{row[2]:+d}z={n}' for row,n in zip(matrix,rhs))+'. Calculate xy+z.'
 elif family=='power_sum_mod':
  bases=r.sample(range(2,40),3);exponents=[r.randint(35,180) for _ in range(3)];m=r.choice([49,81,121,125,169,243,289,343,361,625,729,841]);a=sum(pow(b,e,m) for b,e in zip(bases,exponents))%m
  p={'bases':bases,'exponents':exponents,'modulus':m};q='What is the least nonnegative remainder when '+ ' + '.join(f'{b}^{e}' for b,e in zip(bases,exponents))+f' is divided by {m}?'
 elif family=='subset_residue_count':
  values=r.sample(range(1,45),r.randint(8,11));k=r.randint(3,5);m=r.randint(3,9);residue=r.randrange(m);a=sum(sum(xs)%m==residue for xs in itertools.combinations(values,k))
  p={'values':values,'k':k,'modulus':m,'residue':residue};q=f'For the set S={{{",".join(map(str,values))}}}, how many subsets of exactly {k} elements have an element sum congruent to {residue} modulo {m}?'
 elif family=='quadratic_root_power':
  u,v=r.sample(range(-18,19),2);power=r.randint(4,9);a=u**power+v**power;p={'root_sum':u+v,'root_product':u*v,'power':power}
  q=f'The two roots of x²{-(u+v):+d}x{u*v:+d}=0 are α and β. Compute α^{power}+β^{power}.'
 elif family=='second_order_recurrence':
  aa=r.randint(1,5);bb=r.randint(1,5);u,v=r.randint(0,9),r.randint(0,9);n=r.randint(18,55);m=r.choice([97,101,127,149,169,211,251,343,625]);x,y=u,v
  for _ in range(2,n+1):x,y=y,(aa*y+bb*x)%m
  a=y%m;p={'a':aa,'b':bb,'u0':u,'u1':v,'n':n,'modulus':m};q=f'Let u₀={u}, u₁={v}, and uₖ={aa}uₖ₋₁+{bb}uₖ₋₂ for integers k≥2. Determine the least nonnegative remainder of u{n} modulo {m}.'
 elif family=='determinant_3':
  matrix=[[r.randint(-8,8) for _ in range(3)] for _ in range(3)];a=sum((-1 if sum(perm[j]>perm[k] for j in range(3) for k in range(j+1,3))%2 else 1)*math.prod(matrix[j][perm[j]] for j in range(3)) for perm in itertools.permutations(range(3)))
  p={'matrix':matrix};q='Compute the determinant of the 3×3 matrix with rows '+ '; '.join(str(x) for x in matrix)+'.'
 elif family=='divisor_gcd_sum':
  n=r.randint(25,250);t=r.randint(10,160);a=sum(math.gcd(d,t) for d in range(1,n+1) if n%d==0);p={'n':n,'t':t};q=f'Let D be the set of all positive divisors of {n}. Calculate the sum of gcd(d,{t}) over d in D.'
 elif family=='third_order_recurrence':
  coeff=[r.randint(1,4) for _ in range(3)];initial=[r.randint(0,8) for _ in range(3)];n=r.randint(14,35);m=r.choice([97,101,127,149,211,251]);seq=initial[:]
  for j in range(3,n+1):seq.append(sum(coeff[k]*seq[j-1-k] for k in range(3))%m)
  a=seq[n]%m;p={'coefficients':coeff,'initial':initial,'n':n,'modulus':m};q=f'The sequence starts v₀={initial[0]}, v₁={initial[1]}, v₂={initial[2]} and satisfies vₖ={coeff[0]}vₖ₋₁+{coeff[1]}vₖ₋₂+{coeff[2]}vₖ₋₃ for k≥3. Find the least nonnegative residue of v{n} modulo {m}.'
 elif family=='binomial_product_coefficient':
  u=r.randint(1,5);v=r.choice([-1,1])*r.randint(1,6);aa=r.randint(4,8);bb=r.randint(4,8);degree=r.randint(2,aa+bb-2)
  a=sum(math.comb(aa,j)*u**j*math.comb(bb,degree-j)*v**(degree-j) for j in range(aa+1) if 0<=degree-j<=bb)
  p={'u':u,'v':v,'a':aa,'b':bb,'degree':degree};q=f'Find the coefficient of x^{degree} in (1+{u}x)^{aa}(1{v:+d}x)^{bb}.'
 else:raise ValueError(family)
 return {'id':f'original-math-v3/{family}/{i}','problem':q,'answer':str(a),'source':'original_exact_math_generator','source_revision':'revision3-20261011','template_family':family,'split_group':family,'parameters':p,'generation_seed':f'{SEED}:{family}:{i}','oracle_method':'deterministic_integer_generator_pending_independent_different_method_validation','not_benchmark_derived':True}
trainfamilies=['crt_three','polynomial_coefficient','bounded_weighted_count','diophantine_positive_count','linear_system_three','subset_residue_count','quadratic_root_power','second_order_recurrence']
valfamilies=['determinant_3','divisor_gcd_sum','third_order_recurrence','binomial_product_coefficient']
for phase,ntrain,nval in [('stage256',32,16),('full1024',128,32)]:
 d=OUT/phase;d.mkdir(exist_ok=True)
 for split,families,n in [('train',trainfamilies,ntrain),('val',valfamilies,nval)]:
  rows=[];duplicates=[]
  for family in families:
   unique=set();i=0;accepted=0
   while accepted<n:
    row=generate(family,i);i+=1
    key=' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',row['problem']).lower()))
    if key in unique:duplicates.append(row['id']);continue
    unique.add(key);rows.append(row);accepted+=1
  random.Random(SEED).shuffle(rows);(d/(split+'.candidate.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
  (d/(split+'.duplicate-rejections.json')).write_text(json.dumps(duplicates))
(OUT/'generation-manifest.json').write_text(json.dumps({'passed':False,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'train_families':trainfamilies,'val_families':valfamilies,'group_rule':'entire template family assigned exclusively to one split','different_data_arm':True,'fairness_limit':'Original exact oracle tasks replace published BigMath; do not attribute improvements to reward alone','risks':['Only8trainingtemplates: many parameter variations are structural clones within training; no claim of1152independent reasoning skills','Nominal generated difficulty does not establish current4B difficulty; actualrolloutscreen needed','Independent differentmethod oracle and benchmark/SFT contamination audit required beforeadmission'],'requires':['independent_oracle_all_rows','source_and_family_audit','exact_actual_reward_parser_preflight','MATH12500_AIME60_currentSFT3000_frozenpilot16_exclusion']},indent=2))
print('Generated provisional stage256 train256,val64; full1024 train1024,val128')
