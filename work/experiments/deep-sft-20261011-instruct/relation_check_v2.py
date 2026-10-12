"""Conservative source-relation proof; unsupported expressions fail closed."""
import ast, collections, re

def polynomial(expression):
    def visit(n):
        if isinstance(n, ast.Constant) and type(n.value) is int:
            return {(): n.value}
        if isinstance(n, ast.Name): return {(n.id,): 1}
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return {k: -v for k,v in visit(n.operand).items()}
        if isinstance(n, ast.BinOp):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,(ast.Add,ast.Sub)):
                c=collections.Counter(a)
                for k,v in b.items(): c[k]+=v*(-1 if isinstance(n.op,ast.Sub) else 1)
                return {k:v for k,v in c.items() if v}
            if isinstance(n.op,ast.Mult):
                c=collections.Counter()
                for k,v in a.items():
                    for q,w in b.items(): c[tuple(sorted(k+q))]+=v*w
                return {k:v for k,v in c.items() if v}
        raise ValueError('unsupported_ast')
    return visit(ast.parse(expression.strip(),mode='eval').body)

def numeric_signature(expression):
    """Preserve substituted operands, preventing answer-only expressions passing."""
    def visit(n,sign=1):
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub)):
            return visit(n.left,sign)+visit(n.right,sign*(-1 if isinstance(n.op,ast.Sub) else 1))
        def factors(q):
            if isinstance(q,ast.Constant) and type(q.value) is int:return [q.value]
            if isinstance(q,ast.BinOp) and isinstance(q.op,ast.Mult):return factors(q.left)+factors(q.right)
            raise ValueError('unsupported_numeric_ast')
        fs=factors(n);fs=[v for v in fs if v!=1] or [1]
        return [(sign,tuple(sorted(fs)))]
    return sorted(visit(ast.parse(expression.strip(),mode='eval').body))

def check(text,oracle,blocks):
    expected={};values={f'{n}_0':v for n,v in zip(oracle['names'],oracle['initial'])}
    for s,layer in enumerate(oracle['stages'],1):
        for name,node in zip(oracle['names'],layer):
            a,b=[f'{oracle["names"][i]}_{s-1}' for i in node['parents']]
            sym=f'{node["coefficient"]}*{a}+{b}{node["offset_sign"]}{node["offset"]}'
            num=f'{node["coefficient"]}*{node["operands"][0]}+{node["operands"][1]}{node["offset_sign"]}{node["offset"]}'
            expected[f'{name}_{s}']=(sym,num,node['result'])
            values[f'{name}_{s}']=node['result']
    failures=[];receipts=[];produced={};deps=set()
    for ri,block in enumerate(blocks,1):
        for pid,body in block['paths']:
            matches=list(re.finditer(r'\b([A-Za-z]+_\d+)(?:\s+check)?\s*=\s*([^\n;]+)',body))
            valid_count=0
            for m in matches:
                name=m[1]
                if name not in expected: failures.append(['unknown_path_lhs',ri,int(pid),name]);continue
                # End the equality chain before prose, punctuation, or closing XML.
                chain=m[2].replace('$','').replace('\\times','*').replace('×','*').replace('\\cdot','*')
                chain=re.split(r'\.(?!\d)|,|<',chain)[0].strip()
                parts=[p.strip() for p in chain.split('=')]
                sym,num,result=expected[name]
                try:
                    assert len(parts)>=2 and re.fullmatch(r'-?\d+',parts[-1]) and int(parts[-1])==result
                    numeric=[p for p in parts[:-1] if not re.search('[A-Za-z]',p)]
                    symbolic=[p for p in parts[:-1] if re.search('[A-Za-z]',p)]
                    assert numeric and any(numeric_signature(p)==numeric_signature(num) for p in numeric)
                    for p in numeric:assert polynomial(p)=={():result}
                    for p in symbolic:assert polynomial(p)==polynomial(sym)
                    # A symbolic derivation is mandatory: arithmetic alone cannot prove source parents.
                    assert symbolic
                    parents={n.id for n in ast.walk(ast.parse(sym,mode='eval')) if isinstance(n,ast.Name)}
                    for parent in parents:
                        if parent.endswith('_0'):continue
                        assert parent in produced and produced[parent]<ri
                        deps.add((produced[parent],ri))
                    receipts.append(dict(round=ri,path=int(pid),label=name,source_relation=sym,numeric_relation=num,result=result))
                    valid_count+=1
                except (AssertionError,ValueError,SyntaxError):failures.append(['relation_or_dependency_unproven',ri,int(pid),name,parts])
            if not valid_count:failures.append(['path_without_proven_computation',ri,int(pid)])
        for receipt in receipts:
            if receipt['round']==ri:produced.setdefault(receipt['label'],ri)
    missing=sorted(set(expected)-set(produced))
    if missing:failures.append(['missing_source_nodes',missing])
    # The final merge must explicitly show all weighted final operands.
    final=text.split('Final solution:')[-1]
    final_num='+'.join(f'{w}*{v}' for w,v in zip(oracle['final_weights'],oracle['final_values']) if w)
    merge=False
    # A correct equality chain may simplify weighted products before its last side.
    for line in final.replace('\\times','*').replace('\\cdot','*').replace('×','*').splitlines():
        parts=[p.strip().strip(' .;$') for p in line.split('=')]
        if not parts or parts[-1]!=str(oracle['answer']):continue
        for part in parts[:-1]:
            if not re.fullmatch(r'[\d+*()\s-]+',part):
                suffix=re.search(r'(?:^|[^A-Za-z0-9_])([\d+*()\s-]+)$',part)
                if not suffix:continue
                part=suffix[1].strip()
            try:merge=merge or numeric_signature(part)==numeric_signature(final_num)
            except (ValueError,SyntaxError):pass
    if not merge:failures.append(['final_weighted_merge_unproven'])
    return dict(source_nodes=len(expected),relations_checked=len(receipts),receipts=receipts,failures=failures,
                round_dependencies=[dict(source_round=a,target_round=b) for a,b in sorted(deps)],
                limitations='Conservative explicit AST proof; independent substantive review still checks narrative scheduling and meaning.')
