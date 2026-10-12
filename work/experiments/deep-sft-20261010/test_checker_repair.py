"""Regression proof for confirmed pilot parser failures; no teacher invocation."""
from arithmetic_check_v2 import check
from oracle_check_v2 import check as oracle_check

for text in ['X = 3*32+33+4 = 96+33+4 = 133.',
             'X = 2*53+39-2 = 106+39-2 = 143.',
             'Total = 2*143+118+122 = 286+118+122 = 526.',
             'X = (3+5)*2 = 16.', 'X = 1/3+2/3 = 1.']:
    result = check(text)
    assert result['explicit_scalar_equalities_checked'] > 0 and not result['mismatches'], (text, result)
for text in ['X = 3*32+33+4 = 96+33+4 = 134.',
             'X = 3*32+33+4 = 97+33+4 = 134.',
             'X = (3+5)*2 = 15.', 'X = 8*9*37 = 2952.']:
    assert check(text)['mismatches'], text

oracle = dict(names=['Apple', 'Pear'], initial=[3, 4],
              stages=[[dict(result=7), dict(result=10)]])
def trace(a, p, final):
    return f'<Parallel>2\n<Path>1\n{a}\n</Path><Path>2\n{p}\n</Path></Parallel><Summary>Apple_1 = 7, Pear_1 = 10.</Summary>\nFinal solution:\n{final}'
def checked(text):
    import re
    m = re.search(r'<Parallel>.*?</Summary>', text, re.S)
    paths = re.findall(r'<Path>([12])\n(.*?)</Path>', m[0], re.S)
    summary = re.search(r'<Summary>(.*?)</Summary>', m[0], re.S)[1]
    return oracle_check(text, oracle, [dict(start=m.start(), end=m.end(), paths=paths, summary=summary)])
good = trace('Apple_1 = 3 + 4 = 7.', 'Pear_1 = 2*3 + 4 = 10.',
             'Apple_1 = 7. The weighted sum is 2*7 + 10 = 24.')
assert not checked(good)['failures'], checked(good)
bad = trace('Apple_1 = 3 + 4 = 8.', 'Pear_1 = 2*3 + 4 = 10.', 'Total = 24.')
assert any(f['type'] == 'named_intermediate_mismatch' for f in checked(bad)['failures'])
bad = trace('Apple_1 = Apple_1 + 0 = 7.', 'Pear_1 = 2*3 + 4 = 10.', 'Total = 24.')
assert any(f['type'] == 'reference_unavailable_to_sibling' for f in checked(bad)['failures'])
bad = trace('Apple_1 = 3 + 4 = 7.', 'Pear_1 = Apple_1 + 3 = 10.', 'Total = 24.')
assert any(f['type'] == 'reference_unavailable_to_sibling' for f in checked(bad)['failures'])
print('PASS: five positive and four negative arithmetic chains; final-sum boundary, wrong intermediate, self-reference, sibling leakage.')
