from oracle_check_v3 import check
oracle=dict(names=['Apple','Pear'],initial=[3,4],stages=[[dict(result=7),dict(result=10)]])
def proof(path):
    text='x<Parallel>3\n<Path>1\nApple_1 = 3+4 = 7.\n</Path><Path>2\nPear_1 = 2*3+4 = 10.\n</Path><Path>3\n'+path+'\n</Path></Parallel><Summary>Apple_1 = 7, Pear_1 = 10; check agrees.</Summary>'
    import re
    m=re.search(r'<Parallel>.*?</Summary>',text,re.S)
    return check(text,oracle,[dict(start=m.start(),end=m.end(),paths=re.findall(r'<Path>([123])\n(.*?)</Path>',m[0],re.S),summary='Apple_1 = 7, Pear_1 = 10; check agrees.')])
assert not proof('Apple_1 check = 3+4 = 7.')['failures']
assert any(f['type']=='named_intermediate_mismatch' for f in proof('Apple_1 check = 3+4 = 8.')['failures'])
assert any(f['type']=='reference_unavailable_to_sibling' for f in proof('Apple_1 check = Apple_1+0 = 7.')['failures'])
assert any(f['type']=='reference_unavailable_to_sibling' for f in proof('Apple_1 check = Pear_1-3 = 7.')['failures'])
print('PASS: meaningful verification alias; wrong value, self-reference, and sibling read rejected.')
